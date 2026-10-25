"""Parse actual CCX displacement/reaction outputs for isolated C-frame study."""
from pathlib import Path
import json,re,hashlib,numpy as np,datetime
H=Path(__file__).resolve().parent;records=[]
for name in ['h12','h8']:
 O=H/name;m=json.loads((O/'MESH.json').read_text());coords={int(n):np.array(c)for n,c in m['node_coordinates'].items()};u={};rf={};mode='';setname=''
 for line in(O/'cframe.dat').read_text().splitlines():
  if 'displacements (' in line:mode='U';continue
  if 'forces (' in line:mode='RF';setname=re.search(r'for set (\S+)',line).group(1);continue
  a=line.split()
  if len(a)!=4:continue
  try:n=int(a[0]);v=np.array(list(map(float,a[1:])))
  except ValueError:continue
  if mode=='U':u[n]=v
  elif mode=='RF':
   if n not in rf:rf[n]=np.zeros(3)
   component={'SYMX':0,'SYMZ':2,'PINY':1}[setname];rf[n][component]=v[component]
 loads={};inload=False
 for line in(O/'cframe.inp').read_text().splitlines():
  if line.startswith('*'):inload=line.startswith('*CLOAD');continue
  if inload:
   n,axis,val=line.split(',');loads[int(n)]=np.array([0.,0.,float(val)])
 applied=sum(loads.values(),start=np.zeros(3));reaction=sum(rf.values(),start=np.zeros(3));net=applied+reaction
 moment=sum((np.cross(coords[n],v)for n,v in loads.items()),start=np.zeros(3))+sum((np.cross(coords[n],v)for n,v in rf.items()),start=np.zeros(3))
 patch=[n for n,c in coords.items()if abs(c[2]-14)<1e-6 and c[0]<=168.000001 and -45.000001<=c[1]<=45.000001]
 target=min(patch,key=lambda n:u[n][2]);maximum=-u[target][2]
 mean=sum(v[2]*u[n][2]for n,v in loads.items())/applied[2]
 log=(O/'ccx.log').read_text();version=re.search(r'CalculiX Version ([^\n]+)',log)
 records.append({'mesh':name,'h_max_mm':m['h_max_mm'],'nodes':m['nodes'],'C3D10_elements':m['C3D10_elements'],'minimum_scaled_jacobian':m['minimum_scaled_jacobian'],'connected_components':m['connected_mesh_components'],'pressure_patch_area_quarter_mm2':m['pressure_patch_area_quarter_mm2'],'normal_full_array_force_N':m['normal_force_full_array_N'],'applied_force_N':applied.tolist(),'summed_support_reaction_N':reaction.tolist(),'net_force_N':net.tolist(),'force_balance_relative_error':float(np.linalg.norm(net)/np.linalg.norm(applied)),'net_moment_Nmm':moment.tolist(),'max_loaded_face_inward_displacement_mm':maximum,'max_loaded_face_node_xyz_mm':coords[target].tolist(),'force_weighted_mean_loaded_face_displacement_mm':-mean,'global_max_inward_displacement_mm':max(-v[2]for v in u.values()),'nominal_remaining_1mm_face_envelope_gap_mm':1-maximum,'solver_version_from_log':None if version is None else version.group(1),'job_finished':'Job finished' in log,'source_hashes':{f:hashlib.sha256((O/f).read_bytes()).hexdigest()for f in ['MESH.json','mesh.msh','cframe.inp','ccx.log','cframe.dat']}})
fine=records[-1];relative=abs(records[-1]['max_loaded_face_inward_displacement_mm']-records[0]['max_loaded_face_inward_displacement_mm'])/records[-1]['max_loaded_face_inward_displacement_mm']
field=json.loads((H.parent/'NORMAL_ATTRACTION.json').read_text());C=fine['max_loaded_face_inward_displacement_mm']/fine['normal_full_array_force_N'];sweep=sorted([q for q in field['records']if q['grid_step_mm']==2. and q['domain_X_mm']==600],key=lambda q:q['closure_each_face_mm']);x=np.array([q['closure_each_face_mm']for q in sweep]);f=np.array([q['force_one_array_N']for q in sweep]);delta=fine['max_loaded_face_inward_displacement_mm']
iterations=[]
for k in range(30):
 force=float(np.interp(delta,x,f));nxt=C*force;iterations.append({'iteration':k,'closure_each_face_mm':delta,'force_N':force,'next_closure_mm':nxt})
 if abs(nxt-delta)<1e-9:delta=nxt;break
 delta=nxt
result={'study':'ACR1 isolated open C-frame quarter-symmetry3D elasticity comparison','generated_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'h12_to_h8_max_loaded_face_relative_change':relative,'fine_max_loaded_face_closure_mm':fine['max_loaded_face_inward_displacement_mm'],'fine_nominal_remaining_face_gap_mm':1-fine['max_loaded_face_inward_displacement_mm'],'field_feedback_sensitivity':{'component_FEA_linear_compliance_mm_per_N':C,'interpolated_equilibrium_closure_mm':delta,'remaining_face_gap_mm':1-delta,'iterations':iterations,'meaning':'Field/compliancefixedpointusescoarseinterpolatednormalforcecurvesandlinearcomponentcompliance;notanassemblednonlinearmagnetomechanicalsolution.'},'limits':['Onlyuniform488mmCsection,16mmplates/20mmweb;noattachedmagnets/bond,backstop,rollers,manufacturingjoints/cradle/flexiblesupports.','QuarterX/ZsymmetryandoneUyconstraintremoveidealrigidmotion;actualasymmetricattachmentsnotincluded.','Actualcuboidforce3010.48Nredistributeduniformlyover336x90mm;notlocalphysicalMaxwelltractiononmagnet/bond.','Two mesh sizes give a refinement comparison, not a certified error bound or continuum extrapolation.','LinearE70000MPa,nu0.33assumed;noalloystrength,plasticity,fatigue,bucklingcontactorflightqualification.','A positive isolated component residual does not establish assembled operating gap or an achieved release speed.']}
(H/'CFRAME_FEA_REVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cases':[{k:r[k]for k in ['mesh','nodes','C3D10_elements','max_loaded_face_inward_displacement_mm','force_balance_relative_error','job_finished']}for r in records],'relative_change':relative,'feedback_closure_mm':delta,'feedback_remaining_gap_mm':1-delta},indent=2))
