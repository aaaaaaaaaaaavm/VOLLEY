# Change log / audit record

Every change made to this repository after the initial export is recorded here, so that
each edit can be traced to a cause and a source of truth. This file is deliberately
exhaustive: it exists to be audited later.

Read alongside `docs/PROVENANCE.md` (what stands behind each claim), `OPEN_PROBLEMS.md` (the defect
list these changes close) and `docs/DECISION_LOG.md` (why design choices were made).

---

## 2026-08-14 (thirty-ninth pass): the store was the wrong store, and A35's falsifier passes

| ID | Item | Detail |
|---|---|---|
| **A39** | **Seven of seven bands** | The store trade P60 asked for, declared against A37's window rather than around it, and carrying the gas option A37 deliberately excluded because inventing a pressure-vessel figure to win a trade is worse than leaving it out. |
| **STORE-01** | **Gas wins by four times, and not on energy density** | At 32.7 m/s a steel spring is **11.41 kg** and busts the budget at **34.3 m/s**; **cold gas is 2.98 kg and busts it at 89.4.** A **1.71 litre** bottle runs **all twelve shots** — 15.8 mm bore, 1.00 mm wall, 0.84 kg of cylinder. |
| **WHY-01** | **The spring's problem was never storing the energy** | It was **having to be cocked twelve times.** 7.13 kg of store needs **4.28 kg of mechanism** to re-arm; gas separates the store from the actuator, so re-arming is a valve. |
| **P60** | **Closed. The store is no longer the binding constraint** | Gas fits the budget to 89.4 m/s, which at the 25 g cap needs **18.8 m of stroke** — more than any stage class in A37. **Mass has stopped constraining velocity and stage length has started**, which is the problem the host-integrated reframe was aimed at. |
| **A35-FALSIFIER** | **Settled, and it passes** | A35 declared: *the falsifier is that C3's replacement weighs more than 60 % of what came out* — **14.26 kg of the 23.76 released.** The replacement weighs **2.98 kg. The mass did not relocate**, and A37 bands 4 and 8 failed against a store that was the wrong store. |
| HONEST-01 | **Where this is most likely wrong, checked rather than asserted** | The reservoir vessel at 0.233 kg is **underestimated 4–6×** against real 1.7 L / 200 bar hardware; the 1.5 kg allowance is over half the total; the 1 mm cylinder wall must also serve as rail and take A38's 202 N preload, unmodelled. **Corrected for all three, gas lands near 6 kg and every band still passes.** |
| RISK-01 | **What arithmetic cannot survive** | Filling a 0.43 litre swept volume in a **133 ms** stroke is roughly **3 L/s** through a regulator, and A39 models none of it. **Gas removes a mass problem and introduces a fluid-system problem.** That, and the seal, are where it will actually be decided. |

**What authorised it.** P60, and A38 having established that tip-off does not bind. **No band was
edited, widened or moved**; A39's seven were committed before `analysis/store_trade.py` existed.
All four checks pass.

---

## 2026-08-14 (thirty-eighth pass): tip-off does not bind Gen6, and a run sheet was stale against its own script

| ID | Item | Detail |
|---|---|---|
| **A38** | **Five of six bands, band 1 FAIL** | A34 closed kill criterion 4's open half well, and **every number in it was computed at Gen5.** A37 takes the payload's share of the push from 395 N to 981, a factor of **2.4 on the term driving the whole result.** Checking before adopting is the P19 and P53 pattern applied *before* the point moves rather than after. |
| **TIPOFF-01** | **The closure does not merely survive — it improves** | Settling falls **27.88 → 17.69 ms** in a **133.3 ms** stroke, so it occupies **13 % instead of 19 %**. Critical restitution rises **0.9263 → 0.9462** against a published aluminium range of 0.3–0.7. **Residual at force removal is still exactly zero** for every clearance A23 tabulated. Arrival worsens to 355 °/s and stays what A34 established: transient, never a release rate. |
| **CEILING-01** | **Tip-off is not the binding limit** | The ceiling it imposes is **30.9 g** against a **25 g** qualification cap, so **A37's 1.83–2.18 m window stands** and the store trade has its acceleration. |
| COST-01 | **The cost lands on preload, as predicted** | **81.2 → 201.7 N per contact.** Band 5 passes at a 250 N limit, and passing it is not the same as the mechanism being easy: A34 already records that the cradle mechanism does not exist, and a 202 N preload releasing inside a 1 N residual is harder than an 81 N one. |
| PRED-01 | **The prediction held** | Written before the script: arrival ~55–356 °/s (**355.1**), settling falling to ~18 ms (**17.69**), stroke ~134 ms (**133.3**), preload ~204 N (**201.7**). **The first prediction this session a band did not overturn.** |
| **P61** | **A34's recorded figures are stale against its own script** | Band 1 drove A34's imported forms at the Gen5 point and got **27.88 ms** against a recorded **27.25**. A34 was recorded on 2026-08-13 at the point ADR-030 superseded **the same day**, and `cradle_restitution.py` reads `motor_model` live — **so the script tracked the correction and the record did not.** No verdict flips; all five of A34's bands still pass. |
| RECORD-01 | **Annotated, not edited** | `validation/A*.md` is excluded from every propagation this project runs because each is a record of a run at its own point. A34 carries both columns side by side now, the treatment `CROSS_INDUSTRY.md` and `VALIDATION_REPORT.md` already have. |
| GAP-02 | **And the general case is not fixed** | Every run sheet whose script reads `motor_model` live has the same exposure and **nothing checks it.** A regression band comparing recorded figures against current script output would catch the class; A38 band 1 caught this one by being aimed at it. **Recorded rather than built**, beside the cross-repository manuscript check P58 names. |

**What authorised it.** A37's design point, checked before adoption rather than after. **No band was
edited, widened or moved**; A38's six were committed before `analysis/tipoff_gen6.py` existed, and
A34's five are untouched. All four checks pass.

---

## 2026-08-14 (thirty-seventh pass): the stage is the deployer, and the binding constraint moves to the store

| ID | Item | Detail |
|---|---|---|
| **A37** | **Six of eight bands, 4 and 8 FAIL** | Bands 1–3 enforce the honesty rules mechanically: **the 2.0 kg threshold does not move**, added mass per satellite is never reported without dry mass per satellite beside it, and nothing is credited to the stage without naming the subsystem that provides it. All three pass. |
| **SPLIT-02** | **Where 84.53 kg goes once the stage is the machine** | **29.75 kg deleted** by a design with no mover and no pulse; **43.33 kg provided** by stage structure, skin, avionics, thermal and harness, each naming its subsystem; **11.45 kg added.** The entire added base is cassette shells and gates — **the same 11.45 kg A36 measured as the containment floor, reached from the opposite direction.** |
| **CRIT-01** | **Kill criterion 1 closes at 3U, on a second numerator argued on its merits** | **1.608 kg per satellite** on a small kick-stage class against the unchanged 2.0 kg threshold. **Dry mass per satellite still crosses at 7.044 kg and that is not withdrawn.** P59 stays LIVE: a second numerator is not the criterion being met, and D2 still decides which one a customer pays. |
| **P60** | **The store scales as v², and it is now what binds** | 4.91 kg of spring at 1.5 m, 9.81 at 3.0, **26.16 at 8.0** — **78.5 % of everything added.** Band 4 was A35's own falsifier, declared and left open: the pulse released 23.76 kg and its replacement had to stay under 14.26. **Stage length is free; the spring that exploits it is not.** |
| SELECT-01 | **And the selection rule was badly designed** | No declared class satisfied every band, so the script fell back to maximum velocity — the worst case for both failing bands. **At the small class the falsifier passes comfortably at 7.85 kg.** The bands are evaluated as declared and the failure stands; its proximate cause is recorded rather than glossed. |
| WINDOW-01 | **The declared classes bracket the answer without containing it** | Derived after the run and **not a band**: every declared band is satisfied between **1.83 m and 2.18 m of stroke, 30.0–32.7 m/s, about 1.83 kg/satellite.** The classes declared were 1.5, 3.0 and 8.0 m. **No class was added after the run and none will be.** |
| TENSION-01 | **Velocity and kill criterion 1 are now in direct tension, priced** | 27 m/s closes the criterion; 38 m/s does not. Where to sit on that curve is a product decision rather than an analysis. |

**What authorised it.** A question about scale, and the arithmetic it prompted. **No band was
edited, widened or moved**; A37's eight were committed before `analysis/host_integrated.py`
existed. Two failed and produced **P60**. All four checks pass.

---

## 2026-08-14 (thirty-sixth pass): the last route to kill criterion 1 closes, and it is a market decision

| ID | Item | Detail |
|---|---|---|
| **A36** | **Magazine density measured, six of seven bands, band 4 FAIL** | A35 named the divisor as the only lever reaching kill criterion 1. It reaches it at **N = 116**, not the **N ≤ 30** the band required. **The band is not widened; it produces P59.** |
| SPLIT-01 | **Where the mass actually goes as the manifest grows** | Fixed **59.58 kg**, magazine skin **13.50 kg** growing as N^(2/3), and **0.954 kg per satellite** of containment read from A35's C6 tagging rather than restated. The split was declared in the run sheet **before the script existed** so it could not be tuned to pass. |
| **ENV-01** | **N = 116 cannot be packaged at all** | Every factorisation puts the stack or the width outside the 1500 mm track length — 4 × 29 is a 3016 mm stack, 29 × 4 a 4814 mm width. The largest that fits is **N = 126** at **1.941 kg/satellite**, on a **244.6 kg** machine running a **42-hour** campaign. |
| **CORR-01** | **A number reported from A35 was wrong by more than a factor of two** | A35's saturation figure was divided naively: 49.23 kg over 24 satellites, "2.05 kg each", allowed to be "near 2.5" if containment grew. **It is 4.330 kg** — the naive division held the machine constant while containment *and* skin grow with N. **Band 4 was written to test exactly that claim and caught it.** |
| **P59** | **Two of the three routes to kill criterion 1 are now closed by measurement** | **Architecture**, by A35: 49.23 kg survives all 64 corners. **Manifest size**, by A36: reachable only outside the envelope or at its edge. **Smaller payloads is the only route left**, and it is a different market, a different customer and a different qualification campaign against a repository whose every CAD file is 3U. |
| KILL-01 | **`KILL_CRITERIA.md` states it, and the threshold is not moved** | ~2 kg is what canisterised dispensers achieve; a threshold revised after a result is known is not a threshold. The honest options are recorded as: change the payload class (**D2**), or publish the criterion as crossed on the front page. |
| WARN-01 | **And the flattering metric is named rather than adopted** | *Δv per kilogram per satellite* puts this design **5.4×** ahead of a dispenser and would rescue the criterion. It is recorded as exactly the sort of metric a project reaches for once the plain one has stopped being kind. |

**What authorised it.** A35's own conclusion, tested. **No band was edited, widened or moved**;
A36's seven were committed before `analysis/magazine_density.py` existed. All four checks pass.

---

## 2026-08-14 (thirty-fifth pass): the phase claim was measured against the wrong thing

| ID | Item | Detail |
|---|---|---|
| **P56** | **30° of phase costs 468 seconds of waiting, and the repository sold it as 1.4 days** | Satellites released at different times from the same host arrive at different true anomalies **in the same orbit**, at zero Δv. At 450 km the in-track rate is **0.0641 °/s**. [ADR-020](docs/adr/020-inter-shot-cadence.md)'s adopted 1200 s cadence already gives **76.9° per shot** before the motor is energised. **A spring and a clock do phase spacing.** |
| **A21-R** | **Six bands, declared before `comparators.py` changed, six pass** | Timing beats commanded differential by **255×** and drag by four orders. **`comparators.py` changed by addition only** — the diff deletes no line, so A21's seven bands are provably untouched, and band 3 remains true: a spring's *designed differential* is zero. The error was inferring that phase therefore requires differential velocity. |
| **DRIFT-01** | **And the free method is the better one** | A commanded differential sets a **rate**, not an offset: **21.75 °/day at 10 m/s, and it never stops.** The design passes *through* 30° and keeps going, and a propulsion-less satellite cannot null a drift it has been given. Timed release sets an offset that holds. **For a string of pearls the free method wins outright**, and that is stated rather than softened. |
| **R5, R6** | **What survives, and it is the stronger claim** | A clock changes semi-major axis by **0 m** at any cadence, and lifetime by **×1.0000**. One shot changes them by **+28.8 km** and **×1.602**. **The differentiator is orbit change, and the repository had been leading with the one claim of the two that a clock deletes.** |
| DIR-01 | **It argues for more velocity, not less** | Phase spacing needed only a *differential* and would have justified a much smaller machine. Orbit change scales with **absolute** Δv. The design point moves the other way, and an earlier suggestion in the opposite direction is withdrawn. |
| **P57** | **The nearest published neighbour is still unread** | `RELATED_WORK.md` identified it on 2026-07-30. A voice-coil deployer whose stated purpose is *to control precisely the separation velocity of CubeSats with different masses*, by *regulating the current value*, on a direct-drive linear machine with **no moving magnet carrier**. That is this project's claim and the sled-free topology it treats as open. **Every publisher domain is blocked from this environment**; recorded in `RELATED_WORK.md` at `confirmed`, and **nothing was written into `PRIOR_ART.md`**, whose header states all its entries have been read. |
| **P58** | **The thesis manuscript was a stale fork of the conference manuscript** | ADR-031 says they carry the same concept and not different designs. They shared 414 of 447 lines; **all 33 differences were superseded numbers** — K<sub>t</sub>, exit velocity, efficiency, dry mass, and **6.38 kg against 7.04 kg per satellite** — plus a depth-averaging sentence the thesis lacked. **Not one difference was thesis-specific.** ADR-028 moved the manuscript out of the export tool's reach and nothing replaced it, so the baseline change reached one repository and not the other. **The same shape as P53.** |
| GAP-01 | **And nothing checks it** | Two authored manuscripts in two repositories, and neither `check_links.py` nor `make_baseline.py` can see across a repository boundary. **A cross-repository manuscript check is the missing tool.** Recorded rather than built. |

**What authorised it.** A literature check, and the arithmetic it prompted. **No acceptance band was
edited, widened or moved**; A21-R's six were declared before the script changed, and the change was
purely additive. All four checks pass.

---

## 2026-08-14 (thirty-fourth pass): the sweep that found the propagation had stopped at the documents

| ID | Item | Detail |
|---|---|---|
| **P53** | **Eight analysis scripts were still running at the superseded 16.388 m/s** | ADR-030 was carried through the prose by `propagate_baseline.py` and through `sizing.py` and `motor_model.py` by hand. The tool walks `.md` and `.html` only, so a number pasted into a `.py` was invisible to it, and nothing else had a fork guard. `astro.py` was one of the eight, which put **every astrodynamic headline in the repository** at the wrong operating point. |
| **MASS-01** | **`payload_family.py` carried `DEPLOYER_DRY_KG = 76.5` under a comment reading "mass_properties.json"** | Dry mass had moved to 84.5. Kilograms per satellite — **kill criterion 1's entire subject** — was computed 8 kg light while the documents carried the corrected 7.042. A comment claiming a source is not reading the source; it now reads it. |
| **FORK-01** | **`motor_model.operating_point()`, and no literal anywhere else** | Nine call sites read the rated shot instead of restating it. A literal cannot fork if there is no literal. `payload_family.py` reads `mass_properties.json` the same way. |
| MOVED-01 | **What the corrected point actually changed** | Lifetime multiplier **×1.62 → ×1.60**; extension **+61.8 % → +60.2 %**; ratio against the fastest spring **7.52× → 7.33×** and **6.6× → 6.4×** on velocity; recoil **65.6 → 64.1 N·s**; campaign impulse **0.787 → 0.769 kN·s**; cold-gas loss at 3U **7.5× → 8.3×**; conjunction minimum **54.9 → 42.2 km**; loaded mass **124.5 → 132.5 kg**. **Every direction is unfavourable**, which is the expected sign. |
| **P54** | **A24 band 1 now fails, and is not being edited** | It requires agreement within ±1 % of `payload_family.py` and encodes that figure as the literal **6.375**. The model and its reference still agree — both return 7.042 — but the band's frozen snapshot does not. It stands as declared and as failed. Closing it needs a **re-declared A24-R band 1**, committed before the re-run. |
| **P55** | **`velocity_levers.py` prices every lever at the centre-plane K<sub>t</sub>** | All four distinct geometries in the table predate the depth-resolved solve. **Not fixed by scaling**: applying 0.9558 to the changed-geometry rows assumes the depth factor is independent of magnet thickness and airgap, and nothing has measured that. Four solves would close it. |
| **REG-01** | **The register classifier was matching a hyphenated adjective, and then reading its own answer back** | `\bRESOLVED\b` matches inside *depth-resolved*, so an entry citing ADR-030 by filename was classified `CLOSED`; the `Status:` line it wrote then sat inside the window the next run scanned, carrying the note *"resolved; see the entry for what closed it"*. One wrong call re-justified itself forever. **P18, P30, P32 and P43 were sitting on that latch** and move to their correct statuses. Counts: **90 entries, 36 LIVE, 24 CORRECTED, 30 CLOSED**. |
| SUPER-01 | **The superlinearity table is generated now** | `docs/REVIEW_RESPONSES.md` pasted it by hand, so it kept the operating point it was written at while `astro.py` moved underneath it. `comparators.py` emits it as a REPORT block; no band was touched. |
| BANNER-01 | **The companion banner said "nothing here is authored"** | False since ADR-028 moved the manuscript into the companions. A banner telling a contributor every file will be overwritten, in a repository where some files never are, is wrong in the direction that loses work. It now names what is generated, what is authored, and the freeze rule from ADR-031. |
| **LAB-01** | **`VOLLEY-lab`'s front page still described a Phase II research track** | Rewritten by hand — it is authored, never generated — to the vault role, with the one rule stated and each of the four long-form entries carrying **why it stopped**. |
| LAB-02 | **`docs/VAULT.md`'s link to `PII-14_cable_driven_gondola.md` was reported broken, and was not** | The lab checkout in hand was two commits stale. The file has existed upstream since 2026-08-10, at 295 lines, and a replacement was written before that was checked. **Recorded because the failure mode is the interesting part**: cross-repository links cannot be verified by `check_links.py`, so the only evidence available is a working copy, and a working copy is not evidence of anything unless it has been fetched. |
| LINK-01 | **`tools/lab-seed/` is exempt from link resolution, not from the block check** | Its relative links resolve in the repository it seeds. It stays inside the cross-link consistency check, which is the check it actually needs. |

**What authorised it.** A consistency sweep, not a design change. **No acceptance band was edited,
widened or moved.** One band verdict changed and it changed to FAIL (**P54**). All four checks pass.

---

## 2026-08-13 (thirty-third pass): four repositories, not two phases

| ID | Item | Detail |
|---|---|---|
| **ADR-031** | **The two-phase model is retired; the programme is the four repositories and their roles** | The phase model measures **calendar position**; every decision that mattered turned on **evidence maturity**. "Phase I" needs a glossary before anything parses, and the gate needed administering — *"is this Phase I or Phase II?"* came up repeatedly on 2026-08-13 and cost judgement each time. |
| **ROLE-01** | **The four roles, stated without roman numerals** | **lab** — ideas that never became a complete thing, and the evidence behind them. **main** — the authoritative record, improved continuously. **paper / thesis** — the same concept at its most reliable, **frozen when presented or published.** |
| **FREEZE-01** | **The freeze is an external event now** | Paper and thesis may be improved until publication, **provided what enters them is stable, effective and reliable against the problem statement.** A submission date slips and a boundary is arguable; **publication is neither.** First hard external line this programme has had. |
| GATE-01 | **What replaces the phase gate: three maturity tiers, each with a stated crossing condition** | **vault → main**: bands declared before the script existed, and run — *unchanged and not negotiable*. **main → paper/thesis**: stable, effective, reliable. **paper/thesis → frozen**: published. **Nothing crosses upward on enthusiasm**, which was the point of the phase gate and survives its retirement. |
| VAULT-01 | **`docs/PHASE_II.md` → `docs/VAULT.md`**, retargeted in 21 files | Same eighteen entries, renamed to what it is, with **the one rule made explicit: every entry states why it stopped.** PII-16 carries the edge factor that killed it, PII-17 the mass arithmetic that declined it. **That is what makes it evidence rather than a pile.** |
| BASE-07 | **`BASELINE.md` loses one clause and keeps the rest** | *"Performance improvement may not move the baseline"* was a pure freeze artefact and is withdrawn. **Naming the trigger, stating which validations it invalidates, propagating scripts → figures → paper, and recording it in an ADR all stay** — none of them was ever about phases. Edited in the generator, not the output. |
| DOSSIER-04 | **Amendment 4 to the programme dossier** | Records the departure from §§2 and 10, what it keeps, and what is given up. **Phase I is not un-closed** — `PHASE_I_CLOSURE.md` keeps its name as the record of the event. |
| **RISK-01** | **And the risk is named rather than hidden** | Main improving freely is exactly how the search becomes unbounded again. The protection is that **nothing reaches paper or thesis without being reliable**. If a year from now main carries three architectures and the paper carries none, this decision failed and ADR-029's stopping rule should be reinstated as a date. |

**What authorised it.** A programme decision by the sole author. **No script value, no band, no
operating point and no baseline moved.** All four checks pass.

---

## 2026-08-13 (thirty-second pass): Phase I closed

| ID | Item | Detail |
|---|---|---|
| **CLOSE-03** | **Phase I is closed on Gen5** | Measured against `PHASE_I_CLOSURE.md` §9's own 2026-08-05 definition — *categories A, B and C closed; D, E and E4 open with named owners* — and that state is now reached. §10d records it. |
| CLOSE-04 | **Category A closed by A33, A34 and A15 band 7** | The track's dynamic case, the cradle restitution model, and the one band that could only ever be closed by reading a generator. |
| CLOSE-05 | **Category B closed** | P14 superseded by generated CAD, P19's general claim shown false, P20's lesson made a standing rule that A2 band 4 was then written under, P35's false header struck and given an assertion, P38 and P39 closed on their own criteria. |
| CLOSE-06 | **Category C closed by ADR-030** | All four decisions taken together rather than piecemeal. |
| **CLOSE-07** | **What stays open, with owners** | **E4** — nothing measured, owner **B-1** at ₹22,000, still unordered. Category D to hardware and external parties. Category E blocked, not open. **P36's damping half** to T-2's sine sweep. **Kill criteria 1, 2 and 3 remain crossed** at the 3U design point. |
| CLOSE-08 | **Register at close: 87 entries, 31 live** | 10 P-items, 21 E-items, of which **E4, E5, E14 and E15 are permanent caveats rather than debt.** |
| FRONT-04 | **The front door says so** | README opens with the closure, the four corrections and what they cost, and points at the Phase II target and at B-1. |

**What Phase I is:** a design that is frozen, internally consistent, and knows what is wrong with
it — four verification tools passing on every commit, a baseline generated from the scripts, and
**twelve missed acceptance bands published as numbered defects rather than widened.**

**What it is not:** a design that has been shown to work. **Nothing has been measured.**

---

## 2026-08-13 (thirty-first pass): the baseline moves, and every number moves the wrong way

| ID | Item | Detail |
|---|---|---|
| **ADR-030** | **Four decisions taken together; the baseline moves** | P46, P28, P10 and P32, taken at a boundary rather than piecemeal because **propagation is the expensive part and doing it once is cheaper than twice.** |
| **P46** | **The thrust integral is depth-resolved** | `thrust_constant()` now Gauss-Legendre averages `B_y` over z ∈ [−45, +45] mm before the Lorentz sum — **a change to the physics, not a pasted factor** (ADR-015). **K_t 11.0258 → 10.5386**, ratio **0.9558, exactly A2 band 2's measurement**; **v_exit 16.388 → 16.029 m/s**. `nz = 1` reproduces the superseded value exactly, so A2's ratio stays checkable. Computed and held for three days before being applied. |
| **BASE-06** | **And it dropped the ceiling below the fleet setpoint** | 16.2 m/s against a new ceiling of 16.029 is **101.07 % of it** — the exact condition **ADR-014** forbids, because a setpoint the machine cannot reach makes the dispersion figure a measure of shortfall rather than of sensing noise. **`V_FLEET` 16.2 → 15.8 m/s**, holding ADR-014's *fraction* rather than its number. **The rule survived contact with the correction.** |
| P28 | **Regen section 240 → 39 mm** | 39 + 300 fits the 339 mm arrest section. Recovery 291 → **47 J**. **Dropping regen entirely was recommended first and withdrawn**: 2 points of efficiency, which is in no kill criterion, against **+24 % brake duty**, which worsens **E34**, fourth on the lethality ranking. |
| P10 | **Packaging enters the rollup as a labelled placeholder** | **8.0 kg, no derivation**, named `(P10 PLACEHOLDER, 8.0 kg, no derivation)` so it cannot be cited as computed. Dry **76.5 → 84.5 kg**, per 3U **6.378 → 7.042 kg**. |
| P32 | **Gen4 retired** | Never exported, releases at s = 1200 mm over a 900 mm stroke where `analysis/` assumes 1500 over 1.3 m. **A geometry that cannot be exported, cannot be checked, and does not match the parameters is not a generation this project has.** |
| **SYNC-01** | **`sizing.py`'s fork guard walked the propagation through eleven coupled constants** | `_check_operating_point` refused the run at each one — V_EXIT, E_DRAWN, F_CMD, T_PULSE, Q_COPPER, Q_ESR, SAG_FRAC, E_RECOVERED, KE_TO_BRAKE, S_REGEN and four regen loss terms — until every one matched `motor_model`. **It also caught a unit error I introduced**: `T_PULSE` is in seconds and a blind substitution set it to 162.3 instead of 0.1623. |
| PROP-01 | **`tools/propagate_baseline.py`: 214 occurrences across 37 live documents** | A whitelist, not a `sed`. **Most occurrences of `16.388` in this repository are historical and must not change**, so `CHANGELOG.md`, `OPEN_PROBLEMS.md`, `HISTORY.md`, `DECISION_LOG.md`, `CHANGELOG_CAD.md`, `RESULTS.md`, the ADRs and every `validation/A*.md` run sheet are excluded **by construction**. |
| **COST-01** | **Every headline number moved the wrong way** | Efficiency **21.0 → 18.8 %**, brake duty **977 → 1162 J**, kg per 3U **6.378 → 7.042**, lifetime multiplier 1.618 → 1.602. **Kill criterion 1 goes from crossed by 3.2× to crossed by 3.5×.** Nothing improved. That is what taking these decisions costs, and it is why they were deferred. |
| VALID-01 | **Validations invalidated: none, and it was checked** | Every run sheet records the point it ran at. **A28 is unaffected because the loop is feedback-linearised and K_t cancels out of the loop transfer entirely** — the fact P47 turned on. A4 and A5 already predate the point and say so (P19). |
| CNT-16 | **Register 34 → 31 live** | P46, P28, P10, P32 corrected or closed. 10 P-items live, 21 E-items. |

**What authorised it.** `docs/BASELINE.md` change-control rules 1 and 2, and an explicit owner
decision on all four after the composite cost was put in front of them. **Propagated in the
required order: scripts, then results, then figures, then the baseline.** All four checks pass.

---

## 2026-08-13 (thirtieth pass): Phase I closes on Gen5, and the exploration stops

| ID | Item | Detail |
|---|---|---|
| **ADR-029** | **Phase I closes on Gen5. Gen6 is the Phase II design target and is not built** | Gen6 beats Gen5 on every axis that has been measured, and is **nine measured bands against a hundred analyses**. Re-baselining would move K_t, v_exit, the mass rollup, the cost model, the CAD and the manuscript — to replace an architecture with a hundred analyses by one with nine bands. **The cost is stated plainly: Phase I closes on an architecture its own author now believes is second-best.** |
| **STOP-01** | **And the reason is that the exploration demonstrated ADR-021's failure mode** | Six register entries opened in one day; **two are defects in the machine** (P47, P52) and **four are defects in analyses written that day** (P48–P51). That is the apparatus generating its own workload, which is the sentence ADR-021 froze the register over. Meanwhile **B-1 — one measurement, ₹22,000 — is still unordered.** |
| STOP-02 | **No further architecture exploration before B-1** | Exploration does not terminate on its own. The ADR's own validation test is measurable: **if B-1 is still unordered in a month, the stopping rule did not bind and this decision bought nothing.** |
| **CLOSE-01** | **`PHASE_I_CLOSURE.md` §10c — distance to close, measured** | Against §9's own 2026-08-05 definition rather than against an empty register: **three analyses** (P36 the only substantial one, plus P41 and A15 band 7), **a handful of bookkeeping records**, and **four decisions, none of which is engineering work** (D3 the held K_t correction, D8 retiring Gen4, P28, P10). Categories D, E and E4 stay open with named owners, as they were always meant to. |
| CLOSE-02 | **P52 is not a Phase I blocker, and the reason is on the record** | Gen5's winding is segmented for fault isolation and driven as one section (**ADR-022**), so it has no segment handover. P52 is a property of the Gen6 drive and travels with it. |
| PII-TGT | **`VAULT.md` names Gen6 as the design target** | With its nine bands and its unsized remainder both stated, and the gate untouched: a target is not a promotion, and Gen6's entry criteria are not all written yet, let alone met. |

**What authorised it.** A programme decision by the sole author, recorded as ADR-029. **No script
value, no band, no operating point and no baseline moved.** All four checks pass.

---

## 2026-08-13 (twenty-ninth pass): the Phase II items interact, and two of them cancel

| ID | Item | Detail |
|---|---|---|
| **PRIOR-01** | **The operational shipboard electromagnetic launcher, cited for the first time** | The only electromagnetic launch system in routine service anywhere, and `PRIOR_ART.md` had never mentioned it. **Three of its architectural choices are choices this project reached independently**: linear induction with a passive armature, a segmented stator energised only under the shuttle (**ADR-022**), and flywheel pulsed storage (**A25**). Three convergences with a flown system is a stronger credibility argument than anything in `VALIDATION_REPORT.md`, and it was not being made. |
| **PII-18** | **The plate does not have to be on the satellite** | As a **reusable shuttle** it is 0.398 kg against the Gen5 sled's 9.445, so the arrest falls from **1938 J to 82 J**. The satellite is **unmodified** again — no consumable, no interface to publish, no adopters to recruit — which **dissolves decision D2**, because every payload class works. The geometry that decides it is **twin fins straddling the satellite**, which puts the thrust line through its own axis and removes **P41**'s centre-of-mass offset. Nobody has drawn it. |
| **SYN-01** | **PII-1 is superseded, and the reason is arithmetic** | The momentum-transfer release is the project's self-declared strongest idea, and its lever **is the mover's mass**: Δv = √(2EM/(m(M+m))). On a 0.6 kg shuttle the same 41.8 J buys **1.65 m/s instead of 3.83**, and matching the original costs **225 J**. PII-18 reaches the same velocity by not putting the energy into a sled, and **adds no mechanism to the release path** — which is PII-1's own stated reason for deferring. |
| **SYN-02** | **PII-15 is superseded by margin nobody is spending** | Gen5 runs at **10.5 g of a 25 g budget**, which was never a choice — it is where thrust over mass landed with a 9.445 kg sled aboard. At **16.1 g the stroke is 850 mm instead of 1300**. PII-15's 2:1 reeving was "the only lever found that shortens the machine"; the margin does it for free and **without a cable over a sheave**, which `REV-07` records cannot claim the exemption that screened out the rack. |
| **SYN-03** | **And together they close kill criterion 2** | Brake run-out **240 → 105 mm**. Closed envelope **1839 → 1254 mm** at Gen5's own exit velocity — **inside ESPA-Grande's ~1270 mm**, with 3.9 g of qualification margin still unspent. That criterion has been crossed or unevaluable since the envelope was first drawn, and **ADR-023's re-scope could be reversed on evidence** rather than defended. |
| SYN-04 | **Mass, as a labelled sketch** | Scaling `mass_properties.py`'s own lumps to an 850 mm machine with a 0.6 kg shuttle, **plus** 3 kg of LIM stator iron: dry **76.5 → 59.6 kg**, per 3U satellite **6.378 → 4.967 kg**. **Kill criterion 1 still does not close at 3U** and no version of this architecture makes it — but at PocketQube 1P it is **0.207 kg, passing by 10×**, and those classes are reachable because the satellite is unmodified. |
| SYN-05 | **What the combination does not touch** | **E4** — nothing measured. **P52** — the 30 % segment-handover ripple is topology-level and applies to every variant. **P36** — a shorter, stiffer track has different modes, so that analysis is redone rather than inherited. |

