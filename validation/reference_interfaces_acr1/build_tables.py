"""Regenerate bounded interface arithmetic and comparison tables; no physics reruns."""
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACR1 = ROOT / 'validation/acr1'

def read(path):
    return json.loads(path.read_text())

def write_csv(name, rows):
    with (HERE/name).open('w', newline='') as f:
        out = csv.DictWriter(f, fieldnames=list(rows[0]))
        out.writeheader()
        out.writerows(rows)

home = read(ACR1/'cad/release/VOLLEY_G5_ACR1_home.json')
shots = read(ACR1/'analysis/COUPLED_SHOT.json')
inputs = read(ACR1/'mission/MISSION_INPUTS.json')
cards = read(HERE/'SOURCE_CARDS.json')
supported = [c for c in shots['cases'] if c['target_m_s'] <= 3 and c['all_declared_checks_pass']]
assert len(supported) == 18
dry = shots['dry_CAD_mass_kg']
device = dry + 7
loaded = device + 48
kick = inputs['critical_recoil_mapping_reference_checks'][-1]['inertial_payload_kick_m_s']
impulse = 4*kick
ladder = next(b for b in home['BOM'] if b['name'] == 'Host_mount_ladder')
demand = {
    'configuration_id': 'VOLLEY-G5-ACR1', 'date_utc': '2026-10-25',
    'dimensions_mm': [2250,1240,1348.9], 'powered_stroke_mm':1300,
    'arrest_allocation_mm':210,
    'bounding_volume_m3':2.25*1.24*1.3489,'rectangular_footprint_m2':2.25*1.24,
    'represented_dry_kg':dry, 'separate_power_control_allocation_kg':7,
    'dry_study_kg':device,'payload_kg':48,'loaded_study_kg':loaded,
    'per_payload_dry_allocation_kg':device/12,
    'counted_generic_ladder_kg':ladder['mass_kg'],
    'new_provider_adapter_reinforcement_mass_kg':None,
    'launch_force_per_imposed_g_N':loaded*9.80665,
    'launch_force_formula':'F = loaded mass × g0 × actual vector load factors; dynamic/joint response separate',
    'initial_three_m_s_payload_inertial_kick_m_s':kick,
    'initial_three_m_s_payload_momentum_Ns':impulse,
    'initial_post_arrest_retainedhost_recoil_m_s':-impulse/(500+device+48-4),
    'supported_production_peak_pre_arrest_host_recoil_abs_m_s':max(abs(c['release']['host_recoil_before_arrest_m_s']) for c in supported),
    'host_torque_impulse_relation':'angular impulse = r cross J; delta omega requires actual inertia tensor',
    'illustrative_1mrad_at3m_s_transverse_error_m_s':0.001*3,
    'pointing_limit':None,'actual_host_inertia_tensor':None,
    'net_bank_draw_J_range':[min(c['cap_draw_J'] for c in supported),max(c['cap_draw_J'] for c in supported)],
    'shot_replenishment_only_lower_average_W':max(c['cap_draw_J'] for c in supported)/450,
    'power_exclusions':['charger inefficiency','handling','standby','balancing','thermal control','host operations'],
    'host_supply_voltage_V':None,'total_host_average_power_W':None,
    'release_slot_s':450,'loading_coast_s':400,'declared_cycle_s':355,
    'release_guard_s':{'before':5,'after':20},
    'source_bank':{'arrangement':'32S2P','initial_V':86.4,'nominal_F':6.25,'nominal_ESR_ohm':0.176},
    'source_boundary':'Internal source values are not host supply requirements.',
    'conventional_study_mass_kg':72,'dry_penalty_vs_study_kg':device-72,
    'Nova_three_pod_bare_mass_kg':3*13.32,'dry_difference_vs_Nova_bare_kg':device-3*13.32,
    'Electron_nominal_500kmSSO_payload_kg':200,
    'loaded_excess_before_new_adapter_kg':loaded-200,
    'fit_screen':'Declared protected box fails standard1200mm diameter; customexpanded case not evaluated.',
    'no_claims':['provider-approved load path','payload qualification','actual total host power','attitude recovery','customer requirement','flight accuracy'],
}
(HERE/'HOST_DEMAND.json').write_text(json.dumps(demand,indent=2)+'\n')

