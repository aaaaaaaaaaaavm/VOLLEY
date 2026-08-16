# A43 — the reservoir between shots, and whether it warms back up

**Bands declared 2026-08-16, before `analysis/reservoir_thermal.py` existed.**
Verify with `git show --stat <this commit> -- analysis/reservoir_thermal.py`, which must return nothing.

---

## Why this run exists

**[P64](../OPEN_PROBLEMS.md).** [A42](A42_fill_window.md) found A41's reservoir sized on gas the
bottle cannot give back, and the correction it produced is **bounded but not single-valued**:

| | Reservoir | Store | Added per satellite |
|---|---:|---:|---:|
| **Isothermal** | **7.65 L** | **4.67 kg** | **1.344 kg** |
| **Adiabatic**, as A42 modelled it | **11.25 L** | **6.01 kg** | **1.455 kg** |

**One term separates the two columns**: whether the gas left in the bottle recovers its temperature
between shots. A42 treated the reservoir as adiabatic, which is right for a 4 s blowdown and was
never argued for the **1200 s** cadence of [ADR-020](../docs/adr/020-inter-shot-cadence.md) that
follows it.

**This is the only open number in the Gen6 architecture.** It is worth about **1.3 kg of store**,
and every velocity-control question behind it inherits the reservoir temperature as an input.

## What A42 actually assumed, stated precisely

A42 carried **pressure** across shots and recomputed mass at each shot start as `p·V/(R·T₀)` with
T₀ = 300 K. That is neither limit: it drops pressure adiabatically *within* a fill, then reads the
next fill's mass as though the gas were at 300 K. **A43 carries mass and temperature as the state**,
which is the formulation that has both limits in it.

## Model

**State: gas mass and gas temperature in the reservoir.** Constant volume, ideal gas.

- **During a fill** — isentropic choked flow into the chamber, reservoir expanding adiabatically.
  The flow integration is **imported from `fill_window.py`, not restated.**
- **Between shots** — the gas relaxes toward the structure temperature at constant volume and
  constant mass, first-order with a lumped time constant **τ = m·c_v / (h·A)**, over the 1200 s
  cadence. Pressure follows the temperature back up.

**The heat-transfer coefficient is swept, not chosen.** `h` is the whole answer and this run does
not get to pick it. The sweep spans the range from conduction-only to a well-coupled wall.

**Stated as an input, not derived here:** nitrogen is a homonuclear diatomic and is **effectively
transparent in the infrared**, so radiation from the vessel wall does not warm the gas — only
conduction and any forced circulation do. In free fall there is no buoyancy-driven convection.
**If that is wrong, this run is wrong**, and it is the assumption to attack first.

**Optimistic and pessimistic terms, both stated:** the vessel wall is treated as an infinite
reservoir at the structure temperature, which is optimistic for recovery; no forced circulation
exists, which is pessimistic. Neither is modelled in detail.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | With **instant relaxation** (τ → 0) the required reservoir reproduces A42's isothermal **7.65 L** within **5 %** | The formulation does not contain the isothermal limit, and neither limit can be trusted |
| **2** | With **no relaxation** (τ → ∞) the required reservoir is **strictly larger** than band 1's | The model is not monotone in the thing it exists to measure |
| **3** | Required reservoir is **monotonically non-increasing** in `h` across the sweep | The lumped model is not behaving as a lumped model |
| **4** | The required reservoir at every `h` in the sweep lies **within 6.0 – 15.0 L** | The answer is outside the bracket P64 declared, and P64's framing was wrong rather than merely imprecise |
| **5** | **Minimum gas temperature** across the twelve-shot sequence, at the least favourable `h`, stays **≥ 150 K** | Ideal gas and constant c_v are not defensible and the model is out of validity before it is out of margin |
| **6** | Store mass at the **conservative** end of whatever the sweep gives ≤ **12.55 kg** | The correction breaks A37's budget, as A42 band 5 also tested |
| **7** | Added mass per satellite at that same conservative end ≤ **2.0 kg**, threshold unmoved | Kill criterion 1 re-crosses on the corrected store |
| **8** | Changing the fill orifice from 1.0 mm to **0.5 mm and 2.0 mm** moves the required reservoir by ≤ **2 %** | The answer is an artefact of the orifice rather than a property of the store |

## Predictions, recorded before the run so a miss is on the record

Three of these are mine and I expect at least one to be wrong. Previous runs in this project have
caught me at 2.05 against 4.330 kg/sat, at 40 % against 28.1 %, and on all three of A41's
seal, friction and gas-budget predictions.

1. **τ will come out long compared with the 1200 s cadence**, because conduction through a
   stagnant gas is the only path and the gas thermal mass is around a kilogram. If so the honest
   answer is **nearer the adiabatic 11.25 L than the isothermal 7.65 L**, which is the opposite of
   what [ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md) and P64 both currently say.
2. **Band 5 will pass comfortably.** The expansion is from 200 bar and takes out roughly a quarter
   of the mass over twelve shots, so the temperature excursion should be tens of kelvin, not
   hundreds.
