#!/usr/bin/env python3
'Generate the clean-sheet Gen6 reference-architecture screen.'
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G0 = 9.80665
PAYLOAD_KG = 4.0
SPEEDS = (4.569852, 11.8, 16.029, 29.009)
ACCEL_G = (5.0, 10.0, 25.0)
EFFICIENCIES = (0.60, 0.70, 0.80)
OUTPUTS = (
    ROOT / 'analysis/results/reference_architecture.json',
    ROOT / 'docs/GEN6_REFERENCE_ARCHITECTURE.md',
    ROOT / 'figures/gen6_reference_cell.svg',
)

def s4_speed():
    text = (ROOT / 'docs/MANIFEST_TIMING.md').read_text(encoding='utf-8')
    match = re.search(r'\|\s*bolley_screen\s*\|[^|]*\|[^|]*\|[^|]*\|\s*([0-9.]+)\s*\|', text)
    if not match:
        raise RuntimeError('cannot recover the S4 BOLLEY-screen first-release speed')
    value = float(match.group(1))
    if not math.isclose(value, SPEEDS[0], rel_tol=0.0, abs_tol=5e-7):
        raise RuntimeError(f'S4 study point moved: {value}')
    return value

def duty_row(v, g_multiple):
    a = g_multiple * G0
    energy = 0.5 * PAYLOAD_KG * v * v
    time = v / a
    force = PAYLOAD_KG * a
    return {
        'speed_mps': v, 'acceleration_g': g_multiple, 'acceleration_mps2': a,
        'ideal_payload_energy_J': energy, 'ideal_stroke_m': v*v/(2*a),
        'acceleration_time_s': time, 'constant_force_N': force,
        'average_payload_power_W': energy/time,
        'terminal_constant_force_power_W': force*v,
    }

