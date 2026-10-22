"""Continuous nominal rotary-clearance bounds for the unchanged FM07-R5 gate.

For any angle in an interval centred on theta, every point of the rotating
solid moves at most 2*R*sin(interval_width/4) from its midpoint position.
Distance to a fixed closed obstacle is Lipschitz under this displacement.
Thus a native B-rep distance greater than this bound plus the stated numerical
guard certifies clearance over the whole interval, not just at a sample.
The coaxial hinge shaft is checked separately using rotational symmetry.
"""
from pathlib import Path
import dataclasses
import hashlib
import json
import math
import platform
import sys
import time

SOURCE = Path(__file__).parent
sys.path.insert(0, str(SOURCE))
import FreeCAD as App
import Part
from mechanism import REVISION, cycle, shapes

OUT = Path(__file__).parent
GUARD_MM = 1e-5
VOLUME_CHECK_MM3 = 1e-5
MAX_DEPTH = 16


def difference(a, b):
    overlap = a.common(b).Volume
    return abs(a.Volume - overlap) + abs(b.Volume - overlap)


def run_case(size, length, previous_name, before_state, next_name, after_state):
    before, _ = shapes(length, before_state)
    after, _ = shapes(length, after_state)
    moving = 'sled_front_stop'
    differences = [k for k in dataclasses.asdict(before_state)
                   if getattr(before_state, k) != getattr(after_state, k)]
    assert differences == ['exit_gate_deg'], differences
    for name in before:
        assert before[name].isValid() and after[name].isValid(), name
        if name != moving:
            assert difference(before[name], after[name]) < VOLUME_CHECK_MM3, name
    axis = App.Vector(length + 9.5 + before_state.sled, -12, 0)
    direction = App.Vector(0, 0, 1)
    start_angle = before_state.exit_gate_deg
    a0, a1 = sorted([start_angle, after_state.exit_gate_deg])
    gate = before[moving]
    endpoint = gate.copy()
    endpoint.rotate(axis, direction, -(after_state.exit_gate_deg - start_angle))
    endpoint_error = difference(endpoint, after[moving])
    assert endpoint_error < VOLUME_CHECK_MM3, endpoint_error
    box = gate.BoundBox
    radius = max(math.hypot(x-axis.x, y-axis.y)
                 for x in [box.XMin, box.XMax]
                 for y in [box.YMin, box.YMax])

    # This exact source-derived union consists of three coaxial cylinders.
    # Any rotation around the axis leaves it invariant, so its distance from
    # a rigidly rotating gate is invariant as well. Verify the modeled shaft
    # matches this union before applying that analytic premise.
    shaft = Part.makeCylinder(1.5, 42.4, App.Vector(axis.x, axis.y, 8.8))
    shaft = shaft.fuse(Part.makeCylinder(3, 1.6, App.Vector(axis.x, axis.y, 8.2)))
    shaft = shaft.fuse(Part.makeCylinder(3, 1.6, App.Vector(axis.x, axis.y, 50.2)))
    shaft_error = difference(shaft, before['exit_hinge_pin'])
    assert shaft_error < VOLUME_CHECK_MM3, shaft_error
    hinge_gap = gate.distToShape(shaft)[0]
    assert hinge_gap > GUARD_MM, hinge_gap
    fixtures = {k:v for k,v in before.items()
                if k not in [moving, 'exit_hinge_pin']}
    leaves = []
    failures = []
    cache = {}
    distance_calls = 0
    def at(angle):
        if angle not in cache:
            shape = gate.copy()
            shape.rotate(axis, direction, -(angle-start_angle))
            cache[angle] = shape
        return cache[angle]
    def certify(lo, hi, names, depth):
        nonlocal distance_calls
        mid = (lo+hi)/2
        displacement = 2*radius*math.sin(math.radians(hi-lo)/4)
        sh = at(mid)
        retry = []
        for name in names:
            distance = sh.distToShape(fixtures[name])[0]
            distance_calls += 1
            bound = distance-displacement-GUARD_MM
            if bound > 0:
                leaves.append(dict(part=name, interval_deg=[lo,hi], midpoint_deg=mid,
                                   native_gap_mm=distance, displacement_bound_mm=displacement,
                                   guarded_clearance_lower_bound_mm=bound, depth=depth))
            elif distance <= GUARD_MM:
                witness = sh.distToShape(fixtures[name])
                intersection = sh.common(fixtures[name]).Volume
                failures.append(dict(part=name, interval_deg=[lo,hi],
                                     sampled_angle_deg=mid, native_gap_mm=distance,
                                     sampled_intersection_mm3=intersection,
                                     classification='sampled_penetration' if intersection > VOLUME_CHECK_MM3 else 'sampled_zero_clearance_contact',
                                     witness_points_mm=[[[p.x,p.y,p.z] for p in pair] for pair in witness[1]],
                                     displacement_bound_mm=displacement))
            elif depth < MAX_DEPTH:
                retry.append(name)
            else:
                failures.append(dict(part=name, interval_deg=[lo,hi],
                                     native_gap_mm=distance, displacement_bound_mm=displacement))
        if retry:
            certify(lo, mid, retry, depth+1)
            certify(mid, hi, retry, depth+1)
    certify(a0, a1, list(fixtures), 0)
    # Verify each obstacle's certified intervals tile the entire angle range.
    coverage = {}
    for name in fixtures:
        intervals = sorted(x['interval_deg'] for x in leaves if x['part'] == name)
        cursor = a0
        for lo, hi in intervals:
            if abs(lo-cursor) >= 1e-10:
                coverage[name] = False
                break
            cursor = hi
        else:
            coverage[name] = abs(cursor-a1) < 1e-10
    result = dict(payload=size, phase=next_name, from_pose=previous_name,
                  angle_range_deg=[a0,a1], direction='opening' if after_state.exit_gate_deg > start_angle else 'closing',
                  radius_upper_bound_mm=radius, endpoint_shape_difference_mm3=endpoint_error,
                  stationary_obstacles=len(fixtures)+1,
                  axisymmetric_hinge=dict(source_union_difference_mm3=shaft_error,
                                          invariant_clearance_mm=hinge_gap,
                                          guarded_lower_bound_mm=hinge_gap-GUARD_MM),
                  distance_evaluations=distance_calls, unique_midpoint_poses=len(cache),
                  max_subdivision_depth=max((x['depth'] for x in leaves), default=0),
                  all_intervals_covered=all(coverage.values()),
                  minimum_guarded_lower_bound_mm=min([hinge_gap-GUARD_MM]+[x['guarded_clearance_lower_bound_mm'] for x in leaves]),
                  unresolved=failures, certificates=leaves)
    result['passed'] = not failures and result['all_intervals_covered']
    return result


