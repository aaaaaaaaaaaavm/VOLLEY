#!/usr/bin/env python3
"""Plot the four-cell CAD study dimensions from its machine-readable report."""
from pathlib import Path
import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--release", type=Path, default=HERE/"release")
OUT = parser.parse_args().release
report = json.loads((OUT / "Four_Cell_R0_Report.json").read_text())
fig, ax = plt.subplots(figsize=(13, 5.5))
fig.patch.set_facecolor("#f7f9fb")
ax.set_facecolor("#f7f9fb")
ax.add_patch(Rectangle((100, -55), 1600, 110, facecolor="#d9e8f1",
                       edgecolor="#226a91", linewidth=1.5, label="Common rail corridor"))
for cell in report["cells"]:
    y = -265 if cell["side"] == "left" else 140
    colour = "#188275" if cell["size"] == "3U" else "#e3a131"
    ax.add_patch(Rectangle((cell["x_mm"], y), cell["length_mm"], 125,
                           facecolor=colour, edgecolor="#263746", linewidth=1.3, alpha=.86))
    ax.text(cell["x_mm"]+cell["length_mm"]/2, y+62.5,
            f'{cell["name"]}\n{cell["available_drive_travel_mm"]:.0f} mm',
            ha="center", va="center", color="white" if cell["size"] == "3U" else "#21313d",
            fontsize=8, weight="bold")
ax.axvspan(1450, 1650, facecolor="#d77574", alpha=.37, label="Modeled brake envelope")
ax.axvline(1450, color="#a33e42", linewidth=1.5)
ax.text(1450, 293, "Drive end / brake start", ha="right", va="top", color="#892c32", fontsize=9)
ax.set_xlim(0, 1800)
ax.set_ylim(-310, 310)
ax.set_xlabel("Rail station x (mm)")
ax.set_ylabel("Lateral position y (mm)")
ax.set_title("Gen6 R0: two 3U and two 1U fixed cells — " +
             ("paired sides" if "variant" in report else "staggered") +
             " nominal packaging study", loc="left", weight="bold")
ax.grid(axis="x", color="#d4dde4", linewidth=.7)
ax.legend(loc="lower right", frameon=False)
fig.subplots_adjust(bottom=.19, left=.07, right=.98, top=.87)
fig.text(.07, .04, "Unselected FreeCAD envelope study; no host ICD, restraint, contact or installed mass verified.",
         color="#4c5e68", fontsize=9)
fig.savefig(OUT/"Four_Cell_R0_Plan.png", dpi=180)
fig.savefig(OUT/"Four_Cell_R0_Plan.svg")
