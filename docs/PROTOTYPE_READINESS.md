# From the current record to a prototype design review

Adityavardhan Mishra · 2026-09-16

I am continuing VOLLEY and BOLLEY from their existing evidence. I am not restarting either history or treating a newer generation as a more mature machine. This programme defines the work I want a prospective builder to be able to inspect before committing to a prototype. It is a work programme, not a claim that these deliverables are complete.

[Programme execution](PROGRAMME_EXECUTION.md) is the current sequence. [P113-S4](MANIFEST_TIMING.md) supplies the latest bounded mission result. [The clean-sheet P92 screen](GEN6_REFERENCE_ARCHITECTURE.md) carries that result into a compact reference architecture: independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher. That reference is selected for the next calculations; P92/P113 remain open and no hardware has been built or tested.

## The endpoint

I want a reviewer to be able to identify the configuration, reproduce the controlling analyses, inspect the drawings, understand the remaining uncertainty, and choose the first test article without reconstructing the project from its history.

Computational closure alone does not release a design for manufacture. A build package also needs a selected configuration, materials, tolerances, interfaces, assembly instructions, instrumentation and a test-readiness review. Prototype results will change that package. Qualification and flight acceptance follow their own reviews and physical evidence.

| Milestone | Evidence needed to claim it | Present disposition |
|---|---|---|
| Reviewable engineering record | Controlled configuration, traceable claims, reproducible checks and visible exceptions | Substantial evidence exists; current-state reconciliation continues |
| Computational closure of a named scope | Every relevant analytical question has a result, bounded omission or justified rejection; no hidden dependency on unfinished analysis | Not achieved for either active design |
| Prototype design-review package | Drawings, BOM, tolerance/load-path closure, assembly and instrumented test procedures for one named article | Not achieved |
| Prototype test readiness | Article and facility inspections, calibrated instruments, approved procedure and safe operating limits | Requires hardware and facility work |
| Flight readiness | Mission-specific interfaces, qualified configuration, acceptance evidence and launch-provider disposition | Not established |

There is no useful universal percentage of completion. A single unresolved release mechanism can block the machine while hundreds of other checks pass. I track the dependencies of the controlling claims, not the percentage of documents marked complete.

## What I retain

| Record | Role going forward |
|---|---|
| VOLLEY Gen5 | Frozen electromagnetic comparison case and manuscript baseline, with failed criteria retained |
| Historical gas-driven Gen6 | Evidence-rich comparator/backup; retain its pressure, guide, contact, trim and campaign evidence under that configuration |
| Clean-sheet Gen6 reference | Current calculation reference: independent stored-energy release cells; mechanism details deliberately unselected until falsification evidence exists |
| BOLLEY Fluxrelay | Cooperative-interface comparator; carry the selected 12-turn A9f/A5h candidate through its missing downstream checks |
| BOLLEY Fluxframe and Fluxpiston | Separate exploratory directions, with their own entry criteria and no inherited closure |
| VOLLEY-paper and VOLLEY-thesis | Authored Gen5 manuscripts plus exported evidence; a newer export does not change manuscript scope |
| VOLLEY-lab | Stopped alternatives and explicit conditions for reopening them |

The mission and requirements control the hardware. S4 did not reward authority above 4.569852 m/s in its best tested BOLLEY/Gen5/historical gas-Gen6 campaigns. That result is not a product requirement or global optimum, but it is enough to stop treating higher velocity as inherently better. Every extra joule, metre and subsystem now has to earn its place against a mission.

## Execution order and exit criteria

Each new physical analysis needs its own committed run sheet, justified numerical bands, controlled inputs and explicit consequence of failure before implementation. The acceptance products below define the work packages; they do not replace those run sheets.

