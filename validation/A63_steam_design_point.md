# A63 — the steam design surface, which is the run A62 should have been

**Bands declared 2026-08-20, before `analysis/steam_design.py` existed.**
Verify with `git show --stat <this commit> -- analysis/steam_design.py`, which must return nothing.

---

## Why this run exists

**[P90](../OPEN_PROBLEMS.md). [A62](A62_steam_working_fluid.md) computed every figure at a 2.0 L
chamber** — the volume [A41](A41_precharged_chamber.md) sized for **cold nitrogen** — and concluded
steam needs 550 K, exceeds filled PTFE's limit, breaks [A61](A61_seal_class.md)'s seal
specification and costs 1.285 kg.

**The chamber was never re-optimised for the fluid, and it is the variable steam is most sensitive
to.** A larger chamber **lowers the temperature needed to stay dry and raises the work at the same
time** — at 4.0 L the charge is **523 K** and the shot is **2851 J**, against 550 K and 2397 J.

> **This is the same mistake [A49](A49_design_surface.md) exists to prevent, made one fluid later.**
> A37 swept stage length at a fixed acceleration and A49 observed that *"the inverse was never
> asked."* **A62 swept nothing at all.**

## The physics that makes the chamber the lever

**The expansion must end above the saturation line or it condenses**, and two-phase expansion does
less work and repeats worse — which [A55](A55_trim_authority.md) showed is what this architecture
can least afford.

**T_dry = T_sat(p₀·r^γ) / r^(γ−1)**, where **r = V₀/(V₀ + A·L)**.

**A larger chamber raises r**, which raises the end pressure — *and therefore the saturation
temperature* — but raises the end temperature faster. **The two race and the second wins**, so
T_dry falls toward its floor, **T_sat(p₀) itself: 492 K at 22.73 bar.**

**That floor is what sets the material limits**, not the expansion:

| Material | Limit | **Saturated charge-pressure ceiling** |
|---|---:|---:|
| Aluminium 6061-T6 | 473 K | **15.92 bar** |
| **Filled PTFE** | **533 K** | **48.73 bar** |
| Steel | 700 K | 375.96 bar |

## What has to be traded, and A62 traded none of it

**A larger chamber costs chamber mass and water per shot.** The chamber is sized by
`precharged.chamber_kg`, and the water is p₀V₀M/RT — **both rise with volume, and the store saving
is the reason steam was proposed.** *A62 asked whether steam works. This asks what it costs.*

## Declared before the run

**Everything imported: the expansion from `precharged`, the chamber mass model from
`precharged.chamber_kg`, the tube masses from [A59](A59_tube_structure.md), the store baseline from
[A56](A56_reservoir_resized.md), the solar terms from A62.** Only the sweep is new.

| | |
|---|---|
| Charge pressure swept | **8 – 45 bar** |
| Chamber swept | **2 – 32 L** |
| Steam: M, γ | 0.018 kg/mol, 1.33 — **ideal gas, no steam tables in this repository** |
| Material limits, enthalpy, tank allowance | as A62 declared them — **handbook, NEEDS SOURCE** |
| Baseline to beat | nitrogen: **2350 J, 34.28 m/s, 11.36 g peak, 612 g of gas in a 3.46 L / 200 bar COPV** |

## The prediction, recorded before the run

**I expect band 3 to pass** — a point exists inside filled PTFE's limit that beats nitrogen on work
*and* velocity, because 4 L already does at 523 K.

**I expect band 4 to fail** — nothing reaches aluminium's 473 K at a useful chamber, so **the tube
is steel regardless and A62's band 4 survives its own correction.**

**Band 6 is the one I cannot call.** The store saving is real and the chamber growth and steel tube
are real, and I have not put them on the same page. **That is the whole question, and A62 answered
it at the wrong point.**

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | At **2.0 L and 22.7258 bar** the surface reproduces A62's **550 K** and **2397 J** within 1 % | The surface is not standing on A62 and the correction cannot be compared to it |
| **2** | The nitrogen baseline reproduces **2350 J** and **34.28 m/s** within 1 % | Nothing below is comparable to the fluid it must beat |
| **3** | **A point exists with T_dry ≤ 533 K delivering ≥ 2350 J** | **Steam cannot run inside filled PTFE's limit at any chamber**, and A61's seal specification really does not survive it |
| **4** | A point exists with **T_dry ≤ 473 K** delivering ≥ 2350 J | The tube is steel at every steam design point, and P85 is forced |
| **5** | At the selected point, peak acceleration is **≤ 25 g** — the payload qualification cap | The chamber that fixes the temperature breaks the payload environment |
| **6** | **Net mass is a saving**, counting the store, the water, the tank, the chamber growth **and the tube material the temperature forces** | **Steam costs mass, and A62's verdict survives its own correction** |
| **7** | Campaign water mass is **≤ nitrogen's 612 g** | The fluid advantage is spent on the larger chamber |
| **8** | At the selected point the shot delivers **≥ nitrogen's 34.28 m/s** | Steam is bought at a velocity penalty |
| **9** | The solar terms still close — **α/ε ≤ 20**, absorber **≤ 0.25 m²**, survives eclipse | The larger charge cannot be raised passively, and the heating that motivated this is gone |
| **10** | **REPORT, no pass/fail.** The surface, with the Pareto set published rather than a point | — |

## What this run will not do

- **No steam tables.** Ideal gas throughout, and the wet region is avoided by construction rather
  than modelled.
