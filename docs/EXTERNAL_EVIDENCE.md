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

## A second sourcing map: ground vehicle engineering

**Added 2026-08-20.** Everything above looks to spaceflight literature. **This section looks
sideways instead** — at automotive and motorcycle engineering, where several of VOLLEY's live
entries describe components that road vehicles have built in tens of millions of units.

**The transfer is not free and the section says where it breaks.** Every vehicle device below is
**lubricated, cyclic and atmospheric**. VOLLEY is **dry, in vacuum, and fires twelve times ever.**
That inversion cuts both ways: it makes wear irrelevant, and it makes **one-shot devices far more
attractive here than they are in a car.**

| Entry | Vehicle technology class | What it would settle | What breaks in the transfer |
|---|---|---|---|
| **P67 / P88 / P89** — seal friction, unmeasured | **Telescopic fork and damper rod seals** — a sliding rod seal engineered against *breakaway friction* as its primary figure of merit, in hard-anodised aluminium bores | [A61](../validation/A61_seal_class.md) specified **17.8 N — 4.00 % of the pressure force.** A component class whose whole design brief is minimising exactly that number is the closest existing analogue to VOLLEY's requirement | **Fork seals run wet.** Their friction figure is an oil-film figure. VOLLEY runs dry at −35 °C, and [A61's own note](../validation/A61_seal_class.md) is that the empirical factor is *"difficult to obtain unless evaluated on empirical lines"* |
| **P81** — the backup ejector cannot clear the tube | **Pyrotechnic gas generators** — an automotive restraint inflator produces **0.5 to 0.9 mol** of gas from **20 to 100 g** of solid generant in roughly **30 ms**, filling 60 L | [A53](../validation/A53_backup_ejector.md) failed band 7 because **a spring stores 4.5 J and clearing the tube costs 667.2 J.** A device in this class releases energy of a wholly different order, and it is **one-shot — which the carriage already is.** [A65](../validation/A65_pyrotechnic_ejector.md) tests it | **Total gas temperature is 1000 to 1400 K** and [ADR-035](adr/035-drive-tube-material.md) set a **473 K** tube ceiling. The same ceiling foreclosed steam in [A63](../validation/A63_steam_design_point.md). Pyrotechnics also carry a **range-safety and handling regime this repository has never priced** |
| **P86** — the trim stage's pulse store | **Traction-inverter DC-link capacitors** and **capacitor-discharge ignition** — the same metallised-film construction, sized for millisecond discharge into an inductive load | **Already closed**, by [A64](../validation/A64_pulse_store_technology.md), on pulsed-power literature. The vehicle route is the *second* independent path to the same answer, and it is the one built in volume | Nothing material. **This row is here because it is the worked example**: the store looked impossible at 23–37 kg only because an EDLC was the sole technology in the record |
| **[ADR-033](adr/033-gen6-trim-stage.md) falsifier 3** — no velocity sensor exists | **Variable-reluctance wheel-speed and resolver sensing** — a passive, radiation-tolerant, non-contacting measurement of a moving steel feature | [A55](../validation/A55_trim_authority.md) records that *"there is still no velocity sensor in any file"*, and the loop has **1.4 ms** to measure in. This class needs no optics and no window | A wheel sensor measures a **rotating** target at kHz. VOLLEY needs a **linear** velocity to a tolerance A44's dispersion sets, in a single pass, once |
| **E30 / A47** — twelve-cycle series mechanisms forfeit the manifest | **Sequential gearbox shift drums and detent escapements** — a single-actuator indexer moving a fixed sequence of positions under load | [A47](../validation/A47_gen6_fmea.md) counts the escapement among the **shared elements that forfeit everything remaining.** A drum indexer is the same problem solved for a component with a very large field population | Field reliability for a gearbox is a **warranty** figure, not a mission figure, and it is measured on units that are **serviced.** It cannot be read across to twelve shots with no maintenance |
| **P78** — the chamber-to-tube gas interface | **Internal-floating-piston dampers** — a gas charge separated from the working volume by a free piston with a single dynamic seal | The gas store and the bore meet somewhere, and **no file draws that junction.** This class is the standard answer to the same geometry | It is a *damper*, sized for cyclic low-rate motion. **The pressure is comparable; the rate is not** |

> **The strongest row is P81.** It is the only one that could resurrect a defect **[A53](../validation/A53_backup_ejector.md) closed as architectural**, and [A47](../validation/A47_gen6_fmea.md) priced that defect at **+2.27 satellites delivered against +0.37 for the entire Gen5 → Gen6 change — six times more.** That is why it was run rather than listed.

> **The weakest is E30.** *Automotive reliability data is abundant and is the wrong kind of number.* A warranty rate on a serviced, lubricated, million-cycle component says nothing about twelve unserviced shots in vacuum, and **quoting it would be worse than the current honest blank.**

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
