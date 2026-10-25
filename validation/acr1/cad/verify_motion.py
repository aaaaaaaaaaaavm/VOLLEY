"""Installed ACR1 native BRep motion checks with one captive shuttle pallet."""
from pathlib import Path
import hashlib,json,time
import build_acr1 as b
ROOT=Path(__file__).resolve().parent;cases=[];started=time.perf_counter()
SOURCES=['build_acr1.py','cradle_acr1.py','sled_latches.py','PARAMETERS.json']
SOURCE={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in SOURCES}
def shifted(q,dx=0,dy=0,dz=0):
 out={**q,'shape':b.translated(q['shape'],dx,dy,dz)}
 if 'collision_shapes'in q:out['collision_shapes']=[b.translated(s,dx,dy,dz)for s in q['collision_shapes']]
 return out
def save():
 result={'configuration_id':b.P['configuration_id'],'source_sha256':SOURCE,'case_count':len(cases),'failed_case_count':sum(not x['pass_all']for x in cases),'all_sampled_cases_pass':all(x['pass_all']for x in cases),'cases':cases,'elapsed_s':time.perf_counter()-started,'boundary':'Changed-part sampled nominal native BRep geometry against all12 installed cells;not continuous collision detection or loaded/contact/flight qualification;no horizontal pallet withdrawal.'}
 (b.OUT/'MOTION_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
def check(label,items,names,**kw):
 result=b.audit(items,set(names));result.update(case=label,**kw);cases.append(result);save();print('CASE',label,kw,'hits',len(result['interferences']),flush=True)
fixed=b.foundation()+b.track()+b.winding()+b.bank_mounts()+b.release_cams()
stored=[q for side in [-1,1]for level in range(6)for q in b.cell(side,level)]
carrier_open=b.sled(200,True,pallet_locked=False)
carrier_locked=b.sled(200,False,pallet_locked=True)
template=b.cradle(46,False)
static=[q for q in template if q['group']in ['lift_fixed','lift_drive','lift_catalog']]
dynamic=[q for q in template if q not in static]
occupied=[q for q in stored if q['name']!='Bank_south_L5_Stored_3U']
# Payload,pallet and lift move together; the cassette structures remain installed.
for floor in sorted(set([46,50,54,60,90,120,150,164,180,190,210,240,270,300,310,340,370,400,430,440,470,500,530,560,570,600,630,660,690,700,730,760,790,820,830])):
 moving=[shifted(q,dz=floor-46)for q in dynamic]+b.pallet(floor,lifted=True)+[b.payload('Captured_3U',b.XA,0,floor)]
 check('captured_vertical_transit',fixed+occupied+carrier_open+static+moving,[q['name']for q in moving],floor_z_mm=floor)
# Each feed uses the actual incoming-side keeper pose and the one real pallet.
for side in [-1,1]:
 for level in range(6):
  floor=180+130*level;prefix=f'Bank_{"south"if side<0 else"north"}_L{level}_'
  others=[q for q in stored if not q['name'].startswith(prefix)]
  cradle=b.cradle(floor,False,incoming_side=side);pallet=b.pallet(floor,lifted=True)
  for advance in [0,62.5,125,187.5,250]:
   active=b.cell(side,level,advance,True)
   names=[q['name']for q in active if q['group']in ['cell_pusher','cell_gate','payload']]+[q['name']for q in cradle if q['group']not in ['lift_fixed','lift_drive','lift_catalog']]+[q['name']for q in pallet]
   check('installed_cell_feed',fixed+others+active+carrier_open+cradle+pallet,names,side=side,level=level,feed_mm=advance)
# Capture before release: land,insert,turn,open keepers,then retract lift grips.
pallet=b.pallet(46);sat=b.payload('Seated_3U',b.XA,0,46)
for lift,turn in [(0,0),(4,0),(8,0),(12,0),(12,30),(12,60),(12,90)]:
 moving=b.sled(200,False,pallet_locked=False,pallet_lock_lift=lift,pallet_lock_turn=turn)
 cr=b.cradle(46,False)
 check('pallet_capture_before_grip_release',fixed+occupied+moving+cr+pallet+[sat],[q['name']for q in moving+cr+pallet],pin_lift_mm=lift,bayonet_turn_deg=turn)
for keeper in [0,30,60,90,110]:
 cr=b.cradle(46,keeper)
 check('keeper_upward_retraction',fixed+occupied+carrier_locked+cr+pallet+[sat],[q['name']for q in cr],keeper_stroke_mm=keeper)
for grip in [0,6,13,20,26]:
 cr=b.cradle(46,True,grips_open=grip)
 check('pallet_grip_release_after_sled_capture',fixed+occupied+carrier_locked+cr+pallet+[sat],[q['name']for q in cr],grip_withdraw_mm=grip)
# The pallet stays on the sled while the empty endframe/keepers rise clear.
for floor in [46,50,54,60,90,120,150,164,180,190]:
 cr=b.cradle(floor,True,grips_open=True)
 check('lift_rise_from_retained_pallet',fixed+occupied+carrier_locked+cr+pallet+[sat],[q['name']for q in cr],floor_z_mm=floor)
# The full retained pallet is in the moving carrier mass and geometry in each shot pose.
park=b.cradle(190,True,grips_open=True)
for aft in [200,250,350,500,750,1000,1250,1445,1450,1455,1465,1475,1485,1495,1500,1540,1580,1620,1660,1710]:
 moving=b.sled(aft,False,pallet_locked=True)+b.pallet(46,aft)
 if aft<1500:moving+=[b.payload('Accelerating_3U',aft+64,0,46)]
 check('carrier_pallet_launch_arrest_return_path',fixed+occupied+park+moving,[q['name']for q in moving],carrier_aft_x_mm=aft)
# The released spacecraft crosses the complete retained pallet without a front stop.
carrier=b.sled(1500,False)+b.pallet(46,1500)
for travel in [0,25,50,75,90,100,110,125,150,250,400,600]:
 escaping=b.payload('Escaping_3U',1564+travel,0,46)
 check('payload_departure_over_retained_pallet',fixed+occupied+park+carrier+[escaping],[escaping['name']],payload_relative_advance_mm=travel)
assert SOURCE=={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in SOURCES},'Controlled source changed during verification'
save();print('DONE',len(cases),'failed',sum(not x['pass_all']for x in cases),flush=True)
