"""Check hashes, source preservation, conservation and actual retained dispositions."""
import argparse,ast,copy,hashlib,json
from pathlib import Path
import numpy as np
from derated_source_variant import VoltageParameters,RestoreParameters
P=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(s):return json.loads((P/s).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package-only',action='store_true');args=ap.parse_args();checks=[]
 def check(name,value,detail=None):
  checks.append(dict(name=name,pass_=bool(value),detail=detail));assert value,(name,detail)
 manifest=read('PUBLIC_SOURCE_MANIFEST.json');records=manifest['files']
 for r in records:
  if args.package_only and r['path'].startswith('../'):continue
  p=P/r['path'];check('manifest:'+r['path'],p.is_file() and sha(p)==r['sha256'] and p.stat().st_size==r['bytes'])
 for r in read('INPUT_SOURCE_MANIFEST.json'):
  check('copied_input:'+r['path'],sha(P/r['path'])==r['sha256'])
  original=P.parents[1]/r['original_public_path']
  if original.exists() and not args.package_only:check('original_core_unchanged:'+r['original_public_path'],sha(original)==r['sha256'])
 for r in read('PRIMARY_SOURCE_REGISTER.json'):
  if r.get('local_public_path'):check('primary_snapshot:'+r['id'],sha(P/r['local_public_path'])==r['sha256'])
 for samples in [4096,8192]:
  for stage in range(13):
   name=f'geometry/radiation_{samples}.npz' if stage==0 else f'geometry/radiation_s{stage:02d}_{samples}.npz';g=np.load(P/name);A=g['areas'];F=g['view_factors'];AF=A[:,None]*F
   check('radiation_reciprocity:'+name,np.max(abs(AF-AF.T))<1e-8)
   check('radiation_area_conservation:'+name,np.max(abs(AF.sum(axis=1)+g['escape_areas']-A))<1e-8)
   check('source_no_invented_radiator:'+name,A[6]==0 and A[7]==0)
 mesh=np.load(P/'geometry/cad_mesh.npz');bom=read('inputs/VOLLEY_G5_ACR1_home.json')['BOM'];mass=sum(r['mass_kg'] for r in bom)+7
 check('actual_BOM_mass_plus_source_allowance',abs(mesh['masses'].sum()-mass)<1e-7,dict(network_kg=float(mesh['masses'].sum()),BOM_plus7_kg=mass))
 b=read('THERMAL_RESULTS.json');c=read('THERMAL_CORRECTIONS.json');n=read('NUMERICAL_VERIFICATION.json');v=read('DERATED_SOURCE_RESULTS.json');replay=read('PORTABLE_REPLAY.json')
 for output,script in [(b,'thermal_network.py'),(c,'thermal_corrections.py'),(n,'verify_numerics.py')]:check('current_result_source:'+script,output['source_sha256']==sha(P/script))
 check('current_voltage_adapter',v['adapter_sha256']==sha(P/'derated_source_variant.py'))
 check('current_numerical_solver',n['solver_sha256']==sha(P/'thermal_network.py'))
 tree=ast.parse((P/'inputs/coupled_shot_production.py').read_text());adapter=VoltageParameters();adapted=adapter.visit(copy.deepcopy(tree));restored=RestoreParameters().visit(adapted)
 check('only_three_voltage_parameters_AST_restoration',len(adapter.changes)==3 and ast.dump(tree,include_attributes=False)==ast.dump(restored,include_attributes=False))
 check('18_actual_derated_cases_pass_original_and_extra_gates',len(v['cases'])==18 and all(r['all_declared_checks_pass'] and r['all_derated_checks_pass'] for r in v['cases']))
 check('18_case_combinations_exact',len({(r['target_m_s'],r['adverse'],r['inductance_H']) for r in v['cases']})==18)
 check('original_hot_failure_retained',all(not r['cell_catalogue_band_screen_pass'] for r in b['cases'] if r['environment']['id']=='hot'))
 check('all_numerical_gates_pass',n['all_gates_pass'] and all(n['gates'].values()),n['summary'])
 for key in ['corrected86p4V_cases','combined78p4V_path_cases']:
  result=next(r['result'] for r in n['rows'] if r['case']==key);check('final_refined_60C_gate:'+key,result['temperature_max_C'][6]<60,result['temperature_max_C'][6])
 no_path=next(r['result'] for r in n['rows'] if r['case']=='derated78p4V_cases');check('derating_alone_catalogue_pass_monitor_margin_fail_retained',80<no_path['temperature_max_C'][6]<85,no_path['temperature_max_C'][6])
 diag=read('results/NUMERICAL_VERIFICATION_2P5WK_DIAGNOSTIC.json');check('initial_2p5WK_margin_failure_retained',not diag['gates']['corrected_corner_refined_below60C'])
 allocation=c['provisional_strap_pad_allocation'];check('final_conductance_and_mass_allocation',allocation['required_measured_sourceplate_to_regulated_host_G_W_K']==3 and allocation['calculated_series_path_G_W_K']>=3 and allocation['total_allocated_path_mass_kg']<=.9)
 check('portable18_case_output_bit_identical',replay['all_replay_checks_pass'] and replay['production18_case_output_sha256']==sha(P/'DERATED_SOURCE_RESULTS.json') and replay['refined_hot_corrected_corner_max_peak_delta_K']<1e-10)
 check('portable_script_identity',replay['source_sha256']==sha(P/'portable_replay.py'))
 for row in read('FIGURE_SOURCE_INVENTORY.json'):
  check('figure_source:'+row['figure'],row['source_sha256']==sha(P/row['source_script']))
  for r in row['inputs']:check('figure_input:'+row['figure']+':'+r['path'],r['sha256']==sha(P/r['path']))
  for name in row['files']:check('figure_exists:'+name,(P/name).stat().st_size>1000)
 result=dict(study='ACR1-THERM-ENV-01',checker_sha256=sha(Path(__file__)),manifest_sha256=sha(P/'PUBLIC_SOURCE_MANIFEST.json'),package_only=args.package_only,all_checks_pass=True,count=len(checks),checks=checks)
 (P/'CAPTURE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(all_checks_pass=True,count=len(checks),manifest_sha256=result['manifest_sha256'])))
if __name__=='__main__':main()
