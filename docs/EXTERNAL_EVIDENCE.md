# What the outside world can close, and what it cannot

**Opened 2026-08-20.** Until this date **every number in this repository came from inside it** — its
own scripts, its own run sheets, and handbook values declared at the point of use. **A10 records the
consequence in its own words**: the bank ESR bracket came from distributor listings because
*"the manufacturer's own data could not be obtained; that limitation is recorded rather than
worked around."*

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

**Evidence level: ABSTRACT ONLY.** What the published abstract states:

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

**Evidence level: ABSTRACT ONLY.** The full text has not been read, so this entry is a **lead**:
its method is used to decide what VOLLEY must model, and **no figure from it is cited anywhere in
this repository.**

### What it can move, and what it cannot

| | |
|---|---|
| **[P67](../OPEN_PROBLEMS.md)'s framing** | **Friction is not separable from the geometry that produces it.** B-2 measures a force; the force is a property of a bore, a finish, a clearance and a seat. *The measurement stays first — this changes what it is a calibration point for, not whether to take it* |
| **[P78](../OPEN_PROBLEMS.md)** | Stroke buys gentleness, and the same stroke is more guided length for tolerance and friction to vary over. **P78 already says stroke makes the worst defect worse; this says which defect** |
| **[P102](../OPEN_PROBLEMS.md)** | Names the gap in the same words and does not close it |
| **What it cannot do** | **Supply VOLLEY's clearance.** An optimum belongs to the mechanism it was optimised for — its masses, its rail length, its fit, its release. **Importing one would be the mistake this file exists to prevent**, and it is the same rule already applied to the vault's straightness arithmetic |

### A modern separation mechanism with ground qualification and a flight

**Jiaolong Zhang, Jingao Su, Chao Wang, Yiqian Sun, "Modular design and structural optimization of
CubeSat separation mechanism", *Acta Astronautica* **225** (2024) 758–767**, DOI
`10.1016/j.actaastro.2024.09.067`. **Evidence level: PUBLISHER METADATA VERIFIED.**

| From the publisher record | |
|---|---:|
| Optimised separation-mechanism mass | **2.417 kg** |
| Mass reduction | **34.9 %** |
| CubeSat + mechanism total | **13.417 kg** |
| Mechanism mass proportion | **18 %** |
| Maximum deformation | **0.123 mm** |
| Ground mechanical verification | **overload, sine, random vibration, shock** |
| Flight | **BY-03 deployed in orbit** |

#### What it moves: A21's comparator, on evidence maturity

[A21](../validation/A21_comparators.md) compares VOLLEY against a spring dispenser as a *class*.
**This is one named mechanism carried the whole way**, and the ladder it exposes is the useful
thing:

| Rung | | VOLLEY |
|---|---|:-:|
| 1 | Analysed only | **here** |
| 2 | Prototype with separation tests | — |
| 3 | Ground environmental qualification — overload, sine, random, shock | — |
| 4 | **Flown** | — |

`FIGURE_INDEX.md`'s **class-D evidence has zero members** and **E4** says nothing here has been
built, fired or measured. **The comparator is three rungs above.**

> **Its flight is not evidence that VOLLEY works.** It is evidence about how far VOLLEY's evidence
> has to travel, and the two must never be confused. *A separation mechanism succeeding in orbit
> says nothing whatever about a different mechanism that has never been made.*

**On mass, read it carefully.** 2.417 kg is a **separation mechanism for one CubeSat**, at 18 % of
a 13.417 kg stack. VOLLEY's numerator is a **deployer amortised over a manifest** — 10.547 kg per
3U satellite on dry mass, 1.2145–3.0827 kg on added mass ([P68](../OPEN_PROBLEMS.md)). **They are
not the same quantity and this file does not divide one by the other.** What the comparison
supports is [P69](../OPEN_PROBLEMS.md)'s finding, already recorded: **mass parity with conventional
separation hardware is withdrawn.**

**Not added to [`PRIOR_ART.md`](PRIOR_ART.md).** That file requires the work to have been read in
full, and this entry is metadata plus abstract.

