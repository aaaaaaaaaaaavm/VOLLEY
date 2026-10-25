"""Regression fixtures for unit-specific numerical budgets and exact decisions."""
import json
from pathlib import Path
from reproduce_and_compare import compare,comparison_policy
HERE=Path(__file__).resolve().parent

def main():
    fixtures=json.loads((HERE/'REPRODUCTION_COMPARISON_FIXTURES.json').read_text())['cases'];records=[]
    for fixture in fixtures:
        diagnostic={}
        try:
            compare(fixture['reference'],fixture['reproduced'],fixture['id'],profile=fixture['profile'],diagnostics=diagnostic)
            passed=True
        except AssertionError:
            passed=False
        assert passed==fixture['expect_pass'],fixture['id']
        records.append(dict(id=fixture['id'],expected_pass=fixture['expect_pass'],actual_pass=passed,diagnostics=diagnostic))
    report=dict(scope='Comparator regression evidence only; no physics source/results or acceptance thresholds changed',
                all_fixtures_pass=True,fixture_count=len(records),comparison_policy=comparison_policy('campaign'),fixtures=records)
    (HERE/'REPRODUCTION_COMPARISON_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(records)} comparator fixtures; observed CI mass pair accepted; meaningful changes and discrete outcomes rejected')

if __name__=='__main__':main()
