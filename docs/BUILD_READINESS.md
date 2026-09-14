# Build readiness

Updated 2026-09-14. I have not released either VOLLEY configuration for full-system manufacture.
No hardware has been built, fired, measured, qualified or flown.

This page replaces a stale subsystem snapshot which mixed early Gen5 and Gen6 results with
later corrections. The [previous text](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/67939b7cbef9e2414226f683ebc12f2b6bf01088/docs/BUILD_READINESS.md)
remains available as history. Current result authority belongs to the run sheets and controlled
inputs, not to that snapshot.

## What a builder can use now

| Material | Use | Boundary |
|---|---|---|
| [Gen5 baseline](BASELINE.md) and [closure](GEN5_CLOSURE.md) | Reproduce the electromagnetic comparison case and inspect its failed criteria | Frozen analysis with exceptions, not a flight design |
| [Parametric CAD](../cad/README.md) | Inspect the modelled geometry and rebuild documented scopes | Nominal fit does not establish tolerance, joint, material or assembly readiness |
| [Gen6 Fusion handoff](GEN6_FUSION_BUILD_PACKAGE.md) | Follow the assembly tree, datums and parameter ownership | Open geometry and contact questions remain explicit |
| [Manufacturing study](MANUFACTURING.md) | Starting tolerance, process and make/buy reasoning | Must be reconciled to the selected prototype configuration |
| [Benchtop tests](BENCHTOP_TESTS.md), [B-1](B1_ORDER.md), [B-2](B2_ORDER.md) | Starting experiment designs and instrumentation questions | Procurement, facility checks, calibration and execution are not established |
| [Qualification plan](QUALIFICATION_PLAN.md) | Structure an environmental verification campaign | Mission-specific applicability and physical tests remain necessary |

## Current subsystem disposition

| Scope | Existing evidence | What prevents a complete build release |
|---|---|---|
| Gen5 electromagnetic drive | Frozen operating point, field studies and circuit checks | Purchasable pulse chain, model limitations and measured force/compatibility |
| Gen5 structure and retention | Sled and retention-pin calculations; nominal geometry | Remaining track dynamics, interfaces and measured structural response |
| Gen5 brake and recovery | ADR-030 operating point and explicit remaining questions | Brake field/thermal/packaging and physical arrest evidence must be reviewed for the actual article |
| Gen5 host interaction | A52 addresses the missing angular-impulse calculation | Host-specific mass properties, control authority and interface loads |
| Gen6 gas store and campaign | Precharge, fill, thermal and reservoir-sizing studies | Selected hardware, complete package and campaign uncertainty; computed sizing is not pressure-system qualification |
| Gen6 guide, piston and cradle | Parametric geometry and the A67–A71 contact investigation | P103/P108: credible contact/exit-state prediction, tolerances, compliant/load-bearing details and actual assembly |
| Gen6 trim | A72–A74 expose conducting-wall and secondary problems | P92 architecture decision; the trim stage remains suspended |
| Gen6 release and retention | Requirements and preliminary mechanism/fault work | Complete load path, ascent inhibits, release logic and measured tip-off |
| Both systems' installed budgets | Existing mass, energy and uncertainty studies | Every required purchased and manufactured part tied to the selected configuration; allowances remain labelled |
| Both systems' payload/host interfaces | Public reference cases and parametric requirements | Actual provider/bus data and review; unmodified does not mean universally compatible |

These are engineering-review dispositions. They do not change a run's pass/fail result or close
an entry in [OPEN_PROBLEMS.md](../OPEN_PROBLEMS.md).

## The next useful release

I am targeting a **prototype design-review package for a named configuration**. Its content and
dependency order are in [PROTOTYPE_READINESS.md](PROTOTYPE_READINESS.md). The first article should
be selected to discriminate the controlling uncertain models, rather than to look like the whole
flight machine before those models are trustworthy.

A complete package needs controlled drawings and BOM, material and purchased-part sources,
tolerance/load-path analysis, assembly and inspection instructions, instrumentation and an
uncertainty budget, predicted observables, and a test procedure with acceptance and stop criteria.
It must also identify which test data may calibrate a model and which remain independent checks.

## Work already identified

Use [STATE_OF_THE_PROJECT.md](STATE_OF_THE_PROJECT.md) for the active configuration,
[BSX_REVIEW.md](BSX_REVIEW.md) for the generated live-item list, and
[COMPUTATIONAL_CLOSURE.md](COMPUTATIONAL_CLOSURE.md) for the analytical closure gate.
Programme-scoped P113 still controls the release-velocity requirement even though the Gen6-only
closure count excludes it. A numerical backlog count is not a build-release decision.

Model credibility, manufacturing readiness, test readiness and flight readiness are separate
claims. I require evidence for each rather than letting a completed CAD assembly stand in for all four.
