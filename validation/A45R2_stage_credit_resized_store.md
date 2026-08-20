# A45-R2 — the stage credit, at the store A56 actually sized

**Bands declared 2026-08-20, before `analysis/stage_credit.py` was changed.**
Verify with `git show --stat <this commit> -- analysis/stage_credit.py`, which must return nothing.

---

## Why this re-run exists

**[A45](A45_stage_credit.md) and [A45-R](A45R_stage_credit_rerun.md) both stand as declared and are
not edited.** Both read the store as **5.38 kg**, computed from A43's 9.55 L reservoir.

**[A56](A56_reservoir_resized.md) sized the store properly at ADR-034's charge pressure on
2026-08-20 and got 3.1216 kg** — 42 % lighter. `cad/parameters.json` carries that figure.
`stage_credit.py` still computes its own from `fw.store_kg(V_RES_A43)`.

**A45 predicted this needing to be redone, in its own prediction 1:**

> *"ADR-032's 30 % was written when the store was a different mass; A43 has since settled it at
> 5.38 kg, and the break-even moves with it."*

**The store has moved again.** A45-R's own table already shows the allowance is what governs:

| | Credit | Break-even | May fail |
|---|---:|---:|---:|
| ADR-032, as written | 43.33 kg | 30 % | 13.0 kg |
| A45 | 43.33 kg | 16.5 % | **7.17 kg** |
| A45-R, after A46 | 85.36 kg | 8.4 % | **7.17 kg** |

**"The allowance never moved. The credit did."** *This run is the first time the allowance moves* —
`breakeven_fraction()` is `(2.0 × 12 − added_base − store) / total_credit`, and only the store
changed.

## What is carried forward unchanged

**All eleven surviving fractions are copied verbatim from A45-R** — the six original items and the
five enclosure lines A46 itemised. **Re-arguing them now, knowing what they produced, is exactly
the move this project does not make.** A45-R made that rule explicit and it applies to its own
successor.

**One input changes: the store mass.** Nothing else.

## The second problem, which this run is also asked to settle

**This repository currently publishes at least three different figures for added mass per
satellite, and all three appear on front-facing pages:**

| Figure | Where | What store it descends from |
|---:|---|---|
| **1.403 kg** | A45, A45-R, P68 | A43's **5.38 kg** |
| **1.296 kg** | `README.md`, `docs/index.html`, `GENERATIONS.md` | ADR-034's gas-ratio-scaled **≈ 4.10 kg** |
| **1.324 kg** | `docs/generations/GEN6.md` | the same ≈ 4.10 kg, **plus the trim stage** |

**A56 settled the store and nothing reconciled what depends on it.** The hostile end is no better:
**3.271 kg** in A45-R against **3.164 kg** on the front page.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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
   break-even lands near **11 %**. Better than 8.4 %, **and nowhere near 30 %.**
2. **Band 5 fails**, near **3.08 kg/sat**. A 2.26 kg lighter store spread over twelve satellites is
   0.19 kg each, and the hostile reading is crossing by more than a kilogram.
3. **Band 4 fails.** The enclosure lines are 58.6 % of the credit; removing them was never close.
4. **Band 3 lands near 1.21 kg/sat**, below every figure currently published.
5. **Band 1 passes.** If it does not, the freeze was done wrong.

> **The verdict is expected to survive and the margin to improve.** *A CRITICAL entry getting
> better is not a CRITICAL entry resolved, and this run is not an attempt to close P68.* **The
> falsifier firing by less is still the falsifier firing.**
