# A65 — the per-cell ejector, re-asked against pyrotechnic gas generation

**Bands declared 2026-08-20, before `analysis/pyro_ejector.py` existed.**
Verify with `git show --stat <this commit> -- analysis/pyro_ejector.py`, which must return nothing.

---

## Why this run exists

**[A53](A53_backup_ejector.md) failed on energy and nothing else.** Seven of its eight bands passed.
Band 7 failed because a spring sized for a clean departure stores **4.5 J**, and pushing the payload
the length of a sealed tube against [A41](A41_precharged_chamber.md)'s friction allowance costs
**181.8 J** at 2.18 m and **667.2 J** at [ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md)'s
8.0 m — a **148× shortfall**.

**[P81](../OPEN_PROBLEMS.md) carries the consequence**, and it is the most expensive open entry in
the record: [A47](A47_gen6_fmea.md) priced a per-cell ejector at **+2.27 satellites** delivered at
*r* = 0.99, against **+0.37** for the entire Gen5 → Gen6 architecture change — **six times more**,
because a mechanism in every cell makes the drive **satellite-forfeiting instead of
manifest-forfeiting**, which is the only move that touches what **E30** actually says.

**A53 closed it as architectural. It was not architectural — it was a store choice**, and the same
mistake [A54](A54_pulse_chain.md) made about the pulse store: *it priced the only energy store this
repository happened to have data for.* [A64](A64_pulse_store_technology.md) corrected that one by
changing technology class rather than design. **This run asks whether P81 has the same escape.**

## The technology class

**A solid-propellant gas generator of the automotive restraint class.** Named as a technology class,
as [A39](A39_store_trade.md) named its gas model and A64 named its capacitors. **No product,
supplier or organisation is named.**

| | | |
|---|---|---|
| **Gas produced per unit** | **0.5 – 0.9 mol** | published; set by the volume the unit must fill |
| **Solid generant mass** | **20 – 100 g** | published, driver-side class |
| **Total gas temperature** | **1000 – 1400 K** | published tank-test measurement; combustion chamber above 1200 K |
| **Discharge time** | **order 30 ms**, filling 60 L | published |
| Working gas | nitrogen, **γ = 1.4**, M = 0.028 kg/mol | as [A39](A39_store_trade.md) declared it |
| Filter/heat-sink class | a metal filter that **collects condensed phase and acts as a heat sink** | published; it is why this design has a cooling stage at all |

**Two published numbers decide this run before any design is done.** The tube's swept volume is
**A × L = 1.5696 L**. An automotive unit fills **60 L**. *The device is not marginal here; it is
roughly forty times oversized, and the whole engineering problem is metering it down.*

## The model, declared

**The generator discharges through a heat sink into a plenum of volume V₀ behind the payload, and
the charge then expands adiabatically along the stroke** — the same closed expansion
`precharged.work()` already implements, with the charge arriving hot instead of stored cold.

- The state at the start of expansion is **n moles at the sink outlet temperature**, so
  `p₀ = n·R·T / V₀`.
- Work is `p₀V₀/(γ−1)·[1 − r^(γ−1)]`, `r = V₀/(V₀ + AL)` — **`precharged.work()`, unmodified**.
- **`a_peak = p₀A/m` contains no L**, which A41 recorded and which makes the plenum volume the
  only free variable once the charge is chosen.
- **V₀ is therefore solved, not guessed**: it is the smallest plenum that holds the peak under the
  payload's acceleration cap.
- **The cap used is A37's 25 g payload limit, not Gen6's commanded 11.36 g.** A backup ejector is an
  off-nominal event. The payload must survive it; it does not have to enjoy it.

**Zonal cooling is the model's weakest link and is declared as such.** Treating the sink as reaching
thermal equilibrium with the whole charge before expansion begins is the conservative direction for
work and the optimistic direction for sink mass, and 30 ms is not obviously long enough for either.

## The prediction, recorded before the run

1. **Band 2 passes and passes hugely.** 14 g of gas in a 1.57 L swept volume is a great deal of gas.
2. **Band 4 — per-cell mass — is the one that decides this run.** The generant is light and the
   plenum is light; **the heat sink is not**, and it is being asked to absorb the enthalpy of a
   charge four hundred degrees hotter than the tube can tolerate.
3. **Band 6 passes only because a sink is carried.** Uncooled, the class is 1000–1400 K against
   ADR-035's **473 K**, and the same ceiling foreclosed steam in [A63](A63_steam_design_point.md).
4. **Band 3 will be comfortable at the bottom of the class and tight at the top**, which would mean
   the design must specify a charge rather than accept the class.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The run reproduces the register's own arithmetic: friction work over the 8.0 m stroke at A41's allowance is **667.2 J**, and a 1.5 m/s spring stores **4.5 J**, within 1 % of both | This run is not the same model as A53 and nothing below is comparable to it |
