"""Independent closed-form checks of synchronized twin-screw lift sizing."""
from pathlib import Path
import json,math,hashlib,datetime
R=Path(__file__).resolve().parent.parent;D=R/'analysis/LIFT_SIZING.json';d=json.loads(D.read_text());a=d['assumptions']
travel=a['stroke_mm']/1000;T=a['time_s'];lead=a['screw_lead_mm']/1000;r=19.8
v=1.875*travel/T;acc=10*math.sqrt(3)/3*travel/T**2;root=a['root_diameter_study_mm']/1000;span=a['supported_span_mm']/1000
critical=math.pi**2*a['steel_E_Pa']*(math.pi*root**4/64)/span**2;checks=[]
for q in d['cases']:
 F=q['resistance_N']+q['moving_mass_study_kg']*(q['gravity_m_s2']+acc)
 tout=F*lead/(2*math.pi*a['screw_efficiency'])+a['common_output_drag_Nm']
 tq=tout/(r*a['gear_efficiency'])+a['rotor_and_gear_inertia_kg_m2']*(acc*2*math.pi*r/lead)
 rpm=v/lead*60*r;factor=critical/(F/2)
 checks.append({'mass_kg':q['moving_mass_study_kg'],'resistance_N':q['resistance_N'],'gravity_m_s2':q['gravity_m_s2'],'closed_form_force_N':F,'closed_form_motor_torque_Nm':tq,'closed_form_motor_rpm':rpm,'closed_form_equal_share_buckling_factor':factor,'arithmetic_match':abs(F-q['axial_force_total_peak_N'])<1e-7 and abs(tq-q['motor_torque_peak_Nm'])<1e-9 and abs(rpm-q['motor_rpm_peak'])<1e-9 and abs(factor-q['screw_euler_factor_equal_share'])<1e-7,'root_declared_pass':q['pass_declared_screens'],'holding_torque_frictionless_Nm':F*lead/(2*math.pi),'2Nm_static_holding_to_frictionless_ratio':2/(F*lead/(2*math.pi))})
report={'review':'Independent lift sizing arithmetic check','reviewed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_model_sha256':hashlib.sha256((R/'analysis/lift_sizing.py').read_bytes()).hexdigest(),'source_result_sha256':hashlib.sha256(D.read_bytes()).hexdigest(),'profile':{'stroke_mm':travel*1000,'duration_s':T,'peak_speed_mm_s':v*1000,'peak_acceleration_m_s2':acc,'motor_rpm_peak':v/lead*60*r},'per_screw_pinned_Euler_N':critical,'case_checks':checks,'all_arithmetic_match':all(q['arithmetic_match']for q in checks),'coast_declared_passing_cases':sum(q['root_declared_pass']for q in checks if q['gravity_m_s2']==0),'coast_cases':sum(q['gravity_m_s2']==0 for q in checks),'ground_declared_passing_cases':sum(q['root_declared_pass']for q in checks if q['gravity_m_s2']>0),'ground_cases':sum(q['gravity_m_s2']>0 for q in checks),'interpretation':['Onecommonmotor torquesharedbetweentwosame-leadscrews:totalforcebasedtorquecorrect;Eulerloadperscrewusesassumedequalhalfshare.','Groundgravityfailuresmustremainvisible,notpresentedascoastfailuresormodifythresholdstohidefailure.','Equalshare/synchronization,actualmovingmass,transmissionloss/holdinginterfaces,nutratedloadandpowerlossdynamicsarenotestablishedbythisarithmetic.','A2Nmstaticbrakescreenisnotdynamicarrestacceptance;screwfrictionisnotasafetylatch.']}
(R/'verification/LIFT_SIZING_CROSSCHECK.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['all_arithmetic_match']
print(json.dumps({k:report[k]for k in ['all_arithmetic_match','profile','coast_declared_passing_cases','coast_cases','ground_declared_passing_cases','ground_cases']},indent=2))
