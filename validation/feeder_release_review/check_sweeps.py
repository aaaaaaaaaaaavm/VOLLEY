"""Continuous rigid translation nonpenetration proof for the prescribed cycle.

The sweep of a compact solid under translation is covered by its initial solid
and the prisms of every boundary face. Pair checks use relative translation,
so jointly translating parts are not falsely swept against stationary copies.
This does not address flexible motion, finite tolerances or actual constraints.
"""

from pathlib import Path
import itertools, json, hashlib
import FreeCAD as App
import Part
from mechanism import shapes, cycle, REVISION

H = Path(__file__).parent


def volume(a, b):
    return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0.0


def offset(a, b):
    ca = a.BoundBox.Center
    cb = b.BoundBox.Center
    return App.Vector(cb.x - ca.x, cb.y - ca.y, cb.z - ca.z)


records = []
for label, L in [("1U", 113.5), ("3U", 340.5)]:
    phases = cycle(L)
    for (old, st), (name, en) in zip(phases, phases[1:]):
        if st.exit_gate_deg != en.exit_gate_deg:
            continue  # Rotary phases have a separate sampled audit.
        before, _ = shapes(L, st)
        after, _ = shapes(L, en)
        speeds = {}
        for n, sh in before.items():
            v = offset(sh, after[n])
            moved = sh.copy()
            moved.translate(v)
            # Establish the rigid-translation premise using exact overlap,
            # not only a matching endpoint bounding box.
            err = abs(moved.Volume - after[n].Volume) + abs(
                moved.Volume - volume(moved, after[n])
            )
            assert err < 0.01, (label, name, n, err)
            speeds[n] = v
        cache = {}
        penetrations = []
        pair_count = 0
        prisms_tested = 0
        for (a, sa), (b, sb) in itertools.combinations(before.items(), 2):
            rel = speeds[a] - speeds[b]
            if rel.Length < 1e-7:
                v = volume(sa, sb)
                if v > 1e-5:
                    penetrations.append(
                        dict(parts=[a, b], component="fixed_relative", mm3=v)
                    )
                continue
            # Bounding swept box is a broad phase only; exact prisms decide.
            end = sa.copy()
            end.translate(rel)
            broad = App.BoundBox(sa.BoundBox)
            broad.add(end.BoundBox)
            if not broad.intersect(sb.BoundBox):
                continue
            pair_count += 1
            key = (a, round(rel.x, 7), round(rel.y, 7), round(rel.z, 7))
            if key not in cache:
                pieces = [sa, end]
                for face in sa.Faces:
                    prism = face.extrude(rel)
                    if abs(prism.Volume) > 1e-8:
                        if prism.Volume < 0:
                            prism.reverse()
                        assert prism.isValid(), (label, name, a)
                        pieces.append(prism)
                cache[key] = pieces
            for j, p in enumerate(cache[key]):
                if not p.BoundBox.intersect(sb.BoundBox):
                    continue
                prisms_tested += 1
                v = volume(p, sb)
                if v > 1e-5:
                    penetrations.append(
                        dict(parts=[a, b], component="boundary_prism_" + str(j), mm3=v)
                    )
                    break
        records.append(
            dict(
                payload=label,
                phase=name,
                rigid_translation_checked=True,
                relative_pairs=pair_count,
                exact_prism_tests=prisms_tested,
                penetrations=penetrations,
            )
        )
        print(
            label,
            name,
            "pairs",
            pair_count,
            "prisms",
            prisms_tested,
            "penetrations",
            len(penetrations),
            flush=True,
        )
out = dict(
    revision=REVISION,
    method="Initial solid plus exact boundary-face translation prisms; relative motion; endpoint shape overlap establishes translation premise.",
    cases=records,
    total_penetrations=sum(len(x["penetrations"]) for x in records),
    source_sha256={
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [H / "mechanism.py", Path(__file__)]
    },
    boundary="Nominal prescribed rigid translations only. FreeCAD/OCC numerical thresholds are not a manufacturing clearance. No actual joint constraint, force, tolerance, flex, wear or reliability proof.",
)
(H / "CONTINUOUS_SWEEPS.json").write_text(json.dumps(out, indent=2) + "\n")
