#!/usr/bin/env python3
"""Stdlib-only integrity, analytical cross-check and deterministic replay."""
from pathlib import Path
import hashlib, json, math, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for name,expected in manifest['files'].items():
 p=ROOT/name
 assert p.is_file(),f'Missing capture: {name}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,f'Capture changed: {name}'
p=json.loads((ROOT/'PARAMETERS.json').read_text());d=json.loads((ROOT/'results/DRIVE_SCREENS.json').read_text());m=json.loads((ROOT/'results/MECHANICS.json').read_text());source=json.loads((ROOT/'catalog_reference.json').read_text())
extended=json.loads((ROOT/'results/DRIVE_SCREENS_EXTENDED.json').read_text())
# Independent peak-force/speed and thread-torque substitutions from the declared
# triangular motion law. No stored pass string substitutes for a numeric check.
for r in d+extended:
 local=r['kind']=='local_feed';travel=r['stroke_mm']/1000
 T=r['time_s'];mass=p['local_moving_mass_kg' if local else 'receiver_moving_mass_kg']
 a=4*travel/T**2;v=2*travel/T;F=r['resistance_N']+mass*a
 assert math.isclose(F,r['peaks']['force_N'],rel_tol=1e-12)
 if local:
  tan_lambda=(p['screw_lead_mm']/1000)/(math.pi*p['screw_mean_diameter_mm']/1000)
  f=p['screw_mu_assumed']/math.cos(math.radians(p['screw_half_flank_angle_deg']))
  tq=F*p['screw_mean_diameter_mm']/2000*(tan_lambda+f)/(1-f*tan_lambda)+p['bearing_drag_Nm_assumed']
  rpm=60*v/(p['screw_lead_mm']/1000)*p['local_gear_ratio']
 else:
  tq=F*p['receiver_pulley_radius_mm']/1000
  rpm=60*v/(2*math.pi*p['receiver_pulley_radius_mm']/1000)*p['receiver_gear_ratio']
 assert math.isclose(tq,r['peaks']['output_torque_Nm'],rel_tol=1e-12)
 assert math.isclose(rpm,r['peaks']['motor_rpm'],rel_tol=1e-12)
 assert all(r['criteria'].values()) and r['all_declared_sizing_screens_pass']
 assert r['peaks']['motor_torque_Nm']<=source['motor_basis']['rated_torque_Nm']
 assert r['minimum_torque_speed_margin_rpm']>=0
assert m['backdrive']['receiver_holding_screen_pass']
assert math.isclose(p['receiver_brake_static_torque_Nm']/(p['adverse_axial_resistance_N']*p['receiver_pulley_radius_mm']/1000),m['backdrive']['receiver_static_capacity_to_100N_load'],rel_tol=1e-12)
top3=json.loads((ROOT/'results/TOP3_NUMERICAL.json').read_text())
assert all(x['all_declared_sizing_screens_pass'] for x in top3['rack_reference_cases'])
assert [x['ideal_required_push_work_J'] for x in top3['spring_cases']]==[10.,20.]
# Check capacities directly in N-mm-MPa units, independent of the SI evaluation.
capacity=p['restraint_pin_count']*p['restraint_shear_planes_per_pin']*math.pi*p['restraint_pin_diameter_mm']**2/4*p['assumed_allowable_pin_shear_MPa']
for r in m['restraint']['provisional_load_cases']:
 assert math.isclose(capacity,r['pin_static_capacity_N_assumed'],rel_tol=1e-12)
 assert r['pin_capacity_to_load']>1 and r['lug_capacity_to_load']>1
for r in m['guide_and_clearance']['cases']:
 assert r['nominal_clearance_mm'] is not None and r['remaining_clearance_mm']>0 and r['screen_pass']
logic=json.loads((ROOT/'results/SEQUENCE_FAULT_CHECKS.json').read_text())
assert logic['all_assertions_pass'] and all(r['pass'] for r in logic['checks'])
assert len(logic['manifest_sequences'])==4
assert [r['size'] for r in logic['manifest_sequences']]==p['manifest']
assert all(r['single_release'] for r in logic['manifest_sequences'])
extended=json.loads((ROOT/'results/DRIVE_SCREENS_EXTENDED.json').read_text())
assert all(r['all_declared_sizing_screens_pass'] for r in extended)
logic12=json.loads((ROOT/'results/SEQUENCE_FAULT_CHECKS_12.json').read_text())
assert logic12['all_assertions_pass'] and len(logic12['manifest_sequences'])==12
assert logic12['final_campaign_state']['released_total']==12
assert logic12['isolated_cell_campaign_final_state']['released_total']==11
selected=json.loads((ROOT/'SELECTED_CATALOG_OPTIONS.json').read_text())
assert math.isclose(selected['receiver']['known_hardware_mass_option_kg'],1.409,abs_tol=1e-12)
assert selected['receiver']['brake']['static_torque_Nm']==p['receiver_brake_static_torque_Nm']
assert math.isclose(selected['four_primary_drive_subtotal_kg'],4.473,abs_tol=1e-12)
assert math.isclose(selected['twelve_primary_drive_subtotal_kg'],10.601,abs_tol=1e-12)
# A clean directory proves there are no hidden absolute workspace dependencies.
with tempfile.TemporaryDirectory(prefix='volley-fdr10-') as tmp:
 work=Path(tmp)
 for name in ['verify_feeder.py','PARAMETERS.json','catalog_reference.json']:shutil.copy2(ROOT/name,work/name)
 run=subprocess.run([sys.executable,str(work/'verify_feeder.py'),'--no-plots'],cwd=work,capture_output=True,text=True)
 assert run.returncode==0,run.stderr
 replayed=0
 for pth in sorted((ROOT/'results').iterdir()):
  if pth.name=='SELECTION_TABLE.csv':continue
  if pth.suffix in ('.json','.csv'):
   assert (work/'results'/pth.name).read_bytes()==pth.read_bytes(),f'Numerical replay differs: {pth.name}'
   replayed+=1
print(json.dumps({'capture_files_verified':len(manifest['files']),'replayed_numeric_files':replayed,'nominal_and_adverse_drive_cases':len(d)+len(extended),'logic_cases':logic['assertion_case_count'],'expanded_twelve_cell_logic_cases':logic12['assertion_case_count'],'result':'PASS','scope':'Selected academic analytical and logic capture; geometry signoff and hardware evidence are separate'},indent=2))
