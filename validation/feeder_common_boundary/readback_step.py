from pathlib import Path
import json,math,hashlib
import cadquery as cq
R=Path(__file__).resolve().parent;D=R/'release'
expected={}
for p in D.glob('*_carrier_R1_comparison.json'):
 d=json.loads(p.read_text());name=next(n for n in d['files']if n.endswith('.step'))
 expected[name]={'solids':d['step_solid_count'],'volume':sum(x['volume_mm3']for x in d['BOM'])}
d=json.loads((D/'LEAD_TRIM_R2.json').read_text())['native'];name=next(n for n in d['files']if n.endswith('.step'))
expected[name]={'solids':d['step_solid_count'],'volume':sum(x['volume_mm3']for x in d['BOM'])}
results=[]
for p in sorted(D.glob('*.step')):
 shape=cq.importers.importStep(str(p)).val();solids=shape.Solids();vol=sum(s.Volume()for s in solids)
 e=expected.get(p.name);valid=shape.isValid()and all(s.isValid()for s in solids)
 passed=valid and len(solids)>0 and vol>0
 rec={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'valid':valid,'solids':len(solids),'volume_mm3':vol}
 if e:
  rec['expected']=e;rec['relative_volume_error']=abs(vol-e['volume'])/e['volume'];passed=passed and len(solids)==e['solids']and rec['relative_volume_error']<=1e-6
 rec['pass']=bool(passed);results.append(rec);print(p.name,len(solids),'PASS'if passed else'FAIL',flush=True)
report={'method':'Separate CadQuery/OCC import; same kernel family, no functional acceptance.1ppm relative serialization volume criterion preserves supplied geometric exchange criterion.','exchanges':results}
(R/'INDEPENDENT_STEP.json').write_text(json.dumps(report,indent=2)+'\n')
assert len(results)==10 and all(r['pass']for r in results)
