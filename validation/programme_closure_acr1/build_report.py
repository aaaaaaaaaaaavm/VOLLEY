"""Build public result summary and source-linked scientific figure from captures."""
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    import matplotlib.pyplot as plt
    plt.style.use(HERE/'scientific.mplstyle')
    result=json.loads((HERE/'STUDY_RESULTS.json').read_text())
    coast=json.loads((HERE/'LUNAR_NATIVE_RESULTS.json').read_text())
    disposal=json.loads((HERE/'DISPOSAL_NATIVE_RESULTS.json').read_text())
    nav=json.loads((HERE/'NAVIGATION_REQUIREMENTS.json').read_text())
    demand=result['host_demand'];out=HERE/'figures'
    fig,ax=plt.subplots(figsize=(7.2,3.8),layout='constrained')
    colors={100:'#3a738b',1000:'#c36d3c',10000:'#67734c'}
    for apo in [100,1000,10000]:
        for degree,style,marker in [(20,'--','o'),(40,'-','s')]:
            cases=sorted([x for x in coast['cases'] if x['apo_km']==apo and x['degree_order']==degree],key=lambda x:x['relative_speed_m_s'])
            ax.plot([x['relative_speed_m_s'] for x in cases],[x['min_sampled_altitude_km'] for x in cases],linestyle=style,marker=marker,color=colors[apo],label=f'100 × {apo:,} km, {degree}/{degree}')
    ax.axhline(20,color='#555555',linewidth=1,linestyle=':',label='Declared 20 km sampled floor')
    ax.set(xlabel='Signed relative release command (m/s)',ylabel='Minimum sampled altitude over 30 days (km)',xticks=[-3,0,3])
    ax.legend(frameon=False,fontsize=8,ncol=2,loc='upper left')
    for ext in ['png','svg','pdf']:fig.savefig(out/f'lunar_release_lifetime.{ext}')
    plt.close(fig)
    max_deg=max(abs(next(z['min_sampled_altitude_km'] for z in coast['cases'] if z['apo_km']==x['apo_km'] and z['relative_speed_m_s']==x['relative_speed_m_s'] and z['degree_order']==20)-x['min_sampled_altitude_km']) for x in coast['cases'] if x['degree_order']==40)
    rows=[]
    for x in disposal['cases']:
        if x['failed_payloads']==12 and x['degree_order']==40 and x['pointing_deg']==0:
            rows.append(f"| 100 × {x['staging_apo_km']:,} | {x['burn_duration_s']:.2f} | {x['native_propellant_used_kg']:.4f} | {x['native_impact_time_s']/3600:.3f} |")
    mass_rows=[]
    for x in result['lunar']['separate_start_energy_budgets']:
        if x['payload_count']==12:
            mass_rows.append(f"| {x['starting_boundary']} | 100 × {x['staging_apo_km']:,} | {x['carrier_TLI_delta_v_m_s']:.1f} | {x['carrier_LOI_delta_v_m_s']:.1f} | {x['carrier_required_initial_wet_kg']:.1f} |")
    path='validation/programme_closure_acr1'
    report=f'''# Source-linked programme studies, ACR1

25 October 2026. These computations extend the existing research programme. The near-term machine remains VOLLEY-G5-ACR1: twelve 3U payloads, two six-level banks, supported modeled command range 1–3 m/s, a 13.127806 kg captive sled/pallet, and 64 source cells. Gen6 mixed 1U/3U studies retain their separate identity.

The lunar investigation is **LUNAR-PCS-01**, a separate surrogate with 280 kg retained dry mass, 20 kg independent disposal reserve and 4 kg payloads. Its 300 kg retained wet single-release reference is distinct from the 500 kg wet LEO bus. A real carrier, customer, engine and interface have not been selected.

## Existing results reused

The [accepted native lunar coast study](../validation/lunar_native_coast/README.md) already contains 18 native attempts at 7/30/90/180 days, gravity-degree/step/field sensitivity, SPICE frame settings and raw histories. Its capture checker passes. At its 23 October TAI epoch and specified MJ2000Eq initial states, the circular inclined case stops at the reference sphere after about 116–118 days; the high ellipse stops after about 40.1 days. These results are retained with their original initial conditions. The new release study uses a different declared epoch, apolune starting state and signed release vector; a completed 30-day case cannot replace those longer-horizon findings.

The [accepted navigation sensitivity](../validation/system_feasibility_closure/LUNAR_NAVIGATION_SENSITIVITY.json), [ideal lunar bounds](../validation/extended_feasibility_bounds/README.md), [current mission comparisons](../validation/acr1/mission/MISSION_REPORT.md), resource ledger and eight final native solid-signature captures are also reused. No historical speed dispersion or high-speed result is transferred into the current 1–3 m/s rating.

## Numerical ACR1 host demand and matched mass boundary

The eight native geometry states have a common bounding box **2.250 × 1.240 × 1.3489 m**, or {demand['geometric_state_union_box_m3']:.4f} m³ as a rectangular enclosure. This is geometry occupancy; the unlocated 7 kg power/control allocation, harness routing, service access and provider keep-outs require further accommodation. Installed device mass including that allocation is {demand['dry_device_including_7kg_allocation_kg']:.6f} kg dry and {demand['loaded_device_kg']:.6f} kg loaded.

Across the 18 accepted nominal/adverse, 3/20/100 µH cases at 1/2/3 m/s, the maximum source draw is **{demand['pulse_energy_max_all_18_cases_J']:.3f} J**. Replenishment over the 450 s release spacing requires {demand['energy_replenishment_at_assumed_80pct_charger_efficiency_W']:.3f} W with the declared 80% charger efficiency, plus 1.1664 W balancing and additional feed/lift/standby services. Maximum modeled local pulse loss divided by 450 s is {demand['pulse_loss_average_over_450s_W']:.3f} W; this is an average thermal burden, not a radiator or component-temperature solution. The declared 355 s cycle occupies a 400 s zero-force loading coast.

At 3 m/s, the post-arrest payload momentum is about {demand['release_cases'][-1]['post_arrest_host_momentum_N_s']:.3f} N·s. A 0.1 m offset therefore deposits about 1.171 N·m·s, requiring at least 0.05854 N·m average counter-torque over 20 s. The transient sled recoil and final post-arrest host recoil are kept separate in [STUDY_RESULTS.json](../{path}/STUDY_RESULTS.json). Assumed inertia/offset sensitivities are requirements for comparison, not demonstrated host authority.

The current campaign uses a 72 kg conventional-deployer class proxy, so ACR1 adds **84.556720 kg** device mass. Even the impossible best case of saving the entire common 20 kg host fuel reserve leaves **64.556720 kg** added mass. In matched alternating targets at 5 N, the best tested conventional pretrim consumes 0.053645 kg and ACR1 0.289874 kg. At 1 N, a tested pretrim policy succeeds where no tested ACR1 candidate meets the force ceiling. These are candidate results, not global infeasibility proofs. Full installed power/thermal/volume/reliability/vendor costing remains unavailable; no product or supplier winner is claimed.

## Lunar release vectors and perturbed coast

The new native run set has **18 actual GMAT R2026a propagations**: three staging orbits, signed −3/0/+3 m/s apolune releases, and GRGM900C 20/20 versus 40/40. It uses Earth/Sun DE421 ephemerides, explicit SPICE/MOON_PA lunar coefficient rotation, MJ2000Eq initial planes, and a 25 October 2026 12:00 UTC epoch. The declared criterion is 30 days and a 20 km minimum sampled reference-sphere altitude. All nine geometries pass at both degrees. The smallest 40/40 sampled margin is **{min(x['min_sampled_altitude_km'] for x in coast['cases'] if x['degree_order']==40):.3f} km**. The maximum change in sampled minimum altitude between 20/20 and 40/40 is {max_deg:.3f} km; this is observed model sensitivity, not physical convergence.

![Native lunar release lifetime study; signed commands and minimum sampled altitude at the declared epoch.](../{path}/figures/lunar_release_lifetime.png)

The finite-host release map records payload kick and retained-host recoil for each command. These are last-payload 300 kg retained-wet snapshots; they do not form a full twelve-release campaign. Native histories and source scripts are in the package. Terrain, SRP, perturbed covariance, long-term useful service, communications, conjunction assessment and exact mission targeting remain outside this bounded coast result.

## Inverse navigation accuracy

For a declared 100 × 1,000 km apolune release at +3 m/s, the assumed position and velocity standard deviations are 10 m and 0.01 m/s. A **±1 km three-sigma osculating-perilune study band** requires approximately **{nav['finite_sample_speed_3sigma_requirement_m_s']:.6f} m/s three-sigma release-speed accuracy** with 0.1° pointing standard deviation. The fixed-seed 16,384-sample Monte Carlo, 4,096-sample comparison and independently refined finite-difference sensitivity are captured.

A separately saturated plane-error budget of 1 mrad at the 99.73% quantile yields {nav['finite_sample_pointing_3sigma_budget_deg']:.3f}° three-sigma pointing under this weak plane-only study criterion. Speed and pointing limits cannot both be saturated and treated as a joint pass: pointing also changes orbital energy. The joint periapsis Monte Carlo uses the stated 0.1° pointing band. These are investigation requirements, not customer inputs, measured capability, the historical 0.0274 m/s dispersion or a 30-day perturbed error distribution.

## Engine-only disposal, including all failed releases

The carrier's disposal solution uses its engine with **zero payload-release recoil credit**. A declared 20 N / 220 s chemical-thruster surrogate burns continuously retrograde from apolune to a two-body cutoff targeting −100 km osculating perilune, then coasts. Cutoffs are fixed before independent GMAT replay. Native replays use GRGM900C, Earth/Sun DE421, mass depletion, and the same coefficient frame. All **24 native cases** reach the 1737.4 km reference sphere within 24 hours: no failures or all twelve payloads captive at both gravity degrees, plus ±1% burn-duration and ±1° pointing perturbations for the twelve-failure case. The worst propellant use is **{max(x['native_propellant_used_kg'] for x in disposal['cases']):.4f} kg**, below the independently allocated 20 kg reserve.

| Staging orbit (km) | Nominal all-failure burn (s) | Propellant, 40/40 (kg) | Sphere time from ignition (h) |
|---|---:|---:|---:|
{chr(10).join(rows)}

Earth return, high-lunar disposal and escape are explicitly compared in the result file. Earth return has no valid targeted solution and is rejected as an unsupported claim. Escape energy alone cannot establish an Earth-return path or long-term safe disposal. High-lunar circularization is only an impulsive energy bound. A native sphere impact is a dynamical solution; a selected impact site, terrain model, actual engine, environmental/policy review and applicable approval are external.

## Launch delivery energy remains separate

The same twelve-payload manifest, 280 kg dry carrier, 20 kg disposal reserve and 220 s Isp produce the following ideal patched-conic boundaries. One case starts in 500 km circular LEO and must supply TLI; the other arrives on the same ideal lunar encounter after launch/transport supplied TLI energy. LOI is still charged to the carrier. Neither is evidence that a named provider can deliver that mass/state.

| Starting boundary | Staging orbit (km) | Carrier TLI (m/s) | LOI (m/s) | Required boundary wet mass (kg) |
|---|---|---:|---:|---:|
{chr(10).join(mass_rows)}

![Independent disposal propellant and distinct starting-energy mass boundaries.](../{path}/figures/lunar_independent_disposal.png)

Finite TLI/LOI, launch-provider mass/cost availability and integrated thermal/operations closure remain open. The full lunar multi-payload campaign, release-order/direction optimization, updated full inertia/attitude/propellant histories and failure recovery have not been completed by independent single-release maps or by the disposal replay.

## Evidence and reproduction

The [package README](../{path}/README.md) provides commands; [MANIFEST.json](../{path}/MANIFEST.json) pins every supplied file. Inputs include exact copied ACR1 results, the accepted native signature captures and their SHA-256 source identities. No third-party binaries, ephemerides or gravity data are redistributed. Native model/runtime hashes identify the required installation. The [criterion recommendations](../{path}/CRITERION_RECOMMENDATIONS.json) map all 40 original computational programme rows; they do not change tracker states or convert external evidence into a numerical pass.
'''
    (ROOT/'docs/PROGRAMME_STUDIES_ACR1.md').write_text(report)
    print('Wrote docs/PROGRAMME_STUDIES_ACR1.md and source-derived lifetime figure')


if __name__=='__main__':main()
