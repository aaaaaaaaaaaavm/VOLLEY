"""Extract per-solid native signatures from an immutable copied FCStd state.

Run with system Python and /usr/lib/freecad/lib on sys.path.
"""
from pathlib import Path
import argparse,hashlib,json,sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App

ap=argparse.ArgumentParser();ap.add_argument('snapshot',type=Path);ap.add_argument('stem');a=ap.parse_args()
p=a.snapshot/(a.stem+'.FCStd');raw=p.read_bytes();doc=App.openDocument(str(p));rows=[]
for obj in doc.Objects:
    if not hasattr(obj,'Shape')or obj.Shape.isNull():continue
    solid_rows=[]
    for i,solid in enumerate(obj.Shape.Solids):
        b=solid.BoundBox
        solid_rows.append(dict(index=i,volume_mm3=solid.Volume,centre_mm=list(solid.CenterOfMass),
            bounds_mm=[b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax],valid=solid.isValid()))
    rows.append(dict(name=obj.Label,native_name=obj.Name,solids=solid_rows))
App.closeDocument(doc.Name)
assert raw==p.read_bytes()
(a.snapshot/'NATIVE_SOLID_SIGNATURES.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(raw).hexdigest(),objects=rows),indent=2)+'\n')
print('Captured',sum(len(r['solids'])for r in rows),'native solid signatures',flush=True)
