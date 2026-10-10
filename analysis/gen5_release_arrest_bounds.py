"""P127 conservation bounds for the finite-force Gen5 shot and provisional brake.

No eddy-current force law, release contact, host attitude or thermal partition is
inferred. These are necessary energy/momentum and mean-force calculations only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORCE = ROOT / "analysis/results/gen5_finite_force_map.json"
PARAM = ROOT / "cad/parameters.json"
MASS = ROOT / "analysis/results/mass_properties.json"
RESULT = ROOT / "analysis/results/gen5_release_arrest_bounds.json"
REPORT = ROOT / "validation/P127_gen5_release_arrest_bounds.md"
FIGURE = ROOT / "figures/gen5_release_arrest_bounds.svg"
G0 = 9.80665
PAYLOAD = 4.0
BASE_HOST = 300.0
FUEL = 10.0
COUNT = 12


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    raw = {"force": FORCE.read_bytes(), "parameters": PARAM.read_bytes(),
           "mass": MASS.read_bytes()}
    force, param, mass = (json.loads(raw[k]) for k in ("force","parameters","mass"))
    brake = param["groups"]["brake"]
    speed = force["ideal_finite_stator_exit_upper_m_s"]
    sled = force["moving_mass_kg"] - PAYLOAD
    if abs(sled-mass["sled_kg"]) > .01:
        raise RuntimeError("moving mass and CAD-derived sled ledger disagree")
    length = (brake["x_end"]-brake["x_start"])/1000
    if length <= 0:
        raise RuntimeError("brake length must be positive")
    sled_energy = .5*sled*speed**2
    sled_impulse = sled*speed
    payload_impulse = PAYLOAD*speed
    pre_host = BASE_HOST+mass["dry_kg"]+FUEL+COUNT*PAYLOAD
    # A first-order fixed-frame momentum allocation, not a coupled host shot.
    launch_host_reaction = (sled+PAYLOAD)*speed/pre_host
    brake_host_recovery = sled_impulse/pre_host
    payload_host_net = payload_impulse/pre_host
    cases = {}
    for name,distance in (("provisional_brake_full_length",length),
                          ("half_length_effective",length/2),
                          ("quarter_length_effective",length/4)):
        mean_force=sled_energy/distance
        decel=speed**2/(2*distance)
        cases[name]=dict(effective_stop_m=distance, necessary_mean_force_N=mean_force,
                         necessary_mean_deceleration_g=decel/G0,
                         constant_deceleration_stop_time_ms=2000*distance/speed,
                         below_provisional_200g_mean_cap=decel/G0<=brake["arrest_g_cap"])
    shortest=speed**2/(2*brake["arrest_g_cap"]*G0)
    data=dict(evidence_class="NECESSARY_CONSERVATION_BOUNDS_NOT_BRAKE_OR_HOST_VALIDATION",
              source_sha256={k:hashlib.sha256(v).hexdigest() for k,v in raw.items()},
              source_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              assumptions=dict(speed_m_s=speed,
                               speed_status="P118 ideal phase finite-force upper screen, not achieved",
                               sled_kg=sled,payload_kg=PAYLOAD,host_before_kg=pre_host,
                               modeled_device_kg=mass["dry_kg"],
                               provisional_brake_start_mm=brake["x_start"],
                               provisional_brake_end_mm=brake["x_end"],
                               provisional_peak_deceleration_cap_g=brake["arrest_g_cap"],
                               no_regeneration_or_friction_credit=True),
              sled_kinetic_J=sled_energy,
              twelve_shot_sled_kinetic_J=COUNT*sled_energy,
              sled_arrest_impulse_Ns=sled_impulse,
              payload_departure_impulse_Ns=payload_impulse,
              first_order_host_reaction_during_acceleration_m_s=launch_host_reaction,
              first_order_host_recovery_during_sled_arrest_m_s=brake_host_recovery,
              first_order_net_host_recoil_m_s=payload_host_net,
              stop_distance_for_200g_mean_m=shortest,
              cases=cases,
              limitations=["constant mean braking force is not an eddy-current force curve",
                           "200g is a provisional sled design cap, not a payload qualification limit",
                           "no payload/sled contact, tip-off, structural compliance or friction",
                           "no brake heat distribution, cooling or repeated-shot timing",
                           "host impulse is first-order and excludes attitude, mounting moment and propellant burns",
                           "no failure or abort load case"])
    rows=[f"| {name.replace('_',' ')} | {v['effective_stop_m']*1000:.1f} | {v['necessary_mean_force_N']:.0f} | {v['necessary_mean_deceleration_g']:.1f} |"
          for name,v in cases.items()]
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="280" viewBox="0 0 820 280"><rect width="100%" height="100%" fill="#f6f9fb"/><text x="25" y="35" font-size="20" font-weight="bold">P127 · necessary mean sled arrest load</text>'''
    for i,(name,v) in enumerate(cases.items()):
        y=75+i*58
        svg+=f'<text x="25" y="{y+17}" font-size="14">{name.replace("_"," ")}</text><rect x="315" y="{y}" width="{v["necessary_mean_deceleration_g"]*4:.1f}" height="23" fill="#b96949"/><text x="{325+v["necessary_mean_deceleration_g"]*4:.1f}" y="{y+17}" font-size="14">{v["necessary_mean_deceleration_g"]:.1f} g mean</text>'
    svg+='<text x="25" y="255" font-size="12">Ideal finite-force speed; mean-load lower bound, not peak brake or payload load.</text></svg>\n'
    report="\n".join([
        "# P127 — ideal finite-force release and arrest bounds", "",
        "**Necessary momentum and energy screen only. No brake, host or payload qualification.**", "",
        f"P118's ideal {speed:.3f} m/s speed and the {sled:.3f} kg CAD-derived sled",
        f"imply {sled_energy:.1f} J of sled kinetic energy and {sled_impulse:.1f} N·s",
        f"of sled arrest impulse, if no regeneration is credited. Twelve identical shots",
        f"would put {COUNT*sled_energy:.1f} J into arrest pathways before cooling or",
        "energy recovery. This does not establish where heat is deposited.", "",
        f"The provisional CAD brake runs from {brake['x_start']} to {brake['x_end']} mm",
        f"({length*1000:.0f} mm). Required **mean** force and deceleration are:", "",
        "| Effective stop corridor | Length (mm) | Mean force (N) | Mean deceleration (g) |",
        "|:--|--:|--:|--:|",*rows,"",
        f"At the provisional {brake['arrest_g_cap']:.0f} g sled cap, constant deceleration",
        f"would need at least {shortest*1000:.1f} mm. A mean below 200 g cannot prove",
        "a peak below 200 g: eddy entry, speed dependence, mechanical stop and",
        "compliance must be solved on the same CAD revision.", "",
        f"For the declared {pre_host:.3f} kg first-shot reference mass, a fixed-frame",
        f"momentum screen gives {launch_host_reaction:.3f} m/s host reaction during",
        f"payload-plus-sled acceleration, {brake_host_recovery:.3f} m/s recovery during",
        f"sled arrest, and {payload_host_net:.3f} m/s net from payload departure.",
        "This is neither an orbit prediction nor an attitude/stability analysis;",
        "mounting lever arm, host inertia, release contact and host control are omitted.", "",
        "![P127 mean brake-load bounds](../figures/gen5_release_arrest_bounds.svg)", "",
        "Reproduce with `python3 analysis/gen5_release_arrest_bounds.py`; `--check`",
        "compares JSON, report and figure. The source hashes bind the calculation",
        "to the committed P118 result, CAD brake dimensions and mass ledger.", "",
    ])
    rendered=json.dumps(data,indent=2)+"\n"
    if args.check:
        ok=all(p.exists() and p.read_text()==s for p,s in
               ((RESULT,rendered),(REPORT,report),(FIGURE,svg)))
        print("P127 current" if ok else "P127 STALE")
        return 0 if ok else 1
    RESULT.write_text(rendered)
    REPORT.write_text(report)
    FIGURE.write_text(svg)
    print(f"sled energy {sled_energy:.1f} J; full-brake mean {cases['provisional_brake_full_length']['necessary_mean_deceleration_g']:.1f} g")


if __name__ == "__main__":
    raise SystemExit(main())
