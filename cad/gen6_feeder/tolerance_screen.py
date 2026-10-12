#!/usr/bin/env python3
"""Transparent assumed interval screen, not a controlled drawing tolerance release."""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = json.loads((HERE / "parameters.json").read_text())

# Assumed perturbations for a research sensitivity screen only. They are not
# sourced manufacturing tolerances, provider interface limits or flight margins.
assumed_mm = {
    "payload_width_plus": 1.0,
    "payload_length_plus": 1.0,
    "payload_height_plus": 1.0,
    "payload_lateral_shift": 0.5,
    "guide_inward_shift": 0.5,
    "payload_axial_shift": 1.0,
    "stop_inward_shift": 1.0,
    "gate_vertical_error": 2.0,
    "payload_vertical_shift": 1.0,
}
side_nom = p["nominal_cradle_side_gap_mm"]
side_worst = side_nom - (assumed_mm["payload_width_plus"] / 2
                         + assumed_mm["payload_lateral_shift"]
                         + assumed_mm["guide_inward_shift"])
axial_nom = p["nominal_end_stop_gap_mm"]
axial_worst = axial_nom - (assumed_mm["payload_length_plus"] / 2
                           + assumed_mm["payload_axial_shift"]
                           + assumed_mm["stop_inward_shift"])
gate_nom = p["gate_lift_mm"] - p["payload_height_mm"]
gate_worst = gate_nom - (assumed_mm["payload_height_plus"]
                         + assumed_mm["gate_vertical_error"]
                         + assumed_mm["payload_vertical_shift"])
report = {
    "evidence_class": "ASSUMED_INTERVAL_SENSITIVITY_NOT_DRAWING_TOLERANCE",
    "inputs_assumed_mm": assumed_mm,
    "results_mm": {
        "cradle_side_nominal": side_nom,
        "cradle_side_worst_under_assumptions": side_worst,
        "end_stop_nominal": axial_nom,
        "end_stop_worst_under_assumptions": axial_worst,
        "lifted_gate_over_payload_nominal": gate_nom,
        "lifted_gate_over_payload_worst_under_assumptions": gate_worst,
    },
    "exclusions": ["thermal growth", "launch deflection", "backlash", "joint wear",
                   "actual spacecraft rail/contact tolerance", "actuator positioning evidence",
                   "dynamic contact and jam force", "four-cell alignment"],
}
if min(report["results_mm"].values()) <= 0:
    raise AssertionError("nonpositive illustrative clearance")
out = HERE / "release" / "Gen6_Feed_Assumed_Tolerance_Screen.json"
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report["results_mm"], sort_keys=True))
