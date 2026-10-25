"""Independent balance, time-step and CAD-ray quadrature checks."""
import copy,json
from pathlib import Path
import numpy as np
from thermal_network import HERE,ThermalNetwork,sha

def main():
 c=json.loads((HERE/'THERMAL_INPUTS.json').read_text()); baseline=json.loads((HERE/'THERMAL_RESULTS.json').read_text());cor=json.loads((HERE/'THERMAL_CORRECTIONS.json').read_text());variants=json.loads((HERE/'DERATED_SOURCE_RESULTS.json').read_text());rows=[]
 for old in baseline['cases']:
  e=old['environment'];u=old['command_m_s'];new=ThermalNetwork(c,e,old['parameters'],u).run(dt=5)
  rows.append(dict(check='time_step',case=e['id'],command_m_s=u,max_node_peak_delta_K=float(np.max(abs(np.array(new['temperature_max_C'])-old['temperature_max_C']))),cell_peak_delta_K=new['temperature_max_C'][6]-old['temperature_max_C'][6],result=new))
  print(rows[-1]['check'],e['id'],u,rows[-1]['max_node_peak_delta_K'],flush=True)
 for old in [baseline['cases'][1],baseline['cases'][3],baseline['cases'][4]]:
  e=old['environment'];u=old['command_m_s'];new=ThermalNetwork(c,e,old['parameters'],u,samples=8192).run()
  rows.append(dict(check='ray_samples',case=e['id'],command_m_s=u,max_node_peak_delta_K=float(np.max(abs(np.array(new['temperature_max_C'])-old['temperature_max_C']))),cell_peak_delta_K=new['temperature_max_C'][6]-old['temperature_max_C'][6],result=new))
  print(rows[-1]['check'],e['id'],u,rows[-1]['max_node_peak_delta_K'],flush=True)
 for key,variant in [('corrected86p4V_cases',False),('combined78p4V_path_cases',True),('derated78p4V_cases',True)]:
  old=next(r for r in cor[key] if r['context']=='bounded_contact_corner' and r['command_m_s']==3)
  new=ThermalNetwork(c,old['environment'],old['parameters'],3,samples=8192,source_cases=variants['cases'] if variant else None,regen_cell_V=2.47 if variant else 2.9,cell_temperature_max_C=85 if variant else 65).run(dt=5)
  rows.append(dict(check='combined_time_and_ray',case=key,command_m_s=3,max_node_peak_delta_K=float(np.max(abs(np.array(new['temperature_max_C'])-old['temperature_max_C']))),cell_peak_delta_K=new['temperature_max_C'][6]-old['temperature_max_C'][6],result=new))
  print(rows[-1]['check'],key,rows[-1]['max_node_peak_delta_K'],new['temperature_max_C'][6],flush=True)
 all_results=baseline['cases']+baseline['uncertainty']+[r['result'] for r in rows]+sum([cor[k] for k in ['corrected86p4V_cases','derated78p4V_cases','combined78p4V_path_cases']],[])
 summary=dict(max_time_step_peak_delta_K=max(r['max_node_peak_delta_K'] for r in rows if r['check']=='time_step'),max_ray_peak_delta_K=max(r['max_node_peak_delta_K'] for r in rows if r['check']=='ray_samples'),max_global_energy_balance_residual_J=max(r['max_global_energy_balance_residual_J'] for r in all_results),max_independent_radiosity_balance_residual_W=max(r['max_independent_radiosity_balance_residual_W'] for r in all_results),max_periodic_delta_K=max(r['storage']['periodic_orbit_max_delta_K'] for r in all_results),max_periodic_validation_orbits=max(r['storage']['periodic_validation_orbits'] for r in all_results))
 gates=dict(time_step_below_0p1K=summary['max_time_step_peak_delta_K']<.1,energy_balance_below_0p01J=summary['max_global_energy_balance_residual_J']<.01,independent_radiosity_below_1e8W=summary['max_independent_radiosity_balance_residual_W']<1e-8,periodic_below_0p02K=summary['max_periodic_delta_K']<.02,corrected_corner_refined_below60C=all(r['result']['temperature_max_C'][6]<60 for r in rows if r['check']=='combined_time_and_ray' and r['case']!='derated78p4V_cases'))
 result=dict(source_sha256=sha(__file__),solver_sha256=sha(HERE/'thermal_network.py'),summary=summary,gates=gates,all_gates_pass=all(gates.values()),rows=rows,interpretation='Numerical resolution and internal balance checks; no physical accuracy or independent software validation is inferred. Ray quadrature discrepancy is retained, rather than hidden as a confidence interval.')
 (HERE/'NUMERICAL_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2));print(gates)
if __name__=='__main__':main()
