# Build readiness

**What is settled, what is not, and — for each thing that is not — whether the answer comes from
more computation or from metal.**

This file exists because "TRL 2–3" is a label, not information. A reader deciding whether this
work is worth taking seriously needs to know which subsystems are finished as designs, which are
finished as analyses, and which are neither. Those are three different states and the repository
has all three.

> ## The one sentence that governs everything below
>
> **Nothing has been built, fired, or measured at any scale.** That is `OPEN_PROBLEMS.md` **E4**,
> it is still open, and no amount of the analysis below changes it. Fifty-three validation runs
> exist. **Zero measurements exist.** Every number in this repository is a model output, and the
> field model has only ever been checked *analytic against analytic* — a closed-form wave model
> against magpylib, two implementations of the same physics.
>
> **[`B1_ORDER.md`](B1_ORDER.md) is the order that changes the category of evidence**, it costs
> ₹22,000–52,000, it has had a method since 2026-07-29 and a bill of materials since 2026-07-30,
> and **it has not been placed.** Nothing on this page matters as much as that.

## How to read the columns

| Column | Means |
|---|---|
| **Design** | Is the geometry frozen in `cad/parameters.json` and generated into `cad/step/gen5/`? |
| **Analysis** | Has the governing physics been computed against a band declared before the script? |
| **Blocked by** | What the next step actually requires |

**"Metal"** means the remaining uncertainty cannot be reduced by computation — a material
property, a manufacturing tolerance, a contact behaviour, or a number that only a measurement
settles. **"Computation"** means the work is specified and simply has not been done.

---

## Subsystem by subsystem

### Track — design frozen, structure unanalysed

| | |
|---|---|
| **Design** | **Frozen.** 1800 mm longerons, roller channels, guide rails, launch locks, all in `parameters.json` and generated into Gen5 |
| **Analysis** | **Incomplete.** No structural FEA of the track exists — E2 records FEA for the sled (A4) and the field (A1) and nothing else |
| **Blocked by** | **Computation.** A modal and static case against the GEVS protoflight spectrum, using the method A18 already established |

### Stator — design frozen, thrust constant known to 4.4 %

| | |
|---|---|
| **Design** | **Frozen.** 162 conductors, three-phase belt, 48 mm wavelength, 90 mm active depth |
| **Analysis** | **Substantially complete, with a live correction.** A1 agreed with a 2-D meshed FEM to 0.07 %. **A2 then found K<sub>t</sub> is a centre-plane value overstating thrust by 4.42 %** — P46, computed and held, not applied |
| **Blocked by** | **Both.** A2 band 4 (an independent 3-D FEM solve) is *computation* and was not run. The 4.42 % correction then needs a change-control decision. **And B-1 is the measurement that would settle whether either number is right at all** |

**This is the subsystem the whole machine rests on**, and it is the one where the gap between
"computed twice" and "measured once" is widest.

### Sled — design frozen, mass is the sensitive number

| | |
|---|---|
| **Design** | **Frozen but unpocketed.** 488 mm, 9.445 kg from the Gen3 solids (P15), drawn solid with no lightening |
| **Analysis** | **Complete for the governing case.** A4 ran CalculiX; A12 corrected the inter-array force from 3.7 to 2.69 kN; A23 settled the release |
| **Blocked by** | **Computation, then metal.** Pocketing the sled is the single largest velocity lever available without an architecture change (+13 % at 60 %), and it requires re-running `mass_properties.py` then `motor_model.py`. The gap shim tolerance of ±0.05 mm is then a *manufacturing* question |

### Magazine and retention — design frozen, cycle life unmeasured

| | |
|---|---|
| **Design** | **Frozen.** Two cassettes, six cells each, 104 mm pitch, **two D9 A-286 pins** after A22 resized them from D6 |
| **Analysis** | **Complete for the governing case.** A22 closed P37 and the analysis half of E10: margin **+0.45 at Q = 30**, positive across Q = 10…30 |
| **Blocked by** | **Metal.** Q is **unmeasured** — `STRUCTURAL_GAP.md` records this. A22 sized against Q = 30 as the conservative end, but the actual structural Q of the built article is a measurement, and escapement cycle life is a test, not a calculation |

### Payload cell — a design, and no insert exists

| | |
|---|---|
| **Design** | **Parametric only.** ADR-025 fixed the cell at 340.5 × 100 × 100 mm; `parameters.json` marks it `PARAMETRIC_ONLY_NOT_DRAWN` |
| **Analysis** | **Complete, and it moved the answer.** A24 found **1U no longer closes kill criterion 1** (2.125 kg, not 1.913) and that **ThinSat and 12U do not fit at all** — the 166 mm cassette width is a constraint written down nowhere else |
| **Blocked by** | **Computation.** No insert exists in CAD for any class, and the insert must present CDS corner rails to the machine and a class-specific interface to the satellite. That is real mechanical design, not a parameter change |

### Brake — the least finished subsystem in the machine

