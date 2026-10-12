#!/usr/bin/env python3
"""Compare two nominally verified four-cell placements on the same rail."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
rows = []
for name, folder in (("staggered", "release"), ("paired", "release_paired")):
    report = json.loads((HERE/folder/"Four_Cell_R0_Report.json").read_text())
    verify = json.loads((HERE/folder/"Four_Cell_R0_STEP_Verification.json").read_text())
    cells = report["cells"]
    assert len(cells) == 4 and len(report["states"]) == len(verify["states"]) == 13
    assert all(not x["overlaps"] for x in report["states"])
    rows.append(dict(layout=name, cell_group_x_min_mm=min(c["x_mm"] for c in cells),
                     cell_group_x_max_mm=max(c["x_mm"]+c["length_mm"] for c in cells),
                     shortest_drive_travel_mm=min(c["available_drive_travel_mm"] for c in cells),
                     greatest_ideal_mean_g_for_6_m_s=max(c["ideal_mean_g_for_6_m_s"] for c in cells),
                     lateral_span_mm=report["lateral_outermost_y_mm"][1]-report["lateral_outermost_y_mm"][0],
                     nominal_states=len(report["states"]), verified_step_states=len(verify["states"])))
comparison = dict(status="NOMINAL_PACKAGING_COMPARISON_NOT_ARCHITECTURE_SELECTION",
                  same_boundaries=["1800 mm rail", "x=1450 mm modeled brake start",
                                   "two 3U and two 1U passive boxes", "two fixed cassette sides"],
                  variants=rows, remaining=["host accommodation", "independent payload restraints",
                    "cell-select/shot carrier positioning", "bridge/guide sequencing",
                    "actuator and energy source", "loads and tolerances", "installed mass/CG/inertia",
                    "common-fault analysis and physical reliability"])
(HERE/"Four_Cell_Layout_Comparison.json").write_text(json.dumps(comparison, indent=2)+"\n")
print(json.dumps(rows))
