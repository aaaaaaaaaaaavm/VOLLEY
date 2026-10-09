"""Presentation figures derived directly from the fixed Gen5 result JSON."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"


def load(name):
    return json.loads((ROOT / "analysis/results" / name).read_text())


def save(fig, stem):
    fig.savefig(FIG / f"{stem}.svg",
                metadata={"Date": "2026-10-09", "Creator": "VOLLEY Gen5 result JSON"})
    fig.savefig(FIG / f"{stem}.png", dpi=180,
                metadata={"Software": "VOLLEY Gen5 result JSON"})
    plt.close(fig)
    print(stem)


def mass_decision():
    result = load("mass_properties.json")
    dry = result["dry_kg"]
    per_payload = dry / 12
    assert abs(per_payload - 10.55) < 0.01
    fig, ax = plt.subplots(figsize=(8.6, 4.3), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f7fafc")
    names = ["Gen5 model", "Spring canister comparator", "Economic screen"]
    values = [per_payload, 6.0, 2.0]
    colors = ["#197e91", "#8194a2", "#cf5c52"]
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1], height=0.52)
    for bar, value in zip(bars, values[::-1]):
        ax.text(value + 0.14, bar.get_y() + bar.get_height()/2, f"{value:.2f} kg",
                va="center", color="#102d44", fontweight="bold")
    ax.set_xlim(0, 12.5)
    ax.set_xlabel("Deployer mass per carried 3U payload (kg)")
    ax.grid(axis="x", color="#d7e0e7", lw=0.8)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Gen5 fails both stated 3U mass comparisons",
                 loc="left", pad=14, fontweight="bold", color="#102d44")
    fig.text(0.5, 0.055,
             f"Gen5 = {dry:.1f} kg dry / 12 payloads. The 6 kg canister is an approximate comparator; "
             "the 2 kg criterion is a separate screen.",
             ha="center", fontsize=8.3, color="#4f6474")
    fig.subplots_adjust(left=0.29, right=0.94, top=0.77, bottom=0.23)
    save(fig, "gen5_mass_decision")


def energy_accounting():
    result = load("motor_results.json")
    shot = result["shot"]
    gross = shot["E_drawn"]
    recovered = result["regen"]["E_recovered"]
    net = result["E_drawn_net_J"]
    payload = shot["KE_payload"]
    other = net - payload
    assert abs(gross - recovered - net) < 0.1
    assert other > 0
    fig, ax = plt.subplots(figsize=(8.6, 3.8), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f7fafc")
    ax.barh(["Energy per rated shot"], [payload], color="#197e91", height=0.48,
            label="Payload kinetic energy")
    ax.barh(["Energy per rated shot"], [other], left=[payload], color="#8497a5",
            height=0.48, label="Other net energy")
    ax.text(payload/2, 0, f"Payload\n{payload:.0f} J", ha="center", va="center",
            color="white", fontweight="bold")
    ax.text(payload+other/2, 0, f"Other net energy\n{other:.0f} J", ha="center",
            va="center", color="white", fontweight="bold")
    ax.set_xlim(0, 3100)
    ax.set_yticks([])
    ax.set_xlabel("Energy (J)")
    ax.set_title("Rated Gen5 shot: energy entering the payload",
                 loc="left", pad=13, fontweight="bold", color="#102d44")
    ax.grid(axis="x", color="#d7e0e7", lw=0.8)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.5, 0.12,
             f"Gross draw {gross:.0f} J − modeled recovery {recovered:.0f} J = net {net:.0f} J; "
             f"payload share {100*payload/net:.1f}%.",
             ha="center", fontsize=9, color="#102d44")
    fig.text(0.5, 0.055,
             "The grey balance includes sled energy and modeled losses; it is not a measured or itemized loss audit.",
             ha="center", fontsize=8, color="#4f6474")
    fig.subplots_adjust(left=0.12, right=0.96, top=0.72, bottom=0.32)
    save(fig, "gen5_energy_accounting")


if __name__ == "__main__":
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "VOLLEY-GEN5-2026-10-09"})
    mass_decision()
    energy_accounting()
