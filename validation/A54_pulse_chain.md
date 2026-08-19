# A54 — weighing the pulse chain, which is ADR-033's own first falsifier

**Bands declared 2026-08-19, before `analysis/pulse_chain.py` existed.**
Verify with `git show --stat <this commit> -- analysis/pulse_chain.py`, which must return nothing.

---

## Why this run exists

**[P77](../OPEN_PROBLEMS.md), and [ADR-033](../docs/adr/033-gen6-trim-stage.md) named it as its own
falsifier 1 on the day it was adopted:**

> *"The pulse store weighs more than the 0.340 kg stage it feeds. The correction is 37.7 J at
> 28 kW — requirement **C3**, the energy arrives during the shot, which A35 prices at 26.35 kg and
> ADR-032 deleted. **At a fiftieth of Gen5's energy, but pulse hardware scales with current, not
> energy, and nothing has weighed it.** This is the falsifier most likely to fire, and it is being
> adopted before it is answered."*

**[A55](A55_trim_authority.md) has since resized the section**, so the bar has moved and the
requirement with it: **136.59 J at 28 606 W into a 1.2328 kg section**, not 37.7 J into 0.340 kg.

## The thing ADR-033 said would decide it

**ADR-032 deleted a pulse chain that peaked at 30.7 kW and 319.5 A** — `motor_results.json`,
`I_peak`, at the 96 V bus `sizing.py::capacitor_sizing` declares.

**A55's resized trim section asks for 28 606 W.** *That is the number this run turns on, and it
is not a fiftieth of anything.*

**The reason is in ADR-033's own sentence.** Force per metre is fixed by A2's depth-resolved
thrust constant and A1's sheet current, so a longer correction takes longer rather than harder —
the **energy** grows and the **current** does not. **A store is sized by the current.**

## What is being weighed

| | |
|---|---|
| **The energy store** | priced as an EDLC bank, from data this repository already carries |
| **The switch and the conductors** | **not priced.** Named as unpriced rather than guessed at — see below |

**The EDLC route is fully sourced and nothing in it is invented.**
[A10](A10_bank_esr.md) established that **ESR × C is roughly constant within a cell technology**,
and bracketed it at **0.69 to 1.10 s** from two Eaton cells thirty times apart in capacitance.
`analysis/mass_properties.py` carries one 32-cell string of 190 F — **5.94 F at 96 V — at
6.50 kg**, cells and busbars. **That is the anchor: a mass, a capacitance and an ESR bracket, all
already in the record.**

## The lever this run exists to find

**Peak power is proportional to sheet current and section length is inversely proportional to it.**
A lower sheet current makes the store smaller and the section longer, and **the section is only
1.80 % of an 8 m stroke**, so there is room to spend. **Somewhere there is a minimum, and nobody
has looked for it.**

## The prediction, recorded before the run

**I expect bands 2, 3, 4 and 7 to fail.** The peak power is 93 % of the chain ADR-032 deleted, an
EDLC store sized for that power will weigh tens of kilograms because scaling a bank down raises its
ESR exactly when the requirement needs it lower, and the bank will store hundreds of times the
energy the correction needs — because it is power-limited, not energy-limited.

**I expect band 5 to pass**: that a lower sheet current buys a store-plus-section under 2 kg,
because the trade is a clean 1/x against x and those have minima. **If band 5 fails, ADR-033
reverses**, and the trim stage goes back to the vault with the measurement that retired it.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The requirement reproduces [A55](A55_trim_authority.md) to within 0.1 % — **136.59 J, 28 606 W, 144.01 mm** | This run is not standing on A55 and nothing below is comparable |
| **2** | Peak power is **≤ 50 %** of the 30.7 kW chain ADR-032 deleted | **The trim stage asks for most of the pulse chain back**, which is what ADR-033's falsifier alleged |
| **3** | An EDLC store sized to source that power weighs **≤ the 1.2328 kg section it feeds** | **ADR-033 falsifier 1 fires as written** |
| **4** | The specific power required, at a mass equal to the section, is **≤ 4.72 kW/kg** — what Gen5's own bank achieves | The store is asked for something no bank in this project has ever demonstrated |
| **5** | **There is a sheet current at which section + store ≤ 2.0 kg** | **There is no operating point at which the trim stage is affordable, and ADR-033 reverses** |
| **6** | At that sheet current, added mass per satellite stays **≤ 2.0 kg** | The escape re-crosses the one kill-criterion numerator Gen6 passes |
| **7** | The sized store holds **≤ 10×** the energy the correction needs | The store is power-limited rather than energy-limited, and specific *energy* is the wrong figure of merit for it |
| **8** | **REPORT, no pass/fail.** Section mass and store mass against sheet current, with the minimum located | — |

## What this run will not do

- **It does not price the switch or the conductors.** A 300 A pulse switch and its busbars are real
  mass and **no figure for either exists in this repository.** They are additive to everything
  below, so **every store mass here is a lower bound.** *NEEDS SOURCE: pulse switch and conductor
  mass at 300 A.*
- **It does not evaluate film or electrolytic capacitors.** Their specific power would change the
  answer and **no vendor figure for either is in the record.** Band 4 is stated as a *required
  specific power* precisely so it can be checked against any datasheet without this run inventing
  one. *NEEDS SOURCE: specific power of a film capacitor bank at this pulse duration.*
- **It does not model the converter, the commutation, or the loop.** Gen6 still has no velocity
  sensor in any file.
- **It assumes the 96 V bus `sizing.py` declares.** A higher bus voltage lowers the current for the
  same power and is an escape this run reports but does not size.
- **E4 stands.** Nothing here is measured.
