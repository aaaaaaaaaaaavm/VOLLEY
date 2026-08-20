# A58 — the chamber, the tube and the seal across a campaign

**Bands declared 2026-08-19, before `analysis/chamber_thermal.py` existed.**
Verify with `git show --stat <this commit> -- analysis/chamber_thermal.py`, which must return nothing.

---

## Why this run exists

**Nothing in this repository models the chamber thermally.**
[A43](A43_reservoir_thermal.md) settled the *reservoir* between shots and says so; the chamber, the
expansion cooling and twelve cycles of both are unmodelled.
[A39](A39_store_trade.md) states it designs *"no cylinder, valve, seal or latch"*, and
[A40](A40_blowdown_transient.md) that it does not model *"temperature drop in the chamber"*.

**[ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) made both halves of it worse and
neither was checked.**

## Two opposing effects, and both land on the same component

**The gas gets much colder.** A longer stroke expands the same charge through a larger volume
ratio, so the temperature drop nearly triples: **−22.4 K at 2.18 m becomes −62.1 K at 8.0 m**,
taking the gas to **238 K, −35.2 °C**, every shot.

**And the seal gets much hotter.** Friction work is force × stroke, so it scales directly:
**181.8 J becomes 667.2 J per shot**, at **2419 W instantaneous** where the seal is moving fastest.

> **Both land on the seal — which owns 98.7 % of the dispersion ([A55](A55_trim_authority.md)),
> is the entire justification for ADR-033, and has never been measured, specified or given a
> material.** *P67 is not a room-temperature friction measurement. It is a friction measurement at
> −35 °C on a component dissipating two and a half kilowatts into itself.*

**And [P85](../OPEN_PROBLEMS.md) is in the middle of it.** The tube's material is stated nowhere,
so the differential expansion between piston and bore across a 62 K swing cannot be computed
without choosing one — and the choice is worth about **11 µm of clearance** on a 15.805 mm bore.

## Declared before the run

**Handbook values, named at each use, none of them measured and none vendor-sourced** — the same
standing A39 gave its gas model.

| | Value | |
|---|---|---|
| Steel: c_p, α | **460 J/kg·K**, **12 × 10⁻⁶ /K** | chamber, and the tube if it is steel |
| Aluminium: c_p, α | **900 J/kg·K**, **23 × 10⁻⁶ /K** | the tube if it is aluminium — **P85** |
| Elastomer seal: c_p | **1500 J/kg·K** | |
| **Seal mass** | **swept 0.5 – 10 g** | *NEEDS SOURCE: no seal exists in any file* |
| Nitrogen condensation at 10.10 bar | **≈ 103 K** | |
| Chamber, tube, friction, cadence | 0.3382 kg, 1.1404 / 3.294 kg, 83.4 N, 1200 s | `fill_window`, A49, A59, `gen6_dispersion` |

**The gas model, the friction force and the design point are imported, not restated** — `pc.work`,
`gd.FRICTION_N`, and `cad/parameters.json` through `precharged.design_point()`.

## The prediction, recorded before the run

**I expect bands 1, 2 and 3 to pass** — the gas is nowhere near condensing, and 8007 J of campaign
friction into a kilogram of metal is a few kelvin.

**I expect band 5 to fail**, and badly. A small seal absorbing 667 J in five milliseconds has
nowhere to put it, and the adiabatic bound is hundreds of kelvin. **The question this run should
answer is not whether it fails but what fraction of the heat must leave the seal for it to
survive** — because that fraction is a design requirement nobody has written down.

**I expect band 6 to fail on dissimilar metals and pass on matched ones**, which would make P85 a
thermal decision as well as a mass one.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

- **No FEA, no CFD, no contact model.** Lumped masses, adiabatic bounds, and one conduction path.
- **It does not design a seal**, name a material, or claim any of these is buildable.
- **It does not model the seal's friction changing with its own temperature**, which is the coupling
  that would matter most — friction heats the seal, a hotter seal has different friction, and that
  feeds straight back into the dispersion. **Named here and not computed.**
- **It does not settle P85.** It reports what each material choice costs thermally.
- **E4 stands.** Nothing here is measured.
