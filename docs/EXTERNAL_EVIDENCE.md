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
| **E5** — no host propellant or control authority figure exists. **And [A13](../validation/A13_indexing_disturbance.md) band 5 passed on one anyway — [P94](../OPEN_PROBLEMS.md), 2026-08-20** | Published hosted-payload interface data for a spent-stage platform | **[A20](../validation/A20_reachable_envelope.md) is parametric in exactly this one number** and says so. A single published Δv budget turns a sweep into a result |
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

## The vault, checked the same way

**Added 2026-08-20.** [`VAULT.md`](VAULT.md) holds twenty-one parked entries. **The question asked
of each was not "is it good" but "did it stop on a number that came from inside this repository."**
That is the only kind of stop an outside source can move, and it is the lesson
[A64](../validation/A64_pulse_store_technology.md) taught at the cost of A54.

**Most of the vault fails that test immediately, and it is worth saying why in one line.** Nine
entries stopped on 2026-08-14 because [ADR-032](adr/032-gen6-stage-integrated-gas-store.md) deleted
the subsystem they improve — **no mover, no stator, no bank, no track.** *No literature resurrects an
optimisation of a part that no longer exists.* **PII-9** describes a different programme and
**PII-8** a different vehicle; a source cannot supply a host. **Those are stops by type, and they
stay shut.**

**Three entries survive the filter. One of them has a live route back into Gen6.**

### PII-19 — the passive secondary, and it is aimed at the wrong generation's problem

**PII-19 stopped by attribution, not refutation**: [A35](../validation/A35_constraint_ledger.md)
measured the mover it optimises at **11 % of dry mass**, so it was *"a careful, banded, correct
optimisation of the wrong term."* **That verdict was about Gen5's whole drive. Gen6 no longer has
one — but it has a 144.01 mm motor at the muzzle, and that motor has PII-19's exact problem.**

**[ADR-033](adr/033-gen6-trim-stage.md) brought magnets back to the moving part and listed the
cost itself:** *"**P34** — a payload carrying a magnetometer cannot fly in this magazine. **This
defect returns because the magnets do**"*, plus **E35**, plus a cradle that must now hold magnets in
alignment.

> **PII-19's whole proposition is a passive plate instead of magnets on the moving body.** Applied
> to a trim stage rather than a drive, it would **not** return P34, **not** return E35, and **not**
> ask the cradle to align a magnet set. *The entry was priced against a 9.445 kg sled where its gain
> was 11 %. Against a stage whose stated cost is a returning defect rather than a mass, the same
> idea is answering a different and better question.*

**And PII-19 carries the measurement that may kill its own comeback.** **A30** measured the
transverse edge factor at **0.0253** against the **0.55** it had been sized on — *a factor of 22* —
because the Russell–Norsworthy factor collapses for a secondary narrower than the pole pitch.
**`stator.pole_pitch` is 24 mm and any secondary that fits a 15.805 mm bore is narrower than that.**

**That is the run, and it is not written yet.** It is also why this belongs in a sourcing map rather
than in a decision: **the deciding number is already in the vault, measured, and it points the
unwelcome way.**

**A second PII-19 result transfers whether or not the plate does.** **A32 band 4** found segment
ripple *"intrinsic to a segmented long stator with a short secondary"*, and PII-19's own closing line
says it *"will be rediscovered by anyone who proposes one."* **A55's stage is a short stator crossed
in 1.4 ms by a short secondary, and neither A48 nor A55 models the entry transient A32 measured.**

### PII-14's flywheel — closed by external evidence, in the losing direction

**PII-14 split its flywheel out as an independent candidate against P26**, saying so in the file:
*"an energy store does not care what load it feeds… it is a Phase I candidate against P26 in its own
right."* **[P45](../OPEN_PROBLEMS.md) then found it at mass parity, owned by one unsourced number**,
and [A25](../validation/A25_flywheel_store.md) band 4 failed on it.

