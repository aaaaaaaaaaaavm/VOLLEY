"""Native Orekit replay, independent conservation and common-epoch checks."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import csv,hashlib,json,math,subprocess
import numpy as np

H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(v):return float(np.linalg.norm(v))
def invariants(state):
    r=np.array(state[:3]);v=np.array(state[3:]);R=norm(r);mu=3.986004418e14;re=6378137.;j2=1.08262668e-3
    energy=.5*np.dot(v,v)-mu/R+mu*j2*re**2/(2*R**3)*(3*(r[2]/R)**2-1)
    return float(energy),float(np.cross(r,v)[2])

def main():
    summary=json.loads((H/'MISSION_COMPARISON.json').read_text());selected=[];unique={}
    for family in ['uniform_2','alternating_1_3']:
        for authority in ['1.0','5.0']:
            for arch in ['gen5','spring_fixed2','spring_pretrim']:
                candidates=[r for r in summary['cases']if r['family']==family and r['architecture']==arch and r['authority_results'][authority]['feasible_in_declared_candidate']]
                best=min(candidates,key=lambda r:r['fuel_used_kg'])if candidates else None
                selected.append(dict(family=family,force_authority_N=float(authority),architecture=arch,best_tested_case=None if best is None else best['case_stem'],fuel_used_kg=None if best is None else best['fuel_used_kg'],peak_force_N=None if best is None else best['peak_force_N'],status='Closed within declaredcandidate bounds'if best else'No tested candidate within force ceiling; no global infeasibility inference'))
                if best:unique[best['case_stem']]='nominal'
    diagnostic=min([r for r in summary['cases']if r['family']=='alternating_1_3'and r['architecture']=='spring_fixed2'],key=lambda r:r['peak_force_N']);unique[diagnostic['case_stem']]='diagnostic_above_force_ceiling'
    jobs=[dict(stem=stem,name=stem,step=60,category=category)for stem,category in unique.items()]
    for family in ['uniform_2','alternating_1_3']:
        stem=next(r['case_stem']for r in summary['cases']if r['family']==family and r['architecture']=='gen5');jobs.append(dict(stem=stem,name=stem+'_refine30',step=30,category='step_refinement'))
    (H/'SELECTED_CASES.json').write_text(json.dumps(dict(selected=selected,native_jobs=jobs),indent=2)+'\n')
    def worker(job):
        source=H/'release'/(job['stem']+'.csv');prefix=H/'native'/job['name'];prefix.parent.mkdir(exist_ok=True)
        command=['java','-cp','/workspace/volley-work/2026-10-18/jars/*',str(H/'FiniteReplay.java'),str(source),str(prefix),str(job['step']),'1','1','0','91800']
        reuse=(job['name']=='uniform_2_gen5_f0.35'and prefix.with_name(prefix.name+'_host.csv').exists()and(H/'provisional_window_set/release'/source.name).exists()and sha(source)==sha(H/'provisional_window_set/release'/source.name))
        if not reuse:
            process=subprocess.run(command,capture_output=True,text=True,timeout=180,cwd=H);Path(str(prefix)+'.log').write_text(process.stdout+process.stderr);assert process.returncode==0,(job['name'],process.stderr)
        else:assert'Native Orekit finite-force replay delivered=12'in Path(str(prefix)+'.log').read_text()
        payload=list(csv.DictReader(prefix.with_name(prefix.name+'_payload.csv').open()));host=list(csv.DictReader(prefix.with_name(prefix.name+'_host.csv').open()));commands=list(csv.DictReader(source.open()));report=json.loads((H/'release'/(job['stem']+'.json')).read_text());mass=float(commands[0]['mass_after_kg']);residuals=[]
        assert len(payload)==12 and len(host)==len(commands)-1
        for commandrow,actual in zip(commands[1:],host):
            if commandrow['kind']=='arc':mass-=norm([float(commandrow[k])for k in ['fx_or_ux','fy_or_uy','fz_or_uz']])*(float(commandrow['end_s'])-float(commandrow['start_s']))/(220*9.80665)
            else:mass-=float(commandrow['payload_mass_kg'])
            residuals.append(abs(mass-float(actual['mass_kg'])))
        energy=[];angular=[]
        for planned,actual in zip(report['deliveries'],payload):
            e0,h0=invariants(planned['child_state']);ef,hf=invariants([float(actual[k])for k in ['x_m','y_m','z_m','vx_m_s','vy_m_s','vz_m_s']]);energy.append(abs(ef-e0)/abs(e0));angular.append(abs(hf-h0)/abs(h0))
        result={**job,'command':command,'reused_exact_command_bytes_from_actual_prior_run':reuse,'command_csv_sha256':sha(source),'native_source_sha256':sha(H/'FiniteReplay.java'),'payload_count':len(payload),'max_payload_target_position_error_m':max(float(r['position_target_error_m'])for r in payload),'max_payload_target_velocity_error_m_s':max(float(r['velocity_target_error_m_s'])for r in payload),'max_host_position_difference_m':max(float(r['position_difference_m'])for r in host),'max_host_velocity_difference_m_s':max(float(r['velocity_difference_m_s'])for r in host),'max_host_mass_difference_kg':max(abs(float(r['mass_difference_kg']))for r in host),'max_independent_mass_flow_residual_kg':max(residuals),'max_momentum_residual_kg_m_s':max(float(r['momentum_residual_kg_m_s'])for r in payload),'max_payload_J2_coast_relative_energy_change':max(energy),'max_payload_J2_coast_relative_axial_angular_momentum_change':max(angular),'output_sha256':{p.name:sha(p)for p in [Path(str(prefix)+'.log'),prefix.with_name(prefix.name+'_host.csv'),prefix.with_name(prefix.name+'_payload.csv')]}}
        assert result['max_payload_target_position_error_m']<.01,result
        assert result['max_payload_target_velocity_error_m_s']<1e-5,result
        assert result['max_independent_mass_flow_residual_kg']<1e-8,result
        assert result['max_host_mass_difference_kg']<1e-8,result
        assert result['max_momentum_residual_kg_m_s']<1e-6,result
        assert max(energy)<1e-9 and max(angular)<1e-9,result
        print(json.dumps({k:result[k]for k in ['name','category','max_payload_target_position_error_m','max_independent_mass_flow_residual_kg']}),flush=True);return result
    native=[]
    with ThreadPoolExecutor(max_workers=2)as pool:
        for result in as_completed([pool.submit(worker,j)for j in jobs]):native.append(result.result())
    conservation=[]
    for row in summary['cases']:
        r=json.loads((H/'release'/(row['case_stem']+'.json')).read_text());state=r['initial_state'];now=0.;used=0.;released=0.;prior_arc=None;mapping_error=0.
        expected=500+r['device_retained_dry_kg']+48;assert abs(state[6]-expected)<1e-9
        for index,e in enumerate(r['events']):
            assert abs(e['start_s']-now)<1e-7 and max(abs(a-b)for a,b in zip(state,e['before']))<1e-8
            if e['kind']=='arc':
                flow=norm(e['force_N'])*(e['end_s']-e['start_s'])/(220*9.80665);assert abs(e['before'][6]-e['after'][6]-flow)<1e-8;used+=flow;prior_arc=e
            else:
                assert prior_arc['label']=='pre_release_zero_force_guard'and norm(prior_arc['force_N'])==0 and prior_arc['end_s']-prior_arc['start_s']>=5-1e-8
                following=r['events'][index+1];assert following['label']=='post_release_guard'and norm(following['force_N'])==0 and following['end_s']-following['start_s']>=20-1e-8
                M=state[6];m=e['payload_mass_kg'];u=np.array(e['u_m_s']);assert norm(np.array(e['after'][3:6])-(np.array(state[3:6])-m/M*u))<1e-9;assert abs(e['after'][6]-(M-m))<1e-9;released+=m
                if r['architecture']=='gen5':
                    expected_u=e['measured_release_m_s']*(M-m-e['reusable_sled_kg'])/(M-m);mapping_error=max(mapping_error,abs(norm(u)-expected_u));assert mapping_error<1e-12
                    child_kick=(1-m/M)*norm(u);assert abs(child_kick-e['measured_release_m_s']*(M-m-e['reusable_sled_kg'])/M)<1e-12
            state=e['after'];now=e['end_s']
        assert r['completed_targeting']and now==91800
        assert abs(used-r['fuel_used_kg'])<1e-8 and abs(state[6]-(r['initial_state'][6]-used-released))<1e-8
        if r['architecture']=='gen5':assert min(l['coast_s']for l in r['legs'][:12])>=400-1e-8
        conservation.append(dict(case=row['case_stem'],mass_flow_recoil_continuity_guards_pass=True,actual_released_payload_kg=released,Gen5_recoil_mapping_max_error_m_s=mapping_error,loading_coast_requirement_applied_only_to_Gen5=True))
    refinements=[]
    for job in jobs:
        if job['category']!='step_refinement':continue
        def values(name):return list(csv.DictReader((H/'native'/(name+'_payload.csv')).open()))
        delta=max(norm([float(a[k])-float(b[k])for k in ['x_m','y_m','z_m']])for a,b in zip(values(job['stem']),values(job['name'])));assert delta<.001;refinements.append(dict(case=job['stem'],max_terminal_PV_position_change_m=delta,pass_1mm=True))
    out=dict(study='G5-MISSION-01',native_run_count=len(native),native_runs=native,conservation_and_guards=conservation,native_step_refinement=refinements,all_declared_numerical_checks_pass=True,scope='Independent numerical consistency of the declared synthetic fixed-axis J2 point-release model; errors are not flight delivery accuracy.')
    (H/'NATIVE_REPLAY_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(native),'native runs;',len(conservation),'candidate conservation/guard checks',flush=True)

if __name__=='__main__':main()
