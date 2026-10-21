"""FCE08 verified-input native campaign; no failure is converted to a pass."""
from pathlib import Path
import concurrent.futures,subprocess,json,hashlib,time,datetime,os
H=Path(__file__).resolve().parent;O=H/'campaign_v2';O.mkdir(exist_ok=True);exe=H/'build/feeder_surface';rows=[]
def add(size,m,dt=.0005,mu=.1,g=0,cap=100,iterations=2000,mode='none',guard=.1,label=''):
 rows.append(dict(size=size,mass_kg=m,dt_s=dt,friction=mu,restitution=0,gravity_m_s2=g,drive_cap_N=cap,guide_drag_N=5,yaw_deg=0,iterations=iterations,feed_time_s=10,mode=mode,guard_mm=guard,label=label))
for size,m in [('1U',1.33),('3U',4.)]:
 for dt in [.0005,.00025,.000125]:add(size,m,dt=dt,label='time_refinement')
add('3U',4.,dt=.00025,iterations=4000,label='iteration_refinement')
add('3U',6.,g=9.80665,label='rigid_ground_adverse_mass')
for mu in [0,.3]:add('3U',4.,mu=mu,label='friction_sensitivity')
for mode in ['jam','stuck_pin']:add('3U',4.,mode=mode,label='deliberate_'+mode)
for i,r in enumerate(rows):r['case_id']=f'FCE08-{i+1:02d}'
identity={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision':'FCE08','CAD':'FM06-R1','solver':'Chrono10 PSOR;1ms mass-scaled40rad/s critically damped PD; full-state assumed measurement; ideal prismatic guides','resistance_law':'R*tanh(v/0.01m/s),R=5N. Provisional smooth surrogate, no measured Coulomb/stiction claim.','geometry':'Single closed outward-oriented welded CAD mesh for every actual component; deflection5um, numerical skin radius10um. Only payload-to-mechanism contact active. No overlapping collision constituents.','executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'cpp_sha256':hashlib.sha256((H/'feeder_surface.cpp').read_bytes()).hexdigest(),'CAD_sha256':hashlib.sha256((H.parent/'mechanism.py').read_bytes()).hexdigest(),'surface_audit_sha256':hashlib.sha256((H.parent/'contact_geometry_surfaces/SURFACE_AUDIT.json').read_bytes()).hexdigest(),'cases':rows}
(O/'INPUTS.json').write_text(json.dumps(identity,indent=2)+'\n')
def run(r):
 n=r['case_id'];out=O/(n+'.csv');cmd=[str(exe),str(H.parent/'contact_geometry_surfaces'/r['size']),str(out)]+[str(r[k]) for k in ['mass_kg','friction','restitution','gravity_m_s2','dt_s','drive_cap_N','guide_drag_N','yaw_deg','iterations','feed_time_s','mode','guard_mm']]
 start=time.monotonic()
 with (O/(n+'.log')).open('w') as f:
  p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'1'},timeout=3000)
 rec={**r,'exit_code':p.returncode,'wall_s':time.monotonic()-start,'command':cmd,'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [out,O/(n+'.log'),Path(str(out)+'.metrics.json')] if p.exists()}}
 if Path(str(out)+'.metrics.json').exists():rec['native_metrics']=json.loads(Path(str(out)+'.metrics.json').read_text())
 (O/(n+'.record.json')).write_text(json.dumps(rec,indent=2)+'\n');print(n,r['size'],r['label'],p.returncode,round(rec['wall_s'],2),flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,rows))
assert hashlib.sha256(exe.read_bytes()).hexdigest()==identity['executable_sha256'];assert hashlib.sha256((H/'feeder_surface.cpp').read_bytes()).hexdigest()==identity['cpp_sha256']
(O/'RUNS.json').write_text(json.dumps({'revision':'FCE08','cases':results,'boundary':'Numerical rigid-contact study, not hardware tests or installed actuator/sensor validation. Sequence completion alone does not establish numerical convergence, loaded fit, delivery precision, full launcher reset, reliability or flight approval.'},indent=2)+'\n');print('Finished',len(results),'native cases',flush=True)
