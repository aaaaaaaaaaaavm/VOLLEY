"""Exact geometry containment/identity/separation proof plus final lock/flight checks."""
from pathlib import Path
import hashlib,json,time
import build_acr1 as b
ROOT=Path(__file__).resolve().parent;OUT=b.OUT;started=time.perf_counter();proofs=[];cases=[]
source={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in ['build_acr1.py','cradle_acr1.py','sled_latches.py','PARAMETERS.json','verify_motion.py','verify_final_refinement.py']}
baseline=json.loads((OUT/'MOTION_VERIFICATION_BASELINE_PALLET.json').read_text());assert baseline['all_sampled_cases_pass']
old=lambda name:b.Part.read(str(ROOT/'refinement_baseline'/name))
new_pallet=b.pallet()[0]['shape'];old_pallet=old('pallet.brep')
proofs.append({'proof':'Final pallet is a strict material subset of the143-case tested pallet','added_mm3':new_pallet.cut(old_pallet).Volume,'removed_mm3':old_pallet.cut(new_pallet).Volume,'pass':new_pallet.cut(old_pallet).Volume<1e-5})
closed=b.sled(200,False,pallet_locked=True);opened=b.sled(200,False,pallet_locked=False)
for q in closed:
 if q['name'].startswith('Pallet_bayonet_lock_'):
  previous=old(q['name']+'_locked.brep');delta=q['shape'].cut(previous).Volume+previous.cut(q['shape']).Volume
  proofs.append({'proof':'Closed lock geometry is identical: '+q['name'],'symmetric_difference_mm3':delta,'pass':delta<1e-5})
chassis=next(q['shape']for q in closed if q['name']=='Sled_connected_chassis');previous=old('Sled_connected_chassis_locked.brep');added=chassis.cut(previous)
proofs.append({'proof':'Web-bore reduction only restores chassis material','removed_mm3':previous.cut(chassis).Volume,'added_mm3':added.Volume,'pass':previous.cut(chassis).Volume<1e-5})
fixed=b.foundation()+b.track()+b.winding()+b.bank_mounts()+b.release_cams()
stored=[q for side in [-1,1]for level in range(6)for q in b.cell(side,level)]
occupied=[q for q in stored if q['name']!='Bank_south_L5_Stored_3U'];park=b.cradle(190,True,grips_open=True)
bb=added.BoundBox;sweep=b.box(bb.XLength+1510,bb.YLength,bb.ZLength,bb.XMin,bb.YMin,bb.ZMin)
proxy=b.row('Restored_web_continuous_full_travel_envelope',sweep)
result=b.audit(fixed+stored+park+[proxy],{proxy['name']})
proofs.append({'proof':'A conservative box containing every restored web point over all1510mm carrier translation has no fixed-world collision','envelope_bounds_mm':[sweep.BoundBox.XMin,sweep.BoundBox.XMax,sweep.BoundBox.YMin,sweep.BoundBox.YMax,sweep.BoundBox.ZMin,sweep.BoundBox.ZMax],'pass':result['pass_all'],'audit':result})
# Any open-lock material newly added by the shorter stroke lies below Z35.
# Split the closest lift pose at that plane. Every lower solid is separated
# in XY; every upper point remains above it throughout all positive-Z travel.
changes=[]
for q in opened:
 if q['name'].startswith('Pallet_bayonet_lock_'):
  diff=q['shape'].cut(old(q['name']+'_open.brep'))
  if diff.Volume>1e-5:changes.append(diff)
changes.append(added)
maxz=max(s.BoundBox.ZMax for s in changes)
closest=b.pallet(46,lifted=True)+[q for q in b.cradle(46,False)if q['group']not in ['lift_fixed','lift_drive','lift_catalog']]+[b.payload('Lowest_captured_3U',b.XA,0,46)]
slab=b.box(5000,2000,maxz+1000,-1000,-1000,-1000);overlaps=[];tested=0
for q in closest:
 lower=q['shape'].common(slab)
 for solid in lower.Solids:
  a=solid.BoundBox
  for change in changes:
   c=change.BoundBox;tested+=1
   if min(a.XMax,c.XMax)-max(a.XMin,c.XMin)>1e-8 and min(a.YMax,c.YMax)-max(a.YMin,c.YMin)>1e-8:overlaps.append(q['name'])
