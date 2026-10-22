from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST.json').read_text())
for name,a in m['files'].items():
 p=R/name
 assert p.is_file() and p.stat().st_size==a['bytes'],name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],name
d=json.loads((R/'release/REVIEW.json').read_text())
assert len(d['comparison'])==7 and d['selected_architecture'] is None
assert all(x['cells']==4 and x['common_receivers']==1 and x['full_installed_dry_mass_kg'] is None and not x['downselect_eligible'] for x in d['comparison'])
t=json.loads((R/'release/LEAD_TRIM_R2.json').read_text())
assert t['exact_nominal_payload_sweep_pass'] is True
assert t['all_mandatory_acceptance_gates_pass'] is False
s=json.loads((R/'INDEPENDENT_STEP.json').read_text())
assert len(s['exchanges'])==10 and all(x['pass'] for x in s['exchanges'])
print('PASS: seven comparable four-cell source/CAD captures and restricted R2 correction; installed/loaded/fault gates remain open')
