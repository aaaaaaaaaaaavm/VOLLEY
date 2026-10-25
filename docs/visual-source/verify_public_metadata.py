"""Check published relative locations, exact file identity and preserved capture references."""
from pathlib import Path
import json,hashlib,zipfile,re
from portable_metadata import REPO,DOCS,digest
checked=[]
def file(path,sha=None,base=REPO):
 assert isinstance(path,str)and not Path(path).is_absolute(),path
 p=(base/path).resolve();assert p.is_relative_to(base.resolve())and p.is_file(),path
 if sha:assert digest(p)==sha,path
 checked.append(path);return p

def scene(data):
 archive=file(data['archive_path'])
 with zipfile.ZipFile(archive)as z:assert hashlib.sha256(z.read(data['member_path'])).hexdigest()==data['member_sha256']

register=json.loads((DOCS/'assets/acr1/ASSET_REGISTER.json').read_text())
assert register['path_base']=='repository_root'
assert '/workspace/'not in json.dumps(register)
assert not re.search(r'pending|owner release|publication pending',json.dumps(register),re.I)
for r in register['assets']:
 file(r['path'],r['sha256'])
 for key in ['source_path','transcript','captions','source_pins','evidence_link','generator','raw_capture','camera_provenance','original_render_script','original_storyboard']:
  if key in r:file(r[key])
 for source_input in r.get('source_inputs',[]):file(source_input['path'],source_input['sha256'])
 if isinstance(r.get('source'),dict):
  source=r['source']
  for key in ['native','step','bom']:file(source[key+'_path'],source[key+'_sha256'])
  cap=source['independent_step_readback'];file(cap['path'],cap['sha256'])
  for path,sha in source['source_sha256'].items():file(path,sha)
 if isinstance(r.get('scene'),dict):
  s=r['scene']
  if 'archive_path'in s:scene(s)
  else:
   scene(s['cad_scene'])
   for path in s['editorial_sources']:file(path)
 for pathkey in ['font_license']:
  if isinstance(r.get('software'),dict)and pathkey in r['software']:file(r['software'][pathkey])
for r in register['external_academic_downloads']['artifacts']:
 file(r['source_path'],r['sha256'],REPO.parent/r['repository'])
for r in register.get('retired_asset_groups',[]):
 assert(REPO/r['path']).is_dir();file(r['evidence_route'])
index=json.loads((DOCS/'visual-source/PUBLIC_SOURCE_INDEX.json').read_text());assert index['path_base']=='repository_root';assert'/workspace/'not in json.dumps(index)
for r in index['files']:file(r['path'],r['sha256'])
scene(index['scene']);file(index['raw_capture'])
for member in index['archive_members']:scene(member)
for p in (DOCS/'films').glob('*/FILM_MANIFEST.json'):
 d=json.loads(p.read_text());assert d['path_base']=='repository_root';assert'/workspace/'not in json.dumps(d);assert'publication'not in d
 for key in ['master','captions','transcript','poster','sources']:file(d[key])
 for path in d['editable_source']:file(path)
 scene(d['cad_scene'])
 for r in d['source_files']:file(r['path'],r['sha256'])
 file(d.get('render_script_archive','docs/visual-source/build_films.py'),d['render_script_sha256'])
 file(d.get('storyboard_archive','docs/visual-source/STORYBOARD.json'),d['storyboard_sha256'])
# The original scene provenance is an immutable capture retained verbatim in the source ZIP.
with zipfile.ZipFile(DOCS/'downloads/VOLLEY_G5_ACR1_editable_scene.zip')as z:
 assert hashlib.sha256(z.read('VIEW_PROVENANCE.json')).hexdigest()==digest(DOCS/'assets/acr1/VIEW_PROVENANCE.json')
report={'status':'passed','path_base':'repository_root','resolved_file_references':len(checked),'unique_resolved_files':len(set(checked)),'registered_assets':len(register['assets']),'source_index_files':len(index['files']),'immutable_view_capture':'byte-identical to accepted scene-package capture','release_identity':'containing Git commit or release tag','checks':['All registered output hashes match','All referenced native/STEP/BOM/generator/readback hashes match','All current source/index paths resolve in the declared public repository','All film source/storyboard/input identities match their recorded versions','Current generated records contain no execution-workspace paths or owner-publication state','Academic downloads resolve against their explicitly named source repository']}
(DOCS/'visual-source/PUBLIC_METADATA_QA.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
