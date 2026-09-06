"""A24-R: compare my fixed-cell manifest with the current payload-family reference."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'analysis/results'
OUTPUT=RESULTS/'cell_manifest_reference.json'
def calculate():
    paths=[RESULTS/'cell_manifest.json',RESULTS/'payload_family.json']
    cell,family=[json.loads(p.read_text()) for p in paths]
    c=next(x for x in cell['classes'] if x['tag']=='3U CubeSat')
    f=next(x for x in family['classes'] if x['tag']=='3U CubeSat')
    error=abs(c['kg_per_satellite']/f['kg_per_satellite']-1)
    checks={'count':c['n_per_load']==f['n_per_load']==12,'mass_reference':error<=0.01}
    return {'run':'A24-R','evidence':'model consistency only','declaration_commit':'e0a3cf611824efe19d045cab4fc73dcdfaa7abca',
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            'fixed_cell_kg_per_satellite':c['kg_per_satellite'],'reference_kg_per_satellite':f['kg_per_satellite'],
            'relative_difference':error,'checks':checks,'pass':all(checks.values()),
            'original_a24_bands':cell['bands']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();result=calculate()
    if a.check:
        if json.loads(OUTPUT.read_text())!=result: raise SystemExit('A24-R result is stale')
        print('A24-R current reference reproduced; historical A24 bands retained')
    else: OUTPUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
