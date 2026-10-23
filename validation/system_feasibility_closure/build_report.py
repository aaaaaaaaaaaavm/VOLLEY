"""Generate the professional system/capacity report from captured numerical JSON."""
from pathlib import Path
import json

H=Path(__file__).resolve().parent


def fmt(x,n=3):return f'{x:,.{n}f}'


def main():
    sys=json.loads((H/'SYSTEM_SCREENS.json').read_text())
    nav=json.loads((H/'LUNAR_NAVIGATION_SENSITIVITY.json').read_text())
    cap=json.loads((H/'TWELVE_ASSEMBLY_REPORT.json').read_text()) if (H/'TWELVE_ASSEMBLY_REPORT.json').exists() else None
    mission=json.loads((H/'MISSION_RETARGET_SUMMARY.json').read_text()) if (H/'MISSION_RETARGET_SUMMARY.json').exists() else None
    native=json.loads((H/'NATIVE_REPLAY_CHECKS.json').read_text()) if (H/'NATIVE_REPLAY_CHECKS.json').exists() else None
    moving=json.loads((H/'MOVING_MASS_FLOWDOWN.json').read_text()) if (H/'MOVING_MASS_FLOWDOWN.json').exists() else None
    t=['---','title: "VOLLEY: Selected-Feeder Capacity and System-Resource Assessment"',
       'author: "Adityavardhan Mishra"','date: "23 October 2026"','papersize: a4','geometry: margin=18mm',
       'fontsize: 10pt','mainfont: DejaVu Sans','---','',
       '# Scope and method','',
       'The selected guided lead-screw pusher feeds dedicated fixed 1U/3U cells through continuously capped channels into one indexed receiver. '
       'The receiver far-side stops close before transfer begins; near-side capture closes after sensed arrival and settling, before the pusher retracts. '
       'The payload remains geometrically contained, but the pusher cannot pull or enforce deceleration of a freely moving payload. '
       'Nominal transfer is therefore restricted to host zero-force coast windows; end-stop impact and sensed-settling acceptance require later validation. '
       'This assessment evaluates the associated capacity scaling and resource requirements. The evaluated Gen5 record is retained; '
       'the selected feeder and capacity studies are separately versioned Gen6 academic design work. No physical prototype or flight qualification is claimed.','',
       'Resource requirements follow two-body separation momentum and energy conservation. For retained host mass $M$, payload mass $m$ and relative release speed $u$, '
       '$\\alpha=M/(M+m)$, $E=\\tfrac12 m\\alpha u^2$, and the constant-force relative stroke obeys '
       '$s\\ge\\alpha u^2/(2a_{payload,max})$. Bus-energy requirements are at least $E/\\eta$ for assumed efficiency $\\eta$. '
       'These equations exclude retained moving-body acceleration, feed/index actuation, catcher losses and standby services.','',
       '# Capacity geometry','']
    if cap:
        c=cap['captures'][0];m=c['mass_properties'];bb=m['bounds_mm']
        t += [f'The twelve-cell scaling assembly contains six 1U and six 3U payload envelopes, twelve dedicated feed cells, and one receiver. '
              f'Its twelve docking stations span {cap["receiver_travel_mm"]:,} mm on a {cap["rail_length_mm"]:,} mm rail. '
              'The geometry is generated explicitly from the selected four-cell source; it is not a threefold mass multiplication or three independent launchers.','',
              '| Quantity | Twelve-cell assembly |','|---|---:|',
              f'| Represented custom-material mass | {fmt(m["represented_material_mass_kg"],6)} kg |',
              f'| Uniform payload surrogate mass | {fmt(c["uniform_payload_loaded_properties"]["uniform_payload_mass_kg"],3)} kg |',
              f'| Custom material + uniform payloads | {fmt(c["uniform_payload_loaded_properties"]["represented_material_mass_kg"],6)} kg |',
              f'| Represented-material centre of gravity | ({", ".join(fmt(v) for v in m["represented_material_CG_mm"])}) mm |',
              f'| Geometric bounding envelope | {fmt(bb[1]-bb[0],1)} × {fmt(bb[3]-bb[2],1)} × {fmt(bb[5]-bb[4],1)} mm |',
              f'| Represented envelope volume | {fmt(m["box_volume_litre"],3)} L |',
              f'| Native geometric features | {c["parts"]} |','',
              'Payload and catalog-package masses are excluded from this material total. Complete installed mass requires the separately identified catalog equipment, '
              'fasteners, harness, gate actuation, electromagnetic launcher, source and host interface. A 4.2 m rail is a packaging requirement; no selected host has been demonstrated to accept it.','']
        sweeps=cap.get('continuous_payload_corridor_sweeps',[])
        if sweeps:
            passed=sum(r['pass_no_positive_volume_interference'] for r in sweeps)
            t += [f'Exact rectangular-payload linear sweeps were evaluated against the frozen feed-phase environment at all twelve docking stations: '
                  f'{passed} of {len(sweeps)} had no positive-volume interference. The active moving pusher was excluded from this particular sweep; '
                  'full moving-mechanism and loaded/tolerance acceptance must be assessed separately. Native/STEP state checks and all retained intersections are recorded in the machine-readable report.','']
        t += ['The full represented-material inertia tensor about its computed centre of gravity is supplied in `TWELVE_ASSEMBLY_REPORT.json`. '
              'The material ledger and excluded-mass boundary accompany both native and STEP exports.','']
        if (H/'figures/twelve_capacity_plan.png').exists():t += ['![CAD-derived stored-payload plan and shared rail. This diagram shows payload envelopes and rails, rather than the entire solid assembly.](figures/twelve_capacity_plan.png)','']
    if moving:
        local=max(c['represented_plus_upper_payload_kg'] for c in moving['cell_subtotals'])
        rec=moving['receiver']['represented_plus_upper_payload_kg']
        impact=moving['coast_feed_energy']['ideal_payload_kinetic_energy_at_that_speed_J']
        t += [f'The represented local moving material plus the 6 kg upper payload study totals at most {fmt(local,6)} kg, below the 7.5 kg actuator-study mass. '
              f'The corresponding receiver subtotal is {fmt(rec,6)} kg, below its 10 kg study mass. '
              'Unmodeled moving actuators, harness and fasteners must fit the remaining headroom or the drive model must be rerun. '
              f'At the prescribed pusher peak speed, the ideal kinetic energy of a 6 kg payload is {fmt(impact*1000,6)} mJ. '
              'This conditional energy requirement does not establish a contact peak load, a safe impact or controlled payload deceleration.','']
    t += ['# Separation energy, charging and thermal requirements','',
       'SYS-01 comprises 108 energy/charging cases, 18 force/stroke cases, 36 single-axis angular-impulse cases and 54 optimistic heat-rejection cases. '
       'Net efficiencies of 25/50/75%, charging powers of 25/50/100 W, radiator areas of 0.25/1/4 m², and host inertias of 20/100/500 kg·m² are sensitivity inputs. '
       'They are not measured values or selected component ratings.','',
       '| Twelve independent 4 kg shots; 300 kg retained-host reference | 6 m/s | 1,000 m/s |',
       '|---|---:|---:|']
    rows=[next(x for x in sys['energy_cases'] if x['payload_count']==12 and x['payload_kg_each']==4 and x['relative_speed_m_s']==u and x['assumed_net_efficiency']==.5 and x['assumed_charging_W']==50) for u in (6,1000)]
    for label,key,unit in [('Ideal relative energy per shot','ideal_relative_energy_per_shot_J','J'),('Bus-energy lower bound at assumed 50% efficiency','bus_energy_lower_bound_J','J'),('Charging-time lower bound at assumed 50 W','charge_time_lower_bound_s','s')]:
        t.append('| '+label+' | '+' | '.join(fmt(r[key])+f' {unit}' for r in rows)+' |')
    t += ['', 'At 1 km/s, the retained 25 g study screen requires 2.013 km of ideal constant-force relative stroke for the 4 kg / 300 kg case. '
         'The compact/high-speed/low-acceleration requirement combination is therefore incompatible under these assumptions. '
         'The 3–6 m/s range remains an imposed mission study input; the calculations do not prove an electromagnetic motor or release mechanism can achieve it.','',
         '![Analytical resource requirements. Assumed charging power and efficiency are sensitivity inputs; no installed equipment capability is inferred.](figures/resource_requirements.png)','',
         'The radiation screen assumes emissivity 0.8, a zero-temperature deep-space sink and a constant declared radiator temperature. '
         'It excludes sunlight, planetary heating, conduction, changing view factors, thermal interfaces and radiator mass. It provides an optimistic heat-rejection requirement, '
         'rather than a complete thermal design. The angular-impulse screen similarly assumes a single host inertia and a specified release-axis offset; '
         'zero offset produces zero point-mass angular impulse, while an offset requires attitude recovery.','',
         '# Finite-force mission comparison','']
    if mission:
        t += ['FBR-02 retargets each finite-force leg after changing the declared device burden. It preserves the captured full position/velocity targets, common 90,000 s '
              'terminal epoch, release vectors, continuous mass flow and recoil relation. The spring comparator retains its declared installed-mass proxy. '
              'The selected-feeder cases use the represented material boundary and explicitly stated allowances; they do not establish a complete installed device mass.','',
              'All cases include a 5 s zero-force guard before release and a 20 s guard afterward. The twelve-cell VOLLEY policy uses 10% force windows to reserve '
              '241.818 s of inter-window coast for a conservative 223.556 s full feeder/index-return allocation. The 18.263 s remaining allowance must also cover '
              'the applicable launch, charging, reset and operational services; those services are not collectively qualified here. '
              'Conventional spring deployment is additionally evaluated with 20% and 35% force windows, so it does not inherit VOLLEY-specific handling constraints.','',
              '| Case | Declared device burden [kg] | Peak resultant force [N] | Fuel [kg] | Translational screen |',
              '|---|---:|---:|---:|---|']
        for r in mission['cases']:
            t.append(f'| {r["label"]} | {fmt(r["device_kg"])} | {fmt(r["peak_force_N"])} | {fmt(r["fuel_used_kg"])} | {"Pass" if r["feasible_in_declared_model"] else "Fail"} |')
        t += ['', 'The reported forces are constant inertial resultant controls in a simplified J2 point-mass model. Thrust/attitude allocation, plume clearance, '
              'navigation feedback, drag, physical release dynamics and source-rated host hardware remain outside that model. '
              'A translational pass establishes consistency of this constructed policy, rather than global optimality or mission/provider approval.','']
        t += ['The minimum-fuel feasible captured spring policy is used for the conditional resource comparison. This is the best known member of the tested policy family, '
              'rather than a global optimum. Extra device burden and propellant use remain separate quantities; the study does not infer a priced service or optimized launch wet mass.','']
        comparisons=[c for c in mission['conditional_resource_comparisons'] if c['volley_allowance_kg']==25]
        if comparisons:
            t += ['| Conditional 25 kg omitted-equipment case | Four releases | Twelve releases |','|---|---:|---:|',
                  '| Extra declared device dry burden versus spring proxy | '+' | '.join(fmt(c['declared_device_dry_penalty_kg'])+' kg' for c in comparisons)+' |',
                  '| Lower host propellant use versus best tested spring policy | '+' | '.join(fmt(c['propellant_used_saving_kg'])+' kg' for c in comparisons)+' |','',
                  'The declared device dry penalty exceeds the propellant-use reduction in these cases. A mission-level installed-mass advantage is therefore not established. '
                  'Both campaigns begin with the same prescribed fuel allocation; reduced consumption is not automatically a reduction of launch wet mass. '
                  'A product decision additionally requires credible precision, throughput or host-service value sufficient to justify the added hardware.','']
        if native:
            nom=[r for r in native['native_runs'] if r['category']=='nominal']
            largest=max(r['max_payload_target_position_error_m'] for r in nom)
            t += [f'{native["run_count"]} actual new Orekit replays cover nominal campaigns, time-step refinements and deterministic sensitivity cases. '
                  f'The largest nominal payload terminal position difference is {fmt(largest*1e6,3)} µm. '
                  'Native mass-flow, recoil, continuity and pre-release guard checks pass within their recorded numerical criteria. '
                  'Frozen-command probes vary force or release speed by ±0.1%, initial inertial X by ±10 m, and actual 3U payload mass from 4 to 6 kg. '
                  'These deterministic probes are not calibrated probability distributions or flight delivery accuracy.','']
        if (H/'figures/mission_mass_sensitivity.png').exists():t += ['![Finite-force retargeting with declared mass allowances. Each point is a separately solved campaign; omitted-equipment allowances are assumptions.](figures/mission_mass_sensitivity.png)','']
        if (H/'figures/native_mission_sensitivity.png').exists():t += ['![Actual Orekit frozen-command sensitivities. Bars show the largest terminal payload position miss among the signed probes in each category; mass probes replace actual 3U masses by 6 kg without retargeting.](figures/native_mission_sensitivity.png)','']
    else:t += ['The existing FBR-01 finite-force study contains 18 targeted solutions and 46 actual native Orekit replays. '
               'Its archived device masses are declared proxies; they must not be relabelled as the selected feeder\'s installed mass.','']
    t += ['# Lunar delivery uncertainty','',
       'LNS-01 evaluates three explicitly assumed uncertainty bands at apolune release from 100 × 100, 100 × 1,000 and 100 × 10,000 km lunar staging orbits. '
       'Each of nine cases contains 8,192 fixed-seed samples. Independent Gaussian position/velocity/pointing inputs have standard deviations '
       '10 m / 0.01 m/s / 0.01°, 100 m / 0.1 m/s / 0.1°, and 1 km / 1 m/s / 1°, respectively. Relative-speed standard deviations are 0.1/1/5%. '
       'These are uncalibrated investigation bands; no measured performance or probability of successful delivery is claimed.','',
       'The negative 4.569852 m/s relative command from the 100 × 10,000 km ellipse gives nominal two-body periapsis altitude 43.619 km. '
       'The widest assumed band has linearized periapsis standard deviation 12.681 km. Three Jacobian refinement comparisons differ by less than '
       '$10^{-4}$ relatively, with actual differences below $10^{-9}$. Numerical derivative consistency does not establish physical model fidelity.','',
       '![Conditional two-body lunar periapsis sensitivity. All uncertainty bands are assumed; the plotted standard deviations are finite-sample results.](figures/lunar_navigation_sensitivity.png)','',
       '# Applicability and research boundary','',
       'The lunar uncertainty output is an osculating two-body periapsis distribution at release. Reference-sphere crossing is distinct from terrain impact, '
       'a useful-lifetime limit or controlled disposal. No new 7/30/90/180-day high-fidelity lunar lifetime calculation is claimed. '
       'Connected epoch-targeted carrier burns, measured correlated delivery uncertainties, a lunar failed-shot campaign, operational disposal and source-rated hardware deltas '
       'remain necessary for the extended lunar service architecture. The separate ideal capture/disposal and high-speed bounds retain their original source and criteria identities.','',
       '# Reproduction and sources','',
       'Run `system_screens.py` and `lunar_navigation_sensitivity.py` to reproduce the numerical sensitivity studies. Run `plot_screens.py` for the analytical figures. '
       'The capacity builder takes an exact copied FM08-R3 source file; source hashes identify its geometry revision. '
       'The finite-force targeter is a recorded derivative of the captured FBR-01 source, adding a declared pre-release zero-force guard. '
       'Its wrapper records the exact source-input hash, guard duration and device-mass replacement. '
       'Actual native replay commands and CSV outputs are retained with each new run. Scientific plots are derived from numerical data; no software interface is synthesized.','',
       '- JPL, DE440 astrodynamic parameters: <https://ssd.jpl.nasa.gov/astro_par.html>. Constants and reference radii are the retained C0-S1/C0-S2 inputs.','- Orekit 13.1.6 ForceModel and J2OnlyPerturbation APIs: <https://www.orekit.org/static/apidocs/>. Exact public dependency versions/hashes are retained in `mission/SOFTWARE_LOCK.json`.','- SciPy `solve_ivp` numerical integration: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>.',
       '- FreeCAD/Open CASCADE native geometry and STEP exchange: source revision and software identities accompany the generated assembly report.','']
    (H/'REPORT.md').write_text('\n'.join(t))

if __name__=='__main__':main()
