"""Full actual chassis BREP elasticity with balanced normal attraction.

Run only after root identifies the stable corrected final chassis export.
"""
from pathlib import Path
import argparse,collections,hashlib,json,math,os,subprocess,sys,time
import numpy as np
sys.path.insert(0,'/workspace/volley-work/native-tools/python')
import gmsh

H=Path(__file__).resolve().parent;ROOT=H.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('brep',type=Path);ap.add_argument('--expected-sha',required=True);ap.add_argument('--h',type=float,default=8);a=ap.parse_args()
raw=a.brep.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha==a.expected_sha
O=H/(sha[:16]+'_h'+f'{a.h:g}');O.mkdir(parents=True,exist_ok=True);(O/'CHASSIS_INPUT.brep').write_bytes(raw)
F=json.loads((H.parent/'NORMAL_ATTRACTION.json').read_text())['nominal_reference_force_N'];start=time.perf_counter()
gmsh.initialize();gmsh.logger.start();gmsh.option.setNumber('General.NumThreads',2);gmsh.model.add('actual_chassis_free_body')
original=gmsh.model.occ.importShapes(str(O/'CHASSIS_INPUT.brep'),highestDimOnly=True);assert len(original)==1 and original[0][0]==3,original
initial_volume=sum(gmsh.model.occ.getMass(*q)for q in original)
tools=[(3,gmsh.model.occ.addBox(276,-45,14,336,90,16)),(3,gmsh.model.occ.addBox(276,-45,-30,336,90,16))]
fragments,mapping=gmsh.model.occ.fragment(original,tools,removeObject=True,removeTool=True)
kept={q for row in mapping[:len(original)]for q in row if q[0]==3};extra=[q for q in fragments if q[0]==3 and q not in kept]
if extra:gmsh.model.occ.remove(extra,recursive=True)
gmsh.model.occ.synchronize();final_volume=sum(gmsh.model.occ.getMass(*q)for q in gmsh.model.getEntities(3))
assert abs(final_volume-initial_volume)<=max(.001,1e-9*initial_volume),(initial_volume,final_volume)
patches={};patch_areas={}
for name,z in [('upper',14.),('lower',-14.)]:
    faces=[]
    for dim,tag in gmsh.model.getEntities(2):
        b=gmsh.model.getBoundingBox(dim,tag)
        if max(abs(b[2]-z),abs(b[5]-z))<1e-4 and b[0]>=276-1e-4 and b[3]<=612+1e-4 and b[1]>=-45-1e-4 and b[4]<=45+1e-4:faces.append(tag)
    patch_areas[name]=sum(gmsh.model.occ.getMass(2,t)for t in faces);assert abs(patch_areas[name]-336*90)<1e-5,(name,patch_areas[name],faces)
    patches[name]=faces
gmsh.model.addPhysicalGroup(3,[t for d,t in gmsh.model.getEntities(3)],name='SOLID')
gmsh.option.setNumber('Mesh.MeshSizeMin',min(1.5,a.h/4));gmsh.option.setNumber('Mesh.MeshSizeMax',a.h)
gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',12);gmsh.option.setNumber('Mesh.ElementOrder',2)
gmsh.model.mesh.generate(3);gmsh.model.mesh.setOrder(2)
gmsh.model.mesh.optimize('HighOrder')
gmsh.write(str(O/'mesh.msh'));gmsh.write(str(O/'mesh_export.inp'))
tags,coords,_=gmsh.model.mesh.getNodes();node={int(n):np.asarray(v)for n,v in zip(tags,np.asarray(coords).reshape(-1,3))}
forces=collections.defaultdict(lambda:np.zeros(3));patch_triangles={};areas={}
quadrature=[((1/3,1/3,1/3),.225)]
for pair,weight in [((.059715871789770,.470142064105115),.132394152788506),((.797426985353087,.101286507323456),.125939180544827)]:
    one,two=pair
    quadrature += [((one,two,two),weight),((two,one,two),weight),((two,two,one),weight)]
for name,faces in patches.items():
    triangles=[];area_sum=0.;sign=-1 if name=='upper'else 1
    for face in faces:
        types,_,connectivity=gmsh.model.mesh.getElements(2,face)
        for typ,conn in zip(types,connectivity):
            assert gmsh.model.mesh.getElementProperties(typ)[3]==6
            for tri in np.asarray(conn).reshape(-1,6):
                tri=list(map(int,tri));vertices=np.array([node[n]for n in tri]);triangles.append(tri)
                for(l0,l1,l2),weight in quadrature:
                    N=np.array([l0*(2*l0-1),l1*(2*l1-1),l2*(2*l2-1),4*l0*l1,4*l1*l2,4*l2*l0])
                    dr=np.array([1-4*l0,4*l1-1,0,4*(l0-l1),4*l2,-4*l2]);ds=np.array([1-4*l0,0,4*l2-1,-4*l1,4*l1,4*(l0-l2)])
                    jac=np.linalg.norm(np.cross(dr@vertices,ds@vertices));dA=.5*weight*jac;area_sum+=dA
                    for n,nvalue in zip(tri,N):forces[n][2]+=sign*F/(336*90)*nvalue*dA
    assert abs(area_sum-336*90)<1e-6,(name,area_sum)
    patch_triangles[name]=triangles;areas[name]=area_sum
