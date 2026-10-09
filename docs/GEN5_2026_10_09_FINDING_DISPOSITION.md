# Gen5 finding disposition — finite stator, feeder and mission

**Decision state: adverse finding recorded; no new rated performance baseline selected.** This document distinguishes the evaluated Gen5 geometry and historical model outputs from the unselected R1 feeder. It is a change-impact record for reviewers, not an engineering release.

## P118 force discrepancy

The historical rated shot uses a periodic thrust constant across 1.300 m of powered travel. The actual Gen5 CAD declares a 162-belt finite stator ending at 1.296 m, with a magnet array initially at 0.230–0.570 m. Direct array/stator overlap ends after 1.066 m of travel. The [finite analytic force map](../validation/P118_gen5_finite_force_map.md) gives 1.042 kJ ideal work and a 12.448 m/s geometry-only result under independently optimized phase at each station. It shares the earlier cuboid magnetic field law and is not independent FEM.

| Prior claim/output | Disposition | Required rerun before a performance claim |
|:--|:--|:--|
| 16.029 m/s rated 3U exit speed | **Challenged; historical periodic-model result** | Independent 3-D force integral, revised finite-stator winding/drive and coupled shot with actual phase, current and voltage limits |
| 10.07 g peak acceleration and 162.3 ms pulse | **Historical model point** | Recompute the trajectory and actual force/time history for a selected geometry |
| 18.8% net efficiency, 2.78 kJ draw, 47 J recovery and 1,162 J arrest | **Historical coupled-model outputs** | Reconcile finite-force trajectory, electrical losses, source sizing and brake entry state; separately close P117's 124.488 J gross-energy remainder |
| 0.0274 m/s simulated dispersion | **Historical control simulation** | Recompute under finite-stator handover, latency and uncertain force map; no measured repeatability claim |
| 28.800775 km immediate orbit-axis check and 1.60 lifetime multiplier | **Conditional on the 16.029 m/s input** | New orbit and lifetime runs after a credible release speed is selected; the Cartesian check itself remains mathematically valid at its stated input |
| 126.562 kg modeled Gen5 dry mass | **Unaffected by P118 alone, still incomplete installed mass** | Rerun if stator, inverter, energy source, feeder or structure changes |

## R1 candidate boundary

The [R1 STEP/FreeCAD geometry candidate](../cad/FEEDER_CANDIDATE_R1.md) clears the specific track/cassette clash and twelve scripted 3U envelope transfers after external width increases from 530 to 570 mm. It does not supply a lift actuator, launch restraint, fault handling or provider interface. Its 0.99 kg simple enclosure-skin delta does not authorize using 126.562 kg as an R1 installed mass. The evaluated Gen5 fit failure remains in the record.

## Mission boundary

The [matched reference comparison](MATCHED_MISSION_REFERENCE.md) evaluates one common inertial target and one common twelve-shot optimizer. Its one-event host propellant values and accepted prefixes depend on assumed host thrust, dry mass, fuel, Isp and device class. No sampled twelve-shot option closes; this is a failure to find an accepted trajectory under the stated search, not a global impossibility proof. A provider-specific mission and all relevant conventional alternatives remain to be modeled.

## Release rule

Use the historical numbers only with the words *periodic-model input* or *conditional historical result*. Use **12.448 m/s** only as a geometry-only ideal-phase screen. A future corrected model needs its own revision, source/result hashes, uncertainty and convergence, selected CAD, dependent budget and mission reruns, manuscript rebuild and independent review. Neither Gen5 final academic freeze nor a hardware/flight release is declared by these three screens.
