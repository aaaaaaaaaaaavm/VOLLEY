"""Mesh actual FM-02 receiver solid; prescribed clamped-bore structural fixture.

N, mm, MPa. Imported manufacturer-like boundaries are not implied. All imposed
supports, forces and material constants remain explicitly assumed.
"""
from pathlib import Path
import sys,json,math,hashlib,subprocess,os,argparse
import gmsh
import numpy as np
H=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--size',default='3U');ap.add_argument('--h',type=float,default=4);a=ap.parse_args()
name=f'{a.size}_receiver_h{a.h:g}';O=H/name;O.mkdir(exist_ok=True)
gmsh.initialize();gmsh.logger.start();gmsh.option.setNumber('General.NumThreads',2)
gmsh.model.add(name);gmsh.model.occ.importShapes(str(H/f'{a.size}_sled_entry_bar.step'));gmsh.model.occ.synchronize()
vols=gmsh.model.getEntities(3);assert len(vols)==1
surfs=gmsh.model.getEntities(2);fixed=[];loaded=[]
for dim,tag in surfs:
 typ=gmsh.model.getType(dim,tag);com=gmsh.model.occ.getCenterOfMass(dim,tag)
 if typ=='Cylinder' and abs(com[2]+10)<1e-5:fixed.append(tag)
 if typ=='Plane' and abs(com[1]+0.5)<1e-6:loaded.append(tag)
assert len(fixed)==2 and len(loaded)==2,(fixed,loaded)
gmsh.model.addPhysicalGroup(3,[t for d,t in vols],name='SOLID')
gmsh.option.setNumber('Mesh.MeshSizeMin',a.h/6);gmsh.option.setNumber('Mesh.MeshSizeMax',a.h)
gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',16)
gmsh.option.setNumber('Mesh.ElementOrder',2);gmsh.option.setNumber('Mesh.HighOrderOptimize',1)
gmsh.model.mesh.generate(3);gmsh.model.mesh.setOrder(2)
gmsh.write(str(O/'mesh.msh'));gmsh.write(str(O/'mesh.inp'))
tags,xyz,_=gmsh.model.mesh.getNodes();xyz=np.asarray(xyz).reshape(-1,3);coords={int(t):x for t,x in zip(tags,xyz)}
fixnodes=sorted({int(t) for f in fixed for t in gmsh.model.mesh.getNodes(2,f,includeBoundary=True)[0]})
force_maps=[]
for face in loaded:
 weights={};area_total=0.
 types,elem_tags,conn=gmsh.model.mesh.getElements(2,face)
 for typ,connect in zip(types,conn):
  props=gmsh.model.mesh.getElementProperties(typ);nn=props[3];assert nn==6,props[:4]
  for tri in np.asarray(connect).reshape(-1,nn):
   p=[coords[int(t)] for t in tri[:3]];area=np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))/2;area_total+=area
   # Exact integral for planar six-node triangle with straight edges:
   # corner shape functions integrate to zero; mid-edge functions to area/3.
   for t in tri[3:]:weights[int(t)]=weights.get(int(t),0.)+area/3
 assert abs(area_total-64)<1e-5,area_total
 force_maps.append({t:v/area_total for t,v in weights.items()})
# Use Gmsh's Abaqus exporter to map quadratic tetrahedron node order.
element_text=(O/'mesh.inp').read_text();elements=[];mode=False
for line in element_text.splitlines():
 if line.upper().startswith('*ELEMENT'):
  mode='C3D10' in line.upper();continue
 if line.startswith('*'):mode=False
 if mode and line.strip():
  row=[int(x) for x in line.split(',') if x.strip()];assert len(row)==11,row
  elements.append(row)
assert elements
q=gmsh.model.mesh.getElementQualities([e[0] for e in elements],'minSJ');assert min(q)>0
meshrecord={'part':f'{a.size}_sled_entry_bar','source_step_sha256':hashlib.sha256((H/f'{a.size}_sled_entry_bar.step').read_bytes()).hexdigest(),'gmsh':gmsh.__version__,'h_max_mm':a.h,'nodes':len(tags),'C3D10_elements':len(elements),'min_scaled_Jacobian':float(min(q)),'fixed_bore_surfaces':fixed,'load_surfaces':loaded,'fixed_nodes':len(fixnodes),'units':'N,mm,MPa','support':'Both inserted-pin bore surfaces fully clamped. Idealized fixture; assembled stiffness is not established. Actual pin/hole contact, guide-wall bearing and support flexibility are absent.','material':'Assumed homogeneous steel E200000MPa,nu0.3; no alloy/allowable or plasticity','loads':'1000N towards negative Y, split evenly or applied entirely to one dog; no pretended provider load requirement'}
(O/'MESH.json').write_text(json.dumps(meshrecord,indent=2)+'\n')
(O/'gmsh.log').write_text('\n'.join(gmsh.logger.get())+'\n');gmsh.logger.stop();gmsh.finalize()
for pattern in ['split','one_dog']:
 case=pattern;lines=['*HEADING',name+' '+pattern+'; clamped bore fixture; N/mm/MPa','*NODE']
 lines += [str(int(t))+','+','.join(f'{v:.13g}' for v in x) for t,x in zip(tags,xyz)]
 lines+=['*ELEMENT,TYPE=C3D10,ELSET=SOLID']+[','.join(map(str,e)) for e in elements]
 lines+=['*NSET,NSET=FIXED']+[','.join(map(str,fixnodes[i:i+16])) for i in range(0,len(fixnodes),16)]
 lines+=['*NSET,NSET=ALLNODES,GENERATE',f'1,{max(tags)},1','*MATERIAL,NAME=STEEL_ASSUMED','*ELASTIC','200000,0.3','*SOLID SECTION,ELSET=SOLID,MATERIAL=STEEL_ASSUMED','*BOUNDARY','FIXED,1,3','*STEP','*STATIC','*CLOAD']
 fs={}
 for j,m in enumerate(force_maps):
  total=500 if pattern=='split' else (1000 if j==0 else 0)
  for node,w in m.items():fs[node]=fs.get(node,0)-total*w
 assert abs(sum(fs.values())+1000)<1e-8
 lines += [f'{t},2,{v:.13g}' for t,v in fs.items() if v]
 lines+=['*NODE PRINT,NSET=ALLNODES','U','*NODE PRINT,NSET=FIXED','RF','*EL PRINT,ELSET=SOLID','S','*NODE FILE','U','*EL FILE','S','*END STEP']
 (O/(case+'.inp')).write_text('\n'.join(lines)+'\n')
 env=os.environ.copy();env['OMP_NUM_THREADS']='2'
 with (O/(case+'.log')).open('w') as f:r=subprocess.run([os.environ.get('CCX','ccx'),'-i',case],cwd=O,env=env,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(O,case,r.returncode)
 print(name,pattern,'native solve complete',flush=True)
print(json.dumps(meshrecord),flush=True)
