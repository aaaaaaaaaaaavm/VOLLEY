"""Source-derived campaign figures and C7/H0/H5 engineering interface documents."""
import json
import math
import re
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent


def readable_markdown(text):
    """Keep configuration IDs intact while spacing quantities in prose."""
    protected=['3U','1U','32s2p','GRGM900C','DE421','T0p2_R1','T1_R5','T5_R5','T5_R20_I0p5','T5_R20_I2','T5_R20']
    for i,token in enumerate(protected):text=text.replace(token,f'§TOKEN{chr(65+i)}§')
    text=re.sub(r'(?<=[a-z])(?=\d)',' ',text)
    text=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',text)
    text=re.sub(r'\band(?=[a-zA-Z])','and ',text)
    text=re.sub(r'\bthe(?=(?:host|current|source|same|actual|next|near|existing|declared|lunar|remaining|target|exact|original|shared|selected|payload|reference|provider))','the ',text)
    for i,token in enumerate(protected):text=text.replace(f'§TOKEN{chr(65+i)}§',token)
    text=re.sub(r',(?=[^\s\d])',', ',text)
    text=re.sub(r';(?=\S)','; ',text)
    for old,new in [('kg3U','kg 3U'),('plusEarth/SunDE421','plus Earth/Sun DE421'),('atslot','at slot'),('tozero','to zero'),('foracceptance','for acceptance'),('orchange','or change'),('foracceptance','for acceptance')]:text=text.replace(old,new)
    text=text.replace('\u00ad','')
    text=re.sub(r'(\d) e([+-]?\d)',r'\1e\2',text)
    text=text.replace('GRGM900C20/20','GRGM900C 20/20')
    return text


