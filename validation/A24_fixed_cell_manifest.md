# A24: the payload ladder as a design, not a volume ratio

**Closes:** the arithmetic-only status of every class except 3U in
[`docs/PAYLOAD_CLASSES.md`](../docs/PAYLOAD_CLASSES.md), and tests whether a **fixed-cell
manifest** closes [`KILL_CRITERIA.md`](../docs/KILL_CRITERIA.md) **threat 1**.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/cell_manifest.py` EXISTS.
>
> Everything below is committed before the script is written, and the script is absent at this
> commit. Verify with `git show --stat <this commit> -- analysis/cell_manifest.py`, which returns
> nothing.

## Result, 2026-08-10: five of six. Band 6 failed on one class, and the reason is worth more than the pass

> ## CORRECTION 2026-08-22 — the run is unchanged, its divisor is not. **P101**
>
> **Nothing below is edited.** The bands are not re-declared, the verdicts recorded on 2026-08-10
> stand as run, and this block is the whole of the change.
>
> **Every `kg per satellite` figure on this page is `deployer_dry_kg / n_per_load`, and the
> numerator has moved twice since the run.** A24 divided **76.5 kg**. The committed results file
> was last written against **84.5 kg**. [A46](A46_enclosure_buildup.md) replaced P10's 8.00 kg
> enclosure placeholder with 50.04 kg of derived line items on 2026-08-16, and the rollup has read
> **126.6 kg** ever since. **The counts, the arrangements and the three refusals are geometry and
> do not move at all.**
>
> `analysis/cell_manifest.py` was re-run on 2026-08-22 with no edit to the script, which reads the
> rollup live and always did:
>
> | Class | Per load | This page, 76.5 kg | Results file, 84.5 kg | **Re-run, 126.6 kg** |
> |---|---:|---:|---:|---:|
> | ChipSat / femtosat | 8640 | 0.009 | 0.010 | **0.015** |
> | PocketQube 1P | 288 | 0.266 | 0.293 | **0.440** |
> | PocketQube 3P | 96 | 0.797 | 0.880 | **1.319** |
> | TubeSat | 24 | 3.188 | 3.521 | **5.275** |
> | 1U CubeSat | 36 | 2.125 | 2.347 | **3.517** |
> | **3U CubeSat** | **12** | **6.375** | 7.042 | **10.550** |
>
> **Band 1 now fails, and it is not being edited.** It compares the cell model against a reference
> of **6.375 kg/satellite hardcoded in the script** at line 182. The cell model still reproduces
> the machine exactly — twelve per load, and 10.55 kg is the rollup over twelve — so **what band 1
> detects at the current inputs is its own frozen reference.** That is recorded rather than
> repaired: a band that has to be rewritten to keep passing is a band that was measuring the wrong
> thing, and saying so is worth more than a green row.
>
> **Band 3 still passes and its margin is thinner than it reads here.** It asks whether *some*
> designed class closes the 2.0 kg threshold. **Two rungs do — PocketQube 1P and 3P.** **1U does
> not**, at 3.517 kg, and this page's own text below calls 1U *"the rung this repository had been
> leaning on"*. TubeSat does not either. Bands 2, 4 and 5 are geometric and pass unchanged; band 6
> fails as it did, for the reason [P44](../OPEN_PROBLEMS.md) records.
>
> **One thing on this page has no committed record at all.** The 6U row is produced by the script's
> `multi_cell()` path, which prints and does not write — the results file records 6U as *not
> accommodated*, with zero per load. The classes that consume **whole cells** are therefore
> published here and stored nowhere. [`docs/D2_DECISION.md`](../docs/D2_DECISION.md) does not rest
> on that row.


`analysis/cell_manifest.py`, bands committed at `5fdc978` before it existed. Results in
`analysis/results/cell_manifest.json`.

### What the fixed cell holds

| Class | Per cell | Arrangement | Per load | Volumetric said | **kg per satellite** |
|---|---:|---|---:|---:|---:|
| ChipSat / femtosat | 720 | 9 x 2 x 40 | 8640 | 13322 | **0.009** |
| PocketQube 1P | 24 | 6 x 2 x 2 | 288 | 326 | **0.266** |
| ThinSat | — | — | **NOT ACCOMMODATED** | 123 | — |
| PocketQube 3P | 8 | 2 x 2 x 2 | 96 | 108 | **0.797** |
| TubeSat | 2 | 2 x 1 x 1 | 24 | 41 | **3.188** |
| 1U CubeSat | 3 | 3 x 1 x 1 | 36 | 40 | **2.125** |
| **3U CubeSat** | **1** | 1 x 1 x 1 | **12** | 12 | **6.375** |
| 6U CubeSat | 2 whole cells | — | 6 | 6 | **12.750** |
| 12U CubeSat | — | — | **NOT ACCOMMODATED** | 3 | — |

### Three refusals the volume ratio never made

**This is the difference between a design and arithmetic.** `payload_family.py` reports a count
for every class on the ladder. The fixed cell refuses three of them outright:

- **ThinSat is 114 x 114 x 25.4 mm.** Two of its three dimensions exceed the **100 mm cell
  section** in every orientation. The volume ratio said 123 per load. **Nothing fits.**
- **12U is 340 x 200 x 200 mm.** It needs 200 mm in *both* section axes. Stacking across cells
  in z works; there is **no second cell in y**, because the cassette is 166 mm wide. The volume
  ratio said 3 per load. **Nothing fits.**
- **6U survives, but only in one orientation** — 340 x 100 x 200, consuming two whole cells in z.
  Rotated the other way it is refused for the same reason 12U is.

**The cassette width is the constraint nobody had written down.** It is not in `KILL_CRITERIA.md`,
not in `PAYLOAD_CLASSES.md`, and a volumetric model structurally cannot find it.

### Band 3: threat 1 closes, but not where the ladder said it would

| Class | Volumetric kg/sat | **Fixed-cell kg/sat** | Against the 2.0 kg threshold |
|---|---:|---:|---|
| PocketQube 1P | 0.235 | **0.266** | **crosses** |
| PocketQube 3P | 0.708 | **0.797** | **crosses** |
| 1U CubeSat | 1.913 | **2.125** | **no longer crosses** |
| TubeSat | 1.866 | **3.188** | **no longer crosses** |

**1U was the class the repository leaned on, and a designed cell takes it back over the line.**
The volume ratio gave 40 per load at 1.913 kg. A real insert gives **36** — three 100 mm units
plus two dividers in a 340.5 mm cell, with 37.5 mm of the cell simply unusable — and
**2.125 kg**, which is *above* the threshold. TubeSat is worse: 41 becomes 24, and 1.866 kg
becomes **3.188 kg**, because a 127 mm long unit fits the cell twice with 84 mm wasted.

**Threat 1 still closes, on the PocketQube classes**, at 0.266 and 0.797 kg per satellite. But
the honest reading is that it closes **two rungs further down the ladder than the repository has
been claiming**, and the classes that close it are the ones with no corner rails and no designed
interface at all.

### Band 6: FAILED. The shim hardware outweighs the payload

**The band was ≤ 0.5 % of exit velocity. ChipSats come in at 0.508 %.** Over by 1.6 % of the
limit, on exactly one class:

| Class | Per cell | Payload in the cell | Shim hardware | Mean shift | |
|---|---:|---:|---:|---:|---|
| **ChipSat / femtosat** | 720 | 3.600 kg | **7.190 kg** | **0.0832 m/s (0.508 %)** | **FAIL** |
| PocketQube 1P | 24 | 6.000 kg | 0.230 kg | 0.0016 m/s (0.010 %) | pass |
| PocketQube 3P | 8 | 6.000 kg | 0.070 kg | 0.0005 m/s (0.003 %) | pass |
| 1U CubeSat | 3 | 3.990 kg | 0.020 kg | 0.0002 m/s (0.001 %) | pass |
| TubeSat | 2 | 1.500 kg | 0.010 kg | 0.0003 m/s (0.002 %) | pass |

**720 ChipSats in one cell need 719 shim interfaces. At 10 g each that is 7.19 kg of separation
hardware to disperse 3.6 kg of satellites** — the mechanism is twice the mass of everything it
exists to separate, and it stops being momentum-neutral because that mass departs with one side.

**The band is not widened.** Logged as **P44**. The design response is that **a per-interface
shim is the wrong mechanism at femtosat scale** — and the deeper reading is that the question is
wrong: 8640 ChipSats do not want 10 m of pairwise separation in 120 s, they want a *designed
dispersion across a swarm*, which is a different mechanism with a different acceptance argument.
That is now **PII-13**.

It is worth recording that ChipSat was **already outside the mechanism's declared limit** —
`payload_family.py` flags anything above 200 per load as "a different machine, not a bigger
magazine", and 8640 is 43x that. **That does not rescue the band.** The band as declared covered
every class sharing a cell, it was declared before the script, and one class missed it.

### Bands 1, 2, 4, 5

| Band | Test | Result | |
|---|---|---|---|
| 1 | Reproduces the 3U machine | 12 per load, 6.375 kg/sat, exact | **PASS** |
| 2 | Never beats the free volume ratio | every class at or below | **PASS** |
| 4 | Whole cells only, refusals printed | 3 refused, 0 fractional | **PASS** |
| 5 | Intra-cell differential ≤ 1 % of v_exit | 0.0833 m/s required against 0.164 allowed | **PASS** |

**Band 5 is a weak band and should be read as one.** The differential needed is
`10 m / 120 s = 0.0833 m/s` for every class, because the requirement is kinematic and does not
depend on what is in the cell. It tests that the number is small, not that any mechanism
delivers it — that is band 6's job, and band 6 is the one that failed.

---

## What is being tested

`payload_family.py` answers "how much room is there" with a calibrated volume ratio. It says so
itself: *"No cassette, cradle or gate exists for any class except 3U."* So the ladder that
currently answers threat 1 — 1U at 1.913 kg per satellite against a ~2 kg threshold — is
**arithmetic, not a design**, and a reader is right to discount it.

**The architecture under test is the fixed cell.** One cell geometry, sized to the 3U slot the
machine is already laid out for: **340.5 mm along x, 100 x 100 in section, on the existing
104 mm pitch, twelve cells across two cassettes.** Smaller classes fly in **inserts** — transverse
dividers that subdivide a cell along x and use the cell's own walls in y and z, so no new pitch,
no new gate, no new cradle and one qualification campaign. Mixing happens at ground integration.
This follows the flown canisterised-dispenser cell model rather than inventing one.

**The cost is stated up front, because it is the reason this is an ADR and not a tweak:**
**velocity becomes programmable per _cell_, not per satellite.** Every satellite sharing a cell
leaves on the same shot at the same commanded velocity. At 3U, cell = satellite and nothing is
lost. Below 3U, it is a real capability reduction, and it creates a problem the machine does not
currently have: **satellites that share a cell never separate from each other.**

## Acceptance bands

**Six bands. Bands 3 and 5 can fail, and failing is a result about the architecture, not a
reason to move a band.**

### Band 1 — the cell model reproduces the machine that exists

With the 3U class and no insert, the fixed-cell model returns **exactly 12** satellites per load,
and deployer mass per satellite within **±1 %** of `payload_family.py`'s **6.375 kg**.

A model of the current magazine that cannot return the current magazine is not a model of it.
**FAIL if either misses.**

### Band 2 — the designed cell is never more optimistic than the free volume ratio

For every class the fixed-cell model accommodates, the per-load count is **≤** the volumetric
count in `payload_family.py`.

A cell with divider walls, a fixed 104 mm pitch and a fixed 100 x 100 section **cannot** beat a
free volume ratio. If any class comes out higher, the model is **wrong**, not optimistic.
**FAIL on any class exceeding it.**

### Band 3 — does a designed ladder actually close threat 1?

**At least one** of {ThinSat, PocketQube 1P, PocketQube 3P, TubeSat, 1U} returns
**≤ 2.0 kg** of deployer per satellite under the fixed-cell model.

**This band may fail.** Divider walls and the fixed pitch charge for volume the volumetric model
never charged for, and the 100 x 100 cell section is a hard limit the volume ratio does not
model. If no class crosses, **the fixed-cell architecture does not close threat 1**, and that is
the finding — the answer would then be a different magazine, not a smaller satellite.

The 2.0 kg threshold is `KILL_CRITERIA.md`'s own, and that file already records it as an
estimate rather than a sourced figure. It is used here unchanged.

### Band 4 — whole cells only, and honest refusals

Every class either consumes a **whole number of cells** or is reported **NOT ACCOMMODATED**.
No fractional cell appears anywhere in the output.

A class needing more than **100 mm** in either section axis cannot be accommodated, because the
cell section is set by the 166 mm cassette width and the 104 mm stack pitch, both of which are
fixed by the existing structure. **A refusal is a valid result and must be printed as one**, not
rounded into a count.

### Band 5 — satellites sharing a cell must be able to separate

For every class packing **more than one satellite per cell**, the differential velocity required
to open **≥ 10 m of separation within 120 s** is **≤ 1 %** of the 3U exit velocity
(**≤ 0.164 m/s**).

Above 1 %, supplying the differential is a second deployment event with its own mechanism, its
own qualification and its own failure mode, and **the insert model is not viable as drawn**.
**This band may fail**, and if it does the honest answer is that sub-3U classes need a
per-satellite release, not an insert.

### Band 6 — the separation mechanism must not corrupt the shot

Whatever supplies the intra-cell differential changes the **cell's mean exit velocity by ≤ 0.5 %**
(≤ 0.082 m/s of 16.388).

The mechanism must be **internal to the cell and momentum-neutral to first order** — satellites
pushing against each other, not against the sled. Anything reacting into the sled perturbs the
primary shot, and `v_exit` is a frozen baseline value. **A mechanism that needs to push on the
sled is rejected by this band, not accommodated by it.**

## What this cannot settle

- **No insert has been drawn in CAD.** This sizes one; it does not design its retention, its
  thermal path or its ground handling.
- **The feed engages CubeSat corner rails.** PocketQubes, TubeSats and ThinSats do not have them.
  An insert that presents rails to the machine and a class-specific interface to the satellite is
  assumed to be possible and is **not** designed here.
- **Nothing here is a qualification argument.** One cell geometry means one campaign only if the
  insert is qualified as part of the cell, which is an assertion until a campaign exists.
- **Masses are typical flight masses**, not qualification maxima, inherited from
  `payload_family.py`.
