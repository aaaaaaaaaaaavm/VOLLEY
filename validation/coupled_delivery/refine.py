"""Time-step sensitivity of the same constructed campaign and failed fuel case."""

from pathlib import Path
import json
from run import construct

H = Path(__file__).resolve().parent
old = json.loads((H / "release/RESULTS.json").read_text())
rows = []
for c in old["cases"]:
    try:
        d = construct(c["count"], c["strategy"], step=30)
        rows.append(
            {
                "count": c["count"],
                "strategy": c["strategy"],
                "status": "COMPUTED",
                "fuel_change_kg": d["fuel_used_kg"] - c["fuel_used_kg"],
                "host_dv_change_m_s": d["total_host_dv_m_s"] - c["total_host_dv_m_s"],
                "maximum_terminal_position_residual_m": d[
                    "maximum_terminal_position_residual_m"
                ],
                "same_final_host_position_residual_m": d[
                    "same_final_host_position_residual_m"
                ],
                "all_conditional_clearance_screens_pass": all(
                    x.get("passes", x.get("passes_conditional_20m_screen", False))
                    for x in d["clearance"]
                ),
            }
        )
    except RuntimeError as e:
        rows.append(
            {
                "count": c["count"],
                "strategy": c["strategy"],
                "status": "FAILED",
                "reason": str(e),
            }
        )
    print(rows[-1], flush=True)
(H / "release/REFINEMENT.json").write_text(
    json.dumps(
        {
            "comparison": "60 to30s maximum DOP853 step; same solver, model and conditional bounds, not independent validation",
            "cases": rows,
        },
        indent=2,
    )
    + "\n"
)
