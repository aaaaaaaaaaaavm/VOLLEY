#!/usr/bin/env python3
"""Exact pairwise B-rep interference census for controlled Gen5 and unselected R1.

The aggregate App::Part assembly shape is deliberately excluded because it
duplicates its children and would create misleading overlap pairs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App

CAD = Path(__file__).resolve().parent
INPUTS = {
    "evaluated_gen5": CAD / "native/Gen5_Review.FCStd",
    "unselected_wide_r1": CAD / "native/Feeder_Candidate_R1.FCStd",
}
OUT = CAD / "GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json"


def main():
    result = {
        "method": "FreeCAD 1.0 exact Part B-rep common-volume for every named leaf-solid pair",
        "classification_note": "A nonzero intersection is a geometric conflict or proxy overlap, not by itself a load/flight failure. Every pair needs contact and part-definition disposition.",
        "models": {},
    }
    for key, path in INPUTS.items():
        doc = App.openDocument(str(path))
        leaves = [o for o in doc.Objects if hasattr(o, "Shape") and
                  o.TypeId != "App::Part" and not o.Shape.isNull() and
                  o.Shape.Volume > 0]
        pairs = []
        for i, a in enumerate(leaves):
            for b in leaves[i + 1:]:
                if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):
                    continue
                volume = a.Shape.common(b.Shape).Volume
                if volume > 1e-4:
                    pairs.append({"part_a": a.Name, "part_b": b.Name,
                                  "intersection_mm3": round(volume, 3)})
        result["models"][key] = {
            "source": str(path.relative_to(CAD)),
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "leaf_solid_count": len(leaves),
            "nonzero_pair_count": len(pairs),
            "intersections": sorted(pairs, key=lambda x: -x["intersection_mm3"]),
        }
        App.closeDocument(doc.Name)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v["nonzero_pair_count"] for k, v in result["models"].items()}))


if __name__ == "__main__":
    main()
