# VOLLEY four-repository audit and adversarial review

**Date:** 9 October 2026 (India time). **Status:** self-review, not an external professor's grade, peer review, provider approval or qualification. The scoring below estimates how two demanding readers might react to the *published evidence*, not to work planned for later.

**Engineering update later on 9 October:** [P119](../validation/P119_gen5_finite_force_fem2d.md) independently solves the finite 7-wave magnetic field with a 2-D finite-element vector-potential method and recovers the end-of-stator force decline. It reports 1,081.6 J ideal 2-D work on a 1 mm mesh versus 1,041.7 J from P118's 3-D analytic screen; the missing depth dimension prevents calling these equal 3-D force validations. [P117](../validation/P117_rated_energy_mass_audit.md) now reconstructs the old 124.488 J compact-output energy remainder as 90.964 J assumed converter loss, 32.460 J auxiliaries and 1.064 J numerical integration excess. Its residual is below 0.001 J; actual source components and a selected finite-force shot remain open. The scores below describe the audit snapshot and are not regraded by these two partial closures.

The [P120 follow-up](../validation/P120_gen5_finite_coupled_shot.md) now integrates the finite 3-D analytic force with the historical capacitor/ESR assumptions. It yields 12.448 m/s and 2,098.6 J gross draw if the full winding stays energized, or 1,394.4 J with a hypothetical shorter active-copper section. The branches do not close switching, supplier ratings, contact, arrest or host integration. They replace no accepted performance specification.

## Scope and method

I examined the published `main` branches of VOLLEY, VOLLEY-paper, VOLLEY-thesis and VOLLEY-lab. Together they held **2,069 tracked files** before this cleanup. Automated line-level checks covered the tracked Markdown, Python, LaTeX, JSON, shell and workflow files: approximately **818,000 source lines**. I manually inspected the four front pages, the paper's abstract, methods, decisive results, limitations and conclusions, the college report and review deck, market/prior-art positioning, CAD and validation summaries, and the scripts/results behind the central speed, mass and mission numbers. An automated pass over every line does **not** mean every historical line received independent scientific judgment.

The flagship's full local verification entry point passed **148 tests** and its documentation, baseline, result-freshness, artifact and companion gates in the prepared pinned environment. VOLLEY-lab's own gate initially failed because the new R1 entry was absent from its registry; the registry and heading were corrected and the gate passed. The paper and thesis had no independent current-surface CI; a dependency-light gate now checks their current local links, manuscript figures, decisive captured-result identities, artifact hashes and PDF/ZIP containers. It cannot replace physical tests or independent force FEM.

The current reader routes pass **78 local links and 22 manuscript figures** in VOLLEY-paper, and **192 local links and 22 manuscript figures** in VOLLEY-thesis. A broader heuristic scan still found **188 unresolved references in paper historical Markdown** and **486 in thesis historical/copied Markdown**, concentrated in copied validation sheets and the long thesis appendix. Many point to former flagship paths. These are archive-navigation debt, not evidence that a presently cited result file is missing; they prevent calling the entire historical corpus link-clean. Current academic claims should cite the local P115–P118 records and result files, not those broken historical links.

The decisive trace is local: [finite force](../validation/P118_gen5_finite_force_map.md), [energy and mass identities](../validation/P117_rated_energy_mass_audit.md), [assembly fit](../validation/P116_gen5_assembly_packaging.md), [immediate orbit geometry](../validation/P115_rated_orbit_cartesian.md), [matched mission](MATCHED_MISSION_REFERENCE.md), [mass JSON](../analysis/results/mass_properties.json), [native CAD](../cad/native/Gen5_Review.FCStd) and [unselected R1](../cad/FEEDER_CANDIDATE_R1.md). The corrected academic sources are the [paper manuscript](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper/blob/main/paper/paper.tex) and [college report](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis/blob/main/university/GEN5_FINAL_YEAR_REPORT.md).

## Findings by severity and disposition

