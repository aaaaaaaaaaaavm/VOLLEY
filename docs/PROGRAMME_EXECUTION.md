# Programme execution and architecture decision record

[Resume work and coordinate changes](CONTINUITY.md) · [Mission and redesign](workstreams/MISSION_AND_REDESIGN.md) · [Engineering closure](workstreams/ENGINEERING_CLOSURE.md)

Adityavardhan Mishra · 2026-09-16

## Working on now / next / blocked

**Last reviewed: 2026-09-16, after the clean-sheet P92 reference screen.** This is the current execution summary, not a declaration that every listed task is underway.

| State | Work | Next reviewable result |
|---|---|---|
| Current focus | Architecture-driving mission requirements | Clearing/settling, release/navigation uncertainty, host attitude recovery and complete-manifest terms carried into the same terminal-state framework |
| Reference selected for falsification | Independent retained cell with motor-charged mechanical accumulator, latch, short guided pusher and local catcher | Force-displacement, preload/release sensitivity, friction, latch shock, tip-off and catcher-load bounds with frozen acceptance criteria |
| Next | Installed burden and failure topology | Like-for-like mass, volume, energy, consumables and failure consequences for independent cells, banks and the shared magazine |
| Decision pending | P92 configuration closure | Keep, modify or reject the reference after mission uncertainty, installed burden and decisive release-cell evidence exist |
| Requires external evidence | Provider accommodation and physical model validation | Actual host interfaces and discriminating measurements; numerical checks cannot substitute for either |
| Later | One engineered release cell, scaling and reviewed build package | A named test article with drawings, BOM, assembly, inspection and instrumented acceptance procedure |

P113-S4 is on main with generated JSON, report, SVG, independent tests and a normal freshness gate. It is **not** full-manifest closure: P113/E5 remain open because clearing/settling intervals, release/navigation error, installed burden and the complete manifest can still change the architecture result. The clean-sheet P92 screen has now used S4 to select a compact reference for the next calculations; it did not close P92 or select flight hardware.

### Completed foundation

- [P113-S1 departure allocation](DEPARTURE_TRADE.md): 210 reference cases with finite host recoil and assumed release-speed intervals.
- [P113-S2 sequential energy campaigns](CAMPAIGN_ALLOCATION.md): 180 cases with host propagation, changing manifest mass, propellant and correction-count limits.
- [P113-S3 terminal-state timing](TERMINAL_TIMING.md): 300 single-payload cases requiring position and velocity at a common epoch, with identical timing grids for comparators.
- [P113-S4 two-payload manifest timing](MANIFEST_TIMING.md): 100 schedule/order/authority cases using one evolving host state. Forty-four tested campaigns are accepted. On the fine grid the BOLLEY, Gen5 and historical gas-Gen6 authority screens all reach the same best tested 2.777987 kg ideal host-fuel result with a 4.569852 m/s first release; additional release authority above that does not improve this tested campaign.
- [P92 clean-sheet reference screen](GEN6_REFERENCE_ARCHITECTURE.md): the next calculation reference is independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher. At the S4 study point a 4 kg payload carries 41.77 J ideal kinetic energy; the 10 g constant-acceleration screen is 106.5 mm. Installed mass, repeatability, shock/tip-off, catcher dynamics, cycle life and host compatibility remain open.
- The [host accommodation questions](HOST_COMPATIBILITY.md) are documented. They are not confirmed provider compatibility.

Those are dated verification results for bounded batches, not prototype readiness. All S3 selected release times lie at the latest permitted time; the search does not establish an interior timing optimum. S4 is a bounded enumeration, not a global optimum, and missing roots are not proofs of infeasibility. No operating interval, including the assumed 0.5 m/s minimum, is experimentally demonstrated. P92, P113 and E5 remain open.

### Eight-stage delivery checklist

