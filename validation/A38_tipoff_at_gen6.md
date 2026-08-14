# A38 — does A34's cradle closure survive the Gen6 operating point?

**Bands declared 2026-08-14, before `analysis/tipoff_gen6.py` existed.**
Verify with `git show --stat <this commit> -- analysis/tipoff_gen6.py`, which must return nothing.

---

## Why this run exists

[A34](A34_cradle_restitution.md) closed kill criterion 4's open half on 2026-08-13 and closed it
well: the payload's rattle across its cradle clearance **settles in 27.25 ms of a 146.4 ms powered
stroke**, the **residual angular rate at force removal is exactly zero** for every clearance A23
tabulated, and critical restitution is **0.9261** against a published aluminium range of 0.3–0.7.

**Every one of those numbers was computed at the Gen5 operating point.**

[A37](A37_host_integrated.md) moves it. With no mover, the payload takes the whole push at the 25 g
cap: **981 N instead of 413**, so the offset moment goes from **28.92 N·m to about 68.7 N·m** —
a factor of **2.4 on the term that drives the entire A34 result**.

**This is the P19 and P53 pattern**, which this project has now recorded twice: an analysis that
closed at one operating point, left standing while the point moved underneath it. The difference
here is that the point has not moved yet. **Checking before adopting is the whole discipline.**

## The prediction, written before the script

**Stated now, so it can fail.** From the closed forms A34 already declares:

- Arrival rate scales as **√α**, so 36–231 °/s becomes roughly **55–356 °/s**. Worse, and still
  transient.
- Settling time goes as **ω₀/α ∝ 1/√α**, so it **falls** to roughly **18 ms**. Faster.
- Powered stroke at 25 g over the A37 window is about **134 ms**, close to Gen5's 146.4.
- **So the margin should improve, not degrade** — settling occupies a smaller fraction of a
  similar stroke.
- **The cost lands on preload**, which scales with the moment: **85 N per contact becomes about
  204 N.**

**If that is right, tip-off does not cap Gen6 and the A37 window stands.** If it is wrong, A37's
1.83–2.18 m window is computed at an acceleration the payload cannot take, and the store trade must
be re-run before it is written.

## What is not being changed

**The 2 °/s threshold is the flown figure and does not move**, exactly as it did not move when
P30 made it 2.5× harder. **A34's bands are not edited**; this is a new run at a new point, and
A34's result stands as declared at the point it was declared for.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Driven at the **Gen5** point the model reproduces A34's settling time and critical restitution to **1 %** | The model is not the one that produced A34, and nothing below is comparable |
| **2** | At the Gen6 point, residual angular rate at force removal is **< 2 °/s** for **every** clearance A23 tabulated | The payload leaves tumbling. Kill criterion 4 is crossed and Gen6 is dead as drawn |
| **3** | At the Gen6 point, settling completes **inside the powered stroke** at e = 0.7, the top of the published aluminium range | The rattle is still live at release and band 2 passes only by luck of phase |
| **4** | Critical restitution **e\* ≥ 0.80** at the Gen6 point — **A34's own threshold, not relaxed** | Margin against the aluminium range has been spent |
| **5** | Required cradle preload ≤ **250 N** per contact | The preload is no longer an ordinary spring, and the release mechanism A34 already calls non-existent becomes a harder problem than the deployer |
| **6** | **The acceleration ceiling tip-off imposes is ≥ 25 g** | **A37's window is computed at an acceleration the payload cannot take**, and the store trade must be re-run before anything is written |

### Band 6 is the one the next run needs

A37 chose its window at the 25 g qualification cap because that is the payload's limit. **Band 6
asks whether tip-off is a tighter limit than qualification**, and reports the ceiling either way.
Whatever number it returns is the acceleration the store trade must use.

### Band 5 is where the prediction says the cost lands

If preload rises to ~204 N per contact as predicted, it passes — but **A34 already records that the
cradle mechanism does not exist**, and a 204 N preload that must release cleanly in under 1 N of
residual is a harder mechanism than an 85 N one. **Passing band 5 is not the same as the mechanism
being easy.**

## What this run does not do

