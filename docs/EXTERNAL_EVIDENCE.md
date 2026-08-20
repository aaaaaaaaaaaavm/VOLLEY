# What the outside world can close, and what it cannot

**Opened 2026-08-20.** Until this date **every number in this repository came from inside it** — its
own scripts, its own run sheets, and handbook values declared at the point of use. **A10 records the
consequence in its own words**: the bank ESR bracket came from distributor listings because
*"eaton.com is unreachable from this environment; that limitation is recorded rather than worked
around."*

**That limitation lifted.** This file is the survey: **which live entries an external source can
settle, which it can only inform, and which it cannot touch at all.**

**It is a map, not evidence.** Anything acted on gets a banded run and a `NEEDS SOURCE` line
retired, the way [A64](../validation/A64_pulse_store_technology.md) did.

---

## Closed by it, already

### P86 — the trim stage's pulse store

**[A54](../validation/A54_pulse_chain.md) priced the store at 23.44–37.36 kg and named the gap as
`NEEDS SOURCE`** rather than guessing: *specific energy and ESR × C of a film or pulse capacitor.*

**Published pulsed-power literature gives millisecond-discharge capacitor energy densities of
1.9–2.68 J/cm³** at roughly unit density, in metallised polypropylene with extended-foil or bifilar
electrodes for very low ESR and ESL.

**[A64](../validation/A64_pulse_store_technology.md), six of six: the store is ~70 g**, 522× lighter,
at 400 kW/kg against the 23.20 required. **P86 closed and ADR-033's falsifier 1 does not fire.**

> **A54 was correct in every calculation and wrong in its scope.** It priced an EDLC because that
> was **the only store technology in this repository.** *The lesson generalises, and it is why this
> file exists.*

---

## Could be closed or materially moved

| Entry | What is needed | Why it is gettable |
|---|---|---|
| **P26** — the bank cannot source the shot on purchasable cells | Current EDLC cell data: ESR × C for modern high-power cells | **A10's whole bracket came from distributor listings it could not verify against the manufacturer.** If the product range has moved, the **68 mΩ** ceiling may now be reachable, and **the largest live defect Gen5 carries** changes |
| **E5** — no host propellant or control authority figure exists | Published hosted-payload interface data for a spent-stage platform | **[A20](../validation/A20_reachable_envelope.md) is parametric in exactly this one number** and says so. A single published Δv budget turns a sweep into a result |
| **E30 / A47** — the reliability the design must hit is unmeasured | Flight reliability data for canisterised dispensers | **A47 computes what *r* must be — 0.99326 — and cannot say what *r* is.** Published deployment counts and failure records would give the comparator a real number instead of an assumed one |
| **P44** — separation hardware outweighs a femtosat | ChipSat and femtosat deployer masses actually flown | The claim is a scaling argument with no flown datapoint under it |
| **P45 / A25** — the flywheel is at mass parity, not a saving | Reaction-wheel and flywheel-store specific energy from flown units | **A25's 1.1 kg band-4 failure is owned by one unsourced number**, and it says so |
| **P57** — the voice-coil deployer | Marked *"needs institutional access"* in `GEN6_CLOSURE.md` | May be a literature question rather than an access one |
| **A21 comparators** — spring dispenser performance | Published dispenser specifications | A21-R already uses one published figure; the comparison would be firmer with more |

---

## Informed but not closed

**These have a literature, and the literature does not answer this machine's question.**

### Water and steam propulsion — checked 2026-08-20

**Water propulsion is flight-proven at CubeSat scale.** A water resistojet has flown on a 6U
CubeSat in deep space, performing three ΔV and eleven trajectory-correction manoeuvres at **91 s
specific impulse on under 14 W**, with 1.2 kg of water in 2U. A water **electrolysis** thruster flew
in 2021 and had accumulated **408 firings** by 2023, and a 20 W electrolysis thruster has been
demonstrated at **1.25 mN and 185 s**.

> **None of it transfers.** Every flown system is a **thruster**, where specific impulse is the
> figure of merit. **A gun is sized by pressure-volume work released in milliseconds, and Isp says
> nothing about it.**
>
> **What the literature does establish is that storing and vaporising water on a small spacecraft is
> flown rather than speculative** — which is why
> [PII-21](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/PII-21_water_working_fluids.md)
> stopped steam on **bore temperature and tube mass**, not on feasibility.

---

## Cannot be closed by it

**These need hardware, and no amount of reading substitutes.**

| | |
|---|---|
| **P67** — the seal friction | **Searched 2026-08-20 and it is not there.** The literature confirms the component class — spring-energised graphite-filled PTFE — and confirms that **friction is determined empirically**, with the standard relation carrying an empirical factor *"difficult to obtain unless evaluated on empirical lines."* **There is no published coefficient that answers a specific bore, seal, surface, pressure and temperature.** [A61](../validation/A61_seal_class.md) produced a **requirement — 17.8 N** — and a requirement is what a bench test is measured against |
| **P88** — the seal cannot absorb its own friction | Same. The conduction path out of a seal is a design, not a lookup |
| **P89** — the seal specification | The class ranges A61 used are handbook and stay `NEEDS SOURCE` until measured |
| **E4** — nothing built, fired or measured | **The whole point.** No external source changes the category of this project's evidence |

> **P67 is the sharpest case for why this file has a third section.** Six entries depend on it, it
> now has a number to be measured against, and **the search returned exactly what a careful reader
> would expect: the method, not the answer.**

---

## How this file is used

**Nothing here is evidence.** A row moves out of the middle section by being run: bands declared
first, the source named at the point of use as a **technology class rather than a product**, and
the `NEEDS SOURCE` line retired in the run sheet that carried it.

**No organisation, supplier or individual is named anywhere in this repository**, and a published
performance range for a component class is not an exception to that — it is how A39 declared its gas
model and how A64 declared its capacitors.
