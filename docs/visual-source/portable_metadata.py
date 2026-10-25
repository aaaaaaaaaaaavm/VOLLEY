"""Repository-relative publication indexes; immutable capture bytes are not rewritten."""
from pathlib import Path
import copy,json,hashlib,zipfile
from functools import lru_cache
REPO=Path(__file__).resolve().parents[2]
DOCS=REPO/'docs'
SCENE_ARCHIVE='docs/downloads/VOLLEY_G5_ACR1_editable_scene.zip'
SCENE_MEMBER='VOLLEY_G5_ACR1_scientific_views.blend'
RELEASE_IDENTITY='containing Git commit or release tag'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def repo_path(value):
 if not isinstance(value,str):return value
 if value.startswith('docs/')or value.startswith('validation/'):return value
 if value.startswith('/workspace/volley-work/2026-10-24-gen5-acr1/'):
  return 'validation/acr1/'+value.split('/2026-10-24-gen5-acr1/',1)[1]
 if value.startswith(('assets/','downloads/','films/','visual-source/')):return 'docs/'+value
 if value.endswith('.html'):return 'docs/'+value
 return value

@lru_cache(maxsize=1)
def scene_reference():
 with zipfile.ZipFile(REPO/SCENE_ARCHIVE)as archive:
  sha=hashlib.sha256(archive.read(SCENE_MEMBER)).hexdigest()
 return {'archive_path':SCENE_ARCHIVE,'member_path':SCENE_MEMBER,'member_sha256':sha}

def software_metadata(data):
 d=copy.deepcopy(data)
 if not isinstance(d,dict):return d
 d.pop('publish_status',None)
 d['path_base']='repository_root'
 d['release_identity']=RELEASE_IDENTITY
 d['font']='DejaVuSans, DejaVuSans-Bold and DejaVuSansMono; installed runtime dependencies'
 d['font_license']='docs/visual-source/THIRD_PARTY_FONT_LICENSE.txt'
 d['cad_scene']=scene_reference()
 d['rebuild']='python3 docs/visual-source/build_films.py prepare; python3 docs/visual-source/build_films.py animatic; python3 docs/visual-source/build_films.py render'
 d['source_package_unpack_directory']='docs/'
 return d

def normalize_film(data):
 d=copy.deepcopy(data);key=d['film'];directory='docs/films/'+key+'/'
 d['path_base']='repository_root';d.pop('publication',None);d['release_identity']=RELEASE_IDENTITY
 for field in ['master','captions','transcript','poster']:
  if field in d:d[field]=directory+Path(d[field]).name
 d['editable_source']=['docs/visual-source/build_films.py','docs/visual-source/STORYBOARD.json']
 d['cad_scene']=scene_reference();d['sources']='docs/visual-source/SOURCE_PINS.json'
 for r in d.get('source_files',[]):r['path']=repo_path(r['path'])
 for field in ['render_script_archive','storyboard_archive']:
  if field in d:d[field]=repo_path(d[field])
 d['software']=software_metadata(d.get('software',{}))
 return d

def normalize_source_pins(data):
 return [dict(r,path=repo_path(r['path']),path_base='repository_root')for r in data]

def normalize_registry(data):
 d=copy.deepcopy(data);d['path_base']='repository_root';d['source_root']='validation/acr1'
 d.pop('publication',None);d.pop('release_commit',None)
 d['release_identity']=RELEASE_IDENTITY
 d['reviewer']='Source identity, captions and display checks are recorded in the linked verification files.'
 d['verification']='docs/visual-source/FINAL_ASSET_IDENTITY_REVIEW.json'
 d['public_source_index']='docs/visual-source/PUBLIC_SOURCE_INDEX.json'
 d['raw_capture_policy']='Original capture paths are retained inside immutable provenance files; public file locations are indexed here.'
 for r in d['assets']:
  r.pop('release_commit',None);r['release_identity']=RELEASE_IDENTITY
  if 'reviewer'in r:r['reviewer']='Source and caption checks recorded in the linked verification files.'
  for field in ['path','source_path','transcript','captions','source_pins','evidence_link','generator']:
   if field in r:r[field]=repo_path(r[field])
  if 'source'in r and isinstance(r['source'],dict):
   src=r['source']
   for field in ['native_path','step_path','bom_path']:
    if field in src:src[field]=repo_path(src[field])
   readback=src.get('independent_step_readback',{})
   if 'path'in readback:readback['path']=repo_path(readback['path'])
   src['source_sha256']={k if k.startswith('validation/')else'validation/acr1/cad/'+k:v for k,v in src.get('source_sha256',{}).items()}
   r['raw_capture']='docs/assets/acr1/'+Path(r['path']).stem+'_provenance.json'
  if r.get('asset_id','').startswith('film-'):
   key=r['asset_id'].removeprefix('film-');film=json.loads((DOCS/'films'/key/'FILM_MANIFEST.json').read_text())
   r['scene']={'editorial_sources':film['editable_source'],'cad_scene':scene_reference()}
   r['original_render_script']=film.get('render_script_archive','docs/visual-source/build_films.py')
   r['original_storyboard']=film.get('storyboard_archive','docs/visual-source/STORYBOARD.json')
   r['camera_provenance']='docs/assets/acr1/VIEW_PROVENANCE.json';r['camera']='Source-specific; see camera provenance.'
   r['software']=software_metadata(r['software'])
  elif isinstance(r.get('scene'),str):r['scene']=scene_reference()
  if r.get('asset_id')=='ACR1_social_preview':r['generator']='docs/visual-source/finalize_assets.py';r['software']='Pillow 12.3.0'
  if r['path'].startswith('docs/downloads/'):
   r['evidence_class']='editable visual source package';r['caption']='Source-only visual package with retained source identities and third-party notices.'
 for r in d.get('retired_asset_groups',[]):
  for field in ['path','evidence_route']:
   if field in r:r[field]=repo_path(r[field])
 d.get('academic_release_policy',{}).pop('cutoff_state',None)
 if 'external_academic_downloads'in d:d['external_academic_downloads']['path_base']='source_repository_root'
 d['assets']=list({r['path']:r for r in d['assets']}.values())
 return d

