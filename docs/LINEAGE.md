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

> ## The distinction this file is written around, and it is the one that gets collapsed
>
> **Two different things changed at different rates, and reading them as one produces a false
> history.**
>
> | | |
> |---|---|
> | **Mission architecture** — *what the stage is FOR* | **Settled in 2023 by [ADR-002](adr/002-host-is-a-spent-upper-stage.md) and essentially unchanged since.** A post-primary upper stage is the orbital delivery platform; VOLLEY produces each satellite's individual release condition aboard it |
> | **Mechanism integration** — *how much of the machine the stage IS* | **Changed enormously.** Free-flyer → hosted deployer → self-contained electromagnetic system aboard the platform → a system whose structure and length are the stage's |
>
> **[ADR-024](adr/024-last-mile-delivery-conops.md) did not invent the last-mile mission in 2026.**
> It says so in its own first sentence: *"the concept this project was started to pursue is not
> written down anywhere in it."* **It documented a mission the project already had and had failed
> to state.** *Mission intent can predate its documentation. Mechanical integration genuinely
> evolved. Those are different claims and this file keeps them apart.*

---

## The arc, in six decisions

| When | Decision | What moved |
|---|---|---|
| **2021** | Concept, built around a coilgun | The problem is named: a rideshare secondary inherits an orbit and a 1–2 m/s spring cannot alter it |
| **2023** | **[ADR-002](adr/002-host-is-a-spent-upper-stage.md) — the host is a spent upper stage, not a free-flyer** | **POEM reframes it.** A free-flyer must carry attitude control, power and recoil management, *"which is most of a spacecraft"*. A spent stage already has all three |
| **mid-2025** | Coilgun → linear synchronous motor | A coilgun cannot command a velocity, and commanding it is the product |
| **2026-08-10** | **[ADR-024](adr/024-last-mile-delivery-conops.md) — the last-mile ConOps, written down at last** | **Nothing about the mission moves here. What moves is the record.** The ConOps ADR-002 chose in 2023 is finally stated, seven documents and five generations after it was decided |
| **2026-08-14** | **[ADR-032](adr/032-gen6-stage-integrated-gas-store.md) — Gen6** | **The stage was already the delivery platform; here it also becomes the machine.** No mover, no stator, no bank, no brake — a rail the stage already is. *This is an integration change, not a mission change* |
| **2026-08-19** | **[ADR-034](adr/034-gen6-long-stroke-design-point.md) — the stroke becomes the stage** | **The last thing the machine was still carrying for itself was its own length.** 2.18 m of tube on an 8 m vehicle became **8.0 m**, and the acceleration and the gas each fell **54.5 %** for it. *The stage stopped being a host in 2026-08-14; here it stops being merely a mounting length* |

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

**Two columns, because the answer is different in each and reading one for the other is the
mistake this file exists to prevent.** The left column barely moves after 2023. The right column
is the whole engineering history.

| | **Mission role of the host** | **Mechanical integration with the host** |
|---|---|---|
| **Earliest concept, 2021** | **none — VOLLEY *was* the spacecraft.** A dedicated free-flyer, carrying its own attitude control, power and recoil mass | **Total, with itself.** The free-flyer is an alternate *implementation* of the same delivery mission, not a different mission |
| **[ADR-002](adr/002-host-is-a-spent-upper-stage.md), 2023** | **ACTIVE POST-PRIMARY ORBITAL DELIVERY PLATFORM** — attitude control, navigation, power, recoil mass, and where the vehicle allows it, post-primary manoeuvre capability | **Low.** VOLLEY becomes a hosted payload. *"This is what turns the concept from a mission into a payload"* |
| **[Gen1](generations/GEN1.md)–[Gen4](generations/GEN4.md)** | **unchanged — active delivery platform** | **Low / self-contained.** The *mechanism* model is host-agnostic: it carries its own track, structure, enclosure and energy store, and treats host repositioning parametrically. **That is a statement about the model, not about the mission** |
| **[Gen5](generations/GEN5.md)** | **unchanged — active delivery platform**, and this is the machine the manuscript reports | **Low / self-contained, and frozen that way.** 126.6 kg dry, of which the enclosure alone is **50.04 kg** — a skin the stage already has. **Its weakness is duplication, not its concept of operations** |
| **[Gen6](generations/GEN6.md)** | **unchanged — active delivery platform** | **HIGH.** **85.36 kg — 67.4 % of the ledger — is the stage's**, and 29.75 kg is deleted outright. The rail, the structure, the power, the thermal path and the avionics bay are things a stage already carries |
| **Gen6 at [ADR-034](adr/034-gen6-long-stroke-design-point.md)** | **unchanged — active delivery platform** | **HIGH, including length.** The stroke is **8.0 m** — A37's whole usable acceleration length. **The one resource the machine had never spent was the one the stage gives away free**, and spending it halved both the acceleration and the gas at unchanged velocity |

> **Read the left column downwards.** It says *"active delivery platform"* six times. **The mission
> did not change; the amount of it VOLLEY built for itself did.**
>
> **What may not be claimed in either column.** No launch provider has agreed to anything —
> **[E5](../OPEN_PROBLEMS.md)** — so *"where the vehicle allows it"* is doing real work. **Host
> propulsion, restart authority and post-primary reserve remain parametric in every generation**,
> including this one. [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) carries that as host
> classes rather than as one assumed vehicle.

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
