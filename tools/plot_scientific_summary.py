"""Scientific presentation edition of captured Gen5 mass/lifetime results.

The original result JSON and frozen technical evidence record are unchanged.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
plt.style.use(ROOT / "tools/scientific.mplstyle")
mass = json.loads((ROOT / "analysis/results/gen5_mass_ledger.json").read_text())
life = json.loads((ROOT / "analysis/results/gen5_lifetime_crosscheck.json").read_text())
fig, ax = plt.subplots(figsize=(8.0, 4.6), layout="constrained")
labels = ["Gen5 historical model", "Illustrative −15% mass", "Spring-class assumption"]
values = [mass["historical_dry_kg"], .85 * mass["historical_dry_kg"], 72]
bars = ax.barh(labels[::-1], values[::-1], color=["#467c95", "#c9873b", "#af4a43"])
for bar in bars:
    ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
            f"{bar.get_width():.2f} kg", va="center")
ax.set_xlim(0, 150)
ax.set_xlabel("Device mass for twelve 3U payloads [kg]")
ax.set_title("Gen5 misses the historical mass screen", loc="left", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
fig.set_layout_engine(None)
fig.subplots_adjust(left=.27, right=.97, bottom=.24, top=.88)
fig.text(.02, .015, "Model values and class benchmark; −15% is an assumed sensitivity, not confidence.\nNo installed vendor BOM, measured mass or provider fit is established.", fontsize=9)
fig.savefig(ROOT / "figures/gen5_scientific_mass.png", dpi=300, bbox_inches="tight")
for ext in ("svg", "pdf"):
    name = "gen5_scientific_mass" if len(fig.axes) == 1 else "gen5_scientific_lifetime"
    target = ROOT / "figures" / (name + "." + ext)
    fig.savefig(target, bbox_inches="tight")
    if ext == "svg":
        target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines())+"\n")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(8.0, 4.6), layout="constrained")
cases = life["runs"][3:]
labels = ["Spring input\n2.5 m/s", "Ideal-screen input\n12.448 m/s", "Historical input\n16.029 m/s"]
for ax, key, ylabel in [(axes[0], "lifetime_years", "Modeled lifetime [years]"),
                         (axes[1], "lifetime_ratio", "Ratio to no-impulse model")]:
    ax.bar(range(3), [x[key] for x in cases], color=["#467c95", "#c9873b", "#af4a43"])
    ax.set_xticks(range(3), labels, fontsize=8)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    for i, x in enumerate(cases):
        ax.text(i, x[key]+.025, f"{x[key]:.3f}", ha="center", fontsize=9)
    ax.set_ylim(0, max(x[key] for x in cases)*1.22)
fig.suptitle("P134 · Independent numerical integration of a shared static atmosphere", fontweight="bold", fontsize=11)
fig.set_layout_engine(None)
fig.subplots_adjust(left=.08, right=.98, bottom=.25, top=.86, wspace=.27)
fig.text(.02, .015, "450 km start; BC 61 kg/m²; stop at 120 km perigee. Speeds are imposed inertial inputs.\nNumerical agreement does not validate atmospheric lifetime or an achieved release speed.", fontsize=9)
fig.savefig(ROOT / "figures/gen5_scientific_lifetime.png", dpi=300, bbox_inches="tight")
for ext in ("svg", "pdf"):
    name = "gen5_scientific_mass" if len(fig.axes) == 1 else "gen5_scientific_lifetime"
    target = ROOT / "figures" / (name + "." + ext)
    fig.savefig(target, bbox_inches="tight")
    if ext == "svg":
        target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines())+"\n")
plt.close(fig)
print("PASS: mass and conditional-lifetime figures generated from captured JSON")
