"""Actual STEP tine; linear elastic unit transverse end traction. N/mm/MPa."""
from pathlib import Path
import sys,os,subprocess,json,math,hashlib
sys.path.insert(0,'/workspace/volley-work/native-tools/python')
import gmsh,numpy as np
H=Path(__file__).resolve().parent
for h in [4.,2.5,1.6,1.]:
 O=H/f'h{h:g}';O.mkdir(exist_ok=True)
 gmsh.initialize();gmsh.logger.start();gmsh.option.setNumber('General.NumThreads',1);gmsh.model.add('Tine');gmsh.model.occ.importShapes(str(H/'tine.step'));gmsh.model.occ.synchronize()
 fixed=[];loaded=[]
 for dim,tag in gmsh.model.getEntities(2):
  c=gmsh.model.occ.getCenterOfMass(dim,tag)
  if abs(c[1]+206)<1e-6:fixed.append(tag)
  if abs(c[1]+97)<1e-6:loaded.append(tag)
 assert len(fixed)==len(loaded)==1
 gmsh.option.setNumber('Mesh.MeshSizeMin',h/2);gmsh.option.setNumber('Mesh.MeshSizeMax',h);gmsh.option.setNumber('Mesh.ElementOrder',2);gmsh.model.mesh.generate(3);gmsh.model.mesh.setOrder(2);gmsh.write(str(O/'mesh.msh'));gmsh.write(str(O/'mesh.inp'))
 tags,xyz,_=gmsh.model.mesh.getNodes();xyz=np.asarray(xyz).reshape(-1,3);coords={int(t):x for t,x in zip(tags,xyz)}
 fixed_nodes=sorted({int(t) for f in fixed for t in gmsh.model.mesh.getNodes(2,f,includeBoundary=True)[0]});weights={};area=0
 types,_,conn=gmsh.model.mesh.getElements(2,loaded[0])
 for typ,connect in zip(types,conn):
  assert gmsh.model.mesh.getElementProperties(typ)[3]==6
  for tri in np.asarray(connect).reshape(-1,6):
   p=[coords[int(t)] for t in tri[:3]];a=np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))/2;area+=a
   for t in tri[3:]:weights[int(t)]=weights.get(int(t),0)+a/3
 assert abs(area-102)<1e-6
 element=[];mode=False
 for line in (O/'mesh.inp').read_text().splitlines():
  if line.upper().startswith('*ELEMENT'):mode='C3D10' in line.upper();continue
  if line.startswith('*'):mode=False
  if mode and line.strip():element.append([int(x) for x in line.split(',') if x.strip()])
 q=gmsh.model.mesh.getElementQualities([r[0] for r in element],'minSJ');assert min(q)>0
 (O/'gmsh.log').write_text('\n'.join(gmsh.logger.get()));gmsh.logger.stop();gmsh.finalize()
 lines=['*HEADING','FM04 actual tine, clamped root unit end shear, N/mm/MPa','*NODE']+[str(int(t))+','+','.join(f'{v:.13g}' for v in x) for t,x in zip(tags,xyz)]
 lines+=['*ELEMENT,TYPE=C3D10,ELSET=SOLID']+[','.join(map(str,r)) for r in element]
 lines+=['*NSET,NSET=FIXED']+[','.join(map(str,fixed_nodes[i:i+16])) for i in range(0,len(fixed_nodes),16)]
 lines+=['*NSET,NSET=ALLNODES,GENERATE',f'1,{max(tags)},1','*MATERIAL,NAME=AL_ASSUMED','*ELASTIC','69000,0.33','*SOLID SECTION,ELSET=SOLID,MATERIAL=AL_ASSUMED','*BOUNDARY','FIXED,1,3','*STEP','*STATIC','*CLOAD']+[f'{t},3,{-w/area:.13g}' for t,w in weights.items()]+['*NODE PRINT,NSET=ALLNODES','U','*NODE PRINT,NSET=FIXED','RF','*EL PRINT,ELSET=SOLID','S','*NODE FILE','U','*EL FILE','S','*END STEP']
 (O/'unit.inp').write_text('\n'.join(lines)+'\n')
 env=os.environ.copy();env['LD_LIBRARY_PATH']='/workspace/volley-work/native-tools/root/usr/lib/x86_64-linux-gnu';env['OMP_NUM_THREADS']='1'
 with (O/'unit.log').open('w') as f:r=subprocess.run(['/workspace/volley-work/native-tools/root/usr/bin/ccx','-i','unit'],cwd=O,env=env,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0
 mode=None;U={};RF={};VM=[]
 for line in (O/'unit.dat').read_text().splitlines():
  if 'displacements (' in line:mode='U';continue
  if 'forces (' in line:mode='RF';continue
  if 'stresses (' in line:mode='S';continue
  a=line.split()
  try:
   if mode in ['U','RF'] and len(a)==4:(U if mode=='U' else RF)[int(a[0])]=list(map(float,a[1:]))
   elif mode=='S' and len(a)==8:
    xx,yy,zz,xy,xz,yz=map(float,a[2:]);VM.append(math.sqrt(.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3*(xy*xy+xz*xz+yz*yz)))
  except ValueError:pass
 assert len(U)==len(tags)
 reaction=np.sum(list(RF.values()),axis=0);moment=np.sum([np.cross(coords[t],v) for t,v in RF.items()],axis=0);loadmoment=np.sum([np.cross(coords[t],[0,0,-w/area]) for t,w in weights.items()],axis=0)
 assert np.linalg.norm(reaction-[0,0,1])<1e-5
 assert np.linalg.norm(moment+loadmoment)<1e-3
 out={'h_mm':h,'nodes':len(tags),'elements':len(element),'min_scaled_Jacobian':float(min(q)),'max_abs_Z_mm_per_N':max(abs(v[2]) for v in U.values()),'loaded_mean_Z_mm_per_N':-sum(weights[t]*U[t][2] for t in weights)/area,'max_vm_MPa_per_N':max(VM),'reaction_N':reaction.tolist(),'moment_residual_N_mm':(moment+loadmoment).tolist(),'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file()}}
 (O/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['h_mm'],out['elements'],out['loaded_mean_Z_mm_per_N'],flush=True)
