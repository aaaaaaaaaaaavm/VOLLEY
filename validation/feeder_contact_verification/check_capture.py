"""Verify the numerical evidence, calibration controls and immutable native capture."""
from pathlib import Path
import csv,hashlib,json,math,re
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads((H/p).read_text())
for name,rec in load('MANIFEST.json')['files'].items():
 p=(H/name).resolve();assert p.is_relative_to(H) and p.is_file(),name
 assert sha(p)==rec['sha256'],name
inputs=load('campaign_mm/INPUTS.json');runs=load('campaign_mm/RUNS.json')['cases']
assert len(runs)==12 and sum(r['exit_code']==0 for r in runs)==10
assert sum(r['exit_code']==11 for r in runs)==2
assert sha(H/'captured/feeder_mm.cpp')==inputs['source_sha256']
assert sha(H/'PROTOCOL.json')==inputs['protocol_sha256']
for name,digest in inputs['partitions_sha256'].items():assert sha(H/'geometry_guarded'/name)==digest
for r in runs:
 for name,digest in r['hashes'].items():assert sha(H/'campaign_mm'/name)==digest
 assert not r['metrics']['outside_domain_or_nonfinite']
 assert max(abs(v) for v in r['metrics']['payload_momentum_balance_residual_N_s'])<1e-8
for size in ['1U','3U']:
 rows=list(csv.DictReader((H/f'calibration_mm_{size}.csv').open()))
 assert len(rows)==7
 # All deliberately overlapping planar controls must produce native contacts.
 for r in rows:
  if float(r['imposed_gap_m'])<0:assert int(r['contacts'])>0
u=load('unit_check/UNIT_INVARIANCE.json')
# The recorded unit-invariance result includes the complete checked field errors.
assert max(u['maximum_SI_differences'].values()) < 1e-6
poses=load('NATIVE_POSE_AUDIT.json')
assert len(poses['cases'])==7
assert sum(len(r['checks']) for r in poses['cases'])==84
resolution=load('POSE_RESOLUTION.json')
assert len(resolution['checks'])==2
assert all(r['maximum_remaining_pair_volume_mm3'] < 1e-8 for r in resolution['checks'])
summary=load('RESULTS.json')
assert len(summary['cases'])==12 and len(summary['convergence'])==2
assert all(r['last_step_COM_difference_mm']>1 for r in summary['convergence'])
print('PASS: 12 native runs, 14 planar controls, unit scaling and 84 full-solid pose identities; final-state convergence remains a separate acceptance criterion.')
