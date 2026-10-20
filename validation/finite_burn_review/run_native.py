"""Capture actual Java/Orekit runs; bounded parallel independent jobs."""
from pathlib import Path
import csv,json,os,subprocess,concurrent.futures
H=Path(__file__).resolve().parent
CP=os.environ.get('OREKIT_CLASSPATH',str(H/'jars/*'))
OUT=H/'native';OUT.mkdir(exist_ok=True)
jobs=[]
for p in sorted((H/'release').glob('*.csv')):
    if p.name.endswith('_trajectory.csv'): continue
    jobs.append(dict(name=p.stem,source=p.name,step=60,force=1,shot=1,dx=0,category='nominal'))
for case in ['4_spring_10kg','4_volley_3_6_10kg','12_spring_20kg','12_volley_3_6_20kg']:
    src=case+'_f0.35_h60.csv'
    jobs.append(dict(name=case+'_refine_native30',source=src,step=30,force=1,shot=1,dx=0,category='step_refinement'))
    for label,force,shot,dx in [('force_minus_0p1pct',.999,1,0),('force_plus_0p1pct',1.001,1,0),('shot_minus_0p1pct',1,.999,0),('shot_plus_0p1pct',1,1.001,0),('initial_x_minus10m',1,1,-10),('initial_x_plus10m',1,1,10)]:
        jobs.append(dict(name=case+'_'+label,source=src,step=60,force=force,shot=shot,dx=dx,category='deterministic_sensitivity'))
def worker(j):
    cmd=['java','-cp',CP,str(H/'FiniteReplay.java'),str(H/'release'/j['source']),str(OUT/j['name']),str(j['step']),str(j['force']),str(j['shot']),str(j['dx'])]
    r=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
    (OUT/(j['name']+'.log')).write_text(r.stdout+r.stderr)
    result={**j,'command':cmd,'exit_code':r.returncode}
    print(j['name'],r.returncode,flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(worker,jobs))
(OUT/'RUNS.json').write_text(json.dumps(results,indent=2)+'\n')
if any(r['exit_code'] for r in results): raise SystemExit('A native case failed; see retained log')
