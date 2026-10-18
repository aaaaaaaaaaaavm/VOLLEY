"""Dependency-free integrity and physical limiting checks for captured native output."""
from pathlib import Path
import csv,hashlib,json,math
ROOT=Path(__file__).resolve().parent

def main():
 d=json.loads((ROOT/'ORBIT_RESULTS.json').read_text())
 for name,expected in d['source_hashes'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:raise SystemExit('Captured source/output changed: '+name)
 groups={}
 with (ROOT/'orekit_30s.csv').open()as h:
  for row in csv.DictReader(h):
   key=(row['model'],float(row['relative_speed_m_s']));values=[float(v)for k,v in row.items()if k!='model']
   if not all(math.isfinite(v)for v in values):raise SystemExit('Nonfinite native state')
   groups.setdefault(key,[]).append(row)
 if len(groups)!=8:raise SystemExit('Expected eight native histories')
 for (model,u),rows in groups.items():
  if len(rows)!=1441 or [float(r['t_s'])for r in rows]!=list(range(0,86401,60)):raise SystemExit('Native time grid changed')
  first=rows[0];r=math.sqrt(sum(float(first[k])**2 for k in ('x_m','y_m','z_m')));v2=sum(float(first[k])**2 for k in ('vx_m_s','vy_m_s','vz_m_s'))
  expected=1/(2/r-v2/3.986004418e14)
  if abs(expected-float(first['a_m']))>1e-5:raise SystemExit('Initial energy/axis identity failed')
 for case in d['cases']:
  if case['max_refinement_position_m']>.001 or case['max_scipy_position_difference_m']>.001:raise SystemExit('Numerical check exceeds 1 mm software screen')
  if case['max_relative_energy_drift']>1e-9 or case['max_relative_hz_drift']>1e-9:raise SystemExit('Conservation screen failed')
 if d['cross_code'][1]['same_force_configuration']:raise SystemExit('Unresolved J2 setup falsely marked matched')
 print('PASS: eight captured histories, exact hashes/time grids, energy identity and bounded software checks')
if __name__=='__main__':main()
