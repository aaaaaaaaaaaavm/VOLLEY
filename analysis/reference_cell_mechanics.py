"""P92-S2: declared analytical spring/pusher/catcher envelope."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

from operational_uncertainty import load_s4, selected_campaign

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis/results/reference_cell_mechanics.json"
DOC = ROOT / "docs/REFERENCE_CELL_MECHANICS.md"
G = 9.80665


def case(payload, pusher, speed, stroke, ratio, friction):
    if payload <= 0 or pusher <= 0 or speed <= 0 or stroke <= 0 or not 0 <= ratio < 1 or friction < 0:
        raise ValueError("invalid mechanical inputs")
    mass = payload+pusher
    work = 0.5*mass*speed**2 + friction*stroke
    initial_compression = stroke/(1-ratio)
    final_compression = initial_compression-stroke
    stiffness = 2*work/(initial_compression**2-final_compression**2)
    start_force, end_force = stiffness*initial_compression, stiffness*final_compression
    initial_energy = 0.5*stiffness*initial_compression**2
    integrated_work = (start_force+end_force)*stroke/2
    reconstructed_speed = math.sqrt(2*(integrated_work-friction*stroke)/mass)
    peak_g = (start_force-friction)/(mass*G)
    end_g = (end_force-friction)/(mass*G)
    catcher_energy = 0.5*pusher*speed**2
    reasons = []
    if peak_g > 10:
        reasons.append("PEAK_ACCELERATION_ABOVE_STUDY_CEILING")
    if end_g < 0:
        reasons.append("CONTACT_ASSUMPTION_FAILS_AT_EXIT")
    return {
        "payload_kg":payload, "pusher_kg":pusher, "speed_m_s":speed,
        "stroke_m":stroke, "force_ratio":ratio, "friction_n":friction,
        "spring_work_j":work, "stiffness_n_m":stiffness,
        "initial_compression_m":initial_compression, "final_compression_m":final_compression,
        "peak_latch_force_n":start_force, "end_spring_force_n":end_force,
        "initial_stored_energy_j":initial_energy,
        "peak_net_acceleration_g":peak_g, "end_net_acceleration_g":end_g,
        "work_residual_j":integrated_work-work,
        "speed_residual_m_s":reconstructed_speed-speed,
        "catcher_energy_j":catcher_energy,
        "catcher_average_force_n":{str(s):catcher_energy/s for s in (0.005,0.01,0.02)},
        "charging_energy_j":{str(e):initial_energy/e for e in (0.5,0.7,0.9)},
        "twelve_shot_initial_stored_energy_j":12*initial_energy,
        "twelve_shot_charging_energy_j":{str(e):12*initial_energy/e for e in (0.5,0.7,0.9)},
        "feasible":not reasons, "rejection_reasons":reasons,
        "verification_passed":math.isclose(work, integrated_work, rel_tol=1e-10, abs_tol=1e-9)
            and abs(reconstructed_speed-speed)<=1e-9
            and math.isclose(catcher_energy/(0.5*payload*speed**2), pusher/payload, rel_tol=1e-12),
    }


def build():
    _, _, candidate = selected_campaign(load_s4())
    u = candidate["events"][0]["separation"]["relative_velocity_m_s"]
    speed = math.hypot(*u)
    rows = [case(4.0,p,speed,s,r,f) for p,s,r,f in itertools.product(
        (0.1,0.25,0.5),(0.08,0.12,0.16,0.24),(0.0,0.25,0.5,0.75),(0.0,2.0,5.0))]
    limit = case(4.0,0.25,speed,speed**2/(10*G),0.0,0.0)
    sources = ["analysis/reference_cell_mechanics.py","analysis/results/manifest_timing.json",
               "validation/P92_S2_reference_cell_mechanics.md"]
    return {"study":"P92-S2", "evidence":"ANALYTICAL_SIZING_SCREEN", "open_items":["P92"],
        "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
        "speed_m_s":speed, "payload_kg":4.0, "case_count":len(rows),
        "feasible_count":sum(x["feasible"] for x in rows), "cases":rows,
        "zero_preload_minimum_stroke_m":speed**2/(10*G),
        "constant_acceleration_ideal_stroke_m":speed**2/(20*G),
        "verification_passed":len(rows)==144 and all(x["verification_passed"] for x in rows)
            and abs(limit["peak_net_acceleration_g"]-10)<1e-12}


def report(d):
    feasible=[x for x in d["cases"] if x["feasible"]]
    out=["# Reference-cell spring, pusher and catcher screen", "",
        "I evaluate a linear unloading spring at the S4 study point. No spring, latch, motor or damper is selected. P92 remains open.", "",
        f"**{d['feasible_count']} of {d['case_count']} declared mechanical cases meet the analytical 10 g/contact screen.** Numerical verification: **{'PASS' if d['verification_passed'] else 'FAIL'}**.", "",
        f"The relative-speed study point is {d['speed_m_s']:.6f} m/s for 4 kg. With zero friction and zero end preload, the spring requires at least **{1000*d['zero_preload_minimum_stroke_m']:.1f} mm**, twice the **{1000*d['constant_acceleration_ideal_stroke_m']:.1f} mm** constant-force ideal. Calling 106.5 mm a spring design would miss that distinction.", "",
        "| Quantity across feasible grid | Minimum | Maximum |", "|---|---:|---:|"]
    for key,label in [("stroke_m","Working stroke (m)"),("initial_compression_m","Initial spring compression (m)"),
        ("peak_latch_force_n","Peak latch force (N)"),("stiffness_n_m","Spring stiffness (N/m)"),
        ("initial_stored_energy_j","Initial stored energy (J)"),("catcher_energy_j","Pusher catcher energy (J)")]:
        vals=[x[key] for x in feasible]
        out.append(f"| {label} | {min(vals):.6g} | {max(vals):.6g} |")
    out += ["", "These extrema belong to different cases. They must not be assembled into an imaginary best-of-everything design.", "",
        "## What changed in the design question", "",
        "A higher end preload flattens force and can shorten working stroke, but increases retained compression and initial stored energy. The latch carries spring force even before a shot. The local catcher must absorb the pusher's kinetic energy after payload departure; its average force is not a peak shock prediction. Negative endpoint net force invalidates the assumed continuous pusher contact and is retained as a rejected case.", "",
        "The JSON includes all rejected cases, 5/10/20 mm catcher stopping distances and assumed 50/70/90% charging efficiency, with 12-shot totals and no recovery credit. This is fixed-frame internal sizing: host recoil energy and the conversion from internal pusher speed to payload/host relative speed remain to be coupled to the mission model. Frame, spring, motor, gearbox, latch, catcher, retention, controls, harness and thermal mass remain unallocated. Energy is not a mass estimate.", "",
        "## Coupon needed next", "",
        "Measure force versus travel through the declared stroke, preload after dwell and repeated charging, breakaway/sliding force versus temperature, latch shock, pusher/payload separation, exit speed, angular rate and catcher peak/rebound. Use independent position/time measurements and calibrate their uncertainty before comparing repeatability with a mission allocation. S5's local allowances are not approved hardware tolerances.", "",
        "Reject a candidate if the measured envelope violates its 10 g study ceiling, loses required contact, jams, relatches into the payload, ejects retained hardware or lets catcher rebound recontact it. Flight ascent retention, wear life, contamination and environmental acceptance require separately frozen specifications.", "",
        "[Declared criteria](../validation/P92_S2_reference_cell_mechanics.md) · [Complete result](../analysis/results/reference_cell_mechanics.json) · [Reference architecture](GEN6_REFERENCE_ARCHITECTURE.md)", "",
        "Reproduce: `python analysis/reference_cell_mechanics.py --check`.", ""]
    return "\n".join(out)


def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args()
    d=build(); outputs={RESULT:json.dumps(d,sort_keys=True,indent=2)+"\n",DOC:report(d)}
    if a.check:
        from campaign_allocation import numerical_match
        stored=json.loads(RESULT.read_text())
        if not numerical_match(stored,d) or DOC.read_text()!=report(stored):
            raise SystemExit("P92-S2 outputs stale")
    else:
        for path,content in outputs.items():path.write_text(content)
    if not d["verification_passed"]:raise SystemExit("P92-S2 verification failed; retain evidence")
    print(f"P92-S2: {d['feasible_count']}/144 feasible analytical cases; verification PASS; P92 open")

if __name__=="__main__":main()
