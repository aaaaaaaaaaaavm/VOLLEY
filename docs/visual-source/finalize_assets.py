"""Finalize provenance after source exports, films and browser checks exist."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
from PIL import Image,ImageDraw,ImageFont
from portable_metadata import normalize_registry, public_source_index
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;A=ROOT/'assets/acr1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# A source-derived social card: no geometry edits or simulated scene.
im=Image.new('RGB',(1200,630),'#11161c');d=ImageDraw.Draw(im)
def f(n,bold=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold'if bold else'')+'.ttf',n)
d.text((48,44),'VOLLEY',font=f(28,True),fill='#f6f5f1');d.text((48,99),'G5 ACR1',font=f(15),fill='#bfe3cf')
for y,line in [(185,'Commanded'),(237,'CubeSat'),(289,'deployment.')]:d.text((48,y),line,font=f(39,True),fill='#f6f5f1')
d.text((48,414),'Computational',font=f(20),fill='#bcc3c9');d.text((48,445),'design study',font=f(20),fill='#bcc3c9')
pic=Image.open(A/'01_assembly_isometric.jpg');pic.thumbnail((735,552),Image.Resampling.LANCZOS);im.paste(pic,(435+(735-pic.width)//2,39+(552-pic.height)//2))
d.text((48,580),'CAD-derived render / controlled source',font=f(12),fill='#bcc3c9');im.save(A/'ACR1_social_preview.png')
# Include current image/source metadata and complete download/film identities.
public_source_index()
register=json.loads((A/'ASSET_REGISTER.json').read_text())
for item in register['assets']:
 if item['path'].startswith('docs/'):item['path']=item['path'][5:]
view=json.loads((A/'VIEW_PROVENANCE.json').read_text());records=register['assets']
lookup={r['path']:r for r in records}
sources={
 'coupled_shot_reference':('analysis/COUPLED_SHOT.json','Coupled modeled release, electrical and arrest histories.'),
 'feeder_transfer_profile':('analysis/FEEDER_PROFILES.csv','Prescribed feeder transfer profile with units.'),
 'finite_force_coefficient':('analysis/FINITE_MOTOR.json','Finite-geometry force coefficient over the modeled stroke.'),
 'magnetic_gap_section':('analysis/FINITE_MOTOR_INPUT.json','Scientific section through the controlled magnetic gap geometry.'),
 'shot_energy_ledger':('analysis/COUPLED_SHOT.json','Computed component energy ledger for the reference shot.'),
 'MISSION_RESOURCES':('mission/MISSION_RESULTS.csv','Bounded same-input mission fuel and wet-mass comparison.'),
 'MISSION_TARGETS':('mission/TARGETS.json','Frozen synthetic target families and common-epoch positions.'),
 'MISSION_NATIVE_AGREEMENT':('mission/NATIVE_REPLAY_CHECKS.json','Native Orekit numerical replay and step-refinement agreement.')}
for p in sorted(A.rglob('*')):
 if not p.is_file()or p.name=='ASSET_REGISTER.json':continue
 path=str(p.relative_to(ROOT));r=lookup.get(path)
 if r is None:r={'asset_id':p.stem,'path':path,'configuration':'VOLLEY-G5-ACR1','release':'ACR1-WEB-R1','status':'current'};records.append(r);lookup[path]=r
 r['sha256']=sha(p);r['release_commit']=None
 if p.suffix.lower()in ['.jpg','.png']:
  with Image.open(p)as image:r['dimensions_px']=list(image.size)
  if p.stem in sources:
   source,caption=sources[p.stem];r.update({'evidence_class':'computed result','role':'scientific figure','source_path':'validation/acr1/'+source,'source_sha256':sha(ROOT.parent/'validation/acr1'/source),'caption':caption,'alt_text':caption,'software':'frozen source-defined scientific plotting pipeline','camera':None,'scene':None,'evidence_link':'evidence.html'if not p.stem.startswith('MISSION')else'orbital-analysis.html'})
  if p.stem=='ACR1_social_preview':r.update({'evidence_class':'CAD-derived editorial composite','role':'1200x630 social preview','source_path':'assets/acr1/01_assembly_isometric.jpg','source_sha256':sha(A/'01_assembly_isometric.jpg'),'caption':'G5 ACR1 computational design study; unaltered accepted assembly render in an editorial card.','alt_text':'VOLLEY commanded CubeSat deployment computational design study, beside the ACR1 assembly render.','software':'Pillow 12.3.0; finalize_assets.py','camera':view['views'][0]['camera'],'scene':'VOLLEY_G5_ACR1_scientific_views.blend'})
# Exact supplemental figures and their native-source provenance.
for metadata in json.loads((A/'supplements/SUPPLEMENT_FIGURES.json').read_text())['assets']:
 key=metadata['path'].removeprefix('docs/');record=lookup[key];record.update(metadata)
for p in sorted((ROOT/'downloads').glob('*')):
 if p.is_file():records.append({'asset_id':p.stem,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'configuration':'VOLLEY-G5-ACR1','evidence_class':'source or academic document package','role':'offline download','release':'ACR1-WEB-R1','status':'current','caption':'Frozen academic bytes or a documented source-only web derivative; no numerical evidence changed.'})
for p in sorted((ROOT/'films').glob('*/FILM_MANIFEST.json')):
 d=json.loads(p.read_text());records.append({'asset_id':'film-'+p.parent.name,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'configuration':'VOLLEY-G5-ACR1','evidence_class':'source-driven editorial film; CAD renders, computed results and explicitly conceptual diagrams','role':d['title'],'dimensions_px':d['dimensions_px'],'duration_s':d['duration_s'],'caption':d['title'],'alt_text':d['title'],'transcript':str((p.parent/'transcript.json').relative_to(ROOT)),'captions':str((p.parent/'captions.vtt').relative_to(ROOT)),'scene':d['editable_source'],'software':d['software'],'source_pins':'visual-source/SOURCE_PINS.json','camera':'source-specific; original CAD cameras in VIEW_PROVENANCE.json','release':'ACR1-WEB-R1','status':'current'})
records=list({r['path']:r for r in records}.values())
register['external_academic_downloads']=json.loads((A/'EXTERNAL_ACADEMIC_DOWNLOADS.json').read_text())
register['assets']=records;register['reviewer']='Source identity, captions and recorded display checks.';register['retired_asset_groups']=[{'path':'assets/sequence/','status':'historical','configuration':'original Gen5; superseded for current ACR1 front door','evidence_route':'historical-index.html'},{'path':'assets/selected-feeder/','status':'historical/subsystem identity preserved','configuration':'FM08, not integrated ACR1','evidence_route':'historical-feeder-analysis.html'}]
register['academic_release_policy']={'edition':'ED1 citation-corrected final-year report and companion manuscript','release_cutoff':'2026-10-30 evening Asia/Kolkata','cutoff_state':'planned; not executed','thesis_policy':'Preserve the thesis edition as a fixed release; later research is versioned separately.','manuscript_status':'IEEE-formatted and unsubmitted'}
(A/'ASSET_REGISTER.json').write_text(json.dumps(normalize_registry(register),indent=2))
# Precise derivative source archive manifest: every archived file is unchanged.
archive=ROOT/'downloads/VOLLEY_G5_ACR1_editable_scene.zip'
with zipfile.ZipFile(archive)as z:
 archivefiles=[{'name':n,'sha256':hashlib.sha256(z.read(n)).hexdigest()}for n in z.namelist()]
(HERE/'SCENE_PACKAGE_MANIFEST.json').write_text(json.dumps({'path_base':'repository_root','member_path_base':'archive_root','archive_path':'docs/downloads/VOLLEY_G5_ACR1_editable_scene.zip','release_identity':'containing Git commit or release tag','package_sha256':sha(archive),'role':'web source-only derivative; frozen source files unchanged; rendered views served separately','original_archive_sha256':'a34a89c43e05fd59d3e7fe11501765534902b7ee71ddc67a94b3071ece3c1e5c','files':archivefiles},indent=2))
print('Finalized registered assets:',len(records));print('Social preview:',sha(A/'ACR1_social_preview.png'))
