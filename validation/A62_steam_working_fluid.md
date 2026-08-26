# A62, steam, with the water heated by being in space

**Bands declared 2026-08-20, before `analysis/steam_fluid.py` existed.**
Verify with `git show --stat <this commit> -- analysis/steam_fluid.py`, which must return nothing.

---

## Why this run exists

[A39](A39_store_trade.md) traded a steel spring, cold gas and keeping the motor, and screened a
lead screw, a rack and pinion and a flywheel, each carrying the run that screened it. It never
considered a heated working fluid, and that is a hole in the trade rather than anyone's
oversight.

The proposal is specific and it is not a thruster. Water stored at low pressure, raised to
steam by solar flux alone, no resistive heater, no electrolysis, no combustion, and fired as
the same closed adiabatic expansion A41 specified. The gun is unchanged; only the working fluid
and how it is charged are different.

What makes it worth computing rather than dismissing: steam's molecular weight is 18 against
nitrogen's 28, and its ratio of specific heats is 1.33 against 1.4, so the same charge
pressure is reached with less mass and the pressure falls more slowly through the stroke. Both
point the same way, and the 200 bar COPV disappears.

## What has to be true for it to work

| | |
|---|---|
| **It must not condense in the tube** | Two-phase expansion does less work than the dry figure and is far less repeatable, and [A55](A55_trim_authority.md) found dispersion is the thing this architecture can least afford |
| **The sun must reach the temperature that requires** | Passive equilibrium is **T = (α/ε · S / 2σ)^¼**, and a plain black surface at 1 AU reaches only **331 K** |
| **The machine must survive it** | The tube, the chamber and — critically — **the seal [A61](A61_seal_class.md) has just specified at 17.8 N** |
| **It must survive eclipse** | ~35 minutes of dark in every ~93 minute orbit, and water freezes at 273 K |

## Declared before the run

| | Value | |
|---|---|---|
| Solar constant at 1 AU | **1361 W/m²** | |
| Steam: M, γ | **0.018 kg/mol**, **1.33** | ideal gas — **no steam tables are in this repository** |
| Water: sensible + latent + superheat to raise one charge | **≈ 2.786 MJ/kg** | **handbook. NEEDS SOURCE** |
| **Aluminium 6061-T6 useful limit** | **473 K** | **handbook.** It loses much of its strength and creeps above roughly 200 °C |
| **Steel useful limit** | **≥ 700 K** | handbook |
| **Filled PTFE continuous limit** | **533 K** | **handbook.** This is what A61's specification would have to survive |
| Low-pressure water tank allowance | **0.20 kg** | **a declared guess, and stated as one** |
| Eclipse | **35 min dark in 93** | LEO, and A50's campaign altitudes |
| Baseline to beat | A56's store **3.1216 kg**; A59's tube **1.1404 kg** aluminium / **3.294 kg** steel | |

The expansion model, the design point and the tube masses are imported, not restated.

## The prediction, recorded before the run

**I expect bands 2, 3, 5, 6 and 9 to pass** — steam does slightly more work on roughly a third of
the mass, a selective absorber coating reaches the temperature without a concentrator, and the
absorber is small.

**I expect band 4 to fail**, and for that failure to cascade: the charge must be superheated well
past aluminium's useful limit, which forces the tube to steel and hands [P85](../OPEN_PROBLEMS.md)
its heavy answer, 2.15 kg, for a store saving of about one.