- **It does not design an absorber, a coating, insulation, plumbing or a sun-pointing scheme**, and
  charges nothing for any of them — **so every figure flatters steam, as A62's did.**
- **It does not re-run A44, A48, A54, A55, A58 or A61 at a steam design point.** Dispersion, the
  trim authority, the pulse store and the seal specification all still carry nitrogen's numbers.
- **It names no product, compound or supplier.**
- **E4 stands.** Nothing here is measured.

---

## Result

**RUN 2026-08-20. Eight of ten bands pass. A62's verdict survives its own correction — and by a
wider margin than A62 found — but the reason has moved, and there is a conditional under it.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A62 at 2.0 L | **550 K, 2397 J** | **PASS** |
| 2 | nitrogen baseline reproduces | **2350 J, 34.28 m/s** | **PASS** |
| 3 | a point ≤ 533 K delivering ≥ 2350 J | **43 points** | **PASS** |
| **4** | a point ≤ 473 K | **0 points** | **FAIL** |
| 5 | selected point within the 25 g cap | **10.00 g** | **PASS** |
| **6** | net mass is a saving | **−1.813 kg** | **FAIL** |
| 7 | campaign water ≤ 612 g | **296 g** | **PASS** |
| 8 | selected shot ≥ 34.28 m/s | **34.33 m/s** | **PASS** |
| 9 | solar closes | **α/ε 6.4, 0.0711 m², survives eclipse** | **PASS** |
| 10 | the surface | **108 points, 43 inside PTFE, 0 a saving** | **REPORT** |

### What P90's correction actually bought

**Band 3 passed with 43 points, so [A61](A61_seal_class.md)'s seal specification does survive
steam.** *That was A62's band 7 failure and it is corrected.*

**Band 4 failed with zero points, so A62's band 4 survives its own correction.** **No steam design
point in 108 reaches aluminium's 473 K**, because the floor is T_sat(p₀) and the charge pressures
that make 2350 J all sit above it. **The tube is steel at every steam design point.**

### And that is the whole result

| Selected: **20.00 bar, 3 L → 526 K, 2357 J, 34.33 m/s, 10.00 g** | |
|---|---:|
| Removes — COPV 0.470, gas 0.813, old chamber 0.338 | **−1.622 kg** |
| Adds — water 0.296, tank 0.20, **chamber 0.785**, **steel tube 2.154** | **+3.434 kg** |
| **Net** | **−1.813 kg** |

> **The steel tube penalty alone is 2.154 kg — larger than everything steam removes.**
>
> **A62 found −1.285 kg at the wrong point. The correction made it worse, not better**, because a
> chamber chosen for steam is *larger*, and chamber mass rises with it: **0.338 → 0.785 kg.**

**Zero of the 43 PTFE-feasible points are a net saving.** *It is not close and it is not a corner
case.*

### The conditional, which is the useful part

**The 2.154 kg is charged to steam because the temperature forces it. But [P85](../OPEN_PROBLEMS.md)
has not been decided, and there are reasons to choose steel that have nothing to do with the
fluid** — surface hardness and galling resistance at a sliding seal bore, and
[A59](A59_tube_structure.md) found the material barely moves the beam mode (1.67 Hz aluminium
against 1.68 steel).

**If the tube is steel anyway, steam stops paying for it:**

| At 20.00 bar, 3 L | |
|---|---:|
| Removes | −1.622 kg |
| Adds — water, tank, chamber only | +1.281 kg |
| **Net** | **+0.341 kg** |

| bar | L | T_dry | v | a | Net, tube penalty removed |
|---:|---:|---:|---:|---:|---:|
| **20.00** | **3** | **526 K** | **34.33 m/s** | **10.00 g** | **+0.341 kg** |
| 22.73 | 3 | 533 K | 36.60 m/s | 11.36 g | +0.304 kg |
| 20.00 | 4 | 517 K | 35.42 m/s | 10.00 g | +0.069 kg |

> **So steam is a marginal saving *conditional on a decision that has not been taken*, and a
> 1.8 kg cost if that decision goes the other way.** **It is not a mass argument either way** — the
> best case is **+0.341 kg**, which is **less than the absorber, coating, insulation, plumbing and
> sun-pointing this run charges nothing for.**

### What steam is actually good at, stated separately from the mass

**The mass is a wash. These are not:**

- **The 200 bar COPV disappears** — a pressure-vessel qualification, a burst-safety case and a
  launch-provider conversation, worth more in programme terms than the kilogram either way.
- **The shot is slightly better** — 34.33 m/s at **10.00 g** against nitrogen's 34.28 at 11.36,
  because γ = 1.33 lets the pressure fall more slowly. **A gentler shot at the same velocity.**
- **Campaign propellant halves** — **296 g against 612 g.**
- **The heating closes comfortably** — 57.3 W, **α/ε 6.4** inside the selective-coating class with
  no concentrator, a **27 cm square** absorber, and it survives eclipse.

## What this run did not settle

- **It did not re-run A44, A48, A54, A55, A58 or A61 at a steam design point.** Dispersion, the
  trim authority, the pulse store and the seal specification **all still carry nitrogen's numbers**,
  and a 526 K seal is not a −35 °C seal.
- **It charged nothing for the absorber, coating, insulation, plumbing or sun-pointing.**
- **No steam tables.** Ideal gas, wet region avoided by construction.
- **E4 stands.**
