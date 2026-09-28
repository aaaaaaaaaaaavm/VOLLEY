"""Frozen P92-S6-R1 gate-spacing budget; calibration remains unperformed."""
import argparse,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
u=2*6*math.sqrt((.0001/.2)**2+(.00001/(.2/6))**2)
d=dict(spacing_m=.2,range_m_s=6.,spacing_standard_uncertainty_m=.0001,
    interval_standard_uncertainty_s=.00001,expanded_uncertainty_m_s=u,
    limit_m_s=.01,calculated_budget_pass=u<=.01,physical_calibration_done=False,
    source_sha256={str(path):hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in
        ('analysis/instrument_r1.py','validation/P92_S6R1_instrument.md')})
f=ROOT/'analysis/results/instrument_r1.json'
if a.check: assert json.loads(f.read_text())==d,'stale instrument budget'
else:f.write_text(json.dumps(d,indent=2)+'\n')
print('R1 calculated budget:',u,'m/s; physical calibration not performed');assert d['calculated_budget_pass']
