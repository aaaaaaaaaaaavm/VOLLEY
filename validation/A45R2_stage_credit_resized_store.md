# A45-R2, the stage credit, at the store A56 actually sized

**Bands declared 2026-08-20, before `analysis/stage_credit.py` was changed.**
Verify with `git show --stat <this commit> -- analysis/stage_credit.py`, which must return nothing.

---

## Why this re-run exists

[A45](A45_stage_credit.md) and [A45-R](A45R_stage_credit_rerun.md) both stand as declared and are
not edited. Both read the store as 5.38 kg, computed from A43's 9.55 L reservoir.

[A56](A56_reservoir_resized.md) sized the store properly at ADR-034's charge pressure on
2026-08-20 and got 3.1216 kg, 42 % lighter. `cad/parameters.json` carries that figure.
`stage_credit.py` still computes its own from `fw.store_kg(V_RES_A43)`.

A45 predicted this needing to be redone, in its own prediction 1:

> *"ADR-032's 30 % was written when the store was a different mass; A43 has since settled it at
> 5.38 kg, and the break-even moves with it."*

The store has moved again. A45-R's own table already shows the allowance is what governs:

| | Credit | Break-even | May fail |
|---|---:|---:|---:|
| ADR-032, as written | 43.33 kg | 30 % | 13.0 kg |
| A45 | 43.33 kg | 16.5 % | **7.17 kg** |
| A45-R, after A46 | 85.36 kg | 8.4 % | **7.17 kg** |

"The allowance never moved. The credit did." *This run is the first time the allowance moves*,
`breakeven_fraction()` is `(2.0 × 12 − added_base − store) / total_credit`, and only the store
changed.

## What is carried forward unchanged

All eleven surviving fractions are copied verbatim from A45-R, the six original items and the
five enclosure lines A46 itemised. Re-arguing them now, knowing what they produced, is exactly
the move this project does not make. A45-R made that rule explicit and it applies to its own
successor.

One input changes: the store mass. Nothing else.

## The second problem, which this run is also asked to settle

This repository currently publishes at least three different figures for added mass per
satellite, and all three appear on front-facing pages:

| Figure | Where | What store it descends from |
|---:|---|---|
| **1.403 kg** | A45, A45-R, P68 | A43's **5.38 kg** |
| **1.296 kg** | `README.md`, `docs/index.html`, `GENERATIONS.md` | ADR-034's gas-ratio-scaled **≈ 4.10 kg** |
| **1.324 kg** | `docs/generations/GEN6.md` | the same ≈ 4.10 kg, **plus the trim stage** |

A56 settled the store and nothing reconciled what depends on it. The hostile end is no better:
3.271 kg in A45-R against 3.164 kg on the front page.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | **A45-R reproduces at the frozen store.** At `STORE_KG_A43 = 5.38` the run returns 85.3599 kg of credit, **1.403 kg/sat** full-credit and **3.271 kg/sat** hostile, each within 0.5 % | This re-run is not the same model as what it replaces, and nothing below is comparable |
| **2** | **The credit total is stated explicitly, and it is A45-R's 85.36 kg** | A break-even percentage is meaningless without the credit it is a fraction of — **P68 currently quotes the 43.33-based 16.5 %**, and a reader comparing 8.4 % to 16.5 % is comparing different denominators |
| **3** | Full-credit added mass per satellite at the resized store is **reported against A45's 1.403** | — |
| **4** | **Removing the P10 enclosure lines alone keeps added mass per satellite ≤ 2.0 kg** | A45 band 5's question, re-asked at the lighter store |
| **5** | **The hostile reading keeps added mass per satellite ≤ 2.0 kg**, against the **unmoved** 2.0 threshold | ADR-032 falsifier 1 still fires. **The threshold does not move because the store got lighter** |
| **6** | **The uniform break-even is ≥ 30 %, as [ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md) states** | ADR-032's declared threshold is still wrong, and the decision record still overstates its own margin |
| **7** | Added mass per satellite is **monotone decreasing** in surviving fraction | The model is not behaving. A45 band 7, unchanged |
| **8** | **The three published added-mass figures are reconciled** — each stated with the store and the scope that produces it, and **one named canonical** | The project keeps publishing three numbers for one quantity |
| **9** | **REPORT**: break-even and per-satellite mass across the store masses this project has used — A43's 5.38, ADR-034's ≈ 4.10, A56's 3.1216 | — |

## Predictions, recorded before the run

1. **Band 6 fails.** The allowance rises from 7.17 kg to about 9.4, so on an 85.36 kg credit the
   break-even lands near 11 %. Better than 8.4 %, and nowhere near 30 %.
2. **Band 5 fails**, near **3.08 kg/sat**. A 2.26 kg lighter store spread over twelve satellites is
   0.19 kg each, and the hostile reading is crossing by more than a kilogram.
3. **Band 4 fails.** The enclosure lines are 58.6 % of the credit; removing them was never close.
4. **Band 3 lands near 1.21 kg/sat**, below every figure currently published.
5. **Band 1 passes.** If it does not, the freeze was done wrong.

