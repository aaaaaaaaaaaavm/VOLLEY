# A38, does A34's cradle closure survive the Gen6 operating point?

**Bands declared 2026-08-14, before `analysis/tipoff_gen6.py` existed.**
Verify with `git show --stat <this commit> -- analysis/tipoff_gen6.py`, which must return nothing.

---

## Why this run exists

[A34](A34_cradle_restitution.md) closed kill criterion 4's open half on 2026-08-13 and closed it
well: the payload's rattle across its cradle clearance settles in 27.25 ms of a 146.4 ms powered
stroke, the residual angular rate at force removal is exactly zero for every clearance A23
tabulated, and critical restitution is 0.9261 against a published aluminium range of 0.3-0.7.

Every one of those numbers was computed at the Gen5 operating point.

[A37](A37_host_integrated.md) moves it. With no mover, the payload takes the whole push at the 25 g
cap: 981 N instead of 413, so the offset moment goes from 28.92 N·m to about 68.7 N·m,
a factor of 2.4 on the term that drives the entire A34 result.

This is the P19 and P53 pattern, which this project has now recorded twice: an analysis that
closed at one operating point, left standing while the point moved underneath it. The difference
here is that the point has not moved yet. Checking before adopting is the whole discipline.

## The prediction, written before the script

Stated now, so it can fail. From the closed forms A34 already declares:

- Arrival rate scales as √α, so 36-231 °/s becomes roughly 55-356 °/s. Worse, and still
  transient.
- Settling time goes as ω₀/α ∝ 1/√α, so it falls to roughly 18 ms. Faster.
- Powered stroke at 25 g over the A37 window is about 134 ms, close to Gen5's 146.4.
- So the margin should improve, not degrade, settling occupies a smaller fraction of a
  similar stroke.
- The cost lands on preload, which scales with the moment: 85 N per contact becomes about
  204 N.

If that is right, tip-off does not cap Gen6 and the A37 window stands. If it is wrong, A37's
1.83-2.18 m window is computed at an acceleration the payload cannot take, and the store trade must
be re-run before it is written.

## What is not being changed

The 2 °/s threshold is the flown figure and does not move, exactly as it did not move when
P30 made it 2.5× harder. **A34's bands are not edited**; this is a new run at a new point, and
A34's result stands as declared at the point it was declared for.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

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
asks whether tip-off is a tighter limit than qualification, and reports the ceiling either way.
Whatever number it returns is the acceleration the store trade must use.

### Band 5 is where the prediction says the cost lands

If preload rises to ~204 N per contact as predicted, it passes, but A34 already records that the
cradle mechanism does not exist, and a 204 N preload that must release cleanly in under 1 N of
residual is a harder mechanism than an 85 N one. **Passing band 5 is not the same as the mechanism
being easy.

## What this run does not do

It does not design a cradle, model contact stiffness, or replace the swept restitution with a
measured one, A34's limitations carry forward unchanged. It assumes the same rigid-body impact
treatment and the same single transverse axis. It answers one question: whether A34's closure is
still a closure at 2.4x the moment.

---

## Results

