# From the current record to a prototype design review

Adityavardhan Mishra · 2026-09-14

I am continuing VOLLEY and BOLLEY from their existing evidence. I am not restarting either
history or treating a newer generation as a more mature machine. This programme defines the
work I want a prospective builder to be able to inspect before committing to a prototype.
It is a work programme, not a claim that these deliverables are complete.

## The endpoint

I want a reviewer to be able to identify the configuration, reproduce the controlling analyses,
inspect the drawings, understand the remaining uncertainty, and choose the first test article
without reconstructing the project from its history.

Computational closure alone does not release a design for manufacture. A build package also
needs a selected configuration, materials, tolerances, interfaces, assembly instructions,
instrumentation and a test-readiness review. Prototype results will change that package.
Qualification and flight acceptance follow their own reviews and physical evidence.

| Milestone | Evidence needed to claim it | Present disposition |
|---|---|---|
| Reviewable engineering record | Controlled configuration, traceable claims, reproducible checks and visible exceptions | Substantial evidence exists; public status and handoff need consolidation |
| Computational closure of a named scope | Every relevant analytical question has a result, bounded omission or justified rejection; no hidden dependency on unfinished analysis | Not achieved for either active design |
| Prototype design-review package | Drawings, BOM, tolerance/load-path closure, assembly and instrumented test procedures for one named article | Not achieved for the complete systems |
| Prototype test readiness | Article and facility inspections, calibrated instruments, approved procedure and safe operating limits | Requires hardware and facility work |
| Flight readiness | Mission-specific interfaces, qualified configuration, acceptance evidence and launch-provider disposition | Not established |

There is no useful universal percentage of completion. A single unresolved release mechanism
can block the machine while hundreds of other checks pass. I track the dependencies of the
controlling claims, not the percentage of documents marked complete.

## What I retain

| Record | Role going forward |
|---|---|
| VOLLEY Gen5 | Frozen electromagnetic comparison case and manuscript baseline, with its failed criteria retained |
| VOLLEY Gen6 | Active gas-driven architecture under investigation; the trim stage remains suspended |
| BOLLEY Fluxrelay | Active cooperative-interface machine; carry the selected 12-turn candidate through its missing downstream checks |
| BOLLEY Fluxframe and Fluxpiston | Separate exploratory directions, with their own entry criteria and no inherited closure |
| VOLLEY-paper and VOLLEY-thesis | Authored Gen5 manuscripts plus exported evidence; a newer export does not change manuscript scope |
| VOLLEY-lab | Stopped alternatives and explicit conditions for reopening them |

I reconsider the mission and requirements from first principles before redesigning the hardware.
That means asking what release velocity is useful on a specified host, rather than maximising
velocity first and finding a mission for it afterwards.

## Execution order and exit criteria

Each new physical analysis still needs its own committed run sheet, justified numerical bands,
controlled inputs and explicit consequence of failure before implementation. The acceptance
products below define the work packages; they do not replace those run sheets.

