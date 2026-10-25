"""Replay outside the repository, using only this self-contained study package."""
import json,shutil,subprocess,sys,tempfile,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 with tempfile.TemporaryDirectory(prefix='acr1-thermal-portable-') as tmp:
  dest=Path(tmp)/'study';shutil.copytree(P,dest,ignore=shutil.ignore_patterns('__pycache__','.git','PORTABLE_REPLAY.json'))
  native=subprocess.run([sys.executable,'derated_source_variant.py'],cwd=dest,text=True,capture_output=True,check=True)
  baseline=sha(P/'DERATED_SOURCE_RESULTS.json');replay=sha(dest/'DERATED_SOURCE_RESULTS.json');assert baseline==replay
  code="""import json\nfrom thermal_network import HERE,ThermalNetwork\nc=json.loads((HERE/'THERMAL_INPUTS.json').read_text());a=json.loads((HERE/'THERMAL_CORRECTIONS.json').read_text());r=next(r for r in a['corrected86p4V_cases'] if r['context']=='bounded_contact_corner' and r['command_m_s']==3);n=ThermalNetwork(c,r['environment'],r['parameters'],3,samples=8192).run(dt=5);(HERE/'REPLAY_THERMAL.json').write_text(json.dumps(n,sort_keys=True))\n"""
  subprocess.run([sys.executable,'-c',code],cwd=dest,text=True,capture_output=True,check=True)
  got=json.loads((dest/'REPLAY_THERMAL.json').read_text());original=next(r['result'] for r in json.loads((P/'NUMERICAL_VERIFICATION.json').read_text())['rows'] if r['case']=='corrected86p4V_cases')
  delta=max(abs(a-b) for a,b in zip(got['temperature_max_C'],original['temperature_max_C']));assert delta<1e-10
  result=dict(study='ACR1-THERM-PORTABLE-01',source_sha256=sha(Path(__file__)),isolated_temporary_directory=True,repository_parent_not_used_by_runtime=True,inputs='Copied self-contained study only; no sibling ACR1 or private workspace paths used.',production18_case_output_bit_identical=baseline==replay,production18_case_output_sha256=replay,refined_hot_corrected_corner_max_peak_delta_K=delta,refined_cell_max_C=got['temperature_max_C'][6],python=sys.version,all_replay_checks_pass=True,stdout=native.stdout)
 (P/'PORTABLE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='stdout'},indent=2))
if __name__=='__main__':main()