| Priority / package | Work | Reviewable exit product | Depends on |
|---|---|---|---|
| 0. Evidence repair | Reproduce current gates, reconcile stale public statements and companion payloads, distinguish a successful analysis from an acceptable design | Source-pinned audit; failures, omissions and environment limitations recorded separately | Current repositories |
| 1. Mission requirement | Extend P113 beyond ideal S4: clearing/settling, release/navigation uncertainty, host attitude recovery, complete-manifest effects and replenishment mission definition | Mission cases, payload/host constraints, uncertainty budgets, explicit no-benefit regions and architecture-driving requirements | S1–S4; host classes; public inputs labelled |
| 2. Configuration selection | Falsify the current independent stored-energy reference against banks/shared path and direct-electromechanical/compact-gas backups; keep Gen5 and historical gas Gen6 as comparators | Dated P92 decision, rejected alternatives, dependency map and explicit reason the survivor is worth building | 1; current P92 reference screen; installed-burden evidence |
| 3. Release physics | For the current reference: accumulator force-displacement, preload setting, latch release, pusher friction/guidance, catcher dynamics, payload CG/inertia and 6-DOF tip-off. Historical P103/P108 work stays scoped to the gas guide | Credible release-state envelope, model-form disagreement and domains where prediction is not credible | 2 for detailed reference work; contact-law verification for historical guide |
| 4. BOLLEY electrical closure | Revisit A9f at the A5h winding: fresh field/current-distribution check, hot semiconductor losses, switching, parasitics, supply sag, protection and faults | Coupled time histories and a component-by-component loss/voltage/temperature budget | BOLLEY A9f/A5h; supplier data |
| 5. Structural and tolerance closure | Trace ascent, retained, charged, release, catcher and fault loads through payload, cell, mounts and host interface; include thermal distortion and assembly errors | Drawings linked to stress, modes, clearance and preload margins; worst-case stack plus justified statistical study | 2–4; declared load envelopes |
| 6. Thermal and materials | Couple recharge/repeated releases, duty cycle, vacuum heat paths and temperature-dependent properties; screen materials, insulation, adhesives and contamination | Full-campaign temperature histories, selected materials with sources, limits and measurement dependencies | 4–5; operating timeline |
| 7. Full system accounting | Itemise accumulator, actuator, latch, pusher/catcher, containment, cooling, harness, electronics, fasteners, sensors, support structure and payload interfaces; use the same boundary for banks/shared path and backups | Mass/CG/inertia, power/energy, volume and cost ledgers with uncertainty; installed burden per successfully delivered payload | 2, 4–6 |
| 8. Controls and fault response | Implement command/inhibit/charge/release/catch state machine; inject reset, brownout, stale sensor, timing skew, failed channel, jam and partial-release conditions | Executable fault cases and traces linked to hazards and recovery/abort limits | 3–7; E32 and retention architecture |
| 9. Host campaign | Propagate recoil, changing mass properties, attitude restoration, clearing/settling, thermal recovery, energy use and the last deployment | End-to-end manifest timeline and bounded host requirements; no assumed provider endorsement | 1, 3, 6–8 |
| 10. Manufacturing release candidate | Finish terminals, leads, joints, finishes, fits, datums, inspections, assembly order and tool access for the selected prototype | Revisioned STEP, drawings, BOM, purchased-part records, assembly and inspection travellers | 4–8 |
| 11. Experiment design | Choose the smallest tests that discriminate the dominant uncertain models; specify instrumentation, calibration, uncertainty and model-correlation rules | Coupon and integrated-test packages with predeclared acceptance and redesign branches | 3–10 |
| 12. Independent review | Walk a reviewer through requirements, evidence, failure cases and the build/test package; rerun the release evidence from a clean environment | Review record, discrepancies and a release disposition for the named prototype | 0–11 |

Packages can overlap where their inputs are fixed. A geometry-changing result must invalidate dependent analyses explicitly. I do not keep their old green status while changing the drawing.

## VOLLEY: the work that controls the next design

