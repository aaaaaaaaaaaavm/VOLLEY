"""Read exchange files back and discretize actual STEP curves for figures."""

from pathlib import Path
import hashlib, json
import FreeCAD as App
import Part

H = Path(__file__).parent
data = []
for p in sorted((H / "cad").glob("FM02_3U_*.step")):
    s = Part.read(str(p))
    assert s.isValid()
    data.append(
        dict(
            file=p.name,
            sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            edges=[
                [[v.x, v.y, v.z] for v in e.discretize(Deflection=0.3)] for e in s.Edges
            ],
        )
    )
(H / "cad/STEP_EDGES.json").write_text(json.dumps(data, separators=(",", ":")) + "\n")
p = H / "cad/FM02_3U_transfer.FCStd"
doc = App.openDocument(str(p))
detail = {}
for ob in doc.Objects:
    if ob.Label in ["storage_gate", "gate_crossbolt", "gate_bolt_guide", "fork_body"]:
        detail[ob.Label] = [
            [[v.x, v.y, v.z] for v in e.discretize(Deflection=0.1)]
            for e in ob.Shape.Edges
        ]
App.closeDocument(doc.Name)
(H / "cad/INTERLOCK_EDGES.json").write_text(
    json.dumps(
        dict(
            source=p.name,
            sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            parts=detail,
        ),
        separators=(",", ":"),
    )
    + "\n"
)
print(len(data), "real STEP readback views and native interlock detail")
