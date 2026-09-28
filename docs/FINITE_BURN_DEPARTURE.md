# Finite-duration host burns and slew-constrained departure

Adityavardhan Mishra · 17 September 2026

I replace two ideal impulses with integrated fixed-thrust arcs and mass flow. Every case includes two rest-to-rest slew budgets and settling; the initial attitude is pre-positioned. The assumed planar actuator law is not flight ADCS or a three-axis rigid-body solution.

| Release (s) | Speed (m/s) | Thrust (N) | Replay | Replan | Fuel used (kg) | Terminal position (m) |
|---:|---:|---:|---|---|---:|---:|
| 1200 | 1 | 1 | fail | no accepted result | 0.417157 | 9632.229365 |
| 1200 | 1 | 10 | fail | pass | 1.374296 | 0.000129 |
| 1200 | 1 | 100 | fail | pass | 1.218621 | 0.000129 |
| 1200 | 2 | 1 | fail | no accepted result | 0.417157 | 7903.772793 |
| 1200 | 2 | 10 | fail | pass | 1.191408 | 0.000128 |
| 1200 | 2 | 100 | fail | pass | 1.061853 | 0.000129 |
| 1800 | 1 | 1 | fail | no accepted result | 0.358642 | 7205.853718 |
| 1800 | 1 | 10 | fail | pass | 0.732390 | 0.000064 |
| 1800 | 1 | 100 | fail | pass | 0.693327 | 0.000064 |
| 1800 | 2 | 1 | fail | no accepted result | 0.292304 | 7613.976473 |
| 1800 | 2 | 10 | fail | pass | 0.567854 | 0.000064 |
| 1800 | 2 | 100 | fail | pass | 0.539687 | 0.000064 |

Each result retains three bounded search attempts and explicit burn, slew, fuel and endpoint-perigee accounting. A failed bounded search is not proof that no trajectory exists. Full twelve-payload replanning, navigation uncertainty, physical attitude torque/momentum, plume clearance, flexible dynamics and disposal remain open.

The release speeds are mission assumptions. P92-S5 supplies separate force-law candidates; it does not establish the accuracy or installed burden required by this mission.

Numerical verification: PASS. Physical mission acceptance uses unchanged 10 m / 0.01 m/s terminal bands and 2 kg reserve.

[Criteria](../validation/P113_S11_finite_burn.md) · [Complete attempts](../analysis/results/finite_burn_departure.json)