**I expect band 7 to fail too**, and this is the one that would matter most: **A61 specified a seal
at 17.8 N on the assumption it runs at −35 °C. At steam temperature filled PTFE is at or past its
limit, so the specification produced yesterday would not survive this fluid.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | The nitrogen baseline reproduces A49's **2350 J** and **51.0 g** within 1 % | This run is not standing on the design point and nothing below is comparable |
| **2** | Steam delivers **≥ 100 %** of nitrogen's shot work at the same charge pressure | The lower γ does not pay for itself and the fluid is worse on the axis that matters most |
| **3** | Steam charge mass is **≤ 60 %** of nitrogen's | The mass advantage is not there |
| **4** | The charge temperature needed to keep the expansion **dry** is **≤ 473 K** | **The tube cannot be aluminium**, P85 is forced to its heavy answer, and the store saving is spent on structure |
| **5** | That temperature is reachable passively with **α/ε ≤ 20** | A solar concentrator is required, which must track the sun on a stage whose pointing is already committed to A52's 10.7 mm thrust-line requirement |
| **6** | Absorber area, at the sunlit duty cycle, is **≤ 0.25 m²** | The collector is a deployable structure, which is the class of problem that killed PII-8 and PII-11 |
| **7** | The charge temperature is **within filled PTFE's 533 K limit** | **[A61](A61_seal_class.md)'s 17.8 N specification does not survive this fluid**, and the seal returns to being unspecified |
| **8** | **Net mass is a saving**, counting the store, the water, the tank and the tube material the temperature forces | Steam costs mass rather than saving it, and the COPV argument is spent twice over |
| **9** | The charge survives **35 minutes of eclipse** without the store falling below 273 K, at the emissivity band 5 requires | Water freezes in shadow and every line needs a heater, in the loiter mode this concept exists for |
| **10** | **REPORT, no pass/fail.** Temperature against α/ε and absorber area, so a future design point can be read off it | — |

## What this run will not do

- No steam tables. The ideal-gas treatment is stated at each use and the wet-expansion case is
  bounded rather than computed** — that is why band 4 asks what superheat avoids it entirely.
- It does not design an absorber, a coating, insulation, plumbing or a sun-pointing scheme, and
  none of that mass is counted, so every figure below flatters steam.
- It names no product, compound or supplier, only material and coating classes.
- It does not model the thermal-friction coupling at steam temperature, which A58 named and
  left uncomputed and which would be worse hot than cold.
- E4 stands. Nothing here is measured.

---

## Result

**RUN 2026-08-20. Seven of ten bands pass. The fluid is better than nitrogen on every axis it was
proposed for, the solar heating works comfortably, and the machine that has to contain it is worse
by more than the fluid saves.

| # | Band | Result | |
|---|---|---|---|
| 1 | nitrogen baseline reproduces | **2350 J, 51.0 g** | **PASS** |
| 2 | steam ≥ 100 % of nitrogen's work | **101.98 %** | **PASS** |
| 3 | steam charge ≤ 60 % of nitrogen's mass | **35.1 %** | **PASS** |
| **4** | dry charge temperature ≤ 473 K | **550 K** | **FAIL** |
| 5 | reachable passively with α/ε ≤ 20 | **needs 7.6** | **PASS** |
| 6 | absorber ≤ 0.25 m² | **0.0515 m²** | **PASS** |
| **7** | within filled PTFE's 533 K limit | **550 K** | **FAIL** |
| **8** | net mass is a saving | **−1.285 kg** | **FAIL** |
| 9 | survives 35 min of eclipse | **69.9 kJ lost against 248.8 available** | **PASS** |
| 10 | equilibrium against α/ε | 8 points, **331 → 775 K** | **REPORT** |

### Heating water by being in space works, and that was the part in doubt

| | |
|---|---:|
| Energy per charge | **49.8 kJ** |
| **Average power over the cadence** | **41.5 W** |
| **α/ε required** | **7.6** — inside the selective-absorber coating class, **no concentrator** |
| **Absorber area at a 62 % sunlit duty cycle** | **0.0515 m² — a 23 cm square** |
| Eclipse | loses **69.9 kJ** against **248.8 kJ** held above freezing — **survives** |

None of the objections raised against water before this run survive it. It does not need a
concentrator, it does not need the stage to track the sun, the collector is not a deployable
structure, and it does not freeze in eclipse, the low emissivity that makes the selective
coating work also makes it a poor radiator, which is exactly the property needed.

The fluid is better too. 101.98 % of nitrogen's shot work on 35.1 % of the charge mass, and
the store saving is real: +0.869 kg with the 200 bar vessel and its gas replaced by 215 g of
water and a tank.