| Stage | Status at this review | Remaining exit product |
|---|---|---|
| 1. Consolidate the record | Publication complete; current-state reconciliation in progress | Remove stale statements that still present the historical gas machine as the current Gen6 authority; keep configuration-specific failures intact |
| 2. Define reference missions | Illustrative targets with S1–S4 bounded screens | Individual, initial-distribution and replenishment specifications with windows, tolerances, uncertainty, host limits and disposal assumptions |
| 3. Compare complete campaigns | Two-payload terminal-state screen complete; full manifest open | Clearing/settling, uncertainty, installed burden and full-manifest delivery under one evolving host |
| 4. Select architecture | Clean-sheet reference selected; P92 remains open | Falsify or retain the reference using installed burden, failure topology and decisive release-cell evidence; then record the configuration decision |
| 5. Resolve decisive uncertainties | Coupon questions identified; no measurements | Small friction/latch/pusher/catcher experiments with predictions and acceptance criteria frozen first |
| 6. Engineer one release cell | Functional chain selected; components unselected | Coupled retention, release, actuator/accumulator, arrest, structures, tolerances, thermal behaviour, controls and faults |
| 7. Demonstrate scaling | Resource screens only | Physical two/four/twelve-payload arrangements, bank comparison, adjacent payload interfaces and crossover regions |
| 8. Produce reviewed build package | Not complete | Configuration-controlled drawings, BOM, purchased parts, assembly/inspection, instrumentation and independent review |

### What still controls the decision

1. **Mission value.** Compare springs plus timing and host manoeuvres against programmable release using the same target states and permitted controls. S4 supplies a shared-host two-payload screen; now charge clearing/settling, release/navigation error, attitude recovery and installation burden before using it to justify hardware. Retain failed and partial campaigns.
2. **Reference architecture.** The current calculation reference is the independent stored-energy cell. It is not protected from failure. Compare its installed burden and fault isolation against banks and the shared magazine, and its release implementation against direct electromechanical and compact gas backups. The historical 8 m gas guide and Gen5 remain comparators. Do not select 29, 89 or 120 m/s before a mission earns it.
3. **Fault consequences.** Determine which faults lose one payload versus the remaining manifest, whether backup exits are physically independent, and what stays safely retained after power loss, reset, jam or partial release. Shared command/power can defeat otherwise independent cells. Recovery must not authorize unsafe deployment.
4. **Release credibility.** Accumulator force-displacement, preload setting, latch release, pusher friction, clearance, inertia/CG variation, compliance, catcher dynamics and six-degree-of-freedom tip-off need credible models and ultimately measurements. Preserve superseded failed gas-guide results without treating their magnitudes as settled physics.
5. **Installed implementation.** Resolve actuator/accumulator, latch, pusher, catcher, sensors, controls, containment, support structure, energy, thermal path and complete mass/CG/inertia/cost accounting for the reference. Historical gas backup/vessel/fill work stays configuration-specific rather than silently becoming reference hardware.
6. **Host accommodation.** Turn the checklist into calculated geometry, reaction, power, thermal, command and campaign-duration demands. Provider-supplied envelope, loads, attitude authority and operating permission remain missing. Borrowed stage structure and extra supports are not free mass.
7. **Temporary constellations.** Demonstrate useful distribution or coverage duration, drift, defensible collision assumptions and disposal uncertainty. An initial release does not provide later stationkeeping or avoidance. Three to six years is a possible mission target to evaluate, not a guaranteed passive-decay timer.

### Prototype packages and BOLLEY

The [13-package prototype programme](PROTOTYPE_READINESS.md) remains the detailed build-readiness framework. Evidence maintenance, mission comparison and configuration screening advanced; none of the packages is closed by S4 or the P92 reference screen alone. Release physics, structures/tolerances, thermal/materials, accounting, controls/faults, manufacturing, experiments and independent review still need their own exit evidence. Hardware and facility checks cannot be completed in software.

BOLLEY's [current review](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md) remains a separate cooperative-interface programme. Its selected A9f/A5h winding and drive require fresh actual-geometry field/circuit evidence, supplier-backed current and switching limits, complete installed mass, mechanical tolerances and release/fault dynamics before it can be treated as a mature comparator. Fluxrelay, Fluxframe and Fluxpiston retain separate configurations and evidence. VOLLEY mission results do not complete those BOLLEY design tasks.

