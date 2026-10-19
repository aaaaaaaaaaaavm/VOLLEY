"""Report captured coupled campaigns, including resource and adverse-case limits."""

from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = Path(__file__).resolve().parent
O = H / "release"
F = O / "figures"
F.mkdir(exist_ok=True)
plt.style.use(H.parents[1] / "tools/scientific.mplstyle")
d = json.loads((O / "RESULTS.json").read_text())
reserve = json.loads((O / "RESERVE_CASES.json").read_text())
ref = json.loads((O / "REFINEMENT.json").read_text())
fig, axs = plt.subplots(1, 2, figsize=(9, 4))
labels = {
    "spring": "Spring 2.5 m/s",
    "volley_3_6": "VOLLEY 3–6 m/s",
    "volley_unrestricted": "Unrestricted input",
}
for ax, n in zip(axs, [4, 12]):
    rows = [
        r
        for r in (d["cases"] if n == 4 else reserve["cases"])
        if r["count"] == n and "fuel_used_kg" in r
    ]
    x = np.arange(len(rows))
    ax.bar(
        x,
        [r["device_mass_proxy_kg"] for r in rows],
        label="Device mass proxy",
        color="#8c989f",
    )
    ax.bar(
        x,
        [r["fuel_used_kg"] for r in rows],
        bottom=[r["device_mass_proxy_kg"] for r in rows],
        label="Consumed propellant",
        color="#0072b2",
    )
    ax.set(
        xticks=x,
        xticklabels=[labels[r["strategy"]] for r in rows],
        ylabel="Device proxy + consumed fuel [kg]",
        title=f"{n} payloads · " + ("10" if n == 4 else "20") + " kg initial fuel",
    )
    ax.tick_params(axis="x", labelsize=8, rotation=12)
axs[0].legend(fontsize=8)
fig.subplots_adjust(bottom=0.3, wspace=0.35)
fig.text(
    0.02,
    0.01,
    "Constructed common-epoch states, ideal host impulses and fixed-axis J2. Device proxies are 16/30 kg per 4 payloads,\nnot a designed installed BOM. Loaded reserves differ between panels; no customer service or commercial advantage proven.",
    fontsize=8,
)
for ext in ["png", "svg", "pdf"]:
    p = F / ("resource_comparison." + ext)
    fig.savefig(p, bbox_inches="tight")
    if ext == "svg":
        p.write_text("\n".join(x.rstrip() for x in p.read_text().splitlines()) + "\n")
plt.close(fig)
lines = [
    "---",
    'title: "VOLLEY Gen6 — coupled delivery and host-resource study"',
    'date: "19 October 2026"',
    "geometry: margin=20mm",
    "fontsize: 10pt",
    "mainfont: DejaVu Sans",
    "---",
    "",
    "# Study boundary",
    "",
    "This is a constructed numerical comparison, not a validated customer mission or working launcher. Four and twelve alternating 1.33/4 kg passive payloads start at a 500 km, 97.4° surrogate. Releases occur from 0 to 3600 s. Each target is defined by a 3–9 m/s prograde increment at its release epoch, then propagated to the common 90000 s epoch, 24 h after the final release. These selected targets favor variable release commands and are not evidence of customer demand or an optimum deployment strategy.",
    "",
    "Host dry mass is 300 kg, assumed Isp 220 s. Device proxies are 16 kg for springs and 30 kg for VOLLEY per four payloads. They are explicit assumptions, not installed mass estimates. Spring departure is 2.5 m/s; VOLLEY commands are limited to 3–6 m/s in the first-article case. The unrestricted case reaches about 9.1 m/s relative and is an imposed future-capability diagnostic, not an achievable motor rating.",
    "",
    "# Coupled host construction",
    "",
    "Each shot solves a finite-mass momentum split. Host pre-burn and propellant are coupled through a fixed-point rocket equation. The host coasts 20 s after release, then an ideal-impulse shooting transfer restores the next nominal release position. After the final shot it restores reference host position and velocity at 4200 s before coasting to the common epoch. All pre-burn, transfer and final-restore delta-v is counted. Finite burns, thruster direction/geometry, slew, plume exclusion, navigation, control limits, power, thermal duty and disposal are absent. No host compatibility or resource feasibility follows.",
    "",
    "Full Cartesian payload targets are met by construction; their small residuals check the solver and shooting equations. They are not a release-accuracy prediction. The force model is fixed-axis J2, distinct from the GMAT/Orekit prescribed-pole benchmark.",
    "",
    "![Resource comparison](release/figures/resource_comparison.png)",
    "",
    "# Results",
    "",
    "| N | Strategy | Initial fuel [kg] | Consumed [kg] | Device proxy [kg] | Status |",
    "|--:|:--|--:|--:|--:|:--|",
]
for r in d["cases"] + reserve["cases"]:
    if "fuel_used_kg" in r:
        lines.append(
            f"| {r['count']} | {labels[r['strategy']]} | {r['initial_fuel_kg']:.0f} | {r['fuel_used_kg']:.6f} | {r['device_mass_proxy_kg']:.0f} | Computed ideal-impulse case |"
        )
    else:
        lines.append(
            f"| {r['count']} | {labels[r['strategy']]} |10|—|—| Fuel reserve exhausted |"
        )
lines += [
    "",
    "The twelve-release spring case exceeds the 10 kg reserve at the tenth transfer. Increasing all twelve-payload alternatives to 20 kg initial fuel gives a completing spring countercase; reserve exhaustion therefore does not establish that spring delivery is impossible. Under these proxies, the VOLLEY device mass increase exceeds the propellant saving. This study does not establish a favorable installed-system mass case. A competent alternative may also choose different release times, host paths or target tolerances; no global optimization has been performed.",
    "",
    "# Conditional nominal clearance",
    "",
    "The interval screen starts host/payload assessment20 s after each release, excluding the actual launch-interface/near-field phase. It splits host arcs at each ideal impulse. Pairwise payload assessment begins at the later birth. Over an interval half-width h, the lower bound uses midpoint distance minus relative speed times h minus10h² minus0.02 m. The acceleration term assumes a20 m/s² relative acceleration bound while both bodies remain outside the Earth radius; the domain is checked conservatively from center states. Adaptive bisection retains unresolved or violating intervals.",
    "",
    "The 0.02 m subtraction stipulates at most 1 cm numerical position error per object; it is not an independently rigorous error enclosure. The 20 m threshold applies to nominal point centers. Payload size, swept launch geometry, covariance, navigation, contact, tip-off, plume and finite burns are not included. A passing conditional screen is not collision-free flight, a collision probability or launch-interface clearance proof.",
    "",
    "# Numerical refinement",
    "",
    "Reducing the DOP853 maximum step 60→30 s preserves the retained fuel-exhaustion failure. Completed-case fuel and host-delta-v changes are recorded in REFINEMENT.json. Same-solver refinement is not independent mission validation. Momentum identities are algebraic checks; atmospheric drag, Earth orientation and real propulsion errors remain outside this model.",
    "",
    "# Reproduction",
    "",
    "`python run.py` reproduces the 10 kg cases, `python refine.py` the 30 s refinement, `python reserve.py` the 20 kg twelve-payload countercases, and `python report.py` this report and figure. Raw state CSV filenames identify manifest count, strategy, initial fuel and maximum step. RESULTS.json and RESERVE_CASES.json retain shot and burn histories; source and exact result hashes are recorded in MANIFEST.json. The frozen Gen5 evaluated record is unchanged.",
]
(H / "README.md").write_text("\n".join(lines) + "\n")
print("Coupled campaign report and resource figure written")
