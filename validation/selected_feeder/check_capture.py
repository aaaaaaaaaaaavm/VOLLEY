"""Verify the released feeder files and deterministic analytical/logic replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST.json').read_text())
for n,h in m['files'].items():
 p=R/n
 assert not Path(n).is_absolute() and '..' not in Path(n).parts,n
 assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,n
g=json.loads((R/'cad/release/GEOMETRY_REPORT.json').read_text())
v=json.loads((R/'cad/release/MOTION_VERIFICATION.json').read_text())
x=json.loads((R/'step_exchange/INDEPENDENT_STEP.json').read_text())
source=hashlib.sha256((R/'cad/build_selected.py').read_bytes()).hexdigest()
assert g['builder_sha256']==v['builder_sha256']==source
assert len(g['captures'])==5 and all(c['parts']==154 and c['step_solids']==154 and c['including_catalog_envelopes_audit']['pass'] for c in g['captures'])
assert len(g['motion_samples'])==18 and all(c['pass'] for c in g['motion_samples'])
assert v['case_count']==115 and v['failed_case_count']==0 and v['all_sampled_cases_pass']
assert x['all_checks_pass'] and len(x['exchanges'])==5
for c in x['exchanges']:
 assert hashlib.sha256((R/'cad/release'/c['file']).read_bytes()).hexdigest()==c['sha256']
b=json.loads((R/'cad/figures/BLENDER_PROVENANCE.json').read_text())
for c in b['renders']:
 assert hashlib.sha256((R/'cad/release'/c['source']).read_bytes()).hexdigest()==c['source_sha256']
 assert hashlib.sha256((R/'cad/figures'/c['image']).read_bytes()).hexdigest()==c['sha256']
subprocess.run([sys.executable,str(R/'verification/check_capture.py')],check=True,cwd=R)
print('PASS: selected feeder capture',len(m['files']),'exact files; native geometry and hardware evidence retain their stated boundaries.')
