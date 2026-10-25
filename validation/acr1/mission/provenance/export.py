from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent/'release'
for path in sorted(P.glob('*.json')):
    r=json.loads(path.read_text())
    with path.with_suffix('.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['start_s','end_s','kind','payload','payload_mass_kg','fx_or_ux','fy_or_uy','fz_or_uz','mass_after_kg','rx','ry','rz','vx','vy','vz','target_rx','target_ry','target_rz','target_vx','target_vy','target_vz','label'])
        w.writerow([r['initial_time_s'],r['initial_time_s'],'initial',0,0,0,0,0,r['initial_state'][6],*r['initial_state'][:6],*r['final_host_target'],'initial'])
        for e in r['events']:
            w.writerow([e['start_s'],e['end_s'],e['kind'],e.get('payload',0),e.get('payload_mass_kg',0),*e.get('force_N',e.get('u_m_s',[0,0,0])),e['after'][6],*e['after'][:6],*e.get('target',[0]*6),e.get('label','shot')])
