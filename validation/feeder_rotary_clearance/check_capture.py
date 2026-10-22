"""Validate the captured interval, geometry delta and exchange records."""
from pathlib import Path
import hashlib,json,math
H=Path(__file__).resolve().parent
load=lambda n:json.loads((H/n).read_text())
for name,r in load('MANIFEST.json')['files'].items():
    p=(H/name).resolve()
    assert p.is_relative_to(H) and p.is_file(),name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],name
d=load('CONTINUOUS_ROTARY_CLEARANCE.json')
assert d['geometry_revision']=='FM07-R6-CANDIDATE' and d['all_passed'] and len(d['cases'])==4
for name,digest in d['source_sha256'].items():
    assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,name
for c in d['cases']:
    assert c['passed'] and not c['unresolved'] and c['all_intervals_covered']
    assert c['angle_range_deg']==[0,90]
    by_part={}
    for r in c['certificates']:
        lo,hi=r['interval_deg']
        movement=2*c['radius_upper_bound_mm']*math.sin(math.radians(hi-lo)/4)
        assert abs(movement-r['displacement_bound_mm'])<1e-10
        assert r['native_gap_mm']-movement-d['numerical_guard_mm']>0
        by_part.setdefault(r['part'],[]).append((lo,hi))
    for part,intervals in by_part.items():
        cursor=0
        for lo,hi in sorted(intervals):
            assert abs(lo-cursor)<1e-10,(part,lo,cursor)
            cursor=hi
        assert cursor==90
    assert len(by_part)+1==c['stationary_obstacles']
    assert c['axisymmetric_hinge']['source_union_difference_mm3']<1e-5
    assert c['axisymmetric_hinge']['guarded_lower_bound_mm']>0
x=load('DELTA_AND_EXPORT.json');assert x['source_change_whitelist_verified']
for name,digest in x['source_sha256'].items():
    assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,name
assemblies=[r for r in x['records'] if r['kind']=='assembly']
assert len(assemblies)==8
assert all(r['subset_verified'] and not r['pair_intersections'] for r in assemblies)
assert all(abs(r['removed_volume_mm3']-41)<1e-5 for r in assemblies)
assert all(r['max_unchanged_part_difference_mm3']<1e-5 for r in assemblies)
assert len(load('INDEPENDENT_STEP.json')['cases'])==10
assert all(r['valid'] and abs(r['volume_difference_mm3'])<0.01 for r in load('INDEPENDENT_STEP.json')['cases'])
assert not load('reference_r5/CONTINUOUS_ROTARY_CLEARANCE.json')['all_passed']
print('PASS: 4 complete rotary interval screens; 8 native/STEP assemblies; 2 gate STEP; restricted material-removal delta. Loaded fit and D27 remain separate.')
