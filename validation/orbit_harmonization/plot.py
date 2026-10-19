"""Plot captured native solver outputs with explicit numerical/model boundaries."""

from pathlib import Path
import json, numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = Path(__file__).resolve().parent
O = H / "figures"
O.mkdir(exist_ok=True)
plt.style.use(H.parents[1] / "tools/scientific.mplstyle")
a = np.genfromtxt(H / "residuals.csv", delimiter=",", names=True)
d = json.loads((H / "RESULTS.json").read_text())
fig, axs = plt.subplots(1, 2, figsize=(9, 4))
axs[0].plot(a["t_s"] / 3600, a["gmat_orekit_position_m"] * 1000, label="GMAT–Orekit")
axs[0].plot(
    a["t_s"] / 3600, a["scipy_orekit_position_m"] * 1000, label="Cartesian ODE–Orekit"
)
axs[0].set(
    xlabel="Elapsed time [h]",
    ylabel="Position residual [mm]",
    title="Matched pole and continuous arc",
)
axs[0].legend(fontsize=8)
v = list(d["diagnostic_ablation_m"].values())
labels = [
    "Original\naxis/constants",
    "Matched\nconstants",
    "Matched\npole",
    "Continuous\nGMAT arc",
]
axs[1].bar(range(4), v, color=["#8c989f", "#8c989f", "#0072b2", "#009e73"])
axs[1].set_yscale("log")
axs[1].set(
    xticks=range(4),
    xticklabels=labels,
    ylabel="Maximum position difference [m]",
    title="Diagnostic sequence",
)
axs[1].tick_params(axis="x", labelsize=8)
fig.subplots_adjust(bottom=0.27, wspace=0.4)
fig.text(
    0.02,
    0.015,
    "450 km, 51.6°; one day, J2 only. Shared prescribed GMAT EarthFixed pole. First three bars: SciPy versus repeated-stop GMAT;\nlast: Orekit versus continuous GMAT. Different numerical histories are declared; no flight-accuracy or motor validation.",
    fontsize=8,
)
for ext in ["png", "svg", "pdf"]:
    p = O / ("harmonization." + ext)
    fig.savefig(p, bbox_inches="tight")
    if ext == "svg":
        p.write_text("\n".join(x.rstrip() for x in p.read_text().splitlines()) + "\n")
plt.close(fig)