def build():
    speed = s4_speed()
    duty = [duty_row(v, g) for v in SPEEDS for g in ACCEL_G]
    at_s4 = [r for r in duty if r['speed_mps'] == speed]
    arrangements = [
        {'name':'independent retained cells','blocked_path':'one cell; unrelated cells remain mechanically retained and available','shared_common_modes':'power, command and host services remain shared unless banked','disposition':'REFERENCE','reason':'best mechanical fault isolation without requiring a shared payload path'},
        {'name':'small banks with shared local path','blocked_path':'can strand the affected bank downstream of the blockage','shared_common_modes':'bank path plus power and command','disposition':'BACKUP','reason':'may reduce installed burden, but trades away cell-level mechanical isolation'},
        {'name':'shared magazine/path','blocked_path':'can strand all downstream payloads','shared_common_modes':'path, indexing, power and command','disposition':'COMPARATOR','reason':'mass efficiency is unproven and a single path recreates manifest coupling'},
    ]
    concepts = [
        {'name':'motor-charged mechanical accumulator','energy_control':'pre-release accumulator preload/position','payload_modification':False,'eight_metre_dependency':False,'independent_cell_compatible':True,'pusher_catch_concept':'required local catcher/retainer after payload clears','peak_power':'release power comes from locally stored mechanical energy; recharge can be slow','known_failure_evidence':'repeatability, latch shock, friction and catcher dynamics are unmeasured','installed_mass_state':'UNKNOWN','disposition':'REFERENCE','reason':'passes concept-level hard screens while avoiding the long guide, gas seal/store and full release-power bus demand'},
        {'name':'direct short-stroke electromechanical pusher','energy_control':'commanded force/position/current trajectory','payload_modification':False,'eight_metre_dependency':False,'independent_cell_compatible':True,'pusher_catch_concept':'required local brake/catcher','peak_power':'S4 point at 10 g reaches about 1.79 kW ideal terminal payload power','known_failure_evidence':'electrical storage and actuator thermal duty are unresolved','installed_mass_state':'UNKNOWN','disposition':'BACKUP','reason':'passes geometry screens but adds a high short-duration power path unless energy is stored locally'},
        {'name':'compact gas pusher','energy_control':'charge pressure/mass and valve timing','payload_modification':False,'eight_metre_dependency':False,'independent_cell_compatible':True,'pusher_catch_concept':'required local catcher and pressure-safe end state','peak_power':'stored pneumatic energy supplies the release pulse','known_failure_evidence':'existing Gen6 exposes seal, contact and gas-system uncertainties; compact geometry is not analysed','installed_mass_state':'UNKNOWN','disposition':'BACKUP','reason':'can be compact but imports unresolved fluid/seal/contact hardware'},
        {'name':'existing long gas guide','energy_control':'gas charge/pressure','payload_modification':False,'eight_metre_dependency':True,'independent_cell_compatible':False,'pusher_catch_concept':'historical guide/piston architecture','peak_power':'stored pneumatic energy','known_failure_evidence':'published guide/contact work exposed geometry/contact/tip-off sensitivity','installed_mass_state':'PARTIAL','disposition':'HISTORICAL_COMPARATOR','reason':'fails the clean-sheet no-eight-metre-dependency screen'},
        {'name':'frozen Gen5 electromagnetic LSM','energy_control':'electrical pulse/current waveform','payload_modification':False,'eight_metre_dependency':False,'independent_cell_compatible':False,'pusher_catch_concept':'reusable mover brake/return architecture','peak_power':'high pulse-power electromagnetic system','known_failure_evidence':'frozen 126.6 kg dry baseline plus EMI, arrest and shared-manifest liabilities remain recorded','installed_mass_state':'MODELLED','disposition':'HISTORICAL_COMPARATOR','reason':'evidence baseline, but clean-sheet selection removes demonstrated shared/mass/EM liabilities'},
        {'name':'BOLLEY cooperative interface','energy_control':'cooperative electromagnetic payload/interface interaction','payload_modification':True,'eight_metre_dependency':False,'independent_cell_compatible':True,'pusher_catch_concept':'architecture-specific','peak_power':'architecture-specific','known_failure_evidence':'hot switching, protection, tolerance and installed mass remain open','installed_mass_state':'UNKNOWN','disposition':'COOPERATIVE_PATH','reason':'charged alternative that intentionally relaxes the unmodified-payload boundary'},
    ]
    return {
        'study':'P92 clean-sheet Gen6 reference-architecture screen',
        'status':'REFERENCE_SELECTED_P92_OPEN',
        'source_revisions':{
            'criteria_path':'validation/P92_reference_architecture.md',
            'criteria_declared_commit':'0546e227e790111f2036d66adeb144f35c852fb8',
            's4_report_path':'docs/MANIFEST_TIMING.md',
            's4_merge_commit':'2ae459cadcf56f752e0f0b97bf962b25efb342a2',
        },
        'inputs':{'payload_kg':PAYLOAD_KG,'s4_study_speed_mps':speed,'speed_screens_mps':list(SPEEDS),'acceleration_screens_g':list(ACCEL_G),'stored_energy_efficiency_sensitivity':list(EFFICIENCIES),'compact_stroke_screen_m':0.25},
        'duty':duty,
        's4_point':{'duty':at_s4,'stored_input_energy_J':{f'{int(e*100)}pct':0.5*PAYLOAD_KG*speed*speed/e for e in EFFICIENCIES},'interpretation':'bounded mission-study point, not product minimum or optimum'},
        'payload_arrangements':arrangements,'release_concepts':concepts,
        'reference':{
            'arrangement':'independent retained cells','release_concept':'motor-charged mechanical accumulator',
            'functional_chain':['independent launch retention','slow preload actuator','mechanical energy accumulator','preload/position measurement','independent release latch','short guided pusher','payload clears cell','local pusher catcher/retainer','post-release state sensing'],
            'shared_services':['low-rate power','command/data','host navigation/time','launch/deployment inhibit'],
            'not_selected_yet':['spring form','latch geometry','guide bearing','catcher','motor/gearbox','cell structure'],
        },
        'falsifiers':[
            'measured release repeatability cannot meet the mission-derived terminal-state error budget',
            'latch/pusher shock or tip-off exceeds the payload/interface limit once that limit is declared',
            'friction/tolerance sensitivity consumes the useful preload-control range',
            'catcher loads or required stroke make the installed cell non-compact',
            'installed mass per successfully delivered payload loses to a bank/shared-path alternative after common-mode reliability is charged',
            'required recharge energy/power or thermal rejection is incompatible with the named host',
        ],
        'open_evidence':['mission-derived release/navigation uncertainty budget','clearing and attitude-settling interval','installed mass and envelope for all candidates','accumulator force-displacement law and cycle life','latch repeatability and release shock','pusher friction, guidance, separation contact and tip-off','catcher dynamics and retained post-release state','host power/thermal/interface limits','provider accommodation'],
    }

