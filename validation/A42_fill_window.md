# A42 — the fill window, and the gas a bottle cannot give back

**Bands declared 2026-08-14, before `analysis/fill_window.py` existed.**
Verify with `git show --stat <this commit> -- analysis/fill_window.py`, which must return nothing.

---

## Why this run exists

**[ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md)'s replacement falsifier**, written
when A41 closed P63: *a 2 L chamber cannot be filled to 50 bar inside the inter-shot window.* A41
specified the store and never checked that the store can be reloaded.

**And a second question A41 did not ask, found while scoping this one.** A41 sized the reservoir by
dividing total charge by storage pressure — **6 L at 200 bar for twelve 100 bar·L charges.** That
assumes the bottle can be drawn to *zero*. **It cannot.** Below the charge pressure it can no
longer fill the chamber, so only the gas between **200 and 50 bar** is usable — **three quarters of
it.**

## The two questions

| | |
|---|---|
| **Can it be filled in time?** | 0.1123 kg of nitrogen into a 2 L chamber, against a mechanical window of 4 s indexing plus 6 s return |
| **Does the bottle hold twelve charges?** | A41 says 6 L. Usable gas above the charge pressure says otherwise |

## Model

Isentropic choked flow from reservoir to chamber, integrated until the chamber reaches 50 bar.
**Nitrogen, γ = 1.4, R = 296.8 J/kg·K, 300 K, C_d = 0.8.** Adiabatic reservoir. The pressure ratio
is 0.25 at worst, well below the 0.528 critical value, so flow is **choked throughout** and the fill
is limited by orifice area and reservoir pressure alone.

**Optimistic by construction:** no line losses, no fill-valve dynamics, no heat of compression in
the chamber, no temperature drop in the reservoir across a sequence.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The **first** charge fills in ≤ **10 s** — the 4 s index plus 6 s return already in the cadence | Reloading intrudes on the mechanical window and the cadence has to grow |
| **2** | Fill orifice ≤ **5 mm** | The fill valve is not an ordinary component |
| **3** | **A41's 6 L reservoir delivers twelve full charges** | **A41's reservoir is undersized**, its 4.66 kg store is wrong, and the mass result moves |
| **4** | The **twelfth** charge fills in ≤ **60 s**, inside ADR-020's 1200 s cadence | The last satellites cannot be loaded at any practical cadence |
| **5** | Store mass with whatever reservoir band 3 requires ≤ **12.55 kg** | The correction breaks A37's budget |
| **6** | Added mass per satellite ≤ **2.0 kg**, threshold unmoved | Kill criterion 1 re-crosses on the corrected store |

### Band 3 is the one that bites, and this time it was found before declaring

Scoping arithmetic says the usable fraction is **(200 − 50)/200 = 75 %**, so twelve charges need
**8 L rather than 6**. **The band is declared at A41's 6 L anyway**, because a band restated to
match a number already computed tests nothing. If it fails, it fails as declared and produces a
numbered defect.

### And the prediction, recorded because the last three were wrong

**Band 3 fails and everything else passes.** Fill time at a 1 mm orifice is roughly 4 s from a full
bottle, the correction is 6 L → 8 L, and the store rises by well under a kilogram — not enough to
threaten bands 5 or 6.

## What this run does not do

It designs no fill valve, line or manifold; models no heat of compression, no reservoir cooling
across the sequence, and no gas recovery from the fired chamber — **recovering the vented residual
is the obvious repair if band 3's correction ever becomes expensive.**

---

## Results

*(Filled after the run. Nothing above this line changes.)*