**What authorised it.** Phase II analysis, recorded as interactions rather than promotions:
`VAULT.md`'s gate is untouched and **no item's status was changed**. **Nothing in Gen5 moved.**
All four checks pass.

---

## 2026-08-13 (twenty-eighth pass): the plate drive, tested where it could have died

| ID | Item | Detail |
|---|---|---|
| **A31** | **The plate centres itself, with no bearing** | Layered-media solve, Maxwell stress on planes either side of the plate. **The transverse force is restoring at every offset inside ±1 mm** — the nearer stator induces the larger eddy current and eddy forces are repulsive. **0.1 % of thrust** against a 20 % band. Thrust is blind to alignment: **0.10 %** over half a millimetre of gap error, **1.69 %** over three laterally. This keeps **E21**'s fretting and cold-welding problem — what screened out the screw drive in A27 — out of the architecture entirely. |
| **P50** | **And A30's thrust figure was 4.4× optimistic** | A30 reported **1652 N at 0.45 T** by taking the magnetic-pressure ceiling **B²/2μ₀** and applying the edge factor. The layered solve gives **378 N**: the ceiling is the zero-gap limit and a 7 mm magnetic gap falls far short of it. **The error was treating a bound as an estimate.** Corrected in place; A30 band 4's edge factor of 0.6691 is a separate measurement and stands. |
| A31-01 | **The architecture still closes, at a higher flux density** | Design sweep, kept separate from the bands: **900 N, 21.6 g, 23.48 m/s** at 0.75 T inside the qualification cap, or a conservative **671 N, 16.1 g, 20.26 m/s** at 0.60 T — both on the same **0.248 kg** plate, against Gen5's 16.39 m/s from a 9.445 kg sled. |
| **A32** | **Entry is a non-event** | Time-domain thin-sheet solve, a different model from A31 on purpose. Plate diffusion time **3.198 ms**; thrust reaches 90 % after **0.679 mm** of travel — **0.05 %** of the acceleration zone. The concern that motivated the sheet does not survive contact with the time constant. |
| A32-01 | **And the thrust figure is no longer single-sourced** | Band 1: the time-domain solver agrees with A31's frequency-domain layered solve to **−9.0 %**. Different domain, different implementation, same answer. |
| **P52** | **The segmented stator puts a 30 % force ripple through the track's first mode** | Band 4: **30.1 %** peak-to-peak at a segment boundary against a 20 % band, and **closing the joint gap to zero leaves 25 %** — so it is the longitudinal **truncation** of the travelling field at the edge of an energised section, not the joint. The segment-crossing frequency sweeps **0 → 61.5 Hz** and the track modes are at **48 and 109 Hz**. **A17's chirp problem in a new place**, against a track **P36** says has no dynamic design case. First defect in three sheets that is in the machine rather than in an analysis. |
| P51 | **And one band asked the wrong question** | Band 3 required the transient transverse force not to exceed its steady-state value; it peaks at **2.73×** — but **restoring throughout**, and the absolute peak is ~2.25 N against 611 N of thrust. **A stability band must be on the excursion or the absolute force, never on the ratio to the steady state it is overshooting.** As written it fails on a harmless over-restoring transient and would have passed a destabilising force that was smaller than its own steady state. Band left as declared. |
| **PROC-01** | **Three new solvers, three first runs wrong, three caught by their own verification bands** | A30 returned **exactly zero** for every geometry (travelling wave written as a real cosine). A31 returned **705 % of physics** (single-sided model; flux normalised on the screened field). A32 returned **+304 %** against A31 (thrust as K × B_imposed rather than K × B_total). **Every one would have been published as a result.** In all three the band that caught it was the *verification* band — the one that adds no new physics and is the easiest to leave out. |

**What authorised it.** Two validation outcomes against bands declared before their scripts
existed, verified by `git show --stat` returning nothing at each band commit. **Nothing in Gen5
moved** — no band edited, no operating point, no baseline. All four checks pass.

---

## 2026-08-13 (twenty-seventh pass): the interface has been on every CubeSat since 2003

