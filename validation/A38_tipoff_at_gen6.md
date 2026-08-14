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

*(Filled after the run. Nothing above this line changes.)*
