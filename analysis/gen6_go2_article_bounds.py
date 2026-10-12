#!/usr/bin/env python3
"""P131: necessary mechanics and mass bounds for Gen6 G1 envelope candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import gen6_matched_campaign as mission
import gen6_mixed_mission as orbit

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "cad/gen6_first_article/release/Gen6_G1_Envelope_Report.json"
PARAMS = ROOT / "cad/gen6_first_article/parameters.json"
MASS_LEDGER = ROOT / "cad/gen6_first_article/release/Gen6_G1_Partial_Mass_CG_Inertia.json"
RESULT = ROOT / "analysis/results/gen6_go2_article_bounds.json"
REPORT = ROOT / "validation/P131_gen6_go2_article_bounds.md"
FIGURE = ROOT / "figures/gen6_go2_mass_gate.svg"
G = 9.80665


def build():
    cad = json.loads(CAD.read_text())
    p = json.loads(PARAMS.read_text())
    mass_ledger = json.loads(MASS_LEDGER.read_text())
    events, _, targets = orbit.reference(20)
    spring = mission.case("spring", targets, events, 20)
    target_mass_proxy = spring["device_assumption_kg"] + spring["fuel_used_kg"]
    lo, hi = 0.0, 30.0
    for _ in range(16):
        mid = (lo + hi) / 2
        volley = mission.case("volley", targets, events, 20, volley_device=mid)
        if mid + volley["fuel_used_kg"] > target_mass_proxy:
            hi = mid
        else:
            lo = mid
    threshold = (lo + hi) / 2
    cases = {}
    for name, candidate in cad["candidates"].items():
        export = candidate["export"]
        for filename, digest in ((export["native"], export["native_sha256"]),
                                 (export["step"], export["step_sha256"])):
            actual = hashlib.sha256((CAD.parent / filename).read_bytes()).hexdigest()
            if actual != digest:
                raise AssertionError(f"FreeCAD/STEP artifact hash mismatch: {filename}")
        partial = candidate["partial_material_mass"]["fixed_and_carrier_kg"]
        carrier = candidate["partial_material_mass"]["captured_carrier_kg"]
        ledger = mass_ledger["candidates"][name]
        if abs(ledger["dry_partial_start"]["mass_kg"]-partial) > 1e-8:
            raise AssertionError("FreeCAD mass/CG/inertia ledger disagrees with envelope volume mass")
        if ledger["native_sha256"] != candidate["export"]["native_sha256"]:
            raise AssertionError("mass ledger belongs to a different native CAD file")
        for state in ("dry_partial_start", "loaded_assigned_dummy_start", "loaded_assigned_dummy_at_stroke_end"):
            if any(ledger[state]["inertia_about_cg_kg_m2"][axis][axis] <= 0 for axis in range(3)):
                raise AssertionError("nonphysical partial inertia")
        speeds = []
        for v in (3.0, 6.0):
            moving = p["payload_assigned_mass_kg"] + carrier
            stroke = p["stroke"] / 1000
            stop = p["brake_travel"] / 1000
            speeds.append(dict(speed_m_s=v, ideal_payload_kinetic_J=0.5*p["payload_assigned_mass_kg"]*v*v,
                               ideal_total_moving_kinetic_J=0.5*moving*v*v,
                               ideal_mean_drive_force_N=moving*v*v/(2*stroke),
                               ideal_mean_payload_acceleration_g=v*v/(2*stroke*G),
                               carrier_brake_energy_J=0.5*carrier*v*v,
                               ideal_mean_carrier_brake_force_N=carrier*v*v/(2*stop),
                               ideal_mean_carrier_brake_deceleration_g=v*v/(2*stop*G)))
        gap = candidate["cross_section"]["nominal_each_side_gap_mm"]
        linear_stack = 1.5  # declared study stack only
        yaw = []
        for deg in (0.2, 0.5, 0.7):
            sweep = p["payload_length_3u"] * math.tan(math.radians(deg))
            yaw.append(dict(angle_deg=deg, lateral_sweep_mm=sweep,
                            residual_mm=gap-linear_stack-sweep,
                            conditional_clear=gap-linear_stack-sweep > 0))
        cases[name] = dict(partial_structure_and_carrier_kg=partial,
                           carrier_kg=carrier,
                           partial_dry_cg_m=ledger["dry_partial_start"]["cg_m"],
                           assigned_dummy_combined_cg_start_m=ledger["loaded_assigned_dummy_start"]["cg_m"],
                           assigned_dummy_combined_cg_at_stroke_end_m=ledger["loaded_assigned_dummy_at_stroke_end"]["cg_m"],
                           unresolved_mass_allowance_kg=threshold-partial,
                           speed_bounds=speeds,
                           lateral_tolerance_screen=dict(nominal_side_gap_mm=gap,
                                                          assumed_linear_stack_mm=linear_stack,
                                                          cases=yaw,
                                                          maximum_yaw_deg_given_stack=math.degrees(math.atan((gap-linear_stack)/p["payload_length_3u"]))))
    return dict(evidence_class="GEN6_G1_NECESSARY_BOUNDS_NOT_SOURCEABLE_INSTALLED_DESIGN",
                provenance=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                cad_report_sha256=hashlib.sha256(CAD.read_bytes()).hexdigest(),
                                cad_parameters_sha256=hashlib.sha256(PARAMS.read_bytes()).hexdigest(),
                                mass_cg_inertia_ledger_sha256=hashlib.sha256(MASS_LEDGER.read_bytes()).hexdigest()),
                mission_proxy=dict(spring_device_assumption_kg=16,
                                   spring_host_fuel_kg=spring["fuel_used_kg"],
                                   max_volley_device_kg_for_device_plus_consumed_fuel_parity=threshold,
                                   comparison="P130 same four surrogate states and ideal burn schedule; 10 kg initial host fuel; device plus consumed fuel proxy, not launch manifest mass or price"),
                candidates=cases,
                exclusions=["No wound stator, source, switch, brake, restraints, bearings, harness, electronics, mounting, thermal hardware or qualified payload contact",
                            "FreeCAD masses use full rectangular proxies and assumed material densities, not a sourced BOM or weighed assembly",
                            "Constant-acceleration and stop-length bounds do not predict peak contact force, current, heating, tip-off or achievable release speed",
                            "Tolerance bands are assumed and do not include thermomechanical deflection or a payload-specific provider ICD",
                            "Mass parity uses P130's constructed target topology and ideal host burns; no customer service advantage is established"])


def report(data):
    a = data["candidates"]["A"]
    b = data["candidates"]["B"]
    r = ["# P131 — Gen6 Go 2 first-article necessary bounds", "",
         "**Status:** FreeCAD envelope-derived mass and analytic mechanics screen. Candidate A is a captured permanent-magnet carrier; B is a captured conductive-plate carrier. Both use a passive 4 kg 3U dummy, a shared guide and ideal 1.3 m drive stroke. Neither drive is selected or electrically rated.", "",
         "The [native FreeCAD and STEP review set](../cad/gen6_first_article/README.md) contains two editable primitive assemblies and STEP exports. Five sampled carrier/payload stroke positions have zero solid interference in the nominal envelope; this does not prove contact, swept-path, tolerance, launch-load or brake clearance under deflection.", "",
         "## Mission-derived installed-mass screen", "",
         f"The P130 spring-plus-host surrogate assumes a 16 kg spring device and consumes {data['mission_proxy']['spring_host_fuel_kg']:.4f} kg of host fuel. Re-solving the same ideal campaign over VOLLEY device mass gives a device-plus-consumed-fuel parity ceiling of **{data['mission_proxy']['max_volley_device_kg_for_device_plus_consumed_fuel_parity']:.3f} kg**. It is a narrow study proxy, not a purchase target or accepted host mass limit.", "",
         "| Candidate | FreeCAD partial frame, guide and carrier material | Captured carrier material | Remaining under P130 proxy ceiling |", "|:--|--:|--:|--:|",
         f"| A: PM carrier | {a['partial_structure_and_carrier_kg']:.3f} kg | {a['carrier_kg']:.3f} kg | {a['unresolved_mass_allowance_kg']:.3f} kg |",
         f"| B: conductive plate carrier | {b['partial_structure_and_carrier_kg']:.3f} kg | {b['carrier_kg']:.3f} kg | {b['unresolved_mass_allowance_kg']:.3f} kg |", "",
         "That remainder must cover the actual drive, energy source, inverter, cabling, bearings, launch restraint, payload interface, carrier capture/brake, controls, thermal hardware, mounting and margins. No such installed BOM exists, so **neither candidate passes G1 mass closure**. The CAD proxy itself is not structurally justified or optimized.", "",
         f"The native-CAD partial dry center for A is x={a['partial_dry_cg_m'][0]:.3f} m. With an assigned uniform 4 kg dummy, the combined proxy center moves from x={a['assigned_dummy_combined_cg_start_m'][0]:.3f} m at start to x={a['assigned_dummy_combined_cg_at_stroke_end_m'][0]:.3f} m after the powered stroke. [FreeCAD mass/CG/inertia ledger](../cad/gen6_first_article/release/Gen6_G1_Partial_Mass_CG_Inertia.json). These are not complete host inertia properties.", "",
         "## Ideal mechanical lower bounds", "",
         "| Candidate | Speed | Total moving kinetic energy | Ideal mean drive force | Payload mean acceleration | Captured-carrier brake energy | Ideal mean brake force over 200 mm |", "|:--|--:|--:|--:|--:|--:|",
         *[f"| {name} | {row['speed_m_s']:.0f} m/s | {row['ideal_total_moving_kinetic_J']:.2f} J | {row['ideal_mean_drive_force_N']:.2f} N | {row['ideal_mean_payload_acceleration_g']:.3f} g | {row['carrier_brake_energy_J']:.2f} J | {row['ideal_mean_carrier_brake_force_N']:.2f} N |" for name,c in data["candidates"].items() for row in c["speed_bounds"]], "",
         "The 6 m/s brake mean deceleration is 9.18 g for the captured carrier. Energy recovery, drive efficiency, peak motor force, pusher contact, friction and repeated-stop heat are unmodeled. The four-release P130 study includes 7 and 9 m/s hypothetical commands, outside this first article's proposed 3–6 m/s measurement band.", "",
         "## Lateral tolerance screen", "",
         "The nominal guide width is 110 mm around a 100 mm dummy, giving 5 mm gap per side. With an **assumed** 1.5 mm linear stack, the full 340.5 mm 3U length consumes `L tan(yaw)` of lateral corridor. These are arbitrary screening bands, not provider tolerances or verified payload contact geometry.", "",
         "| Yaw | Swept width consumed | Residual side corridor | Conditional screen |", "|--:|--:|--:|:--:|",
         *[f"| {x['angle_deg']:.1f}° | {x['lateral_sweep_mm']:.2f} mm | {x['residual_mm']:+.2f} mm | {'clear' if x['conditional_clear'] else 'clash'} |" for x in a["lateral_tolerance_screen"]["cases"]], "",
         f"The computed yaw limit at that stack is {a['lateral_tolerance_screen']['maximum_yaw_deg_given_stack']:.3f}°. A 0.7° case fails. The 5 mm gap may itself permit excessive attitude error without a defined contact/retention scheme; geometry clearance alone is not release-vector accuracy.", "",
         "## Disposition", "",
         "A is the *analysis lead* because it is closer to the evaluated Gen5 force-model lineage, while B remains a live challenger that avoids permanent magnets on the moving carrier. This is a sequencing choice, **not** an architecture selection: A inherits magnetic-exposure and capture concerns; B inherits induction efficiency, heating and historical handover-ripple concerns. Both need full drive and source ratings, contacts, safe abort, structural/thermal models and actual component data before G1 can pass.", "",
         "![Partial mass versus residual allowance under the surrogate mission proxy](../figures/gen6_go2_mass_gate.svg)", "",
         "Reproduce analytic bounds with `python3 analysis/gen6_go2_article_bounds.py`; generate and read back CAD with `PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_first_article/build.py` on FreeCAD 1.0. The report and STEP hash ledger are inside the CAD folder.", ""]
    return "\n".join(r)


def figure(data):
    mass=data["mission_proxy"]["max_volley_device_kg_for_device_plus_consumed_fuel_parity"]
    rows=[]
    for i,(name,c) in enumerate(data["candidates"].items()):
        y=122+i*75
        partial=c["partial_structure_and_carrier_kg"]
        rows.append(f'<text x="25" y="{y+19}" font-size="17">Candidate {name}</text>'
                    f'<rect x="205" y="{y}" width="{partial*25:.1f}" height="30" fill="#087e91"/>'
                    f'<rect x="{205+partial*25:.1f}" y="{y}" width="{(mass-partial)*25:.1f}" height="30" fill="#d2dbe3"/>'
                    f'<text x="{205+mass*25+12:.1f}" y="{y+20}" font-size="15">{partial:.2f} kg modeled; {mass-partial:.2f} kg unresolved</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="350" viewBox="0 0 1000 350">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="25" y="43" font-size="23" font-weight="bold">Gen6 Go 2 · necessary installed-mass screen</text>'
            '<text x="25" y="76" font-size="15">P130 surrogate parity ceiling: 19.28 kg device; no actual source or brake selected</text>'
            +''.join(rows)+
            '<text x="25" y="312" font-size="14">Blue: FreeCAD proxy frame, guides and carrier. Grey: all unresolved hardware within an assumed mission boundary.</text></svg>\n')


def equivalent(a,b):
    if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):return math.isclose(a,b,rel_tol=1e-7,abs_tol=1e-4)
    return type(a) is type(b) and a==b


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    data=build()
    prose,graphic=report(data),figure(data)
    if args.check:
        if not RESULT.exists() or not equivalent(data,json.loads(RESULT.read_text())):raise AssertionError("P131 result stale")
        if REPORT.read_text()!=prose or FIGURE.read_text()!=graphic:raise AssertionError("P131 report/figure stale")
        print("P131 Gen6 first-article bounds current")
    else:
        RESULT.write_text(json.dumps(data,indent=2)+"\n")
        REPORT.write_text(prose)
        FIGURE.write_text(graphic)
        print("P131 Gen6 first-article bounds generated")


if __name__=="__main__":main()
