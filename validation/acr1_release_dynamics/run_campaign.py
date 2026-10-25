"""Bounded refinement matrix; logs each native run and keeps failed cases."""
from pathlib import Path
import json,time
from release_model import run,CASES

HERE=Path(__file__).resolve().parent
plan=[]
for c in CASES:
    for step in [100,50,25]:plan.append((c,step,100,'Newton',1e6,2000,'box'))
# Finer nominal and adverse-geometry witnesses.
for name in ['aligned','yaw','half_keeper']:
    c=next(c for c in CASES if c['id']==name)
    plan.append((c,12.5,100,'Newton',1e6,2000,'box'))
# Solver/budget and mathematically equivalent contact-surface partitions.
for name in ['aligned','half_keeper']:
    c=next(c for c in CASES if c['id']==name)
    plan.extend([(c,25,200,'Newton',1e6,2000,'box'),(c,25,200,'CG',1e6,2000,'box'),(c,25,100,'Newton',1e6,2000,'split')])
# Contact-model sensitivities are not calibrated material properties.
for k,b in [(1e5,632.4555320336759),(1e7,6324.555320336759),(1e6,0),(1e6,400)]:
    c=next(c for c in CASES if c['id']=='aligned')
    plan.append((c,25,100,'Newton',k,b,'box'))
for mu in [0,.3]:
    c=dict(next(c for c in CASES if c['id']=='half_keeper'));c['mu']=mu;c['id']=f'half_keeper_mu{mu:g}'
    plan.append((c,25,100,'Newton',1e6,2000,'box'))
records=[]
for i,(c,step,it,solver,k,b,representation) in enumerate(plan):
    started=time.monotonic()
    try:
        r=run(c,step/1e6,it,solver,k,b,representation)
        records.append(r)
        print(i+1,len(plan),c['id'],step,solver,it,k,b,representation,'vx',r['payload_final_velocity_m_s'][0],'omega',r['payload_final_omega_deg_s'],'wall',time.monotonic()-started,flush=True)
    except Exception as e:
        records.append({'case':c,'dt_s':step/1e6,'status':'RUN_FAILED','error':repr(e)})
        print(i+1,'RUN_FAILED',repr(e),flush=True)
    (HERE/'CAMPAIGN.json').write_text(json.dumps({'planned_runs':len(plan),'completed_records':records},indent=2)+'\n')
