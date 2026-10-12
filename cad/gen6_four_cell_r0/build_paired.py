#!/usr/bin/env python3
"""Same-boundary paired-side challenger to the staggered four-cell study."""
import hashlib
import json
from pathlib import Path

import build

HERE = Path(__file__).resolve().parent
build.OUT = HERE / "release_paired"
build.CELLS = (
    ("A_3U", 170.0, 340.5, -1),
    ("B_3U", 170.0, 340.5, 1),
    ("C_1U", 550.0, 113.5, -1),
    ("D_1U", 550.0, 113.5, 1),
)
build.main()
path = build.OUT / "Four_Cell_R0_Report.json"
report = json.loads(path.read_text())
report["variant"] = "PAIRED_OPPOSITE_SIDE_CELLS"
report["variant_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
path.write_text(json.dumps(report, indent=2)+"\n")