proofs.append({'proof':'New open-lock material cannot meet lifted pallet/payload/carriage at any Z>=46: lower regions are XY-disjoint, upper regions stay aboveZ35','added_lock_max_z_mm':maxz,'tested_lower_region_pairs':tested,'XY_overlaps':overlaps,'pass':not overlaps})
def check(label,items,names,**kw):
 r=b.audit(items,set(names));r.update(case=label,evidence_source_sha256=source,**kw);cases.append(r);print('CASE',label,kw,'hits',len(r['interferences']),flush=True)
cr=b.cradle(46,False);pallet=b.pallet();sat=b.payload('Seated_3U',b.XA,0,46)
for lift,turn in [(0,0),(4,0),(8,0),(12,0),(12,30),(12,60),(12,90)]:
 moving=b.sled(200,False,pallet_locked=False,pallet_lock_lift=lift,pallet_lock_turn=turn)
 check('final12mm_lock_insertion_and_rotation',fixed+occupied+moving+cr+pallet+[sat],[q['name']for q in moving if q['name']=='Sled_connected_chassis'or q['name'].startswith('Pallet_bayonet_lock_')]+[q['name']for q in pallet],pin_lift_mm=lift,bayonet_turn_deg=turn)
carrier=b.sled(1500,False)+b.pallet(46,1500)
for travel in [0,25,50,75,90,100,110,125,150,250,400,600]:
 escaping=b.payload('Escaping_3U',1564+travel,0,46)
 check('payload_departure_over_retained_pallet',fixed+occupied+park+carrier+[escaping],[escaping['name']],payload_relative_advance_mm=travel)
assert source=={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in source},'Final source changed during refinement verification'
passed=all(p['pass']for p in proofs)and all(c['pass_all']for c in cases)
result={'configuration_id':b.P['configuration_id'],'source_sha256':source,'baseline_report':'MOTION_VERIFICATION_BASELINE_PALLET.json','baseline_source_sha256':baseline['source_sha256'],'baseline_case_count':baseline['case_count'],'final_native_case_count':len(cases),'proofs':proofs,'final_native_cases':cases,'all_refinement_checks_pass':passed,'elapsed_s':time.perf_counter()-started,'boundary':'Exact material containment,rigid-part identity and conservative continuous separation carry135 unchanged-motion baseline cases to the final bounded refinement;8 old lock-travel cases are superseded;new12mm lock path and0..600mm payload departure are directly audited. No loaded/flight qualification.'}
(OUT/'FINAL_REFINEMENT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
carried=[c for c in baseline['cases']if c['case']!='pallet_capture_before_grip_release']
combined={**baseline,'source_sha256':source,'baseline_source_sha256':baseline['source_sha256'],'case_count':len(carried)+len(cases),'carried_case_count':len(carried),'superseded_lock_case_count':baseline['case_count']-len(carried),'baseline_native_case_count':baseline['case_count'],'final_native_case_count':len(cases),'failed_case_count':sum(not c['pass_all']for c in cases)+(0 if all(p['pass']for p in proofs)else 1),'all_sampled_cases_pass':passed,'cases':[{**c,'evidence_source_sha256':baseline['source_sha256'],'carried_by':'FINAL_REFINEMENT_VERIFICATION.json exact containment/identity/separation proofs'}for c in carried]+cases,'refinement_proof_file':'FINAL_REFINEMENT_VERIFICATION.json','boundary':result['boundary']}
(OUT/'MOTION_VERIFICATION.json').write_text(json.dumps(combined,indent=2)+'\n')
print('DONE_REFINEMENT',passed,len(cases),flush=True)
