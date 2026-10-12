#!/usr/bin/env python3
"""Independently inspect exported integration STEP compounds for solid overlap."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD  # load FreeCAD runtime before Part
import Part

OUT = Path(__file__).resolve().parent / "release"


def main():
    rows = []
    for path in sorted(OUT.glob("Gen6_Integrated_R2_*.step")):
        shape = Part.Shape()
        shape.read(str(path))
        solids = shape.Solids
        collisions = []
        for i, a in enumerate(solids):
            for j in range(i + 1, len(solids)):
                b = solids[j]
                if a.BoundBox.intersect(b.BoundBox):
                    volume = a.common(b).Volume
                    if volume > 1e-4:
                        collisions.append({"solid_a": i, "solid_b": j,
                                           "intersection_mm3": round(volume, 6)})
        rows.append({"step": path.name,
                     "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                     "solid_count": len(solids), "shape_valid": shape.isValid(),
                     "solid_intersections": collisions})
    if len(rows) != 4 or any(not r["shape_valid"] or r["solid_count"] != 27
                             or r["solid_intersections"] for r in rows):
        raise AssertionError("STEP state readback or nominal collision check failed")
    report = {"status": "FOUR_NOMINAL_STATES_PASS_STEP_READBACK_ONLY",
              "method": "FreeCAD 1.0 STEP readback and exact pairwise solid common-volume check",
              "states": rows,
              "not_verified": ["motion between states", "manufacturing tolerances",
                               "contact loads", "launch restraint", "four-cell layout"]}
    (OUT / "Gen6_Integrated_R2_STEP_Verification.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps({"states": len(rows), "collisions": 0}))


if __name__ == "__main__":
    main()
