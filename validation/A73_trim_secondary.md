# A73, the trim secondary derived for the annulus it is actually drawn as

**Closes, if it passes:** [P117](../OPEN_PROBLEMS.md#p117). The Gen6 trim section's force is
`KT * SHEET_A_PER_M / 1e3` in `analysis/trim_stage.py`, and [A2](A2_field_3d.md) defines that
thrust constant over `motor_model.SLED_ACTIVE_LEN` — **0.34 m of flat, double-sided Halbach array
0.09 m deep**. [A55](A55_trim_authority.md) applied it, unrescaled, to **0.14401 m of single-sided
annulus around a 15.805 mm bore**. [A66](A66_tube_shielding.md) found that the 948.0 N this
produces needs 1.3854 T across the real air-gap surface, against a 1.32 T remanence, and stopped
there because bounding a number is not deriving it.

> ## BANDS DECLARED 2026-08-30, BEFORE `analysis/trim_secondary.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/trim_secondary.py`, which must return
> nothing.
>
> An exploratory probe was run in a scratch directory to establish that `magpylib.CylinderSegment`
> can express a radially magnetised ring at all. It is not committed, it computed no band value,
> and every threshold below is taken from a document or from geometry rather than from it.

## What is being computed, and why the transfer needs three corrections and not one

| | Gen5, where the constant is defined | Gen6 trim, where it is used |
|---|---|---|
| Array | **double-sided**, one flat Halbach either side of the winding at ±6 mm | **single-sided**, an annulus inside the winding |
| Interaction surface | flat, 0.34 m × 0.09 m = **306.0 cm²** | annular, 0.14401 m × 52.79 mm = **76.03 cm²** |
| Curvature | none | a 7.9 mm bore radius against a 48 mm wavelength |

A55 applied none of the three. This run derives the constant for the second column by the same
Lorentz integral `motor_model.thrust_constant()` uses, with the annular field substituted for the
flat one, so that no convention — the factor of two in a time average, the phase at which the
current sits, the normalisation to 45 kA/m — is re-decided on the way.

## Inputs

| Input | Value | Source |
|---|---|---|
| Bore, wall | 15.805 mm, 1.0 mm | `gen6_drive` |
| Carriage envelope as drawn | piston radius **7.8025 mm**, length **12.0 mm** | `cad/build_gen6.py` `carriage()` |
| Winding inner radius, radial depth | bore/2 + wall, 6.0 mm | `cad/build_gen6.py` `trim_stator()` |
| Section length | 144.01 mm | `gen6_trim.section_length_mm` |
| Wavelength, pole pitch | 48 mm, 24 mm | `stator` |
| Remanence, winding thickness, fill | 1.32 T, 10.0 mm, 0.60 | `motor_model.BR`, `WIND_THICK`, `FILL` |
| Sheet current, specified force | 90 kA/m, 948.0 N | `gen6_trim` |
| Gen5 thrust constant to reproduce | 10.5386 N per kA/m | `motor_model.thrust_constant()`, A2 |
| Magnet density | 7500 kg/m³ | NdFeB, handbook. E4: not measured |
| Per-satellite added-mass ceiling | 2.0 kg | A55 band 7 |

## Acceptance bands

**Six bands. Bands 3, 4 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Model verification, by identity and by limit.** (a) The generalised Lorentz integral, fed `motor_model`'s own flat field and Gen5's geometry, reproduces **10.5386 N per kA/m to 1e-6** relative. (b) Doubling the annular model's angular sector count moves the peak radial field by **≤ 1 %**. (c) At a bore radius large against the wavelength, `r_o ≥ 20λ`, the annular model reproduces a flat single-sided array of the same depth, standoff, remanence and segments per wavelength to **5 %** | The integral, the discretisation or the curved geometry is wrong before any conclusion rests on it. A66 band 1R's lesson: an identity and a limit, never a tolerance on the gap between two approximations of different kinds |
| **2** | **REPORT, no pass/fail.** Radial field at the wall mid-radius and at the winding, the derived thrust constant, and the force at 90 kA/m, against magnet depth from 1 mm to the largest the bore admits | The transfer's size has to be on the record whichever way band 3 falls |
| **3** | **The section as drawn reaches its specified 948.0 N** at some magnet depth the bore admits | `gen6_trim.force_N` is not available from the geometry it is recorded against, and every number A55 derived from it — the 144.01 mm section, the 28.6 kW peak, the 136.59 J correction, ADR-033's unweighed store — moves |
| **4** | **The array that reaches 948.0 N fits inside the carriage `cad/build_gen6.py` draws**, 7.8025 mm radius and 12.0 mm long | The secondary ADR-033 assumes has no drawn home. The CAD can of course be changed; a decision that requires redrawing the part it acts on, and has not said so, is the thing this band exists to surface |
| **5** | **Per-satellite added mass stays ≤ 2.0 kg with the array counted ONCE PER CARRIAGE** — [ADR-035](../docs/adr/035-drive-tube-material.md) records that the carriage is not recovered and *"each of the twelve satellites has its own"*, so the array is not divided by twelve the way the shared stator section is | Gen6 re-crosses the one kill-criterion numerator it currently passes, and it does so on a mass nobody has weighed |
| **6** | **REPORT.** The annular result against a flat ideal-Halbach closed form at the same depth and standoff, so the size of the curvature and single-sidedness effects is on the record | Curvature is a physical difference and not a numerical error, so no tolerance is set on it. ADR-037 |

## What this run will not do

It does not redesign the secondary. It computes what the geometry already drawn can produce.

It does not re-open [ADR-033](../docs/adr/033-gen6-trim-stage.md), and it does not depend on
[A72](A72_trim_array_drag.md)'s verdict. A72 says the trim stage cannot work behind an aluminium
wall; this run asks the separate question of whether its force number was ever available from its
own geometry, and the answer stands whichever fix P92's trade eventually takes.

It models no end effects. The array is evaluated over its interior, exactly as
`motor_model.build_field()` does with `end_turns_modelled: false`, and every force here is
therefore an upper bound.

It measures nothing. E4 stands, and the remanence and the density are handbook values.

---

## Result

**RUN 2026-08-30. Band 1 passes on all three clauses, bands 3, 4 and 5 fail, and the section's
force specification is wrong by 16.7×.**

| # | Band | Result | |
|---|---|---|---|
| 1 | integral identity, sector convergence, large-radius limit | **0.0e+00**, 0.1037 %, 0.463 % against 1e-6, 1 %, 5 % | **PASS** |
| 2 | thrust constant against magnet depth | below | **REPORT** |
| **3** | the section as drawn reaches 948.0 N | **56.91 N, 6.00 % of specified** | **FAIL, 16.7×** |
| **4** | the array that reaches 948.0 N fits the drawn carriage | **2398.9 mm against a 12.0 mm piston** | **FAIL, 200×** |
| **5** | per-satellite added mass ≤ 2.0 kg, array counted per carriage | as drawn **1.6050 kg**; at 948.0 N, **6.44 kg** | **FAIL** |
| 6 | the annulus against a flat array, same depth and standoff | 0.537261 T against 0.429822 T, **1.2500** | **REPORT** |

### Band 1 is worth stating first, because everything else rests on it

The generalised Lorentz integral, handed `motor_model`'s own flat field and Gen5's geometry,
returns **10.538611491665296 N per kA/m** against `motor_model.thrust_constant()`'s
**10.538611491665296** — a relative difference of **exactly zero**. The integral is the same
integral. No phase convention, no factor of two in a time average, no 45 kA/m normalisation and no
wavelengths-per-array scaling is re-decided between the machine the constant was measured on and
the machine it is being applied to.

The curved geometry is checked against a limit rather than against a second approximation: at a
bore radius of twenty wavelengths the annular model reproduces a flat single-sided array of the
same depth and standoff to **0.463 %**. A cylinder that large is a plane, and the model knows it.

### Band 2, and what the three missing corrections are worth

| Magnet depth | K<sub>t</sub> | force at 90 kA/m | of the specified 948.0 N | peak `B_r` at the wall | per satellite |
|---|---:|---:|---:|---:|---:|
| 1.5 mm | 0.2041 | 18.37 N | 1.94 % | 0.3128 T | 1.4705 kg |
| 3.0 mm | 0.3729 | 33.56 N | 3.54 % | 0.4283 T | 1.5270 kg |
| 4.5 mm | 0.5040 | 45.36 N | 4.78 % | 0.4901 T | 1.5683 kg |
| 6.0 mm | 0.5927 | 53.35 N | 5.63 % | 0.5239 T | 1.5943 kg |
| **7.5 mm** | **0.6323** | **56.91 N** | **6.00 %** | **0.5373 T** | **1.6050 kg** |

The constant falls from Gen5's **10.5386** to **0.6323** N per kA/m, a factor of **16.67**, and it
splits in two:

| | |
|---|---|
| **4.02×** | the interaction surface, 306.0 cm² of flat array against 76.03 cm² of annulus |
| **4.14×** | everything else — chiefly that Gen5's winding lies **between two arrays** while Gen6's lies **entirely outside one**, so its outer copper sits where the field has decayed by `exp(-kd)` across 6 mm at `k` = 130.9 m⁻¹, to 45.6 % of the value at its inner face |

**A55 applied neither.** It took the constant of a 0.34 m double-sided flat machine and wrote it
against 0.14401 m of single-sided annulus.

Returns on magnet depth die at about 6 mm, which is what a 24 mm pole pitch predicts: the field of
a Halbach saturates near `kh` = 1, and `1/k` here is 7.639 mm against a bore radius of 7.9025.
**The array wants essentially the whole bore to develop the field this pole pitch implies**, and at
7.5 mm depth it has 0.3 mm of core left.

### Bands 3, 4 and 5, and what moves with them

`gen6_trim.force_N` is **948.0 N**. The geometry it is recorded against makes **56.91 N**.

Reaching the specified force needs 16.7× more engaged array: **2398.9 mm** of it, against the
**12.0 mm** piston `cad/build_gen6.py` draws — **200 lengths of the part the magnets would live
on**. The CAD can of course be changed. A decision that requires redrawing the component it acts
upon, by two orders of magnitude, and has not said so anywhere, is what band 4 exists to surface.

Mass follows the same factor. `analysis/trim_authority.py` divides the trim section's mass by the
twelve-satellite manifest, which is right for a stator bolted to the machine. It is not right for
the array: [ADR-035](../docs/adr/035-drive-tube-material.md) records that the carriage is not
recovered and *"each of the twelve satellites has its own"*, so **the array is added undivided**.
As drawn that takes the per-satellite figure from A66's 1.4227 kg to **1.6050 kg**; at the length
948.0 N would need, to **6.44 kg** against a 2.0 kg ceiling.

Everything A55 derived from that force moves with it — the 144.01 mm section, the 28.6 kW peak,
the 136.59 J correction energy, and ADR-033's first falsifier, the pulse store still unweighed
under [P77](../OPEN_PROBLEMS.md#p77).

### Band 6: curvature is the only thing on the design's side

A convex array of this radius concentrates its own field. At the same depth and the same 0.6 mm
standoff, the annulus reads **0.537261 T** against a flat array's **0.429822 T** — **1.2500×**.

That is reported and not banded, because the difference is physical rather than numerical and
[ADR-037](../docs/adr/037-a66-band-one-was-unsatisfiable.md) forbids putting a tolerance on a gap
of that kind. It is also the reason the standoff is matched exactly: the first version of this
file compared the annulus at 0.6 mm against a flat array at 0.5 mm and reported 1.1594, which put
an `exp(-k dz)` of 1.3 % inside a number whose whole purpose is to be honest about a 25 % effect.

### What this does not do, and what should not be done next

**It does not change `cad/parameters.json`.** Correcting `force_N` moves the section length, the
peak power, the correction energy, the CAD and A55's own bands, and that is a re-run of A55 rather
than an edit. The wrong number stays visible with [P117](../OPEN_PROBLEMS.md#p117) attached to it
rather than being quietly replaced.

**And that re-run should wait.** [A72](A72_trim_array_drag.md) found, on the same day, that the
carriage-borne secondary and the aluminium wall exclude each other, so re-sizing a trim stage on
an architecture whose fix is undecided would be work thrown away. The order is
[P92](../OPEN_PROBLEMS.md#p92)'s trade first, then A55 re-run against whatever survives it.

Two runs of this file were discarded before the one above: one died serialising a numpy boolean,
and one compared band 6 at mismatched standoffs. Neither produced a number used anywhere.

It models no end effects, so every force here is an upper bound. It measures nothing. E4 stands.
