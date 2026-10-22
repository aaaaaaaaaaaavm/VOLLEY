"""Verify captured public artifacts and reproduce their algebra without writing files."""
from pathlib import Path
import hashlib
import json
import math
import sys
sys.dont_write_bytecode = True
from reproduce_bounds import build

ROOT = Path(__file__).resolve().parent

def compare(expected, actual, path='root'):
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and expected.keys() == actual.keys(), path
        return sum(compare(value, actual[key], path + '.' + key) for key, value in expected.items())
    if isinstance(expected, list):
        assert isinstance(actual, list) and len(expected) == len(actual), path
        return sum(compare(a, b, f'{path}[{i}]') for i, (a, b) in enumerate(zip(expected, actual)))
    if isinstance(expected, bool):
        assert expected is actual, path
        return 0
    if isinstance(expected, (float, int)):
        assert isinstance(actual, (float, int)) and not isinstance(actual, bool), path
        assert math.isfinite(expected) and math.isfinite(actual), path
        assert math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-9), (path, expected, actual)
        return 1
    assert expected == actual, (path, expected, actual)
    return 0

def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    for name, identity in manifest['files'].items():
        path = ROOT / name
        assert path.is_file() and path.stat().st_size == identity['bytes'], name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == identity['sha256'], name
    captured = json.loads((ROOT / 'NUMERICAL_BOUNDS.json').read_text())
    recreated = build()
    count = compare(captured, recreated)
    mismatch = next(row for row in recreated['source_provenance']
                    if row['study'] == 'C0-S2' and row['source'].endswith('.md'))
    assert mismatch['matches'] is False
    assert mismatch['stored_sha256'] == manifest['known_C0_S2_criteria_mismatch']['stored_result_criteria_sha256']
    assert mismatch['current_sha256'] == manifest['known_C0_S2_criteria_mismatch']['supplied_criteria_sha256']
    assert all(recreated['checks'].values())
    print(f'PASS: {len(manifest["files"])} artifact hashes, {count} numerical fields, {len(recreated["checks"])} algebraic checks.')
    print('Known C0-S2 criteria-hash mismatch retained; no orbital propagation, provider or hardware validation performed.')

if __name__ == '__main__':
    main()
