#!/usr/bin/env python3
"""Tessellate saved FreeCAD state solids for a STEP-derived Blender review."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import FreeCAD as App

HERE = Path(__file__).resolve().parent
OUT = Path("/tmp/volley_gen6_feeder_meshes")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=True)
    manifest = {"method": "FreeCAD native B-rep tessellation; corresponding STEP volume checked in build.py", "states": {}}
    for name in ("00_stowed", "01_transfer_armed", "02_mid_transfer", "03_seated"):
        native = HERE / "release" / f"Gen6_Feed_{name}.FCStd"
        step = HERE / "release" / f"Gen6_Feed_{name}.step"
        doc = App.openDocument(str(native))
        parts = []
        for obj in doc.Objects:
            if obj.TypeId != "Part::Box":
                continue
            vertices, triangles = obj.Shape.tessellate(0.7)
            output = OUT / f"{name}_{obj.Name}.obj"
            with output.open("w") as f:
                f.write(f"# FreeCAD tessellation; corresponding STEP sha256 {sha(step)}\n")
                f.write(f"o {obj.Name}\n")
                for v in vertices:
                    f.write(f"v {v.x:.6f} {v.y:.6f} {v.z:.6f}\n")
                for t in triangles:
                    f.write("f " + " ".join(str(i + 1) for i in t) + "\n")
            b = obj.Shape.BoundBox
            parts.append({"name": obj.Name, "obj": output.name, "sha256": sha(output),
                          "bounds_mm": [b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax]})
        manifest["states"][name] = {"native_sha256": sha(native), "step_sha256": sha(step), "parts": parts}
        App.closeDocument(doc.Name)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(OUT / "manifest.json")

if __name__ == "__main__":
    main()
