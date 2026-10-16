# Gen5 uncertainty, acceptance and fault interpretation

A software gate passing means that its stated calculation is consistent. It does not make a failed mechanical or mission criterion pass. Statistical confidence is not assigned to deterministic sensitivity cases or unmeasured reliability.

| Area | Current evidence | Uncertainty boundary | Disposition | Remaining validation |
|:--|:--|:--|:--|:--|
| EM force | P118/P121 ideal work 1041.743 J; P119 2D 1081.6 J | P121/P118 share geometry, remanence and ideal phase; agreement is not model-form uncertainty | HISTORICAL SPEED CHALLENGED | Actual winding, drive, source, friction and force tests |
| Geometry | 17 Gen5 and 5 widened-R1 intersections | Exact saved-solid census only; no tolerance/deflection or continuous motion proof | FAIL / UNRESOLVED | New geometry and re-analysis |
| Mass | 126.561588 kg; 10.546799 kg/3U | Primitive/fill/lump model; ±15% is assumed, not statistical | FAIL HISTORICAL MASS SCREEN | Sourceable installed BOM and measured mass properties |
| Immediate orbit | 28.800775 km for imposed inertial 16.029 m/s | 0.02 m numerical band; no host or atmosphere in P115 | PASS TWO-BODY IDENTITY ONLY | Finite host, real release state and mission control |
| Lifetime | P134 independent integration of shared static density | Numerical refinement below 0.5%; environmental/model-form error unbounded | CONDITIONAL MODEL OUTPUT | Time-varying atmosphere and current independent propagator |
| Mission | Matched twelve-shot reference | Finite optimizer search and 64 prefix corners; no global proof | NO SAMPLED OPTION COMPLETES | Named mission/host, feasible optimization and full resources |
| Release/contact | A34 zero-rate inference withdrawn | No measured compliance, preload or friction law | UNVERIFIED | Contact model and instrumented release |
| Structure/thermal/fields | Historical isolated cases only | No same-revision assembly/load/mesh qualification closure | UNVERIFIED | Updated FE, thermal, exposure and payload interface |
| Gen6 feeder | R2/R0 nominal states and sampled paths | No continuous tolerance/load/fault proof; ordinal scores not probabilities | UNSELECTED | Locks, docking, containment and same-boundary trade |

## Fault tree and safe-state requirements

Top event: unintended release, loose payload or loss of the remaining manifest. Credible branches are: stored-cell restraint failure; wrong-cell or multiple-cell opening; partial transfer with loss of power; unproved shared-path clearance; inconsistent position/lock sensors; premature propulsion command; failed carrier arrest; and loss of host pointing/recovery. These branches share power, control, rail and host resources, so their probabilities cannot be multiplied as independent events.

| Fault path | Required inhibit/containment | Evidence status |
|:--|:--|:--|
| Stuck cell | Keep that payload independently locked; others proceed only after safe-path proof | Requirement; hardware proof absent |
| Power loss during transfer | Positive mechanical capture throughout transfer; supervised recovery | Critical open mechanism requirement |
| Gate/position sensor disagreement | Inhibit shot and cell opening; safe retained state | Logic requirement; implementation unverified |
| Unclear shared path or pusher not withdrawn | Inhibit propulsion and further feed | Nominal CAD states do not prove fault containment |
| Brake/reset or host recovery fault | Retain/contain carrier, halt sequence, supervise recovery | No demonstrated full shot/reset cycle |

No numerical failure rate, P-POD-equivalent reliability, redundancy credit or safety certification follows from this fault tree. The separate [Gen6 cycle and faults](../cad/gen6_feeder/cycle_and_faults.md) defines transition guards; it remains a requirements record.
