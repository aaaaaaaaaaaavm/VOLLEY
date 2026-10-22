"""Reproduce selected FCE13 numerical diagnoses; native SI command arguments are FCE12 unchanged."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,time
H=Path(__file__).resolve().parent
P=Path('/workspace/volley-work/2026-10-21-completion/feeder-contact-correction')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(case):
    name,size,dt,it,warm,solver,mu=case
    results_dir=Path(os.environ.get('FCE_RESULTS_DIR',str(H/'runs')))
    out=results_dir/f'{name}.csv';out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists() or out.with_suffix('.record.json').exists():raise RuntimeError('immutable completed run exists: '+name)
    source=H/os.environ.get('FCE_SOURCE','feeder_probe.cpp');exe=H/'build'/os.environ.get('FCE_EXE','feeder_probe')
    cmd=[str(exe),str(H/'geometry_guarded'/size),str(out),str(1.33 if size=='1U' else 4.),str(mu),'0','0',str(dt),'100','5','0',str(it),'10','none','0.1']
    env={**os.environ,'OMP_NUM_THREADS':'1','FCE_WARM':str(warm),'FCE_SOLVER':solver}
    record={'id':name,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CAD':'FM06-R1, not FM07-R6','command':cmd,'environment_overrides':{k:env[k] for k in ['OMP_NUM_THREADS','FCE_WARM','FCE_SOLVER']},'source_sha256':sha(source),'executable_sha256':sha(exe)}
    out.with_suffix('.started.json').write_text(json.dumps(record,indent=2)+'\n')
    start=time.monotonic()
    with out.with_suffix('.log').open('w') as f:result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=1800)
    record.update(exit_code=result.returncode,wall_s=time.monotonic()-start)
    record['output_sha256']={p.name:sha(p) for p in sorted(out.parent.glob(name+'.*'))}
    mp=Path(str(out)+'.metrics.json');record['metrics']=json.loads(mp.read_text()) if mp.exists() else None
    sp=Path(str(out)+'.solver.json');record['solver_metrics']=json.loads(sp.read_text()) if sp.exists() else None
    out.with_suffix('.record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(name,record['exit_code'],round(record['wall_s'],3),record['solver_metrics'],flush=True)
    assert record['source_sha256']==sha(source) and record['executable_sha256']==sha(exe)
    return record
if __name__=='__main__':
    cases=[tuple(x) for x in json.loads(sys.argv[1])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))
