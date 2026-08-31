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

---

## Result

**RUN 2026-08-30. Bands 1 and 5 pass, 2 and 6 report, and bands 3R and 4R fail at every field on
the ladder by between one and one and a half orders of magnitude.**

| # | Band | Result | |
|---|---|---|---|
| 1 | limits against `precharged`, shear against A66 | zero-σ and zero-length **2.9e-15** against 1e-6; shear **1.6e-16** against 1e-9 | **PASS** |
| 2 | the three lengths at each field | below | **REPORT** |
| **3R** | `L_force ≤ L_parity` at some field | best **6.8×** over, at 0.20 T | **FAIL** |
| **4R** | `L_force ≤ L_stall` at some field | best **5.6×** over, at 0.20 T | **FAIL** |
| 5 | verdicts hold over σ 1.75e7–3.5e7 and wall 0.5–1.0 mm | **4 of 4 corners agree** | **PASS** |
| 6 | the conductance at which 3R would pass at 0.6 T | **1446.3 S**, 4.132 % of aluminium's 35 000 | **REPORT** |

### Band 2, and it is the whole answer

| Air-gap field | `L_force` | `L_parity` | `L_stall` | force/parity | force/stall | exit velocity at `L_force` |
|---|---:|---:|---:|---:|---:|---:|
| **0.20 T** | 997.6 mm | **147.29 mm** | **178.56 mm** | **6.8×** | 5.6× | **3.2991 m/s** |
| **0.40 T** | 498.8 mm | **36.82 mm** | **44.64 mm** | **13.5×** | 11.2× | **1.5763 m/s** |
| **0.60 T** | 332.5 mm | **16.37 mm** | **19.84 mm** | **20.3×** | 16.8× | **1.0433 m/s** |
| **0.80 T** | 249.4 mm | **9.21 mm** | **11.16 mm** | **27.1×** | 22.3× | **0.7806 m/s** |
| **1.00 T** | 199.5 mm | **5.89 mm** | **7.14 mm** | **33.9×** | 27.9× | **0.6238 m/s** |
| **1.32 T** | 151.1 mm | **3.38 mm** | **4.10 mm** | **44.7×** | 36.9× | **0.4721 m/s** |

Read the last column first. **At the array length the section's own force specification requires,
the carriage leaves an 8.0 m tube at between 0.47 and 3.30 m/s** against ADR-034's adopted 29.01,
and at every field it is *decelerating* when it gets there. The eddy drag takes **71 % of the shot
work** at every one of those points — 70.69 % at 0.2 T and 71.59 % at the remanence, which is
nearly field-independent because the array shortens as the field rises and the two effects
cancel. Beside a seal friction the design already spends 28.39 % on, that is the whole shot.

There is no favourable end of the ladder. A weaker magnet needs a longer array, and the drag
scales with the array, so the ratio gets *worse* as the field falls, not better — 6.8× at 0.2 T
against 44.7× at the remanence. **The trade the ladder looks like it offers does not exist.**

### The two decisions are not expensive together, they are exclusive

[ADR-033](../docs/adr/033-gen6-trim-stage.md) put the trim stator outside the tube and its magnets
on the carriage. [ADR-035](../docs/adr/035-drive-tube-material.md) made that tube aluminium, four
days later, on mass. Each is defensible on the questions asked of it. Together they put a
permanent-magnet array and a stationary 35 000 S conducting sheet in relative motion at 34.28 m/s
for eight metres, which is an eddy-current brake, and the brake is stronger than the gas gun.

> The magnets do not need the stator to be energised. They brake from the first millimetre of
> travel, on every shot, whatever the trim stage is doing.

That is what [P92](../OPEN_PROBLEMS.md#p92) meant by a defect in the sequencing rather than in
either decision.

**None of this touches Gen5.** The Phase I machine is a flat ironless stator with no tube, no
sleeve and no conducting member between the winding and the array, and nothing in this run applies
to it or to any number in [`docs/BASELINE.md`](../docs/BASELINE.md).

### Band 5 is the band that makes this hard to dismiss

Halving the conductivity, which a hot wall does, and halving the wall, which the mass argument
would like, **both leave the verdict unchanged, and so does doing both**. Four corners, four
identical answers. The finding is not sitting on a handbook conductivity or on a 1.0 mm wall
chosen for handling; it sits on the architecture.

### Band 6, which is the useful half for P92's trade

Band 3R would pass at 0.6 T only if the wall's sheet conductance fell to **1446.3 S**, **4.132 %**
of the 1.0 mm aluminium wall's 35 000 — at that thickness, **1.4463 × 10⁶ S/m**.

That figure lands within a few per cent of austenitic stainless steel, whose room-temperature
conductivity is conventionally quoted near 1.4 × 10⁶ S/m. **This is a boundary, not a solution.**
A three per cent margin against a handbook conductivity is not a margin, the number is quoted at
room temperature for a wall that heats, and [A63](A63_steam_design_point.md) already priced steel
at **+2.154 kg** — larger than everything the fluid trade was trying to save. A non-conducting
liner or a non-conducting section is the other direction and this run does not choose between
them. It is [P92](../OPEN_PROBLEMS.md#p92)'s trade and it now has a number in it.

### What was wrong on the way here, and is fixed

Two coding defects, both caught before the result was believed, neither a band.

**The shear check was wired to the reduced field rather than the incident one.** The induction
curve `τ = (B²/2μ₀)·2Rm/(1+Rm²)` already carries the transmission inside it, so passing `B_net`
double-counts it by `1/(1+Rm²)` — **36.2 %** at `Rm` = 0.7539. Band 1 caught it, which is what
band 1 is for.

**Neither the drag energy nor the worst acceleration is monotone in the array length.** The drag
force goes as `v·L` and `v` falls roughly as `1/L`, so both turn round once the array is long
enough to have throttled the shot that drives them. A plain bisection from zero to 4 m saw the
same sign at both ends and returned its own upper bound as an answer for three of the six fields.
The shortest crossing — which is the one that means anything — is now found by scanning before
bisecting.

### What this run still does not resolve

It does not choose between ADR-033 and ADR-035, and it does not fix
[P117](../OPEN_PROBLEMS.md#p117). If P117 lowers the 948.0 N this run took at face value,
`L_force` grows and every ratio above gets worse.

It counts only the magnets' field. The stator's own contribution, `μ₀K/2` = 0.0566 T, is left out,
so every drag figure here is a lower bound.

It accelerates `precharged.py`'s 4.0 kg of payload and no carriage, because that is the shot this
repository publishes. A real carriage mass lowers every velocity in the table, the baseline
included.

It measures nothing. E4 stands.
