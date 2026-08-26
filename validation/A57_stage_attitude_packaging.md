# A57: attitude rate and packaging on the stage, the two rows Gen6 never recomputed

> # Correction, 2026-08-22: the run used a lever arm 15.6x its own interface requirement
>
> **Nothing below is edited. No band is re-declared and the verdict is not changed** — the same
> rule that left A1's sheet untouched and put its correction at the top.
>
> The first run imported `attitude_budget.ASSUMED_ARM = 0.166 m`. That is A13's arm from a
> Gen5 host centre of mass to the *deployer's*, and it does not describe a Gen6 geometry. For a
> payload traversing the drive tube, the arm that matters is the perpendicular distance from the
> host centre of mass to the **line of travel** — and [A52](A52_gen6_recoil.md) band 4 already
> published a requirement on exactly that: the thrust line must pass within 10.65 mm of the host
> centre of mass.
>
> 166 mm is 15.6x that requirement. A design meeting its own published interface has the
> smaller arm. The script now reads A52's figure live and sweeps both ends.
>
> | | First run, A13's inherited arm | Corrected, A52's requirement |
> |---|---:|---:|
> | Lever arm | 166.0 mm | 10.65 mm |
> | Offset per shot, 300 kg host | 0.1747° | 0.0112° |
> | Campaign offset, uncorrected | 2.0969° | 0.1346° |
> | Peak body rate | 0.7488 °/s | 0.0481 °/s |
> | Momentum per shot | 22.7619 N·m·s | 1.4609 N·m·s |
> | Momentum over the campaign | 273.14 N·m·s | 17.53 N·m·s |
> | **Band 4, Gen6 ÷ Gen5** | **2.33×** | **0.149×** |
>
> **Every band's verdict is unchanged.** Bands 1, 2, 3, 7 and 8 pass with more margin; band 6 still
> fails at 200 mm, which is geometry and does not depend on the arm; bands 4 and 5 report.
>
> ### Band 4's direction reverses, and that is the finding
>
> The first run said Gen6's per-shot attitude offset is 2.33x Gen5's. At each architecture's own
> arm it is 0.149x, about a seventh. *The conclusion "deleting the mover increased the attitude
> cost" is withdrawn.*
>
> What the reversal actually shows is that the lever arm dominates and the architecture barely
> matters. Gen5's 166 mm is an unsourced assumption; Gen6's 10.65 mm is a requirement this project
> derived. **Band 4 is therefore comparing an assumption against a requirement, not one machine
> against another, and it should be read as a statement about alignment rather than about
> architecture.
>
> ### What survives, and it is the part that mattered
>
> [P99](../OPEN_PROBLEMS.md) survives the correction. At A52's own requirement the campaign is
> 17.53 N·m·s against the 15 N·m·s wheel A52 declared, it still saturates, by 1.17x rather than
> by 18x. The margin is now thin instead of hopeless, which makes it a design question rather than
> a dismissal.
>
> [P100](../OPEN_PROBLEMS.md) records the arm defect itself.

**Closes, if the bands hold:** the two remaining `NEEDS SOURCE` rows in
[`docs/KILL_CRITERIA.md`](../docs/KILL_CRITERIA.md), row 2, envelope and row 5, attitude
rate at firing. Both were quantified for Gen5 and neither has been recomputed for the
architecture now carried as the design target. Recoil was the third and
[A52](A52_gen6_recoil.md) closed it on 2026-08-19.

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/stage_attitude.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> The script is absent at this commit and that absence is checkable:
>
> ```
> git show --stat <this commit> -- analysis/stage_attitude.py
> ```
>
> must return nothing.

---

## Result, 2026-08-22: seven of eight, and band 6 fails exactly as declared

`analysis/stage_attitude.py`, bands committed at `974d0d6` before it existed. Results in
`analysis/results/stage_attitude.json`.

| # | Question | Result | |
|---|---|---|---|
| 1 | host rate returns to zero | **0.0 °/s** | **PASS** |
| 2 | offset per shot, lightest host | **0.1747°** at 300 kg | **PASS**, band was ≤ 2.0° |
| 3 | campaign offset, twelve shots | **2.0969°** at 300 kg | **PASS**, band was ≤ 15° |
| 4 | Gen6 against Gen5, same host | **2.33×** | **REPORT**, as declared |
| 5 | momentum the host must absorb | **22.7619 N·m·s** per shot, **273.14** over the campaign | **REPORT**, and no authority comparison is emitted |
| 6 | rail as drawn fits A37's usable length | **200.0 mm over** | **FAIL**, as declared |
| 7 | velocity cost of fitting the stroke | **1.2579 %** | **PASS**, band was ≤ 2 % |
| 8 | acceleration at the fitted stroke | **11.6543 g** | **PASS**, band was ≤ 25 g |

### Both `NEEDS SOURCE` rows close, and they close differently

