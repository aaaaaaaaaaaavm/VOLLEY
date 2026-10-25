"""Same finite winding, evaluated across the provisional carrier arrest travel."""
from pathlib import Path
import hashlib,json
import finite_motor as m
ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=(ROOT/'cad/PARAMETERS.json').read_bytes();p=json.loads(raw);field=m.make_field(p);rows=[]
    for x in [1.3,1.325,1.35,1.375,1.4,1.425,1.45,1.475,1.5,1.51]:
        c=m.active_coefficients(field,p,x,(3,3,5));q=m.return_coefficients(field,p,x,5,3)
        rows.append({'displacement_m':x,'N_per_peak_A':m.amplitude(c+q)})
        print(x,rows[-1]['N_per_peak_A'],flush=True)
    result={'configuration_id':p['configuration_id'],'CAD_parameter_sha256':hashlib.sha256(raw).hexdigest(),
        'model_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'finite_field_source_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest(),
        'scope':'Analytic finite winding field, ideal opposing phase; not a rated brake','stations':rows}
    (ROOT/'analysis/ARREST_FORCE_MAP.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'analysis/ARREST_FORCE_INPUT.json').write_bytes(raw)

if __name__=='__main__':main()