Gen5's remaining investigations stay in its own record. Complete them when a live claim or reused component needs the result, not as an arbitrary prerequisite to a different mechanism. Historical gas-Gen6 work follows the same rule. Reference/prior-art audits and register reconciliation remain work.

Use the [live register](../OPEN_PROBLEMS.md) and [computational closure view](COMPUTATIONAL_CLOSURE.md) for authoritative dispositions. Dated counts in older reviews are observations, not generated counters.

### Keeping this section current

At each completed batch, update the review date, current focus, next deliverable, blockers and links to committed evidence. Move a task to completed only after its declared checks and publication are finished. Identify partial results, failed searches, external dependencies and stopped alternatives explicitly. A roadmap edit does not close an engineering item, and a green test suite does not select a mechanism.

## Decision in force

Retain VOLLEY's purpose: provider-hosted control of satellite departure conditions. Use mission need to set departure authority rather than maximizing release speed.

The current **calculation reference**, selected by the 2026-09-16 clean-sheet P92 screen, is an independent retained cell with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher. Shared power, command and host navigation remain common-mode services. This selection advances the programme one level deeper; it is not P92 closure, flight-hardware selection, provider accommodation or prototype validation.

The historical gas-driven Gen6 remains an evidence-rich comparator with its 8 m guide, pressure-system studies, contact results and suspended trim retained in the record. Gen5 remains the frozen electromagnetic comparison. Direct short-stroke electromechanical and compact gas remain backups. BOLLEY Fluxrelay remains a separate cooperative-payload path. Banked and shared-magazine arrangements remain comparators to the independent-cell layout.

No working speed envelope, mass saving or provider compatibility is declared by this decision. S4's 4.569852 m/s first release is a bounded campaign result, not a product minimum or optimum. P92 and P113 remain open.

## One backlog, three views

The open-problem register records defects/questions, prototype packages organize their execution, and mission work establishes which configurations deserve further analysis. These are overlapping views, not additive task counts.

| Work stream | Register examples | Prototype packages | Next reviewable exit |
|---|---|---|---|
| Mission and host allocation | P113, E5, E28, P56 | 1, 9 | Clearing/settling, uncertainty, installed burden and full-manifest target-state closure |
| Gen6 configuration | P92; historical P117/P118 only if reused | 2 | Reference-cell falsification plus installed-burden/failure-topology disposition |
| Contact/release credibility | P103, P108, P67, P78, P88 | 3, 11 | Configuration-specific credible model followed by discriminating contact/friction evidence |
| Common-path failure and backups | P75, P81, P91, E32 | 8, 11 | Retention states, fault tree, path independence and recovery evidence |
| Host integration and campaign | P87, P94, P99, P68, E31 | 7, 9 | Installed interface, resource, reaction and last-payload budgets |
| Lifetime, environment and evidence | P79, E6, E11, E16, E18, P57 | 0, 6 | Source-backed assumptions, applicability and uncertainty |
| Gen5 reusable evidence | P18, P33, P34, P36, P45, P52, E24, E25, E33–E35 | 3–7 | Close only work required by a reused component or active claim; preserve other exceptions |
| BOLLEY selected winding and drive | A9f/A5h; current and temperature semantics | 4–7 | Coupled selected geometry, field, circuit, hot losses and protection |
| BOLLEY mechanical interface | P30, P39, P5, P10, P38, P6, P7, P21, P35 | 3, 5–9 | Clearance/load path, installed mass, release imbalance and payload acceptance |
| Build and external review | Configuration-dependent | 10–12 | Named test article, drawings, instrumentation, criteria and independent disposition |

Identifiers in the BOLLEY rows refer to that repository; all other identifiers refer to VOLLEY. No row closes the entries it groups. Use the live registers for current counts. Historical headings and later evidence need scope-aware reconciliation; a superseded branch is not an experimentally closed branch.

## Mission cases and measurable outputs

