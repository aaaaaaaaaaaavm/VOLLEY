"""Independent CadQuery/OCC readback of FreeCAD STEP assemblies and parts."""

from pathlib import Path
import hashlib, json
import cadquery as cq

H = Path(__file__).resolve().parent
out = []
for r in json.loads((H / "CAD_EXCHANGE.json").read_text())["poses"]:
    name = next(n for n in r["files"] if n.endswith(".step"))
    p = H / name
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r["files"][name]
    shape = cq.importers.importStep(str(p)).val()
    assert shape.isValid() and len(shape.Solids()) == r["components"]
    assert abs(shape.Volume() - r["source_volume_mm3"]) < 0.01
    out.append(
        {
            "file": name,
            "valid": True,
            "solids": len(shape.Solids()),
            "volume_difference_mm3": shape.Volume() - r["source_volume_mm3"],
        }
    )
parts = []
for r in json.loads((H / "parts/INDEX.json").read_text())["parts"]:
    p = H / r["file"]
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256"]
    s = cq.importers.importStep(str(p)).val()
    assert (
        s.isValid()
        and len(s.Solids()) == 1
        and abs(s.Volume() - r["volume_mm3"]) < 0.001
    )
    parts.append(
        {
            "file": r["file"],
            "valid": True,
            "volume_difference_mm3": s.Volume() - r["volume_mm3"],
        }
    )
(H / "INDEPENDENT_STEP.json").write_text(
    json.dumps(
        {
            "software": "CadQuery 2.8.0 / OpenCascade 7.9.3.1",
            "assemblies": out,
            "parts": parts,
            "boundary": "Independent nominal geometry exchange check; no operational or manufacturing acceptance.",
        },
        indent=2,
    )
    + "\n"
)
print(len(out), "assemblies and", len(parts), "parts independently checked")
