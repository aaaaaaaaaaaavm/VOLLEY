# Installed burden and failure consequences

I recover the useful accounting and topology from the superseded [architecture-trade work](https://github.com/aaaaaaaaaaaavm/VOLLEY/tree/548ad101b2d3f9605079274837081be4a407c11c), associated with closed PR36. Its source predates the accepted independent-cell reference. I do not restore its obsolete statement that no reference mechanism has been carried forward. [The current reference](GEN6_REFERENCE_ARCHITECTURE.md) remains a calculation candidate, not selected flight hardware.

## Twelve-payload topology, with no invented reliability

| Arrangement | Payloads potentially deliverable after one blocked path | Stranded by that path | Shared command/power failure |
|---|---:|---:|---|
| Independent cells | 11 | 1 | Can stop all 12 unless common services are separated |
| Banks of 2 | 10 | 2 | Same common-service obligation |
| Banks of 3 | 9 | 3 | Same common-service obligation |
| Banks of 4 | 8 | 4 | Same common-service obligation |
| Banks of 6 | 6 | 6 | Same common-service obligation |
| One shared magazine/path | 0 | 12 | Can stop the whole manifest |

These are consequence counts, not probabilities, reliability estimates or guaranteed delivered payloads. A jam must be physically isolated from neighbouring cells for the first row to apply. Contamination, structural damage, harness damage and software common causes can violate that assumption.

## What the installed ledger must contain

| Burden | Conventional spring/timing baseline | Independent programmable cells | Shared-path machine | BOLLEY Fluxrelay |
|---|---|---|---|---|
| Payload-side hardware | Selected compatible dispenser interface | Unmodified-payload objective still unverified | Configuration-specific interface | 0.37136 kg modelled increment per spacecraft |
| Release mechanism | Spring and retention package unselected | Spring/store, charge drive, latch, pusher and catcher unselected | Guide, handling, actuator and arrest package | 15.908 kg primary material; partial subtotal |
| Power electronics | Release electronics unallocated | Motor drive, inhibit and monitoring unallocated | Configuration-specific power chain | 2.5488 kg selected modules only |
| Structure and launch retention | Must be charged | Per-cell plus common support | Shared support plus manifest restraint | Cage attachment, guide/support and retention open |
| Thermal, harness and controls | Must be charged | Shared service allocation open | Shared service allocation open | Cooling, DC link, protection and wiring open |
| Host resources | Navigation, pointing, burns, clearance and disposal | Same mission duty and reserve accounting | Same mission duty and reserve accounting | Same, with cooperative-payload burden |
| Complete installed mass | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

For BOLLEY, 15.908 + 2.5488 = **18.4568 kg** is a rounded partial primary/module subtotal, not an installed system. A twelve-spacecraft manifest would carry twelve passive interfaces; that is an explicitly different accounting scope from a single reference shot. The interface is not free because it is carried by the customer.

For twelve independent cells, write installed mass as `12 × complete cell mass + common services + host support`. For banks, charge every retained payload interface as well as each bank's complete path and services. A shared path may reduce repeated actuator mass while adding feed, return, jam recovery and common-failure burden. Unknown terms stay unknown.

## What the new mechanical screen adds

[P92-S2](REFERENCE_CELL_MECHANICS.md) narrows force, stroke, stored energy and catcher work. It does not supply component mass. The 48 feasible analytical cases cannot support a mass winner until spring geometry/material, latch/load path, charge mechanism, catcher dynamics and mounting are actually selected and checked.

The fair comparison uses a competent selected spring with release timing and the same host manoeuvre authority. It includes spacecraft-side mass and full-manifest host reserves. The S4 2.777987 kg best-tested fuel result is for its two-payload campaign; it must not be presented as a twelve-payload mission result.

## Reference-cell failure review

| Failure | Consequence to analyse | Evidence needed before acceptance |
|---|---|---|
| Premature release or latch failure | Unsafe departure, neighbouring payload exposure | Independent restraint/inhibit architecture, ascent loads and no-fire tests |
| Charge drift or sensor error | Wrong release energy | Calibrated force/travel measurement, dwell/thermal/cycle repeatability |
| Pusher skew, friction or contact loss | Velocity error, tip-off, jam | Six-degree-of-freedom model, tolerance stack and instrumented stroke |
| Catcher rebound or fracture | Recontact, debris, host impulse | Dynamic arrest model and measured peak/rebound envelope |
| Common power/command failure | All cells unavailable | Explicit service segmentation and failure injection |
| Thermal/campaign accumulation | Drift between shots | Full manifest duty, dwell, recovery and host energy balance |

These are unscored failure-review entries. Occurrence probabilities and detectability scores would be invented without a declared implementation and evidence. P92 remains open.
