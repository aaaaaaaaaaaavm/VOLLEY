"""Report exact paths when committed mission evidence differs on another runner."""
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))


def differences(a, b, path=()):
    from campaign_allocation import numerical_match
    if type(a) is not type(b):
        yield path, a, b
    elif isinstance(a, dict):
        if a.keys() != b.keys():
            yield path+('keys',), list(a), list(b)
        for k in a.keys() & b.keys():
            yield from differences(a[k], b[k], path+(k,))
    elif isinstance(a, list):
        if len(a) != len(b):
            yield path+('length',), len(a), len(b)
        for i, (x, y) in enumerate(zip(a, b)):
            yield from differences(x, y, path+(i,))
    elif isinstance(a, float):
        if not numerical_match(a, b, path):
            yield path, a, b
    elif a != b:
        yield path, a, b


def main():
    failed = False
    for name in ['campaign_allocation', 'terminal_timing']:
        module = importlib.import_module(name)
        stored = json.loads((ROOT/'analysis/results'/f'{name}.json').read_text())
        fresh = module.build()
        delta = list(differences(stored, fresh))
        print(name, 'different leaves:', len(delta), flush=True)
        for path, before, after in delta[:30]:
            print(path, 'stored=', before, 'fresh=', after, flush=True)
        failed |= bool(delta)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
