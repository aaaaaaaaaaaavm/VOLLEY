"""Check current lunar source identities and delivered references. Adityavardhan Mishra."""
from pathlib import Path
import hashlib,json
from html.parser import HTMLParser
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1];r=json.loads((R/'analysis/results/lunar_visual_design.json').read_text());m=json.loads((R/'cad/lunar_concept/manifest.json').read_text())
sha=lambda p:hashlib.sha256((R/p).read_bytes()).hexdigest()
assert r['sources']['analysis_sha256']==sha('analysis/lunar_visual_design.py')
assert r['sources']['criteria_sha256']==sha('validation/C0_S2_lunar_visual_design.md')
assert m['source_sha256']==sha('cad/lunar_concept/build_concepts.py')
assert all(r['checks'].values()) and all(c['pass_checks'] for c in m['checks'])
assert len(r['releases'])==42 and len(r['budgets'])==18 and len(m['checks'])==4
class References(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v and not urlsplit(v).scheme and not v.startswith('#'):
    assert (R/'docs'/urlsplit(v).path).exists(),v
References().feed((R/'docs/lunar.html').read_text())
assets=R/'docs/assets/lunar'
assert len(list(assets.glob('*.png')))==11
assert len(list(assets.glob('*.svg')))==6
assert (assets/'mission_data.js').read_text()=='window.VOLLEY_LUNAR='+json.dumps(r,separators=(',',':'))+';\n'
print('C0-S2: source/criteria hashes, four model checks, 42 releases, 18 budgets, 17 images and local page references PASS')
print('Real-browser rendering and all physical mission/hardware gates remain open.')
