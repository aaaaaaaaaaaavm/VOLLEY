"""Create a hash-verified, compact reviewer package from the completed FCE13 study."""
from pathlib import Path
import datetime,hashlib,json,zipfile
H=Path(__file__).resolve().parent
NAME='BB57_FCE13_CONTACT_FAILURE_BOUND_20261022'
roots=['baseline','geometry_guarded','references','runs']
files=[p for p in H.iterdir() if p.is_file() and p.suffix in ['.cpp','.py','.md','.json','.log','.png','.pdf','.svg','.csv','.patch'] and p.name not in ['PACKAGE_MANIFEST.json']]
files.append(H/'CMakeLists.txt')
for root in roots:files += [p for p in (H/root).rglob('*') if p.is_file()]
for name in ['feeder_probe','feeder_bb_probe','feeder_box_probe']:files.append(H/'build'/name)
files=sorted(set(files))
for p,digest in [(H/name,digest) for name,digest in json.loads((H/'BASELINE_HASHES.json').read_text())['sha256'].items()]:assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,p
for i in ['P3-250','W3-250','B3-250','B3-125','X3-250','X3-125']:
 r=json.loads((H/'runs'/(i+'.record.json')).read_text())
 for name,digest in r['output_sha256'].items():assert hashlib.sha256((H/'runs'/name).read_bytes()).hexdigest()==digest,(i,name)
 for key,name in [('source_sha256','feeder_probe.cpp' if i.startswith(('P','W')) else 'feeder_bb_probe.cpp' if i.startswith('B') else 'feeder_box_probe.cpp'),('executable_sha256','build/feeder_probe' if i.startswith(('P','W')) else 'build/feeder_bb_probe' if i.startswith('B') else 'build/feeder_box_probe')]:assert hashlib.sha256((H/name).read_bytes()).hexdigest()==r[key],(i,key)
manifest={'package':NAME,'created_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'final-state convergence still fails retained0.05mm/0.05deg criteria; no correction adopted','applicability':'FM06-R1 contact subcycle only; no FM07-R6 validity, feeder choice, force rating or outside expert review','files':{str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}}
mp=H/'PACKAGE_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2)+'\n');files.append(mp)
checks=H/'SHA256SUMS';checks.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(H))+'\n' for p in sorted(files)));files.append(checks)
zp=H/(NAME+'.zip')
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,NAME+'/'+str(p.relative_to(H)))
with zipfile.ZipFile(zp) as z:assert z.testzip() is None
sha=hashlib.sha256(zp.read_bytes()).hexdigest();(H/(zp.name+'.sha256')).write_text(sha+'  '+zp.name+'\n')
print(json.dumps({'archive':str(zp),'bytes':zp.stat().st_size,'files':len(files),'sha256':sha,'verified':'original184baseline hashes, all completed output/source/executable hashes, zip CRC'},indent=2))
