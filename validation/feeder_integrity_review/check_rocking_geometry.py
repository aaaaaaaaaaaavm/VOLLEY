"""Independent 3-D actual B-rep check of the 2-D rigid clearance optima."""
from pathlib import Path
import json,importlib.util,hashlib
import FreeCAD as App
import Part
from mechanism import shapes,State
H=Path(__file__).resolve().parent;D=json.loads((H/'GUIDE_PLAY.json').read_text());out=[]
# FM03 reference imported under a separate module; same ct_geometry reference.
p=H/'history/FM03/mechanism.py';spec=importlib.util.spec_from_file_location('fm03_rocking_reference',p);mod=importlib.util.module_from_spec(spec);import sys;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
for size,L in [('1U',113.5),('3U',340.5)]:
 for row in D['cases']:
  fn=shapes if row['revision']=='FM04' else mod.shapes;St=State if row['revision']=='FM04' else mod.State
  ss,_=fn(L,St(receiver=0,payload_feed=200));entry=ss['sled_entry_bar'].copy();entry.rotate(App.Vector(0,-10,0),App.Vector(1,0,0),row['theta_deg']);dy,dz=row['pin_center_offset_YZ_mm'];entry.translate(App.Vector(0,dy,dz))
  hits=[]
  for n in ['sled_body','receiver_lock_pin_0','receiver_lock_pin_1']:
   v=entry.common(ss[n]).Volume
   if v>1e-5:hits.append({'part':n,'mm3':v})
  out.append({'size':size,'revision':row['revision'],'direction':row['direction'],'radial_pin_clearance_assumed_mm':row['radial_pin_clearance_mm'],'penetrations':hits,'note':'Actual modeled bore radial clearance is0.15mm;0.1/0.2 sensitivities differ from actual model pin size and are not accepted geometries.'})
  print(size,row['revision'],row['direction'],row['radial_pin_clearance_mm'],hits,flush=True)
(H/'ROCKING_GEOMETRY.json').write_text(json.dumps({'cases':out,'boundary':'Rotated/translated actual receiver solid against actual fixed sled/pins. This checks the2D ideal-slot optimum for overlooked3D nominal interference. It is not loaded contact, strength, tolerances or manufacturing approval. Only0.15mm matches actual modeled pin radial fit.'},indent=2)+'\n')
