"""Scientific figures from the captured numerical/STEP data; no synthesized CAD."""

from pathlib import Path
import json, io
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image

H = Path(__file__).parent
O = H / "figures"
O.mkdir(exist_ok=True)
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.facecolor": "white",
    }
)
NAVY = "#234762"
RED = "#a33f36"
GRAY = "#697782"
ORANGE = "#bd792b"


def save(fig, name, jpg=False):
    fig.tight_layout()
    for ext in ["png", "svg", "pdf"]:
        fig.savefig(O / (name + "." + ext), dpi=180, bbox_inches="tight")
    if jpg:
        fig.savefig(O / (name + ".jpg"), dpi=180, bbox_inches="tight")
    plt.close(fig)


data = json.loads((H / "cad/STEP_EDGES.json").read_text())
lookup = {x["file"]: x for x in data}
phases = [
    ("stored", "Stored and restrained"),
    ("transfer", "200mm lateral transfer"),
    ("sled_captured", "Receiving locks inserted"),
    ("fork_home", "Fork withdrawn"),
    ("cell_closed", "Storage gate closed"),
    ("sled_translation", "Captive sled translated80mm"),
]


def draw(ax, phase):
    d = lookup["FM02_3U_" + phase + ".step"]
    lines = [np.asarray(x)[:, :2] for x in d["edges"]]
    ax.add_collection(LineCollection(lines, colors=NAVY, linewidths=0.35))
    ax.set(
        xlim=(-130, 485),
        ylim=(-350, 120),
        xlabel="X · launch direction [mm]",
        ylabel="Y · feed direction [mm]",
    )
    ax.set_aspect("equal")


fig, axes = plt.subplots(2, 3, figsize=(6.7, 4.8))
for i, (ax, (phase, title)) in enumerate(zip(axes.flat, phases)):
    draw(ax, phase)
    ax.set_title(
        chr(97 + i)
        + ") "
        + [
            "Stored",
            "Transfer",
            "Receiver locked",
            "Fork home",
            "Cell closed",
            "Sled +80 mm",
        ][i],
        loc="left",
        fontsize=8,
    )
    ax.tick_params(labelsize=6)
    ax.xaxis.label.set_size(7)
    ax.yaxis.label.set_size(7)
    ax.set_xticks([0, 200, 400])
    ax.set_yticks([-300, -100, 100])
save(fig, "step_sequence", True)
frames = []
for phase, title in phases:
    fig, ax = plt.subplots(figsize=(8.4, 6))
    draw(ax, phase)
    ax.set_title("FM-02 · " + title, loc="left")
    fig.text(
        0.14,
        0.02,
        "STEP-derived prescribed poses · no time or dynamic fidelity",
        fontsize=8,
        color=GRAY,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=120)
    plt.close(fig)
    b.seek(0)
    frames.append(Image.open(b).convert("RGB"))
frames[0].save(
    O / "prescribed_cycle.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1400,
    loop=0,
)
detail = json.loads((H / "cad/INTERLOCK_EDGES.json").read_text())
fig, ax = plt.subplots(figsize=(8.0, 4.0))
for n, edges in detail["parts"].items():
    ax.add_collection(
        LineCollection(
            [np.array(e)[:, :2] for e in edges],
            linewidths=0.75,
            colors=(
                ORANGE if n == "gate_crossbolt" else NAVY if n == "fork_body" else GRAY
            ),
            label=n.replace("_", " "),
        )
    )
ax.set(
    xlim=(365, 470),
    ylim=(-115, -72),
    xlabel="X [mm]",
    ylabel="Y [mm]",
    title="FM-02 · storage-gate crossbolt and carried withdrawal blocker",
)
ax.set_aspect("equal")
ax.legend(loc="upper left", fontsize=7)
save(fig, "interlock_plan", True)
drive = json.loads((H / "INTEGRATED_DRIVE.json").read_text())
fig, axes = plt.subplots(1, 2, figsize=(6.7, 3.2))
for T, color in zip([5, 10, 15, 20], [RED, ORANGE, GRAY, NAVY]):
    rows = [x for x in drive["cases"] if x["time_s"] == T]
    axes[0].scatter(
        [x["peak_motor_rpm"] for x in rows],
        [1000 * x["peak_motor_torque_Nm"] for x in rows],
        s=8,
        alpha=0.3,
        label=str(T) + "s",
        color=color,
    )
