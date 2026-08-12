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

## Result, 2026-08-10: the screw is dead, the rack is marginal, and **the spring works**

`analysis/actuator_trade.py`, criteria committed at `9857b3c` before it existed.

| Candidate | C1 kinematic | C2 g-cap | C3 commandable | C4 no contact | C5 no stored energy | Peak g |
|---|---|---|---|---|---|---:|
| **Linear synchronous motor** | ok | ok | **PASS** | ok | ok | 10.5 |
| Ball screw | **FAIL** | ok | PASS | **FAIL** | ok | 10.5 |
| Rack and pinion | **FAIL** | ok | PASS | **FAIL** | ok | 10.5 |
| Staged spring, 1 stage | ok | ok | **PARTIAL** | ok | **FAIL** | 21.1 |
| Staged spring, 4 stages | ok | ok | **PARTIAL** | ok | **FAIL** | 21.1 |

### The ball screw is disqualified by kinematics, twice over

Reaching 16.388 m/s on a 20 mm lead needs **49,164 rpm**.

- **DN = 1.229 × 10⁶ mm·rpm** against a conventional ball-screw ceiling of 1.5 × 10⁵ — **8.2×
  over**.
- **Whirling critical speed for a 25 mm screw over 1500 mm is 1,333 rpm** — **37× under what is
  required.**

**This is not a close call and no amount of engineering closes it.** A screw long enough for the
stroke cannot spin fast enough for the velocity, and the two limits worsen in opposite directions:
a fatter screw raises critical speed and worsens DN.

### The rack is marginal on speed and fails on vacuum contact

Pitch-line velocity **is** the linear velocity: **16.4 m/s against roughly 10 m/s** of high-speed
rack practice, **1.64× over**. Torque is a comfortable 69.4 N·m at 3,130 rpm.

**C4 is what actually screens it out.** A rack and pinion carries the full drive load through
**tooth contact at 16.4 m/s in vacuum**, and **E21** records that this repository contains nothing
on lubrication, cold welding or galling. That gap is incidental for rolling guide wheels; for a
contacting drive it becomes the load path.

### The spring works, and that is the finding

| | |
|---|---|
| Energy to the payload | **537 J** |
| Peak force at release | **826 N** |
| **Peak acceleration** | **21.1 g — inside the 25 g cap** |
| Spring steel required | **≈ 1.8 kg** |

**A mechanical spring can deliver 16.388 m/s to a 3U CubeSat within qualification limits, using
about 1.8 kg of steel.** It needs no sled, no stator, no supercapacitor bank, no converter and no
sequencer — and it therefore has almost none of the nine manifest-forfeiting elements
`docs/FMEA.md` counts.

**It fails on exactly one criterion: C3.** A spring delivers the velocity it was built for. Staged,
it delivers *N* discrete velocities for *N* stages. It cannot be commanded to an arbitrary value
per shot.

**And C5:** it stores the full **537 J at rest**, between shots and through launch — a hazard the
incumbent does not have, since VOLLEY's energy sits in a bank that can be left uncharged (which
**E32** now requires anyway).

**Note the 21.1 g.** A linear spring's force peaks at release and falls to zero, so its peak is
**twice its mean** — 21.1 g against the motor's flat 10.5 g. That is inside the cap but with far
less margin, and it is why staging exists.

---

## What this settles, and what it costs the argument

**The linear motor is not chosen for performance. It is chosen for commandability, and that is
the whole of the case.**

- Against a **screw**, the choice is forced: the screw cannot reach the velocity at all.
- Against a **rack**, the choice is well-founded: a contacting drive at 16 m/s in vacuum makes an
  already-open tribology gap load-bearing.
- Against a **spring**, the choice rests on **one criterion only** — that velocity is commanded
  per shot rather than built in.

**This narrows the product argument rather than supporting it**, and it should be read alongside
**E30**: a spring architecture would score dramatically better on reliability, since it has
essentially no shared serial elements. **The honest position is that VOLLEY buys continuous
per-shot velocity control and pays for it in mass, complexity and shared-failure exposure.**

**A four-stage spring giving four discrete velocities at ~2 kg is a real competitor** for any
mission that does not need continuous control, and no document in this repository has previously
acknowledged it.

---

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
