# What this project was always walking toward

**A reader meeting this repository today finds the last-mile delivery concept as a 2026 idea.
It is a 2023 one, and the decision that set the direction is the second one the project ever
took.**

> **[ADR-002](adr/002-host-is-a-spent-upper-stage.md), 2023.** *"The original concept was a
> dedicated free-flying deployer. Learning of ISRO's POEM, a spent PSLV fourth stage operated as a
> stabilised platform, reframed the problem."*
>
> **Consequence, recorded at the time:** *"This is what turns the concept from a mission into a
> payload."*

**Everything since has moved in one direction: from a deployer that rides a stage, to a deployer
that *is* one.** This file is that through-line, and every step in it is a dated record elsewhere
in the repository — nothing here is asserted and nothing is retro-dated.

---

## The arc, in five decisions

| When | Decision | What moved |
|---|---|---|
| **2021** | Concept, built around a coilgun | The problem is named: a rideshare secondary inherits an orbit and a 1–2 m/s spring cannot alter it |
| **2023** | **[ADR-002](adr/002-host-is-a-spent-upper-stage.md) — the host is a spent upper stage, not a free-flyer** | **POEM reframes it.** A free-flyer must carry attitude control, power and recoil management, *"which is most of a spacecraft"*. A spent stage already has all three |
| **mid-2025** | Coilgun → linear synchronous motor | A coilgun cannot command a velocity, and commanding it is the product |
| **2026-08-10** | **[ADR-024](adr/024-last-mile-delivery-conops.md) — the last-mile ConOps, written down at last** | The stage stops being *a place to stand* and becomes *part of the product* |
| **2026-08-14** | **[ADR-032](adr/032-gen6-stage-integrated-gas-store.md) — Gen6** | **The stage stops being the host and becomes the machine.** No mover, no stator, no bank, no brake — a rail the stage already is |

## The step that names the gap, in the project's own words

**ADR-024 opens by admitting the thing this file exists to fix:**

> *"The concept this project was started to pursue is not written down anywhere in it. A search of
> every document and of `paper.tex` returns no mention of last-mile delivery, of the host
> repositioning between deployments, or of multi-orbit delivery from a single vehicle."*
>
> *"What the repository describes instead is a deployer bolted to a **passive** host … ADR-002 chose
> a spent upper stage as that host, and ADR-010 specified the interface host-agnostically, but both
> treat the stage as a place to stand rather than as part of the product. **That is a smaller idea
> than the one the machine was designed for.**"*

**ADR-024 fixed that going forward. It did not go backwards**, which is why six CAD generations sat
in the archive described purely as geometry, with no statement of what each assumed about the
vehicle underneath it. That is what `docs/generations/` now carries.

## What each generation assumed about the host

**The through-line at per-generation resolution. This is the row that changes.**

| | What it assumed the host was | Consequence |
|---|---|---|
| **[Gen1](generations/GEN1.md)–[Gen3](generations/GEN3.md)** | **a mounting surface with a power feed** | The machine carries its own track, structure, enclosure and energy store. Everything is aboard |
| **[Gen4](generations/GEN4.md)** | the same | Nine Fusion documents of a self-contained machine |
| **[Gen5](generations/GEN5.md)** | the same, and **frozen that way** | 126.6 kg dry, of which the enclosure alone is 50.04 kg — a skin the stage already has |
| **[Gen6](generations/GEN6.md)** | **the host is the machine** | **85.36 kg — 67.4 % of the ledger — is the stage's, and 29.75 kg is deleted outright.** The rail, the structure, the power, the thermal path and the avionics bay are all things a stage already carries |

**Read the Gen5 row and the Gen6 row together.** Gen5 built an enclosure because the design assumed
it needed one; A46 later measured that enclosure at **50.04 kg against an 8.00 kg placeholder**.
**Gen6 does not build it, because a stage is already a pressure-grade cylinder with a thermal loop
and an avionics bay.** *The largest single mass in the machine was a duplicate of something the
host already had* — and that is the clearest statement of what the 2023 decision was actually
worth.

## Two operating modes, which is what the concept was for

**[`CONCEPT.md`](CONCEPT.md) states them; they follow directly from being a stage rather than a
passenger on one.**

- **Deploy-on-arrival.** All twelve out shortly after orbit insertion, then disposal. Least
  dependent on the stage staying alive.
- **Loiter-and-distribute.** The stage stays up, repositions between altitude shells on residual
  propellant, and fires at each station — delivering satellites into *different* orbits from one
  launch.

**The honest boundary on the second, and it is measured rather than assumed.** Altitude
repositioning is cheap; **plane change is not, at 133 m/s per degree** (A15 band 8). And **E28**
found that campaign duration and the plane spread that makes the concept attractive are **the same
effect**: the drag that separates the orbital planes is the drag that ends the mission —
**29–36 days at 350 km**, with only the 450 km case surviving 90.

---

## What this file is not

**It is not a claim that the design was planned this way from the start.** The 2021 concept was a
coilgun on a free-flyer, and each step here was taken for a reason recorded at the time, not
toward a destination anyone had drawn. **What is true is narrower and more interesting: every
architecture decision independently moved the design closer to being the stage rather than riding
one, and the 2023 decision is where that direction was set.**

**And it changes no number.** Every figure above appears elsewhere in this repository, and this
file computes nothing.