Row 5, attitude rate, is answered. A shot moves the stage by 0.1747° at the lightest host
in E5's range and 0.0582° at the heaviest; twelve shots reach 2.10° uncorrected. Peak body
rate during the stroke is 0.7488 °/s and it returns to zero when the payload leaves. *The
architecture change did not make this worse in kind, and the numbers are small.*

Row 2, envelope, closes as a measured miss. It has read *"does not apply as stated"* since
ADR-032, and it does apply: the rail is 200 mm longer than the stage class can accelerate over.
What band 7 adds is the price, which nothing had computed — **if the end hardware cannot live
outside the usable length, the stroke gives up 200 mm and 1.2579 % of exit velocity. That is a
real cost and a small one, and it is now a number rather than a caveat.

### Band 4: Gen6's offset is 2.33× Gen5's, which is the opposite of the intuition

Gen6 moves 2.4x less mass 5.3x further on a longer, more slender body. Those pull in opposite
directions and the displacement wins. Deleting the mover did not delete the attitude cost; it
increased it per shot. The absolute numbers stay small, so this changes no decision, but the
sign is worth recording, because "Gen6 moves less mass" has been used loosely in this repository
and it does not imply a smaller disturbance.

### Band 5 reported a number and refused a margin, which is what it was for

**22.76 N·m·s per shot.** The band forbids comparing that against any assumed control authority,
and the script does not: `authority_comparison` returns `NOT COMPUTED`, and the script parses its
own source and asserts that it makes no attribute access to a control-authority constant. A
string search would have tripped on the docstring that forbids it; the AST check cannot.

> **The finding that comparison would have produced is recorded outside the bands, not suppressed.**
> `findings.wheel_observation` states that the per-shot momentum exceeds the 15 N·m·s wheel A52
> declared, so on that assumed wheel the campaign cannot be flown without desaturating between
> shots — and that **no ConOps in this repository describes one.** It is flagged `outside_bands`
> and labelled as a finding about *A52's assumed wheel*, not about any real stage.
>
> Suppressing it would have been the opposite failure to [P94](../OPEN_PROBLEMS.md)'s, and
> widening band 5 to admit it would have been P94's failure exactly. It goes in the findings block
> and opens [P99](../OPEN_PROBLEMS.md).

### The script had a defect and the bands caught it

**Bands 7 and 8 passed on the first run at a 0.0 % velocity loss and an unchanged acceleration.**
The function had cut the stroke to `usable`, which is what the stroke already was, the overrun is
**end hardware**, not stroke, and ADR-034 says so in the sentence the band was written from. *A
band that passes by identity has not been tested.* Corrected before the run was recorded; the
bands are unchanged and the corrected figures are 1.2579 % and 11.6543 g.

**This is the fourth time a declared band has caught a bug in the analysis rather than in the
design.

---

## Why this run exists

Gen6 deleted the mover and kept the problem. [A13](A13_indexing_disturbance.md) computed Gen5's
host attitude response to an internal mass translation: a 9.445 kg sled over 1.50 m, plus a
0.104 m cassette index, on a 200-500 kg host. Gen6 has no sled. What translates internally is
the payload itself, 4 kg over 8.0 m, on a vehicle an order of magnitude heavier.

The displacement went up 5.3x and the moving mass went down 2.4x. Nobody has multiplied those
together, and `KILL_CRITERIA.md` row 5 has said `NEEDS SOURCE: not re-run at Gen6` since ADR-032.

The envelope row is worse than "does not apply". It currently reads *"Gen6 is a rail on an 8 m
stage, not a payload in a rideshare port"*, which is true and is not the whole row: at ADR-034
the rail is 8.2 m against A37's 8.0 m usable acceleration length. A row that dissolves one
constraint and quietly acquires a 200 mm overrun is not a closed row.

### What this run must not do, and it is the reason band 5 is written the way it is

**[P94](../OPEN_PROBLEMS.md) is open because A13 band 5 passed on a host reaction-control authority
of 0.1 N·m that [E5](../OPEN_PROBLEMS.md) records does not exist. A number was declared as an
assumption, a band was written against it, and the band passed — which reports a *capability* the
project has no source for.

**This run does not get to make that mistake twice.** Band 5 below asks for the **momentum the host
must absorb, which is a property of this machine, and explicitly refuses to compare it against a
control authority.** The authority question stays E5's, unanswered, and the band is written so that
it *cannot* be passed by inventing one.

---

## Inputs, and where each comes from

| | | Source |
|---|---|---|
| Payload mass | 4.0 kg | `motor_model`, the 3U reference |
| Stroke | **8.0 m** | `cad/parameters.json` `gen6_drive.stroke_mm`, ADR-034 |
| Rail length as drawn | **8.2 m** | ADR-034, against A37's 8.0 m usable |
| Exit velocity | **34.28 m/s** zero-friction, **29.01** at the allowance | `gen6_drive`, both carried |
| Host class | **300–900 kg**, parametric | **E5.** No candidate stage publishes a mass |
| Wheel capacity for the offset comparison | 15 N·m·s | [A52](A52_gen6_recoil.md), the same wheel, so the two runs are comparable |
| Manifest | 12 | ADR-032 |

