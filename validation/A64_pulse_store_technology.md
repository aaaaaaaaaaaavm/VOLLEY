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
