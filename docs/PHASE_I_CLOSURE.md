> **This is a dated record of the Phase I closure and its figures are contemporaneous, annotated
> 2026-08-21.** Several have since moved and are not edited here. The largest:
> per-satellite mass **6.375 → 10.55 kg** ([A46](../validation/A46_enclosure_buildup.md), **P69**),
> the regeneration credit **291.4 → 47.0 J** after ADR-030 shortened the section from 240 mm to
> 39 mm (**P97**), and the constraint-ledger floor **49.23 → 88.67 kg** (**P95**).
> `docs/BASELINE.md` is the current figure for anything quoted below.

# Closing Phase I: every open item, and what each one actually needs

**Written 2026-08-05, updated 2026-08-10.** [`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) carries
the numbered entries and its own live count — **not restated here**, per
[ADR-021](adr/021-freeze-the-register.md). This file says, for each, what would close it and who
or what has to do the closing, because a list that size with no disposition is a list nobody can
act on.

> **The register was frozen on 2026-08-10 (ADR-021), and this file's dispositions are what it was
> frozen against.** Nothing below is deleted or downgraded. What changed is that closing entries
> is no longer the highest-value work available: **B-1 is**, and the argument is in the ADR.

**Phase I cannot end with an empty register, and pretending otherwise would be the dishonest
version of this document.** Some items close only against hardware that does not exist. One
cannot close in Phase I at all. The useful question is not "is it empty" but **"is every item
either closed, or open for a stated reason with a named next step"**.

---

## 0. The first finding: the register could not distinguish fixed from live — **DONE 2026-08-06**

Entries marked RESOLVED sat alongside entries containing their own correction, with nothing
marking which was which, so the headline count mixed live engineering debt with published
history. Both are kept deliberately — this project publishes defects rather than deleting them —
but a reader could not tell a live threat from a closed one without reading all of them.

**Closed by `tools/register_status.py`**, which writes a `Status:` line under every entry and
derives the counts from them, with a `--check` mode so the file and the numbers quoted elsewhere
cannot drift apart again.

**The live figure is far smaller than the entry count**, and the three-way split is carried in
`OPEN_PROBLEMS.md`'s own header rather than duplicated here — per ADR-021, which stopped this
number being maintained in five places. Run `python3 tools/register_status.py` for the current
tally. Everything below was written before the distinction existed and its dispositions still
hold; the counts in section 1 are superseded by the register's own.

---

## 1. Disposition summary

| Disposition | Count | Meaning |
|---|---:|---|
| **A. Closable here, by analysis** | 13 | This environment has the tools. Bands first, then run |
| **B. Bookkeeping** | 9 | Closes by writing, not computing |
| **C. Needs a decision from the owner** | 7 | Analysis cannot resolve these; a choice must be made |
| **D. Needs hardware or an external party** | 9 | Measurement, a vendor quote, or a host data exchange |
| **E. Blocked** | 3 | Network policy or missing external data |
| **F. Cannot close in Phase I** | 1 | E4 |
| **Already resolved** | 15 | Marked RESOLVED |

Toolchain confirmed present in this environment: `getdp`, `ccx` (CalculiX), `ngspice`, `gmsh`,
`skfem`, `magpylib`, `scipy`, `pdflatex`. **GMAT is not installed.** That is a wider toolchain
than the repository's own notes assume, and it is why category A is as large as it is.

> **A-13's block was stale, and it is worth recording why rather than only that.** A-13 was
> written as blocked behind A-8 and A-9, on the reasoning that the extent of the 61 mT region
> needed a trustworthy 3-D far field. **It never needed a mesh.** magpylib's `Cuboid` is an
> exact analytic solution for a uniformly magnetised block, so the finite-array field was
> already three-dimensional and correct, and `analysis/far_field_sensitivity.py` had since
> resolved **P3** and **P21** and shown the 7-wavelength default converged. The dependency was
> real when it was written and had been lifted for days without anything noticing — which is the
> same failure class as the A1 row in `validation/README.md` that said "not run" while three
> other files recorded the result. **A blocked item needs its block re-tested, not inherited.**

---

## 2. Category A — closable here, by analysis

Every one of these gets a run sheet with **bands declared and committed before the script exists**,
the discipline `validation/README.md` exists to enforce. Ordered by value.

| # | Item | Closes | Tool | Expected |
|---|---|---|---|---|
| ~~A-1~~ | ~~**Tip-off at release (A7)**~~ | E7, KILL_CRITERIA §4 | ~~numpy 6-DOF rigid body~~ | **DONE, and not by A7 — corrected 2026-08-20.** [A23](../validation/A23_tipoff_release.md) modelled it on 2026-08-10 as three rigid-body stages with the mechanism properties as *swept axes*, and [A34](../validation/A34_cradle_restitution.md) answered the impact A23 opened on 2026-08-13, **five of five**. **The prediction here was wrong**: the ideal release is **0 °/s**, skew tolerance **50.6 µs**, cradle reaction **85.0 N against a 200 N band**. *This row asked for a 6-DOF model of a release mechanism that does not exist, which is exactly what [A7-R](../validation/A7_separation_chrono.md) refused to build* |
| A-2 | **Gen4 finite-stator force** | **P32**, E27 | magpylib | Opens the Gen4 export gate. HIGH |
| A-3 | **Ripple vs track modes** | E23 | numpy | 6th harmonic sweeps 0→2048 Hz; track first mode is 109 Hz, so it **crosses** |
| A-4 | **A8 rerun at the corrected point** | A8's self-declared staleness | ngspice | Deck exists at `validation/spice/` |
| A-5 | **Brake force-time profile** | E20, feeds E26 | numpy | The brake has no force-time curve anywhere |
| A-6 | **Magnet eddy heating** | E19 | analytic + magpylib | |
| A-7 | **Brake-fin campaign transient** | E26 | thermal network | Currently only an adiabatic bound (85 K) |
| A-8 | **3-D field and end effects** | E1's remaining half, E2 | gmsh + getdp | Heaviest; a coarse end-effect check is an acceptable outcome |
| A-9 | **Far-field stray, properly** | **P3, P21**, and A14's band 5 | 3-D from A-8 | A14 showed the 2-D model's far field is edge-effect dominated |
| A-10 | **Launch restraint** | E10 | ccx | Needs loads defined first |
| A-11 | **Parasitic eddy drag on the track** | E22 | analytic | |
| A-12 | **The four absent physical effects** | P18 | mixed | Scope each, then close or convert to E-items |
| A-13 | **Payload magnetic environment** | **P34**, narrowed not closed | magpylib | ~~Blocked behind A-8/A-9~~ — **the block was stale. DONE 2026-08-10**, see below |

## 3. Category B — bookkeeping

Closes by writing. No computation needed.

**Worked 2026-08-10.** Outcome against each, because "closes by writing" turned out to be true of
five of them and false of three.

| Item | What it needed | Outcome |
|---|---|---|
| **P7** | Brake sits past the release point — Gen4's 22 mm gap resolves it geometrically | **CLOSED.** Recorded against A16/P32. The envelope-length half was always P9's |
| **P23** | Stroke time stale in six places. Sweep and correct | **CLOSED.** Swept: four prose occurrences already corrected, two survivors are A8's *declared band* and are correct precisely because they were never edited |
| **P27** | A numerical guard hid a failure. Fixed in `shot()`; needs marking | **CORRECTED.** Verified in source — `BankLimitError` is raised on `disc <= 0`; the silent fallback is gone |
| **E8** | Brake energy thrown away; not examined since the efficiency correction | **CLOSED into P28.** The premise was false: A11 recovers 291.4 J, 934.7 J reaches the fin, and the remaining question is P28's layout decision, already priced by A18 |
| **E13** | Two untraced third-party numbers | **CLOSED.** Both already falsified or ruled inapplicable, and neither is load-bearing anywhere in the tree |
| **P20** | A1's array-surface reference is mis-specified in the run sheet | **CARRIES, and the sheet was deliberately not edited** — see below |
| **P14** | Gen3 CAD defects. Audit each against Gen4 | **CARRIES.** Audited: two of six answered by Gen4, four untouched |
| **E16** | Three references flagged verify-before-submission. Verify them | **NARROWED.** Two of the three are no longer in the paper at all; the third is now identified and bibliographically verified but **not read** |
| **P19** | Every validation predating the current operating point | Not worked in this pass |
| **P25** | A retracted claim stayed live for a day | Already `CORRECTED` |
| **P30** | Band chosen at the easier comparator | Already `CORRECTED` |

> **P20 is the one where "fix the sheet" was the wrong instruction, and it is worth stating why.**
> The obvious action is to correct the mis-specified band in `validation/A1_field_femm.md`. **That
> is the single action this project forbids.** The band was declared on 2026-07-27, A1 ran against
> it, and editing an acceptance band after its result is known is the move `validation/README.md`
> exists to prevent — regardless of the correction being provably right. The entry had already
> ruled it out in its own second paragraph. The fix is forward-only, and it now lives in
> `validation/README.md`'s conventions so that **A2** meets it without having to know to search
> the register. P20 closes when A2 is specified, and A2 does not exist.

> **E16 was the item most able to be closed dishonestly, and checking it changed the answer.**
> The instruction was "verify the three references". Two of them — Yudintsev separation dynamics
> and the vibro-impact deployment paper — **return zero matches in `paper.tex`**. They were
> removed from the manuscript at some point and the register went on guarding citations the
> deliverable no longer makes; the bracket numbers were stale too. The third is now a full
> citation. But retrieval of the full text is **blocked by this environment's egress policy**,
> re-tested rather than assumed, so it is verified *bibliographically* and not *substantively* —
> and it is cited for "flight heritage" while what the metadata describes is a bench-tested
> prototype. **Closing that by assertion would have been worse than leaving it live**, which is
> what the item itself says.

## 4. Category C — needs a decision from you

**Analysis cannot close these.** Each is a choice with consequences, and each is currently
blocking work downstream.

| Item | The decision | What it blocks |
|---|---|---|
| **P9** | Target host class. The envelope is 1839 mm against ESPA Grande's ~1270 mm, 44 % over | A kill-criterion item. PII-4 |
| **P28** | 240 mm of regen stator and a 300 mm fin do not both fit the 339 mm arrest section | The regen credit and the brake layout |
| **P29** | Is the stator segmented or not? The paper says yes; the model charges copper for all 1.3 m | Copper loss, efficiency, **and P33's inductance**, which scales with energised length |
| **P10** | Enclosure, radiator and packaged avionics are absent from the mass rollup | Kill criterion 1, which is already crossed at 3U |
| **P31** | Inter-shot cadence: 10–20 s or 1200 s | **Being closed now** as ADR-020 at 1200 s |
| **E9** | Are 6U/12U variants in scope? | Product definition |
| **E14/E15** | Patent posture and sponsorship | Programme, not engineering |

## 5. Category D — needs hardware or an external party

| Item | What closes it |
|---|---|
| **E3** | Vendor datasheets against the parametric masses. No hardware needed, only sourcing |
| **E5** | Host stage properties — a data exchange with a host provider. Paper §VII already names this as the single exchange that converts the analysis from parametric to specific |
| **E11** | T-4 thermal vacuum, ASTM E595 |
| **E12** | **T-6.** A14 scoped it; only measurement closes it |
| **P26** | Bank ESR — a purchasable bank, or PII-7's four parallel strings accepted on paper |
| **P34** | T-6 measures the payload field. A-13 bounds it first |
| **B-1…B-4** | Benchtop programme. B-1 is a Halbach pair on a gaussmeter and is the cheapest first measured number in the project |
| **T-1…T-8** | Qualification campaign |
| **E4** | See category F |

## 6. Category E — blocked

| Item | Why |
|---|---|
| **A9 / E6** | Decay against flown CubeSats. `celestrak.org:443` returns 403 at CONNECT under this environment's network policy — re-tested, not assumed. Space-Track needs an account. The candidate NORAD shortlist is already in the run sheet, so this is an afternoon on any unrestricted machine |
| **P16** | The invariance falsification stands; closing the remainder needs A9 |
| **E18** | Conjunction covariance is invented. Needs a real CDM, which needs an operator relationship |

## 7. Category F — cannot close in Phase I

**E4: nothing has been built or measured at any scale.** This is not a defect to be worked off;
it is the honest description of a TRL 2–3 design study, and it should be stated as a **standing
caveat** rather than carried as an open item that might one day be ticked. Every number in this
repository is a model output. Phase I ends with that still true.

---

## 8. Validations: stated versus run

| | Status |
|---|---|
| A1 field, A4 structural, A5 astro, A6 conjunction, A8 pulse, A10 ESR, A11 regen, A12 attraction, A13 attitude, **A14 EMI** | **RUN** — 10 of 12 |
| **A7** separation and tip-off | **specified, correctly never run — SUPERSEDED, corrected 2026-08-20.** A7-R gave the angular-impulse budget (**1.465 mN·m·s**), [A23](../validation/A23_tipoff_release.md) modelled the three stages, [A34](../validation/A34_cradle_restitution.md) closed the cradle impact. **The question is answered; the tool named in the spec never was, and did not need to be** |
| **A9** decay against flown objects | **specified, blocked.** Not runnable here |
| A2, A3 | never specified. A1 closed only the 2-D half of E1 |
| **A15** POEM campaign | new; script generated here, **GMAT run is external** |

**Two failed** (A5 invariance, A13 attitude), **two partial** (A1 field, A14 EMI), **one returned
three void rows** (A6), **one found a published number 37 % high** (A12).

### Stated and never run, outside `validation/`

- **T-1 … T-8**, the entire qualification plan. Specified 2026-07-29, none run, all need hardware.
- **B-1 … B-4**, the benchtop programme. B-1 has a bill of materials and a purchase order and has
  not been ordered. **It is the cheapest path to the first measured number in this project.**
- **`docs/FEMM_Run_Sheet.md`** — superseded, retained, and correctly marked as unable to function
  as a test.

---

## 9. What Phase I closure actually looks like

1. **Mark every register entry** `LIVE` / `CORRECTED, RETAINED` / `CLOSED`, and derive the counts
   from that. Section 0. Nothing else is meaningful first.
2. **Run category A** — thirteen analyses, bands first, several expected to fail.
3. **Decide category C** — seven choices, all yours. P29 is the highest-leverage one because it
   moves copper loss, efficiency and inductance together.
4. **Convert category D into a plan with dates**, and order B-1.
5. **State categories E and F as permanent caveats**, not as debt.

**A realistic Phase I close leaves E4 open, categories D and E open with named owners, and
categories A, B and C closed.** That is a defensible end state. An empty register would not be.

---

## 10. The four decisions that are yours, costed

**Updated 2026-08-06, after every closable analysis had run.** These did not move, because nothing
computable resolves them. Each is here with what it blocks and what it costs either way, so the
choice can be made rather than deferred again.

> ## Two of the four were decided 2026-08-10
>
> **P29 → [ADR-022](adr/022-stator-segmented-not-block-commutated.md).** The winding is segmented
> **for fault isolation** and driven as one section. `vol_cu = ACCEL_ZONE` stands, **no baseline
> value moves**, and the paper now says so explicitly so no reader infers block commutation.
> Both branches were priced first by `analysis/owner_decisions.py`: block commutation is worth
> **+7.09 points of efficiency** (20.99 → 28.07 %) and **exactly zero exit velocity**, because
> force is commanded. It costs drive hardware that is not in the mass rollup, and mass is a
> crossed kill criterion while efficiency is in none of them.
>
> **P9 → [ADR-023](adr/023-target-host-class.md).** Target host is a spent upper stage or hosted
> platform of POEM class; **ESPA-Grande port compliance is not a requirement.** Shortening to fit
> was priced at **−25 % exit velocity** (16.029 → 12.286 m/s) and rejected. **Kill criterion 2 is
> not thereby passed** — it moves from *crossed* to **NOT EVALUABLE**, because no accommodation
> envelope for the target class is public (**E5**). A measured failure has become an unmeasured
> unknown, which is recorded as the cost it is.
>
> **P28 and P10 remain open**, and P10 is now the sharper of the two: ADR-022's reasoning rests on
> the mass rollup being tight, so the packaging mass P10 tracks is what would reopen it.

### P29 — is the stator segmented? *(highest leverage)*

`paper.tex` says the winding is segmented so a shorted coil degrades thrust rather than ending the
campaign. `motor_model` charges copper loss for **all 1.30 m** regardless of sled position.

| | Segmented | Not segmented (as modelled) |
|---|---|---|
| Copper loss | falls roughly with the energised fraction | **834.7 J/shot** |
| Efficiency | rises | 18.47 % net |
| **P33's inductance** | falls with energised length | **19.70 µH** |
| Drive | one inverter per segment, or switching | one inverter |
| Fault tolerance | the paper's claim becomes true | the claim is currently unsupported |

**It moves three published numbers at once**, and the paper already asserts the answer. Deciding
it is the single highest-leverage thing on this list.

### P9 — target host class

1839 mm closed envelope against ESPA Grande's ~1270 mm, **44 % over**. Kill criterion 2, binary.
Either accept a larger host class and say so, or shorten the machine — and the brake sits beyond
the 1500 mm release point, so the length is structural rather than packaging slack. PII-4 and
PII-8 (free-flyer) both dissolve it differently.

### P28 — regen stator versus eddy fin

240 mm of regenerative stator and a 300 mm fin do not both fit the 339 mm arrest section.
**A18 now prices the fin side**: the brake needs a 0.4–0.5 T pole field to stay inside both the
200 g cap and the 210 mm envelope, so shortening it is not free. Giving up regeneration costs the
**291.4 J** credit and 2.2 points of efficiency.

### P10 — enclosure, radiator and packaged avionics

Absent from the mass rollup. At a plausible 20 kg the per-satellite figure goes **6.375 → 8.08 kg**
against a 2 kg threshold that is already crossed. This is not a decision so much as work nobody
has done, and it makes kill criterion 1 worse in the only direction it can go.

---

## 10b. What to measure first — A19, 2026-08-10

The register says what is open. It has never said what is **worth** resolving first.
`validation/A19_sensitivity_ranking.md` ranks nine assumed inputs by how much each moves
`v_exit`, net efficiency and kg per satellite, with the bands committed before the script existed.

**Band 1 failed**, and usefully: net efficiency has one leader by range-swing (**bank ESR**,
23.24 %) and a different one by local elasticity (**magnet remanence**, 0.487 against −0.038).
Both rankings are published rather than the more convenient one being chosen. Bank ESR leads on
swing **because nobody knows what it is**, not because efficiency is especially sensitive to it —
which is a different reason to measure something, and worth keeping separate.

**Six of the nine inputs return exactly zero on all three headline numbers**, and two of those six
move a pass/fail transition inside their own declared range:

| Input | Effect on the three headline numbers | What it actually moves |
|---|---|---|
| **Structural Q** | **0.000 %** | **retention-gate margin +0.559 → −0.100** — through zero |
| **Brake pole field** | **0.000 %** | brake stopping distance 0.345 → 0.063 m against a 0.210 m section |

**The headline numbers are not what is at risk from the unmeasured assumptions. The design's
viability is.** A ranking that looked only at exit velocity, efficiency and kg per satellite would
have reported six harmless zeros and missed both of these, which is why A19 reports a binding
output for every input that ranks zero.

**Measurement order:** structural Q, then the magnet grade (a look-up, not a measurement), then a
sourced bank ESR, then B-4 for the brake pole field. **This ranks assumptions and makes none of
them less assumed** — every input is exactly as unmeasured afterwards, and E4 is untouched.

## 10c. Distance to close, measured 2026-08-13

**Phase I is closer than the live register count suggests, and the reason is that most of that
count is not supposed to close.** §9 defined a defensible end state on 2026-08-05: **categories
A, B and C closed; D, E and E4 open with named owners.** Measured against that definition rather
than against an empty register:

| Category | Status | What is left |
|---|---|---|
| **A — closable here by analysis** | **near-complete** | **P36** is the only substantial one. **P41** and **A15 band 7** are small |
| **B — bookkeeping** | **near-complete** | A handful of records that disagree with their sources |
| **C — owner decisions** | **the actual gate** | Four, and none is engineering work |
| D — hardware / external party | **stays open by design** | Named owners; **B-1 is the one that matters** |
| E — blocked | **stays open by design** | Network policy, undisclosed host data |
| F — E4 | **stays open permanently** | The standing caveat of a TRL 2–3 study |

### The three analyses

1. **P36 — the track has no dynamic design case.** A17 asked for one on 2026-08-05 and it has
   never been produced. This is the largest single item and it is the only one that could still
   change a Gen5 number: the first mode at 109 Hz is a beam-model output that A28's velocity-loop
   bandwidth is now designed against, so the two are coupled.
2. **P41 — the payload's cradle impact.** Currently stated as a *requirement* on cradle preload
   (> 85 N) and release residual (≤ 1 N) rather than as a result, because no restitution model
   exists. Closing it means either building that model or accepting the requirement as the
   deliverable and saying so.
3. **A15 band 7 — campaign duration.** Reading `build_poem_campaign.py` against ADR-020. Not a
   propagator run; a script read.

### The four decisions, and none of them is engineering

Carried from [`STATE_OF_THE_PROJECT.md`](STATE_OF_THE_PROJECT.md), which holds all ten:

| | | Blocks |
|---|---|---|
| **D3** | **Apply P46's K<sub>t</sub> correction, or write the ADR that says why not.** The depth-resolved value is 4.42 % lower and has been *computed and held* since 2026-08-10 | The published design point |
| **D8** | **Retire Gen4.** It exists only inside Fusion, has never been exported, and its stations do not match the parameters every number rests on | **P32**, **P39**, and the renders' provenance |
| **P28** | Regen stator versus eddy fin in the arrest section | An arrest-section layout |
| **P10** | Enclosure, radiator and packaged avionics in the mass rollup | The mass number kill criterion 1 is computed from — and ADR-022's reasoning rests on the rollup being tight |

### And two that are not Phase I work at all

**Order B-1**, and **decide what happens to the paper**. Neither closes a register entry. Both
decide whether any of this leaves the repository.

> **Honest summary: two working sessions of analysis, one of bookkeeping, and four decisions
> only the author can take.** Then Phase I closes with E4, category D and category E open and
> named — which is exactly the end state §9 defined before any of this year's work was done.

**What is explicitly not on this list: P52, and the whole of Gen6.**
[ADR-029](adr/029-phase-one-closes-on-gen5.md) closes Phase I on Gen5, and Gen5's winding is
segmented for fault isolation and driven as one section (**ADR-022**) — so it has no segment
handover and P52 cannot apply to it. Gen6's debts travel with Gen6.

---

## 10d. CLOSED, 2026-08-13

**Measured against §9's own definition, written 2026-08-05: *categories A, B and C closed;
D, E and E4 open with named owners.* That state is now reached.**

### Category A — closable here by analysis: CLOSED

| | |
|---|---|
| **P36** — the track had no dynamic design case | **A33**, six of six bands. The mode does fall 109.0 → 66.4 Hz with the sled aboard, but the ripple chirp crosses it at x = 133 mm where the sled has depressed it **0.8 %** — excitation and depression are separated in space, so A17's fixed-frequency treatment was adequate. The travelling load is **5.01 %** of critical speed |
| **P41** — the payload's cradle impact was unmodelled | **A34**, five of five. The rattle settles in **27.25 ms of a 146.4 ms powered stroke** and the residual rate at force removal is **exactly zero** for every clearance. A23's 36–231 °/s arrival never becomes a release rate |
| **A15 band 7** | Evaluated by reading the generator, which is the only way it could have been. **PASS.** A15 now has every band evaluated |

### Category B — bookkeeping: CLOSED

**P14** superseded by script-built CAD; **P19**'s general claim shown false with both survivors
dispositioned; **P20**'s lesson is a standing rule in `validation/README.md` that A2 band 4 was
then written under; **P35**'s false header struck and the pin given an import-time assertion;
**P38** and **P39** closed on their own criteria.

### Category C — owner decisions: CLOSED

**All four taken together under [ADR-030](adr/030-apply-the-depth-resolved-thrust-constant.md)**,
at a boundary rather than piecemeal, because propagation is the expensive part.

**P46** applied — the thrust integral is depth-resolved, K_t 11.0258 → **10.5386**, v_exit
16.388 → **16.029 m/s**. **P28** — regen section 240 → **39 mm**. **P10** — an **8.0 kg labelled
placeholder** enters the rollup. **P32** — **Gen4 retired**.

> **Every headline number moved the wrong way and nothing improved.** Efficiency 21.0 → 18.8 %,
> kg per 3U satellite 6.378 → **7.042**, kill criterion 1 from crossed by 3.2× to **3.5×**. That
> is what taking these decisions cost, and it is why they had been deferred. **This project's
> numbers have got worse every time they got truer**, and 20.65 → 20.37 → 16.537 → 16.388 →
> 16.029 m/s is the whole trajectory in one line.

### What stays open, by design and with owners

| | | Owner |
|---|---|---|
| **E4** | Nothing built, fired or measured at any scale | **B-1**, ₹22,000, still unordered |
| **Category D** | Vendor quotations, a host data exchange, cycle-life and shock tests | Hardware and external parties |
| **Category E** | Network policy; undisclosed host accommodation (**E5**) | Blocked, not open |
| **P36's damping half** | No measured Q for a bolted aluminium track | **T-2** sine sweep |
| **The kill criteria** | 1, 2 and 3 remain crossed at the 3U design point | Stated, not solved |

**Register at close: 87 entries, 31 live** — 10 P-items and 21 E-items, of which **E4, E5, E14
and E15 are permanent caveats rather than debt.**

### What Phase I is

**A design that is frozen, internally consistent, and knows what is wrong with it.** Four
independent verification tools pass on every commit; the baseline is generated from the scripts
and cannot silently disagree with them; every analysis declared its acceptance bands before its
script existed, and **twelve bands were missed and published as numbered defects rather than
widened.**

**It is not a design that has been shown to work.** Nothing has been measured. That distinction
is the whole of `PROVENANCE.md` and it is the first thing a reader should be told.

---

## 11. What Phase I closes with, honestly

**Every analysis this environment can run has run.** What remains is one measurement, four
decisions, and a small number of items that are blocked rather than open:

- **E4** — nothing built or measured. The standing caveat of a TRL 2–3 study, not debt to work off.
- **A15 band 6 / A6 / P1** — inter-object safety is **not established**. A15's separations resolve
  2.9 points per orbit; a real conjunction screen is A6's job and A6 returned three VOID rows.
- **A15 band 8** — **evaluated 2026-08-10, and it never needed a propagator.** The plane-change
  cost is closed form: **133 m/s per degree** at POEM circular velocity, against a 16.029 m/s
  shot. It remains **VOID as a capability claim**, which is the disposition the band declared in
  advance, because POEM's control authority is undisclosed (**E5**) — but the void is now about
  the host, not about a missing number. **A15 band 7 is the one still not evaluated**: campaign
  duration is a property of the generator script, not a GMAT output, and closing it means reading
  `build_poem_campaign.py` against ADR-020.
- **A9** — blocked by network policy; the candidate shortlist is already in the run sheet.
