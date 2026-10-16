# Gen5 orbit, lifetime and matched-mission disposition

The 450 km Gen5 study and 500 km mixed-size Gen6 scenario are different configurations. Release speed relative to the host is not generally the payload inertial increment. A 4 kg payload separating at 16.029 m/s from a retained 300 kg host gains 15.818092 m/s and recoils the host by 0.210908 m/s. P115 instead imposes a 16.029 m/s inertial input; its 28.800775 km axis rise is an input-state geometry check.

## Shared-atmosphere lifetime cross-check

A separate DOP853 orbit-averaged energy/eccentricity integration uses midpoint anomaly quadrature and the declared static exponential density table. It imports no historical lifetime routine. Stopping at 120 km perigee gives:

| Imposed inertial increment m/s | Base lifetime yr | Boosted lifetime yr | Ratio |
|--:|--:|--:|--:|
| 2.500000 | 1.303955 | 1.411023 | 1.082110 |
| 12.448437 | 1.303955 | 1.892327 | 1.451222 |
| 16.029000 | 1.303955 | 2.089150 | 1.602165 |

Refining from 360 to 720 anomaly nodes and rtol 1e-7 to 1e-9 changes a ratio by at most 0.000145%, below the declared 0.5% numerical screen. These numbers reproduce the historical 1.60 and spring 1.082 ratios under a shared static atmosphere; they do not validate the atmosphere, physical release or lifetime in space. Uniform density/BC scaling is not a test of solar invariance. The 12.448 m/s row is an imposed inertial value for sensitivity, not the finite-host delivered state or a motor rating.

## Matched reference outcomes

All options carry twelve 4 kg payloads, a 300 kg base host, 10 kg fuel, 2 kg reserve and 220 s host Isp. The common single-event target is +16.029 m/s inertial prograde. The 72 kg spring set and 126.562 kg Gen5 device are study assumptions.

| Option | Device kg | Host preburn m/s | Event fuel kg | Accepted campaign prefix | Passing prefix corners |
|:--|--:|--:|--:|--:|--:|
| Spring dispenser class | 72.000 | 13.552402 | 2.692639 | 4/12 | 24/64 |
| Gen5 finite-force ideal upper | 126.562 | 3.683499 | 0.826601 | 1/12 | 0/64 |
| Gen5 historical rated model | 126.562 | 0.132326 | 0.029719 | 1/12 | 0/64 |

The single-event ideal solutions reach the same state by combining release with a host burn. Gen5 saves event fuel at an installed device penalty of 54.562 kg in this class comparison. A complete twelve-shot sampled solution is absent for every option. The optimizer stopping at a missing accepted seed is not proof of global infeasibility; prefix corner passes are not campaign success probabilities. Finite thrust, host maneuver/service restrictions and acceptance tolerances apply only as declared in [the full comparison](MATCHED_MISSION_REFERENCE.md).

No matched onboard-propulsion, drag or quoted OTV service model is available. Those alternatives remain unevaluated, rather than being assigned losing scores. No customer, provider, continuous collision-clearance, disposal or economic advantage is established.

[P134 inputs and result](../analysis/results/gen5_lifetime_crosscheck.json) · [Matched twelve-shot case](../analysis/results/matched_mission_reference.json) · [A15 corrected orbital screen](../validation/A15_poem_campaign.md).
