# Combined release-error corners

I combine six simultaneous error terms around each of the two stored S4 release events. Each event starts from its nominal host state. This is **conditional event evidence**, not a robust two-event campaign or a probability of success. P113, E5 and P92 remain open.

The illustrative base box uses 0.1 m per host position axis, 0.0001 m/s per host velocity axis, 0.0005 m/s release-speed error and 0.005 degrees release-direction error. These are assumptions, not hardware requirements or provider capabilities.

**512 corners evaluated. Numerical verification: PASS.** Mission failures remain in the table and JSON.

| Event | Box multiplier | Corners within 10 m / 0.01 m/s | Worst sampled position (m) | Worst sampled velocity (m/s) |
|---|---:|---:|---:|---:|
| 1 | 0 | 64/64 | 0.000064 | 0.00000008 |
| 1 | 1 | 64/64 | 6.591224 | 0.00733767 |
| 1 | 2 | 44/64 | 13.182605 | 0.01467563 |
| 1 | 5 | 20/64 | 32.957482 | 0.03669077 |
| 2 | 0 | 64/64 | 0.000002 | 0.00000001 |
| 2 | 1 | 64/64 | 0.879464 | 0.00148286 |
| 2 | 2 | 64/64 | 1.758932 | 0.00296577 |
| 2 | 5 | 64/64 | 4.397376 | 0.00741484 |

A corner maximum is only the maximum among the sampled corners. Nonlinear maxima inside or along the edges of the box are not excluded. The JSON separately reports the triangle-inequality envelope of the local linear model and direct-versus-linear discrepancies.

## What remains to close

First-event host error must be propagated through the second manoeuvre and release, with a declared navigation/control policy. Correlations, full manifest, pointing recovery, collision clearance, disposal reserve and provider resource limits remain absent. The 1,800 s nominal release gap exceeds the illustrative 300 s reserved interval by 1,500 s; this arithmetic is not proof of settling or safety.

A release-cell repeatability target must be allocated together with common navigation and pointing errors. Increasing mechanical precision cannot remove a common host-state error. Reject or change the mission/error allocation if the required operational box cannot satisfy the terminal bands.

[Frozen criteria](../validation/P113_S6_combined_release_errors.md) · [Every corner and source hash](../analysis/results/combined_release_errors.json) · [S5 sensitivities](OPERATIONAL_UNCERTAINTY.md)

Reproduce: `python analysis/combined_release_errors.py --check`.
