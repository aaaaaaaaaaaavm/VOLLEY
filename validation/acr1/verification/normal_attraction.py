#!/usr/bin/env python3
"""Actual ACR1 cuboid-field Maxwell plane integral and bounded frame feedback.
Shares make_field law with finite_motor.py; not an independent FEM calculation.
"""
from pathlib import Path
import json,math,hashlib,datetime,importlib.util,inspect,time,copy
import numpy as np
import magpylib
R=Path(__file__).resolve().parent;BASE=R.parent;P=BASE/'cad/PARAMETERS.json';source=BASE/'analysis/finite_motor.py'
raw=P.read_bytes();p=json.loads(raw);spec=importlib.util.spec_from_file_location('acr1_actual_field',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
field_source=inspect.getsource(mod.make_field);(R/'FIELD_FUNCTION_CAPTURE.txt').write_text(field_source)
MU0=4*math.pi*1e-7;started=time.perf_counter();records=[];cache={}
def integral(closure_mm=0.,length_mm=600.,depth_mm=220.,step_mm=1.):
 key=(closure_mm,length_mm,depth_mm,step_mm)
 if key in cache:return cache[key]
 pp=copy.deepcopy(p);pp['magnetic']['array_inner_z']=p['magnetic']['array_inner_z']-closure_mm
 field=mod.make_field(pp);x=np.linspace(-length_mm/2000,length_mm/2000,int(round(length_mm/step_mm))+1);z=np.linspace(-depth_mm/2000,depth_mm/2000,int(round(depth_mm/step_mm))+1)
 xx,zz=np.meshgrid(x,z,indexing='ij');flat=np.column_stack([xx.ravel(),np.zeros(xx.size),zz.ravel()]);B=np.empty_like(flat)
 tick=time.perf_counter()
 for i in range(0,len(flat),4096):B[i:i+4096]=field.getB(flat[i:i+4096])
 stress=(B[:,1]**2-B[:,0]**2-B[:,2]**2)/(2*MU0);stress=stress.reshape(xx.shape)
 force=float(np.trapezoid(np.trapezoid(stress,z,axis=1),x,axis=0))
 row={'closure_each_face_mm':closure_mm,'array_inner_abs_gap_axis_mm':pp['magnetic']['array_inner_z'],'domain_X_mm':length_mm,'domain_depth_mm':depth_mm,'grid_step_mm':step_mm,'shape':[len(x),len(z)],'points':len(flat),'force_one_array_N':force,'max_midplane_B_T':float(np.linalg.norm(B,axis=1).max()),'max_midplane_stress_Pa':float(stress.max()),'wall_s':time.perf_counter()-tick}
 records.append(row);cache[key]=row
 print(json.dumps(row),flush=True)
 (R/'NORMAL_ATTRACTION_PARTIAL.json').write_text(json.dumps(records,indent=2)+'\n')
 if closure_mm==0. and length_mm==600 and step_mm==1.:
  np.savez_compressed(R/'NORMAL_MIDPLANE.npz',x_m=x,depth_m=z,B_T=B.reshape(len(x),len(z),3),stress_Pa=stress)
 return row
# Nominal domain and mesh refinement: actual84cuboids, not old28x12mm blocks.
coarse=integral(step_mm=2.);nominal=integral(step_mm=1.);fine=integral(step_mm=.5)
wide=integral(length_mm=800.,depth_mm=300.,step_mm=1.)
# Scalar compliance of the declared single-web C-frame, E70GPa.
l=p['launch'];m=p['magnetic'];width=m['blocks_per_array']*m['block_pitch'];t=l['carrier_top_plate_z'][1]-l['carrier_top_plate_z'][0];wy=l['carrier_negative_web_y'];tw=max(wy)-min(wy);root=max(wy);inner=l['carrier_top_plate_z'][0]
a=-m['block_depth_y']/2-root;end=m['block_depth_y']/2-root;wc=root-tw/2;H=2*inner+t;E=70000.;G=E/(2*1.33)
I=width*t**3/12;Iw=width*tw**3/12
c_bend=(end*(end**3-a**3)-(end**4-a**4)/4)/(m['block_depth_y']*6*E*I)
c_rot=(-wc)*H/(2*E*Iw)*(m['block_depth_y']/2-wc)
c_ax=H/(2*E*width*tw);c_shear=((a+end)/2)/((5/6)*G*width*t)
C=c_bend+c_rot+c_ax+c_shear
sweep=[integral(closure_mm=q,step_mm=2.) for q in [.2,.5,.8]]
xs=np.array([0.]+[q['closure_each_face_mm']for q in sweep]);fs=np.array([coarse['force_one_array_N']]+[q['force_one_array_N']for q in sweep])
solutions=[]
for width_fraction in [1.,.75,.5]:
 cc=C/width_fraction;delta=cc*nominal['force_one_array_N'];iterations=[]
 for k in range(30):
  force=float(np.interp(delta,xs,fs));new=cc*force;iterations.append({'iteration':k,'closure_each_face_mm':delta,'force_N':force,'next_closure_mm':new})
  if abs(new-delta)<1e-9:delta=new;break
  delta=new
 solutions.append({'effective_axial_width_fraction':width_fraction,'linear_compliance_mm_per_N':cc,'interpolated_fixed_point_closure_mm':delta,'remaining_1mm_face_envelope_gap_mm':1-delta,'iterations':iterations,'inside_sampled_closure_interval':0<=delta<=.8})
# Directfieldcheckofnominal-widthfixedpoint, then one corrected compliance step.
qstar=solutions[0]['interpolated_fixed_point_closure_mm'];direct=integral(closure_mm=qstar,step_mm=1.)
solutions[0]['direct_field_force_N']=direct['force_one_array_N'];solutions[0]['direct_field_closure_mm']=C*direct['force_one_array_N'];solutions[0]['direct_residual_mm']=abs(qstar-C*direct['force_one_array_N'])
result={'analysis':'ACR1 actual cuboid normal-attraction Maxwell plane integral','generated_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cad_parameter_sha256':hashlib.sha256(raw).hexdigest(),'field_module_sha256_at_import':hashlib.sha256(source.read_bytes()).hexdigest(),'make_field_source_sha256':hashlib.sha256(field_source.encode()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'software':{'numpy':np.__version__,'magpylib':magpylib.__version__},
 'geometry':{'arrays':2,'blocks_per_array':m['blocks_per_array'],'pitch_mm':m['block_pitch'],'block_dimensions_field_X_Y_Z_mm':[m['block_pitch'],m['block_thickness_z'],m['block_depth_y']],'polarization_T':1.32,'top_angle_deg':'90-60*i','bottom_angle_deg':'90+60*i','field_axes':'Xtravel,Ygap,Zdepth;CADXtravel,Zgap,Ydepth','nominal_array_inner_abs_gap_mm':m['array_inner_z']},
 'method':'F=integral(By^2-Bx^2-Bz^2)/(2mu0)dX dZ overY0separatingplane;compositetrapezoidalquadrature,wide-domainandgridrefinement. Forceononearray;opposedarrayfeelsequalopposite. SIunitsT,m,mu0=4pi1e-7.',
 'records':records,'nominal_reference_force_N':fine['force_one_array_N'],'grid_2to1_relative_change':abs(nominal['force_one_array_N']-coarse['force_one_array_N'])/nominal['force_one_array_N'],'grid_1to0p5_relative_change':abs(fine['force_one_array_N']-nominal['force_one_array_N'])/fine['force_one_array_N'],'domain_600x220to800x300_relative_change_at1mm':abs(wide['force_one_array_N']-nominal['force_one_array_N'])/wide['force_one_array_N'],
 'frame_feedback':{'model':'Approximate linear single-webplate-strip+Cframecompliance,notassembledFEA. Uniformforcepatch336x90redistributionassumed;magneticforcevarieswithgap. Fixedpointsinterpolatedfromexplicitfieldgapcasesanddirectcheckedatnominalwidth.', 'plate_mm':t,'web_mm':tw,'web_y_mm':wy,'E_MPa':E,'compliance_mm_per_N':C,'solutions':solutions},
 'limits':['Sharedanalyticcuboidfieldlawwithrootfinite_motor.py;notindependentFEMorfieldmeasurement.','Linearuniformmagnetization,relativepermeabilityassumptionsandnoironsupportorcurrentreactionfieldperturbation.','Maxwellplanefringestressisaforceintegral,notlocalbond/contacttractionorrealplate-loadmap.','Fixedpointcomplianceisaprovisionalstructuralsensitivity;actualassembledsupports,joints,bonds,temperatureandtransient loadsremainoutsideit.','Positivecomputedremaininggapdoesnotestablishhardwareflightqualificationorapositioningaccuracyrating.'],
 'wall_s':time.perf_counter()-started}
(R/'NORMAL_ATTRACTION.json').write_text(json.dumps(result,indent=2)+'\n')
print('COMPLETE',result['nominal_reference_force_N'],result['grid_1to0p5_relative_change'],result['domain_600x220to800x300_relative_change_at1mm'],solutions[0]['direct_field_closure_mm'],flush=True)
