"""Run existing GMAT with isolated outputs and bounded native lunar studies."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime as dt
import hashlib
import json
import subprocess
import time

from generate_decks import ROOT, GMAT, deck

CASES = []
for apogee in (100, 1000, 10000):
    stem = f'p100_a{apogee}'
    CASES.append(deck(stem + '_d20_s120', apogee_km=apogee))
    CASES.append(deck(stem + '_d20_s60', apogee_km=apogee, max_step=60))
    CASES.append(deck(stem + '_d40_s120', apogee_km=apogee, degree=40))
    CASES.append(deck(stem + '_d80_s120_30d', apogee_km=apogee, degree=80, days=(7, 30)))
    CASES.append(deck(stem + '_lp165p_d20_s120_30d', apogee_km=apogee,
                      gravity='LP165P.cof', days=(7, 30)))
    CASES.append(deck(stem + '_i0_d20_s120', apogee_km=apogee, inclination=0))

(ROOT / 'CASES.json').write_text(json.dumps(CASES, indent=2) + '\n')


def run(case):
    name = case['name']
    command = [str(GMAT / 'bin/GmatConsole'), '--startup_file', str(ROOT / 'source/gmat_startup_file.txt'),
               '--logfile', str(ROOT / 'runs' / (name + '_gmat.log')),
               '--run', case['deck'], '--exit']
    started = dt.datetime.now(dt.timezone.utc)
    log = ROOT / 'runs' / (name + '_console.log')
    status = 'finished'
    start = time.monotonic()
    with log.open('w') as stream:
        try:
            process = subprocess.run(command, cwd=GMAT / 'bin', stdout=stream,
                                     stderr=subprocess.STDOUT, timeout=240)
            code = process.returncode
        except subprocess.TimeoutExpired:
            status, code = 'timeout_240s', None
    text = log.read_text(errors='replace')
    result = {**case, 'command': command, 'cwd': str(GMAT / 'bin'),
              'started_utc': started.isoformat(), 'wall_seconds': time.monotonic() - start,
              'execution_status': status, 'exit_code': code,
              'native_completion_message': 'Mission run completed.' in text,
              'console_log': str(log),
              'deck_sha256': hashlib.sha256(Path(case['deck']).read_bytes()).hexdigest()}
    (ROOT / 'runs' / (name + '_execution.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(name, status, 'return', code, 'completed', result['native_completion_message'],
          'wall', round(result['wall_seconds'], 2), flush=True)
    return result


if __name__ == '__main__':
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for task in as_completed([pool.submit(run, case) for case in CASES]):
            results.append(task.result())
            (ROOT / 'EXECUTIONS.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Finished', len(results), 'bounded attempts', flush=True)
