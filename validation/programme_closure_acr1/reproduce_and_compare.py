"""Reproduce arithmetic/covariance in isolation and compare captured results.

Native GMAT is not rerun by this command; its distinct raw-output identities,
events and constant-mass-flow invariants are checked by check_capture.py.
"""
import json
import math
import numbers
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent


DEFAULT_RELATIVE_TOLERANCE=1e-11
DEFAULT_ABSOLUTE_TOLERANCE=1e-8
CAMPAIGN_MASS_ABSOLUTE_KG=1e-7


def comparison_policy(profile='default'):
    """Numerical reproduction floors; physical criteria and discrete decisions are separate."""
    policy=dict(profile=profile,default_float_relative=DEFAULT_RELATIVE_TOLERANCE,
                default_float_absolute=DEFAULT_ABSOLUTE_TOLERANCE,
                discrete='Dictionary keys, list lengths, integers, booleans, strings and policy subtrees exact',
                scientific_acceptance='Unchanged source criteria; reproduced pass/fail outcomes must match exactly')
    if profile=='campaign':
        policy['mass_absolute_kg']=CAMPAIGN_MASS_ABSOLUTE_KG
        policy['mass_scope']='Non-residual *_kg floats and propellant at zero-based index 6 of documented 14-component campaign state vectors only'
        policy['mass_rationale']='0.1 mg numerical floor; observed CI hardware difference 1.196e-8 kg. Same scale as the separate existing 1e-7 kg native mass-agreement criterion; not a mass/reserve acceptance waiver.'
    return policy


def float_budget(path,profile):
    key=path.rsplit('.',1)[-1]
    # Keep conservation residuals at the pre-existing tighter comparison floor.
    mass=(key.endswith('_kg') and 'residual'not in key)
    # Campaign.run packs [position3,velocity3,propellant1,quaternion4,momentum3].
    packed=bool(re.search(r'\.(?:final_host_state|before_host_state|after_host_state|before|after)\[6\]$',path))
    if profile=='campaign'and(mass or packed):
        return DEFAULT_RELATIVE_TOLERANCE,CAMPAIGN_MASS_ABSOLUTE_KG,'campaign_mass_kg'
    return DEFAULT_RELATIVE_TOLERANCE,DEFAULT_ABSOLUTE_TOLERANCE,'default_float'


def compare(a,b,path='root',*,profile='default',diagnostics=None):
    if isinstance(a,dict):
        assert isinstance(b,dict)and set(a)==set(b),(path,'dictionary schema differs')
        for key in a:
            child=path+'.'+key
            if key=='policy':assert json.dumps(a[key],sort_keys=True)==json.dumps(b[key],sort_keys=True),(child,'release policy differs')
            else:compare(a[key],b[key],child,profile=profile,diagnostics=diagnostics)
    elif isinstance(a,list):
        assert isinstance(b,list)and len(a)==len(b),(path,'list structure differs')
        for i,(x,y)in enumerate(zip(a,b)):compare(x,y,f'{path}[{i}]',profile=profile,diagnostics=diagnostics)
    elif isinstance(a,bool):
        assert type(b)is bool and a==b,(path,a,b,'boolean outcome differs')
    elif isinstance(a,int):
        assert isinstance(b,numbers.Integral)and not isinstance(b,bool)and a==b,(path,a,b,'integer/count differs')
    elif isinstance(a,float):
        assert isinstance(b,numbers.Real)and not isinstance(b,bool)and math.isfinite(a)and math.isfinite(b),(path,a,b,'nonfinite/type change')
        relative,absolute,budget=float_budget(path,profile)
        limit=max(absolute,relative*max(abs(a),abs(b)));error=abs(a-b)
        if diagnostics is not None:
            ratio=error/limit
            if budget not in diagnostics or ratio>diagnostics[budget]['maximum_fraction_of_budget']:
                diagnostics[budget]=dict(path=path,reference=a,reproduced=b,absolute_error=error,
                                         absolute_floor=absolute,relative_tolerance=relative,
                                         effective_limit=limit,maximum_fraction_of_budget=ratio)
        assert math.isclose(a,b,rel_tol=relative,abs_tol=absolute),(path,a,b,'absolute_error',error,'effective_limit',limit,'budget',budget)
    else:assert type(a)is type(b)and a==b,(path,a,b)


def main():
    with tempfile.TemporaryDirectory(prefix='volley-pcs-reproduce-') as tmp:
        dest=Path(tmp)
        for name in ['complete_studies.py','navigation_requirements.py','lunar_native.py','study_inputs.json']:
            shutil.copyfile(HERE/name,dest/name)
        shutil.copytree(HERE/'inputs',dest/'inputs')
        for script,args in [('complete_studies.py',['--no-plots']),('navigation_requirements.py',[])]:
            r=subprocess.run([sys.executable,str(dest/script),*args],text=True,capture_output=True)
            assert r.returncode==0,(script,r.stdout,r.stderr)
        for name in ['STUDY_RESULTS.json','NAVIGATION_REQUIREMENTS.json']:
            compare(json.loads((HERE/name).read_text()),json.loads((dest/name).read_text()))
    result=dict(study='PCS-ACR1-01',isolated_arithmetic_and_covariance_reproduction_pass=True,
                compared=['STUDY_RESULTS.json','NAVIGATION_REQUIREMENTS.json'],
                relative_tolerance=1e-11,absolute_tolerance=1e-8,
                native_GMAT_rerun=False,
                native_scope='Raw histories,source/runtime hashes,root stops and mass-flow checks are separate; native runtime commands in README.')
    (HERE/'REPRODUCTION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: isolated arithmetic,finite two-body burn and covariance reproduce within declared comparison tolerance. Native replay is a separate command.')


if __name__=='__main__':main()