> **The external check settles it and the answer is no.** The question a flywheel was competing for
> is now Gen6's pulse store, and **A64 answered it at ~70 g on published pulsed-power capacitor
> data.** *A rotating machine, its bearings, its containment and its 7.15 N·m·s of stored angular
> momentum are not going to beat seventy grams of film capacitor* — and the angular momentum is a
> disturbance in a machine whose shot already dumps **3.28 N·m·s**.
>
> **This is the useful shape of a vault result: the entry is retired by a number, not left ajar.**

### PII-11's straightness arithmetic, which inverts on the way across

**PII-11 §5 argued the straightness requirement had been overstated** — *"a 3.3 m deployed track is
a looser straightness requirement than the machine already meets"* — because an ironless Halbach
airgap tolerates error at **1 mm** of clearance and costs thrust rather than running away.

**Gen6's 8.0 m tube is not an airgap. It is a bore with a sliding seal in it**, and a seal's job is
to *maintain* contact, so the same argument runs backwards: **the tolerance that made a deployed
track plausible does not exist here.** [A59](../validation/A59_tube_structure.md) already found the
tube needs **seven supports**, and **P67**, **P88** and **P89** all rest on a friction that bore
straightness and roundness directly set.

| What is needed | Why it is gettable |
|---|---|
| **Straightness and roundness tolerances for long honed and skived tube** in the bore class Gen6 uses | It is a **stock manufacturing specification**, published per metre of length, for exactly the sliding-seal duty A61 specified. **A61 already found a 16.000 mm ISO 6432 stock bore costs 0.00 %** on the seal specification — the sourcing route into this design is open and has been used once |

**This does not reopen PII-11.** It takes one paragraph of its arithmetic, notes that the sign flips,
and points at three live entries that inherit the consequence.

### What the vault check found that was not in the vault

**[P92](../OPEN_PROBLEMS.md).** Reading PII-19 against ADR-033 to see whether a passive secondary
fits meant reading how the present stator reaches its magnets — **and it reaches them through the
tube.** ADR-035 made that tube aluminium four days after ADR-033 placed the stator outside it, and
**nothing owns the interaction.**

> **That is the strongest argument for keeping a vault at all**, and it is not the one the vault was
> built on. **The entry did not come back. Reading it found a defect in what replaced it.**

---

## Guided separation and contact dynamics — the cluster this file was missing

**Added 2026-08-22**, after a sweep of the outside separation literature was reconciled against
the record. **It found the largest single gap in the Gen6 evidence, and it is not a number — it is a whole class of
model this repository does not have.**

### What the record has, and where it stops

| Run | What it models |
|---|---|
| [A23](../validation/A23_tipoff_release.md) | Tip-off rates against deployer classes. A comparison, not a mechanism |
| [A34](../validation/A34_cradle_restitution.md) | The payload rattling across its **cradle clearance**, Gen5 |
| [A38](../validation/A38_tipoff_at_gen6.md) | The same closed forms at the Gen6 point — corrected to ADR-034's stroke on 2026-08-22, **P102** |

**All three model the release interface. None models the guide.** Gen6 accelerates a payload along
**8.0 m** of bore and this repository has no contact state along it: no straightness, no roundness,
no local clearance, no force-line eccentricity, no payload centre-of-mass offset, and no lateral or
angular state carried through the stroke. **The chain that is modelled is chamber pressure → axial
force → exit velocity.** The chain that decides whether the product works is **contact state →
lateral impulse and torque → release pose and rate**, and it is absent.

### The nearest published neighbour, and it is closer than the electromagnetic literature

**"Design and Analysis of a High-Precision Separation Mechanism for On-Orbit Launch of
Micro-Spacecraft"**, *Aerospace Science and Technology*, 2026 — publisher record
`S1270963826018869`. **Located and checked 2026-08-22 from its abstract and indexing only.**

**Abstract- and indexing-level evidence only.** What two independent retrievals return
consistently:

- Launch-dynamics models of **several separation-mechanism configurations in ADAMS**, to find which
  configuration produces large launch disturbance and why. The **cylindrical** configuration
  performs best, and a **continuous-contact straight guide rail beats a gradient rail** at
  suppressing launch disturbance.
