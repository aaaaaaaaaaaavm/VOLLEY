"""Reconcile finite-force solutions, native captures and resource assumptions."""
from pathlib import Path
import json,csv,math,hashlib
import numpy as np
H=Path(__file__).resolve().parent
def records(p): return list(csv.DictReader(p.open()))
def vector(r,prefix=''):
    return np.array([float(r[prefix+k]) for k in ['x_m','y_m','z_m','vx_m_s','vy_m_s','vz_m_s']])
def difference(a,b):
    aa={x['payload']:x for x in records(a)};bb={x['payload']:x for x in records(b)}
    out=[vector(aa[k])-vector(bb[k]) for k in aa]
    return {'payload_position_change_m':max(np.linalg.norm(x[:3]) for x in out),
            'payload_velocity_change_m_s':max(np.linalg.norm(x[3:]) for x in out)}
solutions=[]
for p in sorted((H/'release').glob('*.json')):
    r=json.loads(p.read_text()); forces=[]
    for event in r['events']:
        if event['kind']=='arc' and np.linalg.norm(event['force_N'])>1e-10: forces.append(event)
    slew=[]
    for a,b in zip(forces[:-1],forces[1:]):
        fa,fb=np.array(a['force_N']),np.array(b['force_N'])
        angle=math.degrees(math.acos(float(np.clip(np.dot(fa,fb)/np.linalg.norm(fa)/np.linalg.norm(fb),-1,1))))
        coast=b['start_s']-a['end_s']
        slew.append({'start_s':a['end_s'],'end_s':b['start_s'],'angle_deg':angle,'available_zero_force_s':coast,
                      'mean_rate_deg_s':angle/coast if coast>1e-9 else None})
    fuel_used=0.;exhaustion=None
    for e in r['events']:
        if e['kind']=='arc':
            df=e['before'][6]-e['after'][6]
            if fuel_used+df>r['initial_fuel_kg'] and exhaustion is None:
                flow=df/(e['end_s']-e['start_s'])
                exhaustion=e['start_s']+(r['initial_fuel_kg']-fuel_used)/flow
            fuel_used+=df
    x={k:r[k] for k in ['case','fraction','max_step_s','force_limit_N','initial_fuel_kg','completed_targeting','feasible_in_declared_model','peak_force_N','fuel_used_kg','fuel_remaining_kg','host_position_error_m','host_velocity_error_m_s']}
    x.update(file=p.name,stem=p.stem,thrust_on_s=sum(e['end_s']-e['start_s'] for e in forces),
             max_payload_position_error_m=max(d['position_error_m'] for d in r['deliveries']),
             max_payload_velocity_error_m_s=max(d['velocity_error_m_s'] for d in r['deliveries']),
             first_fuel_exhaustion_s=exhaustion,slew_requirements=slew,
             max_average_slew_deg_s=max((s['mean_rate_deg_s'] or math.inf for s in slew),default=0))
    solutions.append(x)
runs=json.loads((H/'native/RUNS.json').read_text());native=[]
for job in runs:
    rows=records(H/'native'/(job['name']+'_host.csv'))
    children=records(H/'native'/(job['name']+'_payload.csv'))
    x={k:job[k] for k in ['name','source','step','force','shot','dx','category','exit_code']}
    x.update(max_host_position_difference_m=max(float(r['position_difference_m']) for r in rows),
             max_host_velocity_difference_m_s=max(float(r['velocity_difference_m_s']) for r in rows),
             max_mass_difference_kg=max(abs(float(r['mass_difference_kg'])) for r in rows),
             max_payload_target_position_error_m=max(float(r['position_target_error_m']) for r in children),
             max_payload_target_velocity_error_m_s=max(float(r['velocity_target_error_m_s']) for r in children),
             max_momentum_residual_kg_m_s=max(float(r['momentum_residual_kg_m_s']) for r in children))
    native.append(x)
refine=[]
for case in ['4_spring_10kg','4_volley_3_6_10kg','12_spring_20kg','12_volley_3_6_20kg']:
    f=H/'native'/(case+'_f0.35_h60_payload.csv')
    refine.append({'case':case,'type':'native_same_commands_60_to30_s',**difference(f,H/'native'/(case+'_refine_native30_payload.csv'))})
    refine.append({'case':case,'type':'python_retargeted_60_to30_s',**difference(f,H/'native'/(case+'_f0.35_h30_payload.csv'))})
nominal=[r for r in solutions if r['fraction']==.35 and r['max_step_s']==60 and not r['stem'].endswith('fuel30')]
comparisons=[]
for N in [4,12]:
    a=next(r for r in nominal if r['case'].startswith(str(N)+'_spring'))
    b=next(r for r in nominal if r['case'].startswith(str(N)+'_volley'))
    saved=a['fuel_used_kg']-b['fuel_used_kg'];extra=14*N/4
    comparisons.append({'payload_count':N,'spring_device_proxy_kg':16*N/4,'volley_device_proxy_kg':30*N/4,
      'spring_fuel_consumed_kg':a['fuel_used_kg'],'volley_fuel_consumed_kg':b['fuel_used_kg'],
      'fuel_consumption_saved_kg':saved,'device_mass_added_kg':extra,'device_plus_consumed_fuel_difference_kg':extra-saved,
      'interpretation':'Resource proxy difference; not an optimized installed mass or service-value proof. Infeasible reference runs remain diagnostic.'})
summary={'study':'FBR-01','targeting_solution_count':len(solutions),'native_run_count':len(native),
         'solutions':solutions,'native':native,'refinement':refine,'resource_comparison':comparisons,
         'constants':{'mu_m3_s2':3.986004418e14,'radius_m':6378137.,'J2':1.08262668e-3,'Isp_s':220.,'g0_m_s2':9.80665},
         'limitations':['No rated host, thrust/attitude/pointing, plume/thermal or navigation model.',
         'Unbounded vector force controls are solved then screened; a limit failure is not globally infeasible mission proof.',
         'Fuel-exhausted formal solutions are retained only as diagnostics.',
         'Finite-duration burns do not establish motor/release accuracy or collision-safe physical delivery.']}
(H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Finite-force reconciliation:',len(solutions),'targeted solutions,',len(native),'native runs')
