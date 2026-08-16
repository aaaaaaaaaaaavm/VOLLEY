# A45 — the 43.33 kg stage credit, read hostilely

**Bands declared 2026-08-16, before `analysis/stage_credit.py` existed.**
Verify with `git show --stat <this commit> -- analysis/stage_credit.py`, which must return nothing.

---

## Why this run exists

**[ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md)'s first falsifier**, and the only
one of the four that nothing has ever bounded:

> **The 43.33 kg stage credit is optimistic by more than 30 %.** Then added mass per satellite
> exceeds 2.0 kg and A37 band 5 fails retrospectively.

**[A37](A37_host_integrated.md) assigned every line of A35's ledger to added, deleted or
stage-provided, and required each stage-provided item to name the subsystem providing it.** That is
a good discipline and it is not the same as testing whether the naming survives someone who does
not want to believe it. **This run is that reader.**

## The credit, line by line

| kg | Item | A37's justification |
|---:|---|---|
| 6.83 | Track longerons | primary structure — the stage *is* a long stiff cylinder |
| 5.50 | Battery + avionics + IMU | stage power, command and IMU, kept alive past passivation |
| 2.50 | Harness | stage harness, extended rather than added |
| 6.00 | Thermal (pipes, radiator, MLI) | stage thermal control loop |
| 9.00 | ESPA bracket + fasteners | the stage needs no adapter to itself |
| 5.50 | Panels / closeouts | stage skin and thrust structure |
| 8.00 | Enclosure / radiator / packaged avionics | stage thermal control and avionics bay |
| **43.33** | | |

## The hostile fractions, declared as inputs with their reasons

**These are judgements, not measurements**, and they are written down before the script so the
consequence is computed rather than argued. The script sweeps around them.

| Item | Survives | Because |
|---|---:|---|
| Track longerons | **0.50** | A stage is a stiff cylinder; it is not a 2.18 m rail aligned to a piston bore. Half the structure is genuinely reused and half is rail hardware that has to be added |
| Battery + avionics + IMU | **0.60** | Stage power and IMU are real. A deployer sequencer, its safing chain and the cost of keeping avionics alive past passivation are not the stage's |
| Harness | **0.50** | Extending a harness costs harness |
| Thermal | **0.40** | The stage loop is sized for the stage, not for 131 W of charging plus twelve expansions |
| ESPA bracket | **0.90** | **The strongest credit in the table.** A stage genuinely needs no adapter to itself; 10 % is local mounting |
| Panels / closeouts | **0.80** | Stage skin is real; local closeout around the muzzle is not |
| Enclosure / radiator / packaged avionics | **0.00** | **You cannot credit a mass you never itemised.** **P10** records this as a parametric lump never built up from line items, and the 84.5 kg dry mass as *a floor, not a total*. Deleting it as stage-provided converts an admitted unknown into a saving |

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The line items reproduce A37's **43.33 kg** to 0.01 kg | This run is not reading A37's credit |
| **2** | At the **full** credit, added mass per satellite reproduces **1.403 kg** within 0.5 % | The baseline is not A43's, and nothing after this compares |
| **3** | Every item carries a surviving fraction **with a written reason** — zero unjustified | The hostile reading is assertion rather than argument, which is the thing it exists to test |
| **4** | **Added mass per satellite under the hostile reading ≤ 2.0 kg**, threshold unmoved | **ADR-032 falsifier 1 fires**, A37 band 5 fails retrospectively, and kill criterion 1 is crossed on *both* numerators rather than one |
| **5** | **Removing the P10 lump alone** keeps added mass per satellite ≤ 2.0 kg | A single admitted-unmodelled item is by itself enough to fire the falsifier |
| **6** | The **uniform break-even** credit loss is ≥ **30 %**, as ADR-032 states | ADR-032's own falsifier threshold is wrong, and the design has less margin than the decision record claims |
| **7** | Added mass per satellite is **monotone decreasing** in surviving fraction | The model is not behaving |
| **8** | The largest single contributor to credit loss is **identified and named** | The result is not actionable |

## Predictions, recorded before the run

1. **Band 6 fails.** ADR-032's 30 % was written when the store was a different mass; A43 has since
   settled it at 5.38 kg, and the break-even moves with it. I expect the true figure near **16 %**,
   about half what the decision record claims.
2. **Band 5 fails**, because 8.00 kg is 18.5 % of the credit and that is already past a ~16 %
   break-even. *One line item, admitted by P10 to be unmodelled, would fire the falsifier alone.*
3. **Band 4 fails**, and not narrowly.
4. **Band 2 passes**, since it is arithmetic already done.

If 1–3 all fail, **the honest reading is that Gen6's mass case rests on a credit with far less
margin than ADR-032 records**, and the ADR needs its falsifier restated rather than the design
changed.

## Result

*Not yet run.*
