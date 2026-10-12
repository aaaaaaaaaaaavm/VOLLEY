"""Draw a FreeCAD-derived y-z section at x=300 mm for R1 and R2.

This is a geometric visualization, not a contact, deflection or load result.
Run with PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3.
"""
from pathlib import Path

import FreeCAD as App
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
COLORS = {"Payload": "#31b6a2", "Bridge": "#eaa34b", "Support lip": "#5b8fca", "Raised guide": "#a6b4c2"}


def bounds(doc, name):
    b = doc.getObject(name).Shape.BoundBox
    assert b.XMin < 300 < b.XMax
    return b.YMin, b.YMax, b.ZMin, b.ZMax


fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharex=True, sharey=True, layout="constrained")
for ax, revision in zip(axes, ("R1", "R2")):
    path = HERE.parent / f"gen6_integration_{revision.lower()}" / "release" / f"Gen6_Integrated_{revision}_02_mid_transfer.FCStd"
    doc = App.openDocument(str(path))
    items = [
        (f"Transfer_Bridge_{revision}", "Bridge", 1.0),
        ("Support_Lip_Left", "Support lip", 1.0),
        ("Passive_3U_Box", "Payload", 0.28),
        ("Guide_Left_Lifting_Window", "Raised guide", 0.75),
    ]
    for part, label, opacity in items:
        ymin, ymax, zmin, zmax = bounds(doc, part)
        ax.add_patch(Rectangle((ymin, zmin), ymax-ymin, zmax-zmin,
                               facecolor=COLORS[label], edgecolor="#17324a", linewidth=1.2,
                               alpha=opacity, label=label))
    if revision == "R1":
        ax.annotate("10 mm open gap", xy=(-60, 47), xytext=(-115, 95),
                    arrowprops={"arrowstyle": "->", "color": "#b75139"}, color="#b75139")
    else:
        ax.annotate("nominal face contact\nat y = −55 mm", xy=(-55, 47), xytext=(-115, 95),
                    arrowprops={"arrowstyle": "->", "color": "#116d62"}, color="#116d62")
    ax.set_title(f"Unselected Gen6 {revision} · mid-transfer")
    ax.set_xlim(-160, -30)
    ax.set_ylim(28, 220)
    ax.set_xlabel("Lateral position y (mm)")
    ax.grid(alpha=0.18)
    App.closeDocument(doc.Name)
axes[0].set_ylabel("Height z (mm)")
handles, labels = axes[1].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.10))
fig.text(0.5, -0.16, "Section from saved FreeCAD solids at x = 300 mm. No loaded contact, moving transition or restraint verified.",
         ha="center", fontsize=9, color="#46556a")
for suffix in ("png", "svg"):
    fig.savefig(HERE / "release" / f"Gen6_R1_R2_Handoff_Section.{suffix}", dpi=180,
                bbox_inches="tight", facecolor="white")
