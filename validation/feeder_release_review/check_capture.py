"""Check the controlled native geometry capture without installing CAD software."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
load=lambda name:json.loads((H/name).read_text())
for name,rec in load('MANIFEST.json')['files'].items():
 p=(H/name).resolve();assert p.is_relative_to(H) and p.is_file(),name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'],name
source=hashlib.sha256((H/'mechanism.py').read_bytes()).hexdigest()
a=load('GEOMETRY_AUDIT.json');assert a['revision']=='FM07-R5' and a['CAD_source_sha256']==source
assert sum(len(c['checks']) for c in a['configurations'])==80
assert all(not r['invalid'] and not r['collisions'] for c in a['configurations'] for r in c['checks'])
s=load('CONTINUOUS_SWEEPS.json');assert len(s['cases'])==40 and s['total_penetrations']==0
assert s['source_sha256']['mechanism.py']==source
x=load('INDEPENDENT_STEP.json');assert len(x['assemblies'])==20 and len(x['parts'])==74
assert all(r['valid'] for r in x['assemblies']+x['parts'])
assert all(abs(r['symmetric_volume_difference_mm3'])<1e-5 for r in load('COMPONENT_GEOMETRY_LINEAGE.json')['checks'])
g=load('comparison_reference/D27_GATE_ASSESSMENT.json');assert len(g['candidates'])==7
assert not any(r['eligible_for_selection'] for r in g['candidates'])
print('PASS: 46 cycle poses,34 rotary samples,40 continuous translations,20 assemblies/74 part STEP identities. Selection and loaded/hardware acceptance remain separate gates.')
