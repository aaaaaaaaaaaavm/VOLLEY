"""Retain a fuel-reserve countercase instead of declaring a spring mission impossible."""

from pathlib import Path
import json
from run import construct

H = Path(__file__).resolve().parent
rows = []
for strategy in ["spring", "volley_3_6", "volley_unrestricted"]:
    try:
        d = construct(12, strategy, initial_fuel=20)
        rows.append(d)
        print(
            strategy,
            d["fuel_used_kg"],
            d["initial_device_plus_loaded_fuel_kg"],
            flush=True,
        )
    except RuntimeError as e:
        rows.append(
            {"count": 12, "strategy": strategy, "status": "FAILED", "reason": str(e)}
        )
(H / "release/RESERVE_CASES.json").write_text(
    json.dumps(
        {
            "boundary": "20kg initial fuel for all12-payload alternatives; ideal constructed mission, not optimized or customer-specific. CSV filenames identify initial fuel and maximum integrator step.",
            "cases": rows,
        },
        indent=2,
    )
    + "\n"
)