| ID | Severity | What a reviewer finds | Current action or required closure |
|:--|:--|:--|:--|
| A1 | **Critical to performance claims** | The historical periodic-force model predicts 16.029 m/s. A finite-position 3-D **analytic** screen gives 1.042 kJ ideal work and 12.448 m/s only with optimal phase and omitted circuit/friction losses. It shares the magnetic field law with the older model. | Paper abstract, result heading/caption, thesis report and energy chart now identify the older case as historical. Independent position-dependent integrated-force FEM and a coupled circuit/trajectory rerun are still open. Neither speed is a verified rating. |
| A2 | **Critical to design selection** | The modeled dry system is 126.6 kg, or 10.55 kg per 3U. It fails the internal 2 kg screen by about 5.3× and the approximate 6 kg canister comparison by about 1.76×. The latter comparator is not a supplier quote. | Preserve both separate decision boundaries. Redesign and remeasure the *complete* installed system before asserting parity or economic value. |
| A3 | **Critical to mechanical feasibility** | The evaluated side-fed track and cassettes need 537 mm within 526 mm usable width; exact solids overlap by 32,915 mm³ per cassette. The wider R1 route study lacks actuation, retention, tolerances, mass and provider fit. | Keep R1 unselected. Select one feeder and analyze the full moving envelope, launch restraint, jam/abort and release contact before changing the Gen5 verdict. |
| A4 | **Critical to mission value** | The bounded common-input twelve-shot screen closes no option: accepted prefixes are 4/12 spring, 1/12 finite Gen5 and 1/12 historical Gen5. A single-event ideal-propellant comparison is favorable to the assumed finite Gen5 speed, but that speed is an ideal screen and no installed service benefit follows. | Rerun a selected architecture against spring plus host maneuver, onboard propulsion/drag and orbital transport at the same epoch, payload, deadline and uncertainty. |
| A5 | **High: academic framing** | The old paper abstract and figures foregrounded a challenged speed; the thesis report called a historical shot “rated” without an immediate caveat. | Reworded the abstract, result heading, captions, report and figure so the adverse screen arrives before any claim of current performance. PDFs rebuilt. The 17-page manuscript is IEEE-formatted only; no venue is selected. |
| A6 | **High: evidence boundary** | No VOLLEY article, named satellite/host interface, measured thrust, feeder cycle, magnetic-cleanliness test or provider approval exists. Field-point agreement is not an independent integrated-thrust check. | All remain open. Published tests of other deployers support methods and comparison, never physical validation of VOLLEY. |
| A7 | **Medium: repository hygiene** | The VOLLEY-lab R1 record broke its own namespace gate; three extra remote branches contradicted the one-branch rule. | Lab gate fixed. The three extra branches were inspected against later `main` content and removed; each remote now retains `main` alone. |
| A8 | **Medium: independent reader route** | The paper build guide still described evidence as generated by the flagship and pointed to a nonexistent local figure command. Paper/thesis had no own integrity CI. | Build guide corrected; figure command now syncs manuscript figure copies. New local checks and CI protect current front pages and artifacts. Historical copied links remain a separate backlog. |
| A9 | **Medium: college submission** | The 16-page chaptered report is a review draft; no official college report template or signature/authorship declaration was supplied. The deck and report name two students; the IEEE draft names one. | Keep actual contributions unstated pending the students' own statement. Apply official format and signatures if required by the institution. Do not invent individual work. |
| A10 | **Medium: IEEE contribution** | Programmable electromagnetic separation and stacked transport are prior art, including Zhao *et al.* (2022). Several closest leads remain metadata/abstract-only. | Frame the contribution as a bounded installed-system feasibility result, obtain full texts, and make a fair quantitative comparison before venue submission. |

## Simulated college panel read

**What earns credit:** a clear engineering question, a visible model chain, native CAD/STEP files, honest adverse findings, numerical cross-checks, a source map and a prepared 15-minute two-speaker route. The supplied college rubric awards 10 marks each for objectives and technical quality, 5 each for results/validation and documentation, and 10 for presentation/demonstration/viva. A functional physical prototype receives *additional recognition* in the supplied document; it is not stated as mandatory for those 40 marks.

**Likely viva challenges:** “What did you actually validate?” “Which speed is your result?” “Why does a completed project contain a CAD clash?” “Why use a 2 kg target and a 6 kg comparator?” “Does your orbital calculation prove your motor?” “If both students present, who did which work?” “Where is the official thesis-format report?” Honest answers can defend a computational *study*. A claim of a completed product would be contradicted by the submitted evidence.

| College criterion | Provisional mark | Reason |
|:--|--:|:--|
| Achievement of objectives | **7/10** | The analytical question has a recorded negative decision; build/qualification objectives cannot be claimed. |
| Technical quality and innovation | **6/10** | Broad systems work and useful checks; central force and release mechanics remain unresolved, while related mechanisms predate VOLLEY. |
| Results, validation and analysis | **2/5** | Several reproducible numerical checks and honest failures; no VOLLEY measurement and no independent integrated-force closure. |
| Report and documentation | **4/5** | Strong traceability and presentation pack; draft college format and archive-link debt. |
| Presentation, demonstration and viva | **7/10** | Achievable with the corrected deck and timed route; depends on actual delivery and precise answers. |
| **Illustrative total** | **26/40 (6.5/10)** | **Not a predicted pass/fail decision.** The institution's pass threshold and panel judgment are unknown. |

A strict panel focused on a functioning mechanism or an unreconciled 16 m/s claim could score lower. An examiner who values a carefully bounded negative computational result could score higher. The authors should lead with the discrepancy and failed criteria; concealing them would make the strongest part of the study look like an error caught by the panel.

## Simulated IEEE reviewer read

**Opinion:** the paper is promising as a transparent *negative system study*, but it is not ready for submission as a demonstrated programmable deployer. The direct electromagnetic prior art narrows novelty. The speed chain lacks an independent integrated-force method and the 3U configuration fails mass and CAD selection. The mission comparison is bounded, uses assumed hardware, and closes no manifest. A 17-page IEEEtran draft may exceed an eventual conference limit; no venue has been selected.

