"""Matched reference missions: one delivered state and one 12-shot finite-burn screen.

Every option sees the same payload, host base, epoch/target, fuel and target
manifest. Options lacking a defined dynamical/service model remain unevaluated.
The full campaign uses the pre-existing P113-S12 optimizer and its stated
reference limitations, with installed dispenser mass added to host dry mass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

import astro
import finite_burn_departure as fb
import manifest_finite_burn as mf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/results/matched_mission_reference.json"
DOC = ROOT / "docs/MATCHED_MISSION_REFERENCE.md"
FIG = ROOT / "figures/matched_mission_reference.png"
ALT = 450_000.0
PAYLOAD = 4.0
N = 12
BASE_HOST_DRY = 300.0
FUEL = 10.0
RESERVE = 2.0
TARGET_DV = 16.029
SPRING_MASS = 72.0  # 12 x 6 kg class figure, not a vendor quote


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def one_event(name, release_speed, device_mass):
    initial_mass = BASE_HOST_DRY + device_mass + FUEL + N * PAYLOAD

    def residual(burn):
        mass_at_release = initial_mass * math.exp(-burn / fb.VE)
        inertial_payload_increment = burn + (1 - PAYLOAD / mass_at_release) * release_speed
        return inertial_payload_increment - TARGET_DV

    burn = brentq(residual, 0.0, TARGET_DV + release_speed)
    mass_at_release = initial_mass * math.exp(-burn / fb.VE)
    propellant = initial_mass - mass_at_release
    host_increment_after_release = burn - PAYLOAD / mass_at_release * release_speed
    payload_increment = burn + (1 - PAYLOAD / mass_at_release) * release_speed
    return dict(option=name, release_speed_m_s=release_speed, installed_device_kg=device_mass,
                initial_host_plus_manifest_kg=initial_mass, host_preburn_m_s=burn,
                ideal_propellant_kg=propellant, fuel_after_event_kg=FUEL-propellant,
                host_increment_after_release_m_s=host_increment_after_release,
                payload_increment_m_s=payload_increment,
                target_residual_m_s=payload_increment-TARGET_DV,
                reserve_screen_pass=FUEL-propellant>=RESERVE)


def campaign(name, release_speed, device_mass):
    old = mf.DRY, mf.INITIAL_MASS
    try:
        mf.DRY = BASE_HOST_DRY + device_mass
        mf.INITIAL_MASS = mf.DRY + mf.FUEL + mf.N * mf.PAYLOAD
        result = mf.campaign(release_speed, 100.0)
    finally:
        mf.DRY, mf.INITIAL_MASS = old
    stages = []
    for stage in result["stages"]:
        selected = stage["selected"]
        stages.append(dict(index=stage["index"], reason=stage.get("reason"),
                           selected_accepted=bool(selected and selected.get("accepted")),
                           selected_errors=selected.get("errors") if selected else None,
                           selected_service_pass=selected.get("service_pass") if selected else None,
                           accepted_attempts=sum(bool(a.get("accepted")) for a in stage["attempts"])))
    return dict(option=name, release_speed_m_s=release_speed, device_mass_kg=device_mass,
                base_host_dry_kg=BASE_HOST_DRY, initial_mass_kg=BASE_HOST_DRY+device_mass+FUEL+N*PAYLOAD,
                modeled_thrust_N=100.0, completed_deliveries=result["completed_deliveries"],
                accepted_all_12=result["accepted"], stages=stages,
                accepted_prefix_fuel_remaining_kg=result.get("nominal",{}).get("fuel_remaining_kg"),
                accepted_prefix_convergence=result.get("convergence",{}).get("passed"),
                uncertainty_corners_run=len(result.get("corners",[])),
                passing_prefix_corners=sum(bool(x["prefix_accepted"]) for x in result.get("corners",[])))


def build():
    finite = json.loads((ROOT / "analysis/results/gen5_finite_force_map.json").read_text())
    finite_speed = finite["ideal_finite_stator_exit_upper_m_s"]
    options = [("Spring dispenser class",2.5,SPRING_MASS),
               ("Gen5 finite-force ideal upper",finite_speed,126.562),
               ("Gen5 historical rated model",16.029,126.562)]
    single = [one_event(*x) for x in options]
    manifests = [campaign(*x) for x in options]
    r = astro.RE + ALT
    vc = math.sqrt(astro.MU/r)
    sma = 1/(2/r-(vc+TARGET_DV)**2/astro.MU)
    return dict(status="MATCHED_REFERENCE_SCREEN_NOT_PROVIDER_MISSION_OR_HARDWARE_VALIDATION",
                input=dict(altitude_m=ALT, payload_kg=PAYLOAD, count=N,
                           host_base_dry_kg=BASE_HOST_DRY, host_initial_fuel_kg=FUEL,
                           reserve_kg=RESERVE, isp_s=fb.ISP_S,
                           single_event_target_inertial_tangential_increment_m_s=TARGET_DV,
                           campaign_release_interval_s=1200,
                           campaign_target_spacing_m=5000,
                           campaign_terminal_time_s=18000,
                           campaign_thrust_N=100),
                target_semi_major_axis_rise_km=(sma-r)/1000,
                single_event=single, finite_burn_campaign=manifests,
                unmodeled_alternatives=["onboard propulsion: no named tank, thrust, pointing or installed mass",
                                        "orbital transport: no quoted service, provider trajectory or interface",
                                        "differential drag: cannot provide this immediate same-epoch target; long-deadline trade separate"],
                source_sha256={str(p.relative_to(ROOT)):digest(p) for p in
                               [Path(__file__), ROOT/"analysis/manifest_finite_burn.py",
                                ROOT/"analysis/finite_burn_departure.py",
                                ROOT/"analysis/results/gen5_finite_force_map.json"]})


def report(d):
    one = d["single_event"]
    camp = d["finite_burn_campaign"]
    lines = ["# Matched reference mission comparison", "",
             "**Reference screen, not a supplier quote, qualified mission or proof of global infeasibility.**",
             "All options use 12 identical 4 kg spacecraft, the same 450 km circular starting",
             "state, 300 kg base host, 10 kg fuel, 2 kg reserve and 220 s assumed host Isp.",
             "Installed dispenser mass is added to host dry mass: a 72 kg class spring set",
             "(6 kg per 3U × 12) or the 126.562 kg modeled Gen5 dry mass. The latter mixes",
             "assumed components with a historical sled-volume input and is not measured.", "",
             "## One release at a common epoch", "",
             f"The exact common target is a +{TARGET_DV:.3f} m/s *inertial* tangential payload",
             f"increment, giving a {d['target_semi_major_axis_rise_km']:.3f} km immediate two-body",
             "semi-major-axis rise. Momentum-conserving recoil is included; the host may make an",
             "ideal pre-release burn. No burn time, stage restart or attitude constraint is applied",
             "to this single-event calculation.", "",
             "| Option | Relative release m/s | Installed device kg | Host preburn m/s | Ideal host propellant kg | Fuel left kg |",
             "|:--|--:|--:|--:|--:|--:|"]
    for x in one:
        lines.append(f"| {x['option']} | {x['release_speed_m_s']:.3f} | {x['installed_device_kg']:.3f} | "
                     f"{x['host_preburn_m_s']:.3f} | {x['ideal_propellant_kg']:.3f} | {x['fuel_after_event_kg']:.3f} |")
    lines += ["", "The finite-force speed is an optimistic geometry-only upper bound; the",
              "historical 16.029 m/s is contradicted by the finite-array screen and retained",
              "only to show how the old assumption changes the comparison. The spring figure",
              "is a class assumption, not an exact flight dispenser. The result does not price",
              "power, risk, launch mass value, provider integration or payload propulsion hardware.", "",
              "## Twelve-release finite-burn reference", "",
              "The same existing P113-S12 optimizer is rerun with each installed device mass",
              "included in host dry mass. Every case has the same 20-minute release cadence,",
              "5 km target arc spacing and 18,000 s terminal epoch. Its 100 N thrust and",
              "continuous restart/pointing assumptions are reference values, not a selected host.", "",
              "| Option | Accepted prefix / 12 | First failing stage | 64-corner replay of accepted prefix |",
              "|:--|--:|--:|:--|"]
    for x in camp:
        fail = next((s["index"] for s in x["stages"] if not s["selected_accepted"]),None)
        lines.append(f"| {x['option']} | {x['completed_deliveries']} | {fail} | "
                     f"{x['passing_prefix_corners']}/{x['uncertainty_corners_run']} passing prefix corners |")
    lines += ["", "An optimizer failure means **no accepted trajectory was found under these",
              "seeds and constraints**. It does not prove that no trajectory exists. None of",
              "these cases delivers all twelve. Higher relative release speed can make a short",
              "spacing target harder, and the larger device increases host propellant burden.", "",
              "![Matched reference comparison](../figures/matched_mission_reference.png)", "",
              "## Open alternatives and decisions", ""]
    lines += [f"- {x}" for x in d["unmodeled_alternatives"]]
    lines += ["", "A final paper comparator still needs a named provider/payload, validated",
              "release operating range, real OTV/service terms, reliability, disposal and",
              "same-epoch covariance. The present calculation is an honest matched *reference*,",
              "not a commercial or flight advantage claim.", "",
              "Reproduce: `python analysis/matched_mission_reference.py` in an environment with the declared dependencies.",
              "Exact inputs, outputs and source hashes are in `analysis/results/matched_mission_reference.json`.", ""]
    return "\n".join(lines)


def plot(d):
    fig, (a,b) = plt.subplots(1,2,figsize=(10,4.2),dpi=150)
    labels=["Spring","Finite upper","Historical"]
    a.bar(labels,[x["completed_deliveries"] for x in d["finite_burn_campaign"]],color=["#526b78","#137f88","#aa6a38"])
    a.axhline(12,color="#a72d37",ls="--",lw=1,label="full manifest")
    a.set(ylabel="Accepted sequential deliveries / 12",ylim=(0,12.7),title="Same 12-target finite-burn screen")
    a.legend(fontsize=8)
    b.bar(labels,[x["ideal_propellant_kg"] for x in d["single_event"]],color=["#526b78","#137f88","#aa6a38"])
    b.set(ylabel="Ideal host propellant (kg)",title="Same one-release orbital target")
    fig.tight_layout();FIG.parent.mkdir(parents=True,exist_ok=True);fig.savefig(FIG);plt.close(fig)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    d=build();raw=json.dumps(d,indent=2)+"\n";prose=report(d)
    if args.check:
        okay=OUT.exists() and DOC.exists() and OUT.read_text()==raw and DOC.read_text()==prose
        print("matched mission current" if okay else "matched mission STALE")
        return 0 if okay else 1
    OUT.write_text(raw);DOC.write_text(prose);plot(d)
    assert all(abs(x["target_residual_m_s"])<1e-10 and x["reserve_screen_pass"] for x in d["single_event"])
    print("matched mission: accepted prefixes",[x["completed_deliveries"] for x in d["finite_burn_campaign"]])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
