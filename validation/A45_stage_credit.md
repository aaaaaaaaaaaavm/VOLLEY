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

**RUN 2026-08-16. Five of eight bands pass. The three that fail are bands 4, 5 and 6, and they say
ADR-032's first falsifier fires.**

| # | Band | Result | |
|---|---|---|---|
| 1 | line items reproduce 43.33 kg to 0.01 kg | 43.3299 kg | **PASS** |
| 2 | full credit reproduces A43's 1.403 kg/sat within 0.5 % | 1.403 kg, 0.02 % off | **PASS** |
| 3 | every item carries a written reason | 0 unjustified | **PASS** |
| 4 | hostile reading keeps per satellite ≤ 2.0 kg | **3.108 kg** | **FAIL** |
| 5 | removing P10's lump alone keeps it ≤ 2.0 kg | **2.069 kg** | **FAIL** |
| 6 | uniform break-even ≥ 30 %, as ADR-032 states | **16.5 %** | **FAIL** |
| 7 | monotone in surviving fraction | monotone | **PASS** |
| 8 | largest contributor identified | the P10 lump, 8.00 kg | **PASS** |

### Where the credit goes

| kg | Survives | Lost | Item |
|---:|---:|---:|---|
| 6.83 | 0.50 | 3.41 | Track longerons |
| 5.50 | 0.60 | 2.20 | Battery + avionics + IMU |
| 2.50 | 0.50 | 1.25 | Harness |
| 6.00 | 0.40 | 3.60 | Thermal |
| 9.00 | 0.90 | 0.90 | ESPA bracket |
| 5.50 | 0.80 | 1.10 | Panels / closeouts |
| **8.00** | **0.00** | **8.00** | **Enclosure / radiator / packaged avionics (P10)** |
| **43.33** | | **20.46** | **47.2 % of the credit** |

### The two findings that do not depend on my judgement

**The surviving fractions above are judgements and the reader may substitute their own.** Two
results do not move if they do.

**One — the break-even is 16.5 %, not 30 %.** Pure arithmetic from A43's settled store: the credit
may fail by **7.17 kg** before added mass per satellite reaches 2.0. **ADR-032 states 30 %, which
is nearly twice the real margin.** The ADR was not wrong when written — it predates A43 settling
the store at 5.38 kg — but it is wrong now, and it is the number a reviewer would check.

**Two — the largest item in the credit is a mass the repository already admits it never
itemised.** The 8.00 kg *enclosure, radiator and packaged avionics* line is **P10**, which records
that these have **no line items** in `mass_properties.py` and that the 84.5 kg dry mass is *a
floor, not a total*. Crediting it to the stage converts an admitted unknown into a saving.

**That single item is 18.5 % of the credit, against a 16.5 % break-even.** Removing it and nothing
else gives **2.069 kg per satellite** — **the falsifier fires on one line, with no hostile reading
required at all.**

### What this means, stated plainly

**ADR-032 falsifier 1 fires. [A37](A37_host_integrated.md) band 5 fails retrospectively under a
hostile credit, and kill criterion 1 is crossed on *both* numerators rather than one.**

**A37's band is not edited and its result stands as declared.** A37 asked whether the credit closes
the criterion on the assignment it made, and the answer it recorded is correct for that
assignment. What A45 adds is that the assignment does not survive being disbelieved.

**Nothing here says Gen6 is wrong.** It says the mass case has **half the margin the decision
record claims**, and that the biggest single piece of it is an item this project has been carrying
as unmodelled since long before Gen6 existed. **Recorded as P68.**

### The predictions

**All four held**, which is now twice in a row after A43 and against A44's miss.

1. Break-even near 16 % — **16.5 %**.
2. P10's lump alone fires the falsifier — **2.069 kg**, and 18.5 % against a 16.5 % break-even.
3. Band 4 fails and not narrowly — **3.108 kg against 2.0**.
4. Band 2 passes — 0.02 % off.

## What this run does not do

- **The surviving fractions are not measurements.** They are one reader's judgement, declared in
  advance and swept; the break-even is published so anyone can substitute their own.
- **It does not price the stage agreement**, which remains the thing no analysis can close.
- **It does not re-open A35's ledger.** Every line and every mass is A35's; only the assignment is
  questioned.
- **It proposes no fix.** Closing P10 — building the enclosure, radiator and avionics up from line
  items — is the work that would replace the largest guess with a number, and it is not done here.
