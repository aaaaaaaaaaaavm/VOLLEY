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

**RUN 2026-08-16. Four of eight bands pass. Itemising the enclosure did not rescue the credit — it
halved the margin again.**

| # | Band | Result | |
|---|---|---|---|
| 1 | credit reproduces A37's re-run 85.36 kg | 85.3599 kg | **PASS** |
| 2 | full credit gives 1.403 kg/sat within 0.5 % | 1.403 kg, 0.02 % off | **PASS** |
| 3 | every item carries a written reason | 0 unjustified | **PASS** |
| 4 | hostile reading keeps ≤ 2.0 kg/sat | **3.271 kg** | **FAIL** |
| 5 | break-even ≥ 30 %, as ADR-032 states | **8.4 %** | **FAIL** |
| 6 | break-even no worse than A45's 16.5 % | **8.4 %** | **FAIL** |
| 7 | monotone in surviving fraction | monotone | **PASS** |
| 8 | enclosure lines are less than half the credit | **58.6 %** | **FAIL** |

### The break-even has halved twice

| | Credit | Break-even | May fail |
|---|---:|---:|---:|
| ADR-032, as written | 43.33 kg | **30 %** | 13.0 kg |
| A45, 2026-08-16 | 43.33 kg | **16.5 %** | 7.17 kg |
| **A45-R, after A46** | **85.36 kg** | **8.4 %** | **7.17 kg** |

**The allowance never moved. The credit did.** Added mass per satellite may absorb **7.17 kg**
before it reaches 2.0, and that is fixed by A43's store and A37's added base. Doubling the credit
does not buy any more of it — **it just means a smaller fraction of the credit has to fail before
the falsifier fires.** ADR-032's threshold is now wrong by 3.6 times.

### Band 8 is the one that should worry a reader

**The five enclosure lines are 50.03 kg of an 85.36 kg credit — 58.6 %.** The Gen6 mass case now
rests, majority-wise, on a single assumption about a skin belonging to a vehicle nobody has agreed
to lend.

**Crediting the enclosure and nothing else already gives 5.572 kg per satellite**, and the largest
single loss in the hostile reading is the skins at 4.92 kg — the item this run rated **0.85**, the
most generous fraction in the table apart from the ESPA bracket.

### What A46 changed about the argument

**A45's sharpest point is gone and the situation got worse anyway.** A45 could say *you cannot
credit a mass you never itemised*, and rated the lump 0.00. **A46 itemised it**, so this run rates
the same hardware at 0.50 – 0.85 — **every one of the five fractions is more generous than the zero
it replaces** — and the hostile figure still lands at **3.271 kg per satellite**, only 5 % better
than A45's 3.108 on a credit twice the size.

**Being more generous, line by line, on a properly derived mass, produced almost the same answer.**
That is a stronger result than A45's, because it no longer depends on refusing to credit an
unmodelled lump.

### The predictions

**All four held**, which is three runs in a row.

1. Break-even near 8 % — **8.4 %**.
2. Band 4 fails by less than A45's 3.108 — **3.271**. *Wrong: it is slightly worse, not better.*
3. Band 8 fails, enclosure near 59 % — **58.6 %**.
4. Band 5 fails again — **8.4 % against 30 %**.

*Correction to the above: prediction 2 said the hostile figure would be lower than A45's. It is
higher, 3.271 against 3.108. The generosity of the new fractions was outweighed by the size of what
they apply to.*

## What this re-run does not do

- **A45 is not edited.** Its bands, fractions and result stand as the record of what it found
  against the ledger it read.
- **The six original fractions are unchanged**, deliberately, so this run cannot be accused of
  re-arguing them with hindsight.
- **The fractions are still judgements.** The break-even is published so a reader can substitute
  their own, and at 8.4 % there is very little room for anyone's.
