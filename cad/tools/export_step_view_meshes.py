"""Tessellate the controlled STEP parts for Blender presentation views.

Run with /usr/bin/python3, which has FreeCAD 1.0 on this workstation. The native
FreeCAD documents supply instance placement and source-file provenance; every
triangle is generated anew from the named STEP B-rep, never from old STL renders.
The temporary OBJ files are visualization intermediates, not released CAD.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/usr/lib/freecad-python3/lib")
import FreeCAD as App  # noqa: E402
import Part  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CAD = ROOT / "cad"
DOCUMENTS = {
    "gen5_reference": CAD / "native/Gen5_Review.FCStd",
    "r1_candidate": CAD / "native/Feeder_Candidate_R1.FCStd",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a: float, b: float, tolerance: float = 0.01) -> bool:
    return abs(a - b) <= tolerance


def write_obj(path: Path, vertices: list, triangles: list) -> None:
    with path.open("w") as handle:
        handle.write("# Display mesh tessellated from a VOLLEY STEP B-rep in FreeCAD 1.0\n")
        for vertex in vertices:
            handle.write(f"v {vertex.x:.7f} {vertex.y:.7f} {vertex.z:.7f}\n")
        for a, b, c in triangles:
            handle.write(f"f {a + 1} {b + 1} {c + 1}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("/tmp/volley-step-review-meshes"))
    parser.add_argument("--linear-deflection-mm", type=float, default=1.0)
    args = parser.parse_args()
    if args.linear_deflection_mm <= 0:
        parser.error("linear deflection must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    record = {"method": "FreeCAD Part.read STEP B-rep + tessellate; placements from native review document",
              "linear_deflection_mm": args.linear_deflection_mm, "configurations": {}}
    for config, document_path in DOCUMENTS.items():
        doc = App.openDocument(str(document_path))
        folder = args.output / config
        folder.mkdir(exist_ok=True)
        parts = []
        for feature in doc.Objects:
            if not getattr(feature, "SourceFile", None):
                continue
            source = CAD / feature.SourceFile
            if not source.is_file() or source.suffix.lower() != ".step":
                raise RuntimeError(f"missing source STEP for {feature.Name}: {source}")
            shape = Part.read(str(source))
            if shape.isNull() or not shape.isValid():
                raise RuntimeError(f"invalid STEP solid: {source}")
            shape.Placement = feature.Placement
            actual, expected = shape.BoundBox, feature.Shape.BoundBox
            bounds = ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax")
            if not close(shape.Volume, feature.Shape.Volume) or any(
                not close(getattr(actual, name), getattr(expected, name)) for name in bounds
            ):
                raise RuntimeError(f"STEP and native placement disagree: {feature.Name}")
            vertices, triangles = shape.tessellate(args.linear_deflection_mm)
            if not triangles:
                raise RuntimeError(f"empty mesh: {feature.Name}")
            destination = folder / f"{feature.Name}.obj"
            write_obj(destination, vertices, triangles)
            parts.append({
                "instance": feature.Name,
                "source_step": str(source.relative_to(ROOT)),
                "source_step_sha256": sha256(source),
                "obj_file": f"{config}/{feature.Name}.obj",
                "obj_sha256": sha256(destination),
                "source_volume_mm3": round(shape.Volume, 6),
                "triangle_count": len(triangles),
                "placed_bounds_mm": [round(getattr(actual, name), 4) for name in bounds],
            })
        if not parts:
            raise RuntimeError(f"no source-linked parts in {document_path}")
        record["configurations"][config] = {
            "native_document": str(document_path.relative_to(ROOT)),
            "native_document_sha256": sha256(document_path),
            "parts": parts,
        }
        App.closeDocument(doc.Name)
        print(f"{config}: {len(parts)} STEP-derived instances", flush=True)
    (args.output / "meshes.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"wrote {args.output / 'meshes.json'}")


if __name__ == "__main__":
    main()
