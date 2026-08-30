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

---

## Correction, 2026-08-30, band 1 is withdrawn as defective and band 1R replaces it

The first run is `af526a0`. It failed band 1 at 1.4874 % against 0.5 %, and it failed band 3 at
0.9356 m/s against 1.1543.

Band 3's failure is the answer to P92 and it stands. Band 1's is not a failure of the model.
Holding the sheet conductance at 35 000 S and shrinking the wall, the slab converges on the sheet
at first order across three decades — 1.487 % at 1.0 mm, 0.7665 at 0.5, 0.1571 at 0.1, 0.001581 at
0.001 — so both routes are implemented correctly and the 1.4874 % is the thin-sheet truncation
error at the wall this machine has, where `kd` = 0.131. A 0.5 % tolerance sits underneath a number
the geometry fixes at 1.49 %, so no correct implementation could have passed it, and the only code
that could have was code whose two routes shared an error, which is what band 6 exists to catch.
[ADR-037](../docs/adr/037-a66-band-one-was-unsatisfiable.md) is the full argument.

**The declared row above is not edited.** It stays in the words it was frozen in, and `af526a0`
stays as it ran.

> ### BAND 1R, DECLARED 2026-08-30, BEFORE `analysis/tube_shielding.py` IS TOUCHED AGAIN.
>
> Verify with `git log --oneline <this commit>..HEAD -- analysis/tube_shielding.py`, which must be
> empty at this commit.

| # | Band | FAIL if |
|---|---|---|
| **1R** | **Model verification, by limits and by order rather than by agreement.** (a) At zero conductivity the slab's conductive transmission is 1.000 and its total transmission equals `exp(-kd)`, both to 1e-12. (b) With the sheet conductance `σd` held at the design value, the slab agrees with the sheet to **0.01 %** by `d` = 1e-3 mm. (c) The convergence order observed over that sequence is **first order to within 0.05** | Either route is wrong. A wrong implementation breaks the limit or breaks the order, and cannot fake both |

Band 1R is harder than the band it replaces, and unlike that band it can be met. Bands 2 through 6
are untouched.

### Two things this correction does not cover

**A defect in the loss model, found in reviewing `af526a0` and not in any band.** The wall loss and
every thermal figure in that run are computed from peak-amplitude phasors without the factor of one
half a time average carries, so 231.33 kW and 927.2 K are both exactly twice what the model says.
The tell is that the implied shear, 0.52 MPa, is three times the Maxwell bound `B²/2μ₀` for the
field driving it. The corrected figures follow the same closed-form induction-drag curve
`F/A = (B²/2μ₀)·2Rm/(1+Rm²)` computed independently, which is the check that was missing. That is a
coding defect, not a band, and correcting it does not move a declared target.

**No band was declared for the wall temperature, and none is being declared now.** The 473 K
ceiling is in the input table and nothing gates against it, which is a gap in the declaration of
2026-08-30 that I am not going to close after the fact. The thermal result is reported without a
gate, and the reader should treat it as a report and not as a passed test. A successor run may
declare a thermal band; A66 may not.

---

## Result

**RUN 2026-08-30. Bands 1R, 4, 5 and 6 pass, band 2 reports, band 3 fails. And the run turned up
something an order of magnitude larger than the band it was written around.**

| # | Band | Result | |
|---|---|---|---|
| 1R | zero-σ limits, first-order convergence at fixed `σd` | zero-σ 1.000000; 0.001581 % at a 1e-3 mm wall; worst pairwise order deviation **0.0436** against 0.05 | **PASS** |
| 2 | skin depth against the wall | 714.2 Hz, δ **3.183 mm**, wall = **0.314 δ** | **REPORT** |
| **3** | the section as drawn still delivers 1.1543 m/s | **0.9356 m/s, 81.06 %** | **FAIL** |
| 4 | compensated section within 15 % of stroke | 177.66 mm, **2.2208 %** | **PASS** |
| 5 | per-satellite mass ≤ 2.0 kg | **1.4227 kg** | **PASS** |
| 6 | second implementation within 10 % | sheet 0.798519, slab 0.810576, **1.4874 %** | **PASS** |

### The skin depth is not the governing comparison, and P92 said it was

P92 named the wall against the skin depth as the comparison that decides this. It is 0.314 skin
depths at 714.2 Hz — a third of one — and on that reading the wall is nearly transparent. It
removes **19 %** of the field.

The parameter that governs is the sheet magnetic Reynolds number, `Rm = μ₀σdv/2`, and it is
**0.7539**. Skin depth asks how fast the field alternates. `Rm` asks how fast the field moves
*past the conductor*, and the tube never moves, so it takes the whole synchronous 34.28 m/s as
slip on every shot. A wall can be thin against its skin depth and shield hard, and this one does.

> **P92's own framing is corrected by the run it asked for.** The comparison it named is band 2,
> it is reported, and it is not the answer.

### The section loses a fifth of its authority, and buying it back is cheap

0.9356 m/s against the 1.1543 m/s A55 sized it for. Band 3 fails, which is P92 being real.

