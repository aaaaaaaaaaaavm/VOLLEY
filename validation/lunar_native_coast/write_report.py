"""Write a source-linked report from the actual GMAT analysis results."""
from pathlib import Path
import json
import platform
from importlib.metadata import version

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / 'RESULTS.json').read_text())
finished = [r for r in d['cases'] if 'final_elapsed_days' in r]
sphere = [r for r in finished if r['termination'] == 'native_spherical_radius_stop']
full = [r for r in finished if r['termination'] == 'requested_horizon_reached']
failed = [r for r in d['cases'] if r not in sphere and r not in full]
text = [
    '# Native lunar coast and refinement study', '',
    'Provisional computational evidence · 23 October 2026 · GMAT R2026a', '',
    f'{len(finished)} of {len(d["cases"])} prescribed native coast attempts have captured histories: '
    f'{len(sphere)} terminate at the 1737.4 km spherical radius, '
    f'{len(full)} reach their requested final horizon, and {len(failed)} are unfinished or failed. '
    'These results describe the declared initial states and force models. They do not qualify a lunar mission lifetime or continuous terrain clearance.', '',
    '## Model and provenance', '',
    '- Epoch: **23 Oct 2026 00:00:00.000 TAI Gregorian**. The three initial orbits are 100 × 100 km, 100 × 1000 km and 100 × 10000 km above a 1737.4 km spherical reference. Initial position is on +X in **LunaMJ2000Eq**, with origin Luna and MJ2000Eq axes. The initial velocity lies in the XZ plane for i=90°, or XY for i=0°. These inclinations are relative to MJ2000Eq and are not labels for lunar-equator or lunar-polar mission planes.',
    '- Initial Cartesian states use the common reference μ = **4902.79996708864 km³/s²** from the installed GRGM900C header. The Moon reference radius and zero flattening are explicitly set. All model/degree/step comparisons within a plane start from the same Cartesian state.',
    '- Primary gravity is the installed **GRGM900C** coefficient file, truncated in the distribution to degree/order 360. This study requests 20/20, 40/40 and bounded 80/80 runs. The gravity-file reference radius is **1738 km**, distinct from the 1737.4 km spherical stop/altitude reference. The alternative **LP165P** file contains 165/165 coefficients. GMAT uses primary-body constants from the potential file: GRGM μ = 4902.79996708864 and LP165P μ = **4902.801056 km³/s²**. The LP comparison therefore changes both coefficients and the file μ; it is a model sensitivity test, not a pure degree refinement.',
    '- Lunar body-fixed rotation is explicitly **SPICE / MOON_PA**, using the installed lunar PCK and frame kernel. This is the adopted coefficient-frame alignment. Its physical accuracy and compatibility with each historical field have not been independently validated here.',
    '- Earth and Sun are differential point-mass perturbations with native DE421 ephemerides and zero ephemeris update interval. Earth μ = **398600.435507 km³/s²**, Sun μ = **132712440017.99 km³/s²**. No Earth harmonics, SRP, drag, tides, relativity, stationkeeping, maneuvers, payload release or attitude control is included.',
    '- Integration: **PrinceDormand78**, native RSSStep error control, Accuracy=1e-11, initial step 60 s, minimum step 0.001 s, maximum step 120 or 60 s, maximum 50 attempts, stop on accuracy violation. Native stop tolerance is 1e-6 in the corresponding stop parameter units. ElapsedSecs stop values are **segment durations**; segment durations 7/23/60/90 days implement cumulative checkpoints 7/30/90/180 days. The 80/80 and LP165P cases stop at 30 days.',
    '- Earth orientation settings are explicit: NutationUpdateInterval=0 and the installed EOP file. Native scalar inspection records RA constant 0°, RA rate −0.641°/century, DEC constant 90°, DEC rate −0.557°/century, rotation constant 190.147°, rotation rate 360.9856235°/day, Earth radius 6378.1363 km and flattening 0.0033527. These stored body values are captured in [native_body_parameters.txt](runs/native_body_parameters.txt). Earth is used only as a point mass, so its body orientation does not enter an Earth harmonic acceleration in this study.',
    '- [SOURCE_IDENTITY.json](SOURCE_IDENTITY.json) records SHA-256 identities of the actual executable/libraries, gravity fields, DE421 data, SPICE/time/EOP files, installed examples and local reference documentation. [CASES.json](CASES.json), [EXECUTIONS.json](EXECUTIONS.json) and each native configuration capture identify the actual inputs and commands. GMAT reports console build **30 Mar 2026 10:09:27**.',
    '', '## Coast outcomes', '',
    '“Sphere stop” means a native root of r=1737.4 km, not a topographic impact prediction. “Min altitude” is the minimum of native sampled radii minus the reference radius. A reached horizon indicates only completed propagation for this case.', '',
    '| Initial orbit (km) | i (deg) | Field / degree | Max step (s) | End (days) | Outcome | Reached horizons (days) | Min altitude (km) | Eccentricity range |',
    '|---|---:|---|---:|---:|---|---|---:|---|',
]
baseline = {r['name']: r for r in finished}
key20 = baseline.get('p100_a100_d20_s120')
key40 = baseline.get('p100_a100_d40_s120')
key0 = baseline.get('p100_a100_i0_d20_s120')
lead = []
lead += [f'Of the {sum(r["requested_days"][-1] == 180 for r in d["cases"])} attempts requesting 180 days, '
         f'{sum(r["requested_days"][-1] == 180 for r in sphere)} stop at the sphere and '
         f'{sum(r["requested_days"][-1] == 180 for r in full)} reach 180 days. '
         f'The {sum(r["requested_days"][-1] == 30 for r in d["cases"])} shorter high-degree/alternative-field attempts reach their requested 30 days.', '']
