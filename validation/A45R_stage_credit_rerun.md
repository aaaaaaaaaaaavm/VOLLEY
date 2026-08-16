# A45-R — the stage credit, re-read after the enclosure was itemised

**Bands declared 2026-08-16, before `analysis/stage_credit.py` was changed.**
Verify with `git show --stat <this commit> -- analysis/stage_credit.py`, which must return nothing.

---

## Why this re-run exists

**[A45](A45_stage_credit.md) stands as declared and is not edited.** It read a **43.33 kg** credit
containing an **8.00 kg** enclosure lump, and its central argument was that *you cannot credit a
mass you never itemised.*

**[A46](A46_enclosure_buildup.md) itemised it**, at **50.04 kg**. That removes A45's sharpest
argument and replaces it with a larger problem: the credit is now **85.36 kg of a 126.56 kg
ledger — 67.4 % of the whole machine.**

A45's script cannot run against the new ledger, because five credited lines have no declared
surviving fraction. **Declaring them by editing A45 would be changing a run's inputs after its
result. This is the re-run instead.**

## What is carried forward unchanged

**The six original fractions are copied verbatim from A45** — track longerons 0.50, battery and
avionics 0.60, harness 0.50, thermal 0.40, ESPA bracket 0.90, panels 0.80 — because those items
have not changed and re-arguing them now, knowing what A45 found, is exactly the move this
project does not make.

## The five new fractions, and their reasons

**A45 gave the enclosure lump 0.00 on the grounds that it was never itemised. That reason is
gone**, so these are argued on their merits and every one of them is *more* generous than the
zero it replaces.

| Line | kg | Survives | Because |
|---|---:|---:|---|
| Enclosure skins | 32.82 | **0.85** | A stage is already a skinned cylinder; a deployer inside it needs no 6 m² box of its own. The 15 % is local closeout at the muzzle and the aft cutout |
| Enclosure frames | 8.20 | **0.85** | Stage ring frames and stringers, same argument |
| Radiator | 2.59 | **0.70** | The stage thermal loop provides radiating area; a local cold plate for the sequencer does not come free |
| Equipment-bay boxes | 1.87 | **0.60** | A stage avionics bay is real; mounting for a deployer sequencer is not |
| Fasteners and brackets | 4.55 | **0.50** | Attaching a deployer to a stage costs fasteners the stage does not already have |

---

## Acceptance bands

**Declared before the script is changed. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Credit reproduces A37's re-run **85.36 kg** to 0.01 kg | The re-run is not reading the corrected ledger |
| **2** | At the full credit, added mass per satellite is **1.403 kg** within 0.5 % | Gen6's added-mass numerator moved, which A46 should not have touched |
| **3** | Every item carries a surviving fraction **with a written reason** — zero unjustified | Same failure A45 existed to avoid |
| **4** | **Hostile reading keeps added mass per satellite ≤ 2.0 kg** | ADR-032 falsifier 1 still fires after the enclosure was properly itemised, so P68 is not an artefact of the placeholder |
| **5** | Uniform break-even ≥ **30 %**, as ADR-032 states | The decision record's threshold is still wrong |
| **6** | **Break-even is no worse than A45's 16.5 %** | Itemising the enclosure *reduced* the margin rather than clarifying it, and the credit growing is itself the problem |
| **7** | Added mass per satellite **monotone decreasing** in surviving fraction | The model is not behaving |
| **8** | The five enclosure lines are **less than half** the total credit | The stage credit has become mostly one subsystem, and the whole Gen6 mass case rests on a single assumption about somebody else's skin |

## Predictions

1. **Band 6 fails.** The credit grew by 42 kg while the allowance did not, so the break-even
   should fall to roughly **8 %** — half of A45's already-halved figure.
2. **Band 4 fails**, but by less than A45's 3.108 kg, because the new fractions are generous.
3. **Band 8 fails.** The enclosure is 50.04 kg of an 85.36 kg credit, which is **59 %**.
4. **Band 5 fails**, again.

## Result

*Not yet run.*