def main():
    import matplotlib.pyplot as plt
    plt.style.use(HERE/'scientific.mplstyle')
    studies=json.loads((HERE/'STUDY_RESULTS.json').read_text());demand=studies['host_demand']
    campaigns=json.loads((HERE/'CAMPAIGN_RESULTS.json').read_text());c=campaigns['configuration']
    selected=json.loads((HERE/'campaign/T5_R20_searched.json').read_text())
    native=json.loads((HERE/'CAMPAIGN_NATIVE_RESULTS.json').read_text())
    postdisposal=json.loads((HERE/'CAMPAIGN_DISPOSAL_RESULTS.json').read_text())
    nav=json.loads((HERE/'NAVIGATION_REQUIREMENTS.json').read_text())
    feed=json.loads((HERE/'inputs/FEEDER_SIZING.json').read_text());lift=json.loads((HERE/'inputs/LIFT_SIZING.json').read_text())
    feed_current=max(x['motor_current_peak_A'] for x in feed['feed_cases'])
    lift_current=max(x['current_peak_A'] for x in lift['cases'] if x['gravity_m_s2']==0 and x['moving_mass_study_kg']==10 and x['resistance_N']<=100)
    feed_E=24*feed_current*40;lift_E=24*lift_current*284
    pulse_E=demand['pulse_energy_max_all_18_cases_J'];pulse_heat=demand['pulse_local_loss_upper_from_ledger_J']
    avg=pulse_E/.8/450+feed_E/450+lift_E/450+1.1664
    peak=24*max(feed_current,lift_current)+pulse_E/.8/450+1.1664
    heat=(pulse_heat+feed_E+lift_E+pulse_E*(1/.8-1))/450+1.1664
    power=dict(source_model='24V catalog-reference motors; peak current conservatively held over full motion times,not measured average service.',
               feed_peak_current_A=feed_current,lift_peak_current_A=lift_current,
               feed_upper_energy_J=feed_E,lift_upper_energy_J=lift_E,
               loading_motion_times_s=dict(feed=40,lift_empty=22,lift_loaded=120,lower=120,park=22),
               represented_loads_average_upper_W=avg,represented_loads_peak_upper_W=peak,
               represented_thermal_average_upper_W=heat,
               required_additional_terms=['controller/encoder/communications standby','brake and lock/keeper/index actuators','harness and drive losses','host-provided home index pin','thermal control,heaters and contamination allowances'],
               host_requirement_expression=f'Continuous allocation >= {avg:.3f}W + unallocated service terms; peak allocation >= {peak:.3f}W + concurrent unallocated terms. Host24V availability and return/grounding are acceptance inputs,not facts.')
    releases=[x for x in selected['releases'] if x['released']]
    relative=[x['calibrated_relative_speed_m_s'] for x in releases]
    worst20=min(x['min_sampled_altitude_km'] for row in native['cases'] if row['mode']=='harmonic20' for x in row['payload_lifetime'])
    worst40=min(x['min_sampled_altitude_km'] for row in native['cases'] if row['mode']=='harmonic40' for x in row['payload_lifetime'])
    pass20=sum(x['native30day_sampled_floor_pass'] for row in native['cases'] if row['mode']=='harmonic20' for x in row['payload_lifetime'])
    pass40=sum(x['native30day_sampled_floor_pass'] for row in native['cases'] if row['mode']=='harmonic40' for x in row['payload_lifetime'])
    rows=[
      dict(id='C7-V',requirement='Post-arrest separation command and vector',value=f'Accepted modeled command1–3m/s; actual finite-host relative speeds in this12-shot campaign {min(relative):.6f}–{max(relative):.6f}m/s.6prograde/6retrograde. Direction is body+X; all retargeting consumes finite slew time.',downstream='N2,N3',evidence='campaign/T5_R20_searched.json',acceptance='Imposed source-calibrated point-event mapping; source-rated physical pulse/contact and actual payload release accuracy remain external.'),
      dict(id='C7-Q',requirement='Increment and3sigma state accuracy',value=f'Declared1km osculating-perilune error band: speed3sigma<= {nav["finite_sample_speed_3sigma_requirement_m_s"]:.6f}m/s at the standalone+3m/s reference with10m/0.01m/s navigation sigma and0.1deg pointing sigma. Quantization-only necessary increment<= {nav["necessary_command_increment_if_uniform_quantization_alone_m_s"]:.6f}m/s; allocate finer when other speed errors consume budget.',downstream='N2,N5',evidence='NAVIGATION_REQUIREMENTS.json',acceptance='Study requirements only. Independent speed/angle saturation is not a joint guarantee. Measured sensor/control covariance and perturbed campaign Monte Carlo not supplied.'),
      dict(id='C7-A',requirement='Finite host control authority and recovery',value=f'Surviving tested reference uses20N main thrust,Isp220s,5Nm attitude couple,>= {selected["peak_rate_deg_s"]:.3f}deg/s rate and declared inertia tensor. Cold-gas couple uses60s Isp and0.5m lever.20s guard,400s loading coast,5s preguard and450s slots are included.',downstream='N3,N5',evidence='CAMPAIGN_RESULTS.json',acceptance='An operational demand,not a supplier capability.5deg/s and double-inertia cases retain missed-slot failures; a real host must demonstrate allocated authority/plume/pointing and resources.'),
      dict(id='C7-M',requirement='Mass properties and load path',value=f'Actual source ACR1 dry156.556720kg including unlocated7kg allowance; loaded204.556720kg. Eight-state geometry box2.250x1.240x1.3489m. Campaign uses280kg complete dry retained core with declared inertia,actual CAD payload coordinates and per-shot updated CG/inertia. Payload axial computational load26.8635N and100N guide sensitivity remain source budgets.',downstream='N2,N3,N5',evidence='STUDY_RESULTS.json;inputs/DESIGN_BUDGETS.json',acceptance='Manufactured mass/CG/inertia,external mounting bolts,launch/environment loads and provider interface approval remain external.'),
      dict(id='C7-R',requirement='Retention duration and custody',value='At least5400s from staging campaign start through final nominal release; failed payloads remain captive through abort and independently available disposal. Launch/transfer waiting must be added: ideal Earth–Moon flight is about5days,not a validated retention rating.355s source cycle inside400s coast; captivity/capture precedes prior restraint release.',downstream='N2,N5',evidence='campaign_inputs.json;inputs/MISSION_INPUTS.json',acceptance='Current native custody geometry is retained. Physical latch endurance,launch/thermal retention and failed-path clearance tests remain external; no impossible automatic fault reset is claimed.'),
      dict(id='C7-E',requirement='Pulse and bus services',value=f'64cells32s2p,86.4V internal initial bank.1–3m/s maximum captured pulse {pulse_E:.3f}J; known represented service upper envelope {avg:.3f}W average/{peak:.3f}W peak plus named unallocated services.24V is the motor/charger-interface design request.',downstream='N3,N5',evidence='H0_DEMAND_SHEET.md',acceptance='Host bus quality/isolation,fault current/charger efficiency,standby/brake/lock services and actual circuit/pulse/vacuum acceptance remain external.'),
      dict(id='C7-T',requirement='Thermal,vacuum and material properties',value=f'Represented thermal upper envelope {heat:.3f}W over450s plus unallocated heater/control/actuator terms. Pulse loss and copper/tolerance budgets are source linked. Eaton cell catalog operating range−40..65degC is a reference limit,not space qualification.',downstream='N2,N3,N5',evidence='inputs/DESIGN_BUDGETS.json;inputs/POWER_COMPONENT_REFERENCE.json',acceptance='Required sink/interface temperatures,radiator view factors,thermal contact/conduction,cycling,outgassing,vacuum friction and contamination acceptance must be measured/agreed. No approved lunar radiator is inferred.'),
      dict(id='C7-EMC',requirement='EMC,grounding and magnetic interface',value='40kHz source PWM;86.4V internal bank; source-rated current/voltage/ripple design budgets retained. Separate structure/return/bonding and exclusion-zone interfaces must be allocated around the LSM and pulse wiring.',downstream='N3,N5',evidence='inputs/POWER_COMPONENT_REFERENCE.json',acceptance='Provider conducted/radiated/transient limits,magnetic cleanliness,shielding/harness/bonding tests and payload susceptibility are missing acceptance inputs,not fabricated compliance.'),
      dict(id='C7-F',requirement='Release count,cadence and abort/disposal',value=f'12command attempts at450s spacing; successful reference releases12. Modeled pre-command isolated-cell fault yields11releases/1retained; unresolved shared-path fault atslot6 stops after5releases with7retained. Engine-only disposal remains independent of successful releases; surviving campaign leaves {selected["final_propellant_kg"]:.6f}kg versus8kg reserved floor.',downstream='N2,N3,N5',evidence='CAMPAIGN_RESULTS.json;DISPOSAL_NATIVE_RESULTS.json',acceptance='Sensor/interlock/abort actuation must implement those controlled states. A real impact site,engine/propellant capability and disposal authorization remain external.')]
    rows[1]['acceptance']+=' The harmonic native host endpoint differs from the open-loop point-gravity planner by about1.63km/1.49m/s,exceeding the assumed10m/0.01m/s navigation bands; full-force navigation/planning/feedback is required before combining the standalone covariance with a campaign precision claim.'
    rows[-1]['value']+=f" Additional actual terminal-state disposal replays for nominal/isolated-cell/shared-path-abort cases all hit the sphere with<= {max(x['native_disposal_propellant_kg'] for x in postdisposal['cases']):.6f}kg additional propellant,below8kg,after coasting to apolune and finite attitude preparation."
    flow=dict(study='PCS-LUNAR-C7-FLOWDOWN-01',configuration='LUNAR-PCS-01 requirements investigation,not a new near-term LEO rating',power=power,requirements=rows,
              source_campaign='CAMPAIGN_RESULTS.json',source_native='CAMPAIGN_NATIVE_RESULTS.json',
              near_term_configuration='VOLLEY-G5-ACR1 unchanged; lunar flowdown does not redefine its test-article target')
    (HERE/'HARDWARE_FLOWDOWN.json').write_text(json.dumps(flow,indent=2)+'\n')
    # Campaign figures contain the actual finite-control time histories.
    history=selected['history'];t=np.array([x['t_s'] for x in history])/60
    fig,axes=plt.subplots(2,2,figsize=(9.2,6.4),layout='constrained')
    axes[0,0].plot(t,[x['propellant_kg'] for x in history],color='#397b93');axes[0,0].axhline(8,color='#555',linestyle=':');axes[0,0].set(xlabel='Campaign time (min)',ylabel='Remaining propellant (kg)',title='Finite main+ACS resource history')
    axes[0,1].plot(t,[x['angular_rate_deg_s'] for x in history],color='#c36d3c');axes[0,1].axhline(20,color='#555',linestyle=':');axes[0,1].set(xlabel='Campaign time (min)',ylabel='Body angular rate (deg/s)',title='Finite slew and post-release recovery')
    axes[1,0].plot([x['slot'] for x in releases],[x['after_mass_kg'] for x in releases],marker='o',color='#397b93');axes[1,0].set(xlabel='Release number',ylabel='Retained host mass (kg)',title='Actual payload and fuel removal')
    for policy,color in [('searched','#397b93'),('grouped_baseline','#67734c'),('alternating_baseline','#c36d3c')]:
        cases=[x for x in campaigns['cases'] if x['authority']['id']=='T5_R20' and x['policy_name']==policy]
        axes[1,1].bar(policy.replace('_baseline',''),20-cases[0]['final_propellant_kg'],color=color)
    axes[1,1].set(ylabel='Campaign propellant consumed (kg)',title='Same manifest,host,slots and authority')
    for ext in ['png','svg','pdf']:fig.savefig(HERE/'figures'/f'lunar_campaign_resources.{ext}')
    plt.close(fig)
    table='\n'.join(f"| {x['authority']['id']} | {x['policy_name']} | {x['released_payloads']} | {x['final_propellant_kg']:.5f} | {'pass' if x['nominal_full_manifest_pass'] else 'retained failure'} |" for x in campaigns['cases'])
    rtable='\n'.join(f"| {x['slot']} | {x['payload']} | {x['sign']:+d} | {x['calibrated_relative_speed_m_s']:.6f} | {x['after_mass_kg']:.5f} | {x['after_rate_deg_s']:.5f} | {x['payload_osculating_perilune_altitude_m']/1000:.3f} |" for x in releases)
    report=f'''# Coupled lunar deployment campaign

This is the existing C5 investigation for LUNAR-PCS-01. All12payloads are4kg3U surrogates,with actual ACR1 storage/release coordinates and a280kg retained dry core plus20kg initial propellant. The complete retained-core inertia tensor is declared in campaign_inputs.json,not measured or assigned to a provider. The source-calibrated point-event map includes the13.127806kg retained sled/pallet; the current1–3m/s source command is not equated to the final payload/host relative speed.

The campaign starts at the existing100×1,000km lunar staging orbit and source-pinned25October2026 UTC epoch. It requires six prograde and six retrograde useful bound-orbit departures at450s slots. Each selected cell is unique. Source custody uses355s inside400s zero-force loading,with5s pre-release and20s post-release guards. Finite slews,angular-momentum removal and body-axis recoil recovery compete for the remaining preparation time. Rest-to-rest transport holding torque is bounded from the7.573kg payload/cradle source and consumes ACS propellant; this is a kinematic envelope,not a contact-solver replay.

The search evaluates **{campaigns['search']['evaluated_candidates']:,}** cell/order/sign/roll choices in a12-level,width32beam. The best proxy candidate is then evaluated with the actual coupled model beside alternating and grouped baselines. This is a finite search,not a global-optimum or global-infeasibility proof.

The surviving tested reference uses20N body-axis propulsion/220s Isp,5N·m attitude torque,20°/s rate authority,60s ACS Isp and0.5m couple arm. It releases all12payloads,uses **{20-selected['final_propellant_kg']:.6f}kg** propellant and leaves **{selected['final_propellant_kg']:.6f}kg**,above the8kg independent disposal floor. The actual sampled peak rate is **{selected['peak_rate_deg_s']:.3f}°/s**. This is a demanding allocated host envelope; no actual host has demonstrated it here.

At5N·m/5°/s,the searched order stops after six releases when the sign reversal violates the next loading-coast deadline. Doubling the reference inertia also stops after six. At1N·m/5°/s,the searched order reaches five,while the alternating baseline reaches one. Infeasible policies preserve their states,remaining payloads,fuel and exact missed-window reason.

![Source-derived finite-control campaign resources.](figures/lunar_campaign_resources.png)

| Authority case | Policy | Released | Propellant remaining (kg) | Result |
|---|---|---:|---:|---|
{table}

Every release records the carrier position/velocity,mass,quaternion,full updated inertia/CG,angular momentum and body rate. Exact finite-position linear/angular momentum splitting precedes finite recovery. The largest linear and angular residuals are {campaigns['verification']['max_momentum_residual_kg_m_s']:.3g}kg·m/s and {campaigns['verification']['max_angular_residual_kg_m2_s']:.3g}kg·m²/s; mass closure is {campaigns['verification']['max_mass_closure_residual_kg']:.3g}kg. A halved integration step changes final position by {campaigns['verification']['half_max_step_final_position_difference_m']:.3g}m. Euler/quaternion slew trajectories include anisotropic inertia,gyroscopic torque and fuel-dependent inertia,with checked torque/rate bounds.

| Release | Cell | Direction | Relative speed after arrest (m/s) | Host mass after release (kg) | Immediate body rate (°/s) | Osculating perilune (km) |
|---:|---|---:|---:|---:|---:|---:|
{rtable}

## Independent native astrodynamics

The identical-point-gravity GMAT replay agrees with the Python host within {native['cases'][0]['final_position_difference_vs_python_m']:.5f}m and {native['cases'][0]['final_velocity_difference_vs_python_m_s']:.3g}m/s at its actual terminal stop time. The accumulated stop-time difference is {abs(native['cases'][0]['final_native_time_s']-native['cases'][0]['final_python_time_s']):.3g}s. The native replay independently applies finite main-engine mass flow and every source-frozen separation jump. Zero-resultant ACS consumption is imposed from the Python attitude solution. GMAT is an independent astrodynamics solver; it does not independently validate the attitude controller or release contact.

GRGM900C20/20 and40/40 plusEarth/SunDE421 runs replay the actual frozen campaign controls and released states. At30days,**{pass20}/12** and **{pass40}/12** payloads meet the20km minimum sampled reference-sphere floor; minima are {worst20:.3f}km and {worst40:.3f}km. Native host endpoint differences measure open-loop environment sensitivity,not closed-loop retargeting. The two gravity degrees are sensitivity runs,not a claim of physical convergence or terrain clearance.

The40/40 host endpoint differs from the point-gravity planner by about{next(x['final_position_difference_vs_python_m'] for x in native['cases'] if x['mode']=='harmonic40'):.1f}m and{next(x['final_velocity_difference_vs_python_m_s'] for x in native['cases'] if x['mode']=='harmonic40'):.3f}m/s. That exceeds the10m/0.01m/s navigation inputs assumed by the standalone covariance. The coarse useful-orbit criterion passes; accurate customer placement requires a full-force navigation/planning/feedback solution. The standalone1km covariance result is not silently promoted to a full-campaign accuracy guarantee.

## Faults and unresolved physical acceptance

The pre-command isolated-cell fault atslot6 leaves one payload captive and releases11; it assumes the shared path never becomes occupied. The unresolved shared-path capture fault inhibits subsequent releases after five successful departures and retains seven. No successful automatic jam reset is invented. Both preserve finite host states and independent disposal resources. The earlier engine-only disposal sweep already covers all12payloads retained with zero release-recoil credit.

The three actual nominal/fault terminal states are additionally propagated to the next apolune,prepared with finite attitude authority,and burned with a fixed inertial body-axis20N engine command. Independent native40/40+Earth/Sun replays all reach the reference sphere within24hours using at most{max(x['native_disposal_propellant_kg'] for x in postdisposal['cases']):.6f}kg additional propellant,below the8kg reserved floor. This connects campaign recovery to a surviving engine-only disposal path without release credit. Site/terrain/policy/engine acceptance remains external.

The source event is imposed after arrest; the finite pulse/contact/retention dynamics are not solved by these operational campaigns. Full manufacturing/measurement correlation and real provider/customer control/service/thermal/EMC/acceptance inputs remain external. Mission targets are declared energy classes and a useful bound-orbit floor,not customer full-state/time targets. Those limits remain visible in the C7 flowdown and original N/P gates.

Attitude dynamics in this investigation include release angular momentum andfinite commanded control;gravity-gradient,SRP,magnetic andplume disturbance torques are omitted andrequire a host-specific disturbance margin. The point-gravity controller is not a validated flight ACS.

Sources/results: campaign_inputs.json,lunar_campaign.py,CAMPAIGN_RESULTS.json,campaign/,campaign_native.py,CAMPAIGN_NATIVE_RESULTS.json,campaign_native/. Existing standalone20/40-degree coast and engine-only disposal captures are preserved.
'''
    (HERE/'CAMPAIGN_REPORT.md').write_text(readable_markdown(report))
    h0=f'''# H0 numeric host demand sheet

Configuration:VOLLEY-G5-ACR1,current modeled1–3m/s,twelve4kg3U payloads. The lunar campaign is separately named LUNAR-PCS-01; its280kg dry core and allocated control authority are not a selected provider.

| Interface | Numeric modeled demand | Evidence/meaning |
|---|---|---|
| Geometry |2.250×1.240×1.3489m;{demand['geometric_state_union_box_m3']:.4f}m³ rectangular box|Eight actual native solid-signature states.7kg unlocated hardware,harness,service and provider keep-outs additional.|
| Mass |156.556720kg device dry;204.556720kg loaded;48kg payload removed|Source ledger includes7kg electrical/control allocation;its CG/inertia location is missing.|
| Motion |1.300m powered travel;0.210m arrest;355s custody cycle|400s zero-force loading coast;450s mission slot;20s post/5s pre guards.|
| Pulse source |64cells,32s2p,86.4V internal initial bank;≤{pulse_E:.3f}J per represented1–3m/s shot|Source bank/inverter buffers pulse demand. This is not a request for an86.4V host bus.|
| Source recharge |≤{pulse_E/.8/450:.3f}W over450s at assumed80% efficiency|Balance adds1.1664W. Actual charger input,efficiency,protection and startup need acceptance.|
| Feed drive |24V reference;≤{feed_current:.6f}A peak;≤{feed_E:.2f}J over40s|Highest accepted feed-resistance case155N;peak current held for full duration gives a conservative represented-drive envelope.|
| Lift drive |24V reference;≤{lift_current:.6f}A peak;≤{lift_E:.2f}J over284s total|10kg moving-mass study,zero-g,≤100N resistance;22+120+120+22s motions. Actual cradle/pallet/payload7.573kg is below10kg study mass.|
| Represented host electrical envelope |≤{avg:.3f}W average;≤{peak:.3f}W peak,plus listed services|These are upper bounds for represented loads,not a complete installed bus rating.|
| Represented local heat envelope |≤{heat:.3f}W averaged over450s,plus listed services|Conservatively counts source losses,motor input,balancing andcharger loss. Sink temperature,view factor,contact resistance and actual component duty remain required.|
| Current payload loads |26.8635N source axial computational load;100N transverse guide sensitivity|No launch/environment/mounting-bolt allowable is inferred. Magnetic-gap and guide margins are design budgets requiring physical correlation.|
| Final recoil,3m/s |≈11.708N·s payload momentum|Reference initial704.55672kg assembly:post-arrest host kick≈0.01671m/s;transient source recoil≈0.07293m/s is a different state.|
| Offset attitude demand |0.1m offset→≈1.171N·m·s;≥0.05854N·m average over20s|Inertia and actual release-axis/CG offset must be supplied. This is not slew/pointing acceptance.|
| Pointing / navigation study |0.1°1sigma pointing,10m/0.01m/s navigation sigma;0.192240m/s3sigma release-speed budget for the standalone1km perilune band|These are allocated investigation inputs. Full harmonic navigation/feedback and measured joint accuracy remain required;native open-loop drift exceeds those navigation inputs.|
| Disposal |Independent carrier solution with zero release credit|Existing native20N/220s surrogate impact solutions require≤7.778kg in the all-failure bounds;actual engine/site/policy external.|

Additional service terms requiring numeric provider/article inputs:controller/encoder/communications standby;lock/keeper/index/home-pin actuators and brakes;drive/harness losses;heaters and thermal control. A complete host request is **{avg:.3f}W plus these average terms**,and **{peak:.3f}W plus concurrent peak terms**. No omitted term is silently set tozero. This sheet supplies calculated demands and explicitly unresolved interfaces;P7/provider acceptance remains open.

Sources:STUDY_RESULTS.json,inputs/RESOURCE_LEDGER.json,inputs/FEEDER_SIZING.json,inputs/LIFT_SIZING.json,inputs/POWER_COMPONENT_REFERENCE.json,inputs/DESIGN_BUDGETS.json and eight SIGNATURES captures. HARDWARE_FLOWDOWN.json records the arithmetic.
'''
    (HERE/'H0_DEMAND_SHEET.md').write_text(readable_markdown(h0))
    question='''# H5 provider integration questions

Prepared question sheets for an integration review; no provider was contacted and no answer or approval is implied. Each requested answer should name an ICD revision,value/limit,coordinate frame and evidence maturity. Use H0_DEMAND_SHEET.md and H5_INTERFACE_SKETCH.md as the controlled numeric request.

## Mechanical and payload integration

1. Can the candidate host accommodate the actual2.250×1.240×1.3489m geometry box and204.556720kg loaded mass,with separate service/harness/launch keep-outs and the unlocated7kg allocation?
2. What are the mounting plane,bolt pattern,load distribution,permitted CG/inertia,stiffness/mode,launch/quasi-static,vibration andshock limits? The current generic mounting datum is CAD Z=−150mm;it is not an approved bolt interface.
3. What external retention,release authorization and launch restraint requirements apply? Can the host provide or accept the current6mm retracting home-index pin/6.2mm bore interface,and verify clear travel before the355s cycle?
4. Supply the real payload rail/mass/inertia/CG,retention,venting,tip-off,shock,release-clearance and separation-state acceptance inputs. Are twelve4kg3U surrogates valid for this specific mission?
5. What access is required for captive-pallet capture-before-release inspection,bank/lift servicing,discharge and safe failed-cell removal? Which unresolved shared-path faults mandate abort?

## Electrical,thermal and EMC integration

1. Supply bus voltage/quality,current andenergy limits,startup,inrush,brownout,source isolation andcharging inhibit requirements.24V is the present motor-interface reference,not a known host service.
2. Confirm the represented average/peak power request in H0 plus numeric controller/lock/brake/home-pin/harness/heater allocations. Can pulse charging occur during feed/lift operation? What load-shed andfault-containment states are required?
3. Supply hot/cold mounting-interface temperatures,conductive paths/contact resistance,radiator/view-factor constraints,allowable thermal cycling andvacuum/outgassing/contamination requirements. Catalog operating temperatures do not establish vacuum acceptance.
4. Supply conducted/radiated/40kHzPWM transient limits,ground/return/bonding/isolation policy,magnetic-cleanliness zones andpayload susceptibility. Specify the required qualification/correlation evidence andinstrumentation.
5. Which host commands,telemetry,timing,arming/disarming,cell/source monitoring andindependent inhibit channels must the sequencer implement? How is safe local capacitor discharge confirmed after abort?

## Mission,attitude and operations integration

1. Supply actual delivered orbit/state/epoch,launch-dispersions,target departure states/times andsuccess bands. Separate LEO delivery from launch-suppliedTLI/direct-lunar delivery;include carrier-only TLI/LOI,stationkeeping anddisposal reserves.
2. Supply full host/payload mass/CG/inertia,release-axis lever arm,actuator torque/rate/momentum/thrust authority,cold-gas/chemical Isp andpropellant limits. Are arbitrary body-axis directions available without plume orsolar/communications restrictions?
3. Can the host meet355s custody inside400s zero-force loading at450s slots,including20s post/5s pre guards andfinite recoil/slew recovery? The surviving lunar sensitivity case needs5Nm andup to18.57deg/s;the5deg/s case misses a sign-reversal slot. No existing host is asserted to meet this.
4. What navigation covariance,clock jitter,relative-speed/pointing accuracy,conjunction screening andnon-recontact criterion are required? Which inputs are measured,simulated,allocated orunknown?
5. Who authorizes each release andabort? What disposal method remains valid with all12payloads captive,andwhat exact engine,reserve,site/trajectory,policy andapproval evidence is required? A reference-sphere impact is a dynamics result,not a disposal authorization.

Return answers with the originalPLAN-H1/H2/H3/H6/P7 references. These prepared questions complete a question-set deliverable only;host selection andexternal acceptance require genuine responses.
'''
    (HERE/'H5_PROVIDER_QUESTIONS.md').write_text(readable_markdown(question))
    sketch='''# H5 notional load-path and service interfaces

This sketch references the actual ACR1 source coordinates andsolid-signature box. It does not define an approved provider ICD ormanufacturing bolt pattern. Coordinates are CAD millimetres;the intended host mounting datum is Z=−150mm. The represented ladder occupies Z=−190..−150mm. Final bracket/bolt/grounding/keep-out design needs provider inputs.

```mermaid
flowchart TB
  P["Two six-level banks · twelve3U\nactual box2,250×1,240×1,348.9mm"]
  L["Selected-cell pusher → indexed lift\ncap­tive pallet capture before prior restraint opens"]
  S["Retained13.127806kg sled/pallet\n1,300mm powered stroke +210mm arrest"]
  G["Asymmetric guides / connected C chassis\ncurrent structural and tolerance budgets"]
  M["Host-mount ladder\ngeneric datum CAD Z=−150mm"]
  H["Provider deck / adapter\nbolt pattern,loads,stiffness,CG andkeep-outs required"]
  P --> L --> S --> G --> M --> H
```

Payload axial reaction andLSM source reactions close through the carrier/guide/chassis supports andthe host-mount ladder. Payload departure creates a net host impulse;internal sled motion creates a larger transient reaction andthen returns momentum during arrest. The retained captive pallet stays onthe carrier. A payload-proxy envelope is not a load-bearing provider bracket. Launch restraint paths andexternal access remain tobe defined with the host.

```mermaid
flowchart LR
  B["Host DC service\n24V reference request,quality/limits unknown"] --> C["Isolated charger / source protection\nefficiency andinrush acceptance required"]
  C --> E["64cell32s2p bank\n86.4V internal initial charge"]
  E --> I["Three-phase inverter /40kHzPWM"] --> F["LSM launch / arrest /return"]
  B --> D["Feed /lift /locks /brakes\nsequencer andencoders"]
  A["Host mission authority / independent inhibits"] --> Q["Custody /home-pin /source /release interlocks"]
  Q --> D
  Q --> I
  R["Bonding /return /EMC /thermal deck interface\nprovider numeric limits required"] --- C
  R --- D
  R --- I
```

The home-index interface is a retracting6mm pin in a6.2mm carrier bore;the current model identifies this as external host-provided hardware,unselected. Clear retraction is required before carrier travel. Power/thermal integration must add the unlocated7kg source/control package andnumeric services listed in H0. No unused CAD volume is automatically credited as radiator,harness clearance orspace-qualified electronics packaging.

The mission interface is an individually authorized separation vector plus finite recoil/recovery budget. Keep the generic500kg LEO host andthe separate300kg-wet lunar reference distinct. A supplied provider state,ICD,attitude/thrust authority,plume/visibility constraints andindependent disposal approval are required before adopting either reference.

Sources:inputs/PARAMETERS.json;inputs/RESOURCE_LEDGER.json;inputs/SIGNATURES_home.json;inputs/SIGNATURES_release.json;STUDY_RESULTS.json;HARDWARE_FLOWDOWN.json. The diagrams are notional interface sketches,not CAD orsolver screenshots.
'''
    (HERE/'H5_INTERFACE_SKETCH.md').write_text(readable_markdown(sketch))
    c7='''# C7 hardware requirement flowdown from the lunar campaign

This flowdown completes the translation of the declared surviving lunar investigation into hardware/service requirements. It does not select orqualify a lunar carrier orchange the near-term ACR1 LEO article. Each row names the source result,downstream original task IDs andthe remaining physical/provider evidence needed foracceptance.

'''
    for row in rows:c7+=f"## {row['id']} · {row['requirement']}\n\n{row['value']}\n\nDownstream:{row['downstream']}. Source:{row['evidence']}.\n\nAcceptance:{row['acceptance']}\n\n"
    c7+='The referenced N2/N3/N5 tasks retain their physical andsource-rated build gates. A computational requirement table does not close material measurements,contact correlation,manufacturing release,host/customer inputs orindependent human review. Near-term ACR1 remains twelve3U,1–3m/s modeled command range and64source cells.\n'
    (HERE/'C7_HARDWARE_REQUIREMENTS.md').write_text(readable_markdown(c7))
    print('Wrote campaign report,source-derived figure,C7 flowdown,H0 demand sheet andH5 questions/interfaces')


if __name__=='__main__':main()
