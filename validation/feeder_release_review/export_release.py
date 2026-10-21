"""Release native single-cell geometry and individual neutral STEP exchanges."""

from pathlib import Path
import csv, hashlib, json
import FreeCAD as App
import Part
from mechanism import shapes, cycle, REVISION
import sys, traceback

sys.excepthook = lambda t, v, tb: traceback.print_exception(
    t, v, tb, file=sys.__stderr__
)
H = Path(__file__).resolve().parent
O = H / "cad"
O.mkdir(exist_ok=True)
P = H / "parts"
P.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
density = {"aluminium": 2700, "steel": 7850, "polymer": 1200, "catalogue": 1400}
audit = json.loads((H / "GEOMETRY_AUDIT.json").read_text())
assert audit["CAD_source_sha256"] == sha(H / "mechanism.py")
assert all(
    not r["invalid"] and not r["collisions"]
    for c in audit["configurations"]
    for r in c["checks"]
)
records = []
parts = []
ledgers = []
selected = {
    "stored",
    "transfer",
    "sled_captured",
    "fork_home",
    "exit_unlocked",
    "exit_open",
    "payload_clear",
    "empty_carrier_home",
    "exit_locked",
    "ready_empty",
}
for size, L in [("1U", 113.5), ("3U", 340.5)]:
    for phase, state in cycle(L):
        if phase not in selected:
            continue
        ss, meta = shapes(L, state)
        ss = {n: s.Solids[0] for n, s in ss.items()}
        doc = App.newDocument("FM07")
        for n, shape in ss.items():
            ob = doc.addObject("Part::Feature", "Component")
            ob.Label = n
            ob.Shape = shape
            ob.addProperty("App::PropertyString", "MaterialBasis").MaterialBasis = meta[
                n
            ][0]
            ob.addProperty("App::PropertyString", "ModelRole").ModelRole = meta[n][1]
        doc.Label = "VOLLEY " + REVISION + " " + size + " " + phase
        doc.recompute()
        native = O / ("FM07_" + size + "_" + phase + ".FCStd")
        step = native.with_suffix(".step")
        doc.saveAs(str(native))
        Part.export(doc.Objects, str(step))
        q = Part.read(str(step))
        v = sum(s.Volume for s in ss.values())
        assert q.isValid() and len(q.Solids) == len(ss) and abs(q.Volume - v) < 0.001
        records.append(
            {
                "size": size,
                "pose": phase,
                "components": len(ss),
                "valid": q.isValid(),
                "source_volume_mm3": v,
                "STEP_volume_difference_mm3": q.Volume - v,
                "files": {p.relative_to(H).as_posix(): sha(p) for p in [native, step]},
            }
        )
        if phase != "stored":
            App.closeDocument(doc.Name)
            continue
        masses = []
        for n, s in ss.items():
            p = P / ("FM07_" + size + "_" + n + ".step")
            s.exportStep(str(p))
            part = {
                "size": size,
                "name": n,
                "file": p.relative_to(H).as_posix(),
                "sha256": sha(p),
                "volume_mm3": s.Volume,
                "CG_mm": list(s.CenterOfMass),
                "material_basis": meta[n][0],
                "role": meta[n][1],
            }
            parts.append(part)
            if n == "payload":
                continue
            rho = density.get(meta[n][0])
            assert rho is not None, (n, meta[n])
            mass = 0.179 if n == "motor_3242_envelope" else s.Volume * 1e-9 * rho
            rho = mass / (s.Volume * 1e-9)
            masses.append(
                (
                    mass,
                    list(s.CenterOfMass),
                    [
                        [
                            getattr(s.MatrixOfInertia, "A" + str(i + 1) + str(j + 1))
                            for j in range(3)
                        ]
                        for i in range(3)
                    ],
                    rho,
                )
            )
        print("Mass ledger rows", len(masses), flush=True)
        m = sum(r[0] for r in masses)
        cg = [sum(r[0] * r[1][i] for r in masses) / m for i in range(3)]
        print("CG computed", cg, flush=True)
        inertia = [[0.0] * 3 for _ in range(3)]
        for mi, com, I, rho in masses:
            d = [com[i] - cg[i] for i in range(3)]
            for i in range(3):
                for j in range(3):
                    inertia[i][j] += I[i][j] * rho * 1e-15 + mi * 1e-6 * (
                        (sum(x * x for x in d) if i == j else 0) - d[i] * d[j]
                    )
        boxes = [s.BoundBox for n, s in ss.items() if n != "payload"]
        bounds = [
            min(getattr(b, k + "Min") for b in boxes) for k in ["X", "Y", "Z"]
        ] + [max(getattr(b, k + "Max") for b in boxes) for k in ["X", "Y", "Z"]]
        ledgers.append(
            {
                "size": size,
                "modeled_material_mass_kg": m,
                "CG_mm": cg,
                "inertia_about_CG_kg_m2": inertia,
                "bounding_box_mm": bounds,
                "density_kg_m3": density,
                "boundary": "Nominal modeled material plus declared component-envelope mass proxies; payload excluded. Motor uses its catalogue 0.179 kg, other catalogue envelopes assume 1400 kg/m3. Envelope inertia is approximate. Catalogue actuator, brake, bearing internals, sensors, harness, power electronics and host mounting hardware are not fully modeled. No installed-system mass claim.",
            }
        )
        App.closeDocument(doc.Name)
    print(size, "exported", flush=True)
(H / "CAD_EXCHANGE.json").write_text(
    json.dumps(
        {
            "revision": REVISION,
            "software": {
                "FreeCAD": ".".join(App.Version()[:3]),
                "OpenCascade": Part.OCC_VERSION,
            },
            "poses": records,
            "source_sha256": sha(H / "mechanism.py"),
        },
        indent=2,
    )
    + "\n"
)
(P / "INDEX.json").write_text(
    json.dumps({"revision": REVISION, "parts": parts}, indent=2) + "\n"
)
(H / "METROLOGY.json").write_text(
    json.dumps({"revision": REVISION, "configurations": ledgers}, indent=2) + "\n"
)
print("Assemblies", len(records), "parts", len(parts), flush=True)
