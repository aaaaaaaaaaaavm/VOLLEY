#!/usr/bin/env python3
"""Cross-check the existing feeder states against the original first-article CAD."""
from __future__ import annotations

import json
from pathlib import Path

import FreeCAD as App

CAD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "release" / "Original_Cross_Assembly_Interference.json"
FILES = {
    "feeder_armed": CAD / "gen6_feeder/release/Gen6_Feed_01_transfer_armed.FCStd",
    "feeder_mid": CAD / "gen6_feeder/release/Gen6_Feed_02_mid_transfer.FCStd",
    "feeder_seated": CAD / "gen6_feeder/release/Gen6_Feed_03_seated.FCStd",
    "article_A": CAD / "gen6_first_article/release/Gen6_G1_A_Envelope.FCStd",
    "article_B": CAD / "gen6_first_article/release/Gen6_G1_B_Envelope.FCStd",
}


def main():
    docs = {k: App.openDocument(str(p)) for k, p in FILES.items()}
    parts = {k: [o for o in d.Objects if o.TypeId == "Part::Box" and not o.Shape.isNull()]
             for k, d in docs.items()}
    cross = {}
    for feeder in ("feeder_armed", "feeder_mid", "feeder_seated"):
        for article in ("article_A", "article_B"):
            pairs = []
            for a in parts[feeder]:
                for b in parts[article]:
                    if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):
                        continue
                    v = a.Shape.common(b.Shape).Volume
                    if v > 1e-4:
                        pairs.append({"feeder": a.Name, "article": b.Name,
                                      "intersection_mm3": round(v, 3)})
            cross[feeder + "__" + article] = sorted(
                pairs, key=lambda x: -x["intersection_mm3"])
    result = {
        "status": "ORIGINAL_SEPARATE_STUDIES_NOT_AN_INTEGRATED_ASSEMBLY",
        "method": "FreeCAD 1.0 exact Part B-rep intersections of all Part::Box pairs",
        "input_files": {k: str(p.relative_to(CAD)) for k, p in FILES.items()},
        "part_counts": {k: len(v) for k, v in parts.items()},
        "cross_intersections": cross,
        "interpretation": [
            "The duplicate seated 3U boxes represent one intended spacecraft and are not two real parts.",
            "Some lip/cradle and guide pairs represent alternative proxies for one intended part.",
            "Bridge/guide, mid-transfer payload/guide and end-stop/carrier intersections show that the independently passing studies cannot be combined unchanged.",
            "Zero-volume face contact, moving loads, tolerances, deformations and actual host mounts are outside this screen.",
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: len(v) for k, v in cross.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