| Reference mission | Complete requirements still needed | What the current mission studies supply |
|---|---|---|
| Single propulsion-less payload | Full target orbit, delivery window, dispersion, permitted interface and disposal policy | S1 allocation plus S3 full terminal-state timing for one payload |
| Initial distribution of a group | Relative states/coverage at specified epochs, acceptable drift, collision constraints | S2 sequential resource accounting plus S4 two-payload shared-host terminal-state coupling |
| Replenishment batch | Existing constellation states, phasing tolerances, operational exclusions and launch insertion uncertainty | Not yet represented; do not relabel an energy ladder or two-payload target pair as replenishment |

[P113-S1](DEPARTURE_TRADE.md) is the single-position allocation screen. [P113-S2](CAMPAIGN_ALLOCATION.md) adds sequential two-body host propagation, changing mass, rocket-equation propellant use and assumed correction-count limits. It does not adopt flight requirements. In particular, zero host propellant in a screen does not mean zero deployment energy or zero attitude-control expenditure.

[P113-S3](TERMINAL_TIMING.md) supplies a single-payload terminal-state benchmark with identical timing grids and host controls for every comparator. It requires both Cartesian position and velocity at a common epoch and includes circular destinations. It remains a bounded seed/grid search.

[P113-S4](MANIFEST_TIMING.md) adds a second payload without resetting the host. It enumerates both target orders, ten release-time pairs and five release-authority screens, preserving retained host state, mass, fuel and recoil between deliveries. Forty-four of 100 tested campaigns are accepted. On the fine grid, BOLLEY, Gen5 and historical gas-Gen6 authority screens share the same best tested fuel result and first-release speed. This is a bounded comparison, not a global optimum or hardware ranking.

The next mission-to-architecture step is not another arbitrary velocity sweep. It is to add clearing/settling time, release/navigation error and host attitude recovery where they can change feasibility, then combine those results with installed-system burden and failure topology. Full-manifest closure remains open.

## Architecture shortlist and rejection gates

| Candidate | Account explicitly | Reject for a mission when |
|---|---|---|
| Conventional carrier with selected springs | Canisters, retention, integration, velocity spread, timed-release operations | Complete delivery constraints cannot be met within the allowed host resources |
| Current reference: controlled stored-energy captive pusher | Preload/energy adjustment, accumulator, latch, friction, pusher/catcher, reset and independent retention | Required release repeatability, shock/tip-off or installed burden cannot be met |
| Short-stroke electromechanical pusher | Current/field, power store, heat, moving-part arrest and magnetic exposure | Force/stroke/environment cannot fit the selected interface |
| Compact gas pusher | Seals, pressure containment, valves, consumables, support and contact | Required controllability, packaging or repeatability cannot be met |
| Historical 8 m gas guide | Existing pressure/contact/guide evidence plus full installed support | Mission need cannot justify its stroke, burden or contact uncertainty |
| BOLLEY Fluxrelay | All stationary hardware plus cage, attachment and lost panel area | Payload acceptance or complete drive/mechanical budget fails |

Compare independent cells, small banks and the shared magazine separately from energy source. A magazine is a payload-handling choice, not a necessary consequence of programmable departure. Do not fold unknown failure rates and costs into an invented weighted score. Retain resource tradeoffs and the consequences of uncertain rates.

## Scale and adjacent applications

Start the physical comparison with the existing 4 kg 3U reference. Then evaluate adjacent payload sizes using actual interface changes. At fixed relative speed, energy and momentum scale with payload mass; at fixed acceleration, required stroke scales with speed squared. Finite host recoil matters increasingly as payload/host mass rises. For larger spacecraft, synchronized distributed pushers at a separation interface may be more relevant than an enlarged CubeSat guide. This is a study direction, not CAD.

A programmable ground separation-test rig is a credible adjacent application. It must characterize support friction and gravity effects rather than present terrestrial motion as orbital validation. A flight payload-transfer mechanism is a second possible study, but needs its own customer, interfaces and requirements. Neither is an active product.