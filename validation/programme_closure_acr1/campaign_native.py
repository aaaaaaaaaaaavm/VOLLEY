"""Replay source-frozen campaign arcs/releases in independent native GMAT.

GMAT independently propagates finite main burns, recoil jumps and each released
payload. The Python attitude-control trajectory is an imposed command history;
this is an astrodynamics cross-check, not a second attitude/control solver.
"""
import argparse
import gzip
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from lunar_native import HERE,sha


def generate(case,mode,gmat,gravity,out):
    c=json.loads((HERE/'campaign_inputs.json').read_text());l=json.loads((HERE/'study_inputs.json').read_text())['lunar']
    root=gravity.parents[2];degree=0 if mode=='point_mass' else int(mode[-2:])
    initial=case['events'][0]['before']
    lines=["% Frozen PCS-LUNAR-CAMPAIGN-01 replay; native astrodynamics,imposed attitude history.",
           "SolarSystem.EphemerisSource = 'DE421';",f"SolarSystem.DEFilename = '{root/'planetary_ephem/de/leDE1900.421'}';",
           "SolarSystem.EphemerisUpdateInterval = 0;",f"Luna.Mu = {l['mu_moon_km3_s2']};","Luna.EquatorialRadius = 1737.4;","Luna.Flattening = 0;",
           f"Luna.PlanetarySpiceKernelName = {{'{root/'planetary_coeff/SPICELunaCurrentKernel.bpc'}'}};",
           f"Luna.FrameSpiceKernelName = {{'{root/'planetary_coeff/SPICELunaFrameKernel.tf'}'}};",
           "Luna.RotationDataSource = 'SPICE';","Luna.SpiceFrameId = 'MOON_PA';",
           'Create CoordinateSystem MoonFrame;','MoonFrame.Origin = Luna;','MoonFrame.Axes = MJ2000Eq;',
           'Create ChemicalTank Reserve;','Reserve.AllowNegativeFuelMass = false;','Reserve.FuelMass = 20;','Reserve.PressureModel = PressureRegulated;',
           'Create ChemicalThruster Engine;','Engine.CoordinateSystem = MoonFrame;','Engine.ThrustDirection1 = 1;','Engine.ThrustDirection2 = 0;','Engine.ThrustDirection3 = 0;',
           'Engine.DecrementMass = true;','Engine.Tank = {Reserve};','Engine.MixRatio = [1];',f'Engine.GravitationalAccel = {9.80665};',f'Engine.C1 = {c["main_thrust_N"]};',f'Engine.K1 = {c["main_Isp_s"]};',
           'Create FiniteBurn Recovery;','Recovery.Thrusters = {Engine};',
           'Create Spacecraft Host;','Host.DateFormat = UTCGregorian;',f"Host.Epoch = '{l['epoch_utc']}';",'Host.CoordinateSystem = MoonFrame;','Host.DisplayStateType = Cartesian;',
           'Host.DryMass = 328;','Host.Tanks = {Reserve};','Host.Thrusters = {Engine};']
    for key,value in zip(['X','Y','Z','VX','VY','VZ'],initial[:6]):lines.append(f'Host.{key} = {value/1000:.16g};')
    for i in range(1,13):
        lines+= [f'Create Spacecraft P{i};',f'P{i}.DateFormat = UTCGregorian;',f"P{i}.Epoch = '{l['epoch_utc']}';",f'P{i}.CoordinateSystem = MoonFrame;',f'P{i}.DisplayStateType = Cartesian;',f'P{i}.DryMass = 4;']
    lines+=['Create ForceModel FM;','FM.CentralBody = Luna;','FM.Drag = None;','FM.SRP = Off;','FM.RelativisticCorrection = Off;']
    if degree:
        lines+=['FM.PrimaryBodies = {Luna};','FM.PointMasses = {Earth, Sun};',f'FM.GravityField.Luna.Degree = {degree};',f'FM.GravityField.Luna.Order = {degree};',f"FM.GravityField.Luna.PotentialFile = '{gravity}';"]
    else:lines+=['FM.PrimaryBodies = {};','FM.PointMasses = {Luna};']
    lines+=['Create Propagator Prop;','Prop.FM = FM;','Prop.Type = PrinceDormand78;','Prop.InitialStepSize = 10;','Prop.Accuracy = 1e-12;','Prop.MinStep = 0.001;','Prop.MaxStep = 60;','Prop.StopIfAccuracyIsViolated = true;',
            'Create ReportFile Checkpoints;',f"Checkpoints.Filename = '{out/(mode+'_host.txt')}';",'Checkpoints.Precision = 16;','Checkpoints.WriteHeaders = true;']
    # Subscribers capture untouched native payload histories in perturbation runs.
    if degree:
        for i in range(1,13):
            lines +=[f'Create ReportFile R{i};',f"R{i}.Filename = '{out/(mode+f'_P{i}.txt')}';",f'R{i}.Precision = 16;',f'R{i}.WriteHeaders = true;',f'R{i}.Add = {{P{i}.A1ModJulian,P{i}.Luna.RMAG,P{i}.Luna.SMA,P{i}.Luna.ECC}};']
    lines+=['BeginMissionSequence;']
    if degree:
        for i in range(1,13):lines.append(f'Toggle R{i} Off;')
    keys=['X','Y','Z','VX','VY','VZ'];nchild=0;expected=[]
    for event in case['native_events']:
        if event['kind']=='arc':
            duration=event['end_s']-event['start_s'];force=np.asarray(event['force_inertial_N']);F=float(np.linalg.norm(force))
            if F>0:
                for k,value in enumerate(force/F,1):lines.append(f'Host.Engine.ThrustDirection{k} = {value:.16g};')
                lines+=['BeginFiniteBurn Recovery(Host);',f'Propagate Prop(Host) {{Host.ElapsedSecs = {duration:.16g}}};','EndFiniteBurn Recovery(Host);']
            else:
                lines.append(f'Propagate Prop(Host) {{Host.ElapsedSecs = {duration:.16g}}};')
                # Cold-gas couple has zero resultant in this point-mass model.
                # Its mass use is imposed from the independently bounded Python
                # quaternion/Euler solution; main-engine fuel remains native.
                lines.append(f"Host.Reserve.FuelMass = {event['propellant_after_kg']:.16g};")
            expected.append(dict(t_s=event['end_s'],kind='arc'))
        else:
            nchild+=1;i=nchild
            before=next(x['before_host_state'] for x in case['releases'] if x['released'] and x['t_s']==event['t_s'])
            offset=np.array(event['payload_state'])-np.array(before[:6])
            lines.append(f'P{i}.A1ModJulian = Host.A1ModJulian;')
            for key,value in zip(keys,offset):lines.append(f'P{i}.MoonFrame.{key} = Host.MoonFrame.{key} + {value/1000:.16g};')
            jump=event['parent_position_jump_m']+event['parent_velocity_jump_m_s']
            for key,value in zip(keys,jump):lines.append(f'Host.MoonFrame.{key} = Host.MoonFrame.{key} + {value/1000:.16g};')
            lines.append(f"Host.DryMass = {280+event['remaining_payloads']*4};")
            expected.append(dict(t_s=event['t_s'],kind='release'))
        lines.append('Report Checkpoints Host.ElapsedSecs Host.MoonFrame.X Host.MoonFrame.Y Host.MoonFrame.Z Host.MoonFrame.VX Host.MoonFrame.VY Host.MoonFrame.VZ Host.TotalMass;')
    if degree:
        for i in range(1,nchild+1):
            lines += [f'Toggle R{i} On;',f'Propagate Prop(P{i}) {{P{i}.ElapsedSecs = 2592000, P{i}.Luna.RMAG = 1737.4}};',f'Toggle R{i} Off;']
    return '\n'.join(lines)+'\n',expected


