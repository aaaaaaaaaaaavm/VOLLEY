"""Read the R6 STEP exchanges through CadQuery, independently of the exporter."""
from pathlib import Path
import hashlib,json
import cadquery as cq
H=Path(__file__).resolve().parent
rows=[]
for r in json.loads((H/'DELTA_AND_EXPORT.json').read_text())['records']:
    if r['kind']=='part':
        name=r['file'];volume=r['volume_mm3'];count=1;expected=r['sha256']
    else:
        name=next(n for n in r['files'] if n.endswith('.step'))
        volume=r['source_volume_mm3'];count=r['components'];expected=r['files'][name]
    p=H/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
    s=cq.importers.importStep(str(p)).val()
    assert s.isValid() and len(s.Solids())==count
    assert abs(s.Volume()-volume)<0.01
    rows.append(dict(file=name,kind=r['kind'],valid=True,solids=count,volume_difference_mm3=s.Volume()-volume))
out=dict(method='CadQuery STEP readback; separate importer using OpenCascade, not a different geometric kernel',cases=rows)
(H/'INDEPENDENT_STEP.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',len(rows),'STEP files')
