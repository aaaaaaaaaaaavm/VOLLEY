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
