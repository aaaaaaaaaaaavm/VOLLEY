from pathlib import Path
import json,math,itertools
H=Path(__file__).resolve().parent
r=sorted([json.loads(p.read_text()) for p in H.glob('h*/RESULT.json')],key=lambda r:-r['h_mm'])
assert len(r)==4
E=69000;nu=.33;L=109.;w=12.;d=8.5;I=w*d**3/12;A=w*d;G=E/(2*(1+nu))
eb=L**3/(3*E*I);ts=eb+L/((5/6)*G*A)
for i,row in enumerate(r):
 row['relative_compliance_change']=None if i==0 else abs(row['loaded_mean_Z_mm_per_N']/r[i-1]['loaded_mean_Z_mm_per_N']-1)
row=r[-1];cases=[]
for mass,g,sharing in itertools.product([1.33,2.,4.,6.],[0,1,5,10,25],[.5,1.]):
 F=mass*g*9.80665*sharing;u=F*row['max_abs_Z_mm_per_N'];cases.append({'payload_kg':mass,'acceleration_g':g,'fraction_on_one_tine':sharing,'load_N':F,'max_Z_linear_fixture_mm':u,'nominal_0_6mm_slot_gap_minus_linear_deflection_mm':.6-u,'nominal_vm_scaled_MPa':F*row['max_vm_MPa_per_N'],'small_deflection_warning_gt_1pct_length':u>.01*L})
(H/'SUMMARY.json').write_text(json.dumps({'revision':'FLR02','native_cases':r,'Euler_Bernoulli_compliance_mm_per_N':eb,'Timoshenko_compliance_mm_per_N':ts,'finest_mean_to_EB_ratio':row['loaded_mean_Z_mm_per_N']/eb,'finest_mean_to_Timoshenko_ratio':row['loaded_mean_Z_mm_per_N']/ts,'linear_scaled_sensitivity_cases':cases,'boundary':'Unit traction solve on actual isolated tine STEP; ideal clamped root, assumed E69GPa/nu0.33 aluminium. No selected alloy allowable, root/fork flexibility, gravity self-load, actual rail pressure/contact, manufacturing tolerance or qualification. Both equal and one-tine load partitions are sensitivities. The0.6mm gap comparison omits other deflections and tolerances; positive residual alone does not approve a loaded assembly. Large-deflection/stress cases invalidate a small-elastic strength interpretation. Launch restraints must bypass this operating transfer fixture.'},indent=2)+'\n')
print('4 native meshes;',len(cases),'sensitivity cases; final compliance change',r[-1]['relative_compliance_change'])
print('EB',eb,'Timoshenko',ts,'native',row['loaded_mean_Z_mm_per_N'])