| Scale | Current /10 | Main move toward 10 |
|:--|--:|:--|
| Problem relevance | **7** | Name one specific payload/host/mission and quantify the useful release-state requirement. |
| Novelty against direct prior art | **4** | Complete full-text and patent search; articulate a testable system insight that prior deployers did not establish. |
| Model credibility | **4** | Independent finite-force FEM, winding/circuit closure, uncertainty and mesh/time convergence, mechanism/contact models. |
| Fair comparative evidence | **3** | Common-input springs, host maneuvers, propulsion/drag and transport, with real device masses and sensitivity. |
| Reproducibility and source transparency | **6** | Keep local CI and exact run inputs; repair historical links, pin solvers and expose data/figure lineage. |
| Venue submission readiness | **2** | Choose a venue, fit length and style, verify full texts, obtain independent technical review and resolve the main model discrepancy. |

**Overall publication readiness: roughly 4/10.** This is a review rehearsal, not an acceptance probability. A credible paper could instead ask why an apparently attractive electromagnetic release fails after finite-length force, installed mass and mission closure are counted; that would require the checks above to be strong enough to trust the negative conclusion.

## Simulated separation-mechanism engineer read

**Opinion:** the evidence hygiene and willingness to retain failures are stronger than the hardware maturity. A supplier or integrator would not begin a flight accommodation on the current geometry. They would ask for a payload and provider interface document, a selected feeder and restraint load path, measured or independently solved force over the entire stroke, an actual power/thermal design, host reaction and fault handling, magnetic exposure, and repeated release tests. The current R1 STEP is inspectable geometry, not a functioning dispenser.

| Engineering scale | Current /10 | First decisive closure |
|:--|--:|:--|
| Concept and requirements clarity | **6** | Select an actual reference mission, payload and host boundary. |
| Magnetic drive and power | **3** | Independent integrated-force map, coupled transient circuit, component derating and energy closure. |
| Feed, retention, release and arrest | **2** | Full mechanism CAD, moving-contact dynamics, failure recovery, brake heat and load paths. |
| CAD/manufacturing definition | **3** | Fit/tolerance stack, drawings, BOM, CG/inertia, material and bought-item traceability. |
| Mission and installed-system advantage | **2** | Close a matched campaign and demonstrate value after all installed mass, energy, operations and risk. |
| Safety and flight qualification | **1** | Instrumented article, environment/cycle tests, payload/provider approvals and independent safety review. |
| Evidence organization | **6** | Repair historical navigation and keep one controlled configuration/result/figure lineage. |

**Overall engineering/product maturity: roughly 2–3/10.** This rating says nothing about the student's effort; it reflects how far the design is from a selectable flight product. Code, open-source solvers and CAD can raise analysis credibility. A value near 10 on *flight readiness* requires physical measurements, a qualified satellite and provider acceptance.

## Ordered path to materially higher scores

1. **For the 10 October college review:** use the corrected deck and one-page handout; explicitly label 16.029 m/s historical, 12.448 m/s an ideal analytic screen, and the CAD/mass findings as failures. Do one timed rehearsal and keep the evidence PDFs offline. Explain that Gen5 is a finished *reviewed question*, not a released machine.
2. **Make the study internally decisive:** fix a named reference payload and host surrogate; extend the new independent 2-D force check to depth-resolved 3-D integrated thrust; combine force with winding/inverter/storage limits and propagate uncertainty. The historical 124.488 J arithmetic remainder is now explained, but the revised speed, orbit, heat and control figures still need one coupled rerun.
3. **Select a mechanically possible configuration:** model feed actuator, retention, opening sequence, cradle contact, tip-off, jams, abort/reset and brake. Export revisioned native CAD and STEP, drawings, tolerance stack, mass/CG/inertia and exact collision/motion reports. Rerun all budgets after selection.
4. **Prove mission value on common inputs:** use competent spring canisters with actual impulse and mass, host maneuvers, spacecraft propulsion/drag and transport services. Include host impulse/attitude, power, delay, reliability and disposal; find at least one scenario where VOLLEY loses and one where it may win.
5. **For an IEEE submission:** choose the venue, complete full-text and patent review, publish convergence/uncertainty tables and solver inputs, keep the paper's question narrow, obtain an independent technical read and meet page/format rules. A negative feasibility result is publishable only when the decisive models themselves are credible.
6. **For a product:** build an instrumented coupon then a representative integrated test article; measure force, contact, release speed/rate, brake, thermal, EMI and cycles against predeclared bands. Qualify the named payload and host interface, then submit to provider and safety reviews. Gen6's 1 km/s is a separate architecture trade and must pass the same installed-system gates.

The college can judge a computational investigation tomorrow. An aerospace company would judge a flight product only after the later gates. Keep those two decisions separate in every front page, slide and answer.
