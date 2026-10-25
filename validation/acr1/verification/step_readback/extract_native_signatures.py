from pathlib import Path
import json,hashlib
import FreeCAD as App
H=Path(__file__).resolve().parent;P=H/'home_first_snapshot/VOLLEY_G5_ACR1_home.FCStd';doc=App.openDocument(str(P));rows=[]
for obj in doc.Objects:
 if not hasattr(obj,'Shape') or obj.Shape.isNull():continue
 sh=obj.Shape;ss=[]
 for i,s in enumerate(sh.Solids):
  bb=s.BoundBox;ss.append({'index':i,'volume_mm3':s.Volume,'centre_mm':list(s.CenterOfMass),'bounds_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax],'valid':s.isValid()})
 rows.append({'name':obj.Label,'native_name':obj.Name,'shape_volume_mm3':sh.Volume,'sum_solid_volume_mm3':sum(s['volume_mm3']for s in ss),'solids':ss,'valid':sh.isValid()})
result={'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'objects':rows,'sum_shape_volume':sum(r['shape_volume_mm3']for r in rows),'sum_solids_volume':sum(r['sum_solid_volume_mm3']for r in rows)}
(H/'NATIVE_SOLID_SIGNATURES.json').write_text(json.dumps(result,indent=2)+'\n');print('objects',len(rows),'shapesum',result['sum_shape_volume'],'solidssum',result['sum_solids_volume']);App.closeDocument(doc.Name)
