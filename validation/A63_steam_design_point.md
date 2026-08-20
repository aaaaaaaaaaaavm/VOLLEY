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
