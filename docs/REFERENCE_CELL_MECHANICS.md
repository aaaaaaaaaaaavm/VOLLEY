# Reference-cell spring, pusher and catcher screen

I evaluate a linear unloading spring at the S4 study point. No spring, latch, motor or damper is selected. P92 remains open.

**48 of 144 declared mechanical cases meet the analytical 10 g/contact screen.** Numerical verification: **PASS**.

The relative-speed study point is 4.569852 m/s for 4 kg. With zero friction and zero end preload, the spring requires at least **213.0 mm**, twice the **106.5 mm** constant-force ideal. Calling 106.5 mm a spring design would miss that distinction.

| Quantity across feasible grid | Minimum | Maximum |
|---|---:|---:|
| Working stroke (m) | 0.16 | 0.24 |
| Initial spring compression (m) | 0.24 | 0.96 |
| Peak latch force (N) | 203.863 | 398.233 |
| Spring stiffness (N/m) | 212.358 | 1631.53 |
| Initial stored energy (J) | 42.8113 | 110.144 |
| Pusher catcher energy (J) | 1.04418 | 5.22089 |

These extrema belong to different cases. They must not be assembled into an imaginary best-of-everything design.

## What changed in the design question

A higher end preload flattens force and can shorten working stroke, but increases retained compression and initial stored energy. The latch carries spring force even before a shot. The local catcher must absorb the pusher's kinetic energy after payload departure; its average force is not a peak shock prediction. Negative endpoint net force invalidates the assumed continuous pusher contact and is retained as a rejected case.

The JSON includes all rejected cases, 5/10/20 mm catcher stopping distances and assumed 50/70/90% charging efficiency, with 12-shot totals and no recovery credit. This is fixed-frame internal sizing: host recoil energy and the conversion from internal pusher speed to payload/host relative speed remain to be coupled to the mission model. Frame, spring, motor, gearbox, latch, catcher, retention, controls, harness and thermal mass remain unallocated. Energy is not a mass estimate.

## Coupon needed next

Measure force versus travel through the declared stroke, preload after dwell and repeated charging, breakaway/sliding force versus temperature, latch shock, pusher/payload separation, exit speed, angular rate and catcher peak/rebound. Use independent position/time measurements and calibrate their uncertainty before comparing repeatability with a mission allocation. S5's local allowances are not approved hardware tolerances.

Reject a candidate if the measured envelope violates its 10 g study ceiling, loses required contact, jams, relatches into the payload, ejects retained hardware or lets catcher rebound recontact it. Flight ascent retention, wear life, contamination and environmental acceptance require separately frozen specifications.

[Declared criteria](../validation/P92_S2_reference_cell_mechanics.md) · [Complete result](../analysis/results/reference_cell_mechanics.json) · [Reference architecture](GEN6_REFERENCE_ARCHITECTURE.md)

Reproduce: `python analysis/reference_cell_mechanics.py --check`.
