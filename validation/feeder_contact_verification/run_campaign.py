"""FCE12 guarded volumetric contact refinement, with immutable input identities."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,time
H=Path(__file__).resolve().parent;O=H/'reproduced_runs';O.mkdir(exist_ok=True)
exe=H/'build/feeder_mm'
cases=[]
def add(size,m,dt=.0005,mu=.1,g=0,it=2000,mode='none',label=''):
    cases.append(dict(size=size,mass_kg=m,dt_s=dt,mu=mu,g=g,iterations=it,mode=mode,label=label))
for size,m in [('1U',1.33),('3U',4.)]:
    for dt in [.0005,.00025,.000125]:add(size,m,dt,label='time_refinement')
add('3U',4.,.00025,it=4000,label='iteration_refinement')
for mu in [0,.3]:add('3U',4.,mu=mu,label='friction_sensitivity')
add('3U',6.,g=9.80665,label='rigid_ground_adverse_mass')
for mode in ['jam','stuck_pin']:add('3U',4.,mode=mode,label='deliberate_'+mode)
for i,r in enumerate(cases):r['case_id']=f'FCE12-{i+1:02d}'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
identity={'revision':'FCE12','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CAD':'FM06-R1 unchanged','representation':'Nine disjoint convex payload support meshes (no hull simplification) plus exact rectilinear collision-domain boxes with12mm X-guard to include the actual cassette guide walls per size. Full CAD mass/inertia retained. Only payload/mechanism contact active; full-state1ms40rad/s ideal PD/prismatic guides,100/20/50/5N assumed drive caps.','internal_units':{'length':'mm','mass':'kg','time':'s','force':'mN','output':'SI'},'envelope_m':5e-6,'safe_margin_m':0,'protocol_sha256':sha(H/'PROTOCOL.json'),'source_sha256':sha(H/'feeder_mm.cpp'),'executable_sha256':sha(exe),'partitions_sha256':{p.name:sha(p) for p in [H/'geometry_guarded/PAYLOAD_PARTITION.json',H/'geometry_guarded/MECHANISM_PARTITION.json']},'cases':cases}
(O/'INPUTS.json').write_text(json.dumps(identity,indent=2)+'\n')
def run(r):
    p=O/(r['case_id']+'.csv')
    cmd=[str(exe),str(H/'geometry_guarded'/r['size']),str(p)]+[str(v) for v in [r['mass_kg'],r['mu'],0,r['g'],r['dt_s'],100,5,0,r['iterations'],10,r['mode'],.1]]
    start=time.monotonic()
    with (O/(r['case_id']+'.log')).open('w') as f:
        proc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'1'},timeout=1200)
    record={**r,'exit_code':proc.returncode,'wall_s':time.monotonic()-start,'command':cmd}
    metrics=Path(str(p)+'.metrics.json')
    if metrics.exists():record['metrics']=json.loads(metrics.read_text())
    record['hashes']={q.name:sha(q) for q in [p,metrics,O/(r['case_id']+'.log')] if q.exists()}
    (O/(r['case_id']+'.record.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(r['case_id'],r['size'],r['label'],proc.returncode,round(record['wall_s'],2),flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,cases))
assert sha(exe)==identity['executable_sha256'] and sha(H/'feeder_mm.cpp')==identity['source_sha256']
(O/'RUNS.json').write_text(json.dumps({'revision':'FCE12','cases':results,'scope':'Native numerical contact subcycle, not full launch/reset or hardware reliability.'},indent=2)+'\n')
