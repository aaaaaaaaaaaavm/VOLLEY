#!/usr/bin/env python3
"""Bind the current ACR1 public route and headline values to the actual captured package."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    subprocess.run([sys.executable,str(ROOT/'validation/acr1/check_capture.py')],check=True)
    d=json.loads((ROOT/'validation/acr1/ENGINEERING_DEFINITION_R1.json').read_text())
    mass=d['mass_basis']
    expected=f"{mass['CAD_dry_kg']:.6f}"
    if expected!='149.556720' or abs(mass['device_including_allowance_kg']-mass['CAD_dry_kg']-7)>1e-10:raise SystemExit('ACR1 current mass boundary changed; reconcile public surfaces')
    for name in ['README.md','SUMMARY.md','docs/CURRENT_NUMERICAL_EVIDENCE.md','docs/STATE_OF_THE_PROJECT.md','cad/README.md','CAD_BRIEF.md']:
        text=(ROOT/name).read_text()
        for token in ['ACR1','149.556720']:
            if token not in text:raise SystemExit(f'{name}: missing current ACR1 evidence token {token}')
    for name in ['README.md','SUMMARY.md','docs/CURRENT_NUMERICAL_EVIDENCE.md']:
        text=(ROOT/name).read_text().lower()
        if 'pretrimmed spring'not in text or 'no propellant or initial wet-mass advantage'not in text:raise SystemExit(f'{name}: current mission conclusion missing')
    print('PASS: current ACR1 public surfaces agree with geometry/mass/mission capture')
if __name__=='__main__':main()
