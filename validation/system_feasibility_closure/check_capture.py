"""Check captured analytical, geometry and mission identities without solvers."""
from pathlib import Path
import hashlib,json,math

H=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    for f in ('SYSTEM_SCREENS.json','LUNAR_NAVIGATION_SENSITIVITY.json',
              'TWELVE_ASSEMBLY_REPORT.json','TWELVE_MASS_LEDGER.json',
              'MISSION_RETARGET_SUMMARY.json','NATIVE_REPLAY_CHECKS.json',
              'MOVING_MASS_FLOWDOWN.json','STEP_EXCHANGE_CHECKS.json','SOURCE_IDENTITY.json'):
        assert (H/f).is_file(),f'Missing required captured evidence: {f}'
    identities=json.loads((H/'SOURCE_IDENTITY.json').read_text())
    for f,v in identities['files'].items():assert sha(H/f)==v,f
    s=json.loads((H/'SYSTEM_SCREENS.json').read_text())
    n=json.loads((H/'LUNAR_NAVIGATION_SENSITIVITY.json').read_text())
    assert s['source_sha256']==sha(H/'system_screens.py')
    assert n['source_sha256']==sha(H/'lunar_navigation_sensitivity.py')
    assert all(s['checks'].values())
    for r in s['energy_cases']:
        m=r['payload_kg_each'];M=r['retained_host_kg'];u=r['relative_speed_m_s']
        mu=1/(1/m+1/M)
        energy=.5*mu*u*u
        assert math.isclose(energy,r['ideal_relative_energy_per_shot_J'],rel_tol=1e-12)
        assert math.isclose(r['bus_energy_lower_bound_J'],energy*r['payload_count']/r['assumed_net_efficiency'],rel_tol=1e-12)
        assert math.isclose(r['charge_time_lower_bound_s'],r['bus_energy_lower_bound_J']/r['assumed_charging_W'],rel_tol=1e-12)
    assert len(n['cases'])==9 and all(c['pass_1e_minus4'] for c in n['finite_difference_checks'])
    if (H/'TWELVE_ASSEMBLY_REPORT.json').exists():
        a=json.loads((H/'TWELVE_ASSEMBLY_REPORT.json').read_text())
        assert a['receiver_count']==1 and len(a['stations_X_mm'])==12
        assert a['rail_length_mm']==4200 and a['receiver_travel_mm']==3500
        assert a['original_four_cell_source_sha256']==sha(H/'source_inputs/build_selected_R3.py')
        for c in a['captures']:
            for f,v in c['sha256'].items():assert sha(H/'cad_twelve'/f)==v,f
            assert c['mass_properties']['full_installed_mass_kg'] is None
            assert c['parts']==398 and c['step_solids']==398
            assert not c['including_catalog_envelopes_audit']['positive_volume_interferences']
        assert len(a['captures'])==2
        assert len(a['continuous_payload_corridor_sweeps'])==12
        assert all(x['pass_no_positive_volume_interference'] for x in a['continuous_payload_corridor_sweeps'])
        m=json.loads((H/'TWELVE_MASS_LEDGER.json').read_text())
        assert math.isclose(m['captures'][0]['mass_properties']['represented_material_mass_kg'],a['captures'][0]['mass_properties']['represented_material_mass_kg'],rel_tol=1e-12)
    if (H/'MISSION_RETARGET_SUMMARY.json').exists():
        a=json.loads((H/'MISSION_RETARGET_SUMMARY.json').read_text())
        assert len(a['cases'])==10 and not a['full_installed_system_or_mission_acceptance']
        for filename,value in a['input_identities'].items():assert sha(H/('source_inputs' if filename!='TWELVE_MASS_LEDGER.json' else '')/filename)==value,filename
        for r in a['cases']:
            assert (H/'mission/release'/r['file']).exists()
            assert r['pre_release_zero_force_guard_s']==5
            if r['architecture']=='volley':assert r['feeder_allocation_fits_coast']
    if (H/'NATIVE_REPLAY_CHECKS.json').exists():
        a=json.loads((H/'NATIVE_REPLAY_CHECKS.json').read_text())
        assert a['run_count']==len(a['native_runs']) and all(j['exit_code']==0 for j in a['native_runs'])
        assert all(j['max_mass_conservation_residual_kg']<1e-8 for j in a['native_runs'])
        assert all(j['max_payload_target_position_error_m']<.01 for j in a['native_runs'] if j['category']=='nominal')
        assert all(j['max_payload_target_velocity_error_m_s']<1e-5 for j in a['native_runs'] if j['category']=='nominal')
        assert all(j['max_momentum_residual_kg_m_s']<1e-6 for j in a['native_runs'])
        assert len(a['native_time_step_refinement'])==2 and all(j['pass_1mm'] for j in a['native_time_step_refinement'])
        assert a['run_count']==26 and len(a['conservation_and_timing'])==10
    exchange=json.loads((H/'STEP_EXCHANGE_CHECKS.json').read_text())
    assert len(exchange['checks'])==2
    for c in exchange['checks']:
        assert c['valid'] and c['pass_1ppm'] and c['relative_volume_difference']<1e-6
        assert sha(H/'cad_twelve'/c['file'])==c['sha256']
    if (H/'MANIFEST.json').exists():
        a=json.loads((H/'MANIFEST.json').read_text())
        for f,v in a['files'].items():assert sha(H/f)==v,f
    print('PASS SYS-01/LNS-01/CAP-12/FBR-02 capture checks; scoped numerical/geometry evidence, no installed or flight qualification.')

if __name__=='__main__':main()
