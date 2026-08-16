# A47 — Gen6's failure structure, on Gen5's basis

**Bands declared 2026-08-16, before `analysis/fmea_gen6.py` existed.**
Verify with `git show --stat <this commit> -- analysis/fmea_gen6.py`, which must return nothing.

---

## Why this run exists

**[E30](../OPEN_PROBLEMS.md) is the strongest structural criticism this design has received**, and
it has been LIVE since 2026-08-10:

> A spring dispenser is twelve independent one-shot mechanisms in parallel. One failure costs
> **one** satellite. VOLLEY is one mechanism in series with itself, cycled twelve times.

**`docs/FMEA.md` answered that for Gen5** — nine of thirteen elements forfeit the remaining
manifest, against a spring's zero, and **r ≥ 0.99326 per element per cycle** is needed to match a
spring on delivered orbital life.

**It contains no mention of Gen6.** The architecture changed on 2026-08-14 and the failure
analysis did not follow it. So the honest answer to *"is Gen6 more reliable?"* has been **nobody
has run it**, and the question has been asked.

## Method

**The same model, not a new one.** `analysis/fmea.py`'s `campaign()` and `required_element_r()`
are imported, so Gen5 and Gen6 are scored by identical arithmetic and the only thing that changes
is the element list. A second model would make the comparison meaningless.

**The element list is derived by walking Gen5's thirteen and asking what ADR-032 does to each**,
then adding what Gen6 introduces. Every entry names its fate.

**Optimistic by construction, and stated:** no common-cause failures, elements independent, no
wear-out, and reliability is treated as identical across elements — the same assumptions
`fmea.py` already makes, kept so the two are comparable rather than because they are right.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Re-running the imported model on **Gen5's** element list reproduces **r ≥ 0.99326** to within 0.0001 | The import is not the model `docs/FMEA.md` used, and nothing below is comparable |
| **2** | Every Gen5 element is accounted for in Gen6 as **deleted, retained, or replaced** — none silently dropped | The comparison is an assertion rather than a derivation |
| **3** | Gen6 has **fewer** manifest-forfeiting shared elements than Gen5's nine | Deleting the mover, stator, bank, converter and brake does not simplify the failure structure, and the architecture's main claim needs restating |
| **4** | Gen6's required per-element reliability is **lower** than Gen5's 0.99326 | Gen6 is *harder* to make reliable than the machine it replaced |
| **5** | Expected satellites delivered at a **common** r = 0.99 is **higher** for Gen6 than Gen5 | Same |
| **6** | **Neither** architecture reaches a spring's zero manifest-forfeiting elements | A result that flattering means the model has stopped counting shared elements correctly |
| **7** | The **gas store is counted as manifest-forfeiting** — one reservoir feeds twelve shots | The single most obvious shared element in the new architecture has been missed |
| **8** | A **per-cell backup ejector** is evaluated, and its effect on expected delivery at r = 0.99 is reported | The cheap parallel fix E30 points at is not priced, and the run answers only half the question |

## Predictions, recorded before the run

1. **Band 3 passes** — six of Gen5's nine shared elements are deleted outright, and Gen6 adds
   roughly four or five, so the count falls but by less than the deletion suggests.
2. **Bands 4 and 5 pass, and by a narrower margin than the architecture change implies**, because
   the elements Gen6 keeps — sequencer, cradle, magazine, gate, launch lock — were never the
   drive's, and they are what the campaign multiplies twelve times.
3. **Band 8 shows the backup ejector doing more than the architecture change did.** Converting
   the drive from manifest-forfeiting to satellite-forfeiting is a change of *structure*; deleting
   subsystems only changes the *count*.
4. If 3 is right, the honest conclusion is that **Gen6 improves reliability incidentally and E30
   is not answered by it.**

## Result

*Not yet run.*
