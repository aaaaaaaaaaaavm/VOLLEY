#!/usr/bin/env python3
"""Independent bookkeeping checks and native Orekit endpoint replays.
Does not import the Python targeter or reset native host states at arc boundaries.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import argparse,csv,hashlib,json,math,subprocess
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def norm(v):return math.sqrt(sum(x*x for x in v))
def invariant(state):
    r=state[:3];v=state[3:6];radius=norm(r)
    energy=.5*sum(x*x for x in v)-3.986004418e14/radius+3.986004418e14*1.08262668e-3*6378137.**2/(2*radius**3)*(3*(r[2]/radius)**2-1)
    return energy,r[0]*v[1]-r[1]*v[0]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--jars-dir',type=Path,required=True);ap.add_argument('--captured',action='store_true');args=ap.parse_args()
    summary=load(H/'SUMMARY.json');rows=summary['cases'];selected=[];unique={};checks=[]
    for family in sorted({r['family'] for r in rows}):
        for limit in [1.,5.]:
            for architecture in ['gen5','spring_fixed2','spring_pretrim']:
                eligible=[r for r in rows if r['family']==family and r['architecture']==architecture and r['authority_results'][str(limit)]['feasible_in_declared_candidate']]
                best=min(eligible,key=lambda r:r['fuel_used_kg']) if eligible else None
                selected.append(dict(family=family,architecture=architecture,force_limit_N=limit,
                    case=None if best is None else best['case_stem'],fuel_kg=None if best is None else best['fuel_used_kg'],
                    peak_force_N=None if best is None else best['peak_force_N'],candidate_pass=best is not None))
                if best:unique[best['case_stem']]='selected_feasible'
        # Keep one failed force-ceiling control per alternating family as a diagnostic.
        if 'alternating' in family:
            fixed=min([r for r in rows if r['family']==family and r['architecture']=='spring_fixed2'],key=lambda r:r['peak_force_N'])
            if fixed['peak_force_N']>5:unique[fixed['case_stem']]='diagnostic_above_force_ceiling'
    for r in rows:
        full=load(H/'model/release'/(r['case_stem']+'.json'));n=int(r['family'].split('_')[0][1:])
        assert full['completed_targeting'] and len(full['deliveries'])==n and len(full['legs'])==n+1
        expected_initial=500+full['device_retained_dry_kg']+4*n
        assert abs(full['initial_state'][6]-expected_initial)<1e-9
        state=full['initial_state'];now=0;fuel=0;released=0;max_mass=0;max_momentum=0;max_mapping=0
        for index,e in enumerate(full['events']):
            assert abs(e['start_s']-now)<1e-7 and max(abs(a-b) for a,b in zip(state,e['before']))<1e-8
            if e['kind']=='arc':
                flow=norm(e['force_N'])*(e['end_s']-e['start_s'])/(220*9.80665)
                max_mass=max(max_mass,abs(e['before'][6]-e['after'][6]-flow));fuel+=flow
            else:
                prior=full['events'][index-1];following=full['events'][index+1]
                assert prior['label']=='pre_release_zero_force_guard' and prior['end_s']-prior['start_s']>=5-1e-8 and norm(prior['force_N'])==0
                assert following['label']=='post_release_guard' and following['end_s']-following['start_s']>=20-1e-8 and norm(following['force_N'])==0
                M=state[6];m=e['payload_mass_kg'];u=e['u_m_s']
                assert m==4 and abs(e['after'][6]-(M-m))<1e-10
                vp=[state[3+i]-m/M*u[i] for i in range(3)]
                vc=[state[3+i]+(1-m/M)*u[i] for i in range(3)]
                residual=norm([m*vc[i]+(M-m)*vp[i]-M*state[3+i] for i in range(3)])
                max_momentum=max(max_momentum,residual)
                assert max(abs(vp[i]-e['after'][3+i]) for i in range(3))<1e-9
                if full['architecture']=='gen5':
                    assert 1<=e['command_m_s']<=3
                    expected=e['measured_release_m_s']*(M-m-e['reusable_sled_kg'])/(M-m)
                    max_mapping=max(max_mapping,abs(norm(u)-expected))
                released+=m
            now=e['end_s'];state=e['after']
        assert now==91800 and abs(fuel-full['fuel_used_kg'])<1e-8
        assert abs(state[6]-(expected_initial-fuel-released))<1e-8
        assert max_mass<1e-8 and max_momentum<1e-6 and max_mapping<1e-12
        assert all(q['position_residual_m']<.001 and q['velocity_residual_m_s']<1e-6 for q in full['legs'])
        if full['architecture']=='gen5':assert min(q['coast_s'] for q in full['legs'][:n])>=400-1e-8
        checks.append(dict(case=r['case_stem'],payload_count=n,mass_flow_residual_kg=max_mass,
            momentum_residual_kg_m_s=max_momentum,recoil_mapping_residual_m_s=max_mapping,
            fuel_budget_pass=fuel<=20,force_results=full['authority_results'],all_bookkeeping_targeting_guard_checks_pass=True))
    native=H/'native';native.mkdir(exist_ok=True);classes=H/'runtime/classes';classes.mkdir(parents=True,exist_ok=True)
    jar_classpath=':'.join(str(p) for p in sorted(args.jars_dir.glob('*.jar')))
    compile_command=['java','com.sun.tools.javac.Main','-cp',jar_classpath,'-d',str(classes),str(H/'model/FiniteReplay.java')]
    if not args.captured:
        compile_run=subprocess.run(compile_command,text=True,capture_output=True)
        (H/'runtime/compile.log').write_text(compile_run.stdout+compile_run.stderr);assert compile_run.returncode==0
    prior={r['name']:r for r in load(H/'INDEPENDENT_CHECKS.json')['native_replays']} if args.captured else {}
    jobs=[dict(stem=s,name=s,step=60,category=c) for s,c in unique.items()]
    jobs += [dict(stem=r['case_stem'],name=r['case_stem']+'_refine30',step=30,category='step_refinement') for r in rows if r['architecture']=='gen5']
    def worker(job):
        source=H/'model/release'/(job['stem']+'.csv');prefix=native/job['name']
        cmd=['java','-cp',str(classes)+':'+str(args.jars_dir/'*'),'FiniteReplay',str(source),str(prefix),str(job['step']),'1','1','0','91800']
        if args.captured:
            assert prior[job['name']]['command_sha256']==sha(source)
            for name,digest in prior[job['name']]['output_sha256'].items():assert sha(native/name)==digest
        else:
            run=subprocess.run(cmd,text=True,capture_output=True,timeout=180);Path(str(prefix)+'.log').write_text(run.stdout+run.stderr)
            assert run.returncode==0,(job['name'],run.stderr)
        payload=list(csv.DictReader(Path(str(prefix)+'_payload.csv').open()));host=list(csv.DictReader(Path(str(prefix)+'_host.csv').open()))
        expected=int(job['stem'].split('_')[0][1:]);assert len(payload)==expected
        commands=list(csv.DictReader(source.open()));mass=float(commands[0]['mass_after_kg']);mass_res=[]
        for command,actual in zip(commands[1:],host):
            if command['kind']=='arc':mass-=norm([float(command[k]) for k in ['fx_or_ux','fy_or_uy','fz_or_uz']])*(float(command['end_s'])-float(command['start_s']))/(220*9.80665)
            else:mass-=float(command['payload_mass_kg'])
            mass_res.append(abs(mass-float(actual['mass_kg'])))
        planned=load(H/'model/release'/(job['stem']+'.json'))['deliveries'];energy=[];angular=[]
        for expected_state,actual in zip(planned,payload):
            e0,h0=invariant(expected_state['child_state'])
            ef,hf=invariant([float(actual[k]) for k in ['x_m','y_m','z_m','vx_m_s','vy_m_s','vz_m_s']])
            energy.append(abs(ef-e0)/abs(e0));angular.append(abs(hf-h0)/abs(h0))
        result=dict(**job,command=cmd,payload_count=len(payload),
            max_payload_position_error_m=max(float(a['position_target_error_m']) for a in payload),
            max_payload_velocity_error_m_s=max(float(a['velocity_target_error_m_s']) for a in payload),
            max_host_position_difference_m=max(float(a['position_difference_m']) for a in host),
            max_host_velocity_difference_m_s=max(float(a['velocity_difference_m_s']) for a in host),
            max_host_mass_difference_kg=max(abs(float(a['mass_difference_kg'])) for a in host),
            max_independent_mass_flow_residual_kg=max(mass_res),
            max_J2_coast_relative_energy_change=max(energy),max_J2_coast_relative_axial_angular_momentum_change=max(angular),
            max_momentum_residual_kg_m_s=max(float(a['momentum_residual_kg_m_s']) for a in payload),
            command_sha256=sha(source),native_source_sha256=sha(H/'model/FiniteReplay.java'),
            output_sha256={q.name:sha(q) for q in [Path(str(prefix)+'.log'),Path(str(prefix)+'_host.csv'),Path(str(prefix)+'_payload.csv')]})
        assert result['max_payload_position_error_m']<.01 and result['max_payload_velocity_error_m_s']<1e-5,result
        assert result['max_host_mass_difference_kg']<1e-8 and result['max_independent_mass_flow_residual_kg']<1e-8,result
        assert result['max_momentum_residual_kg_m_s']<1e-6,result
        assert max(energy)<1e-9 and max(angular)<1e-9,result
        print(json.dumps({k:result[k] for k in ['name','category','max_payload_position_error_m','max_host_position_difference_m']}),flush=True)
        return result
    results=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(worker,j) for j in jobs]):results.append(future.result())
    refinements=[]
    for job in jobs:
        if job['category']!='step_refinement':continue
        a=list(csv.DictReader((native/(job['stem']+'_payload.csv')).open()))
        b=list(csv.DictReader((native/(job['name']+'_payload.csv')).open()))
        diff=max(norm([float(x[k])-float(y[k]) for k in ['x_m','y_m','z_m']]) for x,y in zip(a,b))
        assert diff<.001
        refinements.append(dict(case=job['stem'],maximum_terminal_position_change_m=diff,pass_1mm=True))
    out=dict(study='ACR1-PARTIAL-OCCUPANCY-01',passed=True,selected=selected,
        independent_conservation_and_guards=checks,native_replays=sorted(results,key=lambda x:x['name']),
        native_step_refinements=refinements,jar_sha256={q.name:sha(q) for q in sorted(args.jars_dir.glob('*.jar'))},
        compile_command=compile_command,notes='Constant inertial-force fixed-axis J2 numerical agreement; not physical delivery accuracy or host attitude acceptance.')
    (H/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    with (H/'SELECTED_OUTCOMES.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(selected[0]));writer.writeheader();writer.writerows(selected)
    print('PASS',len(checks),'candidate conservation/guard checks;',len(results),'actual native endpoint replays;',len(refinements),'step refinements',flush=True)

if __name__=='__main__':main()