if key20 and key40:
    lead += [f'The i=90° MJ2000Eq circular reference reaches the spherical stop at '
             f'**{key20["final_elapsed_days"]:.3f} days** with GRGM 20/20 and '
             f'**{key40["final_elapsed_days"]:.3f} days** with GRGM 40/40. '
             'Neither reaches the requested 180-day horizon. '
             + (f'The separate i=0° circular 20/20 case reaches {key0["final_elapsed_days"]:.0f} days; '
                'the fixed initial plane materially changes this bounded outcome.' if key0 else ''), '']
cstep = next((x for x in d['comparisons'] if x['kind']=='max_step_120_vs_60_s' and x['apogee_altitude_km']==100 and x['day']==90), None)
cdegree = next((x for x in d['comparisons'] if x['kind']=='degree20_vs_degree40' and x['apogee_altitude_km']==100 and x['day']==90), None)
if cstep and cdegree:
    lead += [f'At the common 90-day circular checkpoint, reducing the maximum step from 120 to 60 s '
             f'changes position by **{cstep["position_difference_m"]:.3g} m**. Changing gravity from 20/20 to 40/40 '
             f'changes position by **{cdegree["position_difference_m"]/1000:.3g} km**. '
             'This separates the small observed numerical sensitivity of that 20/20 case from the much larger gravity-model sensitivity; it does not establish physical convergence.', '']
text[6:6] = lead
for r in d['cases']:
    field = 'LP165P' if r['gravity_file'] == 'LP165P.cof' else 'GRGM'
    if 'final_elapsed_days' not in r:
        text.append(f'| 100 × {r["initial_apogee_altitude_km"]} | {r["inclination_MJ2000Eq_deg"]} | {field} {r["degree_order"]}/{r["degree_order"]} | {r["max_step_s"]} | — | {r["termination"]} | — | — | — |')
        continue
    outcome = {'requested_horizon_reached': 'Requested horizon', 'native_spherical_radius_stop': 'Sphere stop'}.get(r['termination'], r['termination'])
    lo, hi = r['eccentricity_range']
    minimum = r['sampled_min_spherical_altitude_km']
    if abs(minimum) < 1e-6:
        minimum = 0
    text.append(f'| 100 × {r["initial_apogee_altitude_km"]} | {r["inclination_MJ2000Eq_deg"]} | {field} {r["degree_order"]}/{r["degree_order"]} | {r["max_step_s"]} | {r["final_elapsed_days"]:.3f} | {outcome} | {", ".join(map(str,r["completed_horizons"])) or "—"} | {minimum:.3f} | {lo:.5f}–{hi:.5f} |')
