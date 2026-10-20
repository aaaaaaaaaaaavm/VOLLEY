"""Independent CadQuery/OCC7.9 exchange readback of FreeCAD/OCC7.8 exports."""

from pathlib import Path
import json, hashlib
import cadquery as cq

H = Path(__file__).parent
r = json.loads((H / "cad/NATIVE_CAD.json").read_text())
out = []
for pose in r["poses"]:
    filename = next(x for x in pose["files"] if x.endswith(".step"))
    p = H / "cad" / filename
    assert hashlib.sha256(p.read_bytes()).hexdigest() == pose["files"][filename]
    shape = cq.importers.importStep(str(p)).val()
    assert shape.isValid() and len(shape.Solids()) == pose["component_solids"], filename
    assert abs(shape.Volume() - pose["source_volume_mm3"]) < 0.01, filename
    # Native result records total volume by export, not only solid count.
    out.append(
        dict(
            file=filename,
            valid=True,
            solids=len(shape.Solids()),
            volume_mm3=shape.Volume(),
        )
    )
(H / "cad/INDEPENDENT_STEP.json").write_text(
    json.dumps(
        dict(
            software="CadQuery2.8.0/OpenCascade7.9",
            cases=out,
            boundary="Independent exchange topology readback; not a tolerance, material or operational certification.",
        ),
        indent=2,
    )
    + "\n"
)
print(len(out), "STEP files independently valid with expected solid counts")
