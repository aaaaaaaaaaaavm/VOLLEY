#!/usr/bin/env python3
"""Read-only verification of complete captured partial-occupancy source/results."""
import csv,hashlib,json,math
from pathlib import Path
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=load(H/'MANIFEST.json')
    for name,meta in manifest['files'].items():
        p=H/name;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],name
    pins=load(H/'SOURCE_IDENTITIES.json')
    for r in pins['sources']:
        if r['captured_path']=='model/mission_model.py':continue
        assert sha(H/r['captured_path'])==r['accepted_sha256'],r['captured_path']
    assert sha(H/'model/mission_model.py')==pins['model_extension_sha256']
    summary=load(H/'SUMMARY.json');checks=load(H/'INDEPENDENT_CHECKS.json')
    assert len(summary['cases'])==28 and len(checks['independent_conservation_and_guards'])==28 and checks['passed']
    assert len(checks['native_replays'])==17 and len(checks['native_step_refinements'])==4
    for row in summary['cases']:
        r=load(H/'model/release'/(row['case_stem']+'.json'));n=int(row['family'].split('_')[0][1:])
        assert r['source_sha256']==pins['model_extension_sha256']
        assert r['targets_sha256']==sha(H/'model/TARGETS.json')
        assert r['calibration_source_sha256']==sha(H/'analysis/COUPLED_SHOT.json')
        assert len(r['deliveries'])==n and r['completed_targeting']
        assert all(q['position_residual_m']<.001 and q['velocity_residual_m_s']<1e-6 for q in r['legs'])
        assert r['final_time_s']==91800
        assert math.isclose(r['initial_state'][6],500+r['device_retained_dry_kg']+4*n,abs_tol=1e-9)
        assert math.isclose(r['device_retained_dry_kg'],156.55671970039353 if r['architecture']=='gen5' else 72,abs_tol=1e-10)
    for r in checks['native_replays']:
        assert sha(H/'model/release'/(r['stem']+'.csv'))==r['command_sha256']
        assert sha(H/'model/FiniteReplay.java')==r['native_source_sha256']
        for name,digest in r['output_sha256'].items():assert sha(H/'native'/name)==digest
        with (H/'native'/(r['name']+'_payload.csv')).open() as f:actual=list(csv.DictReader(f))
        assert len(actual)==r['payload_count']
        assert max(float(a['position_target_error_m']) for a in actual)==r['max_payload_position_error_m']<.01
        assert max(float(a['velocity_target_error_m_s']) for a in actual)==r['max_payload_velocity_error_m_s']<1e-5
        assert r['max_independent_mass_flow_residual_kg']<1e-8 and r['max_host_mass_difference_kg']<1e-8
        assert r['max_momentum_residual_kg_m_s']<1e-6
        assert r['max_J2_coast_relative_energy_change']<1e-9 and r['max_J2_coast_relative_axial_angular_momentum_change']<1e-9
    assert all(r['pass_1mm'] and r['maximum_terminal_position_change_m']<.001 for r in checks['native_step_refinements'])
    for row in checks['selected']:
        eligible=[r for r in summary['cases'] if r['family']==row['family'] and r['architecture']==row['architecture'] and r['authority_results'][str(row['force_limit_N'])]['feasible_in_declared_candidate']]
        assert (not eligible and row['fuel_kg'] is None) or (eligible and row['fuel_kg']==min(r['fuel_used_kg'] for r in eligible))
    common=load(H/'technical/COMMON_CASE_MATRIX.json')['cases']
    assert sum(r['case_id'].endswith('_EXECUTED') for r in common)==4
    assert not any(r['case_id'].endswith('_DECLARED') for r in common)
    with (H/'technical/MISSION_LEVEL_COMPARISON.csv').open() as f:assert len(list(csv.DictReader(f)))==84
    print(f"PASS: {len(manifest['files'])} file identities, 28 actual finite-force candidates, 17 native replays, 4 step refinements, fixed 2/4 target subsets and unchanged numerical gates; refreshed 2/4/12 comparison has 84 candidate-force rows.")

if __name__=='__main__':main()
