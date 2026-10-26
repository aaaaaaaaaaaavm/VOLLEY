# ACR1 partial-occupancy finite-force mission results

**26 October 2026 · ACR1-PARTIAL-OCCUPANCY-01.** These are actual new two- and four-payload computations using the current same-size passive 4 kg 3U surrogate. They extend the accepted twelve-payload reference, preserved at commit ca67ea95bf5729aa293da3728f79e23d79da9262. They do not establish mixed-size Gen6 performance or actual provider compatibility.

## Matched boundary

Both architectures retain their full twelve-position hardware: ACR1 device dry 156.55671970039353 kg including 7 kg power/control once, versus the frozen 72 kg conventional-device proxy. The unchanged wet host is 500 kg, including 20 kg propellant, at Isp 220 s. Partial occupancy changes payload inventory only: 8 kg or 16 kg. Initial assemblies are therefore 664.556719700/672.556719700 kg ACR1 and 580/588 kg conventional. No empty-cell mass or unselected replacement device is removed.

Targets are exact first-two/first-four subsets of the accepted uniform2 and alternating1/3 families. Initial state/24 October 2026 TAI epoch, release slots 450/900 s or 450/900/1350/1800 s, common host target, and final evaluation at **91800 s** are unchanged. Thus the two- and four-payload final evaluation is 90900 s and 90000 s after their last releases, respectively; it is not relabeled 24 hours after their last release. The host recovery remains at the common first Kepler period, about 5676.978 s, followed by a continuous coast. No native host state is reset to a target.

Finite-force policy, continuous mass depletion, source-calibrated commanded release and recoil are unchanged. All architectures retain 5 s pre/20 s post guards; ACR1 retains 400 s zero-force loading coast for the 355 s mechanism cycle. The command interpolates the accepted computational 1/2/3 m/s source rows and remains clipped to 1–3 m/s. Inherited fields named `measured_release` refer to computed source traces, not physical measurements. The fixed spring uses 2 m/s; ideal pretrim uses frozen per-payload energy tables. Conventional policies may use wider 35%/45% force windows because no 400 s mechanism coast is imposed on them.

## Actual selected outcomes

| Count | Family | Authority | ACR1 fuel (kg) | Fixed2 spring (kg) | Ideal pretrim (kg) |
|---:|---|---:|---:|---:|---:|
| 2 | uniform_2 | 1 N | 0.012398876 | 0.007893670 | 0.012398869 |
| 2 | uniform_2 | 5 N | 0.012398876 | 0.007893670 | 0.012398869 |
| 2 | alternating_1_3 | 1 N | no tested pass | no tested pass | 0.014428505 |
| 2 | alternating_1_3 | 5 N | 0.066359438 | 1.556265075 | 0.014428505 |
| 4 | uniform_2 | 1 N | 0.019642651 | 0.015706426 | 0.019642641 |
| 4 | uniform_2 | 5 N | 0.019642651 | 0.015706426 | 0.019642641 |
| 4 | alternating_1_3 | 1 N | no tested pass | no tested pass | 0.026209613 |
| 4 | alternating_1_3 | 5 N | 0.107286193 | 2.594045517 | 0.021124344 |

All **28 finite-force candidates** solved the original 1 mm position / 1 micrometre/s targeting gates. Force-ceiling failures remain failures. In the alternating family ACR1 peaks near 4.204 N and has no tested 1 N pass; ideal pretrim succeeds at 1 N for both counts. Fixed2 spring now has 5 N passes for two and four payloads, unlike the retained twelve-payload candidate outcome. The lowest-fuel four-payload fixed2 pass uses 2.594045517 kg, while its tested 45% policy consumes 2.851060101 kg. Selection preserves the actual best feasible policy rather than transferring twelve-payload results.

No propellant or initial wet-mass advantage over ideal pretrim is demonstrated. Differences of order 1e-8 kg between uniform ACR1 and pretrim are numerical scale; they are not a physical advantage. The retained hardware mass difference is 84.556719700 kg for every occupancy. These are bounded sampled policies, not global optimizations or impossibility proofs.

## Independent verification

All 28 candidates passed separately reaggregated mass flow, released inventory, linear momentum, recoil mapping, event continuity and release-guard checks. Source/current mass and final inventory close without duplicating the 20 kg reserve. Four ACR1 policies retain 400 s loading coasts and original command limits.

The unchanged native Orekit 13.1.6 / Hipparchus 4.0.3 Java replay was actually executed for **17 cases**: thirteen distinct selected trajectories and four 60→30 s ACR1 refinements. It reads frozen force/release commands, integrates host arcs consecutively, recomputes ACR1 recoil from its independently integrated mass, and propagates payloads to the same final epoch. Maximum native payload target difference: **1.03621474e-05 m / 1.1432157e-08 m/s**. Maximum host-state position difference: **1.27338562e-05 m**. Maximum independent native mass-flow residual: **2.95585778e-12 kg**. Maximum native momentum residual: **1.04287598e-09 kg·m/s**. Maximum 60→30 s terminal-position change: **7.58539187e-06 m**, below the original 1 mm refinement gate.

These numerical differences do not establish physical delivery accuracy. Fixed-axis J2 point-mass gravity, constant inertial resultant force, ideal mass flow and point release remain the accepted model boundary. Real host inertia/attitude/plume, navigation, drag/higher gravity, near-field exit geometry, failures, joint dispersion, provider services and physical qualification remain distinct requirements.

## Source and reproduction

`SCOPED_EXTENSION.diff` records the narrow patch: derive occupancy count for inventory/completion/ledger/coast aggregation, and retain full CAD mass precision. Targeting equations, gravity, calibration, commands, force windows and acceptance thresholds are unchanged. `SOURCE_IDENTITIES.json` pins the accepted inputs; `SUMMARY.json`, `CASE_DEFINITIONS.json`, every model/release JSON/command CSV/trajectory CSV and the native raw CSV/logs preserve the actual evidence. Runtime versions are captured. Scientific dependencies for this capture are NumPy 2.3.5 and SciPy 1.17.0.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_cases.py
python3 verify_and_replay.py --jars-dir /path/to/orekit-13.1.6-and-hipparchus-4.0.3-jars
python3 check_capture.py
```

Use the supplied drivers, which operate on frozen subsets; calling the inherited model's original main entry point would recreate its twelve-payload example inside this study copy. Java is invoked through its installed compiler module where a separate javac executable is absent. No third-party jars are redistributed. `technical/` updates the source-pinned common-case comparison with actual 2/4 outcomes and the retained accepted12 results; the earlier pre-run reference packet remains a dated record.
