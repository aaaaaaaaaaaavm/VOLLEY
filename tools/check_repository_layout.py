"""Verify maintained landing-page structure, catalogue coverage and file navigation."""
from pathlib import Path
import argparse,collections,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'tools/front_page_layout.json'
def tracked():return subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().strip('\0').split('\0')
def headings(text):
 out=[];fenced=False
 for line in text.splitlines():
  if line.startswith(('```','~~~')):fenced=not fenced
  if not fenced and re.match(r'^#{1,2} ',line):out.append(line)
 return out
def expected_map(paths,spec):
 counts=collections.Counter(p.split('/')[0] for p in paths if '/' in p)
 lines=['# Repository map','',''+spec['role']+'','', '[Project overview](../README.md) · [Archive index](../archive/README.md)','','## File areas','','| Area | Tracked files | Purpose |','|:--|--:|:--|']
 for area in sorted(counts):
  purpose=spec['folders'].get(area)
  if purpose is None:raise ValueError('Declare a purpose and storage location for new file area: '+area)
  lines.append(f'| [{area}/](../{area}/) | {counts[area]} | {purpose} |')
 lines+=['','## Root files','','Root files contain project navigation, citation, licensing, repository configuration and cited legacy records. Legacy records retain their filenames when captured source identities depend on them.','']
 for name in sorted(p for p in paths if '/' not in p):lines.append(f'- [{name}](../{name})')
 lines+=['','## Versioned records','','Source, inputs, native CAD, solver logs and numerical outputs stay together within their captured study packages. Published scientific binaries and original captures retain their exact identities. Superseded concept documents are routed through the archive index. Active overview pages link to current and historical material without relabelling their results.','', 'The index is checked against the Git publication set. Its counts describe stored files, not engineering completion.','']
 return '\n'.join(lines)
def check(root=ROOT,write=False):
 global ROOT,SPEC
 ROOT=root;SPEC=ROOT/'tools/front_page_layout.json'
 if not SPEC.exists():raise ValueError('Missing maintained front-page specification')
 spec=json.loads(SPEC.read_text());paths=tracked();text=(ROOT/'README.md').read_text()
 if headings(text)!=spec['headings']:raise ValueError('Landing-page structure changed: review the explicit layout decision; routine updates preserve headings')
 if spec.get('catalogue'):
  required={'experiments/'+p.split('/')[1]+'/' for p in paths if p.startswith('experiments/')}
  required|={p for p in paths if p.startswith('archive/concepts/') and p.endswith('.md')}
  missing=sorted(p for p in required if p not in text)
  if missing:raise ValueError('Research catalogue omits retained study: '+', '.join(missing))
 output=ROOT/'docs/REPOSITORY_MAP.md';expected=expected_map(paths,spec)
 if write:output.write_text(expected)
 elif not output.exists() or output.read_text()!=expected:raise ValueError('Repository map is stale; stage the exact files, run python tools/check_repository_layout.py --write, then stage the map')
 return len(paths)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
 try:n=check(write=args.write)
 except ValueError as e:raise SystemExit('FAIL: '+str(e))
 print(f'PASS: maintained front-page sections, archive/catalogue routes and {n} tracked file locations')
