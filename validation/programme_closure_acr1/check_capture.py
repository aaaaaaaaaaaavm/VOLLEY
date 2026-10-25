"""Verify identities and independent numerical invariants for PCS-ACR1-01."""
import gzip
import hashlib
import json
import math
from pathlib import Path

from lunar_native import HERE, parse_report, sha


def main():
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,expected in manifest['files'].items():
        p=HERE/name
        assert p.stat().st_size==expected['bytes'],name
        assert sha(p)==expected['sha256'],name
    sources=json.loads((HERE/'INPUT_SOURCE_MANIFEST.json').read_text())
    for item in sources:assert sha(HERE/item['path'])==item['sha256'],item['path']
    results=json.loads((HERE/'STUDY_RESULTS.json').read_text())
    assert results['source_sha256']==sha(HERE/'complete_studies.py')
    assert results['study_inputs_sha256']==sha(HERE/'study_inputs.json')
    for name,expected in results['inputs_sha256'].items():assert sha(HERE/'inputs'/name)==expected
    c=json.loads((HERE/'study_inputs.json').read_text())['lunar']
    coast=json.loads((HERE/'LUNAR_NATIVE_RESULTS.json').read_text())
    assert coast['source_identity']['generator_sha256']==sha(HERE/'lunar_native.py')
    assert coast['source_identity']['inputs_sha256']==sha(HERE/'study_inputs.json')
    assert len(coast['cases'])==18
    for case in coast['cases']:
        base=HERE/'native'/case['case']
        assert sha(base.with_suffix('.script'))==case['script_sha256']
        assert sha(base.with_suffix('.txt.gz'))==case['report_sha256']
        parsed=parse_report(base.with_suffix('.txt.gz'),c)
        for key in ['final_day','min_sampled_altitude_km','passes_declared_sampled_floor']:
            assert parsed[key]==case[key],(case['case'],key)
        script=base.with_suffix('.script').read_text()
        assert "Luna.SpiceFrameId = 'MOON_PA'" in script
        assert "SolarSystem.EphemerisSource = 'DE421'" in script
        assert 'MoonFrame.Axes = MJ2000Eq' in script
        assert case['reaches_duration'] or abs(case['min_sampled_altitude_km'])<1e-4
    disposal=json.loads((HERE/'DISPOSAL_NATIVE_RESULTS.json').read_text())
    assert disposal['input_results_sha256']==sha(HERE/'STUDY_RESULTS.json')
    assert disposal['generator_sha256']==sha(HERE/'disposal_native.py')
    assert len(disposal['cases'])==24 and disposal['all_cases_hit']
    for case in disposal['cases']:
        base=HERE/'disposal_native'/case['case']
        # Names contain decimal duration multipliers; append extensions.
        script=Path(str(base)+'.script');history=Path(str(base)+'.txt.gz')
        assert sha(script)==case['script_sha256']
        assert sha(history)==case['report_sha256']
        expected_mass_use=c['disposal_thrust_N']*case['burn_duration_s']/(9.80665*c['disposal_Isp_s'])
        assert abs(expected_mass_use-case['native_propellant_used_kg'])<1e-7
        assert case['native_impact_time_s']<86400
        assert abs(case['final_radius_km']-c['reference_radius_km'])<1e-5
    navigation=json.loads((HERE/'NAVIGATION_REQUIREMENTS.json').read_text())
    assert navigation['source_sha256']==sha(HERE/'navigation_requirements.py')
    assert navigation['inputs_sha256']==sha(HERE/'study_inputs.json')
    assert navigation['finite_difference_relative_refinement']<1e-6
    assert navigation['monte_carlo'][-1]['samples']==16384
    assert all(results['verification'][k] for k in ['all_engine_only_disposal_cases_hit','finite_burn_step_refinement_pass'])
    # Necessary mass bound is independent of candidate optimization.
    mass=results['installed_comparison']
    assert math.isclose(mass['dry_penalty_kg']-mass['fuel_reserve_kg'],mass['optimistic_lower_net_mass_penalty_even_if_all_20kg_fuel_saved_kg'],abs_tol=1e-12)
    assert results['host_demand']['source_cells']==64
    assert len(results['host_demand']['eight_native_state_bounds'])==8
    campaign=json.loads((HERE/'CAMPAIGN_RESULTS.json').read_text())
    assert campaign['verification']['source_sha256']==sha(HERE/'lunar_campaign.py')
    assert campaign['verification']['inputs_sha256']==sha(HERE/'campaign_inputs.json')
    assert campaign['search']['evaluated_candidates']==7152
    assert len(campaign['cases'])==20
    for case in campaign['cases']:
        assert abs(case['mass_closure_residual_kg'])<1e-9
        assert case['max_linear_momentum_residual_kg_m_s']<1e-7
        assert case['max_angular_momentum_residual_kg_m2_s']<1e-7
        assert case['peak_torque_N_m']<=case['authority']['torque_N_m']*(1+1e-7)
        assert case['peak_rate_deg_s']<=case['authority']['rate_deg_s']*(1+1e-7)
        used=[x['payload'] for x in case['releases'] if x['released']]
        assert len(used)==len(set(used))
        for release in case['releases']:
            if release['released']:
                assert abs(release['before_mass_kg']-release['after_mass_kg']-4)<1e-10
                assert 1<=release['command_m_s']<=3
                assert release['coast_requirement_s']==400
        if case['nominal_full_manifest_pass']:
            assert case['released_payloads']==12 and case['final_propellant_kg']>=8
            assert sum(x['sign']==1 for x in case['releases'])==6
            assert sum(x['sign']==-1 for x in case['releases'])==6
    assert campaign['verification']['half_max_step_final_position_difference_m']<1e-4
    native=json.loads((HERE/'CAMPAIGN_NATIVE_RESULTS.json').read_text())
    assert native['generator_sha256']==sha(HERE/'campaign_native.py')
    assert native['campaign_sha256']==sha(HERE/'campaign/T5_R20_searched.json')
    assert len(native['cases'])==3
    for case in native['cases']:
        assert sha(HERE/'campaign_native'/(case['mode']+'.script'))==case['script_sha256']
        assert sha(HERE/'campaign_native'/(case['mode']+'_host.txt.gz'))==case['host_history_sha256']
        if case['mode']=='point_mass':
            assert case['final_position_difference_vs_python_m']<0.1
            assert case['final_velocity_difference_vs_python_m_s']<1e-4
            assert case['final_mass_difference_kg']<1e-7
        else:
            assert len(case['payload_lifetime'])==12
            for child in case['payload_lifetime']:
                path=HERE/'campaign_native'/(case['mode']+f"_P{child['payload']}.txt.gz")
                assert sha(path)==child['history_sha256']
                assert child['native30day_sampled_floor_pass']
    post=json.loads((HERE/'CAMPAIGN_DISPOSAL_RESULTS.json').read_text())
    assert post['generator_sha256']==sha(HERE/'campaign_disposal.py')
    assert post['all_native_hit_within24h'] and post['all_fit_independent8kg']
    assert len(post['cases'])==3
    for case in post['cases']:
        assert sha(HERE/'campaign'/(case['case']+'.json'))==case['source_campaign_sha256']
        assert sha(HERE/'campaign_disposal'/(case['case']+'.script'))==case['script_sha256']
        assert sha(HERE/'campaign_disposal'/(case['case']+'.txt.gz'))==case['history_sha256']
        assert case['native_disposal_propellant_kg']<8
        assert case['native_postcampaign_to_sphere_s']<86400
    assert json.loads((HERE/'CAMPAIGN_REPRODUCTION_CHECK.json').read_text())['isolated_reproduction_pass']
    portable=json.loads((HERE/'portable_replay_capture/REPLAY_RECEIPT.json').read_text())
    assert portable['adapter_sha256']==sha(HERE/'replay_native_portable.py')
    assert portable['mission_run_completed'] and portable['exit_code']==0
    assert not portable['original_sources_modified']
    assert portable['captured_source_sha256']==sha(HERE/portable['captured_source_path'])
    assert portable['translated_source_sha256']==sha(HERE/'portable_replay_capture/point_mass.script')
    assert portable['selected_runtime_matches_captured_core_inputs']
    for report in portable['reports']:
        archive=HERE/'portable_replay_capture'/(report['path']+'.gz')
        assert sha(archive)==report['gzip_sha256']
        with gzip.open(archive,'rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
        assert actual==report['sha256']==report['captured_decompressed_sha256']
        assert report['identical_decompressed_output']
    inventory=json.loads((HERE/'FIGURE_SOURCE_INVENTORY.json').read_text())
    assert len(inventory['figures'])==3
    for figure in inventory['figures']:
        assert sha(HERE/figure['generator'])==figure['generator_sha256']
        for name,digest in figure['source_data_sha256'].items():assert sha(HERE/name)==digest
        for name,digest in figure['output_sha256'].items():assert sha(HERE/name)==digest
    print('PASS: source identities,18 coast cases,24 original disposal cases,20 finite-host campaigns,7152-candidate search,3 native host replays,24 native payload lifetimes,3 postcampaign disposal replays,16,384-sample covariance and matched mass/authority/conservation limits. Physical/customer/provider acceptance is external.')


if __name__=='__main__':main()
