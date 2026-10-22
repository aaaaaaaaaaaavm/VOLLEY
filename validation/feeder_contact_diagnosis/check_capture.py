from pathlib import Path
import hashlib,json,csv
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST.json').read_text())
for name,rec in m['files'].items():
    p=R/name
    assert p.is_file() and p.stat().st_size==rec['bytes'],name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'],name
for name in ['P3-250','W3-250','B3-250','B3-125','X3-250','X3-125']:
    p=R/'runs'/(name+'.csv')
    with p.open() as f:
        rows=list(csv.DictReader(f))
    assert rows,name
    key=next(k for k in rows[-1] if k in ['t','time','time_s','t_s'])
    assert abs(float(rows[-1][key])-26.5)<1e-8,name
assert (R/'runs/P3-250.csv').read_bytes()==(R/'baseline/FCE12-05.csv').read_bytes()
import importlib.util,math
spec=importlib.util.spec_from_file_location('fce13_analysis',R/'analyze_selected.py')
analysis=importlib.util.module_from_spec(spec);spec.loader.exec_module(analysis)
summary=json.loads((R/'SUMMARY.json').read_text())
assert summary['criteria_unchanged']=={'COM_mm':.05,'angle_deg':.05,'work_relative':.01}
for item in summary['observed_sensitivities']:
    paths=[]
    for name in item['pair']:
        matches=[p for parent in ['runs','baseline'] if (p:=R/parent/(name+'.csv')).is_file()]
        assert len(matches)==1,name
        paths.append(matches[0])
    actual=analysis.compare(*paths)
    assert math.isclose(actual['stages'][-1]['COM_delta_mm'],item['COM_delta_mm'],abs_tol=1e-8)
    assert math.isclose(actual['stages'][-1]['angle_delta_deg'],item['orientation_delta_deg'],abs_tol=1e-8)
    assert actual['final_COM_target_pass']==item['COM_pass']
    assert actual['final_angle_target_pass']==item['orientation_pass']
print('PASS: FCE13 hashes, six endpoints, original baseline and independently recalculated pose comparisons; acceptance remains failed')
