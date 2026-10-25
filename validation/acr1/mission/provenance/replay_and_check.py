"""Actual independent native Orekit replays and conservation/timing checks."""
from pathlib import Path
import argparse,concurrent.futures,csv,hashlib,json,math,os,subprocess

H=Path(__file__).resolve().parent

def norm(v):return math.sqrt(sum(x*x for x in v))

def main(classpath):
    summary=json.loads((H.parent/'MISSION_RETARGET_SUMMARY.json').read_text())
    jobs=[]
    for c in summary['cases']:
        jobs.append(dict(name=Path(c['file']).stem,source=Path(c['file']).with_suffix('.csv').name,
            category='nominal',step=60,force=1,shot=1,dx=0))
    for c in [x for x in summary['cases'] if x['architecture']=='volley' and x['allowance_kg']==25]:
        stem=Path(c['file']).stem;source=Path(c['file']).with_suffix('.csv').name
        jobs.append(dict(name=stem+'_refine30',source=source,category='refinement',step=30,force=1,shot=1,dx=0))
        for label,force,shot,dx in [('force_minus0p1pct',.999,1,0),('force_plus0p1pct',1.001,1,0),
            ('shot_minus0p1pct',1,.999,0),('shot_plus0p1pct',1,1.001,0),('initial_x_minus10m',1,1,-10),('initial_x_plus10m',1,1,10)]:
            jobs.append(dict(name=stem+'_'+label,source=source,category='sensitivity',step=60,force=force,shot=shot,dx=dx))
        # Change actual3U masses4→6kg without retargeting frozen force commands.
        # Initial carried mass and every later mass record retain the extra mass
        # until that particular payload leaves; no host state is reset.
        original=list(csv.DictReader((H/'release'/source).open()))
        extra=2*sum(r['kind']=='shot' and abs(float(r['payload_mass_kg'])-4)<1e-9 for r in original)
        altered=[]
        for r in original:
            q=dict(r)
            if q['kind']=='shot' and abs(float(q['payload_mass_kg'])-4)<1e-9:
                q['payload_mass_kg']='6.0';extra-=2
            q['mass_after_kg']=str(float(q['mass_after_kg'])+extra)
            altered.append(q)
        mass_source=stem+'_payload3U6kg_frozen_commands.csv'
        with (H/'release'/mass_source).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(original[0]));w.writeheader();w.writerows(altered)
        jobs.append(dict(name=stem+'_payload3U6kg_frozen_commands',source=mass_source,category='sensitivity',step=60,force=1,shot=1,dx=0))
    out=H/'native';out.mkdir(exist_ok=True)
    def worker(j):
        cmd=['java','-cp',classpath,str(H/'FiniteReplay.java'),str(H/'release'/j['source']),str(out/j['name']),str(j['step']),str(j['force']),str(j['shot']),str(j['dx'])]
        r=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
        (out/(j['name']+'.log')).write_text(r.stdout+r.stderr)
        assert r.returncode==0,(j['name'],r.stderr)
        payload=list(csv.DictReader((out/(j['name']+'_payload.csv')).open()))
        host=list(csv.DictReader((out/(j['name']+'_host.csv')).open()))
        commands=list(csv.DictReader((H/'release'/j['source']).open()))
        mass=float(commands[0]['mass_after_kg']);mass_residual=[]
        assert len(commands)-1==len(host)
        for command,actual in zip(commands[1:],host):
            if command['kind']=='arc':
                F=norm([float(command[k])*j['force'] for k in ('fx_or_ux','fy_or_uy','fz_or_uz')])
                mass-=F*(float(command['end_s'])-float(command['start_s']))/(220*9.80665)
            else:mass-=float(command['payload_mass_kg'])
            mass_residual.append(abs(mass-float(actual['mass_kg'])))
        result={**j,'command':cmd,'exit_code':r.returncode,
            'max_payload_target_position_error_m':max(float(x['position_target_error_m']) for x in payload),
            'max_payload_target_velocity_error_m_s':max(float(x['velocity_target_error_m_s']) for x in payload),
            'max_host_position_difference_m':max(float(x['position_difference_m']) for x in host),
            'max_host_mass_difference_kg':max(abs(float(x['mass_difference_kg'])) for x in host),
            'max_mass_conservation_residual_kg':max(mass_residual),
            'max_momentum_residual_kg_m_s':max(float(x['momentum_residual_kg_m_s']) for x in payload)}
        print(j['name'],j['category'],result['max_payload_target_position_error_m'],flush=True)
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(worker,jobs))
    checks=[]
    for c in summary['cases']:
        r=json.loads((H/'release'/c['file']).read_text());state=r['initial_state'];now=r['initial_time_s'];used=0;released=0
        expected_mass=300+c['device_kg']+c['fuel_kg']+(10.66 if c['count']==4 else 31.98)
        assert abs(state[6]-expected_mass)<1e-8
        last_arc=None
        for e in r['events']:
            assert abs(e['start_s']-now)<1e-7
            assert max(abs(a-b) for a,b in zip(e['before'],state))<1e-8
            if e['kind']=='arc':
                mass_used=norm(e['force_N'])*(e['end_s']-e['start_s'])/(220*9.80665)
                assert abs(e['before'][6]-e['after'][6]-mass_used)<1e-8
                used+=mass_used;last_arc=e
            else:
                assert last_arc['label']=='pre_release_zero_force_guard'
                assert norm(last_arc['force_N'])==0
                assert last_arc['end_s']-last_arc['start_s']>=5-1e-8
                m=e['payload_mass_kg'];M=state[6];released+=m
                for j in range(3):assert abs(e['after'][j+3]-(state[j+3]-m/M*e['u_m_s'][j]))<1e-9
                assert abs(e['after'][6]-(M-m))<1e-9
            state=e['after'];now=e['end_s']
        assert abs(used-r['fuel_used_kg'])<1e-8
        assert abs(state[6]-(r['initial_state'][6]-used-released))<1e-8
        assert now==90000 and r['completed_targeting']
        assert r['feasible_in_declared_model']==(r['fuel_limit_pass'] and r['force_limit_pass'])
        if c['architecture']=='volley':assert c['feeder_allocation_fits_coast']
        checks.append(dict(case=c['label'],mass_flow_recoil_epochs_guards=True,coast_feeder_budget=c['feeder_allocation_fits_coast']))
    nominal=[r for r in results if r['category']=='nominal']
    assert all(r['max_payload_target_position_error_m']<.01 for r in nominal)
    assert all(r['max_payload_target_velocity_error_m_s']<1e-5 for r in nominal)
    assert all(r['max_host_mass_difference_kg']<1e-8 for r in nominal)
    assert all(r['max_mass_conservation_residual_kg']<1e-8 for r in results)
    assert all(r['max_momentum_residual_kg_m_s']<1e-6 for r in results)
    refinements=[]
    for r in [x for x in results if x['category']=='refinement']:
        base=r['name'].removesuffix('_refine30')
        a=list(csv.DictReader((out/(base+'_payload.csv')).open()))
        b=list(csv.DictReader((out/(r['name']+'_payload.csv')).open()))
        delta=max(norm([float(x[k])-float(y[k]) for k in ('x_m','y_m','z_m')]) for x,y in zip(a,b))
        assert delta<.001
        refinements.append(dict(case=base,max_payload_position_change_m=delta,pass_1mm=True))
    checked=dict(study='FBR-02',run_count=len(results),native_runs=results,conservation_and_timing=checks,native_time_step_refinement=refinements,
        retained_scope='Numerical model consistency; no actual host, motor, delivery precision, loaded fit or flight qualification')
    (H.parent/'NATIVE_REPLAY_CHECKS.json').write_text(json.dumps(checked,indent=2)+'\n')
    print('PASS',len(results),'native runs;',len(checks),'campaign checks',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--classpath',required=True);a=p.parse_args();main(a.classpath)
