# Open problems, known errors, and the fix list

Two categories: **P-items are errors in the currently published paper** and should be
fixed first. **E-items are genuinely unsolved engineering.**

> ## How to read the counts
>
> **127 numbered entries, of which 53 are live.** Every entry carries a `Status:` line written by
> `tools/register_status.py`, which derives the headline counts from the entries themselves.
>
> | Status | Count | Meaning |
> |---|---:|---|
> | `LIVE` | **53** (32 P, 21 E) | open engineering; something still has to be done |
> | `CORRECTED` | **41** | found, fixed and propagated — **retained as the published record, not as debt** |
> | `CLOSED` | **35** | resolved, with the closer named in the entry |
>
> **Four of those moves are a classifier repair, not new engineering.** `\bRESOLVED\b` matched
> inside *depth-resolved*, and the tool read its own `Status:` line back in on the next run, so a
> single wrong call re-justified itself forever. P18, P30 and P32 were sitting as `CLOSED` on the
> strength of a hyphenated adjective; P43 was sitting as `CLOSED` on the same latch. **The
> conservative direction is `LIVE`, and the repair moved three entries into it.**
>
> **These counts were stale by four entries until 2026-08-10, under a sentence claiming they
> "cannot drift apart again".** They could: `register_status.py --check` validates each entry's
> own `Status:` line, and never read this table. The claim has been removed rather than repaired,
> because the table is still hand-copied from the tool's output and a promise the checks do not
> enforce is worth less than none. Run `python3 tools/register_status.py` and compare before
> quoting these numbers anywhere.
>
> **This distinction did not exist until 2026-08-06** and its absence was itself a defect: a
> reader could not separate live engineering debt from published history, so "37 defects" counted
> both. `docs/PHASE_I_CLOSURE.md` §0 named fixing it as the first act of closing Phase I.
>
> The statuses are classified from each entry's own text. A handful sit close to the boundary
> between `LIVE` and `CORRECTED` — where the defect is fixed but a consequence remains — and are
> marked `LIVE`, which is the conservative direction.

> ## FROZEN 2026-08-10 — [ADR-021](docs/adr/021-freeze-the-register.md)
>
> **This register is closed to new entries except in three cases.** It remains authoritative and
> nothing in it has been deleted, closed or downgraded — all 81 entries stand, and the 38 live
> ones still carry their named next steps. **A freeze is not a purge.**
>
> **A new numbered entry may be opened only for:**
>
> 1. **a defect in the machine** — an error in the design or a model of it that changes what the
>    hardware would do;
> 2. **a defect that makes a published Phase I deliverable wrong** — the paper, `BASELINE.md`,
>    the portfolio. This is the **P38** case and it stays numbered;
> 3. **a validation band miss.** `validation/README.md`'s rule is untouched: a missed band
>    produces a numbered defect, never a widened band.
>
> **Everything else is fixed in place with a `CHANGELOG.md` line and no number** — defects in
> `tools/`, bookkeeping drift, stale cross-references, and observations about this file.
> **P39 would not be numbered under this rule.** It keeps its number because the freeze is not
> retroactive and this project does not rewrite its record.
>
> **Why.** The discipline caught a separation figure wrong by 5.7×, a force 37 % high, a claim in
> the paper's own abstract, and P38. It also grew to ~16,000 lines of prose around ~3,200 lines of
> analysis, and began producing its own defects: of the three entries opened on 2026-08-10, one
> was in the paper and one was in the export tool's file-copying semantics. Meanwhile **B-1 — the
> first measured number in this project, ~₹22,000, bill of materials already written — has never
> been ordered.** ADR-021 has the full argument and states what the freeze risks.
>
> **The band rule is not affected**, and neither is Phase II: `VOLLEY-lab`'s register is not
> frozen. Reviewed at the next baseline boundary.

Last reviewed 2026-08-10.

---

## Lethality ranking — confirmed 2026-08-10

**Ordered by how likely each live entry is to be design-fatal**, not by ID, date, or the
HIGH/MEDIUM/LOW severity already carried in each entry. Those severities rank *how wrong a
published number is*; this ranks *how likely the machine is not worth building*. The two orders
are different, and neither replaces the other.

**Nothing below is deleted, renumbered, or reworded.** This section only orders what already
exists, and the entries it points at remain the authority on their own content.

**Confirmed by the author on 2026-08-10**, including the two places where it disagrees with the
register's own severity labels.

### The five most likely to be design-fatal

| # | Entry | The failure it would cause | What would settle it either way |
|---|---|---|---|
| **1** | **E30** | Below **r = 0.99326** per element per cycle, the machine delivers less total mission value than a spring dispenser — nine of thirteen elements forfeit the remaining manifest where a spring forfeits one satellite. The product then has no reason to exist | **Cycle-life test of the escapement, retention gate and sled** to twelve cycles with margin, giving a measured per-element reliability. This is metal, not computation |
| **2** | **E4** | Every number in the repository descends from a field model checked only analytic-against-analytic. If the measured thrust constant departs materially from 11.03 N per kA/m, the design point, the velocity, the lifetime multiplier and the comparison against a spring all move together | **B-1** — a gaussmeter and eight magnetised blocks, ₹22,000, method and bill of materials already written in `docs/B1_ORDER.md`. Unordered |
| **3** | **E33** | The residual dipole from magnet tolerance saturates a 15 N·m·s wheel in **3.0–7.5 days with the machine idle**. Combined with **E31**, a host that has lost attitude authority may not legally deploy, so the campaign ends before the manifest does | **Measure the moment and axis of each block on receipt** and compute the assembled residual, rather than assuming the Monte-Carlo tolerance distribution. The same instrument B-1 buys |
| **4** | **E34** | The 200 g arrest puts **18.5 kN through the structure eleven times** while eleven satellites are still stowed. A stowed CubeSat is qualified to 25 g and launch random vibration, not to this. If it does not close, the arrest cap must fall, and the 50 g case needs 202 mm of run-out the envelope does not have | **A shock response spectrum at the cassette interface** for the 200 g arrest, against a stated payload shock qualification level |
| **5** | **E35** | The payload sits 20 mm from the array at **442× a magnetometer's full scale**, and soft-magnetic parts leave permanently magnetised. The claim that the satellite is never modified is therefore false as built, and that claim is the product | **Carry a longitudinal-separation layout into `cad/parameters.json` and recompute the field at the real payload station**, or write a magnetic-cleanliness limit into a payload interface document. Computation, not test |

### Where the rest sit

**Serious but not fatal — each has a known fix and the fix is affordable.** **P46** (K_t is
4.42 % high) moves the design point but not the architecture; **P28**, **P36**, **P37**, **P41**
and **P32** are design or analysis work with no result yet suggesting the machine cannot be
built; **E29** and **E31** compound E33 rather than standing alone; **E32** reduces to a written
inhibit.

**Bounded scope rather than viability.** **E9**, **P44** and **E28** narrow what the machine can
serve without threatening whether it works at all.

**Bookkeeping, provenance and hygiene.** **P10**, **P14**, **P19**, **P20**, **P33**, **P35**,
**P38**, **P39**, **E16**, **E18** and **E25** are records that disagree with each other or with
their sources. They matter for whether the repository can be trusted; none of them is a reason
the hardware would fail.

**Not engineering.** **E14** and **E15** are disclosure and funding.

### The disagreement this ranking has with the register's own severities

**E4 carries no severity label at all** and is ranked second here. **P34** is labelled HIGH and
does not appear in the top five, because a magnetometer-carrying payload being excluded bounds
the market rather than the machine — and **E35** may remove the constraint entirely. **P45** is
labelled LOW and is genuinely low. **Confirmed as written.** If it is revised later, the entries themselves are unchanged and this
section is the only thing that needs editing.

---

## P: Errors found while building this repo (paper does not match its own scripts)

> **STATUS (2026-07-23): P1, P4 all RESOLVED in `paper/paper.tex`.** Fixes, causes and
> before/after values are logged in `CHANGELOG.md` (entries P2-01, P2-04). The items are
> kept in full below for the audit record. Two related defects found in the process were
> also fixed: the F06 conjunction figure was regenerated at the rated velocity, and a
> stale `astro.py` docstring value was corrected, both logged in `CHANGELOG.md`.

### P1. Conjunction minimum is wrong AND not a robust quantity: HIGH PRIORITY
> **Status:** `CLOSED` — resolved; see the entry for what closed it

**RESOLVED 2026-07-23, see CHANGELOG.md P2-01.**
The paper states a 30-day minimum satellite-to-stage approach of **45.3 km**. That
figure was computed at **20.65 m/s**, the superseded operating point. At the paper's
own rated velocity of **20.37 m/s**, `analysis/astro.py` gives **4.6 km**.

Worse, the quantity is fragile. Sweeping ejection velocity:

| Î”v (m/s) | min approach (km) |
|---|---|
| 20.00 | 37.5 |
| 20.37 (rated) | **4.6** |
| 20.50 | 56.1 |
| 20.65 (paper's value) | 45.3 |
| 21.00 | 63.4 |

This is a near-resonant beat sample, not a design property. A ±2.5 % velocity change
moves it by more than an order of magnitude.

**Follow-up:** `validation/A6_conjunction_cara.md` specifies the quantitative version,
probability of collision via NASA's CARA tools, which integrates over the covariance
instead of sampling one geometry. The test is whether Pc stays stable across the velocity
sweep that moves minimum distance by an order of magnitude.

> **A6 ran 2026-07-31 in a reduced form and P1 stays open.** Without GMAT, CARA or
> Space-Track there is no real covariance, so a 2-D Pc was computed against `astro.py`'s own
> propagator with an assumed one. **The stability test came back void**: at 14 to 63 km miss
> distances against a hundreds-of-metres covariance, Pc underflows double precision, and a
> spread of zeros is not a number.
>
> **What the run found instead is better than what it was looking for.** Pc has a maximum over
> covariance scale — a covariance wide enough to reach a 14.5 km miss is too diffuse to put
> probability inside a 5 m disc — and that maximum is **3.7e-8, some 2700x below the 1e-4
> anyone would act on, for any covariance whatsoever.** So Pc is not *robust* where distance is
> fragile; it is **irrelevant**, bounded far below any action threshold.
>
> **This does not close P1**, because a bound is not a probability. It does say the paper's
> current position — the 9.9-day realignment period plus mandatory per-shot COLA, and no
> minimum-distance claim — is the right one, and is now supported rather than merely honest.

**Fix:** stop quoting a specific minimum distance as a safety result. Reframe around
what IS robust: the ~8.1-day phase realignment period, and the mitigation of disposing
of the host stage before the first realignment. State plainly that per-shot COLA is
mandatory because the approach geometry is sensitive to exact ejection velocity.

### P2. Peak current is stale: MEDIUM PRIORITY
> **Status:** `CLOSED` — resolved; see the entry for what closed it

**RESOLVED 2026-07-23, see CHANGELOG.md P2-02.**
Paper says **323 A**. That belongs to the superseded 130 kA/m point. At the rated
140 kA/m, `motor_model.py` gives **392 A**. Fix the paper, and check that the SiC
device derating discussion still holds at the higher current (it should, 96 V rail,
1200 V devices, but the current rating of the bridge and busbars needs restating).

### P3. Far-field stray values don't reproduce exactly: LOW PRIORITY
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


> **QUANTIFIED 2026-08-05 by `analysis/far_field_sensitivity.py`.** P3's diagnosis was right and
> the size of it was not known. Sweeping `build_field(n_wave)` from 3 to 15 wavelengths against a
> converged reference:
>
> | Station | Deviation at the default n=7 (336 mm) | Converged |
> |---|---:|---:|
> | 10 mm | **0.64 %** | 22.688 mT |
> | 20 mm | 4.36 % | 4.290 mT |
> | 50 mm | **374 %** | 0.104 mT |
>
> **The 10 mm value is converged and the 50 mm value is not remotely.** At n=7 it is 0.49 mT
> against a converged 0.104, and it is still 16 % out at n=13. The paper's 1.0 mT corresponds to
> an array shorter than the CAD's 340 mm. **No 50 mm stray figure in this project should be
> cited**, including the 0.4 mT in `field_verification.json`, until the array length is set to
> the CAD value and the model converged.
>
> This needs no mesh: magpylib's Cuboid is an exact analytic solution for a uniformly magnetised
> block, so the field is already three-dimensional. What was missing was the convergence check.
**RESOLVED 2026-07-23, see CHANGELOG.md P2-03.**
Paper quotes 22.7 / 4.7 / 1.0 mT at 10 / 20 / 50 mm. `verify_field.py` reproduces
22.7 mT at 10 mm exactly but gives 4.3 and 0.4 mT at 20 and 50 mm. Likely sensitivity
to modelled array length (edge effects dominate the far field). The 10 mm value is the
one that sets the keep-out spec, so this is minor, but resolve it before anyone cites
the 20/50 mm numbers.

### P4. Brake fin temperature rise conflates per-shot with per-campaign: MEDIUM PRIORITY
> **Status:** `CLOSED` — resolved; see the entry for what closed it

**RESOLVED 2026-07-23, see CHANGELOG.md P2-04.**
The paper states the 0.86 kg copper fin sees "an adiabatic 37 K transient rise" **per
shot**, and later refers to "the adiabatic per-shot rises (0.3 K coil, 37 K fin)".

`analysis/sizing.py` gives 1008 J into 0.86 kg of copper = **3.0 K per shot**. The 37 K
figure is the *full 12-shot campaign* total if the fin never radiated between shots
(12 x 1008 J / 331 J/K = 36.5 K).

The design is therefore *less* thermally stressed than the paper claims, but the number
as written is wrong and internally inconsistent.

**Fix:** state 3.0 K per shot, and 37 K as a bounding campaign-adiabatic case that
radiation between shots relieves. Same correction applies to the coil: 0.28 K per shot,
3.3 K campaign.

---

## P: CAD reconciliation and packaging (found in the 2026-07-23 Fusion 360 CAD build)

> These arose when the parametric design was taken into CAD across nine Fusion documents.
> The CAD is authoritative for **geometry and fit only**; `analysis/*.py` remains
> authoritative for **mass and performance** until FEA closes the open items. All
> geometry values below are traceable to `cad/parameters.json`. **No number in
> `analysis/*.py` or `paper/paper.tex` has been changed** on the strength of the CAD.

### P5. CAD sled mass contradicts the parametric assumption: RESOLVED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **RESOLVED.** `motor_model.M_SLED` and `sizing.M_SLED` now carry the CAD-derived **9.445 kg**
> (P15), not the 4.86 kg parametric estimate. A4 ran, the drawn plate passed all three
> structural bands, and the measurement fell in the decision rule's ≥ 6.80 kg branch, so the
> rule resolved this rather than a judgement call. **Caveat carried forward:** 9.445 kg is
> the as-drawn, unpocketed geometry and A4 reports a 17x stress margin, so a rib-stiffened
> chassis would recover mass. Designing one is the open successor to this item
> (`docs/ROADMAP.md`), and it is tracked under E2 rather than here.

Original item follows for the audit trail.

> **UPDATE 2026-07-28, A4 structural leg has RUN (CalculiX).** The as-drawn 6 mm plate
> passes every declared band: 0.0194 mm airgap closure against a 0.025 mm per-plate budget,
> 33.7 MPa against 587 allowable, first mode 3408 Hz against >200. So there is **no
> structural argument for the chassis being lighter than drawn**, a lighter one has to be
> designed (rib-stiffened), not assumed. Combined with P15's CAD-derived 9.445 kg, the decision
> rule's ≥6.80 kg branch stands and the machine as it exists delivers **16.53 m/s**.
The first-pass Fusion sled (6 mm Ti-6Al-4V chassis, stiffness-driven by the ±0.05 mm gap
tolerance under 3.7 kN inter-array attraction — 2.69 kN since A12 — **no structural FEA behind it**) implies a
sled mass of **~7.50 kg**. `analysis/mass_properties.py` assumes **4.86 kg**, which
`motor_model.py` hard-codes as `M_SLED` and which sets the headline exit velocity. Both
are estimates (one CAD-geometric, one parametric-solid) and neither is FEA-verified. Do
not change the scripts until analysis A4 closes the chassis, specified with a
pre-declared decision rule in `validation/A4_sled_structural.md` (CalculiX or
Code_Aster, both free, both read `cad/step/gen3/EMOCD_Sled_Gen3.step`). Source:
`cad/parameters.json` (sled group, `PROVISIONAL_PENDING_FEA`).

### P6. Payload seating / orientation: RESOLVED (by CAD, 2026-07-23)
> **Status:** `CLOSED` — resolved; see the entry for what closed it

Resolved via the rail interface: the 3U payload now models the four CubeSat Design
Specification corner rails (8.5 mm, `cad/parameters.json` `payload_3u`), which fix seating
and orientation against the sled cradle. No further action.

### P7. Brake sits past the release point: geometry / ConOps — CLOSED 2026-08-10
> **Status:** `CLOSED` — resolved; see the entry for what closed it

The eddy brake occupies **x = 1530-1740 mm**, beyond the **1500 mm** satellite release
point, on an 1800 mm longeron. The sled runs on into the brake after the payload departs
consistent with the fire-then-arrest ConOps, but it forces the track and enclosure to
extend past release, which drives the envelope length (see P9). Source:
`cad/parameters.json` (brake, track).

**Closed 2026-08-10 by the Gen4 layout, geometrically.** `docs/GEN4_STATUS.md` moves release to
**s = 1200 mm** on a 900 mm acceleration stroke and puts brake-fin entry at **s = 1222 mm**, so
the release station sits **22 mm before** the fin reaches x = 1530 mm. The fin then occupies the
brake interval over 330 mm of sled travel, s = 1222 to 1552 mm. **The release-into-brake overlap
is gone, and it is gone without adding track length.** Recorded against **A16**, which computed
the Gen4 finite-stator thrust on this layout, and **P32**.

**The second half of this entry was never P7's to carry.** "It forces the track and enclosure to
extend past release, which drives the envelope length" is true and still true — Gen4 keeps the
track at 1800 mm and the brake at 1530–1740 mm. **That is the envelope problem, and the envelope
problem is P9**, which is a kill-criterion item with an owner decision attached. P7 asked whether
the *overlap* was a defect. It was, Gen4 resolves it, and nothing is gained by keeping a second
entry pointed at P9's problem.

> **What this close is worth, stated plainly.** Gen4 is a CAD configuration record and **has not
> been exported into this repository** — `GEN4_STATUS.md` says so in its own first paragraph, and
> the committed STEP, analyses and baseline remain the Gen3 record. So this closes a **geometry
> question against a geometry that is not yet committed**. It is closed because the layout
> resolves it and the layout is recorded, not because anything was measured. If the Gen4 export
> lands with a different release station, this reopens.

### P8. Exit velocity provisionally 17.88 m/s pending sled structural FEA: RESOLVED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **RESOLVED, and not at 17.88 m/s.** That figure came from the 7.50 kg CAD estimate. The
> CAD-derived mass is 9.445 kg, so the rated velocity is **16.537 m/s at 10.7 g**, now
> propagated into `analysis/`, `paper/paper.tex`, the figures and every front page. The
> machine is no longer acceleration-limited: at 10.7 g against a 25 g cap it is
> thrust-and-mass limited, which changes what recovering velocity means (mass or current,
> not stroke).

Original item follows for the audit trail.

If the CAD sled mass (P5) holds, exit velocity falls from the script's **20.37 m/s** to a
provisional **~17.88 m/s** (with acceleration ~12.5 g, efficiency ~24 %, recoil
~71.5 N·s, lifetime multiplier x1.68, all CAD-corrected and provisional). **These values
are NOT propagated into `analysis/*.py` or `paper/paper.tex`**; the scripts stay
authoritative until analysis A4 locks the sled mass (`validation/A4_sled_structural.md`,
which fixes in advance which of the two estimates wins at which mass). Do not hard-swap
20.37 to 17.88 anywhere. Source: 2026-07-23 CAD Master Plan; see README headline note.

### P9. Closed envelope exceeds ESPA Grande by ~44%: packaging / host — CLOSED 2026-08-10
> **Status:** `CLOSED` — resolved; see the entry for what closed it

The closed installed envelope is **1839x 530x 940 mm** (`cad/parameters.json`). The
1839 mm length exceeds ESPA Grande's ~1270 mm longest-dimension class by ~44%, because
the brake lives past the 1500 mm release point and the enclosure spans it. Owner decision
(cannot be made in code): re-scope the host to POEM / custom accommodation (the paper
already leans host-agnostic), or shorten the track / repackage the brake. This supersedes
the earlier 1825x 516x ~1030 mm figure; the height change (1030 to 940) exceeds what skin
thickness explains and is **flagged for re-verification** in `cad/parameters.json`.

> **CLOSED 2026-08-10 by [ADR-023](docs/adr/023-target-host-class.md): re-scope the host.** The
> target class is a restartable upper stage, kick stage or hosted platform — POEM class. **ESPA
> Grande envelope compliance is not a requirement of this design.** The ESPA *bolt pattern* stays
> as the mechanical interface; what is given up is compliance with a *port envelope*, which is a
> different thing — the deployer mounts on a stage, not in a port.
>
> **The alternative was priced first.** Overhead that is not acceleration zone is 539 mm and does
> not shrink, so fitting 1270 mm means a 731 mm accel zone, and velocity goes as √s:
>
> | | Accel zone | Exit velocity | Lifetime multiplier |
> |---|---:|---:|---:|
> | As designed | 1300 mm | **16.388 m/s** | ×1.62 |
> | Fit ESPA Grande | 731 mm | **12.286 m/s** (−25.0 %) | ×1.44 |
> | Fit, 150 mm repackaged | 881 mm | 13.495 m/s (−17.7 %) | ×1.49 |
>
> **Why re-scope rather than shorten.** ADR-002 put the host as a spent upper stage in 2023 and
> ADR-010 specified the interface host-agnostically; **the ESPA-Grande requirement was a leftover
> from an earlier framing that two accepted decisions had already contradicted.** Shortening
> spends 25 % of the number every product claim rests on, to enter a market this architecture was
> not designed for, and it barely touches the mass threat that is closest. The repackaging branch
> depends on a brake layout nobody has drawn, and **P28** already says the arrest section is
> oversubscribed.
>
> **What this does not do, and it is the part that matters: it does not make kill criterion 2
> pass.** Re-scoping a target after seeing the geometry fail is the band rule violated on a
> threshold. The criterion is unchanged — **it has moved from CROSSED to NOT EVALUABLE**, because
> no accommodation envelope for a POEM-class host is public (**E5**). This design cannot currently
> demonstrate that it fits anything, which is a worse epistemic position than a clean fail against
> a published number, and it is recorded as such. **A decision that converts a measured failure
> into an unmeasurable unknown is not progress.** What it buys is that the project stops carrying
> a requirement it had already abandoned twice. **E5 rises in priority accordingly**, and
> `docs/MARKET.md` needs re-scoping against the lost port population.

### P10. Enclosure, radiator, and packaged avionics absent from the mass rollup: RESOLVED 2026-08-16 by A46
> **Status:** `CLOSED` — resolved; see the entry for what closed it
> **Corrected.** An **8.0 kg placeholder with no derivation** now sits in `mass_properties.py`,
> named `(P10 PLACEHOLDER, 8.0 kg, no derivation)` so it cannot be cited as computed. Dry mass
> 76.5 → **84.5 kg**, per 3U satellite 6.378 → **7.042 kg**, and **kill criterion 1 goes from
> crossed by 3.2× to crossed by 3.5×**. `KILL_CRITERIA.md` already flagged a plausible 20 kg; 8 kg
> is the lean end and deliberately the less flattering choice to leave un-taken. **ADR-030.**
The ninth document (`EMOCD_Enclosure`) adds 2 mm aluminium skins, a 1600x 200x 3 mm
radiator, and equipment bays for the supercapacitor bank, PPU, sequencer, and IMU. **None
have line items in `analysis/mass_properties.py`**, so the 72.3 kg dry-mass rollup is
incomplete. Add line items once masses are estimated (do not alter existing items without
cause). Source: `cad/parameters.json` (`enclosure.mass_note`).

> **Closed 2026-08-16 by [A46](validation/A46_enclosure_buildup.md).** The placeholder is gone and
> five derived line items stand in its place, each tracing to a dimension in `cad/parameters.json`:
> **skins 32.82, frames 8.20, radiator 2.59, bay boxes 1.87, fasteners 4.55 — 50.04 kg.** The
> placeholder was **low by 6.3×**. Dry mass 84.5 → **126.6 kg**, per 3U satellite 7.042 →
> **10.547 kg**, kill criterion 1 from crossed 3.5× to **crossed 5.3×**. A honeycomb sandwich
> gives 29.98 kg for the same five lines; **adopting one is a design decision and is not taken
> here**, so the rollup carries the monolithic 2 mm skins the parameter file specifies.

### P11. The corrections may never have reached the submitted paper: RESOLVED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **RESOLVED: nothing has been submitted anywhere.** checked 2026-07-29.
> There is no version of record, so P1, P4 are not loose in any published document and no
> corrigendum is needed. `paper/archive/EMOCD_submission_uncorrected.pdf` is a draft build
> whose filename overstates its status, it was never sent.
>
> **This unblocks the paper edits that were batched behind it.** The reason P12 and P16 were
> left untouched in `paper/paper.tex` was that editing the source without rebuilding the PDF
> would split it from a published record. There is no published record. The paper is a draft,
> the only cost of editing it is that the committed PDF goes stale until it is recompiled,
> and that is a normal state for a draft rather than a defect. **Fix P12 and P16 in
> `paper.tex` and rebuild before anything is submitted.**

Original item follows, kept for the audit trail.


`paper/archive/EMOCD_submission_uncorrected.pdf` is a build of the paper that still
carries all four P1, P4 values (323 A, 23 A/mm² at 140 kA/m, 37 K per shot, 45.3 km
conjunction minimum). Its filename says *submission*. If that is genuinely the version
that went to the conference, then P1, P4 are corrected **only in this repository** and the
version of record is still wrong, which is a different situation from the STATUS block
at the top of this file, and one that a corrigendum, not a git commit, has to fix.
**Confirm which build was submitted.** If it was the uncorrected one, decide between
withdrawing, submitting an erratum, or correcting at the camera-ready stage, and record
the outcome here. If the submitted build was in fact compiled from the corrected
`paper.tex`, delete this item and say so in `CHANGELOG.md`.

### P12. The paper contradicts the CAD in two places: RESOLVED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **RESOLVED in `paper/paper.tex`.** The Limitations section no longer says masses derive
> from a parametric model rather than detailed CAD; it states what the CAD solid-volume calculation gives and what
> that costs. The ESPA-Grande envelope is no longer asserted as a capability, the
> requirement statement, the Fig. 2 caption and the accommodation section now record 1839 mm
> against the ~1270 mm class and name it an open packaging problem (P9). The mounting-interface
> statements were true and are unchanged. **The committed PDF still predates these edits**;
> see `paper/README.md`.

Original item follows for the audit trail.

Found while sweeping the repository for stale values. Both are prose claims, not computed
numbers, and neither has been changed in `paper/paper.tex`:

1. **Limitations (Sec. XV) says "Masses derive from a parametric solid model, not detailed
   CAD."** That was true when written and is now false, nine Fusion documents exist in
   `cad/`. The honest replacement is not "CAD exists" but the sharper statement: two mass
   estimates exist, they disagree by 54 %, and neither is FEA-verified (P5, P8).
2. **The paper claims an "ESPA-Grande-class envelope and mass allocation"** (abstract-level
   requirement, the Fig. 2 caption, and again in the accommodation section). The CAD closed
   envelope is 1839 mm against the ~1270 mm class limit, **P9, ~44 % over**. As written,
   the paper asserts a compatibility the geometry does not support.

Item 2 is the serious one: it is a capability claim, not a caveat, and it is the kind of
thing a reviewer with an ESPA user's guide open would catch immediately.

**Why this is not fixed yet.** Editing `paper.tex` without rebuilding the PDF would put the
source and the committed build out of step, and no TeX engine is available in the working
environment. It is also entangled with **P11**: until it is known which build is the
version of record, it is not clear whether this is a camera-ready edit or a corrigendum.
Resolve P11 first, then fix both items in one pass and rebuild.

### P13. The committed STEP set was mixed-generation, with two stubs: RESOLVED 2026-07-28
> **Status:** `CLOSED` — resolved; see the entry for what closed it

Found while importing `EMOCD_figs.zip`. The nine files in `cad/step/` matched no single CAD
generation, and two of them were single solids:

| Document | Was committed | Gen1 | Gen3 |
|---|---|---|---|
| Stator | **1 body** | 324 | 162 conductors |
| Interface_ESPA | **1 body** | 6 | 6 + bolt holes |
| Sled | 12 | 5 | 16 |
| Payload_3U | 5 | 5 | 1 |
| Track | 6 | 8 | 4 |
| Assembly | 225 | 43 | 227 |

The stator export therefore contained no winding at all, while `cad/README.md` claimed
"STEP exports of every document" and the paper's §IV-B rests on a winding-resolved model.
Anyone opening the committed stator to check the conductor layout would have found a block.

**Resolved** by replacing the set with `cad/step/gen1|gen2|gen3/`, the three audited
generations. Body counts measured on import with `grep -c MANIFOLD_SOLID_BREP`, not copied
from the source changelog.

### P14. Gen3 CAD defects not previously tracked: CORRECTED 2026-08-13
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `DECISION` — keep Gen4 or declare Gen5 the only generation -- D8

> **Corrected 2026-08-13 by supersession, not by fixing Gen3.** Gen5 is generated from
> `cad/parameters.json` by `cad/build_gen5.py` ([ADR-026](docs/adr/026-cad-built-from-parameters.md)), and
> `build_gen5.py --check` reads 23 dimensions back out of the generated geometry and compares
> them to the parameter file. **It passes.** A defect of the form "the CAD disagrees with
> `parameters.json`" cannot exist in a model that is a function of `parameters.json`.
>
> | | Gen3 defect | Disposition |
> |---|---|---|
> | **G3-D1** | Cassette height 640 mm against the parameter's 690 | **Gone.** `magazine.cassette_height_z = 690` and the generated model is built from it |
> | **G3-D2** | No roller channels, guide flanges or cross-tie outriggers | **Gone.** `build_gen5.py` builds *"two longerons with roller channels, guide rails and launch locks"* from `roller_channel_y_inner`, `guide_rail_y_inner/outer` and `guide_rail_z_contact` |
> | **G3-D4** | Stator layer count open, one layer or two | **Not a CAD defect and never was.** It is a design decision that sits upstream of K_t, and it is **PII-3** in `docs/VAULT.md`, priced at 20.61 m/s on a 7.50 kg sled |
>
> **Gen3 itself is not corrected and will not be.** It is a superseded generation kept for the
> record, like `legacy/`.

From the Gen3 audit in `cad/CHANGELOG_CAD.md`, verified against the exports where possible.
None of these were in this file before.

| ID | Defect | Consequence |
|---|---|---|
| G3-D1 | Cassette height **640 mm** in Gen2 and Gen3 against `parameters.json` `magazine.cassette_height_z = 690` | 50 mm short. Either the CAD or the parameter is wrong; `parameters.json` wins by rule, so the CAD needs correcting |
| G3-D2 | Track is longerons and launch locks only, **no roller channels, guide flanges, or cross-tie outriggers**, all of which `parameters.json` specifies | The 205 mm overall track width exists only as a parameter. The rollers on the sled have nothing modelled to run in |
| G3-D4 | **Stator layer count undecided at the time.** Gen1 built two layers (324 conductors), Gen2 and Gen3 one (162) | `parameters.json` flags the decision open. Roughly x2 force for the same sheet current against x2 copper mass, never computed. This sits upstream of Kt and therefore of the headline velocity |
| G3-D5 | Halbach arrays **not re-centred** after the chassis grew 360 to 488 mm | `sled.halbach_array_x_start = 230 mm` is inherited from the shorter chassis. Array position relative to the winding is what Kt depends on |
| G3-D6 | **No payload-on-sled rigid joint** in any generation | `parameters.json` `documents.EMOCD_Assembly` specifies one. Without it the assembly cannot express the payload riding the sled, which is the thing being modelled |

| G3-D12 | **Assembly geometry extends 156 mm aft of the recorded envelope.** `EMOCD_Assembly_Gen3.step` spans x = −188 to 1810 mm; `parameters.json` records the installed envelope as −32 to 1807 mm | Either the assembly parks the sled further aft than the envelope assumed, or the envelope was measured without it. Found on 2026-07-28 while meshing the assembly for `cad/stl/`. It makes P9 worse, not better: 1998 mm against the ~1270 mm ESPA Grande class limit is ~57 % over rather than ~44 %. Measure which component owns the −188 mm face before changing either number |

**Resolved and recorded:** ESPA bolt holes (24x M9 on Ø400 mm BCD) were absent in Gen1 and
Gen2 and are modelled in Gen3, G1-D5 closed.

**Two discrepancies between `cad/CHANGELOG_CAD.md` and its own exports**, found on import
and left in place there with a note rather than edited:

- **The Gen3 brake-placement fix is not in the exports.** G2-D4 says the Gen2 brake sat at
  the local origin and Gen3 moved it to x = 1530 mm. `EMOCD_Brake_Gen2.step` and
  `EMOCD_Brake_Gen3.step` are geometrically identical, 3 bodies each, 79 points each,
  differing only in file name and time stamp, and **both** already place the brake at
  1530-1740 mm. The fix may have been applied to the Fusion document before the Gen2 export
  was taken; either way the export does not show the defect it is said to have.
- Body counts: `EMOCD_Payload_3U_Gen1.step` measures 5 solids where the inventory says 1,
  and `EMOCD_Sled_Gen1b.step` measures 11 where it says ~16.

The sled fix **is** verifiable: Gen2 chassis half-length measures 180 mm (360 mm plate),
Gen3 measures 244 mm (488 mm plate), so G2-D1 is genuinely closed.

> ### Audited against Gen4, 2026-08-10: two of the six are answered, four carry
>
> Each defect read against the Gen4 configuration recorded in
> [`docs/GEN4_STATUS.md`](docs/GEN4_STATUS.md). **The standard of evidence is the same one P7
> closes under and it is weaker than it looks:** Gen4 exists in Fusion and **has not been
> exported into this repository**, its own status file says the committed STEP, analyses and
> baseline remain the Gen3 record, and the export gate is deliberately closed until the
> finite-stator result is recorded. So "answered by Gen4" means *the successor layout does not
> have this defect*, not *the repository no longer has it*.
>
> | ID | Against Gen4 | Verdict |
> |---|---|---|
> | **G3-D5** Halbach arrays not re-centred after the chassis grew 360 → 488 mm | Gen4 states the arrays explicitly in the 488 mm chassis local frame, x = −96 to +244 against a chassis of −180 to +308. The inherited `halbach_array_x_start = 230 mm` no longer governs, and **A16 computed the Gen4 finite-stator thrust on this layout**, reproducing `F_cmd` to 0.000 % at full overlap | **Answered.** The array position is now stated rather than inherited, and has been used in an analysis |
> | **G3-D12** Assembly extends 156 mm aft of the recorded envelope | Gen4 puts the stowed sled at s = 300 mm, where the **backstop clears the aft enclosure skin by 24 mm** in the envelope check — a clearance where Gen3 had a 156 mm protrusion | **Answered.** And it removes the ~57 % ESPA overrun this defect implied, back to P9's ~44 % |
> | **G3-D1** Cassette height 640 mm in CAD against `parameters.json` 690 mm | Gen4 records nothing about cassette height | **Carries** |
> | **G3-D2** Track has no roller channels, guide flanges or cross-tie outriggers | Gen4 lists the track as "existing source geometry", unchanged, and states in its own limitations that **"the roller-span discrepancy remains open"** | **Carries, explicitly** |
> | **G3-D4** Stator layer count still open, 1 vs 2 layers | Gen4 lists the stator as "existing source geometry". The decision that sits upstream of K<sub>t</sub> is untouched | **Carries** |
> | **G3-D6** No payload-on-sled rigid joint in any generation | Gen4 completes the twelve **stowed** payload occurrences in the cassettes, which is a different thing, and says they are "not independently checked as a mass, mechanism, or interference closure" | **Carries** |
>
> The two `cad/CHANGELOG_CAD.md`-versus-export discrepancies above are **unaffected by Gen4**:
> they are disagreements between the CAD change log and the Gen2/Gen3 exports already committed,
> and a new configuration does not resolve what an old export does or does not contain.
>
> **The one that matters most is G3-D4**, and it is worth saying why it is not a bookkeeping
> item at all. One stator layer or two is roughly ×2 force for the same sheet current against ×2
> copper mass, **it has never been computed**, and it sits upstream of K<sub>t</sub> and
> therefore of the headline velocity. It is filed here as a CAD defect and it is really an
> unmade design decision, in the same class as the four in `docs/PHASE_I_CLOSURE.md` §10.

**What would close it:** the four carried defects corrected in CAD and re-exported, which the
Gen4 export gate already blocks on. **P14 does not close on this audit** — two of six are
answered by a configuration that is not yet in the repository, and the remaining four are
untouched.

### P15. The Gen3 sled as drawn is 9.45 kg, above BOTH existing estimates: RESOLVED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **RESOLVED by adoption.** 9.445 kg is now the operating point across `analysis/`, the
> paper and the figures. `mass_properties.py` keeps the parametric breakdown for the record
> and carries the 4.59 kg difference as an explicit reconciliation line, so system dry mass
> (76.9 kg, up from 72.3) no longer understates.

Original item follows for the audit trail.

Measured on 2026-07-28 from `cad/step/gen3/EMOCD_Sled_Gen3.step`: exact solid volumes from
the OpenCASCADE kernel, times material densities (NdFeB 7500 kg/m3 is this repo's own value,
from `sizing.py`).

| Estimate | Sled mass | Exit velocity |
|---|---|---|
| `mass_properties.py` parametric | 4.86 kg | 20.37 m/s |
| P5's CAD figure | 7.50 kg | 17.87 m/s |
| **Gen3 geometry, CAD solid-volume result** | **9.445 kg** | **16.53 m/s** at 10.7 g, 19.0 % efficiency |

The method reproduces P8 exactly when fed 7.50 kg, it returns 17.87 m/s against P8's stated
17.88, so the discrepancy is in the mass, not the method. Dominated by two chassis plates
(3.63 kg of titanium) and the magnet arrays (3.67 kg of NdFeB).

**What it does not settle.** This is geometry times density, not the structural FEA that A4
specifies. The plates are drawn solid with no lightening pockets, and a real design would
pocket them; the stiffness constraint (airgap held to ±0.05 mm) is still unevaluated. But
A4's pre-declared rule already says a mass at or above 6.80 kg makes 17.88 m/s the headline,
and this is well past that. **Whichever way the FEA goes, the 20.37 m/s headline is not
supported by the geometry that currently exists.**

Do not edit `analysis/*.py` on the strength of this. Run A4, then propagate once.

### P16. The lifetime-multiplier INVARIANCE claim is falsified: HIGH, NEW 2026-07-28
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

GMAT R2022a, run headless against the bands declared in `validation/A5_astro_orekit.md`
before the run:

| Solar activity | GMAT multiplier | vs x1.80 | Band ±5 % |
|---|---|---|---|
| High (F10.7 250) | 1.7302 | −3.88 % | pass |
| Mean (F10.7 150) | 1.7750 | −1.39 % | pass |
| **Low (F10.7 70)** | **2.0739** | **+15.21 %** | **FAIL** |

Spread across the three: **18.48 %** against a ≤5 % band.

**The mechanism, and it is not subtle.** `analysis/astro.py` represents solar activity as a
uniform multiplicative scale on density (`rho(h, scale)`). Sweeping that scale across a
factor of **forty** moves the multiplier from 1.7992 to 1.7968, 0.1 %. A uniform density
factor divides both lifetimes by the same number, so **the ratio is preserved by
construction**. The sweep that the paper cites as demonstrating invariance cannot, in
principle, do so.

MSIS varies the *shape* of the density-altitude profile with F10.7, not only its magnitude.
The boosted orbit's apogee sits ~37 km above the baseline's, the two sample the profile
differently, and the ratio moves. Corroboration from the same runs: the absolute-lifetime
error changes **sign** across the range, GMAT is 2.5x longer at low activity, 9 % shorter
at mean, 23 % shorter at high. An error that changes sign is a wrong shape, not a
miscalibration.

**What survives:** x1.80 as a point value at mean and high activity, checked independently
and comfortably inside band. **What does not:** invariance.

Reproduce the sweep in six lines, no edit to any script:

```python
from analysis.astro import lifetime, boosted_elements, RE
a0 = RE + 450e3
ab, eb = boosted_elements(450e3, 20.37)
for s in (0.25, 0.5, 1.0, 2.5, 5.0, 10.0):
    print(s, lifetime(ab, eb, scale=s) / lifetime(a0, 0.0, scale=s))
```

**Where the claim appears:**

| Location | Text | Status |
|---|---|---|
| `paper/paper.tex` **abstract** | "a ratio shown invariant across ballistic coefficient and a fivefold solar-activity density range" | corrected 2026-07-29, multiplier now quoted at a stated activity level, no invariance claimed |
| `paper/paper.tex` Sec. V-B | "invariant to two decimal places" | corrected 2026-07-29, carries the GMAT three-level result and the mechanism |
| `paper/paper.tex` sensitivity section | "a multiplier invariant across a fivefold density range" | corrected 2026-07-29 |
| `paper/paper.tex` **Limitations** | "the demonstrated invariance of the ratio is the defensible result", the paper leaned on this specific claim | corrected 2026-07-29, no longer offered as the defensible result |
| `README.md`, `wiki/Home.md` headline tables | "x1.80, invariant across BC and solar activity" | corrected 2026-07-28 to "x1.80 at mean activity, invariance falsified, see P16" |
| `docs/RESULTS.md` A5 section and status bar | "GMAT: x1.73 vs x1.80, within band" | corrected 2026-07-28, three-level table, per-activity chart, 40x-sweep chart, status FAIL |
| `docs/index.html` (Pages site) | headline row and GMAT section | corrected 2026-07-28 |
| `docs/VALIDATION_REPORT.md` §2 | "2.55 % spread, inside the ≤5 % band" | corrected 2026-07-28, retraction stated in place |
| `docs/INVENTORY.md` A32 | "Solar-activity UQ, x1.80 invariance" | flagged against P16 |
| `CHANGELOG.md` VAL2-02 | "Invariance spread 2.55 %, inside ≤5 %" | marked SUPERSEDED, text left intact as audit record |
| `paper/figures/F11_uq.png` **caption** | "absolute lifetimes vary fivefold; the x1.8 multiplier does not", a fifth location, missed when this list was written | corrected 2026-07-29, figure now plots `astro.py` against GMAT side by side |

**All documented locations are now corrected.** What is *not* closed:

1. **The BC half has still never been tested against a real atmosphere.** It is proven a
   tautology in `astro.py`, and the paper no longer claims it, but nobody has run GMAT at
   BC 40 and 90 to find out what the true BC dependence is. Until that happens the honest
   position is "unknown", not "invariant".
2. **The GMAT numbers themselves are now stale**, every run was at 20.37 m/s (P19).
3. **The committed PDF predates the correction** (`paper/README.md`).

This item stays open on (1).

**Ballistic-coefficient invariance is not "suspect", it is the identical tautology, proved
2026-07-29.** The abstract's sentence has two halves: invariant across *ballistic
coefficient* **and** across a *fivefold solar-activity density range*. Both rest on the same
construction. In `lifetime()` the drag term is

```python
ft = -0.5 * rho(h, scale) * v ** 2 / BC
```

`scale` and `1/BC` are the **same multiplicative slot**. Scaling one is mathematically
indistinguishable from scaling the other, so a BC sweep is a density sweep wearing a
different label. The reciprocal test confirms it exactly:

| Configuration | Multiplier |
|---|---|
| BC = 61, scale = 2.0 | 1.7987 |
| BC = 30.5, scale = 1.0 | **1.7987** |
| BC = 122, scale = 1.0 | 1.7991 |
| BC = 61, scale = 0.5 | **1.7991** |

And the plain sweep across a 5x BC range, 30 to 150 kg/m²: 1.7983 to 1.7992, spread
**0.05 %**.

So the position is worse than "one half falsified, one half untested". **Neither half of the
claim was ever tested by a method capable of falsifying it**, and the half that was
independently checked failed. Closing the BC half needs the same medicine as the solar half,
GMAT runs at BC 40 and 90, because MSIS's response to ballistic coefficient is not a uniform
rescale, for the same profile-shape reason found above.

**Do not edit `analysis/astro.py`.** Its arithmetic is not wrong; its atmosphere
parameterisation cannot express the effect being claimed. The fix is either a variable-shape
atmosphere in the script or dropping the invariance claim and keeping the point value,
that is a judgement, not a patch. Paper edits batch with P11/P12.

### P17. The inter-array attraction feeding the A4 FEA is 37 % high: **RESOLVED 2026-07-31 by A12**
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **Closed by [`validation/A12_inter_array_force.md`](validation/A12_inter_array_force.md), five
> of five declared bands.** A second numerical method — a Maxwell stress tensor integrated over
> the mid-gap plane, sharing only the block model of the magnets — gives **2627.6 N** against
> magpylib's **2686.6 N**, 2.2 % apart. `sizing.py` adopted 2686.6 N under an adoption rule
> declared before the run: attraction 3.68 → **2.69 kN**, plate stress 33 → **24 MPa**, margin
> 20.2 → **28.1**. A4 is not re-run; it was loaded 37 % heavy, so it was conservative and its
> verdict stands.
>
> **The number below was right and the mechanism below is wrong**, which is why the entry is
> corrected in place rather than deleted. See the correction at the end.
`analysis/sizing.py::inter_array_attraction()` computes the force between the two opposed
Halbach faces from a flat-plate Maxwell-stress formula, a uniform pressure
`B_face**2 / (2*mu0)` at a mean face field of 0.55 T over the 340 x 90 mm footprint,
giving **3672 N**. That number was the applied load in the CalculiX A4 structural run
(`validation/results/A4_sled_structural.json`), and it had never been checked against
anything.

`magpylib.getFT()` meshes each magnet block and integrates the field gradient in three
dimensions. Driven by the repo's own array geometry (`build_field()`), so the two methods
cannot disagree about the magnets themselves:

| Mesh per block | Force |
|---|---|
| (2,2,2) | 2909.4 N |
| (4,4,4) | 2773.0 N |
| (6,6,6) | 2720.8 N |
| (8,8,8) | 2701.6 N |
| (10,10,10) | 2693.3 N |
| (12,12,12) | 2689.0 N |
| **(14,14,14)** | **2686.6 N** |

Converged (successive deltas halve (-8.3, -4.3, -2.5 N)) and insensitive to the
finite-difference step across four orders of magnitude (1e-5 to 1e-8, identical to 0.1 N).
**The analytic formula is high by 36.7 %.**

~~**The mechanism is understood, which is why this is a defect and not a disagreement.**
Maxwell stress needs the mean of `B**2`; the analytic form uses the square of the mean `B`;
and `mean(B**2) >= mean(B)**2` for any non-uniform field, by Jensen. A Halbach face field is
strongly non-uniform along the wavelength, so the analytic form must overestimate. It does.~~

> **CORRECTED 2026-07-31 by A12. The inequality is right and the conclusion drawn from it is
> the wrong way round.** If `mean(B^2) >= mean(B)^2`, a one-point form evaluated at the *true*
> mean field **under**estimates. Jensen cannot be why the analytic value is high.
>
> A12 decomposed it against M2's own field statistics on the stress plane:
>
> | | Force | |
> |---|---|---|
> | Analytic, `B_face = 0.550 T` assumed | 3683 N | as published |
> | Same one-point form at the **actual** mean, 0.4127 T | 2073 N | **x1.776 from the assumed field** |
> | Full integral, `mean(B_y^2)` | 2628 N | **x1.267 back the other way, from Jensen** |
>
> Net x1.402 against an observed x1.402. **The cause is the input, not the formula:** 0.55 T is
> not the mean normal field on the plane where the stress acts. The flat-plate form's own Jensen
> error is 27 % and in the *safe* direction; it was fed a field 0.33x too high, which swamps it.
>
> **A right number with a wrong explanation attached is worse than an open question**, because
> it survives review and then misleads whoever picks it up next. That is why this is struck
> through and left visible rather than quietly rewritten.

**What this does and does not damage.** The real force is *lower*, so A4's structural
results are conservative, not wrong: 0.0194 mm airgap closure and 33.7 MPa were computed
against a load 37 % heavier than the field model supports, and all three bands still passed.
No A4 conclusion reverses. What is damaged is the claim that A4's inputs were checked, they
were not, and this is the first time anyone looked.

**Reproduce:** `python3 validation/magpylib/check_inter_array_force.py` (no new dependency;
magpylib 5.2.3 is already in `requirements.txt`).

**Procedural note, stated rather than hidden.** This was computed *before* an acceptance band
was declared for it, which inverts this project's own rule. It is therefore logged as a
discrepancy, not as a validated result. Proper closure needs a run sheet with a band declared
in advance, and a decision about whether `sizing.py` adopts a corrected formula, which would
move `plate_stress_MPa`, ~~the retention-gate sizing,~~ and the A4 load together. **Do not edit
`sizing.py` on the strength of this entry.**

> **Done 2026-07-31.** A12 declared the bands and the adoption rule first, then ran. The
> retention gate is struck above because it does not depend on this: `retention_gate()` is sized
> from a 24 kg ascent stack at 25 g. This entry was wrong about its own blast radius.

### P18. Four physical effects are absent from the model, not merely unvalidated: MEDIUM, NEW 2026-07-29
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — model the four effects, or bound them and say so

Distinct from the E-items, which record analyses not yet run. These are terms that no script
contains, found by reading `sizing.py` and `motor_model.py` rather than the prose. Each is
carried as an E-item below (E19-E22); this entry exists so they are visible from the P-list,
because "the model does not contain this term" is a different class of gap from "this
analysis has not been run".

### Advanced or resolved by the CAD build (not full closures)
- **Launch restraint now exists as geometry.** The breech launch-lock blocks are modelled
  (`cad/parameters.json` `track`: `launch_lock` at x = 30-50 mm, 2 off). This advances
  **E10** (previously "concept-level"), the lock is drawn, though still not analysed.
- **Payload interface now models CDS corner rails** (see P6), giving the rail contact
  faces the interface-control drawing needs.

---

### P19. Every validation run predates the operating point they validate: HIGH, NEW 2026-07-29

> **RE-AUDITED 2026-08-06 and largely false now.** This entry was true when written. Since then
> **A10, A11, A12, A13, A14, A15, A16, A17, A18 and A8-R2 have all run at or after the operating
> point they test**, and A8-R2 in particular exists because this item's rule was followed rather
> than bent: its bands were declared a third time rather than the earlier ones rewritten to fit.
> What survives is **A4 and A5**, which still predate the current point.
> **Status:** `CORRECTED` — the general claim is false; the two survivors are dispositioned below

> **Corrected.** Dispositioned 2026-08-13, and neither survivor is a live defect.
>
> **A4 set the operating point rather than predating it.** A4 is the CalculiX sled-chassis run
> whose CAD result *adopted* the 9.445 kg sled — that is **P15**, and it is why the velocity moved
> to 16.537 and then 16.388. A4 cannot predate a point it caused. Its structural conclusion is a
> function of the sled geometry, which has not moved since.
>
> **A5 is deliberately pinned, and every figure drawn from it says so.** A5 ran at 20.37 m/s and
> `paper/figures/F11_uq.png` plots both series *at that velocity*, labelled, precisely so the GMAT
> comparison is not silently read at today's point. **P35** records the same pin in the generator,
> now with an import-time assertion behind it. **A15 has since run at the current operating
> point** and covers the campaign question A5 was asked; every one of its bands is now evaluated.
>
> **So the rule this entry created is what survives, and it held:** A8-R2 declared its bands a
> third time rather than have earlier ones rewritten to fit, and every analysis since A10 has run
> at or after the point it tests.

Adopting the CAD-derived 9.445 kg sled moved the rated velocity from 20.37 to 16.537 m/s. The
three analyses that have actually been run were all executed at the **old** point, so none of
them currently validates the design as it stands:

| Analysis | Run at | Still valid? |
|---|---|---|
| **A5** GMAT lifetime | dv = 20.37 m/s | **No.** Both baseline and boosted orbits change; the multiplier the scripts now give is x1.62, not x1.80. The *falsification* of the invariance claim (P16) survives, because that is about the shape of the model and not the velocity, but the numbers do not. |
| **A8** ngspice pulse chain | F = 1413.4 N, m = 8.86 kg, 2630 J | **Re-run 2026-07-30 as A8-R** against fresh bands, at 16.537 m/s. Five of six met; the closure row failed and produced P24. This half of the item is closed. |
| **A4** CalculiX chassis | 3672 N Maxwell attraction | **Yes, structurally.** The load is magnetostatic and does not depend on sled mass or velocity. **37 % heavy**, corrected to 2686.6 N by A12 — so A4 is conservative and is deliberately not re-run. |

**What this costs.** The validation table on the front pages says four of nine analyses have
run (A1 added 2026-07-29, and A1 alone is at the current operating point). Strictly, three have run *against a superseded design*. That is not the same claim, and
the difference is exactly the kind a reviewer notices.

**A8 is done.** A5 remains, and is days of wall time for the low-activity leg.
Neither should be re-run until the sled mass is settled, or the same staleness recurs; that
argues for closing the rib-stiffened-chassis question (P5, E2) **first**.

**Do not quietly restate the old results as if they still applied.** Every place the repo
quotes A5 or A8 numbers now needs the velocity they were obtained at stated alongside.

### P20. The A1 run sheet's array-surface reference is mis-specified: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **Corrected as far as it can be, and the band is not re-run.** The double-sided reference is
> **0.9317 T** and the FEM's fundamental at that plane is **0.9312 T — a ratio of 0.9994.** The
> band as declared measured the wrong quantity, and per `validation/README.md` a band is never
> edited after its run, so A1's row stays as written with the correction recorded beside it.
>
> **The lesson is propagated as a rule rather than a note.** `validation/README.md` now requires
> that **every field band name the plane, the quantity, and — where a magnet surface is involved
> — both possible references**. A2 was written under that rule: its band 4 names the
> double-sided fundamental *and* the raw peak explicitly, and when A2 band 4 ran on 2026-08-13
> **both agreed to better than a tenth of a percent**, so the result did not depend on which the
> band had picked. **That is the rule working.**

A1 ran and missed two of its seven declared bands. **One of the two is a defect in the run
sheet, not in the model.**

`validation/A1_field_femm.md` declares the array-surface band against
`analytic_B0_surface_T` = 0.7714 T. That is the fundamental amplitude of a **single** array's
ideal Halbach wave at its own surface. But any measurement at that plane in a **double-sided**
machine inevitably includes the opposing array, whose contribution there is
`B0·exp(-k·GAP)` = 0.160 T. The correct double-sided reference is **0.9317 T**.

The FEM's fundamental at that plane is **0.9312 T, a ratio of 0.9994 against the correct
value.** Measured as a raw peak it reads 1.4641 T, because the plane sits on the magnet face
where block-corner harmonics dominate and the field is formally singular at the corners; a raw
peak there is mesh-dependent and is not the same quantity as a fundamental amplitude either.

**So the row failed as declared, and the model is right.** Both statements are true and both
are recorded. The band is **not** widened, `validation/A1_field_femm.md` is left exactly as
written on 2026-07-27, because a run sheet edited after seeing results is worth nothing. The
correction belongs in the *next* run sheet.

**Fix:** when A2 (3-D) is specified, declare the array-surface band against the double-sided
value and against the **fundamental**, not a raw peak. Two references need naming, not one.

> **Reviewed 2026-08-10, and the sheet was deliberately NOT edited.**
>
> The obvious reading of this item is "the run sheet is wrong, so fix the run sheet". **That is
> the one action this project forbids.** `validation/A1_field_femm.md` declared its band on
> 2026-07-27 and A1 ran against it; editing that band now — even to a value that is provably
> more correct — is editing an acceptance band after its result is known, which is the move
> `validation/README.md` exists to prevent and which this entry already ruled out in its own
> second paragraph. **A band may be corrected before a run, dated, with the original stated. It
> may never be touched after one.** P30 is the precedent for the permitted case; this is not it.
>
> **So the fix is forward-only, and it now lives somewhere a future run sheet will actually
> meet it.** The requirement has been added to the conventions in
> [`validation/README.md`](validation/README.md), because a correction recorded only in the
> defect register is a correction the next sheet's author has to already know to look for. That
> is the same failure mode as A1's result living only in `OPEN_PROBLEMS.md` while
> `validation/README.md` said "not run".
>
> **P20 stays open, and it stays open for a reason that is not work anyone is avoiding.** It
> closes when **A2** is specified and declares the array-surface band correctly. A2 does not
> exist — it needs a 3-D solver, it is A-8 in `docs/PHASE_I_CLOSURE.md`, and it is the heaviest
> remaining analysis. Marking this closed while the only thing that can close it has not been
> written would be closing by assertion.

### P21. Stray field at 50 mm: 2-D cannot test the far field: LOW, NEW 2026-07-29
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


> **QUANTIFIED 2026-08-05 by `analysis/far_field_sensitivity.py`.** P3's diagnosis was right and
> the size of it was not known. Sweeping `build_field(n_wave)` from 3 to 15 wavelengths against a
> converged reference:
>
> | Station | Deviation at the default n=7 (336 mm) | Converged |
> |---|---:|---:|
> | 10 mm | **0.64 %** | 22.688 mT |
> | 20 mm | 4.36 % | 4.290 mT |
> | 50 mm | **374 %** | 0.104 mT |
>
> **The 10 mm value is converged and the 50 mm value is not remotely.** At n=7 it is 0.49 mT
> against a converged 0.104, and it is still 16 % out at n=13. The paper's 1.0 mT corresponds to
> an array shorter than the CAD's 340 mm. **No 50 mm stray figure in this project should be
> cited**, including the 0.4 mT in `field_verification.json`, until the array length is set to
> the CAD value and the model converged.
>
> This needs no mesh: magpylib's Cuboid is an exact analytic solution for a uniformly magnetised
> block, so the field is already three-dimensional. What was missing was the convergence check.
The second A1 band miss. FEM gives 0.93 mT against a 0.4 mT reference, ratio **2.32** against
a factor-2 band.

**Cause identified, and it is geometric.** The FEM is 2-D: the array is infinitely long out of
plane. The real array is **90 mm deep**. At 10 and 20 mm behind the back face the observation
distance is small against that depth and the two agree (ratios 1.16 and 1.14, both inside
band). At 50 mm the distance is comparable to the depth, a finite source falls off faster than
an infinite one, and the 2-D model necessarily overestimates.

This is **converged, not noise**: the value sits at 0.93 mT across box sizes 0.5-0.8 m and
across mesh refinements from 32 k to 141 k elements.

**Consequence:** a 2-D method cannot validate this row, by construction. `A1_field_femm.md`
already says A1 "does not close 3-D end effects", this is that limitation showing up in the
one row most sensitive to it. The magpylib reference, which models finite 90 mm blocks
exactly, is the more trustworthy number here and the FEM is not evidence against it.

**Do not** change `verify_field.py`. The row needs A2, a 3-D solve.

### P22. The novelty claim was wrong, and its replacement rests on abstracts: HIGH, NEW 2026-07-30
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

A literature check found **published work on this exact concept that the paper did not cite.**
Full record in [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md).

**What was wrong.** §I asserted *"no published deployment system operates in the tens of m/s."*
Feng, Yang & Wu (*Int. J. Aerospace Eng.* 2025, art. 3000765) analyse an on-orbit multi-stage
induction coilgun regulating a 20 kg CubeSat to **321.56 m/s**, with a reachable-domain analysis
serving the same purpose as this paper's lifetime and phasing argument. It was published
**2025-11-12, eight months before this repository went public.** The sentence was false as written.

**What it was changed to.** The regime is unserved *by flown hardware*, which is what the
comparator table always actually showed. The contribution is re-scoped to the narrower and more
defensible claim: a **programmable velocity delivered to an unmodified satellite inside its own
qualification envelope.** Both qualifiers carry weight, and against Feng they carry more than they
did against a spring:

| | Why it holds |
|---|---|
| Unmodified satellite | An induction coilgun accelerates a *conductive armature*, attached to the customer satellite, or a sabot needing its own separation. ADR-006 forbids the first |
| Inside the g-limit | 321.56 m/s at 10.7 g requires a **493 m track**; over 1.5 m it is **3515 g**. Not a secondary payload |

The g-limit argument is not new (ADR-003 made it in mid-2025) but it was an assertion and is now
arithmetic against a published number.

**The declared band, and what happened to it.** Before the full texts were obtained, this was
written down: *if Feng et al. report closed-loop per-satellite velocity regulation at dispersion
comparable to this design's 0.027 m/s 3σ, "programmable" stops being a differentiator; if they
report a track length making 321 m/s survivable for a standard CubeSat, §I needs rewriting rather
than adjusting.*

**All five papers were then supplied and read on 2026-07-30. Neither trigger fired, and three of
this entry's own conclusions turned out to be wrong.** Corrections in
[`docs/PRIOR_ART.md`](docs/PRIOR_ART.md); the material ones:

| Claimed from the abstract | After reading |
|---|---|
| "321.56 m/s at 10.7 g would need a 493 m track", a hypothetical | Their **actual** barrel is 3.9 m to **1352 g** mean, ~3060 g peak from their own >600 kN. The fact is far more decisive than the hypothesis |
| ADR-003's unsourced "1-2 % coilgun efficiency", removed *pending Einat* | **False.** Feng reports **14.9-19.9 %**, comparable to this design's own 20 %. Einat cannot settle it, a **2.5 g** projectile. Argument withdrawn as wrong, not deferred |
| *Aerospace* 12(6) 466 "has experimental verification" | True but narrower: a **32.8 mm/s transport mechanism**, not an ejection |

**Feng quotes no dispersion figure at all**, and controls velocity by charging-voltage selection
(10 to 16 kV to 230 to 321.56 m/s). So the dispersion differentiator survives, but as a claim about
*absent evidence*, not about impossibility, and it is written that way now. Feng is also
**simulation-only**, so on maturity this project and theirs are peers rather than this one being
behind.

**Why it stays open.** The claim corrections have landed, but two things are unfinished:

1. **The reachable-domain method should probably be adopted.** Feng's 3-D reachable-set envelope
   answers "which orbits does one shot make available" directly, where this project reports a scalar
   lifetime multiplier. That is a better astrodynamic product and it is the strongest thing to take
   from this literature. Not yet done, Phase II candidate.
2. **E24**, below: Xu et al. model attitude disturbance from the transfer mechanism itself. This
   project has nothing on disturbance from magazine indexing between shots.

**The maturity gap is real and remains.** The Harbin group built and measured a prototype. This
project has measured nothing. `docs/BENCHTOP_TESTS.md` already specified the answer as **B-1** and
**B-2**; what was added on 2026-07-30 is that their bands are now **derived** from an error budget
rather than chosen, by `validation/bench/bench_predict.py`. See E4.

### P23. The stroke time is stale in six places, and A8's band was set at the old one: MEDIUM, NEW 2026-07-30 — CLOSED 2026-08-10
> **Status:** `CLOSED` — resolved; see the entry for what closed it

Found while building the shot animation, which draws its time axis from `motor_model.shot()`
and came out at **157.3 ms** against the **127.7 ms** printed everywhere else.

127.7 ms is the superseded figure. Under constant acceleration the stroke time is `2s/v`:

| Operating point | 2s/v over the 1.30 m accel zone |
|---|---|
| 20.370 m/s, the pre-P15 point | 127.6 ms |
| 16.537 m/s, current | 157.2 ms |

So it belongs to the 4.86 kg parametric sled and survived the P8/P15 propagation in six
places: `README.md` twice, this file's E23 entry, `validation/A8_pulse_spice.md` twice, the
`CHANGELOG` record of A8's bands, and `docs/VALIDATION_REPORT.md`.

**The part that matters is not the typo.** `validation/A8_pulse_spice.md` declared a band of
**127.7 ms +/-10 %**, so 114.9 to 140.5 ms, and `VALIDATION_REPORT.md` records A8 passing it at
127.66 ms. At the current operating point the value is 157.3 ms, which is **23 % above the band
centre and outside the band entirely**. A8's recorded pass is a pass against a superseded
target.

This is the concrete instance of what P19 says in general. It is not a new failure: A8 ran
correctly against the operating point that existed when it ran. But "A8 passed" cannot be
quoted without saying which operating point it passed at, and until it is re-run the row in
`VALIDATION_REPORT.md` overstates what is known.

**Done:** the four prose occurrences corrected to 157.3 ms.

**Closed 2026-07-30 by A8-R.** The original band and its recorded result are left exactly as they
were, marked as belonging to the superseded point, because rewriting a declared band after the
fact to fit a new number is the one move that would make the whole validation record worthless.
Fresh bands were written and committed before the deck was touched, and the re-run passes the
pulse-duration row at 157.26 ms against 157.3. It failed a different row, which is P24.

**Swept and confirmed 2026-08-10, which is what this entry was still open for.** The entry
recorded the substance as closed but had never been checked against the file tree, so it stayed
`LIVE` on a bookkeeping technicality. Every surviving occurrence of 127.7 / 127.6 ms was read:

| Where | What it is | Correct as it stands? |
|---|---|---|
| this entry, ×4 | the record of the defect itself | **yes** — it is the account of the stale value |
| `validation/A8_pulse_spice.md` line 16, 29 | **the band as declared on the day**, 127.7 ms ±10 % | **yes, and must not be touched.** Editing a declared band after its run is the one move the project forbids |
| `validation/A8_pulse_spice.md` line 109 | A8-R's own note that the windows moved 127.7 → 157.3 ms | **yes** |
| `docs/VALIDATION_REPORT.md` line 123 | A8's pass, annotated "**at the superseded operating point**, see P23. The current value is 157.3 ms, outside this band" | **yes** |

**No stale prose survives.** The six places the entry named were four prose occurrences, since
corrected, and two declared-band occurrences that are correct precisely because they were not.
**The distinction between a stale number and a historical one is the whole of this item**, and
every remaining instance is on the right side of it.

### P24. No script carries a bank ESR, and the placeholder standing in for it is a factor of two high: HIGH, NEW 2026-07-30
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

Found by A8-R, the re-run of the pulse-power simulation at the current operating point
(`validation/A8_pulse_spice.md`). Five of six bands passed. Energy closure failed at **97.0 %**
against a declared 98-102 %.

The simulated draw exceeds the analytic accounting by **86.6 J**. That gap is bank ESR
dissipation, which the circuit deck models and the analytic ledger has no term for:

| | |
|---|---|
| I^2 dt over the shot, integrated by ngspice | 7126.2 A^2 s |
| Bank ESR, per `sizing.py` | 0.012 ohm |
| Product | **85.5 J**, against an 86.6 J gap, agreeing to 98.7 % |

**The ledger is internally consistent and still understates the bank.** `energy_closure()` has no
ESR term, and the `E_DRAWN = 2795.6 J` it closes against comes from `motor_model.py`, which has no
ESR either. Both sides of the equation omit the same term, so the closure reads 100.0 % while the
real draw is about **2881 J**, 3 % higher.

**What moves if the term is carried:**

1. **`thermal_campaign()` carries `Q_esr = 160 J`** as a literal default. Against 85.5 J that is
   1.9x high, and the twelve-shot campaign falls from 28.9 to 28.0 kJ. It was flagged as unsourced
   during the P2 review and has had no second number against it until now.
2. **The per-shot energy headline, 2.80 kJ**, is the analytic draw and appears on the front pages.
   It becomes 2.88 kJ, and electrical-to-payload efficiency falls from 19.6 to about 19.0 %.
3. **Quoted bank sag, 5.19 %**, is the charge depletion with no ESR in the loop. The true figure is
   the 5.35 % A8-R measured.

### Retracted, same day it was written: the claim that the bank goes undersized

This entry first stated that `capacitor_sizing()` at the true draw wants **6.18 F** against the
6.0 F selected, and that the bank was therefore chosen against a draw omitting a loss it causes.
**That is wrong, and the error is in how it was computed.** The 6.18 F came from raising the
energy to 2881 J while holding `SAG_FRAC` at 5.19 %. The two are not independent: the ESR
dissipation is drawn out of the same capacitor, so a higher draw *is* the higher sag. Evaluated
consistently, at 2881 J and 5.35 %,

```
C = 2E / (V0^2 - V1^2) = 2(2881) / (96^2 - 90.864^2) = 6.00 F
```

against 6.0 F selected. **The bank is correctly sized and always was.** The sizing function is not
implicated, and the propagation below is a constant change rather than a design decision.

The mechanism is worth naming because it is a general trap in this repository: `capacitor_sizing()`
takes `E` and `sag_frac` as separate arguments, and its own docstring warns that `sag_frac` is the
droop the shot integration reaches rather than a target. Feeding it a new energy with a stale sag
violates that, and the function has no way to notice.

### Propagated 2026-07-30, in the same pass that wrote this entry

`motor_model.py` gained `R_ESR = 0.012` and now solves `R I^2 - Vc I + P = 0` for the current the
load draws at the bank **terminal** rather than at the capacitor, integrating `Vc*I` out of the
bank and `I^2 R` into a new `Q_esr` output. `sizing.py` follows: `E_DRAWN` 2795.6 to 2881.2 J,
`SAG_FRAC` 5.19 to 5.35 %, `energy_closure()` carries the term on both sides, and
`thermal_campaign()`'s literal 160 J becomes the computed 85.6 J.

Eleven result fields moved, all electrical or thermal. **Exit velocity, acceleration, stroke time,
dispersion, the payload family, mass and cost are unchanged**, which is the expected signature of
an electrical-only correction and was checked rather than assumed.

The correction also closed a disagreement nobody had attributed. A8 and A8-R both recorded peak
current about 5 % above the analytic model and put it down to the integrator. It was the ESR:
corrected, the model gives 346.77 A against ngspice's 346.8.

**This is a simulation result, not a measurement.** It gives a placeholder its first independent
number, which is what E17 asked for, and it is still one model checking another.

> **Superseded in part, 2026-07-30 by A10.** Everything above is arithmetically correct and
> still describes what the model does. What it assumed is not: **12 mohm is not purchasable at
> this bank capacitance**, and at a realistic value the shot does not close at all. The 86 J
> figure is therefore the ESR loss of a bank nobody can build. See **P26**.

### P25. A retracted claim stayed live in the paper, the wiki and two docs for a day: MEDIUM, NEW 2026-07-30
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

P22 withdrew ADR-003's assertion that coilgun efficiency is "1-2 % in the literature", after
Feng et al. were found reporting **14.9-19.9 %** for a multi-stage on-orbit CubeSat launcher.
The withdrawal was recorded in `docs/adr/003`, `docs/PRIOR_ART.md`, `docs/RELATED_WORK.md` and
the changelog.

**It was not propagated to the places that actually assert it.** Four survived:

| Where | What it said |
|---|---|
| `paper/paper.tex` Table I | *Electrical to payload efficiency: coilgun 1-2 %, this work 19 %* |
| `paper/paper.tex` §II and §III | the same figure, once as background and once as a listed cost of the coilgun |
| `wiki/Home.md` | "1-2 % single-stage efficiency" in the locked-decisions list |
| `docs/PROJECT_NOTES.md` | the same, in the locked-decisions list |

**Table I is the one that matters.** It is the architecture trade, and that row claimed an
order-of-magnitude efficiency advantage that the prior art says does not exist. Corrected, the
row reads 14.9-19.9 % against 19 %, which discriminates not at all. The decision survives on the
rows that always carried it: no armature on the customer satellite, closed-loop velocity control,
and an abort path to 45 % of stroke.

**Found by reading the wiki page after publishing it**, not by any check. That is the finding.
The retraction was logged in four places and propagated to none, and nothing in the repository
notices when a ledger entry and an artifact disagree, because the mechanical guards
(`make_baseline.py --check`, `_check_operating_point()`, `check_links.py`) all compare artifacts
to *scripts*. A claim withdrawn in prose has no such guard.

**Half the general case is now fixed**, 2026-07-30. The same blindness had already shipped a
stale PDF: `paper.tex` was corrected twice and the published PDF went on printing the retracted
figure for five hours until it was found by hand.
[`tools/check_artifacts.py`](tools/check_artifacts.py) closes that half by comparing each built
artifact to the sources it was built from, using the commit each was last changed in rather than
file mtimes, which git does not preserve and which a fresh clone destroys. Verified against the
actual failure: at commit `c406da4` it reports the PDF **5.1 hours behind** its own source.

**The other half stays open and is the harder one.** A claim withdrawn in prose still has no
guard. Catching that needs a list of load-bearing claims and where each is asserted, which is
`docs/PROVENANCE.md`'s job and would roughly double it. What is now true is that the *mechanical*
half of this defect cannot recur silently.

### P26. The supercapacitor bank cannot source the shot: HIGH, NEW 2026-07-30
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

P24 recorded that the 12 mohm bank ESR had no source. Looking for one found that the value is
not merely unsourced, it is **not attainable from the cells the design specifies**, and that the
shot does not close without it. Full run: [`validation/A10_bank_esr.md`](validation/A10_bank_esr.md).

**The physics.** For an EDLC, ESR times capacitance is roughly constant within a cell
technology: both are set by the same electrode area and separator. Two Eaton 3.0 V cells thirty
times apart bracket it, and series stacking preserves the product because R scales with N and C
with 1/N.

| Cell | C | ESR | ESR x C |
|---|---|---|---|
| TV1860-3R0107-R | 100 F | 11 mohm | 1.10 s |
| XL60-3R0308T-R | 3000 F | 0.23 mohm | 0.69 s |
| **This bank, as modelled** | **5.94 F** | **12 mohm** | **0.071 s** |

The bank as modelled is an order of magnitude better than either commercial cell. At a realistic
product it is **116 to 185 mohm**.

**The consequence is not a worse efficiency. It is no shot at all.** A source of EMF V behind
series resistance R cannot deliver more than `V^2/4R` into any load. At the rated point the
shot needs 30.0 kW at peak velocity. A10 swept the integrator and found the design completes up
to **65 mohm and fails from 70**, against the 116 to 185 mohm the cells actually give.

| | |
|---|---|
| Hard ceiling on bank ESR | **65 mohm** |
| A single string of 32 x 190 F cells | **116 to 185 mohm** |
| Margin | **none: short by 1.8x to 2.8x** |

**Nothing else in the design is implicated.** Exit velocity, stroke time and dispersion do not
move anywhere in the sweep, because the commanded force is constant and the mechanical
integration never sees the bank until the bank fails to source it. K_t, the magnets, the
winding and the control loop are untouched. This is a pulse-power defect and it is contained
there.

**Not propagated, and that is deliberate.** The baseline still reads 16.537 m/s at 2.88 kJ,
which assumes a 12 mohm bank that cannot be bought. `docs/BASELINE.md`'s change-control rule
admits error correction; what is needed here is a **sizing decision**, and taking one on the
strength of two datasheet points would be exactly the reasoning this repository logs defects
about. Options costed as **PII-7**.

**The gap that let this through, and it is on the record already.**
[`docs/LITERATURE.md`](docs/LITERATURE.md) has 136 entries across nine clusters, and its
pulsed-power-and-capacitors cluster has **two**. The file names that cluster as the sample's
blind spot in its own words. The one area nobody filled is the one that turned out to carry a
defect big enough to stop the machine.

**What is still soft.** Both cell figures come from distributor listings of manufacturer data,
not from the manufacturer PDFs, which are unreachable from the environment this was written in.
A third mid-range point was not obtained. If space-qualified cells behave differently the
numbers move, though the ceiling at 65 mohm does not: that is set by this design's own power
demand and is independent of any datasheet.

### P27. A numerical guard hid the failure it was written next to: MEDIUM, NEW 2026-07-30
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

Found by A10 on its first run, before it found anything about the bank.

`shot()` solves `R I^2 - Vc I + P = 0` for the current drawn at the bank terminal. When the
discriminant went negative it fell back to `I = P/Vc`, the current the load would draw with no
ESR at all. That branch was added on 2026-07-30 in the same commit as the ESR term itself,
as an ordinary numerical guard.

**A negative discriminant is not a numerical edge case. It is the bank being unable to source
the demanded power**, which is precisely the condition A10 exists to detect. The fallback
converted it into a completed run with a working machine in it, at every resistance tested.

The tell was visible in the output and nearly missed: **peak current fell from 630 A at 70 mohm
to 331 A at 183 mohm.** Demanded power was fixed, so current cannot fall as resistance rises.

**Fixed:** the branch raises `BankLimitError`, naming the power demanded, the `V^2/4R` ceiling,
and the point in the stroke where it was hit. The baseline is unaffected, because at 12 mohm the
discriminant never goes negative.

**The general lesson, which is why this is a numbered defect and not a commit message.** Every
other guard in this repository fails loudly: `_check_operating_point()` exits, `make_baseline.py
--check` exits, `bench_predict.py` raises on geometry drift. This one substituted a plausible
value and continued. A guard that degrades silently is worse than no guard, because it converts
a detectable failure into a credible wrong answer.

**Corrected.** Marked 2026-08-10 after verifying the fix in the source rather than taking the
entry's word for it: `analysis/motor_model.py` defines `BankLimitError` and `shot()` raises it on
`disc <= 0`, naming the demanded power, the `V²/4R` ceiling and the stroke position. The silent
`I = P/Vc` fallback is gone. Retained as the published record — the defect is worth keeping
because the lesson about silently degrading guards is, not because anything remains to be done.

### P28. The regen stator and the eddy fin do not both fit the arrest section: CORRECTED 2026-08-13
> **Status:** `CLOSED` — resolved; see the entry for what closed it
> **Corrected.** `S_REGEN` 240 → 39 mm, so 39 + 300 fits the 339 mm section. Recovery falls
> 291 → 47 J and efficiency to 18.8 % net. **Dropping regen entirely was recommended first and
> withdrawn**: it costs 2 points of efficiency, which is in no kill criterion, to raise brake duty
> 24 %, which makes **E34** — fourth on the lethality ranking — worse. **ADR-030.**
Opened by A11 in the act of adopting regenerative braking, and recorded rather than designed
around.

The closed envelope is 1839 mm and release is at 1500 mm, so the arrest section is **339 mm**.
A11 assumes 240 mm of it carries regenerative stator. The eddy fin as sized in `sizing.py` is
**300 mm** long (0.86 kg of 4 mm copper). **240 + 300 > 339.** Both live in the same airgap, so
they cannot overlap.

**The thermal half is not the problem.** Regeneration cuts the fin's duty from 1291 to 952 J, a
26 % reduction, and the fin's adiabatic rise falls from 4.0 to 3.0 K. A fin a third of the
length would still hold its transient.

**The mechanical half is unresolved, and it is tighter than it looks.** Eddy force is
proportional to velocity, so distance to arrest is linear in the velocity removed:
`x = (m/c)*(v0 - v1)`. At the first-order coefficient `paper/make_figures.py` uses,
`c = 670 N*s/m`, the sled needs **186 mm** to fall from 14.2 to 1.0 m/s, and only about 99 mm
would remain. Closing that means **c rising to roughly 1210 N*s/m, a factor of 1.8**, which puts
peak deceleration at **186 g against the 200 g taper cap** — inside it, with 7 % to spare, on a
cap that exists to protect the bonded magnet interfaces. That is not a comfortable margin, and
it is the reason this is a numbered defect and not a note.

**Regeneration is what makes the repartition even arguable.** Without it the sled enters the
brake at 16.5 m/s and the same 99 mm would need `c = 1440`, putting peak deceleration past the
cap outright. The 240 mm of regenerative stator pays part of its own packaging cost.

**Why this is logged instead of fixed.** The obvious fix is to shorten `fin_mass` in
`thermal_campaign()` until the numbers fit. `validation/README.md`'s conventions forbid exactly
that: *"do not hand-edit a script to match an FEA result, record the discrepancy first, decide
second."* The same applies to hand-editing one to match a packaging wish. `sizing.py` keeps the
300 mm fin and carries a comment saying it does not fit.

**What would close it.** A repartitioned arrest-section layout with the fin resized on eddy
authority rather than on heat, checked against the 200 g deceleration cap and the ring-spring
handover below 1.5 m/s. It is mechanical design, and it is the reason A11 says plainly that it
answers the electromagnetic question only.

### P29. The paper says the winding is segmented; the model charges copper for all 1.3 m: MEDIUM, NEW 2026-07-31 — CLOSED 2026-08-10
> **Status:** `CLOSED` — resolved; see the entry for what closed it

Found while pricing a longer track, and it is a question about the machine as built rather than
about any proposal.

`paper/paper.tex` §VII states, under redundancy: *"the winding is segmented so a shorted coil
degrades thrust rather than ending the campaign."* `motor_model.shot()` computes copper loss as
`RHO_CU * J^2 * vol_cu` with `vol_cu = ACCEL_ZONE * DEPTH * WIND_THICK * FILL`, that is, **the
whole 1.30 m winding carrying full current density for the entire 157 ms stroke**.

Those are not consistent with each other. A segmented long-stator machine energises the section
under the mover — roughly the sled's 340 mm active length — and switches segments as it passes.

**What it is worth.** Energising 340 mm rather than 1300 mm takes copper loss from **827.9 J to
about 217 J**, and electrical-to-payload efficiency from 21.2 % to roughly **24.4 %**, with no
design change whatsoever. It also drops peak current from 347 to about 296 A, which raises the
A10 bank ESR ceiling from 66 to about 79 mohm — relevant to P26, though not enough to reach a
single commercial string at 116.

**Three possibilities and this repository cannot currently distinguish them.**

1. The winding is segmented for *fault tolerance* but driven as one, in which case the model is
   right and the paper's sentence is about failure modes only. Then nothing is wrong and the
   distinction needs stating, because a reader will assume block commutation.
2. The winding is block-commutated and the model is deliberately conservative. Then the
   conservatism is real engineering judgement and **it is written down nowhere**, which is the
   same defect class as the 12 mohm ESR (E17): a value with no provenance.
3. It is simply inconsistent, and `Q_copper` is overstated by a factor of about 3.8.

**Why this is logged rather than fixed.** Changing `vol_cu` moves a baseline number, and which
way it should move depends on a design decision nobody has recorded. Guessing in either direction
would put an unsourced value into the baseline, which is exactly what P24 and E17 exist to stop.
`cad/parameters.json` `groups.stator` records conductor counts and belt geometry but says nothing
about drive segmentation, so the CAD cannot settle it either.

**What would close it.** A recorded decision on how many stator segments exist and how many are
energised at once, then `motor_model.py` computing `vol_cu` from that rather than from
`ACCEL_ZONE`, with the paper's redundancy sentence and the drive description made to agree.
Both numbers then follow from one stated fact instead of two unstated ones.

> **CLOSED 2026-08-10 by [ADR-022](docs/adr/022-stator-segmented-not-block-commutated.md):
> possibility 1.** The winding is segmented **for fault isolation** and driven as a single
> energised section. `vol_cu = ACCEL_ZONE` stands and **no baseline value moves.**
>
> **Both branches were priced before choosing**, by `analysis/owner_decisions.py` re-running the
> real pipeline with the energised length as a parameter:
>
> | | Whole winding | ~One sled length | 4 segments |
> |---|---:|---:|---:|
> | Copper per shot | **834.7 J** | 218.3 J | 208.7 J |
> | Net efficiency | **20.99 %** | 28.07 % | 28.22 % |
> | P33 inductance | **19.70 µH** | 5.15 µH | 4.92 µH |
> | **Exit velocity** | **16.388** | **16.388** | **16.388 m/s** |
>
> **The last row decides it. Segmentation changes what the shot costs, not what it delivers** —
> force is commanded, so copper loss is a power draw and not a thrust reduction.
>
> **Why the conservative branch.** Efficiency appears in **no** kill criterion; mass appears in
> the one that is crossed by a factor of three. Block commutation buys 7.09 points and costs an
> inverter per segment or a switching assembly, **none of it in the mass rollup** (**P10**).
> Buying efficiency with mass is the wrong direction for the threat that is live.
>
> **This entry's estimate of "24.4 %" is superseded** — it predates the quadrature correction; the
> computed figure is 28.07 %.
>
> **The price is recorded rather than glossed: 7.09 points of efficiency and 616 J of copper per
> shot, paid for drive simplicity, with 74 % of the copper dissipating under no field.** That was
> possibility 2 — conservatism that was real judgement *"written down nowhere"* — and writing it
> down with both branches costed is the whole of what this entry asked for. `shot()` keeps its
> `energised` parameter, so **the default is now a recorded decision rather than an unexamined
> one**, and the alternative stays priceable without editing the model. Block commutation goes to
> Phase II with a stated entry criterion: it becomes attractive if the mass rollup ever closes
> with room to spare.

### P30. An acceptance band was set at the easier of two available comparators: MEDIUM, NEW 2026-07-31
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `DECISION` — the band stands as declared; what changes is what is claimed from it

**A defect in how a band was chosen, not in a number.** This repository has no other entry of that
kind, which is the reason to write it down.

`validation/A7_separation_chrono.md` declared its tip-off band as **≤ 5 °/s/axis**, citing the
NanoRacks NRCSD-E interface document. Three other files — E7 above, `docs/KILL_CRITERIA.md` §4 and
PII-1's entry criterion in `docs/VAULT.md` — carried a standing flag that this "conflicts" with
a sibling NRCSD ICD quoting 2 °/s, and that the conflict had to be resolved before the band meant
anything. PII-1, the best available velocity lever, was gated on it.

**There is no conflict. They are two different deployers and both numbers are right:**

| | Tip-off target | |
|---|---|---|
| **NRCSD**, internal, ISS airlock | **< 2 °/s/axis** | flown hundreds of times |
| **NRCSD-E**, external, Cygnus-mounted | < 5 °/s/axis | *"additional testing and analysis are being completed... to refine and verify this value"* — its own publisher |

**What that leaves is worse than the flag it replaces.** The band was set at the looser of the two
comparators, taken from the document whose publisher describes the figure as provisional, with
nothing recorded about the tighter flown number existing. Nobody chose the easy number on purpose;
it is what happens when a band cites one source and no one asks what else the source set contains.
**That is the failure mode acceptance bands exist to prevent, occurring inside the band-setting
step itself.**

**Fixed 2026-07-31.** A7's band is now **2 °/s/axis** with NRCSD-E retained as a secondary
reference and labelled provisional. **A7 has never run**, so this is a band tightened before
results rather than after — the distinction the whole validation record depends on, and the sheet
states it above the table. The cost is real: A7 is now **2.5x harder to pass**, on a release path
with no multibody model behind it and a payload centre of mass 70 mm off the thrust line.

**The general rule this implies**, added to `validation/README.md`: *when a band cites an external
document, record which document, which revision, and whether a tighter comparator exists in the
same family.* One line, and it would have caught this.

### P31. The repository carries two different inter-shot cadences and reconciles neither: **RESOLVED 2026-08-05 by ADR-020**
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **The ConOps interval is 1200 s.** Adopted in [`docs/adr/020-inter-shot-cadence.md`](docs/adr/020-inter-shot-cadence.md) because it is the number `astro.py`'s conjunction model,
> the realignment period and the deployment safety case were already computed against, so
> adopting it invalidates nothing, while 10-20 s would require re-running A6 against a
> geometry never evaluated. **A13's failed bands are NOT re-declared against it** -- this
> entry's own instruction, that doing so is a band change belonging declared and dated, is
> followed. Rows 3 and 4 remain FAIL; what changed is their operational significance.
Found while costing A13's failure, and it decides whether that failure matters.

| Where | Interval | For what |
|---|---|---|
| `paper/paper.tex` §III-C | **10–20 s** | described as "set by supercapacitor recharge, at a 150–300 W allocation" |
| `analysis/astro.py` `conjunction(spacing_s=1200.0)` | **1200 s** | the spacing the 30-day conjunction analysis actually models |

**Twenty seconds and twenty minutes, in the same repository, for the same event.** They are not
necessarily contradictory — a machine able to fire every 18 s may still be *operated* every
20 minutes — but **nothing anywhere states which is the ConOps**, and two published analyses
depend on different ones. The conjunction geometry, the realignment period and the whole safety
case are computed at 1200 s. The thermal case is argued at 10–20 s.

**The recharge claim is also wrong, which A13 established separately.** The mechanical chain
between shots — index, sled return, attitude settling — has a floor of **18.1 s** at a 6.9 s
return, against a recharge of 8.6 s at 300 W and 17.2 s at 150 W. **Attitude settling binds at
both allocations.** The paper's sentence has been corrected; this entry is about the second
number, which the correction does not touch.

**Why it matters for A13.** At 1200 s the 8.2 s settling is 0.7 % of the interval and A13's band 5
tested against the wrong quantity. At the 18.1 s floor it is 45 % of it. **The same failure is
either irrelevant or dominant depending on a number nobody has written down.**

**What would close it:** state the ConOps cadence once, in one place, with the reason — and make
`astro.py`'s `spacing_s` default read from it rather than carry an independent literal. If the
answer is 1200 s, A13's bands 3–5 should be re-declared against it and re-run; **that is a band
change and belongs declared and dated, not quietly applied to an existing failure.**

### P32. The working Gen4 geometry has no corresponding operating point: CORRECTED 2026-08-13
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `DECISION` — D8
> **Corrected by retirement.** Gen4 exists only inside Fusion, has never been exported, and
> releases at s = 1200 mm over a 900 mm stroke where `analysis/` assumes 1500 mm over 1.3 m.
> Gen5 is generated from `cad/parameters.json` and `build_gen5.py --check` reads **23 dimensions**
> back out of it. **A geometry that cannot be exported, cannot be checked, and does not match the
> parameters is not a generation this project has.** The renders remain as the only visual record
> and are labelled historical where they appear. **ADR-030.**

The published Phase I result assumes a uniform 1.30 m active stator and release at 1500 mm.
`EMOCD_Gen4_Open v7` instead places the same 488 mm sled at s = 300 mm stowed and s = 1200 mm
release, a 900 mm acceleration stroke. Its 340 mm Halbach array is fully over the stator only
through s = 1051.5 mm. The final 148.5 mm is a finite-edge region, and 191.5 mm of the array
remains over the stator at release.

The current 16.388 m/s, 10.53 g, 2851 J gross and 20.99% net values are still reproducible for
the frozen Phase I geometry. They are not Gen4 results. No public document may attach them to
the open assembly, and a constant-thrust calculation shortened to 900 mm would not repair the
mismatch because it would ignore the changing overlap.

The provisional stationing does resolve one geometry conflict: release is at s = 1200 mm and
the fin enters the brake at s = 1222 mm, leaving 22 mm between the two events. The fin then has
330 mm of travel through the brake before its trailing edge clears at s = 1552 mm. Those are
kinematic envelope results, not an arrest or thermal validation.

**What would close it:** E27's position-dependent force calculation, followed by one controlled
propagation through power, energy, thermal, braking, orbit, paper and validation records. Until
then the Gen4 export gate stays closed and the Phase I baseline remains the only rated point.

### P33. The paper credits a winding inductance nobody had computed: MEDIUM, NEW 2026-08-05
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — compute the winding inductance


`paper/paper.tex` says the drive switches at 20-40 kHz, "high enough that the current ripple is
filtered by the winding inductance and low enough to keep switching loss within the converter's
97 J/shot budget." **There was no inductance anywhere in this repository.** No henry in
`analysis/`, and no phase current either: `motor_model.shot()` integrates in *sheet* current
(A/m), and the `I_peak` it reports is the **DC-link current drawn from the bank**, not the
current in a conductor. Every "peak current" figure in this project, including the lever table in
`docs/DESIGN_OPTIONS_exit_velocity.md` and A10's ESR ceiling, is that DC-link number.

The gap is structural rather than clerical. A sheet-current model is turns-invariant: the same
126 kA/m can be wound as many turns at low current or few at high current, L scales as N², phase
current as 1/N, and the stored field energy is the same either way. **So the model cannot
produce an inductance, and the claim above could not have been checked when it was written.**

`analysis/drive_electrical.py` closes it on the one constraint that does fix the turns count:
the inverter has to synthesise the phase voltage the machine demands at rated speed, out of a
96 V bus sagged to 90.9 V. The required volt-amps are invariant under the turns count, so the
design point follows without a new winding assumption.

| | |
|---|---|
| Armature-reaction field energy | **2.058 J** (harmonic sum over the belt distribution) |
| Peak phase current | **373.2 A**, against the 338.8 A DC-link figure quoted everywhere |
| Phase inductance | **19.70 µH** |
| Phase resistance | **25.18 mΩ** |
| Electrical time constant | **0.782 ms**, fast against the 158.6 ms stroke |
| Modulation index at exit | **1.00**, by construction |
| Ripple at 20 kHz | **60.9 A pp, 16.3 % of peak** |
| Ripple at 40 kHz | **30.5 A pp, 8.2 % of peak** |

**Half the paper's sentence survives and half does not.** The loss half is fine: the ripple adds
**3.71 J to an 834.7 J** copper budget at 20 kHz, four tenths of one percent, so nothing in the
thermal or energy record moves. The filtering half does not: **16 % peak-to-peak ripple at
20 kHz is not a filtered current**, and the sentence asserts it of the whole 20-40 kHz range.
Only the top of that range is defensible.

**Two consequences that are not in any document.** First, the SiC devices carry the phase
current, so they are being selected against **373 A** and the repository only ever wrote down
339 A; the paper specifies the 1200 V rating and never a current rating. Second, exit velocity
and phase current are locked together through the bus: more velocity means more back-EMF, which
means fewer turns, which means more current, which lands on the bank ESR ceiling **P26** already
tracks. That coupling is real but it is **not a new velocity ceiling** — the machine can be
rewound for any speed, it just pays in current — and it should not be written up as one.

**What would close it:** a winding layout with an actual turns count, conductor cross-section
and end-turn geometry, at which point L stops being inferred from an energy balance and becomes
a property of drawn hardware. The 2-D energy method here omits end turns entirely, so 19.70 µH
is a **lower bound** and the ripple figures are upper bounds. `docs/VAULT.md` PII-7 and the
segmentation decision in **P29** both move it: energising less stator cuts L and R together.

### P34. A payload carrying a magnetometer cannot fly in this magazine: HIGH, NEW 2026-08-05
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — a magnetically screened cell, or a declared exclusion


> **EXTENT BOUNDED 2026-08-05.** `analysis/far_field_sensitivity.py` profiles the field outward
> from the thrust line. It falls below magnetometer full scale only at **z = 251 mm** and below
> Earth's own field at **z = 332 mm**. The 3U payload envelope spans z = 20 to 120 mm, so
> **every part of the payload sits above magnetometer full scale** -- 610.8x at the near face and
> still 3.4x at the far face. This is not a near-face problem with a safe interior; it is the
> whole satellite.

**Found by A14, against a band declared before the run.** The payload's nearest face sits **6 mm**
behind the Halbach array back face — `cad/parameters.json` puts the array back face at z = 14 mm
and a 3U payload at z = 20 to 120 mm — and the static field there is **61.1 mT**. That is
**1357× Earth's field** and **611× the full scale of the class of magnetometer a CubeSat carries
to sense Earth's field.**

**This is a payload compatibility constraint and it is not in the interface specification.**
`paper.tex` §on the interface lists four things VOLLEY asks of a host and publishes a magnetic
keep-out radius for the *host*. Nothing anywhere states what the deployer does to the satellite
inside it. A customer flying a magnetometer, a magnetorquer, a fluxgate, or anything with
soft-magnetic structure is affected, and "the satellite is never modified" — the central claim of
this project — is doing quiet work here that it has not earned.

**What A14 did and did not establish.** The 61.1 mT figure is in the exponential near field where
the model reproduces the 10 mm station exactly, so it is sound. The centre-of-mass and far-face
figures, 0.463 and 0.341 mT, sit in the edge-effect tail that **P3** already records this model
getting wrong, so the *extent* of the affected volume is not established. A14's band 5 is VOID
for that reason and for the absence of a materials list.

> **NARROWED 2026-08-10. Step 1 is done, and the block behind it was stale.** Step 1 was written
> as "resolve P3 first", and P3 and P21 are both `CORRECTED` — magpylib's Cuboid is an exact
> analytic solution in free space, so the finite-array field was already three-dimensional and
> correct, and `far_field_sensitivity.py` showed the 7-wavelength default converged to 0.64 % at
> 10 mm. The far field has been trustworthy for some time and this entry went on citing a block
> that had been lifted.
>
> The exposure is now published as [`docs/PAYLOAD_ENVIRONMENT.md`](docs/PAYLOAD_ENVIRONMENT.md),
> a payload environment specification rather than a host keep-out, and attached to **ADR-010**
> and the paper's interface section — the two places that previously specified only what VOLLEY
> asks of a *host*.
>
> **Two things the profile shows that the single 61 mT figure did not.** The near face sits in a
> steep exponential with a gradient of **−17 mT/mm**, so 10 mm of standoff is worth a factor of
> eight and carries essentially all of the magnetic force, which goes as ∇(B²). Everything beyond
> ~60 mm sits in a nearly uniform tail — 0.54 down to 0.34 mT — with a gradient three orders of
> magnitude smaller. **Standoff fixes the near face and does nothing for the tail**, so one
> mitigation does not cover both regimes.
>
> **And the exposure is not "one shot plus dwell".** The Halbach array is a permanent magnet: the
> static field is present continuously from magazine loading onward, through ground handling and
> launch, not only during the 158.6 ms shot. Cradle dwell is specified nowhere in this
> repository, so the bound runs from one 1200 s cadence interval to the whole campaign plus
> ground time. The original wording understated it and is corrected above.
>
> **P34 stays open.** The extent is established; the materials are not.

**What would close it,** in the order that costs least:

1. ~~**State the exposure.**~~ **DONE 2026-08-10**, `docs/PAYLOAD_ENVIRONMENT.md`. The field is
   published across the whole 3U envelope, z = 20 to 120 mm, against both comparators, with the
   two-regime structure and the exposure duration stated. P3 no longer blocks it and had not for
   some time.
2. **Decide whether it is a constraint or a defect.** **This is now the whole of P34.** A
   saturated magnetometer recovers and a magnetorquer becomes uncommandable but recovers;
   **remanent magnetisation of soft-magnetic parts does not**, and only the third is a
   modification. That distinction needs a **payload materials list**, which this project does not
   have and will not invent — A14's band 5 was declared VOID-able in advance on exactly this
   ground. It needs a customer or a stated reference payload. **Open.**
3. **T-6** measures it. Its priority rises on this result. **Open.**

**One thing the specification found that was not in the original entry.** The deployer's own load
path contains soft-magnetic material: the magazine septum is **silicon steel**, 1.0 mm, between
adjacent satellites (`cad/parameters.json` `groups.magazine.septum_material`). It will both shunt
flux, which helps, and itself magnetise, which changes the field a neighbouring satellite sees.
**Nothing has modelled that**, and it is a second reason the in-cassette field is not simply the
sled field at greater distance. The cassette case remains unmodelled and is stated as such in the
specification rather than left to be assumed benign.

Shielding the payload is the option that should be resisted: it adds mass to the customer's
satellite, which is the modification the architecture exists to avoid.

### P35. The GMAT script generator is pinned to a superseded operating point: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **Corrected 2026-08-13.** The header claiming the point was *"identical to `astro.py`
> __main__ and `conjunction()` defaults"* is **struck**, because it was not and had not been
> since 2026-07-29.
>
> **The value stays at 20.37 m/s on purpose.** A5 and A6 were run at 20.37 and their sheets say
> so, so the generator matches the results it actually produced; regenerating at today's point
> would silently break the correspondence between a published result and the script that made
> it. **The defect was never the number — it was a file claiming to track a source it did not
> read.**
>
> **And the pin now checks itself.** `build_scripts.py` asserts at import that `DV` does *not*
> equal `astro.conjunction`'s current default, so if the two ever converge the stale explanation
> fails loudly instead of rotting in place. That is the same mechanism the 3-D field solve got
> after it returned zero: an assertion where a comment used to be.


`validation/gmat/build_scripts.py` carries `DV = 20.37` under a header saying the operating point
is "identical to `astro.py` __main__ and `conjunction()` defaults". **It is not.** `astro.py`'s
`conjunction()` default is now `dv=16.388`, three corrections later. Anyone regenerating the A5 or
A6 inputs today gets scripts at a velocity the project abandoned on 2026-07-29.

**It is LOW because nothing currently reads it wrongly.** A5 and A6 *were* run at 20.37 and their
sheets say so, so the generator matches the results it produced. The defect is that the file
claims to track `astro.py` and silently does not, which is the same failure class as the stray
`results/sizing.json` and the stale companion generator: **a second copy of an operating point
that nothing regenerates.**

**Deliberately not fixed by editing `DV`.** Changing it would make regenerated scripts differ from
the ones whose results are recorded, which trades one dishonesty for another. A15 therefore got
its own generator, `build_poem_campaign.py`, which reads Δv from `motor_results.json` at run time
and cannot go stale.

**Which branch was taken, 2026-08-13: the second.** The generator stays pinned to 20.37 m/s so
it keeps matching the results it produced, the false "tracks `astro.py`" claim is struck, and an
import-time assertion now fails if the pin ever silently becomes true. **The original criterion,
written when this was opened:** either re-run A5 and A6 at the current point and update the generator
together, or mark `DV` explicitly as the frozen historical value those two analyses were run at
and delete the claim that it tracks `astro.py`. The second is honest and costs nothing.

### P36. The track has no dynamic design case, and A17 says it needs one: CORRECTED 2026-08-13
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — a dynamic design case for the track

> **A33 ran 2026-08-13 and closed two of the three missing pieces, both as negative results.**
> Bands declared at `7baa062` before the script existed; **six of six pass.**
>
> **The moving-load model exists now, and the effect is not the problem.** With the sled aboard
> the first mode really does fall — **109.0 → 66.4 Hz** at midspan — so the track's first mode is
> not a number during a shot. But the ripple chirp reaches the fundamental at **x = 133 mm, 9 %
> into the stroke**, while the sled is still near the anchored end: the mode is depressed
> **0.8 %** there. **The excitation and the depression are separated in space, and A17's
> fixed-frequency SDOF was adequate.**
>
> **The travelling load is quasi-static.** Exit velocity is **5.01 %** of the beam's 327 m/s
> critical speed.
>
> **A dynamic acceptance criterion now exists** beside the static 70 Hz one, in the form of six
> declared bands, and the arrest — applied where it actually acts rather than at midspan —
> deflects the track **0.142 mm, 1.18 % of the winding gap.**
>
> **And a feedback path nobody had named is quantified.** Ripple acts 57.5 mm off the neutral
> axis → bending → gap change → thrust change → ripple. **Loop gain 0.095**, an order of
> magnitude from self-excitation, scaling with the square of eccentricity.
>
> **What stays live is the first of P36's three items: there is no measured damping anywhere
> in this project.** A17's 8.18x is used as given, and no bolted-aluminium Q has been measured.
> A17's 8.18× is used as given. That is a measurement, not an analysis, and it belongs to T-2's
> sine sweep in `docs/QUALIFICATION_PLAN.md`. Full sheet: `validation/A33_track_dynamics.md`.


`sizing.py::track_first_mode()` checks the track against one static target -- above 70 Hz to clear
the launch primary band. **A17 shows that is necessary and not sufficient.** Every shot chirps the
force ripple through the 109 Hz fixed-fixed mode, and the mode amplifies it **8.18x** at the
fundamental crossing, twelve times per campaign.

**It does not go away with damping.** Amplification moves from 6.51 at Q = 20 to 8.33 at Q = 500,
so no plausible bolted-aluminium Q rescues it. The governing parameter is the normalised sweep
rate `rate/f^2 = 0.18`, slow enough for the mode to respond fully regardless of Q.

**What the project does not have:** any damping specification, loss factor or Q for the track; a
moving-load model, since the ripple force travels with the sled and A17's SDOF does not represent
that; and a dynamic acceptance criterion beside the static 70 Hz one.

**What would close it:** a damping specification with a measurement behind it, and a moving-load
response model. **T-2's sine sweep becomes a pass/fail qualification item rather than a signature
comparison** on this result, and that belongs in `docs/QUALIFICATION_PLAN.md`.

**Not a kill criterion.** A17's displacement estimate -- 49 % of the +/-0.05 mm gap budget --
rests on an assumed effective mass and the unmodelled moving load, so it shows the coupling
matters without establishing that it breaks anything.

### P37. The retention gates were sized against a quasi-static load, not the launch environment: HIGH, NEW 2026-08-06
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — size the gates against the launch environment


**Found by A18 band 9, against a band declared before the run.** `sizing.py` sizes the retention
gate at **5.9 kN** through two D6 A-286 pins at MoS 1.2. Miles' equation on the GEVS protoflight
spectrum (14.1 g_rms, 0.16 g^2/Hz) at the track's 109 Hz fixed-fixed mode gives **11.7 kN at
Q = 10 and 20.2 kN at Q = 30** -- two to three and a half times the load the gates were sized for.

| Q | 3-sigma load | vs sized | MoS |
|---:|---:|---:|---:|
| 10 | 11.7 kN | 1.98x | 0.56 |
| 20 | 16.5 kN | 2.80x | **0.10** |
| 30 | 20.2 kN | 3.43x | **-0.10** |

**The pins may not be undersized; the load case was.** 5.9 kN is quasi-static. Random vibration
through a lightly damped 109 Hz mode is a different problem, and the claimed MoS 1.2 collapses to
0.10 at Q = 20 and goes negative at Q = 30, past the pins' 18.2 kN shear capacity.

**This compounds P36.** Both turn on a structural Q this project has never specified or measured,
and both make the same test decisive. `docs/QUALIFICATION_PLAN.md` already calls T-1 *"the single
most likely qualification failure"*; **it is now a predicted failure rather than a ranked risk.**

**What would close it:** a damping specification with measurement behind it, then resize the gates
against the random-vibration case, or isolate the cassette stack so the mode does not drive the
pins. **This is analysis only -- T-1 closes the test half of E10 and nothing here substitutes.**

> **RESIZED 2026-08-10 by A22, and the fix is eleven grams.** The gates go from **2 x D6 to
> 2 x D9 A-286 pins**: capacity 18.2 -> **41.0 kN**, and the margin of safety at Q = 30 goes
> **-0.36 to +0.45**. Across the whole sweep it stays positive, **+0.45 at Q = 30 to +1.51 at
> Q = 10**, so **the design no longer depends on where Q lands** -- which is the entire point,
> since A19 found Q was the only assumed input moving a margin through zero.
>
> **No architecture change was needed.** Splitting the stack across two gates was in the allowed
> space and is not required, so the magazine is untouched. The quasi-static case improves as
> well, MoS 1.21 -> 3.98, and **pin shear still governs** over bearing at 41.0 against 52.2 kN,
> so resizing pins was the right fix rather than the wrong one.
>
> **A definitional discrepancy fell out of it.** A18 quotes this margin as **-0.10**, computed as
> capacity/load - 1; `sizing.py` applies a **1.4 design factor** and gives **-0.36** for the same
> hardware. Both are correct and they are different quantities. **The factored form is used**,
> because dropping a design factor while resizing would be a silent relaxation -- so the figure
> quoted in this entry above is the kinder of the two readings.
>
> **The test half is untouched.** T-1 still closes E10, and Q is still unmeasured.

### P38. The paper claimed a payload magnetic environment its own validation had already falsified: CORRECTED 2026-08-10
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Corrected in the manuscript and the PDF rebuilt, 2026-08-10.** The EMC section stated that
because the Halbach self-shielding weak side faces outward, *"a magnetometer-carrying customer
payload sees a field comparable to a conventional reaction-wheel assembly at the same standoff"*.

**A14 band 4 falsified that on 2026-08-05** at **611× magnetometer full scale**, and opened
**P34** on the strength of it. The sentence survived for five days after the run that disproved
it, in the published PDF, because A14's outcome was propagated into `OPEN_PROBLEMS.md` and
`docs/KILL_CRITERIA.md` and not into `paper.tex`.

**This is the P25 failure mode with a longer fuse.** P25 recorded a retracted claim staying live
for a day; this is a falsified claim staying live for five, in the artifact most likely to be
read by someone outside the project. The defect is not the original sentence — it was written
before A14 existed and was a reasonable guess — it is that **nothing connects a failed validation
band to the deliverables that repeat the claim it failed.** `tools/check_artifacts.py` catches a
PDF older than its source; nothing catches a source older than its own validation result.

**Closed on its own terms, and the criterion says so.** **The original wording:** the correction is made, so the sentence itself is closed. The general
case is not, and is the part worth keeping: a band that FAILS should name the documents that
assert the thing it falsified, the way `docs/BASELINE.md` change control already requires a
baseline change to *"state which validations it invalidates"*. That rule exists in one direction
only. **Carried as the open half of this entry.**

### P39. The companion repositories were not a function of the commit they claim: CORRECTED 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `COMPUTATION` — the companion provenance gate exists; the entry predates it


**Corrected 2026-08-10 in `tools/export_companion.py`.** Found while regenerating the companions
from a clean clone, because the regeneration **deleted twelve files nobody had removed**.

`copy()` walked the **working tree** with `shutil.copytree`, so every file sitting inside a
manifest directory went into the companion whether or not the flagship tracked it. The published
`VOLLEY-paper` and `VOLLEY-thesis` therefore carried `validation/fea/plate.inp`,
`plate_clamped.frd`, `plate_clamped.dat`, `plate_modal.*` and the rest of A4's CalculiX
input decks and solver output — **twelve paths that are in no VOLLEY commit at all.**
`git log --all --diff-filter=A -- 'validation/fea/plate*'` returns nothing. The flagship tracks
exactly one file in that directory, `build_deck.py`.

**The stray files are not the defect. The provenance is.** Each companion carries a banner
reading *"generated from VOLLEY flagship 45332a7"*, and that statement was false: the tree it
described contained files that commit does not have. Worse, the output depended on **what
happened to be lying around when the export ran** — a machine that had executed A4 produced a
different companion from a clean clone of the identical commit.

**A generated artifact that is not a function of its stated input is not generated. It is
collected.** That is the same class as P19 and as the duplicate `results/sizing.json` that
`motor_model.py`'s header records: a second copy of something, produced by a path nobody
declared, that then disagrees with the original.

**Fixed:** `copy()` now filters against `git ls-files`, so nothing untracked can enter a
companion, and the export **names every path it skipped** rather than silently dropping it. On a
clean clone the filter is a byte-for-byte no-op, which was verified rather than assumed — and it
was verified to fire, by planting an untracked `plate_clamped.frd` and confirming it was excluded
and reported.

**What this does not fix, and it is the part worth arguing about.** `validation/README.md`'s own
conventions say to *"commit input decks and result JSON, never vendored solver code"* — and the
A4 decks are **not committed**. So the correct end state is probably that `plate*.inp` belongs in
the flagship and the solver output does not, rather than that all of it disappears. **The
companions have lost the input decks in this regeneration**, and they were the only published
copy. Recorded here rather than quietly restored, because restoring them means committing them to
the flagship first, and that is a decision about what the repository tracks.

**The decision was taken, and it is already in `.gitignore`.** `validation/fea/*.inp`, `*.dat`,
`*.frd`, `*.sta`, `*.cvg` and `*.log` are ignored, under the comment *"decks are regenerated by
`validation/fea/build_deck.py`"* — which **is** tracked. A deck is an output of a committed
generator, so the repository holds the generator and not the deck, exactly as it does for
`cad/`, `validation/fem3d/` and `validation/cfd/`. **The original criterion:** decide whether
`validation/fea/plate*.inp` belongs in the flagship. If
it does, commit the decks — `build_deck.py` regenerates them and needs only `gmsh` — and the next
export republishes them with real provenance. If it does not, `validation/README.md`'s convention
about committing input decks should say so. **Either answer closes this; the current state
answers it by accident**, which is what made the leak possible.

### P40. The repositioning cost was stated at half its real value, in the ADR that adopted the ConOps: MEDIUM, NEW 2026-08-10
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Corrected.** Same day, 2026-08-10, by the band that caught it.

`docs/CONCEPT.md` §4 and **ADR-024** both stated altitude repositioning at *"~14 m/s per Hohmann
leg"* and called it cheap. **A 50 km shell change is a two-burn transfer costing 27.82 m/s** —
13.92 m/s on the first burn and 13.90 m/s on the second. **14 m/s is one burn. The quantity is
two.**

**Found by A20 band 1 failing**, which is the only reason it was found at all. The band was
declared at 10–20 m/s against a row explicitly naming a two-burn Hohmann, so the band carried the
same error as the documents and **failed against the correct answer**. It is recorded as a
failure and **was not widened**.

**This is the A15 band 2 error repeating**: a band whose named quantity and whose stated limit
describe different things. There it was apogee spread against altitude extent; here it is one
burn against two. **Both times the error was in the band, not the model, and both times the run
is what exposed it.**

**What it changes.** Repositioning is not cheap. At 100 m/s of host budget the stage reaches four
shells rather than the seven the halved figure implied, and the propellant bill is a real
constraint against a budget nobody has disclosed (**E5**) rather than a rounding item. The
delivery claim in `CONCEPT.md` survives — A20 bands 2 and 3 both pass — but it survives at twice
the stated price.

**Why this is numbered under the freeze.** [ADR-021](docs/adr/021-freeze-the-register.md) admits
two of the three categories here at once: it is a defect that made a published Phase I deliverable
wrong, and it is a validation band miss. Both were live within hours of each other.

### P41. The payload slams into its cradle at the start of every shot, and nothing modelled it: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **A34 ran 2026-08-13. Bands declared at `77d45bb` before the script existed; five of five pass.**
>
> **The rattle settles long before the force is removed.** At a restitution of 0.7 — the top of
> the aluminium-on-aluminium range — bouncing stops after **27.25 ms of a 146.4 ms powered
> stroke**, and **the residual angular rate at force removal is exactly zero for every clearance
> in A23's table.** Critical restitution, above which bouncing would still be in progress, is
> **0.9261**.
>
> **So the 36–231 °/s arrival never becomes a release rate.** It is spent in the first tens of
> milliseconds, against a stop, while the force that caused it is still holding the payload
> there. Kill criterion 4's last open question resolves in the design's favour.
>
> **Corrected.** And A23's preload is now derived rather than asserted: Computed independently from the same
> moment and geometry — two contacts a half-length either side reacting 28.92 N·m as a couple —
> the answer is **85.0 N per contact**, reproducing A23's stated > 85 N. Propagated to
> `docs/KILL_CRITERIA.md` threat 4.
>
> **What is not closed:** restitution is **swept, not measured**, and `cad/parameters.json` still
> specifies no cradle fit. The requirement stands as a requirement. Full sheet:
> `validation/A34_cradle_restitution.md`.


**Found by A23 band 3**, which was declared as a `REPORT` row precisely because nobody knew what
it would return.

**The payload CoM sits 70 mm off the thrust line**, so the 413.2 N push produces a **28.92 N·m**
moment about it and an angular acceleration of **688 rad/s²** if the payload is free to rotate.
The cradle holds it **with clearance**. It is therefore not free for long — but it is free for
long enough:

| Cradle clearance | Time to cross | **Arrival rate** | vs the 2 °/s tip-off band |
|---:|---:|---:|---:|
| 0.05 mm | 0.92 ms | **36.5 °/s** | **18×** |
| 0.50 mm | 2.92 ms | **115.3 °/s** | **58×** |
| 2.00 mm | 5.84 ms | **230.6 °/s** | **115×** |

**No clearance in that range is benign**, including one tighter than the sled's own 0.05 mm
gap-shim tolerance.

**Two consequences, and the second is worse than the first.**

1. **It is an unsized load case.** The payload arrives with rotational energy into its own CDS
   corner rails, twelve times per campaign, and nothing in this repository has sized the rails,
   the cradle or the seat for it.
2. **It may set the tip-off rate instead of the release mechanism.** After impact the payload
   rebounds, re-crosses the gap and rattles. **Whether that has settled by release, 158 ms later,
   depends on a restitution and damping model this project does not have.** If it has not, tip-off
   is governed by a rattle at 18–115× the band rather than by the mechanism A23 specified.

**Tightening the clearance does not fix it.** Arrival rate goes as √(clearance), so a factor of
ten tighter buys √10 — 115 °/s becomes 36 °/s, still 18× the band.

**What closed it, written before A34 ran:** **preload the cradle** so there is no gap to accelerate across. A23 band
4 measured the couple reaction the preload must exceed at **85.0 N per contact**, which is modest
and achievable. The alternative is geometric — A23 band 5 prices it — and needs the CoM offset
cut from **70 mm to 3.5 mm**, which is aligning the payload CoM with the thrust line rather than
trimming it. **Preload is the cheap route and the redesign is the expensive one.**

**This is analysis only.** The rattle question is exactly what the multibody run **A7** was
specified for and has never had, and **T-5** is the test that would settle it on hardware.

### P42. The public site served superseded numbers for a week, and nothing was watching it: MEDIUM, NEW 2026-08-10
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Corrected.** 2026-08-10, and the guard that would have caught it is added in the same pass.

`docs/index.html` is the GitHub Pages site — **the most public artifact this project has**, and
the first thing anyone following a link sees. It carried the **pre-quadrature operating point**:

| Quantity | Site said | Correct since 2026-08-03 |
|---|---|---|
| Thrust constant | 11.22 N/kA·m, ±1.26 % | **11.03, ±0.99 %** |
| Exit velocity | 16.54 m/s at 10.7 g | **16.388 m/s at 10.53 g** |
| Net efficiency | 21.2 % | **20.99 %** |
| Dry / loaded mass | 76.9 / 124.9 kg | **76.5 / 124.5 kg** |
| Recoil per shot | 66.1 N·s | **65.6 N·s** |

**Seven days of a public page contradicting the repository's own baseline.**

**Its validation section was worse than stale — it was wrong about the project's own record.** It
said *"Three have now been run, and one of the three failed"* and listed A1, A6 and A7 as
"specified", against an actual **19 of 21 run**. A reader judging this project on its evidence
discipline was being shown a two-month-old snapshot of it.

**The cause is the one P38 already named, in a place nobody had checked.**
`tools/check_artifacts.py` guarded the paper PDF, the CV, `BASELINE.md` and the figures against
their sources. **It did not guard the website**, so the website was the one published artifact
with no tie to the numbers it quotes. P38 recorded that *"nothing catches a source older than its
own validation result"*; this is the same gap one layer out — nothing caught an **artifact** older
than its own **source**, for the one artifact that was not in the list.

**Fixed:** `docs/index.html` is now a guarded artifact of `motor_results.json`,
`mass_properties.json` and `astro_results.json`. It fired immediately on a 70-hour drift, which is
the check doing exactly what it exists for.

**What is not fixed, and is the honest remainder.** The site is **hand-authored HTML**, so the
guard can only detect drift, not prevent it — unlike `BASELINE.md`, which is *generated* and
therefore cannot drift at all. **The durable fix is to generate the headline table from
`analysis/results/*.json`** the way `make_baseline.py` does. That is not done, and until it is,
this failure mode is detectable rather than impossible.

**And the fix did not reach every surface. Found 2026-08-10, while replacing the renders.**
The **GitHub wiki** — a third public surface, and one nothing in this repository had ever
compared against anything — was serving the same pre-quadrature operating point the site was
(**11.22 N/kA·m, 16.54 m/s at 10.7 g, 19 % efficiency, 76.9/124.9 kg, 66.1 N·s**), plus the
render set withdrawn under P43, plus a repository link still reading `aaaaaaaaaaaavm/emocd`
under the old project name.

`wiki/Home.md` **in this repository is correct** and has been for a week; the live wiki is a
*separate git repository* (`VOLLEY.wiki.git`) that nothing syncs it to. So the flagship's copy
being right was never evidence that the wiki was, and `check_artifacts.py` cannot help: the
artifact it would guard is not in this repository at all.

**This is not closed.** The corrected page cannot be pushed from the working environment — a
wiki is not addressable as a repository through the GitHub API, so the tooling that publishes
the rest of this project cannot reach it, and it refuses
it. **Until `wiki/Home.md` is copied into the live wiki by hand, the wiki still publishes
superseded numbers.** That is the one part of P42 that remains outstanding, and it is recorded
here rather than left to be rediscovered.

### P43. The renders on the front page showed the satellite being fired into its own host: HIGH, NEW 2026-08-10
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record
> a provenance gap of its own, recorded below and not hidden


**Corrected.** 2026-08-10. Found by inspection of the render set, not by any check.

`cad/renders/seq2_midstroke.png` and `cad/renders/seq3_release.png` — used in `README.md`, on
the Pages site and in the wiki, three of the four surfaces a stranger sees first — showed the
payload **departing through the ESPA mounting flange**: the face that bolts to the host. They
also drew the CubeSat as a **wheeled road vehicle**, a sample-asset placeholder that was never
replaced.

**This is worse than a cosmetic defect, because the geometry is the argument.** The entire
interface case rests on the payload leaving along the track axis, out the muzzle, away from the
host. A reader taking those frames at face value would conclude the machine fires backwards into
the vehicle it is bolted to — and would be right to stop reading. The images had been the
project's most-viewed artifact for the whole time they were wrong.

**Cause.** The renders were produced as illustration and were never checked against the
requirement they illustrate. Nothing in `tools/` looks at an image, so no check could have caught
it; `check_artifacts.py` guards numbers against their sources and has no notion of a picture
being wrong about the thing it depicts. The render specification was written *after* the
defective set existed, which is why the departure direction is now stated explicitly wherever
the renders are described.

**Fixed.** The seven-shot Gen4 set replaces them: `hero_open`, `espa_interface`, `track_stator`,
`brake`, `sled_detail`, `envelope_closed`, `magazine_feed`. In every one the payload leaves along
the track axis, away from the flange, and each carries a drawn departure arrow so the direction is
stated rather than merely happening to be right. `cad/tools/prepare_renders.py` regenerates the
published set from the uncropped frames in `cad/renders/source/`. Only `exploded_view.png` is
retained from Gen3, because Gen4 has no equivalent shot, and it is labelled as Gen3 wherever it
appears.

**The honest remainder, and it is not small.**

1. **Gen4 has no committed STEP export** (ADR-019, `docs/GEN4_STATUS.md`), so the published
   renders now show geometry that **no file in `cad/step/` matches**. The repository trades a
   set that was wrong about physics for a set that is right about physics and unverifiable
   against a committed model. That trade is deliberate — a reader misled about the deployment
   direction is worse off than one told the picture is ahead of the export — but it is a trade,
   and it stands until the Gen4 export gate opens or Gen5 supersedes it.
2. **Gen4's stations are not the analysis model's.** Gen4 releases at s = 1200 mm over a 900 mm
   stroke; `analysis/` assumes release at 1500 mm over 1.5 m. P39 already holds this. Every
   caption on every surface has therefore been stripped of performance figures, and each states
   that no number is taken from Gen4.
3. **The payload is still a plain rectangular proxy**, not a modelled 3U satellite. Correct in
   its envelope and its direction of travel, and nothing more than that.
4. **No check exists that would catch the next one.** An image cannot be diffed against a
   requirement by anything currently in `tools/`. The renders remain the one class of published
   artifact with no automated tie to the repository's own claims — the same shape of gap as P42,
   one layer further out, and this time with no fix proposed because none is cheap.

### P44. At femtosat scale the separation hardware outweighs the satellites it separates: MEDIUM, NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `FLIGHT_OPS` — femtosat deployer masses actually flown


**A24 band 6 miss, 2026-08-10.** Declared ≤ 0.5 % of exit velocity, measured **0.508 %**.
The band is not widened; see `validation/README.md`.

The fixed-cell manifest (ADR-025) puts several satellites in one cell, and everything in a cell
leaves on the same shot at the same commanded velocity — so **cell-mates have a designed
differential of exactly zero and never separate from each other.** A24 band 6 tested the obvious
mechanism: a compressed shim at each internal interface, momentum-neutral because it pushes
cell-mates against each other rather than against the sled.

**It works for every class except the smallest, and there it inverts.**

| Class | Per cell | Payload in the cell | Shim hardware | Mean shift |
|---|---:|---:|---:|---:|
| **ChipSat / femtosat** | 720 | 3.600 kg | **7.190 kg** | **0.0832 m/s, 0.508 %** |
| PocketQube 1P | 24 | 6.000 kg | 0.230 kg | 0.010 % |
| 1U CubeSat | 3 | 3.990 kg | 0.020 kg | 0.001 % |

**720 ChipSats need 719 interfaces. At 10 g each that is 7.19 kg of separation hardware to
disperse 3.6 kg of satellites** — twice the mass of everything it exists to act on. It also stops
being momentum-neutral, because that mass leaves with one side of each interface, which is the
term the band actually caught.

**The 10 g shim is an assumption**, carried explicitly in `cell_manifest.py` and not sourced.
A lighter interface moves the number; nothing plausible moves it by the factor needed, because
the ratio is set by count, not by mass — 719 of anything is heavy next to 3.6 kg.

**ChipSat was already outside the mechanism's declared limit.** `payload_family.py` flags
anything above 200 per load as "a different machine, not a bigger magazine", and 8640 is 43× that.
**This does not rescue the band**, which was declared over every class sharing a cell, before the
script existed, and which one class missed.

**What would close it.** Not a lighter shim. The requirement itself is wrong at this scale:
8640 femtosats do not want 10 m of pairwise separation within 120 s, they want a **designed
dispersion across a swarm** — a distribution of velocities produced once, at cell level, rather
than an interface between every pair. That is a different mechanism with a different acceptance
argument, and it is **PII-13**. Until it exists, **the fixed-cell architecture is qualified for
PocketQube 1P and above, and is not qualified for ChipSat/femtosat.**

### P45. The flywheel buys the impedance and pays it back in mass: LOW, NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — flywheel specific energy from flown units


**A25 band 4 miss, 2026-08-10.** Declared ≤ the 3-string bank it replaces (19.5 kg), measured
**20.61 kg** — over by **1.11 kg**. The band is not widened; see `validation/README.md`.

A25 tested a flywheel motor-generator against **P26**, the supercapacitor bank that cannot source
the shot. **Band 6, the reason the analysis exists, passed decisively**: 35 mΩ series resistance
against A10's 68 mΩ ceiling, delivering 66 kW against 32.5 kW required. The impedance problem is
solved and the coupling that made P26 poisonous — the ceiling tightening as velocity rises — is
broken.

**It is not free.** The store lands at **mass parity**, not a saving:

| | Mass |
|---|---:|
| Motor-generators (the dominant term) | **9.76 kg** |
| Rotors + containment, counter-rotating pair | 6.00 kg |
| Bearings + converter | 4.85 kg |
| **Total** | **20.61 kg** vs a 19.50 kg bank |

**The miss is owned by a single unsourced assumption.** `MG_KG_PER_KW = 0.30` is an engineering
estimate for a high-speed PM machine with no datasheet behind it. At **0.25 the band passes**; at
0.20 it passes by 2.1 kg. And against the **four-string** bank that
`docs/DESIGN_OPTIONS_exit_velocity.md` calls the configuration "with margin", the flywheel wins at
every value tested, by **5.4 to 10.3 kg**.

**Two independent things would close this**, and neither is analysis:

1. **A real specific-mass figure for a 16 kW high-speed PM machine.** One datasheet decides the
   band. This is the same class of gap as E3 (no vendor quotations anywhere in this project) and
   is the cheapest thing on this list to close.
2. **Deciding whether the comparator is three strings or four.** The repository currently says
   both — 3 in the ESR table, "4 with margin" in the same paragraph. Against four, the flywheel
   already wins and this entry would not exist.

**What this does not settle, and is the real risk.** Bearings for a multi-thousand-rpm rotor in
vacuum across a multi-year mission are not designed here, and are a more credible route to
rejecting the flywheel than mass ever was. Neither is the launch restraint for a rotor. Band 5's
0.175 N·m·s residual also assumes the controller holds two rotors to **1 % speed match**, against
a single-rotor store of 17.5 N·m·s — five times the shot disturbance it sits beside.

### E29. Nothing computes the shot's angular impulse about the host, and a reaction wheel saturates in about four shots: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — the shot's angular impulse about the host


**Found 2026-08-10 while pricing momentum management, not by any check.**

`analysis/astro.py` models the host interaction as one line:

```python
res['recoil_Ns_per_shot'] = round(4.0 * DV, 1)
```

**That is linear momentum only.** A13 covers the *indexing* and *sled-return* disturbance —
0.44 °/s peak and a 1.37° attitude offset on a 200 kg host — but **nothing anywhere computes the
angular impulse the shot itself delivers about the host's centre of mass**, which is the term
that decides whether the host can hold attitude across a campaign at all.

**The linear part is mostly a non-problem, and should be said so plainly:**

| Host | Δv per shot | Campaign, 12 shots | Orbit change |
|---:|---:|---:|---:|
| 200 kg | 0.328 m/s | 3.93 m/s | −14 km |
| **2000 kg spent stage** | 0.033 m/s | **0.393 m/s** | **−1.4 km** |

On the ConOps ADR-024 adopted it is noise, and it is retrograde — the direction a stage wants for
disposal. **No flywheel, reaction wheel or CMG can cancel it anyway**: those store *angular*
momentum, and linear momentum in a closed system has three exits only — expel propellant, accept
the Δv, or fire something the other way.

**The angular part is the severe one and it is unmodelled:**

| Thrust line misses host CoM by | H per shot | Campaign | vs a 15 N·m·s ESPA-class wheel |
|---:|---:|---:|---:|
| 50 mm | 3.28 N·m·s | 39.3 | **2.6× saturated** |
| 250 mm | 16.39 N·m·s | 196.7 | 13× saturated |
| 500 mm | 32.78 N·m·s | 393.3 | 26× saturated |

**A wheel saturates around shot four at a 50 mm offset.** Desaturating 393 N·m·s needs thrusters,
which is the OTV this project exists not to be, or magnetorquers, which are orders of magnitude
short in any useful time. Bigger wheels do not help and CMGs do not help: the constraint is
momentum **storage**, not torque.

**There is no interface requirement anywhere in this repository that the thrust line pass through
the host centre of mass.** [ADR-010](docs/adr/010-host-agnostic-interface.md) specifies the mount
host-agnostically and `docs/PAYLOAD_ENVIRONMENT.md` covers the inward-facing half, but neither
states a permissible thrust-line-to-CoM offset. That absence is the defect: the cheapest fix by orders of magnitude attacks the moment arm rather
than the momentum, and it is currently nobody's requirement.

**The related lever, and it is the highest-leverage geometric number in the machine.**
`cad/parameters.json` carries `payload_com_offset_above_thrust_line = 70 mm`. That single number
drives **three separate open problems**:

1. **tip-off** — A23's 36–231 °/s cradle arrival, and the 2 °/s release band;
2. **this entry** — the angular impulse, via the payload's 413 N reacting 70 mm off-axis;
3. **track bending stiffness** — the same couple is the 96 N transverse load that sets the
   track's EI requirement, which scales as L³ and is what makes any longer track expensive
   (PII-11, PII-14).

Driving it toward zero is **cradle geometry, not new hardware, and not an architecture change**.

**What would close it:** a rigid-body angular-momentum budget for the shot over a campaign,
against a named host inertia and a stated CoM tolerance, with bands declared first — and an
interface requirement, in ADR-010's successor or an amendment to it, stating the permissible
thrust-line-to-CoM offset, which is the number the budget exists to set. Neither exists.


> **Answered 2026-08-16 by [A52](validation/A52_gen6_recoil.md), and the requirement now exists.**
> The angular impulse is **117.32 N·s × the CoM offset** per shot, accumulating across twelve
> because the magazine fires one way. **The thrust line must pass within 10.7 mm of the host centre
> of mass** to keep a 15 N·m·s wheel unsaturated over a campaign; Gen5's equivalent was 19.5 mm.
>
> **This entry's complaint was that no such requirement existed. It does now** — and it is
> demanding, because it is 10.7 mm to the centre of mass of a spent stage whose mass properties are
> not public (**E5**). **Momentum management is not optional at Gen6:** either the alignment is
> met, or the host dumps momentum between shots, and ADR-020's 1200 s cadence is enough time to.

### P46. K_t is a centre-plane value and overstates thrust by 4.42 %: CORRECTED 2026-08-13
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `DECISION` — apply the K_t correction or hold it -- D3
> **Corrected.** Applied 2026-08-13, three days after being computed and held. `thrust_constant()`
> now Gauss-Legendre averages `B_y` over z ∈ [−45, +45] mm before the Lorentz sum, which is a
> change to the physics rather than a pasted factor (ADR-015). **K_t 11.0258 → 10.5386, ratio
> 0.9558 — exactly A2 band 2's measurement — and v_exit 16.388 → 16.029 m/s.** `nz = 1`
> reproduces the superseded value exactly, so A2's ratio stays checkable. Propagated across 214
> occurrences in 37 live documents by `tools/propagate_baseline.py`, with the audit record
> excluded by construction. **ADR-030.**

**Found by A2, 2026-08-10.** The correction is **computed and held, not applied.** See below.

`motor_model.build_field()` has always used magpylib `Cuboid` sources with the real **90 mm
depth**, so the field was never two-dimensional. **The two-dimensional assumption is in the
thrust integral**, which samples `B_y` on the centre plane z = 0 and then multiplies by the full
depth as though that value held across all 90 mm:

```python
By = field.getB(np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1))[:, 1]
...
return float((...).sum() * dx * (WIND_THICK / 2) * DEPTH)
```

It does not hold. The field falls off toward the array's z-edges.

| | K_t, N per kA·m |
|---|---:|
| Centre-plane — reproduces the published value to 0.000 % | **11.0258** |
| **Depth-resolved**, Gauss-Legendre over z ∈ [−45, +45] mm | **10.5386** |
| Ratio | **0.9558** |

**A2 band 2 was declared at ≥ 0.95 and this passes by 0.008.** The model is inside the tolerance
that was declared for it, which is why this is a defect rather than a band miss. **But the better
number is now known, and it is 4.42 % lower.**

**What it moves, computed through `motor_model.shot()` with nothing else changed:**

| | Published | Depth-resolved |
|---|---:|---:|
| K_t | 11.0258 N/kA·m | **10.5386** |
| **v_exit** | **16.388 m/s** | **16.029 m/s** (−2.19 %) |
| Acceleration | 10.53 g | 10.07 g |
| Peak current | 339 A | 320 A |
| Stroke time | 158.6 ms | 162.3 ms |

**Why it has not been applied.** `docs/BASELINE.md` fixes K_t and v_exit, and every published
number in the repository, the paper and the CV descends from them. A re-baseline is a change-
control action with its own propagation pass across `BASELINE.md`, `paper.tex`, `docs/index.html`,
`SUMMARY.md`, the wiki, the companions and 23 guarded baseline values — **not something a
validation run does to itself.** The correction is recorded here, computed, reproducible from
`analysis/field_3d.py`, and waiting on that decision.

**What would close it:** either the propagation pass, or a decision that the centre-plane value
is retained deliberately as a stated approximation with its 4.42 % error quoted alongside it.
**Both are defensible; leaving the two numbers coexisting silently is not.**

**And the correction is probably not final.** A2 band 4 — an independent `getdp` 3-D FEM
cross-check — **was not run**, so 10.5386 is still magpylib, which is analytic superposition.
E2's objection that nothing here *solves a field equation* in 3-D stands. Re-baselining onto a
number that a different method has never checked would repeat the mistake this entry is about,
one level down.

### P47. The published velocity-loop gain is linearly unstable, and its numeric value is a bandwidth: HIGH, CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by A28, 2026-08-13, on bands declared at `3ae36ad` before the script existed.** Raised in
external review as an essential missing piece of work, and the review was right.

`motor_model.closed_loop_mc()` carried **proportional velocity feedback at a gain of 3500**, with
no plant model, no transfer function, no margin, no controller rate, no sensor dynamics, and no
check against the track's modes. Four of A28's six bands failed.

**The controller is feedback-linearised.** It divides the command by the modelled thrust constant
and multiplies by the modelled mass, so the plant's own K_t/m cancels and the loop transfer is
`L(s) = Kp/s · exp(−sτ)`. **Kp is not a current gain — it is an acceleration per unit velocity
error, in s⁻¹, and its numeric value is the gain crossover in rad/s.** 3500 s⁻¹ is a crossover at
**557 Hz**. That was never stated anywhere, and read as a current gain the number looks harmless.

| At Kp = 3500 s⁻¹, τ = 0.700 ms | | Band |
|---|---:|---|
| Gain crossover | 557.0 Hz | — |
| Phase margin | **−50.4°** | ≥ 45° |
| Gain margin | **−3.86 dB** | ≥ 6 dB |
| Closed-loop bandwidth | **671.0 Hz** | ≤ 36.3 Hz |
| Stroke with command above rating | **29.7 %** | ≤ 5 % |

**Two things made this invisible for as long as it was.** `closed_loop_mc` feeds back the
*undelayed* state, so its loop sits at zero latency, where 3500 does hold +69.9° of phase margin;
the published gain is marginally stable at a total lag of **449 µs** and no real sensor is that
fast. And the command is clipped to `[0, K_RATED]`, which turns a linearly unstable loop into a
bang-bang relay whose mean follows the feedforward term, with the terminal ±0.3 m/s photogate trim
removing the residual. **The dispersion figure was dominated by the saturation limits and the
terminal correction, not by the feedback it was attributed to.**

**Corrected.** `motor_model.KP_VELOCITY = 195` s⁻¹ — `design_gain()` returns 195.2 s⁻¹ as the
largest gain holding ≥ 50° of phase margin at 0.6 ms *and* bandwidth at or below a third of the
109 Hz first mode; the implemented value is rounded down to sit at or below it. Result: PM
**+82.2°**, GM **+21.2 dB**, bandwidth **36.3 Hz**, **0.0 %** of the stroke above rating.

**The gain falls 18× and the dispersion does not move**: 0.0271 → **0.0267 m/s**, both 0.027 to
two significant figures. The loop never needed the bandwidth; the dispersion is set by the
terminal trim and by the K_t and mass tolerances.

**Baseline change under rules 1 and 2** of `docs/BASELINE.md`. Only the dispersion row moved.
**K_t stays 11.0258 N/kA·m and v_exit stays 16.388 m/s** — neither depends on the controller.
**Validations invalidated: none**; nothing else reads `closed_loop_mc`.

**Two limits belong to other entries, not to this one:** the plant is rigid, so the 48 Hz and
109 Hz modes appear as a frequency the bandwidth is held away from rather than as a compliant
model in the loop (**P36**); and the delay is a stated assumption, because no sensor has been
selected (**E7**).

Full sheet: `validation/A28_control_stability.md`. ADR-027.


### P48. Two A29 bands failed, and neither failure is in the machine: LOW, NEW 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by A29, 2026-08-13**, on bands declared at `949fdf4` before `validation/cfd/` existed.
Numbered under [ADR-021](docs/adr/021-freeze-the-register.md) case 3: **a missed band produces a
numbered defect, never a widened band.**

**Band 2 — drag coefficient in 0.7 ≤ C_d ≤ 2.5. Result 0.523.**

The floor of 0.7 came from a rectangular bluff body normal to the flow, which sits near 1.05–1.2.
**The assembly is a stepped body, not a solid one:** the 3U payload leads with a 100 × 100 mm
face and the sled behind it is 172 × 140 mm, so a large part of the reference frontal area lies
in the payload's own wake. A coefficient referenced to a partly shadowed area is below the
textbook value for the shape the band compared it against.

**Band 1 settles that this is not a mesh artefact:** 6.3× the cells (92,774 → 581,779) moves
C_d by **4.86 %**, to 0.5497 — still far below the 0.7 floor. Refining does not recover the
missing drag. Three further checks say the solve is sound: peak C_p on the body is **0.975**
where stagnation should approach 1.000; the meshed wetted area is **0.4173 m² of 0.5612 m²** of raw STL, the difference
being the interior payload–sled interface; and the drag splits as forward faces **+0.233**, base
suction **+0.156**, sides **+0.001**, which is the classic bluff-body signature.

**Band 5 — the stator channel raises C_d by ≥ 10 %. Result −12.7 %.**

The plates **lower** drag, from 0.523 to 0.457, and tighten the spread from ±8.3 % to ±3.5 %.
The plate sits in the mid-plane the sled straddles and is acting as a **splitter**, not a wall —
a splitter plate in the near wake suppresses wake oscillation and raises base pressure, which is
what the tighter spread reports. **The consequence is useful: the free-stream figure is the
conservative one**, so the ground-test correction is quoted from the free case.

**Corrected.** What changes is the practice, not a number: no result moved and no band was edited.
**A drag band must name its reference area and the shape it is being compared against**, because
a drag coefficient without its reference area is not a number. This is the same class as A2's
band 3, which passed while measuring numerical cancellation on a symmetry axis: **a band can be
satisfiable and still be the wrong question.**

Full sheet: `validation/A29_ground_test_air_drag.md`.

### P49. A Gen6 proposal was sized on an assumption wrong by 22x, and the band declared to kill it did: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by A30 band 1, 2026-08-13**, on bands declared at `7df75ac` before
`analysis/edge_effect.py` existed. Numbered under [ADR-021](docs/adr/021-freeze-the-register.md)
case 3.

**PII-16 proposed driving a linear induction motor on the CubeSat Design Specification's own
aluminium corner rails** — the interface every deployer already touches, on every satellite,
requiring nothing to be added. `analysis/rail_drive.py` sized it at **513 N, 18.26 m/s on 1182 J**
and it looked better than Gen5 on every axis.

**It rested on a transverse edge-effect derating assumed at 0.55.** The file declared that at the
top as its dominant assumption; `docs/GEN6_RAIL_DRIVE.md` named 0.20 as the value at which the
idea would be dead. **The measured figure is 0.0253.**

| | |
|---|---:|
| Assumed | 0.55 |
| **Measured** | **0.0253** |
| Thrust, four rails at a generous 0.60 T | **41.9 N** |
| Required to reproduce Gen5's 10.5 g on a 3U | 413 N |

**No pole pitch rescues it**, and the reason is a contradiction rather than a shortfall: the edge
factor wants the secondary wide against the pole pitch, the airgap wants the pole pitch large
against the gap, and an 8.5 mm conductor in a 10.5 mm effective gap demands both at once. For a
narrow secondary the factor collapses as **(πc/τ)²/3** — quadratically, not gradually.

**Band 2 caught a bug in the solver before any of that was read off it.** The first run returned
**exactly 0.0000 for every geometry**, including one Russell–Norsworthy puts at 0.66. The imposed
field had been written as a real `cos(kx)`, which puts the stream function 90° out of phase and
integrates the thrust to zero for every width. With the travelling wave carried as a phasor the
solver agrees with the closed form to **1.0 %**. Fourth time a declared band has caught a defect
in an analysis rather than in the design; second time a solver has returned identically zero and
reported success.

**Corrected.** `rail_drive.py`'s `EDGE` is set to the measured 0.0253, so the file now reports
the rejection instead of the proposal, with the original assumption recorded rather than deleted.
`docs/GEN6_RAIL_DRIVE.md` carries a rejection header. **Nothing in Gen5 was ever changed on the
strength of the proposal**, which is why this is a corrected defect and not a baseline event.

**What survives, and it is the reason band 4 was declared in advance.** The same solver puts a
**90 mm flat plate** — the widest that fits inside a 3U's own section — at **0.6691**, 26× the
rail, making **1652 N at only 0.45 T** for **0.248 kg** of aluminium. **The drive is sound; the
rail is the wrong conductor.** Those are different findings and the band structure exists to keep
them apart.

### P50. The plate drive's thrust was quoted at the magnetic-pressure ceiling, and it reaches 23 % of it: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by A31 band 5, 2026-08-13**, on bands declared at `f3b73d6` before
`analysis/plate_normal_force.py` existed. The figure has been corrected wherever it appeared and
propagated.

`validation/A30_rail_drive.md` reported that a 90 mm × 340 mm × 3 mm aluminium plate makes
**1652 N at 0.45 T**, obtained by taking the magnetic-pressure ceiling **B²/2μ₀** and applying
A30's measured edge factor. **A layered-media solve of the actual double-sided geometry gives
378 N** — a factor of **4.4**.

| | |
|---|---:|
| Quoted in A30 | 1652 N |
| **A31, layered solve, same 0.45 T and same geometry** | **378 N** |
| Fraction of the magnetic-pressure ceiling actually reached | **22.9 %** |

**The ceiling is not reached because the gap is not zero.** B²/2μ₀ is the ideal thin-sheet limit;
with a 7 mm magnetic gap against a 48 mm pole pitch the field decays across the gap and the
coupling falls well short of it. The error was to treat a bound as an estimate.

**A30 band 4 is unaffected** — the edge factor is 0.6691 and that is a separate measurement, made
with a separate solver, and it still stands.

**Corrected in place, and the architecture still closes.** A31's design sweep puts the best point inside
the 25 g payload qualification cap at **900 N, 21.6 g, 23.48 m/s** at 0.75 T, and a conservative
**671 N, 16.1 g, 20.26 m/s** at 0.60 T — both on the same 0.248 kg plate, against Gen5's
16.39 m/s from a 9.445 kg sled. **What changes is the flux density the stator has to produce**,
from 0.45 T to 0.60–0.75 T, which is inside what an iron-cored stator gives.

**Band 5 also caught two structural faults in the solver before any of this was readable.** The
first run returned **705 % of the magnetic-pressure ceiling**: the model had one current sheet
and a flux return, which is a single-sided machine rather than the double-sided one being
designed; and the flux density was normalised on the **screened** field at the plate instead of
the **open-gap** field. Fifth time a declared band has caught a defect in an analysis rather than
in the design, and the second time in one day.

Full sheets: `validation/A31_plate_drive_normal_force.md`, `validation/A30_rail_drive.md`.

### P51. An A32 band tested a ratio where it should have tested an excursion: CORRECTED 2026-08-13
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by A32 band 3, 2026-08-13**, on bands declared at `0635b5c` before
`analysis/entry_transient.py` existed. Numbered under
[ADR-021](docs/adr/021-freeze-the-register.md) case 3.

Band 3 required the transverse force on the plate during the entry transient not to exceed its
own steady-state value. **It peaks at 2.73×.** But it never changes sign — it is **restoring
throughout**, and the overshoot is *toward* centre.

| | |
|---|---:|
| Steady-state transverse force at 0.5 mm offset | **0.824 N** |
| Thrust at the same point | 611 N |
| Transient peak | **~2.25 N**, for about 6 ms |

**The band asked the wrong question.** What decides whether the plate touches a stator is the
**excursion** across its 2 mm clearance, not a ratio to a steady state it is transiently
overshooting. As written, the band fails on a harmless over-restoring transient and **would have
passed a genuinely destabilising force that happened to be smaller than its own steady state.**

**Corrected.** The change is to the practice, not to a number: no result moved and no band
was edited. **A
stability band must be on the excursion or on the absolute force.** Same class as A2 band 3,
which passed while measuring numerical cancellation on a symmetry axis: **a band can be
well-formed, falsifiable, and still not be the question.**

### P52. The segmented stator puts a 30 % force ripple through the track's first mode: HIGH, NEW 2026-08-13
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — segment handover through the track mode


**Found by A32 band 4, 2026-08-13.** This one is in the machine.

Thrust ripple as the plate crosses a segment boundary is **30.1 % peak-to-peak** against a 20 %
band. **It is not the joint gap:** closing the unenergised gap from 10 mm to zero leaves **25 %**.
The cause is the **longitudinal truncation of the travelling field** at the edge of an energised
section — the end effect of a segmented long stator with a short secondary, intrinsic to the
topology rather than to the joint.

**Why it matters.** With four segments over the 1.30 m acceleration zone, the segment-crossing
frequency sweeps **0 → 61.5 Hz** across the stroke, and `analysis/sizing.py` puts the track's
first two modes at **48 Hz and 109 Hz**. A 30 % force disturbance sweeping through 48 Hz is
**A17's force-ripple chirp in a new place**, and **P36** already records that the track has no
dynamic design case. It cannot be assumed clear.

**What would close it.** Energising **overlapping** segments so the field under the plate is
never truncated is the obvious candidate and is not computed. Longer segments lower the crossing
frequency without removing the truncation. Either way this is a drive-and-track question that has
to be answered before the plate architecture is adopted, and it is the first item found in three
sheets that is a defect in the *machine* rather than in an analysis.

### P53. The 2026-08-13 baseline change reached the documents and not the scripts: CRITICAL, NEW 2026-08-14
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

**Found by a consistency sweep, 2026-08-14.** [ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md)
moved the rated shot from 16.388 to **16.029 m/s**. `tools/propagate_baseline.py` carried that
through the prose, and `sizing.py` and `motor_model.py` were edited by hand. **Eight other
analysis scripts were not**, because the propagation tool walks `.md` and `.html` only and a
number pasted into a `.py` is invisible to it:

| Script | What it carried | What it fed |
|---|---|---|
| `astro.py` | `DV = 16.388` | **every astrodynamic headline in the repository** |
| `attitude_budget.py` | `V_EXIT = 16.388` | recoil and campaign impulse |
| `actuator_trade.py` | `V = 16.388` | the whole A27 trade |
| `cell_manifest.py` | `V_EXIT_3U = 16.388` | A24 bands 5 and 6 |
| `mover_separation.py` | `v_exit=16.388` default | the reeving study |
| `reliability_architecture.py` | `16.388`, twice | delivered-life ratio |
| `segment_redundancy.py` | `V_NOM = 16.388` | dead-segment velocities |
| `sensitivity_ranking.py` | `pc.e19(16.388)` | the magnet-eddy elasticity |

**And one more, of a different kind:** `payload_family.py` carried `DEPLOYER_DRY_KG = 76.5`
under a comment reading *"mass_properties.json"*. Dry mass had moved to **84.5 kg**. So
kg-per-satellite — **kill criterion 1's entire subject** — was computed **8 kg light** while the
documents carried the corrected 7.042. A comment claiming a source is not reading the source.

**What moved when they were re-run.**

| Quantity | Published | Correct |
|---|---|---|
| Orbital lifetime multiplier | ×1.62 | **×1.60** |
| Lifetime extension | +61.8 % | **+60.2 %** |
| Lifetime ratio, fastest spring | 7.52× | **7.33×** |
| Velocity ratio, fastest spring | 6.6× | **6.4×** |
| Recoil per shot | 65.6 N·s | **64.1 N·s** |
| Campaign impulse | 0.787 kN·s | **0.769 kN·s** |
| Cold-gas mass loss at 3U | 7.5× | **8.3×** |
| Conjunction minimum | 54.9 km | **42.2 km** |

**No band verdict changed except A24 band 1** (**P54**). Every direction is unfavourable, which
is the expected sign: the correction lowered the velocity and raised the mass.

**Corrected.** No script holds a literal operating point any more. `motor_model.operating_point()`
is the single source and the eight callers read it; `payload_family.py` reads
`mass_properties.json`. A literal cannot fork if there is no literal.

**What this does not fix.** `tools/propagate_baseline.py` still walks `.md` and `.html` only. The
repair here removes the *literals it could not see*, rather than teaching it to see them — which
is the stronger fix, but only for the values that were de-forked.

### P54. A24 band 1 fails against a reference literal that has since been corrected: MEDIUM, NEW 2026-08-14
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — the band is against a superseded literal; the run is A24

A24 band 1 requires the fixed-cell model to return deployer mass per satellite within ±1 % of
`payload_family.py`'s figure, and encodes that figure as the literal **6.375 kg**. That literal
was `payload_family.py`'s output when the band was declared. **P53** corrected the output to
**7.042 kg**, so the band now reads `7.042 against 6.375` and **FAILS by 10.5 %**.

**The model and its reference still agree.** Both return 7.042. What disagrees is the band's
frozen snapshot of the reference.

**The band is not being edited.** It stands as declared and it stands as failed, because the rule
that bands are never adjusted after a result is known does not carry an exception for the times
it is inconvenient — and a band that references a moving quantity by value is a real defect in
the band, not a technicality.

**What would close it.** A **re-declared A24-R band 1** stating the tolerance against
`payload_family.py`'s *current* output rather than a snapshot of it, dated, with the original
band quoted beside it, and committed **before** the re-run. Every other band in A24 is unaffected.

### P55. `velocity_levers.py` prices every lever at the superseded centre-plane K<sub>t</sub>: MEDIUM, NEW 2026-08-14
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — re-price the levers at the depth-resolved K_t

`analysis/velocity_levers.py` drives `motor_model.shot()` with a per-row K<sub>t</sub>, and every
row carries a value derived **before** [ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md): the
as-drawn rows at `11.0258e-3`, the thinner-magnet rows at `9.14e-3` and `8.02e-3`, the two-layer
rows at `7.33e-3`. All four are **centre-plane** figures. The depth-resolved solve measured the
as-drawn array at **0.9558** of its centre-plane value, so every row in the table is optimistic
and `docs/DESIGN_OPTIONS_exit_velocity.md` inherits it.

**Why it is not fixed by scaling.** Applying 0.9558 to the changed-geometry rows assumes the depth
factor is independent of magnet thickness and airgap, and **nothing has measured that**. Scaling
them would produce four numbers that look derived and are assumed.

**What would close it.** Re-derive K<sub>t</sub> for each distinct magnetic geometry in the table
with `thrust_constant(nz=9)`, the same way the as-drawn value was re-derived, and re-run. It is
one solve per distinct geometry, four in total.

### P56. The phase-spacing claim is compared against the wrong baseline: **CORRECTED 2026-08-14 by A21-R**
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `COMPUTATION` — state the free baseline wherever the phase claim appears

> **Corrected.** A21-R ran on 2026-08-14, six of six bands pass, and the claim has been restated
> as orbit change in `README.md`, `SUMMARY.md`, `wiki/Home.md`, `docs/index.html`, `CONCEPT.md`,
> `LANDSCAPE.md`, `MARKET.md`, `CASE_STUDY.md`, `REVIEW_RESPONSES.md`, `FIGURE_INDEX.md` and both
> manuscripts, with release timing named as the free baseline for phase. **No band was edited:**
> A21's seven stand as declared and A21-R's six were declared before `comparators.py` changed,
> which changed by addition only. Measured: **468 s** by waiting against **1.38 days** commanded;
> **+28.8 km** of semi-major axis against **0 m**; **×1.602** of lifetime against **×1.0000**.

**Found by a literature check, 2026-08-14.** The front door, `SUMMARY.md`, `docs/CONCEPT.md`,
`docs/LANDSCAPE.md` and the manuscript all carry a version of:

> 30° of constellation phase spacing in **1.4–6.9 days**, against roughly **25 days** by
> differential drag, and **not achievable by design** with a spring.

**Differential drag is not the baseline a reviewer will use.** Satellites released at different
times from the same host arrive at different true anomalies **in the same orbit**, at zero Δv. At
450 km the in-track rate is **0.0641 °/s**, so:

| | |
|---|---|
| 30° of in-track separation, by waiting | **468 s — 7.8 minutes** |
| 30° by commanded differential velocity | 1.4 days |
| 30° by differential drag | ~25 days |

**And this project's own adopted cadence already does it.** [ADR-020](docs/adr/020-inter-shot-cadence.md)
sets the inter-shot interval at **1200 s**, which is **76.9° of in-track separation per shot** —
two and a half times the spacing the claim celebrates, for free, before the motor does anything.

**A spring and a clock deliver 30° of phase. The claim that a spring cannot is false.**

**What the two things actually do is different, and that difference is the fix.**

| | Timed release | Commanded differential |
|---|---|---|
| Satellites end up in | **the same orbit**, different true anomaly | **different orbits**, different period |
| Phase behaviour | **static — holds forever** | **drifts — never stops** |
| Cost | zero | the whole machine |

For a string-of-pearls constellation, **timed release is not merely cheaper, it is better**: it
gives a spacing that holds. Commanded differential velocity passes *through* 30° at 1.4 days and
keeps going, and a propulsion-less satellite cannot null it. **The design cannot hold a
constellation it phases.**

**What survives, and it is the stronger claim.** No amount of waiting changes an *orbit*. Raised
apogee (450 → 507.6 km), **+60.2 % of orbital life** against a spring's +8.2 %, and placement into
a chosen altitude shell are things only Δv buys. **The differentiator is orbit change, not phase
change**, and the repository has been leading with the weaker of the two.

**What would close it.** Restate the claim wherever it appears — front door, `SUMMARY.md`,
`CONCEPT.md`, `LANDSCAPE.md`, `MARKET.md`, `REVIEW_RESPONSES.md` and the manuscript — as orbit
change rather than phase spacing, with timed release named as the correct free baseline for phase.
`analysis/comparators.py` band 3 asserts *"a spring's designed differential is zero"*, which is
true and no longer sufficient; it needs a companion row for release timing. **The band is not
edited** — it passed as declared. A re-declared A21-R adds the row.

### P57. A voice-coil CubeSat deployer making this project's core claim has been on the reading list unread since 2026-07-30: HIGH, NEW 2026-08-14
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — read the voice-coil deployer in full and record it in PRIOR_ART under that file's five fields

[`RELATED_WORK.md`](docs/RELATED_WORK.md) already flags it: *"the nearest published neighbour to
this design's topology that has turned up so far. It has not been read."* A search on 2026-08-14
establishes what it claims, and it is this project's claim.

**Zhao, Yue, F. Yang & Zhu (2022),** *IEEE Trans. Ind. Electron.* **69**, 13305 — a double
magnetic-circuit voice coil actuator **for CubeSat deployers**, whose stated purpose is *to control
precisely the separation velocity of CubeSats with different masses*, where *the separation speed
of the CubeSat can be directly controlled by regulating the current value*. It is a **direct-drive
linear machine with no moving magnet carrier** — the sled-free topology this project has been
treating as an open design direction — and it is cited by **all three** Harbin papers.

**Why this is a defect and not a reading task.** `docs/PROVENANCE.md` records **P22**: a literature
check found published work on this exact concept that the paper did not cite, and two claims did
not survive it. **This is the same failure, on the paper the project had already identified as the
nearest neighbour and then did not retrieve for two weeks.** Any novelty claim about programmable
separation velocity is unsupported until it is read.

**What would close it.** Retrieve and read it in full; record thrust, stroke, actuator mass,
velocity range, payload range and whether hardware was tested, in `PRIOR_ART.md` under the same
five fields as the other five; then state explicitly what this project claims that it does not.
The full text is behind a subscription, so this needs institutional access.

### P58. The thesis manuscript was a stale fork of the conference manuscript: CORRECTED 2026-08-14
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

**Found while correcting P56.** [ADR-031](docs/adr/031-four-repositories-not-two-phases.md) states
that paper and thesis carry **"the same concept … different scope … but not different designs."**
They were different designs.

`VOLLEY-thesis/source/paper.tex` and `VOLLEY-paper/paper/paper.tex` share every section heading,
every figure path and 414 of 447 lines. **The 33 that differed were all superseded numbers** —
K<sub>t</sub> 11.03 against 10.54, exit velocity 16.4 against 16.0, 10.5 g against 10.1, 2.85 kJ
against 2.78, 240 mm of regen stator against 39, 76.5 kg against 84.5, efficiency 21.0 % against
18.8 %, deployer mass per 3U satellite **6.38 kg against 7.04**, and the depth-averaging sentence
[ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md) added, which the thesis lacked
entirely. **Not one difference was thesis-specific.**

**Why it happened.** The manuscript moved into the companions under
[ADR-028](docs/adr/028-no-latex-in-the-flagship.md) on 2026-08-13 and stopped being generated. The
export tool that had kept the two in step no longer touches either, and nothing replaced it — so
the baseline change reached the repository the author edited and not the one they did not. **The
same shape as P53**: a propagation that stopped at the boundary of the tool that performed it.

**Corrected.** The thesis manuscript is now byte-identical to the conference manuscript and rebuilt
at fifteen pages with no undefined references.

**What is not fixed.** Nothing checks this. Two authored manuscripts in two repositories can fork
again the moment either is edited, and neither `check_links.py` nor `make_baseline.py` can see
across a repository boundary. **A cross-repository manuscript check is the missing tool**, and
until it exists this defect is one edit away from recurring.

### P59. Kill criterion 1 is unreachable by architecture and unreachable by manifest size: CRITICAL, NEW 2026-08-14
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — D2: which payload class is the product

**A36 band 4 missed.** The band required kilograms per satellite to reach the ~2 kg threshold at a
manifest of **N ≤ 30**. It first reaches it at **N = 116**.

Two runs have now closed two of the three routes to this criterion by measurement:

| Route | |
|---|---|
| **Architecture** | **Closed by [A35](validation/A35_constraint_ledger.md).** **88.67 kg — 70.06 %** of dry mass survives every deletion of every requirement in all 64 corners; the deletable fraction caps at **29.90 %**. *A35's run sheet still reads 49.23 / 58.2 / 41.8 at the pre-A46 dry mass — [P95](#p95-a35s-headline-survives-everything-figure-is-pre-a46-and-correcting-it-reverses-a35s-own-escape-route-critical-new-2026-08-20)* |
| **Manifest size** | **Closed by [A36](validation/A36_magazine_density.md) band 4.** The N → ∞ limit is a healthy 0.954 kg/satellite, but 2.0 kg is first reached at **N = 116**, and no factorisation of 116 packages inside the 1500 mm track length. The largest manifest that fits is **N = 126**, at **1.941 kg/satellite** on a **244.6 kg** machine running a **42-hour** campaign |
| **Smaller payloads** | **Open.** `docs/PAYLOAD_CLASSES.md` already puts PocketQube at 0.266 kg/satellite |

**The criterion survives by one route, and that route is a different market.** A PocketQube
deployer is not a 3U deployer with smaller cells — it is a different product, a different customer
and a different qualification campaign, and every CAD file, cassette and cost model in this
repository is 3U. That is **D2** in `docs/STATE_OF_THE_PROJECT.md`, which has been open since
2026-08-13 and is now the only thing standing between this project and a crossed kill criterion.

**What this is not.** It is not a reason to widen the criterion. `docs/KILL_CRITERIA.md` sets ~2 kg
because that is the class figure a canisterised dispenser achieves, and a threshold moved after a
result is known is not a threshold. **The correct outcomes are: change the payload class, accept
the criterion as crossed and say so on the front page, or renegotiate it against a stated
capability-normalised metric** — and the third needs care, because *Δv per kilogram per satellite*
flatters this design by 5.4× and is exactly the sort of metric a project adopts when the plain one
has stopped being kind.

**What would close it.** An owner decision on payload class (**D2**), taken explicitly and recorded
as an ADR. No analysis closes this; two have now tried.

> ### A third route opened the same day, 2026-08-14 (**A37 band 5**)
>
> **If the deployer is not carried by a stage but *is* one**, 43.33 kg of this ledger becomes stage
> structure that names the subsystem providing it, and 29.75 kg is deleted outright by a design
> with no mover and no pulse. What remains is **11.45 kg of containment**, and on a small
> kick-stage class **added mass per satellite is 1.608 kg against the unchanged 2.0 kg threshold.**
>
> **The threshold did not move and dry mass per satellite still crosses at 7.044 kg.** Both
> numerators are reported together wherever either appears, which is what A37 bands 1–3 exist to
> enforce. **This entry stays LIVE** — a second numerator argued on its merits is not the same as
> the criterion being met, and D2 remains the decision that settles which numerator a customer
> actually pays.

### P60. The energy store scales as v² and is now the binding constraint: **CORRECTED 2026-08-14 by A39**
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **Corrected.** A39 ran the store trade the entry asked for, seven of seven bands. **The store was
> the wrong store.** A steel spring is 11.41 kg at 32.7 m/s and busts the budget at 34.3; **cold gas
> is 2.98 kg and busts it at 89.4.** The reason is not energy density — **a spring must be cocked
> twelve times and gas does not**, so 4.28 kg of wind mechanism becomes a valve. Corrected for the
> three assumptions most likely to be optimistic, gas lands near 6 kg and every band still passes.
>
> **A35's falsification test passes with it:** the pulse chain released 23.76 kg and its replacement
> weighs 2.98, against a 14.26 kg falsifier. **The mass did not relocate.**
>
> **What replaces it:** gas removes a mass problem and introduces a fluid-system problem. Filling a
> 0.43 litre swept volume in a 133 ms stroke is roughly **3 L/s** through a regulator, and A39
> models none of it. The binding constraint on velocity is now **stroke length**, not mass.

**A37 bands 4 and 8 missed.** Band 4 was the falsification test
[A35](validation/A35_constraint_ledger.md) declared and left open: the pulse chain released
**23.76 kg**, so its replacement had to weigh under **14.26 kg** or the mass had merely relocated.
Band 8 required the store to stay under half of everything added.

At the selected point the store and its mechanism weigh **41.86 kg — 78.5 %** of added mass.

**The physics.** Store energy goes as **v²**, so spring mass does too: 4.91 kg at 1.5 m of stroke,
9.81 kg at 3.0 m, **26.16 kg at 8.0 m**. Stage length is free and the spring that exploits it is
not. **Every previous run in this project was about where the kilograms live. This one says the
next question is a store trade.**

**Two things about this failure are recorded rather than glossed.**

**The selection rule was badly designed.** No declared stage class satisfied every band, so the
script fell back to maximum velocity — the worst case for both failing bands. **At the small class
the falsifier passes comfortably at 7.85 kg.** The bands are evaluated as declared and the failure
stands, but its proximate cause is a fallback rule rather than the physics.

**And the declared classes bracket the answer without containing it.** Derived after the run and
not a band: every declared band is satisfied for stroke between **1.83 m and 2.18 m**, at
**30.0–32.7 m/s** and about **1.83 kg/satellite**. The classes declared were 1.5, 3.0 and 8.0 m.
**No class was added after the run and none will be.**

**What closed it.** [A39](validation/A39_store_trade.md), the store trade this entry asked for,
declared against the window above rather than around it and carrying the gas store A37 deliberately
excluded. Seven of seven bands. **The gas mechanism model is still assumed rather than derived** —
1.5 kg of piston, seals, regulator and valving, the largest guess in that run and over half the
selected total.

**What it does not undo.** A37 band 5 passed at **1.608 kg/satellite**, so kill criterion 1 closes
at 3U on the small class. **P60 is about how fast the machine can be, not whether it closes.**

### P61. A34's recorded figures are stale against its own script: MEDIUM, NEW 2026-08-14
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

**A38 band 1 missed.** It drove A34's own imported closed forms at the Gen5 point and required
A34's published answer back within 1 %. It returns **27.88 ms** against a recorded **27.25**, a
2.3 % miss.

A34 was recorded on **2026-08-13**, at the operating point
[ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md) superseded **the same day**.
`analysis/cradle_restitution.py` computes its inputs live from `motor_model`, so **the script
tracked the correction and the record did not.**

| | Recorded | Current |
|---|---:|---:|
| Payload force | 413.2 N | **395.1 N** |
| Offset moment | 28.92 N·m | **27.65 N·m** |
| Angular acceleration | 688 rad/s² | **658 rad/s²** |
| Settling at e = 0.7 | 27.25 ms | **27.88 ms** |
| Preload per contact | 85.0 N | **81.2 N** |

**No band verdict flips.** Re-running A34 today passes all five of its bands. Only the recorded
detail values are stale.

**Corrected.** A34's run sheet is **not edited** — it is a record of a run at its own operating
point, which is why `validation/A*.md` is excluded from every propagation this project runs. It is
**annotated in place** with both columns side by side, the treatment `docs/CROSS_INDUSTRY.md` and
`docs/VALIDATION_REPORT.md` already carry, so a reader reaches the current figures without the
record being rewritten.

**The general case is not fixed.** Every run sheet whose script reads `motor_model` live has the
same exposure, and **nothing checks it.** A regression band comparing a run sheet's recorded
figures against its script's current output would catch the whole class; A38 band 1 caught this one
by being pointed at it deliberately. **Recorded rather than built**, alongside the cross-repository
manuscript check **P58** names and the same tool does not exist for either.

### P62. The published wiki drifted sixteen days and four corrections behind its own source: MEDIUM, NEW 2026-08-14
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

`wiki/Home.md` is tracked here and is corrected by every propagation this project runs. **The live
wiki is a different git repository** — `VOLLEY.wiki.git` — that nothing here writes to, and
**nothing anywhere said so.**

On 2026-08-14 the live page had not been touched since **2026-07-30**. It still named the project
*emocd*, still quoted a **20.37 m/s** headline from before the CAD sled reconciliation, still
reported a **×1.62** lifetime multiplier from before the depth-resolved thrust constant, and still
made the phase-spacing claim withdrawn the same week as **P56** — **a claim shown to be false, on
the most public surface this project has.**

**Two charts on it were worse than the prose.** The energy split carried the pre-correction values,
and the conjunction chart plotted **20.00–21.00 m/s**, a velocity regime three corrections out of
date. Both are recomputed at the current point, and the conjunction chart gained the caption it
needed: a 2.5 % change in velocity moves the minimum approach from **42.2 km to 9.3**, which is why
this project quotes the realignment period as the robust quantity.

**This is P58 and P61's class.** Every check here walks tracked files; the wiki is tracked, so it
was corrected. **It is published across a repository boundary no check can see.**

> **Still unpublished as of 2026-08-16, and the reason is now precise rather than vague.**
> `tools/publish_wiki.sh` clones, diffs and dry-runs correctly from any environment — reading
> `VOLLEY.wiki.git` works — but the push is refused: *the wiki is not in the session's authorized
> repository set, so no credential is injected for it.* **A wiki cannot be added to that set
> either, because GitHub does not expose wiki repositories through its API**, which is what this
> script's own header warned. **There is no automated route; the script has to be run from an
> ordinary clone with ordinary push credentials.**
>
> The live page is now **seventeen days and six corrections behind**: it still says *emocd*, still
> reports a **×1.62** lifetime multiplier against the current ×1.60, and predates the enclosure
> buildup entirely. The pending change is **92 insertions and 37 deletions**.

**Corrected.** `tools/publish_wiki.sh` publishes the source and `--dry-run` shows the delta first;
`wiki/README.md` states that committing `Home.md` changes nothing a reader sees until it is
published. **The publish itself is not done** — GitHub does not expose wiki content through its
API, and the publishing route used for every other surface here cannot credential a `.wiki`
repository, so it needs an
ordinary checkout.

**And the honest disposition of the surface itself.** The wiki is **the least trustworthy thing
this project publishes**, because it is the only one that can be stale without anything failing.
The page says the repository is authoritative; it now also says so where it can be checked.

### P63. A39's gas result assumed a regulator it did not price: **CORRECTED 2026-08-14 by A41**
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **Corrected.** The regulator was removed rather than priced. A41 ran the third repair —
> a chamber charged to a commanded pressure over the indexing window, fired as a closed adiabatic
> expansion. Eight of eight bands. **A 2 L chamber at 50 bar gives 30.54 m/s at 25 g, on a 4.66 kg
> store**, against A39's regulated estimate of 2.98 and A40's fixed-orifice **14.16 m/s**.
> **Added mass per satellite is 1.343 kg** against A37's 1.608, at a higher velocity.
>
> **There is no regulator, no flow-rate problem and no valve timed to a millisecond.** Velocity is
> commanded by charge pressure at **0.499 % per 1 %**, a static measurement taken before the shot,
> against A40's valve timing at **10.53 % per ms**.

**A40 bands 1, 3, 6, 7 and 8 missed.** [A39](validation/A39_store_trade.md) selected cold gas at
**2.98 kg** on a quasi-static argument: swept volume times a **50 bar working pressure** equals the
energy needed. **Holding 50 bar at the piston through a 2.18 m stroke is a regulator**, and A39
neither said so nor sized one.

[A40](validation/A40_blowdown_transient.md) modelled the unregulated version — a fixed orifice fed
from the 200 bar bottle — and it does not work:

| | |
|---|---:|
| Mean acceleration needed for 32.7 m/s over 2.18 m | **25.0 g** |
| Mean acceleration delivered by a fixed orifice | **4.7 g** |
| Exit velocity | **14.16 m/s** against a 30 m/s band |
| Gas consumed | **3.39 g** against A39's 24.02 |

**The cylinder is smallest at the start, so pressure peaks there; as the piston runs away the
volume grows faster than a fixed orifice can fill it.** Flow area is not the constraint — the
orifice is **0.71 mm** against a 10 mm limit. A fixed area cannot track a growing volume.

**What this does and does not overturn.** A39's mass result is **not refuted, it is conditional**:
2.98 kg holds *if* a regulator that maintains 50 bar while flowing ~0.36 kg/s, and settles inside a
133 ms stroke, fits inside the **1.5 kg** allowance A39 declared for "piston, seals, regulator and
valving" — **the largest guess in that run, and now the component the whole result depends on.**

**What survives.** One **1.71 L** bottle does run twelve shots, with **4.5 %** velocity droop
(A40 band 5). That was the result most likely to fail on a transient and it held.

**What closed it.** The third of the three: a **pre-charged chamber**, in
[A41](validation/A41_precharged_chamber.md). The first-order guess that the expansion ratio would
be the binding variable was right — **velocity saturates toward the 2139 J constant-pressure
ceiling while gas grows linearly with chamber volume**, so 2 L to 4 L buys 1.0 m/s and costs
3.2 kg. **The regulator and the profiled orifice are not disproved, only unnecessary.**

**And one band failure was a declaration error, recorded as such.** A40 band 1 assumed a wide
orifice reproduces A39's case. It does not — it reproduces the *unregulated* 200 bar case, which is
**100 g** on this piston. The band stands as failed; what it exposed is this entry.

### P64. A41's reservoir is sized on gas the bottle cannot give back: HIGH, RESOLVED 2026-08-16 by A43
> **Status:** `CLOSED` — resolved; see the entry for what closed it

**A42 band 3 missed.** [A41](validation/A41_precharged_chamber.md) sized the reservoir by dividing
total charge by storage pressure — **6 L at 200 bar for twelve 100 bar·L charges.** That assumes
the bottle can be drawn to **zero**. It cannot: below the charge pressure it can no longer fill a
50 bar chamber, and the last quarter of the gas is stranded.

**A42 measures it running out at shot seven of twelve.**

**The correction is bounded, not single-valued, and the reason is A42's own model.** It treats the
reservoir as **adiabatic**, so it cools as it empties and loses pressure faster than mass alone
would give. That is right for a fast blowdown and **wrong for a cadence of twenty minutes**
([ADR-020](docs/adr/020-inter-shot-cadence.md)), where the bottle re-equilibrates between shots.

| | Reservoir | Store | Added per satellite |
|---|---:|---:|---:|
| **Isothermal**, the cadence case | **7.65 L** | **4.67 kg** | **1.344 kg** |
| **Adiabatic**, as modelled | **11.25 L** | **6.01 kg** | **1.455 kg** |

**Band 3 fails at either end and bands 5 and 6 pass at either end**, so the architecture is not in
doubt — **the store mass is, by about 1.3 kg**, and the truth sits nearer the isothermal figure.

**What would close it.** A thermal model of the reservoir between shots, which is the only term
separating the two columns. Failing that, **carry the adiabatic figure**, which is the conservative
one, and say that it is.

**And the cheap repair if the reservoir ever needs to shrink:** the fired chamber vents **43 bar of
a 2 L volume every shot** and A41 models no recovery of it at all.

> **Closed 2026-08-16 by [A43](validation/A43_reservoir_thermal.md), and the answer is the opposite
> of the one this entry expected.** A thermal model of the reservoir between shots gives a
> conduction-only time constant of **17 460 s against a 1200 s cadence** — the bottle does not
> re-equilibrate, because nitrogen is transparent in the infrared and free fall removes convection.
> **The design number is 9.55 L**, the no-relaxation case, against the 11.25 L this entry carried.
> The sentence above reading *"the truth sits nearer the isothermal figure"* is **withdrawn**; it
> sits at the other end. Added mass per satellite is **1.403 kg** at the conservative end and
> **1.384 kg** at the physical one, against a 2.0 kg threshold that has not moved.

### P66. Both ends of P64's bracket are unreproducible, and they are in the parameter file: MEDIUM, NEW 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by [A43](validation/A43_reservoir_thermal.md) band 1**, which was declared to check that the
new formulation reproduced A42's isothermal figure before anything else in the run was believed. It
does not, and neither does the other end.

| | A42 carried | A43 computes | |
|---|---:|---:|---|
| Isothermal | **7.65 L** | **8.25 L** | 7.8 % low |
| Adiabatic | **11.25 L** | **9.55 L** | 17.8 % high |

**The two errors have different causes and only one of them is arithmetic.**

**The isothermal figure was never computed by a script.** `analysis/fill_window.py` contains no
isothermal path; 7.65 L appears in A42's result table, in `cad/parameters.json` as
`reservoir_volume_isothermal_l`, and in ADR-032, without a generator. It is the only number in the
Gen6 store that no file produces.

**The adiabatic figure is a bookkeeping error.** A42 carried *pressure* across shots and recomputed
mass at each shot start as `p·V/(R·T₀)`. Gas that has cooled adiabatically is denser than that at
the same pressure, so the model **discarded mass that was really there** and asked for a bigger
bottle than the physics does.

**Corrected.** `cad/parameters.json` now carries **9.55 L** as the design reservoir with the
conduction estimate and the isothermal limit beside it, each naming A43 as its source; the Gen6 CAD
is regenerated against it; and ADR-032 and A42's result table are annotated rather than rewritten,
because A42's bands stand as declared and its result is the record of what that run found.

**What it does not change.** The *direction* of A42's correction was right — A41's 6 L bottle is
undersized and runs out at shot seven. Band 3 fails at 8.25 L just as it failed at 11.25.

### P65. `register_status.py --check` never checked the generated result it was written to guard: MEDIUM, NEW 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found on 2026-08-16 by a working-tree check, not by any tool here.** `analysis/results/register_status.json`
still read **98 entries, 39 live** after **P64** was added on 2026-08-14. The four checks were run
repeatedly across that window and every one of them passed.

**The cause is two lines of control flow.** `--check` verified that every entry carried a `Status:`
line and then returned — *before* the code that builds the JSON. The generated result was written
only by a bare run, and nothing anywhere compared the committed file against a fresh one. The
tool's own docstring said `--check` "verifies that every entry has one and that the headline counts
match"; the second half of that sentence was never true.

**Why it is worth numbering rather than quietly regenerating.** This is the same failure as
**P63** — a generated artifact whose currency was assumed rather than demonstrated — and the same
repair: prove it by rebuilding and comparing, never by inspecting a timestamp or trusting a
docstring. Two guards in this repository had the defect they exist to prevent.

**Corrected.** The payload is now built by one function used by both paths, `--check` rebuilds it
and compares against the committed file, and it names the fields that differ so the failure says
what moved. Verified by reverting the file and confirming a non-zero exit. The stale counts are
propagated to the front page, the register header and the wiki source.

### P67. Gen6's precision rests on a seal friction nobody has measured, and its rated velocity excludes it: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HARDWARE` — measure the seal friction -- B-2


**[A44](validation/A44_gen6_dispersion.md) bands 4 and 6 failed, and both failed on the same term.**

| Term | 3σ alone | Share of variance |
|---|---:|---:|
| **Seal friction**, ±20 % of A41's allowance | **0.3115 m/s** | **93.4 %** |
| Payload mass, ±0.5 % | 0.0725 m/s | 5.1 % |
| Charge pressure, ±0.25 % FS | 0.0399 m/s | 1.5 % |

**Two separate defects, and the second is the one that will be quoted wrongly.**

**The precision claim.** Gen5 commanded velocity through a designed loop at **0.0274 m/s (3σ)**.
Gen6 has no loop — the shot is a 133 ms open-loop expansion — so its spread is whatever the
hardware's repeatability is, and **93.4 % of it is a seal friction that has never been measured,
specified or designed.** A41 band 8 computed an *allowance* of **83.4 N**, meaning the machine
tolerates that much; no run has ever said what the friction *is*. **A fivefold better pressure
transducer moves the answer by 0.008 %**, so there is no instrumentation route to the claim.
Dispersion is also worst where the setpoint is lowest — **2.290 % at 20 m/s** against 1.041 % at
30 — which is exactly where a customer asking for a small trim would use it.

**The rated velocity.** **30.535 m/s is a zero-friction number.** It is what `cad/parameters.json`
carries as `exit_velocity_m_s` and what ADR-032 quotes. At A41's own full tolerable friction the
same charge gives **29.009 m/s**, 5.00 % lower. Both are real — a ceiling and a floor — and
neither should appear alone. The parameter file now carries both with its source naming this run;
**the value is not silently changed**, because which of the two is the design point is a decision
and not a correction.

**What would close it.** A measured or supplier-bounded seal friction, with a shot-to-shot spread,
for the actual piston seal at 50 bar in vacuum. That is a bench test on a component, not a
calculation, and it is the second item after `docs/B1_ORDER.md` that changes the category of
evidence rather than its degree.

> **It has an order now, 2026-08-22: [`docs/B2_ORDER.md`](docs/B2_ORDER.md).** Written the same way
> B-1 was and for the same reason — *a procedure invites more analysis, a purchase order invites a
> purchase.* A stock ISO 6432 16 mm cylinder, which [A61](validation/A61_seal_class.md) band 7
> already showed costs **0.00 %** against the drawn bore; a logging load cell, where the binding
> requirement is sample rate rather than accuracy because breakaway is a transient; three units,
> because the spread is half the question. **₹8,000–26,000, all of it estimated and none of it
> quoted.**
>
> **Its bands are declared in the order file, before the cylinder is bought**, and **band 8 is the
> one that constrains the author**: it requires an explicit answer to *"does this discriminate, or
> only bound?"* **before** the thresholds are quoted anywhere. An air-side, low-speed, possibly
> unpressurised pull is a *different* measurement from a PTFE seal at 22.73 bar and 17 m/s in
> vacuum — **not a cheaper version of the right one** — and the order says so. *Landing between
> 17.8 and 22.3 N is declared in advance as a real outcome that answers nothing*, so it cannot be
> argued into an answer afterwards.

**What it does not touch.** Bands 1, 2, 3, 7 and 8 all pass. The architecture is not in question
and the store is not affected.

> ### This entry now decides an architecture, 2026-08-20 — [ADR-036](docs/adr/036-seal-specification-and-the-trim-stage.md)
>
> **It has a threshold to be measured against, in the unit seal data is quoted in.**
>
> | Measured friction | Consequence |
> |---|---|
> | **≤ 17.8 N** (4.00 %) | **P88** closes, and the trim stage is unnecessary. ADR-033 is amended out |
> | **17.8 – 22.3 N** | The stage is still unnecessary, but the seal does not survive its own heat — **P88 stays open** |
> | **> 22.3 N** (5.00 %) | **The trim stage is needed.** ADR-036 falsifier 1 fires, ADR-033 stands, and **P92** becomes the next run |
>
> **Every published Gen6 dispersion figure descends from A41's 83.4 N ceiling, which is 4.68× the
> specification.** *This is no longer one measurement among several. It is the measurement that
> chooses between two architectures*, and ADR-036 suspended a subsystem rather than guess which.

### P68. ADR-032's first falsifier fires, and the largest piece of the stage credit is a mass P10 says was never itemised: CRITICAL, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HOST_DATA` — a real stage interface: what a provider will actually credit


**[A45](validation/A45_stage_credit.md) bands 4, 5 and 6 failed.** ADR-032 records that the design
is wrong if the 43.33 kg stage credit is optimistic by more than 30 %. **The real break-even is
16.5 %**, and the credit does not survive being read by someone who does not want to believe it.

| | Added mass per satellite |
|---|---:|
| Full credit, as A37 assigned it | **1.403 kg** |
| **Removing the P10 lump alone** | **2.069 kg** — *crosses* |
| Hostile reading of all seven items | **3.108 kg** — *crosses by 55 %* |

**Two of the three findings do not depend on anyone's judgement.**

**The break-even is arithmetic.** With A43's store settled at 5.38 kg, the credit may fail by
**7.17 kg** before added mass per satellite reaches 2.0 — **16.5 %, not 30 %.** ADR-032 was not
wrong when written; it predates A43. It is wrong now, and it is the number a reviewer checks first.

**The biggest item in the credit is one this repository already calls unmodelled.** The 8.00 kg
*enclosure, radiator and packaged avionics* line is **P10** — no line items in
`mass_properties.py`, and the dry mass recorded as *a floor, not a total*. **Crediting it to the
stage converts an admitted unknown into a saving.** At **18.5 % of the credit against a 16.5 %
break-even, that one line fires the falsifier on its own**, with no hostile reading required.

> ### Re-run at A56's store, 2026-08-20 — [A45-R2](validation/A45R2_stage_credit_resized_store.md). **Still CRITICAL.**
>
> **Every number above descends from A43's 5.38 kg store.** [A56](validation/A56_reservoir_resized.md)
> sized the store at ADR-034's charge pressure rather than scaling it and got **3.1216 kg — 42 %
> lighter** — and nothing that depends on it had been re-run.
>
> | Store | Source | kg/satellite | Hostile | Break-even |
> |---:|---|---:|---:|---:|
> | 5.3800 | A43, from a 9.55 L reservoir | 1.4027 | 3.2709 | **8.4 %** |
> | 4.1000 | ADR-034, gas-ratio scaled | 1.2961 | 3.1642 | 9.9 % |
> | **3.1216** | **A56, sized** | **1.2145** | **3.0827** | **11.0 %** |
>
> **A45-R found that the allowance never moves and only the credit does. This is the exception** —
> and it is the only lever the design has. **Sizing the store bought 2.6 points of break-even.**
> *ADR-032 declared 30 %.* **The falsifier fires by less and it still fires.**
>
> **A 42 % lighter store moved the hostile reading by 5.7 %.** *The store is not what is wrong with
> the mass case.* The enclosure is still **58.6 %** of the credit, crediting it alone still gives
> **5.384 kg per satellite**, and the largest single loss is still the skins at 4.92 kg.
>
> **Two figures in this entry are superseded**: **1.403 → 1.2145** and **3.108 → 3.0827**. **And the
> 16.5 % quoted below is against the 43.33 kg credit [A46](validation/A46_enclosure_buildup.md)
> replaced** — on A45-R's 85.36 kg credit the same allowance reads 8.4 %, and at A56's store 11.0 %.
> *A break-even percentage means nothing without the credit it is a fraction of.*
>
> **This entry does not close.** *A CRITICAL entry improving is not a CRITICAL entry resolved.*

**What this does and does not say.** **A37's band 5 is not edited and its result stands as
declared** — it asked whether the credit closes the criterion on the assignment A37 made, and for
that assignment its answer is right. What fails is the assignment's robustness. **Kill criterion 1
is now crossed on both numerators rather than one**, and the threshold has not moved.

> **Re-run 2026-08-16 as [A45-R](validation/A45R_stage_credit_rerun.md), after A46 closed P10.
> The situation is worse, not better.** Itemising the enclosure removed this entry's sharpest
> argument — a mass never itemised cannot be credited — so every enclosure fraction was re-argued
> upward, to 0.50–0.85 from zero. **The hostile figure still lands at 3.271 kg per satellite**, and
> the break-even **halved again to 8.4 %** because the credit grew to 85.36 kg while the 7.17 kg
> allowance did not. **The five enclosure lines are 58.6 % of the credit**, so the Gen6 mass case
> now rests, majority-wise, on one assumption about somebody else's skin. ADR-032's 30 % threshold
> is wrong by 3.6 times.

**What would close it.** **~~Close P10~~** — done 2026-08-16, and it made this entry worse. That replaces the largest guess in the
credit with a number, and it is computation rather than metal. Until then the honest figure to
publish is the range **1.403 – 3.108 kg per satellite**, not the lower end alone.

### P69. Mass parity with a canisterised dispenser is withdrawn: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — the comparison stands; what changes is what is claimed


**[A21](validation/A21_comparators.md) band 4 failed on 2026-08-16.** The band asked for parity
within 15 %; the ratio is **1.758**.

| | |
|---|---:|
| Deployer mass per 3U satellite | **10.547 kg** |
| Canisterised dispenser class, 3U-equivalent slot | ~6 kg |
| **Ratio** | **1.758** — was 1.062 |

**Nothing about the comparison changed. The rollup did.** [A46](validation/A46_enclosure_buildup.md)
replaced P10's 8.00 kg enclosure placeholder with 50.04 kg of derived line items, and parity did
not survive it.

**The band is not widened.** It was declared before `comparators.py` existed and it stands as
declared; what changes is that VOLLEY now fails it.

**This costs the project one of its two surviving competitive arguments.** `LANDSCAPE.md` led with
*"a magazine-fed electromagnetic launcher lands in the same mass class as a canister of springs"*,
and it no longer does — it is **1.76× heavier per satellite**, and against a cold-gas module on the
satellite it is about **12×**. **The argument that survives is the commanded differential**: a
spring's designed differential between satellites is exactly zero, which is categorical rather than
a ratio, and no mass correction touches it.

**What would close it.** Either a lighter enclosure — the honeycomb sandwich A46 costed at 29.98 kg
would give **8.87 kg per satellite**, ratio 1.48, still failing — or a smaller payload class, which
`PAYLOAD_CLASSES.md` and **P59** already identify as the only route that moves this criterion at
all. **No enclosure change reaches parity.**

### P70. The register classifier read a status keyword out of a title: LOW, CORRECTED 2026-08-16
> **Status:** `CLOSED` — resolved; see the entry for what closed it


**P69 was classified `CLOSED` on the day it was opened.** Its heading reads *"Mass parity with a
canisterised dispenser **is withdrawn**: HIGH, NEW 2026-08-16"* — and `CLOSED_RE` matches
`WITHDRAWN` anywhere in the heading. **The claim was withdrawn. The defect was not.**

**This is the third time the same mistake has been made in this one tool**, and the pattern is now
clear enough to name: **it keys on a word appearing anywhere rather than on where status actually
lives.**

| | |
|---|---|
| First | `\bRESOLVED\b` matched inside *depth-resolved* |
| Second | the classifier read back its own written `Status:` line and latched its own verdict |
| **Third** | a status keyword used as ordinary English in a title |

**Corrected.** An entry is titled `<what is wrong>: <STATUS>, <date>`, so the close scan now reads
the **status suffix after the final colon** rather than the whole heading. One entry reclassified —
**P69, CLOSED → LIVE** — and the live count goes 41 → 42. No other entry moved.

**Found by cross-checking the register against the GitHub issue list**, not by any check here. The
tool cannot detect a misclassification, because a wrong verdict is a well-formed one.

### P71. Every generated Gen5 sled had both rollers outside their channels: MEDIUM, CORRECTED 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by building the same machine a second time, in a different CAD kernel, and comparing.**

`cad/build_gen5.py` placed the sled rollers with `Workplane("XZ").circle(r).extrude(rw)` and a
`sgn*ry - rw/2` offset, as though the extrude were symmetric about the plane. **It is not —
`Workplane("XZ")` extrudes towards −Y** — so the offset moved the roller instead of centring it.

| | y extent | Its channel |
|---|---|---|
| **+y roller** | **54.0 → 70.0** | 70.0 → 86.0 |
| **−y roller** | **−102.0 → −86.0** | −86.0 → −70.0 |

**Neither roller was in its channel.** One sat entirely inboard, in the stator gap; the other
entirely outboard. **The sled was asymmetric about y = 0**, which a machine symmetric by
construction cannot be, and `roller_y_inner` / `roller_y_outer` had no effect on the result.

**Corrected.** `extrude(rw/2, both=True)` translated to `sgn*ry` gives 70.0 → 86.0 and
−86.0 → −70.0. Gen5 STEP and STL regenerated; `build_gen5.py --check` passes, as it did before —
**the check verifies extents and station positions, and a part in the wrong place inside an
unchanged overall envelope passes it.**

**What it does not change.** No number moves. `mass_properties.py` takes the sled at **9.445 kg
from the Gen3 solids** (P15), not from Gen5, and nothing in `analysis/` reads a Gen5 STEP. This is
a geometry defect in a published model, not a performance correction.

**What it does change** is what the published Gen5 STEP showed: a sled that could not run in its
own track. Anyone importing it to check clearances would have found the rollers fouling the stator
on one side and outside the longeron on the other.

**Why no check here caught it.** Every guard in this repository compares a generated artifact
against `parameters.json` or against a rebuild of itself. **Both agreed, because both descend from
the same script.** `parameters.json` had been checked against exactly one model built from it since
the geometry was written. A second implementation is the only thing that could have found this,
and it found it on the first run.

### P72. The published renders advertised a velocity withdrawn twice: MEDIUM, CORRECTED 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by asking why a new render looked unlike the published set.**

`cad/tools/prepare_renders.py` hardcoded **"16.388 m/s"** in three places — the hero caption, the
arrow label, and the text-width measurement that positions it. It stayed there through
[ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md), which moved exit velocity
**16.388 → 16.029**, and through the propagation that corrected every document around it.

**So the most-viewed artifact in this repository advertised a figure the repository had already
withdrawn twice, on the front page, while every sentence beside it was right.**

**No propagation could have caught it.** `tools/propagate_baseline.py` and its successors walk
prose; this number was baked into a PNG, and **nothing in `tools/` reads an image.** It is the same
blind spot as **P43** — a picture being wrong about the thing it depicts — and the same class as the
GitHub About text, the published wiki and the issue tracker: **a surface that is published from
here but not readable from here.**

**Corrected.** The value is now read from `analysis/results/motor_results.json` at render time, so
the annotation cannot diverge from the shot it describes. The set is regenerated from the
uncropped frames in `cad/renders/source/`, which is why regenerating was possible at all.

**What it does not fix.** These remain **Gen4** frames — geometry no file in `cad/step/` matches,
with an export gate deliberately closed (**P43**). The velocity on them is now current; the
machine in them still is not.

### P73. A35's shares are percentages of a rollup that has since moved: MEDIUM, CORRECTED 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found while drawing the architecture evolution on the front page, by trying to put two of A35's
figures in one sentence and noticing they had different denominators.**

[A35](validation/A35_constraint_ledger.md) attributed every kilogram of the ledger to the
requirement causing it and published the result as **percentages of dry mass** — the pulse at
**28.1 %**, the mover at **13.6 %**, and **88.67 kg, 70.06 %,** surviving every deletion (**P95**; A35 published 49.23 kg at the pre-A46 dry mass).
[A46](validation/A46_enclosure_buildup.md) then moved the rollup from **84.53 to 126.56 kg**.

**Every one of those percentages fell without a single kilogram moving.**

| Requirement | Attributed | Share of the old rollup | Share of the new |
|---|---:|---:|---:|
| **C3**, the energy arrives during the shot | **26.35 kg** | 28.1 % | **20.8 %** |
| **C2**, a reusable mover carries the magnets | **11.54 kg** | 13.6 % | **9.1 %** |
| C5, the deployer carries its own store | 6.50 kg | — | 5.1 % |

**The argument is unharmed and slightly stronger.** The pulse is still the largest single driver
and still the reason Gen6 exists; the ratio it beats the mover by went from **2.07× to 2.28×**.
What is wrong is only the *form* the result was published in.

**Corrected.** Where this is being newly written, the front page quotes **kilograms**, which are what
A35 measured and which do not move when the denominator does.

**Not rewritten where it is a record.** [ADR-032](docs/adr/032-gen6-stage-integrated-gas-store.md)
and `docs/VAULT.md` keep the percentages they were decided against, each now annotated with the
rollup they were computed at. A decision records the numbers it was taken on.

**The general lesson, and it is not specific to A35.** *A share is two numbers pretending to be
one.* Any figure published as a percentage of a rollup goes stale when the rollup moves, silently,
without the analysis being re-run and without any check firing — `make_baseline.py` guards the 23
values it knows, and a derived percentage sitting in prose is not one of them.

### P74. No Fusion document is committed for any generation built in Fusion: MEDIUM, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — export the Fusion documents, or declare Gen5 the only geometry -- D8


**Found by building the generation archive and filling in a "source document" row six times.**

Four generations were built in Fusion — Gen1, Gen2, Gen3 and Gen4 — and **not one `.f3d` is
committed anywhere in this repository.**

| | Committed | Source |
|---|---|---|
| Gen1 | 11 STEP | Fusion hub. **Not here** |
| Gen2 | 9 STEP | Fusion hub. **Not here** |
| Gen3 | 10 STEP, 2 STL | Fusion hub. **Not here** |
| **Gen4** | **nothing at all** | Fusion hub. **Not here** |
| Gen5 | 8 STEP, 8 STL | `cad/build_gen5.py`, **here** |
| Gen6 | 6 STEP, 6 STL | `cad/build_gen6.py`, **here** |

**STEP is a result of the model, not the model.** It carries geometry and no parameters, no
sketches, no constraints and no feature tree, so a STEP export cannot be edited back into the
design it came from. **For Gen1–Gen3 the repository holds the output and not the source; for Gen4
it holds neither.**

**This is a single point of failure outside version control.** `cad/parameters.json` opens with a
warning that Fusion user parameters are document-scoped and *"will silently drift across the nine
documents"* — and the documents that would let anyone check that are not in the repository. **If
the Fusion hub is lost, Gen1 through Gen4 are lost with it.**

**Gen5 and Gen6 do not have this problem, and that is the entire argument of
[ADR-026](docs/adr/026-cad-built-from-parameters.md).** Their source is a script here, and their
geometry is a function of a parameter file that is also here.

**What would close it.** Export each Fusion document as `.f3d` and commit it, largest first: Gen4,
because nothing of it exists here at all, then Gen3, because every mass in the project descends
from its solids. **This cannot be done from inside the repository** — it is a manual export from
Fusion, and no tool here can perform or verify it.

**What it does not affect.** No number moves. This is an archival gap, not a technical error, and
the exports that do exist have not been shown to be wrong.

### P75. Gen6 improves reliability incidentally, and E30 is not answered by it: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — a Gen6 reliability architecture, the way A47 did Gen5


**[A47](validation/A47_gen6_fmea.md) scored Gen6 on Gen5's own model, imported unchanged.**

| | Elements | Manifest-forfeiting | Required *r* | Delivered at *r* = 0.99 |
|---|---:|---:|---:|---:|
| Gen5 | 13 | **9** | 0.99326 | **6.620** |
| **Gen6** | 12 | **8** | 0.99252 | **6.992** |
| Gen6 + per-cell ejector | 8 | **3** | 0.98388 | **9.261** |
| *a spring dispenser* | 12 | **0** | — | **11.880** |

**ADR-032 deletes six of the nine and the count falls by one.** It adds the reservoir, both
valves, the piston and seals, and the chamber — **and one Gen5 never had at all: a host stage kept
alive past passivation, which no launch provider has agreed to and which forfeits the manifest
exactly as a bank failure did.**

**The failure modes changed discipline. The structure barely moved.**

**The number that matters is the comparison, not either figure.** An entire architecture change is
worth **+0.37 satellites**. A spring in every cell is worth **+2.27** — **six times more** — because
deleting subsystems changes the *count* of shared elements and a per-cell mechanism changes the
*structure*.

**E30 says the architecture trades twelve parallel one-shot mechanisms for one twelve-cycle series
mechanism. Gen6 is still one twelve-cycle series mechanism.** The criticism stands against it
essentially undiminished, and **this entry exists so that is written down rather than assumed
away by an architecture change that did not address it.**

**What would close it.** Design the per-cell ejector — mass, volume, its own failure rate, and
whether it fits the cell the magazine already uses. **Zero manifest-forfeiting elements is not
available to any architecture sharing a magazine**, so the target is the ejector's +2.27, not a
spring's 11.880.

### P76. A48 band 5 compared a charging budget against an instantaneous power: LOW, CORRECTED 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**My declaration error, recorded as one.** [A48](validation/A48_trim_stage.md) band 5 required the
trim stage's peak electrical power to stay inside **200 W**, citing A37. **A37's 200 W is a
*charging* budget** — power drawn from the host across a sixty-second indexing window. **The trim
stage's figure is instantaneous mechanical power during a 1.4 ms correction.** Different
quantities; the comparison was never meaningful.

**The band was also unreachable by construction, which I should have seen before declaring it.**
At 29 m/s, power is force times velocity. 200 W needs **6.9 N**, and delivering 37.7 J at 6.9 N
takes **5.5 m** — longer than the 2.18 m stroke. **No trim stage of any design could have passed
it.**

**Corrected.** The band stands as failed and is not edited; what is corrected is the record of
why it was wrong. Precedent: A40 band 1, where the same class of error was logged the same way.

**What survives is the real finding underneath it.** The trim stage is **pulse power** — 37.7 J at
**28 kW** — which is requirement **C3**, *the energy arrives during the shot*, at 1/50th of Gen5's
energy. Whether that store weighs grams or kilograms **is not answered by A48**, because pulse
hardware scales with current rather than energy. That is the question that decides the idea and it
needs its own bands.

### P77. The trim stage is adopted with its pulse store unweighed: HIGH, CORRECTED 2026-08-19
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[ADR-033](docs/adr/033-gen6-trim-stage.md) falsifier 1, recorded here so it is a defect and not
only a caveat inside a decision.**

The trim stage corrects **±0.323 m/s** for **37.7 J**, delivered over **39.7 mm** in **1.4 ms** —
which is **28 kW**. That is requirement **C3**, *the energy arrives during the shot*, the one A35
prices at **26.35 kg** and ADR-032 deleted.

**At a fiftieth of Gen5's shot energy. But pulse hardware scales with current, not energy**, and
the current is set by the 948 N the section develops, which is Gen5's sheet current. **Nothing
has weighed the store, the switch or the conductors.**

| | |
|---|---:|
| Trim section, weighed | **0.340 kg** |
| Pulse store feeding it | **unweighed** |
| `cad/parameters.json` → `gen6_trim.pulse_store_kg` | **null**, deliberately |

**Why this is a defect rather than a to-do.** [A39](validation/A39_store_trade.md) chose gas over
a spring while assuming 50 bar held at the piston throughout — **a regulator it never named** —
and [A40](validation/A40_blowdown_transient.md) killed that implementation at **14.16 m/s against
a 30 m/s band**. **Adopting a store before pricing its hardware is a mistake this project has
already made once**, and ADR-033 makes it knowingly because the claim is being made now.

**What closed it.** [A54](validation/A54_pulse_chain.md) sized the pulse chain on 2026-08-19 and
**it exceeds the section it feeds by 19 to 30 times.**

> **Corrected.** Priced as an EDLC bank from A10's ESR × C bracket, sized so its ESR takes at most
> 10 % of the delivered energy: **23.44 to 37.36 kg against the 1.2328 kg section**, holding
> **723× to 1152×** the energy the correction needs. **The store is power-limited, not
> energy-limited**, exactly as this entry alleged.
>
> **The requirement A55 resized it to is 136.59 J at 28 606 W — 93.3 % of the peak power and
> 93.3 % of the peak current of the whole chain ADR-032 deleted.** The energy fell twenty times
> and the current fell seven percent.
>
> **No sheet current rescues it**: the section/store trade bottoms out at **10.755 kg**, 5.4× the
> band. **Every figure is a lower bound** — the switch and the conductors are still unpriced.

**This entry closes and [P86](OPEN_PROBLEMS.md) opens in its place**, because what remains is not
"weigh the store" but "decide what to do now that it is weighed" — and that is the owner's, between
finding a **23.2 kW/kg** store, shortening the stroke, or withdrawing the stage.

**And the cheaper outcome still stands.** **P67** — measure the seal friction. If it is small, the
dispersion the stage exists to correct is not there, and neither the stage nor its store is needed.

### P78. Stroke buys velocity and gentleness together, and makes the worst defect worse: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HARDWARE` — it resolves with P67; the friction share is what is unmeasured


**[A49](validation/A49_design_surface.md) swept the surface A37 never asked about, and found a
better design point — with one cost that lands squarely on the defect that already matters most.**

**The win.** Holding Gen6's exit velocity and spending stroke instead of pressure:

| | Gen6 today | **8 m recommended** |
|---|---:|---:|
| Stroke | 2.18 m | **8.00 m** |
| Charge | 50.00 bar | **22.73 bar** |
| **Peak acceleration** | **25.00 g** | **11.36 g** |
| Gas per shot | 112.3 g | **51.0 g — 54.5 % less** |
| Added mass per satellite | 1.403 kg | **1.296 kg** |

**Fourteen of sixty-three surface points beat the current design on velocity, peak acceleration and
gas simultaneously.** The best on velocity-per-g is 8 m at 25 bar: **30.97 m/s at 12.50 g on 56.2 g
of gas.**

**The cost, and A49 band 6 failed to catch it because I declared the band on backwards reasoning.**

| | 1.3 m | 2.18 m | 8.0 m |
|---|---:|---:|---:|
| Constant-pressure ceiling realised | 91.9 % | 87.2 % | **65.9 %** |
| **Friction share of the shot** | 9.25 % | 9.75 % | **12.90 %** |

**Friction work scales linearly with stroke. Shot work saturates.** So a longer tube gives friction
a growing share of the energy — **9.25 % to 12.90 %** — and **P67**, the seal friction that already
owns 93.4 % of the velocity dispersion, becomes *more* load-bearing as the machine gets longer, not
less.

**Why this is one entry and not two.** The velocity, the gentleness and the gas saving are all the
same physics as the rising friction share: a fixed charge expanding down a longer tube extracts
more work while the pressure falls, and falling pressure is exactly when a constant friction force
costs proportionally more. **The benefit and the cost cannot be separated, and a design point that
takes one takes the other.**

**What would close it.** **P67** — measure the seal friction. At 9.25 % it is a rounding error and
the long stroke is free; at 12.90 % of a shot it is a design driver; and if the real friction is
several times A41's *allowance*, the long-stroke direction inverts. **The same measurement decides
this, ADR-033's trim stage and P77's pulse store.** One bench test governs three open decisions.

### P79. The decay model is optimistic by about two against the runs that raised E28: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — a variable-atmosphere decay model and an independent propagator check


**[A50](validation/A50_campaign_altitude.md) band 1 was declared as a calibration against E28's own
GMAT runs, and it failed.**

| | 350 km satellite lifetime |
|---|---:|
| E28's GMAT runs, observed | **29 and 36 days** |
| `astro.py`, modelled | **70.6 days** |

**Roughly a factor of two, at the altitude where campaign duration actually binds.**

**The cause is a defect this project already carries.** `astro.py` uses a **static** atmosphere.
**P16** records what that cost once before: a uniform density scaling preserves a lifetime *ratio*
by construction, so the invariance claim in the paper's abstract was tested by a sweep that could
not have falsified it. **The same property is now producing durations a real atmosphere does not
support.**

**What it affects.** Every campaign duration in A50 is an **upper bound**, and the honest reading
of that run is *"450 km buys months"* rather than any day count. It does **not** affect A50's Δv
figures, its monotonicity findings, or its central result that spread is nearly
altitude-independent while life is not.

**What would close it.** Re-run the decay model against a variable-density atmosphere — or against
GMAT directly, which is what produced the numbers it disagrees with. **The GMAT runs already
exist**: `validation/gmat/` carries the campaign that stopped early. Until then **E28 stays open**,
and it stays open *because* a model disagreeing with its own evidence is not a closure.

### P80. Gen6's charging power is a spring's, quoted for a machine that has no spring: MEDIUM, CORRECTED 2026-08-16
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[ADR-032](docs/adr/032-gen6-stage-integrated-gas-store.md) states Gen6's charging as
"25 to 131 W, which is solar". It is not Gen6's figure.**

It is `analysis/host_integrated.py`'s **`charge_W_60s = e / 60.0`**, where *e* is **the spring
option's** shot energy — the power needed to wind a spring across a sixty-second indexing window.
**Gen6 has no spring. Its reservoir is filled on the ground to 200 bar and nothing in the
architecture recompresses gas on orbit.**

**[A51](validation/A51_gen6_power.md) computed the real figure from a named component list:**

| | |
|---|---:|
| Electrical energy per shot | **311.76 J** |
| **Average power over the 1200 s cadence** | **≈ 0.26 W** |
| Peak instantaneous | **36.0 W** |
| The claim it replaces | 25–131 W |

**About a hundredth of what was being claimed, and the error was in the conservative direction** —
Gen6 asks the host for far less than the record says, which is unusual enough to note.

**How far it spread.** ADR-032 originally, then repeated on 2026-08-16 in
[ADR-033](docs/adr/033-gen6-trim-stage.md), `docs/GENERATIONS.md`, `docs/LINEAGE.md` and the front
page — **four times in one day, by me, from a source I did not check.**

**Corrected.** Every live occurrence now carries A51's figures; ADR-032 keeps the number it was
decided against with an annotation, as decision records do.

**The lesson, and it is not new here.** *A number inherited from an adjacent analysis is not a
result.* The spring option and the gas option were priced side by side in the same script, and the
wrong column was carried forward. **No check could catch it: both figures are real outputs of a
real run, and only their applicability differs.**

### P81. The backup ejector cannot get the payload out of the tube: HIGH, NEW 2026-08-16
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — an ejector concept that clears the tube on the energy available


**[A53](validation/A53_backup_ejector.md) band 7 failed by a factor of forty, and it takes the
highest-value reliability change in the record with it.**

[A47](validation/A47_gen6_fmea.md) priced a per-cell ejector at **+2.27 satellites** delivered at
*r* = 0.99, against **+0.37** for the entire Gen5 → Gen6 architecture change — **six times more**,
because a mechanism in every cell makes the drive satellite-forfeiting instead of
manifest-forfeiting, which is the only move that touches **E30**.

**A47 priced the effect. A53 designed the thing, and it does not fit the architecture.**

| | |
|---|---:|
| Spring for a clean 1.5 m/s departure | **4.5 J** |
| Pushing the payload 2.18 m along a sealed tube at A41's friction allowance | **181.8 J** |
| **Shortfall** | **40.4×** |
| **At ADR-034's 8.0 m stroke, 2026-08-19** | **667.2 J — a 148× shortfall** |

**In Gen5 the payload sat in an open cell. In Gen6 it is inside a tube with a piston behind it**,
and if the drive is dead something must move both the length of the stroke.

> **[ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) made this worse by 3.67×, 2026-08-19.**
> The stroke is now **8.0 m** and the friction work to traverse it is **667.2 J**. The masses below
> are the 2.18 m case and are no longer the governing ones. **A53 has not been re-run**, and at
> 8.0 m the "clearing the tube" row cannot plausibly stay under the threshold. *The two unpriced
> escapes — venting the tube, disengaging the piston — are now the only routes this entry has.*

**Sizing the spring to actually do that costs the mass argument:**

| | × 12 | Added per satellite |
|---|---:|---:|
| Clearance only — *cannot clear the tube* | 1.620 kg | 1.538 kg |
| **Clearing the tube** | **8.713 kg** | **2.129 kg — crosses the 2.0 threshold** |

**So the change is either ineffective or it re-crosses the one kill-criterion numerator Gen6
currently passes.**

> ### The energy verdict is withdrawn, 2026-08-20 — [A65](validation/A65_pyrotechnic_ejector.md)
>
> **A53 closed this as architectural. It was a store choice.** *The same mistake A54 made about the
> pulse store, and [A64](validation/A64_pulse_store_technology.md) corrected the same way — by
> changing technology class rather than design.*
>
> **A solid-propellant gas generator of the automotive restraint class delivers 2331.6 J** at the
> smallest charge in the published range, **after** being cooled to the tube's own 473 K material
> ceiling. **Against 667.2 J needed: 3.49×, where the spring was short by 148×.**
>
> **And the mass argument inverts.** A53's tube-clearing spring re-crossed the kill criterion at
> **2.129 kg per satellite**. The pyrotechnic version is **1.6496 kg** — *under it, with 0.35 kg to
> spare* — and A47's re-run still returns **9.261 satellites**.
>
> **What remains open is 185 g, not an architecture.** A65 band 4 missed A53's inherited 0.25 kg
> per-cell threshold at **0.4350 kg**, and **46.6 % of that is a minimum-gauge steel plenum**, not
> the pyrotechnic parts. **That miss is [P91](#p91-a65-band-4-misses-a53s-per-cell-mass-threshold-and-the-mass-is-in-the-pressure-vessel-medium-new-2026-08-20).**
>
> **Unpriced and named, not counted as a pass:** range safety, ordnance handling, shelf life,
> hazard classification for twelve initiators in one magazine, and the fact that **a fired
> generator cannot be proof-tested before flight where a spring could have been.**
>
> **This entry remains open** on P91's mass and on every unpriced cost above.

**What survives, and the distinction matters.** Bands 1 through 6 all pass. **The failure is
architectural, not conceptual** — the ejector works wherever the payload does not traverse a sealed
tube. Two escapes are unpriced: **venting the tube** and **disengaging the piston**.

**And P67 decides this as well.** The 181.8 J uses A41's friction *allowance*, which has never been
measured. At a genuinely small friction the light ejector works and this entry closes. **One bench
test now governs four open decisions** — this, A49's long-stroke design point, ADR-033's trim
stage, and **P77**'s pulse store.

### P82. The Gen6 reservoir is still sized for a charge pressure the design no longer uses: MEDIUM, CORRECTED 2026-08-19
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) dropped the charge pressure from 50 bar
to 22.73 bar and cut gas per shot by 54.55 %. The reservoir did not move.**

`cad/parameters.json` still carries **9.55 L at 200 bar**, which
[A43](validation/A43_reservoir_thermal.md) sized around a thermal argument at 50 bar refills:
conduction through stagnant nitrogen gives a **17 460 s** time constant against a **1200 s**
cadence, so the vessel never warms back up and the no-relaxation figure is the physically right
one. **That argument has to be re-run at the new refill mass before the volume can move.**

| | |
|---|---:|
| Store mass ADR-034 quotes | **≈ 4.10 kg** |
| What it actually is | **[A49](validation/A49_design_surface.md)'s gas-ratio scaling of A43's 5.38 kg** |
| Reservoir scaling factor applied | **45.45 %** |
| Tube mass, which is real and grew | **0.311 → 1.140 kg** |

**Why this matters more than a bookkeeping note.** The reservoir saving is the whole of ADR-034's
mass argument — the tube itself gains 0.829 kg. **If A43 re-run at 22.73 bar does not recover the
saving, ADR-034 buys gentleness and pays mass for it**, and the added-mass-per-satellite figures in
`docs/generations/GEN6.md`, `docs/GENERATIONS.md` and the front page are optimistic by up to
0.829 kg spread over twelve.

**What closed it:** [A56](validation/A56_reservoir_resized.md) re-ran A43 at 22.73 bar with its
bands declared first, and wrote the sized volume into `parameters.json`.

> **Corrected.** **3.460 L, and a store of 3.1216 kg.** Band 1 reproduced A43's 9.550 L and its
> 17 460 s time constant exactly, so the two are the same model at two pressures.
>
> **The reservoir falls further than the gas does** — 63.8 % against 54.55 % — because a lower
> target pressure lets the bottle be drawn further down before it can no longer fill the chamber.
> **A favourable nonlinearity nobody had claimed.**
>
> **So ADR-034's ≈ 4.10 kg was pessimistic, not optimistic.** A sized store comes in **24 % below**
> the scaled estimate, and **falsifier 2 does not fire.** *This entry alleged the mass argument
> might not be there; it is there, with 0.98 kg to spare.*
>
> **And A43's central finding survives the resizing.** Conduction gives **8873 s against the 1200 s
> cadence — 7.39×** where it was 14.55×. A smaller bottle relaxes faster and the margin halves,
> **but the no-relaxation figure remains the physically right end** and is not pressure-dependent
> above 20 bar.
>
> **One new boundary.** Minimum reservoir temperature falls 201.9 → **161.3 K** against A43's
> declared 150 K floor, and at 15 bar it fails at 143.7 K. **The floor sits between 15 and 20 bar**,
> which constrains how far a future design point can lower the charge pressure — relevant to
> **P86**.

### P83. The trim stage's authority was sized against a friction share that has since tripled: HIGH, CORRECTED 2026-08-19
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[ADR-033](docs/adr/033-gen6-trim-stage.md) exists because Gen6 cannot command velocity
open-loop.** [A44](validation/A44_gen6_dispersion.md) measured **1.113 % at 3σ** with **93.4 % of
the variance in seal friction**, and [A48](validation/A48_trim_stage.md) sized a 39.7 mm stator
carrying **±0.323 m/s** to cover it.

**[ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) tripled the term that dominates that
variance.**

| | Gen6 at ADR-033 | Gen6 at ADR-034 |
|---|---:|---:|
| Friction work per shot | 181.8 J | **667.2 J** |
| **As a fraction of shot work** | **9.75 %** | **28.39 %** |
| Trim authority | ±0.323 m/s | **unchanged, and unverified** |

**Neither A44 nor A48 has been re-run.** If dispersion scales with the friction share — which is
what A44's own variance attribution implies — the correction the stage must make grows with it,
and **0.323 m/s may not cover ±3σ at the adopted design point.**

**This is HIGH because of what it feeds.** A48's section length and mass scale with the authority
required, and **ADR-033 falsifier 1 is that the pulse store weighs more than the 0.340 kg stage it
feeds** — a store that has never been weighed at *any* authority. **A larger authority makes the
project's most likely falsifier more likely.**

**What closed it:** [A55](validation/A55_trim_authority.md) re-ran A44 at ADR-034's stroke and
friction, re-declared A48's bands against the result, and **resized the section rather than
confirming it.** **P67 governs the result** — the whole chain still rests on a seal coefficient
measured on nothing.

> **Corrected.** [A55](validation/A55_trim_authority.md) ran on 2026-08-19 and **the allegation
> holds, by more than this entry estimated.**
>
> | | A48 as built | A55, resized |
> |---|---:|---:|
> | 3σ dispersion | 1.113 % | **3.980 %** |
> | Authority | 0.323 m/s | **1.1543 m/s — 3.57× short** |
> | Section | 39.7 mm | **144.01 mm** |
> | Mass | 0.340 kg | **1.2328 kg** |
>
> **The section is resized in `cad/parameters.json` and ADR-033 is amended rather than reversed.**
> Added mass per satellite goes to **1.3987 kg** against an unmoved 2.0 kg threshold, so no
> kill-criterion numerator moves and ADR-034 stands.
>
> **And the falsifier this entry expected to aggravate does not move.** ADR-033's own argument is
> that pulse hardware scales with *current*, not energy — and **peak power goes 27 820 → 28 606 W,
> 2.8 %**, because the force per metre is fixed. The section gets longer, not harder to drive.
> **P77 is not made worse.**
>
> **What replaces this entry is band 9's sweep**: the section crosses a kilogram somewhere between
> a **20 % and a 28 %** friction share, so **P67's bench measurement now sets a section length as
> well as a dispersion.**

### P84. ADR-034 moved the parameter file and the documents, and left the analysis scripts at the old design point: HIGH, CORRECTED 2026-08-19
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**`analysis/precharged.py` still declares `STROKE = 2.18` and `G_CAP = 25.0`.**
[ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) took the stroke to **8.0 m** and the
charge pressure to **22.73 bar**, and propagated that into `cad/parameters.json`, the CAD, the
renders and eleven documents. **It did not propagate into the scripts.**

| Reads the stale constant | Consequence |
|---|---|
| `analysis/gen6_dispersion.py` — `w_net = w - friction_N * pc.STROKE` | **A44's dispersion is computed over 2.18 m.** It is the input to ADR-033's whole justification |
| `analysis/trim_stage.py` — `STROKE = pc.STROKE` | **A48's section length and authority are sized against that dispersion** |
| `analysis/precharged.py::store_mass` | Uses `P_MAX`, the charge pressure at the **25 g** cap — the point ADR-034 replaced |

**A44 and A48 are currently answering a superseded question**, which is the same finding as
**P83** arriving by a second route: P83 says the friction *share* tripled, and this says the
scripts never saw it.

> **Why the checks did not catch it, which is the part worth keeping.** `make_baseline.py --check`
> compares the scripts against **their own outputs**, and `build_gen6.py --check` compares the CAD
> against **`parameters.json`**. **Nothing in this repository compares the parameter file against
> the analysis scripts**, so a design point can move in one and not the other and every gate stays
> green. That is a hole in the verification, not just a stale constant.

**What closed it.** `precharged.py` reads the design point from `cad/parameters.json` rather
than declaring it — ADR-015's *derive, never paste*, which
[`cad/tools/make_scad_params.py`](cad/tools/make_scad_params.py) already cites for the CAD side.
A41's own declared values stay in the file under their own names so **A41 continues to reproduce**;
the Gen6 scripts read the current point. **And a check that fails when the two disagree**, which is
the thing that was actually missing. **Landed with A55 on 2026-08-19.**

**This is a defect in work done three days ago, and it was found by reading rather than by any
gate.** It is recorded here rather than quietly fixed, which is the rule the register exists to
enforce.

> ### A third live instance, found 2026-08-20
>
> **This entry named A44 and A48 as "answering a superseded question" and repaired neither
> script.** `gen6_dispersion.py` — A44's — now has **one leg in each design point**:
>
> | | |
> |---|---|
> | `P_NOMINAL = 50e5` | **hard-coded**, A41's charge pressure |
> | `pc.STROKE` | **live**, and P84's own fix made it 8.0 m on 2026-08-19 |
>
> **So it computes a shot at 50 bar over 8.0 m, which is not a design point this project has ever
> adopted.** Re-run today it returns **1.504 % and 96.3 %** against A44's published **1.113 % and
> 93.4 %** — *and 1.504 is not the corrected number either, because the pressure is still A41's.*
>
> **Nothing surfaced it because the stored artefact was never regenerated.**
> `analysis/results/gen6_dispersion.json` still holds 1.113 %, last written **2026-08-16** with the
> script; `precharged.py` changed underneath it on **2026-08-19**. **`trim_stage.py` band 1 asserts
> against that stored file**, so it passes today and **fails the moment anyone runs
> `gen6_dispersion.py`.**
>
> **This is the hole this entry already identified, one level down.** P84 found that nothing
> compares the parameter file against the scripts and fixed that. **Nothing compares a script
> against the run sheet it produced**, so a dated result can stop reproducing and every gate stays
> green.
>
> **What closed the scripts, 2026-08-20.** `gen6_dispersion.py` now freezes **`STROKE_A44 = 2.18`**
> and `trim_stage.py` **`STROKE_A48 = 2.18`**, the way `precharged.py` freezes `STROKE_A41` — *the
> pattern already existed in this repository and had not been applied here.* Both reproduce their
> run sheets again: **1.1133466932586118 %** and **93.4 %**, and A48 band 3 is back to **1.822 %**
> from the 0.497 % the live stroke had silently made it.
>
> ### The last sentence of this block was wrong when it was written, and is corrected here
>
> It said Gen6's dispersion at ADR-034's design point *"is not known"*. **It was known, and had been
> for a day.** [A55](validation/A55_trim_authority.md) computed **3.9798 %** on 2026-08-19 with its
> bands declared first, and [A61](validation/A61_seal_class.md) reproduced it independently on
> 2026-08-20. **No further run is needed and none should be written.**
>
> **The defect was never a missing number. It was that the number never propagated** — four
> documents still carried A44's 1.113 % as Gen6's, which is what this entry's correction now fixes
> everywhere. *A stale figure with a correct replacement sitting one file away is a worse failure
> than an unknown one, because nothing about it looks unfinished.*

> **Corrected 2026-08-19, with A55.** `precharged.py::design_point()` reads the stroke,
> acceleration and charge pressure from `cad/parameters.json`, and
> **`check_against_parameters()` is the gate that did not exist** — it also verifies that the force
> and acceleration the parameter file records actually follow from the pressure it records, so the
> three cannot drift apart silently.
>
> **A41's own point is frozen as `STROKE_A41` and `G_CAP_A41`, and `main()` asserts A41 still
> reproduces**: 30.54 m/s at 25.00 g on a 4.66 kg store. *A refactor that breaks a dated result is
> worse than a stale constant, so it fails loudly.*
>
> **The consequence was real and is now measured.** A44 and A48 had been answering a superseded
> question for three days; [A55](validation/A55_trim_authority.md) re-ran them and found the trim
> stage **under-authority by 3.57×** — see **P83**.
>
> ### That correction was partial, and the second instance was found the same day
>
> **`analysis/fill_window.py` declared `P_CHARGE = 50e5` and was not touched by the first
> repair** — which is the same defect in a second file, feeding **A42, A43 and A45**. It was found
> while starting [A56](validation/A56_reservoir_resized.md) and repaired the same way, with A42's
> own point frozen as `P_CHARGE_A42` and `V_CHAMBER_A42`.
>
> **The lesson is the one this entry already stated and I did not act on fully: the hole was never
> that one constant was stale. It was that nothing compares the parameter file against the
> analysis.** *Fixing the instance I had in front of me, and closing the entry on that basis, was
> the same mistake at one remove.* **`check_against_parameters()` covers `precharged.py` only, and
> a repository-wide version of it does not exist.***

### P85. Nobody has said what the drive tube is made of, and the two candidates differ by 2.15 kg: MEDIUM, CORRECTED 2026-08-20
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[A59](validation/A59_tube_structure.md) band 9 went looking for the tube's material and could
not find it stated anywhere in this repository.**

| | |
|---|---|
| [`analysis/design_surface.py`](analysis/design_surface.py) | `RHO_AL = 2700.0`, and A49's `tube_kg` is computed from it |
| [`analysis/precharged.py`](analysis/precharged.py) | sizes the chamber — **the same pressure boundary** — at **7800 kg/m³** with a 500 MPa allowable and a safety factor of 2 |
| `cad/parameters.json` | carries `tube_wall_mm` and now `tube_mass_kg`, and **names no material** |
| [`cad/build_gen6.py`](cad/build_gen6.py) | says the wall "is set by handling and by carrying A38's 201.7 N cradle preload — neither of which is modelled here" |

**The difference is larger than everything else A59 computed put together.**

| | Aluminium | Steel |
|---|---:|---:|
| Tube over 8.0 m | **1.140 kg** | **3.294 kg** |
| Tube + the 7 supports A59 found necessary | **1.240 kg** | **3.394 kg** |
| Against A49 band 7's declared 2.0 kg limit | **passes** | **fails by 1.7×** |

**A49 band 7 passed at 1.140 kg. In steel it fails**, and A49 did not know it was choosing.

> **This is not a structural problem and stiffness will not settle it.** A59 found the unsupported
> first mode is **1.67 Hz in aluminium and 1.68 Hz in steel** — E/ρ is nearly identical for both
> metals, so the material buys no stiffness per kilogram. **It is purely a mass and compatibility
> decision, and it has never been taken.**

**What actually decides it.** The tube is a sliding seal bore, so surface hardness, thermal
expansion against the piston, and galling behaviour matter more than modulus.

> ### And [A58](validation/A58_chamber_thermal.md) measured the thermal half on 2026-08-19
>
> **The expansion takes the bore to −35.2 °C every shot, a 62.1 K swing.** Across it:
>
> | | Clearance change |
> |---|---:|
> | **Matched** piston and bore materials | **0.00 µm** |
> | **Dissimilar** — steel in aluminium, or the reverse | **10.79 µm** |
>
> **On a 15.805 mm bore that is a real fraction of any sensible seal clearance, and the repository
> specifies neither part.** A58 band 6 failed on it.
>
> **This is the cheap half of the decision.** Nothing about the mass argument forces the piston and
> the tube to differ, and **matching them removes 10.79 µm for free.** The mass question — 1.140 kg
> against 3.294 — is the one that still needs deciding.

**What closed it:** [ADR-035](docs/adr/035-drive-tube-material.md), 2026-08-20.

> **Corrected. The tube is hard-anodised aluminium and the piston is the same alloy.**
>
> **Only mass discriminated.** A59 found strength (13.9× margin), stiffness (1.67 against 1.68 Hz)
> and buckling (both fail unsupported, both fine at 1.0 m) **indifferent between the metals**, and
> A58 found it is **matching** the piston and bore that removes the 10.79 µm differential, not which
> metal is chosen. **So the decision fell to 2.154 kg — 0.18 kg per satellite against the project's
> tightest threshold.**
>
> **The functional requirement nobody had stated is that the tube is a sliding seal bore**, which
> makes it a surface question rather than a strength one — and **hard anodising is what makes
> aluminium available.** *The duty is far lighter than it looks: the carriage is not recovered, so
> **every seal makes exactly one 8.0 m pass** and the tube sees **96 m across an entire campaign.***
>
> **A49 band 7's 1.140 kg stands, and it now stands on a stated choice.**
>
> **What it costs is steam.** The 473 K ceiling forecloses it — [A63](validation/A63_steam_design_point.md)
> found **none of 108 steam design points reaches it**. ADR-035 falsifier 4 names that, and it is
> the first decision in this project that closes a door rather than opening one.

### P86. The trim stage cannot be fed by any store this repository has data for: HIGH, CORRECTED 2026-08-20
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[ADR-033](docs/adr/033-gen6-trim-stage.md)'s first falsifier has fired, and it fired on the
argument the ADR itself used to name it.**

> *"Pulse hardware scales with current, not energy, and nothing has weighed it. This is the
> falsifier most likely to fire, and it is being adopted before it is answered."*

**[A54](validation/A54_pulse_chain.md) weighed it. One of eight bands passes.**

| | The chain [ADR-032](docs/adr/032-gen6-stage-integrated-gas-store.md) deleted | The trim stage that replaced it |
|---|---:|---:|
| Peak power | 30 674 W | **28 606 W — 93.3 %** |
| Peak current at 96 V | 319.5 A | **298.0 A — 93.3 %** |
| Energy per shot | 2782 J | **136.6 J — 4.9 %** |

**The energy fell twenty times and the current fell seven percent.** ADR-032 deleted a pulse chain
and ADR-033 asked for 93 % of it back.

**Priced as an EDLC bank from [A10](validation/A10_bank_esr.md)'s ESR × C bracket and the 6.50 kg
string `mass_properties.py` carries**, sized so its ESR takes at most 10 % of the delivered energy:

| | |
|---|---:|
| ESR required | **≤ 32.2 mΩ** |
| Capacitance | **21.4 – 34.2 F**, 3.6 – 5.7 strings |
| **Store mass** | **23.44 – 37.36 kg**, against the **1.2328 kg** section it feeds |
| Energy it would hold | **98.7 – 157.3 kJ** for a **136.6 J** correction — **723× to 1152×** |

**And no sheet current rescues it.** Peak power scales with sheet current and section length
inversely, so the trade has a minimum — **the minimum is 10.755 kg**, 5.4× the 2.0 kg band, with
added mass per satellite at **2.4313 kg**, which **re-crosses the one kill-criterion numerator Gen6
passes.**

> **What it proves is narrower than "impossible", and more useful.** Any store that fits inside the
> section it feeds must deliver **23.20 kW/kg** — against the **4.72 kW/kg** Gen5's own bank
> achieves. **4.92× on the axis that binds**, and specific energy is not the constraint at all
> (110.8 J/kg required, against thousands available).
>
> **Every mass above is a lower bound**: the switch and the conductors are not priced and no figure
> for either is in this repository.

> ### Two of the three routes first named here do not exist, checked 2026-08-19
>
> **Raising the bus voltage does nothing.** The store reduces to
> **m ≥ ½·(ESR×C)·P/(f · specific energy)** — **V cancels exactly.** A 300 V bank needs a tenth the
> capacitance at ten times the voltage: same stored energy, same cells, same mass.
>
> **Shortening the stroke does nothing either.** Peak power is force-per-metre × exit velocity,
> force per metre is set by sheet current and the velocity is held — **stroke appears nowhere.** At
> A48's own 2.18 m point the store would have been **22.8–36.3 kg.**
>
> **So ADR-033 was never affordable at any stroke, and this entry is not a consequence of ADR-034.**
> *Both escapes were checked after the run rather than before, which is the wrong order.*

**What the levers actually are.** **ESR × C** — the store technology — needs **≤ 36.3 ms** against
an EDLC's **690–1100 ms**, **19–30× better**, and it is the only lever with that range; a film or
pulse capacitor flips the binding constraint from power to energy and **no figure for either is in
the record.** **Sheet current** bottoms the trade at **10.755 kg**. **P67** takes that to
**6.68 kg** at a 9.75 % friction share, since the total scales as √energy. **The loss budget** gives
7.81–12.45 kg at 30 %, and 41 J of heat per shot. **Or withdraw the trim stage and accept 3.980 %
open-loop** — **which deletes the commanded-velocity claim the product is sold on**, and is the one
route that survives unchanged.

**What closed it:** the source this entry's own title named as missing.

> **Corrected.** **[A64](validation/A64_pulse_store_technology.md), six of six**, priced the store
> against published pulsed-power capacitor technology — **2000 to 2680 J/kg**, metallised
> polypropylene with extended-foil electrodes.
>
> | | EDLC | **Pulsed-power capacitor** |
> |---|---:|---:|
> | Energy needed to *source the current* | 98.7 – 157.3 kJ | **0.14 – 143 J** |
> | Binds on | **power, by 723×** | **energy** |
> | **Store mass** | **23.44 – 37.36 kg** | **0.051 – 0.072 kg** |
> | Specific power | 4.72 kW/kg | **400 – 561 kW/kg** |
>
> **522× lighter, and 17× the specific power A54 said was required. The store is about 70 grams.**
>
> **ADR-033's falsifier 1 does not fire**: the store weighs **6 %** of the section it feeds.
> Added mass per satellite is **1.4047 kg** against an unmoved 2.0 kg threshold.
>
> **A54 was correct in every calculation and wrong in its scope.** It priced an EDLC because A10's
> bracket and the 6.50 kg string were **the only store data in this repository**, and it flagged the
> alternative as NEEDS SOURCE rather than guessing. **The defect was not in the analysis. It was
> that the repository had one technology in it.**

**[A61](validation/A61_seal_class.md)'s route is still cheaper** — a specified seal may *delete* the
trim stage rather than feed it — **but it is no longer the only one.**

### P87. The last fill of the campaign does not fit the window, and never did: MEDIUM, NEW 2026-08-19
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — re-plan the campaign fill schedule against the window


**[A42](validation/A42_fill_window.md) established that filling is *not* the constraint** — 4.14 s
through a 1 mm orifice, against the 10 s of index-plus-return already inside the cadence.

**That is the *first* fill, from a full bottle. Nothing had looked at the last one.**

[A56](validation/A56_reservoir_resized.md) computed the whole twelve-shot sequence and band 7
failed:

| | Last fill |
|---|---:|
| At A43's 50 bar sizing, 9.55 L | **14.391 s** |
| At ADR-034's 22.73 bar, 3.46 L | **11.516 s** |
| Window | **10 s** |

**By shot twelve the bottle is depleted, the pressure ratio across the orifice has collapsed, and
the same hole takes roughly three times as long.** *The resizing improves it — a smaller bottle at
the same storage pressure holds its ratio better — but does not fix it.*

**This is a defect in the fill design rather than in the store sizing, and it is not ADR-034's.**
It was present at A43's point and would have been found by anyone who looked past the first shot.

> **The escape is arithmetic rather than architectural.** [A43](validation/A43_reservoir_thermal.md)
> band 8 measured that the orifice moves the required reservoir by **0.00 %** across 0.5 to 2.0 mm.
> **A larger orifice buys fill time for no mass at all.** What it costs instead is fill-rate
> controllability, which is what commands the charge pressure and therefore the exit velocity —
> and that trade has not been run.

**What would close it:** size the orifice against the *last* fill rather than the first, and check
what the larger hole does to the pressure-setting resolution [A44](validation/A44_gen6_dispersion.md)
depends on. **Neither the cadence nor the store needs to change.**

### P88. The seal cannot absorb its own friction, and P67 is a harder measurement than it has been described as: HIGH, NEW 2026-08-19
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HARDWARE` — the seal's own conduction path, measured


**[A58](validation/A58_chamber_thermal.md) band 5 failed across the whole swept range.**

**667.2 J arrives in the seal in about five milliseconds**, at **2419 W** where it is moving
fastest. Adiabatic rise per shot:

| Seal mass | 0.5 g | 1 g | 2 g | 5 g | 10 g |
|---|---:|---:|---:|---:|---:|
| **Rise per shot** | **889.6 K** | **444.8 K** | **222.4 K** | **89.0 K** | **44.5 K** |

**Only the 10 g end clears 50 K, and only if nothing else is true.** The requirement that follows
is band 8's, and it is the useful part:

> **For a 2 g seal to stay within 50 K, 77.52 % of its friction heat must leave it during the
> stroke.**

**That is a design requirement on a component that exists in no file.** No seal is drawn, no
material is named, and its friction coefficient — the thing generating the heat — has never been
measured. [A39](validation/A39_store_trade.md) states it designs *"no cylinder, valve, seal or
latch"*; [A40](validation/A40_blowdown_transient.md) the same.

### What this does to P67

**[P67](OPEN_PROBLEMS.md) has been described throughout as a bench measurement of a friction
coefficient. It is a harder measurement than that.**

| | |
|---|---|
| **Temperature** | the gas is at **237.9 K, −35.2 °C**, every shot ([A58](validation/A58_chamber_thermal.md) band 1) |
| **Self-heating** | the seal dissipates **667.2 J per stroke at 2419 W peak** |
| **Stroke** | **8.0 m**, not a short rig |
| **Repeats** | **twelve**, and the shot-to-shot spread is the quantity wanted |

**A room-temperature coefficient on a short rig would not answer the question the design asks.**

### And the coupling nobody has modelled

**Friction heats the seal; a hotter seal has different friction; that changes the shot.**
[A55](validation/A55_trim_authority.md) found the seal owns **98.7 %** of the dispersion, so a
thermal-friction loop feeds straight into the one number this architecture is sold on. **A58 names
it and does not compute it.**

**What would close it:** a seal specification — material, section, mass and a conduction path out —
and P67 run at temperature, over a representative stroke, with the spread reported. **Until a seal
exists, the 83.4 N in `gen6_dispersion.py` is an allowance A41 declared rather than a property of
anything.**

### P89. The seal has a specification now, and `parameters.json` still carries no seal: HIGH, CLOSED 2026-08-20
> **Status:** `CLOSED` — resolved; see the entry for what closed it


**[A61](validation/A61_seal_class.md) inverted the question A41 left open.** Rather than asking what
a seal would give, it asked what the loosest seal is that the design can tolerate — **and the answer
is a number, in the unit seal data is quoted in.**

> ### **17.8 N — 4.00 % of the piston's pressure force. The thermal case sets it.**

| Requirement | Maximum friction |
|---|---:|
| **A 2 g seal stays within 50 K** — A58 band 5, **P88** | **4.00 % = 17.8 N** |
| The trim stage becomes unnecessary — below A48's ±0.323 m/s | 5.00 % = 22.3 N |
| Section + store ≤ 2.0 kg — A54 band 5, **P86** | **not reachable at any friction** |

**A61 band 6 failed, and that is the finding: the binding requirement on this component is not the
control loop, it is that the seal must survive its own friction.**

### What the design has actually been assuming

**A41's 83.4 N allowance is 18.71 % of the pressure force**, which A61 band 2 confirmed sits inside
the **elastomer O-ring** range. **The project has been sized since A41 against the worst common seal
class, and nobody ever chose it.** [A55](validation/A55_trim_authority.md)'s dispersion,
[A54](validation/A54_pulse_chain.md)'s store, [A58](validation/A58_chamber_thermal.md)'s seal
heating and [A49](validation/A49_design_surface.md)'s band 6 failure all descend from it.

**The specification is 4.7× tighter than the allowance.**

### What meeting it would do

| | A41's allowance | At 5.00 % |
|---|---:|---:|
| Friction work per shot | 667.2 J | **178.4 J** |
| **3σ dispersion** | **3.9798 %** | **0.9051 %** |
| Authority needed | 1.1543 m/s | **0.2982 m/s** |
| 2 g seal rise | 222.4 K | **59.5 K** |

**P88 closes at 4.00 %. P86 becomes deletable at 5.00 %** — the trim stage is unnecessary rather
than affordable. **But A61 band 5 found no friction in 1–30 % makes the store itself affordable:
4.23 kg even at 1 %.** *Seal choice cannot solve P86; it can only make it irrelevant.*

> ### Closed 2026-08-20 by [ADR-036](docs/adr/036-seal-specification-and-the-trim-stage.md)
>
> **`cad/parameters.json` now carries a `gen6_seal` group.** It holds **both** numbers and says
> which is which: **`friction_max_N` 17.8 as the specification**, and **`friction_allowance_N`
> 83.40371375447981 as A41's retained ceiling** — *4.68× apart, with every published Gen6
> dispersion figure descending from the ceiling rather than from the specification.*
>
> **The allowance was not deleted and that is deliberate.** [P67](#p67-gen6s-precision-rests-on-a-seal-friction-nobody-has-measured-and-its-rated-velocity-excludes-it-high-new-2026-08-16)
> has measured neither, so the ceiling remains the only honest number for a worst-case argument.
> **`measured` is recorded in the group as `NO`.**
>
> **What this entry asked for is done: the specification is a design parameter rather than a
> finding in a run sheet.** *What it does not do is make the number true* — and ADR-036 turns that
> into a decision by suspending the trim stage rather than building or deleting it.

> ### The specification is fluid-dependent and A61 did not say so
>
> **[A62](validation/A62_steam_working_fluid.md), 2026-08-20**, found the seal specification only
> holds for the fluid it was computed against. **A61 assumed the seal runs at −35 °C, which is what
> cold nitrogen gives.** A steam working fluid needs **550 K** to keep its expansion dry, and at
> that temperature **filled PTFE is past its 533 K limit** — so the 17.8 N figure would not survive
> a change of working fluid.
>
> **The specification is therefore conditional on the gas, and that condition belongs in it.**

**What would close this entry:** a seal in `cad/parameters.json` — section, material class, mass, a
friction figure **and the temperature range it is specified at** — and **[P67](OPEN_PROBLEMS.md)
measured against the 17.8 N specification rather than against nothing.** *A61 measured nothing and
names no product; its class ranges are handbook and flagged as such.*

### P90. A62 screened steam at nitrogen's design point, not at steam's: HIGH, CORRECTED 2026-08-20
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[A62](validation/A62_steam_working_fluid.md)'s conclusion does not hold, and the defect is in how
the run was set up rather than in anything it computed.**

**Every figure in A62 was computed at a 2.0 L chamber** — the volume [A41](validation/A41_precharged_chamber.md)
sized for **cold nitrogen**, carried into `cad/parameters.json` and then into a run about a
different fluid. **The chamber was never re-optimised for steam, and it is the variable steam is
most sensitive to.**

| Chamber | Expansion ratio | **Temperature to stay dry** | Work |
|---:|---:|---:|---:|
| 2.0 L — **A62's, and A41's** | 0.5603 | **550 K** | 2397 J |
| 4.0 L | 0.7182 | **523 K** | 2851 J |
| 8.0 L | 0.8360 | **508 K** | 3163 J |
| 20.0 L | 0.9272 | **498 K** | 3392 J |

**A larger chamber lowers the dry temperature and raises the work at the same time.** The floor is
**T_sat(p₀) itself — 492 K at 22.73 bar** — approached from above.

### What that does to A62's verdict

**A62 band 7 failed because 550 K exceeds filled PTFE's 533 K limit, and that failure was the
reason [A61](validation/A61_seal_class.md)'s seal specification was said not to survive steam.**

**At 4.0 L the charge is 523 K — inside PTFE's limit — and the shot delivers 2851 J and 37.75 m/s
against nitrogen's 2350 J and 34.28.** *More work, more velocity, and the seal specification holds.*

**Band 8's net −1.285 kg is equally suspect**: it charged a steel tube against a store saving
computed at the wrong chamber, and did not count the chamber growth a larger volume costs.

### What still stands

**Band 4's aluminium limit.** Every point found so far sits above **473 K** — the best is 478 K at
16 bar and 32 L — so **the tube is steel regardless**, and P85 keeps its heavy answer. *That part of
A62 survives its own correction.*

**And the heating.** Bands 5, 6 and 9 are about the sun, not the design point: **α/ε ≥ 7.6, a 23 cm
absorber, and it survives eclipse.** Those hold at any chamber.

**What closed it:** [A63](validation/A63_steam_design_point.md) swept 108 points with its bands
declared first.

> **Corrected.** **A62's seal failure was an artefact and is withdrawn** — 43 points sit inside
> filled PTFE's limit, so **A61's specification survives steam.**
>
> **A62's aluminium failure was not** — **zero of 108 points reach 473 K**, because the floor is
> T_sat(p₀) and every charge pressure that makes 2350 J sits above it. **The tube is steel at every
> steam design point.**
>
> **And that settles the verdict A62 reached for the wrong reason.** The steel penalty is
> **2.154 kg — larger than everything steam removes** — so the best point is **−1.813 kg** and
> **none of the 43 is a saving.** *The correction made it worse than A62 found, because a chamber
> chosen for steam is larger and chamber mass rises with it.*
>
> **One conditional survives, and it is not a mass argument.** If **P85** chooses steel for reasons
> independent of the fluid — hardness and galling at a sliding bore, and A59 found the material
> barely moves the beam mode — steam stops paying for the tube and becomes **+0.341 kg**. *That is
> less than the absorber hardware A63 charges nothing for.*

### P91. A65 band 4 misses A53's per-cell mass threshold, and the mass is in the pressure vessel: MEDIUM, NEW 2026-08-20
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — a pressure vessel design that meets A53's per-cell mass


**[A65](validation/A65_pyrotechnic_ejector.md) band 4 failed at 0.4350 kg against 0.25 kg.** Nine of
its ten bands passed, including the one that governs — **1.6496 kg per satellite against the 2.0 kg
kill criterion** — so this is a numbered band miss, not a dead architecture.

| Per cell, smallest charge in the class | | |
|---|---:|---:|
| Solid generant | 0.0200 kg | 4.6 % |
| **Plenum pressure vessel** | **0.2025 kg** | **46.6 %** |
| Heat sink to the 473 K tube ceiling | 0.0926 kg | 21.3 % |
| Housing, initiator, gas path — **declared guess, no derivation** | 0.1200 kg | 27.6 % |
| **Total** | **0.4350 kg** | |

**The pyrotechnic parts are not what fails the band.** The generant is 20 g and the sink is 92.6 g.
**The vessel is 202.5 g and it is minimum-gauge limited, not pressure limited**: at 0.3933 L the
hoop wall the pressure needs is **0.909 mm** against `precharged.chamber_kg`'s **1.0 mm** floor, and
that function builds in steel at 7800 kg/m³.

**Three routes exist and none has been run:**

1. **The vessel material.** The same shell in the aluminium [ADR-035](docs/adr/035-drive-tube-material.md)
   chose for the tube is **70.1 g**, taking the cell to **0.3031 kg** — *still over, so this alone
   does not close it.*
2. **The housing guess.** 0.1200 kg is carried from A53 unchanged with **no derivation**, so that
   the two runs compare. It is the largest unexamined term left.
3. **The threshold itself.** 0.25 kg is A53's band 1, **set for a spring**. It is a proxy for the
   2.0 kg per-satellite kill criterion, which A65 passes. *A band is never widened after a result
   is known — but a new run may declare its own threshold, argued from the criterion rather than
   inherited from a different device.*

**What would close it:** a run declaring its bands first that brings the cell under a threshold it
argues for, with the vessel material and the housing allowance both derived rather than assumed.

### P92. The trim stator has to reach its magnets through a conducting tube, and nothing has computed what that costs: HIGH, NEW 2026-08-20
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — A66: the tube attenuation, induced loss and wall temperature


**[ADR-033](docs/adr/033-gen6-trim-stage.md) puts the stator outside the tube and the magnets
inside it.** `cad/build_gen6.py` draws the section as an annulus running from `bore/2 + wall` to
`bore/2 + wall + 6.0`, and the ADR's own words are *"a magnet set carried by the carriage"*. **The
travelling field therefore crosses the drive tube on its way to the thing it acts on.**

**[ADR-035](docs/adr/035-drive-tube-material.md) made that tube aluminium on 2026-08-20**, four days
after ADR-033 was adopted. **A conducting sleeve between a travelling-field stator and its secondary
is a shorted turn**, and **no file in this repository computes the attenuation, the induced loss, or
the heating.**

| | |
|---|---|
| `gen6_drive.tube_wall_mm` | **1.0 mm** |
| `gen6_drive.tube_material` | **aluminium 6061-T6, hard anodised** |
| `stator.pole_pitch` | **24 mm** |
| Carriage speed through the section | **34.28 m/s**, `exit_velocity_m_s_zero_friction` |
| Aluminium conductivity already in the repository | **3.5 × 10⁷ S/m**, `analysis/phase1_closeout.py` |

**Every input exists and the calculation has never been done.** The governing comparison is the wall
thickness against the skin depth at the excitation frequency the pole pitch and the carriage speed
set between them.

### Why this was not caught

**Three runs examined this tube in 2026 and none of them looked at it electromagnetically.**
[A59](validation/A59_tube_structure.md) took it structurally and found the metals barely
distinguishable. [A58](validation/A58_chamber_thermal.md) took it thermally. [A61](validation/A61_seal_class.md)
took it tribologically. **ADR-035 then chose on mass alone** — and mass was the right tie-breaker
among the questions that had been asked.

> **The defect is in the sequencing, not in any one decision.** ADR-033 chose where the stator sits;
> ADR-035 chose what stands between it and its magnets; **and no document owns the interaction.**
> *ADR-033's cost table lists what the magnets bring back — P34, E35, the cradle, a velocity sensor,
> one more shared element — and the tube is not on it, because when that table was written the tube
> had no stated material.*

**What would close it:** a run with its bands declared first, comparing the 1.0 mm wall against the
skin depth at the section's own excitation frequency, and reporting the thrust attenuation, the
induced loss and the resulting wall temperature against **ADR-035's 473 K ceiling**. If the
attenuation is material, [A55](validation/A55_trim_authority.md)'s **1.1543 m/s** of authority and
[ADR-033](docs/adr/033-gen6-trim-stage.md)'s **28 606 W** are both optimistic, and the section grows
again — which is **P83**'s failure mode a second time.

**A cheaper answer may exist and is not this entry's to choose:** a non-conducting liner, a slotted
or non-conducting section of tube local to the stator, or the passive-secondary route
[`docs/VAULT.md`](docs/VAULT.md) records under **PII-19**, which removes the magnets from the moving
part rather than reaching them through metal.

> ### Deferred, not dropped, 2026-08-20 — [ADR-036](docs/adr/036-seal-specification-and-the-trim-stage.md)
>
> **A66 is not being written yet, and the reason is not that this entry got smaller.**
> [A61](validation/A61_seal_class.md) band 3 showed that a seal meeting its own **thermal**
> requirement makes the trim stage unnecessary, so **ADR-036 suspends the stage** rather than
> building or deleting it. *Computing how well a stator couples through a conducting tube is only
> worth doing for a stator that is going to exist.*
>
> **This entry stays LIVE precisely so that it is not forgotten.** If **P67** measures friction
> above **22.3 N**, the stage is needed, and **A66 becomes the next run with nothing else in front
> of it.**

### P93. The paper's system mass is 50 % low, in the abstract, and A46 never propagated into it: CRITICAL, CLOSED 2026-08-20
> **Status:** `CLOSED` — resolved; see the entry for what closed it


**Found while closing Gen5, which is the only reason it was found at all.**

| Source | Dry mass | Loaded |
|---|---:|---:|
| `analysis/results/mass_properties.json`, and [`BASELINE.md`](docs/BASELINE.md) | **126.6 kg** | **174.6 kg** |
| `paper.tex` **abstract** and **conclusion** | **84.5 kg** | 132.5 kg |
| `paper.tex` **Table \ref{tab:family} caption** | **76.5 kg** | — |

**Three figures for one quantity, two of them in the published deliverable.**

### The arithmetic identifies the cause exactly

**[A46](validation/A46_enclosure_buildup.md) itemised the enclosure on 2026-08-16.** It had been an
**8.00 kg placeholder**; built up from the geometry it is **50.04 kg**.

> **84.5 − 8.00 + 50.04 = 126.54.** The repository says **126.6**.
>
> **And 84.5 − 8.00 = 76.5**, which is the table caption — *the same total with the placeholder
> removed and nothing put back.*

**So both paper figures are pre-A46, and neither is a different scope or a rounding.** The paper
was last built **2026-08-19**, three days after A46 landed. **The correction propagated to
`BASELINE.md`, to the README and to the register, and stopped at the paper.**

### Why this is worse than a stale number

**The 76.5 kg figure is not decorative — it is an input.** The Table caption reads *"Deployer mass
per satellite uses the 76.5 kg dry mass and a packing model calibrated so the 3U case returns the
twelve the magazine is laid out for."* **Every per-satellite mass in the payload-family table
descends from it**, and at 126.6 kg they all move by **65 %**.

**This is therefore a re-run, not a find-and-replace**, and it is recorded as such rather than
patched. *Editing the abstract alone would leave the table inconsistent with its own caption and
the caption inconsistent with the repository — three numbers instead of two.*

### What would close it

**What closed it, 2026-08-20.** *And it was not a re-run — this entry was wrong about its own
cost.* `payload_family.py` **already reads `dry_kg` live**; its docstring records this exact failure
mode — *"It was pasted, at 76.5 kg, and it stayed at 76.5 when mass_properties moved to 84.5"* — and
`payload_family.json` already carried **`deployer_dry_kg: 126.6`** with all nine class rows. **The
analysis was current the whole time. Only the manuscript was stale.**

**And it was worse than this entry described.** Fixing it exposed two things the mass audit had not:

| | |
|---|---|
| **A third stale mass** | The mechanical section also read **84.5 kg** (loaded 132.5, CoG 0.44 m). Now **126.6 / 174.6 / 0.46 m** |
| **The family table was stale in *every* column, not just mass** | Its velocities and accelerations were at the **pre-ADR-030** operating point — the 3U row read **16.4 m/s at 10.5 g** against the paper's own rated point of **16.0 at 10.1**, stated two paragraphs earlier. **The table contradicted its own paper** |
| **And it was internally inconsistent** | Seven rows were 76.5-based; the 3U row alone was 84.5-based. *One row had been updated and the others had not* |

**All eight rows are now regenerated from `payload_family.json`.** 3U reads **10.550 kg/satellite**,
and the *"varies by a factor of thirty across the family"* claim — which is invariant in dry mass and
was therefore always checkable — is corrected to **109×**.

**Both PDFs rebuilt and verified**: `126.6` present, `84.5` and `76.5` absent from both.

> **The audit that opened this entry checked thirteen headline scalars in prose and passed eleven.
> It could not see the table**, because the prose carries 16.0 and the table carried 16.4 — *the
> right number in the wrong place hides the wrong number in the right one.* **`check_paper.py`
> must read tables, not just prose.**

> **The register's own first sentence says P-items are errors in the currently published paper and
> should be fixed first.** This one sat through four passes that touched the paper's companions
> because **nothing compares the paper against `BASELINE.md`** — the same shape of gap as P84, one
> deliverable further out.

### P94. A13 band 5 passes on a host control authority that E5 says does not exist: HIGH, NEW 2026-08-20
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HOST_DATA` — a published control authority for a real stage


**Found by a provenance audit of every module-level constant in the analysis scripts, 2026-08-20.**

`analysis/attitude_budget.py` carried, with no units, no comment and no source:

```python
RCS_TORQUE = 0.1
```

**It is a host reaction-control torque in N·m, and [A13](validation/A13_indexing_disturbance.md)
band 5 passes on it:** *"Settling to below 0.01 °/s with a 0.1 N·m RCS authority — under 2 s at
500 kg."* **The run sheet states the value twice and justifies it nowhere.**

> **And [`EXTERNAL_EVIDENCE.md`](docs/EXTERNAL_EVIDENCE.md) records E5 as:
> *"no host propellant or control authority figure exists."***

**So this project simultaneously records that it has no host control-authority figure, and uses one
to pass a validation band.** *That is not a stale number or a rounding choice. It is a claim resting
on a quantity the register elsewhere declares absent.*

### What has been done, and what has not

**The constant is now labelled a declared assumption in the script**, pointing at this entry and at
E5. **A13 band 5's verdict is not changed and not re-declared** — it is annotated with what it rests
on. *Whether 0.1 N·m is a reasonable authority for a spent stage is a separate question from whether
it was ever declared, and only the second was answerable here.*

**No source was invented.** An assumption that cannot be sourced is labelled as an assumption.

**What would close it:** a published host control-authority figure — the same data exchange **E5**
already names as the one that converts this analysis from parametric to specific — or a re-run of
A13 band 5 as a *required* authority rather than an assumed one, in the shape
[A54](validation/A54_pulse_chain.md) used when it stated a required specific power instead of
guessing a store.

> **The audit that found it was looking for undocumented constants and this was the only genuine
> contradiction in 126.** [A46](validation/A46_enclosure_buildup.md)'s seven assumed enclosure
> inputs — which drive the **50.04 kg** that is **58.6 % of the stage credit** — are every one of
> them declared, and its band 7 says so: *"Every line item traces to a parameter or a declared
> input — zero undeclared."* **The discipline works. This slipped through it.**

### P95. A35's headline survives-everything figure is pre-A46, and correcting it reverses A35's own escape route: CRITICAL, NEW 2026-08-20
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — A35's run sheet against the post-A46 rollup


**Found while drawing the A35 ledger for the front page. The figure would not agree with the text,
and the figure was right.**

`analysis/results/constraint_ledger.json` was **regenerated on 2026-08-16** in the commit *"Apply
A46: the enclosure is 50 kg, and mass parity does not survive it."* `validation/A35_constraint_ledger.md`
**was last touched on 2026-08-14.** *The script ran at the new dry mass and the run sheet was never
re-read.*

| | A35 as published | At the ledger's own current output |
|---|---:|---:|
| Dry mass | 84.59 kg (implied) | **126.56 kg** |
| Survives every deletion in all 64 corners | **49.23 kg — 58.2 %** | **88.67 kg — 70.06 %** |
| Best corner, deleting C2 and C3 | — | removes 37.89 kg, **29.90 %** |
| **Per satellite at twelve** | **4.10 kg** | **7.39 kg** |
| **Per satellite at twenty-four** | **2.05 kg** | **3.69 kg** |

**49.23 / 0.582 = 84.59 kg**, which is the pre-A46 dry mass. **The arithmetic identifies the cause
exactly, the same way it did for [P93](#p93-the-papers-system-mass-is-50--low-in-the-abstract-and-a46-never-propagated-into-it-critical-closed-2026-08-20).**

### The part that is not just a stale number

**A35's section 4 offers the only escape route the whole ledger found:**

> *"At twenty-four satellites the same 49.23 kg is **2.05 kg each, and the criterion closes** — even
> allowing the containment lines to grow with the manifest, it lands near 2.5 kg. **Magazine density
> is the only lever in this run that reaches the criterion.**"*

**At the current ledger it is 3.69 kg each. The criterion does not close at twenty-four.** *A35's
one route out of kill criterion 1 was an artefact of a dry mass that A46 superseded two days later.*

**A35's harder finding is unchanged and is now harder still**: no combination of requirement
deletions closes kill criterion 1 — and the irreducible remainder is **1.8× larger** than published.

### Where the stale pair is quoted

**`README.md`, `docs/GEN5_CLOSURE.md`, `docs/KILL_CRITERIA.md` and `P59`** carry
*"49.23 kg — 58.2 % — survives the deletion of every requirement in all 64 corners."*

> **Corrected 2026-08-21: the manuscripts do not.** This entry named them and it was wrong.
> Neither `VOLLEY-paper/paper/paper.tex` nor `VOLLEY-thesis/source/paper.tex` cites A35 at all —
> no ledger figure, no corner count, no per-satellite survivor mass. **The stale pair was never
> propagated into the manuscripts, so there is nothing there to correct**, and the four repository
> locations above are the whole of it. Checked by grep for `49.23`, `58.2`, `64 corners` and
> `ledger` across both `.tex` files, all returning nothing.

**What would close it:** propagate **88.67 kg / 70.06 % / 7.39 kg per satellite** everywhere, and
**withdraw the twenty-four-satellite escape** rather than restating it at a number that no longer
closes anything. **A35's bands are not re-declared and its verdict is not edited** — the run sheet
gets a dated block, as A45-R2 and P84 did.

> **This is the sixth place A46 had to be chased to**, after `BASELINE.md`, the register, the
> paper's abstract, its conclusion, its family table and `mass_properties.py`'s own docstring.
> *A46 landed on 2026-08-16 and the project is still finding what it moved.*

### P96. The manuscript argued mass-per-satellite from pre-A46 numbers against its own post-A46 table, and still priced phase against drag: HIGH, CORRECTED 2026-08-21
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found while preparing a printed carry copy of the manuscript, which is the first time anyone
had read Section V straight through since [A46](validation/A46_enclosure_buildup.md) landed.**

**Three defects, all of them the same propagation failing in a different place.**

**1. The table was regenerated and the prose was not.** Table~\ref{tab:family} was rebuilt at the
current operating point on 2026-08-20 and gives **10.550 kg of deployer per 3U satellite**. The
paragraph immediately below it still argued from **7.04 kg**, the pre-A46 figure, and drew three
conclusions from it: *"by a factor of thirty"*, *"loses to a cold-gas module by roughly a factor
of eight"*, and *"at PocketQube it spends 0.24 kg and wins by two to five"*. **A reader comparing
the paragraph to the table directly above it would have caught this.**

| | As printed | Current |
|---|---:|---:|
| Deployer mass per 3U satellite | 7.04 kg | **10.550 kg** |
| Spread across the class column | ×30 | **×27** 3U against PocketQube 1P, **×109** across the full column |
| Loss to a cold-gas module | ×8 | **×9 to ×21**, and **×12.4** at the 0.85 kg mid-class figure |
| PocketQube 1P per satellite | 0.24 kg | **0.388 kg**, winning by 1.3 to 3.1 rather than 2 to 5 |

**2. Section V-C still priced in-track phase against differential drag.** The abstract and the
conclusion both carry [P56](#p56)'s correction — that release timing delivers 30° of phase for
468 s of waiting at zero Δv — and **the body section making the claim did not**. It compared
commanded splits at 1.4 days against drag at 25 days and stopped there. *The correction was
propagated to the two places a reader looks first and not to the place the claim actually lives.*
`F05_dragvs.png`'s caption now states what the figure omits; the figure is not redrawn, because
the drag comparison it makes is still correct.

**3. The limitations section said the depth-resolved thrust constant was "computed and
deliberately not applied here"** — [ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md)
applied it on 2026-08-13, and every figure in the paper, including the abstract's, is quoted after
it. **The paper contradicted itself on the provenance of its own headline.** The replacement text
states the adoption date, the reason it was held for three days, and the limit of the
three-dimensional check: A2 band 4 tests the field model at midgap to 0.059 %, **not** the depth
average, and no three-dimensional check of the integrated thrust constant exists.

### What else the same read found

**`tab:tier` carried 125 kg loaded** — pre-A46. Now 126.6 dry, 174.6 loaded.
**The array-length sweep in V-A carried 4.95 N per kA/m and 13.3 m/s** for a 150 mm array, against
`docs/PAYLOAD_CLASSES.md`'s current **4.65** and **12.9 m/s** — the same ADR-030 propagation.
**Four overfull lines ran into the page margin**, three of them predating this pass; all four are
now zero.

**And the comparison the paper had never stated at all is now stated**: VOLLEY is **1.758× heavier
per 3U satellite** than a canisterised dispenser, A21 band 4 fails, and kill criterion 1 is crossed
at **5.3×** on dry mass. [P69](#p69) recorded that on 2026-08-16 and the manuscript did not carry
it. *A paper that omits its own failed comparator band is a brochure.*

> **A46 landed on 2026-08-16. This is the seventh place it had to be chased to**, after
> `BASELINE.md`, the register, the paper's abstract, its conclusion, its family table and
> `mass_properties.py`'s docstring — and P95 found the eighth in A35 the day before this one.
> *The lesson is not that the propagation was careless. It is that a rollup change touches prose
> that no gate reads, and there is no gate that reads prose.*

### P97. ADR-030 shortened the regenerative section from 240 mm to 39 mm and the recovery figure never moved with it: HIGH, CORRECTED 2026-08-21
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found while checking the manuscript's energy chain against `motor_results.json` for a printed
copy. The paper and the front page both reported a recovery that the current design cannot
produce.**

[ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md) took four decisions on
2026-08-13. The one everything chased was the depth-resolved thrust constant. **The second one was
that the regenerative section shortens from 240 mm to 39 mm**, because 240 mm of regenerative
stator plus a 300 mm eddy fin were oversubscribed in a 339 mm airgap ([P28](#p28)). *Only the
first was propagated.*

| | As published | At the 39 mm section |
|---|---:|---:|
| Regenerative section | 240 mm | **39 mm** |
| Energy recovered | 291 J | **47.0 J** |
| **As a fraction of the sled's energy** | **23 %** | **3.9 %** |
| Sled kinetic energy at release | 1268 J | **1213 J** |
| **To the eddy brake** | **935 J** | **1162 J** |
| Braking pulse | 15.8 ms | **2.46 ms** |
| Copper burnt braking | 15 J | **0.39 J** |
| Speed reaching the brake | 14.1 m/s | **15.68 m/s** |
| Peak current during recovery | 219 A | **212 A** |
| Brake-fin adiabatic rise per shot | 7.1 K | **9.0 K** |
| Twelve-shot no-cooling bound | 85 K | **108 K** |
| Campaign thermal total | 24.3 kJ | **26.6 kJ** |
| Bulk rise over a campaign | 1.8 K | **2.0 K** |

**Everything in the right-hand column was already committed.** `motor_results.json`'s `regen`
block and `sizing.json`'s `energy_closure` and `thermal` blocks have carried these values since
the ADR; `make_baseline.py --check` passed throughout, because none of the twenty-three values it
guards is a recovery figure. **The gate was green and the prose was wrong.**

### The shape of the error is worth naming

**The brake got 24 % more energy and nobody noticed**, because the number that moved was the one
nothing quotes. Every document quoted the *recovery*, which is the flattering half. The fin
transient going 7.1 K to 9.0 K, and the twelve-shot bound 85 K to 108 K, are the consequences,
and they sat unstated in a section titled *Thermal Analysis*.

**And the efficiency was quoted at the wrong figure in the other direction.** `SUMMARY.md`, the
wiki and `README.md` all published **18.5 %**, which is `shot.eff_pct` — the *gross* figure, before
any recovery credit — while describing it as net of regeneration. `BASELINE.md` has published the
correct **18.8 %** (`eff_net_pct`) the whole time. *Three front-door documents disagreed with the
gate-checked baseline and with themselves.*

### What was corrected

`SUMMARY.md`, `wiki/Home.md`, `README.md` — including its energy pie, which was drawn with the
pre-ADR-030 closure — `validation/README.md`'s A11 row, `analysis/velocity_levers.py`'s docstring,
and both manuscripts. **`docs/RESULTS.md` and `docs/PROJECT_NOTES.md` carried a 2026-08-03 audit
banner that had itself gone stale**; each gets a superseding banner rather than an edit.

**[A11](validation/A11_regen_braking.md) is not touched.** Its eight bands were declared before
`regen_brake()` was written, they passed, and 291.4 J was the right answer for the section it
integrated over. *A decision taken ten days later removed that section.* The 500 mm and 1 m
comparison points in the manuscript were recomputed from `motor_model.regen_brake` at the current
operating point — 540 J and 727 J against the 570 J and 783 J published — and the 39 mm case
reproduces the committed 47.0 J exactly, which is what makes the other two trustworthy.

> **This is what a validation run looks like when an architectural decision outruns it.** A11 is
> not wrong and its bands are not widened. It simply answers a question about a machine that
> stopped existing on 2026-08-13, and for eight days nothing in the repository said so.

### P98. The acceleration ceiling was presented as a CubeSat qualification limit, and it is a number this project chose: HIGH, CORRECTED 2026-08-21
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Raised in review of the printed manuscript, 2026-08-21, and it is the strongest technical
criticism the front-page claim has received.**

The claim, in the abstract and on every summary page, was that VOLLEY ejects a satellite *"within
standard qualification loads"* and *"inside its existing qualification envelope"*. The derivation
behind it, in `docs/VELOCITY_CEILING.md` and §III-B of the manuscript, was:

> *NASA GEVS protoflight random vibration integrates to **14.1 g rms**, whose **3σ envelope of
> roughly 42 g** bounds the launch load, and a **25 g** design cap preserves margin against it.*

**That is a unit error dressed as a margin argument.**

| | |
|---|---|
| `g_rms` is | the root-mean-square of a **stationary random process** over a broadband spectrum |
| 3 × `g_rms` is | a **peak-response estimate for that process**, used for fatigue and Miles'-equation load derivation |
| It is **not** | a quasi-static limit load, and a structure qualified to a random-vibration spectrum is **not** thereby qualified to a sustained 162 ms acceleration of similar nominal magnitude |

**The second error compounds the first.** `docs/PRIOR_ART.md`, ADR-003 and the manuscript's related-work
section all stated that *"a standard CubeSat qualifies to roughly **14 g quasi-static**"*. **There is no
such published figure.** It is 14.1 g rms with its units changed. The CubeSat Design Specification Rev. 14
publishes a mechanical interface, not a load level, and **defers test levels to the launch provider** —
so they vary by vehicle and by mission, and this repository holds no launch-vehicle user guide and no
payload-specific load case to substitute.

### What is actually true

| | |
|---|---|
| **10.07 g for 162 ms** | the rated model result. **Unchanged** |
| **25 g** | a ceiling **this project chose**. Everything downstream is sized against it consistently — the retention chain, the cradle preload, the abort logic, the payload-family table, A27, A38, A63, A65 — and that consistency is real |
| **Payload compatibility** | **not established, and not establishable from anything in this repository.** It depends on the satellite's own qualified load environment and on an integration review |
| **Mechanical qualification against this machine** | **none. No payload has been tested against it** |

**The 25 g figure survives as a requirement. What does not survive is calling it a capability.**

### Corrected. Propagated 2026-08-21

`docs/VELOCITY_CEILING.md` — the canonical page, which loses its two derived rows and gains the
correction in full · `docs/PRIOR_ART.md` · `docs/ICD_COMPLIANCE.md` · `docs/GEN5_CLOSURE.md` ·
`docs/PAYLOAD_CLASSES.md` · `docs/QUALIFICATION_PLAN.md` · `docs/REVIEW_RESPONSES.md` ·
`docs/DESIGN_OPTIONS_exit_velocity.md` · `SUMMARY.md` · both manuscripts, in the abstract, the
related-work section, the requirements list, the parameter table, the topology trade, the
competitive claim, the conclusion and a new first limitation · and the printed brochure.

**ADR-003 keeps its text**, because its comparison block is a dated decision record; the figure it
quotes is annotated where it is defined rather than edited where it is cited.

### What the correction costs, and what it does not

**It does not weaken the comparison with an armature-based launcher.** Feng's design imposes two to
three orders of magnitude more acceleration than this one, and that ratio needs no CubeSat standard
to state — only the two accelerations, both of which are known.

**It does weaken the headline.** *"Inside its existing qualification envelope"* was doing real work
in the abstract, and there is no honest replacement for it. What replaces it is narrower and duller:
**a deployment acceleration of 10.07 g, and an open question about whether any given satellite
accepts it.**

> **The lesson is the same one P16 taught and it is worth stating twice.** Both were claims this
> project made *about its own defensibility* — the invariant lifetime ratio, and the qualification
> envelope — and both were the strongest-sounding sentence in the abstract. *A claim that a result
> is safe is still a claim, and it needs a source like any other.*

### P99. One shot's angular momentum exceeds the only wheel this project has ever named: HIGH, NEW 2026-08-22
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HOST_DATA` — a real host wheel, or a host that does not need one


**Found by [A57](validation/A57_stage_attitude_packaging.md), and recorded outside its bands on
purpose.**

| | |
|---|---:|
| Angular momentum the host absorbs per shot | **1.46 N·m·s** |
| Over a twelve-shot campaign | **17.53 N·m·s** |
| The wheel [A52](validation/A52_gen6_recoil.md) declared | **15 N·m·s** |

> **Corrected 2026-08-22, hours after this entry opened.** It first read 22.76 and 273.14 N·m·s.
> A57 had used a lever arm **15.6× its own interface requirement** — see **P100** — and the figures
> above are at A52's published 10.65 mm. **The entry survives the correction**: the campaign still
> exceeds the wheel, by **1.17×** rather than by 18×. *That change is the difference between a
> dismissal and a design question, and it is why the arm was worth chasing.*

**The campaign saturates it, and by a margin thin enough that a real wheel might close it.** On A52's wheel the campaign cannot be flown without desaturating between
shots, and **no concept of operations in this repository describes desaturation.**
[`docs/CONCEPT.md`](docs/CONCEPT.md) §3.3 has the stage repositioning between altitude shells on its
own reaction control and firing at each station; it does not have it dumping momentum twelve times.

### Why this is a finding and not a band

**A57 band 5 forbids exactly this comparison.** It was written that way because
[P94](#p94-a13-band-5-passes-on-a-host-control-authority-that-e5-says-does-not-exist) is open:
A13 band 5 *passed* by dividing a correct result by a host control authority of 0.1 N·m that
**[E5](#e5-host-stage-properties-unavailable)** records does not exist.

**So A57 had two ways to fail and took neither.** Widening band 5 to admit the comparison would
have repeated P94. Suppressing the number because the band forbade it would have been the opposite
failure — *hiding a real consequence behind a procedural rule.* It is reported in
`findings.wheel_observation`, flagged `outside_bands`, and it opens this entry.

### What this entry is not

**It is not a finding about any real stage.** A52's 15 N·m·s wheel is a **declared assumption**,
chosen so two attitude runs could be compared, and it is not a property of any candidate vehicle.
**E5 stands: no candidate stage publishes its mass or its control authority.** On a real stage this
number could be comfortable or hopeless and nothing here can tell which.

**What is real is the momentum**, which is a property of this machine: 4 kg leaving at 34.28 m/s
through a lever arm the design chose.

**What would close it.** Either **E5** — a host that publishes a momentum-storage figure — or a
ConOps that states how momentum is dumped between shots and what it costs. *The second is
writable today and the first is not*, which makes it the cheaper half. **At 1.17× a wheel one size
up also closes it**, which was not true at the figure this entry opened with.

> **The lever arm was the soft spot, and it gave way within hours.** This entry originally warned
> that `ASSUMED_ARM = 0.166 m` was inherited, unsourced, and that *"a factor of two either way is
> entirely possible and nothing in this repository would catch it."* **It was a factor of 15.6, and
> what caught it was reading A52 — a run in this same repository that had already published the
> right number.** **P100.**

### P100. A57 used a lever arm 15.6 times the interface requirement this project had already published: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by reading [A52](validation/A52_gen6_recoil.md) after
[A57](validation/A57_stage_attitude_packaging.md) had already run and been recorded.**

[A57](validation/A57_stage_attitude_packaging.md) imported `attitude_budget.ASSUMED_ARM = 0.166 m`
for the perpendicular distance from the host centre of mass to the payload's line of travel.

**That is A13's arm, and A13 is a Gen5 run.** It measures from a Gen5 host centre of mass to *the
deployer's* — a sensible quantity for a 9.445 kg sled moving inside a 1.839 m box bolted to a
satellite bus. **A Gen6 payload traverses an 8 m tube that is the stage**, and the arm that matters
is how far that tube's axis sits from the stage's own centre of mass.

**A52 band 4 had already published a requirement on precisely that**, on 2026-08-16, six days
earlier: *the thrust line must pass within **10.65 mm** of the host centre of mass*, derived as the
offset at which a 15 N·m·s wheel saturates within twelve shots.

| | |
|---|---:|
| Arm A57 used | **166.0 mm** |
| Arm A52 requires | **10.65 mm** |
| **Ratio** | **15.6×** |

**A design meeting its own published interface has the smaller arm.** A57 was conservative by 15.6×
in every attitude figure it reported.

### What it changed

| | First run | Corrected |
|---|---:|---:|
| Offset per shot, 300 kg | 0.1747° | **0.0112°** |
| Campaign offset | 2.0969° | **0.1346°** |
| Momentum per shot | 22.76 N·m·s | **1.46 N·m·s** |
| Campaign momentum | 273.14 N·m·s | **17.53 N·m·s** |
| **Band 4, Gen6 ÷ Gen5** | **2.33×** | **0.149×** |

**No band verdict moves.** Five pass with more margin, band 6 still fails at 200 mm because
geometry does not depend on the arm, and two report.

**But band 4 reverses.** A57 concluded that *"deleting the mover increased the attitude cost"*, and
**that conclusion is withdrawn** — at each architecture's own arm, Gen6's offset is about a seventh
of Gen5's. *What the reversal actually demonstrates is that the lever arm dominates the result and
the architecture barely enters it*, which is a more useful finding than either number.

### Why it was not caught

**The two runs are six days apart and both are mine.** A52 derived an alignment requirement and
A57 modelled an alignment-driven disturbance, and **nothing connected them** — A57 imported the
arm from the file it imported the *model* from, which is the natural thing to do and was the wrong
thing to do.

> **The entry that warned about it was written by the run that got it wrong.**
> [P99](#p99) — opened by A57, hours before this — says the arm *"has never been sourced"* and that
> *"a factor of two either way is entirely possible and nothing in this repository would catch it."*
> **It was a factor of 15.6, and what caught it was a run already in the repository.** The warning
> was right about the risk and wrong about the size, and it looked in the wrong place for the fix.

### Corrected. Propagated 2026-08-22

`attitude_budget.move()` takes an optional `arm`, defaulting to `ASSUMED_ARM` so **A13's own results
are byte-identical** — verified: only the source hash moved. `stage_attitude.py` reads A52's
`saturating_offset_mm` live rather than restating it, and **sweeps both ends** so the sensitivity is
in the results file rather than in a comment. A57 gets a dated correction block; its bands are not
re-declared and its verdict is not edited. P99's figures are corrected in place and **it survives**:
the campaign still exceeds A52's wheel, at 1.17× instead of 18×.

**The Gen5 arm is still unsourced.** `ASSUMED_ARM` remains a declared assumption with no derivation
behind it, and A13's numbers still rest on it. This entry corrects where Gen6 got its arm; it does
not give Gen5 one.

### P101. The payload ladder D2 turns on was three rollup generations stale, and the rung the project was leaning on does not close: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found while writing [`docs/D2_DECISION.md`](docs/D2_DECISION.md)**, which needed the one table
the decision actually turns on and could not quote it.

**D2 asks which payload class is the product.** The answer is a ladder of deployer kilograms per
satellite against a ~2 kg threshold, and there are two of them:
[`payload_family.py`](analysis/payload_family.py)'s *volumetric* ladder and
[A24](validation/A24_fixed_cell_manifest.md)'s *designed-cell* ladder, which
[`docs/PAYLOAD_CLASSES.md`](docs/PAYLOAD_CLASSES.md) says in its own words supersedes it: *"Read
A24 and ADR-025 before quoting anything above."*

**The superseding table was the stale one.** Three vintages of the same ladder were in the
repository at once, and they disagreed about every rung:

| Where | Dry mass it divides | 1U | PocketQube 3P |
|---|---:|---:|---:|
| `PAYLOAD_CLASSES.md`, the A24 blockquote | **76.5 kg** | 2.125 | 0.797 |
| `analysis/results/cell_manifest.json`, committed | **84.5 kg** | 2.347 | 0.880 |
| **`mass_properties.py`, the rollup since A46** | **126.6 kg** | — | — |

**The script was never wrong.** `cell_manifest.py` line 47 reads
`DEPLOYER_DRY_KG = pf.DEPLOYER_DRY_KG`, and `payload_family.py` reads `dry_kg` out of the rollup
at import. Nothing in either file hardcodes a mass. **Only the committed results file and a
hand-typed blockquote were stale**, and re-running the script is the entire repair — the same
shape as the commit that last touched this file, whose message was *"the baseline change reached
the documents and stopped at the scripts."* This time it reached the scripts and stopped at their
outputs.

### Re-run 2026-08-22, at the rollup A46 produced

| Class | Per load, designed cell | Was, at 84.5 kg | **Now, at 126.6 kg** | Against 2.0 kg |
|---|---:|---:|---:|:--|
| ChipSat / femtosat | 8640 | 0.010 | **0.015** | closes |
| **PocketQube 1P** | 288 | 0.293 | **0.440** | **closes** |
| **PocketQube 3P** | 96 | 0.880 | **1.319** | **closes** |
| 1U CubeSat | 36 | 2.347 | **3.517** | **crosses** |
| TubeSat | 24 | 3.521 | **5.275** | crosses |
| 3U CubeSat | 12 | 7.042 | **10.550** | crosses, 5.3× |
| ThinSat, 6U, 12U | — | — | — | not accommodated |

**Two band verdicts move, and the bands are not edited.**

**Band 1 fails.** It tests that the cell model reproduces the machine that exists, against a
reference of **6.375 kg/satellite written into the script** at a rollup two corrections old. The
cell model reproduces the machine exactly — 12 per load, and 10.55 kg/satellite is the rollup
divided by twelve. **What band 1 is now detecting is its own hardcoded reference**, not a defect in
the cell model. It is recorded as failing because that is what it does at the current inputs; it is
not re-declared, and A24's original verdict stands as run.

**Band 3 still passes, on two rungs instead of four.** It asks whether *some* designed class closes
kill criterion 1, and PocketQube 1P and 3P both do. **1U does not**, and 1U is the rung this
repository had been leaning on — `PAYLOAD_CLASSES.md` already recorded A24 taking it from 1.913 to
2.125 and over the threshold, and at the current rollup it is **3.517 kg**, over by 76 %.

Band 6 fails as it did at A24, for the reason [P44](#p44) records. Bands 2, 4 and 5 pass unchanged.

### What it changes for D2

**It does not change the shape of the answer and it removes the ambiguity from it.** The only
designed classes that close kill criterion 1 on dry mass are the two PocketQube rungs and ChipSat,
which [`payload_family.py`](analysis/payload_family.py) marks *beyond the mechanism*. Every ladder
figure quoted in a decision document must now come from the re-run file.

### Why it was not caught

**[`tools/check_crossrefs.py`](tools/check_crossrefs.py) was written the same day and this pair was
not one of the nine it declared.** It fails when two committed results files disagree about the
same quantity, which is exactly this: `cell_manifest.json` published a `deployer_dry_kg` of 84.5
while `mass_properties.json` published 126.6, in the same repository, for four commits' worth of
work. **It is declared now**, and the gate reproduces the failure when the old value is restored.

### Corrected. Propagated 2026-08-22

`cell_manifest.py` was re-run with **no edit to the script** — it read the rollup live and always
did — and the four documents that quoted the ladder were re-quoted from the re-run file:
[`docs/PAYLOAD_CLASSES.md`](docs/PAYLOAD_CLASSES.md) in two places,
[`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md)'s route table, which had one row at 126.6 kg and
four at 76.5, and [A24](validation/A24_fixed_cell_manifest.md), which gets a dated correction block
with its bands not re-declared and its 2026-08-10 verdict not edited.
[`docs/D2_DECISION.md`](docs/D2_DECISION.md) is written against the re-run file only.
**Two cross-references are declared in `tools/check_crossrefs.py`** — the rollup against
`cell_manifest.deployer_dry_kg`, and the 3U rung of the two ladders against each other, which must
agree because at 3U a designed cell holds exactly one satellite. **Restoring 84.5 kg reproduces the
failure and the gate exits 1.**

**One thing is corrected and one is not.** The multiplier `PAYLOAD_CLASSES.md` quoted for
PocketQube against a cold-gas module was derived from the stale figure; it is **removed rather than
re-derived**, with a NEEDS SOURCE line in its place, because re-computing it here would put a
number in a document that no results file holds.

### P102. The only Gen6 tip-off run was left at A37's window when ADR-034 moved the stroke, and its run sheet predicted exactly this: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found while reconciling a sweep of the outside separation literature against the record.** Its
strongest claim is that a long guided interface makes contact and geometry matter more than the
energy path, and that tip-off is the term to watch. **Checking whether this project had answered
that at 8 m found that it had answered it at 2.18 m.**

[A38](validation/A38_tipoff_at_gen6.md) is the only run that takes tip-off to Gen6.
`analysis/tipoff_gen6.py` held its operating point as two module constants:

| | A38, hardcoded | `gen6_drive`, since [ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) |
|---|---:|---:|
| Acceleration | **25.0 g** | **11.362895 g** |
| Acceleration length | **2.18 m** | **8.0 m** |

**2.18 m was the long end of [A37](validation/A37_host_integrated.md)'s feasible window**, and
ADR-034 replaced that window with the host stage's whole usable length on 2026-08-19. **The script
was never re-run and nothing pointed at it.**

> ### The run sheet wrote the warning and then became the example
>
> A38's own opening, and `tipoff_gen6.py`'s docstring, both say:
>
> > *"This is the P19 and P53 pattern, which this project has now recorded twice: an analysis that
> > closed at one operating point, left standing while the point moved underneath it. **The
> > difference here is that the point has not moved yet.** Checking before adopting is the whole
> > discipline."*
>
> **The point moved three days later.** The run that was written to demonstrate checking before
> adopting is the run that was not re-checked after.

### Corrected. Re-run 2026-08-22, and no band verdict moves

`tipoff_gen6.py` now reads `acceleration_g` and `stroke_mm` from `cad/parameters.json` at import,
the same repair [P84](#p84) applied to `precharged.py`. **`G_CAP` stays at 25.0** — it is the
payload qualification cap and **band 6's declared threshold**, not the design point, and lowering
it to the design point would have widened a band.

| | A37 window | **Design point** | |
|---|---:|---:|---|
| Powered stroke | 133.3 ms | **378.9 ms** | band 3 gains margin |
| Worst cradle arrival | 355.1 °/s | **239.4 °/s** | improves |
| Settling at e = 0.7 | 17.69 ms | **26.24 ms** | still inside the stroke |
| Residual at release | 0.0000 °/s | **0.0000 °/s** | unchanged |
| Critical restitution | 0.9462 | **0.9712** | improves |
| **Preload per contact** | **201.7 N** | **91.7 N** | **the one that propagated** |
| Tip-off ceiling | 30.9 g | **30.9 g** | preload-limited, so the stroke does not enter it |

**Every published figure moved and every verdict stayed.** Band 1 fails as it already did
([P61](#p61)); bands 2–6 pass, four of them with more margin. **The correction rescues nothing and
damages nothing — it corrects the record**, which is the outcome an entry like this should
usually have.

**[P61](#p61) named the missing tool and this is the same class again.** It asked for *"a
regression band comparing a run sheet's recorded figures against its script's current output"* and
recorded it as not built. `tools/check_crossrefs.py` now does the results-file half of that, and
**the pair that would have caught this is declared in it** — the design point in
`cad/parameters.json` against the point `tipoff_gen6.json` says it ran at. Restoring 25 g and
2.18 m makes the gate exit 1.

### Two things it leaves open, and neither is bookkeeping

**1. `cad/parameters.json` carries 201.7 N and the design point needs 91.7.**
`gen6_drive.cradle_preload_N_per_contact` is A38's figure at 25 g, and `cad/build_gen6.py` says in
its own docstring that the tube wall is set partly by *"carrying A38's 201.7 N cradle preload"*.
**The parameter is not being changed here.** It is conservative by 2.2×, no script reads it as a
driver, and lowering a retention requirement on the strength of a re-run is a design decision
rather than a correction. **It is recorded as one.**

**2. The model is constant-acceleration, and at 8 m that is the constant-pressure bound.**
`point()` takes `v = sqrt(2 a L)` and returns **42.23 m/s**, which is exactly
`gen6_drive.exit_velocity_m_s_constant_pressure_bound`. **The delivered figure is 29.01 m/s** and
the shot is a blowdown, not a constant push.

**The conservatism this buys is one scalar wide.** A lower delivered exit velocity over the same
8.0 m means a longer powered stroke, so **band 3's settling-time-against-time-available comparison
is understated**. It does **not** follow that the contact trajectory or the angular response is
conservative under the real pressure–time history: under blowdown the acceleration is time-varying,
the angular forcing from force-line eccentricity varies with it, and contact timing, arrival rate
and rebound timing all move. **A38's Gen6 answer is a bound on one comparison, not a bound on the
motion.** *Narrowed here on the same day it was written; the first version of this paragraph
claimed the direction was safe without qualifying what it was safe about.* **Contained in
[P103](#p103), which owns the trajectory, rather than opened as a separate entry.**

### What this does not touch, and it is the larger gap

**A38 models the payload rattling across its cradle clearance at the start of the stroke. Nothing
in this repository models the other 8 metres.** There is no contact state along the bore, no
straightness or roundness input, no force-line eccentricity, no payload centre-of-mass offset, and
no lateral or angular state carried through the stroke — and `docs/EXTERNAL_EVIDENCE.md` records
that the nearest published work makes exactly those the dominant terms. **P67 measures a force;
what that force is a property of has never been modelled.**

### P103. Gen6 has no model of the payload's guided contact state through the 8 m bore, so its exit angular and lateral state is not established: HIGH, NEW 2026-08-22
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — A67 has run; what is left is roundness, stick-slip, inertia variation, tube compliance and a contact law that passes its own restitution check


**[P102](#p102) found this while correcting something smaller and did not own it.** That entry is a
propagation defect and it is closed. **This one is the engineering, and it is open.**

**The chain Gen6 models is chamber pressure → axial force → exit velocity.** The chain that decides
whether a customer's satellite arrives usable is **contact state → lateral impulse and torque →
release pose and rate**, and no file in this repository contains it.

[A34](validation/A34_cradle_restitution.md) and [A38](validation/A38_tipoff_at_gen6.md) model the
payload crossing its **cradle clearance** in the first tens of milliseconds and answer it well —
the rattle settles, the residual rate at force removal is exactly zero. **Then the payload travels
another eight metres inside a tube and nothing follows it.**

### What is missing

**Necessary for a first-order answer.** Without these there is no exit angular or lateral state at
all, only an axial one:

| Term | Where it stands today |
|---|---|
| **Local clearance**, bore against carriage, as a distribution | Not stated anywhere. `gen6_drive.bore_mm` is a nominal 15.805 |
| **Bore straightness over 8.0 m** | Not stated. [A59](validation/A59_tube_structure.md) needs **seven supports at 1.0 m** and models no resulting shape |
| **Force-line eccentricity** — gas thrust axis against bore axis | No tolerance exists. [A52](validation/A52_gen6_recoil.md) publishes a **10.65 mm** requirement against the *stage* centre of mass, which is a different quantity |
| **Payload CG eccentricity** | `cradle_restitution.COM_OFFSET` exists for the cradle moment and nothing sweeps it |
| **Friction law** — breakaway and sliding, with spread | **[P67](#p67).** [`docs/B2_ORDER.md`](docs/B2_ORDER.md) is the order |
| **Contact stiffness and damping** | Only as a restitution coefficient, swept not measured, inside A34 |
| **Lateral translation and pitch/yaw integrated through the stroke** | **Does not exist** |
| **Exit lateral velocity, exit angular rate** | **Does not exist.** Kill criterion 4's Gen6 answer is the cradle result and says nothing about the other 8 m |
| **Peak contact load and contact impulse count** | **Does not exist**, and nothing in the record states what either may be |

**Second order, and explicitly not required for the first model.** Adding these before the
first-order terms are swept would be false precision:

bore **roundness**; friction **pressure**, **velocity** and **temperature** dependence — B-2 bands
7, 6 and 12 respectively; **stick-slip** within a stroke — B-2 band 11; **payload inertia
variation** across the manifest; **tube structural compliance**, which A59 says is real enough to
need seven supports; **seal preload** as distinct from the friction it produces.

### Why it is not owned by anything already open

**Checked before this entry was written.** [P67](#p67) is a *measurement* and B-2 is its order —
it produces one input to the model below and is not the model. [P78](#p78) is the **energy** cost
of stroke, friction's growing share of shot work, and says nothing about geometry or attitude.
[P88](#p88) is the seal's own thermal survival. [P89](#p89) is closed. [P41](#p41) is corrected and
is the cradle. **No live entry carries the guided-contact problem, and until this one it had no
owner at all.**

### What the outside literature contributes, and what it does not

[`docs/EXTERNAL_EVIDENCE.md`](docs/EXTERNAL_EVIDENCE.md) records the nearest published work:
guided ejection of a CubeSat-class body along an anodised aluminium rail, analysed in a multibody
contact model for **release attitude**, with **fit clearance found to have an optimum rather than a
minimum**. **It supplies the shape of the problem and the modelling method. It supplies no number
this repository may use** — its clearance, its rail length and its tolerances belong to its
mechanism, and importing them is the failure this project has recorded twice.

### What would close it

> ### AMENDED 2026-08-22: the model does not wait for B-2
>
> **As first written this entry put the measurement first and said step 1 was not optional.** That
> was wrong about the order and it would have stalled the whole model behind a purchase.
> **A measurement calibrates a contact model; it is not a precondition for having one.**
>
> [`docs/EXTERNAL_EVIDENCE.md`](docs/EXTERNAL_EVIDENCE.md) records three separation-dynamics
> records that make the point independently: the contact parameters are **identified** — in one
> case by unscented Kalman filter against a finite-element collision solve — rather than measured
> first and inserted. **So the model is built now, on bounded friction, and B-2 replaces the bound
> with a distribution when it lands.**
>
> **What changes:** step 1 moves from a precondition to a calibration input, and the model may
> report *bounded* exit state before B-2 and *calibrated* exit state after it. **What does not
> change:** the model's own acceptance bands are declared before its script exists, and a bounded
> result is published as bounded.

**Ordered. B-2 calibrates step 2; it no longer gates it.**

1. **[P67](#p67) is measured** — B-2 — giving a friction force with its spread, its direction
   dependence and its force–time character rather than a scalar allowance. **Until it lands, the
   model runs on a declared bracket and says so.**
2. **A reduced multibody contact model propagates the payload across the full 8.0 m**, carrying
   lateral and angular state, driven by the design point read live from `cad/parameters.json` and
   **not** by a constant acceleration. *Its acceptance bands are declared before its script exists,
   as every run here is; none is declared in this entry.*
3. **The reduced model is checked** — against a higher-fidelity contact solve at selected points,
   or against a representative guided-ejection article, and the disagreement is quoted.
4. **A sweep over the necessary terms above** returns, as distributions: exit axial velocity, exit
   lateral velocity, exit angular rate, peak contact load, and contact impulse count and timing.
5. **The results are checked against thresholds that already exist** — the **2.0 °/s** residual
   rate A38 band 2 was declared against and A23 quotes as the tighter flown deployer figure, and
   the exit-velocity dispersion chain [A44](validation/A44_gen6_dispersion.md) publishes.
   **For peak contact load and contact impulse there is no threshold in this repository**, and the
   run that produces them will have to say against what they are being judged before it judges them.

**No numerical tolerance is declared here**, because a tolerance declared in a register entry is a
band chosen outside the discipline that makes bands worth anything.

> **Nothing here says the machine fails.** It says the quantity that decides kill criterion 4 for
> Gen6 has not been computed, and that **the cradle settling result must stop being quoted as
> though it had been.**

### P104. B-2 as first written measures a pneumatic cylinder and would have been recorded as measuring the Gen6 seal: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[`docs/B2_ORDER.md`](docs/B2_ORDER.md) was written on 2026-08-22 and this was found the same
day, before anything was ordered.** *That is the only good thing about it.*

**The order specified a stock ISO 6432 cylinder, a logging load cell, and twelve bands about what
to do with the reading. It never asked what the load cell is attached to.**

| | |
|---|---:|
| Threshold — [A61](validation/A61_seal_class.md)'s seal-thermal specification, 4.00 % | **17.8352 N** |
| Threshold — trim-unnecessary fraction, 5.00 % | **22.294 N** |
| **The decision window between them** | **under 4.5 N** |

**A rod on a stock cylinder carries four friction paths and VOLLEY has one.**
[ADR-035](docs/adr/035-drive-tube-material.md) records that the carriage is not recovered and that
**every seal makes exactly one 8.0 m pass** — the Gen6 interface is **a free piston in a bore**,
with no rod, no rod seal, no wiper and no rod bearing. **A pull on a cylinder rod measures all
four, plus a return spring if one is fitted**, and §1.1 as first written permitted *"spring-return
or double-acting"*. A return spring on a 16 mm bore develops a force of the same order as **the
whole of the lower threshold**.

**So the parasitic terms are plausibly the size of the gap the measurement exists to resolve, and
in the spring case the size of the thresholds themselves.**

> **Band 1 asked for breakaway. Band 2 asked for running friction. Band 5 asked for unit-to-unit
> spread. Band 8 asked whether the measurement discriminates.** *Every one of them is a question
> about a number the rig could not produce.* **Band 8 was written to catch exactly this class of
> self-deception and it looked at speed, pressure and vacuum — not at what the sensor was in series
> with.**

### Corrected. Propagated 2026-08-22, before purchase

**Bands 1–12 are not edited and no threshold moves.** Two bands are added, declared before the
cylinder is ordered and before any data exists, and both are **prerequisites on bands 3 and 4** in
the way band 8 already is:

- **Band 13** requires the non-target force to be measured **on the same hardware**: each unit
  pulled twice, complete and with **the piston seal removed**, everything else unchanged. **The
  deliverable is the difference**, not a load-cell reading.
- **Band 14** requires the result to **classify**: the difference, with its combined 3σ spread,
  must lie wholly below 17.8352 N, wholly above 22.294 N, or wholly between them. **If it straddles
  a boundary, P67 is not answered** and band 8's third outcome applies.

**Band 14 declares no new number.** Both bounds are A61's, already in
`analysis/results/seal_class.json`, and both were declared before this order existed.

**Spring-return is excluded from the purchase.** Double-acting only.

### What is still not representative, and it is not this entry's to fix

The rod stays in the fixture, so its side load acts on the piston seal in **both** configurations
and lives inside the difference rather than being subtracted. And the difference is a piston seal
**in a rod cylinder at ambient**, not a free piston at **22.73 bar and 17 m/s in vacuum**.
**Band 8 governs that and always did.** *What changed is that the quantity band 8 is judging is now
the seal rather than the assembly.*

### P105. The companion reproducibility payloads went four commits stale and no gate in the project could see it: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**`VOLLEY-paper` and `VOLLEY-thesis` publish the analysis, the results and the run sheets as a
reproducibility payload, generated by `tools/export_companion.py`.** Both were sitting at flagship
commit **`28bfaba`** while the flagship stood at **`ef8f07b`** — four commits, carrying P100's
propagation, [P101](#p101) and [P102](#p102).

**Both companions were therefore publishing `validation/A38_tipoff_at_gen6.md` with no correction
block on it**, at 25 g over 2.18 m, under a banner that names a flagship commit and says *"where a
generated file disagrees with VOLLEY, VOLLEY is right and this copy is stale."* **The banner was
telling the truth and nothing was listening.**

### Why no gate caught it

**The provenance was never missing.** The export has stamped the flagship commit into each
companion's README since it was written. **The problem is where that stamp lives**: in the other
repository, which no gate in this one opens. `check_links.py`, `register_status.py`,
`make_baseline.py`, `check_artifacts.py`, `check_public.py` and `check_crossrefs.py` all read the
flagship and all passed.

> **This is P84, P100, P101 and P102 across a repository boundary.** A value moved and something
> that restates it did not — except that here the restatement is an entire published tree, and the
> thing that moved was the correction record itself.

### Corrected. Propagated 2026-08-22

**`tools/check_companions.py`**, a sixth gate. `export_companion.py` now writes
`tools/companion_export.json` recording the flagship commit it ran at and the manifest source
paths; the gate fails when **any commit since has touched a manifest source**, which git answers
offline. Where the companion working copies are on disk it also requires their README banner
commit to match, and it says which copies it could not check rather than passing silently.

**It lives in `tools/` rather than `analysis/results/` because `analysis` is itself a manifest
source** — a record written there would have been a payload file whose own commit made the payload
look stale, and the gate would have tripped on the act of recording that it had not.

**Both payloads were regenerated and pushed.** The gate is offline by construction, like the other
six: it asks git about this repository and reads files that happen to be present. It never reaches
the network, because none of the others do either.

### P106. VOLLEY-paper's LICENSE was the MIT text while its own NOTICE and LICENSING.md said the payload is CC BY 4.0 and pointed at that file: MEDIUM, RESOLVED 2026-08-22
> **Status:** `CLOSED` — resolved; see the entry for what closed it


**Found while checking, before running the export, that nothing authored would be overwritten.**

`VOLLEY-paper/LICENSING.md`, in its own table: *the reproducibility payload is* **CC BY 4.0. Full
text in `LICENSE`**. `VOLLEY-paper/NOTICE`: *"This work is licensed under the Creative Commons
Attribution 4.0 International License. The full licence text is in LICENSE."*

**`VOLLEY-paper/LICENSE` is the MIT licence**, and it is that on purpose.
`PAPER_MANIFEST` maps **`LICENSE-MIT-superseded` → `LICENSE`** with the reason written beside it:

> *"LICENCE HELD, 2026-08-10. The flagship is CC BY 4.0; this companion deliberately is not …
> Relicensing the IEEE manuscript sets terms that an IEEE copyright transfer on acceptance would
> supersede, and this repository cannot license rights it has transferred."*

**So the hold is deliberate, documented, and mechanically enforced — and two files added to that
repository afterwards assert the opposite, on its front page.** `NOTICE` and `LICENSING.md` are not
in the manifest, so the export does not touch them and the contradiction survives every run.
**Every export re-asserts the MIT text under a notice that says it is CC BY.**

### What this is not

**It is not a stale generated file** — the export is behaving exactly as specified.
**It is not a correction** either, and it is not being fixed here. Which licence the payload
carries is **[D4](docs/STATE_OF_THE_PROJECT.md)** — *submit to IEEE, or publish openly* — an owner
decision that has been open since 2026-08-10, and *a correction is not a design decision*.

### What would close it

**Either half, and the choice is D4's.** If the hold stands, `NOTICE` and `LICENSING.md` in that
companion say so and stop pointing at `LICENSE` for a CC BY text it does not contain. If the hold
is released, `PAPER_MANIFEST` already documents the one-line change in a comment — five mapping
lines that `THESIS_MANIFEST` carries today — and the export does the rest.

**Until then the two statements disagree in public**, and the flagship's own licence is not in
question: it is CC BY 4.0 and always has been.

> ### RESOLVED 2026-08-22. D4 is decided: CC BY 4.0.
>
> **The hold had nothing left to hold against.** It was placed against an IEEE copyright transfer
> *on acceptance*, and **no venue has been selected** — so the position being protected was
> hypothetical while the contradiction it produced was public and permanent.
>
> `PAPER_MANIFEST` now carries the five lines its own comment already documented as the release:
> `LICENSE`, `NOTICE`, `LICENSING.md`, `LICENSE-MIT-superseded` and `CITATION.cff`, which is what
> `THESIS_MANIFEST` has carried since 2026-08-10. **`LICENSE-MIT-superseded` is still shipped under
> its own name** — the repository was MIT for a period, and dropping the file would erase that
> rather than supersede it.
>
> **This is a decision, not a correction**, and it is recorded as one in
> [`docs/STATE_OF_THE_PROJECT.md`](docs/STATE_OF_THE_PROJECT.md) at D4. *If a venue is selected and
> requires a transfer, that is a decision taken then, on the accepted version, and recorded then.*

### P107. The Gen6 CAD described the pre-ADR-034 design point for three days, and called Gen5 a measured baseline: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**`cad/build_gen6.py`'s header, `cad/README.md` and `CAD_BRIEF.md` all described a machine the
parameter file had already replaced.**

| Described | `cad/parameters.json` |
|---|---|
| chamber **2 L at 50 bar** | 2 L at **22.7258 bar** — [ADR-034](docs/adr/034-gen6-long-stroke-design-point.md) |
| reservoir **11.25 L**, *"A42, the ADIABATIC figure"* | **3.46 L** — [A56](validation/A56_reservoir_resized.md), **sized** rather than scaled |
| exit velocity **30.54 m/s at 25 g** | **29.01 m/s** at the friction allowance, **11.36 g** peak |
| hoop stress *"at 50 bar … needs 0.16 mm"* | A59 band 1: **17.96 MPa against 250 allowable**, 13.9× |

**The reservoir figure was two corrections old, not one.** A42 gave a bracket — 7.65 L isothermal
against 11.25 adiabatic. [A43](validation/A43_reservoir_thermal.md) superseded both at **9.55 L**.
A56 superseded that at **3.46 L** and **P82** closed. `CAD_BRIEF.md` was still instructing a reader
to *"model the reservoir at 11.25 L and expect it to shrink."*

### The geometry was never wrong

**`build_gen6.py` reads every one of those numbers from `parameters.json` at import**, and
`--check` verifies the built solids against it: chamber 2.0000 L, reservoir 3.4600 L, force
445.8802 N, acceleration 11.3629 g, all OK. **The STEP files describe the current machine. The
prose around them described the old one**, and nothing could see the difference because **none of
these three files was a checked surface.**

> **This is P84, P101 and P102 in a fourth place.** A value moved and a restatement of it did not.
> The restatement here was a docstring, which is the one kind that a reader trusts most and a gate
> reads least.

### And the gate found a second thing on its first run

**`CAD_BRIEF.md` called Gen5 "the measured baseline", twice.** That phrase is the first entry in
`check_public.py`'s withdrawn list — *nothing in this project has been built, fired or measured,*
**E4** — and it had been sitting in a document that `THESIS_MANIFEST` exports to a public
repository. **It was never caught because the file was not on the list.**

### Corrected. Propagated 2026-08-22

All three files are corrected in place with dated notes naming what they replaced; nothing is
deleted. **`check_public.py` now checks thirteen surfaces instead of ten** — `cad/README.md`,
`CAD_BRIEF.md` and `cad/build_gen6.py` are added — **against twenty-seven withdrawn claims instead
of twenty-two**, the five new ones being ADR-034's superseded design point: the 11.25 L, 7.65 L and
9.55 L reservoirs, a 50 bar charge, and the 30.54 m/s zero-friction velocity. **Fifteen historical
passages are explicitly allowed**, each naming the file, the pattern and why that occurrence is a
correction quoting what it corrected.

**What this does not fix.** The gate is a pattern list, so it catches values it has been told
about. **The general case — every live document that restates a parameter — is still not
mechanically guarded**, and `check_crossrefs.py` only covers results files. *That gap is real and
is recorded here rather than claimed closed.*

### P108. Gen6's exit angular rate misses the tip-off band by 7.4x, and the input that decides it is bore straightness: CRITICAL, NEW 2026-08-22
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — retest the guided-contact solver on A69's CORRECTED continuous centreline, then price the land-separation trade against its 400 mm admissibility ceiling


**[A67](validation/A67_guided_contact.md) ran on 2026-08-22 — six of nine — and band 5 is the
finding.**

| | |
|---|---:|
| Exit angular rate at the nominal point | **14.845 °/s** |
| The band, from [A38](validation/A38_tipoff_at_gen6.md) band 2 and [A23](validation/A23_tipoff_release.md) | **2.0 °/s** |
| **Miss** | **7.4×** |
| 3σ under the declared tolerance brackets | **52.33 °/s — 26×** |
| Median of 271 good Monte Carlo samples | **19.39 °/s** |
| Samples inside the band | **none** |

### Why the record said the opposite until today

**A38 answers the cradle and A67 answers the bore, and both are right about what they model.**
A38's residual angular rate at force removal is **exactly zero** for every clearance A23 tabulated
— the rattle settles in 26 ms against a stop while the gas is still holding the payload.
**Then the payload spends 0.42 s crossing eight metres of a bore that is not straight**, and
acquires an angular rate the cradle model has no way to see.

> **Kill criterion 4's Gen6 answer has been quoted against the wrong 27 milliseconds.**
> [`KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) threat 4 already said *"not demonstrated"* and
> *"nothing models the 8 m of guided travel after the cradle"* — [P103](#p103). **This is what was
> behind that sentence.**

### The input that decides it is not the one the programme has been chasing

**Sobol total-order indices over 288 samples**: bore straightness **0.894**, land separation
**0.257**, payload CG offset 0.175, **seal friction 0.141**, force-line eccentricity 0.108,
clearance 0.099, restitution 0.086.

**[P67](#p67) owns 93.4 % of the *velocity* dispersion and is fourth here.** The quantity that
decides whether the satellite leaves straight is **the straightness of eight metres of tube** — a
manufacturing property that appears in no document in this repository. *`docs/MANUFACTURING.md` is
a Gen5 document and does not contain a bore.*

### What has been ruled out already

**Land separation does not rescue it.** A67 band 8 swept 40–400 mm: the best clean point is
**10.219 °/s at 200 mm** and the worst is 14.845. **No piston geometry in the swept range reaches
2.0 °/s**, and longer lands trade angular rate against a peak contact force the model cannot yet
resolve in the tails.

### What would close it, in order

1. **Couple the tube's own deflection in.** [A59](validation/A59_tube_structure.md) requires seven
   supports at 1.0 m and models no resulting shape; A67 declares a straightness bracket instead.
   **Band 9 has just made that the most important input in the model**, so a declared bracket is no
   longer good enough. *This is computation and it is the next run.*
2. **Then sweep the straightness a real 8 m bore can actually hold**, against published
   manufacturing capability rather than a bracket — honing, skiving, segmenting, support pitch.
3. **Then decide.** If no achievable straightness reaches 2.0 °/s, the honest outcomes are a
   shorter stroke, an actively guided carriage, a different release concept, **or a declared
   payload tip-off environment that is not 2.0 °/s** — and the last of those is a product decision
   that must be taken as one, not by widening a band.

**The 2.0 °/s band is not being moved.** It is the flown deployer figure, it was declared before
A38 and before A67, and **a band that moves when a model fails it is not a band.**

### What conditions this entry

**A67 band 3 failed and [A68](validation/A68_contact_law.md) measured what that cost.** LN
under-damps by 40 % at the nominal restitution — χ = 0.3825 against an identified 0.6348 — and
**the same VOLLEY case gives 14.845 °/s under LN and 8.954 under Hunt–Crossley. A68 band 6 fails
at a 65.8 % model-form spread.**

> ### The number is restated, 2026-08-22. The finding is not withdrawn.
>
> **14.845 °/s is not a physical prediction.** The honest statement is: **the first full-bore
> contact model puts Gen6's exit angular rate between roughly 9 and 15 °/s against a 2.0 °/s band,
> with the spread between two credible contact laws accounting for most of the range, and bore
> straightness as the dominant sensitivity.**
>
> **What survives every objection:** *both* laws miss the band, by **4.5×** at the friendlier one;
> A67 band 9's ranking is a variance attribution and is not a contact-law property; and
> [P109](#p109)'s admissibility constraint — the harder finding — needs no contact model at all.
>
> **What does not survive:** quoting 14.845, or 7.4×, as settled. *A67's band 5 verdict stands as
> recorded; what is corrected is the use made of its number.*

### P109. ~~At a one-kelvin gradient the Gen6 bore does not admit its own piston~~ **WITHDRAWN**: was CRITICAL, CORRECTED 2026-08-22
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> ## WITHDRAWN the same day it was opened — [P110](#p110).
>
> **This entry rested on a centreline that kinked a continuous tube at every support.** On the
> corrected continuous solve the sagitta at 1 K over 120 mm is **2.39 µm, not 37.3** — agreeing
> with the closed form κL²/8 to 0.2 % — against **25 µm** of radial clearance. **The piston clears
> at every gradient tested to 5 K.**
>
> **What survives, and it is an order of magnitude weaker:** **400 mm lands are inadmissible at
> 1 K** and 200 mm at 5 K. A67 band 8's "longer lands reduce tip-off" therefore has a ceiling —
> at 400 mm, not at 120. *That is the only part of this entry that stands, and it is a trade limit
> rather than a design failure.*
>
> **The text below is the original entry and is wrong.** It is kept because a withdrawal needs
> something to withdraw.


**[A70](validation/A70_guided_contact_derived.md) asked the question that comes before tip-off:
can the piston physically pass through the bore it is in?**

**Three-point sagitta of [A69](validation/A69_tube_centreline.md)'s computed centreline over the
piston's own length, against a nominal radial clearance of 25.0 µm:**

| Across-diameter gradient | 40 mm lands | 80 mm | **120 mm — nominal** | 200 mm | 400 mm |
|---|---:|---:|---:|---:|---:|
| **0 K** | 0.0 | 0.2 | **0.4** | 1.2 | 4.4 µm |
| **0.5 K** | 6.4 | 12.7 | **18.7** | **30.7** ✗ | **56.5** ✗ |
| **1.0 K** | 12.8 | **25.1** ✗ | **37.3** ✗ | **60.4** ✗ | **109.5** ✗ |
| **2.0 K** | **25.7** ✗ | ✗ | ✗ | ✗ | ✗ |

**At the design point — 120 mm lands, 50 µm diametral clearance — a one-kelvin gradient across the
tube's 17.8 mm diameter puts the bore 37.3 µm out of line over the piston's length. That is 1.5×
the radial clearance.** At 2 K nothing passes at any land separation tested.

### Why this is harder to argue with than a tip-off number

**It needs no solver.** No contact law, no integrator, no friction, no restitution, no
eccentricity. **It is the geometry of a rigid body in a curved tube**, computed from A69's beam
solve and `gen6_drive.bore_mm`, with a three-point construction that does not differentiate
anything. *[P108](#p108) depends on a contact model whose own model-form spread is **65.8 %**
([A68](validation/A68_contact_law.md) band 6). This does not.*

### And the trade runs the wrong way

**[A67](validation/A67_guided_contact.md) band 8 found longer lands reduce exit angular rate** —
10.219 °/s at 200 mm against 14.845 at 120. **Longer lands jam sooner**: 200 mm is inadmissible at
half a kelvin and 400 mm is inadmissible there too. **Angular constraint and geometric
admissibility pull in opposite directions**, and nothing in this repository had priced that
because nothing had computed the centreline.

### Where the gradient comes from, and it is not a wild number

**A69**: the bow is `κ = α ΔT / D` at `α = 23.6e-6 /K` and `D = 17.805 mm`, so **one kelvin across
the diameter is a curvature of 1.33e-3 /m** — enough to move the line 0.166 mm over a single 1.0 m
support span. **A thin-walled aluminium tube 8 m long in orbit, with the sun on one side, is not a
place where a one-kelvin gradient is unusual.** [A58](validation/A58_chamber_thermal.md) puts the
gas at **238 K** every shot, so there is also an internal gradient the tube sees from the inside.

**What has never been computed is the tube's actual gradient**, and that is
[E-thermal work](docs/COMPUTATIONAL_CLOSURE.md) rather than a bracket.

### What would close it

**A design, and it is design rather than repair.** Every one of these is a free variable that has
never been chosen against this constraint:

1. **The gradient itself** — a thermal model of the tube in orbit, then coatings, wrapping or a
   heater. *This is the lever with the most authority and the least mass.*
2. **Clearance** — 50 µm diametral is a declared assumption with no source. A larger clearance
   admits more curvature and costs tip-off.
3. **Land separation** — the piston has no length in any file; the trade against A67 band 8 is now
   two-sided and has an optimum.
4. **Support pitch** — sagitta goes as the span squared. Halving 1.0 m quarters it.
5. **A piston that is not rigid** — two lands on a compliant or articulated carrier, which is what
   long-stroke pneumatic practice actually does.

**Nothing is being changed here.** A70 explicitly changed no parameter to make a band pass, and the
redesign belongs in a run of its own with its bands declared first.

> **This does not say Gen6 fails.** It says **this configuration** does not admit its own piston at
> a gradient nobody has computed, and that **five design variables have been carried this far
> without anyone knowing there was a constraint on them.**

### P110. A69's thermal centreline kinked a continuous tube at every support, and two bands were hardcoded PASS: CRITICAL, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**Found by an independent audit of [A69](validation/A69_tube_centreline.md) and
[A70](validation/A70_guided_contact_derived.md), hours after both were published.**

### The physics defect

`orbital_centreline()` built the thermal bow as **an independent parabola in each support span,
reset to zero at every support**. A uniform across-diameter gradient imposes a uniform curvature
on the **whole continuous member**. Imposing it span-by-span put a slope discontinuity of
**κ × span** at each of seven supports — **it kinked a continuous aluminium tube seven times**.
The supports are transverse constraints; they are not cuts.

**What it cost, at a 1 K gradient over the nominal 120 mm land separation:**

| | Sagitta |
|---|---:|
| As published | **37.3 µm** |
| **Corrected, continuous solve** | **2.39 µm** |
| **Independent closed form, κL²/8** | **2.386 µm** |
| Radial clearance | 25.0 µm |

**15.6× too large, and the corrected value agrees with the closed form to 0.2 %.**

> ### [P109](#p109) does not survive it
>
> P109 claimed the bore does not admit its own piston at 1 K. **On the corrected model the piston
> clears at every gradient tested to 5 K, with a factor of 2 in hand.** *That entry is withdrawn
> as stated and what remains of it is an order of magnitude weaker.*

### The verification defect, and it is the more general one

**Two bands were `= True`.**

- **A69 band 4** — *"a continuous centreline is returned and exported"* — was `b4 = True`. **The one
  band that would have caught the kink was the one that was not computed.**
- **A70 band 6** — energy closure — was `b6 = True` with the dynamics disabled, so **no energy
  balance was evaluated at all**. A70's recorded verdict is corrected to **1 PASS, 5 NOT
  EVALUABLE**.

**A69 band 7 was not hardcoded but was not a centreline either**: it added two scalar peaks. It now
takes the peak of solved combined centrelines, and **on that basis it fails** — 5.30 mm at 5 K,
outside the bracket A67 swept.

### Corrected. Propagated 2026-08-22

The gradient enters as an **eigenstrain on the continuous beam**, `f_th = ∫Bᵀ EI κ dx =
EI κ [0, −1, 0, +1]`, solved **together** with the support offsets. **Band 1 gains a second
limiting case** — a simply supported span under uniform imposed curvature against `κL²/8`, which
returns **0.0000 %**. **Band 4 is four computed conditions**: finite displacement, finite slope,
slope jump below 1 % of the peak slope, and peak curvature within 5× the imposed. It returns
**0.7454 %** and a curvature ratio of **1.00**.

**A third conclusion is withdrawn.** A69 ranked thermal bow above manufacturing straightness —
**with manufacturing straightness absent from the ranking.** It is now a declared superposable
input, and the honest statement is that **the ranking cannot decide between them.**

### What this says about the gate set

**Every repository gate passed while the physics was wrong**, and they would have passed on any
value of that sagitta. **The gates check that the record is consistent. They do not check that a
model is right**, and the verification language is corrected to say so.
[`tools/check_bands.py`](tools/check_bands.py) is the narrow thing that can be automated: it finds
band verdicts that are assigned rather than computed.

### P111. A68 attached Hunt–Crossley's name to a relation they did not write, and reasoned from the attribution: HIGH, CORRECTED 2026-08-22
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record


**[A68](validation/A68_contact_law.md) implemented `χ = 3(1−e)/(2e)` and called it *"Hunt–Crossley's
own coefficient"*, adding that it *"does not assume e → 1"*. Both statements are wrong.**

**Hunt & Crossley (1975)**, *Coefficient of restitution interpreted as damping in vibroimpact*,
J. Appl. Mech. **42**(2), give the damping factor to first order in (1−e) as
**λ = 3k(1−e)/(2v⁻)** — **χ = 3(1−e)/2, with no `e` in the denominator.** It is a first-order
relation and it degrades exactly as Lankarani–Nikravesh does: **+9.7 % at e = 0.7 and +173 % at
0.2**, against LN's +13.7 % and +236 %.

**The relation A68 implemented belongs to the later corrected family**, whose members carry `e` in
the denominator. **Its primary sources have not been read** — publisher records were not
retrievable — so it is renamed **`MOD`, for its form, not for an author**, and the run sheet says
what is and is not known about where it comes from.

> **The defect is not the formula, which works: it returns −0.4 % at the nominal restitution.**
> **The defect is that a name was attached to it and then used as an argument.** *"HC does not
> assume e → 1"* was reasoning from a label, and the label was wrong. **[P22](#p22) is the entry
> about citing what has not been read; this is citing what has not been checked.**

### And the second claim was also not what it was presented as

**A68's `ID` root-finds the damping coefficient using the same fixed-step RK4 solver until that
solver returns the requested restitution.** That is **parameter identification**. A68 reported it
under *"restitution recovery"* alongside the two derived relations, where it reads as verification
of the impact model. **It cannot be: the solver is being asked to agree with itself.**

**Corrected. Propagated.** Something genuinely independent is added. `impact_ivp()` solves the same impact
with **scipy's adaptive implicit Radau integrator** at `rtol = 1e-11` with event-terminated
separation — a different code path, order, step control and stiffness treatment. **It agrees with
the RK4 result to 0.000 % at every identified coefficient.** *That is the verification. The
identification is a fitting step and is now labelled as one.*

### What survives

**Band 6 still fails at 65.8 %** and the three correctly-named formulations give **14.845, 12.390
and 8.954 °/s** on the same VOLLEY case. **The conclusion — that the magnitude of Gen6's tip-off
problem is model-form-limited and unresolved — is unchanged.** What changes is that it now rests
on three formulations that are named for what they are.

### E30. The architecture trades twelve parallel one-shot mechanisms for one twelve-cycle series mechanism, and nothing estimates its reliability: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `FLIGHT_OPS` — published dispenser deployment counts and failure records


**Raised in review, 2026-08-10, and it is the strongest structural criticism this design has
received.**

A spring dispenser is **twelve independent one-shot mechanisms in parallel**. One failure costs
**one** satellite. VOLLEY is **one mechanism in series with itself, cycled twelve times**: the
sled, stator, bank, sequencer and brake serve every shot, and the escapement and retention gate
cycle twelve times each. A failure at shot *k* forfeits shots *k* through 12.

**That is a real and unfavourable structural change, and no amount of component quality removes
it.** It is arithmetic, not opinion:

| Per-shot p (or per-unit q) | VOLLEY satellites | Spring satellites | VOLLEY fleet-years | Spring fleet-years |
|---:|---:|---:|---:|---:|
| 0.99 | 11.25 | 11.88 | 23.74 | 16.78 |
| 0.95 | **8.73** | 11.40 | 18.44 | 16.10 |
| **0.935** | 7.96 | 11.22 | **16.81** | **15.84** — break-even |
| 0.90 | **6.46** | 10.80 | 13.63 | 15.25 — **spring wins** |
| 0.80 | 3.73 | 9.60 | 7.86 | 13.56 |

**The two crossover numbers are the answer to "what is the risk/reward ratio":**

- To match a 0.99-reliable spring **on satellites delivered**, VOLLEY needs per-shot
  **p = 0.9985**. For a twelve-cycle electromechanical system with no flight heritage, that is
  not a realistic target.
- To match it **on delivered orbital life**, VOLLEY needs only **p = 0.9347** — because each
  satellite it *does* deliver is worth **1.495×** a spring-deployed one (2.111 yr against
  1.412 yr at 450 km).

**The gap between 0.9347 and 0.9985 is the risk/reward ratio, and it is the whole argument.**
VOLLEY can afford to lose satellites and still deliver more total mission value — but only above
about **93.5 % per-shot reliability.** Below it, the spring wins outright.

**And a correction the project should make to itself.** The headline **7.52× lifetime extension**
is a ratio of *gains* (+61.8 % against +8.2 %). On **delivered orbital life** the ratio is
**1.495×**. Both are true; the second is the one that governs a risk-weighted comparison, because
a satellite that is never released delivers nothing. **The 7.5× figure flatters in exactly the
comparison a reviewer will make.**

**What is missing, and it is the finding.** **Nothing in this repository estimates p.** There is
no FMEA, no fault tree, no parts count, and no cycle-life test for the escapement, the gate or
the sled. `grep -ri "failure point"` returns nothing. **The project therefore cannot say which
side of 0.9347 it is on**, which means it cannot presently answer whether it beats a spring at
all.

**What would close it:** a parts count and an FMEA to the level of naming every element whose
failure forfeits the remaining manifest; a stated single-failure-loses-N figure; cycle-life tests
for the three cycling mechanisms; and a per-shot p with the reasoning behind it. Adjacent to
**P28** (brake), and it subsumes the specific jam case raised as review item 22.

> **The FMEA half was done 2026-08-10** — [`docs/FMEA.md`](docs/FMEA.md),
> `analysis/fmea.py`. **Nine of thirteen elements forfeit the remaining manifest on a single
> failure, against zero for a spring dispenser, and nine shared elements over twelve cycles is
> 108 chances to fail.**
>
> It converts this entry into a **requirement**: to beat a 0.99-reliable spring on delivered
> orbital life, each element needs **r ≥ 0.99326 per cycle** (surviving the campaign with
> probability 0.922). To match it on **satellite count** needs **r ≥ 0.99984**, which is not a
> realistic target — **VOLLEY should not be sold on satellite count.**
>
> **Segmentation analysed 2026-08-10** (`analysis/segment_redundancy.py`): a dead segment is a
> length the sled **coasts over**, not a stopped machine, so at four segments a later failure
> still exits at **14.19 m/s — 86.6 % of nominal and 1.41× a spring**. **The breech segment is the
> exception**: no force acts on a stationary sled, so if the first segment dies the shot never
> starts. **The stator is therefore two elements, not one** — three of four stator failures are
> survivable at four segments, eleven of twelve at twelve — and the cheap design action is to
> duplicate or overlap the breech segment.
>
> **This entry stays LIVE because r is still unmeasured.** No cycle-life test exists for the
> escapement, the gate or the sled, and that is metal rather than computation. The jam case of
> review item 22 is answered structurally — it is one of nine ways to lose the manifest, not a
> special case — but there is still no recovery mode and no accepted-risk statement.

**Mitigations that exist but are unquantified:** the winding is segmented, so losing one segment
degrades rather than stops (`paper.tex` §VII, and P29 closed the modelling half). The retention
gates are per-cassette, so one gate failure forfeits six rather than twelve. **Neither has been
credited in a reliability model because no reliability model exists.**

### E31. The two ConOps have different launch-interface compliance positions, and nothing distinguishes them: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HOST_DATA` — the launch-interface position of an actual provider


**Found by the ICD survey, 2026-08-10.** See [`docs/ICD_COMPLIANCE.md`](docs/ICD_COMPLIANCE.md).

The review question was whether a published rideshare interface permits deployment at 16.388 m/s.
**It does** — §3.2.2 of the Rideshare Payload User's Guide, Version 10 (September 2024), caps
separation at 1.0 m/s and then exempts containerised CubeSat deployments explicitly, with no
numeric ceiling. **That question is closed and the premise survives.**

**What the survey found instead is that VOLLEY's two configurations are not equally compliant, and
the repository has always treated them as one product.**

| | Dedicated: VOLLEY as a dispenser on the launch vehicle | Hosted: VOLLEY on a separated stage (ADR-024) |
|---|---|---|
| Deployment class | primary, from the launch vehicle | **secondary deployment** — a deployed object deploying sub-payloads |
| Seven-day hold before first shot | **no** | **yes** |
| Active attitude control required at every release | yes | yes |

**The seven-day hold is the expensive one.** E28 found campaign mission life at a real POEM
altitude is about a month — two GMAT runs at 350 km reentered at **36 and 29 days**. **Seven days
is 20–24 % of the window, spent before the first satellite leaves**, and ADR-024 adopted the
hosted configuration as the product framing without this cost in view.

**And it compounds with E29.** The same document requires that *"all secondary deployments must be
performed while under active attitude control. Deployments in uncontrolled directions or during
Payload tumbling are not allowed."* E29 computes wheel saturation at roughly **shot four of
twelve** for a 50 mm thrust-line-to-CoM offset. **After that point the remaining deployments are
not merely degraded, they are non-compliant** — an engineering problem converted into an approval
problem.

**What would close it:** a compliance matrix per configuration, a campaign timeline for the hosted
case that carries the seven-day hold against E28's reentry window, and the CoM-alignment
requirement E29 already asks for — which is now a compliance requirement rather than an
engineering preference.

**Two further items from the same document, neither in any analysis here:**

1. **A dispenser quasi-static case of 10 g axial and 17 g lateral (RSS).** The structural work in
   A18 and A22 is random-vibration and axial-dominated; **lateral is the larger number** and the
   retention gates are least studied in that axis.
2. **An exit-direction requirement** that deployed payloads leave through the +X face of the
   allowable payload volume. VOLLEY fires along its track axis, which on a radial ESPA port is not
   the launch vehicle's +X. Whether the deployer's own volume is the governing frame is an
   interface-review question and is unanswered.

**The survey is one document deep.** No claim about the market should be made from it, only about
this interface at this revision.

### E32. Nothing inhibits the drive during the ascent pressure transit, and a fault there would break down: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — design the ascent inhibit and its fault logic


**Found answering review item 26, 2026-08-10.** `analysis/paschen_multipaction.py`.

**Ordinary operation is safe, by a margin that does not depend on geometry.** The 96 V bus is
**3.41× below air's 327 V Paschen minimum**, and below a gas's *minimum* no voltage breaks down at
any pressure-distance product. Multipaction is the wrong regime by **2.5 × 10⁴** — the converter
gives f × d = 40 Hz·m against a ~10⁶ Hz·m threshold. **Neither mechanism is credible in normal
use, and review item 26 is answered.**

**The fault case is not safe.** The winding is **19.70 µH at 373.2 A, storing 1.37 J per phase**.
A healthy bridge freewheels through its antiparallel diodes and clamps near the bus; an
**open-circuit fault has no such path**:

| Interrupted in | Induced | vs air's 327 V minimum |
|---:|---:|---|
| 1 µs | **7,351 V** | **exceeds by 22×** |
| 10 µs | **735 V** | **exceeds** |
| 100 µs | 74 V | below |

For a 1 mm gap, air reaches its Paschen minimum at **760 Pa (~5.7 Torr)**, a pressure the vehicle
passes through on **every ascent**.

**The defect is that nothing prevents the coincidence.** There is no requirement anywhere in this
repository that the bank be uncharged or the winding unenergised during ascent. The machine has no
reason to be energised then; the rideshare guide read for E31 calls out **power inhibits** as
separately-verified testing; and **the requirement is simply not written down.**

**What would close it:** a stated inhibit — *the bank shall be uncharged and the winding
unenergised while the vehicle transits the Paschen-critical pressure band* — carried into the
qualification plan as a verified inhibit, plus a clamping requirement on the bridge so that a
fault during *operation* in vacuum has a defined current path. Neither exists.

**What this does not need:** a CFD venting model. The conclusion turns on the bus sitting below a
gas constant, which no depressurisation model changes.

### E33. Magnet tolerance leaves a residual dipole that saturates the host's wheel in days, with the machine idle: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — magnet tolerance and the residual dipole


**Review item 11, computed 2026-08-10.** `analysis/residual_dipole.py`.

**The reassuring half first: an ideal Halbach array has no net moment.** Summing all 56 blocks
over seven whole wavelengths gives **3.5 × 10⁻¹⁴ A·m²** — numerically zero, as it must be, because
the magnetisations rotate through 360° and cancel.

**Tolerance does not cancel.** With class figures for sintered NdFeB — **±2 % on Br, ±2° on
magnetisation axis**, 4000 Monte-Carlo trials over 56 blocks:

| | Residual dipole |
|---|---:|
| median | **0.77 A·m²** |
| 95th percentile | **1.56 A·m²** |
| 99th percentile | **1.92 A·m²** |

**This is at or above typical small-spacecraft magnetic cleanliness allocations**, which commonly
sit in the 0.1–1 A·m² range.

**What it does to the host, in a 30 µT field at 450 km:**

| Residual | Torque | H per orbit | **Wheel saturated in** |
|---|---:|---:|---:|
| median | 2.30 × 10⁻⁵ N·m | 0.129 N·m·s | **7.5 days** |
| 95th | 4.69 × 10⁻⁵ N·m | 0.263 N·m·s | **3.7 days** |
| 99th | 5.76 × 10⁻⁵ N·m | 0.323 N·m·s | **3.0 days** |

**against a 15 N·m·s ESPA-class wheel, and this happens whether or not the machine ever fires.**

**Three independent paths now lead to the same failure**, and this is the one that does not
require a shot:

1. **E29** — the shot's mechanical angular impulse saturates the wheel at about **shot four**;
2. **E33** — the residual dipole saturates it in **3–7.5 days**, idle;
3. **E31** — and once attitude authority is gone, remaining deployments are **not compliant**,
   not merely degraded.

**Against E28's 29–36 day campaign window and E31's seven-day hold, the magnets alone can exhaust
the wheel before the campaign finishes.**

**Worst case, deliberately.** No orbital averaging is credited. A body-fixed dipole in a rotating
geomagnetic field averages partially, so these are an **upper bound** — but the bound is the number
that decides whether the ACS can hold a campaign, and no lower bound has been computed either.

**What would close it, and the fix is cheap.** **Magnet screening and matched-set assembly**: measure
each block's moment and axis on receipt, sort into matched sets, and place them to cancel. That is
a manufacturing procedure, not a design change, and it is the standard answer to exactly this
problem. **B-1 already buys a teslameter and eight blocks**, so the screening method could be
demonstrated on the bench article at no additional hardware cost. A compensating magnet is the
fallback. Neither is specified anywhere.

### E34. The brake dumps 18.5 kN into a structure holding eleven stowed satellites, eleven times: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — a shock response spectrum at the cassette interface


**Review item 12, 2026-08-10.**

**Release is the benign half and A23 already showed why:** separation happens **12.2 ms into
coast, at zero commanded force**, so the payload leaves with no force step. The only shock sources
are gate withdrawal and stiction break, both small.

**Brake engagement is not benign, and the payload is the wrong thing to worry about.** By then it
has gone — but **eleven satellites are still in the cassettes**, and they see the arrest through
the structure:

| Arrest | Force into the track | Stops in | Over |
|---:|---:|---:|---:|
| 50 g | 4.6 kN | 201.7 mm | 28.7 ms |
| 100 g | 9.3 kN | 100.9 mm | 14.3 ms |
| **200 g** — the design cap | **18.5 kN** | 50.4 mm | **7.2 ms** |

The sled enters the brake at **14.07 m/s carrying 935 J**, and `cad/parameters.json` sets
`arrest_g_cap: 200` — the tapered pole entry exists specifically to limit deceleration to it.

**A stowed 3U's qualification case is the 25 g CDS cap and the launch random-vibration
spectrum.** It is **not** a 200 g mechanical shock delivered through its own dispenser, **repeated
eleven times**. Nothing in this repository computes what actually reaches a cassette — there is no
shock response spectrum anywhere; `grep -ri "shock spectrum"` returns nothing.

**What would close it:** a shock response spectrum at the cassette interface for the 200 g arrest,
compared against a stated payload shock qualification level, and — if it does not close — either a
lower arrest cap (the 50 g row costs 202 mm of run-out, which the envelope may not have, P9) or
isolation between the brake reaction and the cassette mounts. **Adjacent to P28**, which already
records that the regen stator and the eddy fin do not both fit the arrest section.

### E35. The payload's field exposure is a design variable nobody varied, and fixing it would make the product claim true: NEW 2026-08-10
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — vary the payload field exposure as a design variable


**Review items 16 and 14, computed 2026-08-10.** `analysis/mover_separation.py`.

The payload rides **on** the sled, 20 mm from the Halbach faces, and `docs/PAYLOAD_ENVIRONMENT.md`
concedes two losses because of it: a magnetometer-carrying payload cannot use its magnetometer,
and **soft-magnetic parts leave permanently magnetised** — *"the satellite leaves permanently
altered."*

**Nobody had asked what happens if the payload simply sits further away.**

| Standoff | \|B\| | × magnetometer FS | × Earth |
|---:|---:|---:|---:|
| **20 mm — today** | 44.2 mT | **442×** | 983× |
| 100 mm | 306 µT | 3.1× | 6.8× |
| **251 mm** | 90 µT | **0.90× — usable** | 2.0× |
| **400 mm** | 23.7 µT | 0.24× | **0.53× — below Earth's own field** |

(The 251 mm crossing reproduces `PAYLOAD_ENVIRONMENT`'s own figure, which is the cross-check that
the model is the same one.)

**At 400 mm the satellite sees less than Earth's field, and both conceded losses disappear.**

**Why this is more than an optimisation.** The project's central claim is that the satellite is
never modified. **Item 9 established that it is** — magnetically, invisibly, and without the
customer's knowledge. That makes the current configuration the *worst* of the available options,
because it is the only one where the modification is undisclosed:

| | |
|---|---|
| Today | modified, invisibly, unspecified |
| With separation | **genuinely unmodified** |
| With a declared magnetic-cleanliness spec | modified, **knowingly**, to a written interface |

**Separation is what makes the product claim true**, rather than what makes it faster.

**Perpendicular separation is unaffordable** — the machine is 530 mm wide. **Longitudinal is**, and
it is what a tug-and-carriage architecture gives for free (**PII-15**), which also halves the
acceleration zone and therefore bears on **P9**.

**What would close it:** either a longitudinal-separation layout carried into `cad/parameters.json`
with its field recomputed at the real payload station, or — if separation proves unaffordable — a
**declared magnetic-cleanliness zone in a payload interface document**, which does not exist.
ADR-010 covers mechanical mounting only, and **E29 already asks for that same document for an
unrelated reason.**

### E28. Campaign mission life at a real POEM altitude is about a month, and is not modelled: MODELLED 2026-08-16 by A50, STILL OPEN
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — campaign mission life at a real deployment altitude


**Found by A15, and only because two GMAT runs stopped early.** R2 (350 km, 55.2 deg) and R3
(350 km, 9.6 deg) never reached the declared 90 days: their twelve satellites **reentered**, R2
halting at **36 days** with all twelve between 182 and 190 km, R3 at **29 days** between 103 and
115 km. Only the 450 km case ran the full 90.

**Nothing in this project models campaign mission life.** `astro.py` computes a lifetime
*multiplier* (x1.62) for a single boosted satellite against an unboosted one, which is a ratio and
not a duration. The deployment story -- twelve satellites, spread in altitude and plane -- has
always been told without saying how long the fleet exists.

**At 350 km that duration is about one month**, and the plane spread this project is pleased about
develops *faster* there, 365 deg in 29 to 36 days against 367 deg in 90 at 450 km, **because the
same drag that separates the nodes is what pulls the satellites down.** The two are not
independent effects to be traded; they are the same effect.

**Why it matters beyond the analysis.** `docs/MARKET.md`, `SUMMARY.md` and `paper.tex` Sec. VII
all present POEM as the flown precedent, and POEM missions have operated near 350 km. A
twelve-satellite campaign there is a **month-long** product, which is materially different from
what a reader assumes when the analysis is quoted at 90 days.

**What would close it:** a stated campaign mission life per host altitude, computed rather than
assumed, with the customer-facing consequence written where the host is described rather than only
in a run sheet. The GMAT runs already contain the data for 350 and 450 km.

> **Not all of these weigh the same.** Three of the entries below are threats to whether the
> machine has a reason to exist rather than engineering work, and they are hard to see in a
> numbered list. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) separates them, with the value
> at which each becomes fatal.

## E: Unsolved engineering


> **Modelled 2026-08-16 by [A50](validation/A50_campaign_altitude.md), and it stays open because
> the model disagrees with the runs that raised this entry.** A50 gives **70.6 days at 350 km**
> against the **29 and 36** these GMAT runs observed — **optimistic by roughly two**, for the
> reason **P16** already names: `astro.py` uses a *static* atmosphere and cannot represent the
> solar-activity variation that actually kills a satellite at that altitude.
>
> **What A50 does establish, as upper bounds:** satellite life is **476.6 days at 450 km** and
> repositioning three 50 km shells costs **≈ 55 m/s**, inside every host budget A20 swept. **Days,
> weeks and months are all purchasable from 450 km up.**
>
> **And it collapses this entry's central trade.** E28 framed altitude as a choice between plane
> spread and mission life. Across 350 → 450 km the 90-day spread moves **47.1° → 44.6°, about 5 %,
> while satellite life changes by 6.7×.** At the shell spacing this architecture uses, **spread is
> nearly altitude-independent and life is not — so there is no trade, and the design rule is
> simply to go higher.**
>
> **This entry closes when the decay model is checked against a variable atmosphere**, not before.


### E1. Three-dimensional field closure: 2-D HALF CLOSED 2026-07-29 by A1
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **A1 has run.** A meshed 2-D magnetostatic FEM (scikit-fem P1, 141 k elements, gmsh) gives
> **K_t = 11.228 N per kA/m against the model's 11.22 (a ratio of 1.0007**) with force
> ripple 1.25 % against 1.26 %. Midgap peak and winding mean both land at ratio 1.001.
> **The thrust band, the one that matters, is met.**
>
> What remains open is the 3-D half: end effects on a 340 mm array of finite 90 mm depth.
> P21 is that limitation showing up directly, the 2-D model overestimates far field because
> it has infinite depth. That needs A2.
>
> **A2 ran 2026-08-10 and closed the 3-D half.** The field was never 2-D — magpylib has always
> used the real 90 mm depth. The 2-D assumption was in the *thrust integral*, which sampled
> `B_y` at z = 0 and multiplied by the full depth. Resolving it costs **4.42 % of K_t**
> (11.0258 → 10.5386), which is **P46**, computed and held rather than applied. Band 5 also
> settled a background assumption never stated: seven wavelengths is enough for the array
> centre to be effectively infinite, to 0.01 %.
>
> **E2's half is NOT closed by this.** A2 band 4, an independent `getdp` 3-D FEM solve, was not
> run, so the depth-resolved number is still analytic superposition.
`motor_model.py` resolves the winding in 2-D. End effects of a few percent on Kt remain
uncomputed. This is the declared close-out task for the electromagnetic model. The
magnetostatic package now exists, `analysis/femm/emocd_cross_section.dxf` plus
`analysis/femm/FEMM_RUN_SHEET.md` (analysis A1), which supersedes the older
`docs/FEMM_Run_Sheet.md`; the acceptance band in that older sheet predates the
winding-resolved model and should not be used. **Nothing has been run.** A1 closes the
2-D half; the 3-D end effects still need a 3-D solver (Elmer or GetDP are the free
options). Acceptance band declared in `validation/A1_field_femm.md`.

### E2. No FEA confirmation of anything: CLOSED
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **Closed 2026-08-13 by A2 band 4.** A `getdp` 3-D magnetostatic solve — reduced scalar
> potential, 274,105 degrees of freedom on a 315,370-node tetrahedral mesh, geometry imported
> from `motor_model` — agrees with magpylib on the double-sided midgap fundamental to
> **0.059 %** (0.70182 T against 0.70140 T). The objection this item raised was that the field
> had only ever been checked analytic-against-analytic; it has now been checked against a
> meshed PDE solve in three dimensions. `validation/fem3d/`.
>
> **Two earlier FEA results.** A4 (CalculiX, structural) ran 2026-07-28. **A1 (magnetostatic,
> 2-D) ran 2026-07-29** and agreed to 0.07 %.
>
> **What is still not FEA-checked, tracked elsewhere:** no FEA of the track, the brake, or the
> cassette structure. Those belong to the structural items, not to this one.
The field cross-check is analytic-vs-analytic (both magpylib and the wave model assume
ironless geometry, where superposition is exact). That is a genuine check of the wave
model but is NOT independent confirmation from a different physical method. Two analyses
are specified and neither has been executed: **A1** magnetostatic (E1 above) and **A4**
sled-chassis structural, which is what P5 and P8 are waiting on. Both, plus A5, A8, are
written up with pre-declared acceptance bands in `validation/`, and A5's GMAT toolkit is
built (`validation/gmat/`) though not yet run. A8 (pulse-power, E17) is
the cheapest of them and needs no CAD, no mesh, and no licence.

### E3. Masses are parametric and unchecked against vendor data
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — select components from public vendor data instead of parametric masses

CAD now exists (`cad/`, nine documents), so the "no CAD" half of this item is closed,
but the mass problem is not. `mass_properties.py` still uses primitive solids with
shell/fill factors, and no component mass is checked against a vendor datasheet;
estimate spread perhaps ±15 %. Fusion-computed masses are **not** a substitute: they use
solid-copper stator, solid-aluminium CubeSats, and steel standing in for NdFeB, which is
why they are deliberately excluded from `cad/parameters.json`. The sled mass (4.86 kg)
propagates directly into the headline velocity (see P5 and P8) and the enclosure,
radiator, and avionics are still missing from the rollup entirely (P10).

### E4. No hardware at any level
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HARDWARE` — build something

> **A protocol now exists, 2026-07-29.** `docs/BENCHTOP_TESTS.md` specifies four sub-scale
> experiments, cheapest first, each closing a named claim with its acceptance band declared
> in advance: a Halbach pair on a gaussmeter (B-1), single-coil thrust against
> K<sub>t</sub> (B-2), capacitor discharge against the pulse model (B-3), and a drop-test
> brake coupon against the plate-drag law (B-4). **B-1 costs roughly the price of two magnets
> and would give this project its first measured number.** Full-scale qualification is
> specified separately in `docs/QUALIFICATION_PLAN.md`. None of it is run, this item stays
> open until something is measured.
>
> **Strengthened 2026-07-30, and the reason is competitive.** The Harbin group
> (`docs/PRIOR_ART.md`) has **built and measured a prototype**; this project has not, and that
> difference is visible to any reviewer. B-1 and B-2's bands were declared before any test but
> *chosen* rather than derived. `validation/bench/bench_predict.py` now derives them, importing
> `verify_field.py` and `motor_model.py` with a guard against geometry drift. Measurement error
> comes out at **4.4 % for B-1's field rows and 13.5 % for B-2's thrust**, against bands of ±15 %
> and ±20 %. The bands do not move, they must also cover model error, which is the thing under
> test, but a failure is now interpretable, because the rig can no longer be blamed for it.
> Two procedural traps were found in the process and are documented in `BENCHTOP_TESTS.md`: a
> two-block bench pair built poles-facing reads **exactly zero field**, and B-2's load cell must
> be sized to the smallest force in the sweep rather than the largest.
TRL 2-3. Nothing has been built, fired, or measured. The velocity, dispersion, and
tip-off claims are all model outputs.

### E5. Host stage properties unavailable
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `HOST_DATA` — host stage propellant, authority and restart constraints

Recoil budgets are parametric across 300-900 kg host classes because no candidate
stage publishes its mass and control authority. Cannot be closed from public data.

### E6. Absolute orbital lifetimes are uncertain
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — uncertainty range from a variable atmosphere, not a single multiplier

Static exponential atmosphere at mean solar activity. Absolute lifetimes swing
severalfold across the solar cycle. The x1.80 ratio was believed invariant and defensible;
**P16 has since falsified the invariance**: GMAT gives 1.73 / 1.78 / 2.07 across low to high
activity. The point value at mean and high activity survives; the invariance does not. `validation/A5_astro_orekit.md` specifies an independent
re-run under GMAT (toolkit built in `validation/gmat/`, Orekit an equally valid
substitute) (different codebases, independently implemented force models) with the band on the ratio and explicitly not on the absolutes. It now also
carries a second leg: reproduce the **measured** decay of 3-5 non-manoeuvring 3U CubeSats
from CelesTrak / Space-Track TLE histories, band 15 % on time-to-decay. Two models
agreeing is weaker than a model reproducing a flown decay, and the flight data is free.

### E7. Velocity dispersion rests on assumed sensor noise
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — select a sensor from public data and use its stated noise

The 0.027 m/s (3σ) result is a closed-loop simulation using an assumed 8 mm/s sensor
sigma and assumed tolerance distributions. No sensor has been selected or characterised.
The separation side of this is specified in `validation/A7_separation_chrono.md`, whose
tip-off band is taken from a flown deployer rather than chosen. **Tightened 2026-07-31 from
5 to 2 °/s/axis**: the band cited NRCSD-E, the external Cygnus deployer, whose 5 °/s its own
publisher calls provisional, while the internal NRCSD that has flown hundreds of times specifies
**< 2 °/s/axis**. Two deployers, not a contradiction, and the band had been set at the easier of
them. See **P30**.

### E8. Brake energy is thrown away — CLOSED 2026-08-10, into P28
> **Status:** `CLOSED` — resolved; see the entry for what closed it

~1.0 kJ per shot dissipated in the fin. Whether any of it is worth recovering (and what
that would cost in mass and complexity) has not been examined since the efficiency
correction.

**It has been examined since, twice, and this entry did not notice.** The premise — "has not been
examined since the efficiency correction" — was false by 2026-08-03.

| | |
|---|---:|
| Sled energy at release | 1.27 kJ |
| **Recovered by regeneration** (A11, eight of eight bands) | **291.4 J**, 23.0 % of sled KE |
| **Reaching the fin** | **934.7 J** — the "~1.0 kJ" above, now exact |
| Efficiency this credit is worth | 2.2 points, 20.99 % net |

**A11 answered "is any of it worth recovering": yes, 291.4 J of it, and the machine already
does.** What A11 could not answer is whether *more* of it can be, and that question is not open —
it is **P28**, an owner decision with the geometry already priced: 240 mm of regenerative stator
and a 300 mm fin do not both fit the 339 mm arrest section, and **A18 priced the fin side**, which
needs a 0.4–0.5 T pole field to stay inside both the 200 g cap and the 210 mm envelope. Shortening
the fin is not free and giving up regeneration costs the 291.4 J.

**So the remaining question is a layout decision with a cost attached, not an unexamined
possibility.** E8 closes into P28 rather than sitting beside it duplicating the question. The
934.7 J the fin does absorb is not unaccounted for either: **A18 closed E26**, the fin's campaign
transient, and it passes.

### E9. 6U/12U variants are force-limited, not designed
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — design 6U/12U or withdraw them

The payload family table is arithmetic from the same thrust constant. No mechanism,
cassette, or structural design exists for larger classes.

### E10. Launch restraint is drawn but not analysed
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **ANALYSIS HALF CLOSED 2026-08-06 by A18, and it FAILED.** Miles' equation on the GEVS
> spectrum gives 11.7-20.2 kN through the retention pins against the 5.9 kN they were sized for.
> Opened as **P37**. T-1 closes the test half and nothing here substitutes for it.
> **RESIZED 2026-08-10 by A22: two D9 pins, 41.0 kN, margin +0.45 at Q = 30 and positive across
> the whole range. The analysis half now passes; the test half is still T-1's.**

Retention gate pin sizing exists (**two D9 A-286 since 2026-08-10**, quasi-static margin 3.98) and the breech launch-lock
blocks are now modelled in CAD (`cad/parameters.json` `track`: `launch_lock`, x = 30-50
mm, 2 off). The rest, escapement caging, cam lock, tolerance stack-up under vibration,
is drawn or described, not analysed.

### E11. No contamination or outgassing analysis
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — public material screening -- ASTM E595 class data for the Gen6 BOM

> **ADR-004 gains external support 2026-07-29:** coreless construction lowers outgassing and
> vacuum-rated ironless linear motors are catalogue products, so this architecture converges
> with fielded vacuum practice. Does not close the item, T-4 tests *this* material set.
> **Specified 2026-07-29** as T-4 in `docs/QUALIFICATION_PLAN.md`: 8 thermal-vacuum cycles,
> −40 to +60 °C, with ASTM E595 limits (TML ≤ 1.0 %, CVCM ≤ 0.1 %) as pass criteria. The
> materials rule B16 already requires E595-compliant selection; T-4 is where that gets tested
> rather than asserted. Not run.
Materials were selected against E595 limits by rule, not by analysis. No contamination
budget for customer optics exists.

### E12. EMC beyond stray field
> **Status:** `CORRECTED` — found, fixed and propagated. Retained as the published record

> **Specified 2026-07-29** as T-6 in `docs/QUALIFICATION_PLAN.md`: MIL-STD-461 RE102/CE102
> class emissions during a 330 A pulse, plus static field measured at the payload envelope
> against the 22.7 / 4.3 / 0.4 mT model. A customer flying a magnetometer or magnetorquer
> needs that number measured, not modelled. Not run.
Static magnetic keep-out is computed. Induced currents from switching transients in
adjacent payloads are discussed but not calculated.

> **Sharpened 2026-08-05, and it is now the oldest unquantified thing in the project.** Two
> separate facts landed on this item on the same day. First, the mid-2025 decision to drop the
> coilgun rested partly on the electromagnetic environment being unacceptable for an unmodified
> CubeSat, and **that judgement has no working behind it** anywhere in my notebooks or here
> ([`docs/HISTORY.md`](docs/HISTORY.md#why-the-coilgun-was-actually-dropped)). Second, my
> sole-authored silo-launch paper lists "electromagnetic coupling" among the challenges its
> abstract says are "identified and analyzed", and its body never returns to the subject
> ([`docs/SKILLS.md`](docs/SKILLS.md)).
>
> **So an architecture was rejected on EMI grounds that were never computed, and the successor
> architecture has never had its own EMI computed either.** The question has also now been asked
> from outside the project, by a systems engineer wanting to know what the emissions do to the
> payload and to the launch vehicle's communications, which is exactly the pair this item covers
> and has never answered.
>
> **SCOPED 2026-08-05 as A14, and it found the dominant term is not the one anyone was asking
> about.** Six of eight declared bands pass, one fails, one is void as declared.
>
> | | |
> |---|---|
> | Induced EMF, 10 cm² loop at the payload's nearest face | **11.8 mV** commutation, **36.0 mV** at 20 kHz ripple |
> | Static Halbach field at the same face | **61.1 mT**, 1357× Earth, **611× magnetometer full scale** |
> | Comms margin below the SiC knee | 56 dB at UHF, 86–102 dB at S-band |
> | Radiation efficiency at the fundamental | 6.0e-8 — the structure cannot radiate at its own drive frequency |
> | Coilgun comparator | **666×** VOLLEY at equal geometry |
>
> **The switching transient is not the problem; the permanent magnets are.** The AC half of this
> item is now scoped and hands off to T-6 for confirmation. The static half became **P34**, which
> is a payload compatibility constraint rather than an emissions question.
>
> Two things A14 established as side effects. **Band 2 passes by only 1.4×** on an
> upper-bound calculation, halving at 40 kHz, which independently corroborates **P33**'s finding
> that only the top of the declared switching range is defensible. And the credible path to a
> launch vehicle's communications is **conducted, through a shared power bus**, not radiated —
> a specification problem, not a physics one.
>
> **E12 is not closed by this.** A14 is a scoping calculation from quantities already in
> `analysis/results/`; nothing in it is measured, and E12 closes on T-6.

### E13. Two numbers in source documents were never traced — CLOSED 2026-08-10
> **Status:** `CLOSED` — resolved; see the entry for what closed it

- The "780 deg/s" tumble rate from a third-party document. Falsified as
  implausible (would require a ~7.6 m line-of-action offset on a 1 m vehicle) but its
  origin was never found.
- The "1,000+ G hardening" figure, whose context (ground-launch guns) does not apply
  to this design.

**Closed 2026-08-10, on the ground that neither number is load-bearing anywhere.** Both were
disposed of on their merits when they were logged — one falsified by a physical argument, one
ruled inapplicable by context — and what stayed open was only the provenance question, "where did
it come from".

**That question cannot be answered from here and does not need to be.** A search of the tree finds
**no current claim resting on either figure**: "780" survives only in this entry and in
`docs/INVENTORY.md`, which already records it as *"Tumble-rate plausibility to 780 °/s falsified"*
and points at this entry. "1,000+ G" survives only in this entry. Neither appears in `analysis/`,
in any run sheet, or in `paper/paper.tex`.

**An untraced number that nothing depends on is a resolved item, not an open one.** Tracing the
origin of a figure this project has already falsified and does not use would buy nothing, and
carrying it as live debt overstates the register. The falsifications themselves are retained
above, which is the part with any value in it.

### E14. Patent / disclosure: the disclosure has now happened
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — file or let it go -- D5

Concept and results are public (LinkedIn, and this repository, which is now a **public**
repo carrying the scripts and therefore the operating point). No provisional application
was filed first, so this is done and cannot be undone. What remains is not a decision but
a consequence to be handled: any patent route now runs on whatever post-disclosure grace
period applies in each jurisdiction, India and the US have one, most of Europe does not
counted from the earliest public disclosure, not from today. **If a filing is still
wanted, establish that earliest date and take advice quickly.** If it is not, close this
item out explicitly so it stops reading as pending.

### E15. Sponsorship not secured
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `PROGRAMME` · **Next step:** `DECISION` — fund it or scope it -- D10

The build is the declared next step and is unfunded.

### E16. Reference hygiene
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — a reference audit against publisher records

Three references in `paper/paper.tex` were flagged verify-before-submission and have
not been fully verified: eddy-damper heritage [15], Yudintsev separation dynamics [17],
and the vibro-impact deployment paper [18]. `docs/RELATED_WORK.md` adds a further list of
comparator sources and tooling, **none of it retrieved and read either**, and it carries
the same rule: fetch before citing. The differential-drag comparator (Foster et al. flown
Planet Labs results) is the one worth chasing first, since the paper's 25-day baseline is
currently a model output rather than a measurement.

> **CHECKED 2026-08-10, and two of the three references do not exist in the paper any more.**
> This entry was checked against the manuscript rather than taken at its word, which is the
> whole point of it.
>
> **Yudintsev separation dynamics and the vibro-impact deployment paper are not in
> `paper.tex`.** A search of the source returns **zero** matches for "Yudintsev", "vibro" or
> "impact" in any form. They were removed from the bibliography at some point and **E16 went on
> flagging them for verification** — the register was guarding citations the deliverable no
> longer makes. **The reference numbers were stale too:** the bibliography now runs to 31 entries
> and [15], [17], [18] are the POEM-4, Vallado and OAM references, none of which this entry is
> about.
>
> **What is left is one reference, and it is now identified.** `\bibitem{eddy}` read
> *"Eddy current damper modelling for space mechanisms, Actuators; CDA InterCorp flight-heritage
> documentation"* — a paraphrased title with no author, volume, number, year or DOI, which is not
> a locatable citation. The journal half resolves to **Diez-Jimenez, Alén-Cordero,
> Alcover-Sánchez and Corral-Abad, "Modelling and Test of an Integrated Magnetic Spring–Eddy
> Current Damper for Space Applications," *Actuators*, vol. 10, no. 1, art. 8, 2021,
> doi:10.3390/act10010008**. The manuscript is corrected to that.
>
> ### The standard of evidence, stated exactly, because "verified" is doing work here
>
> **The citation was verified to exist and to have those bibliographic details, from four
> independent indexes that agree. It was NOT read.** The full text has not been retrieved —
> re-tested rather than assumed. So this is **bibliographic verification, not substantive**, and
> the difference matters for what the reference is being asked to support.
>
> **And it is being asked to support something a bench paper cannot.** `paper.tex` cites it for
> *"flight heritage in the damper class"*. What the retrievable metadata describes is a
> laboratory device — three configurations designed, simulated, manufactured and tested, with
> stiffness and damping coefficients measured on a bench. **A tested prototype is not flight
> heritage.** The flight-heritage half of the claim rests entirely on the vendor documentation
> bundled into the same `\bibitem`, which has not been retrieved and cannot be from here.
>
> **The paper's sentence is deliberately left alone.** Rewriting a published claim on the
> strength of a title and an abstract I could not open would be the same error this entry
> exists to prevent, in the opposite direction. It is recorded as a named, specific risk instead.
>
> **The two Foster references check out** at the same bibliographic standard:
> `foster2` is confirmed as arXiv:1509.03270, *"Orbit Determination and Differential-drag Control
> of Planet Labs Cubesat Constellations"*, Foster, Hallam and Mason, 2015, also circulated as
> AAS 15-524; `foster` is confirmed as *"Constellation Phasing with Differential Drag on Planet
> Labs Satellites"* in the *Journal of Spacecraft and Rockets*, doi:10.2514/1.A33927. Author
> list, title and venue match what `paper.tex` prints. **Neither was read**, so the 25-day
> differential-drag baseline is still a comparator this project has not checked against the
> flown result it attributes it to.

**What would close it:** full-text retrieval of `\bibitem{eddy}` and the two Foster papers on a
machine with unrestricted access to the publisher, and a decision on the flight-heritage claim once the
vendor documentation is actually in hand. `docs/RELATED_WORK.md`'s wider list remains
**unretrieved and is not claimed otherwise**. **This is narrowed, not closed** — from three
unverified references to one substantively unverified claim and a reading list.

### E17. The pulse-power chain: PARTIALLY CLOSED 2026-07-28 by A8, with two findings
> **Status:** `CLOSED` — resolved; see the entry for what closed it

**A8 has been run** (ngspice 42, `validation/spice/emocd_shot.cir`). All five declared bands
were met, exit velocity and pulse duration agree to 0.03 % across two different integrators,
peak current +5.98 %, sag +0.18 points, energy +3.59 %. Two findings came out of it anyway:

1. **Quoted sag is state-of-charge, not terminal voltage.** `motor_model.py` models no ESR
   at all; it reports the capacitor's charge depletion, 4.88 %. With a 12 mohm ESR the
   terminal droops to 86.16 V, a **10.25 % total sag**. The servo-headroom argument behind
   the 0.027 m/s dispersion claim is stated against the smaller number.
2. **The `Q_esr = 160 J` default does not reconcile with 12 mohm.** Integral of I^2 dt over
   the shot is 8008 A^2 s, giving 96 J at 12 mohm. The two agree only at about 20 mohm. This
   item asked for a second number against the 160 J; here it is.

The 12 mohm itself appears only in `docs/EMOCD_Computation_Results_C1-C10.md`, which is
superseded. **Datasheets have since been checked against it and it does not survive**: a bank of
this capacitance built from commercial cells is 116 to 185 mohm, and the shot does not close
above 65. See **P26**. This item is no longer about provenance; the number was not merely
unsourced, it was unattainable.

> **Re-run 2026-07-30 (A8-R), then corrected.** Five of six bands met; the pulse-duration row
> that P23 is about passes at 0.03 %. Energy closure failed at 97.0 %, and the cause was the
> gap this item names: 7126.2 A^2 s at 12 mohm is **85.5 J of ESR dissipation per shot** the
> analytic ledger had no term for. That is the second number against `Q_esr = 160 J` this item
> asked for, and it is 1.9x lower.
>
> **`motor_model.py` now carries `R_ESR` and solves for the current at the bank terminal**
> rather than at the capacitor, so the loss is integrated rather than assumed. P24 records the
> propagation. Two things fell out that are worth more than the correction itself:
>
> - **The 5.98 % peak-current deviation this item recorded was the ESR, not the integrator.**
>   Corrected, the analytic model gives 346.77 A against ngspice's 346.8, agreeing to 0.01 %
>   where it previously disagreed by 5 %. Two independent methods now agree on the number that
>   sets the device rating.
> - **The energy budget closed at 100.0 % while missing a real 86 J term**, because the draw it
>   balanced against came from the same model that omitted the loss. Closure tests arithmetic
>   consistency, not physical completeness, and this file had been quoting it as if it tested
>   both.
>
> The sag finding above stands and is unaffected: the quoted figure is still charge depletion,
> and the terminal dip is still additional.

Original item follows.

### E17 (as originally written). The pulse-power chain has never left the analytic model
The supercapacitor bank, the SiC bridge, and the winding exist only as lumped resistances
and ideal switching inside `motor_model.py` and `sizing.py`. Three numbers depend on that
model and nothing else: the **392 A peak current** (which sets the device rating and the
paper's derating discussion), the **4.9 % bank sag** (which underwrites the servo headroom
behind the 0.027 m/s dispersion claim), and the **672 J copper loss** (which carries the
32 % efficiency figure). No transient overshoot at commutation has been computed, and the
`Q_esr = 160 J` default in `sizing.py`, flagged as unsourced during the P2 review before
being traced to the script's own default, has no second number against it.

Specified as **A8** in `validation/A8_pulse_spice.md` (ngspice or PySpice, both free).
This is the least expensive analysis in the plan: no geometry, no mesh, no licence, and it
attacks three headline-adjacent numbers at once.

### E18. Conjunction covariance is invented: NEW 2026-07-27
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN6` · **Next step:** `COMPUTATION` — a conjunction covariance from a defensible public source

Any probability-of-collision result (A6) inherits whatever covariance it is given, and no
covariance exists for a satellite that has never flown. Space-Track **Conjunction Data
Messages** carry real post-deployment covariances for comparable objects and are the
defensible source; `validation/A6_conjunction_cara.md` now names them as the preferred
input, with an explicitly documented assumption as the fallback. Until that is done, no Pc
figure from this project should be quoted as anything but conditional on its assumption.

### E19. Eddy-current heating inside the magnet blocks is not modelled: NEW 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **CLOSED 2026-08-06 by A18, benign by a factor of 400.** 25.2 W of eddy loss in 3.67 kg of
> NdFeB over a 158.6 ms pulse is **0.0025 K per shot, 0.030 K per campaign** against a 1 K band.
> **Segmentation is not needed**: the trade is real for steady-state rotating machines and
> irrelevant to a 159 ms pulse at 341 Hz.> **Cross-industry review 2026-07-29** (`docs/CROSS_INDUSTRY.md`): this is a named, well-studied
> loss mechanism in PM machines, and **magnet segmentation is the standard mitigation, which
> reduces thrust and mechanical robustness.** That is a design option this project did not
> previously have. Item stays open: the literature is steady-state rotating machines, and
> nobody has computed the 157 ms pulsed case here.
`sizing.py::magnet_temperature()` models exactly one thermal effect on the magnets:
reversible remanence drift with ambient temperature, `alpha = -0.11 %/K`. NdFeB is a
conductor (roughly 1.4-1.6 uOhm*m, some 80-90x copper's resistivity but far from an
insulator), and the blocks sweep past the winding at up to 20 m/s through the field's
spatial harmonics, the belt winding's own 6th-harmonic ripple, slot-like content, and
whatever switching harmonics the SiC bridge puts on the current. That drives eddy currents
in the magnet bulk.

This is not the same failure mode as reversible drift. Local heating risks crossing the
knee point and causing **irreversible** demagnetisation, which no amount of cooling
recovers, and it is worst where the field harmonics are strongest rather than where the
bulk temperature sensor would sit.

No number is offered here because nothing in the repo computes one, and inventing an
order of magnitude for a loss that depends on harmonic content the model does not resolve
would be worse than recording the gap. What can be said without computation: this term
grows with current density, so it works directly against the "raise sheet current to
213 kA/m" option in `docs/DESIGN_OPTIONS_exit_velocity.md`, which that document already
calls thermally hard for the winding alone.

### E20. The brake's force-time profile does not exist: NEW 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **CLOSED 2026-08-06 by A18.** Velocity-proportional eddy drag gives a peak of **15.1 kN at
> 162.9 g** at a 0.5 T pole field, arresting in 124 mm and 40 ms, with energy matching
> `regen.KE_to_brake` to 0.005 %. **Bands hold only for a 0.4-0.5 T pole field**: below it the
> sled overruns the 210 mm envelope, above it the 200 g cap is exceeded. The pole field is a
> specification nothing in `cad/parameters.json` states.`sizing.py` asserts a 200 g deceleration **cap**, used to size the magnet bond. No script
anywhere simulates the arrest: there is no force against velocity, no force against
position, no peak, and no duration. `legacy/c3_c4_em.py` sizes the brake by energy, not by
transient.

A first-order estimate from the sled's own kinetic energy across the 210 mm arrest zone
puts the **average** force near 6 kN over roughly 8-20 ms, some 4x the 1413 N
acceleration force, over a tenth of the duration, and with a peak that nothing bounds. The
host therefore sees two oppositely-signed impulses of very different shape per shot, not
one smooth push, and a 12-shot campaign is 24 load reversals through the ESPA bolted
interface.

E5 covers the *magnitude* of the recoil budget across host mass classes. Nothing covers its
*shape*, and A4 is a static analysis that cannot. This is a fatigue and control-bandwidth
question, and it is the natural companion to A7.

### E21. No vacuum tribology anywhere: SUBSTANTIALLY RETIRED BY CITATION 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it

> **This is solved engineering with a handbook.** The ESA Space Tribology Handbook (Roberts,
> ESTL) covers lubricant and component selection, cold welding, and rolling-element life in
> vacuum; MoS2 is the broadly accepted solid lubricant. **Twelve cycles is a trivial life
> requirement** by space-mechanism standards. The remaining task is a *selection calculation*
> against the 1.48 kN per pair load, not research. See `docs/CROSS_INDUSTRY.md`.
Searching the entire repository for lubrication, tribology, cold welding or galling returns
nothing. The sled runs on four rollers (30 mm dia x 16 mm) carrying roughly 763 N per pair
at arrest (`sizing.py::arrest_loads()`), reused across twelve shots, in vacuum. Repeated
metal-on-metal rolling and sliding contact in vacuum with marginal or no lubrication is a
well-known deployable-mechanism failure class, and the reusable sled is the one part of
this architecture that a single-shot spring deployer does not have to solve.

Distinct from the neighbouring items: E10 covers the launch-restraint escapement, E11
covers outgassing and contamination. Neither covers the roller-to-rail interface, and no
lubricant, coating, or material pair is specified for it in `cad/parameters.json`.

### E22. Parasitic eddy drag on the track structure is not in the thrust model: REFRAMED 2026-07-29
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **CLOSED 2026-08-06 by A18 as the design rule it was reframed to be: no conductive structure
> within 20 mm of the array back face**, where drag is 0.285 % of thrust. At 10 mm it is 3.9 %
> and at 5 mm **14.5 %**. Applying the rule to every part needs a 3-D minimum-distance check
> against the assembly, which A18 does not perform -- the track longerons reach 6 mm axially but
> sit outside the array's half-width, so they are laterally clear rather than axially.> **Reframed as a design rule rather than an analysis** (`docs/CROSS_INDUSTRY.md`): vendor
> ironless motors keep conductive structure out of the magnet track's field. Specify a minimum
> standoff and check the CAD against it, cheaper than the computation this item implied.
The eddy brake works because a moving Halbach field drags on a nearby stationary conductor.
That is also the geometry of the entire 1.3 m acceleration zone wherever aluminium or
titanium structure (longerons, guide rails, enclosure skins) sits within reach of the
field. `verify_field.py` puts the stray field at 22.7 mT at 10 mm behind the array and
4.3 mT at 20 mm, which is not negligible at plausible standoffs.

`motor_model.thrust_constant()` computes Kt purely as the Lorentz force against winding
current. It carries no term for eddy coupling into any other conductor. So the model
accounts for eddy drag exactly where it is wanted (the brake) and nowhere it might be
unwanted, and the sign is unfavourable: any such drag subtracts from delivered thrust and
adds heat to the track.

Not quantified here, it depends on the track-to-array standoff and the conductivity of
whatever is actually there, and the standoff is not a single number in `cad/parameters.json`.
The check is cheap once that geometry is pinned, and it belongs with A1.

### E23. Force-ripple harmonics sweep the track's own structural modes every shot: **CLOSED 2026-08-05 by A17, and it FAILED**
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **This item predicted the answer would be benign. It is not.** Peak amplification is **8.18x**
> at the fundamental crossing of the 109 Hz fixed-fixed mode and **3.34x** at the 6th-harmonic
> crossing, against a declared band of 2x. **Q is not the variable that matters**: between Q = 20
> and Q = 500 the fundamental case moves only from 6.51 to 8.33, saturated at the lowest damping
> anyone would assign to bolted aluminium. What governs it is the normalised sweep rate
> `rate/f^2`, which is 0.18 at that crossing -- slow enough for the mode to respond fully.
>
> The dangerous crossing is the **fundamental at 5.23 m/s, 132.5 mm into the stroke**, not the
> 6th harmonic near the breech this entry emphasised. Opened as **P36**. See
> [`validation/A17_ripple_chirp.md`](validation/A17_ripple_chirp.md).
> **The cogging half retires; the sweep half does not.** Ironless construction has zero cogging
> by design, so the largest ripple source in an iron-core machine is absent. But E23 is about
> the *electrical* ripple chirping through the modes, and industrial stages run at constant
> velocity and do not chirp. **No citation found addresses this**: it appears genuinely
> unusual (`docs/CROSS_INDUSTRY.md`).
`sizing.py::track_first_mode()` reports 48 Hz pinned-pinned and 109 Hz fixed-fixed, and
checks them against a single static target: above 70 Hz to clear the launch primary band.
That is the right check for the launch environment and the wrong one for the shot.

The electrical excitation is not at a fixed frequency. It sweeps from zero upward as
`f = n*v/lambda` with lambda = 48 mm, so every shot chirps through the whole band below the
running frequency. At the as-drawn 9.445 kg sled (a = 105 m/s^2):

| Crossing | Speed | Time from start | Distance into the 1300 mm stroke |
|---|---|---|---|
| 6th harmonic through the 48 Hz pinned mode | 0.38 m/s | 3.7 ms | 0.7 mm |
| 6th harmonic through the 109 Hz fixed mode | 0.87 m/s | 8.3 ms | 3.6 mm |
| fundamental through 109 Hz | 5.23 m/s | 49.8 ms | 130 mm |

So both modes are crossed inside the first 4-50 ms of a 158.6 ms stroke, twelve times per
campaign, and the crossings happen in the first few millimetres of travel where the sled is
still adjacent to the breech and the launch-lock hardware.

**The likely answer is that this is benign, and the point is that nobody has shown it.** The
sweep rate is roughly `a/lambda` ~ 2.2 kHz/s, so transit through any plausible half-power
bandwidth takes on the order of a millisecond, which is far too fast for resonant buildup.
But that argument depends on the structure's Q, and **no Q, damping ratio, or loss factor
appears anywhere in the repository**. A static frequency check against a launch target does
not settle a swept-excitation question; the analysis that would is a chirp or Campbell-style
dwell-time check, and it does not exist.

Cheap to close, and it belongs with A4's dynamic leg rather than with A1.

### E24. Attitude disturbance from magazine indexing is not modelled: NEW 2026-07-30
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — attitude disturbance from magazine indexing

Found by reading a competitor's problem statement rather than by examining this design, which is
worth stating plainly: Xu et al. (*Aerospace* 11(5) 394, 2024) build a **cost model for attitude
disturbance caused by moving CubeSats around inside the deployer**, and optimise their transfer
paths against it, because a shifting centre of mass degrades platform pointing and therefore release
accuracy.

**This project models the recoil of the shot and nothing about the indexing between shots.**
`analysis/sizing.py` gives 66.1 N·s per ejection and the host nulls it with cold gas. But twelve
satellites feed from two transverse cassettes, so between every pair of shots a mass of order a few
kilograms translates across the structure, and:

- the centre of mass moves, so the host's attitude reference sees a disturbance torque that is
  **not** the shot recoil and is not in any budget here;
- the sled returns to the breech, a second mass motion, also unmodelled;
- the dispersion claim (0.027 m/s 3σ) assumes the track is where the model says it is at trigger
  time. If indexing leaves residual attitude rate or structural motion that has not damped out, the
  release direction carries an error the velocity servo cannot see, because it measures position
  along the track and not the track's own orientation.

**Why it is probably small, and why that is not an answer.** The indexed mass is a few kg against a
124.9 kg loaded system on a host of hundreds to thousands of kg, and the campaign has time between
shots, nothing here suggests a feasibility problem. But P16 was also "probably fine" until an
independent propagator was pointed at it. The quantity that matters is **residual attitude rate at
trigger, and the settling time to reach it**, and neither number exists anywhere in this repository.

**What would close it:** a rigid-body momentum budget for one index cycle, then the settling time
against the campaign's inter-shot interval. Cheap (it is bookkeeping, not a new solver) and it
belongs with the recoil analysis in `sizing.py` rather than with the motor model. Explicitly *not*
claimed to be negligible until that is done.

> ## Done 2026-07-31 as A13. **Verdict FAIL, and this entry was worried about the wrong mass.**
>
> **Indexing is negligible**, exactly as the paragraph above guessed: 0.208 N·s, **0.31 % of the
> shot impulse**, 0.007 °/s at a 500 kg host.
>
> **The sled return is not, and it appears nowhere in this entry or anywhere else.** 9.445 kg
> travelling 1.5 m back to the breech is **4.723 N·s, 7.14 % of the shot, 23x the indexing
> momentum** — the largest unbudgeted term in the host interaction by a wide margin.
>
> | Band | Result | |
> |---|---|---|
> | peak rate below 0.05 °/s at a 500 kg host | **0.161 °/s** | **FAIL, 3.2x over** |
> | peak rate below 0.2 °/s at 200 kg | **0.740 °/s** | **FAIL, 3.7x over** |
> | settle to 0.01 °/s in under 2 s at 0.1 N·m | **8.2 s** | **FAIL, 4x over** |
>
> Four of seven bands; the three that failed are the three that mattered. **Nothing inside the
> 10–20 s cadence passes** — the bands are only met at a 30 s sled return, which does not fit.
>
> **The velocity servo cannot see this.** It measures position along the track, not the track's
> orientation, so residual attitude rate at trigger is a pointing error the 0.027 m/s dispersion
> figure neither includes nor can detect.
>
> **Why this entry missed it is worth keeping.** E24 came from reading Xu et al., whose deployer
> moves satellites and does not return a sled — so the competitor's problem was the indexing, and
> this design's problem is in a place their paper never had to look. **Reading someone else's
> problem statement finds their gaps, not yours.**
>
> Full working, the three fixes and what each costs: [`validation/A13_indexing_disturbance.md`](validation/A13_indexing_disturbance.md).

### E25. A13 now leaves attitude restoration and structural settling open: CORRECTED 2026-08-03
> **Status:** `LIVE` — open engineering; something still has to be done
> **Scope:** `GEN5` · **Next step:** `COMPUTATION` — attitude restoration and structural settling


The corrected rigid-body budget does not leave a residual angular rate after an internal mass
starts and stops. It leaves a transient rate and an attitude offset. At the assumed 166 mm
lever arm, the 500 kg example reaches about 0.136 deg/s during sled return and finishes about
0.42 deg from its initial attitude. The 200 kg example reaches about 0.443 deg/s and 1.37 deg.

The declared transient-rate rows remain FAIL. The ideal residual-rate row passes, but that does
not establish structural settling. No controller, thruster geometry, wheel/RCS authority,
flexible-body mode, damping ratio, or firing schedule closes the attitude offset before the next
trigger. The previous 8.2 s rate-null and 18.1 s cadence floor are superseded. P31's 10--20 s
versus 1200 s cadence contradiction remains unresolved.

### E26. Brake-fin transient temperature across a campaign is not modelled: NEW 2026-08-03
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **CLOSED 2026-08-06 by A18, and ADR-020 is what closed it.** All sixteen swept
> (emissivity, contact-conductance) pairs fully decay between shots at the 1200 s cadence, so
> peak fin temperature is always one shot's rise: **34.1 C** against a 150 C band. Even bare
> copper at the lowest conductance clears 934.7 J in 1200 s. **At the paper's former 10-20 s it
> would not have**, so this is a result about the cadence rather than the fin.
The thermal calculation previously used a 300 x 80 x 4 mm copper fin. The Gen3 STEP and the
validation mass table specify 120 x 80 x 4 mm, 0.344 kg. Correcting that input raises the
adiabatic increment from about 3 K to about 7 K per shot and the twelve-shot no-cooling bound
to about 85 K.

The former statement that each transient decays before the next 10--20 s shot had no transient
conduction or radiation model behind it and is removed. A thermal network, contact conductance,
surface properties, and the resolved P31 cadence are required. The 0.32 m2 radiator number remains
an assumed 130 W steady rejection case, not a demonstrated campaign transient.

### E27. Gen4 finite-stator force and energy are not modelled: **CLOSED 2026-08-05 by A16**
> **Status:** `CLOSED` — resolved; see the entry for what closed it


> **Run against bands declared at `13b4b3b`.** Thrust per metre of overlapped array is 4086.0 N/m;
> at full overlap that reproduces `F_cmd` to **0.000 %**, the self-consistency test the analysis
> turns on. Force at release falls to **782.5 N**, 56.3 % of full. **Work over the 900 mm stroke
> is 1205.3 J and exit velocity is 13.390 m/s -- 81.7 % of the Phase I 16.388.** The stationing
> costs 18.3 % of velocity, and because the method omits end fields, winding termination and
> phase-progression disturbance, **that is an upper bound.** See
> [`validation/A16_gen4_finite_stator.md`](validation/A16_gen4_finite_stator.md).

The Gen4 working assembly exposes an end effect that the Phase I periodic/uniform-stator model
does not contain. The array is fully overlapped for 751.5 mm of the 900 mm acceleration stroke,
then progressively leaves the stator over the final 148.5 mm. At release, the remaining overlap
is 191.5 mm of a 340 mm array.

An overlap fraction alone is not an accepted force law. End fields, phase progression, winding
termination, current control and force ripple all matter in the edge region. The Phase I
regenerative section is also absent from the declared Gen4 operational selection, so its 291.4 J
credit cannot be carried into a Gen4 efficiency result.

**What would close it:** a position-dependent electromagnetic calculation using the recorded
Gen4 body bounds and stations, with the implementation, tool version, input hash, numerical
settings, tolerances and output hash retained. Compare it with the existing periodic result only
over the fully overlapped interval. Then integrate the force/current trajectory and rerun every
dependent result before exporting or publishing Gen4 performance.