| | |
|---|---|
| **Design** | **Provisional.** Two tapered pole plates at 15 mm, **lightened from solid blocks on structural reasoning alone** |
| **Analysis** | **Not done.** `parameters.json` states it plainly: *"Magnetic sizing against the required pole area has NOT been done."* A11 adopted regenerative braking and opened **P28** in the same act — the regen stator and the eddy fin do not both fit the arrest section |
| **Blocked by** | **Computation.** An eddy-brake field solve, and a resolution of P28 |

**If one subsystem would embarrass this repository under review, it is this one.** It is stated
here rather than left for a reader to find.

### Drive and energy store — the largest open defect

| | |
|---|---|
| **Design** | **Not frozen.** The bank is 96 V, 6 F in `parameters.json`, but **P26 says it cannot source the shot on purchasable parts** |
| **Analysis** | **Complete, and negative.** A10 derived the **68 mΩ ESR ceiling**; a single commercial string is 116–185 mΩ. Three to four parallel strings are required. **A25 then showed a flywheel clears the ceiling at 35 mΩ with 66 kW deliverable**, at mass parity (P45) |
| **Blocked by** | **Metal, and one datasheet.** P45's band miss turns entirely on an unsourced machine specific-mass figure. **One datasheet decides whether the flywheel is lighter than the bank or heavier** |

### Host interface — specified, with one requirement missing

| | |
|---|---|
| **Design** | **Frozen.** Ø460 mm ring flange, Ø400 mm bolt circle, 24 holes, per ADR-010 |
| **Analysis** | **Incomplete in one specific way.** **E29**: nothing computes the shot's angular impulse about the host CoM. `astro.py` models the interaction as one line and that line is linear only |
| **Blocked by** | **Computation.** At a 50 mm CoM miss a 15 N·m·s wheel saturates around shot four. **No interface requirement exists that the thrust line pass through the host centre of mass**, and that absence is the defect |

### Avionics, thermal and packaging — absent from the rollup

| | |
|---|---|
| **Design** | Equipment bays are located and verified clear of the track |
| **Analysis** | **Missing.** **P10**: the enclosure, radiator and packaged avionics have **no line items** in `mass_properties.py`. The 126.6 kg dry mass is a **floor, not a total** |
| **Blocked by** | **Computation.** Straightforward bookkeeping that has simply not been done, and it makes every kg-per-satellite figure in the project optimistic |

---

---

## Gen6 — the architecture now carried as the design target

