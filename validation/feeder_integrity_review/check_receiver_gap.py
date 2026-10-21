from pathlib import Path
import FreeCAD as App
import Part
import json
from mechanism import shapes,State
H=Path(__file__).resolve().parent;out=[]
for size,L in [('1U',113.5),('3U',340.5)]:
 for x in [0,10,15,20,40,80]:
  ss,_=shapes(L,State(receiver=0,payload_feed=200,sled=x))
  for n,sh in ss.items():
   if n.startswith('cassette_L_'):
    out.append({'size':size,'sled_X_mm':x,'pair':['sled_entry_bar',n],'minimum_distance_mm':ss['sled_entry_bar'].distToShape(sh)[0],'intersection_mm3':ss['sled_entry_bar'].common(sh).Volume})
(H/'RECEIVER_GAP_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
