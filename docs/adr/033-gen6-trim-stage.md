# ADR-033: Gen6 gains a motor that steers, and it is adopted on a number nobody has weighed

**Status:** Accepted · **Date:** 2026-08-16 · **Phase:** I · **Extends:** [ADR-032](032-gen6-stage-integrated-gas-store.md)

## Context

[ADR-032](032-gen6-stage-integrated-gas-store.md) deleted the motor and bought a **50 % reduction
in added mass per satellite** with it. [A44](../../validation/A44_gen6_dispersion.md) then priced
what that cost: **3σ dispersion of 1.113 % against Gen5's 0.0274 m/s**, with **93.4 % of the
variance a seal friction nobody has measured** — and a fivefold better transducer moving it
**0.008 %**. **There is no instrumentation route to the product's central claim.**

**The claim is commanded per-satellite velocity.** Gen6 as adopted cannot command it; it can only
*set* it, before a 133 ms open-loop expansion, and hope the seal behaves.

## Decision

**Gen6 gains a short stator section at the muzzle end, energised only after the gas has finished,
acting on a magnet set carried by the carriage. It corrects the velocity the gas actually
produced. It never throws the payload.**

**Gas supplies the energy. The motor supplies the control.** Each does what it is good at: a gas
store charges slowly from solar and releases fast; a linear machine is a mediocre energy store and
an excellent servo.

[A48](../../validation/A48_trim_stage.md), seven of eight bands:

| | |
|---|---:|
| Energy to correct ±3σ | **37.7 J — 2.021 %** of the shot |
| Section length | **39.7 mm — 1.822 %** of the 2.18 m stroke |
| Added mass | **0.340 kg** |
| Added mass per satellite | **1.403 → 1.431 kg** |
| At **3×** the friction spread | 5.53 % of stroke, 1.032 kg |

**Band 6 is why this is adopted: the precision Gen6 traded is recoverable.** A loop correcting a
*measured* velocity does not care that the gas produced it open-loop.

## What this costs, stated rather than absorbed

**The magnets come back to the moving part, and the defects come with them.**

| | |
|---|---|
| **P34** | A payload carrying a magnetometer cannot fly in this magazine. **This defect returns because the magnets do** |
| **E35** | The payload's field exposure is a design variable again |
| **The cradle** | Must hold magnets in alignment as well as the payload — and it still does not exist |
| **A velocity sensor** | Gen6 has no equivalent. The loop is only as good as what it measures |
| **[A47](../../validation/A47_gen6_fmea.md)** | One more element, shared across all twelve shots, in an architecture whose shared elements are what cost delivered satellites |

## Falsifiers

**This decision is wrong if any of these turns out true.**

1. **The pulse store weighs more than the 0.340 kg stage it feeds.** The correction is **37.7 J at
   28 kW** — requirement **C3**, *the energy arrives during the shot*, which A35 prices at
   **26.35 kg** and ADR-032 deleted. **At a fiftieth of Gen5's energy, but pulse hardware scales
   with current, not energy, and nothing has weighed it.** *This is the falsifier most likely to
   fire, and it is being adopted before it is answered.*
2. **The measured seal friction is small.** Then the dispersion the stage exists to correct is not
   there, and the whole section is mass spent on a problem that did not exist. **P67** is the
   measurement.
3. **The velocity sensor cannot resolve what the loop must correct** in the 1.4 ms available.
4. **P34 proves binding** — if a magnetometer-carrying payload is a real customer rather than a
   hypothetical, the magnets cannot come back at any mass.

> ### This is adopted the way ADR-032 was, and for the same reason
>
> **ADR-032 was taken with its stage credit unbounded**, and [A45](../../validation/A45_stage_credit.md)
> later fired its first falsifier. **ADR-033 is taken with its pulse store unweighed**, which is
> the same shape of exposure, and it is named here rather than discovered later.
>
> **The precedent that should worry a reader is A39.** It chose gas over a spring while assuming
> **50 bar held at the piston throughout — a regulator it never named** — and
> [A40](../../validation/A40_blowdown_transient.md) killed that implementation at **14.16 m/s
> against a 30 m/s band.** *Adopting a store before pricing its hardware is exactly the mistake
> this project has already made once.*

## Alternatives, and why not

**Leave Gen6 open-loop.** Then the product claim is *set* velocity, not *commanded* velocity, and
`SUMMARY.md`, `LANDSCAPE.md` and the paper all need rewriting to say so. **That is the honest
alternative and it is a marketing retreat, not an engineering one.**

**Two full drives, each a fail-safe for the other.** Declined as **PII-20** without running:
each sized for full duty re-adds the **37.89 kg** ADR-032 deleted, the redundancy covers three of
eight shared elements, and the two drives tax each other on every shot neither fails.

**A better seal.** The correct first move, and it is a *measurement*, not a design — **P67**. If
the friction is small this ADR is unnecessary. **It is adopted anyway because the measurement does
not exist and the claim is being made now.**

## What this does not change

**Exit velocity, store, reservoir and stroke are untouched.** The trim stage adds no energy to the
shot; it moves velocity within ±3σ of where the gas already put it.

**Kill criterion 1 is not met.** 1.431 kg per satellite on added mass, **10.547 kg on dry mass**,
and **1.403–3.271 kg once the stage credit is read hostilely** ([P68](../../OPEN_PROBLEMS.md)).

**Nothing is measured.** Not the friction, not the store, not the sensor.
