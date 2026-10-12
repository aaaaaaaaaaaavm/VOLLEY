#!/usr/bin/env python3
"""Gen6 G0 surrogate mission and prototype requirement screen (stdlib only).

This is a requirements generator. It is not a selected payload, host, hardware
architecture, measured command range, customer demand, or completed campaign.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/results/gen6_g0_reference.json"
REPORT = ROOT / "validation/P128_gen6_g0_reference.md"
FIG = ROOT / "figures/gen6_g0_reference.svg"
P124 = ROOT / "analysis/results/precision_delivery_design_space.json"

MU = 3.986004418e14
R_EARTH = 6_378_137.0
ALTITUDE = 450_000.0
PAYLOAD = 4.0
COUNT = 4
HOST_DRY = 300.0
HOST_ISP = 220.0
FUEL_REFERENCE = 10.0
FUEL_RESERVE = 2.0
SPRING_PER_PAYLOAD = 6.0
SPRING_RELEASE = 2.5
G0 = 9.80665
STROKE = 1.3
STUDY_DEVICE = 30.0  # study mass for recoil correction, not a Gen6 estimate
AXIS_TARGETS_KM = (5.0, 10.0, 15.0, 20.0)
AXIS_TOLERANCE_KM = 1.0
TRIAL_ERROR_ALLOCATIONS = {
    "host_navigation": 0.10,
    "host_control_and_recoil": 0.10,
    "release_magnitude": 0.15,
    "release_direction_projection": 0.10,
    "epoch_propagation_tracking": 0.10,
}


def axis_increment(rise_km: float) -> float:
    r = R_EARTH + ALTITUDE
    rise = rise_km * 1000
    if rise < 0:
        raise ValueError("negative axis rise is outside the prograde screen")
    return math.sqrt(MU * (2/r - 1/(r+rise))) - math.sqrt(MU/r)


def inverse_axis_increment(dv: float) -> float:
    r = R_EARTH + ALTITUDE
    speed = math.sqrt(MU/r) + dv
    return (1 / (2/r - speed*speed/MU) - r) / 1000


def root(fn, lo: float, hi: float) -> float:
    if fn(lo) > 0 or fn(hi) < 0:
        raise ValueError("root outside bracket")
    for _ in range(90):
        mid = (lo+hi)/2
        if fn(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


def event(target: float, release: float, device: float, fuel: float) -> dict:
    """One ideal common-epoch host preburn followed by one release and recoil."""
    initial = HOST_DRY + device + COUNT*PAYLOAD + fuel
    ve = HOST_ISP*G0

    def residual(burn: float) -> float:
        before_release = initial*math.exp(-burn/ve)
        return burn + (1-PAYLOAD/before_release)*release - target

    if residual(0) > 0:
        return {"status": "RELEASE_OVERSHOOTS_WITH_ZERO_BURN",
                "zero_burn_excess_m_s": residual(0)}
    burn = root(residual, 0.0, target+release)
    return {"status": "IDEAL_ONE_EVENT_SOLVED", "preburn_m_s": burn,
            "propellant_used_kg": initial*(1-math.exp(-burn/ve)),
            "target_residual_m_s": residual(burn)}


def fuel_load(target: float, release: float, device: float) -> float:
    """Fuel for only one ideal event plus equal reserve; not four-shot sizing."""
    def residual(fuel: float) -> float:
        result = event(target, release, device, fuel)
        if result["status"] != "IDEAL_ONE_EVENT_SOLVED":
            raise ValueError("overspeed in fuel sizing")
        return fuel-FUEL_RESERVE-result["propellant_used_kg"]
    return root(residual, FUEL_RESERVE, 30.0)


def device_parity(target: float, release: float, spring_fuel: float) -> float:
    spring_proxy = COUNT*SPRING_PER_PAYLOAD + spring_fuel
    return root(lambda device: device+fuel_load(target, release, device)-spring_proxy,
                0.0, 100.0)


def build() -> dict:
    prior = json.loads(P124.read_text())
    if prior["inputs"]["altitude_m"] != ALTITUDE or prior["inputs"]["payload_kg"] != PAYLOAD:
        raise ValueError("P124 orbit or payload basis changed")
    host_mass = HOST_DRY+STUDY_DEVICE+COUNT*PAYLOAD+FUEL_REFERENCE
    orbit = []
    for rise in AXIS_TARGETS_KM:
        dv = axis_increment(rise)
        margin = min(dv-axis_increment(rise-AXIS_TOLERANCE_KM),
                     axis_increment(rise+AXIS_TOLERANCE_KM)-dv)
        release_no_burn = dv/(1-PAYLOAD/host_mass)
        orbit.append(dict(axis_rise_km=rise, axis_band_km=AXIS_TOLERANCE_KM,
                          ideal_inertial_tangential_increment_m_s=dv,
                          all_error_tangential_margin_m_s=margin,
                          no_burn_relative_speed_at_study_mass_m_s=release_no_burn,
                          ideal_mean_acceleration_g=release_no_burn**2/(2*STROKE*G0),
                          ideal_payload_kinetic_J=.5*PAYLOAD*release_no_burn**2))
    target = orbit[-1]["ideal_inertial_tangential_increment_m_s"]
    spring_device = COUNT*SPRING_PER_PAYLOAD
    spring_fuel = fuel_load(target, SPRING_RELEASE, spring_device)
    alternatives = []
    for release in (SPRING_RELEASE, 3.0, 6.0, 11.2):
        parity = device_parity(target, release, spring_fuel)
        case = event(target, release, parity, fuel_load(target, release, parity))
        alternatives.append(dict(relative_release_m_s=release,
                                 max_device_kg_for_one_event_mass_proxy_parity=parity,
                                 one_event_fuel_at_parity_kg=fuel_load(target, release, parity),
                                 ideal_host_preburn_at_parity_m_s=case["preburn_m_s"]))
    first_article = dict(payload_surrogate_kg=PAYLOAD, command_range_m_s=[3.0,6.0],
                         ideal_max_mean_g_at_6_m_s=6**2/(2*STROKE*G0),
                         payload_kinetic_J_at_6_m_s=.5*PAYLOAD*6**2,
                         ideal_host_reaction_impulse_Ns_at_6_m_s=PAYLOAD*6,
                         status="PROPOSED_MEASUREMENT_RANGE_NOT_SELECTED_HARDWARE_OR_CUSTOMER_REQUIREMENT")
    return dict(evidence_class="SURROGATE_G0_REQUIREMENTS_SCREEN_NOT_CUSTOMER_OR_PROVIDER_APPROVAL",
                provenance=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                p124_sha256=hashlib.sha256(P124.read_bytes()).hexdigest()),
                inputs=dict(host_base_dry_kg=HOST_DRY,payload_count=COUNT,payload_each_kg=PAYLOAD,
                            start_altitude_km=ALTITUDE/1000,starting_fuel_kg=FUEL_REFERENCE,
                            one_event_fuel_reserve_kg=FUEL_RESERVE,host_isp_s=HOST_ISP,
                            spring_device_per_payload_kg=SPRING_PER_PAYLOAD,
                            spring_release_m_s=SPRING_RELEASE,study_device_for_recoil_kg=STUDY_DEVICE,
                            study_stroke_m=STROKE,axis_tolerance_km=AXIS_TOLERANCE_KM),
                target_states=orbit,trial_tangential_error_allocations_m_s=TRIAL_ERROR_ALLOCATIONS,
                trial_error_sum_m_s=sum(TRIAL_ERROR_ALLOCATIONS.values()),
                one_event_20km_comparator=dict(spring_device_kg=spring_device,
                                               spring_one_event_fuel_kg=spring_fuel,
                                               spring_device_plus_fuel_kg=spring_device+spring_fuel,
                                               alternatives=alternatives),
                first_article=first_article,
                exclusions=["no named spacecraft, customer, host, provider ICD or signed acceptance",
                            "semimajor axis only; no full state/covariance, plane, along-track or disposal target",
                            "no sequential four-shot or twelve-shot campaign, attitude, collision or duty model",
                            "no selected Gen6 motor, source, feed, restraint, brake, thermal design or mass",
                            "spring 6 kg per 3U and 2.5 m/s are class study values, not supplier quote",
                            "mass parity is a resource benchmark, not a price or product acceptance criterion"])


def report(d: dict) -> str:
    rows = d["target_states"]
    options = d["one_event_20km_comparator"]["alternatives"]
    lines = ["# P128 — Gen6 G0 surrogate mission and first-article requirement screen", "",
             "**Evidence class:** preliminary, reproducible requirement calculation. No customer, provider, hardware or delivery capability has approved it.", "",
             "Four identical 4 kg 3U payload surrogates start from a 450 km circular orbit on an assumed 300 kg base host. They are assigned distinct **immediate semimajor-axis rise targets** at one reference epoch. This is a requirements screen, **not** a four-release trajectory: the host and payload states after each event, collision avoidance and disposal have not been propagated.", "",
             "| Axis-rise target | Ideal inertial prograde increment | No-burn relative release at 30 kg study device | ±1 km axis margin if all error is tangential | Ideal mean load over 1.3 m |",
             "|--:|--:|--:|--:|--:|" ]
    lines += [f"| {r['axis_rise_km']:.0f} km | {r['ideal_inertial_tangential_increment_m_s']:.3f} m/s | {r['no_burn_relative_speed_at_study_mass_m_s']:.3f} m/s | {r['all_error_tangential_margin_m_s']:.3f} m/s | {r['ideal_mean_acceleration_g']:.2f} g |" for r in rows]
    lines += ["", "The 30 kg device is **only a recoil calculation input**, not a CAD or mass estimate. A host burn can replace some relative speed. The ideal mean load excludes force ripple, rail contact and release shock. The ±1 km axis tolerance is a deliberately loose trial band; it does not define a complete delivered orbital state.", "",
              "## Error allocation trial", "",
              "At the 20 km endpoint, the smaller-side tangential margin is "
              f"{rows[-1]['all_error_tangential_margin_m_s']:.3f} m/s. The following **absolute worst-case trial allocations** sum to "
              f"{d['trial_error_sum_m_s']:.2f} m/s: host navigation 0.10, host control/recoil 0.10, release magnitude 0.15, release direction projection 0.10, and epoch/propagation/tracking 0.10 m/s. This leaves only "
              f"{rows[-1]['all_error_tangential_margin_m_s']-d['trial_error_sum_m_s']:.3f} m/s in this one-dimensional screen. They are proposed budgets to challenge, **not measured 3σ performance, a covariance budget, or an approved requirement**. Cross-track, radial, along-track, collision and disposal limits remain open.", "",
              "## What the one-event mass proxy permits", "",
              "A spring-class comparator uses four assumed 6 kg units at 2.5 m/s. Both sides carry the same 300 kg base host, four payloads, 220 s host Isp, ideal host preburn and 2 kg fuel reserve. Fuel is re-solved for **one 20 km event only**, so these values must not size a four-shot tank.", "",
              "| Relative release | Maximum device for equal device + one-event fuel | Fuel at parity | Host preburn at parity |",
              "|--:|--:|--:|--:|" ]
    lines += [f"| {o['relative_release_m_s']:.1f} m/s | {o['max_device_kg_for_one_event_mass_proxy_parity']:.2f} kg | {o['one_event_fuel_at_parity_kg']:.3f} kg | {o['ideal_host_preburn_at_parity_m_s']:.3f} m/s |" for o in options]
    lines += ["", f"The spring-class device is {d['one_event_20km_comparator']['spring_device_kg']:.1f} kg; its one-event loaded fuel is {d['one_event_20km_comparator']['spring_one_event_fuel_kg']:.3f} kg. Release impulse buys only a small mass allowance here. **Mass parity is a benchmark, not a necessary product condition**: a buyer could pay for delivery accuracy, schedule or payload-side savings, but none has been demonstrated or priced. A four-payload Gen6 design should not inherit Gen5's 126.562 kg ledger or quietly count an integrated host structure as mass-free.", "",
              "## First instrumented article decision", "",
              "Propose a restrained, reusable-carrier **single-payload 4 kg dummy** rig with commanded 3–6 m/s release and instrumented current, force, speed/vector, contact, brake temperature and host reaction. This is a first measurement range; it does not promise the 11.3 m/s no-burn 20 km endpoint or a sequential feeder. At 6 m/s over a fully usable 1.3 m ideal stroke, mean load is "
              f"{d['first_article']['ideal_max_mean_g_at_6_m_s']:.2f} g and payload kinetic energy is {d['first_article']['payload_kinetic_J_at_6_m_s']:.0f} J before losses. Mechanical containment and an abort state must precede powered shots. A four-slot feed/retention prototype follows only after this single-payload model and test agree within declared bands. Keep 1 km/s in a separate payload/stroke research branch.", "",
              "**G0 disposition: partial, not passed.** The state is only semimajor axis and the host, payload, interface authority, buyer, deadline, full error covariance, disposal and alternatives' priced terms are unselected. The next decision is to obtain or openly surrogate those inputs before promoting an architecture.", "",
              "![Gen6 G0 target and mass screen](../figures/gen6_g0_reference.svg)", "",
              "Reproduce with `python3 analysis/gen6_g0_reference.py`; `--check` verifies the captured data, report and vector figure. P124's result hash is recorded in the JSON.", ""]
    return "\n".join(lines)


def figure(d: dict) -> str:
    rows=d["target_states"]
    opts=d["one_event_20km_comparator"]["alternatives"]
    circles="".join(f'<circle cx="{85+30*r["no_burn_relative_speed_at_study_mass_m_s"]:.1f}" cy="{125+i*53}" r="7" fill="#087e91"/><text x="40" y="{130+i*53}" font-size="16">{r["axis_rise_km"]:.0f} km</text><text x="{105+30*r["no_burn_relative_speed_at_study_mass_m_s"]:.1f}" y="{130+i*53}" font-size="15">{r["no_burn_relative_speed_at_study_mass_m_s"]:.2f} m/s</text>' for i,r in enumerate(rows))
    bars="".join(f'<text x="520" y="{130+i*53}" font-size="15">{o["relative_release_m_s"]:.1f} m/s</text><rect x="608" y="{112+i*53}" width="{6*o["max_device_kg_for_one_event_mass_proxy_parity"]:.1f}" height="26" fill="#b36b3d"/><text x="{619+6*o["max_device_kg_for_one_event_mass_proxy_parity"]:.1f}" y="{130+i*53}" font-size="15">{o["max_device_kg_for_one_event_mass_proxy_parity"]:.2f} kg</text>' for i,o in enumerate(opts))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="410" viewBox="0 0 1000 410">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="35" y="40" font-size="22" font-weight="bold">Gen6 G0 · surrogate state targets and mass boundary</text>'
            '<text x="35" y="72" font-size="14">Four 4 kg 3U payloads · 450 km circular start · one-event resource proxy</text>'
            '<text x="35" y="100" font-size="16" font-weight="bold">No-burn release for axis rise</text>'
            '<text x="515" y="100" font-size="16" font-weight="bold">Device mass at one-event spring parity</text>'
            +circles+bars+
            '<text x="35" y="375" font-size="13">All results are ideal, input-dependent requirements screens; no selected Gen6 hardware or customer mission.</text></svg>\n')


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    data=build()
    for row in data["target_states"]:
        if abs(inverse_axis_increment(row["ideal_inertial_tangential_increment_m_s"])-row["axis_rise_km"])>1e-7:
            raise AssertionError("two-body inverse identity changed")
    if not all(row["all_error_tangential_margin_m_s"]>data["trial_error_sum_m_s"] for row in data["target_states"]):
        raise AssertionError("trial tangential error allocations exceed target margin")
    result=json.dumps(data,indent=2)+"\n"
    prose=report(data)
    svg=figure(data)
    if args.check:
        if not all(p.exists() and p.read_text()==content for p,content in ((OUT,result),(REPORT,prose),(FIG,svg))):
            raise AssertionError("P128 committed artifacts are stale")
        print("P128 G0 reference: result, report and figure current")
    else:
        OUT.write_text(result)
        REPORT.write_text(prose)
        FIG.write_text(svg)
        print("P128 G0 reference generated")


if __name__=="__main__":
    main()