> ## CORRECTION 2026-08-22, the run is unchanged, its operating point is not. P102
>
> **Nothing below is edited.** The bands are not re-declared, the verdicts recorded on 2026-08-14
> stand as run, and this block is the whole of the change.
>
> This run took the Gen6 point to be 25 g over 2.18 m, the acceleration cap and the long end
> of [A37](A37_host_integrated.md)'s feasible window, and `analysis/tipoff_gen6.py` held both as
> module constants. [ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) replaced that
> window with the host stage's whole usable length on 2026-08-19, three days later, and this run
> was never pointed at again.
>
> *The opening of this page says the P19/P53 pattern is an analysis left standing while its point
> moves underneath it, and that "the difference here is that the point has not moved yet."
> It moved.*
>
> The script now reads `acceleration_g` and `stroke_mm` from `cad/parameters.json` at import, the
> repair [P84](../OPEN_PROBLEMS.md) applied to `precharged.py`. `G_CAP` stays at 25.0: it is
> the payload qualification cap and **band 6's declared threshold**, and lowering it to the design
> point would have widened a band.
>
> | | Recorded, A37 window | Re-run, design point |
> |---|---:|---:|
> | Acceleration | 25.0 g | 11.362895 g |
> | Acceleration length | 2.18 m | 8.0 m |
> | Payload force | 981.0 N | 445.88 N |
> | Offset moment | 68.67 N·m | 31.21 N·m |
> | Powered stroke | 133.3 ms | 378.9 ms |
> | Worst cradle arrival | 355.1 °/s | 239.4 °/s |
> | Settling at e = 0.7 | 17.69 ms | 26.24 ms |
> | Residual at release | 0.0000 °/s | 0.0000 °/s |
> | Critical restitution | 0.9462 | 0.9712 |
> | Preload per contact | 201.7 N | 91.7 N |
> | Tip-off ceiling | 30.9 g | 30.9 g |
>
> **No band verdict moves.** Band 1 fails as it already did (**P61**); bands 2–6 pass, four with
> more margin. The ceiling does not move because it is set by the 250 N preload limit, which
> depends on acceleration and not on stroke.
>
> Two things this correction does not repair.
>
> `cad/parameters.json` still carries 201.7 N. `gen6_drive.cradle_preload_N_per_contact` is
> this run's figure at 25 g, and `cad/build_gen6.py` says the tube wall is set partly by carrying
> it. It is conservative by 2.2x and nothing reads it as a driver, so it is left as it stands
> and recorded as a decision rather than corrected into a lower retention requirement.
>
> The model is constant-acceleration, and the conservatism that buys is narrower than it first
> reads. `point()` returns 42.23 m/s, which is exactly
> `gen6_drive.exit_velocity_m_s_constant_pressure_bound`; the delivered figure is 29.01 m/s and
> the shot is a blowdown.
>
> What is conservative: the *time available*. A lower delivered exit velocity over the same
> 8.0 m means a longer powered stroke than 378.9 ms, so **band 3's comparison of settling time
> against time available is understated in that one respect.
>
> What is not established: that the contact trajectory or the angular response is conservative
> under the real pressure, time history. Under blowdown the acceleration is time-varying, so the
> angular forcing from any force-line eccentricity is time-varying with it, and contact timing,
> arrival rate and rebound timing all move. A closed form driven by a constant acceleration
> cannot bound a trajectory whose forcing changes shape. This run's Gen6 answer is a bound on one
> scalar comparison, not a bound on the motion. That is [P103](../OPEN_PROBLEMS.md)'s to settle,
> and it is why P103 step 2 requires the design point to be read live rather than a constant
> acceleration to be assumed.
>
> And the larger gap is not in this run at all. A38 models the payload crossing its cradle
> clearance at the start of the stroke. Nothing in this repository models the other eight
> metres, no contact state along the bore, no straightness or roundness, no force-line
> eccentricity, no payload centre-of-mass offset, no lateral or angular state carried through.
> See [`docs/EXTERNAL_EVIDENCE.md`](../docs/EXTERNAL_EVIDENCE.md).


**RUN 2026-08-14. Five of six bands pass. Band 1, the regression check, fails — and that is the
find.

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

A34's closure does not merely survive the Gen6 point, it improves. Settling occupies 13 % of
the stroke instead of 19 %, and margin against the published aluminium range of 0.3-0.7 widens.
The arrival rate worsens to 355 °/s and remains what A34 established it to be: transient, and
never a release rate.

**Band 6 is what the store trade needed.** The ceiling tip-off imposes is **30.9 g**, above the
25 g qualification cap. Tip-off is not the binding limit and A37's 1.83-2.18 m window
stands. The cost lands exactly where the prediction said it would: preload rises from 81 N to
202 N per contact.

### The prediction, and it held

Written before the script: arrival to *roughly 55-356 °/s* (355.1), settling *falling to
roughly 18 ms* (17.69), stroke *about 134 ms* (133.3), preload *about 204 N* (201.7),
and *the margin should improve, not degrade*, it did. The first prediction this session that a
band did not overturn.**

### Band 1 fails because A34's recorded numbers are stale, and its script is not

Driving A34's own imported forms at today's Gen5 point returns 27.88 ms and e\* = 0.9263.
A34's run sheet records 27.25 ms, 0.9261, an 85.0 N preload and a 146.4 ms stroke,
from a 413.2 N push, a 28.92 N·m moment and 688 rad/s².

Today those are 395.1 N, 27.65 N·m and 658 rad/s². A34 was recorded on 2026-08-13 at the
operating point that ADR-030 superseded the same day, and `analysis/cradle_restitution.py` computes
its inputs live from `motor_model`, so the script moved and the record did not.

**No band verdict flips.** Re-running A34 today passes every one of its five bands: settling
27.88 ms inside a 150.1 ms stroke, e\* 0.9263 >= 0.80, preload 81.2 N within 20 % of A23's 85.
Only the recorded detail values are stale, and they are stale by 2.3 %.

A34's run sheet is not edited. It is a record of a run at its own operating point, which is why
`validation/A*.md` is excluded from every propagation this project runs. It is annotated in
place, the same treatment `docs/CROSS_INDUSTRY.md` and `docs/VALIDATION_REPORT.md` carry for the
same reason. Recorded as P61.

### What has not changed

The cradle mechanism still does not exist, and A34 said so. Restitution is still swept rather than
measured. A 202 N preload that must release cleanly inside a 1 N residual is a harder mechanism
than an 81 N one**, and passing band 5 is not the same as that mechanism being easy. Kill criterion
4 remains *modelled, not demonstrated*, what this run establishes is that raising the acceleration
does not make it worse.