applied=sum(forces.values(),start=np.zeros(3));moment=sum((np.cross(node[n],v)for n,v in forces.items()),start=np.zeros(3))
assert np.linalg.norm(applied)<1e-7 and np.linalg.norm(moment)<1e-4,(applied,moment)
text=(O/'mesh_export.inp').read_text();elements=[];mode=False
for line in text.splitlines():
    if line.upper().startswith('*ELEMENT'):mode='C3D10'in line.upper();continue
    if line.startswith('*'):mode=False
    if mode and line.strip():
        q=[int(v)for v in line.split(',')if v.strip()];assert len(q)==11;elements.append(q)
assert elements
qualities=gmsh.model.mesh.getElementQualities([r[0]for r in elements],'minSJ');assert min(qualities)>0,min(qualities)
parent={int(n):int(n)for n in tags}
def find(n):
    while parent[n]!=n:parent[n]=parent[parent[n]];n=parent[n]
    return n
for e in elements:
    head=find(e[1])
    for n in e[2:]:parent[find(n)]=head
assert len({find(n)for n in parent})==1
# Exactly six scalar conditions; no finite-area edge or face clamps.
targets=[np.array([200.,-100.,0.]),np.array([688.,-100.,0.]),np.array([200.,-80.,0.])]
anchors=[min(node,key=lambda n:np.linalg.norm(node[n]-target))for target in targets];assert len(set(anchors))==3
constraints=[(anchors[0],1),(anchors[0],2),(anchors[0],3),(anchors[1],2),(anchors[1],3),(anchors[2],3)]
rigid=[]
for n,axis in constraints:
    r=(node[n]-targets[0])/488;basis=np.column_stack((np.eye(3),np.array([[0,r[2],-r[1]],[-r[2],0,r[0]],[r[1],-r[0],0]])));rigid.append(basis[axis-1])
assert np.linalg.matrix_rank(np.array(rigid))==6
runtime=gmsh.option.getString('General.Version');(O/'gmsh.log').write_text('\n'.join(gmsh.logger.get())+'\n');gmsh.logger.stop();gmsh.finalize()
lines=['*HEADING','Actual ACR1 chassis; balanced normal attraction; N/mm/MPa','*NODE']
lines += [str(n)+','+','.join(f'{v:.14g}'for v in c)for n,c in node.items()]
lines += ['*ELEMENT,TYPE=C3D10,ELSET=SOLID']+[','.join(map(str,e))for e in elements]
for name,nodes in [('ALLNODES',sorted(node)),('ANCHORS',anchors)]:lines+=['*NSET,NSET='+name]+[','.join(map(str,nodes[i:i+16]))for i in range(0,len(nodes),16)]
lines+=['*MATERIAL,NAME=AL_ASSUMED','*ELASTIC','70000,0.33','*SOLID SECTION,ELSET=SOLID,MATERIAL=AL_ASSUMED','*BOUNDARY']
lines += [f'{n},{axis},{axis},0'for n,axis in constraints]
lines += ['*STEP','*STATIC','*CLOAD']+[f'{n},3,{v[2]:.14g}'for n,v in forces.items()if v[2]!=0]
lines += ['*NODE PRINT,NSET=ALLNODES','U','*NODE PRINT,NSET=ANCHORS','RF','*NODE FILE','U','*EL FILE','S','*END STEP'];(O/'chassis.inp').write_text('\n'.join(lines)+'\n')
metadata=dict(configuration_id='VOLLEY-G5-ACR1',input_BREP_sha256=sha,mesh_builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),h_max_mm=a.h,original_volume_mm3=initial_volume,fragmented_retained_volume_mm3=final_volume,discarded_tool_only_volumes=extra,gmsh_binding_version=gmsh.__version__,gmsh_runtime_version=runtime,nodes=len(node),C3D10_elements=len(elements),minimum_scaled_jacobian=float(min(qualities)),connected_mesh_components=1,normal_force_each_array_N=F,patch_areas_mm2=areas,applied_force_N=applied.tolist(),applied_moment_Nmm=moment.tolist(),constraints=[dict(node=n,axis=axis,coordinates_mm=node[n].tolist())for n,axis in constraints],rigid_constraint_rank=6,node_coordinates={str(n):v.tolist()for n,v in node.items()},nodal_forces_N={str(n):v.tolist()for n,v in forces.items()},patch_triangles6=patch_triangles,boundary='Actual single chassis solid with all exported holes/supports; no magnets, adhesive, rollers or assembled stator constraints.3-2-1 conditions remove rigid modes only; loads are self-equilibrated.',wall_s_before_solve=time.perf_counter()-start)
(O/'MESH.json').write_text(json.dumps(metadata,indent=2)+'\n')
assert raw==a.brep.read_bytes()
env=os.environ.copy();env['OMP_NUM_THREADS']='2';env['CCX_NPROC_STIFFNESS']='2';env['LD_LIBRARY_PATH']='/workspace/volley-work/native-tools/root/usr/lib/x86_64-linux-gnu:'+env.get('LD_LIBRARY_PATH','')
with(O/'ccx.log').open('w')as f:result=subprocess.run(['/workspace/volley-work/native-tools/root/usr/bin/ccx','-i','chassis'],cwd=O,env=env,stdout=f,stderr=subprocess.STDOUT)
assert result.returncode==0,(result.returncode,O/'ccx.log')
print(json.dumps(dict(run_directory=str(O),nodes=len(node),elements=len(elements),solver_exit=result.returncode,wall_s=time.perf_counter()-start)),flush=True)
