"""Exact B-rep spot checks independent of the solver's triangle contacts."""
from pathlib import Path
import argparse, csv, hashlib, json
import FreeCAD as App
import Part
from mechanism import shapes, State

H = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('campaign')
args = p.parse_args()
C = Path(args.campaign).resolve()
out = []

def posed(shape, xyz, q):
    s = shape.copy()
    s.translate(-s.Solids[0].CenterOfMass)
    s.Placement = App.Placement(App.Vector(*xyz), App.Rotation(q[1], q[2], q[3], q[0])).multiply(s.Placement)
    return s

for record in sorted(C.glob('*.record.json')):
    info = json.loads(record.read_text())
    if info['label'] != 'time_refinement': continue
    src = C / (info['case_id'] + '.csv')
    rows = list(csv.DictReader(src.open()))
    L = 113.5 if info['size'] == '1U' else 340.5
    parts, _ = shapes(L, State(gate=120, bolt=0))
    checks = []
    for time in [0, 8, 10, 26.5]:
        row = min(rows, key=lambda r: abs(float(r['time_s']) - time))
        if abs(float(row['time_s']) - time) > .011: continue
        payload = posed(parts['payload'], [float(row[k])*1000 for k in ['payload_x_m','payload_y_m','payload_z_m']], [float(row[k]) for k in ['qw','qx','qy','qz']])
        fork = posed(parts['fork_body'], [float(row[k])*1000 for k in ['fork_x_m','fork_y_m','fork_z_m']], [float(row[k]) for k in ['fork_qw','fork_qx','fork_qy','fork_qz']])
        overlap = payload.common(fork)
        box = overlap.BoundBox
        r = {'time_s': float(row['time_s']), 'payload_fork_intersection_mm3': overlap.Volume,
             'intersection_bounds_mm': [box.XMin,box.YMin,box.ZMin,box.XMax,box.YMax,box.ZMax] if overlap.Volume > 1e-8 else None,
             'minimum_distance_mm': payload.distToShape(fork)[0]}
        checks.append(r)
        print(info['case_id'], time, r['payload_fork_intersection_mm3'], flush=True)
    out.append({'case_id': info['case_id'], 'size': info['size'], 'dt_s': info['dt_s'], 'csv_sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'checks': checks})
(H/'DYNAMIC_BREP_SPOTS.json').write_text(json.dumps({'cases':out,'boundary':'Four discrete-time payload/fork checks per nominal refinement case, using full native B-rep and actual solver COM/quaternions. No all-component or continuous dynamic nonpenetration claim. Positive overlap is retained and precludes a zero-interference claim for the corresponding simulated state.'},indent=2)+'\n')