- Contact force and moment formulas derived analytically, then **parametric optimisation of
  guide-rail length and fit clearance**, reported as an **82.76 % improvement in launch attitude
  accuracy** at a **270 mm rail and 0.2 mm fit clearance**.
- A 3U-form-factor device in **7075 aluminium**, with **hard-anodised guide-rail surfaces coated
  with PTFE to reduce friction**.
- Post-launch **angular velocity** treated as the quantity that decides mission success.

> **The 270 mm and the 0.2 mm are that mechanism's answers and are not to be imported.** They are
> quoted here so that the *shape* of the result is on the record — **fit clearance has an optimum,
> not a minimum** — and because a number left unstated tends to get remembered as a
> recommendation. VOLLEY's bore is 15.805 mm over 8.0 m and shares nothing with a 270 mm rail but
> the physics.

> **Two of those land directly on Gen6.** The tribological pair is the one
> [ADR-035](adr/035-drive-tube-material.md) and [A61](../validation/A61_seal_class.md) chose —
> **hard-anodised aluminium against PTFE** — and the output quantity is the one
> [`KILL_CRITERIA.md`](KILL_CRITERIA.md) threat 4 is written in. *This is a guided ejection of a
> CubeSat-class body along an anodised aluminium rail, analysed for release attitude. It is the
> same physical problem.*

**It has not been read in full. ScienceDirect is blocked from this environment**, the same
limitation [P57](../OPEN_PROBLEMS.md) records for IEEE Xplore, and this entry is a **lead, not
evidence.** Nothing in this repository may cite a figure from it until it has been retrieved.

### What it can move, and what it cannot

| | |
|---|---|
| **[P67](../OPEN_PROBLEMS.md)'s framing** | **Friction is not separable from the geometry that produces it.** B-2 measures a force; the force is a property of a bore, a finish, a clearance and a seat. *The measurement stays first — this changes what it is a calibration point for, not whether to take it* |
| **[P78](../OPEN_PROBLEMS.md)** | Stroke buys gentleness, and the same stroke is more guided length for tolerance and friction to vary over. **P78 already says stroke makes the worst defect worse; this says which defect** |
| **[P102](../OPEN_PROBLEMS.md)** | Names the gap in the same words and does not close it |
| **What it cannot do** | **Supply VOLLEY's clearance.** An optimum belongs to the mechanism it was optimised for — its masses, its rail length, its fit, its release. **Importing one would be the mistake this file exists to prevent**, and it is the same rule already applied to the vault's straightness arithmetic |

### A modern separation mechanism with ground qualification and a flight

**Jiaolong Zhang *et al.*, "Modular design and structural optimization of CubeSat separation
mechanism", *Acta Astronautica* **225**, 2024**, DOI `10.1016/j.actaastro.2024.09.067`.
**Abstract-level evidence. The publisher record is unreachable from this environment** — see the
retrieval note below.

What two independent retrievals return consistently: a topology-then-size optimisation using a
surrogate-model-assisted hybrid search, reducing the mechanism's **mass proportion to 18 %** at a
maximum deformation of **0.123 mm**; **ground verification by overload, vibration and shock
mechanical tests**; and **in-orbit deployment of the BY-03 satellite**.

| | |
|---|---|
| **What it moves** | **[A21](../validation/A21_comparators.md)'s comparator, on maturity rather than mass.** A21 compares VOLLEY against a spring dispenser as a *class*. This is one named mechanism that has been optimised, environmentally qualified on the ground **and flown** |
| **Why that matters more than a mass number** | `FIGURE_INDEX.md`'s **class-D evidence has zero members** and **E4** says nothing here has been built, fired or measured. **The comparator is four rungs up the evidence ladder from VOLLEY, not one** — simulation-only, prototype-tested, environmentally qualified, flight-proven, and VOLLEY is on the first rung |
| **What it cannot supply** | **A mass for the comparison.** The abstract gives a mass *proportion*, not a mechanism mass, and the **2.417 kg** figure this file was offered is a full-text claim that has not been read here. **It is not quoted anywhere in this repository** |
| **What it must never be used for** | **Another mechanism's flight is not evidence about VOLLEY.** It sharpens how far behind VOLLEY's evidence is; it moves nothing about whether VOLLEY works |