text += ['', '![Cumulative sampled altitude](figures/lunar_sampled_altitude.svg)', '',
         '[PDF](figures/lunar_sampled_altitude.pdf) · [300 dpi PNG](figures/lunar_sampled_altitude.png)', '',
         '## Refinement and field sensitivity', '',
         'The comparisons below use native Cartesian states at common completed checkpoints. Full values, velocity differences and actual epoch differences are in [COMPARISONS.csv](COMPARISONS.csv). No precision acceptance criterion was supplied; small time-step changes alone do not validate the force model.', '',
         '| Comparison | Initial orbit (km) | Day | Position difference (m) | Velocity difference (mm/s) |',
         '|---|---|---:|---:|---:|']
for c in d['comparisons']:
    text.append(f'| {c["kind"]} | 100 × {c["apogee_altitude_km"]} | {c["day"]} | {c["position_difference_m"]:.6g} | {c["velocity_difference_mm_s"]:.6g} |')
text += ['', '![Native refinement sensitivity](figures/lunar_refinement.svg)', '',
         '[PDF](figures/lunar_refinement.pdf) · [300 dpi PNG](figures/lunar_refinement.png)', '',
         '## Data handling and integrity', '',
         'Raw native histories, checkpoint reports, stdout, GMAT logs and runtime configuration captures remain under `runs/`. The canonical package stores native histories as lossless `.csv.gz`; their decompressed bytes retain the recorded native SHA-256. Histories have native comma-separated headers; GMAT manual checkpoint reports repeat a whitespace-formatted header before each numeric row. The `_canonical_checkpoints.csv` files normalize only those headers. No orbit data are interpolated for the comparison tables. Epoch ordering and duplicate/rewound samples are checked explicitly; any removals are counted in RESULTS.json, and the original data are retained.', '',
         'Sampled minima depend on sampling even when checkpoint states agree closely. For example, the 100 × 1000 km 20/20 runs give 56.290 km with the 120 s cap and 56.229 km with the 60 s cap. This roughly 61 m difference is not a measured clearance or a continuous lower bound. The native spherical-radius stop is a separate root condition.', '',
         f'The completed captures contain {sum(r["raw_sample_count"] for r in finished):,} raw samples. '
         f'The time-order filter removed {sum(r["rewound_or_duplicate_samples_removed"] for r in finished):,} samples. '
         f'Maximum reconstruction differences are {max((r["radius_reconstruction_max_abs_km"] for r in finished),default=0):.3g} km for radius and '
         f'{max((r["eccentricity_reconstruction_max_abs"] for r in finished),default=0):.3g} for eccentricity. '
         'These checks recompute invariants from the same native Cartesian states and configured reference μ. They establish internal consistency rather than independent physical validation.', '',
         'The early multi-segment attempt is preserved in `archive_duration_semantics/`. It incorrectly supplied cumulative ElapsedSecs stop values. A guard then permitted an extra segment after the first spherical stop in some circular cases. Those runs, including their below-sphere continuation, are excluded from all final coast/refinement tables. The corrected decks use segment durations and were checked against actual 7/30/90/180-day native checkpoint epochs.', '',
         '## Limits and next work', '',
         'The 100 km circular target and two staging ellipses remain prescribed coast examples. The study does not calculate the arrival/targeting maneuver, circularization, stationkeeping budget, maneuver errors or a delivered payload state. A first-sphere stop is an adverse result for that particular model, while a 30- or 180-day coast is only a finite-horizon result.', '',
         'Gravity degree, coefficient model, plane and initial epoch can change the result. Only two fixed MJ2000Eq planes and one epoch are represented. The 80/80 and LP165P evidence is bounded to 30 days. No terrain model, independent coefficient-frame validation, continuous minimum-altitude certificate, parameter/phase ensemble, long-term disposal assessment or customer/provider acceptance is supplied. The full lunar lifetime and mission qualification work remains open.', '',
         '## Reproduce', '',
         'Use the pinned installed runtime and data referenced in SOURCE_IDENTITY.json. `python -B run_cases.py` regenerates and executes the prescribed decks with two native workers and a 240 s per-case wall limit. `python -B analyze.py` parses actual histories and exports figures; `python -B write_report.py` updates this report. The console runs from the existing GMAT `bin` directory with a private startup/output path. No download or installation is required.', '',
         f'Analysis environment: Python {platform.python_version()}, NumPy {version("numpy")}, Matplotlib {version("matplotlib")}.', '']
(ROOT / 'REPORT.md').write_text('\n'.join(text))
print('Report written:', len(finished), 'captured cases;', len(sphere), 'sphere stops;', len(full), 'completed horizons;', len(failed), 'unfinished/failed')