**No host control authority is an input to this run.** That is deliberate and it is band 5.

---

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| **1** | **Angular momentum conservation.** Host rate returns to zero after the payload stops, in the ideal rigid-body model | **\|residual rate\| ≤ 1e-9 °/s** | The script repeats A13's original error, which was reporting peak internal momentum as a residual host rate. **Stop; nothing else in the run is trustworthy** |
| **2** | **Attitude offset per shot**, 8.0 m translation of 4.0 kg, across the 300–900 kg host range | **≤ 2.0°** at the *lightest* host | The pointing budget is not a footnote. Above 2° a single shot moves the stage further than most attitude systems hold, and the ConOps needs a settle-and-re-point step it does not have |
| **3** | **Campaign offset**, twelve shots, worst case with no correction between them | **≤ 15°** at the lightest host | The campaign cannot be flown open-loop and ADR-032's "the stage repositions on its own reaction control" acquires a cost nobody has priced |
| **4** | **Gen6 against Gen5 on offset per shot**, same host mass | **report the ratio; no pass/fail** | *Written as a report deliberately.* The two architectures differ in moving mass and stroke in opposite directions and the sign of the result is not obvious. A band here would be a guess dressed as a criterion |
| **5** | **Momentum the host must absorb per shot, and over the campaign** | **report in N·m·s, and state explicitly that no host control authority exists to compare it against (E5)** | **This band fails if the script emits a margin, a percentage, or any comparison against an assumed authority.** It is written to make P94's failure mode impossible rather than unlikely |
| **6** | **Rail length as drawn against A37's usable acceleration length** | **overrun ≤ 0 mm**, i.e. it fits | **It is already known to fail** — 8.2 m against 8.0 m. Declared as a band anyway so the overrun is recorded as a measured miss rather than a caveat, and so its size is on the record |
| **7** | **What the overrun costs in exit velocity** if the stroke is cut to fit 8.0 m | **≤ 2 % of the zero-friction exit velocity** | Above 2 % the packaging problem is a performance problem and ADR-034's design point does not survive its own stage |
| **8** | **Payload acceleration at the fitted stroke** stays under the 25 g design ceiling | **≤ 25 g** | The ceiling is this project's own requirement (**P98**), and shortening a stroke at fixed energy raises acceleration. If cutting 200 mm crosses it, the two rows are coupled and neither closes alone |

### Band 5 and band 6 are the two written to constrain the author rather than the machine

**Band 5 forbids an answer.** Every other band in this repository asks for a number. This one asks
for a number *and* a refusal, because the failure it exists to prevent, P94, was not a wrong
calculation but a right calculation compared against an invented reference.

**Band 6 is declared knowing it fails.** 8.2 against 8.0 is arithmetic, not analysis. It is a band
so that the miss is dated, sized and carried in the results file rather than living in prose as
"the rail is slightly long".

---

## What happens at each outcome, fixed now

1. **Band 1 fails.** Stop. The model is wrong in the way A13 was wrong and P19 warned about.
2. **Band 2 fails.** `KILL_CRITERIA.md` row 5 closes as **crossed**, not as answered, and the
   ConOps in `docs/CONCEPT.md` §3.3 needs a pointing step between shots.
3. **Band 3 fails.** ADR-032's stage-repositioning claim carries an attitude cost as well as a
   propellant one, and A50's campaign has to be re-read with it.
4. **Band 4** cannot fail. It reports.
5. **Band 5 fails** only if the script compares against an authority. If it does, delete the
   comparison and re-run; do not report the number it produced.
6. **Band 6 fails as expected.** Row 2 is rewritten from *"does not apply as stated"* to the
   measured overrun, and band 7 decides whether that overrun is cosmetic or structural.
7. **Band 7 fails.** ADR-034's 8.0 m stroke is not available on A37's stage and the design point
   moves, which is P78's territory and would be the third time stroke has moved a Gen6 number.
8. **Band 8 fails.** Bands 6 and 7 stop being a packaging question and become a payload question.

**No band may be widened after the run.**

---

## Provenance

Payload mass and exit velocities from `cad/parameters.json` and `motor_model` by import, never as
literals. Host mass range from E5, which is why it is a range. Wheel capacity from
[A52](A52_gen6_recoil.md), reused rather than re-chosen so the two attitude runs are comparable.

Nothing in this run is measured. It is a rigid-body model of an internal mass translation on a
vehicle whose mass and control authority are both undisclosed, and the second of those is why
band 5 refuses to compute a margin.
