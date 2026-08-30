# A66, what the drive tube costs the trim stator

**Closes, if it passes:** [P92](../OPEN_PROBLEMS.md#p92). [ADR-033](../docs/adr/033-gen6-trim-stage.md)
puts the trim stator outside the drive tube and its magnets inside.
[ADR-035](../docs/adr/035-drive-tube-material.md) then made that tube aluminium, four days later,
on mass alone. A conducting sleeve between a travelling-field stator and its secondary is a
shorted turn at full slip, and no file in this repository has computed what it costs.

> ## BANDS DECLARED 2026-08-30, BEFORE `analysis/tube_shielding.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/tube_shielding.py`, which must return
> nothing.

## What is being computed

The tube never moves. The stator's field travels at synchronous speed past it, so the wall sees
the full synchronous velocity as slip, every shot, whatever the carriage is doing. That is the
whole of the problem and it is why the wall is not a passive spacer.

| Input | Value | Source |
|---|---|---|
| Wall thickness | 1.0 mm | `gen6_drive.tube_wall_mm` |
| Wall material | aluminium 6061-T6 | `gen6_drive.tube_material`, ADR-035 |
| Conductivity | 3.5e7 S/m | `SIG_AL`, `analysis/phase1_closeout.py` |
| Pole pitch, wavelength | 24 mm, 48 mm | `stator.pole_pitch`, `stator.wavelength` |
| Carriage speed at the section | 34.28 m/s | `gen6_drive.exit_velocity_m_s_zero_friction` |
| Section length, force | 144.01 mm, 948.0 N | `gen6_trim.section_length_mm`, `.force_N` |
| Authority the section was sized for | 1.1543 m/s | `gen6_trim.authority_m_s`, A55 band 4 |
| Wall temperature ceiling | 473.0 K | `gen6_drive.tube_temperature_ceiling_K` |
| Shots per campaign | 12 | ADR-030 |

## Acceptance bands

**Six bands. Bands 3, 4 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Model verification.** The sheet model returns transmission 1.000 and zero induced loss at zero conductivity, and reproduces the analytic thin-sheet transmission for a travelling wave to **0.5 %** across at least two decades of sheet conductance | The model is wrong before any VOLLEY geometry enters it. This is A55 band 1's lesson applied again |
| **2** | **REPORT, no pass/fail.** Skin depth at the section's own excitation frequency, and the wall expressed in skin depths | P92 names this as the governing comparison, and it has to be on the record whichever way it falls |
| **3** | **The section as drawn still delivers its sized authority**, 1.1543 m/s, through the wall | The section is under-authority again and [P83](../OPEN_PROBLEMS.md#p83) reopens at the point A55 closed it |
| **4** | **The section length needed to restore 1.1543 m/s stays inside A55 band 5**, 15 % of the 8.0 m stroke | The correction has stopped being a trim and become a second drive, which is A48's own limit |
| **5** | **Added mass per satellite, with the compensated section, stays ≤ 2.0 kg** | Gen6 re-crosses the one kill-criterion numerator it currently passes, A55 band 7 |
| **6** | **An independent implementation agrees on the transmitted force fraction within 10 %** | One method is not a result. Two wrappers around the same expression are not two methods |

## What this run will not do

It does not choose the fix. A non-conducting liner, a slotted or non-conducting section local to
the stator, and the passive-secondary route [`docs/VAULT.md`](../docs/VAULT.md) records under
PII-19 are all live options and none is this run's to pick.

It does not re-open ADR-035. That decision was correct on the questions asked of it, and the
defect P92 records is in the sequencing, not in the choice of aluminium.

It does not measure anything. E4 stands. Conductivity is a handbook value at room temperature and
the wall gets hot, which the run reports rather than resolves.

It does not size the pulse store. That is P77 and A54, still open, and it is ADR-033's falsifier.