**The product requirement comes first.** P113 is programme-scoped and still controls what Gen6 should be. S4 establishes a bounded two-payload terminal-state comparison, not a complete mission requirement. The next mission evidence must add clearing/settling, release/navigation uncertainty, attitude recovery and replenishment/full-manifest cases before a hardware burden is justified.

**The current reference is meant to be killed if it is weak.** The functional chain is independent launch retention → slow preload actuator → mechanical accumulator → preload measurement → independent latch → short guided pusher → payload clears → local catcher/retainer → post-release state sensing. Spring form, latch, bearings, catcher, motor/gearbox and cell structure are deliberately unselected. Before detailed CAD I need force-displacement bounds, preload-to-exit sensitivity, latch shock, pusher friction, clearance/tolerance sensitivity, payload CG/inertia variation, tip-off, catcher impulse and cycle-life evidence.

**Installed burden decides whether fault isolation is worth it.** Independent cells isolate a blocked mechanical path, but duplicate structure and actuators. Small banks and a shared magazine may be lighter. Compare them using one accounting boundary: structure, retention, actuator/energy storage, control, sensors, harness, thermal hardware, host reinforcement, volume, operations and failure consequences. Shared command and power remain common-mode risks even with independent mechanical paths.

**The historical gas machine stays useful without staying current.** P103/P108, pressure-vessel, fill-schedule, backup-ejector and trim evidence remain valuable where they answer a live comparison or reusable engineering question. Their geometry and failure magnitudes do not automatically transfer to the clean-sheet cell. The approximately 8 m guide is no longer the assumed Gen6 packaging basis.

**Gen5 remains useful.** Its remaining structural dynamics, field exposure, winding inductance, segment handover and release-environment questions belong to its own baseline. I will not quietly mark them complete because the reference removes those components. Improvements are worthwhile when they resolve a live claim or enable a specific experiment.

## BOLLEY: finish Fluxrelay before adding another generation

A9f selects twelve turns and A5h establishes nominal winding-envelope CAD. The older A9 transient used a different 4-turn/380 A point, so it does not close the selected 12-turn/126.667 A configuration. The next electrical package must use actual conductor routing and terminations, carry resistance/inductance/coupling through the driver, and audit supplier current definitions before crediting ratings.

The design also needs the 0.20 mm lane gap evaluated as a manufacturing/thermal/dynamic stack; four-face force imbalance propagated into motion; cage attachment and ascent load paths; powered and unpowered magnetic-environment bounds; and a complete installed mass budget. Module-only or active-primary mass is not the packaged system. The spacecraft's added interface mass and lost panel area stay in the system comparison.

Fluxframe receives mass credit only when named parts are actually displaced and their functions are demonstrated in the replacement design. Fluxpiston remains a different pressure/contact problem and cannot inherit Fluxrelay's results.

## What every controlling simulation must show

| Evidence | What I require |
|---|---|
| Intended use | The decision the simulation supports and its valid operating domain |
| Inputs | Configuration revision, units, source, uncertainty and correlations |
| Verification | Analytical limiting cases, conservation where applicable, numerical convergence and injected failure cases |
| Independent check | Different implementation or governing approximation; disagreement investigated, not averaged away |
| Uncertainty | Separate numerical error, parameter uncertainty and model-form uncertainty; probabilities only where distributions are defensible |
| Result | Time histories and worst cases, acceptance comparison, failed cases and sensitivity |
| Reproduction | Exact inputs, source revision, solver/dependency versions, commands, logs and hashes |
| Validation status | Measurement data and calibration/holdout split if available; otherwise explicitly absent |

