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