3. **Band 8 will pass**, because the required reservoir is set by usable gas above the charge
   pressure and not by flow rate — A42 already found flow area was never the constraint.

## Result

**RUN 2026-08-16. Seven of eight bands pass. The one that fails is the one that was checking
somebody else's arithmetic, and it found it wrong.**

| # | Band | Result | |
|---|---|---|---|
| 1 | instant relaxation reproduces A42's 7.65 L within 5 % | **8.25 L, 7.8 % off** | **FAIL** |
| 2 | no relaxation requires strictly more | 9.55 L against 8.25 L | **PASS** |
| 3 | monotonically non-increasing in `h` | monotone | **PASS** |
| 4 | every solved point within 6.0 – 15.0 L | 8.25 – 9.55 L | **PASS** |
| 5 | minimum gas temperature ≥ 150 K | **201.9 K** | **PASS** |
| 6 | store at the conservative end ≤ 12.55 kg | **5.38 kg** | **PASS** |
| 7 | added mass per satellite there ≤ 2.0 kg | **1.403 kg** | **PASS** |
| 8 | orifice 0.5 and 2.0 mm move it by ≤ 2 % | **0.00 %** | **PASS** |

### The sweep

| h (W/m²K) | Reservoir | τ | T_min | Store | Per satellite |
|---:|---:|---:|---:|---:|---:|
| **0** — no relaxation | **9.55 L** | ∞ | 201.9 K | 5.38 kg | 1.403 kg |
| 0.1 | 9.30 L | 56 442 s | 212.9 K | 5.29 kg | 1.395 kg |
| **0.3** — *conduction only* | **8.95 L** | 18 575 s | 230.6 K | **5.16 kg** | **1.384 kg** |
| 1.0 | 8.45 L | 5 467 s | 259.6 K | 4.97 kg | 1.369 kg |
| 3.0 | 8.30 L | 1 811 s | 274.3 K | 4.92 kg | 1.364 kg |
| 10 – ∞ | **8.25 L** | ≤ 542 s | 276.9 K | 4.90 kg | 1.362 kg |

### The answer: the bottle does not warm back up

**Conduction through stagnant nitrogen gives h = 0.326 W/m²K at this geometry, and τ = 17 460 s
against a 1200 s cadence — fourteen and a half times longer than the wait between shots.**

**[ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md) and [A42](A42_fill_window.md) both
say the truth sits nearer the isothermal figure. It does not.** It sits at the other end, and the
reason is that the two paths that would carry heat into the gas are both absent in this
application: nitrogen is a homonuclear diatomic and does not absorb infrared, so the wall cannot
radiate to it, and free fall removes buoyancy-driven convection. **Conduction across 80 mm of
stagnant gas is all that is left.**

**The design number is 9.55 L**, the no-relaxation case, carried for the same reason ADR-032 gave
for carrying the adiabatic figure before: it is the conservative end and this run says so. The
physical estimate is **8.95 L**.

### Band 1, and what it caught

**A42's 7.65 L is not reproducible.** Carrying mass and temperature as the state and letting the
gas fully re-equilibrate gives **8.25 L**.

**A42's 11.25 L is not reproducible either, and it is wrong in the other direction.** A42 carried
pressure across shots and recomputed mass as `p·V/(R·T₀)` at each shot start. Gas that has cooled
adiabatically is *denser* than that at the same pressure, so the bookkeeping **discarded mass that
was really there** and demanded a bigger bottle than the physics does. The true no-relaxation
figure is **9.55 L**.

> **So the bracket P64 declared was wrong at both ends.** Not 7.65 – 11.25 L but **8.25 – 9.55 L**,
> a spread of 1.30 L rather than 3.60, and **the answer sits at the top of it rather than the
> bottom.** The direction of the correction was right; its size and its resolution were not.
> Recorded as **P66**, because those two numbers are in `cad/parameters.json`, in ADR-032 and in
> A42's own result table.

### The predictions

All three held, which has not happened before in this project.

1. **τ long against the cadence, answer nearer adiabatic** — 17 460 s against 1200 s, and the
   design number is the no-relaxation one. *This contradicted ADR-032 and P64 and it was right.*
2. **Temperature excursion in tens of kelvin, not hundreds** — 98 K at the adiabatic extreme,
   which is the top of "tens" and only just held; **69 K** at the conduction point.
3. **Band 8 passes** — 0.00 %. The required reservoir is set by usable gas above the charge
   pressure, exactly as A42 found for flow area.

## What this run does not do

- **No wall thermal mass.** The vessel is treated as an infinite reservoir at 300 K. Including it
  would slow recovery further, so this is optimistic in the direction that matters.
- **No forced circulation.** A fan or a recirculation loop would move the answer toward the
  isothermal end, and would be the way to buy the 0.60 L back if it were ever worth the hardware.
- **No gas recovery from the fired chamber**, which still vents 43 bar of a 2 L volume every shot
  and is modelled nowhere.
- **k for nitrogen is taken at 300 K and 1 bar.** It rises with pressure, which moves h up; the
  sweep spans three decades, so the conclusion does not turn on the constant.
- **Nothing here is measured.**
