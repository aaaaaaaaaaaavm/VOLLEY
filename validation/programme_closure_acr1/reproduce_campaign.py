"""Isolated reproduction of search,feasible campaign,negative and fault branches."""
import json
import shutil
import tempfile
from pathlib import Path

from reproduce_and_compare import compare,comparison_policy

HERE=Path(__file__).resolve().parent


def main():
    # Source functions use their own package root; loading a copied module is
    # enough to ensure no private filesystem dependency feeds the reproduction.
    import importlib.util
    diagnostics={}
    from check_reproduction_comparison import main as check_comparison_fixtures
    check_comparison_fixtures()
    with tempfile.TemporaryDirectory(prefix='volley-lunar-campaign-') as tmp:
        dest=Path(tmp)
        for name in ['lunar_campaign.py','campaign_inputs.json','study_inputs.json']:
            shutil.copyfile(HERE/name,dest/name)
        shutil.copytree(HERE/'inputs',dest/'inputs')
        spec=importlib.util.spec_from_file_location('isolated_campaign',dest/'lunar_campaign.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        config=json.loads((dest/'campaign_inputs.json').read_text())
        expected=json.loads((HERE/'campaign/T5_R20_searched.json').read_text())
        policy=[(x['index'],x['sign'],x['roll_deg']) for x in expected['policy']]
        searched,search=module.beam_search(module.Campaign(config,config['authority_cases'][3]))
        assert searched==policy
        summary=json.loads((HERE/'CAMPAIGN_RESULTS.json').read_text())
        compare(summary['search'],search,profile='campaign',diagnostics=diagnostics)
        cases=[('T5_R20_searched',3,None,False),('T5_R5_searched',2,None,False),('unresolved_shared_path_failure',3,6,True)]
        for name,index,failed,blocked in cases:
            original=json.loads((HERE/'campaign'/(name+'.json')).read_text())
            actual=module.Campaign(config,config['authority_cases'][index]).run(policy,failed_slot=failed,blocked=blocked)
            actual['policy_name']=original['policy_name']
            compare(original,actual,name,profile='campaign',diagnostics=diagnostics)
    result=dict(study='PCS-LUNAR-CAMPAIGN-01',isolated_reproduction_pass=True,
                search_candidates=search['evaluated_candidates'],
                reproduced_cases=[x[0] for x in cases],
                comparison_policy=comparison_policy('campaign'),
                comparison_fixture_count=12,
                runtime_diagnostics='Printed to stdout; hardware-dependent errors are not frozen metadata.',
                native_GMAT_rerun=False,
                scope='Actual source search,finite-host state/resource history,negative cadence andblocked-path fault branch reproduced from copied public inputs. Independent native astrodynamics is captured separately.')
    (HERE/'CAMPAIGN_REPRODUCTION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(numerical_comparison_diagnostics=diagnostics),indent=2))
    print('PASS: isolated7152-candidate search,12-release campaign,missed-slot case andshared-path abort reproduce.')


if __name__=='__main__':main()
