"""P126 illustrative worst-case lateral tolerance stack for the R1 feeder.

Nominal clearances come from exact-solid R1 CAD checks. The tolerances below are
declared study values, not drawing requirements or measured manufacturing data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cad/FEEDER_CANDIDATE_R1.json"
RESULT = ROOT / "cad/FEEDER_R1_TOLERANCE_SCREEN.json"
REPORT = ROOT / "cad/FEEDER_R1_TOLERANCE_SCREEN.md"
FIGURE = ROOT / "figures/feeder_r1_tolerance_screen.svg"
PAYLOAD_LENGTH_MM = 340.5


def case(nominal, install_track, install_cassette, form, tilt_deg):
    tilt = PAYLOAD_LENGTH_MM * math.tan(math.radians(tilt_deg))
    stack = install_track + install_cassette + form + tilt
    return dict(track_mount_mm=install_track, cassette_mount_mm=install_cassette,
                combined_form_mm=form, angular_error_deg=tilt_deg,
                angular_lateral_sweep_mm=tilt, worst_case_stack_mm=stack,
                residual_clearance_mm=nominal-stack,
                conditional_pass=nominal-stack > 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    source_bytes = SOURCE.read_bytes()
    original = json.loads(source_bytes)
    nominal = original["cassette_to_track_clearance_mm"]
    if not original["all_routes_clear"] or nominal <= 0:
        raise RuntimeError("nominal R1 route or clearance is not valid")
    cases = {
        "controlled_study_band": case(nominal, 1, 1, 0.5, .2),
        "looser_alignment_band": case(nominal, 1, 1, 0.5, .5),
    }
    allowable_tilt = math.degrees(math.atan((nominal-2.5)/PAYLOAD_LENGTH_MM))
    result = dict(evidence_class="CAD_DERIVED_NOMINAL_CLEARANCE_WITH_ASSUMED_WORST_CASE_TOLERANCES",
                  source_sha256=hashlib.sha256(source_bytes).hexdigest(),
                  source_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  nominal_track_to_cassette_mm=nominal,
                  nominal_cassette_to_skin_mm=original["static"]["cassette_outer_clearance_mm"],
                  payload_proxy_length_mm=PAYLOAD_LENGTH_MM,
                  assumed_cases=cases,
                  maximum_tilt_with_fixed_2_5mm_linear_stack_deg=allowable_tilt,
                  limitations=["illustrative tolerance bands, not GD&T or supplier process capability",
                               "rigid-body lateral stack only; no deformed, thermal or launch-loaded shapes",
                               "no moving gripper, gate, hinge, fasteners, harness or latch envelope",
                               "not a selected Gen5 revision or flight-interface clearance"])
    bars=[]
    for i,(name,c) in enumerate(cases.items()):
        y=85+i*70
        bars.append(f'<text x="25" y="{y}" font-size="15">{name.replace("_"," ")}</text>'
                    f'<rect x="280" y="{y-20}" width="{40*nominal:.1f}" height="25" fill="#c9d8df"/>'
                    f'<rect x="280" y="{y-20}" width="{40*c["worst_case_stack_mm"]:.1f}" height="25" fill="#ba6c4c"/>'
                    f'<text x="680" y="{y}" font-size="14">{c["residual_clearance_mm"]:+.2f} mm</text>')
    svg=('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="260" viewBox="0 0 800 260">'
         '<rect width="100%" height="100%" fill="#f6f9fb"/>'
         '<text x="25" y="38" font-size="20" font-weight="bold">R1 lateral clearance · assumed tolerance bands</text>'
         +''.join(bars)+
         '<text x="25" y="230" font-size="12">Grey = 5 mm nominal; orange = worst-case stack. Study assumptions, not production tolerances.</text></svg>\n')
    rows=[f"| {n.replace('_',' ')} | {c['angular_error_deg']:.1f}° | {c['worst_case_stack_mm']:.2f} | {c['residual_clearance_mm']:+.2f} | {'yes' if c['conditional_pass'] else 'no'} |"
          for n,c in cases.items()]
    report="\n".join([
        "# P126 — R1 feeder lateral tolerance screen", "",
        "**CAD-derived nominal clearance plus assumed alignment bands; not a released tolerance analysis.**", "",
        f"The exact-solid R1 candidate reports {nominal:.1f} mm nominal cassette-to-track",
        f"lateral clearance on each side and {result['nominal_cassette_to_skin_mm']:.1f} mm nominal",
        "cassette-to-inner-skin clearance. For a 340.5 mm payload proxy, a yaw/roll",
        "alignment angle is converted to lateral sweep as `L tan(angle)`. The worst-case",
        "linear contributions are added, not root-sum-squared.", "",
        "| Declared study band | Angle | Total stack (mm) | Residual (mm) | Conditional clear? |",
        "|:--|--:|--:|--:|:--:|",*rows,"",
        f"With the declared 2.5 mm linear stack, the angular limit is {allowable_tilt:.3f}°.",
        "A 0.5° misalignment fails the 5 mm nominal corridor in this simple screen.",
        "The actual allowable angle may be lower after gripper, thermal and load margins.", "",
        "![R1 assumed tolerance bands](../figures/feeder_r1_tolerance_screen.svg)", "",
        "A real release requires datum-controlled part drawings, process capability,",
        "measured payload/interface envelope, full moving-mechanism swept solids and",
        "thermal/structural deflection. The wide R1 assembly remains unselected; Gen5's",
        "original 11 mm side-feed clash is preserved in its baseline evidence.", "",
        "Reproduce with `python3 cad/screen_feeder_r1_tolerance.py`; `--check` compares",
        "the captured JSON, report and SVG byte for byte.", "",
    ])
    rendered=json.dumps(result,indent=2)+"\n"
    if args.check:
        ok=all(p.exists() and p.read_text()==v for p,v in
               ((RESULT,rendered),(REPORT,report),(FIGURE,svg)))
        print("P126 current" if ok else "P126 STALE")
        return 0 if ok else 1
    RESULT.write_text(rendered)
    REPORT.write_text(report)
    FIGURE.write_text(svg)
    print({k:round(v["residual_clearance_mm"],3) for k,v in cases.items()})


if __name__ == "__main__":
    raise SystemExit(main())