> The verdict is expected to survive and the margin to improve. *A CRITICAL entry getting
> better is not a CRITICAL entry resolved, and this run is not an attempt to close P68.* The
> falsifier firing by less is still the falsifier firing.

---

## Result

**RUN 2026-08-20. Four of eight decidable bands pass. The verdict survives and the margin improves
by a third, and it is still nowhere near the threshold [ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md) declared.

All five predictions held.

| # | Band | Result | | Script label |
|---|---|---|---|---|
| 1 | A45-R reproduces at the frozen 5.38 kg store | 85.3599 kg, **1.403**, **3.271** | **PASS** | `1`, `1b` |
| 2 | the credit total is stated, and is 85.36 kg | 85.3599 kg | **PASS** | `2` |
| 3 | full credit at the resized store | **1.2145 kg/sat — 13.43 % below A45's 1.403** | REPORT | `3r2` |
| 4 | removing the enclosure lines alone stays ≤ 2.0 | **5.384 kg/sat** | **FAIL** | `4r2` |
| 5 | hostile reading stays ≤ 2.0 kg | **3.083 kg/sat** | **FAIL** | `4` |
| 6 | break-even ≥ ADR-032's 30 % | **11.0 %** | **FAIL** | `5` |
| 7 | monotone in surviving fraction | monotone | **PASS** | `7` |
| 8 | the three published figures are reconciled | **5 rows, one canonical** | **PASS** | `8r2` |
| 9 | REPORT across every store used | 3 stores | REPORT | `9` |

*A45-R's own bands (`3`, `6`, `8`) still print and still fail; they belong to that run and are not
re-declared here.*

### The allowance moved for the first time

A45-R's finding was that the allowance never moves and only the credit does. This run is the
exception, and it is the only lever the design has.

| Store | Source | kg/satellite | Hostile | Break-even |
|---:|---|---:|---:|---:|
| **5.3800** | A43, from a 9.55 L reservoir | 1.4027 | 3.2709 | **8.4 %** |
| 4.1000 | ADR-034, gas-ratio scaled | 1.2961 | 3.1642 | 9.9 % |
| **3.1216** | **A56, sized at 22.7258 bar** | **1.2145** | **3.0827** | **11.0 %** |

Sizing the store rather than scaling it bought 2.26 kg, and it bought 2.6 points of break-even,
8.4 % to 11.0 %. *ADR-032 declared 30 %.* The falsifier fires by less and it still fires.

> A 42 % lighter store moved the hostile reading by 5.7 %, from 3.2709 to 3.0827. The store
> is not what is wrong with the mass case. It is the second-largest term in a numerator whose
> largest term, the 11.452976 kg added base, this run does not touch, and whose denominator is a
> 2.0 kg threshold that has never moved.

### Band 8: the project was publishing three numbers for one quantity

| Source | Store | Trim stage | kg/satellite |
|---|---:|---|---:|
| A45, A45-R, **P68** | 5.3800 | no | 1.4027 |
| `README.md`, `docs/index.html`, `GENERATIONS.md` | 4.1000 | no | 1.2961 |
| `docs/generations/GEN6.md` | 4.1000 | **yes** | 1.3988 |
| **A45-R2 — CANONICAL** | **3.1216** | no | **1.2145** |
| A45-R2, with the suspended trim stage | 3.1216 | yes | 1.3173 |

None of the three was wrong for its own scope, and no page said which scope it was using. The
front page's hostile figure of 3.164 is the 4.10 kg row; P68's 3.108 is A45's arithmetic at
5.38. *Two different stores, two different runs, both published as "Gen6".*

> The canonical figure is 1.2145 kg per satellite, at A56's sized store, without the trim stage.
> The trim stage is excluded because [ADR-036](../docs/adr/036-seal-specification-and-the-trim-stage.md)
> suspended it, and any page quoting 1.3173 must say it includes a section that may not be
> built.

### What did not move, and it is the whole finding

The enclosure is still 58.6 % of the credit, 50.03 kg of 85.36, and crediting it alone still
gives 5.384 kg per satellite. A lighter store does nothing about that, because
[A46](A46_enclosure_buildup.md)'s itemisation is the thing the mass case now rests on, and it is a
skin belonging to a vehicle nobody has agreed to lend.

The largest single loss in the hostile reading is unchanged: the enclosure skins at 4.92 kg, the
line A45-R rated 0.85, the most generous fraction in the table apart from the ESPA bracket.

### P68 does not close

It gets more honest and stays CRITICAL. Three of its numbers are superseded, 1.403 to 1.2145,
3.108 to 3.0827, and the break-even it quotes as 16.5 % is against the 43.33 kg credit A46 replaced.
The falsifier ADR-032 declared still fires, at 11.0 % against 30 %.

*A CRITICAL entry improving is not a CRITICAL entry resolved.*

### Provenance

Model output. The eleven surviving fractions are judgements, carried verbatim from A45-R and
not re-argued. The store is read live from `cad/parameters.json`; A43's 5.38 kg is frozen as
`STORE_KG_A43` and `main()` raises if it stops reproducing, so A45 and A45-R cannot drift the way
A44 and A48 did. Nothing here has been built or measured.
