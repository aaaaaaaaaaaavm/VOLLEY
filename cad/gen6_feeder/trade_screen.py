"""Reproduce the provisional Gen6 feeder decision-matrix arithmetic.

Scores are ordinal expert hypotheses in input CSV, never measured reliability,
mass, power, volume or qualification. A ±1 score interval tests rank stability.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEIGHTS = {
    "fault_safety": 0.35,
    "fit_mass": 0.25,
    "positioning": 0.20,
    "cycle_power": 0.10,
    "manufacturability": 0.10,
}


def main():
    with (ROOT / "trade_screen_inputs.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for row in rows:
        scores = {key: float(row[key]) for key in WEIGHTS}
        assert all(1 <= value <= 5 for value in scores.values())
        nominal = sum(WEIGHTS[key] * scores[key] for key in WEIGHTS)
        low = sum(WEIGHTS[key] * max(1, scores[key] - 1) for key in WEIGHTS)
        high = sum(WEIGHTS[key] * min(5, scores[key] + 1) for key in WEIGHTS)
        out.append({
            "candidate": row["candidate"],
            "nominal_ordinal_score_of_5": round(nominal, 3),
            "one_point_interval_of_5": [round(low, 3), round(high, 3)],
            "physical_gates_passed": 0,
            "scores": scores,
        })
    out.sort(key=lambda item: item["nominal_ordinal_score_of_5"], reverse=True)
    (ROOT / "release" / "Gen6_Feeder_Provisional_Trade.json").write_text(
        json.dumps({
            "status": "ORDINAL_SCREEN_ONLY_NO_BASELINE_SELECTION",
            "weights": WEIGHTS,
            "score_meaning": "1 = unfavorable, 5 = favorable engineering hypothesis",
            "uncertainty": "Every unmeasured criterion varied by ±1 ordinal point, clipped to 1–5; not a statistical confidence interval",
            "physical_selection_gates": [
                "same-boundary four-cell 1U/3U CAD and STEP",
                "full motion and loaded/tolerance sweep",
                "positive power-off restraint and independent cell isolation",
                "installed mass, CG, inertia, actuator and cycle power",
                "launch/load, fault and recovery analysis",
            ],
            "results": out,
        }, indent=2) + "\n"
    )
    for item in out:
        print(item["candidate"], item["nominal_ordinal_score_of_5"], item["one_point_interval_of_5"])


if __name__ == "__main__":
    main()
