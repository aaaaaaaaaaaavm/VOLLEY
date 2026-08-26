# A58, the chamber, the tube and the seal across a campaign

**Bands declared 2026-08-19, before `analysis/chamber_thermal.py` existed.**
Verify with `git show --stat <this commit> -- analysis/chamber_thermal.py`, which must return nothing.

---

## Why this run exists

Nothing in this repository models the chamber thermally.
[A43](A43_reservoir_thermal.md) settled the *reservoir* between shots and says so; the chamber, the
expansion cooling and twelve cycles of both are unmodelled.
[A39](A39_store_trade.md) states it designs *"no cylinder, valve, seal or latch"*, and
[A40](A40_blowdown_transient.md) that it does not model *"temperature drop in the chamber"*.

[ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) made both halves of it worse and
neither was checked.

## Two opposing effects, and both land on the same component

The gas gets much colder. A longer stroke expands the same charge through a larger volume
ratio, so the temperature drop nearly triples: −22.4 K at 2.18 m becomes −62.1 K at 8.0 m,
taking the gas to 238 K, −35.2 °C, every shot.

And the seal gets much hotter. Friction work is force x stroke, so it scales directly:
181.8 J becomes 667.2 J per shot, at 2419 W instantaneous where the seal is moving fastest.

> Both land on the seal, which owns 98.7 % of the dispersion ([A55](A55_trim_authority.md)),
> is the entire justification for ADR-033, and has never been measured, specified or given a
> material. *P67 is not a room-temperature friction measurement. It is a friction measurement at
> −35 °C on a component dissipating two and a half kilowatts into itself.*

And [P85](../OPEN_PROBLEMS.md) is in the middle of it. The tube's material is stated nowhere,
so the differential expansion between piston and bore across a 62 K swing cannot be computed
without choosing one, and the choice is worth about 11 µm of clearance on a 15.805 mm bore.

## Declared before the run

Handbook values, named at each use, none of them measured and none vendor-sourced, the same
standing A39 gave its gas model.

| | Value | |
|---|---|---|
| Steel: c_p, α | **460 J/kg·K**, **12 × 10⁻⁶ /K** | chamber, and the tube if it is steel |
| Aluminium: c_p, α | **900 J/kg·K**, **23 × 10⁻⁶ /K** | the tube if it is aluminium — **P85** |
| Elastomer seal: c_p | **1500 J/kg·K** | |
| **Seal mass** | **swept 0.5 – 10 g** | *NEEDS SOURCE: no seal exists in any file* |
| Nitrogen condensation at 10.10 bar | **≈ 103 K** | |
| Chamber, tube, friction, cadence | 0.3382 kg, 1.1404 / 3.294 kg, 83.4 N, 1200 s | `fill_window`, A49, A59, `gen6_dispersion` |

The gas model, the friction force and the design point are imported, not restated, `pc.work`,
`gd.FRICTION_N`, and `cad/parameters.json` through `precharged.design_point()`.

## The prediction, recorded before the run

**I expect bands 1, 2 and 3 to pass** — the gas is nowhere near condensing, and 8007 J of campaign
friction into a kilogram of metal is a few kelvin.

**I expect band 5 to fail**, and badly. A small seal absorbing 667 J in five milliseconds has
nowhere to put it, and the adiabatic bound is hundreds of kelvin. The question this run should
answer is not whether it fails but what fraction of the heat must leave the seal for it to
survive, because that fraction is a design requirement nobody has written down.

**I expect band 6 to fail on dissimilar metals and pass on matched ones**, which would make P85 a
thermal decision as well as a mass one.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | Gas temperature after expansion stays **≥ 50 K above** nitrogen's condensation point at the end pressure | The working fluid condenses in the tube and the single-phase model is wrong |
| **2** | Tube temperature rise over a **twelve-shot campaign**, adiabatic, is **≤ 15 K** in either candidate material | Friction heating is a campaign-level thermal problem and not just a local one |
| **3** | Chamber wall swing per shot is **≤ 20 K** once its thermal mass is carried | The chamber is a thermal cycler and needs a fatigue case nobody has opened |
| **4** | The chamber returns to within **5 K** of the structure temperature across the **1200 s** cadence | Shots are not thermally independent and the twelfth differs from the first |
| **5** | **Seal temperature rise per shot is ≤ 50 K** across the whole swept mass range | **The seal cannot absorb its own friction**, and a heat path out of it is a requirement rather than a detail |
| **6** | **Differential piston/bore clearance change across the 62 K swing is ≤ 5 µm** for the material pairing the repository specifies | **P85's undeclared material is a thermal decision too**, and the seal clearance moves with it |
| **7** | Friction heating and expansion cooling **do not cancel** — the net tube temperature moves in one identified direction | The two effects are the same size and the sign of the problem is undetermined |
| **8** | **REPORT, no pass/fail.** Seal temperature against seal mass and against the fraction of friction heat conducted away, so the requirement can be read off it | — |

## What this run will not do

