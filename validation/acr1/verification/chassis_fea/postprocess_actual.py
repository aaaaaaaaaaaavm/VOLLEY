"""Actual free-body chassis result extraction with paired-face closure.

The paired displacement difference is invariant to the chosen rigid-motion gauge.
"""
from pathlib import Path
import argparse,hashlib,json,re,os
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-mpl-config')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-xdg-cache')
import matplotlib.tri as mtri

ap=argparse.ArgumentParser();ap.add_argument('run_directory',type=Path);a=ap.parse_args();O=a.run_directory
m=json.loads((O/'MESH.json').read_text());coords={int(k):np.array(v)for k,v in m['node_coordinates'].items()};u={};reactions={};mode=''
for line in(O/'chassis.dat').read_text().splitlines():
    if 'displacements ('in line:mode='U';continue
    if 'forces ('in line:mode='RF';continue
    fields=line.split()
    if len(fields)!=4:continue
    try:n=int(fields[0]);v=np.array(list(map(float,fields[1:])))
    except ValueError:continue
    if mode=='U':u[n]=v
    elif mode=='RF':reactions[n]=v
assert len(u)==m['nodes'],(len(u),m['nodes'])
constrained={(r['node'],r['axis']-1)for r in m['constraints']}
max_patch_affinity_error=0.
for triangles in m['patch_triangles6'].values():
    for tri in triangles:
        for i,j,k in [(0,1,3),(1,2,4),(2,0,5)]:max_patch_affinity_error=max(max_patch_affinity_error,float(np.linalg.norm(coords[tri[k]]-(coords[tri[i]]+coords[tri[j]])/2)))