def public_source_index():
 raw=json.loads((DOCS/'assets/acr1/VIEW_PROVENANCE.json').read_text());refs=[]
 for v in raw['views']:
  src=v['native_provenance']
  for kind in ['native','step','bom']:
   path=repo_path(src[kind+'_path']);refs.append({'role':kind,'view':v['view_id'],'path':path,'sha256':src[kind+'_sha256']})
  readback=src['independent_step_readback'];refs.append({'role':'independent STEP readback','view':v['view_id'],'path':repo_path(readback['path']),'sha256':readback['sha256']})
  for name,sha in src['source_sha256'].items():refs.append({'role':'CAD generator source','path':'validation/acr1/cad/'+name,'sha256':sha})
 for r in json.loads((DOCS/'visual-source/SOURCE_PINS.json').read_text()):refs.append({'role':'film input','path':repo_path(r['path']),'sha256':r['sha256']})
 story=json.loads((DOCS/'visual-source/STORYBOARD.json').read_text())
 for film in story.values():
  for slide in film['slides']:
   for label in slide['source'].split(';'):
    label=label.strip()
    path='docs/assets/acr1/'+Path(label).name if label.startswith('visuals/')else'validation/acr1/'+label
    if not(REPO/path).is_file():
     candidate='docs/visual-source/inputs/'+Path(label).name
     if(REPO/candidate).is_file():path=candidate
    if not(REPO/path).is_file():raise FileNotFoundError(path)
    refs.append({'role':'storyboard evidence','source_label':label,'path':path,'sha256':digest(REPO/path)})
 refs.append({'role':'CAD view renderer','path':'docs/assets/acr1/render_cad_views.py','sha256':raw['render_script_sha256']})
 refs=list({(r['role'],r['path'],r.get('view'),r.get('source_label')):r for r in refs}.values())
 index={'revision':'ACR1-public-source-index-R1','path_base':'repository_root','release_identity':RELEASE_IDENTITY,'configuration':'VOLLEY-G5-ACR1','raw_capture':'docs/assets/acr1/VIEW_PROVENANCE.json','scene':scene_reference(),'archive_members':[{'role':'visualization mesh','view':v['view_id'],'archive_path':SCENE_ARCHIVE,'member_path':'meshes/'+Path(v['source_mesh_file']).name,'member_sha256':v['source_mesh_sha256']}for v in raw['views']],'files':refs}
 (DOCS/'visual-source/PUBLIC_SOURCE_INDEX.json').write_text(json.dumps(index,indent=2))
 return index

if __name__=='__main__':
 source=DOCS/'visual-source';pins=source/'SOURCE_PINS.json';pins.write_text(json.dumps(normalize_source_pins(json.loads(pins.read_text())),indent=2))
 metadata=source/'FILM_SOURCE_MANIFEST.json';metadata.write_text(json.dumps(software_metadata(json.loads(metadata.read_text())),indent=2))
 for p in (DOCS/'films').glob('*/FILM_MANIFEST.json'):p.write_text(json.dumps(normalize_film(json.loads(p.read_text())),indent=2))
 public_source_index()
 reg=DOCS/'assets/acr1/ASSET_REGISTER.json';reg.write_text(json.dumps(normalize_registry(json.loads(reg.read_text())),indent=2))
 print('Generated repository-relative publication metadata and public source index.')
