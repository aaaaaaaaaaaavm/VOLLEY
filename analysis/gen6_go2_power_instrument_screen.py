#!/usr/bin/env python3
"""P132: first-article pulse-source and measurement necessary bounds.

All efficiencies, voltages, timing and baseline values are declared study
inputs. This does not model a winding, select a vendor part or rate hardware.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P131=ROOT/"analysis/results/gen6_go2_article_bounds.json"
RESULT=ROOT/"analysis/results/gen6_go2_power_instrument_screen.json"
REPORT=ROOT/"validation/P132_gen6_go2_power_instrument_screen.md"
FIGURE=ROOT/"figures/gen6_go2_power_sensitivity.svg"

EFFICIENCIES=(0.05,0.10,0.20)
BUS_MAX_V=96.0
BUS_MIN_V=72.0
PHOTOGATE_BASELINE_M=0.2
SPEED_MEASUREMENT_GOAL_M_S=0.01


def build():
    source=json.loads(P131.read_text())
    cases={}
    for name,candidate in source["candidates"].items():
        speeds=[]
        for mechanical in candidate["speed_bounds"]:
            v=mechanical["speed_m_s"]
            energy=mechanical["ideal_total_moving_kinetic_J"]
            time=2*1.3/v
            peak_mechanical_power=mechanical["ideal_mean_drive_force_N"]*v
            samples=[]
            for eta in EFFICIENCIES:
                input_energy=energy/eta
                samples.append(dict(assumed_end_to_end_efficiency=eta,
                                    required_bus_energy_at_least_J=input_energy,
                                    loss_heat_somewhere_in_chain_J=input_energy-energy,
                                    four_identical_shots_input_J=4*input_energy,
                                    four_identical_shots_loss_heat_J=4*(input_energy-energy),
                                    ideal_min_capacitance_F=2*input_energy/(BUS_MAX_V**2-BUS_MIN_V**2),
                                    mean_bus_power_lower_bound_W=input_energy/time,
                                    end_of_stroke_bus_power_lower_bound_W=peak_mechanical_power/eta,
                                    bus_current_at_72V_lower_bound_A=peak_mechanical_power/(eta*BUS_MIN_V)))
            # Two ideal optical gates; independent position-calibration and
            # synchronization errors must fit inside the same speed budget.
            interval=PHOTOGATE_BASELINE_M/v
            timing_budget=SPEED_MEASUREMENT_GOAL_M_S*PHOTOGATE_BASELINE_M/(v*v)
            distance_budget=SPEED_MEASUREMENT_GOAL_M_S*PHOTOGATE_BASELINE_M/v
            speeds.append(dict(speed_m_s=v,ideal_constant_acceleration_shot_time_s=time,
                               ideal_peak_mechanical_power_W=peak_mechanical_power,
                               gate_interval_s=interval,
                               gate_timing_error_if_sole_source_us=timing_budget*1e6,
                               gate_baseline_error_if_sole_source_mm=distance_budget*1000,
                               efficiency_scenarios=samples))
        cases[name]=dict(captured_carrier_kg=candidate["carrier_kg"],cases=speeds)
    return dict(evidence_class="GEN6_G2_NECESSARY_SOURCE_AND_SENSOR_BOUNDS_NO_SELECTED_HARDWARE",
                provenance=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                p131_result_sha256=hashlib.sha256(P131.read_bytes()).hexdigest()),
                assumptions=dict(end_to_end_efficiencies=EFFICIENCIES,
                                 voltage_swing_V=[BUS_MAX_V,BUS_MIN_V],
                                 capacitor_model="0.5*C*(Vmax^2-Vmin^2); 100% usable capacitor energy, no ESR or inverter limits",
                                 optical_gate_baseline_m=PHOTOGATE_BASELINE_M,
                                 illustrative_speed_measurement_resolution_m_s=SPEED_MEASUREMENT_GOAL_M_S,
                                 same_dummy_shots_for_heat_screen=4),
                candidates=cases,
                exclusions=["Efficiencies are scenarios, not measured or supported by motor/circuit selection",
                            "Ideal average and end-of-stroke power assume constant acceleration; actual force and source peaks can be higher",
                            "Capacitance and bus-current values omit ESR, ripple, switching, reactive current, derating, aging, thermal limits and recharge",
                            "Heat is an aggregate energy difference; local component temperatures and spacecraft magnetic/EMI exposure are unknown",
                            "Optical gate timing and baseline values are single-error budgets, not calibrated instrument specifications or 3-D vector accuracy",
                            "No launch or bench operation authorized by this calculation"])


def report(d):
    rows=[]
    for name,candidate in d["candidates"].items():
        for trial in candidate["cases"]:
            for scenario in trial["efficiency_scenarios"]:
                rows.append(f"| {name} | {trial['speed_m_s']:.0f} | {scenario['assumed_end_to_end_efficiency']:.0%} | {scenario['required_bus_energy_at_least_J']:.0f} | {scenario['ideal_min_capacitance_F']:.3f} | {scenario['end_of_stroke_bus_power_lower_bound_W']:.0f} | {scenario['bus_current_at_72V_lower_bound_A']:.1f} | {scenario['four_identical_shots_loss_heat_J']:.0f} |")
    gate=[]
    for trial in d["candidates"]["A"]["cases"]:
        gate.append(f"| {trial['speed_m_s']:.0f} m/s | {trial['ideal_constant_acceleration_shot_time_s']:.3f} s | {trial['gate_interval_s']*1000:.2f} ms | {trial['gate_timing_error_if_sole_source_us']:.1f} µs | {trial['gate_baseline_error_if_sole_source_mm']:.3f} mm |")
    return "\n".join([
        "# P132 — Gen6 Go 2 source and instrument bounds", "",
        "**Status:** necessary algebraic source and metrology screen for the P131 inert 4 kg first article. No coil, inverter, capacitor, controller, brake or sensor is selected or rated; no shot has been fired.", "",
        "The FreeCAD candidates differ only slightly in moving material mass. For a constant-acceleration 1.3 m stroke, 3 and 6 m/s require about 0.867 and 0.433 s respectively. The table divides P131's total moving kinetic energy by **illustrative** 5/10/20% wall-to-kinetic efficiencies, then applies an ideal 96-to-72 V capacitor swing. Those voltages are a screening choice, **not** a selected Gen6 bus. Current is only the hypothetical DC bus power divided by 72 V; winding and switch currents can differ sharply.", "",
        "| Candidate | Exit m/s | Assumed efficiency | Minimum bus energy J | Ideal capacitor F | Ideal end-stroke bus W | Lower-bound 72 V bus A | Four identical shots' aggregate loss J |",
        "|:--|--:|--:|--:|--:|--:|--:|--:|",*rows,"",
        "At 6 m/s and 10% assumed efficiency, A's source would need at least **818 J**, an ideal **0.406 F** across this voltage swing and about **3.77 kW** at the stroke end under constant acceleration. Four identical shots would deposit roughly **2.94 kJ of loss somewhere in the drive chain**. No particular capacitor, winding or thermal path has been shown to survive these numbers. Actual peak power can exceed them with position-varying force, friction, handover, source sag or control action. The 200 mm carrier stop's roughly 10 J per shot is a separate local brake-heat concern.", "",
        "## Measurement floor for a future contained test", "",
        "With two ideal optical gates 200 mm apart, an **illustrative** 0.01 m/s scalar speed resolution has the following *single-source* timing and baseline-error ceilings. Real uncertainty must combine both gates, their positions, synchronization, alignment, event detection and calibration. No 3-D vector or tip-off accuracy is derived here.", "",
        "| Speed | Ideal shot duration | Gate interval | Timing error if sole source | Baseline error if sole source |",
        "|--:|--:|--:|--:|--:|",*gate,"",
        "A future test plan must capture synchronized voltage/current, carrier and payload position, exit speed/vector, rail contact, brake displacement/temperature and retained carrier status; choose sensor bandwidth from the fastest expected current/force and contact transients, which this screen does **not** resolve. The power-off safe state, containment and aborted-shot procedure need a separate reviewed design before any energized test.", "",
        "The [FreeCAD/STEP candidate record](../cad/gen6_first_article/README.md), [P131 mechanics](P131_gen6_go2_article_bounds.md) and [G1 issue](https://github.com/aaaaaaaaaaaavm/VOLLEY/issues/46) define the next model and hardware-selection evidence. A vendor component table must include part number, revision, mass, temperature and voltage/current/pulse ratings, ESR/inductance, material data and data-sheet link. No line should be marked selected from this calculation alone.", "",
        "![Illustrative source energy versus assumed efficiency](../figures/gen6_go2_power_sensitivity.svg)", "",
        "Reproduce with `python3 analysis/gen6_go2_power_instrument_screen.py --check`.", ""])


def figure(d):
    c=d["candidates"]["A"]["cases"][1]
    vals=c["efficiency_scenarios"]
    bars=[]
    for i,s in enumerate(vals):
        y=105+i*65
        width=s["required_bus_energy_at_least_J"]*0.36
        bars.append(f'<text x="25" y="{y+21}" font-size="17">{s["assumed_end_to_end_efficiency"]:.0%} efficiency</text>'
                    f'<rect x="210" y="{y}" width="{width:.1f}" height="30" fill="#087e91"/>'
                    f'<text x="{220+width:.1f}" y="{y+21}" font-size="16">{s["required_bus_energy_at_least_J"]:.0f} J</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="350" viewBox="0 0 1000 350">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="25" y="40" font-size="23" font-weight="bold">Gen6 Go 2 · 6 m/s first-article source screen</text>'
            '<text x="25" y="71" font-size="15">Candidate A · 4 kg dummy · assumed wall-to-kinetic efficiency</text>'
            +''.join(bars)+
            '<text x="25" y="322" font-size="14">Necessary bus energy only. No selected coil, inverter, capacitor, thermal path or rated speed.</text></svg>\n')


def equivalent(a,b):
    if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-5)
    return type(a) is type(b) and a==b


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    d=build()
    prose,graphic=report(d),figure(d)
    if args.check:
        if not RESULT.exists() or not equivalent(d,json.loads(RESULT.read_text())):raise AssertionError("P132 data stale")
        if REPORT.read_text()!=prose or FIGURE.read_text()!=graphic:raise AssertionError("P132 report/figure stale")
        print("P132 Gen6 source and instrument bounds current")
    else:
        RESULT.write_text(json.dumps(d,indent=2)+"\n")
        REPORT.write_text(prose)
        FIGURE.write_text(graphic)
        print("P132 Gen6 source and instrument bounds generated")


if __name__=="__main__":main()
