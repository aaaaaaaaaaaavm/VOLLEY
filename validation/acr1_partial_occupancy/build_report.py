#!/usr/bin/env python3
"""Report executed current ACR1 partial occupancy and refresh engineering-only comparison."""
import csv,hashlib,json,re,shutil
from pathlib import Path
H=Path(__file__).resolve().parent
OLD=H/'inputs/reference_comparison_base'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def table(p,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in r.items()})
def main():
    s=load(H/'SUMMARY.json');c=load(H/'INDEPENDENT_CHECKS.json');assert c['passed']
    native=c['native_replays'];selected=c['selected']
    lines=['| Count | Family | Authority | ACR1 fuel (kg) | Fixed2 spring (kg) | Ideal pretrim (kg) |',
           '|---:|---|---:|---:|---:|---:|']
    for n in [2,4]:
        for family in ['uniform_2','alternating_1_3']:
            for limit in [1.,5.]:
                values=[]
                for arch in ['gen5','spring_fixed2','spring_pretrim']:
                    r=next(r for r in selected if r['family']==f'n{n}_{family}' and r['architecture']==arch and r['force_limit_N']==limit)
                    values.append('no tested pass' if r['fuel_kg'] is None else f"{r['fuel_kg']:.9f}")
                lines.append(f"| {n} | {family} | {limit:g} N | "+' | '.join(values)+' |')
    report=f'''# ACR1 partial-occupancy finite-force mission results

**26 October 2026 · ACR1-PARTIAL-OCCUPANCY-01.** These are actual new two- and four-payload computations using the current same-size passive 4 kg 3U surrogate. They extend the accepted twelve-payload reference, preserved at commit ca67ea95bf5729aa293da3728f79e23d79da9262. They do not establish mixed-size Gen6 performance or actual provider compatibility.

## Matched boundary

Both architectures retain their full twelve-position hardware: ACR1 device dry 156.55671970039353 kg including 7 kg power/control once, versus the frozen 72 kg conventional-device proxy. The unchanged wet host is 500 kg, including 20 kg propellant, at Isp 220 s. Partial occupancy changes payload inventory only: 8 kg or 16 kg. Initial assemblies are therefore 664.556719700/672.556719700 kg ACR1 and 580/588 kg conventional. No empty-cell mass or unselected replacement device is removed.

Targets are exact first-two/first-four subsets of the accepted uniform2 and alternating1/3 families. Initial state/24 October 2026 TAI epoch, release slots 450/900 s or 450/900/1350/1800 s, common host target, and final evaluation at **91800 s** are unchanged. Thus the two- and four-payload final evaluation is 90900 s and 90000 s after their last releases, respectively; it is not relabeled 24 hours after their last release. The host recovery remains at the common first Kepler period, about 5676.978 s, followed by a continuous coast. No native host state is reset to a target.

Finite-force policy, continuous mass depletion, source-calibrated commanded release and recoil are unchanged. All architectures retain 5 s pre/20 s post guards; ACR1 retains 400 s zero-force loading coast for the 355 s mechanism cycle. The command interpolates the accepted computational 1/2/3 m/s source rows and remains clipped to 1–3 m/s. Inherited fields named `measured_release` refer to computed source traces, not physical measurements. The fixed spring uses 2 m/s; ideal pretrim uses frozen per-payload energy tables. Conventional policies may use wider 35%/45% force windows because no 400 s mechanism coast is imposed on them.

## Actual selected outcomes

{chr(10).join(lines)}

All **28 finite-force candidates** solved the original 1 mm position / 1 micrometre/s targeting gates. Force-ceiling failures remain failures. In the alternating family ACR1 peaks near 4.204 N and has no tested 1 N pass; ideal pretrim succeeds at 1 N for both counts. Fixed2 spring now has 5 N passes for two and four payloads, unlike the retained twelve-payload candidate outcome. The lowest-fuel four-payload fixed2 pass uses 2.594045517 kg, while its tested 45% policy consumes 2.851060101 kg. Selection preserves the actual best feasible policy rather than transferring twelve-payload results.

No propellant or initial wet-mass advantage over ideal pretrim is demonstrated. Differences of order 1e-8 kg between uniform ACR1 and pretrim are numerical scale; they are not a physical advantage. The retained hardware mass difference is 84.556719700 kg for every occupancy. These are bounded sampled policies, not global optimizations or impossibility proofs.

## Independent verification

All 28 candidates passed separately reaggregated mass flow, released inventory, linear momentum, recoil mapping, event continuity and release-guard checks. Source/current mass and final inventory close without duplicating the 20 kg reserve. Four ACR1 policies retain 400 s loading coasts and original command limits.

The unchanged native Orekit 13.1.6 / Hipparchus 4.0.3 Java replay was actually executed for **{len(native)} cases**: thirteen distinct selected trajectories and four 60→30 s ACR1 refinements. It reads frozen force/release commands, integrates host arcs consecutively, recomputes ACR1 recoil from its independently integrated mass, and propagates payloads to the same final epoch. Maximum native payload target difference: **{max(r['max_payload_position_error_m'] for r in native):.9g} m / {max(r['max_payload_velocity_error_m_s'] for r in native):.9g} m/s**. Maximum host-state position difference: **{max(r['max_host_position_difference_m'] for r in native):.9g} m**. Maximum independent native mass-flow residual: **{max(r['max_independent_mass_flow_residual_kg'] for r in native):.9g} kg**. Maximum native momentum residual: **{max(r['max_momentum_residual_kg_m_s'] for r in native):.9g} kg·m/s**. Maximum 60→30 s terminal-position change: **{max(r['maximum_terminal_position_change_m'] for r in c['native_step_refinements']):.9g} m**, below the original 1 mm refinement gate.

These numerical differences do not establish physical delivery accuracy. Fixed-axis J2 point-mass gravity, constant inertial resultant force, ideal mass flow and point release remain the accepted model boundary. Real host inertia/attitude/plume, navigation, drag/higher gravity, near-field exit geometry, failures, joint dispersion, provider services and physical qualification remain distinct requirements.

## Source and reproduction

`SCOPED_EXTENSION.diff` records the narrow patch: derive occupancy count for inventory/completion/ledger/coast aggregation, and retain full CAD mass precision. Targeting equations, gravity, calibration, commands, force windows and acceptance thresholds are unchanged. `SOURCE_IDENTITIES.json` pins the accepted inputs; `SUMMARY.json`, `CASE_DEFINITIONS.json`, every model/release JSON/command CSV/trajectory CSV and the native raw CSV/logs preserve the actual evidence. Runtime versions are captured. Scientific dependencies for this capture are NumPy 2.3.5 and SciPy 1.17.0.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_cases.py
python3 verify_and_replay.py --jars-dir /path/to/orekit-13.1.6-and-hipparchus-4.0.3-jars
python3 check_capture.py
```

Use the supplied drivers, which operate on frozen subsets; calling the inherited model's original main entry point would recreate its twelve-payload example inside this study copy. Java is invoked through its installed compiler module where a separate javac executable is absent. No third-party jars are redistributed. `technical/` updates the source-pinned common-case comparison with actual 2/4 outcomes and the retained accepted12 results; the earlier pre-run reference packet remains a dated record.
'''
    (H/'REPORT.md').write_text(report)
    (H/'requirements-python.txt').write_text('numpy==2.3.5\nscipy==1.17.0\n')
    # Produce a fresh engineering-only comparison; preserve the original pre-run packet.
    T=H/'technical';T.mkdir(exist_ok=True)
    for p in OLD.iterdir():shutil.copyfile(p,T/p.name)
    common=load(T/'COMMON_CASE_MATRIX.json');updated=0
    for row in common['cases']:
        if row['case_id'].endswith('_DECLARED'):
            row['case_id']=row['case_id'].replace('_DECLARED','_EXECUTED')
            row['status']='executed new finite-force current ACR1 3U partial occupancy; independently replayed; force failures retained'
            row['sources'] += [dict(input='partial_occupancy_summary',json_pointer='/cases',sha256=sha(H/'SUMMARY.json')),
                               dict(input='partial_occupancy_independent',json_pointer='/native_replays',sha256=sha(H/'INDEPENDENT_CHECKS.json'))]
            updated+=1
    assert updated==4
    dump(T/'COMMON_CASE_MATRIX.json',common)
    table(T/'COMMON_CASE_MATRIX.csv',[{k:v for k,v in r.items() if k!='targets'} for r in common['cases']])
    with (T/'MISSION_LEVEL_COMPARISON.csv').open() as f:outcomes=list(csv.DictReader(f))
    for i,row in enumerate(s['cases']):
        for limit in [1.,5.]:
            outcomes.append(dict(case=row['case_stem'],family=row['family'],architecture=row['architecture'],payload_count=int(row['family'].split('_')[0][1:]),
                force_limit_N=limit,peak_force_N=row['peak_force_N'],feasible=row['authority_results'][str(limit)]['feasible_in_declared_candidate'],
                fuel_kg=row['fuel_used_kg'],initial_wet_kg=row['initial_state'][6],retained_device_dry_kg=row['device_retained_dry_kg'],
                evaluation_s=row['final_time_s'],host_position_error_m=row['host_position_error_m'],host_velocity_error_m_s=row['host_velocity_error_m_s'],
                targets_sha256=row['targets_sha256'],source=dict(input='partial_occupancy_summary',json_pointer=f'/cases/{i}',sha256=sha(H/'SUMMARY.json'))))
    table(T/'MISSION_LEVEL_COMPARISON.csv',outcomes)
    with (T/'SELECTED_MISSION_OUTCOMES.csv').open() as f:combined=list(csv.DictReader(f))
    for row in selected:
        combined.append(dict(family=row['family'],force_authority_N=row['force_limit_N'],architecture=row['architecture'],
            best_tested_case=row['case'],fuel_used_kg=row['fuel_kg'],peak_force_N=row['peak_force_N'],
            status='Closed within declared candidate bounds' if row['candidate_pass'] else 'No tested candidate within force ceiling; no global infeasibility inference'))
    table(T/'SELECTED_MISSION_OUTCOMES.csv',combined)
    for name in ['SUMMARY.json','INDEPENDENT_CHECKS.json','CASE_DEFINITIONS.json']:shutil.copyfile(H/name,T/('PARTIAL_OCCUPANCY_'+name))
    inventory=load(T/'SOURCE_INVENTORY.json')
    for key,name in [('partial_occupancy_summary','SUMMARY.json'),('partial_occupancy_independent','INDEPENDENT_CHECKS.json'),('partial_occupancy_definitions','CASE_DEFINITIONS.json')]:
        inventory['sources'].append(dict(input=key,path='PARTIAL_OCCUPANCY_'+name,sha256=sha(H/name),bytes=(H/name).stat().st_size,
            revision='ACR1-PARTIAL-OCCUPANCY-01; newly executed 26 October 2026',commit=None))
    inventory['method']='Accepted twelve-payload results and dated primary sources reused; new 28 partial-occupancy finite-force policies and 17 actual native replays captured separately.'
    dump(T/'SOURCE_INVENTORY.json',inventory)
    readme=(T/'README.md').read_text()
    a=readme.index('COMMON_CASE_MATRIX contains 27 declarations.')
    b=readme.index('\n\nLEO targets',a)
    readme=readme[:a]+'''COMMON_CASE_MATRIX contains 27 cases: six executed target families for two/four/twelve same-size 3U payloads, three unchanged-hardware occupancy accounting rows, and eighteen ideal lunar energy bounds. The twelve-payload results are accepted baseline evidence; two/four results are distinct new finite-force calculations with native endpoint replay. There are 42 finite-force candidate policies across all three occupancies, or 84 candidate/force-ceiling rows, and 36 selected comparisons. The three accounting-only rows remain arithmetic. No case is a mixed-size Gen6 campaign or provider delivery commitment.'''+readme[b:]
    readme=readme.replace('MISSION_LEVEL_COMPARISON retains all fourteen candidate policies at both force ceilings, and SELECTED_MISSION_OUTCOMES retains twelve lowest-fuel feasible selections or explicit no-pass results.',
        'MISSION_LEVEL_COMPARISON retains all 42 candidate policies at both force ceilings, and SELECTED_MISSION_OUTCOMES retains 36 lowest-fuel feasible selections or explicit no-pass results. The common fixed 91800 s epoch is preserved for every occupancy; it is 90900/90000 s after the last two/four-payload release, respectively.')
    a=readme.index('The supplied tables are derived')
    readme=readme[:a]+'''The supplied tables are derived from the immutable accepted sources and the distinct new captures in SOURCE_INVENTORY. PARTIAL_OCCUPANCY_REPORT gives exact new results, limits and reproduction commands; PARTIAL_OCCUPANCY_SUMMARY and INDEPENDENT_CHECKS contain all numeric checks and actual native replay receipts. The new source/calculation package accompanies this comparison. Existing lunar histories are reused. Unknown fields remain null rather than zero. Accounting-only rows remain distinct from executed outcomes.\n'''
    (T/'README.md').write_text(readme)
    shutil.copyfile(H/'REPORT.md',T/'PARTIAL_OCCUPANCY_REPORT.md')
    position=(T/'COMPETITIVE_POSITION.md').read_text()
    position=position.replace('No native dynamics was rerun.','Accepted twelve-payload results are reused; distinct new two/four-payload native replays are documented below.')
    position += '\nTwo- and four-payload partial occupancy has now actually been computed with the same full retained hardware, frozen target subsets and fixed evaluation epoch. New twenty-eight policies and seventeen actual native replays retain the same negative advantage conclusion versus ideal pretrim. Fixed2 spring has 5 N passes for these smaller manifests; the twelve-payload failure is not transferred to them. See PARTIAL_OCCUPANCY_REPORT and the updated 2/4/12 outcome tables.\n'
    (T/'COMPETITIVE_POSITION.md').write_text(position)
    # Native actual command paths are engineering provenance, not control data.
    for p in T.iterdir():
        assert not re.search(r'PLAN-[A-Z]|MAC021|TASK_MATRIX|Grand Plan|AVM Work Index',p.read_text()),p.name
    print('PASS: actual two/four results reported; refreshed',len(list(T.iterdir())),'engineering comparison files, 84 candidate/force rows, 36 selected rows; original pre-run packet preserved')

if __name__=='__main__':main()
