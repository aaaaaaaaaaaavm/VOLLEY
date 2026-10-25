#!/usr/bin/env python3
"""Extract actual native mass-normalized modal output and compatible source static fields."""
from pathlib import Path
import argparse,hashlib,json,re,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-sd-mpl');os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-sd-cache')
import numpy as np
import matplotlib.tri as mtri
from scipy.sparse import coo_matrix
H=Path(__file__).resolve().parent;R=H.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,required=True);a=ap.parse_args()
S=a.raw/'verification/chassis_fea/d4b53d520c1bc0d3_h8';meta=json.loads((S/'MESH.json').read_text());config=json.loads((H/'MODAL_INPUT.json').read_text());log=(H/'runs/free_free/SOLVER_STDOUT.txt').read_text();assert 'Job finished'in log
nodes=config['patch_nodes'];lookup={n:i for i,n in enumerate(nodes)};phi=np.zeros((46,len(nodes),3));stress={};frequencies=[];mode=None;state=''
for line in(H/'runs/free_free/modal.dat').read_text().splitlines():
 if 'P A R T I C I P A T I O N'in line:state='';continue
 if 'MODE NO    EIGENVALUE'in line:state='F';continue
 m=re.search(r'E I G E N V A L U E\s+N U M B E R\s+(\d+)',line)
 if m:mode=int(m.group(1))-1;state='';continue
 if 'displacements ('in line:state='U';continue
 if 'stresses ('in line:state='S';continue
 fields=line.split()
 try:
  if state=='F'and len(fields)==5:frequencies.append([int(fields[0]),*map(float,fields[1:])])
  elif state=='U'and len(fields)==4:phi[mode,lookup[int(fields[0])]]=list(map(float,fields[1:]))
  elif state=='S'and len(fields)==8:
   key=(int(fields[0]),int(fields[1]));stress.setdefault(key,np.zeros((46,6)))[mode]=list(map(float,fields[2:]))
 except (ValueError,KeyError):pass