| **2** | At the **bottom** of the published class — **0.5 mol**, cooled to the tube ceiling — expansion work over the 8.0 m stroke **exceeds 667.2 J** | The smallest device in the class does not do the one thing the device is for. **This is A53 band 7, re-asked** |
| **3** | The plenum the 25 g cap requires, at the bottom of the class, is **≤ 2.0 L** — no larger than the chamber `gen6_store` already carries | The backup needs a bigger pressure vessel than the drive it backs up |
| **4** | Per-cell mass — generant, plenum vessel, heat sink and a declared housing allowance — is **≤ 0.25 kg** | A53's own band 1 threshold, unchanged, so the two runs are directly comparable |
| **5** | Twelve of them keep added mass per satellite **≤ 2.0 kg**, against A56's **3.1216 kg** store and A37's 11.452976 kg base | It re-crosses the one kill-criterion numerator Gen6 currently passes — **which is exactly how A53's tube-clearing variant died, at 2.129 kg** |
| **6** | The gas **entering the tube** is at or below **ADR-035's 473 K ceiling**, with the sink that achieves it costed inside band 4 | The device destroys the tube it is clearing, and ADR-035's falsifier fires |
| **7** | Exit velocity firing alone, **after** the 667.2 J of friction, is **≥ 1.0 m/s** | It clears the tube on paper and not in the tube. A53 band 7's own wording, at the new stroke |
| **8** | The A47 model re-run **with the device as a shot-scope element that can itself fail** returns **≥ 9.0 satellites** at *r* = 0.99 | The gain is an artefact of giving a new pyrotechnic part infinite reliability. **A53 band 5, unchanged** |
| **9** | The **unpriced costs are named and not counted as a pass**: range safety, ordnance handling, shelf life, a hazard classification for twelve initiators, and the fact that a fired generator cannot be tested before flight | The run claims a benefit it has not paid for |
| **10** | **REPORT**: work, peak pressure, plenum volume, sink mass and exit velocity across the full published class, **0.5–0.9 mol × 1000–1400 K**, and whether the top of the class is usable at all | — |

## What this run is not

**It is not a proposal to replace the gas drive.** If the numbers come out where band 2 predicts,
that question follows immediately and **it is a Gen7 question, not this one.** A65 is scoped to the
defect P81 names: *can a per-cell device clear the tube when the drive is dead.*

**It is not evidence that the device works.** It is evidence about **energy, mass and temperature**.
Nothing here has been built, and **E4** still says what it has always said.

---

## Result

**RUN 2026-08-20. Nine of ten bands pass. Band 4 fails at 0.4350 kg against A53's 0.25 kg
threshold — and the band that governs the design, band 5, passes with 0.35 kg per satellite to
spare.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces 667.2 J and 4.5 J within 1 % | 667.23 J, 4.50 J, **148.3×** | **PASS** |
| 2 | bottom of the class exceeds 667.2 J | **2331.6 J — 3.49×** | **PASS** |
| 3 | plenum ≤ the existing 2.0 L chamber | **0.3933 L** | **PASS** |
| 4 | **per-cell mass ≤ 0.25 kg** | **0.4350 kg** | **FAIL** |
| 5 | added mass per satellite ≤ 2.0 kg | 5.2204 kg total, **1.6496 kg/sat** | **PASS** |
| 6 | gas entering the tube ≤ 473 K | 473 K on a **92.6 g** sink | **PASS** |
| 7 | firing alone, ≥ 1.0 m/s after friction | **28.85 m/s** | **PASS** |
| 8 | A47 re-run ≥ 9.0 satellites at *r* = 0.99 | **9.261** | **PASS** |
| 9 | unpriced costs named, not counted | 6 named | **PASS** |
| 10 | REPORT: the published class | 15 points; **the top of the class is usable** | REPORT |

### The energy objection is gone, and it is not close

| | |
|---:|---|
| **4.5 J** | what A53's spring stored |
| **667.2 J** | what clearing the 8.0 m tube costs |
| **2331.6 J** | what the **smallest** charge in the published class delivers, **after** being cooled to the tube's own material ceiling |

**A53 failed by 148×. This clears by 3.49× on the worst case of the class.** The reason is stated in
one line and it is not subtle: **the tube's swept volume is 1.5696 L, and a unit of this class is
built to fill 60 L.** The engineering problem was never finding enough energy — it is metering it
down, and the plenum volume does that arithmetically, because `a_peak = p₀A/m` has no `L` in it.

### Band 4 fails, and prediction 2 named the right band for the wrong reason

**I predicted the heat sink would be what breaks the mass budget. It is not.**

| Per cell, bottom of class | |
|---|---:|
| Solid generant | 0.0200 kg |
| **Plenum vessel** | **0.2025 kg** |
| Heat sink | 0.0926 kg |
| Housing, initiator, gas path — **declared guess, carried from A53 unchanged** | 0.1200 kg |
| **Total** | **0.4350 kg** |

