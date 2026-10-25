"""Reproduce current-host demand, matched mass limits and lunar engine disposal.

Inputs are frozen copies of accepted public artifacts. No vendor performance is
inferred. Requires numpy/scipy/matplotlib; all output paths are local to package.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
G0 = 9.80665


def read(name):
    return json.loads((HERE/'inputs'/name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def host_demand():
    ledger, shot = read('RESOURCE_LEDGER.json'), read('COUPLED_SHOT.json')
    mission, budget = read('MISSION_INPUTS.json'), read('DESIGN_BUDGETS.json')
    current_cases = [x for x in shot['cases'] if 1 <= x['target_m_s'] <= 3]
    peak_energy = max(x['cap_draw_J'] for x in current_cases)
    peak_heat = max(sum(x['energy_ledger'][k] for k in ['copper_J','inverter_J','bank_J','auxiliary_J']) for x in current_cases)
    cases=[]
    for u in [1,2,3]:
        selected=[x for x in shot['cases'] if x['target_m_s']==u]
        # Arrest ends with captive sled returned to retained host. Payload inertial
        # kick, rather than transient sled velocity, controls final host momentum.
        kicks=[x['release']['payload_inertial_delta_v_m_s'] for x in selected]
        impulse=4*max(kicks)
        cases.append(dict(command_m_s=u, max_cap_draw_J=max(x['cap_draw_J'] for x in selected),
                          min_payload_inertial_kick_m_s=min(kicks),
                          max_payload_inertial_kick_m_s=max(kicks),
                          post_arrest_host_momentum_N_s=impulse,
                          reference_post_arrest_host_recoil_m_s=impulse/(mission['mass_basis']['initial_Gen5_wet_kg']-4),
                          transient_sled_recoil_max_m_s=max(abs(x['release']['host_recoil_before_arrest_m_s']) for x in selected)))
    authority=[]
    for inertia in [20,100,500]:
        for offset in [0,0.1,0.5]:
            h=cases[-1]['post_arrest_host_momentum_N_s']*offset
            authority.append(dict(inertia_kg_m2=inertia, thrust_axis_offset_m=offset,
                                  release_angular_impulse_N_m_s=h,
                                  unrecovered_rate_deg_s=math.degrees(h/inertia),
                                  minimum_recovery_torque_N_m_for_20s=h/20))
    state_bounds=[]
    for path in sorted((HERE/'inputs').glob('SIGNATURES_*.json')):
        signatures=json.loads(path.read_text())
        boxes=[s['bounds_mm'] for o in signatures['objects'] for s in o['solids']]
        bounds=[min(b[i] for b in boxes) if i%2==0 else max(b[i] for b in boxes) for i in range(6)]
        state_bounds.append(dict(state=path.stem.removeprefix('SIGNATURES_'),bounds_mm=bounds,
                                 native_FCStd_sha256=signatures['source_sha256']))
    union=[min(b['bounds_mm'][i] for b in state_bounds) if i%2==0 else max(b['bounds_mm'][i] for b in state_bounds) for i in range(6)]
    return dict(configuration='VOLLEY-G5-ACR1',
                dry_device_including_7kg_allocation_kg=ledger['device_including_allowance_kg'],
                loaded_device_kg=ledger['loaded_device_kg'],
                retained_moving_sled_pallet_kg=ledger['moving_sled_with_pallet_kg'],
                payload_count=12, payload_each_kg=4,
                eight_native_state_bounds=state_bounds,
                geometric_state_union_dimensions_m=[(union[i+1]-union[i])/1000 for i in [0,2,4]],
                geometric_state_union_box_m3=math.prod((union[i+1]-union[i])/1000 for i in [0,2,4]),
                envelope_scope='Union of8 accepted native solid-signature states, not a continuous swept envelope or provider clearance.7kg unlocated power/control allowance and external service/inspection volumes require accommodation.',
                rail_length_m=read('PARAMETERS.json')['launch']['rail_length']/1000,
                supported_command_m_s=[1,3],
                source_cells=read('POWER_COMPONENT_REFERENCE.json')['pulse_store']['total_cells'],
                source_charge_voltage_V=32*2.7,
                pulse_energy_max_all_18_cases_J=peak_energy,
                pulse_local_loss_upper_from_ledger_J=peak_heat,
                pulse_loss_average_over_450s_W=peak_heat/450,
                energy_replenishment_at_assumed_80pct_charger_efficiency_W=peak_energy/450/0.8,
                balance_dissipation_W=read('POWER_COMPONENT_REFERENCE.json')['pulse_store']['balance_dissipation_W'],
                host_power_scope='Pulse recharge and balancing only; feeder/lift/standby/charger thermal services are additional, not zero.',
                declared_cycle_s=mission['timing']['declared_Gen5_worst_cycle_s'],
                required_zero_force_loading_coast_s=mission['timing']['Gen5_required_loading_coast_s'],
                mission_release_spacing_s=450,
                single_axis_attitude_sensitivities=authority,
                release_cases=cases,
                structural_budget_min_guide_margin_mm=min(x['remaining_side_clearance_mm'] for x in budget['guide_clearance']),
                magnetic_face_budget_mm=budget['magnetic_face_budget']['minimum_individual_face_budget_mm'],
                pointing_requirement='No real customer accuracy requirement or provider attitude authority supplied; sensitivity table is the numerical demand for selected offsets/inertias.',
                disposal_requirement='Host-provided disposal must remain available with zero payload releases.',
                source_classification='Accepted same-revision model plus explicitly declared charger/inertia/offset assumptions; no provider approval.')


def installed_comparison():
    c=read('MISSION_COMPARISON.json')['cases']
    inputs=read('MISSION_INPUTS.json')
    penalty=inputs['mass_basis']['Gen5_extra_device_kg']
    rows=[]
    for family in ['uniform_2','alternating_1_3']:
        for ceiling in [1,5]:
            best={}
            for arch in ['gen5','spring_fixed2','spring_pretrim']:
                choices=[x for x in c if x['family']==family and x['architecture']==arch
                         and x['completed_targeting'] and x['fuel_limit_pass'] and x['peak_force_N']<=ceiling]
                best[arch]=min(choices,key=lambda x:x['fuel_used_kg']) if choices else None
            for arch in ['spring_fixed2','spring_pretrim']:
                g,s=best['gen5'],best[arch]
                rows.append(dict(family=family,force_ceiling_N=ceiling,comparator=arch,
                                 gen5_candidate_pass=g is not None, spring_candidate_pass=s is not None,
                                 gen5_fuel_kg=g['fuel_used_kg'] if g else None,
                                 spring_fuel_kg=s['fuel_used_kg'] if s else None,
                                 propellant_saving_kg=(s['fuel_used_kg']-g['fuel_used_kg']) if s and g else None,
                                 gen5_added_dry_mass_kg=penalty,
                                 required_unmodeled_spring_installed_burden_for_mass_crossover_kg=(penalty+g['fuel_used_kg']-s['fuel_used_kg']) if s and g else None,
                                 scope='Same targets/epoch/Isp/bus/reserve; dry-device proxy differs. Full installed comparator unknown.'))
    return dict(study='Matched ACR1 campaign installed-mass necessary bounds', rows=rows,
                fuel_reserve_kg=inputs['mass_basis']['initial_propellant_kg'],
                dry_penalty_kg=penalty,
                optimistic_lower_net_mass_penalty_even_if_all_20kg_fuel_saved_kg=penalty-20,
                conclusion='At the accepted device proxies, no propellant-only crossover is possible inside the common 20kg reserve. No full installed-system commercial winner follows.',
                mounted_vs_free_flying='Any added autonomous bus mass must be offset by omitted host accommodation/service burden plus fuel savings. At these proxies, even eliminating the entire common20kg fuel allocation leaves64.56kg penalty before an autonomous bus. Real bus/host prices, reliability, power/thermal accommodation and interfaces are unknown.')


def elements(r,v,mu):
    r=np.asarray(r); v=np.asarray(v)
    h=np.cross(r,v); energy=float(np.dot(v,v)/2-mu/np.linalg.norm(r))
    e=np.linalg.norm(np.cross(v,h)/mu-r/np.linalg.norm(r))
    a=-mu/(2*energy)
    return float(a),float(e),float(a*(1-e))


def finite_disposal(c,apo,failed, execution=1.0,pointing_deg=0,step=10):
    mu=c['mu_moon_km3_s2']*1e9; radius=c['reference_radius_km']*1000
    ra=radius+apo*1000; rp=radius+c['staging_perilune_km']*1000
    speed=math.sqrt(mu*(2/ra-2/(ra+rp)))
    # 300kg retained wet surrogate includes280kg dry plus independent20kg
    # disposal reserve. Captive failed payloads add mass. Separate from LEO host.
    m0=c['retained_host_kg']+failed*c['payload_kg']
    y0=np.array([ra,0,0,0,speed,0,m0],float)
    thrust=c['disposal_thrust_N']; isp=c['disposal_Isp_s']
    angle=math.radians(pointing_deg)
    def rhs(t,y):
        r,v=y[:3],y[3:6]; vel=np.linalg.norm(v)
        radial=r/np.linalg.norm(r)
        direction=-v/vel*math.cos(angle)+radial*math.sin(angle)
        return np.r_[v,-mu*r/np.linalg.norm(r)**3+thrust/y[6]*direction,-thrust/(G0*isp)]
    def integrate(t):
        return solve_ivp(rhs,[0,t],y0,method='DOP853',rtol=2e-11,atol=1e-9,max_step=step)
    target=radius+c['disposal_target_osculating_perilune_altitude_km']*1000
    def f(t):
        y=integrate(t).y[:,-1]
        return elements(y[:3],y[3:6],mu)[2]-target
    # Recompute nominal cutoff without pointing error, then perturb execution.
    if pointing_deg:
        nominal=finite_disposal(c,apo,failed,step=step)
        duration=nominal['burn_duration_s']*execution
    else:
        duration=brentq(f,0.001,3000,xtol=1e-8)*execution
    burn=integrate(duration); yf=burn.y[:,-1]
    def coast(t,y):return np.r_[y[3:6],-mu*y[:3]/np.linalg.norm(y[:3])**3,0]
    def impact(t,y):return np.linalg.norm(y[:3])-radius
    impact.terminal=True; impact.direction=-1
    coastsol=solve_ivp(coast,[duration,c['disposal_completion_hours']*3600],yf,
                       events=impact,method='DOP853',rtol=2e-11,atol=1e-8,max_step=step*6)
    hit=bool(coastsol.t_events[0].size)
    a,e,rperi=elements(yf[:3],yf[3:6],mu)
    return dict(staging_apo_km=apo, failed_retained_payload_count=failed,
                assumed_initial_wet_mass_kg=m0, thrust_N=thrust, Isp_s=isp,
                burn_duration_s=duration, disposal_propellant_kg=m0-yf[6],
                integral_thrust_delta_v_m_s=G0*isp*math.log(m0/yf[6]),
                burnout_perilune_altitude_km=(rperi-radius)/1000,
                burn_execution_multiplier=execution, pointing_error_deg=pointing_deg,
                impact_event_within_24h=hit,
                time_from_burn_start_to_spherical_impact_s=float(coastsol.t_events[0][0]) if hit else None,
                propellant_reserve_20kg_pass=bool(m0-yf[6]<20),
                burnout_state_SI=yf.tolist(),
                impact_state_SI=coastsol.y[:,-1].tolist(),
                scope='Two-body finite continuous retrograde engine burn, then numerical coast to spherical surface; not epoch/site targeting, approval or supplier capability.')


def lunar_studies(c):
    mu=c['mu_moon_km3_s2']; r=c['reference_radius_km']; me=398600.435507; re=6378.137; d=384400
    budgets=[]; alternatives=[]; disposal=[]
    for apo in c['staging_apolune_km']:
        rp=r+100; ra=r+apo; a=(rp+ra)/2
        for start in ['500km_LEO','TLI_apogee_384400km']:
            leo=re+500; at=(leo+d)/2
            tli=math.sqrt(me*(2/leo-1/at))-math.sqrt(me/leo)
            vinf=math.sqrt(me/d)-math.sqrt(me*(2/d-1/at))
            capture=math.sqrt(vinf**2+2*mu/rp)-math.sqrt(mu*(2/rp-1/a))
            for n in [1,4,12]:
                # Disposal reserve is propagated as mass.20kg is an allocation;
                # finite disposal below checks it, independent of successful shots.
                dry_plus_payload=c['retained_dry_mass_kg']+4*n
                arrival=(dry_plus_payload+c['reserved_disposal_propellant_kg'])*math.exp(capture*1000/(G0*220))
                departure=arrival*math.exp(tli*1000/(G0*220))
                budgets.append(dict(staging_apo_km=apo,payload_count=n, starting_boundary=start,
                                    carrier_TLI_delta_v_m_s=tli*1000 if start=='500km_LEO' else 0,
                                    carrier_LOI_delta_v_m_s=capture*1000,
                                    independent_disposal_reserve_kg=20,
                                    carrier_required_initial_wet_kg=departure if start=='500km_LEO' else arrival,
                                    total_propellant_mass_fraction=1-dry_plus_payload/(departure if start=='500km_LEO' else arrival),
                                    assumed_Isp_s=220,
                                    delivery_state='500km circular Earth orbit' if start=='500km_LEO' else 'ideal lunar-encounter arrival Vinf from a500km-origin transfer; TLI launch energy supplied upstream',
                                    scope='Ideal coplanar patched-conic lower bound; finite LOI/TLI, targeting, tanks, gravity loss and launch mass availability unclosed.'))
        vapo=math.sqrt(mu*(2/ra-1/a)); vperi=math.sqrt(mu*(2/rp-1/a))
        impact_speed=math.sqrt(mu*(2/ra-2/(ra+r-100)))
        high_r=r+10000
        high_a=(rp+high_r)/2
        high1=abs(math.sqrt(mu*(2/rp-1/high_a))-vperi)
        high2=abs(math.sqrt(mu/high_r)-math.sqrt(mu*(2/high_r-1/high_a)))
        alternatives.extend([
            dict(staging_apo_km=apo,alternative='lunar_impact',ideal_delta_v_m_s=(vapo-impact_speed)*1000,
                 disposition='Finite-burn independent spherical-impact solution calculated; site/approval/environmental policy external.'),
            dict(staging_apo_km=apo,alternative='lunar_escape',ideal_delta_v_m_s=(math.sqrt(2*mu/rp)-vperi)*1000,
                 disposition='Zero lunar-energy threshold only; long-term heliocentric/Earth encounter fate unverified.'),
            dict(staging_apo_km=apo,alternative='10000km_circular_high_lunar',ideal_delta_v_m_s=(high1+high2)*1000,
                 disposition='Impulsive reshaping bound only; stable disposal and lunar Hill-region perturbations unverified.'),
            dict(staging_apo_km=apo,alternative='Earth_return',ideal_delta_v_m_s=None,
                 disposition='No valid Earth-return solution: lunar escape energy alone does not target Earth. Epoch, departure asymptote, atmosphere/entry and risk unknown; retained as infeasible-to-claim.')])
        for failed in [0,1,4,12]:
            disposal.append(finite_disposal(c,apo,failed))
        # All-shot failure is the controlling mass case. Execution/pointing
        # perturbations are bounded investigation inputs, not a probability.
        for ex in [0.99,1.01]:
            for pointing in [-1,1]:
                disposal.append(finite_disposal(c,apo,12,execution=ex,pointing_deg=pointing))
    release_map=[]
    for apo in c['staging_apolune_km']:
        ra=(r+apo)*1000;rp=(r+100)*1000;mu_si=mu*1e9
        v=math.sqrt(mu_si*(2/ra-2/(rp+ra)))
        for u in c['release_relative_speeds_m_s']:
            dp=c['retained_host_kg']/(c['retained_host_kg']+4)*u
            dh=-4/(c['retained_host_kg']+4)*u
            pa,pe,pperi=elements([ra,0,0],[0,0,v+dp],mu_si)
            ha,he,hperi=elements([ra,0,0],[0,0,v+dh],mu_si)
            release_map.append(dict(staging_apo_km=apo,relative_command_m_s=u,
                                    payload_delta_v_m_s=dp,retained_host_recoil_m_s=dh,
                                    momentum_residual_kg_m_s=4*dp+c['retained_host_kg']*dh,
                                    payload_perilune_altitude_km=pperi/1000-r,
                                    payload_apolune_altitude_km=pa*(1+pe)/1000-r,
                                    host_perilune_altitude_km=hperi/1000-r,
                                    scope='Last-payload snapshot,300kg retained wet reference; not full campaign.'))
    return dict(study='PCS-LUNAR-ENGINE-01',configuration='LUNAR-PCS-01 surrogate',
                separate_start_energy_budgets=budgets,disposal_alternatives=alternatives,
                finite_host_single_release_map=release_map,
                engine_only_finite_disposal_cases=disposal,
                no_release_dependency=all(x['impact_event_within_24h'] and x['propellant_reserve_20kg_pass'] for x in disposal),
                no_recoil_credit=True,
                limits='Spherical two-body engine/coast solution. Native perturbed lifetime results are separate. A landing/impact site, engine selection, covariance, topography, exact targeting and authorization are absent.')


def figures(result):
    import matplotlib.pyplot as plt
    plt.style.use(HERE/'scientific.mplstyle')
    out=HERE/'figures';out.mkdir(exist_ok=True)
    fig,axes=plt.subplots(1,2,figsize=(9.2,3.7),layout='constrained')
    d=result['lunar']['engine_only_finite_disposal_cases']
    for n,color in [(0,'#397b93'),(12,'#cb6b3f')]:
        rows=[x for x in d if x['failed_retained_payload_count']==n and x['pointing_error_deg']==0]
        axes[0].plot([x['staging_apo_km'] for x in rows],[x['disposal_propellant_kg'] for x in rows],marker='o',color=color,label=f'{n} failed payloads retained')
    axes[0].set(xscale='log',xlabel='Staging apolune altitude (km)',ylabel='Engine-only disposal propellant (kg)',title='Finite burn to spherical lunar impact')
    axes[0].legend(frameon=False)
    b=result['lunar']['separate_start_energy_budgets']
    for boundary,color in [('500km_LEO','#cb6b3f'),('TLI_apogee_384400km','#397b93')]:
        rows=[x for x in b if x['payload_count']==12 and x['starting_boundary']==boundary]
        axes[1].plot([x['staging_apo_km'] for x in rows],[x['carrier_required_initial_wet_kg'] for x in rows],marker='o',color=color,label='Carrier starts in LEO' if boundary=='500km_LEO' else 'Launch supplies TLI energy')
    axes[1].set(xscale='log',xlabel='Staging apolune altitude (km)',ylabel='Required boundary mass (kg)',title='Different delivery energies; 12 × 4 kg')
    axes[1].legend(frameon=False)
    for ext in ['png','svg','pdf']:fig.savefig(out/f'lunar_independent_disposal.{ext}')
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--no-plots',action='store_true');args=parser.parse_args()
    c=json.loads((HERE/'study_inputs.json').read_text())['lunar']
    result=dict(study='PCS-ACR1-01',source_sha256=digest(Path(__file__)),
                inputs_sha256={p.name:digest(p) for p in sorted((HERE/'inputs').glob('*'))},
                study_inputs_sha256=digest(HERE/'study_inputs.json'),
                host_demand=host_demand(), installed_comparison=installed_comparison(),lunar=lunar_studies(c))
    nominal=finite_disposal(c,1000,12,step=10)
    fine=finite_disposal(c,1000,12,step=5)
    result['verification']=dict(
        all_engine_only_disposal_cases_hit=result['lunar']['no_release_dependency'],
        finer_step_burn_duration_difference_s=abs(nominal['burn_duration_s']-fine['burn_duration_s']),
        finer_step_propellant_difference_kg=abs(nominal['disposal_propellant_kg']-fine['disposal_propellant_kg']),
        finer_step_impact_time_difference_s=abs(nominal['time_from_burn_start_to_spherical_impact_s']-fine['time_from_burn_start_to_spherical_impact_s']),
        finite_burn_step_refinement_pass=abs(nominal['time_from_burn_start_to_spherical_impact_s']-fine['time_from_burn_start_to_spherical_impact_s'])<0.001)
    (HERE/'STUDY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    if not args.no_plots:figures(result)
    print(json.dumps(dict(verification=result['verification'],pulse_energy_J=result['host_demand']['pulse_energy_max_all_18_cases_J'],mass_penalty_kg=result['installed_comparison']['dry_penalty_kg']),indent=2))


if __name__=='__main__':main()
