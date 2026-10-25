"""Native GMAT finite-thrust, mass-depleting, perturbed lunar disposal replay.

Replays analytical cutoff durations; no targeter adjusts them after viewing native
results. Includes all-payload failure and bounded execution/pointing disturbances.
"""
import argparse
import gzip
import json
import math
import subprocess
from pathlib import Path

from lunar_native import HERE, make_script, sha


def script_for(case,c,degree,gravity,output):
    text=make_script(c,degree,0,case['staging_apo_km'],gravity,output)
    failed=case['failed_retained_payload_count']; angle=math.radians(case['pointing_error_deg'])
    dry=c['retained_dry_mass_kg']+failed*c['payload_kg']
    text=text.replace(f"Payload.DryMass = {c['payload_kg']};",f"Payload.DryMass = {dry};\nPayload.Tanks = {{Reserve}};\nPayload.Thrusters = {{Engine}};")
    hardware=f"""Create ChemicalTank Reserve;
Reserve.AllowNegativeFuelMass = false;
Reserve.FuelMass = 20;
Reserve.PressureModel = PressureRegulated;
Create ChemicalThruster Engine;
Engine.CoordinateSystem = Local;
Engine.Origin = Luna;
Engine.Axes = VNB;
Engine.ThrustDirection1 = {-math.cos(angle):.16g};
Engine.ThrustDirection2 = 0;
Engine.ThrustDirection3 = {math.sin(angle):.16g};
Engine.DutyCycle = 1;
Engine.ThrustScaleFactor = 1;
Engine.DecrementMass = true;
Engine.Tank = {{Reserve}};
Engine.MixRatio = [1];
Engine.GravitationalAccel = 9.80665;
Engine.C1 = {c['disposal_thrust_N']};
Engine.K1 = {c['disposal_Isp_s']};
Create FiniteBurn Disposal;
Disposal.Thrusters = {{Engine}};
"""
    # Parameters referencing hardware must be created after hardware.
    text=hardware+text
    text=text[:text.index('BeginMissionSequence;')]+f"""BeginMissionSequence;
BeginFiniteBurn Disposal(Payload);
Propagate MoonProp(Payload) {{Payload.ElapsedSecs = {case['burn_duration_s']:.16g}}};
EndFiniteBurn Disposal(Payload);
Propagate MoonProp(Payload) {{Payload.Luna.RMAG = {c['reference_radius_km']}, Payload.ElapsedSecs = 86400}};
"""
    text=text.replace('Payload.Luna.ECC};','Payload.Luna.ECC, Payload.TotalMass};')
    return text


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmat',required=True,type=Path);p.add_argument('--gravity',required=True,type=Path);args=p.parse_args()
    c=json.loads((HERE/'study_inputs.json').read_text())['lunar']
    analytical=json.loads((HERE/'STUDY_RESULTS.json').read_text())['lunar']['engine_only_finite_disposal_cases']
    selected=[x for x in analytical if x['failed_retained_payload_count'] in [0,12]]
    native=HERE/'disposal_native';native.mkdir(exist_ok=True);results=[]
    for case in selected:
        degrees=c['gravity_degrees'] if case['pointing_error_deg']==0 else [40]
        for degree in degrees:
            stem=f"apo{case['staging_apo_km']}_failed{case['failed_retained_payload_count']}_duration{case['burn_execution_multiplier']}_point{case['pointing_error_deg']}_d{degree}"
            script=native/(stem+'.script');output=native/(stem+'.txt');gzpath=output.with_suffix('.txt.gz')
            source=script_for(case,c,degree,args.gravity,output)
            if gzpath.exists() and (not script.exists() or script.read_text()!=source):
                raise RuntimeError(f'Cached report has different source: {stem}; reproduce in a separate package copy')
            script.write_text(source)
            receipt=native/(stem+'.receipt.json')
            expected=dict(script_sha256=sha(script),GMAT_binary_sha256=sha(args.gmat),gravity_file_sha256=sha(args.gravity))
            if gzpath.exists() and receipt.exists() and json.loads(receipt.read_text())!=expected:
                raise RuntimeError(f'Cached report has different runtime: {stem}; reproduce in a separate package copy')
            if not gzpath.exists():
                r=subprocess.run([str(args.gmat),'--run',str(script)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                (native/(stem+'.log')).write_text(r.stdout)
                if r.returncode or not output.exists() or 'Mission run completed' not in r.stdout:
                    raise RuntimeError(f'Native disposal failed: {stem}; inspect exact log')
                with gzip.open(gzpath,'wb') as f:f.write(output.read_bytes())
                output.unlink()
            receipt.write_text(json.dumps(expected,indent=2)+'\n')
            rows=[]
            with gzip.open(gzpath,'rt') as f:
                for line in f:
                    try:vals=[float(x) for x in line.split()]
                    except ValueError:continue
                    if len(vals)==5:rows.append(vals)
            last=rows[-1]
            hit=abs(last[1]-c['reference_radius_km'])<1e-5 and last[0]<1
            results.append(dict(case=stem,staging_apo_km=case['staging_apo_km'],
                                failed_payloads=case['failed_retained_payload_count'],degree_order=degree,
                                duration_multiplier=case['burn_execution_multiplier'],pointing_deg=case['pointing_error_deg'],
                                burn_duration_s=case['burn_duration_s'],native_impact_time_s=last[0]*86400,
                                final_radius_km=last[1],native_propellant_used_kg=case['assumed_initial_wet_mass_kg']-last[4],
                                native_impact_within24h=hit,script_sha256=sha(script),report_sha256=sha(gzpath)))
    out=dict(study='PCS-LUNAR-DISPOSAL-NATIVE-01',generator_sha256=sha(__file__),
             input_results_sha256=sha(HERE/'STUDY_RESULTS.json'),
             force_model='GMAT R2026a GRGM900C SPICE/MOON_PA, Earth/Sun DE421, finite20N VNB thruster, Isp220s, mass depletion',
             no_release_recoil_credit=True,all_cases_hit=all(x['native_impact_within24h'] for x in results),cases=results,
             limits='Investigation engine assumptions; no selected supplier, impact site, terrain/approval/compliance, launch/LOI finite-burn closure or flight claim.')
    (HERE/'DISPOSAL_NATIVE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(case_count=len(results),all_cases_hit=out['all_cases_hit'],max_propellant_kg=max(x['native_propellant_used_kg'] for x in results)),indent=2))


if __name__=='__main__':main()
