# A46 — the enclosure, built up from line items instead of guessed

**Bands declared 2026-08-16, before `analysis/enclosure_buildup.py` existed.**
Verify with `git show --stat <this commit> -- analysis/enclosure_buildup.py`, which must return nothing.

---

## Why this run exists

**[P68](../OPEN_PROBLEMS.md).** [A45](A45_stage_credit.md) found that ADR-032's first falsifier
fires, and that **the single largest item in the 43.33 kg stage credit is the 8.00 kg enclosure,
radiator and packaged-avionics line — which is [P10](../OPEN_PROBLEMS.md), a mass this repository
records as never itemised.** At 18.5 % of the credit against a 16.5 % break-even, that one line
fires the falsifier on its own.

**P10's own text says what to do:** *"Add line items once masses are estimated."* It has said so
since the enclosure document was drawn, and instead an **8.00 kg placeholder with no derivation**
was entered on 2026-08-13 so that a caveated number would be auditable where a hole was not. That
was the right move at the time and it was never meant to be the answer.

**The geometry to do it properly has existed all along**, in `cad/parameters.json` under
`enclosure`: skins, thickness, envelope, three apertures, radiator dimensions and four equipment
bays with coordinates.

## What is being built

**The Gen5 enclosure**, because that is what the placeholder is in and what A35's ledger carries.
Gen6 deletes it — the stage provides the skin — which is exactly why the number matters: it is
the largest thing being credited away.

| Element | From |
|---|---|
| Skins | `enclosure` envelope, less the muzzle aperture, the Ø466 aft flange cutout and the belly notch |
| Frames and ribs | a declared fraction of skin mass |
| Radiator | `radiator_length` × `radiator_width` × `radiator_thickness` |
| Equipment-bay boxes | the four `bays` volumes, walled at a declared thickness |
| Fasteners, brackets, tie-downs | a declared fraction of the structure |

**Two skin cases, because `parameters.json` specifies one and flight hardware uses the other.**
The file says **2 mm monolithic aluminium**. Real spacecraft panels of this size are honeycomb
sandwich. **Both are computed**; the sandwich areal density is declared and swept.

## Declared inputs

| | Value | Because |
|---|---|---|
| Aluminium density | 2700 kg/m³ | as `mass_properties.py` already uses |
| Sandwich areal density | **3.0 kg/m²**, swept 2.0 – 4.0 | an aluminium honeycomb panel with thin facesheets; the sweep is wider than the spread between real designs |
| Frames and ribs | **25 %** of skin mass | a declared fraction, with no derivation, and named as such |
| Bay wall thickness | **1.5 mm** aluminium | thinner than the skin because a bay is not a load path |
| Fasteners and brackets | **10 %** of structure | a declared fraction, named as such |

**Three of those five are guesses.** They are smaller guesses than the one they replace, and each
is stated rather than folded into a total.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Envelope read from `parameters.json` is **1839 × 530 × 914 mm** within 1 mm | The run is not reading the authoritative geometry |
| **2** | Aperture area subtracted is **> 0** and **< 5 %** of gross skin area | The cutouts are being ignored or double-counted |
| **3** | **Built-up mass, monolithic 2 mm case, ≤ 8.0 kg** | The placeholder is low, the dry-mass floor rises again, and every kg-per-satellite figure in the project moves the wrong way |
| **4** | **Built-up mass, sandwich case, ≤ 8.0 kg** | Same, and it cannot be blamed on the parameter file specifying a heavy skin |
| **5** | Sandwich case is **lighter** than monolithic across the whole areal-density sweep | The model is not behaving |
| **6** | Radiator area **0.32 m²** rejects the campaign-average heat load at 300 K, ε = 0.85, to a 4 K sink | The radiator is undersized and the enclosure has a second defect |
| **7** | Every line item traces to a **parameter or a declared input** — zero undeclared | The buildup has a hole of its own, which is the thing it exists to remove |
| **8** | **A45's P10-only case improves** — added mass per satellite on the corrected lump is **≤ 2.069 kg** | The correction makes P68 worse rather than better, and the honest range in `KILL_CRITERIA.md` widens again |

## Predictions, recorded before the run

1. **Bands 3 and 4 both fail, and band 3 badly.** Six square metres of 2 mm aluminium is about
   33 kg before anything is attached to it. I expect the monolithic case near **35 kg** and the
   sandwich case near **22 kg**, against a placeholder of 8.
2. **Band 8 therefore fails too**, and P68 gets worse rather than better: a bigger P10 lump is a
   bigger thing being credited to the stage.
3. **Band 6 passes comfortably.** The campaign-average dissipation is a couple of watts against a
   radiator that should reject over a hundred.
4. `KILL_CRITERIA.md` already flagged **a plausible 20 kg** of missing mass. I expect this run to
   land near or above that figure, which would mean the file's own warning was closer than the
   placeholder chosen instead of it.

## Result

*Not yet run.*
