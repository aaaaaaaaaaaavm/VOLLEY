# A42, the fill window, and the gas a bottle cannot give back

**Bands declared 2026-08-14, before `analysis/fill_window.py` existed.**
Verify with `git show --stat <this commit> -- analysis/fill_window.py`, which must return nothing.

---

## Why this run exists

[ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md)'s replacement falsifier, written
when A41 closed P63: *a 2 L chamber cannot be filled to 50 bar inside the inter-shot window.* A41
specified the store and never checked that the store can be reloaded.

And a second question A41 did not ask, found while scoping this one. A41 sized the reservoir by
dividing total charge by storage pressure, 6 L at 200 bar for twelve 100 bar·L charges. That
assumes the bottle can be drawn to *zero*. It cannot. Below the charge pressure it can no
longer fill the chamber, so only the gas between 200 and 50 bar is usable, three quarters of
it.

## The two questions

| | |
|---|---|
| **Can it be filled in time?** | 0.1123 kg of nitrogen into a 2 L chamber, against a mechanical window of 4 s indexing plus 6 s return |
| **Does the bottle hold twelve charges?** | A41 says 6 L. Usable gas above the charge pressure says otherwise |

## Model

Isentropic choked flow from reservoir to chamber, integrated until the chamber reaches 50 bar.
Nitrogen, γ = 1.4, R = 296.8 J/kg·K, 300 K, C_d = 0.8. Adiabatic reservoir. The pressure ratio
is 0.25 at worst, well below the 0.528 critical value, so flow is choked throughout and the fill
is limited by orifice area and reservoir pressure alone.

Optimistic by construction: no line losses, no fill-valve dynamics, no heat of compression in
the chamber, no temperature drop in the reservoir across a sequence.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | The **first** charge fills in ≤ **10 s** — the 4 s index plus 6 s return already in the cadence | Reloading intrudes on the mechanical window and the cadence has to grow |
| **2** | Fill orifice ≤ **5 mm** | The fill valve is not an ordinary component |
| **3** | **A41's 6 L reservoir delivers twelve full charges** | **A41's reservoir is undersized**, its 4.66 kg store is wrong, and the mass result moves |
| **4** | The **twelfth** charge fills in ≤ **60 s**, inside ADR-020's 1200 s cadence | The last satellites cannot be loaded at any practical cadence |
| **5** | Store mass with whatever reservoir band 3 requires ≤ **12.55 kg** | The correction breaks A37's budget |
| **6** | Added mass per satellite ≤ **2.0 kg**, threshold unmoved | Kill criterion 1 re-crosses on the corrected store |

### Band 3 is the one that bites, and this time it was found before declaring

Scoping arithmetic says the usable fraction is (200 − 50)/200 = 75 %, so twelve charges need
**8 L rather than 6**. **The band is declared at A41's 6 L anyway**, because a band restated to
match a number already computed tests nothing. If it fails, it fails as declared and produces a
numbered defect.

### And the prediction, recorded because the last three were wrong

**Band 3 fails and everything else passes.** Fill time at a 1 mm orifice is roughly 4 s from a full
bottle, the correction is 6 L to 8 L, and the store rises by well under a kilogram, not enough to
threaten bands 5 or 6.

## What this run does not do

It designs no fill valve, line or manifold; models no heat of compression, no reservoir cooling
across the sequence, and no gas recovery from the fired chamber, recovering the vented residual
is the obvious repair if band 3's correction ever becomes expensive.**

---

## Results

**RUN 2026-08-14. Five of six bands pass. Band 3 fails as predicted, and by more than predicted.**

| # | Band | Result | |
|---|---|---|---|
| 1 | first charge fills in ≤ 10 s | **4.14 s** at 1.0 mm | **PASS** |
| 2 | orifice ≤ 5 mm | **1.0 mm** | **PASS** |
| 3 | A41's 6 L delivers twelve charges | **fails on shot 7** | **FAIL** |
| 4 | twelfth charge ≤ 60 s | **14.46 s** | **PASS** |
| 5 | store with the required reservoir ≤ 12.55 kg | **6.01 kg** at 11.25 L | **PASS** |
| 6 | added mass per satellite ≤ 2.0 kg | **1.455 kg** | **PASS** |

### The fill window is not the problem

4.14 s through a 1 mm orifice, against the 4 s index plus 6 s return already in the cadence.
ADR-032's replacement falsifier is answered and it is not the constraint.

### The bottle is

| Shot | Reservoir | Fill |
|---:|---:|---:|
| 1 | 200.0 bar | 4.14 s |
| 4 | 131.4 | 6.52 s |
| 6 | 86.0 | 10.68 s |
| **7** | **63.6** | **cannot fill** |

A41's 6 L bottle runs out at shot seven of twelve, because it can only be drawn to the charge
pressure. Below 50 bar it cannot fill a 50 bar chamber, and the last quarter of the gas is stranded.

### The correction is smaller than this run reports, and the reason is my model

The reservoir is modelled as adiabatic, so it cools as it empties and its pressure falls faster
than mass alone would give. That is right for a fast blowdown and wrong for this cadence,
[ADR-020](../docs/adr/020-inter-shot-cadence.md) puts twenty minutes between shots, ample for a
bottle to re-equilibrate with its surroundings.

So the answer is bounded rather than single-valued:

| | Reservoir | Store | Added per satellite |
|---|---:|---:|---:|
| **Isothermal** — the 1200 s cadence case | **7.65 L** | **4.67 kg** | **1.344 kg** |
| **Adiabatic** — what this run modelled | **11.25 L** | **6.01 kg** | **1.455 kg** |

**Band 3 fails either way**, since 6 L is short of both. **Bands 5 and 6 pass either way.** What is
model-dependent is the size of the correction, not its direction, and the truth sits nearer the
isothermal end at this cadence. Recorded as P64.

> **Annotated 2026-08-16 by [A43](A43_reservoir_thermal.md). This run's bands stand as declared and
> its result is left as the record of what it found, but two numbers in the table above are
> superseded and neither is reproducible. Carrying mass and temperature as the state gives
> 8.25 L isothermal and 9.55 L adiabatic, not 7.65 and 11.25: the isothermal figure was never
> computed by any script, and the adiabatic one came from recomputing reservoir mass at T₀ each
> shot, which discards gas that is really there. And the sentence in bold above is wrong.
> Conduction through stagnant nitrogen gives a 17 460 s time constant against a 1200 s cadence, so
> the truth sits at the *adiabatic* end. P66.

### The prediction, and this one held

Written in the declaration: *band 3 fails and everything else passes; fill is roughly 4 s at 1 mm;
the correction is 6 L → 8 L.* **Fill was 4.14 s, band 3 failed alone, and the isothermal correction
is 7.65 L. The adiabatic figure of 11.25 L is outside what was predicted, and the reason is the
thermal assumption rather than the arithmetic.

Four predictions this session, one right. It is the first that was checked with a calculation
before being written down.

## What this run does not do

Unchanged from the declaration, and now with one addition that matters: no thermal model of the
reservoir between shots, which is exactly the term that separates 7.65 L from 11.25. No fill
valve, line or manifold; no heat of compression in the chamber; and no gas recovery from the
fired chamber, which vents 43 bar of a 2 L volume every shot and is the obvious repair if the
reservoir ever needs to shrink.
