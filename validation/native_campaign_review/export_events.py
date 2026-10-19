from pathlib import Path
import csv,json,hashlib,importlib.util
H=Path(__file__).resolve().parent;O=H/'events';O.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('campaign_export',H/'export_campaign.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
archived=H/'reference'
refs=json.loads((archived/'RESULTS.json').read_text())['cases']+json.loads((archived/'RESERVE_CASES.json').read_text())['cases']
rows=[]
for count,strategy,fuel in [(4,'spring',10),(4,'volley_3_6',10),(12,'spring',20),(12,'volley_3_6',20),(12,'volley_3_6',10),(12,'spring',10)]:
 name=f'{count}_{strategy}_{fuel}kg'
 try:
  d=mod.construct(count,strategy,initial_fuel=fuel)
  reference=next(x for x in refs if x.get('count')==count and x.get('strategy')==strategy and x.get('initial_fuel_kg')==fuel and 'fuel_used_kg' in x)
  assert abs(d['fuel_used_kg']-reference['fuel_used_kg'])<1e-8,(name,d['fuel_used_kg'],reference['fuel_used_kg'])
  out=O/(name+'_events.csv')
  with out.open('w',newline='') as file:
   writer=csv.writer(file,lineterminator="\n");writer.writerow(['t_s','kind','payload','dx','dy','dz','mass_before_kg','mass_after_kg','payload_kg','rx','ry','rz','vx','vy','vz','target_rx','target_ry','target_rz','target_vx','target_vy','target_vz','event_role'])
   for e in d['events']:writer.writerow([e['t_s'],e['kind'],e['payload'],*e['delta'],e['mass_before_kg'],e['mass_after_kg'],e['payload_kg'],*e['expected_host'],*e['target_final'],e.get('role',e['kind'])])
  (O/(name+'_source.json')).write_text(json.dumps(d,indent=2)+'\n')
  rows.append({'case':name,'status':'exported','events':len(d['events']),'fuel_kg':d['fuel_used_kg'],'reference_fuel_difference_kg':d['fuel_used_kg']-reference['fuel_used_kg'],'event_sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 except RuntimeError as e:
  rows.append({'case':name,'status':'failed_source_campaign','reason':str(e)})
 print(rows[-1],flush=True)
(O/'EXPORT_RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n')