| Priority / package | Work | Reviewable exit product | Depends on |
|---|---|---|---|
| 0. Evidence repair | Reproduce current gates, reconcile stale public statements and companion payloads, distinguish a successful analysis from an acceptable design | Source-pinned audit; failures, omissions and environment limitations recorded separately | Current repositories |
| 1. Mission requirement | Resolve P113: useful release-velocity envelope versus host-provided orbital energy; compare spring release, release timing and host manoeuvre under the same mission assumptions | Mission cases, payload/host constraints, benefit and sensitivity plots, explicit no-benefit region | Host classes; public inputs labelled |
| 2. Configuration selection | Preserve Gen5; compare gas-only Gen6 and any justified trim alternative against velocity accuracy, tip-off, mass and host integration; resolve P92 by a dated decision | One active configuration per machine, rejected alternatives and a dependency map | 1; A72–A74; existing kill criteria |
| 3. Release physics | Resolve P103/P108 against the corrected continuous guide; include six-degree-of-freedom motion, inertia/CG error, bore shape, compliance, friction and contact | Converged release-state envelope, model-form disagreement and domains where prediction is not credible | 2; contact-law verification |
| 4. BOLLEY electrical closure | Revisit A9f at the A5h winding: fresh field/current-distribution check, hot semiconductor losses, switching, parasitics, supply sag, protection and faults | Coupled time histories and a component-by-component loss/voltage/temperature budget | BOLLEY A9f/A5h; supplier data |
| 5. Structural and tolerance closure | Trace ascent, retained, firing and fault loads through payload, inserts, guides, mounts and host interface; include thermal distortion and assembly errors | Drawings linked to stress, modes, clearance and preload margins; worst-case stack plus justified statistical study | 2–4; declared load envelopes |
| 6. Thermal and materials | Couple repeated shots, duty cycle, vacuum heat paths and temperature-dependent properties; screen materials, insulation, adhesives and contamination | Full-campaign temperature histories, selected materials with sources, limits and measurement dependencies | 4–5; operating timeline |
| 7. Full system accounting | Itemise tanks/chambers, valves, containment, cooling, harness, electronics, fasteners, sensors and payload interfaces; eliminate unowned allowances | Mass/CG/inertia, power/energy and cost ledgers with uncertainty; consistent comparator boundary | 2, 4–6 |
| 8. Controls and fault response | Implement the command/inhibit/release state machine; inject reset, brownout, stale sensor, timing skew, failed channel, jam and partial-release conditions | Executable fault cases and traces linked to hazards and recovery/abort limits | 3–7; E32 and retention architecture |
| 9. Host campaign | Propagate recoil, changing mass properties, attitude restoration, settling, thermal recovery, gas/power use and the last deployment | End-to-end manifest timeline and bounded host requirements; no assumed provider endorsement | 1, 3, 6–8 |
| 10. Manufacturing release candidate | Finish terminals, leads, joints, finishes, fits, datums, inspections, assembly order and tool access for the selected prototype | Revisioned STEP, drawings, BOM, purchased-part records, assembly and inspection travellers | 4–8 |
| 11. Experiment design | Choose the smallest tests that discriminate the dominant uncertain models; specify instrumentation, calibration, uncertainty and model-correlation rules | Coupon and integrated-test packages with predeclared acceptance and redesign branches | 3–10 |
| 12. Independent review | Walk a reviewer through requirements, evidence, failure cases and the build/test package; rerun the release evidence from a clean environment | Review record, discrepancies and a release disposition for the named prototype | 0–11 |

Packages can overlap where their inputs are fixed. A geometry-changing result must invalidate
dependent analyses explicitly. I do not keep their old green status while changing the drawing.

## VOLLEY: the work that controls the next design

**The product requirement comes first.** P113 is programme-scoped and therefore is not included
in the Gen6-only closure count. It still controls what Gen6 should be. A host that supplies most
of the orbital change may need much less deployment velocity. That trade must include the
mass, integration, payload environment and operations bought by the higher-velocity machine.
The spring and release-timing controls stay in the comparison.

**The exit-state model must earn trust.** A71 did not settle P108. A model with excessive contact
penetration can converge numerically to the wrong mechanical approximation. Before using it
for design selection, I need restitution and conservation checks, timestep/tolerance studies,
contact-stiffness or constraint-formulation studies, and an independent implementation whose
equations and failure modes differ. A contact coefficient remains an uncertain input until
measured. Varying an assumed coefficient is not calibrating it.

**The trim question is an architecture decision.** A72–A74 prevent treating the present magnetic
secondary and conducting wall as a solved combination. I will not add a trim-stage render to
imply that this is settled. Gas-only operation must meet the actual velocity-accuracy requirement
over the declared uncertainty envelope before the stator can be deleted on performance grounds.

**A prototype must have a load path.** Piston, cradle, seal, retention and release geometry need
to be physically compatible with the unmodified-payload objective. The approximately 8 m guide
requires a host envelope and support concept; available stage length is not automatically an
available straight, thermally stable mounting interface.

**Gen5 remains useful.** Its remaining structural dynamics, field exposure, winding inductance,
segment handover and release-environment questions belong to its own baseline. I will not
quietly mark them complete because Gen6 removes those components. Improvements are worthwhile
when they resolve a live claim or enable a specific experiment.

## BOLLEY: finish Fluxrelay before adding another generation

The A9b sectional-drive reclosure passes its recorded checks. A9c exposes a narrow hot-winding
margin. A9e rejects the selected switching arrangement even though the screening calculation
itself passes. A9f selects twelve turns, and A5h establishes nominal winding-envelope CAD.
That is a useful chain of decisions. It does not establish an operational drive.

The next package must use actual conductor routing and terminations, then carry the resulting
resistance, inductance and coupling through the driver. The supplier-current definition needs
an explicit audit: RMS, instantaneous peak, internal-path current, package current, pulse length
and junction temperature must not be substituted for one another.

