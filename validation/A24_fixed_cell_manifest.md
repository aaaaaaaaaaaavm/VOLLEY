# A24: the payload ladder as a design, not a volume ratio

**Closes:** the arithmetic-only status of every class except 3U in
[`docs/PAYLOAD_CLASSES.md`](../docs/PAYLOAD_CLASSES.md), and tests whether a **fixed-cell
manifest** closes [`KILL_CRITERIA.md`](../docs/KILL_CRITERIA.md) **threat 1**.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/cell_manifest.py` EXISTS.
>
> Everything below is committed before the script is written, and the script is absent at this
> commit. Verify with `git show --stat <this commit> -- analysis/cell_manifest.py`, which returns
> nothing.

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