assert len(frequencies)==46 and len(stress)==4*len(config['stress_monitor_elements'])
freq=np.array(frequencies);assert np.max(np.abs(freq[:6,1]))<1e-3 and np.min(freq[6:,3])>100
coords={int(n):np.array(v)for n,v in meta['node_coordinates'].items()};xy=np.load(S/'PAIRED_PATCH_DISPLACEMENT.npz')['query_xy_mm'];static_closure=np.load(S/'PAIRED_PATCH_DISPLACEMENT.npz')['separation_reduction_mm']
def interpolation(tris):
 oriented=[]
 for q in tris:
  q=list(q);p=np.array([coords[n][:2]for n in q[:3]])
  if np.linalg.det(np.column_stack((p[1]-p[0],p[2]-p[0])))<0:q=[q[i]for i in [0,2,1,5,4,3]]
  oriented.append(q)
 tris=np.array(oriented);corners=sorted({n for q in tris for n in q[:3]});local={n:i for i,n in enumerate(corners)};pts=np.array([coords[n][:2]for n in corners]);mesh=mtri.Triangulation(pts[:,0],pts[:,1],np.array([[local[n]for n in q[:3]]for q in tris]));ix=mesh.get_trifinder()(xy[:,0],xy[:,1]);assert np.min(ix)>=0
 selected=tris[ix];p=np.array([[coords[n][:2]for n in q[:3]]for q in selected]);inverse=np.linalg.inv(np.stack((p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=2));rs=np.einsum('nij,nj->ni',inverse,xy-p[:,0]);l0=1-rs[:,0]-rs[:,1];l1=rs[:,0];l2=rs[:,1];N=np.column_stack((l0*(2*l0-1),l1*(2*l1-1),l2*(2*l2-1),4*l0*l1,4*l1*l2,4*l2*l0))
 return coo_matrix((N.ravel(),(np.repeat(np.arange(len(xy)),6),[lookup[int(n)]for n in selected.ravel()])),shape=(len(xy),len(nodes))).tocsr()
W=interpolation(meta['patch_triangles6']['lower'])-interpolation(meta['patch_triangles6']['upper'])
elastic=phi[6:];D=W@elastic[:,:,2].T;F0=meta['normal_force_each_array_N'];fz=np.array([meta['nodal_forces_N'].get(str(n),[0,0,0])[2]for n in nodes]);wz=fz/F0;wx=-np.sign(np.array([coords[n][2]for n in nodes]))*fz/(2*F0);assert abs(wx.sum()-1)<1e-10
Gz=elastic[:,:,2]@wz;Gx=elastic[:,:,0]@wx;omega=freq[6:,2];modal_static=D@(Gz*F0/omega**2)
# Native accepted static nodal displacements, for compatible C3D10 integration-point stress recovery.
u={};active=False
for line in(S/'chassis.dat').read_text().splitlines():
 if 'displacements ('in line:active=True;continue
 if 'forces ('in line:active=False
 fields=line.split()
 if active and len(fields)==4:
  try:u[int(fields[0])]=np.array(list(map(float,fields[1:])))
  except ValueError:pass
assert len(u)==meta['nodes']
monitored=set(config['stress_monitor_elements']);elems={};active=False
for line in(S/'chassis.inp').read_text().splitlines():
 if line.startswith('*ELEMENT'):active=True;continue
 if line.startswith('*'):active=False
 if active:
  v=[int(q)for q in line.split(',')if q.strip()]
  if v[0]in monitored:elems[v[0]]=v[1:]
def gradients(L):
 dl=np.array([[-1.,-1.,-1.],[1,0,0],[0,1,0],[0,0,1]])
 return np.vstack([(4*L[i]-1)*dl[i]for i in range(4)]+[4*(L[i]*dl[j]+L[j]*dl[i])for i,j in [(0,1),(1,2),(2,0),(0,3),(1,3),(2,3)]])
E=70000.;nu=.33;mu=E/(2*(1+nu));lam=E*nu/((1+nu)*(1-2*nu));static_stress=[];recovery_errors=[];keys=sorted(stress);stress_modes=np.array([stress[k][6:]for k in keys])
for element,ip in keys:
 q=elems[element];points=np.array([coords[n]for n in q]);displacements=np.array([u[n]for n in q]);L=np.full(4,(5-np.sqrt(5))/20);L[ip-1]=(5+3*np.sqrt(5))/20;g=gradients(L);dg=g@np.linalg.inv(points.T@g);grad=displacements.T@dg;eps=(grad+grad.T)/2;tensor=lam*np.trace(eps)*np.eye(3)+2*mu*eps;static_stress.append([tensor[0,0],tensor[1,1],tensor[2,2],tensor[0,1],tensor[0,2],tensor[1,2]])
 mode_u=elastic[:,[lookup[n]for n in q],:];mode_grad=np.einsum('mni,nj->mij',mode_u,dg);mode_eps=(mode_grad+np.swapaxes(mode_grad,1,2))/2;mode_tensor=lam*np.trace(mode_eps,axis1=1,axis2=2)[:,None,None]*np.eye(3)[None,:,:]+2*mu*mode_eps
 recovered=np.column_stack((mode_tensor[:,0,0],mode_tensor[:,1,1],mode_tensor[:,2,2],mode_tensor[:,0,1],mode_tensor[:,0,2],mode_tensor[:,1,2]));reference=stress[(element,ip)][6:];recovery_errors.append(float(np.max(np.abs(recovered-reference))/max(np.max(np.abs(reference)),1e-12)))

# Affine manufactured-displacement check against exact constant strain (postprocessing only).
L=np.full(4,.25);q=next(iter(elems.values()));points=np.array([coords[n]for n in q]);dg=gradients(L)@np.linalg.inv(points.T@gradients(L));affine=points@np.diag([.001,.002,.003]);assert np.max(np.abs(affine.T@dg-np.diag([.001,.002,.003])))<1e-10
# Actual accepted native nodal stress maximum, with extrapolation/singularity boundary retained.
vmmax=(-1.,None,None);active=False
for line in(S/'chassis.frd').read_text().splitlines():
 if line.startswith(' -4'):active='STRESS'in line;continue
 if active and line.startswith(' -1'):
  n=int(line[3:13]);s=np.array([float(line[13+i*12:25+i*12])for i in range(6)]);vm=np.sqrt(.5*((s[0]-s[1])**2+(s[1]-s[2])**2+(s[2]-s[0])**2)+3*np.dot(s[3:],s[3:]))
  if vm>vmmax[0]:vmmax=(float(vm),n,s.tolist())
convergence=[]
for count in [10,20,40]:
 pred=D[:,:count]@(Gz[:count]*F0/omega[:count]**2)
 convergence.append({'elastic_modes':count,'peak_paired_closure_mm':float(np.max(pred)),'max_spatial_error_against_accepted_static_mm':float(np.max(np.abs(pred-static_closure)))})
np.savez_compressed(H/'MODAL_BASIS.npz',node_ids=nodes,mode_numbers=freq[6:,0].astype(int),frequencies_Hz=freq[6:,3],omega_rad_s=omega,patch_phi=elastic,D_paired=D,G_normal_per_N=Gz,G_axial_per_N=Gx,query_xy_mm=xy,accepted_static_closure_mm=static_closure,modal_static_closure_mm=modal_static,stress_keys=keys,stress_modes=stress_modes,accepted_static_monitor_stress_MPa=static_stress)
record={'configuration_id':'VOLLEY-G5-ACR1','native_solver':'CalculiX2.23','native_job_finished':True,'rigid_modes':freq[:6].tolist(),'elastic_frequencies_Hz':freq[6:,3].tolist(),'modal_normalization':'Native mass normalized; N/mm/s/tonne consistent units; modal mass1','bare_chassis_mass_kg':meta['original_volume_mm3']*2700e-9,'static_compliance_convergence':convergence,'accepted_static_nodal_von_Mises_max_MPa':vmmax[0],'accepted_static_nodal_peak_node':vmmax[1],'accepted_static_nodal_peak_coordinates_mm':coords[vmmax[1]].tolist(),'accepted_static_nodal_peak_tensor_frd_order_MPa':vmmax[2],'stress_monitor_points':len(keys),'C3D10_stress_recovery_max_relative_component_error':max(recovery_errors),'stress_component_order':['xx','yy','zz','xy','xz','yz'],'source_identities':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [S/'chassis.dat',S/'chassis.frd',S/'MESH.json',S/'PAIRED_PATCH_DISPLACEMENT.npz',H/'runs/free_free/modal.inp',H/'runs/free_free/modal.dat',H/'runs/free_free/SOLVER_STDOUT.txt']},'mesh_boundary':'One accepted actual C3D10 mesh; mesh-converged modal/stress qualification is not asserted.','force_boundary':'3010.480631N permanent-magnet DC pinch is static preload, not a full-amplitude oscillatory rating. Current-induced normal ripple remains an explicit bracket.'}
(H/'MODAL_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k]for k in ['elastic_frequencies_Hz','bare_chassis_mass_kg','static_compliance_convergence','accepted_static_nodal_von_Mises_max_MPa']}))
