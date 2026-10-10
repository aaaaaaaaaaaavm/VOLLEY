# Gen5 evidence-build programme

**Programme status: in work.** [Issue #44](https://github.com/aaaaaaaaaaaavm/VOLLEY/issues/44) tracks the six scoring gaps. This page defines the engineering routes and the evidence required to close each one. Gen5 is the **evaluated academic configuration**, with adverse results preserved. R1 and every new topology remain **unselected candidate revisions** until their dependent analyses are rerun. Gen6 is the separate future scaling programme; 1 km/s is an objective, not a Gen5 or Gen6 demonstrated result.

## First decision: is this architecture worth carrying forward?

[P123](../validation/P123_gen5_one_event_mass_screen.md) reproduces the fixed-fuel matched reference and re-solves a hypothetical one-event fuel load. At the optimistic finite-force 12.448 m/s conversion, the 126.562 kg Gen5 device is 54.562 kg heavier than a 72 kg spring class. It saves 1.866 kg of fuel for one event with both options loaded with 10 kg. Resizing fuel for only that event still gives a **+52.717 kg device-plus-fuel penalty**. Parity would require about **73.932 kg device mass**, a 52.630 kg reduction, at the same ideal speed. This is a *screen*, not a full-campaign or provider comparison. The existing six sampled twelve-release campaigns do not close.

The first architecture review should ask whether any credible mass and interface revision can approach that threshold **without** losing validated separation speed, structural margin, thermal control, payload protection or reliability. If it cannot, a rigorous IEEE contribution may be the quantified feasibility limit and failed criteria. That is a legitimate study result; it is not a product qualification.

The [necessary one-event bound](../analysis/results/gen5_architecture_bounds.json) shows that even zero host fuel burn would allow only 74.659 kg of Gen5 device for parity in this reference. The unselected [H1 captive passive-armature hypothesis](GEN5_H1_INTEGRATED_DEPLOYER_HYPOTHESIS.md) combines moving-mass reduction with structural integration as a falsifiable candidate. Its component ideas have prior art; neither its mass nor its novelty has been demonstrated.

## 1. Drive, force and power

**Ideas to test:** compare a segmented ironless stator with local commutation, a shorter active winding, different coil pitch and copper fill, and a lower speed command where the mission actually benefits. P120's 0.34 m and 1.30 m energized lengths are exploratory branches, not selected windings. Add the actual end turns, series/parallel connections, bus impedance, switching dead time and position-estimation latency before choosing a branch.

**Build and publish:**
- one source-controlled winding table and inverter/source bill of materials with part numbers, hot/cold resistance, inductance, ESR, continuous/pulsed current, voltage and thermal limits;
- FreeCAD/CadQuery coil and magnet geometry, a 3-D meshed magnetostatic position sweep (open-source candidate: Gmsh plus Elmer or GetDP), and an independent comparison with P121's surface-charge integral and P119's 2-D PDE;
- a circuit netlist (ngspice), explicit switching logic, position-dependent back EMF and force, and coupled electrical/kinematic integration using the same CAD revision;
- voltage/current/force/speed/temperature/energy histories, a closed energy ledger, time-step and mesh convergence, parameter corners, and failed cases.

[P125](../validation/P125_gen5_voltage_limited_screen.md) adds an ideal quasi-steady three-phase voltage/current screen using unselected historical winding and source values. It bounds sensitivity but does not specify a switch, coil or cell. A single string at the older 116–185 mΩ commercial ESR bound fails before release in that model; ideal two- or three-parallel-string branches complete while increasing cell count and source mass.

**Decision gate:** report the **achievable** release range under component limits and uncertainty. The 12.448 m/s ideal conversion is an upper screen until this gate closes. Preserve 16.029 m/s as a historical contradicted result.

## 2. Mechanism, packaging and mass

**Ideas to test:** center lift (R1), a translating shuttle, and a more compact low-count magazine. Score them on restraint during launch, single-payload indexing, fault isolation, reset after an abort, actuator count, service access, moving clearance, width, and installed mass. A lower-count magazine may reduce mass but must be compared on delivered payload count and operations, not per-shot performance alone.

**Build and publish:** one controlled native CAD model per candidate; part and assembly STEP exports; dimensioned envelope/interface/section drawings; identified datum scheme and GD&T assumptions; state-by-state kinematics, swept-solid interference and tolerance stack; hardware/fastener/harness/radiator keep-outs; revised part-level mass, center of gravity and inertia, with material densities and mass margins. Keep a compact design-selection table rather than quietly replacing Gen5 with R1. The current Gen5 side feed has an **11 mm width shortfall**; R1's scripted clearances do not show feed actuation or launch restraint. [P126](../cad/FEEDER_R1_TOLERANCE_SCREEN.md) further shows that R1's 5 mm nominal corridor fails an illustrative 0.5° alignment stack by 0.47 mm, while a 0.2° stack leaves 1.31 mm. These are declared study bands, not released drawing tolerances.

**Decision gate:** a candidate must close its own envelope, swept clearance, tolerance and mass ledger against a *named or explicitly surrogate* payload and host interface. Recalculate the drive and structural modes after any track, enclosure or cassette change.

## 3. Release, brake, safety and payload behavior

**Ideas to test:** use a latched sled with a documented preload/contact law; vary contact stiffness, friction, rail misalignment and trigger skew; include a redundant independent release path only if its added mass and common-mode risks improve the system trade. Compare passive eddy arrest with a hybrid mechanical backup sized for worst-case energy and thermal soak.

**Build and publish:** contact force and tip-off time histories; host reaction impulses/torques; brake deceleration and repeated-shot temperature; reset and jam-clearance envelopes; abort state machine and FMEA; magnetic-field map at payload equipment locations; structural modal/transient response on the *revised* geometry. Use the named payload's acceleration, shock, magnetic and cleanliness limits. Without them, label results as sensitivity cases, not compliance.

[P127](../validation/P127_gen5_release_arrest_bounds.md) now gives necessary ideal-speed sled energy, mean brake load and first-order host momentum bounds using the provisional 210 mm corridor. It does not solve eddy-current peak force, contact or heat.

**Decision gate:** every claimed limit traces to a source or declared study band, with uncertainty and fault corners. Physical bench/qualification tests and provider sign-off remain future work.

## 4. Matched mission, utility and economics

**Ideas to test:** give VOLLEY a mission target it can plausibly help, rather than choosing a spacing target that its higher release speed makes harder. Vary deployment altitude, target phasing time, orbital plane opportunity and release-speed command as a constrained trade. Compare springs plus competent host burns, onboard propulsion, differential drag where deadlines permit, and relevant transport services on *identical* payloads, epoch, host, constraints and accounting boundary.

**Build and publish:** a named reference payload and host or openly labeled surrogate; interface assumptions; twelve-shot sequential propagation and optimization with multiple starts; fuel, battery energy, mass, launch volume, delivery count, covariance/disposal and operations table; sensitivity and feasibility maps rather than a single favorable orbit point. Include failed optimizations as “no trajectory found under these starts and bounds,” not impossibility proofs. P123 is the reproducible one-event baseline for this package, not its conclusion.

**Decision gate:** at least one defined mission must close all twelve releases with the selected drive and installed mass, or the paper states that the studied Gen5 mission does not close.

**P124 update:** the [ideal precision-delivery design-space screen](../validation/P124_precision_delivery_design_space.md) now maps specified 450 km semimajor-axis targets and tolerance bands to tangential velocity requirements and minimum stroke acceleration. It exposes why 1 km/s cannot be assigned to a first ordinary-3U Gen6 article on the Gen5 stroke. It does not close host-state, release-vector or delivery-accuracy budgets. The [Gen6 prototype-to-flight roadmap](GEN6_PROTOTYPE_TO_FLIGHT_ROADMAP.md) makes the subsequent evidence gates explicit.

## 5. IEEE research claim and reproducibility

**Candidate contribution:** a source-graded, falsifiable *system-level feasibility evaluation* of a specific electromagnetic multi-satellite deployment architecture, including an independent force check, coupled constraints, installed burden and adverse mission results. Adjustable electromagnetic separation and stacked feed are prior art; neither is claimed as VOLLEY's invention without a narrower demonstrated distinction.

**Build and publish:** full-text and patent comparison with traceable claim/source/revision, a quantitative comparator table, design/solver convergence, model-form uncertainty, validated code and input/output snapshot, plus an independent technical read with logged responses. Keep analytic agreement, numerical convergence, literature analogy, measured validation and flight qualification as distinct evidence classes. Choose an IEEE venue before declaring compliance with its template or length rules.

**Decision gate:** every abstract number and graph points to one configuration, result file and uncertainty statement. A negative design finding is publishable if the method and scope are tight.

## 6. College release and public package

**Build and publish:** the college-format report, 15-minute two-presenter deck, demonstration route, claim-to-evidence table, figure and drawing indexes, reproducible source/results/CAD/STEP bundle, frozen configuration hashes, known exceptions and an independent panel-style read. Keep individual contribution claims unstated, as requested. Put the adverse 11 mm geometry, installed-mass and twelve-shot findings in the results and viva route, not only in footnotes.

**Decision gate:** freeze one academic Gen5 snapshot only after all figures and PDFs are generated from the same source/result/CAD revision, the repository checks pass on that commit, and all unresolved criteria are explicit. Freeze means a controlled **computational study**, not a built or certified dispenser.

## Publication sequence

1. **Published:** P123 source, committed numerical snapshot, figure and validation record; CI check recomputes the snapshot. This addresses a slice of package 4 and quantifies the package 2 mass target.
2. **Next:** choose one actual drive circuit and one mechanism candidate under an explicitly surrogate payload/host; publish their input sheets and negative as well as passing results.
3. **Then:** run the matched twelve-shot and payload safety analyses on that *same* revision; only then regenerate manuscript claims and presentation visuals.
4. **Final:** obtain an independent technical review and the college's official format; release the evidence bundle with hashes and exceptions. Provider acceptance, physical tests and peer-review acceptance cannot be generated computationally.
