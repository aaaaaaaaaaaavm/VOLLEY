"""Verify the captured release study using only stdlib and NumPy.

Read-only: no MuJoCo import and no dynamics regeneration. Individual native
run records are the raw endpoint evidence; sampled CSVs independently support
the no-contact control. Full native contact-wrench balances cannot be rebuilt
because complete per-step wrenches were not exported.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import sys
import xml.etree.ElementTree as ET
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def require(condition,message):
    if not condition:raise AssertionError(message)

def read(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def close(a,b,atol=1e-11,rtol=1e-10):
    return bool(np.allclose(a,b,atol=atol,rtol=rtol,equal_nan=False))
def rotation(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def angle(q1,q2):
    return math.degrees(2*math.acos(min(1,abs(float(np.dot(q1,q2))))))
def stem(r):
    return (f'{r["case"]["id"]}_{round(r["dt_s"]*1e6,3):g}us_'
            f'{r["solver"]}{r["iterations"]}_k{r["direct_stiffness_s_minus2"]:g}_'
            f'b{r["direct_damping_s_minus1"]:g}_{r["representation"]}')

def verify():
    manifest=read(HERE/'MANIFEST.json')
    entries=manifest['files']
    if isinstance(entries,dict):entries=[dict(v,path=k) for k,v in entries.items()]
    require(isinstance(entries,list),'Manifest files must be a list or mapping')
    names=[]
    for entry in entries:
        relative=Path(entry['path'])
        require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe manifest path')
        p=HERE/relative
        require(p.is_file(),f'Missing captured file: {relative}')
        require(p.stat().st_size==entry['bytes'],f'Byte count differs: {relative}')
        require(digest(p)==entry['sha256'],f'SHA256 differs: {relative}')
        names.append(str(relative))
    require(len(names)==len(set(names)),'Duplicate manifest paths')
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()
            and p.name!='MANIFEST.json' and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    require(actual==set(names),f'Publish set differs: unlisted={sorted(actual-set(names))}, missing={sorted(set(names)-actual)}')
    report=manifest.get('main_report')
    if report:require(digest(ROOT/report['path'])==report['sha256'],'Main report identity differs')

    geometry=read(HERE/'GEOMETRY_AND_INPUTS.json')
    for pin in geometry['input_pins']:
        require(digest(ROOT/pin['path'])==pin['sha256'],f'Controlling source differs: {pin["path"]}')
    prior=geometry['prior_Chrono_diagnosis']
    require(digest(ROOT/prior['path'])==prior['sha256'],'Prior Chrono diagnosis identity differs')
    require(len(geometry['collision_surfaces'])==66,'Unexpected adopted surface count')
    inertia=4/12*np.array([.1**2+.1**2,.3405**2+.1**2,.3405**2+.1**2])
    require(close(geometry['surrogate']['uniform_box_principal_inertia_kg_m2'],inertia),'Surrogate inertia differs')
    source=read(HERE/'SOURCE_REPLAY.json')
    original=(ROOT/'validation/acr1/analysis/coupled_shot.py').read_text()
    require(hashlib.sha256(original.encode()).hexdigest()==source['source_sha256'],'Source replay identity differs')
    change=source['instrumentation_change']
    require(original.count(change['before'])==1,'Instrumentation target is ambiguous')
    instrumented=original.replace(change['before'],change['after'])
    require(hashlib.sha256(instrumented.encode()).hexdigest()==source['instrumented_sha256'],'Trace-only instrumentation differs')

    # Independently rebuild the decisive source mechanical-work identity from
    # every recorded force, displacement, velocity and attached-state sample.
    source_checks=[]
    for case in source['cases']:
        trace=np.load(HERE/f'source_{case["case"]}.npz')['trace']
        require(trace.ndim==2 and trace.shape==(case['dense_trace_rows'],10),'Dense trace shape differs')
        require(np.isfinite(trace).all(),'Nonfinite source trace')
        require(np.all(np.diff(trace[:,0])>0) and close(np.diff(trace[:,0]),5e-6,atol=2e-12),'Source time grid differs')
        require(case['all_declared_checks_pass'],'Captured source gate failed')
        row=trace[np.argmin(abs(trace[:,0]-case['release']['time_s']))]
        require(close(row[:3],[case['release']['time_s'],case['release']['position_m'],case['release']['relative_speed_m_s']]),'Source release event differs')
        require(close(trace[-1,1],case['stop_position_m']),'Source stop position differs')
        ms=case['moving_sled_kg'];mh=case['reference_rest_host_kg']
        mu_attached=(ms+4)*mh/(mh+ms+4);mu_detached=ms*mh/(mh+ms)
        mu=np.where(trace[:,9]>.5,mu_attached,mu_detached)
        dx=np.diff(np.r_[0.,trace[:,1]])
        dv2=np.diff(np.r_[0.,trace[:,2]**2])
        net_work=float(np.sum(trace[:,8]*dx))
        kinetic=float(np.sum(.5*mu*dv2))
        residual=kinetic-net_work
        require(abs(residual)<1e-8,'Source reduced-mass work balance changed')
        C=6.25*(.9*.7 if case['adverse'] else 1)
        draw=.5*C*(86.4**2-trace[-1,4]**2)
        require(close(draw,case['cap_draw_J'],atol=1e-8),'Source capacitor draw differs')
        kick=mh/(mh+ms+4)*row[2]
        require(close(kick,case['release']['payload_inertial_delta_v_m_s']),'Source recoil mapping differs')
        source_checks.append({'case':case['case'],'samples':len(trace),'recomputed_work_J':net_work,
                              'recomputed_kinetic_change_J':kinetic,'work_balance_residual_J':residual})

    campaign=read(HERE/'CAMPAIGN.json');summary=read(HERE/'SUMMARY.json')
    records=campaign['completed_records']
    require(campaign['planned_runs']==len(records)==42,'Adopted run count differs')
    require(summary['completed_runs']==42 and not summary['failed_runs'],'Summary run status differs')
    require(not summary['full_P3_BB_criterion_complete'],'Scope boundary changed')
    require(len(list((HERE/'runs').glob('*.json')))==42,'Unexpected native run-record count')
    raw={}
    for record in records:
        s=stem(record);r=read(HERE/'runs'/f'{s}.json')
        require(r==record,f'Campaign/native record mismatch: {s}')
        tree=ET.parse(HERE/'runs'/f'{s}.xml')
        option=tree.find('option')
        require(close(float(option.attrib['timestep']),r['dt_s']),'Native XML time step differs')
        require(close(np.fromstring(option.attrib['gravity'],sep=' '),[0,0,0]),'Native gravity differs')
        pi=tree.find('.//body[@name="payload"]/inertial')
        require(float(pi.attrib['mass'])==4 and close(np.fromstring(pi.attrib['diaginertia'],sep=' '),inertia),'Native payload inertia differs')
        raw[s]=r

    # Recompute every reported pose/velocity/rate refinement from individual
    # native final-state outputs, without importing the dynamics implementation.
    with (HERE/'REFINEMENT.csv').open(newline='') as f:refinements=list(csv.DictReader(f))
    recomputed=[]
    for row in refinements:
        matches=[]
        for dt in [float(row['coarse_dt_us']),float(row['fine_dt_us'])]:
            candidates=[r for r in raw.values() if r['case']['id']==row['case'] and abs(r['dt_s']*1e6-dt)<1e-8
                        and r['solver']=='Newton' and r['iterations']==100 and r['representation']=='box'
                        and r['direct_stiffness_s_minus2']==1e6 and r['direct_damping_s_minus1']==2000]
            require(len(candidates)==1,'Ambiguous refinement pair');matches.append(candidates[0])
        x,y=matches
        values={'COM_difference_mm':1000*float(np.linalg.norm(np.array(y['payload_final_position_m'])-x['payload_final_position_m'])),
                'orientation_difference_deg':angle(x['payload_final_quaternion_wxyz'],y['payload_final_quaternion_wxyz']),
                'speed_vector_difference_m_s':float(np.linalg.norm(np.array(y['payload_final_velocity_m_s'])-x['payload_final_velocity_m_s'])),
                'omega_vector_difference_deg_s':float(np.linalg.norm(np.array(y['payload_final_omega_deg_s'])-x['payload_final_omega_deg_s']))}
        for key,value in values.items():require(close(value,float(row[key])),f'Refinement claim differs: {row["case"]}/{key}')
        passed=values['COM_difference_mm']<=.05 and values['orientation_difference_deg']<=.05
        require(str(passed)==row['within_inherited_0p05mm_0p05deg_reference'],'Refinement reference-screen flag differs')
        recomputed.append(dict(case=row['case'],coarse_dt_us=float(row['coarse_dt_us']),fine_dt_us=float(row['fine_dt_us']),**values))
    require(len(recomputed)==len(summary['refinement_pairs']),'Summary refinement count differs')
    for value in recomputed:
        candidates=[r for r in summary['refinement_pairs'] if r['case']==value['case'] and close(r['coarse_dt_us'],value['coarse_dt_us']) and close(r['fine_dt_us'],value['fine_dt_us'])]
        require(len(candidates)==1,'Ambiguous summary refinement claim')
        for key in ['COM_difference_mm','orientation_difference_deg','speed_vector_difference_m_s','omega_vector_difference_deg_s']:
            require(close(candidates[0][key],value[key]),f'Summary refinement claim differs: {value["case"]}/{key}')
    for key in ['aligned_25us','half_keeper_25us','no_contact_control_25us']:
        require(summary[key]==raw[stem(summary[key])],f'Summary endpoint record differs: {key}')

    # Independent conservation/control checks from sampled native pose/velocity
    # data. Contact wrenches for the other cases are not available at every step.
    controls=[]
    for r in raw.values():
        if r['case']['id']!='freeflight':continue
        samples=np.genfromtxt(HERE/'runs'/f'{stem(r)}.csv',delimiter=',',names=True)
        pos=np.column_stack([samples[f'{axis}_m'] for axis in 'xyz'])
        vel=np.column_stack([samples[f'v{axis}_m_s'] for axis in 'xyz'])
        omega=np.radians(np.column_stack([samples[f'w{axis}_deg_s'] for axis in 'xyz']))
        quats=np.column_stack([samples[k] for k in ['qw','qx','qy','qz']])
        t=samples['time_s']-r['tstart_s'];v0=np.array(r['payload_initial_velocity_m_s'])
        position_error=float(np.max(np.linalg.norm(pos-np.array(r['payload_initial_position_m'])-t[:,None]*v0,axis=1)))
        linear_error=float(np.max(np.linalg.norm(4*(vel-v0),axis=1)))
        momenta=np.array([rotation(q)@np.diag(inertia)@rotation(q).T@w for q,w in zip(quats,omega)])
        H0=inertia*np.radians(r['payload_initial_omega_deg_s'])
        angular_error=float(np.max(np.linalg.norm(momenta-H0,axis=1)))
        kinetic=2*np.sum(vel*vel,axis=1)+.5*np.sum(omega*momenta,axis=1)
        energy_error=float(np.max(abs(kinetic-kinetic[0])))
        require(position_error<1e-8 and linear_error<1e-10 and angular_error<1e-8 and energy_error<1e-8,'No-contact numerical control changed')
        controls.append({'dt_us':r['dt_s']*1e6,'sampled_position_residual_m':position_error,
                         'sampled_linear_momentum_residual_Ns':linear_error,'sampled_angular_momentum_residual_Nms':angular_error,
                         'sampled_kinetic_energy_change_J':energy_error})
    require(len(controls)==3,'No-contact control count differs')

    recorded={
        'maximum_total_x_momentum_residual_Ns':max(abs(r['conservation']['total_x_momentum_residual_kg_m_s']) for r in raw.values()),
        'maximum_payload_linear_impulse_residual_Ns':max(float(np.linalg.norm(r['conservation']['payload_linear_impulse_residual_Ns'])) for r in raw.values()),
        'maximum_payload_angular_impulse_residual_Nms':max(float(np.linalg.norm(r['conservation']['payload_angular_impulse_residual_Nms'])) for r in raw.values()),
        'maximum_contact_vs_generalized_force_error_N':max(r['conservation']['native_generalized_vs_contact_force_max_N'] for r in raw.values()),
        'full_budget_steps':sum(r['solver_full_budget_steps'] for r in raw.values()),
        'native_warning_increments':sum(sum(r['native_warning_increments']) for r in raw.values())}
    for key,value in recorded.items():require(close(value,summary[key],atol=1e-16),f'Recorded diagnostic aggregation differs: {key}')
    require(recorded['full_budget_steps']==1,'Documented CG iteration-budget limitation differs')
    aligned=next(r for r in raw.values() if r['case']['id']=='aligned' and r['dt_s']==25e-6 and r['solver']=='Newton' and r['iterations']==100 and r['representation']=='box' and r['direct_stiffness_s_minus2']==1e6 and r['direct_damping_s_minus1']==2000)
    require(not aligned['post_source_release_absolute_impulse_by_group_Ns'],'Nominal recorded contact disposition differs')
    return {'status':'PASS','manifest_files_verified':len(entries),'adopted_native_records_verified':42,
            'source_work_balances_recomputed_from_dense_data':source_checks,'pose_refinement_pairs_recomputed':len(recomputed),
            'no_contact_conservation_recomputed_from_sampled_raw_data':controls,
            'recorded_native_contact_diagnostics_reaggregated':recorded,
            'limitations':['Complete native contact-wrench conservation is recorded, not independently reconstructed: per-step contact wrenches were not exported.',
                           'No MuJoCo runtime used and no physics regenerated.','Physical repeatability requires correlation with an instrumented article.']}

if __name__=='__main__':
    try:print(json.dumps(verify(),indent=2))
    except Exception as error:
        print(json.dumps({'status':'FAIL','error':str(error)},indent=2));sys.exit(1)
