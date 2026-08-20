# A61 — what the design requires of a seal, which it has never said

**Bands declared 2026-08-20, before `analysis/seal_class.py` existed.**
Verify with `git show --stat <this commit> -- analysis/seal_class.py`, which must return nothing.

---

## Why this run exists

**No seal exists in this repository.** [A39](A39_store_trade.md) states it designs *"no cylinder,
valve, seal or latch"*; [A40](A40_blowdown_transient.md) that it does not model one; **A41 declared
an 83.4 N friction *allowance* and every number since has been computed against it.**

**That allowance is 18.7 % of the piston's pressure force.** Expressed that way it is recognisably
an *elastomer* figure — **so the project has been implicitly assuming the worst common seal class
without ever choosing it**, and four analyses now rest on that choice:

| | |
|---|---|
| **[A55](A55_trim_authority.md)** | dispersion **3.980 %**, of which **98.7 %** is this seal |
| **[A54](A54_pulse_chain.md)** | a trim store of **23–37 kg**, sized to correct that dispersion |
| **[A58](A58_chamber_thermal.md)** | **667.2 J** into the seal per shot, band 5 failed across the range |
| **[A49](A49_design_surface.md)** | friction at **28.39 %** of shot work, band 6 failed — **P78** |

## What this run is, and what it deliberately is not

**It is not a comparison of seal products, and it does not claim any class achieves any number.**
Friction fractions for component classes are handbook ranges, no better sourced than A39's gas
model, and **they do not replace [P67](../OPEN_PROBLEMS.md).**

**It inverts the question instead.** Rather than asking *what would this seal give*, it asks:

> **What is the loosest seal the design can tolerate, for each downstream requirement to be met?**

**That produces a specification** — a maximum friction, in a unit a supplier quotes — where the
repository currently has an allowance nobody chose. **The mapping is computed from models already
in the record; only the input is assumed.**

## Declared before the run

| | |
|---|---|
| Friction parameterised as a **fraction of the piston pressure force**, p₀·A = **445.9 N** | the unit seal data is quoted in |
| Swept **1 % to 30 %** | spanning every common class |
| **Filled PTFE glide ring: 2–10 %** · **elastomer O-ring: 10–25 %** | **handbook ranges. NEEDS SOURCE, and stated as such** |
| Dispersion, trim geometry, store model | imported from `gen6_dispersion`, `trim_stage`, `pulse_chain` — not restated |
| Bore alternatives | **15.805 mm** as drawn, **16.000 mm** as an ISO 6432 stock size |

## The prediction, recorded before the run

**I expect band 3 to pass and band 5 to fail** — that a good seal makes the trim stage
*unnecessary* rather than affordable, which resolves **P86** by deleting its requirement, while the
store itself stays out of reach because it is sized by peak power and friction does not touch it.

**I expect band 6 to find the thermal case binds first** — that the seal must be better for P88
than for the trim stage, because 667 J into a few grams is a harsher constraint than 0.323 m/s of
authority.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | At **83.4 N** the chain reproduces A55's **3.980 %** and A54's store within 1 % | This run is not standing on A55 and A54, and nothing below is comparable |
| **2** | A41's allowance, expressed as a fraction of pressure force, is **reported** and falls inside a named class range | The allowance cannot be placed against any seal anyone sells, and the parameterisation is wrong |
| **3** | **There is a friction fraction at which open-loop dispersion needs less authority than A48's original ±0.323 m/s** | **No seal makes the trim stage unnecessary**, and P86 must be solved rather than deleted |
| **4** | **There is a friction fraction at which a 2 g seal stays within 50 K** — A58 band 5's threshold | **P88 cannot be closed by seal choice** and needs a conduction path regardless |
| **5** | **There is a friction fraction at which section + store ≤ 2.0 kg** | The trim store stays out of reach at any seal, confirming it is power-limited rather than friction-limited |
| **6** | The friction required by band 4 is **looser** than the friction required by band 3 | **The thermal case binds the seal specification, not the control case** — which changes what P67 has to measure |
| **7** | Moving to the **16.000 mm** stock bore changes the required friction fraction by **≤ 5 %** | The design cannot use a standard bore without re-deriving its seal specification |
| **8** | Across the swept range the **two velocity numerators stay within 25 %** of each other | Friction is eating so much of the shot that the zero-friction figure is no longer a useful reference |
| **9** | **REPORT, no pass/fail.** The specification: maximum friction, in N and as a fraction of p₀·A, for each downstream requirement | — |

## What this run will not do

- **It does not select a product, a compound or a supplier**, and names no organisation.
- **It does not measure anything.** The class ranges are handbook and the output is a requirement,
  not a validation. **P67 still has to be run**, and [A58](A58_chamber_thermal.md)/**P88** showed it
  is a harder test than previously described — at **−35.2 °C**, on a seal dissipating **667.2 J per
  stroke**, over **8.0 m**.
- **It does not model the seal's friction changing with its own temperature**, which A58 named and
  left uncomputed, or with pressure, velocity or wear across twelve shots.
- **It does not re-run A44, A48, A54 or A58.** It reports what each would return.
- **E4 stands.** Nothing here is measured.