assert max_patch_affinity_error<1e-8,'Use isoparametric inverse mapping for curved optimized patch triangles'
rf={n:np.array([v[i]if(n,i)in constrained else 0. for i in range(3)])for n,v in reactions.items()}
loads={int(n):np.array(v)for n,v in m['nodal_forces_N'].items()};netforce=sum(loads.values(),start=np.zeros(3))+sum(rf.values(),start=np.zeros(3))
netmoment=sum((np.cross(coords[n],v)for n,v in loads.items()),start=np.zeros(3))+sum((np.cross(coords[n],v)for n,v in rf.items()),start=np.zeros(3))
def evaluator(triangles):
    oriented=[]
    for q in triangles:
        q=list(q);p=np.array([coords[n][:2]for n in q[:3]])
        if np.linalg.det(np.column_stack((p[1]-p[0],p[2]-p[0])))<0:q=[q[i]for i in [0,2,1,5,4,3]]
        oriented.append(q)
    triangles=np.asarray(oriented);corners=sorted(set(int(n)for q in triangles for n in q[:3]));lookup={n:i for i,n in enumerate(corners)}
    xy=np.array([coords[n][:2]for n in corners]);mesh=mtri.Triangulation(xy[:,0],xy[:,1],np.array([[lookup[int(n)]for n in q[:3]]for q in triangles]));finder=mesh.get_trifinder()
    def evaluate(points):
        indices=finder(points[:,0],points[:,1]);assert min(indices)>=0,'Query outside pressure patch'
        selected=triangles[indices];p=np.array([[coords[int(n)][:2]for n in q[:3]]for q in selected])
        inverse=np.linalg.inv(np.stack((p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=2));r=np.einsum('nij,nj->ni',inverse,points-p[:,0]);b0=1-r[:,0]-r[:,1];b1=r[:,0];b2=r[:,1]
        N=np.column_stack((b0*(2*b0-1),b1*(2*b1-1),b2*(2*b2-1),4*b0*b1,4*b1*b2,4*b2*b0));values=np.array([[u[int(n)][2]for n in q]for q in selected]);return np.sum(N*values,axis=1)
    return evaluate
grid=np.array(np.meshgrid(np.linspace(276,612,169),np.linspace(-45,45,46))).reshape(2,-1).T
nodes_xy=np.array([coords[n][:2]for triangles in m['patch_triangles6'].values()for tri in triangles for n in tri]);query=np.unique(np.vstack((grid,nodes_xy)),axis=0)
query[:,0]=np.clip(query[:,0],276+1e-7,612-1e-7);query[:,1]=np.clip(query[:,1],-45+1e-7,45-1e-7)
top=evaluator(m['patch_triangles6']['upper'])(query);bottom=evaluator(m['patch_triangles6']['lower'])(query);closure=bottom-top;peak=int(np.argmax(closure))
face_stats={}
for name,sign in [('upper',-1),('lower',1)]:
    nodes=sorted(set(n for tri in m['patch_triangles6'][name]for n in tri));n=max(nodes,key=lambda n:sign*u[n][2]);face_stats[name]=dict(max_inward_Uz_in_web_321_gauge_mm=float(sign*u[n][2]),node=n,coordinates_mm=coords[n].tolist(),nominal_1mm_minus_inward_Uz_in_same_gauge_mm=float(1-sign*u[n][2]))
log=(O/'ccx.log').read_text();version=re.search(r'CalculiX Version ([^\n]+)',log)
report=dict(configuration_id='VOLLEY-G5-ACR1',study='Full actual chassis single-solid BREP; balanced normal attraction;6scalar rigid-mode-removing constraints',
    final_CAD_identity_status='Candidate BREP hash pinned. Acceptance remains conditional until root confirms final source-generated chassis geometry/hash identity.',
    input_BREP_sha256=m['input_BREP_sha256'],h_max_mm=m['h_max_mm'],nodes=m['nodes'],C3D10_elements=m['C3D10_elements'],minimum_scaled_jacobian=m['minimum_scaled_jacobian'],connected_mesh_components=m['connected_mesh_components'],
    normal_force_each_array_N=m['normal_force_each_array_N'],pressure_patch_areas_mm2=m['patch_areas_mm2'],
    volume_before_fragment_mm3=m['original_volume_mm3'],volume_after_fragment_mm3=m['fragmented_retained_volume_mm3'],
    rigid_constraint_rank=m['rigid_constraint_rank'],constraints=m['constraints'],net_force_N=netforce.tolist(),net_moment_Nmm=netmoment.tolist(),
    force_balance_relative_to_total_absolute_load=float(np.linalg.norm(netforce)/(2*m['normal_force_each_array_N'])),
    moment_balance_relative_to_force_times488mm=float(np.linalg.norm(netmoment)/(2*m['normal_force_each_array_N']*488)),
    paired_face_closure=dict(max_face_separation_reduction_mm=float(closure[peak]),sample_xy_mm=query[peak].tolist(),sample_count=len(query),maximum_patch_midside_affinity_error_mm=max_patch_affinity_error,remaining_sum_of_two_nominal_1mm_gaps_mm=float(2-closure[peak]),method='Exact6-node quadratic surface displacement interpolation at commonXY after checking affine patch geometry: union of patch nodes and2mm grid; boundary queries inset1e-7mm for robust triangulation. Rigid translation and infinitesimal rigid rotation cancel in lowerUz−upperUz.'),
    per_face_web_gauge=face_stats,
    declared_load_sensitivity_1p3=dict(method='Linear elasticity scaling of the same native solution; no additional solve and no magnetic-field uncertainty probability implied.',normal_force_each_array_N=1.3*m['normal_force_each_array_N'],max_paired_face_separation_reduction_mm=float(1.3*closure[peak]),remaining_sum_of_two_nominal_1mm_gaps_mm=float(2-1.3*closure[peak]),max_inward_Uz_web_gauge_mm={k:1.3*v['max_inward_Uz_in_web_321_gauge_mm']for k,v in face_stats.items()}),
    solver_version=None if version is None else version.group(1),job_finished='Job finished'in log,
    sources_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [O/'CHASSIS_INPUT.brep',O/'MESH.json',O/'mesh.msh',O/'chassis.inp',O/'chassis.dat',O/'ccx.log',Path(__file__)]},
    limits=['Actual exported chassis holes and integral supports are included; separate magnets, bonds, joints, rollers, stator and complete assembly constraints are excluded.','Material E70GPa and nu0.33 assumed; load is the3010.48N array total redistributed uniformly over each336x90mm patch.','Absolute face displacements depend on the declared rigid-motion gauge; paired face separation is gauge invariant. Positive summed gap does not prove both individual assembled gaps.','One native mesh is a bounded geometry-delta check. A second mesh is added only if controlling loaded-clearance uncertainty requires it.','No whole-product or hardware qualification conclusion.'])
assert report['job_finished'];assert report['force_balance_relative_to_total_absolute_load']<1e-5;assert report['moment_balance_relative_to_force_times488mm']<1e-5
identity=O/'FINAL_CAD_IDENTITY.json'
if identity.exists():
    evidence=json.loads(identity.read_text());assert evidence['byte_identical']and evidence['final_source_BREP_sha256']==m['input_BREP_sha256']
    report['final_CAD_identity_status']='Final source-generated chassis BREP byte-identical to analyzed candidate; seeFINAL_CAD_IDENTITY.json. Overall assembly scope remains excluded.'
    report['final_CAD_identity_sha256']=hashlib.sha256(identity.read_bytes()).hexdigest()
(O/'CHASSIS_FEA_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');np.savez_compressed(O/'PAIRED_PATCH_DISPLACEMENT.npz',query_xy_mm=query,upper_Uz_mm=top,lower_Uz_mm=bottom,separation_reduction_mm=closure)
print(json.dumps({k:v for k,v in report.items()if k not in ['sources_sha256','constraints','limits']},indent=2),flush=True)
