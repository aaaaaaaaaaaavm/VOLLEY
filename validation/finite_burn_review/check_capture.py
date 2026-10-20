"""Independent captured-evidence checks; standard Python, no targeter import."""
from pathlib import Path
import csv,hashlib,json,math
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(v):return math.sqrt(sum(x*x for x in v))
def rows(p):return list(csv.DictReader(p.open()))
S=json.loads((H/'SUMMARY.json').read_text()); identity=json.loads((H/'SOURCE_IDENTITY.json').read_text())
assert S['targeting_solution_count']==18 and S['native_run_count']==46
for name,expected in identity['unchanged_input_files'].items():assert sha(H/name)==expected,name
for info in S['solutions']:
    r=json.loads((H/'release'/info['file']).read_text())
    assert r['source_sha256']==identity['unchanged_input_files']['inputs/'+r['case']+'_events.csv']
    state=r['initial_state'];now=r['initial_time_s']; used=0.;released=0.
    for e in r['events']:
        assert abs(e['start_s']-now)<1e-7
        assert max(abs(a-b) for a,b in zip(e['before'],state))<1e-8
        if e['kind']=='arc':
            delta=norm(e['force_N'])*(e['end_s']-e['start_s'])/(220*9.80665)
            assert abs(e['before'][6]-e['after'][6]-delta)<1e-9
            used+=delta
        else:
            m=e['payload_mass_kg'];M=state[6];released+=m
            assert abs(e['after'][6]-(M-m))<1e-9
            for j in range(3):
                assert abs(e['after'][j]-state[j])<1e-8
                assert abs(e['after'][j+3]-(state[j+3]-m/M*e['u_m_s'][j]))<1e-9
        state=e['after'];now=e['end_s']
    assert abs(used-r['fuel_used_kg'])<1e-8
    assert abs(state[6]-(r['initial_state'][6]-used-released))<1e-8
    assert now==90000 and info['completed_targeting']
    assert r['fuel_limit_pass']==(used<=r['initial_fuel_kg'])
    assert r['force_limit_pass']==(r['peak_force_N']<=r['force_limit_N'])
    assert info['feasible_in_declared_model']==(r['fuel_limit_pass'] and r['force_limit_pass'])
for job in S['native']:
    assert job['exit_code']==0
    command=rows(H/'release'/job['source']);actual=rows(H/'native'/(job['name']+'_host.csv'))
    assert len(actual)==len(command)-1
    mass=float(command[0]['mass_after_kg'])
    for e,a in zip(command[1:],actual):
        if e['kind']=='arc':
            F=norm([float(e[k])*job['force'] for k in ['fx_or_ux','fy_or_uy','fz_or_uz']])
            mass-=F*(float(e['end_s'])-float(e['start_s']))/(220*9.80665)
        else:mass-=float(e['payload_mass_kg'])
        assert abs(mass-float(a['mass_kg']))<1e-8
        assert abs(float(a['t_s'])-float(e['end_s']))<1e-8
    children=rows(H/'native'/(job['name']+'_payload.csv'))
    shots={e['payload']:e for e in command if e['kind']=='shot'}
    assert len(children)==len(shots)
    for c in children:
        e=shots[c['payload']]
        dr=[float(c[k])-float(e[t]) for k,t in zip(['x_m','y_m','z_m'],['target_rx','target_ry','target_rz'])]
        dv=[float(c[k])-float(e[t]) for k,t in zip(['vx_m_s','vy_m_s','vz_m_s'],['target_vx','target_vy','target_vz'])]
        assert abs(norm(dr)-float(c['position_target_error_m']))<1e-6
        assert abs(norm(dv)-float(c['velocity_target_error_m_s']))<1e-8
        assert float(c['momentum_residual_kg_m_s'])<1e-6
    if job['category']=='nominal':
        assert job['max_payload_target_position_error_m']<.01
        assert job['max_payload_target_velocity_error_m_s']<1e-5
        assert job['max_host_position_difference_m']<.01
        assert job['max_mass_difference_kg']<1e-8
assert max(r['payload_position_change_m'] for r in S['refinement'])<.001
assert any(r['first_fuel_exhaustion_s'] is not None for r in S['solutions'])
assert any(r['peak_force_N']>20 for r in S['solutions'])
assert all(r['feasible_in_declared_model'] for r in S['solutions'] if r['initial_fuel_kg']==30)
assert any(r['max_payload_target_position_error_m']>1000 for r in S['native'] if r['category']=='deterministic_sensitivity')
if (H/'MANIFEST.json').exists():
    for name,expected in json.loads((H/'MANIFEST.json').read_text())['files'].items():assert sha(H/name)==expected,name
print('PASS FBR-01:18 finite-force targets/46 native runs; mass flow, recoil, epochs, refinement and retained resource failures checked. No host, motor, precision or physical-clearance rating.')
