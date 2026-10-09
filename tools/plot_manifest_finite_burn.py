"""Plot the reproducible P113-S12 accepted-prefix screen."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analysis/results/manifest_finite_burn.json"
SVG = ROOT / "figures/manifest_finite_burn.svg"
PNG = ROOT / "figures/manifest_finite_burn.png"


def main():
    data = json.loads(DATA.read_text())
    cases = data["cases"]
    assert len(cases) == 6
    assert all(data["verification"][k] for k in
               ("s11_identities", "event_accounting", "manifest_accounting", "convergence"))
    by_speed = {speed: {c["thrust_N"]: c["completed_deliveries"]
                        for c in cases if c["speed_m_s"] == speed}
                for speed in (1.0, 2.0)}
    thrusts = [1.0, 10.0, 100.0]
    assert all(set(by_speed[speed]) == set(thrusts) for speed in by_speed)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "P113-S12-2026-10-09"})
    fig, ax = plt.subplots(figsize=(9, 5.1), dpi=160)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f7fafc")
    x = np.arange(len(thrusts))
    width = 0.31
    for offset, speed, color in ((-width/2, 1.0, "#197e91"),
                                 (width/2, 2.0, "#dd9b38")):
        values = [by_speed[speed][t] for t in thrusts]
        bars = ax.bar(x + offset, values, width, color=color,
                      label=f"{speed:g} m/s assumed release", zorder=3)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x()+bar.get_width()/2, value+0.18, f"{value}/12",
                    ha="center", va="bottom", color="#102d44", fontweight="bold")
    ax.axhline(12, color="#c54f4f", lw=1.6, ls="--", label="Full manifest", zorder=2)
    ax.set(xticks=x, xticklabels=["1", "10", "100"], ylim=(0, 13.2),
           xlabel="Assumed host thrust (N)", ylabel="Accepted delivery prefix / 12")
    ax.set_yticks(range(0, 13, 2))
    ax.grid(axis="y", color="#d7e0e7", lw=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    fig.suptitle("No complete 12-payload campaign in six sampled finite-burn cases",
                 x=0.5, y=0.98, fontsize=14, fontweight="bold", color="#102d44")
    fig.text(0.5, 0.012,
             "P113-S12 · planar two-body surrogate · 300 kg dry host + 10 kg fuel · fixed 1200 s cadence\n"
             "Bounded optimizer and assumed thrust/release speeds; counts are not hardware or mission validation.",
             ha="center", va="bottom", fontsize=8.2, color="#4f6474")
    fig.subplots_adjust(top=0.76, bottom=0.19, left=0.12, right=0.98)
    fig.savefig(SVG, metadata={"Date": "2026-10-09", "Creator": "VOLLEY P113-S12"})
    fig.savefig(PNG, dpi=180, metadata={"Software": "VOLLEY P113-S12"})
    print(f"Wrote {SVG.relative_to(ROOT)} and {PNG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