start = time.time()
record = dict(study='FM07-R5 continuous nominal rotary-clearance supplement',
              geometry_revision=REVISION,
              method='Adaptive native B-rep distance with a conservative rigid-rotation displacement bound; source-verified axisymmetric hinge exception.',
              numerical_guard_mm=GUARD_MM,
              boundary='Nominal rigid geometry only; does not establish manufacturing tolerance, loaded fit, actuator capability, contact convergence, reliability or D27 selection.',
              tools=dict(FreeCAD=list(App.Version()), OCC=Part.OCC_VERSION, Python=platform.python_version()),
              source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [SOURCE/'mechanism.py', SOURCE/'fm06.py', Path(__file__)]},
              cases=[])
for size, length in [('1U',113.5),('3U',340.5)]:
    phases = cycle(length)
    for (old, st), (new, en) in zip(phases, phases[1:]):
        if st.exit_gate_deg == en.exit_gate_deg:
            continue
        result = run_case(size, length, old, st, new, en)
        record['cases'].append(result)
        record['elapsed_s'] = time.time()-start
        record['all_passed'] = all(c['passed'] for c in record['cases']) and len(record['cases']) == 4
        (OUT/'CONTINUOUS_ROTARY_CLEARANCE.json').write_text(json.dumps(record,indent=2)+'\n')
        print(size,new,'passed',result['passed'],'distance checks',result['distance_evaluations'],
              'minimum bound mm',result['minimum_guarded_lower_bound_mm'],flush=True)
print('Elapsed',time.time()-start,flush=True)
assert record['all_passed']