Restoring it costs a factor of 1.2337 in length: **177.66 mm**, still only 2.2208 % of the 8.0 m
stroke against A55 band 5's 15 %, and **1.4227 kg** per satellite against A55 band 7's 2.0 kg.
Bands 4 and 5 pass with room. On the evidence of the bands alone, the tube is a nuisance that
another 34 mm of stator absorbs.

### The wall takes more force than the stator makes, and no band asked

The wall's eddy currents produce a drag, and the ratio of that drag to the thrust the same field
makes on the stator carries no area, no section length and no thrust constant:

> **drag / thrust = σ d v B_net / 2K**

Everything the section's geometry and its force specification could get wrong divides out. What is
left is the wall, the speed, and the stator's sheet current. Setting the ratio to one:

> **Above an air-gap field of 0.1500 T, the tube takes more force than the stator makes.**

| Air-gap field | drag / thrust | wall loss | per shot | peak over 12 | 473 K ceiling |
|---|---:|---:|---:|---:|---|
| **0.200 T** | **1.08** | 4.11 kW | 0.94 K | 304.4 K | within |
| **0.400 T** | **2.16** | 16.44 kW | 3.75 K | 338.2 K | within |
| **0.600 T** | **3.24** | 36.98 kW | 8.45 K | 394.5 K | within |
| **0.800 T** | **4.32** | 65.75 kW | 15.02 K | 473.3 K | **over** |
| **1.000 T** | **5.40** | 102.73 kW | 23.46 K | 574.7 K | **over** |
| **1.320 T** | **7.13** | 178.99 kW | 40.88 K | 783.7 K | **over** |
| 1.385 T\* | 7.49 | 197.18 kW | 45.04 K | 833.6 K | **over** |

\* the field the current parameters imply, and it is above the remanence of the magnet material.
Carried so it is visible, not because it is an operating point.

**There is no row in that table where the machine works.** 0.2 T is a weak magnet at a wide gap
and the drag already exceeds the thrust; at anything a Halbach array actually delivers, it exceeds
it three to seven times over. The ladder was chosen as a neutral 0.2-to-remanence sweep, not
fitted to the answer, and the answer does not depend on which row is right.

The reaction is on the carriage, not on the supply. The stator's own contribution to the air-gap
field is `μ₀K/2` = **0.0566 T** against the magnets' several tenths of a tesla, so the wall is
braking against the magnet array it is supposed to be pushing. It is an eddy-current brake with a
stator bolted to the outside of it.

### The force specification does not survive its own geometry either

Backing the working flux density out of the specified force needs the area the force acts across,
and I first used `SECTION × stator.active_width_y`. **90 mm is the depth of the flat Gen5 array.**
The Gen6 trim section is an annulus around a 15.805 mm bore and `cad/build_gen6.py` has always
drawn it as one. The real air-gap surface is **76.03 cm²** against the 129.61 cm² I used, 1.7047×.

Corrected, **948.0 N at 90 kA/m across that annulus needs 1.3854 T**, against the **1.32 T**
remanence `motor_model.py` gives the magnet material. The specified force is not available from
the specified current over the specified geometry, by 5 %, before any gap or leakage.

The cause is upstream and it is not A66's to fix. `analysis/trim_stage.py` sets the section's
force as `KT * SHEET_A_PER_M / 1e3`, and A2 defines that thrust constant over
`motor_model.SLED_ACTIVE_LEN` — **0.34 m of flat array, 0.09 m deep**. A55 applied it to 0.14401 m
of annulus around a 15.805 mm bore, unrescaled for length or for area. That is
[P117](../OPEN_PROBLEMS.md#p117).

### The wall temperature, reported without a gate

**I declared no band for it.** The 473 K ceiling sits in this run sheet's own input table and
nothing in the six bands tests against it. That is a gap in the declaration of 2026-08-30, it is
recorded in the correction block above, and it is not being closed after the fact.

What the run reports: the ceiling is crossed somewhere near 0.8 T, and every stack in the table
assumes the heat stays where it was made for the whole campaign. It does not. ADR-020 puts 1200 s
between shots and the section is welded into eight metres of the same metal; the axial diffusion
length over that gap is **287.8 mm**, twice the section. Every campaign column above is an upper
bound with a named and unmodelled mitigation, in the same way A43 compared 8873 s of conduction
against the same 1200 s cadence for the reservoir. **A66 does not resolve the accumulation**, and
the per-shot column is the part of it I would defend.

### What this run does not resolve

**The brake is not confined to the 144 mm the stator occupies.** The magnets ride the carriage and
face the aluminium wall for the whole 8.0 m stroke, energised stator or not, so the drag acts over
the stroke and not over the section. The magnet array's own length is not in `cad/parameters.json`
— only the stator section's is — so that integral cannot be closed here. It is
[P118](../OPEN_PROBLEMS.md#p118) and it is the larger of the two.

The split of the drag reaction between the carriage and the stator mounting is modelled as
overwhelmingly carriage-side on the field ratio above, and not computed.

Conductivity is a handbook room-temperature value and the wall gets hot, which raises resistivity
and lowers `Rm`. E4 stands: nothing here is measured.

It does not choose the fix. A non-conducting liner, a slotted or non-conducting section local to
the stator, and the passive secondary `docs/VAULT.md` records under PII-19 are all live, and none
is this run's to pick.
