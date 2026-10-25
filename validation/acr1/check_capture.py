#!/usr/bin/env python3
"""Verify public ACR1 identities, nominal states and supported model boundaries offline."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    errors=[]
    manifest=read('MANIFEST.json')
    for name,item in manifest['files'].items():
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():errors.append(f'missing/external: {name}')
        elif sha(path)!=item['sha256'] or path.stat().st_size!=item['bytes']:errors.append(f'identity changed: {name}')
    origin=read('PROMOTION_ORIGIN.json')
    for name,item in origin['files'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=item['sha256']:errors.append(f'frozen capture changed: {name}')
    cad=read('cad/release/FINAL_CAD_MANIFEST.json')
    states=cad['states']
    if len(states)!=8 or len({r['state']for r in states})!=8:errors.append('eight distinct CAD states required')
    for state in states:
        if not state['all_single_connected'] or not state['native_interference_pass'] or state['physical_pallet_count']!=1:errors.append(f"CAD criteria: {state['state']}")
        for name,item in state['files'].items():
            if sha(ROOT/'cad/release'/name)!=item['sha256']:errors.append(f'CAD state identity: {name}')
    for name,expected in cad['source_sha256'].items():
        if sha(ROOT/'cad'/name)!=expected:errors.append(f'CAD source identity: {name}')
    motion=read('cad/release/MOTION_VERIFICATION.json')
    if motion['case_count']!=154 or motion['failed_case_count']!=0 or not motion['all_sampled_cases_pass']:errors.append('154 accepted motion cases required')
    if not read('cad/release/FINAL_REFINEMENT_VERIFICATION.json')['all_refinement_checks_pass']:errors.append('final refinement')
    if not read('verification/FINAL_STEP_READBACK_SUMMARY.json')['all_eight_states_pass']:errors.append('independent STEP readback')
    shot=read('analysis/COUPLED_SHOT.json')
    if sha(ROOT/'analysis/coupled_shot.py')!=shot['source_sha256']:errors.append('shot source identity')
    supported=[r for r in shot['cases']if r['target_m_s']in[1,2,3]]
    if len(supported)!=18 or not all(r['all_declared_checks_pass']for r in supported):errors.append('18 supported source/inductance cases')
    if not math.isclose(shot['dry_CAD_mass_kg'],149.55671970039353,abs_tol=1e-9):errors.append('CAD dry mass')
    if not read('analysis/TRANSFER_INTERLOCKS.json')['all_passed']:errors.append('interlock capture')
    mission=read('mission/MISSION_CAPTURE.json')
    if not mission['all_declared_numerical_checks_pass'] or mission['accepted_native_replay_case_count']!=9:errors.append('mission native replay checks')
    if errors:raise SystemExit('\n'.join(errors))
    print(f"PASS: ACR1 {len(manifest['files'])} public file identities; {len(origin['files'])} frozen captures; 8 CAD/STEP states; 154 motion cases; 18 supported shot cases; 9 native replays")
if __name__=='__main__':main()
