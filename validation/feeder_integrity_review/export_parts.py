"""Reference individual STEP exchanges at the controlled stored assembly datum."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
import Part
from mechanism import shapes,State,REVISION
H=Path(__file__).resolve().parent;O=H/'parts';O.mkdir(exist_ok=True);records=[]
for size,L in [('1U',113.5),('3U',340.5)]:
 ss,meta=shapes(L,State())
 for n,shape in ss.items():
  sh=shape.Solids[0];d=App.newDocument('Component');ob=d.addObject('Part::Feature','Component');ob.Label=n;ob.Shape=sh;d.recompute();p=O/(REVISION.replace('-','')+'_'+size+'_'+n+'.step');Part.export([ob],str(p));q=Part.read(str(p));assert q.isValid() and len(q.Solids)==1;assert abs(q.Volume-sh.Volume)<1e-3
  records.append({'file':p.name,'size':size,'part':n,'material_basis':meta[n][0],'role':meta[n][1],'volume_mm3':sh.Volume,'CG_mm':list(sh.CenterOfMass),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});App.closeDocument(d.Name)
 print(size,len(ss),'individual STEP components exported',flush=True)
(O/'INDEX.json').write_text(json.dumps({'revision':REVISION,'state':'stored; original assembly coordinates and axes retained','boundary':'Nominal reference component exchanges, not manufacturing drawings or supplier-approved geometry. Catalogue envelopes, pins, guide/actuator joints and contact faces remain subject to the report limitations. All masses are separate declared/material proxies.','source_sha256':hashlib.sha256((H/'mechanism.py').read_bytes()).hexdigest(),'parts':records},indent=2)+'\n')
