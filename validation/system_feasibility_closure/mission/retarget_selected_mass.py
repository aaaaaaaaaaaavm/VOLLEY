"""Retarget captured matched missions for a declared selected-device mass.

The source input states/targets and original targeter remain unchanged. This
wrapper records device dry mass and a pre-release zero-force guard before
retargeting every finite-force leg. Hardware availability is not established.
"""
from pathlib import Path
import argparse, hashlib, json
import target

H = Path(__file__).resolve().parent
ORIGINAL_READ = target.read_case


def run_case(count, architecture, device_kg, fuel_kg, force_limit_N=100., step_s=60., fraction=.35, pre_release_guard_s=5.):
    if count not in (4, 12) or architecture not in ('spring', 'volley'):
        raise ValueError('Supported controlled manifests are four/twelve spring/VOLLEY')
    input_fuel = 10 if count == 4 else 20
    case = f'{count}_{architecture}' + ('_3_6' if architecture == 'volley' else '') + f'_{input_fuel}kg'
    old_device = (16. if architecture == 'spring' else 30.) * count / 4.

    def modified_read(name):
        data = ORIGINAL_READ(name)
        data['mass'] += device_kg - old_device
        return data

    target.read_case = modified_read
    previous_guard=target.PRE_RELEASE_GUARD
    target.PRE_RELEASE_GUARD=pre_release_guard_s
    try:
        r = target.run(case, fraction, step_s, force_limit_N, fuel_kg)
    finally:
        target.read_case = ORIGINAL_READ
        target.PRE_RELEASE_GUARD=previous_guard
    r['study'] = 'FBR-02 selected-device mass retarget'
    r['mass_update'] = dict(
        original_device_proxy_kg=old_device,
        replacement_declared_device_dry_kg=device_kg,
        device_mass_delta_kg=device_kg-old_device,
        actual_installed_mass_claim=False,
        basis='caller-supplied represented CAD/BOM mass plus declared allowances; see assembly ledger',
    )
    r['wrapper_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    r['targeter_sha256']=hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest()
    r['pre_release_zero_force_guard_s']=pre_release_guard_s
    stem = f'{count}_{architecture}_device{device_kg:.6f}_fuel{fuel_kg:g}_f{fraction:g}_guard{pre_release_guard_s:g}_h{step_s:g}'
    # Preserve the original targeter output; this named issue identifies the new boundary.
    p = H/'release'/(stem+'.json')
    p.write_text(json.dumps(r, indent=2)+'\n')
    auto_stem=f'{case}_f{fraction:g}_h{step_s:g}_fuel{fuel_kg:g}'
    trajectory=H/'release'/(auto_stem+'_trajectory.csv')
    if trajectory.exists():trajectory.replace(H/'release'/(stem+'_trajectory.csv'))
    # The named report contains every original result plus the mass-change record.
    # Remove only this call's redundant generated report, never an input capture.
    redundant=H/'release'/(auto_stem+'.json')
    if redundant.exists() and redundant!=p:redundant.unlink()
    return r, p


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--count',type=int,required=True)
    p.add_argument('--architecture',choices=['spring','volley'],required=True)
    p.add_argument('--device-kg',type=float,required=True)
    p.add_argument('--fuel-kg',type=float,required=True)
    p.add_argument('--force-limit-N',type=float,default=100.)
    p.add_argument('--step-s',type=float,default=60.)
    p.add_argument('--fraction',type=float,default=.35)
    p.add_argument('--pre-release-guard-s',type=float,default=5.)
    a=p.parse_args()
    r,path=run_case(a.count,a.architecture,a.device_kg,a.fuel_kg,a.force_limit_N,a.step_s,a.fraction,a.pre_release_guard_s)
    print(path.name)
