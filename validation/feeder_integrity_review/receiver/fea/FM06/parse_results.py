"""Check force/moment balance and energy directly from native CalculiX output.

No acceptance against provider limits, material allowables or an assembled fit
is inferred from these prescribed clamped-bore component fixtures.
"""
from pathlib import Path
import math,json,hashlib,argparse
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--revision',default='FM-02');a=ap.parse_args();H=a.root
out=[]
for directory in sorted(H.glob('*_receiver_h*')):
 if not (directory/'MESH.json').exists():continue
 mesh=json.loads((directory/'MESH.json').read_text())
 for pattern in ['split','one_dog']:
  p=directory/(pattern+'.dat')
  if not p.exists():continue
  mode=None;U={};RF={};S=[]
  for line in p.read_text().splitlines():
   if 'displacements (' in line:mode='U';continue
   if 'forces (' in line:mode='RF';continue
   if 'stresses (' in line:mode='S';continue
   v=line.split()
   try:
    if mode in ['U','RF'] and len(v)==4:(U if mode=='U' else RF)[int(v[0])]=np.array(list(map(float,v[1:])))
    elif mode=='S' and len(v)==8:
     xx,yy,zz,xy,xz,yz=map(float,v[2:]);vm=math.sqrt(.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3*(xy**2+xz**2+yz**2));S.append((int(v[0]),int(v[1]),vm))
   except ValueError:pass
  if len(U)!=mesh['nodes'] or not S or not RF:raise ValueError(directory)
  coords={};forces={};mode=None
  for line in p.with_suffix('.inp').read_text().splitlines():
   if line.startswith('*'):mode=line.strip().upper();continue
   v=line.split(',')
   if mode=='*NODE':coords[int(v[0])]=np.array(list(map(float,v[1:4])))
   if mode=='*CLOAD':
    t,dof=int(v[0]),int(v[1])-1;forces.setdefault(t,np.zeros(3))[dof]+=float(v[2])
  applied=np.array(list(forces.values())).sum(axis=0);reaction=np.array(list(RF.values())).sum(axis=0)
  ma=np.array([np.cross(coords[n],f) for n,f in forces.items()]).sum(axis=0);mr=np.array([np.cross(coords[n],f) for n,f in RF.items()]).sum(axis=0)
  ferr=float(np.linalg.norm(applied+reaction)/np.linalg.norm(applied));merr=float(np.linalg.norm(ma+mr)/np.linalg.norm(ma))
  assert ferr<1e-5 and merr<1e-5,(directory,pattern,ferr,merr)
  energy_Nmm=.5*sum(float(np.dot(f,U[n])) for n,f in forces.items());assert energy_Nmm>0
  F=float(np.linalg.norm(applied))
  row={'case':directory.name+'/'+pattern,'mesh':mesh,'max_displacement_mm_at_1000N':max(float(np.linalg.norm(v)) for v in U.values()),'max_abs_Y_mm_at_1000N':max(abs(float(v[1])) for v in U.values()),'min_Y_displacement_mm':min(float(v[1]) for v in U.values()),'max_Y_displacement_mm':max(float(v[1]) for v in U.values()),'loaded_face_mean_displacement_mm':2*energy_Nmm/F,'loaded_face_max_abs_Y_mm':max(abs(float(U[n][1])) for n in forces),'elastic_strain_energy_J':energy_Nmm/1000,'max_vm_MPa_at_1000N':max(v[2] for v in S),'reaction_N':reaction.tolist(),'applied_force_N':applied.tolist(),'applied_moment_Nmm':ma.tolist(),'reaction_moment_Nmm':mr.tolist(),'force_balance_relative_error':ferr,'moment_balance_relative_error':merr,'file_hashes':{q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in [p,p.with_suffix('.inp'),p.with_suffix('.log'),p.with_suffix('.frd')]}}
  out.append(row)
# Mesh convergence uses actual element count, not an assumed mesh ratio.
conv=[]
for size in ['1U','3U']:
 for pattern in ['split','one_dog']:
  rr=sorted([r for r in out if r['case'].startswith(size+'_') and r['case'].endswith('/'+pattern)],key=lambda r:r['mesh']['C3D10_elements'])
  if len(rr)>=2:
   k='loaded_face_mean_displacement_mm';conv.append({'size':size,'pattern':pattern,'finest_case':rr[-1]['case'],'previous_case':rr[-2]['case'],'last_relative_compliance_change':abs(rr[-1][k]-rr[-2][k])/rr[-1][k],'last_relative_peak_stress_change':abs(rr[-1]['max_vm_MPa_at_1000N']-rr[-2]['max_vm_MPa_at_1000N'])/rr[-1]['max_vm_MPa_at_1000N']})
result={'revision':a.revision,'boundary':'Actual receiver solid; assumed homogeneous steel E200GPa,nu0.3 and fully clamped pin bores. No actual pin/hole contact, support flexibility, clearance take-up, impact, material allowable or assembly qualification. Negative-Y loads move the dogs away from the payload, increasing retention excursion; comparing displacement to0.5mm nominal gap is a scale comparison, not a proved penetration or an acceptance criterion.','native_cases':out,'convergence':conv}
(H/'CHECKED_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
for r in conv:print(a.revision,r)
print('Nativecases',len(out),'force/momentbalancechecked')
