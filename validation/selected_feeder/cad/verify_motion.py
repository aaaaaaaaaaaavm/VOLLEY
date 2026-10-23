"""Native BRep phase verification for FM08-R3. No dynamic/continuous certification."""
from pathlib import Path
import json,time,hashlib,itertools
import build_selected as b
O=b.O;started=time.perf_counter();cases=[]
SOURCE_HASH=hashlib.sha256(Path(b.__file__).read_bytes()).hexdigest()
def record(label,items,**kwargs):
 cid=kwargs.get('cell')
 dynamic={q['name'] for q in items if (q['name'].startswith(cid+'__') and q['role'] in ['moving','payload','gate','latch']) or q['name'].startswith('Receiver__Y_capture_tab')}
 hits=[];tested=0
 for a,bb in itertools.combinations(items,2):
  if a['name'] not in dynamic and bb['name'] not in dynamic:continue
  if not a['shape'].BoundBox.intersect(bb['shape'].BoundBox):continue
  tested+=1;vol=a['shape'].common(bb['shape']).Volume
  if vol>1e-5:hits.append({'a':a['name'],'b':bb['name'],'volume_mm3':vol})
 r={'pass':not hits,'positive_volume_interferences':hits,'tested_bounding_box_pairs':tested,'pair_scope':'Every changed activecell part/receivercapturetab against completeassembly;unchangedpartpairsverifiedin5fullcaptureaudits'}
 r.update({'case':label,**kwargs});cases.append(r)
 print(label,kwargs,'hits',len(r['positive_volume_interferences']),r['positive_volume_interferences'],flush=True)
 return r
# Four installed cells at each local stroke station,allothercellspresent.
for cid,fmt,x,side in b.CELLS:
 for u in [0,50,100,150,200]:
  pp=b.assembly(cid,u,'transfer',False,fmt,x)
  record('installed_feed',pp,cell=cid,feed_mm=u)
 # Payloadheldbyreceiver;thepush-onlyframe returnswithoutpayloadreturn.
 for u in [200,150,100,50,0]:
  pp=b.assembly(cid,u,'return',False,fmt,x)
  record('captured_payload_fork_return',pp,cell=cid,feed_mm=u)
# Full900mmcommonindex:pathincludesallcassettesandallreleasedstationpins.
for fmt,cid in [('1U','CellA_1U'),('3U','CellB_3U')]:
 pp=b.assembly(cid,0,'index',False,fmt,0)
 static=[q for q in pp if not q['name'].startswith('Receiver__')]
 moving=[q for q in pp if q['name'].startswith('Receiver__')]
 for x in range(0,901,25):
  dyn=[{**q,'shape':q['shape'].copy()} for q in moving]
  for q in dyn:q['shape'].translate(b.V(x,0,0))
  # Checkdynamicvsstatic only; static/state-constantinternalpairschecked elsewhere.
  hits=[];tested=0
  for a in dyn:
   for bb in static:
    if not a['shape'].BoundBox.intersect(bb['shape'].BoundBox):continue
    tested+=1;vol=a['shape'].common(bb['shape']).Volume
    if vol>1e-5:hits.append({'a':a['name'],'b':bb['name'],'volume_mm3':vol})
  r={'case':'receiver_index','format':fmt,'index_X_mm':x,'tested_bounding_box_pairs':tested,'positive_volume_interferences':hits,'pass':not hits};cases.append(r)
  print('index',fmt,x,'hits',len(hits),flush=True)
# Fullrectangularpayloadsweptsolid alongX is exact forrectangularsurrogate.
pp=b.assembly('CellB_3U',0,'launch',True,'3U',0)
sweep=b.box((1240.5,100,100),(0,0,22));hits=[]
for q in pp:
 if q['name'].startswith('Receiver__'):continue
 if not sweep.BoundBox.intersect(q['shape'].BoundBox):continue
 v=sweep.common(q['shape']).Volume
 if v>1e-5:hits.append({'part':q['name'],'volume_mm3':v})
cases.append({'case':'exact_rectangular_payload_X_sweep','X_interval_mm':[0,1240.5],'positive_volume_interferences':hits,'pass':not hits})
summary={'revision':b.REV,'builder_sha256':SOURCE_HASH,'case_count':len(cases),'all_sampled_cases_pass':all(q['pass'] for q in cases),'failed_case_count':sum(not q['pass'] for q in cases),'cases':cases,'numerical_penetration_limit_mm3':1e-5,'nominal_geometry_only':True,'boundary':'Discrete native BRep comparisons of every moving/changed part against complete assembly; unchanged partpairs referenced to five full capture audits. Receiver rectangular payloadX sweep is a continuous exact geometric envelope; full mechanism motion is sampled, not certifiedcontinuous. Includes knowncatalogenvelopes; no fitted/thread/dynamic/contactloadqualification.', 'elapsed_s':time.perf_counter()-started}
assert SOURCE_HASH==hashlib.sha256(Path(b.__file__).read_bytes()).hexdigest(),'Builderchangedwhileverificationrunning'
(O/'MOTION_VERIFICATION.json').write_text(json.dumps(summary,indent=2)+'\n')
print('DONE',summary['case_count'],'fail',summary['failed_case_count'],'elapsed',summary['elapsed_s'],flush=True)