def report(d):
    r10 = next(r for r in d['s4_point']['duty'] if r['acceleration_g']==10.0)
    lines=[
        '# Clean-sheet Gen6 reference architecture','',
        'Generated by `analysis/reference_architecture.py`. Do not hand-edit.','',
        '**Reference selected for the next calculations; P92/P113 remain open. No hardware has been built or tested.**','',
        'S4 changed the useful question. The bounded two-payload screen did not reward release authority above 4.569852 m/s in its best tested BOLLEY/Gen5/existing-Gen6 campaigns. That number is not a product requirement, but it is enough to test whether Gen6 still needs to look like an eight-metre launcher.','',
        f"It does not. For a 4 kg payload, 4.569852 m/s is 41.77 J of ideal payload energy. At a 10 g constant-acceleration screen the ideal stroke is {r10['ideal_stroke_m']*1000:.1f} mm and the acceleration lasts {r10['acceleration_time_s']*1000:.1f} ms. The terminal constant-force payload power is {r10['terminal_constant_force_power_W']/1000:.2f} kW. That is a compact release-cell problem, not evidence for an 8 m guide.",'',
        '![Gen6 reference-cell functional architecture](../figures/gen6_reference_cell.svg)','',
        '## What moves forward','',
        'The next Gen6 reference is **independent retained cells with a motor-charged mechanical accumulator and a short guided pusher**. A small actuator charges the accumulator before release; preload/position is the commanded release-energy variable; an independent latch releases the pusher; a local catcher keeps the pusher with the host after the payload clears. Shared power, command and host navigation remain common-mode services and are not disguised as independent.','',
        'This is a reference architecture, not a final mechanism. Spring form, latch, bearings, catcher, motor/gearbox and cell structure are deliberately unselected. The point is to move peak release power out of the host bus, remove the historical eight-metre dependency, keep the payload passive, and isolate a blocked mechanical path to one cell.','',
        '## Physics screen','',
        '| speed (m/s) | accel (g) | ideal energy (J) | ideal stroke (m) | time (ms) | force (N) | terminal power (kW) |',
        '|---:|---:|---:|---:|---:|---:|---:|'
    ]
    for r in d['duty']:
        lines.append(f"| {r['speed_mps']:.6g} | {r['acceleration_g']:.0f} | {r['ideal_payload_energy_J']:.2f} | {r['ideal_stroke_m']:.3f} | {r['acceleration_time_s']*1000:.1f} | {r['constant_force_N']:.1f} | {r['terminal_constant_force_power_W']/1000:.2f} |")
    lines += [
        '',
        'The old high-speed points show why they must not be inherited as requirements. Even at the 25 g study ceiling, 16.029 m/s needs about 0.524 m of ideal constant-acceleration stroke and 29.009 m/s needs about 1.716 m. At the S4 point, the same screen needs only 42.6 mm. Mission need now has to justify every extra metre and joule.','',
        'At 4.569852 m/s, a stored-energy path would need 69.61 J, 59.67 J or 52.21 J of input energy at assumed 60%, 70% or 80% release-path efficiency. Those are sensitivity values, not measured efficiencies.','',
        '## Arrangement trade','',
        '| arrangement | blocked path consequence | disposition |','|---|---|---|'
    ]
    for a in d['payload_arrangements']: lines.append(f"| {a['name']} | {a['blocked_path']} | {a['disposition']} |")
    lines += ['','Independent cells take the reference position because the failure topology is explicit: a jammed pusher does not mechanically strand the rest of the manifest. That may cost more structure and actuators. The installed-mass trade is still open, so this is not yet a P92 closure.','','## Release-concept trade','','| concept | control variable | installed mass | disposition |','|---|---|---|---|']
    for c in d['release_concepts']: lines.append(f"| {c['name']} | {c['energy_control']} | {c['installed_mass_state']} | {c['disposition']} |")
    lines += [
        '',
        'The direct electromechanical pusher remains the clean backup. It is mechanically compact, but at the S4 point a 10 g idealized push reaches about 1.79 kW of terminal payload power; a real actuator would need more electrical input. Once local energy storage is added to avoid that bus pulse, the architecture starts converging on the same idea as the motor-charged accumulator. Compact gas remains a backup, but it carries seal, valve and gas-system uncertainties that the clean-sheet reference does not need to import. The long gas guide and Gen5 remain evidence-rich comparators, not erased history. BOLLEY stays a cooperative path.','',
        '## Reference cell, deliberately only one level deeper','',
        'Functional chain: independent launch retention → slow preload actuator → mechanical accumulator → preload measurement → independent latch → short guided pusher → payload clears → local catcher/retainer → post-release state sensing.','',
        'The first hardware-facing work should therefore be small. A bench coupon can measure force-displacement, latch release repeatability, pusher friction, exit velocity/tip-off and catcher load before a flight-like cell is designed. The release-energy setting should be frozen before each shot and the acceptance bands written before the coupon is built.','',
        '## What would kill this reference',''
    ]
    lines += [f'- {x}' for x in d['falsifiers']]
    lines += ['','If one of those fires, the backup is not automatically the old gas guide. The same mission and installed-burden screens are rerun against direct electromechanical, compact gas, banked layouts and BOLLEY.','','## Still open before P92 can close','']
    lines += [f'- {x}' for x in d['open_evidence']]
    lines += ['','[Frozen criteria](../validation/P92_reference_architecture.md) · [S4 campaign](MANIFEST_TIMING.md) · [Mission/redesign workstream](workstreams/MISSION_AND_REDESIGN.md)','','## Reproduce','','```bash','python3 analysis/reference_architecture.py','python3 analysis/reference_architecture.py --check','python3 -m pytest tests/test_reference_architecture.py','```','']
    return '\n'.join(lines)

