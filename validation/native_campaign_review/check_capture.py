"""Verify the captured full-event replay, bookkeeping and declared scope."""
from pathlib import Path
import csv,hashlib,json,math
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open() as f:return list(csv.DictReader(f))
def norm(r,keys):return math.sqrt(sum(float(r[k])**2 for k in keys))
def error(a,b,ak,bk):return math.sqrt(sum((float(a[x])-float(b[y]))**2 for x,y in zip(ak,bk)))
R=json.loads((H/'full/RESULTS.json').read_text());S=json.loads((H/'full/SUMMARY.json').read_text())
assert len(R['cases'])==51 and S['native_case_count']==51
assert len(S['metrology'])==324 and len(S['dynamic_metrology'])==108 and len(S['thrust_time'])==20
assert len(S['nominal_crosschecks'])==4 and len(S['sensitivity'])==28
for p,expected in S['source_identities'].items():assert sha(H/p)==expected,p
identity=json.loads((H/'EXPORT_SOURCE_IDENTITY.json').read_text())
assert sha(H/'reference/run.py')==identity['upstream_sha256']
assert sha(H/'export_campaign.py')==identity['derived_sha256']
for record in R['cases']:
    assert record['java_source_sha256']==sha(H/'CoupledEvents.java')
    source=H/'events'/record['source_csv'];assert sha(source)==record['source_sha256']
    for name,expected in record['output_hashes'].items():assert sha(H/'full'/name)==expected,name
    events=rows(source);shots={int(r['payload']):r for r in events if r['kind']=='shot'}
    stem=f"{record['case']}_{record['probe']}_step{record['maximum_step_s']}"
    host=rows(H/'full'/(stem+'_host.csv'));payload=rows(H/'full'/(stem+'_payload.csv'))
    assert len(payload)==len(shots)==record['release_count']
    assert len(host)==len(events) # one post-event row per burn/shot, plus final epoch
    mass=float(events[0]['mass_before_kg']);fuel=record['initial_fuel_kg'];probe=record['parameters']
    for event,actual in zip(events[1:],host[:-1]):
        if event['kind']=='burn':
            after=mass*math.exp(-norm(event,['dx','dy','dz'])*probe['burn_multiplier']/(220*9.80665))
            fuel-=mass-after;mass=after
            shift=probe['shot_latency_s'] if event['event_role'].startswith('transfer ') else 0
        else:
            mass-=float(event['payload_kg']);shift=probe['shot_latency_s']
        assert abs(float(actual['mass_kg'])-mass)<1e-9
        assert abs(float(actual['fuel_remaining_kg'])-fuel)<1e-9 and fuel>=0
        assert abs(float(actual['t_s'])-float(event['t_s'])-shift)<1e-9
    assert abs(record['fuel_used_kg']-(record['initial_fuel_kg']-fuel))<1e-9
    errors=[]
    for p in payload:
        target=shots[int(p['payload'])]
        errors.append(error(p,target,['x_m','y_m','z_m'],['target_rx','target_ry','target_rz']))
        assert abs(errors[-1]-float(p['position_target_error_m']))<2e-7
        assert abs(error(p,target,['vx_m_s','vy_m_s','vz_m_s'],['target_vx','target_vy','target_vz'])-float(p['velocity_target_error_m_s']))<2e-9
        assert float(p['momentum_residual_kg_m_s'])<1e-7
        assert float(p['energy_identity_residual_J'])<1e-8
    assert abs(max(errors)-record['max_payload_position_error_m'])<2e-7
    if record['probe']=='nominal':
        assert max(errors)<.01 and record['final_host_position_error_m']<.01
        assert record['max_payload_velocity_error_m_s']<1e-5
        assert record['max_host_mass_residual_kg']<1e-8
assert all(r['max_payload_position_change_m']<.001 for r in S['refinement'])
assert any(r['violates_3600s_pre_final_release_necessary_time'] for r in S['thrust_time'])
assert any(r['position_error_m']>10000 for r in S['sensitivity'])
if (H/'MANIFEST.json').exists():
    for name,expected in json.loads((H/'MANIFEST.json').read_text())['files'].items():assert sha(H/name)==expected,name
print('PASS CNR-01: 51 native captures, independent mass/epoch/target bookkeeping, step comparisons, retained adverse sensitivities and exact evidence identities. No hardware accuracy or mission-acceptance claim.')