It does not design a cradle, model contact stiffness, or replace the swept restitution with a
measured one — A34's limitations carry forward unchanged. It assumes the same rigid-body impact
treatment and the same single transverse axis. **It answers one question: whether A34's closure is
still a closure at 2.4× the moment.**

---

## Results

**RUN 2026-08-14. Five of six bands pass. Band 1, the regression check, fails — and that is the
find.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A34 at the Gen5 point within 1 % | settle **27.88** against a recorded **27.25 ms** | **FAIL** |
| 2 | residual < 2 °/s, every clearance | **0.0000 °/s** | **PASS** |
| 3 | settling inside the powered stroke at e = 0.7 | **17.69 ms of 133.3** | **PASS** |
| 4 | critical restitution ≥ 0.80, unrelaxed | **0.9462** | **PASS** |
| 5 | preload ≤ 250 N per contact | **201.7 N** | **PASS** |
| 6 | tip-off ceiling ≥ 25 g | **30.9 g** | **PASS** |

### The answer to the question asked

| | Gen5 | **Gen6** |
|---|---:|---:|
| Acceleration | 10.07 g | **25.00 g** |
| Payload force | 395 N | **981 N** |
| Offset moment | 27.65 N·m | **68.67 N·m** |
| Worst arrival rate | 225.4 °/s | **355.1 °/s** |
| **Settling at e = 0.7** | 27.88 ms | **17.69 ms** |
| Powered stroke | 150.1 ms | 133.3 ms |
| **Residual at release** | 0.0000 °/s | **0.0000 °/s** |
| **Critical restitution** | 0.9263 | **0.9462** |
| Preload per contact | 81.2 N | **201.7 N** |

**A34's closure does not merely survive the Gen6 point — it improves.** Settling occupies **13 % of
the stroke instead of 19 %**, and margin against the published aluminium range of 0.3–0.7 widens.
The arrival rate worsens to 355 °/s and remains what A34 established it to be: **transient, and
never a release rate.**

**Band 6 is what the store trade needed.** The ceiling tip-off imposes is **30.9 g**, above the
**25 g** qualification cap. **Tip-off is not the binding limit and A37's 1.83–2.18 m window
stands.** The cost lands exactly where the prediction said it would: **preload rises from 81 N to
202 N per contact.**

### The prediction, and it held

Written before the script: arrival to *roughly 55–356 °/s* (**355.1**), settling *falling to
roughly 18 ms* (**17.69**), stroke *about 134 ms* (**133.3**), preload *about 204 N* (**201.7**),
and *the margin should improve, not degrade* — it did. **The first prediction this session that a
band did not overturn.**

### Band 1 fails because A34's recorded numbers are stale, and its script is not

Driving A34's own imported forms at today's Gen5 point returns **27.88 ms** and **e\* = 0.9263**.
A34's run sheet records **27.25 ms**, **0.9261**, an **85.0 N** preload and a **146.4 ms** stroke,
from a **413.2 N** push, a **28.92 N·m** moment and **688 rad/s²**.

**Today those are 395.1 N, 27.65 N·m and 658 rad/s².** A34 was recorded on 2026-08-13 at the
operating point that ADR-030 superseded the same day, and `analysis/cradle_restitution.py` computes
its inputs live from `motor_model`, so **the script moved and the record did not.**

**No band verdict flips.** Re-running A34 today passes every one of its five bands: settling
27.88 ms inside a 150.1 ms stroke, e\* 0.9263 ≥ 0.80, preload 81.2 N within 20 % of A23's 85.
**Only the recorded detail values are stale, and they are stale by 2.3 %.**

**A34's run sheet is not edited.** It is a record of a run at its own operating point, which is why
`validation/A*.md` is excluded from every propagation this project runs. It is **annotated in
place**, the same treatment `docs/CROSS_INDUSTRY.md` and `docs/VALIDATION_REPORT.md` carry for the
same reason. Recorded as **P61**.

### What has not changed

The cradle mechanism still does not exist, and A34 said so. Restitution is still swept rather than
measured. **A 202 N preload that must release cleanly inside a 1 N residual is a harder mechanism
than an 81 N one**, and passing band 5 is not the same as that mechanism being easy. Kill criterion
4 remains *modelled, not demonstrated* — what this run establishes is that raising the acceleration
does not make it worse.
