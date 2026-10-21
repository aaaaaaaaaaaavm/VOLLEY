"""FM-06 exact-solid inspection. Failed cases are retained; no forced pass."""

from pathlib import Path
import itertools, json, hashlib, time
import FreeCAD as App
import Part
from mechanism import shapes, cycle, interpolate, REVISION

H = Path(__file__).parent
O = H / "cad"
O.mkdir(exist_ok=True)


def hits(ss):
    out = []
    for (a, sa), (b, sb) in itertools.combinations(ss.items(), 2):
        if sa.BoundBox.intersect(sb.BoundBox):
            v = sa.common(sb).Volume
            if v > 1e-5:
                out.append({"parts": [a, b], "mm3": v})
    return out


report = {
    "revision": REVISION,
    "software": {
        "FreeCAD": ".".join(App.Version()[:3]),
        "OpenCascade": Part.OCC_VERSION,
    },
    "poses": [],
    "motion": [],
}
for label, L in [("1U", 113.5), ("3U", 340.5)]:
    phases = cycle()
    for phase, s in phases:
        ss, meta = shapes(L, s)
        bad = [
            {"part": n, "valid": sh.isValid(), "solids": len(sh.Solids)}
            for n, sh in ss.items()
            if not sh.isValid() or len(sh.Solids) != 1
        ]
        hh = hits(ss)
        print(label, phase, "hits", len(hh), "bad", bad, flush=True)
        if hh:
            print(hh[:10], flush=True)
        doc = App.newDocument("FM06")
        for n, sh in ss.items():
            ob = doc.addObject("Part::Feature", "Component")
            ob.Label = n
            ob.Shape = sh
            ob.addProperty("App::PropertyString", "MaterialBasis").MaterialBasis = meta[
                n
            ][0]
            ob.addProperty("App::PropertyString", "ModelRole").ModelRole = meta[n][1]
        stem = "FM06_" + label + "_" + phase
        native = O / (stem + ".FCStd")
        step = O / (stem + ".step")
        doc.Label = "VOLLEY FM-06 - " + label + " " + phase.replace("_", " ")
        doc.recompute()
        doc.saveAs(str(native))
        Part.export(doc.Objects, str(step))
        read = Part.read(str(step))
        report["poses"].append(
            {
                "payload": label,
                "phase": phase,
                "invalid_parts": bad,
                "penetrations": hh,
                "step_valid": read.isValid(),
                "step_solids": len(read.Solids),
                "component_solids": sum(len(x.Solids) for x in ss.values()),
                "source_volume_mm3": sum(x.Volume for x in ss.values()),
                "step_volume_error_mm3": read.Volume
                - sum(x.Volume for x in ss.values()),
                "files": {
                    p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [native, step]
                },
            }
        )
        App.closeDocument(doc.Name)
    for i in range(len(phases) - 1):
        for f in [0.25, 0.5, 0.75]:
            ss, meta = shapes(L, interpolate(phases[i][1], phases[i + 1][1], f))
            report["motion"].append(
                {
                    "payload": label,
                    "phase": phases[i + 1][0],
                    "fraction": f,
                    "penetrations": hits(ss),
                }
            )
report["boundary"] = (
    "Prescribed motion and exact-solid samples, not continuous contact dynamics, actual actuator ratings, real toleranced joints or hardware validation."
)
(O / "NATIVE_CAD.json").write_text(json.dumps(report, indent=2) + "\n")
print(
    "Total pose collision pairs",
    sum(len(x["penetrations"]) for x in report["poses"]),
    "motion",
    sum(len(x["penetrations"]) for x in report["motion"]),
    flush=True,
)
