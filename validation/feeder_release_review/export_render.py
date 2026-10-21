"""Export actual nominal FreeCAD geometry for identified technical renders."""

from pathlib import Path
import json, hashlib
import FreeCAD as App
from mechanism import shapes, cycle, REVISION

H = Path(__file__).resolve().parent
O = H / "render_meshes"
O.mkdir(exist_ok=True)
rows = []
for phase, state in cycle(340.5):
    if phase not in ["stored", "transfer", "exit_open", "empty_carrier_home"]:
        continue
    ss, _ = shapes(340.5, state)
    parts = []
    for n, s in ss.items():
        vertices, faces = s.tessellate(0.08)
        p = O / (phase + "_" + n + ".obj")
        with p.open("w") as f:
            for v in vertices:
                f.write(
                    "v %.10g %.10g %.10g\n" % (v.x * 0.001, v.y * 0.001, v.z * 0.001)
                )
            for face in faces:
                f.write("f %d %d %d\n" % tuple(i + 1 for i in face))
        parts.append(
            {
                "name": n,
                "file": p.name,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            }
        )
    source = H / "cad" / ("FM07_3U_" + phase + ".FCStd")
    rows.append(
        {
            "phase": phase,
            "source": source.name,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "parts": parts,
        }
    )
(O / "MESHES.json").write_text(
    json.dumps(
        {
            "revision": REVISION,
            "source_sha256": hashlib.sha256(
                (H / "mechanism.py").read_bytes()
            ).hexdigest(),
            "tessellation_mm": 0.08,
            "evidence_class": "Native CAD meshes for labeled visualization; no solver or hardware evidence",
            "poses": rows,
        },
        indent=2,
    )
    + "\n"
)
print("Exported four actual CAD states")
