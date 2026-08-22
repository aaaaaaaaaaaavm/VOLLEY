# A57: attitude rate and packaging on the stage, the two rows Gen6 never recomputed

**Closes, if the bands hold:** the two remaining `NEEDS SOURCE` rows in
[`docs/KILL_CRITERIA.md`](../docs/KILL_CRITERIA.md) — **row 2, envelope** and **row 5, attitude
rate at firing**. Both were quantified for Gen5 and neither has been recomputed for the
architecture now carried as the design target. **Recoil was the third and
[A52](A52_gen6_recoil.md) closed it on 2026-08-19.**

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/stage_attitude.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> **The script is absent at this commit and that absence is checkable:**
>
> ```
> git show --stat <this commit> -- analysis/stage_attitude.py
> ```
>
> must return nothing.

---

## Why this run exists

**Gen6 deleted the mover and kept the problem.** [A13](A13_attitude_budget.md) computed Gen5's
host attitude response to an internal mass translation: a 9.445 kg sled over 1.50 m, plus a
0.104 m cassette index, on a 200–500 kg host. **Gen6 has no sled.** What translates internally is
**the payload itself — 4 kg over 8.0 m** — on a vehicle an order of magnitude heavier.

**The displacement went up 5.3× and the moving mass went down 2.4×.** Nobody has multiplied those
together, and `KILL_CRITERIA.md` row 5 has said `NEEDS SOURCE: not re-run at Gen6` since ADR-032.

**The envelope row is worse than "does not apply".** It currently reads *"Gen6 is a rail on an 8 m
stage, not a payload in a rideshare port"*, which is true and is not the whole row: **at ADR-034
the rail is 8.2 m against A37's 8.0 m usable acceleration length.** A row that dissolves one
constraint and quietly acquires a 200 mm overrun is not a closed row.

### What this run must not do, and it is the reason band 5 is written the way it is

**[P94](../OPEN_PROBLEMS.md) is open because A13 band 5 passed on a host reaction-control authority
of 0.1 N·m that [E5](../OPEN_PROBLEMS.md) records does not exist.** A number was declared as an
assumption, a band was written against it, and the band passed — which reports a *capability* the
project has no source for.

**This run does not get to make that mistake twice.** Band 5 below asks for the **momentum the host
must absorb**, which is a property of this machine, and **explicitly refuses to compare it against a
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
for a number *and* a refusal, because the failure it exists to prevent — P94 — was not a wrong
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
   moves — which is **P78**'s territory and would be the third time stroke has moved a Gen6 number.
8. **Band 8 fails.** Bands 6 and 7 stop being a packaging question and become a payload question.

**No band may be widened after the run.**

---

## Provenance

Payload mass and exit velocities from `cad/parameters.json` and `motor_model` by import, never as
literals. Host mass range from **E5**, which is why it is a range. Wheel capacity from
[A52](A52_gen6_recoil.md), reused rather than re-chosen so the two attitude runs are comparable.

**Nothing in this run is measured.** It is a rigid-body model of an internal mass translation on a
vehicle whose mass and control authority are both undisclosed, and the second of those is why
band 5 refuses to compute a margin.