**Not added to [`PRIOR_ART.md`](PRIOR_ART.md).** That file's own first line requires every work in it
to have been read and its metadata verified against the publisher record. **Neither is true here**,
and P22 is the entry recording what happened the last time this file was written from abstracts.

### The citations were checked, and the first check was partly wrong

> **As written 2026-08-22, and preserved so the correction has something to correct:**
>
> | Named as | What the check found |
> |---|---|
> | A 2024 modular CubeSat separation mechanism, *Acta Astronautica* **225**, pp. 758–767, with a stated mechanism mass, a full environmental campaign and an in-orbit deployment | **The paper is real and the page range is wrong** — it is **pp. 615–624**. Its abstract describes a surrogate-model size optimisation reducing the mechanism's **mass proportion to 18 %** at **0.123 mm** maximum deformation. **The mass figure, the test campaign and the flight are not visible in it** and could not be confirmed |
> | Two 2026 micro-spacecraft separation papers, carried as the strongest new evidence | **Could not be confirmed from the sources reachable here.** One pairs a publisher series identifier with an unrelated publisher's URL. *Not "they do not exist" — not found* |
> | — | **The paper that did confirm, twice, was named by neither**, and it is the one above |

#### Corrected 2026-08-22, later the same day. Two of those three findings are withdrawn.

**1. "The test campaign and the flight are not visible in it" — withdrawn.** They are stated in the
abstract, and a second retrieval returns them in the paper's own words: *ground verification with
overload, vibration and shock mechanical tests, and successful in-orbit deployment of the BY-03
satellite.* **The first check read a partial abstract summary as if it were the whole abstract**
and reported an absence that was an absence in the summary. *The 2.417 kg mass is still unread and
is still not quoted.*

**2. "The page range is wrong — it is pp. 615–624" — withdrawn.** **No source reachable from here
gives a page range at all.** The 615–624 was taken from a single search summary and published as a
correction to a citation. **A correction asserted from a snippet is the same defect as a claim
asserted from a snippet**, and this one was worse because it was framed as due diligence. The
pagination is **unverified**, in both directions.

**3. "Two 2026 papers could not be confirmed" — narrowed, not withdrawn.** Exact-title searches for
both return other work. **That remains "not retrieved", and it is now clear that it is a property
of this environment rather than of the sources**, because the environment cannot retrieve anything.

> ### The retrieval note, and it is the whole reason the three findings above are graded rather than settled
>
> **Every publisher and bibliographic host is refused by this session's egress policy.** Checked
> 2026-08-22: `doi.org`, `api.crossref.org`, `api.openalex.org`, `api.semanticscholar.org`,
> `sciencedirect.com`, `mdpi.com`, `iopscience.iop.org`, `arxiv.org` and `scholar.google.com` all
> return **403 at the proxy**. The only external retrieval that works is web search, which returns
> **abstracts, indexing records and summaries** — never a publisher record and never a full text.
>
> **So no source in this section has been verified the way [`PRIOR_ART.md`](PRIOR_ART.md) requires**,
> and every entry says so at the point of use. **A10 recorded the same limitation for a component
> datasheet in its own words** — *"unreachable from this environment; that limitation is recorded
> rather than worked around"* — and this is that, for literature.
>
> **"Not retrieved" is not "does not exist", and it is also not "verified".** Both halves of that
> sentence are the rule.

**This is recorded because the rule is the rule.** [P22](../OPEN_PROBLEMS.md) and
[P57](../OPEN_PROBLEMS.md) are both entries about a source that was cited or relied on before it was
read. **The engineering in the sweep survived the check. Its citations are still unverified, and so
was the correction to them.**

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
