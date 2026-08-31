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
