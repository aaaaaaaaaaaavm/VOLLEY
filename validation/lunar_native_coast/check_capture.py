"""Check identities and native-output consistency; this is not mission acceptance."""
from pathlib import Path
import hashlib
import gzip
import json

ROOT = Path(__file__).resolve().parent
record = json.loads((ROOT / 'MANIFEST.json').read_text())
for name, expected in record['files'].items():
    path = ROOT / name
    assert path.is_file() and path.stat().st_size == expected['bytes'], name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected['sha256'], name
results = json.loads((ROOT / 'RESULTS.json').read_text())
for case in results['cases']:
    path = ROOT / 'decks' / Path(case['deck']).name
    if 'deck_sha256' in case:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == case['deck_sha256'], path
    if 'final_elapsed_days' not in case:
        continue
    history = ROOT / 'runs' / (case['name'] + '.csv')
    if history.exists():
        stream = history.open('rb')
    else:
        stream = gzip.open(history.with_suffix('.csv.gz'), 'rb')
    with stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert actual == case['raw_history_sha256'], case['name']
    assert case['all_output_values_finite'], case['name']
    assert case['radius_reconstruction_max_abs_km'] < 1e-7, case['name']
    assert case['eccentricity_reconstruction_max_abs'] < 1e-10, case['name']
    for point in case['checkpoints']:
        if point['reached']:
            assert abs(point['elapsed_s'] - point['requested_day'] * 86400) < .001
    if case['termination'] == 'native_spherical_radius_stop':
        assert abs(case['checkpoints'][-1]['radius_km'] - results['reference_radius_km']) < 1e-3
        assert case['sampled_min_spherical_altitude_km'] > -1e-5, case['name']
print('PASS: captured file identities and stated native invariants/checkpoint/stop consistency; terrain, lifetime and physical validation remain open')
