#!/usr/bin/env python3
"""Tessellate the saved FreeCAD native boxes for an explicitly CAD-derived render.

Run with /usr/bin/python3 and PYTHONPATH=/usr/lib/freecad-python3/lib.
The OBJ mesh files are temporary render inputs; STEP and FCStd are the geometry record.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parent
OUT = Path("/tmp/volley_gen6_go2_meshes")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    manifest = {"method": "FreeCAD 1.0 native Part::Box B-rep tessellation to OBJ for Blender review",
                "candidates": {}}
    for kind in ("A", "B"):
        native = ROOT / "release" / f"Gen6_G1_{kind}_Envelope.FCStd"
        step = ROOT / "release" / f"Gen6_G1_{kind}_Envelope.step"
        doc = App.openDocument(str(native))
        entries = []
        for obj in doc.Objects:
            if obj.TypeId != "Part::Box":
                continue
            vertices, triangles = obj.Shape.tessellate(0.7)
            output = OUT / f"{kind}_{obj.Name}.obj"
            with output.open("w") as f:
                f.write(f"# FreeCAD tessellation of {obj.Name}; STEP {sha(step)}\n")
                f.write(f"o {obj.Name}\n")
                for v in vertices:
                    f.write(f"v {v.x:.6f} {v.y:.6f} {v.z:.6f}\n")
                for triangle in triangles:
                    f.write("f " + " ".join(str(i+1) for i in triangle) + "\n")
            entries.append(dict(name=obj.Name, obj=output.name, sha256=sha(output),
                                bounds_mm=[obj.Shape.BoundBox.XMin,obj.Shape.BoundBox.XMax,
                                           obj.Shape.BoundBox.YMin,obj.Shape.BoundBox.YMax,
                                           obj.Shape.BoundBox.ZMin,obj.Shape.BoundBox.ZMax]))
        manifest["candidates"][kind] = dict(native_sha256=sha(native), step_sha256=sha(step), parts=entries)
        App.closeDocument(doc.Name)
    (OUT / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(OUT / "manifest.json")


if __name__ == "__main__":
    main()
