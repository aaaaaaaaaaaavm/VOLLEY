# A64 — the pulse store, priced against pulsed-power capacitor technology

**Bands declared 2026-08-20, before `analysis/pulse_store_tech.py` existed.**
Verify with `git show --stat <this commit> -- analysis/pulse_store_tech.py`, which must return nothing.

---

## Why this run exists

**[A54](A54_pulse_chain.md) priced the trim store as an EDLC bank at 23.44–37.36 kg and left one
route open**, stated as a required number rather than a comparison it could not honestly make:

> *"Any store that fits inside the 1.2328 kg section must deliver **23.20 kW/kg**. Film and pulse
> capacitors trade energy density for exactly this, and **no vendor figure for either is in the
> record** — which is why band 4 is stated as a required specific power. NEEDS SOURCE: specific
> energy and ESR × C of a film or pulse capacitor bank."*

**That source now exists.** Published pulsed-power literature gives **millisecond-discharge
capacitor energy densities of 1.9 to 2.68 J/cm³**, at roughly unit density — **2000 to 2680 J/kg** —
and metallised polypropylene construction with **extended-foil or bifilar electrodes for very low
ESR and ESL**, developed for exactly this duty.

**The correction A54 carries matters here.** [A54's dated correction block](A54_pulse_chain.md)
established that the store reduces to

> **m ≥ ½ · (ESR × C) · P / (f · specific energy)**

**with the bus voltage cancelling exactly.** So a technology change enters through only two terms:
**ESR × C** and **specific energy** — and a film capacitor moves the first by orders of magnitude.

## What that does to the shape of the problem

**An EDLC is power-limited by three orders of magnitude** — A54 band 7 found the bank would hold
**723× to 1152×** the energy the correction needs, purely to source the current.

**A film capacitor's ESR × C is microseconds rather than seconds.** If that holds, the power term
collapses and **the store becomes energy-limited** — sized by the 136.59 J it must deliver, at a
specific energy that is now sourced.

**This run tests whether that is true and what it weighs.**

## Declared before the run

| | | |
|---|---|---|
| Requirement | **136.59 J at 28 606 W**, from [A55](A55_trim_authority.md) via A54 | imported |
| **Pulsed-power capacitor specific energy** | **2000 – 2680 J/kg** | **published pulsed-power literature.** Named as a technology class, no product or supplier |
| **ESR × C, film** | **swept 10⁻⁶ to 10⁻³ s** | *conservative: typical metallised polypropylene is nearer 10⁻⁷* |
| ESR × C, EDLC | **0.69 – 1.10 s** | [A10](A10_bank_esr.md)'s bracket, for the comparison |
| Loss budget | **10 %** | as A54 declared it |
| Target | the **1.2328 kg** section it feeds | A55 |

## The prediction, recorded before the run

**I expect every band to pass**, which is unusual enough to say plainly. **The power constraint
should collapse by six orders of magnitude and leave the store energy-limited at well under a
tenth of the section it feeds.**

**If that holds, P86 closes on a sourcing answer rather than a design change** — and the reason
A54 failed was that it priced the only technology this repository happened to have data for.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The closed form reproduces A54's EDLC result — **23.44–37.36 kg** — within 1 % | This run is not the same model as A54 and nothing below is comparable |
| **2** | At the worst swept ESR × C, the **power-driven** stored energy is **≤ 10×** the 136.59 J delivered | The store stays power-limited even on film, and the technology change buys nothing |
| **3** | Store mass at the worst corner — 10⁻³ s, 2000 J/kg — is **≤ the 1.2328 kg section it feeds** | **A54's falsifier stands and P86 does not close on technology** |
| **4** | Store mass at the **typical** corner is **≤ 0.25 kg** | The store is a significant fraction of the section and the trade against a per-cell ejector must be re-run |
| **5** | Added mass per satellite, section plus store, stays **≤ 2.0 kg** | The design re-crosses the one kill-criterion numerator Gen6 passes |
| **6** | The **specific power** achieved exceeds A54's required **23.20 kW/kg** | The store cannot source the current whatever its energy density, and band 3 passed for the wrong reason |
| **7** | **REPORT, no pass/fail.** Store mass against ESR × C and specific energy, so a datasheet can be read off it | — |

## What this run will not do

- **It does not name a product, a series or a supplier**, only a technology class and a published
  performance range.
- **It does not price the switch or the conductors.** A54 named both as unpriced and they remain so,
  **so every mass here is still a lower bound.**
- **It does not model derating, voltage reversal, or life.** Twelve shots is a trivial duty for a
  pulse capacitor, and that is an argument rather than a calculation.
- **It does not re-open the trim stage's necessity.** [A61](A61_seal_class.md) found a specified
  seal may delete it entirely, and **that remains the cheaper answer.**
- **E4 stands.** Nothing here is measured.

---

## Result

**RUN 2026-08-20. Six of six bands pass, and the prediction held exactly. [P86](../OPEN_PROBLEMS.md)
closes on a sourcing answer.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A54's EDLC 23.44–37.36 kg | **23.44–37.36 kg** | **PASS** |
| 2 | power-driven energy ≤ 10× the delivered | **143.03 J against 136.59** | **PASS** |
| 3 | store ≤ the 1.2328 kg section | **0.0715 kg** | **PASS** |
| 4 | typical corner ≤ 0.25 kg | **0.0683 kg** | **PASS** |
| 5 | added mass per satellite ≤ 2.0 kg | **1.4047 kg** | **PASS** |
| 6 | specific power ≥ 23.20 kW/kg | **400.0 kW/kg** | **PASS** |

### The constraint flips, exactly as A54's own algebra said it would

| | EDLC | **Pulsed-power capacitor** |
|---|---:|---:|
| ESR × C | 0.69 – 1.10 s | **10⁻⁶ – 10⁻³ s**, swept conservatively |
| Energy the store must hold to *source the current* | **98.7 – 157.3 kJ** | **0.14 – 143 J** |
| Binds on | **power, by 723×** | **energy**, at every corner but the worst |
| **Store mass** | **23.44 – 37.36 kg** | **0.051 – 0.072 kg** |
| Specific power achieved | 4.72 kW/kg | **400 – 561 kW/kg** |

> **522× lighter at the worst corner**, and **17× the specific power A54 said was required.**
>
> **The store is 51 to 72 grams** — against the **1.2328 kg** section it feeds, and against **23 to
> 37 kg** on the only technology this repository happened to have data for.

**Band 2 is the one that shows the mechanism.** At an EDLC's ESR × C the bank must hold **723×** the
energy it delivers, purely to source the current. **At a film capacitor's it holds 1.00×** — the
power term collapses below the energy term and stops mattering at all.

**Band 6 checks that band 3 did not pass for the wrong reason.** It did not: the store sources
**400 kW/kg** against A54's required 23.20.

### Why A54 failed, stated plainly

**A54 was correct in every calculation and wrong in its scope.** It priced the store as an EDLC
bank because **A10's ESR × C bracket and `mass_properties.py`'s 6.50 kg string were the only store
data in the repository** — and it said so, flagging the alternative as **NEEDS SOURCE** rather than
guessing.

> **The defect was not in the analysis. It was that the repository had one technology in it.**
>
> *A54's own correction block had already derived the form that makes this a two-term question —
> ESR × C and specific energy — and named both as unsourced. This run sources them.*

## Consequences

- **P86 closes.** The trim store is **~70 g**, not 23–37 kg.
- **[ADR-033](../docs/adr/033-gen6-trim-stage.md)'s falsifier 1 is answered and does not fire.** The
  store weighs **6 %** of the 1.2328 kg section it feeds, not more than it.
- **Added mass per satellite is 1.4047 kg** against an unmoved 2.0 kg threshold. **The design does
  not re-cross the numerator it passes.**
- **[A61](A61_seal_class.md)'s route is still cheaper.** A specified seal may **delete** the trim
  stage rather than feed it, and that remains the better answer — but **it is no longer the only
  one.**

## What this run did not do

- **It names no product, series or supplier**, only a technology class and a published range.
- **The switch and the conductors are still unpriced** — A54 named both and they remain so, so
  **every mass here is a lower bound.**
- **Derating, voltage reversal and life are not modelled.** Twelve shots is a trivial duty for a
  pulse capacitor, and that is an argument rather than a calculation.
- **E4 stands.** Nothing here is measured.
