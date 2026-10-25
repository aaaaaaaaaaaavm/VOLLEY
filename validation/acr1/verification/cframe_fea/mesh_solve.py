"""Quarter-symmetry isolated C-frame3D elasticity; not full assembled sled FEA."""
from pathlib import Path
import argparse,os,subprocess,json,hashlib,math,time,collections
import numpy as np
import gmsh
H=Path(__file__).resolve().parent;BASE=H.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--h',type=float,default=12);args=ap.parse_args();O=H/f'h{args.h:g}';O.mkdir(exist_ok=True)
P=BASE/'cad/PARAMETERS.json';raw=P.read_bytes();p=json.loads(raw);l=p['launch'];m=p['magnetic'];F=json.loads((H.parent/'NORMAL_ATTRACTION.json').read_text())['nominal_reference_force_N']
L=l['carrier_length']/2;webmin,webmax=l['carrier_negative_web_y'];top=l['carrier_top_plate_z'][1];inner=l['carrier_top_plate_z'][0];ymax=70.;maghalf=m['block_depth_y']/2;activehalf=m['blocks_per_array']*m['block_pitch']/2
started=time.perf_counter();gmsh.initialize();gmsh.logger.start();gmsh.option.setNumber('General.NumThreads',2);gmsh.option.setNumber('General.Terminal',1);gmsh.model.add('isolated_cframe_quarter')
vol=[]
for x0,x1 in [(0,activehalf),(activehalf,L)]:
 vol.append((3,gmsh.model.occ.addBox(x0,webmin,0,x1-x0,webmax-webmin,inner)))
 for y0,y1 in [(webmin,webmax),(webmax,-maghalf),(-maghalf,maghalf),(maghalf,ymax)]:
  vol.append((3,gmsh.model.occ.addBox(x0,y0,inner,x1-x0,y1-y0,top-inner)))
fragment,_=gmsh.model.occ.fragment(vol,[]);gmsh.model.occ.synchronize()
loadfaces=[]
for dim,tag in gmsh.model.getEntities(2):
 bb=gmsh.model.getBoundingBox(dim,tag);cx,cy,cz=gmsh.model.occ.getCenterOfMass(dim,tag)
 if abs(bb[2]-inner)<1e-4 and abs(bb[5]-inner)<1e-4 and bb[0]>-1e-4 and bb[3]<activehalf+1e-4 and bb[1]>-maghalf-1e-4 and bb[4]<maghalf+1e-4:loadfaces.append(tag)
assert loadfaces, 'Pressure patch not imprinted'
area=sum(gmsh.model.occ.getMass(2,t)for t in loadfaces);assert abs(area-activehalf*2*maghalf)<1e-5,(area,loadfaces)
gmsh.model.addPhysicalGroup(3,[tag for dim,tag in gmsh.model.getEntities(3)],name='SOLID')
gmsh.option.setNumber('Mesh.MeshSizeMin',args.h/2);gmsh.option.setNumber('Mesh.MeshSizeMax',args.h);gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',0);gmsh.option.setNumber('Mesh.ElementOrder',2)
gmsh.model.mesh.generate(3);gmsh.model.mesh.setOrder(2);gmsh.write(str(O/'mesh.msh'));gmsh.write(str(O/'mesh_export.inp'))
tags,coords,_=gmsh.model.mesh.getNodes();xyz=np.asarray(coords).reshape(-1,3);node={int(n):np.asarray(c)for n,c in zip(tags,xyz)}
fixx=[int(n)for n,c in node.items()if abs(c[0])<1e-6];fixz=[int(n)for n,c in node.items()if abs(c[2])<1e-6]
fixy=min(fixz,key=lambda n:(node[n][0])**2+(node[n][1]-(webmin+webmax)/2)**2)
pressure=F/(2*activehalf*2*maghalf);forces=collections.defaultdict(float);integrated_area=0.
for face in loadfaces:
 types,ets,conn=gmsh.model.mesh.getElements(2,face)
 for typ,cn in zip(types,conn):
  nn=gmsh.model.mesh.getElementProperties(typ)[3];assert nn==6
  for tri in np.asarray(cn).reshape(-1,6):
   a,b,c=[node[int(t)]for t in tri[:3]];A=np.linalg.norm(np.cross(b-a,c-a))/2;integrated_area+=A
   for n in tri[3:]:forces[int(n)]-=pressure*A/3
