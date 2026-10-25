# G5-MISSION-01

Accepted same-input synthetic comparison for twelve 4 kg 3U releases from the corrected Gen5 device and two spring class-study comparators.

- `MISSION_REPORT.md`: findings, comparison table, model boundary and figures.
- `MISSION_INPUTS.json`: mass, propulsion, timing, recoil mapping and source identities.
- `TARGETS.json`: architecture-independent full PV targets at the common 91800 s epoch.
- `MISSION_COMPARISON.json`: fourteen constructed two-window policy candidates.
- `SELECTED_CASES.json` and `MISSION_RESULTS.csv`: best tested feasible selections at 1 N and 5 N.
- `NATIVE_REPLAY_CHECKS.json`: nine accepted Orekit replay cases, conservation/guard checks and two step refinements.
- `release/`: frozen finite-force commands, states, masses and trajectories.
- `native/`: actual native replay PV output and logs. Each selected case is named separately.
- `figures/`: inspected scientific PNG, PDF and SVG artifacts.
- `SOFTWARE_LOCK.json` and `MISSION_CAPTURE.json`: runtime/source and accepted-artifact identities.

Use the portable commands in [the public engineering package](../README.md#reproduce-a-short-example). The runner creates a scratch copy, verifies the exact jar lock and adapts the recorded jar-directory selector. Original source and execution receipts retain the captured runtime identity.

The initial wet bus is 500 kg, comprising 480 kg dry and 20 kg propellant. The propellant is included once. The spring 72 kg device is a declared class-study assumption. The ideal ground-pretrimmed spring freezes a per-payload energy table before native replay; it does not claim inflight retasking. Only Gen5 requires the 400 s loading coast. Spring may select the same short-window schedule or wider available windows.

The `provisional_window_set/` and `provisional_native_log_naming/` folders retain intermediate audit history and are excluded from the accepted artifact capture. The first records the initial schedule set before adding the shared narrow-window spring option. The second preserves native outputs from an aggregate-reporter log-path defect; the accepted checker uses distinct log names and completed successfully. These folders contain no alternative accepted result set.

This is a synthetic fixed-axis J2 point-release study with constant inertial host forces and Isp 220 s. Numerical agreement does not establish physical delivery accuracy or a global mission optimum.
