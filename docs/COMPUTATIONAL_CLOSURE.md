# Computational closure: what "the computer work is finished" would mean

**Opened 2026-08-22.** The programme goal for Gen6 is **computational closure**: the state in
which **no remaining question's honest next step is another calculation.** This file defines it,
counts against it, and is checked by
[`tools/check_computational_closure.py`](../tools/check_computational_closure.py) on every commit.

> ## Computational closure is not hardware validation, qualification, or flight readiness.
>
> **It means the remaining uncertainty can no longer be honestly reduced by an analysis that
> should have been run before building hardware.** It says nothing about whether the machine
> works. **E4** stands: nothing in this project has been built, fired or measured, and closure
> does not change the evidence class of a single figure.

---

## Remaining COMPUTATION items: 16

**It is not zero and this file will not pretend otherwise.** The sixteen are named below, each
with what would close it. **Every one of them is executable now** — no hardware, no launch
provider, no flight.

---

## The classification

Every LIVE entry in [`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) carries a machine-readable line
under its status:

```
> **Scope:** `GEN6` · **Next step:** `HARDWARE` — measure the seal friction -- B-2
```

| Class | The next honest action |
|---|---|
| **COMPUTATION** | model, simulate, optimise, FEA, CFD, Monte Carlo, CAD, a standards comparison, a public-data literature check, or **selecting a component from published data** |
| **HARDWARE** | measure, manufacture, qualify, test |
| **HOST_DATA** | non-public launch-provider or host-stage interface data |
| **FLIGHT_OPS** | flight or operational data that does not exist until something flies |
| **DECISION** | a human programme decision that no analysis settles |

**Scope is `GEN6`, `GEN5` or `PROGRAMME`, and closure is counted over `GEN6` only.** Gen5 is a
frozen baseline; **reclassifying its history to shrink the number would be the same dishonesty in
a different place**, so its sixteen live computation items are counted separately and left alone.

> **The gate reads the words, because it cannot read intent.** An entry classified `HARDWARE`
> whose next step says *model*, *simulate*, *compute*, *design the* or *select from public data*
> is caught and named. **A calculation relabelled as hardware is exactly how a closure count gets
> faked**, and it is the only failure this gate exists to prevent.

---

## Where the register stands

| Scope | COMPUTATION | HARDWARE | HOST_DATA | FLIGHT_OPS | DECISION |
|---|---:|---:|---:|---:|---:|
| **GEN6** | **16** | 4 | 5 | 1 | 0 |
| PROGRAMME | 2 | 0 | 0 | 1 | 6 |
| GEN5 | 16 | 0 | 0 | 0 | 4 |

---

## The sixteen, and what closes each

| Entry | What is left to compute |
|---|---|
| **[P103](../OPEN_PROBLEMS.md)** | **A67**, the 6-DOF guided-contact model through the 8 m bore. *Bands declared `246b7ee`; the run is the largest single item on this list* |
| **[P92](../OPEN_PROBLEMS.md)** | **A66**: the trim stator's field through a 1.0 mm aluminium tube — attenuation, induced loss, wall temperature against ADR-035's 473 K |
| **[P75](../OPEN_PROBLEMS.md)** | A Gen6 reliability architecture, the way [A47](../validation/A47_gen6_fmea.md) did Gen5 |
| **[P79](../OPEN_PROBLEMS.md)** / **[E6](../OPEN_PROBLEMS.md)** | A variable-atmosphere decay model and an independent propagator check. **The headline should become an uncertainty range, not a single multiplier** |
| **[P81](../OPEN_PROBLEMS.md)** | A backup ejector concept that clears the tube on the energy actually available |
| **[P87](../OPEN_PROBLEMS.md)** | Re-plan the campaign fill schedule against the window the last fill does not fit |
| **[P91](../OPEN_PROBLEMS.md)** | A pressure vessel design meeting [A53](../validation/A53_backup_ejector.md)'s per-cell mass |
| **[P57](../OPEN_PROBLEMS.md)** | Read the voice-coil deployer in full and record it in [`PRIOR_ART.md`](PRIOR_ART.md) under that file's five fields |
| **[E3](../OPEN_PROBLEMS.md)** | **Select components from public vendor data** instead of carrying parametric masses. *This is what deletes the remaining mass allowances* |
| **[E7](../OPEN_PROBLEMS.md)** | Select a velocity sensor from public data and use its stated noise instead of an assumed one |
| **[E11](../OPEN_PROBLEMS.md)** | **Public material screening** — ASTM E595-class data for the Gen6 bill of materials. *Measurement is hardware; screening is not* |
| **[E18](../OPEN_PROBLEMS.md)** | A conjunction covariance from a defensible public source rather than an invented one |
| **[E28](../OPEN_PROBLEMS.md)** | Campaign mission life at a real deployment altitude |
| **[E32](../OPEN_PROBLEMS.md)** | Design the ascent inhibit and its fault logic |
| **[E16](../OPEN_PROBLEMS.md)** | A reference audit against publisher records |

---

## What is genuinely blocked

**These cannot be closed by any analysis, and saying so is the point of the exercise.**

### Hardware or measurement — 4

| | |
|---|---|
| **[P67](../OPEN_PROBLEMS.md)** | The seal friction. [`B2_ORDER.md`](B2_ORDER.md) is the order, and its bands 13 and 14 exist because the rig must measure the seal rather than the assembly |
| **[P78](../OPEN_PROBLEMS.md)** | Resolves with P67 — the friction *share* of a long stroke is the same unmeasured number |
| **[P88](../OPEN_PROBLEMS.md)** | Whether the seal can conduct away its own friction heat, at 238 K, over 8 m, twelve times |
| **[E4](../OPEN_PROBLEMS.md)** | Nothing has been built. **This is the one that does not move until something is made** |

### Host or launch-provider data — 5

**[E5](../OPEN_PROBLEMS.md)** host stage propellant, authority and restart constraints ·
**[P94](../OPEN_PROBLEMS.md)** a published control authority for a real stage ·
**[P99](../OPEN_PROBLEMS.md)** a real host wheel, or a host that does not need one ·
**[P68](../OPEN_PROBLEMS.md)** what a provider will actually credit against the stage ·
**[E31](../OPEN_PROBLEMS.md)** the launch-interface position of an actual provider.

> **Every one of these is a conversation, not a calculation**, and
> [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) is where the assumptions they stand in for
> are written down as host classes rather than as a single assumed vehicle.

### Flight or operations — 1

**[E30](../OPEN_PROBLEMS.md)**: the reliability a twelve-cycle series mechanism must hit is
**computed — 0.99326 per element per cycle**. What it *is* needs published deployment counts and
failure records, which is operational history and not a model.

---

## How this file is checked

`tools/check_computational_closure.py` fails if:

1. any LIVE entry has no `Scope`/`Next step` line;
2. a scope or class is not one of the declared values;
3. a `HARDWARE`, `HOST_DATA` or `FLIGHT_OPS` entry's next step contains a computational verb;
4. **the count above disagrees with the register** — the number in *"Remaining COMPUTATION
   items"* is parsed and compared;
5. `--closed` is passed while any GEN6 entry is still `COMPUTATION`.

**Point 4 is the one that matters.** A closure document that drifts from the register is worse
than no closure document, because it is the same claim made twice with only one of them true.
