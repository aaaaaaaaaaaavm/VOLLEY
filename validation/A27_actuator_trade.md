# A27: why a linear motor, and not a screw, a rack, or a spring

**Answers review item 18**, which asked why the hardest possible actuator was chosen. **The
repository has no recorded answer.** `grep -ri "lead screw"` and `grep -ri "rack and pinion"`
both return zero, and `docs/DECISION_LOG.md` records the choice of *eddy brake* and *ironless
stator* but never the choice of **linear motor over every other way of pushing a satellite**.

> ## SCREENING CRITERIA DECLARED 2026-08-10, BEFORE `analysis/actuator_trade.py` EXISTS.
>
> The script is absent at this commit. These are **requirement-derived thresholds**, taken from
> the frozen baseline and from published component limits — not thresholds chosen to produce a
> preferred answer.

## The duty every candidate must meet

From `docs/BASELINE.md` and `cad/parameters.json`, unchanged:

| | |
|---|---|
| Moving mass | **13.445 kg** (9.445 kg sled + 4 kg payload) |
| Stroke | **1.30 m** acceleration zone |
| Exit velocity | **16.388 m/s** |
| Peak acceleration | **≤ 25 g**, the CubeSat Design Specification qualification cap |
| Mechanical energy to the payload | **537 J** |
| Cycles | **12** per campaign, in vacuum, after launch vibration |
| **Velocity control** | **commanded per shot** — the product |

## Screening criteria

A candidate **passes** only if it meets all five. Any candidate failing one is screened out and
the reason recorded; **a candidate may fail and still be the right answer for a different
product**, which is stated where it applies.

### C1 — kinematically capable

The mechanism can reach **16.388 m/s** at the actuator's own limiting quantity, with the limit
named and sourced: rotational speed for a screw, pitch-line velocity for a rack, stored energy
for a spring. **Fails if the required value exceeds a published class limit.**

### C2 — within the payload g-cap

Peak acceleration **≤ 25 g**. A mechanism whose force profile peaks early — a spring — must be
checked at its peak, not its mean.

### C3 — velocity is commandable per shot

**The mechanism can deliver a different exit velocity on consecutive shots without hardware
change.** Continuous control passes; a fixed number of discrete levels is recorded as **partial**
with the count stated; a single fixed velocity fails.

**This is the criterion the product rests on**, and it is stated third rather than first so the
physical criteria are not read as having been chosen to protect it.

### C4 — no contact at speed in vacuum

Sliding or rolling contact carrying the drive load at full velocity is a **fail**, because
`OPEN_PROBLEMS.md` **E21** records that this repository contains nothing on lubrication, cold
welding or galling, and a contacting drive at 16 m/s makes that gap load-bearing rather than
incidental.

### C5 — energy is releasable safely and repeatably

Stored energy must be containable between shots and re-armable in vacuum without servicing.
**A mechanism storing the full shot energy mechanically at rest is recorded with its stored
energy stated**, since that is a hazard the incumbent does not have between shots.

## Candidates

1. **Ironless double-sided Halbach linear synchronous motor** — the incumbent.
2. **Ball screw**, rotary motor driving a nut or screw along the stroke.
3. **Rack and pinion**, rotary motor driving a pinion against a fixed rack.
4. **Staged mechanical spring**, one or more compression springs released in sequence.

Each is sized against the same duty, with the same moving mass, using the repository's own
operating point rather than a re-derived one.

## What this cannot settle

- **No candidate is designed here.** This is a screen, not a design; passing C1–C5 means a
  candidate is not obviously disqualified, not that it works.
- **No cost is compared.** Every cost claim in this project was withdrawn for lack of a vendor
  quotation (**E3**) and this adds none.
- **Reliability is not scored here.** `docs/FMEA.md` and **E30** hold that comparison, and a
  simpler mechanism scoring well on parts count is exactly the argument E30 says the project must
  answer rather than avoid.
