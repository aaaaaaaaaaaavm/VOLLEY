"""Independent closed-form checks of the ACR1 sizing capture; no CAD edits."""
from pathlib import Path
import json,math,hashlib,datetime
R=Path(__file__).resolve().parent.parent;P=R/'cad/PARAMETERS.json';raw=P.read_bytes();p=json.loads(raw);d=json.loads((R/'analysis/FEEDER_SIZING.json').read_text());s=p['storage']
h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
travel=s['feed_stroke']/1000;T=s['nominal_feed_time_s'];lead=s['local_screw_lead']/1000
v=1.875*travel/T;a=10*math.sqrt(3)/3*travel/T**2;ratio=9.;eta_s=.42;eta_g=.5;mass=7.5
rpm=v/lead*60*ratio;cases=[]
for rec in d['feed_cases']:
 F=rec['resistance_N']+mass*a;Tout=F*lead/(2*math.pi*eta_s);Mt=Tout/(ratio*eta_g)
 J=3e-6+4.34e-7;inert=J*ratio*2*math.pi*a/lead;with_allowance=(Tout+.015)/(ratio*eta_g)+inert
 cases.append({'resistance_N':rec['resistance_N'],'closed_form_peak_axial_N':F,'closed_form_peak_motor_torque_Nm':Mt,'captured_motor_torque_Nm':rec['motor_torque_peak_Nm'],'absolute_torque_difference_Nm':abs(Mt-rec['motor_torque_peak_Nm']),'closed_form_peak_motor_rpm':rpm,'captured_peak_motor_rpm':rec['motor_rpm_peak'],'arithmetic_match':abs(Mt-rec['motor_torque_peak_Nm'])<1e-9 and abs(rpm-rec['motor_rpm_peak'])<1e-9,'additional_declared_0p015Nm_bearing_drag_plus_input_inertia_motor_torque_Nm':with_allowance,'with_allowance_current_A':.089+with_allowance/.0414,'with_allowance_below_0p0418Nm_continuous_catalog':with_allowance<=.0418})
span=s['local_guide_span']/1000;E=200e9;stack=.30+(p['manifest']['payload_mm'][0]/2)*math.tan(math.radians(.1))+200*40*12e-6;guides=[]
for diameter in [8.,10.,float(s['local_guide_diameter'])]:
 I=math.pi*(diameter/1000)**4/64
 for total in [10.,25.,50.,100.]:
  delta=(total/2)*span**3/(48*E*I)*1000;remaining=s['channel_side_clearance']-stack-delta
  guides.append({'diameter_mm':diameter,'total_transverse_study_N':total,'deflection_mm':delta,'nondeflection_stack_mm':stack,'remaining_side_clearance_mm':remaining,'positive':remaining>0,'is_current_parameter_diameter':diameter==float(s['local_guide_diameter'])})
report={'review':'Independent closed-form feeder-sizing arithmetic/guide screen','reviewed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cad_parameter_sha256':hashlib.sha256(raw).hexdigest(),'sizing_model_sha256':h(R/'analysis/feeder_sizing.py'),'sizing_results_sha256':h(R/'analysis/FEEDER_SIZING.json'),'sizing_capture_matches_current_full_parameter_hash':d['cad_parameter_sha256']==hashlib.sha256(raw).hexdigest(),'profile':{'stroke_mm':travel*1000,'duration_s':T,'quintic_peak_velocity_mm_s':v*1000,'quintic_peak_acceleration_m_s2':a,'motor_rpm_peak':rpm},'feed_case_checks':cases,'all_motor_profile_arithmetic_match':all(q['arithmetic_match']for q in cases),'guide_checks':guides,'notes':['Rootmodelusesassumed0.42screwefficiency/0.50gearefficiency. Separatebearingdragandreflectedrotor/gearinputinertiaarenotcurrentlyincluded;thecomparisonshowstheirdeclaredallowancewouldnotflipcatalogtorquepass. Clarifyboundarytoavoiddoublecountingfriction.','CurrentCAD sourcecheckedusesactual10mmguidecylinders and10.2mmbush/supportbores;8mmhistorical100Ncasefails,10mmproposed/currentcasepassesdeclaredstack. Nominal boreclearance is not precision or reliability validation.','Parent sizing capture must be regenerated after CADparameters settle if its full-file hash differs. This review does not silently rewrite its earlier result.','Actual pusher/lift moving mass, support stiffness, current-limit calibration and sourceenvironmentremain same-revision dependencies; no supplier approvalorhardware performance inferred.']}
(R/'verification/FEEDER_SIZING_CROSSCHECK.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['all_motor_profile_arithmetic_match']
print(json.dumps({'arithmetic_match':report['all_motor_profile_arithmetic_match'],'capture_current_hash':report['sizing_capture_matches_current_full_parameter_hash'],'current_guide_diameter_mm':s['local_guide_diameter'],'100N_10mm_remaining_mm':next(q['remaining_side_clearance_mm']for q in guides if q['diameter_mm']==10 and q['total_transverse_study_N']==100)},indent=2))
