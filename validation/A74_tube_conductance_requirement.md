# A74, what the tube has to become, stated as a requirement rather than a material

**Closes, if it passes:** the part of [P92](../OPEN_PROBLEMS.md#p92) that is a calculation.

[A66](A66_tube_shielding.md) priced the attenuation. [A72](A72_trim_array_drag.md) integrated the
drag and found that ADR-033's carriage-borne secondary and ADR-035's aluminium wall exclude each
other. P92's remaining work is the fix trade, and two of its three candidates have already gone: a
non-conducting *section* local to the stator does nothing about a brake that acts over the whole
stroke. This run takes the third and turns the question round.

> ## BANDS DECLARED 2026-08-31, BEFORE `analysis/tube_requirement.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/tube_requirement.py`, which must return
> nothing.

## Why a requirement and not a screen

Screening materials means importing a conductivity and a density for each candidate, and this
repository has exactly one of each — aluminium's 3.5 × 10⁷ S/m and 2700 kg/m³. Six more would be
six more handbook numbers carried at face value into a conclusion, and
[E11](../OPEN_PROBLEMS.md) already records public material screening as its own open item.

So the run computes what the tube must satisfy, from models the repository already owns, and
leaves the search against that requirement to E11 and [E3](../OPEN_PROBLEMS.md). **A requirement
derived from the machine is worth more than a shortlist derived from a table.**

## Inputs

Every one is already in the repository. No new material data enters this run.

| Input | Value | Source |
|---|---|---|
| Drag over thrust | `σ d v B_net / 2K` | [A66](A66_tube_shielding.md), derived there |
| Bands 3R and 4R | `L_force` against `L_parity` and `L_stall` | [A72](A72_trim_array_drag.md), imported not restated |
| Aluminium sheet conductance at 1.0 mm | 35 000 S | `SIG_AL`, `gen6_drive.tube_wall_mm` |
| Wavelength, and the decay it sets | 48 mm, `k` = 130.9 m⁻¹ | `stator.wavelength` |
| Bore | 15.805 mm | `gen6_drive.bore_mm` |
| Wall the gas alone needs | 0.16 mm | [A59](A59_tube_structure.md), hoop at 13.9× margin |
| Wall as drawn, and why | 1.0 mm, set by handling and A38's 201.7 N cradle preload | `cad/build_gen6.py` docstring, A59 |
| The one lower-conductivity metal already priced | steel, **+2.154 kg** | A59 band 9, [A63](A63_steam_design_point.md), ADR-035 |

## Acceptance bands

**Five bands. Bands 3 and 4 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Model verification by identity.** The drag ratio and the band-3R and 4R machinery are imported from `tube_shielding` and `array_drag` rather than restated, and fed A72's own inputs they reproduce A72's published break-even field of 0.1500 T and its best `L_force/L_parity` of 6.8 to **1e-9** | The requirement is being computed by a second, unverified copy of the model it claims to invert |
| **2** | **REPORT, no pass/fail.** The largest sheet conductance `σd` at which A72's bands 3R and 4R pass, at each field on A66's ladder, as an absolute value and as a fraction of aluminium's 35 000 S | This is the requirement, and it has to be on the record as a number a materials search can be run against |
| **3** | **A non-conducting liner inside the aluminium tube can bring the drag-to-thrust ratio to one, within the bore.** The liner thickness required must be **less than the bore radius**, 7.9025 mm | A liner thicker than the radius of the hole it lines is not a liner, and the last of P92's three original candidates goes with it |
| **4** | **Thinning the aluminium wall alone can meet the requirement**, at a thickness A59 admits — that is, **not below the 0.16 mm the gas alone needs** | The wall is not a free variable here. `σd` falls with `d`, so if the required thickness is under the pressure floor, no thickness of *this metal* works and the material has to change |
| **5** | **REPORT.** The mass consequence of the one lower-conductivity metal this repository has already priced, and the per-satellite figure that follows it | ADR-035 chose aluminium on mass alone. What that choice costs, once the electromagnetics is in the room, belongs beside it |

## What this run will not do

**It does not choose the tube material, and it does not name one.** It produces a number. E11 and
E3 own the search against it, and neither is closed by this run.

It does not re-open [ADR-033](../docs/adr/033-gen6-trim-stage.md) or
[ADR-035](../docs/adr/035-drive-tube-material.md). Which of the two yields is a programme decision
and this run supplies one side of the input to it.

It does not price a non-metallic tube. That is a pressure boundary, a sliding seal bore and a
structural column at once, and A59, A58 and A61 would all have to be re-run against it. Naming
that as the next question is the whole of what this run says about it.

It does not revisit A72's verdict. If the requirement is met, A72's bands are re-run against the
new conductance by A72, not here.

It measures nothing. E4 stands.

---

## Result

**RUN 2026-08-31. Band 1 passes by identity, bands 3 and 4 both fail, and the requirement is a
number the tube's present material misses by between eight and fifty-three times.**

| # | Band | Result | |
|---|---|---|---|
| 1 | the imported model reproduces A66's and A72's committed values | **0.0e+00** on both, against 1e-9 | **PASS** |
| 2 | the largest `σd` at which A72's 3R and 4R pass | below | **REPORT** |
| **3** | a liner brings the drag-to-thrust ratio to one within the bore | **0.59 to 15.01 mm; fits at 2 of 6 fields** | **FAIL** |
| **4** | thinning the aluminium wall alone meets it | **18.8 µm against a 160 µm floor, 8.5× below** | **FAIL** |
| 5 | the mass of the one lower-conductivity metal already priced | steel **+2.154 kg**, per satellite **1.7845 kg** | **REPORT** |

### Band 1, and why it is an identity and not a cross-check

This file imports `tube_shielding` and `array_drag` and calls their functions. It does not
re-derive the drag ratio or the length comparisons, so agreement between it and them would prove
nothing about the physics — it would be two names for one expression, which
[A66](A66_tube_shielding.md) band 1R exists to forbid. What band 1 does check is that the import
is **live**: that calling those functions now reproduces the values `tube_shielding.json` and
`array_drag.json` published, to a relative difference of **exactly zero**. A stale import is the
failure mode this run actually has, and that is the one it tests.

### Band 2, the requirement

| Air-gap field | band 3R needs | band 4R needs | as a fraction of aluminium | as an aluminium wall |
|---|---:|---:|---:|---:|
| 0.20 T | **4350.7 S** | 5089.4 S | 12.430 % | 124.3 µm |
| 0.40 T | **2170.4 S** | 2534.9 S | 6.201 % | 62.0 µm |
| 0.60 T | **1446.3 S** | 1688.7 S | 4.132 % | 41.3 µm |
| 0.80 T | **1084.6 S** | 1266.2 S | 3.099 % | 31.0 µm |
| 1.00 T | **867.6 S** | 1012.9 S | 2.479 % | 24.8 µm |
| 1.32 T | **657.2 S** | 767.3 S | 1.878 % | 18.8 µm |

The 0.60 T row is **1446.3 S**, which is A72 band 6's number to the digit — the two runs invert
the same model from opposite ends and land on the same value, which is what makes the rest of the
table worth reading.

> **The drive tube may carry between 1.9 % and 12.4 % of the sheet conductance it has now**,
> depending on the field the secondary works at. That is the requirement, and it is stated without
> naming a single material.

### Band 3: the liner buys one power of the exponential, not two

A liner lines the bore, so the magnets shrink to fit and their surface moves `t` further from the
**winding outside the tube** as well as from the wall. The drag falls as `B²` and the thrust as
`B`, so the *ratio* falls as `exp(-kt)` and not `exp(-2kt)`. At `k` = 130.9 m⁻¹ that is 12.3 % per
millimetre on the ratio rather than 23 %.

| Air-gap field | drag / thrust | liner for ratio = 1 | inside a 7.9025 mm bore radius |
|---|---:|---:|---|
| 0.20 T | 1.08 | **0.59 mm** | yes |
| 0.40 T | 2.16 | **5.89 mm** | yes |
| 0.60 T | 3.24 | 8.98 mm | **no** |
| 1.32 T | 7.13 | **15.01 mm** | **no** |

**The band's wording admitted two readings** — a liner that works at *some* field, or at *every*
field — and the implementation takes the strict one, so the verdict above is the all-fields
reading. Both counts are on the record: it fits at **two of six**. The any-field reading would
pass, and it would pass in the corner where the secondary makes 18.37 N
([A73](A73_trim_secondary.md) band 2) against a 948.0 N specification. A band that passes where
the machine makes nothing tests nothing, which is
[ADR-037](../docs/adr/037-a66-band-one-was-unsatisfiable.md)'s point, and the wording should have
said so.

**P92's third original candidate is gone with it.** All three of the fixes that run-sheet named —
a local non-conducting section, a slotted section, a liner — are now eliminated by the same fact:
the brake is not local, and an insulator does not stop a field.

### Band 4: the wall is not a free variable here

`σd` falls with `d`, so the obvious move is to thin the tube. At the remanence the requirement is
**18.8 µm**. [A59](A59_tube_structure.md) puts the wall the gas alone needs at **0.16 mm**, and
`cad/build_gen6.py` sets the 1.0 mm as drawn by handling and by A38's 201.7 N cradle preload.

**18.8 µm is 8.5× below the pressure floor and 53× below the wall as drawn.** No thickness of this
metal works, so the material has to change.

### Band 5, and the one number ADR-035 did not have

[ADR-035](../docs/adr/035-drive-tube-material.md) chose aluminium on mass alone, and it was right
on the questions asked of it — [A59](A59_tube_structure.md) found strength, stiffness and buckling
all indifferent between the metals. The mass argument was **2.154 kg**.

The tube is shared across the manifest, so that is **+0.1795 kg per satellite**, taking A73's
1.6050 kg to **1.7845 kg** against A55 band 7's 2.0 kg ceiling. **The mass ADR-035 saved is
affordable to give back.** It was never a large number; it was the only number in the room.

### Where this leaves P92

| | |
|---|---|
| A local non-conducting or slotted section | **eliminated by A72** — the brake acts over the whole stroke |
| A non-conducting liner | **eliminated here** — 15.01 mm inside a 7.9025 mm bore radius |
| A tube of a lower-conductivity material | **survives**, and now has a requirement: 657 to 4351 S, 1.9 % to 12.4 % of aluminium's |
| The passive secondary under PII-19 | **survives**, and takes the magnets off the carriage instead |
| Give up ADR-033's carriage-borne secondary | **survives**, and is the fourth route none of the three named |

### What this run does not do

**It names no material and does not choose one.** The requirement is stated so that
[E11](../OPEN_PROBLEMS.md)'s public material screening and [E3](../OPEN_PROBLEMS.md)'s component
selection can be run against it, and neither is closed here. A72's own run sheet already records
the one observation this repository can make without new data, and it stays there rather than
being repeated as though this run produced it.

It does not price a non-metallic tube. That part is a pressure boundary, a sliding seal bore and a
structural column at once, and A59, A58 and A61 would all have to be re-run against it.

It does not re-run A72 at the new conductance. If a material is chosen, A72's bands are re-run
there, in A72, against whatever it is.

Two runs died on wrong imports before the one above, neither producing a value.

It measures nothing. E4 stands, and 3.5 × 10⁷ S/m is a handbook figure at room temperature for a
wall this repository has shown gets hot.
