#!/usr/bin/env python3
"""Independent exact-solid pair census of exported four-cell STEP states."""
from pathlib import Path
import argparse
import hashlib
import json

import FreeCAD  # load runtime before Part
import Part

DEFAULT_OUT = Path(__file__).resolve().parent / "release"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, default=DEFAULT_OUT)
    out = parser.parse_args().release
    rows = []
    for path in sorted(out.glob("*.step")):
        shape = Part.Shape()
        shape.read(str(path))
        solids = shape.Solids
        overlaps = []
        for i, a in enumerate(solids):
            for j in range(i+1, len(solids)):
                b = solids[j]
                if a.BoundBox.intersect(b.BoundBox):
                    volume = a.common(b).Volume
                    if volume > 1e-4:
                        overlaps.append([i, j, round(volume, 5)])
        rows.append(dict(step=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                         solids=len(solids), shape_valid=shape.isValid(), overlaps=overlaps))
    expected = json.loads((out/"Four_Cell_R0_Report.json").read_text())["states"]
    by_name = {s["step"]: s for s in expected}
    if len(rows) != 13 or any(r["overlaps"] or not r["shape_valid"] or
                               r["step"] not in by_name or
                               r["solids"] != by_name[r["step"]]["parts"] or
                               r["sha256"] != by_name[r["step"]]["step_sha256"] for r in rows):
        raise AssertionError("STEP census disagrees with nominal builder report")
    result = dict(status="NOMINAL_STEP_READBACK_ONLY", states=rows,
                  exclusions=["continuous swept motion", "manufacturing tolerance",
                              "contact/load", "bridge/guide sequencing", "flight interface"])
    (out/"Four_Cell_R0_STEP_Verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"verified_states":len(rows), "overlap_pairs":0}))


if __name__ == "__main__":
    main()
