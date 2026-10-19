"""Native full-event baselines and deterministic uncertainty probes.

No measurement-derived probability, flight precision or component rating.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os,subprocess,csv,json,hashlib,math
H=Path(__file__).resolve().parent;O=H/'full';O.mkdir(exist_ok=True)
CP=os.environ.get('OREKIT_CLASSPATH')
if not CP:raise SystemExit('Set OREKIT_CLASSPATH to the pinned Orekit/Hipparchus jars')
CASES=[('4_spring_10kg',10),('4_volley_3_6_10kg',10),('12_spring_20kg',20),('12_volley_3_6_20kg',20),('12_volley_3_6_10kg',10)]
# [shot multiplier,burn multiplier,pitch degrees,yaw degrees,shot latency seconds]
PROBES={
 'nominal':[1,1,0,0,0],
 'shot_plus_1pct':[1.01,1,0,0,0], 'shot_minus_1pct':[.99,1,0,0,0],
 'shot_plus_0p1pct':[1.001,1,0,0,0],
 'pitch_plus_0p1deg':[1,1,.1,0,0], 'pitch_minus_0p1deg':[1,1,-.1,0,0],
 'yaw_plus_0p1deg':[1,1,0,.1,0], 'yaw_minus_0p1deg':[1,1,0,-.1,0],
 'burn_plus_0p1pct':[1,1.001,0,0,0], 'burn_minus_0p1pct':[1,.999,0,0,0],
 'shot_delay_5ms':[1,1,0,0,.005], 'shot_delay_50ms':[1,1,0,0,.05],
}

def run(job):
 name,fuel,probe,step=job
 source=H/'events'/(name+'_events.csv');stem=f'{name}_{probe}_step{step}';prefix=O/stem
 parameters=PROBES[probe]
 command=['java','-cp',CP,'CoupledEvents.java',str(source.relative_to(H)),str(prefix.relative_to(H)),str(step),str(fuel),*[str(v) for v in parameters]]
 process=subprocess.run(command,cwd=H,capture_output=True,text=True)
 (O/(stem+'.log')).write_text(process.stdout+process.stderr)
 if process.returncode:raise RuntimeError(stem+': '+process.stdout+process.stderr)
 host=list(csv.DictReader((O/(stem+'_host.csv')).open()))
 payload=list(csv.DictReader((O/(stem+'_payload.csv')).open()))
 src=list(csv.DictReader(source.open()));initial_mass=float(src[0]['mass_before_kg'])
 fuel_used=fuel-float(host[-1]['fuel_remaining_kg']);final_mass=float(host[-1]['mass_kg'])
 released_mass=sum(float(r['mass_kg']) for r in payload)
 ledger_residual=initial_mass-final_mass-released_mass-fuel_used
 assert abs(ledger_residual)<1e-8,ledger_residual
 assert len(payload)==int(name.split('_')[0])
 row={'case':name,'probe':probe,'maximum_step_s':step,'initial_fuel_kg':fuel,'parameters':dict(zip(['shot_multiplier','burn_multiplier','pitch_deg','yaw_deg','shot_latency_s'],parameters)),
      'release_count':len(payload),'fuel_used_kg':fuel_used,'mass_ledger_residual_kg':ledger_residual,
      'max_payload_position_error_m':max(float(r['position_target_error_m']) for r in payload),
      'max_payload_velocity_error_m_s':max(float(r['velocity_target_error_m_s']) for r in payload),
      'final_host_position_error_m':float(host[-1]['position_residual_m']),
      'final_host_velocity_error_m_s':float(host[-1]['velocity_residual_m_s']),
      'max_host_event_position_residual_m':max(float(r['position_residual_m']) for r in host),
      'max_host_mass_residual_kg':max(abs(float(r['mass_residual_kg'])) for r in host[:-1]),
      'max_release_momentum_residual_kg_m_s':max(float(r['momentum_residual_kg_m_s']) for r in payload),
      'max_release_energy_identity_residual_J':max(float(r['energy_identity_residual_J']) for r in payload),
      'source_csv':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'java_source_sha256':hashlib.sha256((H/'CoupledEvents.java').read_bytes()).hexdigest(),
      'command_template':['java','-cp','$OREKIT_CLASSPATH',*command[3:]],
      'output_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/(stem+'.log'),O/(stem+'_host.csv'),O/(stem+'_payload.csv')]}}
 if probe=='nominal':
  assert row['max_payload_position_error_m']<.01,row
  assert row['final_host_position_error_m']<.01,row
  assert row['max_payload_velocity_error_m_s']<1e-5,row
  assert row['max_host_mass_residual_kg']<1e-8,row
 print(name,probe,step,'max payload position',row['max_payload_position_error_m'],'m',flush=True)
 return row

jobs=[(name,fuel,'nominal',60) for name,fuel in CASES]
jobs += [(name,fuel,'nominal',30) for name,fuel in CASES if name in ['12_spring_20kg','12_volley_3_6_20kg']]
jobs += [(name,fuel,probe,60) for name,fuel in CASES[:4] for probe in PROBES if probe!='nominal']
# Each process writes a distinct case; controls and outputs are independent.
with ThreadPoolExecutor(max_workers=2) as executor:rows=list(executor.map(run,jobs))
result={'revision':'CNR-01-2026-10-19','force_model':'500km97.4deg surrogate,fixed inertial+Z J2,ideal impulses,common90000s epoch',
 'thresholds':'Nominal numerical cross-check:1cm position and1e-5m/s velocity; not a flight accuracy or rigorous integration-error enclosure',
 'case_count':len(rows),'cases':rows,
 'limitations':['Frozen commanded controls are replayed,not independently optimized','Both SciPy and Hipparchus use DOP853; force,recoil and rocket bookkeeping are separate implementations','Sensitivity inputs are deterministic assumptions,not measured dispersions or reliability','No finite burn,slew,closed-loop navigation,contact,body geometry,source rating or environmental qualification']}
(O/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed',len(rows),'full native coupled campaign cases')