### The separation-dynamics method cluster

**Three records, and their value is method rather than number.** None of their dimensions,
clearances, tolerances or coefficients may enter VOLLEY: those belong to the mechanisms they were
derived for.

| Record | Evidence level | What it contributes to [P103](../OPEN_PROBLEMS.md) |
|---|---|---|
| **Zhenyu Jin *et al.*, "Rapid Modeling Method and Analysis of Factors Affecting the Dynamics of On-Orbit Launch Systems for Micro-Spacecraft", *Aerospace* **13**(6) 541, 2026**, DOI `10.3390/aerospace13060541` | PUBLISHER METADATA VERIFIED | **The two-level modelling structure P103 step 2 and step 3 adopt**: a high-fidelity rigid–flexible model, a reduced multibody model calibrated against it, and parametric sweeps run on the reduced one. Also the *factor list* — **thrust misalignment, thrust eccentricity and mass eccentricity** as first-class inputs, not second-order corrections |
| **Linfei Yang *et al.*, "Research on the Influence of Structural Parameters of Micro-Spacecraft On-Orbit Launch Separation Mechanism on Launch Accuracy"**, DOI `10.3233/ATDE260113` | PUBLISHER METADATA VERIFIED | **Monte Carlo over structural parameters — guide clearance, sliding length, step thickness — with guide clearance identified as the key one.** The transferable finding is that **guided-contact geometry has an optimum and drives release accuracy**, which is why P103 lists clearance as first-order rather than a tolerance detail |
| **Zengqiao Tan, Haibo Yang, Xiaoyu Tao, "General method for establishing a contact force model during the in-orbit launch of micro-spacecraft", *J. Phys. Conf. Ser.* **3240** 012008, 2026**, DOI `10.1088/1742-6596/3240/1/012008` | PUBLISHER METADATA VERIFIED | **The contact model itself.** Micro-spacecraft-against-barrel collision, a **Lankarani–Nikravesh** continuous contact force law, a finite-element collision model with mesh validity checked, and **inverse identification of the contact parameters by unscented Kalman filter** against the FE result. *This is the answer to "where do contact stiffness and damping come from before there is hardware?"* |

> **Together they say the same thing three ways, and it is the thing P103 exists for:** for a
> guided ejection, **the exit attitude is set by contact, clearance and eccentricity**, the contact
> law needs parameters that are *identified* rather than assumed, and the practical route is a
> reduced model calibrated against a higher-fidelity one. **None of that requires hardware**, which
> is why P103's model is no longer waiting behind B-2 — see the amendment in that entry.

**What none of them supplies:** VOLLEY's clearance, VOLLEY's straightness, VOLLEY's friction
coefficient, or a tolerance any of them optimised. **Those are configuration-specific and
importing one would be the failure this file exists to prevent.**

### The audit that preceded this, and why it is wrong

> **Written 2026-08-22 and superseded the same day.** An earlier revision of this section reported
> that the *Acta Astronautica* pagination was **615–624**, that the 2.417 kg mass, the test
> campaign and the BY-03 flight **could not be confirmed**, and that two 2026 separation papers
> **could not be confirmed at all**.
>
> **Every one of those findings is withdrawn.** The pagination is **758–767**. The mass, the
> campaign and the flight are in the publisher record. All four records above are real and their
> metadata is verified.
>
> **The defect was method, not carelessness.** Those conclusions were drawn from indexing summaries
> rather than from the publisher records, and **an absence in a summary was reported as an absence
> in the paper** — including a *correction to a citation* that was itself unsourced, which is worse
> than the claim it corrected because it wore the authority of having been checked.
>
> **The rule this produces**, and it is now the rule for this file: **every entry states its
> evidence level** — `FULL TEXT READ`, `PUBLISHER METADATA VERIFIED`, `ABSTRACT ONLY`,
> `SECONDARY LEAD`, `NEEDS SOURCE` — **and no numerical result is quoted below the level that
> supports it.** [P22](../OPEN_PROBLEMS.md) is the entry that first taught this project the cost of
> writing a literature file from abstracts. This is the second time.

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