The design also needs the 0.20 mm lane gap evaluated as a manufacturing/thermal/dynamic stack;
four-face force imbalance propagated into motion; cage attachment and ascent load paths;
powered and unpowered magnetic-environment bounds; and a complete installed mass budget.
The 15.908 kg primary is not that budget. Local bridge module mass is not packaged electronics.

I keep the spacecraft's added interface mass and lost panel area in the system comparison.
Fluxframe receives mass credit only when named parts are actually displaced and their functions
are demonstrated in the replacement design. Fluxpiston remains a different pressure/contact
problem and cannot inherit Fluxrelay's results.

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

I use [NASA-STD-7009B](https://standards.nasa.gov/standard/nasa/nasa-std-7009) as a source for
model-credibility practice, not a certification label. Environmental requirements must be tailored
to the selected mission. [GSFC-STD-7000B](https://standards.nasa.gov/standard/gsfc/gsfc-std-7000)
is a reference for that planning, not a universal CubeSat acceleration limit or a substitute for
a launch-provider interface specification. Both official catalogue pages were reviewed on
2026-09-14; a detailed applicability matrix remains a separate deliverable.

## Reuse that would earn its place

I will reuse existing project code first. A new dependency needs a specific unanswered question,
a pinned version, retained licence/attribution, an independently checked example, and a bounded
integration test before it supports a claim.

| Candidate | Useful role | Admission condition |
|---|---|---|
| [Project Chrono](https://projectchrono.org/) | Independent multibody/contact implementation for guide travel and separation | First reproduce contact/restitution and rigid-body limiting cases; document formulation and disagreement with the existing solver |
| [Basilisk](https://hanspeterschaub.info/basilisk/) | Coupled host attitude/orbit campaign and repeatable dispersion studies | Check impulse and momentum balances before connecting the deployment model; distinguish public host assumptions from supplied data |
| Existing CalculiX / field / circuit paths | Structural, electromagnetic and electrical reclosure already represented in this programme | Use the selected geometry and operating point; demonstrate convergence and avoid counting a wrapper as independence |

A recognised solver adds no credibility merely by appearing in a badge or screenshot. Nor does
using an open package transfer validation of its example problem to this machine.

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

The first useful physical work may precede full-system computational closure. If seal friction
or magnetic force dominates the uncertainty, a well-designed coupon can prevent months spent
refining the wrong model. Software effort stops when another calculation will not change the
next build decision within the declared uncertainty.

## Presentation standard

The front page should explain the machine, show the correct configuration, name the controlling
result and admit the blocking uncertainty. It should then offer separate routes to the evidence,
CAD, manuscript and test package. The complete history stays available through the engineering
documents and git history.

The most useful visuals are a labelled assembly/cutaway, a shot sequence from the actual model,
a mission trade envelope, a clearance/thermal margin plot and a release-state distribution with
its limits visible. Solver screenshots need units, boundary conditions, mesh information, source
revision and evidence status. Deformation scale must be visible. Rendered geometry is labelled
as geometry, and an animation is labelled as simulated motion.

I want capability to be apparent from decisions a reviewer can audit: finding a wrong load case,
rejecting a topology, correcting a current convention, closing a tolerance stack, and designing
a test that can prove a model wrong. More pages, generation labels or green checks do not replace
that evidence.

## Entry points for the existing work

- [Current VOLLEY handoff](STATE_OF_THE_PROJECT.md), [live work list](BSX_REVIEW.md), and [computational closure](COMPUTATIONAL_CLOSURE.md).
- [Gen5 baseline](BASELINE.md), [declared exceptions](GEN5_CLOSURE.md), and [provenance](PROVENANCE.md).
- [Manufacturing study](MANUFACTURING.md), [qualification plan](QUALIFICATION_PLAN.md), and [Gen6 CAD handoff](GEN6_FUSION_BUILD_PACKAGE.md). These are inputs to the package, not evidence that it is complete.
- [BOLLEY completion standard](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/COMPLETION_STANDARD.md) and [latest Fluxrelay evidence](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md).

## Audit basis and limits

This programme was prepared against VOLLEY `67939b7`, BOLLEY `2028393`, VOLLEY-paper `a18f789`,
VOLLEY-thesis `d3174fb` and VOLLEY-lab `5d02e0b`. I inspected the current entry points, working
rules, closure records, relevant latest results and reproduction tooling. This is not a fresh
independent solve of every stored analysis, a line-by-line manuscript review, or a manufacturing
release. The work packages above remain planned until their own evidence is committed.
