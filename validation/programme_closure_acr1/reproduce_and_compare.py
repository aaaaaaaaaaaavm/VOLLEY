"""Reproduce arithmetic/covariance in isolation and compare captured results.

Native GMAT is not rerun by this command; its distinct raw-output identities,
events and constant-mass-flow invariants are checked by check_capture.py.
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent


def compare(a,b,path='root'):
    if isinstance(a,dict):
        assert set(a)==set(b),path
        for key in a:compare(a[key],b[key],path+'.'+key)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,f'{path}[{i}]')
    elif isinstance(a,(float,int)) and not isinstance(a,bool):
        assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-8),(path,a,b)
    else:assert a==b,(path,a,b)


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