**Added 2026-08-16.** Everything above is **Gen5**, which remains the *measured baseline* and the
record of what a self-contained deployer costs. [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
moved the design target on 2026-08-14: the payload is accelerated directly by cold gas along a rail
a spent upper stage provides. **No mover, no stator, no bank, no brake, no return stroke.**

**Six of the nine subsystems above do not exist in Gen6.** Track, stator, sled, brake, drive and
energy store are all deleted rather than improved. Their rows are kept because Gen5 is the baseline
that was actually analysed, and deleting the record of a superseded design would remove the only
measured thing this project has.

**Gen6 is younger than Gen5 by every measure**: eleven run sheets against forty-five for the
programme, one CAD generation, no packaging, no thermal model, and three parts that have no
geometry at all.

### Stage rail and drive tube — geometry generated, mechanism absent

| | |
|---|---|
| **Design** | **Generated, not frozen.** `cad/build_gen6.py` emits six parts from `parameters.json` — drive tube, carriage, chamber, reservoir, stage rail, magazine cassette. Bore 15.805 mm, stroke 2180 mm |
| **Analysis** | **A37** made the stage the machine and A38 showed tip-off does not bind at 25 g |
| **Blocked by** | **Design work, not computation.** The **piston, seals, valve and plumbing have no geometry**. The rail is drawn; the thing that pushes is not |

### The gas store — specified, and its size is wrong by about 1.3 kg

| | |
|---|---|
| **Design** | **Specified.** A 2 L chamber charged to 50 bar, fired as a closed adiabatic expansion, giving **30.535 m/s at 25 g**. There is no regulator — A41 closed P63 by deleting the component rather than pricing it |
| **Analysis** | **Four runs, one failed band.** A39 chose gas over a spring; **A40 killed the fixed-orifice implementation** at 14.16 m/s against a 30 m/s band; A41 passed eight of eight; **A42 failed band 3** — the reservoir is sized on gas the bottle cannot give back, and runs out at shot seven of twelve |
| **Blocked by** | **Nothing computational — A43 closed it on 2026-08-16.** Conduction through stagnant nitrogen gives a **17 460 s** time constant against a **1200 s** cadence, so the bottle does not re-equilibrate and the design reservoir is **9.55 L** on a **5.38 kg** store. P64 is resolved; **P66** records that both of A42's bracket endpoints were unreproducible. What remains is **metal** |

### The cradle — the part that does not exist

| | |
|---|---|
| **Design** | **None.** There is no cradle mechanism in any file |
| **Analysis** | **A38 states the requirement**: **201.674 N per contact** of preload, released inside A34's **≤ 1 N** residual. Passing A38 band 5 is not the same as that being easy |
| **Blocked by** | **Design work.** This is a mechanism concept before it is an analysis, and **kill criterion 4 stays *modelled, not demonstrated* until it exists** |

### The stage itself — neither computation nor metal

| | |
|---|---|
| **Design** | Not applicable. The vehicle is somebody else's |
| **Analysis** | **[A45](../validation/A45_stage_credit.md) bounded it on 2026-08-16, and the falsifier fired.** The real break-even is **16.5 %**, not the 30 % ADR-032 states, and the credit's largest item — 8.00 kg of enclosure, radiator and packaged avionics — is **P10**, a mass recorded here as never itemised. That one line is 18.5 % of the credit and fires the falsifier alone. Added mass per satellite is **1.403 – 3.108 kg**. **P68** |
| **Blocked by** | **A conversation, which is a third category this page did not previously have.** No launch provider has agreed to keep a stage alive past passivation, and doing so on terms that do not spend its disposal propellant is a regulatory discussion this project has not had |

### What Gen6 has no analysis of at all

**Stated as a list rather than left to be found**, in the order they bear on the claim:

1. ~~**Velocity control.**~~ **Modelled 2026-08-16 by [A44](../validation/A44_gen6_dispersion.md),
   and it failed two bands.** 3σ dispersion is **1.113 %** against a declared 0.5 %, and **93.4 %
   of the variance is a seal friction nobody has measured** — a fivefold better transducer moves
   the answer by 0.008 %. Chamber temperature cancels outright, which turns the thermal question
   into a sequencing requirement. **P67**, and it is now a bench test rather than a computation.
2. **Recoil**, which scales with the impulse, and the impulse has roughly doubled.
3. **Envelope and packaging** on the stage.
4. **Thermal**, including the expansion cooling that P64 turns on.
5. **Mass line items for avionics and packaging**, which is P10 carried across unchanged.

## What this adds up to

**Four subsystems are frozen as designs and analysed against declared bands**: stator, sled,
magazine, interface. **Three are frozen but under-analysed**: track, avionics, payload cell.
**One is genuinely provisional**: the brake. **One is a known negative result with a candidate
fix**: the energy store.

**Of the remaining work, most is computation, not metal.** That is the honest position and it
cuts both ways: it means the design is further along than a TRL label suggests, and it means
the claim "everything computable is done" is **not yet true**.

The specific things that still need computing, in the order they matter:

1. **Design the per-cell backup ejector.** [A47](../validation/A47_gen6_fmea.md) priced it at
   **+2.27 satellites** delivered at *r* = 0.99, against **+0.37** for the entire Gen5 → Gen6
   architecture change — **six times more**, because it converts the drive from
   manifest-forfeiting to satellite-forfeiting. It is the only change found that touches what
   **E30** actually says. **P75.**
2. **Close P10.** Build the enclosure, radiator and packaged avionics up from line items instead
   of carrying a parametric lump. It is the largest single piece of the stage credit, it fires
   ADR-032's first falsifier on its own (**P68**), and it is bookkeeping rather than research.
3. **Nothing else, on the Gen6 store or its velocity.** A43 closed P64 and A44 modelled the
   dispersion on 2026-08-16. **What remains there is not computation** — it is a measured seal
   friction (**P67**) and a cradle mechanism that does not exist.
3. **A2 band 4** — a 3-D FEM solve, so K<sub>t</sub> has been checked by a method that solves a
   field equation. Everything downstream rests on it, and P46 should not be applied without it.
4. **The brake's magnetic sizing**, and P28. *Gen5 only; Gen6 has no brake.*
5. **P10's mass line items**, without which no kg-per-satellite figure is trustworthy — and that
   applies to both architectures.
4. **E29's angular momentum budget**, and the interface requirement it would set.
5. **Track structural FEA.**

And the things that need metal, which no amount of the above replaces:

- **The thrust constant.** B-1, ₹22,000, unordered.
- **Structural Q**, which A22's margins are conditional on.
- **Escapement and gate cycle life.**
- **Manufacturing tolerance on the 1.0 mm air gap**, which sets everything.

---

## The claim this repository is entitled to make

**Not** "it is ready to build."

**This:** the design is specified to the level where a builder knows what to make; the physics has
been computed against bands declared before the analyses that tested them; **twenty-four
validation runs exist, three failed outright, several missed individual bands, and every one of
those is recorded rather than removed**; and the remaining uncertainty has been enumerated rather
than estimated.

**Three times a declared band caught a bug in the analysis rather than a problem in the design**
(A19, A20, A2). That is what declaring bands first is for, and it is the strongest evidence here
that the numbers were not fitted to the conclusion.

**What is missing is a measurement.** Not a model, not a document, not another analysis — a
gaussmeter, eight magnets, and an afternoon.
