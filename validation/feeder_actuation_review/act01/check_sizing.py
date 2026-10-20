"""Independent dimensions, kinematics and mechanical-work checks for ACT-01."""
from pathlib import Path
import json,math
H=Path(__file__).resolve().parent;P=json.loads((H/'parameters.json').read_text());R=json.loads((H/'RESULTS.json').read_text())
assert len(R['cases'])==4860
for c in R['cases']:
 T=c['time_s'];a=4*P['stroke_m']/T**2;v=2*P['stroke_m']/T
 assert abs(.5*a*(T/2)**2*2-P['stroke_m'])<1e-12
 assert abs(c['screw_peak_rpm']-60*v/P['screw_lead_m'])<1e-8
 assert abs(c['max_force_N']-(c['resistance_N']+c['moving_mass_kg']*a))<1e-9
 # Mechanical energy dissipated by declared resistance is independent of the drive train.
 assert c['input_energy_proxy_J']>=c['resistance_N']*P['stroke_m']
 assert c['all_catalog_screens_pass']==(c['catalog_continuous_torque_pass'] and c['catalog_voltage_speed_pass'] and c['nut_catalog_screen_pass'])
 if c['screw_peak_rpm']>1000: assert not c['nut_rating_available'] and not c['all_catalog_screens_pass']
 assert c['root_euler_buckling_margin']>1
assert all(not x['all_catalog_screens_pass'] for x in R['cases'] if x['time_s']<=10)
assert any(x['all_catalog_screens_pass'] for x in R['cases'] if x['time_s']>=15)
print('ACT-01 independent kinematic,work,load and catalogue-domain checks pass; no installed drive/holding/flight rating')
