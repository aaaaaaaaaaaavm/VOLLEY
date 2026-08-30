# A72, how long a magnet array the shot can afford to carry

**Closes, if it passes:** the closable half of [P118](../OPEN_PROBLEMS.md#p118).
[A66](A66_tube_shielding.md) found that the wall's drag exceeds the stator's thrust above an
air-gap field of 0.1500 T, and that the carriage magnets face the aluminium wall for the whole
8.0 m stroke rather than only the 144.01 mm under the stator. A66 could not integrate that,
because the magnet array's length is not in `cad/parameters.json` and is dimensioned nowhere.

> ## BANDS DECLARED 2026-08-30, BEFORE `analysis/array_drag.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/array_drag.py`, which must return
> nothing.

## The question, put so that the missing number does not block it

The array length is unknown, so it becomes the variable rather than an input. Two lengths are
computed at each air-gap field and compared:

| | |
|---|---|
| **L_force** | the array length whose engaged area makes the section's specified 948.0 N at 90 kA/m, `L = F / (B K 2πr)` |
| **L_energy** | the array length at which the eddy drag over the 8.0 m stroke has taken the exit velocity down to ADR-034's adopted 29.01 m/s |
| **L_clear** | the array length at which the carriage no longer reaches the muzzle at all |

If `L_force` is larger than `L_energy` at every field a magnet can produce, then no array both
makes the force and lets the shot happen, and the conducting tube and the carriage-borne
secondary do not coexist. That is a statement about the architecture, not about a length nobody
has chosen.

## Inputs

| Input | Value | Source |
|---|---|---|
| Wall, conductivity | 1.0 mm, 3.5e7 S/m | `gen6_drive.tube_wall_mm`, `SIG_AL` in `analysis/phase1_closeout.py` |
| Air-gap radius | bore/2 + wall/2 | `gen6_drive.bore_mm`, A66 |
| Stroke, chamber, charge | 8.0 m, 2.0 L, 22.7258 bar | `gen6_drive.stroke_mm`, `gen6_store` |
| Accelerated mass | 4.0 kg | `precharged.M_PAY` |
| Seal friction | 83.4 N | A41 band 8's allowance, as `gen6_dispersion` uses it |
| Exit velocity, zero friction / adopted | 34.28 / 29.01 m/s | `gen6_drive` |
| Section force, sheet current | 948.0 N, 90 kA/m | `gen6_trim` |
| Magnet remanence | 1.32 T | `motor_model.BR` |
| Wavelength | 48 mm | `stator.wavelength` |

The drag law is A66's, unchanged: the thin-sheet induction curve
`τ = (B²/2μ₀)·2Rm/(1+Rm²)` with `Rm = μ₀σdv/2`, evaluated at the carriage's instantaneous
velocity. It is not linear in velocity and this run does not treat it as though it were: `Rm`
reaches 0.7539 at the muzzle, three quarters of the way to the peak of that curve.

## Acceptance bands

**Six bands. Bands 3, 4 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Model verification.** At zero conductivity, or at zero array length, the integrated shot reproduces `precharged.shot()`'s exit velocity to **1e-6**; and the drag law reproduces A66's shear at A66's own point to **1e-9** | The integrator or the drag law is wrong before any conclusion rests on it. A66's band 1R lesson: verify against a limit and an identity, not against a second approximation |
| **2** | **REPORT, no pass/fail.** The drag energy over the 8.0 m stroke per metre of array, and `L_force`, `L_energy` and `L_clear`, at each field on A66's 0.2 T to remanence ladder | The numbers have to be on the record whichever way the comparison falls |
| **3** | **Some field admits an array that is both long enough to make the force and short enough to keep 29.01 m/s**, `L_force ≤ L_energy` | ADR-033's trim stage cannot be built behind ADR-035's aluminium wall at the adopted design point |
| **4** | **Some field admits an array long enough to make the force that still lets the carriage clear the tube**, `L_force ≤ L_clear` | The two decisions are not merely expensive together, they are mutually exclusive, and one of ADR-033 or ADR-035 has to go |
| **5** | **The verdicts of bands 3 and 4 are unchanged** over conductivity 1.75e7 to 3.5e7 S/m and wall 0.5 to 1.0 mm | The finding rests on two handbook numbers rather than on the architecture, and a hot wall or a thinner one would overturn it |
| **6** | **REPORT.** The wall conductance `σd` at which band 3 would pass at 0.6 T, expressed against the 1.0 mm aluminium wall | *What would have to change* is more useful than *it does not work*, and it is the input to P92's fix trade |

## What this run will not do

It does not choose the fix, and it does not re-open [ADR-035](../docs/adr/035-drive-tube-material.md)
or [ADR-033](../docs/adr/033-gen6-trim-stage.md). It computes what they cost together, which is
the thing [P92](../OPEN_PROBLEMS.md#p92) said no document owns.

It does not resolve [P117](../OPEN_PROBLEMS.md#p117). The 948.0 N it uses is the number A55
specified, carried at face value so that this run's answer does not depend on the one A55 got
wrong. If P117 lowers that force, `L_force` grows and this run's verdict gets worse, not better.

It does not add the stator's own field to the drag. Only the magnets' field is counted, which
makes every drag figure here a lower bound.

It does not correct the accelerated mass. `precharged.py` accelerates 4.0 kg of payload and no
carriage, and this run uses the repository's own shot so the comparison is like for like. A real
carriage mass lowers every exit velocity below, including the baseline.

It measures nothing. E4 stands, and 3.5e7 S/m is a handbook value at room temperature.

---

## Correction, 2026-08-30, bands 3 and 4 are withdrawn as defective, before the script exists

**No result has been produced. Nothing has been run.** Both defects are visible from the inputs
alone, and both are the failure [ADR-037](../docs/adr/037-a66-band-one-was-unsatisfiable.md)
describes: a band that cannot discriminate is not a gate, whichever way it is stuck.

**Band 4 could never fail.** The eddy drag is proportional to velocity at small `Rm` and vanishes
with it, and the gas force never falls below the seal friction: the charge starts at 22.7258 bar,
445.88 N, and is still at 10.0994 bar, **198.15 N**, at the muzzle, against 83.4 N of friction.
A carriage carrying any array therefore always reaches the muzzle, however slowly. `L_clear` is
unbounded and `L_force ≤ L_clear` is true for every input.

**Band 3 fails at zero array length, so it measures nothing.** ADR-034's adopted 29.01 m/s is
`sqrt(2(W − 83.4 × 8.0)/4.0)` = 29.0089, which is the zero-friction 34.28 m/s with the *entire*
tolerable friction allowance already subtracted — 28.3887 % of shot work. There is no margin left
between the adopted velocity and the loss budget, so `L_energy` is 0 and the band fails before
any magnet exists. That is a true and useful sentence about the design point, and it is written
into the result below as one. It is not a threshold.

**The declared rows above are not edited.** They stay as frozen, and the two below replace them.

> ### BANDS 3R AND 4R, DECLARED 2026-08-30, BEFORE `analysis/array_drag.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/array_drag.py`, which must return
> nothing.

Both thresholds are taken from quantities the repository already accepts, so that neither is a
number chosen by me:

| | |
|---|---|
| **L_parity** | the array length at which the eddy drag takes **the same energy the seal friction takes**, 28.3887 % of shot work. ADR-034 and A49 band 6 already accept a loss of that size, so it is the repository's own yardstick for *what a tolerable parasitic loss looks like* |
| **L_stall** | the array length at which the carriage stops accelerating before the muzzle — `dv/dx = 0` somewhere in the stroke. Beyond it the machine is a gas spring against a brake rather than an accelerator, and that is a change of kind, not of degree |

| # | Band | FAIL if |
|---|---|---|
| **3R** | **Some field admits an array both long enough to make the section's force and short enough that the drag costs no more than the friction already does**, `L_force ≤ L_parity` | The eddy drag is not a second friction term to be budgeted. It is a larger loss than the one ADR-034 spent a design point accommodating |
| **4R** | **Some field admits an array long enough to make the force at which the carriage is still accelerating at the muzzle**, `L_force ≤ L_stall` | ADR-033's carriage-borne secondary and ADR-035's aluminium wall are mutually exclusive, not merely expensive together |

Bands 1, 2, 5 and 6 are untouched, and band 5 now tests the stability of 3R and 4R.