axes[0].axhline(41.8, color=GRAY, lw=0.8, ls="--")
speed = np.linspace(0, 5600, 100)
axes[0].plot(speed, (5600 - speed) / 20.4, color=GRAY, lw=0.8, label="24V slope")
axes[0].axvline(5600, color=GRAY, lw=0.8, ls=":")
axes[0].set(
    ylim=(0, 45),
    xlabel="Peak motor speed [rpm]",
    ylabel="Peak motor torque [mNm]",
    title="Motor demand · ambient catalogue screen",
)
axes[0].legend(ncol=2, fontsize=7)
trace = np.array(drive["thermal_trace"])
axes[1].plot(trace[:, 0] / 60, trace[:, 1], color=NAVY, label="Winding")
axes[1].plot(trace[:, 0] / 60, trace[:, 2], color=GRAY, label="Housing")
axes[1].axhline(125, color=RED, ls="--", lw=0.8, label="Winding ceiling")
axes[1].set(
    xlabel="Time [min]",
    ylabel="Temperature [°C]",
    title="Repeated-cycle thermal sensitivity",
)
axes[1].legend(fontsize=7)
save(fig, "drive_thermal")
brake = json.loads((H / "BRAKE_REVIEW.json").read_text())
fig, ax = plt.subplots(figsize=(6.7, 3.6))
for v, color in zip([0.02, 0.0266666666667, 0.04, 0.08], [NAVY, GRAY, ORANGE, RED]):
    r = [
        x
        for x in brake["cases"]
        if x["initial_m_s"] == v and x["total_runout_mm"] is not None
    ]
    ax.scatter(
        [x["total_delay_s"] * 1000 for x in r],
        [x["total_runout_mm"] for x in r],
        s=9,
        alpha=0.25,
        color=color,
        label=f"{v*1000:.1f}mm/s",
    )
ax.axhline(24, ls="--", color=GRAY, lw=0.8, label="Proposed24mm allowance")
ax.set(
    xlabel="Assumed total delay [ms]",
    ylabel="Modeled total runout [mm]",
    title="BXW-L candidate · static torque scaled as a dynamic hypothesis",
)
ax.legend(ncol=3, fontsize=7)
save(fig, "stop_sensitivity")
fit = json.loads((H / "FIT_BUDGET.json").read_text())
names = list(dict.fromkeys(x["interface"] for x in fit["cases"]))
fig, ax = plt.subplots(figsize=(6.7, 3.8))
samples = [
    [x["residual_mm"] for x in fit["cases"] if x["interface"] == n] for n in names
]
ax.boxplot(
    samples,
    tick_labels=[n.replace("_", "\n") for n in names],
    showfliers=False,
    medianprops={"color": NAVY},
)
ax.axhline(0, color=RED, lw=0.8)
ax.set(
    ylabel="Residual nominal gap [mm]",
    title="Datum and thermal sensitivity · ranges, not manufacturing acceptance",
)
ax.tick_params(axis="x", labelsize=7)
save(fig, "fit_budget")
sch = json.loads((H / "SCHEDULE.json").read_text())
fig, ax = plt.subplots(figsize=(6.7, 3.6))
for name, color, offset in [
    ("slow_auxiliaries", ORANGE, -0.12),
    ("faster_auxiliaries", NAVY, 0.12),
]:
    rows = [
        x for x in sch["cases"] if x["input"].startswith("12_") and x["policy"] == name
    ]
    ax.bar(
        np.array([x["release_index"] for x in rows]) + offset,
        [x["margin_s"] for x in rows],
        0.24,
        color=color,
        label=name.replace("_", " "),
    )
ax.axhline(0, color=GRAY, lw=0.8)
ax.set(
    xlabel="Release index · twelve-payload constructed campaign",
    ylabel="Available coast minus assumed cycle [s]",
    title="Handling schedule · unselected auxiliary actuator speeds",
)
ax.legend(fontsize=8)
save(fig, "handling_margin")
convergence=json.loads((H/'CONVERGENCE.json').read_text())
fig,ax=plt.subplots(figsize=(6.7,3.5))
for key,label,color in [('peak_torque_relative_error','Torque',NAVY),('energy_relative_error','Input-energy proxy',ORANGE)]:
    x=[101,201,401,801,1601]
    y=[max(r[key] for r in convergence['refinements'] if r['samples']==n) for n in x]
    ax.loglog(x,y,'o-',color=color,label=label,markersize=4)
ax.set(xlabel='Trajectory samples',ylabel='Maximum relative error against polynomial reference',title='Drive numerical consistency · same equations, independent evaluation')
ax.legend(fontsize=8);save(fig,'drive_convergence')
print("Seven numerical/STEP figure sets and a prescribed-pose GIF generated")
