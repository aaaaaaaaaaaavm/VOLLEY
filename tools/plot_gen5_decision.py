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
    svg = FIG / f"{stem}.svg"
    fig.savefig(svg,
                metadata={"Date": "2026-10-09", "Creator": "VOLLEY Gen5 result JSON"})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
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
    audit = load("rated_energy_mass_audit.json")["derived"]
    shot = result["shot"]
    gross = shot["E_drawn"]
    recovered = result["regen"]["E_recovered"]
    net = result["E_drawn_net_J"]
    payload = shot["KE_payload"]
    sled = result["regen"]["KE_sled_in"]
    copper = shot["Q_copper"]
    esr = shot["Q_esr"]
    modeled_other = (audit["converter_loss_at_model_assumption_J"]
                     + audit["auxiliary_draw_at_model_assumption_J"]
                     + audit["forward_euler_mechanical_excess_J"])
    assert abs(gross - recovered - net) < 0.1
    assert abs(gross - payload - sled - copper - esr - modeled_other) < 0.1
    fig, ax = plt.subplots(figsize=(8.6, 3.8), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f7fafc")
    parts = [("Payload KE", payload, "#197e91"), ("Sled KE", sled, "#355f80"),
             ("Copper", copper, "#b67545"), ("Bank ESR", esr, "#884f5f"),
             ("Converter + aux + step", modeled_other, "#8497a5")]
    left = 0.0
    for label, value, color in parts:
        ax.barh(["Historical model shot"], [value], left=[left], color=color,
                height=0.48, label=f"{label}: {value:.0f} J")
        if value > 300:
            ax.text(left + value/2, 0, f"{label}\n{value:.0f} J", ha="center", va="center",
                    color="white", fontweight="bold", fontsize=8.7)
        left += value
    ax.set_xlim(0, 3100)
    ax.set_yticks([])
    ax.set_xlabel("Energy (J)")
    fig.suptitle("Historical periodic-model shot: energy allocation",
                 x=0.12, y=0.98, ha="left", fontweight="bold", color="#102d44")
    ax.grid(axis="x", color="#d7e0e7", lw=0.8)
    ax.set_axisbelow(True)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.12, 0.91),
               ncol=3, fontsize=7.8, frameon=False, borderaxespad=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.5, 0.12,
             f"Gross draw {gross:.0f} J − modeled recovery {recovered:.0f} J = net {net:.0f} J; "
             f"payload share {100*payload/net:.1f}%.",
             ha="center", fontsize=9, color="#102d44")
    fig.text(0.5, 0.055,
             "The 124 J modeled balance resolves arithmetically; converter and auxiliary ratings are unverified.",
             ha="center", fontsize=8, color="#4f6474")
    fig.subplots_adjust(left=0.12, right=0.96, top=0.67, bottom=0.32)
    save(fig, "gen5_energy_accounting")


if __name__ == "__main__":
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "VOLLEY-GEN5-2026-10-09"})
    mass_decision()
    energy_accounting()
