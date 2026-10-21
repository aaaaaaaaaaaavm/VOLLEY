"""Actual CAD meshes for labelled Blender render; no mechanical evidence is created."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
import Part
H=Path(__file__).resolve().parent;O=H/'render_meshes';O.mkdir(exist_ok=True)
rows=[]
for phase in ['stored','transfer','fork_home']:
 p=H/'cad'/('FM06_3U_'+phase+'.FCStd');d=App.openDocument(str(p));out=[]
 for ob in d.Objects:
  if not hasattr(ob,'Shape'):continue
  sh=ob.Shape;v,ff=sh.tessellate(.08);name=ob.Label;fn=phase+'_'+name+'.obj';f=O/fn
  with f.open('w') as h:
   for q in v:h.write('v %.10g %.10g %.10g\n'%(q.x*.001,q.y*.001,q.z*.001))
   for tri in ff:h.write('f %d %d %d\n'%tuple(i+1 for i in tri))
  out.append({'name':name,'file':fn,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 App.closeDocument(d.Name);rows.append({'phase':phase,'source':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parts':out})
(O/'MESHES.json').write_text(json.dumps({'revision':'FM06','tessellation_mm':.08,'evidence_class':'CAD-derived visualization meshes, not analysis or hardware','poses':rows},indent=2)+'\n');print('3actual CAD states exported for visualization')