| ID | Item | Detail |
|---|---|---|
| **PII-16** | **Gen6 proposal: the satellite's own CDS corner rails as the motor secondary** | The CubeSat Design Specification has mandated four hard-anodised aluminium corner rails since 2003. Every deployer built since — P-POD, NRCSD, this project's own cassette — treats them as a **bearing surface**. They are also **116 cm² of standardised, structural, conductive, axially symmetric induction-motor armature that every customer already owns and already qualifies.** Nobody has driven on them. |
| A30-00 | **Sizing, and it clears the requirement** | `analysis/rail_drive.py`, goodness-factor sheet secondary, double-sided stators straddling each rail, holding G·s = 1. At a modest **0.45 T**, a realistic **2 mm** clearance and the **worse** of the two rail alloys: **513 N, 13.1 g, 18.26 m/s in 142 ms on 1182 J** — faster than Gen5 on **2.4× less energy**, because the moving mass is 4 kg instead of 13.45 kg. Rails warm **1.7 K**. |
| **PII-16-01** | **What stops existing rather than being solved** | No sled → no brake → no arrest section → no sled return → no cradle. That removes the source of **E34** (18.5 kN through eleven stowed satellites), **E24** (the attitude budget's dominant term), **P28**, **P41** and the 339 mm of envelope behind **kill criterion 2**. No permanent magnets anywhere removes **E33** and **E35**. |
| PII-16-02 | **And "unmodified" stops being a claim** | It becomes a property of the topology: nothing is attached, added or left behind. The contradiction between the abstract and **E35** dissolves rather than being qualified. |
| **PII-16-03** | **What would kill it, stated first** | The **transverse edge-effect derating is the whole result** — assumed at **0.55** and declared as an assumption at the top of the file. At 0.2 the design point falls to 187 N and the idea is dead. **A30 band 1 is a 3-D transient eddy-current solve**, and it is the cheapest possible way to find out. |
| PII-16-04 | **The tension that better engineering does not fix** | The drive works only on classes carrying CDS rails, and kill criterion 1 fails at 3U and closes only at PocketQube, which has a different rail standard. That is decision **D2**, unmade. |
| PII-17 | **The mover-departs family, considered and not recommended in its naive form** | A fin or keel carrying the Halbach array weighs **6.04 kg at the full array, 3.20 kg at 170 mm**, against a COTS cold-gas module at 0.5–1.2 kg for the same Δv — so VOLLEY would compete with cold gas on its own ground and lose 3–6×, forfeiting kill criterion 1's only escape clause. Recoil rises 74 %. **What the idea is right about** is that dropping "unmodified" re-opens the topology trade; taken to its conclusion that is PII-16. |

**What authorised it.** Phase II is where candidate architectures are recorded with entry
criteria, not adopted. **Nothing in Gen5 moved** — no band, no operating point, no baseline.
All four checks pass.

---

## 2026-08-13 (twenty-sixth pass): no LaTeX in the engineering record

| ID | Item | Detail |
|---|---|---|
| **ADR-028** | **The flagship holds no LaTeX, no `.cls`, and no compiled PDF** | `paper.tex`, `IEEEtran.cls`, the built PDF, `archive/` and `cv/` are now **authored** in `VOLLEY-paper`; the thesis carries its own copy in `source/`. A `.tex` file is not a derived artefact — it is written, submitted, reviewed and revised, and it acquires a copyright status the flagship cannot license, which is why `PAPER_MANIFEST` already carried a deliberate licence hold. |
| MOVE-01 | **`paper/figures/` → `figures/`; the generators → `tools/`** | A figure is a **result**: drawn from `analysis/`, indexed by `docs/FIGURE_INDEX.md`. It belongs in the engineering record whether or not a paper cites it. `tools/make_figures.py` and `tools/make_animation.py` regenerate at the new location and were re-run to prove it. |
| **MOVE-02** | **`export_companion.py` no longer wipes the companion** | It called `shutil.rmtree(dest)` and now removes only the paths in its own manifest. **Run unchanged after this move, it would have deleted the paper.** ADR-017's "delete and regenerate" rule now applies to the manifest paths only, and the ADR says so. |
| MOVE-03 | **What the flagship stops having to carry** | `check_artifacts.py` loses the two pairs it could verify only by page count. `env-setup.sh`'s LaTeX dependency now exists for nothing in this repository. |
| **FRONT-01** | **The front page leads with results, and shows the ones that were missing** | README gains a **Results** section: the shot, lifetime, **both A28 control figures**, the **full A29 CFD report** and the air-drag result, each captioned with what it shows and what it cost. Opens by stating that every image is a script output and pointing at the figure index. |
| FRONT-02 | **`docs/index.html` gains two sections** | *Control stability, and a gain that was never designed* and *CFD: what air costs a ground test* — the second showing the convergence history and the surface-pressure distribution, not only the answer. |
| FRONT-03 | **Historical paths are not rewritten** | `CHANGELOG.md` and `OPEN_PROBLEMS.md` describe edits made to `paper/paper.tex` on dates when that path existed. They are the audit record; the paths in them are historical facts, not links. |

**What authorised it.** A structural decision by the sole author, recorded as ADR-028. **No
script value, no band and no operating point moved** — all four checks pass unchanged.

---

## 2026-08-13 (twenty-fifth pass): the machine flies in vacuum, the test happens in a room

| ID | Item | Detail |
|---|---|---|
| **A29** | **What air costs a ground test, computed for the first time** | Every velocity in this repository is computed with no aerodynamic term. The TRL-5 step fires a mass simulator down a full 1.5 m track **at sea level**, and nothing said what the air was worth. Steady RANS (`simpleFoam`, k-ω SST) on the **Gen5 sled and payload as generated**, meshed by `snappyHexMesh` from `cad/stl` — not an idealised box. |
| **A29-01** | **The answer, and why it is the comparison that matters** | C_d **0.523** on a 201.6 cm² projected frontal area at Re 7.0 × 10⁵ → **1.734 N** at exit velocity → **1.127 J** over the 1.30 m stroke → deficit **5.116 mm/s (0.0312 %)**. Small against the design point; **19.2 % of the 3σ dispersion the test exists to resolve.** No vacuum chamber needed; an air correction on every measured velocity is. |
| A29-02 | **Open loop and closed loop are different tests** | Open-loop the deficit is 5.1 mm/s of velocity; closed-loop the servo nulls it and it appears as **1.734 N of extra command, 0.125 % of the shot**. `QUALIFICATION_PLAN.md` does not currently say which the full-scale test is. |
| **A29-03** | **The solve does not converge, and that is reported** | Velocity residuals fall three orders then **plateau near 5 × 10⁻² and oscillate** — what a steady solver does on a massively separated wake. The drag is a **windowed mean, 1.734 ± 0.144 N (8.3 %)**. The first attempt read a single iteration, 1.946 N, **12 % high**. |
| A29-04 | **Two OpenFOAM function objects abort in this build, and the workaround is stronger than the tool** | `forceCoeffs` and `wallShearStress` both fail with an IOstream error before the first iteration. Pressure drag is integrated in `validation/cfd/forces.py` as **F = ρ Σ p S_f** directly from `constant/polyMesh` and the solved field, so every step from solve to coefficient is inspectable. Viscous drag is a **flat-plate bound**, 17.7 % of the total, labelled as one everywhere. |
| A29-05 | **The sign convention was inverted and produced a negative drag** | OpenFOAM boundary normals point out of the **fluid**, i.e. into the body, so the body's outward normal is −S_f and the force is +Σ p S_f. `forces.py` now **asserts** drag is positive: a bluff body in a uniform stream does not produce thrust. |
| **P48** | **Two of five bands fail, and neither failure is in the machine** | **Band 2** (0.7 ≤ C_d ≤ 2.5) fails at 0.523 — the band was declared against a *solid* bluff body and the assembly is a **stepped** one, so part of the reference frontal area sits in the payload's own wake. Three checks say the solve is sound: peak C_p **0.975** where stagnation should approach 1; meshed wetted area **0.4173 of 0.5612 m²** of raw STL, the difference being the interior payload–sled interface; drag splitting as forward **+0.233**, base **+0.156**, sides **+0.001**. |
| P48-01 | **Band 5 fails in the opposite direction to the one predicted** | The stator plates were expected to **raise** C_d by ≥ 10 % through confinement. They **lower** it by **12.7 %** and tighten the spread from ±8.3 % to ±3.5 % — the plate acts as a **wake splitter**, not a wall. **The consequence is useful: the free-stream figure is the conservative one**, so the correction is quoted from it. |
| P48-02 | **What is corrected is the practice** | **A drag band must name its reference area and the shape it is being compared against**, because a drag coefficient without its reference area is not a number. Same class as A2 band 3, which passed while measuring numerical cancellation on a symmetry axis: **a band can be satisfiable and still be the wrong question.** No band edited, no result moved. |
| **PAPER-10** | **§VI-E added; the manuscript is 14 → 15 pages** | With `F14_airdrag.png`. Reports the plateau and the viscous bound in the body text rather than in a footnote. Zero undefined references. |
| FIG-07 | **The figure stamp now carries A29 too** | `BUILD.json` gained the drag and the deficit, because F14 is drawn from them and a stamp that cannot see a figure's source cannot police it. |
| **INDEX-01** | **`docs/FIGURE_INDEX.md`** — every figure with its generator, its source, and its class of evidence | Five classes, and the count that matters is that **class D — something physically observed — has zero members.** Records the Gen4 render mismatch where the renders appear rather than only in the register. |
| CNT-15 | **Register 82 → 83, 12 → 13 corrected** | P48. Header propagated. Live count unchanged at 38. |

**What authorised it.** A validation outcome against bands declared before the case directory
existed, verified by `git show --stat 949fdf4 -- validation/cfd` returning nothing. **Two bands
failed and produced a numbered defect, not a widened band.** All four checks pass.

---

## 2026-08-13 (twenty-fourth pass): the velocity loop was never designed, and the 3-D solve lands

| ID | Item | Detail |
|---|---|---|
| **A2-04** | **Band 4 runs and E2 closes** | A `getdp` 3-D magnetostatic solve — reduced scalar potential, **274,105 DoF** on a **315,370-node** tetrahedral mesh, geometry imported from `motor_model` — agrees with magpylib on the double-sided midgap fundamental to **0.059 %** (0.70182 T against 0.70140 T). Band was ≤ 5 %. Both of the two named references agree to better than a tenth of a percent, so the result does not turn on which the band picked. |
| A2-05 | **The first solve of it returned exactly zero and reported success** | Residual 150.2 → 4 × 10⁻¹³, clean log, **zero field at every sampled point**. `gmsh.model.getBoundary()` on the air volume returns the six outer faces *and* all twenty-four magnet–air interfaces; tagging them all as the outer boundary pinned φ = 0 on every magnet surface and the source-free air then gave φ ≡ 0 by uniqueness. Caught by checking the value against physical expectation, not by any tool. The fix selects faces by bounding box and **asserts exactly six are found**. |
| A2-06 | **Periodic endpoint dropped before projection** | `getdp`'s `OnLine` includes both ends; x = ±λ/2 are the same point of a periodic field, so keeping both weighted one phase twice. Moves the result 0.084 % → **0.059 %**. |
| **P47** | **The published velocity-loop gain is linearly unstable** | A28, bands declared at `3ae36ad` before the script existed. **Four of six bands fail.** The controller is feedback-linearised, so `L(s) = Kp/s·exp(−sτ)` and **Kp is the crossover in rad/s, not a current gain** — a fact stated nowhere. 3500 s⁻¹ is a crossover at **557 Hz**, above both track modes, with **−50.4°** phase margin and **−3.86 dB** gain margin at 0.7 ms of total lag. |
| P47-01 | **Why it was invisible** | `closed_loop_mc` feeds back the **undelayed** state, so its own loop sits at zero latency where 3500 does hold +69.9°. And the command is clipped to `[0, K_RATED]`, turning an unstable loop into a **bang-bang relay** whose mean follows the feedforward term, with the terminal ±0.3 m/s trim removing the residual. **The dispersion figure was set by the saturation limits and the terminal correction, not by the feedback.** |
| **P47-02** | **Corrected: `motor_model.KP_VELOCITY = 195` s⁻¹** | `design_gain()` returns 195.2 s⁻¹ as the largest gain holding ≥ 50° phase margin at 0.6 ms **and** bandwidth ≤ one third of the 109 Hz first mode; implemented value rounded **down**. Result: PM **+82.2°**, GM **+21.2 dB**, bandwidth **36.3 Hz**, **0.0 %** of stroke above rating. |
| **BASE-05** | **Baseline: dispersion 0.0271 → 0.0267 m/s** | Change-control rules 1 and 2. **The gain falls 18× and the dispersion does not move** — both are 0.027 to two significant figures — because dispersion is set by the terminal trim and the K_t and mass tolerances, not by loop gain. **K_t stays 11.0258 N/kA·m, v_exit stays 16.388 m/s.** **Validations invalidated: none**; nothing else reads `closed_loop_mc`. |
| ADR-027 | **The loop is designed against a named constraint set** | Phase margin ≥ 50°, bandwidth ≤ f_mode/3, command within rating. Alternatives recorded and rejected: keep 3500 and declare zero latency; raise the controller rate; notch at 109 Hz (deferred to Phase II — a notch commits to a mode frequency `STRUCTURAL_GAP.md` says is unmeasured); design to the 45° band exactly. |
| FIG-06 | **Two figures added, both generated** | `F12_bode.png` — open-loop Bode at both gains with the 48–109 Hz mode band shaded and both crossovers marked. `F13_latency.png` — phase margin against transport delay, with the stability floor. Both import `analysis/control_design.py`; nothing re-derived in the figure script. |
| CNT-14 | **Register 81 → 82, 11 → 12 corrected** | P47. Header propagated. Live count unchanged at 38. |
| **PAPER-09** | **§IV-D *Velocity-Loop Stability* added; the manuscript is 13 → 14 pages** | States the fact the repository had never written down — the loop is feedback-linearised, so Kp is the crossover in rad/s — reports the earlier gain as what it was, and gives the designed gain with its margins. **No other body text moved**: the 0.027 m/s in the abstract, §V-A, §V-E, §VIII and the conclusion is 0.027 to two significant figures before and after. Zero undefined references. |
| PAGES-02 | **`docs/index.html` carries the margins and the correction** | Dispersion row to 0.0267 m/s, plus a velocity-loop-margins row naming P47 and the superseded gain. The public page is an artifact of the results under the P42 rule, so it moves with them. |
| **STATE-01** | **`docs/STATE_OF_THE_PROJECT.md`** — the disposition layer the repository did not have | Four sections: **ten decisions nobody has taken**, every live weakness grouped by *kind* rather than by number, the crossed thresholds and **the seven places a published claim contradicts the project's own evidence**, and a four-tier fix list. Adds no evidence: every figure is carried from a file that already holds it. |
| STATE-02 | **The decisions layer is genuinely new** | `OPEN_PROBLEMS.md` holds defects, `KILL_CRITERIA.md` holds thresholds, `VAULT.md` holds deferred work — **none of them holds a decision only the author can take.** B-1 unordered, the payload class unchosen, P46 held, the provisional's 2027 date, the bank, the envelope, the wiki, Gen4. |
| **STATE-03** | **And it names the most reviewable weakness as a writing problem** | Every contradiction in the table is disclosed *somewhere* — but several only in a limitations section while the abstract states the unqualified version. **Three of the seven close with an editing pass and no new analysis.** |
| **STAMP-01** | **Three build stamps could not see this change, and now can** | `paper/figures/BUILD.json`, `BUILD_anim.json` and the generated `cv.tex` each recorded a hand-picked subset of the operating point. **The velocity-loop gain changed, F03 was redrawn, and every field in all three stayed identical** — the exact blind spot the stamps exist to close. Each now also carries the sha256[:16] of `motor_results.json`, so any change to the results moves the stamp. |

**What authorised it.** Two validation outcomes against bands declared before their scripts
existed. **A2 band 4 passed; A28 bands 2, 3, 4 and 5 failed and produced a numbered defect, not a
widened band.** All four checks pass.

---

## 2026-08-10 (twenty-third pass): CC BY 4.0 across the repository, and the front matter raised

| ID | Item | Detail |
|---|---|---|
| **LIC-01** | **The whole repository is relicensed CC BY 4.0**, single licence at root | A code/documents split placing Apache-2.0 on `analysis/` and `tools/` was considered and **rejected**. This repository does not separate cleanly: `validation/` holds fourteen Python files beside its run sheets, `cad/` holds the generator that produces the geometry, `paper/` holds figure generators — and **`analysis/` is not incidental tooling**. `motor_model.py` computes the thrust constant and `sizing.py` sets the geometry, so that code **is the design expressed executably**. A carve-out would have drawn a line through the middle of one disclosure. |
| LIC-02 | **The licence text is canonical, not reproduced from memory** | CC BY 4.0 legal code taken from the SPDX `license-list-data` source, all eight sections verified before installing. `creativecommons.org` is blocked by the network egress proxy, and writing legal text from memory was declined. |
| LIC-03 | **Not retroactive, stated in three places** | `LICENSING.md`, the README licence section, and `NOTICE`. The previous MIT text is retained at `LICENSE-MIT-superseded`; every snapshot taken before this change stays available under it and nothing revokes rights already granted. |
| LIC-04 | **`paper/` marked as a separate case** | The reproducibility package is CC BY 4.0; the manuscript is CC BY 4.0 **provisionally**, because **an IEEE copyright transfer on acceptance would supersede this licence for the accepted version.** The repository cannot license rights it has transferred. |
| **LIC-05** | **The companion export is deliberately held** | The manifest now carries `LICENSE`, `NOTICE`, `LICENSING.md`, `LICENSE-MIT-superseded` and `CITATION.cff`, so one export run would relicense both companions. **That run is held pending the IEEE decision**, so `VOLLEY-paper` and `VOLLEY-thesis` remain MIT while this repository is CC BY 4.0. **Intentional divergence, recorded rather than left to be found as drift.** |
| LIC-06 | **Sibling repositories relicensed, and two of them not as first planned** | `VOLLEY-lab`, `pulsed-linear-motor-design-lab` and `orbital-deployment-trade-study` → **CC BY 4.0**; `engineering-evidence-toolkit` → **Apache-2.0**. The two design-lab repositories were originally assigned Apache-2.0 and reassigned on inspection: **both carry `reference/volley/motor_model.py`**, so a patent-granting licence there would have defeated the reason for the split. |
| **RANK-01** | **`OPEN_PROBLEMS.md` opens with a lethality ranking, confirmed** | Live entries ordered by how likely each is to be **design-fatal**, which is a different question from the HIGH/MEDIUM/LOW severities already carried — those rank how wrong a published number is. Top five: **E30, E4, E33, E34, E35**. **Nothing deleted, renumbered or reworded.** It disagrees with the register's own labels in two places and says so. |
| README-01 | **The front matter leads with the design point** | Design point, mass and energy budget, TRL, and the spring comparison on the first screen; background below. The comparison table carries **losses in the same table as the wins** — TRL 9 against 2–3, and **nine of thirteen single-failure elements against zero** — under a framing line naming the axis where a spring does not compete at any price. |
| DOC-01 | **Three superseded ripple figures annotated, none edited** | The ±1.26 % records in `CROSS_INDUSTRY.md`, `A1_field_femm.md` and `VALIDATION_REPORT.md` are pre-quadrature. Current value **±0.99 % (0.9874 unrounded)** from `motor_model.py`, with identical wording in all three and a matching entry in `PROVENANCE.md`. |
| DOC-02 | **Smaller corrections** | `CITATION.cff` v0.1.0 → **v1.1** with that tag's commit date and `license: CC-BY-4.0`; **cogging *torque* → cogging *force*** in ADR-004, a linear machine having no torque; SUMMARY's validation count corrected from "nineteen of twenty-one" to twenty-four run sheets. |

**What authorised it.** A licensing decision by the sole copyright holder, plus documentation
work. **No script, CAD file, result, or manuscript body changed** —
`git diff main repo-altitude -- analysis/ cad/ paper/paper.tex` is empty, and all four checks
pass unchanged.

---

## 2026-08-10 (twenty-second pass): propagating the correction I logged and then left in the register

| ID | Item | Detail |
|---|---|---|
| **E30-04** | **The delivered-life correction was logged and never propagated** | E30-02 established on 2026-08-10 that the headline **7.52×** is a ratio of *gains*, and that on **delivered orbital life** it is **1.495×**. That correction went into the register and `REVIEW_RESPONSES.md` and **nowhere else** — `SUMMARY.md`, `docs/index.html`, `docs/LANDSCAPE.md` and `paper/README.md` all continued to publish the flattering half alone. **This is the P42 defect class**: a known correction sitting in the register while the public pages say something different. |
| E30-05 | **Fixed on all four surfaces, without touching a band** | **7.52× is not wrong** — A21 band 1 was declared before its run and passed. The fix is to carry **1.495×** alongside it, not to delete it, which would be editing a passed band's result. A **forward note** was added to `A21_comparators.md` that alters nothing below it, following the precedent set when A1's sheet was left as written and its correction placed elsewhere. |
| E30-06 | **And the paper is flagged rather than quietly fixed** | `paper.tex` still carries **7.5×** in the abstract with no delivered-life figure. `paper/README.md` now records that explicitly: **the compiled PDF currently quotes the flattering half alone**, outstanding for the next build. |

**What authorised it.** Propagation of an existing register entry. **No band edited, no operating
point moved**, and `make_baseline.py --check` still passes 23 of 23.

---

## 2026-08-10 (twenty-first pass): the last five review items, and the field exposure turns out to be optional

| ID | Item | Detail |
|---|---|---|
| **E35** | **The payload's field exposure is a design variable nobody varied** | Review item 16. The payload rides **on** the sled, 20 mm from the magnets, at **442× magnetometer full scale**. At **251 mm it is usable (0.90×)**; at **400 mm the satellite sees less than Earth's own field**. The 251 mm crossing reproduces `PAYLOAD_ENVIRONMENT`'s own figure, which is the cross-check. |
| **E35-01** | **And it reframes item 14 rather than optimising it** | Item 9 established the satellite **is** modified — magnetically, invisibly, without the customer's knowledge. That makes today's configuration the **worst** of three options, being the only one where the modification is undisclosed. **Separation is what makes the "never modified" claim true**, not what makes it faster. |
| **PII-15** | **An LSM tug reeved to a separate carriage** | Review item 15, and distinct from PII-14: the motor **stays**, only the coupling changes. **2:1 reeving halves the acceleration zone — 1.30 m to 0.65 m — for 4 % of exit velocity**, because the tug's 9.445 kg is divided by *n²*. **The only lever found that shortens the machine without lengthening anything else**, against P9's 44 % overrun — and it delivers E35's separation for free. |
| REV-07 | **Item 19 gated, and A27 makes it sharper** | A cable over a sheave **is** a contacting drive at speed, so it **cannot claim the exemption that screened out the rack** in A27. It must answer the same E21 objection: fretting, cold welding, lubricant with no outgassing budget, sheave bearing life, and a single tension load path that becomes another manifest-forfeiting element. |
| **REV-08** | **Item 5 answered as far as it can be: no customer exists** | And this review's strongest findings **narrow** the addressable set — A24 (threat 1 closes only at PocketQube), A21 (cold gas wins 7.5× at 3U), A27 (a ~2 kg spring suffices without continuous control), E30 (the case needs 93.5 % per-shot reliability, unmeasured). **The product the evidence supports is one sentence: continuous per-shot velocity control, to an operator distributing a fleet from one release event, who values schedulability over mass.** First time the repository has been able to state it. |
| REV-09 | **Review register closed out** | **20 answered, 14 partial or scoped, 1 open.** From 11/10/14 at triage. The one still open is item 5, and **no analysis substitutes for asking an operator.** |
| CNT-13 | **Register 80 → 81, 37 → 38 live** | E35. Header propagated. |

**What authorised it.** E35 is unmodelled engineering raised in external review; PII-15 is a
candidate architecture recorded in Phase II, not adopted. **No operating point moved.**

**Eight register entries came out of this review — E29 through E35 and P45.** More than the review
found wrong, which is the argument for having asked.

---

## 2026-08-10 (twentieth pass): the magnets torque the host while idle, and the brake shakes eleven stowed satellites

| ID | Item | Detail |
|---|---|---|
| **E33** | **Magnet tolerance leaves a residual dipole that saturates the host's wheel in days, with the machine idle** | Review item 11. **An ideal Halbach cancels exactly — 3.5 × 10⁻¹⁴ A·m² over seven whole wavelengths.** Tolerance does not: at ±2 % Br and ±2° axis over 56 blocks, the residual is **0.77 A·m² median, 1.92 at the 99th percentile** — at or above typical small-spacecraft magnetic cleanliness allocations. |
| E33-01 | **And it needs no shot to do damage** | In a 30 µT field that is 2.3–5.8 × 10⁻⁵ N·m, **saturating a 15 N·m·s wheel in 3.0–7.5 days**. **Three independent paths now reach the same failure**: E29 (shot impulse, ~shot four), E33 (dipole, 3–7.5 days idle), and E31 (once attitude authority is gone, deployments are **not compliant**). Against E28's 29–36 day window and E31's seven-day hold, **the magnets alone can exhaust the wheel before the campaign ends.** |
| E33-02 | **The fix is manufacturing, not design** | **Magnet screening and matched-set assembly** — measure each block on receipt, sort, place to cancel. **B-1 already buys a teslameter and eight blocks**, so the method could be demonstrated on the bench article at no extra hardware cost. Not specified anywhere. |
| **E34** | **The brake dumps 18.5 kN into a structure holding eleven stowed satellites** | Review item 12. **Release is benign** — A23 puts it 12.2 ms into coast at **zero commanded force**. Brake arrest is not: the sled enters at **14.07 m/s carrying 935 J**, and at the `arrest_g_cap: 200` design cap that is **18.5 kN through the track in 7.2 ms**, with **eleven satellites still in the cassettes**. |
| E34-01 | **And it is outside every qualification case the payload has** | A stowed 3U is qualified to the **25 g CDS cap and launch random vibration** — not a 200 g mechanical shock through its own dispenser, **repeated eleven times**. `grep -ri "shock spectrum"` returns nothing. Lowering the cap to 50 g costs **202 mm of run-out** the envelope may not have (P9). |
| REV-05 | **Items 10 and 25 scoped, not answered** | Both are **qualification paths, not analyses**, and are recorded as such. **A27 made E21 worse**: the actuator trade screened out a rack *because* contacting drive in vacuum is unqualified, which only holds if the incumbent's own rollers, leadscrew and escapement are benign — never shown. `cad/BOM.md` carries **no outgassing spec at all**, and `QUALIFICATION_PLAN.md` does not mention radiation. |
| REV-06 | **The review register, re-tallied** | **17 answered, 13 partial or scoped, 5 open**, from 11/10/14 at triage. **Seven new register entries came out of this review — E29 through E34 and P45 — more than the review found wrong.** |
| CNT-12 | **Register 78 → 80, 35 → 37 live** | E33, E34. Header propagated. |

**What authorised it.** E33 and E34 are unmodelled engineering raised in external review. **No
operating point moved.**

---

## 2026-08-10 (nineteenth pass): the actuator trade nobody had made, and it narrows the case

| ID | Item | Detail |
|---|---|---|
| **A27** | **Why a linear motor rather than a screw, rack or spring — criteria declared at `9857b3c` before the script** | Review item 18. **The repository had no recorded answer**: `DECISION_LOG.md` records the eddy brake and the ironless stator, never the choice of linear motor over every other way of pushing a satellite. |
| A27-01 | **The ball screw is disqualified by kinematics, twice over** | 16.388 m/s on a 20 mm lead needs **49,164 rpm**. **DN = 1.23 × 10⁶ against a 1.5 × 10⁵ ceiling, 8.2× over**; **whirling critical speed 1,333 rpm, 37× under**. The two limits worsen in opposite directions — a fatter screw raises critical speed and worsens DN — so no geometry closes it. |
| A27-02 | **The rack fails on vacuum contact, not on speed** | Pitch-line velocity **is** 16.4 m/s against ~10 m/s practice (1.64× over), and torque is a comfortable 69.4 N·m. **C4 screens it**: a contacting drive at full speed makes **E21**'s open tribology gap the load path rather than an incidental. |
| **A27-03** | **The spring works, and that is the finding** | **537 J, 826 N peak, 21.1 g — inside the 25 g cap — from about 1.8 kg of spring steel.** No sled, no stator, no bank, no converter, no sequencer, and therefore almost none of the nine manifest-forfeiting elements in `docs/FMEA.md`. **It fails on exactly one criterion: C3, commandability.** And on C5, storing 537 J at rest. |
| **A27-04** | **What that costs the argument** | **The linear motor is not chosen for performance; it is chosen for commandability, and that is the whole of the case.** Against a screw the choice is forced, against a rack well-founded, against a spring it rests on one criterion. **A four-stage spring giving four discrete velocities at ~2 kg is a real competitor** for any mission not needing continuous control, and no document here had acknowledged it. |
| A27-05 | **A detail worth keeping** | A linear spring's force **peaks at release and falls to zero**, so its peak is twice its mean — **21.1 g against the motor's flat 10.5 g**. Inside the cap, with far less margin, which is why staging exists. |

**What authorised it.** A trade study with screening criteria declared before the script, answering
an external review item. **No operating point moved.** The outcome narrows the product argument and
is recorded that way.

---

## 2026-08-10 (eighteenth pass): segmentation is real redundancy except at the breech, and neither breakdown mechanism is credible

| ID | Item | Detail |
|---|---|---|
| **SEG-01** | **The segmented stator is genuine redundancy, and it was only ever an assertion** | `analysis/segment_redundancy.py`. A dead segment is a length the sled **coasts over**, not a stopped machine: at four segments a later failure still exits at **14.19 m/s — 86.6 % of nominal, and 1.41× a spring**. At twelve segments, 95.8 %. |
| **SEG-02** | **Except at the breech, and that asymmetry is the finding** | **There is no force on a stationary sled**, so if the *first* segment dies the shot never starts. **The stator is two elements, not one** — three of four stator failures are survivable at four segments, eleven of twelve at twelve. `docs/FMEA.md`'s count of nine manifest-forfeiting elements becomes **eight and a fraction**. |
| SEG-03 | **And it names a cheap design action** | Duplicate or overlap the **breech segment**, or provide any independent means of starting the sled. That converts the winding's last manifest-forfeiting mode into a degradation. |
| **PAS-01** | **Review item 26 answered: neither mechanism is credible in normal use** | The 96 V bus is **3.41× below air's 327 V Paschen minimum**, and below a gas's minimum nothing breaks down at **any** pd. Multipaction is the wrong regime by **2.5 × 10⁴** — f × d = 40 Hz·m against ~10⁶ Hz·m. Both results are **geometry-independent**, which is why this is arithmetic. |
| **E32** | **The fault case is not safe, and nothing inhibits it** | The winding stores **1.37 J per phase** at 19.70 µH and 373.2 A. An **unclamped** interruption induces **7,351 V in 1 µs** and 735 V in 10 µs, against a 327 V minimum — and for a 1 mm gap air reaches that minimum at **760 Pa**, which the vehicle transits on **every ascent**. **No requirement anywhere in this repository keeps the bank uncharged during ascent.** |
| PAS-02 | **CFD was installed, and deliberately not used** | The conclusion turns on the bus sitting below a gas constant, which no venting model changes; a depressurisation time constant is orifice flow, not a Navier–Stokes solve. **Using a CFD solver here would have been theatre**, and is recorded as declined rather than omitted. |
| CNT-11 | **Register 77 → 78, 34 → 35 live** | E32. Header propagated. E30 gains the segmentation result and stays LIVE — **r is still unmeasured**. |

**What authorised it.** SEG closes a mitigation `docs/FMEA.md` explicitly declined to credit
without analysis; E32 is unmodelled engineering raised in external review. **No operating point
moved.**

---

## 2026-08-10 (seventeenth pass): the launch interface permits it, and the FMEA turns E30 into a requirement

| ID | Item | Detail |
|---|---|---|
| **ICD-01** | **Review item 30 answered: the interface permits 16.388 m/s** | Rideshare Payload User's Guide **Version 10, September 2024, §3.3.2**, read in full: a 1.0 m/s cap exists and *"containerized deployments such as CubeSats may be deployed at a velocity greater than 1.0 m/s"*, with **no numeric ceiling anywhere in the document**. The question expected to be lethal is not. `docs/ICD_COMPLIANCE.md`. |
| **E31** | **The same document found three worse problems** | **(1)** Deployments must be under **active attitude control** and are *"not allowed"* while tumbling — and **E29 puts wheel saturation at about shot four of twelve**, so the remainder are non-compliant, not merely degraded. **(2)** A **seven-day hold** on secondary deployments, which applies to the hosted ConOps ADR-024 adopted and costs **20–24 %** of the 29–36 day campaign window E28 measured. **(3)** An **exit-direction requirement** (+X face) that a radially-mounted deployer may not satisfy. |
| ICD-02 | **Numbers to adopt, not previously in any analysis** | **10 g axial / 17 g lateral (RSS)** quasi-static for a CubeSat dispenser — **lateral is larger**, and the structural work in A18/A22 is random-vibration and axial-dominated. Launch vehicle rates before separation: **±2.0 °/s roll, ±1.0 °/s pitch and yaw**. |
| ICD-03 | **A qualification gap that is paperwork, not physics** | NRCSD-E reportedly requires CubeSats to withstand **0.5–2.5 m/s** at ejection *(second-hand, not read in the primary document, and flagged as such)*. VOLLEY is **6.6×** that. Physically irrelevant — satellites are damaged by acceleration, not velocity, and 10.53 g sits inside the 25 g CDS cap — but a customer qualified "per NRCSD-E" has **no qualification basis** for 16.4 m/s. |
| **FMEA-01** | **Nine of thirteen elements forfeit the remaining manifest on a single failure** | Against **zero** for a spring dispenser. **Nine shared elements over twelve cycles is 108 chances to fail.** `docs/FMEA.md`, `analysis/fmea.py`. **This answers review item 22 structurally**: a jammed sled is not a special case, it is one of nine. |
| **FMEA-02** | **E30 becomes a requirement instead of a criticism** | To beat a 0.99-reliable spring **on delivered orbital life**, each element needs **r ≥ 0.99326 per cycle** — surviving the campaign with probability 0.922. **The first quantitative reliability requirement this project has had.** |
| FMEA-03 | **And a claim the project should stop making** | Matching a spring **on satellite count** needs **r ≥ 0.99984**, which is not realistic for a twelve-cycle electromechanical system with no flight heritage. **VOLLEY should not be sold on satellite count**; the defensible claim is fewer satellites and more total mission value, above r ≈ 0.9933. |
| FMEA-04 | **Two mitigations exist and are deliberately not credited** | The winding is **segmented** (P29 closed the modelling half) so losing a segment should degrade rather than stop — **never analysed as redundancy**, and crediting it without analysis would be the optimism this file exists to avoid. Gates are **per-cassette**, already in the model's structure. |
| CNT-10 | **Register 76 → 77, 33 → 34 live** | E31. Header propagated. E30 stays LIVE: **r is unmeasured**, and cycle-life testing is metal, not computation. |

**What authorised it.** `ICD_COMPLIANCE.md` is a document review and declares no band, which it
says of itself; `FMEA.md` sweeps reliability as a parameter rather than asserting one. **No
operating point moved.**

---

## 2026-08-10 (sixteenth pass): a reviewer's register, and the reliability arithmetic it forces

| ID | Item | Detail |
|---|---|---|
| **REV-01** | **`docs/REVIEW_RESPONSES.md`** | Thirty-five reviewer questions, answered or conceded. **11 answered, 10 partial, 14 with no answer in this repository at all.** Each answer cites the analysis behind it or says "open" and names what would close it. |
| REV-02 | **Three answers are losses, stated plainly** | A cold-gas module beats VOLLEY at 3U by **7.5×** (A21 band 5, declared as a loss *before* the run); the satellite **leaves permanently magnetised** by remanent magnetisation of soft-magnetic parts; and a payload's **magnetometer is unusable** inside the deployer at 611× full scale. All three predate the review and come from the project's own analyses. |
| REV-03 | **Two of the four judged potentially lethal have nothing behind them** | **Item 22** — a jammed sled forfeits the manifest, not one satellite; `grep -ri jam` returns zero. **Item 30** — no launch-vehicle ICD has ever been checked for whether it permits separation at 16 m/s, and if one caps near 1–2 m/s the central number is non-compliant by 8× regardless of the physics. **Item 30 is also the cheapest question here to answer.** |
| REV-04 | **A unit correction** | Review item 35 cites 18 kW. Peak is **32.5 kW** (96 V × 339 A); **16.1 kW** is the average over the 158.6 ms stroke. |
| **E30** | **The architecture trades twelve parallel one-shot mechanisms for one twelve-cycle series mechanism** | A spring dispenser fails one satellite at a time. VOLLEY's sled, stator, bank, sequencer and brake serve every shot, so a failure at shot *k* forfeits shots *k*–12. **Arithmetic, not opinion.** |
| E30-01 | **The risk/reward ratio, as two numbers** | Matching a 0.99-reliable spring **on satellites delivered** needs per-shot **p = 0.9985**; matching it **on delivered orbital life** needs **p = 0.9347**, because each delivered satellite is worth **1.495×** a spring-deployed one. **Break-even is p ≈ 0.935; below it the spring wins outright.** |
| **E30-02** | **A correction to the project's own headline** | The **7.52× lifetime extension** is a ratio of *gains* (+61.8 % against +8.2 %). On **delivered orbital life** it is **1.495×**. Both are true, but the second governs any risk-weighted comparison, and **7.5× flatters in exactly the comparison a reviewer makes.** |
| E30-03 | **And nothing estimates p** | No FMEA, no fault tree, no parts count, no cycle-life test for the escapement, gate or sled. **The project cannot say which side of 0.9347 it is on**, so it cannot presently claim to beat a spring at all. Two mitigations exist — segmented winding, per-cassette gates — and neither is credited, because there is no model to credit them in. |
| CNT-09 | **Register 75 → 76, 32 → 33 live** | E30. Header propagated. |

**What authorised it.** E30 is unmodelled engineering raised in external review.
`REVIEW_RESPONSES.md` is triage and claims no analysis. **No operating point moved and no band
was edited** — but E30-02 identifies a headline figure that overstates the case in the comparison
that matters, and that correction is now on the record.

---

## 2026-08-10 (fifteenth pass): the build-readiness position, stated subsystem by subsystem

| ID | Item | Detail |
|---|---|---|
| **BR-01** | **`docs/BUILD_READINESS.md`** | Nine subsystems, each with: is the design frozen, is the analysis complete, and — for everything unfinished — **whether the answer comes from more computation or from metal**. "TRL 2–3" is a label; this is information. |
| BR-02 | **It names the least finished subsystem rather than leaving it to be found** | **The brake.** Pole plates lightened from solid blocks on structural reasoning alone, **no magnetic sizing done**, and P28 opened by A11 in the act of adopting regen. Written as *"if one subsystem would embarrass this repository under review, it is this one."* |
| BR-03 | **The honest aggregate** | Four subsystems frozen and analysed; three frozen but under-analysed; one provisional; one a known negative with a candidate fix. **Most of what remains is computation, not metal** — which means the design is further along than the label suggests **and** that "everything computable is done" is **not yet true**. |
| BR-04 | **The claim the repository is entitled to make, written out** | Not "ready to build". Instead: specified to the level where a builder knows what to make, computed against bands declared first, 24 runs with two outright failures **all recorded rather than removed**, and the remaining uncertainty enumerated rather than estimated. |
| BR-05 | **README and SUMMARY lead with readiness** | Both now open on how far along the work is, not on the motor. `SUMMARY.md` gains a "How far along it actually is" section ahead of the discipline argument, and both carry **E4 and the unplaced ₹22,000 B-1 order** where a reader meets them rather than deep in the register. |
| BR-06 | **Three bands caught bugs in the analysis, surfaced as evidence** | A19, A20 and now A2 — most recently a **57 % normalisation error** that would otherwise have been reported as a plausible result. Promoted to the front door as the strongest available evidence the numbers were not fitted to the conclusion. |

**What authorised it.** Documentation of existing state. No operating point moved, no band edited,
no register entry changed.

---

## 2026-08-10 (fourteenth pass): the thrust constant is a centre-plane value, and it is 4.42 % high

| ID | Item | Detail |
|---|---|---|
| **A2** | **The 3-D field, bands declared at `964af2c` before the script** | The field was **never** 2-D — `build_field()` has always used magpylib cuboids with the real 90 mm depth. **The 2-D assumption is in the thrust integral**, which samples `B_y` on the plane z = 0 and multiplies by the full depth as though it held across all 90 mm. It falls off toward the array's z-edges. |
| **P46** | **Resolving the depth costs 4.42 % of K_t** | 11.0258 → **10.5386 N/kA·m**, ratio **0.9558** against a declared band of ≥ 0.95 — **passes by 0.008**. Propagated: **v_exit 16.388 → 16.029 m/s**, 10.53 → 10.07 g, 339 → 320 A. **The baseline is NOT changed**; a re-baseline is a change-control action with its own propagation pass, not something a validation does to itself. Computed, reproducible, and held. |
| A2-01 | **Band 1 caught a bug in the analysis, which is what band 1 was for** | The first run reported centre-plane K_t as **17.2954** against 11.0258 — a **56.9 %** reproduction error, from normalising by `45e3 * DEPTH` instead of `SLED_ACTIVE_LEN / LAM`. The 0.9558 ratio survived the fix because both sides carried the same error, **but that is luck, not method**. Third time a declared band has caught a bug in the analysis rather than the design (A19, A20, A2). |
| A2-02 | **Band 3 passes and is uninformative — the band was badly chosen** | Both sides come out at 10⁻²⁰–10⁻¹⁹ T, fourteen orders below Earth's field, because the probe sits on the array's **symmetry axis** where the net dipole cancels. It measures numerical cancellation, not field. **Left exactly as declared and not re-run**; recorded so the next sheet probes off-axis. |
| A2-03 | **Band 5 settles an assumption the model never stated** | A 7-wavelength array is within **0.01 %** of a 21-wavelength one at its centre, so seven wavelengths is effectively infinite. `build_field` has used `n_wave=7` throughout without justification. |
| A2-04 | **E1's 3-D half closes. E2 does not** | Band 4, an independent `getdp` 3-D FEM cross-check, **was not run**, so 10.5386 is still analytic superposition — exactly the *"neither solving a field equation"* E2 objects to. Stated as not-run rather than quietly dropped. `gmsh` 4.15.2 and `getdp` 3.2.0 are now installed and working, so the obstacle is work, not tooling. |
| CNT-08 | **Register 74 → 75, 31 → 32 live** | P46. Header propagated. |

**What authorised it.** A2 is a validation with bands declared before its script; P46 is a defect
in a model of the machine that changes what the hardware would do, which freeze rule 1 covers.
**No baseline value was changed** — `make_baseline.py --check` still passes 23 of 23 against the
published K_t and v_exit.

---

## 2026-08-10 (thirteenth pass): Gen5, generated from the parameters instead of drawn

| ID | Item | Detail |
|---|---|---|
| **ADR-026** | **The CAD is generated, not drawn** | `cad/build_gen5.py` reads `cad/parameters.json` and emits STEP and STL for all eight documents using CadQuery 2.8.0. **Nothing is drawn**, so the drift `parameters.json` warns about — *"user parameters are document-scoped and will silently drift across the nine documents"* — becomes structurally impossible. Matches ADR-015: derive, never paste. |
| GEN5-01 | **It resolves Gen4 rather than stacking on it** | Gen4 exists only in Fusion, has never been exported, and releases at s = 1200 mm where `analysis/` assumes 1500 (P39). Gen5 depends on no unexported document, so it closes the gap P43 had to publish around. **It does not open Gen4's export gate and does not supersede Gen4 as a design — it supersedes the method.** |
| GEN5-02 | **Byte-stable, and deliberately so** | Two consecutive builds are identical. The STEP header timestamp is normalised to a fixed epoch precisely so "the geometry changed" and "the clock changed" cannot be confused. |
| GEN5-03 | **Checked against its own source, and the check earned its place immediately** | `--check` reads **23 dimensions** back out of the built solids — envelope, stations, cassette, flange, payload, and the magnetic air gap — and compares them to the parameter file. It **failed three on its first run**: a longeron built to the roller-channel width (180) instead of the track's overall width (205); a gate pin extruded outboard because a CadQuery `XZ` workplane extrudes along −Y, reporting the cassette as 332 mm against 166; and a check that called the radiator standing proud of the top skin an error when `parameters.json` records it as intended. **Two geometry bugs and one bad check. None would have been visible in a render.** |
| GEN5-04 | **The output was held out of the repository until the check passed** | A `.gitignore` guard kept `cad/step/gen5/` uncommitted while `--check` failed, with its own removal condition written into the comment. Committing known-wrong geometry would have been the same defect class as P43. The guard is now lifted at 23 of 23. |
| GEN5-05 | **Guarded going forward** | `check_artifacts.py` ties the Gen5 STEP to `parameters.json` and `build_gen5.py`, so a dimension changed without a rebuild is caught. |
| GEN5-06 | **The limitation, stated rather than implied** | **Geometry and interface model, not a manufacturing model.** No fillets, chamfers, fasteners, harness routing or tolerancing. One value is derived rather than read — the Halbach array is given in assembly coordinates and centred on the 488 mm sled for the sled's own frame — and is flagged as an assumption in the docstring. |
| GEN5-07 | **CadQuery recorded as optional** | `requirements.txt` marks it CAD-only: nothing in `analysis/` and no number in the repository depends on it. |

**What authorised it.** ADR-026, and P39's own named next step. No operating point moved.

---

## 2026-08-10 (twelfth pass): a flywheel clears the ceiling the bank fails, and the shot's angular impulse turns out to be unmodelled

| ID | Item | Detail |
|---|---|---|
| **A25** | **A flywheel motor-generator against P26, bands declared at `d254759` before the script** | **Band 6 — the reason the analysis exists — passes decisively: 35 mΩ series resistance against A10's 68 mΩ ceiling, delivering 66 kW against 32.5 kW required.** P26 is a property of capacitors; a rotating machine is not subject to the mechanism. **It requires no architecture change** — the LSM, sled, track, cassettes and all of A1–A24 stand untouched. |
| A25-01 | **And it breaks the coupling that made P26 poisonous** | The bank's ESR ceiling *tightens* as velocity rises, which is why it inverted the ranking of every lever in `DESIGN_OPTIONS_exit_velocity.md`. A store with 66 kW against a 32.5 kW demand does not. |
| **P45** | **Band 4 failed by 1.1 kg: the flywheel is at mass parity, not a saving** | 20.61 kg against a 19.50 kg three-string bank. **Band not widened.** The miss is owned by one unsourced number — `MG_KG_PER_KW = 0.30`; at **0.25 it passes**, and against the four-string bank the same file calls "with margin" it wins by **5.4–10.3 kg** at every value tested. One datasheet decides it. |
| A25-02 | **A script bug found and fixed before the result was written** | The first run failed band 4 by **16.9 kg**: `system_mass()` doubled a full-size rotor *and* a full-power machine for the counter-rotating pair, sizing a store that holds and delivers twice what the shot needs. A pair **splits** the duty. Same class as the A20 apsides bug — model wrong, band untouched. |
| A25-03 | **Band 2 passing by 18.8× is itself informative** | The rotor is nowhere near a material limit, so the design is not energy-density-constrained. **The machine is the binding item** — which is where band 4 landed from the other side. |
| **E29** | **Nothing computes the shot's angular impulse about the host** | `astro.py` models the host interaction as one line, `4.0 * DV` — **linear only**. A13 covers indexing and sled return; the shot's own angular impulse is unmodelled. At a 50 mm CoM miss it is **3.28 N·m·s per shot, 39.3 over a campaign — 2.6× saturation of a 15 N·m·s ESPA-class wheel**, saturating around shot four. Bigger wheels and CMGs do not help: the constraint is momentum *storage*. |
| E29-01 | **The linear recoil is a non-problem, and should say so** | 0.393 m/s over a campaign on a 2000 kg spent stage, −1.4 km of orbit, and retrograde — the direction a stage wants for disposal. **No wheel can cancel it in any case**; linear momentum has three exits and none is a flywheel. |
| E29-02 | **No interface requirement exists that the thrust line pass through the host CoM** | ADR-010 specifies the mount host-agnostically. The cheapest fix by orders of magnitude attacks the moment *arm*, and it is currently nobody's requirement. |
| E29-03 | **One number drives three open problems** | `payload_com_offset_above_thrust_line = 70 mm` sets A23's tip-off, E29's angular impulse, and the 96 N transverse load that fixes the track's EI requirement — which scales as L³ and is what makes any longer track expensive. **Cradle geometry, not an architecture change.** |
| **PII-14** | **The cable-driven gondola, assessed and declined** | Recorded in `VOLLEY-lab` and registered here. The **+49.7 %** headline assumed **zero drivetrain inertia**; `m_eff = I/r²` adds directly to moving mass, a 34 kW machine at a 100 mm drum is 1–5 kg of it before drum or gearbox, and **at 7.4 kg the entire gain vanishes**. Honest range **+15 to +30 %**, against deleting the LSM and the 24 validations behind it. **Entry criterion: m_eff ≤ 2 kg, and a measured baseline.** |
| CNT-07 | **Register 72 → 74, 29 → 31 live** | P45, E29. Header propagated. |

**What authorised it.** A25 is a validation with bands declared before its script; P45 is a band
miss, which `validation/README.md` requires to become a numbered defect; E29 is unmodelled
engineering. No operating point moved — `v_exit` 16.388 m/s and Kt 11.0258 N/kA·m untouched.

---

## 2026-08-10 (eleventh pass): the payload ladder was arithmetic, and building it as a design moved the answer

| ID | Item | Detail |
|---|---|---|
| **A24** | **The fixed-cell manifest, bands declared at `5fdc978` before the script existed** | One cell of **340.5 × 100 × 100 mm** on the existing 104 mm pitch, twelve cells, with class-specific inserts subdividing along x. **Five of six bands passed.** `validation/A24_fixed_cell_manifest.md`, `analysis/cell_manifest.py`. |
| A24-01 | **1U no longer closes kill criterion 1 — the rung the repository leaned on** | A real insert fits three 100 mm units plus two dividers in a 340.5 mm cell, wasting 37.5 mm: **36 per load and 2.125 kg**, not 40 and 1.913. TubeSat is worse — 41 → **24**, 1.866 kg → **3.188 kg**. Threat 1 still closes, on **PocketQube 1P (0.266) and 3P (0.797)** — two rungs lower, and on the classes with **no corner rails and no designed interface at all**. |
| A24-02 | **Three classes refused outright, which a volume ratio structurally cannot find** | **ThinSat** (114 × 114 × 25.4) exceeds the 100 mm cell section in two axes in every orientation. **12U** needs 200 mm in both section axes and there is **no second cell in y**. **6U** survives only as 340 × 100 × 200 across two cells in z. **The binding constraint is the 166 mm cassette width**, written down nowhere else in this repository. |
| **P44** | **Band 6 failed: at femtosat scale the separation hardware outweighs the satellites** | Declared ≤ 0.5 % of exit velocity, measured **0.508 %**. 720 ChipSats in one cell need 719 shim interfaces — **7.19 kg of hardware to disperse 3.6 kg of payload**, and it stops being momentum-neutral because that mass departs with one side. **The band was not widened.** ChipSat was already 43× outside the mechanism's 200-shot limit; that does not rescue a band declared over every class sharing a cell. |
| ADR-025 | **One cell, class-specific inserts; the per-satellite shoe deferred** | One pitch, one gate, one cradle, one campaign, and A22/A23's results carry across the ladder unchanged. **The cost is stated rather than buried: velocity is programmable per _cell_, not per satellite.** At 3U cell = satellite and nothing is lost; below 3U it is a real reduction. |
| PII-12/13 | **Two Phase II entries with entry criteria** | **PII-12** the per-satellite shoe, entered only by a customer needing per-satellite control below 3U. **PII-13** designed swarm dispersion, entered by P44 — and the only programme item a *market* argument points at rather than an engineering one, since `MARKET.md` claims a designed dispersion no spring can offer and P44 says there is no mechanism behind it. |
| CAD-03 | **`payload_cell` added to `parameters.json`** | The cell, pitch, divider thickness, accommodated classes and the three refusals, with `section_limit_origin` recording *why* y and z cannot grow. Status `PARAMETRIC_ONLY_NOT_DRAWN` — **no insert exists in CAD for any class.** |
| CNT-06 | **Register 71 → 72, 28 → 29 live** | P44. Header propagated. |

**What authorised it.** A24 is a validation with bands declared before its script; P44 is a band
miss, which `validation/README.md` requires to become a numbered defect. No operating point moved.

---

## 2026-08-10 (tenth pass): the renders showed the satellite being fired into its own host

| ID | Item | Detail |
|---|---|---|
| **P43** | **Two published renders fired the payload through the ESPA mounting flange** | `seq2_midstroke.png` and `seq3_release.png` — in `README.md`, on the Pages site and in the wiki — showed the payload departing **through the face that bolts to the host**, and drew the CubeSat as a **wheeled road vehicle** from a sample-asset library. The geometry *is* the interface argument, so this was not cosmetic: a reader taking those frames at face value would conclude the machine fires backwards into the vehicle it is bolted to. |
| P43-01 | **No check could have caught it** | Nothing in `tools/` looks at an image. `check_artifacts.py` guards numbers against sources and has no notion of a picture being wrong about what it depicts. This is P42's shape one layer further out, and **no fix is proposed because none is cheap** — stated rather than implied. |
| P43-02 | **Seven Gen4 shots replace them** | `hero_open`, `espa_interface`, `track_stator`, `brake`, `sled_detail`, `envelope_closed`, `magazine_feed`. In each the payload leaves along the track axis, away from the flange, with a drawn departure arrow so the direction is **stated** rather than merely happening to be right. `seq1_stowed` and `seq3_release` are withdrawn with no replacement. `exploded_view.png` is the only Gen3 render retained, labelled as Gen3 wherever it appears. |
| P43-03 | **The replacement carries a provenance gap, and it is published anyway** | **Gen4 has no committed STEP export** (ADR-019), so the renders now show geometry **no file in `cad/step/` matches**. A set that was wrong about physics is traded for one that is right about physics and unverifiable against a committed model. Deliberate, and recorded as a trade rather than a fix. |
| P43-04 | **Every caption stripped of performance figures** | Gen4 releases at s = 1200 mm over a 900 mm stroke where `analysis/` assumes 1500 mm over 1.5 m, and `CHANGELOG_CAD.md` forbids a Gen4 performance claim until the partial-overlap calculation is done. **A caption is a claim.** The `track_stator` caption asserting the 1.3 m acceleration zone was removed before publication for this reason. |
| REN-01 | **The published set is generated, not hand-edited** | `cad/tools/prepare_renders.py` crops to content, fits to a 1600x900 box, draws the arrow and adds the caption bar, from uncropped frames committed to `cad/renders/source/`. Arrow direction is **per-render** because the camera flips between views — the first pass drew every arrow leftward and pointed the brake shot's arrow **back into its own machine**, which would have reproduced, in the fix, the exact error the fix exists to correct. |
| P42-04 | **P42's fix reached two public surfaces of three** | The **GitHub wiki** was still serving the pre-quadrature point — 11.22 N/kA·m, 16.54 m/s, 19 %, 76.9/124.9 kg — the withdrawn renders, and a link reading `aaaaaaaaaaaavm/emocd`. `wiki/Home.md` here has been correct for a week, but the live wiki is a **separate git repository** nothing syncs to, so the flagship copy being right was never evidence the wiki was. **Outstanding:** it cannot be pushed from this environment (a wiki is not API-addressable), so it stays wrong until copied across by hand. |
| MASS-01 | **`mass_properties.py`'s own docstring was four values stale** | It advertised **72.3 kg dry, 120.3 kg loaded, CG 0.46 m** against the script's actual **76.5 / 124.5 / 0.44** — the header never moved when the sled CAD reconciliation and the gate resize landed. A docstring is the first thing anyone reads about a script, and the CAD brief now sends modellers straight at this one. `legacy/README.md` carried the same figure and is corrected with it. No number changed; only the description of them. |
| CNT-05 | **The register head was stale by four entries, under a claim it could not be** | It read 67 / 29 live against an actual **71 / 28** (14 P, 14 E), 11 `CORRECTED`, 32 `CLOSED`. The sentence saying this file and the numbers elsewhere "cannot drift apart again" was **removed rather than repaired**: `register_status.py --check` validates each entry's own `Status:` line and never read the summary table, so the promise was never enforced by anything. |

**What authorised it.** Freeze rule 2 — a defect that makes a published Phase I deliverable
wrong. No operating point moved; `v_exit` 16.388 m/s and Kt 11.0258 N/kA·m are untouched.

---

## 2026-08-10 (ninth pass): the public site was a two-month-old snapshot of the project

| ID | Item | Detail |
|---|---|---|
| **P42** | **The Pages site served the pre-quadrature operating point for seven days** | `docs/index.html` carried **11.22 N/kA·m, 16.54 m/s at 10.7 g, 21.2 %, 76.9/124.9 kg, 66.1 N·s** — every one superseded on 2026-08-03. It is the most public artifact this project has and it contradicted the repository's own baseline. |
| P42-01 | **Its validation section was wrong about the project's own record** | It said *"Three have now been run, and one of the three failed"* and listed A1, A6 and A7 as "specified", against an actual **19 of 21**. Anyone judging this work on its evidence discipline was reading a two-month-old snapshot of that discipline. |
| P42-02 | **The cause is P38's gap, one layer out** | `check_artifacts.py` guarded the paper, the CV, `BASELINE.md` and the figures. **It did not guard the website** — the one published artifact with no tie to the numbers it quotes. Now added, against `motor_results`, `mass_properties` and `astro_results`; it fired immediately on a 70-hour drift. |
| P42-03 | **What is not fixed, stated rather than implied** | The site is **hand-authored HTML**, so the guard detects drift but cannot prevent it, unlike `BASELINE.md` which is generated and cannot drift at all. **The durable fix is to generate the headline table from `analysis/results/*.json`.** Not done; until it is, this failure mode is detectable rather than impossible. |
| SITE-01 | **The site now carries the concept** | "The idea" gains the last-mile framing with A20's boundary attached — 27.8 m/s per shell, 367° of free nodal spread, **plane change excluded at 133 m/s/deg**, and the honest division that above ~100 m/s the *stage* supplies most of the altitude range. |
| SITE-02 | **And the real validation record** | The verification table is rebuilt from A1 through A23: the two outright failures, A12's 37 % finding, A14's 611× band-4 miss, A17's 8.18× amplification, A19 and A20's band-1 failures, and A22/A23's outcomes. Plus the note that **twice this month a failed band led to a bug in my own analysis script rather than in the design** — which is what declaring a band beforehand is for. |

**What authorised it.** A defect that made a published Phase I artifact wrong, which
`docs/BASELINE.md` change control names explicitly. No operating point moved.

---

## 2026-08-10 (eighth pass): WS2 closes both predicted failures, and the paper catches up

| ID | Item | Detail |
|---|---|---|
| **A22** | **Retention gates resized, and the fix is eleven grams** | 2 × D6 → **2 × D9 A-286**. Capacity 18.2 → **41.0 kN**, margin at Q = 30 **−0.36 → +0.45**, positive across Q = 10–30. **The design no longer depends on where the unmeasured Q lands**, which is the whole point — A19 found Q was the only assumed input moving a margin through zero. Band 1 reproduced A18 band 9 to **0.000 %** because the load relation is imported, not reimplemented. |
| A22-01 | **No architecture change needed** | Splitting the stack across two gates was in the allowed space and is not required, so the magazine is untouched. Quasi-static margin 1.21 → 3.98; pin shear still governs over bearing. D8 misses the 0.20 target by 0.06 and is named because a reader will ask. |
| A22-02 | **A definitional discrepancy** | A18 quotes this margin as **−0.10** (capacity/load − 1); `sizing.py` applies a **1.4 design factor** and gives **−0.36** for the same hardware. Both correct, different quantities. The factored form is used — dropping a design factor while resizing would be a silent relaxation. |
| A22-03 | **Adopted, not just asserted** | `sizing.py` and `cad/parameters.json` both carry D9, with the reason and run sheet named. The analysis said D9 while the scripts said D6 for one commit; that drift is the class this project logs, closed in the same pass. |
| **A23** | **The release was never the risk** | Acceleration ends at 1300 mm and release is at 1500, so the payload coasts **12.2 ms at zero commanded force**. At the ~1 N residual that leaves, the mechanism has **250 µs** of slack and lands two orders of magnitude inside the 2 °/s band. **A7-R's 50.7 µs was a full-push worst case that does not occur.** |
| **P41** | **The payload slams into its cradle at the start of every shot** | The 70 mm CoM offset gives a 28.92 N·m moment and **688 rad/s²**; the payload crosses its cradle clearance and **arrives at 36–231 °/s — 18 to 115× the band.** An impact load on the payload's own rails, twelve times per campaign, that appears nowhere in this repository. After impact it rattles, and whether that has settled by release needs a restitution model this project does not have. |
| P41-01 | **Tightening the clearance does not fix it** | Arrival goes as √(clearance): ten times tighter buys √10, 115 → 36 °/s, still 18×. **Preload the cradle** instead — A23 band 4 measured the couple reaction it must exceed at **85.0 N per contact**. The geometric alternative needs the CoM offset cut **70 mm → 3.5 mm**. |
| KC-01 | **Kill criterion 4 moves from unmodelled to modelled, and is still not passed** | It is now a stated requirement on a cradle preload and a release residual, against a mechanism that does not exist. `STRUCTURAL_GAP.md` loses one of its four findings, and its stale margins are reconciled rather than deleted. |
| **PAPER** | **Three factual errors corrected** | The gate passage described a **negative margin as an open problem** — now D9 at +0.45. Tip-off said the analytic budget "remains a failure against the comparator" — now A23's result. And the claim that the 10–20 s versus 1200 s cadence contradiction **"remains open"** was simply wrong: **ADR-020 closed it at 1200 s** on 2026-08-05 and the paper never caught up. |
| PAPER-01 | **Two additions** | §VII gains the **last-mile ConOps** with A20's boundary attached — 27.8 m/s per 50 km shell, plane change excluded at 133 m/s/deg, and the honest division that above ~100 m/s the *stage* supplies most of the altitude range. The abstract gains A21's **7.5× lifetime-extension** ratio, which the velocity ratio of 6.6 understated. **13 pages, zero undefined references.** |
| SWEEP-01 | **Repo-wide consistency pass** | Validation counts 9-of-11 → **19 of 21** in `README.md` and `SUMMARY.md`; D6 corrected in **ADR-008** (amended, not rewritten), `QUALIFICATION_PLAN.md`, `PROVENANCE.md`, `INVENTORY.md`, E10 and the paper. **A18's run sheet keeps its D6 record and gains a forward pointer** — the record of what it found is not edited. `README.md` gains the concept paragraph; page counts corrected in three places; `BASELINE.md` regenerated. |

**What authorised it.** Two validation outcomes against bands declared before their scripts
existed, one design change adopted under `BASELINE.md` change-control rule 2, and a correction
pass over documents that a defect had made wrong. **No operating point moved:** `v_exit` stays
16.388 m/s, K<sub>t</sub> stays 11.0258 N/kA·m.

---

## 2026-08-10 (seventh pass): two owner decisions, both branches priced first

| ID | Item | Detail |
|---|---|---|
| OD-00 | **Both branches costed before either was chosen** | New `analysis/owner_decisions.py` → `results/owner_decisions.json`. It re-runs the real pipeline rather than reasoning about it, and **adopts nothing** — no branch is written to the baseline. `shot()` gains an `energised` parameter defaulting to `ACCEL_ZONE`, so the alternative is priceable without editing the model; `make_baseline.py --check` confirms the default moves nothing. |
| **ADR-022** | **P29: the winding is segmented for fault isolation and driven as one section** | `vol_cu = ACCEL_ZONE` stands and **no baseline value moves.** |
| OD-01 | **The row that decided it** | Copper 834.7 → 218.3 J, net efficiency 20.99 → 28.07 %, P33 inductance 19.70 → 5.15 µH, peak current 339 → 288 A — and **exit velocity identical at 16.388 m/s in every case.** Force is commanded, so copper loss is a power draw and not a thrust reduction. **Segmentation changes what the shot costs, not what it delivers.** Robust to segment count: four segments and one-sled-length differ by 0.15 points. |
| OD-02 | **Why the conservative branch** | **Efficiency appears in no kill criterion; mass appears in the one crossed by a factor of three.** Block commutation costs an inverter per segment or a switching assembly, none of it in the mass rollup (**P10**). Buying efficiency with mass is the wrong direction for the live threat. It is also the conservative direction in a model with nothing measured behind it. |
| OD-03 | **The price is recorded, not glossed** | **7.09 points of efficiency and 616 J of copper per shot, paid for drive simplicity, with 74 % of the copper dissipating under no field.** P29's second possibility was conservatism that was real judgement *"written down nowhere"*; it is now written down with both branches costed, which is what the entry asked for. The `energised` default is now **a recorded decision rather than an unexamined one**. P29's own "24.4 %" estimate is superseded — it predates the quadrature correction. |
| **ADR-023** | **P9: the target host is a spent upper stage, not an ESPA-Grande port** | ESPA-Grande *port envelope* compliance is not a requirement; the ESPA *bolt pattern* remains the mechanical interface. The deployer mounts on a stage, not in a port. |
| OD-04 | **The alternative was priced and rejected** | Overhead that is not acceleration zone is 539 mm and does not shrink, so fitting 1270 mm means a 731 mm accel zone. Velocity goes as √s: **16.388 → 12.286 m/s, −25 %**, payload KE 537 → 302 J, lifetime ×1.62 → ×1.44. Repackaging 150 mm recovers about a third and depends on a brake layout nobody has drawn, against an arrest section **P28** already calls oversubscribed. |
| OD-05 | **Why re-scope** | **ADR-002 put the host as a spent upper stage in 2023 and ADR-010 specified the interface host-agnostically.** The ESPA-Grande requirement was a leftover from an earlier framing that two accepted decisions had already contradicted. Shortening spends 25 % of the number every product claim rests on, to enter a market this architecture was not designed for, and barely touches the mass threat that is closest. |
| **OD-06** | **It does NOT make kill criterion 2 pass, and that is stated as loudly as the decision** | Re-scoping a target after seeing the geometry fail is `validation/README.md`'s band rule violated on a threshold. The threshold is unchanged. **Kill criterion 2 moves from CROSSED to NOT EVALUABLE**, because no accommodation envelope for a POEM-class host is public (**E5**). **A decision that converts a measured failure into an unmeasurable unknown is not progress**, and `KILL_CRITERIA.md`, the paper's limitations section and P9's entry all say so in those terms. E5 rises in priority; `MARKET.md` needs re-scoping against the lost port population. |
| OD-07 | **Paper** | Driving requirements drop ESPA-Grande envelope compliance and state the host class; the redundancy sentence says the segmentation is fault isolation and **not** block commutation, because a segmented long-stator machine would normally imply the latter; the layout caption and the limitations paragraph carry the re-scope and its 25 % cost. `sec:host` label added — the host section had none. PDF rebuilt: 12 pages, zero undefined references. |
| OD-08 | **Phase II** | **PII-12** opened for block commutation with a stated entry criterion: P10 closing with margin, or some claim becoming efficiency-limited. **PII-4 narrows** — no longer about fitting 1270 mm, live again only if a host envelope arrives that 1839 mm also fails. |
| CNT-04 | **Register** | 29 live → **27 live**; 31 closed. P29 and P9 both closed by decision. |

**What authorised it.** Two owner decisions taken with both branches priced, recorded as ADRs
with their falsifiers named. **No operating point moved:** `v_exit` stays 16.388 m/s,
K<sub>t</sub> stays 11.0258 N/kA·m, net efficiency stays 20.99 %.

---

## 2026-08-10 (sixth pass): freeze the register, and turn B-1 into an order

| ID | Item | Detail |
|---|---|---|
| **ADR-021** | **The register is frozen** | `OPEN_PROBLEMS.md` is closed to new entries except for **a defect in the machine**, **a defect that makes a published Phase I deliverable wrong**, or **a validation band miss**. Everything else — defects in `tools/`, bookkeeping drift, stale cross-references, observations about the register — is fixed in place with a `CHANGELOG.md` line and no number. |
| ADR21-01 | **What the discipline bought, stated first** | It caught a separation figure wrong by **5.7×**, an inter-array force **37 % high**, an invariance claim **in the paper's own abstract**, and **P38**. It is not overhead and freezing it is not a repudiation. |
| ADR21-02 | **What it now costs** | ~**16,000** lines of prose around ~**3,200** lines of analysis, and **five** tools whose only job is policing the record. Of the three entries opened on 2026-08-10, **one was in the paper and one was in the export tool's file-copying semantics** — the apparatus has begun generating its own defect load. **A19** confirmed what `STRUCTURAL_GAP.md` already said four days earlier. And **B-1 has never been ordered**. |
| ADR21-03 | **Nothing is deleted, and it is not retroactive** | All 67 entries stand with their dispositions; the 29 live ones keep their named next steps. **A freeze is not a purge** — a register that shed its inconvenient entries would destroy the only thing this project has instead of hardware. **P39 keeps its number** although it would not be opened under the new rule. |
| ADR21-04 | **The band rule is untouched** | Bands still declared before runs, still never widened after one, still producing a numbered defect on a miss. That half is load-bearing and is not what became expensive. Phase II is unaffected: `VOLLEY-lab`'s register is not frozen. |
| ADR21-05 | **The counts stop being propagated** | One number in five places was five chances to drift and a tax on every register change. `OPEN_PROBLEMS.md` carries the count from `tools/register_status.py`; `KILL_CRITERIA.md`, `ROADMAP.md` and `PHASE_I_CLOSURE.md` now point at the register instead of restating it. |
| ADR21-06 | **The risk this accepts, stated rather than hidden** | A real defect in `tools/` will now be fixed and logged rather than tracked, so one could be forgotten. Judged cheaper than the alternative on the evidence that the last two apparatus defects consumed a working session between them while three kill criteria sat crossed and unmoved. **The falsifier is named in the ADR: if the next machine-level defect is found late, this was wrong. The counter-test is whether B-1 gets ordered.** |
| **B1-01** | **B-1 becomes a purchase order** | New `docs/B1_ORDER.md`. B-1 has had a method since 2026-07-29 and a bill of materials since 2026-07-30 and has not been ordered. **A procedure invites more analysis; a purchase order invites a purchase.** |
| B1-02 | **The magnetisation sketch and quotation wording** | The near-certain failure mode is a supplier magnetising **through the largest face**, the default tooling orientation, yielding eight identical blocks and no Halbach array — invisible on arrival because the blocks are correctly magnetised, just not on the axis needed. The order now carries an ASCII sketch of the four-block wavelength and paste-ready enquiry wording requiring written confirmation of the axis per group before production. |
| B1-03 | **Receiving inspection, before assembly** | Added: confirm the axis on every block individually with a compass or second magnet and sort into two piles of four **before anything closes across the gap**. If all eight behave identically the order was magnetised on one axis. Once a pair closes at 12 mm it does not come apart by hand, and by then the mistake has already cost the fixture. |
| B1-04 | **Bands restated unchanged** | The five B-1 rows are carried verbatim from `BENCHTOP_TESTS.md` with the derived rig error beside each, and the absolute accept ranges spelled out — 0.590–0.798 T, 0.469–0.635 T, 18.1–27.2 mT, 2.60–6.06 mT, order-of-magnitude. **Declared 2026-07-30, derived 2026-08-06, and not editable after a reading.** |
| B1-05 | **Supplier names removed from the repository** | The existing bill of materials named four companies and an institution. Replaced with supplier *classes* and a three-quotation instruction, which is better ordering practice than a named vendor regardless. |

**What authorised it.** A governance decision recorded as an ADR, and a document that converts an
existing specification into an actionable order without changing a single declared band. No
operating point moved: `v_exit` stays 16.388 m/s, K<sub>t</sub> stays 11.0258 N/kA·m.

---

## 2026-08-10 (fifth pass): the companions were not a function of the commit they name

| ID | Item | Detail |
|---|---|---|
| **P39** | **Twelve published files are in no VOLLEY commit** | Found because regenerating the companions from a clean clone **deleted twelve files nobody had removed**. `export_companion.py`'s `copy()` walked the **working tree**, so anything sitting in a manifest directory went into the companion regardless of whether the flagship tracked it. `VOLLEY-paper` and `VOLLEY-thesis` carried A4's CalculiX decks and solver output — `plate.inp`, `plate_clamped.frd`, `plate_modal.*` and the rest. `git log --all --diff-filter=A` finds them in **no commit**; the flagship tracks exactly one file in that directory. |
| P39-01 | **The stray files are not the defect; the provenance is** | Each companion carries a banner reading "generated from VOLLEY flagship 45332a7", and that was false — the tree it described contained files that commit does not have. The output depended on **what happened to be lying around when the export ran**, so a machine that had executed A4 produced a different companion from a clean clone of the same commit. **A generated artifact that is not a function of its stated input is not generated, it is collected.** Same class as P19 and as the duplicate `results/sizing.json` in `motor_model.py`'s header. |
| P39-02 | **Fixed, and the fix was verified to fire** | `copy()` now filters against `git ls-files`, and the export **names every path it skips** instead of silently dropping it. On a clean clone the filter is a byte-for-byte no-op — checked by diffing a pre-fix and post-fix export, not assumed. That it actually catches a leak was checked too, by planting an untracked `plate_clamped.frd` and confirming it was excluded and reported. |
| P39-03 | **What the fix does not settle, and it is left open deliberately** | `validation/README.md`'s conventions say to "commit input decks and result JSON" — and the A4 decks **are not committed**. So the right end state is probably that `plate*.inp` belongs in the flagship and the solver output does not, rather than that all of it vanishes. **This regeneration removes the input decks from the companions, which were their only published copy.** Restoring them means first deciding what the flagship tracks, which is why P39 stays open rather than being quietly patched. |
| CNT-03 | **Register counts** | 66 / 28 live → **67 / 29 live** (15 P, 14 E), 9 `CORRECTED`, 29 `CLOSED`, propagated to all five places that quote them. |

**What authorised it.** A defect in a tool whose output is published under a provenance claim it
could not support. No operating point moved.

---

## 2026-08-10 (fourth pass): A19 ranks the assumptions, and band 1 fails usefully

| ID | Item | Detail |
|---|---|---|
| A19-00 | **Bands committed before the script existed** | `validation/A19_sensitivity_ranking.md` at `03628da`; `analysis/sensitivity_ranking.py` did not exist at that commit and the absence was checked, not assumed. The bands are about **rank stability**, not a pass/fail value, because a sensitivity ranking has no correct answer to check against. |
| **A19-01** | **Band 1 FAILS: net efficiency has two different leaders** | By range-swing the leader is **bank ESR at 23.240 %**; by local elasticity it is **magnet remanence at 0.4869** against bank ESR's −0.0376, a factor of thirteen the other way. Both are correct and measure different things: ESR wins on swing because its range is a factor of eleven wide, **because the nominal has no source at all** (E17). The rule fixed in advance was to publish both and not pick the convenient one. Both tables are in the sheet. |
| A19-02 | **`v_exit` does not respond to the bank at all, and the mechanism matters** | Bank ESR was declared as having a path to exit velocity and its swing is **exactly zero to the ceiling**. `shot()` commands a sheet current, so force is fixed and ESR changes energy drawn and sag, not push — until the bank cannot source the demand, at which point `BankLimitError` is raised rather than a plausible current substituted. **The bank's effect on exit velocity is nil, then total. A cliff, not a slope**, which is a more useful thing to know about P26 than a coefficient — and P27's fix is what makes it visible. |
| A19-03 | **Bands 2–5 pass; band 3 passes exactly** | All declared no-path entries return **0.000**, not merely small, so no undeclared coupling and no module-routing bug. Largest `v_exit` swing 5.660 % clears the 1 % floor. Rank order survives halving every range. |
| A19-04 | **Six of nine inputs are zero on every headline number, and two of them move a pass/fail transition** | **Structural Q**: 0.000 % on all three, and the retention-gate margin **+0.559 → −0.100** across its range — through zero. **Brake pole field**: 0.000 %, and the brake stopping distance 0.345 → 0.063 m against a 0.210 m arrest section. **The headline numbers are not what is at risk from these assumptions; the design's viability is.** A ranking that looked only at the three outputs would have reported six harmless zeros and missed both, which is why every zero-ranked input also reports the quantity it does govern. |
| A19-05 | **Band 6 reports, and two of three leaders lead on unsourced ranges** | `v_exit`'s leader is magnet remanence over a ±0.075 T interval that exists **because the CAD states no magnet grade**; efficiency's leader is bank ESR over a range that exists because the nominal has no provenance. Reported as the band required. The ordering is stable and the zeros are real, so the ranking stands with its top two entries flagged as resting on intervals of my own construction. |
| **A19-06** | **Limitation found on the first run: one-at-a-time cannot see interactions** | Fin emissivity returns **exactly zero on every output including its own binding quantity**, because at the nominal 500 W/m²K contact conductance the joint sinks the heat. That is true at the nominal point and false generally — at 100 W/m²K the fin residual moves **0.1701 → 0.0746 K** across the emissivity range. **A18 swept the two as a grid and would have caught it; A19 sweeps one at a time and does not.** Where two uncertain inputs gate each other, this ranking understates the one currently masked. |
| A19-07 | **And band 5 passes vacuously on two of three outputs** | Rank stability under halved ranges is a real test only where entries are non-zero. On net efficiency bank ESR leads magnet remanence 23.24 % to 5.50 % at full range and 9.92 % to 2.76 % at half, so that ordering is physics. On `v_exit` and kg per satellite only one input is non-zero and second and third place are **ties among structural zeros broken by list order**. The band passed; on two outputs it passed on nothing, and the sheet says so. |
| A19-08 | **Measurement order, which is the deliverable** | Structural Q first — the only input that moves a margin through zero, with four findings already queued behind it in `STRUCTURAL_GAP.md`. Then the magnet grade, a look-up rather than a measurement. Then a sourced bank ESR. Then B-4 for the brake pole field. Propagated to `PHASE_I_CLOSURE.md` §10b and `STRUCTURAL_GAP.md`. |
| A19-09 | **The framing, fixed before any number existed** | **It ranks assumptions and makes none of them less assumed.** Every input is exactly as unmeasured after this as before. The project's existing Monte Carlo measures *dispersion*, which is a different question. E4 is unaffected and no band that any of these inputs feeds has moved. |

**What authorised it.** A new analysis with bands declared and committed before the script, the
discipline `validation/README.md` exists to enforce. No operating point moved — the sweep harness
reproduces `v_exit` 16.388 m/s, net efficiency 20.99 % and 6.375 kg per satellite exactly, which
is itself the check that it drives the real pipeline rather than a copy of it. K<sub>t</sub> stays
11.0258 N/kA·m.

---

## 2026-08-10 (third pass): the bookkeeping items, and the three that would not close

| ID | Item | Detail |
|---|---|---|
| P7-01 | **Closed geometrically by the Gen4 layout** | Release moves to s = 1200 mm on a 900 mm stroke and brake-fin entry to s = 1222 mm, so release sits **22 mm before** the fin reaches x = 1530 mm, without adding track length. Recorded against **A16** and **P32**. The entry's second half — that the brake drives envelope length — was **always P9's problem** and stays there rather than being carried twice. |
| P7-02 | **What that close is worth** | Gen4 **has not been exported into this repository**; the committed STEP, analyses and baseline remain the Gen3 record and the export gate is deliberately closed. This closes a geometry question against a geometry that is not yet committed. Stated in the entry rather than implied. |
| P23-01 | **Swept, and the two survivors are correct because they were never edited** | Every remaining 127.7 / 127.6 ms occurrence read. Four prose instances had already been corrected. The two in `validation/A8_pulse_spice.md` are **the band as declared on the day**, and `VALIDATION_REPORT.md` carries its pass annotated "at the superseded operating point". **The distinction between a stale number and a historical one is the whole of this item**, and every instance is on the right side of it. |
| P27-01 | **Verified in source, not taken at the entry's word** | `motor_model.py` defines `BankLimitError` and `shot()` raises it on `disc <= 0`, naming the demanded power, the `V²/4R` ceiling and the stroke position. Marked `CORRECTED`. |
| E8-01 | **The premise was false and the entry had not noticed** | "Not examined since the efficiency correction" stopped being true on 2026-08-03. A11 recovers **291.4 J**, 23.0 % of sled KE; **934.7 J** reaches the fin, which is the "~1.0 kJ" made exact; A18 closed E26 on the fin transient. **Closed into P28**, which owns the live layout decision with its cost already priced, rather than sitting beside it asking the same question. |
| E13-01 | **Closed on the ground that nothing depends on either number** | Both were disposed of on their merits when logged; only the provenance question stayed open. A tree search finds **no current claim resting on either** — "780" survives in this entry and in `INVENTORY.md`, which already records it as falsified; "1,000+ G" survives only in the entry. **An untraced number nothing depends on is resolved, not open.** |
| **P20-01** | **"Fix the sheet" was the wrong instruction, and the sheet was deliberately not edited** | Correcting the mis-specified array-surface band in `validation/A1_field_femm.md` would be **editing an acceptance band after its run** — the single move `validation/README.md` exists to prevent, and one this entry had already ruled out itself. A band may be corrected before a run, dated, with the original stated; never after. The fix is forward-only. |
| P20-02 | **So it now lives where the next sheet will meet it** | A new convention in `validation/README.md`: a field band must name **which field, at which plane, as which quantity** — single- or double-sided, fundamental or raw peak. Single-sided 0.7714 T, correct double-sided 0.9317 T, FEM fundamental 0.9312 T (ratio 0.9994), raw peak 1.4641 T and mesh-dependent. **P20 stays open** and closes when **A2** is specified. A2 does not exist. |
| P14-01 | **Audited against Gen4: two of six answered, four carry** | **G3-D5** (arrays not re-centred) — Gen4 states them explicitly in the 488 mm chassis local frame and A16 computed thrust on that layout. **G3-D12** (assembly 156 mm aft of envelope) — Gen4's stowed station clears the aft skin by 24 mm, which also removes the implied ~57 % ESPA overrun. **G3-D1, G3-D2, G3-D4, G3-D6 carry**; Gen4's own limitations section says the roller-span discrepancy remains open. |
| P14-02 | **The one that matters is filed in the wrong category** | **G3-D4**, one stator layer or two, is ×2 force for the same sheet current against ×2 copper mass, **has never been computed**, and sits upstream of K<sub>t</sub> and the headline velocity. It is filed as a CAD defect and is really an unmade design decision. |
| **E16-01** | **Two of the three references do not exist in the paper any more** | A search of `paper.tex` returns **zero** matches for "Yudintsev", "vibro" or "impact". They were removed from the bibliography and the register went on flagging them for verification — guarding citations the deliverable no longer makes. The bracket numbers were stale too: the bibliography now runs to 31 entries and [15], [17], [18] are three unrelated references. |
| E16-02 | **The third is now a citation rather than a paraphrase** | `\bibitem{eddy}` read "Eddy current damper modelling for space mechanisms, Actuators" with no author, volume, number or year. Corrected to **Diez-Jimenez, Alén-Cordero, Alcover-Sánchez and Corral-Abad, *Actuators*, vol. 10, no. 1, art. 8, 2021**, doi:10.3390/act10010008. PDF rebuilt. |
| E16-03 | **Verified bibliographically, NOT substantively, and the difference is load-bearing** | Full-text retrieval is **blocked by this environment's egress policy** — `doi.org`, `www.mdpi.com` and `arxiv.org` all refuse at the proxy, re-tested rather than assumed. The citation is confirmed to exist and to have those details from four independent indexes. **It was not read.** It is cited for *"flight heritage in the damper class"* while the retrievable metadata describes a bench-tested laboratory device, so the flight-heritage half rests on vendor documentation not in hand. **The paper's sentence is deliberately left alone** — rewriting a published claim on the strength of a title I could not open is the same error in the opposite direction. |
| E16-04 | **Both Foster references check out at the same standard** | `foster2` confirmed as arXiv:1509.03270, Foster, Hallam and Mason, 2015, also AAS 15-524; `foster` confirmed as *J. Spacecraft and Rockets*, doi:10.2514/1.A33927. Author list, title and venue match what the paper prints. **Neither was read**, so the 25-day differential-drag baseline is still unchecked against the flown result it is attributed to. **E16 narrows, it does not close.** |
| CNT-02 | **Register counts** | 66 / 33 live → **66 / 28 live** (14 P, 14 E), 9 `CORRECTED`, 29 `CLOSED`. Derived from `tools/register_status.py` and propagated to `KILL_CRITERIA.md`, `ROADMAP.md`, `PHASE_I_CLOSURE.md` and the `OPEN_PROBLEMS.md` header — including a fifth counts table in that header which the previous propagation had missed. |

**What authorised it.** Bookkeeping dispositions against entries whose evidence was checked rather
than assumed, plus one bibliographic correction to the manuscript. **Three items refused to close
and are recorded as refusing**: P20 because closing it means breaking the band rule, P14 because
four of six defects are untouched, E16 because a reference verified only by its title has not been
verified. No operating point moved: `v_exit` stays 16.388 m/s, K<sub>t</sub> stays 11.0258 N/kA·m.

---

## 2026-08-10 (second pass): what the deployer does to the satellite inside it

| ID | Item | Detail |
|---|---|---|
| P34-01 | **The block on P34 step 1 was stale, and had been for days** | Step 1 read "resolve P3 first". **P3 and P21 are both `CORRECTED`** — magpylib's `Cuboid` is an exact analytic solution for a uniformly magnetised block, so the finite-array field was already three-dimensional and correct with no mesh, and `far_field_sensitivity.py` had shown the 7-wavelength default converged to 0.64 % at 10 mm. `PHASE_I_CLOSURE.md` A-13 also carried "blocked behind A-8/A-9". **A blocked item needs its block re-tested, not inherited**, which is the same failure class as the A1 row that said "not run" while three other files recorded the result. |
| P34-02 | **The exposure is published as a payload environment specification** | New `docs/PAYLOAD_ENVIRONMENT.md`, from new `analysis/payload_environment.py`. Field across the whole 3U envelope, z = 20 to 120 mm: **61.081 mT at the near face, 0.341 mT at the far face**, below magnetometer full scale only at **z = 251 mm** and below Earth's field at **332 mm**. Every part of the payload sits above both, 611× to 3.4×. Attached to **ADR-010** and the paper's interface section, which previously specified only what VOLLEY asks of a *host*. |
| P34-03 | **The profile has two regimes and one mitigation does not cover both** | Not visible in the single 61 mT figure. The near face is a steep exponential, **−17.1 mT/mm**, so 10 mm of standoff is worth a factor of eight and carries essentially all the magnetic force, which goes as ∇(B²). Beyond ~60 mm the field is a nearly uniform 0.54 → 0.34 mT tail with a gradient three orders of magnitude smaller. **Standoff fixes the near face and does nothing for the tail.** |
| P34-04 | **The exposure was understated as "one shot plus dwell"** | The Halbach array is a permanent magnet. The static field is continuous from magazine loading through ground handling, launch and the whole campaign — not the 158.6 ms of a shot, which A14 had already found is not the dominant term. **Cradle dwell is specified nowhere in this repository**, so it is recorded as a bound: one 1200 s cadence interval at the low end, the full 4.0 h campaign plus ground time at the high end. That is a ConOps gap, not a physics one. |
| P34-05 | **The deployer's own load path contains soft-magnetic material** | `cad/parameters.json` gives the magazine septum as **silicon steel, 1.0 mm**, between adjacent satellites. It will both shunt flux and itself magnetise, changing the field a neighbouring satellite sees. **Nothing has modelled that.** It is a second reason the in-cassette field is not simply the sled field at greater distance, and the cassette case is stated as unmodelled rather than assumed benign. |
| P34-06 | **P34 narrows, it does not close** | Step 1 done. Step 2, the **payload** materials list that would separate recoverable saturation from permanent magnetisation, is now the whole of the item and needs a customer or a stated reference payload — A14 band 5 was declared VOID-able in advance on exactly this ground. Step 3, T-6, still needs measurement. **"The satellite is never modified" holds mechanically and electrically and is not established magnetically**, and that qualification now sits next to the claim rather than in an appendix. |
| **P38** | **The paper asserted a payload environment its own validation had falsified** | **New numbered defect.** The EMC section said a magnetometer-carrying customer payload "sees a field comparable to a conventional reaction-wheel assembly at the same standoff". **A14 band 4 falsified that on 2026-08-05 at 611× full scale** and opened P34 on the strength of it. The sentence survived five days in the published PDF because A14's outcome was propagated to `OPEN_PROBLEMS.md` and `KILL_CRITERIA.md` and not to `paper.tex`. Corrected, and the PDF rebuilt: 12 pages, zero undefined references. |
| P38-01 | **The general case is the part worth keeping** | `check_artifacts.py` catches a PDF older than its source. **Nothing catches a source older than its own validation result.** `BASELINE.md` change control already requires a baseline change to state which validations it invalidates; that rule runs in one direction only. Carried as the open half of P38. |
| CNT-01 | **Register counts** | 65 entries / 32 live → **66 / 33** (17 P live, 16 E live), derived from `tools/register_status.py` and propagated to `KILL_CRITERIA.md`, `ROADMAP.md`, `PHASE_I_CLOSURE.md` and the `OPEN_PROBLEMS.md` header. |

**What authorised it.** P34-01 through P34-06 are an analysis whose block had lifted. P38 is a
defect that makes a Phase I deliverable wrong, which `docs/BASELINE.md` change control names
explicitly as a permitted trigger. No operating point moved: `v_exit` stays 16.388 m/s and
K<sub>t</sub> stays 11.0258 N/kA·m.

---

## 2026-08-10: A15 band 8 was never waiting on a propagator

| ID | Item | Detail |
|---|---|---|
| A15B8-01 | **Band 8 was recorded as not evaluated for the wrong reason** | The sheet said "Case B is not generated", which reads as a missing GMAT run. An impulsive plane change at a circular orbit is closed form, Δv = 2·v·sin(Δi/2), and no integrator contributes to it. What Case B is actually missing is the **host**: POEM's mass and control authority are undisclosed (**E5**), so there is nothing to spend the Δv from. Only the second kind of missing is real, and the sheet now says which one it is. |
| A15B8-02 | **The number, and a second confirmation of band 1** | `validation/gmat/case_b_plane_change.py`, importing `MU` and `RE` from `astro.py` rather than restating them. **133.3 m/s per degree** at R1's 7.640 km/s, 134.3 at R2/R3. One 16.388 m/s shot spent entirely on plane change buys **0.1229°** — the identical figure GMAT measured for band 1. Two independent routes to the same ceiling. |
| A15B8-03 | **Verdict: VOID as a capability claim, as declared in advance** | The committed band reads "**report**; VOID as a capability claim". The report is made and the void stands on the reason it always named. This is the pre-declared disposition being applied, not a judgement formed after seeing the result. |
| A15B8-04 | **The trade shape is worse than the ceiling alone suggests** | One degree costs the host **8.1× the entire VOLLEY shot**. Case B is not a capability the deployer adds to a host; it is one the host would have to already possess, at a scale that makes the deployer's contribution irrelevant. `KILL_CRITERIA.md` §7 carried "plane change 0.12°, effectively nil" as an estimate; it is now a propagated result and a closed-form one that agree, and the row can be read as settled rather than pending. |
| A15B8-05 | **Band 7 is still open, and is not being folded in quietly** | Band 7 asks whether the campaign spans exactly 12 × 1200 s. That is a property of `build_poem_campaign.py`'s shot scheduling, not a GMAT output, so no propagator run will ever produce it. It closes by reading the generator against ADR-020, which has not been done. Recorded as not evaluated in both the results table and `PHASE_I_CLOSURE.md`. |

**What authorised it.** Evaluating a band by the method the band itself implies, with the
disposition unchanged from the one committed before the run. No acceptance band was edited. No
operating point moved: `v_exit` stays 16.388 m/s and K<sub>t</sub> stays 11.0258 N/kA·m.

---

## 2026-08-05 (second pass): reading the silo paper, and what it says about ADR-003

| ID | Item | Detail |
|---|---|---|
| ADR3-01 | **ADR-003's armature clause was wrong and my own other paper is what shows it** | It rejected the coilgun partly because "it needs a conductive armature, either bolted to the customer satellite or separated as a sabot with its own release event." That is a false choice. *Electromagnetic Launch System for Vertical Silo-Based Missile Deployment* considers exactly this trade and selects an **inductive cradle** — reusable, never carried by the payload — over a conducting sabot, to avoid rail ablation and suit repeated cycling. Architecturally that is the same move as this project's reusable sled. Struck rather than rewritten, because it was doing rhetorical work it could not support. |
| ADR3-02 | **The decision is unaffected** | The load-bearing reasons were never about where the conductor sits: sequential coil triggering is fire-and-commit against a synchronous machine commanding current on measured position, and Feng et al. run 1352 g mean against 10.53 g here. Both were already stated in the ADR and both stand. `docs/SKILLS.md` points readers at both papers, so a reader could have found this before I did. |
| SILO-01 | **Two of Table III's four rate-of-fire rows do not follow from its own caption** | The caption fixes `t_index = 1.5 s` and the text gives `t_cycle = E_input/P + t_index`. The 1 MW optimistic row prints **18.5 rounds/min** where the stated method gives **15.00** (it implies t_index = 0.74 s), and the 500 kW optimistic row prints **8.6** where the method gives **9.23** (implying 1.98 s). The 18.5 propagates into that paper's abstract and conclusion, so its headline cadence is high by 23 %. `SKILLS.md` had already corrected the 1 MW figure; the 500 kW row had not been noticed. Recorded in `docs/SKILLS.md` because that paper has no defect log of its own. |
| SILO-02 | **Its abstract claims an EMI analysis its body does not contain** | The abstract says g-load tolerance, **electromagnetic coupling** and pulsed-power thermal management "are identified and analyzed". Section IX lists six challenges and electromagnetic coupling is not among them. |
| E12-01 | **The pair is the argument for closing E12** | Two electromagnetic launch studies and no EMI calculation in either: one dropped an architecture partly on electromagnetic grounds it never computed, the other lists the analysis in its abstract without performing it. The question has now also been asked from outside the project. E12 records what a first-pass scoping calculation needs and notes that **P33 has just supplied the missing inputs** — phase current and winding inductance — so the `dI/dt`, the field at the payload envelope, the induced EMF and the spectral knee are all computable from `analysis/results/` without new apparatus. T-6 remains the measurement. |

**What authorised it.** ADR3-01 is a correction to a published argument in an architecture
decision record, which is the class this project fixes in place with the original struck and
visible. The SILO items are defects in a document cited on my CV and described in `SKILLS.md`;
recording them where the paper is described is the only defect log it has. No VOLLEY operating
point, band or verdict moved.

---

## 2026-08-05: the coilgun's real rejection reason, and the inductance behind it

| ID | Item | Detail |
|---|---|---|
| HIST-01 | **The recorded reason for the pivotal architecture change was incomplete** | `DECISION_LOG.md` and ADR-003 both explained the mid-2025 coilgun-to-LSM switch through velocity accuracy. My 2021-2025 notebooks give two different reasons and they come first: the acceleration is enormous and the electromagnetic environment is severe, and either one defeats the point of carrying an **unmodified** CubeSat. Added to `docs/HISTORY.md` in the notebook's own words, with the seven constraints the motor answered at once. |
| HIST-02 | **One half of that judgement is now a number and the other never was** | ADR-003 already carries the acceleration comparison: Feng et al. run 1352 g mean over a 3.9 m barrel against this design's 10.53 g peak. **The EMI half has no working behind it anywhere**, in this repository or the notebooks. It was an instinct about pulsed megaampere discharges beside unshielded commercial electronics. `E12` already records the near half of the gap; the file now says so rather than implying the decision was quantified. |
| P33-01 | **`paper.tex` credited a winding inductance that did not exist** | The drive section said 20-40 kHz is "high enough that the current ripple is filtered by the winding inductance". There was no henry anywhere in `analysis/`, and no phase current either: `motor_model.shot()` integrates in *sheet* current and its `I_peak` is the **DC-link** current, not a conductor current. Logged as **P33**. |
| P33-02 | **The model cannot produce an inductance, which is why nobody had** | A sheet-current model is turns-invariant: the same 126 kA/m winds as many turns at low current or few at high, L scales as N², phase current as 1/N, stored field energy is unchanged. The claim could not have been checked when it was written. |
| P33-03 | **The bus closes it** | `analysis/drive_electrical.py`. The inverter must synthesise the phase voltage the machine demands at rated speed from a 96 V bus sagged to 90.9 V, and the required volt-amps are invariant under the turns count, so the design point follows with no new winding assumption. Armature field energy **2.058 J** by harmonic sum over the actual belt distribution; **373.2 A** peak phase current, **19.70 µH**, **25.18 mΩ**, τ = **0.782 ms**, modulation index 1.00 at exit. |
| P33-04 | **Half the paper's sentence survives** | Ripple adds **3.71 J to an 834.7 J** copper budget at 20 kHz, so the loss claim is fine and no thermal or energy number moves. But ripple is **16.3 % peak-to-peak at 20 kHz** and 8.2 % at 40 kHz, and 16 % is not a filtered current. The sentence asserted it of the whole range; only the top of the range is defensible. Corrected in the manuscript and the PDF rebuilt. |
| P33-05 | **Two things nobody had written down** | The SiC devices carry **373 A**, not the 339 A quoted everywhere, and the paper specifies a 1200 V rating and no current rating. And exit velocity couples to phase current through the bus, landing on the ESR ceiling **P26** already tracks. That coupling is **not** a new velocity ceiling and is not written up as one: the machine can be rewound for any speed, it just pays in current. |
| STALE-01 | **`KILL_CRITERIA.md` §5 still carried the superseded A13 conclusion** | The 2026-08-03 correction reached §6 but not §5, which went on quoting 0.16 °/s residual, an 8.2 s null, an 18.1 s cadence floor and the counter-mass route. Rewritten to the corrected transient-rate result, with the withdrawn cadence conclusion stated as withdrawn. |
| STALE-02 | **`DECISION_LOG.md` cited a comparator struck four lines above it** | The line read "32 % electrical-to-payload efficiency against the coilgun's 1-2 %". The 1-2 % was withdrawn on 2026-07-30 and never removed here, and 32 % predates both the sled-mass adoption and the quadrature correction. Replaced with 20.99 %, and the efficiency comparison is explicitly **not** restated as a reason for the decision, because Feng's 14.9-19.9 % is this design's own range. |
| STALE-03 | **ADR-003 carried a pre-quadrature operating point and called A1 unrun** | 10.7 g and 2.80 kJ moved to 10.53 g and 2.85 kJ gross / 2.56 kJ net. Its validation note still called Kt "checked only analytic-against-analytic" and A1 "the top roadmap item"; A1 has run and agrees to 0.03 %. |
| STALE-04 | **Counts and per-satellite mass** | 31 numbered defects to **33** in `KILL_CRITERIA.md`, 32 to **33** in `ROADMAP.md`. The 6.41 kg per satellite in `KILL_CRITERIA.md`, `MARKET.md` and `PAYLOAD_CLASSES.md` prose predated the brake-fin correction; `payload_family.json` gives **6.375**. `BASELINE.md` was stamped at `d82877a` while carrying post-`d82877a` values, and is regenerated. |

**What authorised it.** HIST-01 and HIST-02 are record corrections: the repository stated an
incomplete reason for its most load-bearing decision. P33 is a defect in a published claim, which
`docs/BASELINE.md` change control admits as Phase I error correction. No operating point, band or
verdict moved; the ripple loss is four tenths of one percent of the copper budget and the frozen
baseline still holds at 23 values. The STALE items are propagation the 2026-08-03 audit missed.

---

## 2026-08-03: Gen4 open assembly recorded before performance propagation

| ID | Item | Detail |
|---|---|---|
| G4-01 | **The working CAD and the analysed baseline are now separate states** | `EMOCD_Gen4_Open v7` uses the 488 mm sled at s = 300 mm stowed and s = 1200 mm release. The committed STEP, STL, renders, paper and operating point remain the Phase I / Gen3 record. I recorded the split in `docs/GEN4_STATUS.md` instead of attaching the Phase I numbers to new geometry. |
| G4-02 | **The 900 mm stroke reaches the finite stator edge** | The 340 mm Halbach array is fully over the stator only through s = 1051.5 mm. The final 148.5 mm of acceleration is under partial overlap, with 191.5 mm of array overlap left at release. A shortened constant-thrust calculation would not represent the CAD. P32 and E27 keep the missing operating point visible. |
| G4-03 | **Release and brake entry no longer overlap in the provisional stationing** | The fin leading face reaches the brake at s = 1222 mm, 22 mm after the provisional release station. Its trailing face clears the brake at s = 1552 mm, giving 330 mm of interaction travel. This is a geometry result only; brake force, thermal response and arrest remain unvalidated. |
| G4-04 | **The explanatory assembly stays open** | The enclosure is a separate envelope-check configuration. The named operational export selection excludes audit, linked-source, duplicate-brake, construction and released-payload reference occurrences. No Gen4 STEP, STL or render has been exported, and the export gate remains closed pending the finite-stator run. |
| G4-05 | **The twelve-payload stowed manifest is present in Fusion** | Six port and six starboard payload occurrences are present. That closes the missing-occurrence CAD housekeeping item only; it does not establish mass, feed-mechanism or interference closure. |

**What authorised it.** The Fusion configuration changed the geometry on which thrust, release
and arrest depend. I recorded the observed state and its consequences without changing a Phase I
number. ADR-019 keeps the successor assembly separate until the affected calculations are run.

---

## 2026-08-03: full numerical audit corrections

| ID | Item | Detail |
|---|---|---|
| AUD-01 | **Shared thrust quadrature corrected** | The reference model and A1 FEM post-processor both used endpoint-inclusive samples with an unweighted thickness divided by sample count. I replaced that invalid rule with nine-point Gauss-Legendre quadrature. Kt moves 11.22 to **11.03 N per kA/m**, ripple 1.26 to **0.99%**, velocity 16.537 to **16.388 m/s**, and net efficiency 21.16 to **20.99%**. A1 remains PARTIAL on its original two field misses. |
| AUD-02 | **A13 residual-rate conclusion superseded** | Internal mass motion produces transient host counter-rotation and an attitude offset; it does not leave ideal rigid-body rate after the mass stops. Rows 3 and 4 remain FAIL at **0.136 deg/s** for 500 kg and **0.443 deg/s** for 200 kg. Row 7 is VOID. The 8.2 s rate-null and 18.1 s cadence floor do not follow and are superseded. |
| AUD-03 | **A6 bound repaired** | The 3.7e-8 result swept one fixed 5:1:1 covariance shape and was not a bound over all covariance. At the old 14.49 km geometry an anisotropic case reaches 1.67e-4. At the corrected rated geometry, 54.9 km, a one-dimensional Gaussian slab gives a valid covariance-independent upper bound of about **4.4e-5**. P1 remains open because the propagated geometry is fragile and no CDM exists. |
| AUD-04 | **A12 stress plane extended** | The 340 x 90 mm plane omitted fringe stress. A 600 x 220 mm plane converges to **2680.0 N**, within 0.25% of the 2686.6 N volume-force result. The adopted conservative force and five-of-five verdict stand. |
| AUD-05 | **Mass and thermal ownership corrected** | The Gen3 sled already includes the 0.344 kg moving copper brake fin, which the dry-mass rollup counted again inside a 1.20 kg brake lump. Dry/loaded mass moves to **76.5/124.5 kg**. The thermal model also used a 300 mm fin against the CAD's 120 mm; the per-shot adiabatic rise moves from 3 K to **7 K**, and the twelve-shot no-cooling bound is about **85 K**. No between-shot cooling claim remains. |
| AUD-06 | **Old recoil table corrected** | Twelve shots at 65.552 N s are **786.6 N s**, not 0.98 kN s. The paper's host recoil table still carried the older 20.4 m/s operating point even though its caption said 66.1 N s; the rows now use the corrected impulse. |
| AUD-07 | **Evidence language tightened** | A1 and A12 are independent numerical/model-to-model checks. Neither is experimental validation. A7 remains outstanding and its 3.9 deg/s analytic tip-off exceeds the adopted 2 deg/s comparator. The current 1.62 lifetime multiplier has not been independently rerun in GMAT; A5 reproduced the earlier operating point. |

**What authorised it.** Every item above corrects arithmetic, numerical integration, physical
interpretation, geometry ownership, or evidence language against repository inputs. I did not
move any declared acceptance band after seeing a result. FAIL, PARTIAL, VOID, superseded results,
and open hardware requirements remain visible.

---


## 2026-07-31 (fifth pass): costing A13's failure found a wrong cause and a second cadence

| ID | Item | Detail |
|---|---|---|
| FIX-01 | **The disturbance costs cadence, not pointing** | Peak attitude rate during an index cycle threatens nothing — **nothing is fired during an index cycle.** What matters is residual rate *at trigger*, which is settling against the interval. So the failure is priced in seconds of cadence, and that is computable. |
| FIX-02 | **The sled return duration has an optimum, and 6 s was on it by luck** | Settling falls as `1/T` while the return grows as `T`, so `index + return + settle` has a minimum: **18.1 s at a 6.9 s return.** The 6 s originally assumed sits almost exactly there, which nobody designed. |
| FIX-03 | **A published claim fell out of costing it** | `paper.tex` §III-C said *"Cadence is set by supercapacitor recharge, 10–20 s at a 150–300 W allocation."* Recharge is **8.6 s at 300 W** and **17.2 s at 150 W**; the mechanical chain floors at **18.1 s**. **Attitude settling binds at both allocations** and the paper attributed the cadence to the wrong subsystem. The 10–20 s *range* survives, which is why nobody checked — **the number looked right, so the cause went unexamined.** Corrected. |
| P31-01 | **The repository carries two inter-shot cadences and reconciles neither** | `paper.tex` §III-C says **10–20 s**. `analysis/astro.py` models the deployment at **`spacing_s = 1200.0`** — twenty minutes — and the conjunction geometry, realignment period and safety case are all computed at it. **Twenty seconds and twenty minutes, same event, same repository.** Logged as **P31**. |
| P31-02 | **Which one it is decides whether A13 matters at all** | At 1200 s the 8.2 s settling is **0.7 %** of the interval and the failure is irrelevant. At the 18.1 s floor it is **45 %** and it dominates. **The same result is negligible or binding depending on a number that appears nowhere.** |
| FIX-04 | **The three routes, costed** | **Accept the 18.1 s floor**: free if the ConOps cadence is ≥ 18.1 s, and free thirty times over at `astro.py`'s own 1200 s. **Raise host control authority**: 0.5 N·m → 10.2 s floor, but it is a fifth item on a four-item interface spec and narrows the host set the generic-interface positioning depends on. **Counter-mass**: removes the momentum at source and costs **~9.4 kg**, taking 6.41 kg/satellite to 7.2 on a design already failing kill criterion 1. |
| FIX-05 | **The bands stay failed** | Routes 1 and 2 give time to null the rate; they do not reduce it. Bands 3 and 4 asked about the rate itself and **that is still 0.161 °/s at 500 kg**. A legitimate answer to the operational question is not an answer to the declared band. Nothing here touches structural ringing either, which is the other half of E24. |

**What authorised it.** FIX-03 is an error correction to a published claim about which subsystem
sets an operating parameter. P31 records an inconsistency rather than resolving it — resolving it
is a ConOps decision, and re-declaring A13's bands against a 1200 s interval would be a band
change and belongs declared and dated rather than quietly applied to an existing failure.

---

## 2026-07-31 (fourth pass): a band chosen at the easy end, and a mass nobody was watching

| ID | Item | Detail |
|---|---|---|
| P30-01 | **A "discrepancy" three documents gated work on turns out to be two deployers** | `A7_separation_chrono.md`, `KILL_CRITERIA.md` §4 and PII-1's entry criterion all carried a flag that A7's band declares ≤5 °/s citing NRCSD-E while a sibling NRCSD ICD says 2 °/s, unresolved. **Both are right.** NRCSD is the internal ISS-airlock deployer at **< 2 °/s/axis**, flown hundreds of times; NRCSD-E is the external Cygnus-mounted one at < 5, a figure its own publisher describes as *"additional testing and analysis are being completed... to refine and verify this value"*. |
| P30-02 | **What the flag was hiding is worse than what it claimed** | The band was set at the **looser** of two comparators, from the **provisional** document, with nothing recorded about the tighter flown number existing. Nobody chose the easy number on purpose — it is what happens when a band cites one source and no one asks what else that source set contains. **That is the failure mode acceptance bands exist to prevent, occurring inside the band-setting step.** Logged as **P30**. |
| P30-03 | **A7's band tightened to 2 °/s, before the run and not after** | A7 has never run, so there are no results to have tightened it against. `A1_field_femm.md` kept a band it *failed* for exactly the opposite reason. The sheet states the distinction above its own table, because a reader who sees "band changed" and stops there will draw the wrong conclusion. **The cost is real: A7 is now 2.5x harder to pass**, on a release path with no multibody model and a payload CoM 70 mm off the thrust line. |
| P30-04 | **A rule that would have caught it**, added to `validation/README.md` | *When a band cites an external document, record which document, which revision, and whether a tighter comparator exists in the same family.* A band may still be tightened **before** a run; it may never be touched after one. |
| P30-05 | **The spring comparison was softer than advertised** | The same document specifies deployment at **0.5 to 2.5 m/s**. Against the fastest published spring the claim is **6.6x, not 8x**. Corrected in `SUMMARY.md`, `LANDSCAPE.md`, `DESIGN_OPTIONS` and the profile README. |
| A13-01 | **E24 closed, verdict FAIL, four of seven bands** | `astro.py`'s entire host-interaction budget was `4.0 * DV` — the payload's momentum, the shot alone. A13 adds the masses that move *between* shots. |
| A13-02 | **The indexing is negligible and E24 was worried about it** | 0.208 N·s, **0.31 % of the shot impulse**, 0.007 °/s at a 500 kg host. E24's own instinct that a few kg against 124.9 kg would not matter was right. |
| A13-03 | **The sled return is the disturbance, and it is in no budget anywhere** | 9.445 kg over 1.5 m back to the breech: **4.723 N·s, 7.14 % of the shot, 23x the indexing term.** At a 500 kg host that leaves **0.161 °/s** against a 0.05 band, needing **8.2 s** to null against a 2 s band and a 10–20 s cadence. **Nothing inside the cadence passes** — the bands are met only at a 30 s return, which does not fit. |
| A13-04 | **The velocity servo cannot see any of it** | It measures position along the track, not the track's orientation. Residual attitude rate at trigger is a pointing error the 0.027 m/s dispersion figure neither includes nor can detect. |
| A13-05 | **Why E24 missed it, which is the part worth keeping** | E24 came from reading Xu et al., whose deployer moves satellites and **does not return a sled**. The competitor's problem was the indexing; this design's problem is where their paper never had to look. **Reading someone else's problem statement finds their gaps, not yours.** |
| A9-01 | **A9's candidate objects shortlisted so it can run elsewhere** | The block is real and was re-tested: 403 at the CONNECT, logged as a policy denial. What was missing *besides* the data was the object selection, and that needs no element feed. QB50 is the cohort — no propulsion by design, eight of them on PSLV-C38 into the ~505 km SSO A9 specifies. **Aalto-1 (42775) is primary, conditional on whether its plasma brake deployed**; if it did, the sheet's own exclusion rule discards it. InflateSail and QARMAN excluded as drag devices. SATCAT numbers flagged unconfirmed. |

**What authorised it.** P30 is an error correction to how a band was sourced, taken before A7
runs — the only time it could be taken honestly. A13 closes E24, which is a budget published as
complete that omitted a term the hardware will have, the same class as the bank ESR. A9 changes
nothing; it removes an excuse.

---

## 2026-07-31 (third pass): two analyses close, and the run sheets start recording their own results

| ID | Item | Detail |
|---|---|---|
| REC-01 | **A1 and A5 write their results into their own sheets** | Both were pure specifications. A1 ran 2026-07-29 and A5 the same day with verdict **FAIL**, but the outcomes lived only in `OPEN_PROBLEMS.md`, `CHANGELOG.md` and `RESULTS.md`, while A4, A8, A10 and A11 carried theirs inline. `validation/` is the directory this project's credibility rests on and two of its sheets read as unrun. **A run sheet that does not record its own result is not a record.** |
| REC-02 | **The index was wrong about A1 for a day, and the cause is the point** | It said "specified, not run", contradicting `OPEN_PROBLEMS.md` E1 and `ROADMAP.md`. A search of `validation/` for completed runs found the sheets that record their results and missed the two that do not. Corrected, with the reason kept. |
| A12-01 | **P17 closed by a second independent method** | A Maxwell stress tensor integrated over the mid-gap plane gives **2627.6 N** against magpylib's volume integral of the field gradient at **2686.6 N**, 2.2 % apart, sharing only the block model of the magnets. Five of five declared bands. The second method was chosen *because it could disagree*: refining one method's mesh only shows it agreeing with itself. |
| A12-02 | **`sizing.py` adopts 2686.6 N under a rule declared before the run** | Attraction 3.68 → **2.69 kN**, plate stress 33 → **24 MPa**, margin 20.2 → **28.1**. **A4 is not re-run**: it was loaded 37 % heavy, so it is conservative and its verdict stands, and repeating a passing analysis at a lighter load would replace a real result with a weaker one. Its JSON records the overload. |
| A12-03 | **P17's explanation of its own finding was backwards** | It blamed Jensen's inequality. `mean(B²) ≥ mean(B)²` means a one-point form at the **true** mean field *under*estimates — Jensen cannot be why the analytic value is high. The cause is the input: 0.55 T is not the mean normal field on the stress plane, which is 0.4127 T. **x1.776** from the assumed field, **x1.267** back from Jensen, net **x1.402** against an observed **x1.402**. Struck through and corrected in place: a right number with a wrong explanation survives review and then misleads whoever picks it up next. |
| A6-01 | **A6's bands re-declared at the current operating point** | The 2026-07-27 bands are written at **20.37 m/s**, superseded. Running against them would have been **P19** a second time. |
| A6-02 | **A6 runs reduced; three of five bands come back VOID** | No GMAT, no CARA, no Space-Track, so a 2-D P<sub>c</sub> against `astro.py`'s own propagator with an assumed covariance. At 14–63 km miss distances against a hundreds-of-metres sigma, P<sub>c</sub> **underflows double precision**, and a spread of zeros is not a number. Recorded void, the call A10 made on its own row 4. |
| A6-03 | **What it found instead is better than what it asked for** | P<sub>c</sub> has a **maximum over covariance scale** — a covariance wide enough to reach a 14.5 km miss is too diffuse to put probability inside a 5 m disc. **P<sub>c</sub> ≤ 3.7e-8 for any covariance whatsoever, 2700x below the 1e-4 anyone would act on.** So P<sub>c</sub> is not *robust* where distance is fragile; it is **irrelevant**. **P1 stays open** — a bound is not a probability — but the paper's realignment-plus-COLA position is now supported rather than merely honest. |
| SW-01 | **Every current-state count recomputed** | `ROADMAP.md` said 27 problems, 24 E-items, "4 of 9" and "3 of 9" validations, 179 result fields. Actual: **29, 25, 8 of 10, 611**. `KILL_CRITERIA.md` said 27 defects. The README's first screen said FEA was outstanding, which stopped being true when A4 and A1 ran. `SUMMARY.md` said four of nine. |
| SW-02 | **A cwd-relative output path that had already fired** | Every script in `analysis/` wrote to a relative `results/`, so running one from the repository root created a **second, silently stale copy** of its JSON. One had been committed on 2026-07-30 carrying the superseded inter-array force. Removed; all eight now write next to themselves. |

**What authorised it.** A12 is an error correction admitted by `docs/BASELINE.md`, taken
band-first so it does not repeat the procedural failure P17 logs against itself. A6 changes no
baseline value. Everything under REC and SW is documentation catching up with what the scripts
already said.

---

## 2026-07-31 (second pass): the payload ladder, the market case, and the bank as the real constraint

Four pieces of work that share one finding: **the bank, not the winding, is what limits this
machine**, and three separate lines of enquiry arrived at it independently.

| ID | Item | Detail |
|---|---|---|
| PL-01 | **`analysis/payload_family.py`, and the packing counts corrected downward** | `PAYLOAD_CLASSES.md` carried four hand-typed tables whose counts were raw volumetric bounds, published alongside a note that realistic packing is 40–60 % of them and then quoted unadjusted. PocketQube 1P appeared as **546 per load and 0.14 kg per satellite**. The script calibrates packing efficiency against the one configuration laid out in CAD — the 3U case, where a volume ratio predicts 21 and the magazine holds 12 — and applies the same 56.2 % to every class: **326 and 0.236 kg**. `KILL_CRITERIA.md` threat 1 still closes, by 2–5x rather than 6x. The ladder now runs from chipsats to 12U, and classes beyond what a twelve-shot escapement and thermal case support are flagged rather than tabulated as available. |
| PL-02 | **A payload-class subsection in the paper** | Velocity is flat across the family because the sled is most of the moving mass; deployer mass per satellite moves by a factor of thirty. That is the answer to the cold-gas comparison and it turns on payload class, not on any machine parameter. Its three qualifications are in the section rather than beneath it. |
| MK-01 | **`docs/MARKET.md`** | Kept out of the paper deliberately. The number it turns on is not a forecast: of the 4,800-odd nanosatellites catalogued as of January 2026, about **222 carry propulsion**. The other 92 % did not decline propulsion because they had no use for orbital control. The CubeSat market projections are third-party research and the file tabulates five firms disagreeing — 15.6 to 18.3 % CAGR, USD 1.65 to 1.98 B, same market, same year — rather than picking one. Section 5 is where VOLLEY loses. Two sourced sentences and two references into the paper's introduction. |
| LV-01 | **`analysis/velocity_levers.py`, and the ranking inverts** | The lever table was hand-computed on 2026-07-28, before anything modelled bank ESR. The new column is the **highest bank ESR at which each lever's shot still completes**, bisected on the real integrator because the ceiling is set at the sagged voltage, not at 96 V. Two-layer stator draws **597 A and needs 39 mohm**; raised sheet current **749 A and 31 mohm**; as drawn, 347 A and 66 mohm. A single commercial string is 116–185. **No row in the table clears it.** |
| LV-02 | **PII-3 gated behind PII-7, in the entry criterion rather than in prose** | The two levers with the best electromagnetic case are the two that make the bank hardest to buy. `VAULT.md` now says PII-3 may not be reviewed before PII-7 closes. |
| LV-03 | **A modelling error in the old table, found by generating it** | The two-layer rows were reported at 42 A/mm² because nothing told the model the winding got thicker. It runs at 21, the same as today. The 2026-07-28 prose had this right and the arithmetic did not. |
| PI1-01 | **PII-1 re-modelled, and it compounds with regeneration** | Regeneration takes a fixed ~296 J over 240 mm of stator whatever speed the sled enters at, so the spring moves energy to the payload and regeneration takes its slice of what remains. Together: efficiency **21.2 to 31.6 %**, brake duty **1291 to 711 J**. Past what the superseded 4.86 kg design claimed, on a sled twice the mass. **It still defers**, and the file now states why the risk is not comparable to regeneration's. |
| LIT-01 | **The pulsed-power cluster, 2 entries to 29** | PII-7's entry criterion names this gap. Filled by database search rather than reference harvesting, and marked as a **different provenance** inside its own section: where the search did not return volume, issue or pagination, the fields are marked unverified rather than filled in plausibly. Two findings already sharpen P26 — end of life for these parts is a **two-fold ESR increase**, and −40 °C can **double ESR without shortening life**. |

**What authorised it.** PL-01 and LV-01/LV-03 are error corrections: published numbers that
disagreed with their own stated method. MK-01, PL-02 and LIT-01 add documentation and change no
baseline value. PI1-01 quantifies a deferred item and leaves it deferred. Nothing here needed an
amendment.

---

## 2026-07-31: the sled's energy stops being a write-off

A11 asked a question the record had closed without answering. The 2025 arrest decision
established that motor braking cannot *stop* the sled, which is true; five documents and one
docstring had turned that into "the sled's energy is not recovered", which does not follow and
was never argued. Braking regeneratively over the 240 mm the closed envelope allows past the
release point returns 296.6 J, 23.0 % of the sled's 1291 J.

| ID | Item | Detail |
|---|---|---|
| RG-01 | **Bands declared before the sweep, in `6606567`** | Eight of eight held. The one that mattered was "no interior optimum below the winding's rating": the braking pulse is 15.6 ms over 240 mm of stator against the shot's 157 ms over 1300 mm, so copper during regeneration is **15 J against the shot's 828**, and recovery rises monotonically with force to the rating. The intuition that resistive loss defeats regenerative braking is an intuition about long duty cycles. |
| RG-02 | **`motor_model.regen_brake()`, integrating from the shot's own end state** | Exit velocity and post-shot bank voltage are read from `shot()`, never typed, so this cannot be quoted against a stale operating point (P19). Charging solves `R I^2 + Vc I - P = 0`, the mirror of the discharge solve, so the ESR is paid in both directions rather than credited on the way back. `copper_coeff(length)` makes the energised-copper length a parameter, because it is the one modelling choice that moves the answer: the pessimistic 1.30 m convention gives 235.9 J and 20.68 % rather than 296.6 J and 21.16 %, and both sit inside the declared efficiency band. |
| RG-03 | **`sizing.py` follows on all four loss terms** | Brake duty 1291 to **952 J**, winding heat 828 to **843 J**, converter 97 to **113 J**, bank ESR 86 to **94 J**. `energy_closure()` now closes on the *net* draw, 2583 J accounted against 2584.6 J, with the sled's energy split three ways instead of dumped in one. Campaign heat 28.0 to **24.4 kJ**, bulk rise 2.1 to 1.8 K, fin transient 4.0 to 3.0 K. `_check_operating_point()` gained seven regen rows so the two scripts cannot fork. |
| RG-04 | **Exit velocity unchanged, and asserted rather than hoped** | 16.537 m/s. Regeneration acts after release, so it cannot reach back through it; `motor_model.__main__` raises if it does. That was band 6 and it is the one whose failure would have meant a modelling defect rather than a result. |
| RG-05 | **The old claim corrected in place, not deleted** | `DECISION_LOG.md`'s 2025 entry keeps its text and gains an amendment underneath it; `PROJECT_NOTES.md` keeps the line struck through; `RESULTS.md`, `README.md`, `SUMMARY.md`, `wiki/Home.md` and the Pages site each say what they used to say and why it changed. P25 exists because a retraction once reached four artifacts and none of the places asserting it. |
| RG-06 | **Distinguished from the 55 % claim this project already retracted** | A reader who remembers that correction will assume this is it returning. It is less than half the size, it is integrated against stator that has to be built, the copper it burns is subtracted, the brake still absorbs 952 J, and it has a run sheet. `RESULTS.md` says so at the point of the old retraction. |
| RG-07 | **P28 opened: the regen stator and the fin do not both fit** | 240 mm plus a 300 mm fin against a 339 mm arrest section. Thermally trivial, mechanically not: arrest in the remaining ~99 mm needs the eddy coefficient up 1.8x, which puts peak deceleration at 186 g against the 200 g cap protecting the magnet bonds. Logged rather than fixed by shortening `fin_mass` in a script, which is the hand-edit `validation/README.md` forbids. |
| RG-08 | **Paper, figures and baseline follow** | Abstract, prior-art comparison row, architecture, results, thermal and conclusion. `F08_brake.png` now draws both arrest stages from `regen_brake()` rather than a second copy of the physics. `docs/BASELINE.md` goes from 20 to **23 values**, gross and net draw now distinguished. The thermal section's stale 160 J ESR and 28.9 kJ campaign, which the 2026-07-30 propagation missed, are corrected in the same pass. |

**What authorised it.** Two different things, and only one needed authorising. The *analysis* is
an error correction, which `docs/BASELINE.md` admits into Phase I: a published claim was wider
than its evidence. The *design change* is an improvement, which the same rule puts in Phase II,
so it went through `docs/programme/ADOPTION.md` **Amendment 3** with the argument against it
recorded alongside the argument for. The amendment is gated on the bands declared in `6606567`:
had the run missed them, it lapsed.

---

## 2026-07-30 (propagation): the bank's own resistance enters the model

A8-R, the pulse simulation re-run at the current operating point, failed its energy-closure
band at 97.0 %. The gap was bank ESR dissipation, which the circuit deck carried and no
analysis script did. Propagated in the order the standing rule requires: scripts, then
figures, then paper.

| ID | Item | Detail |
|---|---|---|
| ESR-01 | **`motor_model.py` gains `R_ESR = 0.012` and a terminal-voltage current solve** | The load draws its power at the bank terminal, which sits `I*R` below the cell voltage, so the current is not `P/Vc`. Solving `R I^2 - Vc I + P = 0` gives it, the energy leaving the capacitor becomes `Vc*I` rather than `P`, and `I^2 R` is integrated into a new `Q_esr` output. **11 of 179 result fields moved, all electrical or thermal.** Energy drawn 2795.6 to **2881.2 J**, peak current 330.3 to **346.8 A**, sag 5.19 to **5.35 %**, efficiency 19.56 to **18.98 %**, campaign 28.9 to 28.0 kJ. |
| ESR-02 | **Exit velocity, acceleration, stroke time, dispersion, payload family, mass and cost are unchanged** | Checked rather than assumed. The commanded force and the moving mass are untouched, so the mechanical integration cannot move; anything else would have meant the change was wrong. `v_exit` holds at 16.537 m/s and the 3σ dispersion at 0.027 m/s. |
| ESR-03 | **A five-percent disagreement that had been recorded twice and explained wrongly** | A8 and A8-R both put the analytic model about 5 % below ngspice on peak current and attributed it to forward-Euler against trapezoidal integration. It was the missing ESR. Corrected, the model gives **346.77 A against ngspice's 346.8, agreeing to 0.01 %**, energy to 0.04 % and sag to 0.004 points. The number that sets the SiC device rating now has two independent methods behind it instead of one and an excuse. |
| ESR-04 | **`sizing.py` follows, and `energy_closure()` carries the term on both sides** | `E_DRAWN`, `SAG_FRAC` and a new `Q_ESR` constant track `motor_model`; `_check_operating_point()` gained a `Q_ESR` row so the two cannot fork. `thermal_campaign()`'s literal `Q_esr = 160 J`, flagged as unsourced during the P2 review and never sourced since, becomes the computed **85.6 J**: the placeholder was 1.9x high. |
| ESR-05 | **A closing energy budget was hiding the loss, and now says so** | The ledger read 100.0 % closure while omitting a real 86 J term, because the draw it balanced against came from the same model that omitted it. `docs/RESULTS.md` and the Pages site now state that closure tests arithmetic consistency and not physical completeness. This repository had been quoting it as evidence of both. |
| ESR-06 | **A retraction inside the entry that made the claim** | P24 first stated that the correction pushes the 6.0 F bank under its required capacitance, computed by raising energy while holding sag fixed. Energy and sag are the same physical quantity seen twice: evaluated consistently at 2881 J and 5.35 %, required capacitance is **6.00 F** and the bank was always correctly sized. Withdrawn in place. |
| ESR-07 | **Paper, front pages and generated artifacts follow the scripts** | `paper/paper.tex` abstract, results and conclusion; `README.md`, `SUMMARY.md`, `docs/RESULTS.md`, `docs/index.html`, `wiki/Home.md`, `docs/PRIOR_ART.md`, the profile README and the generated CV. `docs/BASELINE.md` regenerated. The energy pie charts gain an ESR slice. |
| ESR-08 | **E17 stays open, on the provenance rather than the modelling** | The 12 mΩ has no current source: it reaches this repository through a superseded computation note, and no cell datasheet has been checked against it. The modelling gap is closed; the sourcing gap is not, and the code comment says so at the constant. |

**What authorised it.** `docs/BASELINE.md`'s change-control rule admits error correction as a
Phase I change. This is one: the model was missing a term that exists in the hardware.

---

## 2026-07-23: reproduction check, paper corrections, repo hygiene

Worked in four phases, with a review at each boundary. Environment: macOS
(arm64), Python 3.9.6 in a local `.venv`, `numpy 2.0.2`, `magpylib 5.0.1`. PDF rebuilt
with `tectonic 0.16.9` (no system TeX was present).

### Phase 1: Reproduction verification (no files changed)

Ran all five scripts in `analysis/` from a clean `.venv` and regenerated
`analysis/results/*.json`. Compared every output against the README headline table and
every value quoted in `paper/paper.tex`. Result: all script numbers reproduce; the paper
disagreed with the scripts in the places already listed as P1, P4, plus one additional
current-density value. No file was edited in this phase. The full comparison
table is kept in the working notes.

### Phase 2: Paper corrections (`paper/paper.tex`)

Rule applied throughout: **the scripts are the source of truth. Where the paper and a
script disagreed, the paper was changed to match the script; no script was edited to
match the paper.**

| ID | Location (section) | Cause | Removed to Added | Source of truth |
|---|---|---|---|---|
| P2-01 | V-C Deployment Safety | **P1.** Quoted conjunction minimum belongs to a superseded operating point AND is not a robust quantity (swings 4.6 to 63 km over ±2.5% ejection velocity). | Removed the "45.3 km minimum / 52 km median / 5.8 km sat-sat / 347 km pre-disposal" framing. Added a reframing around the robust **8.1-day phase realignment**, an explicit statement that the minimum is a near-resonant beat sample (varies "below 5 km to above 60 km"), **mandatory per-shot COLA**, and **host-stage disposal before first realignment** as the mitigation. | `analysis/astro.py` (`conjunction()` to 8.1 d); velocity sweep from `OPEN_PROBLEMS.md` P1 table (4.6-63.4 km). 5.8 km and 347 km were **not traceable** to any current script output and were dropped rather than reconstructed. |
| P2-02 | V-A Launch Performance | **P2.** Peak current belongs to the superseded 130 kA/m point. | `323 A` to `392 A` | `analysis/motor_model.py` `shot()` to `I_peak = 391.7 A` |
| P2-03 | IV-A Field Model **and** XIII EMC | **P3.** Far-field stray values at 20/50 mm did not reproduce (10 mm did). | `4.7 mT` to `4.3 mT` (20 mm); `1.0 mT` to `0.4 mT` (50 mm), both occurrences | `analysis/verify_field.py` to `stray_field {20mm: 4.3, 50mm: 0.4}` |
| P2-04 | III-F Arrest **and** XI Thermal | **P4.** Fin rise stated as 37 K "per shot"; that is the 12-shot campaign-adiabatic total. Per-shot is 3.0 K. | `37 K per shot` to `3.0 K per shot`; 37 K recast as the campaign-adiabatic bound relieved by inter-shot radiation, both occurrences | `analysis/sizing.py` `thermal_campaign()` to `fin_adiabatic_dT_K = 3.0` (x12 = 36.5 ≈ 37 K) |
| P2-05 | IV-B Thrust Constant | Additional discrepancy found in Phase 1: copper current density. Paper's 23 A/mm² is the density at the 140 kA/m *rating*; the script emits the *commanded operating* density. | `140 kA/m (23 A/mm² …)` to `140 kA/m and commanding 126 kA/m (21 A/mm² …)`, corrects the density to the emitted value and removes the 140 kA/m ↔ 23 A/mm² arithmetic inconsistency | `analysis/motor_model.py` `shot()` to `J_Amm2 = 21.0`; `K_nom = 126 kA/m` (`sizing.py` `magnet_temperature`) |
| P2-06 | preamble | **Build bug, not a claim.** `\graphicspath{{figs3/}}` pointed at a directory absent from the repo; the shipped `.tex` could not compile from a clean checkout (figures are in `paper/figures/`). | `\graphicspath{{figs3/}}` to `\graphicspath{{figures/}}` | Repo layout (`paper/figures/`) |

**Not changed, a Phase-1 false flag, corrected here for the record.** The thermal
prose lists "160 J in the supercapacitor ESR." This was initially reported as
unsourced. On reading `analysis/sizing.py` it is the `Q_esr=160` default in
`thermal_campaign()`, consistent with the 23.6 kJ campaign total and with
`energy_closure()` (ESR loss is internal to the cells, additional to the 2630 J
delivered at the bank terminals). **The value is correct; no edit was made.**

#### Figure

| ID | Artifact | Cause | Action | Source of truth |
|---|---|---|---|---|
| P2-07 | `paper/figures/F06_conj.png` | The committed plot was generated by `legacy/make_figs.py` at `dv = 25.0 m/s` (an operating point matching neither the rated 20.37 m/s nor the superseded 20.65 m/s) and headlined a hard "fleet minimum = X km" annotation, contradicting the reframed P2-01 prose. | Regenerated at the rated 20.37 m/s driven by `analysis/astro.py`'s own `propagate()`/`boosted_elements()`; reframed to show the range beat and the 8.1-day realignment, with no single-minimum headline. Only the PNG artifact changed; the generator lives in the working scratchpad, matching the repo convention (committed PNGs, no in-repo figure generators). | `analysis/astro.py` (realign 8.06 d ≈ 8.1 d) |

#### Build

| ID | Action | Detail |
|---|---|---|
| P2-08 | Rebuilt the PDF | `tectonic 0.16.9` compiled `paper.tex` to PDF (749 KB, no errors; only cosmetic underfull-hbox warnings). Written to the canonical `paper/VOLLEY_IEEE_Conference.pdf` (see P3-04). |

### Phase 3: Repository hygiene

| ID | File | Cause | Removed to Added |
|---|---|---|---|
| P3-01 | `analysis/astro.py` (docstring) | The docstring claimed "conjunction min (12 shots) 45.3 km", a stale comment its own code contradicts (computes 4.6 km). Comment only; no computed value changed. | `45.3 km sat-stage, resolved at 0.25 s` to `4.6 km min / 12.3 km median at 20.37 m/s -- fragile`; realignment line annotated as the robust quantity |
| P3-02 | `README.md` | (a) Reproduce command omitted `sizing.py`. (b) "Known issues" described P1, P4 as unresolved. | (a) Added `sizing.py` to the run chain. (b) Rewrote to state the four were corrected 2026-07-23, pointing to this log and `OPEN_PROBLEMS.md`. |
| P3-03 | `docs/PROJECT_NOTES.md` | Ground-rule 3 and the work queue described P1, P4 as open. | Updated both to past tense with a pointer to this log; next open items are E1/E3/E4. |
| P3-04 | `.gitignore`, `paper/` | `.venv/` and the transient `paper.pdf` were not ignored; two PDFs of the same document existed (one stale). | Added `.venv/`, `venv/`, `*.toc`, `*.bbl`, `*.blg`, `paper.pdf` to `.gitignore`. Refreshed `paper/VOLLEY_IEEE_Conference.pdf` with the corrected build (P2-08) and removed the transient `paper.pdf`. |
| P3-05 | `OPEN_PROBLEMS.md` | P1, P4 were still listed as open defects. | Added a top-of-section RESOLVED status block and a per-item "RESOLVED 2026-07-23, see CHANGELOG.md" line. The original defect descriptions are retained in full for the audit trail. |
| P3-06 | `CITATION.cff` | No machine-readable citation metadata existed. | Added a CITATION.cff (author, affiliation, title, TRL/design-study caveat). |
| P3-07 | `LICENSE`, `CITATION.cff` | Owner chose **MIT** (2026-07-23), aware it interacts with the unresolved patent/disclosure question (`OPEN_PROBLEMS.md` E14) and that it only takes effect on sharing. MIT chosen over Apache-2.0 to avoid an explicit patent grant. | Added MIT `LICENSE` (© 2026 Adityavardhan Mishra); set `CITATION.cff` `license: MIT`. |

**Scripts verified to run standalone** from a clean checkout: all five write to
`analysis/results/` via `os.makedirs('results', exist_ok=True)` and require only
`numpy` + `magpylib` (matplotlib/scipy pulled transitively). Run from `analysis/`.
No CI, tests, or other tooling was added.

### Phase 4: Git and GitHub (completed 2026-07-23)

`git init` with a repo-local identity (Adityavardhan Mishra
<adityavardhanmishr@gmail.com>). History was built as four logically separable commits:

1. `Baseline: VOLLEY design-study repo as exported`, 47 files, pre-audit state (original
   paper with the P1, P4 defects intact, so the corrections show as real diffs).
2. `fix(paper): correct P1-P4 and current density against the scripts`, 3 files
   (paper.tex, regenerated F06, rebuilt PDF).
3. `chore(repo): license, citation, audit log, gitignore, doc sync`, 8 files.
4. `docs: add status badges to README`.

Pushed to **https://github.com/aaaaaaaaaaaavm/EMOCD**, created **PRIVATE** and confirmed
private via API (`"private": true`), the analysis scripts disclose the design operating
point and no provisional patent is filed (`OPEN_PROBLEMS.md` E14). **Visibility remains
the owner's decision.**

Repository presentation: set description; added 15
topics (cubesat, electromagnetic-launch, halbach-array, linear-synchronous-motor,
astrodynamics...); disabled wiki and projects, kept issues; added honest static README
badges (MIT license, Python 3.9+, TRL 2-3, "model only, unverified"). No CI or fake
status badges were added. Added `docs/CONTRIBUTING.md` (provenance-first: scripts are the
source of truth, mark verification status, no reconstruction) and a GitHub issue template
for reporting reproduction discrepancies, both matching the repo's existing P-item
discipline. Tagged **v0.1.0** (annotated) and published a matching GitHub release, with
notes stating the design-study / unverified status up front.

---

## 2026-07-23: CAD integration (9 Fusion 360 documents)

Since the paper corrections above, the Fusion 360 CAD was completed (nine documents: Track, Stator, Sled, Payload_3U, Magazine_Cassette, Brake,
Interface_ESPA, **Enclosure (new)**, Assembly). This entry records the import of the
durable CAD artifacts and reconciles the repository's now-stale claims.

**Guardrail honoured: no number in `analysis/*.py` or `paper/paper.tex` was changed.** The
CAD is authoritative for **geometry and fit only**; the scripts remain authoritative for
**mass and performance** until FEA closes the open items. File-size report was reviewed
before committing; nothing approached 50 MB, so Git LFS was not used.

### Artifacts imported

| ID | Path | What | Source | Size |
|---|---|---|---|---|
| CAD-01 | `cad/step/*.step` (9) | STEP exports of all nine documents (8 parts + `EMOCD_Assembly`) | `~/Desktop/EMOCD_figs` | 1.8 MB total (largest: Assembly 1.3 MB) |
| CAD-02 | `cad/renders/*.png` (8) | Render set: `exterior_closed`, `exterior_aft_mounting`, `interior_open`, `exploded_view`, `seq1_stowed`...`seq4_braking` | `~/Desktop/EMOCD_figs` | 1.0 MB total |
| CAD-03 | `cad/parameters.json` | Geometry source of truth, 9 groups incl. the new `enclosure`; ESPA rebuilt as Ø460 ring flange / Ø400 bolt circle / 24 holes / hub / 4 gussets; brake as 15 mm tapered pole plates; envelope recorded as 1839x 530x 940 mm | CAD export (`files.zip`) | 12 KB |
| CAD-04 | `analysis/femm/emocd_cross_section.dxf` | 2-D magnetic cross-section (one wavelength, layers `MAG_*`/`BELT`) for FEMM analysis A1 | CAD export | 1.5 KB |
| CAD-05 | `analysis/femm/FEMM_RUN_SHEET.md` | Run sheet for the FEMM airgap-field check (A1, closes half of E1); distinct from and supersedes the older `docs/FEMM_Run_Sheet.md` | CAD export | 3.1 KB |

All CAD artifacts are **unverified by FEA or hardware** (`cad/parameters.json` itself
carries `PROVISIONAL_PENDING_FEA` flags and an incomplete final-verification note).

### Documentation reconciled (before to after)

| ID | File | Cause | Removed to Added |
|---|---|---|---|
| CAD-06 | `README.md` status line | "No hardware, no CAD, no FEA" is now false | to "CAD complete across 9 Fusion 360 documents with STEP exports committed (`cad/`); FEA and hardware still outstanding" |
| CAD-07 | `README.md` headline table | CAD sled mass (7.50 kg) implies a lower exit velocity than the 20.37 m/s headline, but the chassis is a first-pass 6 mm design with no FEA | Added a ⚠ note: figures assume the 4.86 kg parametric sled and are pending CAD structural reconciliation (P8; provisional ~17.88 m/s). **Computed numbers left unchanged.** |
| CAD-08 | `README.md` layout | New folders undocumented | Added `cad/` and `analysis/femm/` entries |
| CAD-09 | `OPEN_PROBLEMS.md` | P5, P10 absent | Added a "CAD reconciliation" P-section: **P5** sled mass 7.50 vs 4.86 kg; **P6** RESOLVED (CDS corner rails); **P7** brake past the 1500 mm release point; **P8** provisional 17.88 m/s pending FEA; **P9** envelope 1839 mm, ~44% over ESPA Grande; **P10** enclosure/radiator/avionics absent from `mass_properties.py`. Noted launch-lock geometry now exists (advances E10) and CDS corner rails modelled. |

---

## 2026-07-27: archived paper build, live CAD link

| ID | Item | Detail |
|---|---|---|
| ARC-01 | `paper/archive/EMOCD_submission_uncorrected.pdf` | Added an earlier compile of the paper, predating the 2026-07-23 corrections. It still carries the P1, P4 values (323 A peak current, 23 A/mm² at 140 kA/m, 37 K per-shot fin rise, 45.3 km conjunction minimum). Filed under `paper/archive/` with a README stating the deltas, so it cannot be mistaken for the current build. The canonical PDF remains `paper/VOLLEY_IEEE_Conference.pdf`. |
| ARC-02 | `cad/README.md` | Added the Fusion 360 web-view link (https://a360.co/4vSG6cb) under a "Live model" heading, noting that the committed STEP files and `parameters.json` (not the live model) are what the repository stands behind. |
| OP-01 | `OPEN_PROBLEMS.md` | Review pass. **P11 added (NEW):** the archived build still carries all four P1, P4 values and its filename says *submission*, if that is the version of record, P1, P4 are fixed only in this repo and need a corrigendum, not a commit. Flagged UNCONFIRMED pending an answer. |
| OP-02 | `OPEN_PROBLEMS.md` | **E3** retitled and rewritten: the "no CAD" half is closed by `cad/`, but masses are still parametric and unchecked against vendor data, and Fusion masses are proxies (solid copper / solid aluminium / steel for NdFeB) that cannot substitute. Points at P5, P8, P10. |
| OP-03 | `OPEN_PROBLEMS.md` | **E1** updated: the magnetostatic package now exists (`analysis/femm/`, superseding `docs/FEMM_Run_Sheet.md`) but has not been run; A1 closes the 2-D half only. **E2** names the two specified-but-unexecuted analyses (A1, A4). **E10** notes the launch-lock blocks now exist as CAD geometry. |
| OP-04 | `OPEN_PROBLEMS.md`, `CHANGELOG.md` | **E14** rewritten: the repository is public, so the disclosure decision is spent; what remains is the post-disclosure grace-period question and an explicit close-out if no filing is wanted. The stale "repo visibility stays private" open decision corrected to match. |
| OP-05 | `README.md`, `docs/INVENTORY.md`, `wiki/Home.md` | Open-problem summaries synced: P11 added, E1 noted as written-but-unrun, E14 reworded from "unresolved decision" to "disclosure already happened". |

---

## 2026-07-27: validation plan

| ID | Item | Detail |
|---|---|---|
| VAL-01 | `validation/` (new) | Cross-check plan: **A1** airgap field (FEMM), **A4** sled chassis structural (CalculiX/Code_Aster), **A5** lifetime and seeding (Orekit/GMAT), **A6** conjunction probability (NASA CARA), **A7** separation and tip-off (Project Chrono). Each names the P/E item it closes, its inputs from already-committed files, and its output JSON. **Nothing has been run**: this is a specification. |
| VAL-02 | `validation/README.md` | Sets the governing rule: the acceptance band is declared before the analysis runs, and every band traces to a current value in `analysis/results/*.json`. A missed band opens a P-item; it does not get widened. Licence note: GPL solvers stay external to this MIT repo. |
| VAL-03 | `validation/A4_sled_structural.md` | Highest-leverage item. Frames P5 as "what is the lightest chassis that holds the airgap to ±0.05 mm under 3.68 kN" rather than "what does the sled weigh", and fixes the decision rule in advance: ≤5.35 kg the parametric model stands; 5.35-6.80 kg both estimates are wrong and the scripts move; ≥6.80 kg **17.88 m/s becomes the headline** and the paper changes. |
| VAL-04 | `analysis/femm/FEMM_RUN_SHEET.md` | **Stale comparison targets corrected.** Run 3 told the operator to compare stray field against 22.7 / 4.7 / 1.0 mT, the 4.7 and 1.0 are pre-P3 values. Now 22.7 / 4.3 / 0.4 mT per `analysis/results/field_verification.json`. A run sheet carrying superseded targets is worse than none: it would have "confirmed" the wrong numbers. |
| VAL-05 | `docs/FEMM_Run_Sheet.md` | Marked **SUPERSEDED** at the top. Its ⟨B⟩ ≈ 0.62 T winding-gap target predates the winding-resolved model, which computes 0.552 T, so the sheet can no longer function as a test (this is what E1 flagged). Kept for the record. |
| VAL-06 | `docs/RELATED_WORK.md` (new) | Comparator literature and tooling, **explicitly marked as not retrieved and not read**, leads under the E16 rule, not citations. Flags Foster et al. (differential-drag phasing, flown Planet Labs results) as the one worth chasing first, since the paper's 25-day baseline is currently a model output rather than a measurement. |
| VAL-07 | `OPEN_PROBLEMS.md`, `README.md`, `docs/PROJECT_NOTES.md`, `wiki/Home.md` | Cross-references wired: P1 to A6, P5/P8 to A4, E1/E2 to A1, E6 to A5, E7 to A7, E16 to `docs/RELATED_WORK.md`. Layout sections updated for `validation/`. |

---

## 2026-07-27: repository-wide consistency sweep

Swept every committed `.md`, `.tex` and `.json` for values superseded by A27 (efficiency),
A28 (winding-resolved Kt), A29 (servo Monte Carlo), A30 (mass properties) and the P1, P4
corrections. Files that quote old values *deliberately*, `CHANGELOG.md`,
`OPEN_PROBLEMS.md`, `docs/PROVENANCE.md`, `paper/archive/`, `legacy/`, were left alone.

| ID | Item | Detail |
|---|---|---|
| FIX-01 | `docs/EMOCD_Computation_Results_C1-C10.md` | **Marked SUPERSEDED with an old to current mapping table.** It was presented as current computation notes while quoting a 4 kg sled at K = 45 kA/m: 22.4 m/s at 19.7 g, 463 A peak, 3σ 0.054 m/s to ±0.19 km, ⟨B⟩ 0.62 T. Worse, its efficiency line (52 %, crediting 55 % of sled KE as regeneration) is the **falsified** double-count that A25/A27 corrected to 32 %. Nothing deleted; the header states each delta and why. |
| FIX-02 | `docs/INVENTORY.md` | D5 flagged superseded; D8 repointed from `docs/FEMM_Run_Sheet.md` (superseded) to `analysis/femm/FEMM_RUN_SHEET.md` (current) with the band in `validation/A1_field_femm.md`. |
| FIX-03 | `.github/ISSUE_TEMPLATE/reproduction_discrepancy.md` | The worked example cited "paper/paper.tex Sec. V-A to 323 A", a defect fixed in P2-02, so the template implied the paper still carried it. Replaced with a neutral placeholder. |
| FIX-04 | `OPEN_PROBLEMS.md` | **P12 added.** The paper's Limitations section still says masses are "not detailed CAD", and the paper claims an ESPA-Grande-class envelope that P9 contradicts by ~44 %. Prose, not computed values; deliberately **not** edited in `paper.tex`, see the item for why (PDF/source drift, and P11 is unresolved). |
| FIX-05 | `docs/INVENTORY.md`, `wiki/Home.md` | Summaries synced for P11 and P12. |

**Checked and found consistent** (no action): the paper's field values against
`field_verification.json` (0.351 / 0.694 / 0.702 T, 22.7 / 4.3 / 0.4 mT, 0.55 T winding
mean); the paper's mechanical values against `sizing.json` (3.7 kN inter-array, 33 MPa,
9.5 kN arrest, 0.76 kN roller pair, 0.64 kN abort latch, 0.12 MPa bond, 109 Hz first
mode); the README and wiki headline tables against `motor_results.json` and
`astro_results.json`; every file path referenced in the docs.

---

## 2026-07-27: validation plan, second pass

| ID | Item | Detail |
|---|---|---|
| VAL-08 | `validation/A8_pulse_spice.md` (new) | Pulse-power chain under ngspice/PySpice. Bands: 391.7 A ±10 %, 4.88 % sag ±1.5 pts, 2634 J drawn ±5 %, 672 J copper ±15 %, 127.7 ms ±10 %, energy closure 98-102 %. Cheapest analysis in the plan (no geometry, no mesh, no licence) and it attacks three headline-adjacent numbers at once. |
| VAL-09 | `OPEN_PROBLEMS.md` **E17** (new) | The pulse-power chain has never left the analytic model. The 392 A peak, the 4.9 % sag, and the 672 J copper loss all rest on lumped R and ideal switching; no commutation overshoot has been computed, and the `Q_esr = 160 J` default has no second number against it. |
| VAL-10 | `OPEN_PROBLEMS.md` **E18** (new) | Conjunction covariance is invented. Any Pc result inherits it, so no Pc figure may be quoted except as conditional on its assumption until a real covariance is used. |
| VAL-11 | `validation/A5_astro_orekit.md` | Second leg added: reproduce the **measured** decay of 3-5 non-manoeuvring 3U CubeSats from CelesTrak / Space-Track TLE histories, band 15 % on time-to-decay. Two models agreeing is weaker than a model reproducing a flown decay. The 15 % follows published guidance that lifetime prediction tops out near 10 % of residual life. |
| VAL-12 | `validation/A6_conjunction_cara.md` | Covariance input changed from "documented assumption" to **Space-Track CDMs preferred**, assumption as explicit fallback. |
| VAL-13 | `validation/README.md`, `docs/INVENTORY.md`, `OPEN_PROBLEMS.md` E2/E6 | A8 added to the plan table; E-range updated to E1, E18; E2 and E6 cross-referenced to the new legs. |

**Checked, no item raised:** the paper already cites Inductrack (Post & Ryutov, IEEE Trans.
Appl. Supercond. 2000) in both the related-work section and the bibliography, so the
architectural prior art is covered and no E-item was needed for it.

---

## 2026-07-27: GMAT toolkit for A5 (and the A6 ephemeris input)

| ID | Item | Detail |
|---|---|---|
| GM-01 | `validation/gmat/` (new) | Script templates, a builder, and a parser for analysis A5. `emocd_lifetime.script.tmpl` propagates a baseline 450 km circular orbit against the boosted ellipse to a 120 km perigee under MSISE90 / 20x20 gravity / RK89, one script per solar-activity level. `emocd_fleet.script.tmpl` propagates the 12-shot fleet plus host stage for 30 days and writes one CCSDS OEM per object. **Nothing has been run.** |
| GM-02 | `validation/gmat/build_scripts.py` | Fills the templates from `analysis/results/astro_results.json` and **imports `boosted_elements()` and `_kepE()` from `analysis/astro.py`** rather than reimplementing them, so the orbit definition cannot fork between the two codes. Asserts the generated orbit equals `astro.py`'s exactly. Runs with no GMAT installed. Verified: a = 6864.790 km, e = 0.005339269, perigee back at the 450 km injection altitude. |
| GM-03 | `validation/gmat/parse_reports.py` | GMAT `ReportFile` to `validation/results/A5_astro.json`, applying the bands already declared in `validation/A5_astro_orekit.md` (multiplier ±5 %, invariance spread ≤5 %) with an explicit verdict. Exits non-zero on a miss, and the failure text says to open a P-item rather than edit `astro.py`. Absolute lifetimes are recorded but never judged (E6). |
| GM-04 | `validation/gmat/README.md` | Install and headless invocation, with the warning to **verify the run flags against the installed User Guide** rather than assume them, and to record the working command in the results JSON. Documents one real modelling gap: `astro.py` scales density 0.5/1.0/2.5 while GMAT takes F10.7 = 70/150/250, which are not equivalent, it affects the absolutes, not the ratio the band is on. |
| GM-05 | `validation/A6_conjunction_cara.md` | Ephemeris input changed from "export from `astro.py`" to the GMAT-generated OEMs, which replaces Kepler + secular J2 with a real integrator for the conjunction geometry. |
| GM-06 | `validation/A5_astro_orekit.md`, `validation/README.md`, `OPEN_PROBLEMS.md` E2/E6, `.gitignore` | GMAT named as the primary implementation with Orekit as substitute; A5 status now "toolkit built, not run"; `validation/gmat/output/` ignored as regenerable. |

**Scope note.** GMAT closes E6 and feeds A6. It does nothing for P5/P8 or E4, it validates
the consequences of a Δv, not the Δv itself, so A4 remains the highest-leverage analysis
in `validation/`.

---

## 2026-07-28: CAD generations imported, mixed/stubbed STEP set replaced

Source: `EMOCD_figs.zip` (three Fusion generations plus a 543-line `CHANGELOG_CAD.md`
auditing all three by direct Fusion API read). Body counts below were **measured on import**
with `grep -c MANIFOLD_SOLID_BREP`, not copied from the source changelog.

| ID | Item | Detail |
|---|---|---|
| CAD2-01 | `cad/step/` | **The committed set was replaced wholesale.** It matched no single generation and two files were stubs: the stator STEP held **1 solid** where Gen3 holds 162 conductors, and the ESPA interface held **1** where Gen3 holds 6 plus bolt holes. Others were mid-generation (sled 12, track 6, payload 5, assembly 225). Anyone opening the committed stator to check the winding layout would have found a block. Logged as **P13**, marked resolved by this import. |
| CAD2-02 | `cad/step/gen3/` | Current generation: 9 component files plus `EMOCD_Gen3.step`, the monolithic single-file model (395 solids, all nine sub-systems). Stator 162, sled 16, cassette 24, assembly 227. |
| CAD2-03 | `cad/step/gen2/`, `cad/step/gen1/` | Heritage, superseded, kept for the record as `legacy/` already is. Gen1 includes the pre-split `EMOCD_Deployer_Assembly_Gen1.step` and a second sled revision (`Sled_Gen1b`). ~11 MB across all three generations; no LFS needed. |
| CAD2-04 | `cad/CHANGELOG_CAD.md` | Imported verbatim, with a repository verification note added at the top recording what was checked against the exports on import. Nothing in the body was edited. |
| CAD2-05 | `OPEN_PROBLEMS.md` **P14** (new) | Five Gen3 defects that were never tracked here: cassette height 640 mm vs the 690 mm spec (G3-D1); track has no roller channels or guide flanges though `parameters.json` specifies them (G3-D2); stator layer count still open, Gen1 built two layers, Gen2/Gen3 one, and the x2 force vs x2 copper trade is uncomputed (G3-D4); Halbach arrays not re-centred after the chassis grew 360 to 488 mm (G3-D5); no payload-on-sled rigid joint in any generation (G3-D6). ESPA bolt holes recorded as **resolved** in Gen3 (G1-D5). |
| CAD2-06 | Verification findings | **Sled length fix confirmed:** Gen2 chassis half-length measures 180 mm (360 mm plate), Gen3 measures 244 mm (488 mm plate). **Brake placement fix not visible in the exports:** `EMOCD_Brake_Gen2.step` and `_Gen3.step` are geometrically identical (3 bodies and 79 points each, differing only in file name and time stamp) and *both* already place the brake at x = 1530-1740 mm, so the G2-D4 defect is not present in the file said to have it. Minor count deltas: Gen1 payload measures 5 solids where the inventory says 1; `Sled_Gen1b` measures 11 where it says ~16. |
| CAD2-07 | `cad/README.md` | Rewritten: three generations with status, what is authoritative, the six before-use rules, and the stub finding stated plainly rather than quietly fixed. |
| CAD2-08 | `validation/A4_sled_structural.md`, `A7_separation_chrono.md`, `validation/README.md`, `OPEN_PROBLEMS.md` P5 | Inputs repointed to `cad/step/gen3/*`. A4 gains an explicit note that Gen3 is the dimensionally corrected sled, meshing Gen2 would size a chassis that no longer exists. |
| CAD2-09 | `README.md`, `docs/INVENTORY.md` (C6, new C8), `docs/PROJECT_NOTES.md`, `wiki/Home.md` | Summaries synced to three generations with Gen3 current. |

The CAD-01 row in the 2026-07-23 block above described the set committed that day and is
left as written; this block supersedes it.

---

## 2026-07-28: visual pass: renders on the front page, STL viewer, Pages site

The repository had **no images anywhere**: eight 1920x1080 CAD renders and twelve result
figures were committed and shown on no page. Fixed across three surfaces, adding no claim
the repository does not already support and keeping every caveat intact.

| ID | Item | Detail |
|---|---|---|
| VIS-01 | `cad/stl/` (new) | GitHub renders `.stl` natively and does **not** render STEP, so the Gen3 assembly and sled were meshed with `gmsh` (OCC STEP reader) into browser-viewable binary STLs: assembly 50,692 triangles / 2.5 MB at a 40 mm mesh, sled 23,332 / 1.1 MB at 8 mm. `cad/stl/README.md` carries the regeneration command and states plainly that these are derived, non-authoritative meshes. |
| VIS-02 | Mesh verification | Each STL was bounding-box checked against its STEP source on generation. Sled matches exactly at 616x 172x 140 mm; assembly measures 1995 mm in X against a 1998 mm point-cloud bound on the STEP, the 3 mm being spline control points outside their own surface. |
| VIS-03 | `OPEN_PROBLEMS.md` **P14 / G3-D12** (new) | Found while meshing: the Gen3 assembly spans x = −188 to 1810 mm where `parameters.json` records −32 to 1807 mm. 156 mm of geometry sits aft of the recorded envelope, which makes the ESPA overrun ~57 % rather than ~44 %. |
| VIS-04 | `README.md` | Hero render above the badges; a 2x2 render gallery; a Mermaid ConOps flow (feed to gate to accelerate to coast/trim to release to brake to recover); two result figures beside the reproduce section; a validation-status table putting "nothing has been run" on the front page rather than three directories down; links to the spinnable STLs. |
| VIS-05 | `wiki/Home.md` | Same hero, gallery and ConOps diagram, with absolute `raw.githubusercontent.com` image URLs, since wiki pages cannot resolve repo-relative paths. |
| VIS-06 | `docs/index.html`, `docs/.nojekyll` (new) | A single self-contained landing page, dark/light aware, responsive, no framework, no build step and **no CI**, which keeps the "no CI by design" rule in `docs/CONTRIBUTING.md`. Assets are referenced from `../cad/renders/` and `../paper/figures/` so nothing is duplicated. Serves from `main` to `/docs` once Pages is enabled. |
| VIS-08 | `docs/index.html`, **defect fixed same day** | The site referenced its images as `../cad/renders/…`. Pages deploying from `main` to `/docs` publishes **only the contents of `docs/`** as the site root, so every `../` path pointed above the published root and all nine images plus the paper link would have 404'd on the live site while working fine locally. Switched to absolute `raw.githubusercontent.com` URLs, the same approach `wiki/Home.md` already used and for the same reason. |
| VIS-07 | Duplicate render found | `interior_open.png` and `seq1_stowed.png` are **byte-identical** (same MD5). The firing sequence is therefore three distinct frames, not four, and no gallery presents it as four. Worth regenerating a real stowed frame when the CAD is next opened. |

Every number on the new surfaces is copied from `analysis/results/*.json` or the existing
README table, and the P5/P8 caveat travels with the headline figures onto each one. A
prettier page must not become a more confident one.

---

## 2026-07-28: GMAT actually run, and native charts everywhere

| ID | Item | Detail |
|---|---|---|
| A5-01 | **GMAT R2022a installed and run headless** | `GmatConsole` on Linux, no missing libraries. Two script bugs fixed on the way: GMAT rejects any script containing non-ASCII characters with an error that does not name the line (an em dash in a comment), and it resolves relative `ReportFile` paths against `bin/../output`, not the working directory. `build_scripts.py` now guards the first and emits absolute paths for the second. |
| A5-02 | **Bounded 30-day leg** | Fitted decay rate −0.1618 km/day (GMAT) vs −0.1216 km/day (`astro.py`), GMAT decays **1.33x faster**. Expected: static exponential atmosphere vs MSISE90 at F10.7 = 150. Reported SMA is osculating with 12.2 km peak-to-peak short-period variation, several times the decay across the window, so the comparison is a least-squares rate over 31 daily samples, **not** a difference of endpoints. New template `emocd_sma_window.script.tmpl`. |
| A5-03 | **Full decay, high activity, the x1.80 claim holds** | Baseline 144.51 days, boosted 250.03 days, multiplier **1.7302**, deviation **−3.88 %** against the ±5 % band declared before the run. An independently implemented force model reproduces the headline astrodynamics claim. The absolute baseline lifetime does *not* agree (144.5 days vs 190), exactly the 1.33x rate difference, and exactly what E6 says to expect. Mean and low activity still propagating. |
| A5-04 | Parser hardened | `parse_reports.py` read a decay file GMAT was still writing, treated the partial decay as final, and emitted a confident `FAIL`. It now requires the 120 km floor (or the 40-year cap) to have been reached before reporting a multiplier, and distinguishes "not run" from "in progress". Also handles GMAT re-emitting headers mid-file. |
| VIS-09 | `docs/RESULTS.md` (new) | Chart hub, everything drawn by GitHub from text: energy budget (Mermaid `pie`), conjunction fragility, payload family, seeding, stray field, sled-mass decision thresholds, validation dependency graph, and the GMAT comparison. Each chart names the JSON field behind it. |
| VIS-10 | `README.md`, `wiki/Home.md`, `docs/index.html`, `validation/README.md` | Energy pie and conjunction fragility inlined on README and wiki; the Pages site gets pure CSS/HTML bar charts (no images, no JS); validation status tables updated to show A5 as run. |

**No number was invented.** Charts for unrun analyses show an explicit "specified" state; no
placeholder curves, no "expected" lines. The one genuinely new result (GMAT) was produced
by running the tool, not by estimating what it would have said.

---

## 2026-07-28: validation run against every claim

Four analyses actually executed; three could not be. Full account in
[`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md).

| ID | Item | Detail |
|---|---|---|
| VAL2-01 | **Reproducibility, passes** | All five `analysis/` scripts re-run from a clean copy with an empty `results/`, output compared field by field against the committed JSON: **173 values, 173 identical, 0 differing.** The reproducibility claim (D12) holds today. |
| VAL2-02 | **A5 GMAT, the x1.80 claim holds**: ⚠️ **SUPERSEDED 2026-07-28 by A5-01 below: the low-activity run finished and the invariance claim FAILS. The entry is left unedited because it is the audit record of what was believed with two levels of three in hand.** | Mean activity 1.7750 (−1.39 %), high activity 1.7302 (−3.88 %), both inside the ±5 % band declared before the run. **Invariance spread 2.55 %**, inside ≤5 %. An independently implemented force model reproduces the claim the paper actually defends. Low activity still propagating, and early state (4.1 years elapsed, still at 401 km, against `astro.py`'s 2.61-year total) suggests GMAT decays *slower* there, opposite to the other two levels. Not a result until it finishes. |
| VAL2-03 | **A5, absolute lifetimes do not agree, as E6 predicted** | GMAT 144.5 days against `astro.py`'s 190 at high activity. The bounded 30-day window measured the same 1.33x rate difference independently, and 190 ÷ 1.33 ≈ 143 reconciles the two. |
| VAL2-04 | **A8 ngspice, all bands met, two findings** | Exit velocity and pulse duration agree to 0.03 % across two different integrators. **Finding:** `motor_model.py` reports capacitor state-of-charge sag (4.88 %) and models no ESR; terminal voltage droops to 86.16 V, a 10.25 % total sag, and the dispersion claim's headroom argument is stated against the smaller figure. **Finding:** ∫I²dt = 8008 A²s gives 96 J of ESR loss at 12 mohm against the `Q_esr = 160 J` default, consistent only at ~20 mohm. E17 updated; original text kept. |
| VAL2-05 | **P15 (new, HIGH), the sled is heavier than either estimate** | Exact OCC solid volumes from `EMOCD_Sled_Gen3.step` times material densities give **9.445 kg**, against 4.86 kg parametric and the 7.50 kg quoted in P5. Exit velocity falls to **16.53 m/s**. The method reproduces P8's 17.88 m/s exactly when fed 7.50 kg, so the discrepancy is in the mass, not the method. Not the structural FEA A4 specifies (plates are drawn solid, pocketing would reduce it) but past A4's own 6.80 kg threshold either way. |
| VAL2-06 | Tooling committed | `validation/spice/emocd_shot.cir` (A8 netlist), `validation/results/A5_astro.json`, `validation/results/A8_pulse.json`. |

**Not run, and recorded as not run:** A1 (FEMM is Windows-only; no magnetostatic solver was
set up, so Kt = 11.22 N per kA/m remains single-method), A4's structural half, A6 (needs a
covariance that does not exist, E18), A7 (Project Chrono unavailable here). Nothing in this
block is inferred from an analysis that did not happen.

**No script or paper value was changed.** The standing rule applies: record the discrepancy,
run the analysis, then propagate once.

---

## 2026-07-28: exit-velocity options, and where this sits against what flies

| ID | Item | Detail |
|---|---|---|
| OPT-01 | `docs/DESIGN_OPTIONS_exit_velocity.md` (new) | Every lever for recovering 20.37 m/s at the CAD-derived 9.445 kg sled, computed by driving `motor_model.py` with modified inputs, the repo's own field model and integrator, no new physics. **Marked exploration, not a result.** Mass reduction alone tops out at 18.68 m/s with 60 % of the titanium pocketed. **Thinning the magnets moves backwards** (6 mm gives 15.68 m/s) because the Halbach field decays as e^(-ky) faster than the mass comes off. Raising sheet current to 213 kA/m works at J = 31.9 A/mm² against 21 today. Lengthening the stroke to 1.97 m works and adds 673 mm to an envelope already 44 % over ESPA. |
| OPT-02 | Two-layer stator costed for the first time | Doubling the winding widens the magnetic gap 12 to 22 mm and drops Kt from 11.22 to 7.46 N per kA/m, but sheet current doubles at unchanged current density: **20.61 m/s at 7.50 kg, J still 21 A/mm²**. The stator does not ride the sled, so its copper costs dry mass (P10), not velocity. Costs: copper loss doubles, peak current ~580 A against 392, which collides with the A8 ESR finding. This is the first time G3-D4's open decision has had its electromagnetic consequence computed. |
| OPT-03 | Reconciliation hypothesis for P5 vs P15 | Pocketing 40 % of the titanium gives 7.50 kg and 17.88 m/s, **exactly** P5's and P8's figures. The 7.50 kg may never have been the as-drawn mass but an estimate with lightening assumed, in which case P15 and P5 are the same design before and after pocketing. Flagged as an inference to check against the CAD Master Plan, not as a finding. |
| LAND-01 | `docs/LANDSCAPE.md` (new) | Comparison against fielded deployers (P-POD, ISIPOD, NRCSD, CSD, EXOpod) and transfer vehicles (ION, Vigoride). VOLLEY carries **6.0 kg of deployer per 3U satellite** against roughly 2 kg per U for canisterized dispensers, the same mass class, which is the genuinely favourable result. Against that: tip-off and dispersion advantages are **unproven** (A7 unrun, E7 assumed sensor noise), springs need no power at all, and the machine does not currently deliver the velocity it advertises. Competitor figures are marked unverified under the E16 rule. |

No script or paper value changed.

---

## 2026-07-28: A4 structural run, and the front pages corrected to match

| ID | Item | Detail |
|---|---|---|
| A4-01 | **A4 structural leg RUN** (CalculiX ccx 2.21) | Quadratic-tet FE of one 488x140x6 chassis plate taken straight from `cad/step/gen3/EMOCD_Sled_Gen3.step` (29,312 nodes, 143,930 C3D10) under the 3672 N Maxwell attraction from `sizing.json`. Support bracketed pinned vs clamped because the real web joint is between. **All three declared bands pass: 0.0194 mm airgap closure against a 0.025 mm per-plate budget (78 %), 33.7 MPa against 587 allowable (17x margin), first mode 3408 Hz against >200.** |
| A4-02 | What A4 did *not* settle | It answers "does the drawn chassis meet the constraint" (yes) rather than "what is the lightest chassis that does". Uniform thinning is nearly worthless, deflection goes as 1/t³, budget spent at ~5.5 mm for 0.30 kg, moving exit velocity 16.53 to ~16.7 m/s. Real reduction needs a rib-stiffened redesign that nothing has evaluated, so the 60 % pocketing row in `docs/DESIGN_OPTIONS_exit_velocity.md` is **unsupported**. The decision rule's ≥6.80 kg branch stands. |
| A4-03 | Deck bug worth recording | First run failed with `nonpositive jacobian` on every element: gmsh's tet10 edge order is `{0,1},{1,2},{2,0},{3,0},{3,2},{3,1}` and CalculiX C3D10 wants nodes 9 and 10 the other way round. `build_deck.py` carries the mapping and a comment so the next person does not lose an hour to it. |
| A4-04 | `validation/fea/` (new) | `build_deck.py` regenerates both decks from the STEP; results in `validation/results/A4_sled_structural.json` with mesh, material, load, bands, and five stated idealisations. Run artifacts gitignored. |
| DOC-01 | **README, wiki and the Pages site now lead with the real number** | All three previously headlined 20.37 m/s with a caveat about a provisional 17.88, while `docs/VALIDATION_REPORT.md` said 16.5. A reader finding that gap themselves reads it as overclaiming; the front page saying it first reads as rigour. Each now carries the three-row mass/velocity table and the sentence "treat 20.37 m/s as an upper bound the current geometry does not support". The computed values are still left exactly as the scripts produce them. |

The standing rule held throughout: **no script or paper value was changed.** Discrepancy
recorded, analysis run, and the propagation into `analysis/*.py` still waits on a decision
about the chassis and the stator layer count.

---

## 2026-07-28: A5 completes, and falsifies the claim the paper calls its defensible one

| ID | Item | Detail |
|---|---|---|
| A5-01 | **A5 GMAT complete, verdict `FAIL`** | The low-activity leg finished: baseline 2359.1 d, boosted 4892.4 d, **multiplier 2.0739, +15.21 % against x1.80**, outside the ±5 % band. With high (1.7302) and mean (1.7750), the **invariance spread is 18.48 % against a ≤5 % band declared before the run.** The point value survives at mean and high activity; the *invariance* does not. `validation/results/A5_astro.json` regenerated and carries the FAIL. |
| A5-02 | **Mechanism identified and tested, not guessed** | `astro.py` models solar activity as a uniform multiplicative scale on density. Sweeping that scale over **40x** (0.25 to 10.0) moves the multiplier only 1.7992 to 1.7968, constant to 0.1 %. A uniform density factor divides both lifetimes by the same number, so **the ratio is invariant by construction of the model, not as a physical result.** MSIS changes the shape of the density, altitude profile with F10.7, the boosted orbit's apogee sits ~37 km higher, and the ratio then moves 1.73 to 2.07. Reproducible from `analysis/astro.py` `lifetime()` unedited. |
| A5-03 | **`OPEN_PROBLEMS.md` P16 (new, HIGH)** | Records the falsification, the 40x sweep table as evidence, and every location the claim appears, including the **abstract** of `paper/paper.tex` ("invariant across ballistic coefficient and a fivefold solar-activity density range"), Sec. V-B ("invariant to two decimal places") and Limitations, which calls the invariance "the defensible result". E6 updated: it warned the absolutes were weak, and now has to say the ratio is weaker than advertised too. |
| A5-04 | **Absolute-lifetime error changes sign** | GMAT is **2.5x longer** than `astro.py` at low activity, **9 % shorter** at mean, **23 % shorter** at high. E6 predicted absolute disagreement; it did not predict a sign change across the range. Same profile-shape effect, seen from the other side. |
| A5-05 | **Correction to my own text in `docs/VALIDATION_REPORT.md`** | Section 2 read "Invariance across activity: 2.55 % spread, inside the ≤5 % band" and "the claim the paper actually defends survives an independent propagator". Both were computed from two levels before the third finished, and both were wrong. Replaced with the three-level result and the mechanism, and the retraction is stated in place rather than quietly overwritten. |
| DOC-02 | Front pages corrected | `README.md` and `wiki/Home.md` headline rows now read "x1.80 at mean activity, **invariance falsified, see P16**" instead of "invariant across BC and solar activity"; README's validation summary rewritten around the four run analyses. `docs/RESULTS.md` A5 section replaced with the three-level table, a per-activity chart and the 40x-sweep chart; its status bar moved from `████████░░` "within band" to `██████████` **FAIL**. `docs/INVENTORY.md` A32 flagged against P16. |
| A5-06 | **`paper/paper.tex` deliberately not edited** | Four locations are affected (abstract, Sec. V-B, sensitivity, Limitations). Same reasoning as P12: no TeX engine is available here, editing without rebuilding splits the source from the committed PDF, and it is entangled with **P11**: which this makes urgent, because if the submitted build is the uncorrected one, the paper of record carries P1, P4 *and* a falsified abstract claim. Batched for one pass. |

Standing rule held: **no value in `analysis/` was changed.** The parser's own instruction on
a failed band is explicit (*"open a P-item; do not edit `analysis/astro.py`"*) and that is
what happened.

---

## 2026-07-29: review sweep: two falsifications, one new lever, four missing model terms

Three independent reviews of the repository, each verified against the code rather than the
prose before anything was written down. Every number below was recomputed here.

| ID | Item | Detail |
|---|---|---|
| REV-01 | **P16 extended, the BC half of the abstract is the same tautology** | The abstract claims the ratio is invariant across ballistic coefficient **and** solar activity. In `lifetime()` the drag term is `ft = -0.5 * rho(h, scale) * v**2 / BC`, so `scale` and `1/BC` are the **same multiplicative slot**. Reciprocal test: BC=61/scale=2.0 gives 1.7987 and BC=30.5/scale=1.0 gives **1.7987**; BC=122/scale=1.0 gives 1.7991 and BC=61/scale=0.5 gives **1.7991**. Plain BC sweep 30 to 150 kg/m²: spread **0.05 %**. So the position is not "one half falsified, one half untested", **neither half was ever tested by a method that could fail**, and the half that was independently checked did fail. |
| REV-02 | **P17 (new, HIGH), the A4 load input is 37 % high** | `sizing.py::inter_array_attraction()` gives 3672 N from a flat-plate Maxwell-stress formula; that number was the applied load in the CalculiX run. `magpylib.getFT()` on the repo's own `build_field()` geometry converges to **2686.6 N** (mesh (14,14,14), deltas −8.3/−4.3/−2.5 N, step-size independent 1e-5 to 1e-8). Mechanism: Maxwell stress needs mean(B²), the formula uses mean(B)², and mean(B²) ≥ mean(B)² by Jensen, so the analytic form must overestimate a non-uniform Halbach face. **A4's conclusions do not reverse** (the real load is lighter, margins widen); what fails is the claim that A4's inputs were checked. |
| REV-03 | `validation/magpylib/check_inter_array_force.py` (new) | Reproduces P17 in one command, no new dependency, magpylib 5.2.3 is already in `requirements.txt`. Documents the 3672 vs 3680 N provenance (`build_deck.py` multiplied the rounded 120.0 kPa by the footprint). |
| REV-04 | **Momentum-transfer release costed, a lever absent from the options table** | Every option costed so far accelerates sled and payload as one rigid mass. They need not separate at the same speed. A momentum-conserving spring push recovers the full headline shortfall for **41.8 J against a 2630 J shot (1.6 %)**, and brake duty *falls* 1291 to 1050 J. The binding constraint is the payload's 25 g qualification limit, not energy: at 25 g the kick is **15.6 ms over 42.7 mm of relative stroke at 981 N**, an ordinary spring, not a shock event. Against the stroke-lengthening row, which needs **673 mm** more envelope on a machine already 44 % over ESPA, this needs **43 mm** of guided rail. Written up as **exploration, not a result**; the tip-off objection is real and makes A7 load-bearing. |
| REV-05 | Mission-value framing added to the re-scope option | A **23 % velocity shortfall costs 9.7 % of the lifetime multiplier**, x1.624 at the as-drawn 16.54 m/s against x1.799 at 20.37. The re-scope case had been argued only in m/s, where it looks like a collapse. |
| REV-06 | **E19, E22 (new), four terms no script contains** | Distinct from "analysis not yet run". **E19** eddy-current heating *inside* the NdFeB blocks (`magnet_temperature()` models only reversible Br drift; the risk is irreversible knee-point demagnetisation, and it grows with the current-density option). **E20** the brake's force, time profile does not exist anywhere, only a 200 g cap used for bond sizing; a first-order estimate puts the average near 6 kN over 8-20 ms, ~4x the acceleration force, 24 load reversals per campaign through the ESPA joint. **E21** no vacuum tribology anywhere in the repo, four rollers at ~763 N per pair, reused twelve times, cold welding and galling unaddressed. **E22** parasitic eddy drag on track structure during acceleration; `thrust_constant()` models eddy coupling only where it is wanted. P18 added so these are visible from the P-list. |
| REV-07 | **Dhruva Space added to `docs/LANDSCAPE.md`** | The closest fielded comparator is Indian and was absent. DSOD family space-qualified on PSLV-C55 (22 Apr 2023), non-pyrotechnic HDRM, **< 2 m/s**, and (pointedly) **onboard telemetry for ejection-velocity measurement**, which is the quantity VOLLEY claims as its differentiator and currently has only as a model output. Deployer unit mass could not be retrieved (403), so no mass comparison is made; marked unverified under E16. |
| REV-08 | **A7's pre-declared acceptance band may be mis-sourced** | `validation/A7_separation_chrono.md` declares ≤5 °/s citing NRCSD-E. Snippets of the sibling NRCSD ICD (NR-SRD-029) give "less than two (2) deg/sec/axis" verbatim; the NRCSD-E PDF 403s so the variant is unconfirmed. **Flagged, not asserted**: but a band declared before a run is no protection if the band itself misquotes its source. To be checked by hand before A7 runs. |
| REV-09 | Two "blocked" verdicts corrected as overstated | **A1:** FEMM 4.2 runs under Wine (documented by the FEMM project; `py2femm` automates it), and Elmer / GetDP+Gmsh are native-Linux meshed FEM, a not-yet, not a cannot. **A7:** `pychrono` ships on conda-forge, not PyPI, so `pip install pychrono` fails by design; linux-64 is supported. Both corrected in `docs/VALIDATION_REPORT.md`. Recorded against them: for an *ironless* geometry magpylib's analytic superposition is essentially exact and already 3-D, so the weak link was never the field model, it was the closed-form expressions on top of it, which is exactly what P17 caught. **Radia is not worth pursuing** for A1; same solver family, no independence gained. |
| REV-10 | References upgraded from lead to verified | Foster et al. **both companion preprints are open-access** (arXiv 1806.01218, 1509.03270), so the highest-value modelled to measured swap has no paywall. Shambaugh, arXiv 2601.02453 (Jan 2026), verified: backtests lifetime prediction against **934 non-manoeuvring decayed satellites, 1961-2024**, reporting 12.4 % median error under fully predictive conditions. That supplies the accuracy band **E6 never had**: GMAT and `astro.py` differing 9-23 % on absolutes is near the state-of-the-art floor, not evidence either is broken, and it independently corroborates P16's mechanism by naming solar-cycle forecast error as dominant after ballistic coefficient. |
| REV-11 | A6 tooling risk removed | The 2-D Pc algorithm is a published closed-form integral, ~50 lines against the already-installed `scipy`, applied to the OEM ephemerides `validation/gmat/` already emits. No MATLAB, no Octave port. E18's covariance problem is untouched either way. |

**No value in `analysis/`, `cad/` or `paper/` was changed.** P17 in particular is logged as a
discrepancy rather than a correction, and it carries an explicit instruction not to edit
`sizing.py` on the strength of it, adopting a corrected formula would move the plate stress,
the retention-gate sizing and the A4 load together, and that is a propagation decision, not a
patch.

**Stated plainly because it inverts this project's own rule:** the P17 force was computed
*before* an acceptance band was declared for it. That is the wrong order, it is recorded as
such in the P-item, and proper closure still needs a run sheet with a band fixed in advance.

---

## 2026-07-29 (later): P11 resolved, and one review finding that was missed

| ID | Item | Detail |
|---|---|---|
| REV-12 | P11 RESOLVED, nothing has been submitted | Checked. There is no version of record, so P1, P4 are not loose in any published document and no corrigendum or erratum is needed. `paper/archive/EMOCD_submission_uncorrected.pdf` is a draft whose filename overstates its status. |
| REV-13 | **The paper edits are no longer blocked** | P12 and P16 were held out of `paper/paper.tex` because editing the source without rebuilding would split it from a published record. With nothing published, the only cost is a stale committed PDF until recompilation, a normal state for a draft. **Both should now be fixed in the source and the PDF rebuilt before any submission.** |
| REV-14 | **E23 (new), a review finding not covered by E19, E22** | `track_first_mode()` gives 48 Hz pinned / 109 Hz fixed and checks them only against a static launch-band target. The shot's own excitation sweeps from zero as `f = n·v/λ`, so every shot chirps through both modes: the 6th harmonic crosses 48 Hz at 3.7 ms and 0.7 mm of travel, and 109 Hz at 8.3 ms and 3.6 mm; the fundamental crosses 109 Hz at 49.8 ms. Twelve times per campaign, in the first millimetres of stroke. Probably benign (the sweep rate is ~2190 Hz/s, so transit is sub-millisecond) but that argument needs the structure's Q, and **no damping figure appears anywhere in the repository**. |

---

## 2026-07-29 (propagation): the first time a script value has moved

P11 resolved (nothing has ever been submitted) which removed the reason `paper/paper.tex`
was frozen. The CAD-derived sled mass was then propagated in the order the standing rule
requires: **scripts, then figures, then paper.**

| ID | Item | Detail |
|---|---|---|
| PROP-01 | **`analysis/` adopts the CAD-derived 9.445 kg sled** | Authorised by the rule in `validation/A4_sled_structural.md` declared *before* A4 ran: at ≥ 6.80 kg the headline changes and the paper changes materially. A4 has since run, all three structural bands pass, and P15 gives **9.445 kg** from the Gen3 STEP solid volumes. **55 of 179 result fields moved.** Exit velocity 20.372 to **16.537 m/s**, acceleration 16.26 to **10.72 g**, efficiency 31.5 to **19.6 %**, energy 2634 to 2796 J, copper loss 672 to 828 J, peak current 392 to 330 A, pulse 128 to 157 ms, multiplier x1.80 to **x1.62**, recoil 81.5 to 66.1 N·s, realignment 8.1 to 9.9 d, dry mass 72.3 to 76.9 kg. |
| PROP-02 | **The closed-loop Monte Carlo had silently saturated** | Its 20.0 m/s setpoint now sits above the open-loop ceiling, so `Kc` pinned at `K_RATED` and the run reported a 0.267 m/s "dispersion" that was really a 2.27 m/s shortfall. The setpoint moved to **16.2 m/s (98.2 % of the ceiling, the same fraction 20.0 held against the old 20.37**) so the headroom argument is unchanged rather than re-tuned to taste. Dispersion returns at 0.027 m/s. A guard now raises if the servo ever fails to reach its setpoint again. |
| PROP-03 | **Loss terms were pasted literals** | `sizing.py` hard-coded 672 J copper and 26 J auxiliary, so energy closure fell to 94.2 % on the first run after the change. They now derive from the operating point; closure is back to **100.0 %**. |
| PROP-04 | **Capacitor sizing quoted a droop the bank no longer meets** | 5.97 F was computed against a 4.9 % sag target; at 2795.6 J, holding 4.9 % needs **6.35 F**, which the selected 6 F bank does not provide. It sags 5.19 % instead. The function now derives from the sag actually reached, returns 6.0 F against 6 F selected, and reports the 6.35 F alternative rather than hiding it. |
| PROP-05 | **A fork guard, because the operating point was duplicated** | `M_SLED`, `V_EXIT`, `E_DRAWN`, `F_CMD` lived in both `motor_model.py` and `sizing.py`. `sizing.py` now asserts agreement against `motor_model`'s own JSON on six quantities and exits with a diagnostic if they drift. `mass_properties.py` keeps the parametric sled breakdown and carries the 4.59 kg CAD-reconciliation delta as its own line, so system dry mass no longer understates. |
| PROP-06 | **`paper/make_figures.py` (new)** | The committed figures had **no generator in the repository**: `legacy/make_figs.py` is at a superseded point and reimplements the physics instead of importing it, so the figures could not follow the operating point. All ten now regenerate from `analysis/`, with trace accessors added to the analysis modules (`shot(trace=True)`, `thrust_constant(profile=True)`, `conjunction(trace=True)`) rather than the physics copied into figure code. |
| PROP-07 | **F11 reframed, F09 given both bands** | F11's caption asserted the falsified invariance; it now plots `astro.py` against GMAT side by side, which shows P16 directly, the script series is flat across the whole activity range while GMAT moves 2.07 / 1.78 / 1.73. F09 draws both the 5 °/s line the paper cites and the 2 °/s wording in the sibling NRCSD ICD, since which applies is unresolved. |
| PROP-08 | **`paper/paper.tex` follows the scripts** | Abstract, results, family table, comparison and sensitivity tables, mechanical, thermal, cost and conclusion. Sec. III is *rewritten*, not renumbered: the design used to be acceleration-limited and is now thrust-and-mass limited with more than half its qualification margin unused, which changes what recovering velocity means. Sec. V-B drops the invariance claim and explains the defect. Limitations no longer offers that invariance as the defensible result. |
| PROP-09 | **P12 closed** | The ESPA-Grande envelope is no longer asserted as a capability, 1839 mm against ~1270 mm is stated and named an open packaging problem (P9). "Masses derive from a parametric solid model, not detailed CAD" is replaced by what the CAD solid-volume calculation gives. |
| PROP-10 | **A pre-existing build defect fixed** | `\ref{sec:opt}` pointed at a section that has never existed and would have rendered as "Sec. ??". The length trade it promised is now stated inline from `sizing.py`'s own sweep. |
| PROP-11 | **P19 (new, HIGH)** | Every validation run predates the operating point it validates. A5 and A8 were propagated at 20.37 m/s; A4 survives because its load is magnetostatic and velocity-independent. "Three of eight analyses have run" is really "three have run against a design that has since moved". |
| PROP-12 | **P5, P8, P15 closed; each keeps its original text** | P5 carries a caveat forward: 9.445 kg is the as-drawn, unpocketed geometry and A4 reports a 17x stress margin, so a rib-stiffened chassis would recover mass and nobody has designed one. That successor question moves to E2 and the roadmap. |
| PROP-13 | **`docs/ROADMAP.md`, `SUMMARY.md` (new); contact details** | Nineteen numbered defects only read as rigour if there is also a plan for closing them; without one a reader cannot tell mid-flight from abandoned. A1 is sequenced first because Kt is checked only analytic-against-analytic and everything is downstream of it. Dates are assumed from a standard Indian final-year calendar and the header says so. Contact details previously existed only in `CITATION.cff`. |
| PROP-14 | **Host-integration work surfaced** | The POEM and Vikram-1 analysis was at line 245 of the LaTeX, the most India-specific engineering in the project, invisible from the front page. Now in `README.md` and `SUMMARY.md`. |

**The committed PDF is knowingly stale.** No TeX engine is available in this environment, so
`paper.tex` was revised without recompiling. `paper/README.md` declares the divergence and
says how to rebuild; a silent split between source and PDF would be worse than either being
wrong alone.

---

## 2026-07-29 (blockers and gaps): three blockers cleared, three gaps closed

Re-checking the standing blockers found three of four had changed status. The environment,
not the problem, had been the obstacle.

| ID | Item | Detail |
|---|---|---|
| BLK-01 | Git history tidied | `git-filter-repo` installs from PyPI, so the rewrite that was previously blocked ran. A stray working-notes file was dropped from the three commits carrying it, and one commit message reworded. Verified: 37 commits preserved and the **tree hash byte-identical before and after** (`1435acc`), so no content moved, only history. Force-pushed with `--force-with-lease` against the recorded prior head. |
| BLK-02 | **PDF rebuilt** | TeX Live 2023 installs from apt (`texlive-latex-base`, `-latex-recommended`, `-fonts-recommended`; `-latex-extra` is unnecessary and pulls a broken dependency set). `pdflatex` run twice: **10 pages, zero undefined references, zero missing figures.** Verified the build came from corrected source, the PDF reads 16.5 m/s, states the ESPA envelope as unmet, and its only mentions of 20.4 m/s and of invariance are the explicit historical ones. `paper/README.md`'s stale-PDF notice removed, which is what it existed for. |
| BLK-03 | **Wiki push still blocked** | The wiki remote now *clones* (it holds a 1-line placeholder against the repo's 227-line `wiki/Home.md`) but pushing returns `403`. Reads permitted, writes denied. Reported, not worked around. |
| BLK-04 | **`xychart-beta` confirmed rendering** | No chart work needed. |
| BLK-05 | **Tag pushes blocked** | Six annotated tags created locally; `refs/tags/*` pushes return `403` while `refs/heads/*` succeed. The remote's pre-existing `v0.1.0` now points at a commit the rewrite removed and cannot be updated from here. |
| GAP-01 | **`analysis/cost.py` (new), and it contradicts the paper** | Parametric BOM driven by `mass_properties.py`'s own part list, imported rather than re-entered. **Every price is an assumption and the file says so in its first paragraph.** The paper claimed recurring hardware "is dominated by the magnet set and the SiC drive". It is not: **avionics 23.7 %, supercapacitors 17.8 %, SiC 13.3 %, NdFeB 4.8 %.** Doubling the magnet price still leaves it under a tenth of the total, so the ordering survives the price uncertainty even though the ₹1.35 M total does not. **This machine is an avionics and energy-storage cost problem, not a magnetics one**, the opposite of where the design effort has gone. Paper corrected and rebuilt. |
| GAP-02 | **`docs/QUALIFICATION_PLAN.md` (new)** | Eight tests, T-1 to T-8, against GEVS and the CubeSat Design Specification, each naming the item it closes and its pass criteria. Two have no spring-deployer counterpart: T-6 measures static field at the payload envelope, and T-7 instruments a mass simulator to test whether "unmodified CubeSat" is true. Flags T-1 as the most likely failure, the track's first mode is 48 Hz pinned and 109 Hz fixed against a 70-100 Hz convention, and the as-built joint is between the two. |
| GAP-03 | **`docs/BENCHTOP_TESTS.md` (new)** | Four sub-scale experiments, cheapest first, **bands declared in advance** as `validation/` does. B-1 (Halbach pair on a gaussmeter) costs about two magnets and would be this project's first measured number. Bands are deliberately wide where the model deserves no better (±40 % at 20 mm stray field, order-of-magnitude at 50 mm) and B-3's ESR row carries **no** band, because declaring one around a number no script commits to would be inventing a target. |
| GAP-04 | **`validation/A9_tle_decay.md` + `validation/tle/fit_decay.py` (new)** | Decay rate against element-set histories of real decayed 3U CubeSats, **the only analysis specified anywhere that compares the model against something that happened** rather than against another model. **Specified, not run:** CelesTrak and Space-Track return 403 on CONNECT under this environment's network policy. Script committed unrun; its offline half is verified (`model_rate` returns −121.6 m/day at 450 km, matching A5's independently measured −0.1216 km/day). Band set at ±40 % on the median because Shambaugh's backtest puts state-of-the-art at 12.4 %, holding a static exponential atmosphere tighter than that would guarantee a meaningless failure. |
| GAP-05 | Limitation recorded rather than hidden | `fit_decay.py`'s `model_rate` runs at mean activity regardless of what each object's decay window experienced, because `cowell_sma_after()` takes no density scale. An object that decayed near solar maximum will look like a model failure when it is partly an activity mismatch. Documented in the function's own docstring. |

---

## 2026-07-29 (governance): the Engineering Programme adopted, four repositories stood up

The Engineering Programme Dossier v1.0 and TRB Prompt v1.0 now govern this project. A review
against both found six gaps; all are closed here. **This entry adds documents and zero
engineering**, right once, because the dossier asks for exactly this before new concepts, but
it must not become the pattern. The next work is A1.

| ID | Item | Detail |
|---|---|---|
| GOV-01 | **Governing documents committed verbatim** | `docs/programme/`. They existed only as uploads; a repository whose authoritative record lacks the document governing it has a hole exactly where this project claims strength. |
| GOV-02 | **Two amendments recorded, not buried** | `docs/programme/ADOPTION.md`. §3 designates repos 2-4 *Future* and we created them; §9 defines no Phase II promotion route and we added one. Both carry authorisation, reasoning, and the risk they create. **The dossier itself is not edited**: a governing document that quietly changes to match practice is not governing anything. |
| GOV-03 | **`docs/BASELINE.md`, generated, not typed** | `tools/make_baseline.py` reads 20 values from `analysis/results/*.json`. A hand-typed baseline is a set of numbers that can silently disagree with the scripts, which is the defect class this repo logs twice (P16, P19). `git diff --exit-code BASELINE.md` after regeneration is now a real check. |
| GOV-04 | **The change-control rule** | What may move the baseline: error correction, a validation outcome against a pre-declared band, a defect that makes a deliverable wrong. What may not: anything motivated by *better* rather than *correct*. **The boundary is by type, not convenience**: the momentum-transfer release is the most interesting idea here and defers; P17 is tedious and does not. |
| GOV-05 | **Seventeen ADRs at the time** | `docs/adr/`. `DECISION_LOG.md` is not superseded, its prose became the Context sections. 012-017 record decisions never written down anywhere, including the three second-order effects of the sled-mass change that were not obvious at the time. |
| GOV-06 | **`docs/VAULT.md`, the gate** | Items reviewed **only at baseline boundaries**, each against an entry criterion **written when it was deferred**. Same discipline as declaring acceptance bands before a run: a criterion written afterwards is written by someone who already knows what they want the answer to be. |
| GOV-07 | **`docs/MANUFACTURING.md`, and a finding** | Three budgets were being conflated: 1.000 mm clearance, A4's 0.025 mm deflection band, and the 0.050 mm shim *setting* spec. **The build stack had never been computed.** RSS of seven contributors is 0.101 mm; with A4's deflection bias the total is 0.121 mm to **1.58 % thrust spread against the 0.65 % claimed, 2.4x.** Not a contact risk (12 % of clearance) but the paper's open-loop spread counted the shim and not the parts. **Not propagated**: the contributors are assumptions. Ranking is the deliverable: track straightness and plate flatness dominate, and tightening the shim is nearly worthless. |
| GOV-08 | **Halbach assembly named as the largest manufacturability unknown** | 2.69 kN closing on brittle sinter, magnetisation order undecided, and absent from cost, schedule and the qualification plan. |
| GOV-10 | **`docs/CROSS_INDUSTRY.md`, sourced, not asserted** | **E21 substantially retires by citation** (ESA Space Tribology Handbook; MoS₂; twelve cycles is trivial). **E19 characterised**: segmentation is the standard mitigation and it costs thrust, a design option this project lacked. **E11** gains external support for ADR-004. It cuts both ways: E23's cogging half retires, but its *sweep* half appears genuinely unusual, industrial stages do not chirp through their velocity range in 157 ms. **E20 was not searched and says so** rather than padding with a plausible citation. |
| GOV-11 | **Four repositories, two generated** | `tools/export_companion.py`. The paper companion was verified to reproduce standalone, `v_exit = 16.537`, matching the flagship. §4's divergence warning is answered mechanically, not behaviourally: if a companion is ever hand-edited, delete and regenerate rather than reconcile. |
| GOV-12 | **Linkage prepared where it could not be pushed** | `bootstrap_repos.sh`, `seed_issues.sh` (14 issues, the roadmap and open HIGH defects, not all 42), `setup_project.sh`. **Found while testing: Issues are disabled on the repository** (API returns 410), a settings flag, now handled by the bootstrap. |
| GOV-13 | **Validation chain positioned honestly** | Dossier §7's eight rungs added to `docs/ROADMAP.md`. The project is at **Simulation, one rung of eight**. **Repeatability has no rung, nothing has been run twice by anyone.** Manufacturability opened today but holds analysis *about* manufacturing, not manufacturing evidence. |
| GOV-14 | **Literature review restructured** | `RELATED_WORK.md` was a leads list; it now carries five fields per source, claim, method, what VOLLEY takes, where it differs, verification status. Status is per-source, because the old blanket "none of this has been read" became untrue and a blanket statement that is wrong is worse than none. |
| GOV-15 | `PROJECT_NOTES.md` de-staled | It claimed 32 % efficiency and listed P5/P8 as open, both wrong since the propagation. Now defers to `docs/BASELINE.md`, `docs/ROADMAP.md` and `VAULT.md` rather than competing with them. |

**No value in `analysis/` changed.** `analysis/results/cost.json` is the only file added there,
and every existing result field is untouched, verified, because this is governance work and a
moved number would mean something went wrong.

---

## 2026-07-29 (companions): the three repositories exist; content still to be pushed

| ID | Item | Detail |
|---|---|---|
| REPO-01 | `VOLLEY-paper`, `VOLLEY-thesis`, `VOLLEY-lab` created | Created 2026-07-29. All three public, `main` default, currently empty. Repository creation is not possible from the working environment at all, the GitHub App returns `403 Resource not accessible by integration`, because **GitHub Apps cannot create repositories on a personal account**; that endpoint needs a user token, not an installation token. No permission setting changes it. |
| REPO-02 | **Content generated and verified, not yet pushed** | 84 files to `VOLLEY-paper`, 148 to `VOLLEY-thesis`, 3 to `VOLLEY-lab`. The paper companion was verified to **reproduce standalone**: run from a clean copy it returns `v_exit = 16.537`, matching the flagship. |
| REPO-03 | **Why the push did not happen here** | The environment's git proxy serves only `aaaaaaaaaaaavm/emocd`; `git ls-remote` fails against all three companions. Extending session scope needs `add_repo`, which required an approval the environment could not grant. Reported rather than worked around. `tools/bootstrap_repos.sh` covers it in one command from any machine with `gh`. |
| REPO-04 | **Three stale counts fixed from the A1 propagation** | A1 moved the tally 3-of-8 to 4-of-9 and three places did not follow. `SUMMARY.md` had become **self-contradictory**: "four of nine ... and all three predate the current operating point", which was introduced in the same edit that added A1. A1 *is* at the current point; A5 and A8 are not. `README.md` and P19 carried the same stale framing. |
| REPO-05 | `docs/PROGRAMME.md` and `docs/HISTORY.md` narrowed | Both described the companions as prepared-but-unpushed in general terms. They now state precisely what exists, what is empty, and which specific things remain blocked: tags and releases, descriptions and topics, the programme board, and the Issues toggle. |

**Still outstanding, all of it one command each:** `bootstrap_repos.sh` (fills the three
companions), `publish_releases.sh` (six milestone tags and releases), `setup_project.sh` (the
programme board), and the Issues toggle in repository settings.

---

## 2026-07-30: prior art found, two claims retracted, one ADR argument found false

The most consequential entry in this log. A literature check found **published work on this exact
concept that the paper did not cite**, and reading it retracted two claims and falsified an argument
this design's central decision was partly resting on. Full record in `docs/PRIOR_ART.md`, tracked as
**P22**.

| ID | Item | Detail |
|---|---|---|
| ART-01 | **Two independent groups are already here** | Feng, Yang & Wu (NUDT, *IJAE* 2025, art. 3000765) simulate an on-orbit three-stage induction coilgun driving a 20 kg CubeSat to **321.56 m/s** with a 3-D reachable-domain analysis, **published 2025-11-12, eight months before this repository went public.** Separately the Harbin Institute of Technology mechatronics group has three papers (2022, 2024, 2025) on magazine-fed electromagnetic storage, transport and release of stacked CubeSats. The paper had 24 references and none of them. |
| ART-02 | **§I claim retracted** | *"No published deployment system operates in the tens of m/s"* was **false**: Feng operates at hundreds. Now restricted to **flown hardware**, which is what the comparison table always actually showed. Feng's own Table 1 surveys the same 1-2 m/s spring deployers and identifies the same gap, so the gap is real; the word *published* was wrong. |
| ART-03 | Contribution re-scoped in the abstract | From electromagnetic deployment as such to **programmable velocity + unmodified satellite + inside its own qualification envelope**. Narrower and defensible. Both qualifiers do real work against Feng, where against a spring they were nearly free. |
| ART-04 | **ADR-003's efficiency argument was false, and unsourced. Withdrawn.** | It claimed coilgun efficiency is *"1-2 % in the literature"* with no citation. Feng reports **14.9-19.9 %**: the same order as this design's own 20 % electrical-to-payload. Einat & Orbach (*Sci. Rep.* 2023) measure a real multi-stage launcher but at a **2.5 g** projectile, five orders below a CubeSat, so it cannot settle the question either way. The argument is removed rather than re-sourced. It was never load-bearing. |
| ART-05 | ADR-003's second claim softened | *"Cannot command velocity closed-loop"* to a claim about **absent published dispersion evidence**. Feng varies exit velocity 230 to 321.56 m/s by charging voltage (10 to 16 kV) with position/velocity feedback for stage trigger timing. That is genuine velocity selection. They quote **no dispersion figure**, so this design's 0.027 m/s 3σ stands unopposed rather than proven superior. |
| ART-06 | **The decision survives, now on arithmetic instead of assertion** | ADR-003 argued in mid-2025 that a coilgun's velocity advantage is *"erased by the payload's own g-limit."* Against Feng's published 3.9 m barrel: **1352 g mean**, ~3060 g peak from their own >600 kN on 20 kg, against ~14 g CubeSat qualification. Also **6.91 MJ per shot against 2.80 kJ**: 2470x. Not a flaw in their work; they target debris removal with a purpose-built body. It is why this one is not a coilgun. |
| ART-07 | **Three of my own abstract-level conclusions were wrong** | Listed in `PRIOR_ART.md` rather than quietly corrected. The worst: I asserted 321.56 m/s "would need a 493 m track at 10.7 g" as a hypothetical, when their actual barrel length was in their Table 2 all along. The fact is more decisive than my hypothesis was. Also: Feng has **no hardware** (so this project and theirs are maturity peers, not one behind), and *Aerospace* 12(6) 466's experiment measures a **32.8 mm/s transport pusher**, not an ejection, a real maturity gap but narrower than "they have experiment and we don't". |
| ART-08 | **E24 opened**, from a competitor's problem statement | Xu et al. build a cost model for **attitude disturbance caused by moving CubeSats inside the deployer**. This project budgets recoil from the *shot* (66.1 N·s) and has nothing on disturbance from **magazine indexing between shots**: a few kg translating across the structure between every pair of shots, unmodelled, on a design whose dispersion claim assumes the track is where the model says it is at trigger time. |
| ART-09 | Phase II candidate: adopt reachable-domain analysis | Feng's 3-D reachable-set envelope answers "which orbits does one shot make available" directly, where this project reports a scalar lifetime multiplier. The strongest thing to take from this literature. |
| ART-10 | `docs/RELATED_WORK.md` gained the section it should always have had | It had 7 citations and **no competitor section at all**. Its absence was the defect that let ART-02 stand. All five works now carry `verified` status with the file's own five-field format. |

---

## 2026-07-30 (bench): B-1 and B-2 bands derived instead of chosen

Prompted by ART-01: the Harbin group has measured hardware and this project has measured nothing.

| ID | Item | Detail |
|---|---|---|
| BENCH-01 | **I duplicated existing work and then removed it** | `docs/BENCHTOP_TESTS.md` already specified a single-coil thrust measurement as **B-2**, with a better rig than the one I designed, real Halbach pair, design coil geometry, swept over a wavelength. I wrote a competing `BENCH_E4.md` around a simpler two-magnet rig before checking. Deleted; the effort was redirected into strengthening B-1 and B-2. Recorded because the repository logs its own process defects, and "check whether it already exists" is one. |
| BENCH-02 | `validation/bench/bench_predict.py` | Derives the acceptance bands B-1 and B-2 previously asserted. **Imports** `verify_field.py` and `motor_model.py` rather than reimplementing the field geometry, and carries a guard that exits non-zero if its local build ever drifts from `verify_field.make_array`, the same idea as `_check_operating_point()` in `sizing.py`. Perturbs gap ±0.5 mm, Br ±3 %, thickness ±0.1 mm, re-solves, reports RSS. |
| BENCH-03 | The bands do not move, and that is the finding | Measurement error is **4.4 % on B-1's field rows, 13.5 % on B-2's thrust**, against declared bands of ±15 % and ±20 %. The bands must also cover *model* error, which is the thing under test and cannot be budgeted from the model. What the budget establishes is that **the rig is not the limiting factor**: a reading outside ±15 % can no longer be blamed on shim stack or magnet grade. That is what makes a failure interpretable. |
| BENCH-04 | **A two-block bench pair built poles-facing reads exactly zero** | 0.00000 T at midgap, against 0.329 T built correctly. B-1's wording, "a two-block *opposed* pair", is ambiguous in precisely the way that matters, and a zero reading would look like a falsified field model rather than a reversed magnet. Found by hitting it, the first version of the predictor divided by zero. `verify_field.py` probes for the convention automatically on the four-block array, so the trap exists only on the bench. |
| BENCH-05 | B-2's load cell must be sized to the smallest force, not the largest | A cell specified at 0.5 % of full scale contributes error inversely with the reading, so sizing it to the largest expected force makes the lowest-current point the least trustworthy, the opposite of what B-2 needs, since low current is where it is designed to operate. |
| BENCH-06 | One budget term is known-incomplete, and says so | For the stray rows the probe sits a fixed distance behind the **back face**, so block thickness moves the reference plane as well as the source; the budget captures only the source term. Affected contributions are 0.8-1.8 % against an RSS of 3.3-4.2 %, so no conclusion changes. Flagged in the script and the doc rather than left to be found. |
| BENCH-08 | **`.gitignore` has never ignored `paper.pdf`** | Line 17 read `paper.pdf          # transient output; committed PDF is VOLLEY_IEEE_Conference.pdf`. In `.gitignore`, `#` opens a comment **only at the start of a line**, so the pattern was the entire string including the comment text and matched no file. Found because `git add -A` staged `paper/paper.pdf` when the documented intent was that it never be tracked. Comment moved to its own line; `git check-ignore` now confirms the match. The committed `VOLLEY_IEEE_Conference.pdf` has also been refreshed from the corrected `paper.tex` (11 pages, zero undefined references) since the ART-02 rewrite made it stale. |
| BENCH-07 | Two unit and definition errors caught by cross-checking | `motor_model.thrust_constant()` returns N per **A/m**, not per kA/m, a factor of 1000, caught because 0.011 was obviously not 11.22. And `verify_field` computes stray field as the **max of the full 3-vector**, not the mean of the in-plane components; using the latter gave 16.2 mT where the repository publishes 22.7 mT. Both found by requiring the script to reproduce `field_verification.json` rather than merely look plausible. |

---

## 2026-07-29 (toolchain): the validation environment made reproducible

| ID | Item | Detail |
|---|---|---|
| ENV-01 | **`tools/env-setup.sh` added** | Until now `requirements.txt` covered only the analysis layer. Everything under `validation/` needs external solvers, and those were installed ad hoc each time the working environment was rebuilt, which means the validation results were reproducible in principle and awkward in practice. The script installs GetDP, CalculiX, ngspice, gmsh, scikit-fem and a minimal LaTeX set, then **verifies each one and exits non-zero if any is missing**. |
| ENV-02 | Two install failures encoded as comments, not rediscovered | `apt-get update` must run first, a stale container index makes the first `texlive` fetch 404. And `texlive-latex-extra` is deliberately excluded: nothing in `paper/` uses it and it pulls a mesa/ruby chain that fails to configure in a minimal container. Both cost time once; neither should again. |
| ENV-03 | `README.md` cross-check count corrected 2 to 3 | The README still read "Two results have independent cross-checks", naming the magpylib field check and the orbital decay check. A1 (the meshed magnetostatic FEM confirming the thrust constant to 0.07 %) is a third, and a stronger one, since it is a PDE solve rather than another superposition. `SUMMARY.md` already said so; the README contradicted it. Same class of staleness as REPO-04, from the same propagation. |
| ENV-04 | `README.md` and `docs/CONTRIBUTING.md` point at the setup script | Both previously implied `pip install -r requirements.txt` was sufficient to run everything in the repository. It is sufficient for `analysis/` only, and that distinction is now stated where each instruction appears. |

---

## 2026-07-29 (companions live): all four repositories now carry content

| ID | Item | Detail |
|---|---|---|
| REPO-06 | **The three companions are published** | `VOLLEY-paper` at `8c80f78` (84 files), `VOLLEY-thesis` at `fe6756d` (148), `VOLLEY-lab` at `2ebb6a3` (3). The two generated ones were built by `tools/export_companion.py` against flagship `c927df9` and carry that commit in their banner, so a reader can tell exactly which flagship state they are a copy of. |
| REPO-07 | What actually unblocked it | REPO-03 recorded this as blocked on session repository scope. The real cause was narrower and was found by testing rather than assumed: the **GitHub App installation was scoped to `VOLLEY` alone**, because the other three were created after it was installed. Widening the installation's repository access made the scope extension succeed on the first attempt. The earlier diagnosis was correct about the symptom and wrong about the cause. |
| REPO-08 | The paper companion was verified **before** publishing, not after | `analysis/` was run from the clean pushed tree with an empty `results/`, and returned `v_exit = 16.537 m/s`, identical to the flagship. The rest of the tree then diffed byte-identical against the export. For a reproducibility package this is the only check that matters, and it precedes the push rather than trailing it. |
| REPO-09 | Still blocked, retested rather than assumed | `refs/tags/*` still fails (the proxy drops the connection mid-push) and `api.github.com/repos/*` still returns `403 GitHub access is not enabled for this session`. Both were re-tested after the App scope widened, on the chance that fixed them too. It did not, they are proxy behaviour, not permissions. The six tags, their releases, the descriptions and topics, and the programme board all still need `tools/publish_releases.sh` and `tools/setup_project.sh` run from an ordinary machine. |

---

## 2026-07-29 (tags): the six milestones are on GitHub, and the publish path was found broken

| ID | Item | Detail |
|---|---|---|
| TAG-01 | **Six milestone tags pushed** | `v0.0-concept` (2021-03-22) through `v1.0` (2026-07-29), annotated, carrying their design-period tagger dates. Verified against the remote by SHA: all six tag objects on GitHub are the objects built here. Supersedes the "tags cannot be pushed" note in REPO-09 for `refs/heads`-adjacent reasons, the block was the *proxy's* credential path, not GitHub. |
| TAG-02 | **`publish_releases.sh` would have silently created nothing** | Found by actually cloning the repository and running it, rather than reading it. The script pushes tags **if they exist locally**: and they existed only in the environment they were built in. They were never on GitHub, so **no clone has them**. A fresh clone arrives with one tag, `v0.1.0`, pointing at a commit the reconstruction removed. The script would have printed `MISSING locally -- skipped` six times, created zero releases, and exited 0. A defect that reports success is worse than one that fails. |
| TAG-03 | `tools/restore_tags.sh` added | Rebuilds all seven annotated tags (message, tagger date and tagger identity) from data embedded in the script plus commits already in the clone. Every tagged commit is an ancestor of the default branch, so a full clone suffices. **Verified by cloning fresh, running it, and comparing tag objects: all seven reproduce bit-for-bit.** `publish_releases.sh` now invokes it when the tags are absent, so the failure in TAG-02 cannot recur. |
| TAG-04 | Two bugs in that script, both found by testing it | **(a)** The tagger identity was inherited from git config, so in a fresh clone whose config named someone else, every milestone was silently restamped with that identity and the tag objects stopped matching. Now pinned, overridable via `TAGGER_NAME`/`TAGGER_EMAIL`. **(b)** `v0.1.0` was treated like the others and skipped when already present, but a clone always has it, pointing at the wrong commit, so the re-point step would have force-pushed a stale pointer and changed nothing. It is now always rewritten. Neither bug was visible by reading the script. |
| TAG-05 | Identity audit across all four repositories | Every commit author, committer and tag tagger in the flagship history and in all three companions: a single identity, `Adityavardhan Mishra <adityavardhanmishr@gmail.com>`. No stray identity anywhere. |
| TAG-06 | **Still outstanding: the `v0.1.0` re-point and the six Releases** | The re-point needs a force-push, which the working environment declines to perform, and Releases need the REST API, which it intercepts. Both are one `tools/publish_releases.sh` run from an ordinary machine. Reported rather than worked around. |

---

## Open decisions

1. **LICENSE**: RESOLVED 2026-07-23: owner chose **MIT** (P3-07).
2. **Repo visibility**: RESOLVED: the repository is now **public**, which discloses the
   scripts and the operating point. See `OPEN_PROBLEMS.md` E14 for what that costs on the
   patent side.

## Known follow-ups not yet addressed

- The two remaining figure generators (`legacy/make_figs.py`, `legacy/c5b_conj.py`) are
  legacy and use `dv = 25.0 m/s`. Only `F06` was regenerated; other figures were not
  audited against the current operating point.
- `OPEN_PROBLEMS.md` E-items (E1 3-D field closure, E3 CAD, E4 hardware, E16 reference
  hygiene...) remain open engineering, unchanged.
