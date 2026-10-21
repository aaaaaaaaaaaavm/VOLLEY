"""Check immutable captured evidence and independent mechanical identities."""
from pathlib import Path
import gzip, hashlib, json, math

H = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads((H / p).read_text())
manifest = load('MANIFEST.json')
for name, rec in manifest['files'].items():
    p = (H / name).resolve()
    assert p.is_relative_to(H) and p.is_file(), name
    assert sha(p.read_bytes()) == rec['sha256'], name

cad = load('cad/NATIVE_CAD.json')
assert len(cad['poses']) == 30
assert all(not r['invalid_parts'] and not r['penetrations'] and r['step_valid'] for r in cad['poses'])
assert len(load('cad/INDEPENDENT_STEP.json')['cases']) == 30
assert all(r['valid'] for r in load('cad/INDEPENDENT_STEP.json')['cases'])
sweep = load('CONTINUOUS_SWEEPS.json')['cases']
assert len(sweep) == 28 and all(r['rigid_translation_checked'] and not r['penetrations'] for r in sweep)
parts = load('parts/INDEX.json')['parts']
assert len(parts) == 70
independent = load('parts/INDEPENDENT_STEP.json')['parts']
assert len(independent) == 70 and all(r['independently_valid'] for r in independent)
surface = load('contact_geometry_surfaces/SURFACE_AUDIT.json')['cases']
assert sum(len(r['parts']) for r in surface) == 70
assert max(p['relative_volume_error'] for r in surface for p in r['parts']) < 4e-5
gap = load('RECEIVER_GAP_CHECK.json')
assert len(gap) == 24 and all(r['intersection_mm3'] < 1e-5 for r in gap)
assert abs(min(r['minimum_distance_mm'] for r in gap) - 4) < 1e-6

count = 0
for rev in ['FM02', 'FM03_stem8', 'FM03', 'FM06']:
    data = load('receiver/fea/' + rev + '/CHECKED_RESULTS.json')
    for row in data['native_cases']:
        count += 1
        assert row['force_balance_relative_error'] < 1e-4
        assert row['moment_balance_relative_error'] < 1e-4
        directory, pattern = row['case'].split('/')
        for ext in ['inp', 'dat']:
            p = H / 'receiver/fea' / rev / directory / (pattern + '.' + ext + '.gz')
            if p.exists():
                assert sha(gzip.decompress(p.read_bytes())) == row['file_hashes'][pattern + '.' + ext]
assert count == 52
lineage = load('COMPONENT_GEOMETRY_LINEAGE.json')['checks']
assert len(lineage) == 4
assert all(r.get('symmetric_volume_difference_mm3', r.get('fixture_material_missing_from_current_fork_mm3', 1)) < 1e-5 for r in lineage)
tine = load('tine/SUMMARY.json')
assert len(tine['native_cases']) == 4 and len(tine['linear_scaled_sensitivity_cases']) == 40
for r in tine['native_cases']:
    for ext in ['inp', 'dat']:
        p = H / 'tine' / ('h' + format(r['h_mm'], 'g')) / ('unit.' + ext + '.gz')
        assert sha(gzip.decompress(p.read_bytes())) == r['hashes']['unit.' + ext]
    assert math.dist(r['reaction_N'], [0, 0, 1]) < 1e-4
assert abs(109**3 / (3 * 69000 * (12 * 8.5**3 / 12)) - tine['Euler_Bernoulli_compliance_mm_per_N']) < 1e-12
fits = load('FIT_SENSITIVITY.json')['cases']
assert len(fits) == 1215 and sum(not r['positive_parametric_fit'] for r in fits) == 1117

inputs = load('contact/campaign/INPUTS.json')
runs = load('contact/campaign/RUNS.json')['cases']
assert len(runs) == 12
assert inputs['CAD_sha256'] == sha((H / 'mechanism.py').read_bytes())
assert inputs['cpp_sha256'] == sha((H / 'contact/captured/feeder_surface.cpp').read_bytes())
for r in runs:
    for name, expected in r['hashes'].items():
        assert sha((H / 'contact/campaign' / name).read_bytes()) == expected
    assert r['exit_code'] in {0, 10, 11}
assessment = load('CONTACT_ASSESSMENT.json')
assert assessment['engineering_acceptance'] == 'not_established'
print('PASS: captured geometry, exchange, load, fit and native-contact identities. No hardware acceptance follows.')
