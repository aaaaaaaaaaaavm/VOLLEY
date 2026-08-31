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