assert abs(integrated_area-area)<1e-6 and abs(sum(forces.values())+F/2)<1e-7
text=(O/'mesh_export.inp').read_text();elements=[];mode=False
for line in text.splitlines():
 if line.upper().startswith('*ELEMENT'):mode='C3D10' in line.upper();continue
 if line.startswith('*'):mode=False
 if mode and line.strip():
  q=[int(v)for v in line.split(',')if v.strip()];assert len(q)==11;elements.append(q)
assert elements
quality=gmsh.model.mesh.getElementQualities([q[0]for q in elements],'minSJ');assert min(quality)>0
# Connected mesh, not coincident but disconnected volume islands.
parent={int(n):int(n)for n in tags}
def find(n):
 while parent[n]!=n:parent[n]=parent[parent[n]];n=parent[n]
 return n
for e in elements:
 root=find(e[1])
 for n in e[2:]:parent[find(n)]=root
assert len({find(int(n))for n in tags})==1
runtime=gmsh.option.getString('General.Version');(O/'gmsh.log').write_text('\n'.join(gmsh.logger.get())+'\n');gmsh.logger.stop();gmsh.finalize()
lines=['*HEADING','ACR1 isolated C-frame quarter;N/mm/MPa;not assembled qualification','*NODE']
lines += [str(int(n))+','+','.join(f'{v:.13g}'for v in c)for n,c in node.items()]
lines+=['*ELEMENT,TYPE=C3D10,ELSET=SOLID']+[','.join(map(str,q))for q in elements]
for name,ns in [('SYMX',fixx),('SYMZ',fixz),('PINY',[fixy]),('ALLNODES',sorted(node))]:
 lines+=['*NSET,NSET='+name]+[','.join(map(str,ns[i:i+16]))for i in range(0,len(ns),16)]
lines+=['*MATERIAL,NAME=AL_ASSUMED','*ELASTIC','70000,0.33','*SOLID SECTION,ELSET=SOLID,MATERIAL=AL_ASSUMED','*BOUNDARY','SYMX,1,1','SYMZ,3,3','PINY,2,2','*STEP','*STATIC','*CLOAD']
lines += [f'{n},3,{v:.14g}'for n,v in forces.items()]
lines += ['*NODE PRINT,NSET=ALLNODES','U','*NODE PRINT,NSET=SYMX','RF','*NODE PRINT,NSET=SYMZ','RF','*NODE PRINT,NSET=PINY','RF','*NODE FILE','U','*EL FILE','S','*END STEP']
(O/'cframe.inp').write_text('\n'.join(lines)+'\n')
metadata={'configuration':p['configuration_id'],'cad_parameters_sha256':hashlib.sha256(raw).hexdigest(),'mesh_builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'gmsh_binding_version':gmsh.__version__,'gmsh_runtime_version':runtime,'h_max_mm':args.h,'nodes':len(node),'C3D10_elements':len(elements),'minimum_scaled_jacobian':float(min(quality)),'connected_mesh_components':1,'pressure_patch_area_quarter_mm2':area,'normal_force_full_array_N':F,'applied_quarter_pressure_N_mm2':pressure,'applied_quarter_nodal_force_N':sum(forces.values()),'supports':'Xmidplane Ux0,Zmidplane Uz0;onewebmidplaneUyconstraint removes rigid translation. No artificial double-web or loaded-edge clamp.','geometry':'UpperXhalf/Zhalf of uniform488mmextrudedCframe;plate16mm/web20mm ascurrentparameters;no backstop,magnets,bonds,rollers,joints,cradleorassembledsupportmodel.','units':'N,mm,MPa','symmetry_assumption':'Symmetricpairednormalattraction andsymmetriclongitudinalloadpatch;model omits actual asymmetric attachments.','load_definition':'ActualcuboidMaxwelltotalforceredistributeduniformlyover336x90patch;notphysicaltractionmap.','loaded_node_tags':sorted(forces),'node_coordinates':{str(n):c.tolist()for n,c in node.items()},'wall_s_before_solve':time.perf_counter()-started}
(O/'MESH.json').write_text(json.dumps(metadata,indent=2)+'\n')
env=os.environ.copy();env['OMP_NUM_THREADS']='2';env['CCX_NPROC_STIFFNESS']='2'
ccx='/workspace/volley-work/native-tools/root/usr/bin/ccx'
with (O/'ccx.log').open('w') as f:run=subprocess.run([ccx,'-i','cframe'],cwd=O,env=env,stdout=f,stderr=subprocess.STDOUT)
assert run.returncode==0,(run.returncode,O/'ccx.log')
print(json.dumps({'h':args.h,'nodes':len(node),'elements':len(elements),'load':sum(forces.values()),'solve_exit':run.returncode,'wall_s':time.perf_counter()-started}),flush=True)
