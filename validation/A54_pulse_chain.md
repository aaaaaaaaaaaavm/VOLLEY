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

---

## Result

**RUN 2026-08-19. One of eight bands passes. ADR-033's first falsifier has fired, and it fired
through the band that was predicted to survive.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A55 within 0.1 % | 136.59 J, 28 606 W, 144.01 mm | **PASS** |
| **2** | peak power ≤ 50 % of the deleted chain | **93.3 %** | **FAIL** |
| **3** | EDLC store ≤ the section it feeds | **23.44–37.36 kg against 1.233 kg** | **FAIL, 19–30×** |
| **4** | required specific power ≤ 4.72 kW/kg | **23.20 kW/kg, 4.92×** | **FAIL** |
| **5** | some sheet current gives ≤ 2.0 kg | **none** | **FAIL** |
| **6** | added mass per satellite ≤ 2.0 kg | **2.4313 kg** | **FAIL** |
| **7** | store holds ≤ 10× the correction energy | **723× to 1152×** | **FAIL** |
| 8 | section and store against sheet current | minimum **10.755 kg** at 20 kA/m | **REPORT** |

### ADR-033 said the current would decide it, and the current decides it

| | The chain ADR-032 deleted | **The trim stage that replaced it** |
|---|---:|---:|
| Peak power | 30 674 W | **28 606 W — 93.3 %** |
| Peak current at the 96 V bus | 319.5 A | **298.0 A — 93.3 %** |
| Energy per shot | 2782 J | **136.6 J — 4.9 %** |

**The energy fell by twenty times and the current fell by seven percent.** That is the whole
result, and ADR-033 wrote it down before it was measured: *"pulse hardware scales with current,
not energy."*

**ADR-032 deleted a pulse chain and ADR-033 asked for 93 % of it back.**

### The store is power-limited by three orders of magnitude

**Sized so its ESR dissipates at most 10 % of the delivered energy, an EDLC bank needs
≤ 32.2 mΩ.** [A10](A10_bank_esr.md)'s bracket of ESR × C then fixes the capacitance at
**21.4 to 34.2 F**, which is **3.6 to 5.7 of the 6.50 kg strings** `mass_properties.py` carries.

| | |
|---|---:|
| Store mass | **23.44 to 37.36 kg** |
| Against the section it feeds | **19.0× to 30.3×** |
| Energy it would hold | **98.7 to 157.3 kJ** |
| For a correction of | **136.6 J** |
| Ratio | **723× to 1152×** |

**The bank is sized entirely by the current it must source and holds a thousand times the energy
the job needs.** Specific *energy* is the wrong figure of merit for this store, which is band 7,
and it failed by three orders of magnitude.

**And every one of those masses is a lower bound.** The switch and the conductors are not priced
and no figure for either exists in this repository.

### There is no sheet current that rescues it

**Peak power scales with sheet current and section length scales inversely**, so the trade has a
minimum. **The minimum is 10.755 kg**, at 20 kA/m, on the optimistic end of A10's bracket —
**5.4× the 2.0 kg band, and 8.7× on the pessimistic end.**

| Sheet current | Section | Store | **Total** |
|---:|---:|---:|---:|
| 15 kA/m | 864 mm, 7.40 kg | 3.91–6.23 kg | **11.30–13.62 kg** |
| **20 kA/m** | 648 mm, 5.55 kg | 5.21–8.30 kg | **10.76–13.85 kg** |
| 25 kA/m | 519 mm, 4.44 kg | 6.51–10.38 kg | **10.95–14.82 kg** |
| 90 kA/m *(A1's, as built)* | 144 mm, 1.23 kg | 23.44–37.36 kg | **24.67–38.60 kg** |

**The curve is flat near its minimum and the minimum is an order of magnitude too high.** Lowering
the sheet current does not buy an affordable stage; it trades a heavy store for a heavy section.

**Added mass per satellite at the minimum is 2.4313 kg**, which **re-crosses the one
kill-criterion numerator Gen6 currently passes.**

### The prediction, and the one that mattered was wrong

**Recorded before the run: bands 2, 3, 4 and 7 fail, and band 5 passes** — *"because the trade is a
clean 1/x against x and those have minima."*

**The trade does have a minimum. The minimum is 10.755 kg.** The reasoning was right and the
conclusion drawn from it was wrong, because having a minimum says nothing about where it is.

## What this does and does not settle

**It does not prove the trim stage is impossible. It proves it cannot be fed by the only store
technology this repository has data for**, and it converts an unbounded worry into a single
checkable number:

> **Any store that fits inside the 1.2328 kg section must deliver 23.20 kW/kg and 110.8 J/kg.**
> **Gen5's own bank achieves 4.72 kW/kg.** *That is 4.92× on the axis that binds, and specific
> energy is not the constraint at all.*

**Film and pulse capacitors trade energy density for exactly this**, and **no vendor figure for
either is in the record** — which is why band 4 is stated as a required specific power rather than
as a comparison this run could not make honestly. *NEEDS SOURCE: specific power of a film or pulse
capacitor bank at a 4.77 ms discharge.*

**A higher bus voltage is the other escape and is not sized here.** Current falls as 1/V for the
same power, and the ESR budget rises as V², so a 300 V bus would relax the capacitance requirement
by about ten times. **`sizing.py` declares 96 V and nothing in this project has examined another.**

## The decision this forces, which is not this run's to take

**Band 5's declared FAIL text says ADR-033 reverses.** *I declared that before the run and it is
recorded here rather than quietly dropped.* **But reversing it requires choosing what replaces it,
and that is a design decision rather than an analysis result**, because deleting the trim stage
deletes the commanded-velocity claim the product is sold on — Gen6's shot disperses at **3.980 %
open-loop** with nothing correcting it.

**Three routes exist and A54 cannot choose between them:**

| | | |
|---|---|---|
| **Find the store** | a technology at **23.2 kW/kg**, or a higher bus voltage | Neither is in the record. **This is a sourcing question, not an analysis one** |
| **Shorten the stroke** | dispersion tracks friction work, and friction work tracks stroke | **[A49](A49_design_surface.md)'s surface is already published** and [A55](A55_trim_authority.md) band 9 gives the authority at every friction share. *This is the route that needs no new data* |
| **Withdraw the trim stage** | accept 3.980 % open-loop | **The commanded-velocity claim goes with it**, and that is what distinguishes VOLLEY from a spring |

**And [P67](../OPEN_PROBLEMS.md) still governs all three.** The dispersion that sets the authority
that sizes the store is **98.7 % a seal coefficient measured on nothing.** *A bench measurement
below a 20 % friction share moves every number on this page.*

**Recorded as P86.**

## What this run did not do

- **It did not price the switch or the conductors.** Every store mass here is a lower bound.
- **It did not evaluate film, pulse or electrolytic capacitors**, or any bus voltage but 96 V.
- **It assumed a 10 % ESR loss budget**, declared before the run. A looser budget scales the
  capacitance, and therefore the mass, in proportion.
- **E4 stands.** Nothing here is measured.
