# Twelve-payload finite-burn campaign — P113-S12

Adityavardhan Mishra · 26 September 2026

A matched reference screen carries finite burns, propellant, host recoil and the previous release attitude through twelve planned deliveries. Every scenario uses the same targets and release times. The host dry mass is held equal as a sensitivity, not an installed architecture comparison.

| Speed (m/s) | Thrust (N) | Delivered / 12 | Fuel used (kg) | Passing partial-history corners |
|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0.000000 | no accepted prefix |
| 1 | 10 | 3 | 6.018343 | 16 / 64 |
| 1 | 100 | 4 | 6.497304 | 16 / 64 |
| 2 | 1 | 0 | 0.000000 | no accepted prefix |
| 2 | 10 | 4 | 7.813638 | 24 / 64 |
| 2 | 100 | 5 | 7.736459 | 24 / 64 |

Fuel in incomplete campaigns counts only accepted deliveries; an unsuccessful search is retained but not executed. Each failed nominal leaves the remaining payloads unserved. A bounded search miss does not prove infeasibility.

The 64 corners are deterministic signed error combinations, not a probability or a flight navigation covariance. Replay retains fixed commands and correlated calibration errors across all releases; it is not feedback navigation. Partial-history corners assess only delivered payloads; every complete mission still fails because payloads remain unserved. Numerical verification and mission acceptance are distinct.

Limits: planar two-body gravity; assumed thrust and slew law; endpoint perigee guard only; no continuous collision/plume clearance, torque/momentum, flexible-body response, disposal, hardware accuracy or installed mass advantage is established.

[Frozen criteria](../validation/P113_S12_manifest_finite_burn.md) · [All attempts and histories](../analysis/results/manifest_finite_burn.json)
