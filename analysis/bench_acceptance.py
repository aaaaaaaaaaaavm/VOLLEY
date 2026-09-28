"""Evaluate measured MC-L2 speed characterization; fail closed on missing evidence."""
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path


def evaluate(run, directory):
    reasons=[]
    for field in ('article_serial','source_commit','drawing_revision','configuration_id','calibration_record','reviewer_release_record'):
        if not isinstance(run.get(field),str) or not run[field].strip(): reasons.append('MISSING_'+field.upper())
    for field in ('calibration_record','reviewer_release_record'):
        if run.get(field) and not (directory/run[field]).is_file(): reasons.append('UNAVAILABLE_'+field.upper())
    shots=run.get('shots',[])
    if not isinstance(shots,list): return dict(speed_characterization_pass=False,reasons=['INVALID_SHOTS'])
    if len(shots)!=20: reasons.append('REQUIRE_20_CONSECUTIVE_SHOTS')
    speeds=[]; ids=[]
    for i,s in enumerate(shots):
        if not isinstance(s,dict):
            reasons.append(f'SHOT_{i}_INVALID_RECORD'); continue
        try:
            if type(s['shot_id']) is not int: raise ValueError()
            ids.append(s['shot_id'])
            v,p,u=(float(s[k]) for k in ('measured_speed_m_s','predicted_speed_m_s','expanded_uncertainty_m_s'))
            if not all(math.isfinite(x) for x in (v,p,u)) or min(v,p,u)<0: raise ValueError()
            speeds.append(v)
            if v>6 or u<=0: reasons.append(f'SHOT_{i}_INSTRUMENT_RANGE_OR_BUDGET')
            if abs(v-p)>.10+1e-12: reasons.append(f'SHOT_{i}_MODEL_ERROR')
            if u>.01: reasons.append(f'SHOT_{i}_UNCERTAINTY')
            if s.get('captured') is not True: reasons.append(f'SHOT_{i}_CAPTURE')
            if s.get('configuration_id')!=run.get('configuration_id'): reasons.append(f'SHOT_{i}_CONFIGURATION')
            raw=directory/s['raw_file']; digest=hashlib.sha256(raw.read_bytes()).hexdigest()
            if digest!=s['raw_sha256']: reasons.append(f'SHOT_{i}_RAW_HASH')
        except (KeyError,TypeError,ValueError,OSError): reasons.append(f'SHOT_{i}_INVALID_OR_MISSING_EVIDENCE')
    if ids!=list(range(1,21)): reasons.append('NONCONSECUTIVE_SHOT_IDS')
    sigma=statistics.stdev(speeds) if len(speeds)>1 else None
    if sigma is None or sigma>.03: reasons.append('REPEATABILITY')
    return dict(speed_characterization_pass=not reasons,reasons=reasons,sample_std_m_s=sigma,
                disposition='SPEED_CHARACTERIZATION_ONLY_NOT_HARDWARE_RELEASE')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args()
    d=evaluate(json.loads(a.run.read_text()),a.run.parent);print(json.dumps(d,indent=2))
    raise SystemExit(0 if d['speed_characterization_pass'] else 1)
