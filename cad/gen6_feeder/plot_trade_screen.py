"""Plot the provisional ordinal trade; bars are not measured performance."""
import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / "release" / "Gen6_Feeder_Provisional_Trade.json").read_text())["results"]
labels = [r["candidate"].replace("Fixed-cell ", "").replace("Geneva ", "") for r in rows]
value = [r["nominal_ordinal_score_of_5"] for r in rows]
left = [v-r["one_point_interval_of_5"][0] for v, r in zip(value, rows)]
right = [r["one_point_interval_of_5"][1]-v for v, r in zip(value, rows)]
fig, ax = plt.subplots(figsize=(10.5, 5.6), layout="constrained")
ax.errorbar(value, range(len(rows)), xerr=[left, right], fmt="o", capsize=4,
            color="#0e5a75", ecolor="#8497a5", markersize=8, linewidth=2)
ax.set_yticks(range(len(rows)), labels)
ax.invert_yaxis()
ax.set_xlim(1, 5)
ax.set_xlabel("Weighted ordinal hypothesis (1 unfavorable, 5 favorable)")
ax.set_title("Gen6 feeder provisional comparison — no architecture selected")
ax.grid(axis="x", alpha=0.25)
fig.text(0.01, 0.01,
         "Ranges vary every unmeasured criterion by ±1 point. They are sensitivity bounds, not confidence intervals.",
         fontsize=9, color="#475569")
for suffix in ("svg", "png"):
    fig.savefig(ROOT / "release" / f"Gen6_Feeder_Provisional_Trade.{suffix}", dpi=180)
