# A75, whether the decay model is the wrong shape or just at the wrong level

**Closes, if it passes:** the calculable half of [P79](../OPEN_PROBLEMS.md#p79).

[A50](A50_campaign_altitude.md) band 1 was declared as a calibration against
[E28](../OPEN_PROBLEMS.md)'s own GMAT runs and it failed: `astro.py` gives **70.6 days** at 350 km
where those runs reentered at **36 and 29**. P79 records the cause as a static atmosphere and asks
for a variable-density model.

**Before writing one, this run asks the cheaper question.** `astro.rho` already carries a
piecewise-exponential table with its own scale heights, so its *shape* in altitude is not flat. It
takes a single multiplicative `scale` for activity, and A50 ran at 1.0 without saying so. If one
uniform scale reproduces both GMAT cases and does not break the third, then the defect is the
*level* the model is quoted at and not its *form*, and the repair is to quote a range rather than
to rebuild the atmosphere.

> ## BANDS DECLARED 2026-08-31, BEFORE `analysis/decay_calibration.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/decay_calibration.py`, which must return
> nothing.
>
> A coarse probe of `astro.lifetime` over seven scale values was run in a scratch directory to
> confirm the function returns years and that the search interval brackets the answer. It is not
> committed, and no threshold below is taken from it.

## The evidence this run is calibrated against

All of it is already in the repository, and none of it is a measurement — GMAT is a second model,
which is what makes this a calibration between two models and not a validation against reality.

| | | |
|---|---|---|
| R2, 350 km, 55.2° | reentered at **36 days** | E28, quoted in A50 |
| R3, 350 km, 9.6° | reentered at **29 days** | E28, quoted in A50 |
| 450 km case | **ran the full 90 days** | E28; a one-sided constraint, not a fitting point |
| `astro.py` at scale 1.0, 350 km, BC 61 | **70.6 days** | A50 band 1 |
| Ballistic coefficient | 61.0 kg/m², `BC_SAT`, carried unchanged | `analysis/campaign_altitude.py` |

## Acceptance bands

**Six bands. Bands 3, 4 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Verification by identity.** `astro.rho` and `astro.lifetime` are imported and not restated, and at scale 1.0 the model reproduces A50's published **70.6 d** at 350 km and A50's own 450 km figure to **0.1 %** | The calibration is being fitted with a second, unverified copy of the model it claims to calibrate |
| **2** | **REPORT, no pass/fail.** The uniform density scale that reproduces each GMAT case, and the largest scale the 450 km case still permits | The numbers have to be on the record whichever way the bands fall |
| **3** | **One uniform scale explains both 350 km cases**, the two inferred values agreeing within a factor of **2** | The repair's own spread is as large as the defect it repairs, and a uniform scale explains nothing — the atmosphere's *form* is then the problem and a variable-density model is required rather than optional |
| **4** | **The scale calibrated at 350 km does not break the 450 km evidence**: at the calibrated scale, a satellite at 450 km still exceeds **90 days** | A scale fitted at one altitude that falsifies the evidence at another is not a calibration, it is a curve through one point |
| **5** | **A50's altitude monotonicity survives**, its band 3, at the calibrated scale | A conclusion A50 published changes because of this repair, which would make the repair a correction to A50 rather than a calibration of its input |
| **6** | **REPORT.** A50's campaign durations re-quoted across the calibrated scale band, and what is left open in E28 and P79 | *"450 km buys months"* is the honest reading P79 asked for, and it needs a number beside it |

## What this run will not do

**It does not write a variable-density atmosphere**, and it does not close that half of P79. It
tests whether one is needed, which is a different and cheaper question, and if bands 3 and 4 pass
then the answer is that the model's altitude shape was never the problem.

**It does not close [E28](../OPEN_PROBLEMS.md).** E28 asks for a campaign mission life at a real
deployment altitude, written where the host is described rather than only in a run sheet. This
supplies the number; the propagation is separate.

**It does not run [A9](A9_tle_decay.md), and A9 is still not runnable.** CelesTrak was re-tested
from this environment on 2026-08-31 and the egress proxy still refuses the connection under
organisation policy, exactly as A9 recorded when it was written. The repository therefore still
has no comparison against a flown object, and this run is two models against each other like every
other one. [E4](../OPEN_PROBLEMS.md) stands.

**It does not change A50's bands or re-run A50.** A50's band 1 failed and stays failed; a
calibration performed after a band fails does not retroactively pass it.

It does not touch Gen5's baseline, which contains no lifetime figure derived from this model
beyond the ×1.60 ratio [P16](../OPEN_PROBLEMS.md) already withdrew and re-quoted at a stated
activity level.

---

## Result

**RUN 2026-08-31. All six bands pass, and the answer is that `astro.py`'s altitude shape was never
the problem.**

| # | Band | Result | |
|---|---|---|---|
| 1 | the imported model reproduces A50's published figures | **70.5656 d against 70.6**, 4.9e-4; 450 km 476.6 d | **PASS** |
| 2 | the scale each GMAT case implies | **1.9667** and **2.4443**; 450 km permits up to 5.3093 | **REPORT** |
| 3 | one uniform scale explains both 350 km cases, within 2× | **1.2428×** | **PASS** |
| 4 | the calibrated scale does not break the 450 km evidence | **195.1 to 242.5 d** against the 90 it survived | **PASS** |
| 5 | A50's altitude monotonicity survives at both ends | monotone at 1.9667 and at 2.4443 | **PASS** |
| 6 | A50's durations re-quoted across the band | below | **REPORT** |

### The disagreement is a level, and it is a factor of about two

| GMAT case | inclination | reentered | uniform density scale it implies |
|---|---:|---:|---:|
| R2 | 55.2° | 36 d | **1.9667** |
| R3 | 9.6° | 29 d | **2.4443** |

> `astro.py`'s piecewise-exponential table already carries eleven base altitudes and their own
> scale heights. **Its shape in altitude was never in question.** What A50 published was that
> table at mean activity, ×1.0, and it did not say so.

The two scales agree to **1.2428×**, against a band that asked for a factor of two. A single
uniform multiplier reproduces two independent GMAT reentries at the same altitude, which is what
band 3 was written to test and is the reason a variable-density atmosphere is not required to
explain the discrepancy P79 records.

### The calibration is checked against evidence it was not fitted to

The 450 km case was never a fitting point — it is a one-sided fact, that the run went the full
90 days. At the calibrated band a 450 km satellite lives **195.1 to 242.5 days**, comfortably
clearing it, and on its own that case would have permitted any scale up to **5.3093**. A scale
fitted at one altitude that falsified the evidence at another would be a curve through one point;
this one is not.

### Re-quoted, which is what P79 asked for

| Altitude | at scale 1.0, as A50 published it | across the calibrated band |
|---|---:|---:|
| 300 km | 23.9 d | **9.8 to 12.2 d** |
| 350 km | 70.6 d | **29.0 to 36.0 d** |
| 400 km | 189.1 d | **77.5 to 96.3 d** |
| 450 km | 476.6 d | **195.1 to 242.5 d** |
| 500 km | 1128.0 d | **461.6 to 573.7 d** |
| 600 km | 5792.0 d | **2369.7 to 2945.1 d** |

**"450 km buys months" is 6.4 to 8.0 months.** And the 400 km row is the one worth reading twice:
**77.5 to 96.3 days straddles the 90-day campaign this project has quoted**, so a 90-day campaign
needs 400 km at the mild end of the band and more than 400 km at the harsh end. That is a design
statement the single number could not make.

### The 1.2428× residual is not noise, and it is not explained away

Two cases at the *same altitude* need *different* scales. A scalar multiplier cannot carry that by
construction, so the residual is real and it is what a variable-density atmosphere would account
for. Inclination is the obvious candidate — 55.2° and 9.6° sample very different mean densities
along their ground tracks — and this run does not attempt it. **The half of P79 that asks for a
variable-density model stays open**, and it is now a 1.24× question rather than a 2.4× one.

### What this does not do, stated because each is a way to over-read the result

**It does not retroactively pass A50 band 1.** That band asked for ≤ 60 days at 350 km and got
70.6, and it failed. At the calibrated scale the model gives 29.0 to 36.0, which would have
passed — and a calibration performed after a band fails does not reach back and change the
verdict. A50 band 1 stays failed on the page.

**It does not rescue [P16](../OPEN_PROBLEMS.md).** P16 withdrew a lifetime-invariance claim
because a uniform density scaling preserves a lifetime *ratio* by construction, so the sweep that
tested it could not have falsified it. Nothing here changes that: this run calibrates absolute
lifetimes at one altitude, and it says nothing about whether a real atmosphere preserves ratios.
A5's GMAT falsification stands, and the ×1.60 stays quoted at a stated activity level.

**It is not a measurement.** GMAT is a second model. [A9](A9_tle_decay.md) remains the only run
specified anywhere in `validation/` that would compare against a flown object, and CelesTrak was
re-tested from this environment on 2026-08-31: the egress proxy still refuses the connection under
organisation policy, exactly as A9 recorded when it was written. **[E4](../OPEN_PROBLEMS.md)
stands, and it stands for the same reason it did in July.**

**It does not close [E28](../OPEN_PROBLEMS.md).** E28 asks for a campaign mission life at a real
deployment altitude, written where the host is described rather than in a run sheet. This supplies
the number.

### One thing measured on the way

`astro.lifetime` advances in chunks of `int(min(50/|da|, 5000))` revolutions, and `int()` of a
float is a step function — the class of hazard that made the freshness gate compare numerically
rather than byte-for-byte. Rather than argue about it, the density scale was perturbed by one, two
and four ulp and the ballistic coefficient by one, and the 350 km lifetime moved by **exactly zero
in all four cases**: the chunked advance quantises the answer. This run is therefore *in* the
freshness gate at its default tolerance rather than excluded from it.