def svg(d):
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="540" viewBox="0 0 1200 540">
<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111827}.t{font-size:30px;font-weight:700}.s{font-size:16px}.h{font-size:18px;font-weight:700}.box{fill:#f8fafc;stroke:#334155;stroke-width:2}.cell{fill:#eef2ff;stroke:#4338ca;stroke-width:2}.payload{fill:#f0fdf4;stroke:#15803d;stroke-width:2}.arrow{stroke:#475569;stroke-width:3;fill:none;marker-end:url(#a)}.dash{stroke:#64748b;stroke-width:2;stroke-dasharray:8 7;fill:none}</style>
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#475569"/></marker></defs>
<text x="60" y="55" class="t">Gen6 reference cell: stored energy, independent release</text><text x="60" y="86" class="s">Functional allocation only. Component geometry is intentionally not selected.</text>
<rect x="60" y="130" width="220" height="95" rx="12" class="box"/><text x="85" y="165" class="h">Shared host services</text><text x="85" y="194" class="s">power · command · nav/time</text>
<rect x="355" y="120" width="520" height="280" rx="18" class="cell"/><text x="385" y="155" class="h">Independent retained release cell</text>
<rect x="395" y="190" width="135" height="70" rx="9" class="box"/><text x="414" y="218" class="s">slow preload</text><text x="425" y="241" class="s">actuator</text>
<rect x="570" y="190" width="135" height="70" rx="9" class="box"/><text x="586" y="218" class="s">mechanical</text><text x="585" y="241" class="s">accumulator</text>
<rect x="745" y="190" width="95" height="70" rx="9" class="box"/><text x="770" y="218" class="s">latch</text><text x="760" y="241" class="s">+ inhibit</text>
<rect x="470" y="305" width="140" height="62" rx="9" class="box"/><text x="489" y="333" class="s">guided pusher</text><text x="500" y="355" class="s">+ sensing</text>
<rect x="665" y="305" width="140" height="62" rx="9" class="box"/><text x="684" y="333" class="s">local catcher</text><text x="690" y="355" class="s">+ retainer</text>
<rect x="945" y="210" width="190" height="110" rx="12" class="payload"/><text x="982" y="250" class="h">4 kg payload</text><text x="976" y="279" class="s">passive interface</text><text x="975" y="303" class="s">no onboard actuator</text>
<path d="M280 177 L395 215" class="arrow"/><path d="M530 225 L570 225" class="arrow"/><path d="M705 225 L745 225" class="arrow"/><path d="M792 260 L590 305" class="arrow"/><path d="M610 336 L665 336" class="arrow"/><path d="M805 336 L945 280" class="arrow"/><path d="M875 260 L945 260" class="dash"/>
<text x="60" y="455" class="h">S4 study point</text><text x="60" y="484" class="s">4.569852 m/s · 41.77 J ideal payload energy · 106.5 mm ideal stroke at 10 g</text><text x="60" y="513" class="s">Peak release power comes from stored mechanical energy; host electrical power can recharge between releases.</text>
</svg>
'''

def render(d):
    return {OUTPUTS[0]:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),OUTPUTS[1]:report(d).encode(),OUTPUTS[2]:svg(d).encode()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    generated=render(build())
    if args.check:
        bad=[str(p.relative_to(ROOT)) for p,c in generated.items() if not p.exists() or p.read_bytes()!=c]
        if bad:
            print('STALE: '+', '.join(bad)); return 1
        print('reference architecture freshness: PASS'); return 0
    for p,c in generated.items():
        p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(c)
    print('reference architecture generated'); return 0
if __name__=='__main__': raise SystemExit(main())
