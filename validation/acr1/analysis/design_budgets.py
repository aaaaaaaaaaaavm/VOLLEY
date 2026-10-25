"""Traceable secondary budgets for the completed computational reference study.

Allocations and material assumptions are separate from native-solver results.
No statistical confidence level or physical qualification is inferred.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def read(rel):
    p=ROOT/rel;raw=p.read_bytes()
    return json.loads(raw),hashlib.sha256(raw).hexdigest()

def main():
    shots,hshot=read('analysis/COUPLED_SHOT.json');params,hparams=read('cad/PARAMETERS.json')
    guide,hguide=read('analysis/FEEDER_SIZING.json')
    home,hhome=read('cad/release/VOLLEY_G5_ACR1_home.json')
    accepted=[c for c in shots['cases']if c['target_m_s']<=3 and c['all_declared_checks_pass']]
    assert len(accepted)==18
    # Independent stiffness figures come from actual-source chassis FE report.
    frame_path=ROOT/'verification/chassis_fea/d4b53d520c1bc0d3_h8/CHASSIS_FEA_REVIEW.json'
    raw_frame=frame_path.read_bytes()
    paired_closure_130=.371778355
    allocations={'guide_centring_mm':.20,'surface_flatness_mm':.15,'assembly_mm':.15,'differential_thermal_mm':.05}
    gap=1-paired_closure_130/2-sum(allocations.values())
    endwall=[]
    for dT in [0,20,40,60]:
        thermal=340.5*12e-6*dT
        endwall.append({'differential_temperature_K':dT,'nominal_mm':.5,
            'machining_allocation_mm':.10,'docking_repeatability_allocation_mm':.10,
            'differential_CTE_assumed_um_mK':12,'differential_thermal_mm':thermal,
            'rigid_stack_residual_mm':.5-.1-.1-thermal})
    # Thermal rise: spatially resolved DC current, adiabatic pulse bound.
    material={'copper_density_kg_m3':8960,'copper_Cp_J_kgK':385,'copper_k_W_mK':400,
        'resistivity_20C_ohm_m':1.7e-8,'temperature_coefficient_K_inv':.00393}
    copper_mass=0.;phase_data=[]
    for ph,h in [('A',2),('B',3),('C',3)]:
        p=ROOT/'analysis/conduction'/f'phase_{ph}'/f'h{h}'
        d=json.loads((p/'RESULT.json').read_text());z=np.load(p/'solution.npz')
        j=np.linalg.norm(z['J_A_m2_at1V'],axis=1)/d['current_at1V_A']
        weights=z['element_volume_m3'];order=np.argsort(j);cum=np.cumsum(weights[order])/weights.sum()
        q99=float(j[order][min(np.searchsorted(cum,.99),len(j)-1)])
        copper_mass+=d['copper_volume_m3']*8960
        phase_data.append({'phase':ph,'J_per_phase_A_volume99_A_m2_A':q99,
            'J_per_phase_A_mesh_max_A_m2_A':float(j.max()),'native_conduction_result_sha256':hashlib.sha256((p/'RESULT.json').read_bytes()).hexdigest()})
    thermal=[]
    for c in accepted:
        I2=c['conservative_phase_current_sq_with_ripple_A2s']
        rho=1.7e-8*(1+.00393*(80 if c['adverse'] else 30))
        factor=rho*I2/(8960*385)
        thermal.append({'target_m_s':c['target_m_s'],'adverse':c['adverse'],'L_H':c['inductance_H'],
            'bulk_copper_rise_K_upper':c['energy_ledger']['copper_J']/(copper_mass*385),
            'volume99_local_adiabatic_rise_K_upper':max(q['J_per_phase_A_volume99_A_m2_A']**2*factor for q in phase_data),
            'mesh_max_local_adiabatic_rise_K_observation':max(q['J_per_phase_A_mesh_max_A_m2_A']**2*factor for q in phase_data)})
    alpha=400/(8960*385);diffusion=.09**2/alpha
    worstbulk=max(q['bulk_copper_rise_K_upper']for q in thermal)
    worstlocal=max(q['mesh_max_local_adiabatic_rise_K_observation']for q in thermal)
    # Elastic-energy angular bound, not a time-resolved contact-trajectory claim.
    peakN=max(c['peak_payload_normal_reaction_N']for c in accepted)
    inertia_pitch=4*(.3405**2+.1**2)/12;inertia_roll=4*(.1**2+.1**2)/12
    rail_k=70e9*(.008*.008)/.3405;pad_k=70e9*(.008*.006)/.004
    contact=[]
    for nrail in [1,2,4]:
        k=nrail/(1/rail_k+1/pad_k)
        U=peakN**2/(2*k)
        contact.append({'active_reference_rails':nrail,'effective_axial_stiffness_N_m':k,
            'stored_elastic_energy_J':U,
            'pitch_yaw_energy_bound_deg_s':math.degrees(math.sqrt(2*U/inertia_pitch)),
            'all_axis_energy_bound_deg_s':math.degrees(math.sqrt(2*U/inertia_roll))})
    speed=params['storage']['feed_stroke']/1000/params['storage']['nominal_feed_time_s']*1.875
    energy=.5*4*speed*speed
    EI=200e9*math.pi*.003**4/64;length=.118
    stiffness=2*3*EI/length**3;deflection=math.sqrt(2*energy/stiffness)
    feedstop={'payload_kg':4,'maximum_commanded_pusher_speed_m_s':speed,
        'free_payload_kinetic_energy_J':energy,'two_3mm_steel_keepers_effective_length_m_assumed':length,
        'parallel_cantilever_stiffness_N_m_assumed':stiffness,'elastic_impact_deflection_mm':deflection*1000,
        'peak_total_impact_force_N':stiffness*deflection,
        'scope':'Low-speed nominal feed capture bound; excludes stored jam energy, guide play and measured restitution.'}
    result={'configuration_id':params['configuration_id'],'model_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs_sha256':{'coupled':hshot,'parameters':hparams,'home':hhome,'feeder_sizing':hguide,
            'actual_chassis':hashlib.sha256(raw_frame).hexdigest()},
        'magnetic_face_budget':{'nominal_each_mm':1,'actual_FE_paired_closure_at130pct_mm':paired_closure_130,
            'allocated_bounds':allocations,'minimum_individual_face_budget_mm':gap,
            'interpretation':'Paired FE closure split about stated centring allocation; manufacturing/assembly bounds are design allocations, not measured tolerances.'},
        'endwall_rigid_stack':endwall,
        'endwall_scope':'Rigid datum/tolerance budget only; elastic retainer contact and manufactured docking repeatability need prototype correlation. No flight compliance is asserted.',
        'guide_clearance':guide['guide_clearance_sensitivity'],
        'copper_thermal':{'material_assumptions':material,'copper_mass_from_FE_volumes_kg':copper_mass,
            'phase_current_density':phase_data,'cases':thermal,'90mm_diffusion_time_s':diffusion,
            'reference_intershot_s':450,'12shot_no_external_cooling_bulk_rise_K_upper':12*worstbulk,
            'local_recovery_estimate_K':12*worstbulk+worstlocal,
            'scope':'Adiabatic pulse bound with DC FE current field and ripple-current upper integral. Mesh corner maximum is an observation, not a converged physical hotspot rating. Local recovery assumes repeated-cell thermal diffusion between450s shots; external cooling is not credited.'},
        'contact_energy':{'peak_payload_axial_normal_N':peakN,'surrogate_pitch_yaw_inertia_kg_m2':inertia_pitch,
            'surrogate_roll_inertia_kg_m2':inertia_roll,'rail_geometry_assumed_mm':[8,8,340.5],
            'rail_E_Pa_assumed':70e9,'rear_pad_geometry_mm':[8,6,4],'cases':contact,
            'scope':'Elastic-energy upper bounds for a declared four-rail payload surrogate; not measured tip-off, a universal CubeSat property, or a rigid-contact peak-force prediction. Actual payload inertia/stiffness and guide/friction coupling require physical correlation.'},
        'nominal_feed_capture':feedstop,
        'qualification_boundary':'The budgets complete the stated computational characterization; provider-specific environmental acceptance and physical correlation belong to hardware development.'}
    (ROOT/'analysis/DESIGN_BUDGETS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'magnetic_face_residual_mm':gap,'copper_mass_kg':copper_mass,
        'worst_bulk_pulse_rise_K':worstbulk,'worst_local_mesh_pulse_rise_K':worstlocal,
        '12shot_bulk_plus_local_estimate_K':12*worstbulk+worstlocal,
        'contact_cases':contact,'feed_capture':feedstop},indent=2))

if __name__=='__main__':main()
