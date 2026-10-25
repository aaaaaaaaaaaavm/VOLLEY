"""Changed-part native geometry checks for the actual integrated ACR1 assembly."""
from pathlib import Path
import hashlib,json,time
import build_acr1 as b
ROOT=Path(__file__).resolve().parent;cases=[];started=time.perf_counter()
SOURCE={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'build_acr1.py',ROOT/'cradle_acr1.py',ROOT/'sled_latches.py',ROOT/'PARAMETERS.json']}
def shifted(q,dx=0,dy=0,dz=0):
    out={**q,'shape':b.translated(q['shape'],dx,dy,dz)}
    if 'collision_shapes'in q:out['collision_shapes']=[b.translated(s,dx,dy,dz) for s in q['collision_shapes']]
    return out
def save():
    r={'configuration_id':b.P['configuration_id'],'source_sha256':SOURCE,'case_count':len(cases),'failed_case_count':sum(not x['pass_all'] for x in cases),'all_sampled_cases_pass':all(x['pass_all']for x in cases),'cases':cases,'elapsed_s':time.perf_counter()-started,'boundary':'Changed-part sampled nominal BRep geometry; pure axis-aligned box intersections exact, general shapes use native common volume. No loaded/contact/flight qualification.'}
    (b.OUT/'MOTION_VERIFICATION.json').write_text(json.dumps(r,indent=2)+'\n')
def check(label,items,names,**kw):
    r=b.audit(items,set(names));r.update(case=label,**kw);cases.append(r);save()
    print('CASE',label,kw,'hits',len(r['interferences']),flush=True)
    return r['pass_all']

# A highest-level south-cell transfer, then all twelve docking levels and directions.
fixed=b.foundation()+b.track()+b.winding()+b.bank_mounts()+b.brake()+b.release_cams()
stored=[q for side in [-1,1]for lev in range(6)for q in b.cell(side,lev)]
carrier_open=b.sled(200,True,False);carrier_closed=b.sled(200,False,False)
template=b.cradle(46,False,0)
lift_static=[q for q in template if q['group']in ['lift_fixed','lift_drive','lift_catalog']]
lift_dynamic=[q for q in template if q not in lift_static]
south_prefix='Bank_south_L5_'
occupied=[q for q in stored if not(q['name']==south_prefix+'Stored_3U')]

# The cradle and captured payload undergo the whole vertical range. Actual occupied
# cassettes remain installed; the selected spacecraft has left its original cell.
for floor in sorted(set([46,60,90,120,150,164,180,190,210,240,270,300,310,340,370,400,430,440,470,500,530,560,570,600,630,660,690,700,730,760,790,820,830])):
    dynamic=[shifted(q,dz=floor-46)for q in lift_dynamic]
    sat=b.payload('Captured_3U',b.XA,0,floor)
    check('captured_vertical_transit',fixed+occupied+carrier_open+lift_static+dynamic+[sat],[q['name']for q in dynamic]+[sat['name']],floor_z_mm=floor)

# Every occupied-cell interface has both the release-side storage keeper and the
# incoming cradle keeper in their open, actually modeled poses.
for side in [-1,1]:
 for lev in range(6):
    floor=180+130*lev;prefix=f'Bank_{"south"if side<0 else"north"}_L{lev}_'
    others=[q for q in stored if not q['name'].startswith(prefix)]
    cradle=b.cradle(floor,False,0,side)
    for u in [0,62.5,125,187.5,250]:
        active=b.cell(side,lev,u,True,False)
        changed=[q['name']for q in active if q['group']in ['cell_pusher','cell_gate','payload']]
        changed += [q['name']for q in cradle if q['group']not in ['lift_fixed','lift_drive','lift_catalog']]
        check('installed_cell_feed',fixed+others+active+carrier_open+cradle,changed,side=side,level=lev,feed_mm=u)

# Load transfer and withdrawal use the captured spacecraft on the sled, not a
# spacecraft translated with the withdrawing floor. Three millimetres of lowering
# gives a physical load-transfer gap before the comb moves horizontally.
for floor,withdraw,label in [(46,0,'seated'),(45,0,'transfer_lowering'),(44,0,'transfer_lowering'),(43,0,'handoff')]+[(43,u,'fork_withdraw')for u in [30,60,90,120,150]]+[(z,150,'withdrawn_rise')for z in [60,90,120,150,158]]+[(158,u,'fork_reextend')for u in [120,90,60,30,0]]+[(z,0,'above_sled_park')for z in [164,174,184,190]]:
    cr=b.cradle(floor,True,withdraw)
    sat=b.payload('Seated_3U',b.XA,0,46)
    changed=[q['name']for q in cr if q['group']not in ['lift_fixed','lift_drive','lift_catalog']]
    check(label,fixed+occupied+carrier_closed+cr+[sat],changed,floor_z_mm=floor,withdraw_mm=withdraw)

# The full carrier, wheels, magnet arrays, latches and conductive fin traverse the
# powered and arrest path against the parked receiver and all twelve bank structures.
park=b.cradle(190,True,0)
for aft in [200,250,350,500,750,1000,1250,1445,1450,1455,1465,1475,1485,1495,1500,1540,1580,1620,1660,1710]:
    moving=b.sled(aft,False,aft>=1500)
    others=fixed+occupied+park
    # Payload follows only until commanded release, after which its flight is not
    # replaced by a payload rigidly attached to the arresting sled.
    if aft<1500:moving=moving+[b.payload('Accelerating_3U',aft+64,0,46)]
    check('carrier_powered_and_arrest_translation',others+moving,[q['name']for q in moving],carrier_aft_x_mm=aft)

assert SOURCE=={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [ROOT/'build_acr1.py',ROOT/'cradle_acr1.py',ROOT/'sled_latches.py',ROOT/'PARAMETERS.json']},'Controlled source changed during verification'
save();print('DONE',len(cases),'failed',sum(not x['pass_all']for x in cases),flush=True)
