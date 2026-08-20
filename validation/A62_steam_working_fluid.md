# A62 — steam, with the water heated by being in space

**Bands declared 2026-08-20, before `analysis/steam_fluid.py` existed.**
Verify with `git show --stat <this commit> -- analysis/steam_fluid.py`, which must return nothing.

---

## Why this run exists

**[A39](A39_store_trade.md) traded a steel spring, cold gas and keeping the motor, and screened a
lead screw, a rack and pinion and a flywheel — each carrying the run that screened it.** It never
considered **a heated working fluid**, and that is a hole in the trade rather than anyone's
oversight.

**The proposal is specific and it is not a thruster.** Water stored at low pressure, raised to
steam by **solar flux alone** — no resistive heater, no electrolysis, no combustion — and fired as
the same closed adiabatic expansion A41 specified. **The gun is unchanged; only the working fluid
and how it is charged are different.**

**What makes it worth computing rather than dismissing:** steam's molecular weight is **18 against
nitrogen's 28**, and its ratio of specific heats is **1.33 against 1.4**, so the same charge
pressure is reached with less mass and the pressure falls more slowly through the stroke. **Both
point the same way, and the 200 bar COPV disappears.**

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

**The expansion model, the design point and the tube masses are imported, not restated.**

## The prediction, recorded before the run

**I expect bands 2, 3, 5, 6 and 9 to pass** — steam does slightly more work on roughly a third of
the mass, a selective absorber coating reaches the temperature without a concentrator, and the
absorber is small.

**I expect band 4 to fail**, and for that failure to cascade: the charge must be superheated well
past aluminium's useful limit, **which forces the tube to steel and hands [P85](../OPEN_PROBLEMS.md)
its heavy answer — 2.15 kg — for a store saving of about one.**

**I expect band 7 to fail too**, and this is the one that would matter most: **A61 specified a seal
at 17.8 N on the assumption it runs at −35 °C.** At steam temperature filled PTFE is at or past its
limit, so **the specification produced yesterday would not survive this fluid.**

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

- **No steam tables.** The ideal-gas treatment is stated at each use and **the wet-expansion case is
  bounded rather than computed** — that is why band 4 asks what superheat avoids it entirely.
- **It does not design an absorber, a coating, insulation, plumbing or a sun-pointing scheme**, and
  **none of that mass is counted** — so every figure below flatters steam.
- **It names no product, compound or supplier**, only material and coating classes.
- **It does not model the thermal-friction coupling** at steam temperature, which A58 named and
  left uncomputed and which would be worse hot than cold.
- **E4 stands.** Nothing here is measured.
