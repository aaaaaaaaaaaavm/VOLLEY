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

---

## Result

**RUN 2026-08-20. Six of nine bands pass. The design has been sized against a seal 4.7× looser
than it needs, and specifying one closes two open defects — but not the third.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A55 and A54 at 83.4 N | **3.9798 %**, min **10.54 kg** | **PASS** |
| 2 | A41's allowance falls in a named class | **18.71 % — elastomer O-ring** | **PASS** |
| 3 | some friction makes the trim stage unnecessary | **≤ 5.00 % = 22.3 N** | **PASS** |
| 4 | some friction keeps a 2 g seal within 50 K | **≤ 4.00 % = 17.8 N** | **PASS** |
| **5** | some friction gives section + store ≤ 2.0 kg | **none in 1–30 %** | **FAIL** |
| **6** | thermal requirement looser than control | **4.00 % against 5.00 %** | **FAIL** |
| 7 | the 16.000 mm stock bore shifts it ≤ 5 % | **0.00 %** | **PASS** |
| **8** | velocity numerators within 25 % | **26.23 %** at the 30 % end | **FAIL** |

### The diagnosis, confirmed

**A41's 83.4 N allowance is 18.71 % of the piston's pressure force, and that sits inside the
elastomer O-ring range.** Band 2 was a check on the parameterisation and it landed.

> **The project has been sized, since A41, against the worst common seal class — and nobody ever
> chose it.** A55's dispersion, A54's store, A58's seal heating and A49's band 6 failure all
> descend from a number declared as an allowance.

### The specification, which is what this run was for

| Requirement | Maximum friction | |
|---|---:|---|
| **A 2 g seal stays within 50 K** — [A58](A58_chamber_thermal.md) band 5, **P88** | **4.00 %** | **17.8 N** |
| The trim stage becomes unnecessary — below A48's ±0.323 m/s | 5.00 % | 22.3 N |
| Section + store ≤ 2.0 kg — [A54](A54_pulse_chain.md) band 5, **P86** | **not reachable** | — |

> ### **The seal specification is 4.00 % of p₀·A — 17.8 N — and the thermal case sets it**
>
> **Band 6 failed and that is the finding.** The seal must be better for **P88** than for the trim
> stage: **4.00 % against 5.00 %.** *The binding requirement on this component is not the control
> loop everyone has been discussing; it is that the seal must survive its own friction.*
>
> **A41's allowance is 4.7× looser than the specification.**

**The requirement sits inside a filled-PTFE glide ring's handbook range of 2–10 %, but not at its
loose end.** *This run does not claim any class achieves 4.00 %, and it is not a substitute for
[P67](../OPEN_PROBLEMS.md) — which now has a number to be measured against.*

### What a specified seal would close, and what it would not

**At 5.00 % — 22.3 N — the whole chain moves:**

| | A41's allowance, 18.71 % | **At 5.00 %** |
|---|---:|---:|
| Friction work per shot | 667.2 J | **178.4 J** |
| Friction share of shot work | 28.39 % | **7.59 %** |
| **3σ dispersion** | **3.9798 %** | **0.9051 %** |
| Authority needed | 1.1543 m/s | **0.2982 m/s — below A48's 0.323** |
| Section | 144.0 mm | **41.6 mm** |
| 2 g seal rise per shot | 222.4 K | **59.5 K** |

**P88 closes at 4.00 %. The trim stage becomes unnecessary at 5.00 %, which resolves P86 by
deleting its requirement rather than meeting it.**

**And band 5 says the store itself stays out of reach at any seal** — **4.23 kg even at 1 %
friction.** *That confirms A54's correction: the store is power-limited, and peak power is set by
sheet current, which friction does not touch. **Seal choice cannot solve P86; it can only make it
irrelevant.***

### The stock bore is free

**Band 7 returned 0.00 %.** Moving from the drawn **15.805 mm** to the **16.000 mm** ISO 6432 stock
bore changes the required friction fraction not at all, because the fraction is *of* the pressure
force and the acceleration cap fixes that force whatever the area. **The charge pressure moves
22.73 → 22.18 bar and nothing else does.**

### Band 8 failed, and it bounds this run rather than the design

**The two velocity numerators diverge by 26.23 % at the 30 % friction end.** Beyond roughly 28 %,
friction is eating so much of the shot that the zero-friction figure stops being a useful reference
and the sweep's far end should not be quoted. **A41's 18.71 % is inside the valid range; an
elastomer at the top of its class is not.**

## Consequences

- **P89 opens**: the seal specification is 17.8 N and `parameters.json` carries no seal at all.
- **P88 becomes closable by specification** rather than by adding a conduction path.
- **P86 becomes deletable** rather than solvable, if the specification is met.
- **P85 gains a cheap answer**: a stock 16 mm honed bore settles the bore, and matching the piston
  material removes A58's 10.79 µm.
- **Nothing is re-run here.** A44, A48, A54 and A58 all still carry A41's allowance.

## What this run did not settle

- **It measured nothing**, names no product, compound or supplier, and its class ranges are
  handbook. **P67 still has to be run** — at −35.2 °C, on a seal dissipating its own friction, over
  8.0 m, twelve times (**P88**).
- **It does not model friction changing with the seal's own temperature**, with velocity, with
  pressure, or with wear across twelve shots.
- **E4 stands.**