def numeric_rows(path):
    with gzip.open(path,'rt') as f:
        result=[]
        for line in f:
            try:values=[float(x) for x in line.split()]
            except ValueError:continue
            if values:result.append(values)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmat',required=True,type=Path);p.add_argument('--gravity',required=True,type=Path);p.add_argument('--point-mass-only',action='store_true');args=p.parse_args()
    casepath=HERE/'campaign/T5_R20_searched.json';case=json.loads(casepath.read_text())
    assert case['released_payloads']==12 and case['nominal_full_manifest_pass'],'No feasible frozen12-release case for native replay'
    out=HERE/'campaign_native';out.mkdir(exist_ok=True);results=[]
    for mode in ['point_mass'] if args.point_mass_only else ['point_mass','harmonic20','harmonic40']:
        source,expected=generate(case,mode,args.gmat,args.gravity,out);script=out/(mode+'.script')
        history=out/(mode+'_host.txt.gz')
        if history.exists() and (not script.exists() or script.read_text()!=source):raise RuntimeError('Cached native campaign source differs; preserve old run before changing inputs')
        script.write_text(source)
        if not history.exists():
            r=subprocess.run([str(args.gmat),'--run',str(script)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (out/(mode+'.log')).write_text(r.stdout)
            if r.returncode or 'Mission run completed' not in r.stdout:raise RuntimeError(f'Native campaign failed:{mode}; inspect actual log')
            for q in out.glob(mode+'*.txt'):
                with gzip.open(q.with_suffix('.txt.gz'),'wb') as f:f.write(q.read_bytes())
                q.unlink()
        rows=numeric_rows(history);assert len(rows)==len(expected),(len(rows),len(expected))
        last=np.array(rows[-1]);goal=np.array(case['final_host_state'])
        result=dict(mode=mode,script_sha256=sha(script),host_history_sha256=sha(history),events=len(rows),
                    final_native_time_s=float(last[0]),final_python_time_s=case['elapsed_s'],
                    final_position_difference_vs_python_m=float(np.linalg.norm(last[1:4]*1000-goal[:3])),
                    final_velocity_difference_vs_python_m_s=float(np.linalg.norm(last[4:7]*1000-goal[3:6])),
                    final_mass_difference_kg=abs(float(last[7])-case['final_mass_kg']),
                    final_native_state_SI=(last[1:7]*1000).tolist(),payload_lifetime=[])
        if mode!='point_mass':
            for i in range(1,13):
                q=out/(mode+f'_P{i}.txt.gz');payload=numeric_rows(q);first,lastp=payload[0],payload[-1]
                elapsed=(lastp[0]-first[0])*86400;minimum=min(x[1]-1737.4 for x in payload)
                result['payload_lifetime'].append(dict(payload=i,elapsed_s=elapsed,min_sampled_altitude_km=minimum,
                                                       native30day_sampled_floor_pass=elapsed>=2592000-.01 and minimum>=20,
                                                       history_sha256=sha(q)))
        results.append(result)
    capture=dict(study='PCS-LUNAR-CAMPAIGN-NATIVE-01',generator_sha256=sha(__file__),campaign_sha256=sha(casepath),
                 GMAT_binary_sha256=sha(args.gmat),gravity_sha256=sha(args.gravity),cases=results,
                 attitude_scope='Native astrodynamics only. Frozen Python finite attitude commands and zero-resultant ACS mass consumption are imposed,not independently solved by GMAT.',
                 interpretation='Point-mass run compares identical dynamics.20/40-degree+Earth/Sun replay measures open-loop environment sensitivity and native30day useful-floor outcomes for the actual released states.')
    (HERE/'CAMPAIGN_NATIVE_RESULTS.json').write_text(json.dumps(capture,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='payload_lifetime'}|dict(native_payloads_pass=sum(x['native30day_sampled_floor_pass'] for x in r['payload_lifetime'])) for r in results],indent=2))


if __name__=='__main__':main()
