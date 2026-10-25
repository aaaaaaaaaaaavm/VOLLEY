"""Close engine-only disposal from nominal and failed campaign terminal states.

Coast to next apolune,consume finite attitude preparation,hold a fixed inertial
engine direction during the burn,and independently replay the frozen sequence
with GMAT40/40+Earth/Sun. Payload recoil supplies no disposal credit.
"""
import argparse
import gzip
import json
import math
import subprocess
from datetime import datetime,timedelta
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.spatial.transform import Rotation

from lunar_campaign import Campaign,unit,norm
from lunar_native import HERE,sha,make_script


def calculate(source,config):
    model=Campaign(config,config['authority_cases'][3]);remaining_ids=set(source['retained_payload_ids'])
    model.remaining=[i for i,x in enumerate(model.manifest) if x['id'] in remaining_ids]
    model.state=np.array(source['final_host_state']);model.now=source['elapsed_s'];initial=model.state.copy();start=model.now
    period=2*math.pi*math.sqrt(((model.radius+100000+model.radius+1000000)/2)**3/model.mu)
    def rhs(t,y):return np.r_[y[3:6],-model.mu*y[:3]/norm(y[:3])**3]
    def apo(t,y):return np.dot(y[:3],y[3:6])
    apo.terminal=True;apo.direction=-1
    sol=solve_ivp(rhs,[start,start+2*period],initial[:6],events=apo,method='DOP853',rtol=2e-12,atol=1e-8,max_step=60)
    assert sol.t_events[0].size
    delay=sol.t[-1]-start;model.state[:6]=sol.y[:,-1];model.now=sol.t[-1]
    normal=unit(np.cross(model.state[:3],model.state[3:6]));x=-unit(model.state[3:6]);z=normal;y=np.cross(z,x)
    model.events=[];model.native_events=[];model.history=[];model.main_prop=0;model.attitude_prop=0;model.peak_torque=0;model.peak_rate=0
    model.slew(Rotation.from_matrix(np.stack([x,y,z],axis=1)),'disposal_axis_preparation')
    prep_duration=model.now-(start+delay);prepared=model.state.copy();direction=Rotation.from_quat(prepared[7:11]).apply([1,0,0])
    m0=model.mass_props(model.remaining,prepared[6])[0];thrust=20;isp=220;ce=9.80665*isp
    def burn_rhs(t,y):return np.r_[y[3:6],-model.mu*y[:3]/norm(y[:3])**3+thrust/y[6]*direction,-thrust/ce]
    def burn(t):return solve_ivp(burn_rhs,[0,t],np.r_[prepared[:6],m0],method='DOP853',rtol=2e-12,atol=1e-8,max_step=10)
    def peri(y):
        r,v=y[:3],y[3:6];h=np.cross(r,v);energy=np.dot(v,v)/2-model.mu/norm(r);a=-model.mu/(2*energy);e=norm(np.cross(v,h)/model.mu-r/norm(r));return a*(1-e)-model.radius
    duration=brentq(lambda t:peri(burn(t).y[:,-1])+100000,.001,2500,xtol=1e-8)
    b=burn(duration);end=b.y[:,-1]
    def impact(t,y):return norm(y[:3])-model.radius
    impact.terminal=True;impact.direction=-1
    coast=solve_ivp(rhs,[0,86400],end[:6],events=impact,method='DOP853',rtol=2e-12,atol=1e-8,max_step=60)
    prop_main=m0-end[6];prop_total=prop_main+model.attitude_prop
    return dict(initial_host_state=initial.tolist(),initial_epoch_offset_s=start,retained_payloads=len(model.remaining),
                coast_to_apolune_s=delay,attitude_preparation_s=prep_duration,attitude_preparation_propellant_kg=model.attitude_prop,
                prepared_state=prepared.tolist(),fixed_inertial_thrust_direction=direction.tolist(),
                burn_duration_s=duration,main_propellant_kg=prop_main,total_additional_disposal_propellant_kg=prop_total,
                propellant_after_disposal_kg=initial[6]-prop_total,
                fits_independent8kg_disposal_allocation=bool(prop_total<8),
                postcampaign_to_sphere_s=delay+prep_duration+duration+coast.t[-1],
                point_mass_sphere_hit=bool(coast.t_events[0].size),
                peak_preparation_torque_N_m=model.peak_torque,peak_preparation_rate_deg_s=math.degrees(model.peak_rate))


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmat',required=True,type=Path);p.add_argument('--gravity',required=True,type=Path);args=p.parse_args()
    c=json.loads((HERE/'campaign_inputs.json').read_text());l=json.loads((HERE/'study_inputs.json').read_text())['lunar'];out=HERE/'campaign_disposal';out.mkdir(exist_ok=True);cases=[]
    names=['T5_R20_searched','pre_command_isolated_cell_failure','unresolved_shared_path_failure']
    for name in names:
        sourcepath=HERE/'campaign'/(name+'.json');source=json.loads(sourcepath.read_text());calc=calculate(source,c)
        epoch=datetime(2026,10,25,12)+timedelta(seconds=calc['initial_epoch_offset_s'])
        local=dict(l);local['epoch_utc']=epoch.strftime('%d %b %Y %H:%M:%S.')+f'{epoch.microsecond//1000:03d}'
        history=out/(name+'.txt');script=out/(name+'.script');archive=history.with_suffix('.txt.gz')
        text=make_script(local,40,0,1000,args.gravity,history)
        initial=calc['initial_host_state'];dry=280+4*calc['retained_payloads']
        for key,value in zip(['X','Y','Z','VX','VY','VZ'],initial[:6]):
            import re
            text=re.sub(rf'Payload\.{key} = [^;]+;',f'Payload.{key} = {value/1000:.16g};',text)
        text=text.replace('Payload.DryMass = 4;',f'Payload.DryMass = {dry};\nPayload.Tanks = {{Reserve}};\nPayload.Thrusters = {{Engine}};')
        hardware=f'''Create ChemicalTank Reserve;
Reserve.AllowNegativeFuelMass = false;
Reserve.PressureModel = PressureRegulated;
Reserve.FuelMass = {initial[6]:.16g};
Create ChemicalThruster Engine;
Engine.CoordinateSystem = MoonFrame;
Engine.DecrementMass = true;
Engine.Tank = {{Reserve}};
Engine.MixRatio = [1];
Engine.GravitationalAccel = 9.80665;
Engine.C1 = 20;
Engine.K1 = 220;
Engine.ThrustDirection1 = {calc['fixed_inertial_thrust_direction'][0]:.16g};
Engine.ThrustDirection2 = {calc['fixed_inertial_thrust_direction'][1]:.16g};
Engine.ThrustDirection3 = {calc['fixed_inertial_thrust_direction'][2]:.16g};
Create FiniteBurn Disposal;
Disposal.Thrusters = {{Engine}};
'''
        text=hardware+text[:text.index('BeginMissionSequence;')]
        text=text.replace('Payload.Luna.ECC};','Payload.Luna.ECC,Payload.TotalMass};')
        text+=f'''BeginMissionSequence;
Propagate MoonProp(Payload) {{Payload.ElapsedSecs = {calc['coast_to_apolune_s']+calc['attitude_preparation_s']:.16g}}};
Payload.Reserve.FuelMass = {calc['prepared_state'][6]:.16g};
BeginFiniteBurn Disposal(Payload);
Propagate MoonProp(Payload) {{Payload.ElapsedSecs = {calc['burn_duration_s']:.16g}}};
EndFiniteBurn Disposal(Payload);
Propagate MoonProp(Payload) {{Payload.Luna.RMAG = 1737.4,Payload.ElapsedSecs = 86400}};
'''
        if archive.exists() and (not script.exists() or script.read_text()!=text):raise RuntimeError('Postcampaign disposal cached source changed')
        script.write_text(text)
        if not archive.exists():
            r=subprocess.run([str(args.gmat),'--run',str(script)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/(name+'.log')).write_text(r.stdout)
            if r.returncode or 'Mission run completed' not in r.stdout:raise RuntimeError('Native postcampaign disposal failed:'+name)
            with gzip.open(archive,'wb') as f:f.write(history.read_bytes())
            history.unlink()
        rows=[]
        with gzip.open(archive,'rt') as f:
            for line in f:
                try:vals=[float(x) for x in line.split()]
                except ValueError:continue
                if len(vals)==5:rows.append(vals)
        last=rows[-1];native_prop=dry+initial[6]-last[4]
        calc.update(case=name,source_campaign_sha256=sha(sourcepath),script_sha256=sha(script),history_sha256=sha(archive),
                    native_sphere_hit=bool(abs(last[1]-1737.4)<1e-5 and last[0]*86400<86400),
                    native_postcampaign_to_sphere_s=last[0]*86400,native_disposal_propellant_kg=native_prop,
                    native_fits8kg_disposal_allocation=bool(native_prop<8))
        cases.append(calc)
    result=dict(study='PCS-POSTCAMPAIGN-DISPOSAL-01',generator_sha256=sha(__file__),cases=cases,
                all_native_hit_within24h=all(x['native_sphere_hit'] for x in cases),all_fit_independent8kg=all(x['native_fits8kg_disposal_allocation'] for x in cases),
                no_release_recoil_credit=True,
                limits='Campaign terminal states are the point-gravity control solution; future native propagation is40/40+Earth/Sun. No accepted impact site,engine/provider capability orpolicy approval follows.')
    (HERE/'CAMPAIGN_DISPOSAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({x['case']:{k:x[k] for k in ['native_sphere_hit','native_disposal_propellant_kg','native_postcampaign_to_sphere_s']} for x in cases},indent=2))


if __name__=='__main__':main()