- No FEA, no CFD, no contact model. Lumped masses, adiabatic bounds, and one conduction path.
- It does not design a seal, name a material, or claim any of these is buildable.
- It does not model the seal's friction changing with its own temperature, which is the coupling
  that would matter most, friction heats the seal, a hotter seal has different friction, and that
  feeds straight back into the dispersion. Named here and not computed.
- It does not settle P85. It reports what each material choice costs thermally.
- E4 stands. Nothing here is measured.

---

## Result

**RUN 2026-08-19. Six of eight bands pass. The two that fail both land on components the
repository has never specified, and band 7 passed on a test that was declared wrong.**

| # | Band | Result | |
|---|---|---|---|
| 1 | gas ≥ 50 K above condensation | **237.9 K, 134.9 K of margin** | **PASS** |
| 2 | tube campaign rise ≤ 15 K | steel **5.28 K**, aluminium **7.80 K** | **PASS** |
| 3 | chamber swing ≤ 20 K | **15.11 K** | **PASS** |
| 4 | chamber recovers across the cadence | **τ = 7 s**, nothing left after 1200 | **PASS** |
| **5** | seal rise ≤ 50 K per shot | **44.5 to 889.6 K** adiabatic | **FAIL** |
| **6** | differential clearance ≤ 5 µm | **10.79 µm** dissimilar, 0 matched | **FAIL** |
| 7 | heating and cooling do not cancel | 8007 J in against ≤ 28 203 J out | **PASS, but see below** |
| 8 | seal rise against mass and heat-out | **a 2 g seal must shed 77.52 %** | **REPORT** |

### The bulk thermal case is unremarkable, and that is worth knowing

The tube warms 5-8 K over a whole campaign and the chamber recovers with a 7 s time
constant against a 1200 s cadence, so shots are thermally independent, the twelfth is the
same as the first. The gas ends 135 K above where nitrogen would condense.

None of the components anyone would have worried about is in trouble. The problem is somewhere
else entirely.

### The seal cannot absorb its own friction, and it is the component that does not exist

667.2 J arrives in the seal in about five milliseconds, at 2419 W where it is moving fastest.

| Seal mass | Adiabatic rise per shot |
|---:|---:|
| 0.5 g | **889.6 K** |
| 1 g | **444.8 K** |
| 2 g | **222.4 K** |
| 5 g | **89.0 K** |
| 10 g | **44.5 K** |

**Only the 10 g end clears the band, and only if nothing else is true.** Band 8 states the
requirement that follows, and it is the useful output of this run:

> For a 2 g seal to stay within 50 K, 77.52 % of its friction heat must leave it during the
> stroke.
>
> That is a design requirement on a component that exists in no file, has no material, and
> whose friction coefficient, the thing that generates the heat, has never been measured.

And the coupling that matters most is named and not computed. Friction heats the seal; a hotter
seal has different friction; that changes the shot. [A55](A55_trim_authority.md) found the seal
owns 98.7 % of the dispersion, so a thermal-friction loop feeds straight into the one number this
architecture is sold on. *Nothing in this repository models it.*

> P67 is a harder measurement than it has been described as. It is not a room-temperature
> friction coefficient. It is a friction coefficient at −35 °C, on a component dissipating
> 2.4 kW into itself, over 8 m, twelve times. Recorded as P88.

### P85 is a thermal decision as well as a mass one

| | Clearance change across the 62.1 K swing |
|---|---:|
| Matched materials | **0.00 µm** |
| **Dissimilar** — steel piston in aluminium bore, or the reverse | **10.79 µm** |

On a 15.805 mm bore that is a real fraction of any sensible seal clearance, and the
repository specifies neither the piston nor the tube. [P85](../OPEN_PROBLEMS.md) recorded the
material as a 2.15 kg mass question; it is also a 10.79 µm clearance question, and matching the
two materials makes it disappear entirely.

That is a free result. Nothing about the mass argument forces the piston and tube to differ,
and matching them removes a term nobody had counted.

### Band 7 was the wrong test, declared before the run and left standing

It passed, and it should not be read as settling anything.

The band asked whether friction heating and expansion cooling cancel, and compared **8007 J of
campaign friction, which definitely enters the structure, against <= 28 203 J the gas could
absorb, which is an *upper bound* reached only if the residual gas fully equilibrates with the
walls before it is vented. The two are not the same kind of quantity.

> The sign of the net thermal load is not determined by this run. If venting is fast the
> machine runs warm at 8007 J; if the residual sits, it runs cold. Which one depends on
> vent timing, which is not modelled anywhere.
>
> **The band is not widened and the verdict is not changed.** It is recorded as a badly-formed
> band, the fifth time in this project that writing one down in advance has exposed a defect in the
> analysis rather than in the design.

## Consequences

- P88 opens: the seal cannot absorb its own friction, and P67's measurement is harder than
  stated.
- P85 gains a second axis, matching the piston and tube materials removes 10.79 µm for free.
- **Nothing here moves a design point.** Bands 1–4 say the bulk thermal case is comfortable.

## What this run did not settle

- It does not design a seal, name a material, or claim any of this is buildable.
- It does not model the thermal-friction coupling, which is the term that would matter most.
- **It does not model vent timing**, which is what band 7 turned out to need.
- E4 stands. Nothing here is measured.