I use [NASA-STD-7009B](https://standards.nasa.gov/standard/nasa/nasa-std-7009) as a source for model-credibility practice, not a certification label. Environmental requirements must be tailored to the selected mission. [GSFC-STD-7000B](https://standards.nasa.gov/standard/gsfc/gsfc-std-7000) is a reference for that planning, not a universal CubeSat acceleration limit or a substitute for a launch-provider interface specification.

## Reuse that would earn its place

I will reuse existing project code first. A new dependency needs a specific unanswered question, a pinned version, retained licence/attribution, an independently checked example, and a bounded integration test before it supports a claim.

| Candidate | Useful role | Admission condition |
|---|---|---|
| [Project Chrono](https://projectchrono.org/) | Independent multibody/contact implementation for guide or pusher travel and separation | First reproduce contact/restitution and rigid-body limiting cases; document formulation and disagreement with the existing solver |
| [Basilisk](https://hanspeterschaub.info/basilisk/) | Coupled host attitude/orbit campaign and repeatable dispersion studies | Check impulse and momentum balances before connecting the deployment model; distinguish public host assumptions from supplied data |
| Existing CalculiX / field / circuit paths | Structural, electromagnetic and electrical reclosure already represented in this programme | Use the selected geometry and operating point; demonstrate convergence and avoid counting a wrapper as independence |

A recognised solver adds no credibility merely by appearing in a badge or screenshot. Nor does using an open package transfer validation of its example problem to this machine.

## The build handoff

For each proposed coupon and integrated prototype I require:

1. A configuration index connecting CAD, drawings, BOM, circuit and software revisions.
2. Purchased-part identifiers and traceable properties, with substitutions controlled.
3. Manufacturing drawings with datums, fits, finishes, tolerance and inspection requirements.
4. An assembly sequence, tooling, alignment/preload methods and acceptance inspections.
5. An instrumented test procedure with calibrated ranges, bandwidth, sampling and uncertainty.
6. Predicted observables, frozen acceptance criteria and explicit stop/rework conditions.
7. A correlation plan that says which data may calibrate the model and which tests remain independent.
8. A route from coupon evidence to integrated mechanism tests and later environmental qualification.

The first useful physical work may precede full-system computational closure. If latch repeatability, pusher friction or catcher impulse dominates the uncertainty, a well-designed coupon can prevent months spent refining the wrong model. Software effort stops when another calculation will not change the next build decision within the declared uncertainty.

## Presentation standard

The front page should explain the machine, show the correct configuration, name the controlling result and admit the blocking uncertainty. It should then offer separate routes to the evidence, CAD, manuscript and test package. The complete history stays available through the engineering documents and git history.

The most useful visuals are a labelled assembly/cutaway, a shot sequence from the actual model, a mission trade envelope, a clearance/thermal margin plot and a release-state distribution with its limits visible. Solver screenshots need units, boundary conditions, mesh information, source revision and evidence status. Deformation scale must be visible. Rendered geometry is labelled as geometry, and an animation is labelled as simulated motion.

I want capability to be apparent from decisions a reviewer can audit: finding a wrong load case, rejecting a topology, correcting a current convention, closing a tolerance stack, and designing a test that can prove a model wrong. More pages, generation labels or green checks do not replace that evidence.

## Entry points for the existing work

- [Current VOLLEY handoff](STATE_OF_THE_PROJECT.md), [live work list](BSX_REVIEW.md), [computational closure](COMPUTATIONAL_CLOSURE.md) and [current Gen6 reference](GEN6_REFERENCE_ARCHITECTURE.md).
- [Gen5 baseline](BASELINE.md), [declared exceptions](GEN5_CLOSURE.md), and [provenance](PROVENANCE.md).
- [Manufacturing study](MANUFACTURING.md) and [qualification plan](QUALIFICATION_PLAN.md). Historical gas-Gen6 CAD/build documents remain configuration-specific inputs, not the manufacturing package for the current reference.
- [BOLLEY completion standard](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/COMPLETION_STANDARD.md) and [latest Fluxrelay evidence](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md).

## Audit basis and limits

This programme is maintained against current `main`, not a frozen September 14 repository snapshot. The current authority is the evidence linked above plus the live problem registers. This document is not a fresh independent solve of every stored analysis, a line-by-line manuscript review, or a manufacturing release. The work packages remain planned until their own criteria and evidence are committed.