### And then the dryness requirement sets the temperature, and the temperature costs more

Steam condenses below 454 K at the 10.52 bar the stroke ends at, so the charge must start at
550 K, 277 °C, to stay dry.

| Material | Limit | |
|---|---:|---|
| Aluminium 6061-T6 | 473 K | **exceeded** |
| **Filled PTFE** | **533 K** | **exceeded** |
| Steel | 700 K | OK |

> ### The cascade, and it is the whole result
>
> | | |
> |---|---:|
> | Store saving, vessel and gas out, water and tank in | +0.869 kg |
> | Tube forced from aluminium to steel by the temperature | −2.154 kg |
> | Net | −1.285 kg |
>
> And that is before any absorber, coating, insulation, plumbing or pointing mass is counted,
> none of which this run charges for.

The second failure is worse than the mass. [A61](A61_seal_class.md) specified the seal at
17.8 N one day earlier, on filled PTFE, on the assumption it runs at −35 °C. At 550 K that
class is past its limit. The specification does not survive this fluid, and the seal returns to
being the unspecified component that four analyses already rest on.

There is no cheaper variant. Accepting *saturated* steam at 492 K keeps the seal inside PTFE's
range but still exceeds aluminium's 473 K, so the tube is steel either way, and it puts the
expansion into the wet region, which attacks dispersion, the thing this architecture can least
afford.

### The prediction held, including the part that mattered

**Recorded before the run: bands 2, 3, 5, 6 and 9 pass; band 4 fails and cascades to steel; band 7
fails and breaks A61's specification. All of it. *The prediction was made from the material
limits alone and the run put numbers on it.*

## What this settles

Steam is not adopted, and the reason is not the one it was likely to be. It is not the heating,
which works; not the eclipse, which it survives; not the fluid, which is better. It is that
staying dry costs 550 K, and 550 K costs a steel tube and the seal specification.

> A39's trade is no longer missing a heated working fluid. It has one, and it is screened by this
> run.

## What this run did not do

- No steam tables. Ideal gas throughout, and the wet case is bounded rather than computed,
  which is why band 4 asked what superheat avoids it entirely.
- It charged nothing for the absorber, the coating, the insulation, the plumbing or sun-pointing.
  Every figure flatters steam and it still fails band 8.
- It did not model the thermal, friction coupling at temperature, which A58 named and left
  uncomputed and which would be worse hot than cold.
- It names no product, compound or supplier, only material and coating classes.
- E4 stands. Nothing here is measured.

---

## Correction, 2026-08-20, this run screened steam at nitrogen's design point

The verdict above does not hold. The defect is in how the run was set up, not in what it
computed, and it is recorded as P90.

Every figure here was computed at a 2.0 L chamber, the volume A41 sized for cold nitrogen.
It was never re-optimised for steam, and it is the variable steam is most sensitive to.

| Chamber | **Temperature to stay dry** | Work |
|---:|---:|---:|
| **2.0 L — this run's** | **550 K** | 2397 J |
| 4.0 L | **523 K** | **2851 J** |
| 8.0 L | **508 K** | **3163 J** |

A larger chamber lowers the dry temperature *and* raises the work. At 4.0 L the charge is
523 K, inside filled PTFE's 533 K limit, delivering 2851 J and 37.75 m/s against nitrogen's 2350 J
and 34.28.

**So band 7 fails only at 2 L, and [A61](A61_seal_class.md)'s seal specification does survive steam
at a chamber chosen for it.** Band 8's net figure is equally suspect: it charged a steel tube
against a store saving computed at the wrong volume and did not count the chamber growth.

**What survives.** **Band 4's aluminium limit** — every point found sits above 473 K, so the tube is
steel regardless. And **bands 5, 6 and 9**, which are about the sun rather than the design point:
α/ε >= 7.6, a 23 cm absorber, survives eclipse. Those hold at any chamber.

[A63](A63_steam_design_point.md) is the run this should have been. *This sheet is annotated
rather than rewritten, and its verdict stands as the record of what was found at the wrong point.*