**The sink is 92.6 g. The pressure vessel is 202.5 g — 46.6 % of the cell.**

> **And it is minimum-gauge limited, not pressure limited.** At 0.3933 L the sphere-equivalent
> radius is 45.45 mm and the hoop wall the pressure actually needs is **0.909 mm**, against
> `precharged.chamber_kg`'s **1.0 mm** minimum. **The vessel is as light as that function will
> ever make it at this size**, and the function builds it in steel at 7800 kg/m³.

**This is recorded as an observation and not as a band**, because the band failed and a band is
never widened after a result is known: *the same shell in the aluminium ADR-035 chose for the tube
would be **70.1 g**, and the cell would come to **0.3031 kg** — still above A53's threshold.* **Band
4 fails either way.** What the observation establishes is **where** the mass is, so that the next
run knows what to attack.

### The threshold that failed is not the threshold that governs

**Band 4's 0.25 kg is A53's own band 1, inherited unchanged so the two runs compare.** A53 set it
for a spring, and it is a proxy. **Band 5 is the real constraint** — it is the kill-criterion
numerator, the one thing Gen6 currently passes and A53's tube-clearing variant re-crossed at
**2.129 kg per satellite**.

| | Per satellite |
|---|---:|
| A53, spring sized only for clearance — *and it could not clear the tube* | 1.538 kg |
| **A53, spring sized to clear the tube** | **2.129 kg — over the threshold** |
| **A65, pyrotechnic, bottom of the class** | **1.6496 kg — under it, with 0.35 kg to spare** |

**So P81 does not stay closed as architectural.** It moves from *"no per-cell device can clear this
tube"* to *"a per-cell device clears it, and owes 185 g of mass reduction against an inherited
threshold it does not have to meet."*

### The whole published class is usable, which prediction 4 got wrong

**I expected the plenum to be tight at the top of the class. It is comfortable everywhere** —
0.3933 L to 0.7079 L across 0.5–0.9 mol and 1000–1400 K, against the 2.0 L chamber the design
already carries.

**The reason is the cooling stage.** The plenum is sized by `V₀ = nRT·A/(m·g·25)` at the **sink
outlet** temperature, not the flame temperature, so **the same 473 K ceiling that makes the sink
necessary also shrinks the vessel by a factor of two to three.** My estimate used the uncooled
temperature and was wrong by that factor.

**Peak pressure is 50.00 bar and peak acceleration 25.00 g at every point in the class**, by
construction — the cap is what sizes the plenum, so it is met identically everywhere and the charge
only moves how long the push lasts.

### What this run refuses to do

**Exit velocity firing alone, at the smallest charge in the class, is 28.85 m/s. The gas drive's
own rated exit velocity is 29.01 m/s.**

> **That is not a result about a backup ejector.** It says a per-cell pyrotechnic charge reproduces
> the entire Gen6 shot, which would delete the reservoir, the fill valve, the fire valve, the
> chamber and the store — **five of the seven shared elements A47 counts**, and the store's
> 3.1216 kg with them.
>
> **A65 is not that run and does not claim it.** It is scoped to the defect P81 names, the sizing
> here is deliberately a *backup* sizing carried on top of a store that stays, and **the mass table
> above keeps the store in.** The larger question is recorded as **P91** and belongs to whatever
> comes after Gen6.

### What was not paid for

**Named, and none of it counted as a pass:**

- **Range safety.** Twelve initiators on a launch vehicle is a licensing question and **no file in
  this repository has ever priced one.**
- **Ordnance handling.** Integration, transport and storage all change category.
- **Shelf life.** A generant has one, and the standby interval runs from integration to the last
  shot — *the same problem [A39](A39_store_trade.md) recorded against gas and A53 against a held
  spring.* **The pyrotechnic version does not fix the standby problem; it changes which specialist
  owns it.**
- **Hazard classification** for twelve units in one magazine, including sympathetic initiation.
- **A fired generator cannot be tested before flight.** A spring could have been proof-loaded.
  This is a genuine loss against A53's design and it is the one place the spring was better.
- **The zonal cooling model assumes the sink reaches equilibrium with the whole charge inside a
  ~30 ms discharge, and nothing here establishes that it does.** If it does not, the gas arrives
  hotter than 473 K and band 6's verdict is provisional.

### Provenance

**Model output.** The gas generator is named as a **technology class** — solid-propellant
automotive restraint inflators — with published ranges declared at the point of use, as
[A39](A39_store_trade.md) declared its gas model and [A64](A64_pulse_store_technology.md) its
capacitors. **No product, supplier or organisation is named.** The expansion is
`precharged.work()`, unmodified. The housing allowance is a **declared guess with no derivation**,
carried from A53 at 0.12 kg so the two runs are directly comparable, and it is the largest
assumption in the run after the cooling model.

**Nothing has been built or fired. E4 says what it has always said.**
