# Computational closure: live register view

> **Architecture disposition, 2026-09-28:** The separate motor-charged spring-cell bank is withdrawn as VOLLEY's next architecture. It is retained here only as a dated study. Any selection or current-reference wording below describes the former decision and is superseded. A reusable shared launch path with sequential loading is the open design objective; no speed envelope is validated. See [current status](NEXT_GENERATION_STATUS.md).


Updated 2026-09-16. This document answers one narrow question: **what live VOLLEY register items still have an honest next step that is more computation?** It is checked by [`tools/check_computational_closure.py`](../tools/check_computational_closure.py).

> ## Computational closure is not hardware validation, qualification, architecture selection or flight readiness.
>
> It means only that a named scope has no remaining question whose uncertainty should honestly be reduced by analysis before hardware. Nothing in VOLLEY has been built, fired or measured.

The `historical study` scope in the register was created while the approximately 8 m gas guide was active. The later [compact spring-cell study](LEGACY_STUDY_REFERENCE_ARCHITECTURE.md) has also been withdrawn as a selected reference. Both retain open, configuration-specific evidence. The count below is not a completion metric for any new architecture.

## Remaining COMPUTATION items: 18

It is not zero and this file will not pretend otherwise. The current live-register classification is:

| Scope | COMPUTATION | HARDWARE | HOST_DATA | FLIGHT_OPS | DECISION |
|---|---:|---:|---:|---:|---:|
| historical study | 18 | 4 | 5 | 1 | 1 |
| GEN5 | 11 | 0 | 0 | 0 | 3 |
| PROGRAMME | 1 | 0 | 0 | 1 | 6 |

Use the generated [BSX review](BSX_REVIEW.md) for the complete live-item table. The entries below are the eighteen `historical study` computation items and the configuration in which their present next step makes sense.

| Entry | Current computational question | Configuration/use |
|---|---|---|
| [P57](../OPEN_PROBLEMS.md) | Read the voice-coil deployer in full and complete the five-field prior-art record | Prior art; reusable |
| [P75](../OPEN_PROBLEMS.md) | Build the historical study reliability architecture | Historical gas configuration unless a current-reference fault tree explicitly supersedes it |
| [P79](../OPEN_PROBLEMS.md) | A76 falsified inclination-dependent density as the 1.2428x residual cause; check reference-orbit provenance next | Mission/environment; reusable |
| [P81](../OPEN_PROBLEMS.md) | Size a backup ejector that clears the historical tube on available energy | Historical gas configuration |
| [P87](../OPEN_PROBLEMS.md) | Re-plan the historical gas campaign fill schedule against its window | Historical gas configuration |
| [P91](../OPEN_PROBLEMS.md) | Pressure-vessel design meeting A53's per-cell mass condition | Historical gas configuration |
| [P103](../OPEN_PROBLEMS.md) | Roundness, stick-slip, inertia variation, tube compliance and a contact law that passes restitution | Historical gas guide; contact-method lessons may be reusable |
| [P108](../OPEN_PROBLEMS.md) | Re-establish credible contact convergence on the corrected continuous geometry or change formulation | Historical gas guide; do not quote the old tip-off magnitude as settled physics |
| [E32](../OPEN_PROBLEMS.md) | Design ascent inhibit and fault logic | Reusable only after mapping to the selected retention/energy architecture |
| [E28](../OPEN_PROBLEMS.md) | Campaign mission life at a real deployment altitude | Mission/environment; reusable |
| [P117](../OPEN_PROBLEMS.md) | Historical trim re-run once the relevant architecture decision says the subsystem is still needed | Historical gas trim; do not restart automatically |
| [P118](../OPEN_PROBLEMS.md) | Historical trim/tube fix trade quantified by A72 | Historical gas trim; do not restart automatically |
| [E3](../OPEN_PROBLEMS.md) | Replace parametric component masses with public supplier data | Reusable, but component list must match the configuration being costed |
| [E6](../OPEN_PROBLEMS.md) | Atmosphere/lifetime uncertainty beyond a scalar density multiplier | Mission/environment; reusable |
| [E7](../OPEN_PROBLEMS.md) | Select a real velocity sensor from public data and propagate its stated noise | Reusable after measurement location/range are defined |
| [E11](../OPEN_PROBLEMS.md) | Public materials/outgassing screening for the actual BOM | Configuration-specific; wait for named materials where necessary |
| [E16](../OPEN_PROBLEMS.md) | Complete publisher-record/reference audit | Evidence quality; reusable |
| [E18](../OPEN_PROBLEMS.md) | Replace invented conjunction covariance with a defensible public source | Mission/environment; reusable |

## P92 and the change in programme context

The register still classifies [P92](../OPEN_PROBLEMS.md) as `DECISION` because A66 and A72-A74 reduced the **historical gas trim/tube problem** to a programme choice. That history remains true for that machine.

On 2026-09-16 the P92 screen selected independent spring cells as a calculation reference. That selection was withdrawn on 2026-09-28 because it did not meet the shared loading objective or establish a complete-manifest benefit. P92 remains open. Installed burden, release/navigation uncertainty, clearing/settling, mechanism behaviour, repeatability, cycle life and provider accommodation still control the next decision.

Until the register entry itself is reconciled without rewriting its historical close condition, read its `DECISION` classification as the legacy gas-architecture disposition and use [LEGACY_STUDY_REFERENCE_ARCHITECTURE.md](LEGACY_STUDY_REFERENCE_ARCHITECTURE.md) plus [PROGRAMME_EXECUTION.md](PROGRAMME_EXECUTION.md) for the current P92 path.

## What is genuinely external

Four live `historical study` items require hardware or measurement: [P67](../OPEN_PROBLEMS.md), [P78](../OPEN_PROBLEMS.md), [P88](../OPEN_PROBLEMS.md) and [E4](../OPEN_PROBLEMS.md). The first three are historical gas seal/friction evidence unless reused; E4 remains the simple programme truth that nothing has been built.

Five require host or launch-provider data: [E5](../OPEN_PROBLEMS.md), [P94](../OPEN_PROBLEMS.md), [P99](../OPEN_PROBLEMS.md), [P68](../OPEN_PROBLEMS.md) and [E31](../OPEN_PROBLEMS.md). These are conversations/interfaces, not numbers to invent from public launcher descriptions.

[E30](../OPEN_PROBLEMS.md) requires operational deployment history rather than another model.

## The classification

Every LIVE entry in [`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) carries a machine-readable scope and next-step class. The classes are:

| Class | The next honest action |
|---|---|
| COMPUTATION | model, simulate, optimise, FEA, CFD, deterministic/Monte-Carlo analysis, CAD, standards comparison, public-data literature work or component selection from published data |
| HARDWARE | measure, manufacture, qualify, test |
| HOST_DATA | non-public launch-provider or host-stage interface data |
| FLIGHT_OPS | flight or operational data that does not exist until something flies |
| DECISION | a programme decision that no further analysis settles |

The gate fails if a live entry has no classification, if a class/scope is invalid, if computational work is disguised as hardware/host/flight work, if the `historical study` computation count above drifts from the register, or if `--closed` is asserted while any `historical study` computation item remains.

## Limits of the gate

A green closure gate proves classification consistency, not physics. A wrong equation can be computed perfectly and still be wrong. Failed bands, withdrawn results and model-form disagreements remain evidence. The current redesign therefore uses the same rule as the older work: criteria before implementation, independent checks where they can disagree meaningfully, and a failed result is allowed to change or kill the design.