write_csv('DEPLOYER_COMPARISON.csv',[
 {'option':'ACR1 retained-carrier','manifest_basis':'12 × 4 kg 3U','dry_mass_kg':device,'mass_evidence':'CAD +7 kg allocation','release_basis':'1–3 m/s computed carrier-host commands','installed_exclusions':'provider adapter/reinforcement; qualified installation margins','services':'charger/control; feed/lift; shared source/carrier/path; host attitude/navigation','maturity':'computational concept','source':'ACR1 controlled records'},
 {'option':'Frozen spring-class mission reference','manifest_basis':'12 ×4 kg3U;12 ×6 kg device assumption','dry_mass_kg':72,'mass_evidence':'declared study assumption,not vendor product','release_basis':'fixed2 m/s or ideal ground-pretrim table','installed_exclusions':'real product volume/power/thermal/sequence/harness not resolved','services':'same generic host;no imposed400 s loading coast','maturity':'mathematical comparator','source':'ACR1 mission/MISSION_INPUTS.json'},
 {'option':'3 ×EXOpod Nova12U S4','manifest_basis':'12 independent3U slots','dry_mass_kg':39.96,'mass_evidence':'bare catalog total,±5%;not installed','release_basis':'spring energy;mission ICD defines satellite velocity','installed_exclusions':'adapters,fasteners,host mounting,harness,sequencer','services':'redundant magnetic locks and telemetry per slot;host commands','maturity':'manufacturer-reported flight heritage','source':'NovaRev1.2June2024§2.2Fig12;§3.2Table4'},
 {'option':'NRCSD interface precedent','manifest_basis':'6U volume with mixed sizes per source;not a12-slot design','dry_mass_kg':None,'mass_evidence':'not extracted;not zero','release_basis':'payload survives0.5–2m/s requirement','installed_exclusions':'mission-specific installation unmodeled','services':'ISS-specific release command and interface','maturity':'flight interface precedent','source':'NRCSDIDDRev.–§3.3/4.1.6'},
])
write_csv('MISSION_LEVEL_COMPARISON.csv',[
 {'family':'uniform2','force_ceiling_N':'1 or5','VOLLEY_fuel_kg':0.052443,'fixed2_spring_fuel_kg':0.046957,'ideal_pretrim_fuel_kg':0.052443,'VOLLEY_dry_kg':device,'spring_assumed_dry_kg':72,'scope':'same12targets/host/epoch;sampledpolicies;no fuel or wet-mass advantage'},
 {'family':'alternating1/3','force_ceiling_N':1,'VOLLEY_fuel_kg':'no tested pass','fixed2_spring_fuel_kg':'no tested pass','ideal_pretrim_fuel_kg':0.075002,'VOLLEY_dry_kg':device,'spring_assumed_dry_kg':72,'scope':'bounded policy failure;not global infeasibility'},
 {'family':'alternating1/3','force_ceiling_N':5,'VOLLEY_fuel_kg':0.289874,'fixed2_spring_fuel_kg':'no tested pass','ideal_pretrim_fuel_kg':0.053645,'VOLLEY_dry_kg':device,'spring_assumed_dry_kg':72,'scope':'same12targets/host/epoch;preplanned;no late retasking simulated'},
 {'family':'actual ION or Nova installation','force_ceiling_N':'unknown','VOLLEY_fuel_kg':'not calculated','fixed2_spring_fuel_kg':'not calculated','ideal_pretrim_fuel_kg':'not calculated','VOLLEY_dry_kg':'installation-specific','spring_assumed_dry_kg':'installation-specific','scope':'provider data missing;do not insert fake budget or substitute bare39.96kg into frozen result'},
])
write_csv('HOST_INTEGRATION_MATRIX.csv',[{
    'host_id':h['id'],'reference':h['name'],'class':h['class'],'source_date':h['source_date'],
    'checked_utc':h['accessed_utc'],'maturity':h['maturity'],'fit_status':h['fit_status'],
    'maneuver_boundary':h['can_manoeuvre'],'mission_match':h['ACR1_mission_match'],
    'provider_approval':False,'remaining_inputs':'; '.join(h['unknowns']),
    'source':'; '.join(h['primary_urls'] or h['project_sources'])
} for h in cards['hosts']])

source_paths=['cad/release/VOLLEY_G5_ACR1_home.json','analysis/COUPLED_SHOT.json','analysis/POWER_COMPONENT_REFERENCE.json','analysis/FEEDER_SIZING.json','analysis/LIFT_SIZING.json','mission/MISSION_INPUTS.json','mission/MISSION_REPORT.md']
integrity={'date_utc':'2026-10-25','method':'Read existing results; recompute table arithmetic only; no new solver run','inputs':[{'path':'validation/acr1/'+p,'sha256':hashlib.sha256((ACR1/p).read_bytes()).hexdigest()} for p in source_paths],'formulas':['dry study=CAD+7','loaded=dry study+48','Nova bare=3×13.32','force per g=loaded×9.80665','payload impulse=4×computed inertial kick','post-arrest recoil=-impulse/remaining host mass','lower average=maximum net bank draw/450'],'frozen_academic_files_written':False,'provider_contacts':False,'external_publication':False}
(HERE/'ARITHMETIC_AND_INPUT_PINS.json').write_text(json.dumps(integrity,indent=2)+'\n')
print(json.dumps({'dry_study_kg':device,'loaded_kg':loaded,'Nova_bare_kg':39.96,'host_cards':len(cards['hosts']),'supported_existing_cases':len(supported),'recoil_after_arrest_m_s':demand['initial_post_arrest_retainedhost_recoil_m_s'],'host_power_lower_bound_W':demand['shot_replenishment_only_lower_average_W']},indent=2))
