"""Single closed exterior contact mesh per actual CAD solid, with topology audit."""
from pathlib import Path
import json,hashlib,itertools
import FreeCAD as App
import Part
from mechanism import shapes,State
H=Path(__file__).resolve().parent;O=H/'contact_geometry_surfaces';O.mkdir(exist_ok=True);records=[]
for size,L,m in [('1U',113.5,1.33),('3U',340.5,4.)]:
 d=O/size;d.mkdir(exist_ok=True);ss,meta=shapes(L,State(gate=120,bolt=0));rows=[];proof=[]
 for n,sh in ss.items():
  solid=sh.Solids[0];c=solid.CenterOfMass;v,faces=solid.tessellate(.005);unique={};verts=[];remap={}
  tol=1e-5
  import math
  for i,p in enumerate(v):
   key=tuple(math.floor(q/tol) for q in (p.x,p.y,p.z));found=None
   for delta in itertools.product([-1,0,1],repeat=3):
    for j in unique.get(tuple(key[a]+delta[a] for a in range(3)),[]):
     if (p-verts[j]).Length<=tol:found=j;break
    if found is not None:break
   if found is None:
    found=len(verts);verts.append(p);unique.setdefault(key,[]).append(found)
   remap[i]=found
  ff=[tuple(remap[i] for i in f) for f in faces];ff=[f for f in ff if len(set(f))==3];edges={};vol=0
  for f in ff:
   a,b,cross=[verts[i] for i in f];vol+=a.dot(b.cross(cross))/6
   for i,j in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted([i,j])),[]).append((i,j))
  assert all(len(q)==2 and q[0]==q[1][::-1] for q in edges.values()),(size,n,'not_closed_or_inconsistent_winding',[(k,len(vv)) for k,vv in edges.items() if len(vv)!=2][:8])
  assert vol>0,(size,n,vol)
  c=solid.CenterOfMass;f=d/(n+'.obj')
  with f.open('w') as h:
   for p in verts:h.write('v %.12g %.12g %.12g\n'%((p.x-c.x)*.001,(p.y-c.y)*.001,(p.z-c.z)*.001))
   for tri in ff:h.write('f %d %d %d\n'%tuple(i+1 for i in tri))
  role={'payload':'payload','fork_body':'fork','fork_front':'front','sled_entry_bar':'receiver'}.get(n,'fixed');mass=m if n=='payload' else sh.Volume*{'aluminium':2.7e-6,'steel':7.85e-6,'catalogue':1.4e-6,'payload':0}[meta[n][0]];I=solid.MatrixOfInertia;inertia=[mass/sh.Volume*getattr(I,'A'+str(i)+str(j))*1e-6 for i,j in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]]
  rows.append([n,role,str(mass)]+[str(q) for q in [c.x*.001,c.y*.001,c.z*.001]+inertia]+[f.name]);proof.append({'part':n,'source_vertex_count':len(v),'merged_vertex_count':len(verts),'triangles':len(ff),'closed_edges':len(edges),'signed_mesh_volume_mm3':vol,'actual_cad_volume_mm3':sh.Volume,'relative_volume_error':abs(vol/sh.Volume-1),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 (d/'bodies.tsv').write_text('\n'.join('\t'.join(r) for r in rows)+'\n');records.append({'size':size,'parts':proof});print(size,len(rows),'closed consistently wound CAD meshes',flush=True)
(O/'SURFACE_AUDIT.json').write_text(json.dumps({'source_sha256':hashlib.sha256((H/'mechanism.py').read_bytes()).hexdigest(),'tessellation_deflection_mm':.005,'method':'One exterior closed mesh for each actual solid; coincident vertices merged, all edges required to have two oppositely directed incident faces, positive oriented volume checked. No internal collision decomposition surfaces. Full CAD homogeneous material inertia retained.','cases':records},indent=2)+'\n')
