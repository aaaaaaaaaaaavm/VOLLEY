"""Plot the measured Gen5 reference-assembly transverse packaging conflict."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "cad/REVIEW_ASSEMBLY.json").read_text())
parameters = json.loads((ROOT / "cad/parameters.json").read_text())
g = parameters["groups"]
half_enclosure = report["side_by_side_width_screen_mm"]["enclosure_internal_width"] / 2
half_track = g["track"]["overall_width"] / 2
half_mag = g["magazine"]["cassette_width_y"] / 2
center = report["reference_placement_mm"]["cassette_center_y_abs"]

fig, ax = plt.subplots(figsize=(6.5, 8.4), layout="constrained")
ax.add_patch(Rectangle((-half_enclosure, -205), 2 * half_enclosure, 910,
                       facecolor="#f5f8fa", edgecolor="#4e6575", linewidth=2,
                       label="Enclosure internal face"))
ax.add_patch(Rectangle((-half_track, -45), 2 * half_track, 65,
                       facecolor="#b8c6ce", edgecolor="#617582", linewidth=1.4,
                       label="Track bounding section"))
for sign, label in ((-1, "S"), (1, "P")):
    y0 = sign * center - half_mag
    ax.add_patch(Rectangle((y0, 0), 2 * half_mag, 690,
                           facecolor="#b5d9ca", alpha=0.68, edgecolor="#26745d",
                           linewidth=1.8, label="Cassette bounding section" if sign == -1 else None))
    ax.text(sign * center, 360, f"Cassette {label}", va="center", ha="center",
            rotation=90, fontsize=12, color="#1c5d4b", weight="bold")
    inner = center - half_mag
    ax.add_patch(Rectangle((sign * inner if sign > 0 else -half_track, 0),
                           half_track - inner, 20, facecolor="#d6544d",
                           edgecolor="#8b2924", linewidth=1.2,
                           label="Track/cassette clash region" if sign == -1 else None))
ax.annotate("11 mm shortfall before clearance", (0, 24), xytext=(0, 158),
            ha="center", fontsize=10, color="#8b2924", weight="bold",
            arrowprops={"arrowstyle": "->", "color": "#8b2924"},
            bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#d9e2e7"})
ax.set(xlim=(-285, 285), ylim=(-65, 730), xlabel="Transverse y (mm)",
       ylabel="Height z (mm)", title="Gen5 reference assembly: side-fed section")
ax.set_aspect("equal")
ax.grid(alpha=0.18, zorder=0)
ax.legend(loc="upper right", fontsize=8.5, framealpha=0.96)
target = ROOT / "figures/gen5_packaging_section"
fig.savefig(target.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.16)
fig.savefig(target.with_suffix(".png"), dpi=180, bbox_inches="tight", pad_inches=0.16)
plt.close(fig)
print(f"saved {target.name}; side-fed arrangement has {report['side_by_side_width_screen_mm']['shortfall_without_clearance']} mm width shortfall")
