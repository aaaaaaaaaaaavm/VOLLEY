# Review responses

**A reviewer's register, answered or conceded, question by question.**

Thirty-five questions. Items 1–3, 7–8, 14–16 and 20–21 were raised in review by a former ISRO
scientist; the remainder is the register a reviewer of that background would be expected to
bring, written down in advance rather than waited for.

> **The honest aggregate, before any individual answer:**
>
> | | Count | Meaning |
> |---|---:|---|
> | **Answered** | **20** | An analysis or document exists, with a band or criteria declared before it ran |
> | **Partial / scoped** | **14** | Something exists, or the path is named; neither fully answers the question |
> | **Open** | **1** | **Item 5 — no customer exists, and no analysis substitutes for asking one** |
>
> *Updated 2026-08-10 as the register was worked: **30** answered (the interface permits it, and
> the survey found three worse problems), **20/22** answered structurally by the FMEA, **26**
> answered and reduced to an inhibit, **18** answered by the actuator trade, **11** and **12**
> answered and severe, **10** and **25** scoped as qualification paths rather than analyses.*
>
> **Seven new register entries came out of this review** — E29 through E34, and P45 — which is
> more than the review found wrong. **That is the point of asking someone who has flown things.***
>
> **Fourteen of thirty-five have no answer at all.** Several are not hard — they are simply not
> done. Two of the four the author judges potentially project-lethal (**22** and **30**) are in
> that group, and **one of the other two (28) is already answered as a loss.**

**Rules for this file.** An answer cites the analysis or document that supports it, or it says
"open" and names what would close it. No question is answered by assertion. Where the honest
answer damages the project's case, that is the answer given.

---

## The four judged potentially project-lethal

### 4. Why not restart the upper stage and let the host do the phasing? — **PARTIAL, and the most commercially dangerous question here**

**What exists.** ADR-024 and A20 quantify host repositioning: a 50 km altitude shell costs
**27.82 m/s** two-burn Hohmann, and above roughly 100 m/s of host budget *the stage supplies most
of the altitude range and the deployer supplies the distribution within it.*

**What is missing is the direct comparison the question asks for.** If a restartable stage can
reposition between deployments, it can also phase satellites by simply waiting between releases —
and no analysis in this repository prices that against VOLLEY.

**The argument that should survive** is that a stage restart moves *all remaining satellites
together* — it changes the stage's orbit, not the relative velocity between the satellites it
still holds. Twelve satellites needing twelve different along-track positions need either twelve
burns or one commanded differential per satellite. **But "should survive" is not "has been
computed", and this needs a number.**

**Closing it:** a burn-count and propellant comparison for a 12-satellite along-track
distribution, host-only versus host-plus-VOLLEY, with bands declared first.

### 22. If the sled jams mid-stroke, don't you lose the entire campaign rather than one satellite? — **OPEN. Nothing addresses it**

**Yes.** One sled serves all twelve cells. There is no redundant sled, no manual release, and no
analysed jam case anywhere in this repository — `grep -ri jam` returns nothing.

**This is a single point of failure for the entire payload manifest**, and it compares badly with
a P-POD-class dispenser, where each tube's failure costs one satellite.

**It is worse than a generic reliability concern**, because a jam mid-stroke leaves a satellite
retained by a partially-actuated mechanism with a charged bank behind it.

**Answered structurally, 2026-08-10** — [`docs/FMEA.md`](FMEA.md). **The jam is not a special
case: it is one of nine elements that forfeit the remaining manifest on a single failure**, and
the sled is merely the most obvious. A spring dispenser has **zero** such elements. Nine shared
elements over twelve cycles is **108 chances to fail**.

**What is still missing is what was asked for second:** there is **no recovery mode and no
accepted-risk statement**, and the per-element reliability that would make the risk quantifiable
is **unmeasured** — cycle-life testing is metal, not computation. See **E30**.

### 28. How does the mass compare against a COTS cold-gas module delivering the same Δv? — **ANSWERED, and it is a loss**

**A cold-gas module wins by 7.5× at 3U.** `validation/A21_comparators.md` band 5 **declared this
loss in advance** rather than discovering it: 6.375 kg of shared deployer per satellite against a
0.5–1.2 kg module.

**What the module costs instead is the thing VOLLEY exists to avoid:** a pressure vessel, a
propulsion system, a regulatory path, and a modification to the customer's satellite. VOLLEY's
case is that the *satellite* carries nothing.

**And this got worse on 2026-08-10, not better.** The repository's answer to this has been the
payload ladder — smaller classes amortise the deployer across more customers. **A24 then built
that ladder as an actual design and found 1U no longer crosses the 2 kg threshold** (2.125 kg,
not 1.913). The threat now closes only at PocketQube class, which is the class with **no corner
rails and no designed interface at all**.

**This is the strongest argument against the project and it is stated in its own kill criteria.**

### 30. Do launch vehicle ICDs even permit deployment at 16 m/s? — **ANSWERED 2026-08-10. Yes. And the survey found three worse problems**

**Rideshare Payload User's Guide, Version 10 (September 2024), §3.3.2**, read in full:

> *"Payloads must target a minimum separation velocity of 0.3 m/s and a maximum separation
> velocity of 1.0 m/s. **Containerized deployments such as CubeSats may be deployed at a velocity
> greater than 1.0 m/s.**"*

**A 1.0 m/s cap exists and containerised CubeSat deployments are explicitly exempt, with no
numeric ceiling anywhere in the document.** VOLLEY is a containerised CubeSat deployment.
**16.388 m/s is not prohibited on this interface at this revision.** The question expected to be
lethal is not.

**But the same document contains three requirements that matter more**, all recorded in
[`docs/ICD_COMPLIANCE.md`](ICD_COMPLIANCE.md) and **E31**:

1. **Deployments must be under active attitude control**, and *"deployments in uncontrolled
   directions or during Payload tumbling are not allowed."* **E29 puts wheel saturation at about
   shot four of twelve.** After that, remaining releases are **non-compliant**, not merely
   degraded.
2. **A seven-day hold before secondary deployments**, which applies to the hosted last-mile
   configuration ADR-024 adopted. **E28 found the campaign window at a real POEM altitude is
   29–36 days**, so the hold costs 20–24 % of it before the first shot.
3. **An exit-direction requirement** — deployed payloads must leave through the +X face of the
   allowable payload volume. VOLLEY fires along its track axis, which on a radial ESPA port is
   not +X.

**Plus a qualification gap that is paperwork, not physics.** NRCSD-E reportedly requires CubeSats
to withstand **0.5–2.5 m/s** at ejection *(second-hand, not read in the primary document)*.
VOLLEY is 6.6× that ceiling. **Physically irrelevant** — a satellite is damaged by acceleration,
not velocity, and 10.53 g sits well inside the 25 g CDS cap. **Programmatically real**: a customer
qualified "per NRCSD-E" has no qualification basis for 16.4 m/s even though nothing about their
hardware is threatened.

**The survey is one document deep** and supports no claim about the market.

### 30 (original assessment, retained) — **OPEN, and it may be decisive**

**Nothing in this repository checks it.** The only ICD references are to NRCSD tip-off *rate*
limits (2 °/s versus 5 °/s, an unresolved conflict already logged), not to separation *velocity*
limits.

**This matters more than any physics on this page.** Conventional dispensers release at 1–2 m/s,
and if a launch provider's ICD caps separation velocity anywhere near that figure, **VOLLEY's
entire premise is non-compliant by a factor of eight** regardless of whether it works.

**It is also the cheapest question here to answer** — it requires reading published rideshare
user guides, not running an analysis.

**Closing it:** a survey of published rideshare payload user guides for stated separation
velocity limits, with the documents and revisions named per `validation/README.md`'s external-
document rule. **Until then, the project's central number has never been checked against the
rule that would govern it.**

---

## Answered

### 1. Why 16.4 m/s when the satellite is already travelling at 7.6 km/s?

Orbital speed is not the quantity that matters; **Δv relative to the host is.** 7.6 km/s is shared
by the host and every satellite on it, so it produces no separation and no orbit change. The
16.388 m/s is *differential*, and differential velocity is what changes an orbit.

Computed in `analysis/astro.py`: one shot raises apogee from 450 to **508.9 km** and extends
orbital lifetime **+61.8 %**. A 2.5 m/s spring gives +8.2 %.

### 2. Why go beyond conventional 1–2 m/s deployment velocity at all?

Because the payoff is **superlinear in Δv**, so the marginal value of each m/s rises:

| Δv | Lifetime gain | per m/s |
|---:|---:|---:|
| 2.5 m/s (spring) | +8.2 % | 3.29 %/m/s |
| 16.39 m/s | +61.8 % | 3.77 %/m/s |
| 25.3 m/s | +104 % | 4.11 %/m/s |

And a spring's *designed differential is zero*, so a spring-deployed fleet can only phase by drag.

### 3. Why build a complex system when a spring at 2 m/s already works?

**For a single satellite into the orbit it was already going to, a spring is the correct answer**
and this project does not dispute it. `docs/LANDSCAPE.md` records mass parity — about 6 kg per 3U
either way — so the complexity does not buy mass. **It buys commanded differential velocity**,
which a spring cannot produce at any mass.

At 3U against a cold-gas module, VOLLEY loses (see 28). The case is a *fleet* needing distinct
orbits from one release event.

### 6. What's wrong with free drag-differential phasing over three weeks?

Nothing, and `A21` treats it as the real comparator rather than the spring. It is free and has
flown. VOLLEY's advantage is **time and schedulability**: ~**1.4 days** to 30° of phase against
~**25 days** by drag, roughly **18×**.

Drag phasing also requires differential ballistic coefficient — attitude control or deployable
area — which is itself a satellite modification.

### 7. How severe is the magnetic/EMI environment, and could it interfere with or damage electronics?

**Severe, and quantified.** `docs/PAYLOAD_ENVIRONMENT.md`, from A14:

| Standoff | Peak field | × Earth's field | × magnetometer full scale |
|---:|---:|---:|---:|
| **20 mm** | **61.081 mT** | **1357×** | **611×** |

**A payload carrying an attitude magnetometer cannot use it inside this deployer**, and
magnetorquers cannot be commanded meaningfully against a 611× bias. A14 band 4 **falsified** an
earlier paper claim that the payload sees a field comparable to a reaction-wheel assembly, and
that sentence was removed from `paper.tex`.

Saturation is recoverable. Remanent magnetisation is not — see 9.

### 8. Is 10.5 g tolerable for typical CubeSat payloads?

**Yes, with margin.** The CubeSat Design Specification qualification cap used here is **25 g**;
the shot is **10.53 g**, about **42 %** of it. `docs/VELOCITY_CEILING.md` records that the 25 g
cap — not the motor — is what limits exit velocity to 25.25 m/s over the 1.30 m stroke.

**The caveat is duration, not magnitude:** 158.6 ms is long compared with a pyroshock, and
whether 25 g survives review as a *sustained* load rather than a transient is flagged in
`docs/PHASE_II.md` as an unresolved question.

### 9. Do soft-magnetic parts inside the payload retain permanent magnetisation — and isn't that itself a modification?

**Yes, and yes.** `docs/PAYLOAD_ENVIRONMENT.md` states it directly: soft-magnetic structure,
screws, shielding cans and motor laminations are **not** recoverable —

> *"The satellite leaves permanently altered. A residual dipole perturbs attitude control for the
> rest of the mission."*

**This is the sharpest question in the register**, because "the satellite is never modified" is
the project's central claim, and a permanent residual dipole is a modification by any reasonable
reading. The repository concedes the physics but has **not** revised the claim's wording, and has
**not** quantified the induced dipole. That part is open.

### 17. Why not simply shield or add standoff instead — was that evaluated?

**Yes.** `PAYLOAD_ENVIRONMENT.md`: **10 mm of standoff at the near face is worth a factor of
eight**, and is the cheapest mitigation available.

**Shielding is explicitly the option to resist** — it adds mass to the *customer's* satellite,
which is precisely the modification the design exists to avoid. Standoff is a deployer-side
change; shielding is a customer-side one.

### 32. How do you manage conjunction with the host and previously released satellites?

`A6` runs a CARA-style conjunction screen and `A15` propagates a twelve-satellite campaign in
GMAT for 90 days, measuring **396 m** worst-case separation and **367°** of nodal spread.

**The gap is intra-cell**, not inter-satellite: A24 found satellites sharing a fixed cell leave at
identical velocity and never separate from each other, and the shim mechanism proposed for it
**failed band 6 at femtosat scale** (P44).

### 34. If this is a good idea, why has nobody flown it?

Partly answered by `docs/PRIOR_ART.md` and `LANDSCAPE.md`: electromagnetic launch has flown
nowhere in space, and the published CubeSat electromagnetic-deployer work sizes for **6.91 MJ per
shot**, which is why those papers need a solar array for recharge. This design's **2.56 kJ** is
three orders of magnitude lower because it targets metres per second, not kilometres.

**The honest remainder:** absence of flight heritage is also evidence about difficulty, and this
answer does not dispose of that.

---

## Partial

| # | Question | What exists | What is missing |
|---:|---|---|---|
| **13** | Where does ~2250 J of loss per shot go thermally, with no convection? | A18's campaign case: **24.4 kJ over twelve shots** at the 1200 s cadence, a 0.32 m² radiator, brake-fin capacity with radiation and conduction | The **per-shot** path, transient fin temperature, and the joint conductance the answer depends on (A19 found it sensitive at 500 W/m²K) |
| **21** | Power, batteries from Earth, POEM-style array mass | P26 (the bank), A10 (68 mΩ ESR ceiling), A25 (flywheel alternative) | **No array sizing, no battery mass, no recharge energy budget.** `mass_properties.py` carries no line item for any of it (P10) |
| **23** | If the brake fails, doesn't the sled exit at 16.4 m/s and become debris? | A tapered pole entry as a 200 g arrest limiter, a ring-spring stop as backstop | **No failure case analysed.** Whether the ring spring alone arrests a 9.445 kg sled at 16 m/s is not computed. Adjacent to 22 |
| **24** | Supercapacitor imbalance, venting, ESR growth over storage and cycling | A10's ESR ceiling; E17 records that the 12 mΩ figure comes from a superseded document with no cell datasheet checked | **No balancing scheme, no venting path, no ageing model.** ESR growth would tighten a ceiling already missed |
| **27** | Ascent random vibration and separation shock for the loaded 124.5 kg stack | A18's Miles case, GEVS protoflight; A22 resized the gates to **+0.45 at Q = 30** | **Q is unmeasured** (`STRUCTURAL_GAP.md`), and the analysis covers the retention gates, not the whole stack |
| **29** | No flight heritage — qualification path and honest TRL | `docs/QUALIFICATION_PLAN.md` specifies a campaign; badges read TRL 2–3 | The campaign is **specified, not costed or scheduled**, and no article exists to qualify |
| **31** | How to verify 16.4 m/s over 1.3 m on the ground in 1 g | `docs/BENCHTOP_TESTS.md`; B-1 measures the **field**, not the shot | **No answer for the full-stroke shot.** A horizontal 1.5 m track on air bearings is the obvious approach and is not specified |
| **33** | Who pays — rideshare customer or launch provider? | `docs/MARKET.md` frames the customer | **No commercial model, no price, and every cost claim was withdrawn** for lack of a vendor quotation (E3) |
| **35** | Host power, peak isolation, interface ownership | 96 V bank, **32.5 kW peak** at 339 A (not 18 kW — the average over the 158.6 ms stroke is 16.1 kW) | **No host bus interface defined, no isolation scheme, no ownership boundary.** ADR-010 specifies the mechanical interface only |
| **14** | Is zero modification actually necessary, or would a small interface change simplify it? | The premise of ADR-002 and the whole product argument | **Never revisited as a trade.** And 9 shows the claim is already compromised by remanent magnetisation, which strengthens the question rather than answering it |

---

## Open — nothing in this repository addresses these

| # | Question | Nearest thing that exists | Severity |
|---:|---|---|---|
| **5** | Which specific customer or mission has asked for this? | `MARKET.md` describes a segment. **No customer exists, and none has been approached** | **High** — commercial |
| **10** | Contamination and outgassing | **Scoped 2026-08-10, not analysed** — see below. **E11** and **E21** both open, and **A27 made E21 load-bearing** | High |
| **11** | Residual dipole → secular torque on the host | **ANSWERED 2026-08-10** — **E33**. Ideal Halbach cancels exactly; **tolerance leaves 0.77–1.92 A·m², saturating a 15 N·m·s wheel in 3–7.5 days with the machine idle** | Answered, and severe |
| **12** | Shock spectrum at release and brake engagement | **ANSWERED 2026-08-10** — **E34**. Release is benign (zero force, per A23). **Brake arrest puts 18.5 kN through a structure holding eleven stowed satellites, eleven times** | Answered, and open |
| **15** | Why not an LSM-driven tug beneath the track, cable-and-pulley to the carriage, EMALS-like with reversed tug motion? | **PII-14** assessed a cable-driven gondola on 2026-08-10 and declined it on margin — but that concept moves the motor *off* the vehicle entirely. **The tug variant, where the LSM stays and only the coupling changes, was not assessed** | Medium |
| **16** | Would separating the mover from the payload sled reduce field exposure and simplify the sled? | PII-11's side-rail layout and PII-14 both touch it. **Neither computes the field-exposure benefit**, which is the point of the question given 611× | **High** — it may be the cheapest fix to 7 and 9 |
| **18** | Why a linear motor rather than a screw, rack, or staged spring? | **ANSWERED 2026-08-10** — A27. Screw disqualified by kinematics, rack by vacuum contact, **spring works and fails only on commandability** | Answered, and it narrows the case |
| **19** | Cable in vacuum: fretting, cold welding, lubricant, pulley bearing life at 16.4 m/s, single load path | PII-14 flags it as unresolved; E21 covers tribology generally | Medium — only bites if a cable architecture is adopted |
| **20** | How reliable is a system with this many failure points? | **Now partly answered — see below.** The *structure* is quantified in **E30**; **p itself is still unestimated** | **High** |
| **22** | Sled jam loses the campaign | **Nothing** — see above | **Lethal** |
| **25** | Radiation and SEE qualification for the SiC drive | **Scoped 2026-08-10, not analysed** — see below | High |
| **26** | Multipaction and Paschen breakdown during ascent depressurisation | **ANSWERED 2026-08-10** — see below. Both ruled out on ordinary operation; an **inhibit requirement** falls out | Closed to an inhibit |
| **30** | Do LV ICDs permit deployment at 16 m/s? | **Nothing** — see above | **Lethal** |

---

---

## 20, expanded: redundancy of springs against a shared serial mechanism

**Raised in review as the risk/reward question, and it deserves a number rather than an argument.**

A spring dispenser is **twelve independent one-shot mechanisms in parallel** — one failure costs
one satellite. VOLLEY is **one mechanism in series with itself, cycled twelve times**. The sled,
stator, bank, sequencer and brake serve every shot; the escapement and gate cycle twelve times
each. **A failure at shot k forfeits shots k through 12.**

`analysis/reliability_architecture.py`:

| Per-shot p (or per-unit q) | VOLLEY sats | Spring sats | VOLLEY fleet-years | Spring fleet-years |
|---:|---:|---:|---:|---:|
| 0.99 | 11.25 | 11.88 | 23.74 | 16.78 |
| 0.95 | **8.73** | 11.40 | 18.44 | 16.10 |
| **0.935** | 7.96 | 11.22 | **16.81** | **15.84** — break-even |
| 0.90 | **6.46** | 10.80 | 13.63 | 15.25 — **spring wins** |

**The risk/reward ratio is the gap between two numbers:**

- Matching a 0.99 spring **on satellites delivered** needs **p = 0.9985** — not a realistic
  target for a twelve-cycle electromechanical system with no flight heritage.
- Matching it **on delivered orbital life** needs **p = 0.9347**, because each delivered
  satellite is worth **1.495×** a spring-deployed one.

**So VOLLEY can afford to lose satellites and still deliver more mission value — but only above
about 93.5 % per-shot reliability.** Below that the spring wins outright, on both metrics.

> **A correction this analysis forces on the project's own headline.** The **7.52× lifetime
> extension** figure is a ratio of *gains* (+61.8 % against +8.2 %). On **delivered orbital
> life** the ratio is **1.495×**. Both are true, but the second governs any risk-weighted
> comparison — a satellite never released delivers nothing — and **the 7.5× figure flatters in
> exactly the comparison a reviewer makes.**

**And the finding: nothing in this repository estimates p.** No FMEA, no fault tree, no parts
count, no cycle-life test. **The project cannot currently say which side of 0.9347 it sits on**,
which means it cannot yet claim to beat a spring at all. Logged as **E30**, which subsumes the
jam case of item 22.

**Two mitigations exist and neither is credited**, because there is no reliability model to credit
them in: the winding is segmented, so losing a segment degrades rather than stops; and gates are
per-cassette, so one gate failure forfeits six rather than twelve.

---

## 26, answered: neither mechanism is credible, and the requirement is an inhibit

`analysis/paschen_multipaction.py`. Both are ruled out for reasons **independent of geometry**,
which is why this is arithmetic rather than a simulation.

**Paschen: the bus is below the minimum, so no pressure and no gap breaks down.**

| Gas | Paschen minimum | Margin over the 96 V bus |
|---|---:|---:|
| Air | 327 V | **3.41×** |
| Neon | 245 V | 2.55× |
| Helium | 156 V | 1.62× |
| Argon | 137 V | 1.43× |

Below a gas's Paschen **minimum**, breakdown cannot occur at *any* pd. For a 1 mm gap air reaches
that minimum at **760 Pa (~5.7 Torr)** — a pressure the vehicle passes through on every ascent —
and **at 96 V that transit is harmless.**

**Multipaction: the wrong regime by four orders of magnitude.** It requires electron transit time
comparable to the RF half-period. The converter gives **f × d = 40 Hz·m** against a lowest
relevant threshold of ~10⁶ Hz·m (1 GHz·mm) — a ratio of **2.5 × 10⁴**. At 40 kHz the half-period
is 12.5 µs and an electron crosses 1 mm in nanoseconds, so **electrons are collected, not
resonantly multiplied.**

**The one case that is not ruled out is a fault.** An *unclamped* interruption of winding current
— 19.70 µH at 373.2 A, **1.37 J stored per phase**:

| Interrupted in | dI/dt | Induced | vs air's 327 V |
|---:|---:|---:|---|
| 1 µs | 3.73 × 10⁸ A/s | **7,351 V** | **exceeds** |
| 10 µs | 3.73 × 10⁷ A/s | **735 V** | **exceeds** |
| 100 µs | 3.73 × 10⁶ A/s | 74 V | below |

A healthy bridge freewheels through its antiparallel diodes and holds the winding near the bus.
**An open-circuit fault has no such path**, and at the critical ascent pressure that is a
breakdown.

**So the requirement is an inhibit, not a design change:** *the bank shall be uncharged and the
winding unenergised while the vehicle transits the Paschen-critical pressure band during ascent.*
The machine has no reason to be energised then, the rideshare guide already calls out **power
inhibits** as separately-verified testing, and **no such requirement is currently written down
anywhere in this repository.** That absence is the finding.

**CFD was not used and is not needed.** The conclusion turns on the bus being below a gas
constant, which no venting model changes. A venting time constant would be orifice flow, not a
Navier–Stokes solve, and using one here would be theatre.

---

## 18, answered: the screw is dead, the rack is marginal, and the spring works

`validation/A27_actuator_trade.md`, criteria declared before the script. **The repository had no
recorded answer to this at all** — `DECISION_LOG.md` records the choice of eddy brake and ironless
stator, never the choice of linear motor over every other way of pushing a satellite.

| Candidate | Verdict |
|---|---|
| **Ball screw** | **Disqualified by kinematics, twice.** 16.388 m/s on a 20 mm lead needs **49,164 rpm**: DN = 1.23 × 10⁶ against a 1.5 × 10⁵ ceiling (**8.2× over**), and whirling critical speed for a 25 mm screw over 1500 mm is **1,333 rpm — 37× under**. The two limits worsen in opposite directions, so no geometry closes it |
| **Rack and pinion** | Pitch-line velocity **is** 16.4 m/s against ~10 m/s practice (1.64× over), and it carries the drive load through **tooth contact at full speed in vacuum** — making **E21**'s open tribology gap the load path |
| **Staged spring** | **Works.** 537 J, 826 N peak, **21.1 g — inside the 25 g cap**, about **1.8 kg of steel**. Fails only on **C3 (commandability)** and **C5 (stores 537 J at rest)** |

**So the answer to "why the hardest actuator" is: against a screw the choice is forced, against a
rack it is well-founded, and against a spring it rests on exactly one criterion — that velocity is
commanded per shot rather than built in.**

**This narrows the product argument rather than supporting it.** A spring architecture needs no
sled, stator, bank, converter or sequencer, so it has almost none of the nine manifest-forfeiting
elements in `docs/FMEA.md` — it would score dramatically better on **E30**. **A four-stage spring
giving four discrete velocities at ~2 kg is a real competitor** for any mission not needing
continuous control, and nothing in this repository had acknowledged it.

**The honest position: VOLLEY buys continuous per-shot velocity control, and pays for it in mass,
complexity and shared-failure exposure.**

---

## 10 and 25, scoped rather than answered

**Both are qualification paths, not analyses, and pretending otherwise would be worse than saying
so.** Neither can be closed by computation; both need parts selection and test.

### 10 — contamination and outgassing

**Nothing exists.** `OPEN_PROBLEMS.md` **E11** records the absence of any contamination or
outgassing analysis and **E21** records that this repository contains nothing on lubrication, cold
welding or galling.

**A27 made E21 worse rather than better.** The actuator trade screened out a rack and pinion
*specifically because* a contacting drive at 16 m/s in vacuum would make the tribology gap the
load path. That reasoning only holds if the incumbent's own rolling contacts — four rollers, the
cassette follower leadscrew, the escapement — are benign, and **that has never been shown.**

**What the path looks like:** screen every non-metallic against ASTM E595 (**TML ≤ 1.0 %,
CVCM ≤ 0.10 %**), which the PEEK formers and any potting must meet; specify a vacuum-rated dry
lubricant for the rolling elements; and state a molecular contamination budget for the payload,
which matters because a CubeSat with an optical payload sits inside this machine for the whole
ascent. **Nothing in `cad/BOM.md` currently carries an outgassing spec at all.**

### 25 — radiation and single-event effects in the SiC drive

**Nothing exists**, and the converter is one of the manifest-forfeiting elements in `docs/FMEA.md`
— so an unqualified part here is not a degraded shot, it is the end of the campaign.

**SiC is not a neutral choice in this respect.** SiC MOSFETs are known to be susceptible to
single-event burnout at derated drain voltages, and the derating required is often severe. The
bus here is 96 V, which is modest, and that is the honest mitigating factor — but **derating
policy, part selection and a TID budget for the mission duration are all absent.**

**What the path looks like:** a TID budget from the orbit and duration (short, at LEO, so likely
undemanding), a SEE-qualified part selection with the drain derating stated, and single-event
burnout test data for the specific device. **None of this is analysis** — it is procurement and
test, and it belongs in `docs/QUALIFICATION_PLAN.md`, which does not currently mention radiation.

---

## The last five, worked 2026-08-10

Taken in dependency order rather than list order: **16 → 14 → 15 → 19 → 5**. Item 16 attacks a
loss the repository already concedes; its answer decides 14; 15 is what 16 points at; 19 only
bites if 15 is adopted; and 5 depends on what the product turns out to be.

### 16 — separating the mover from the payload. **Answered, and it is the cheapest fix available**

`analysis/mover_separation.py`. Field perpendicular to the array plane, reproducing
`PAYLOAD_ENVIRONMENT`'s own 251 mm figure as a cross-check:

| Standoff | \|B\| | × magnetometer FS | × Earth |
|---:|---:|---:|---:|
| 20 mm — where the payload sits today | 44.2 mT | **442×** | 983× |
| 100 mm | 306 µT | 3.1× | 6.8× |
| **251 mm** | 90 µT | **0.90× — usable** | 2.0× |
| **400 mm** | 23.7 µT | 0.24× | **0.53× — below Earth's field** |

**Yes, and by a wide margin.** Separation converts the field exposure from a fixed property of the
architecture into a design variable. At **251 mm the payload's magnetometer becomes usable**; at
**400 mm the satellite sees less than Earth's own field**, which also collapses the remanent-
magnetisation problem behind item 9 — *the* claim that "the satellite is never modified" currently
fails on.

**Perpendicular separation is not affordable** — the whole machine is 530 mm wide. **Longitudinal
separation is**, and it is what item 15 delivers for free: a payload carried *ahead* of the
magnets sits beyond the array's end, where an ideal Halbach's field is smaller still.

**This is the cheapest available fix to two conceded losses**, and no document in this repository
had evaluated it.

### 15 — an LSM tug reeved to a separate carriage. **Answered, and it also attacks P9**

Distinct from **PII-14**, which moved the motor off the vehicle entirely and was declined. Here
the linear motor **stays**; only the coupling changes. A reeving ratio *n* means the carriage
moves *n* times the tug's distance at *n* times its speed, for *n* times the force — and the
tug's inertia referred to the carriage falls as **1/n²**, which is the one favourable term and the
reason reeving is interesting at all.

| Ratio | Track length needed | Effective mass | Exit velocity | Tug speed |
|---:|---:|---:|---:|---:|
| 1:1 | 1.30 m | 15.45 kg | 15.29 m/s | 15.29 m/s |
| **2:1** | **0.65 m** | **8.36 kg** | **14.70 m/s** | 7.35 m/s |
| 3:1 | 0.43 m | 7.05 kg | 13.07 m/s | 4.36 m/s |

**A 2:1 reeving halves the acceleration zone — 1.30 m to 0.65 m — for 4 % of exit velocity**,
because the tug's 9.445 kg is divided by four. Against **P9**, where the closed envelope is
1839 mm and **44 % over the ESPA Grande class**, that is the only lever found so far that shortens
the machine without lengthening anything else.

**And it separates the payload from the magnets longitudinally at the same time**, which is
item 16's fix. **The two items are one architecture.**

**What it costs**, and none of it is analysed: a cable and pulleys in vacuum (item 19), a second
guided body, and a single tension load path. Recorded as **PII-15**.

### 14 — is zero modification actually necessary? **The claim is already compromised, and that changes the question**

**Item 9 settled the physics and the repository conceded it**: soft-magnetic parts inside the
payload leave *"permanently altered — a residual dipole perturbs attitude control for the rest of
the mission."* **A satellite that leaves permanently magnetised has been modified**, whatever the
mechanical interface says.

So the honest position is not "zero modification versus a small interface change". It is:

| | |
|---|---|
| **Today** | The satellite is modified — magnetically, invisibly, and without the customer's consent or knowledge |
| **With item 16's separation** | The satellite is genuinely unmodified, because the field never reaches it |
| **With a declared interface** | The satellite is modified, *knowingly*, to a written spec |

**The worst of the three is the current one**, because it is the only one where the modification is
undisclosed. **Item 16 is therefore not merely an optimisation — it is what makes the product
claim true**, and that reframing is the answer to item 14.

**A small interface change is not needed if separation works.** If it does not, the least-bad
alternative is a declared magnetic-cleanliness zone in the payload interface document, which is a
*specification* rather than a hardware modification. **No such document exists** (ADR-010 covers
mechanical mounting only), and E29 already asks for one for a different reason.

### 19 — cable in vacuum. **Gated behind 15, and the risks are named**

Only bites if a cable architecture is adopted. **PII-14 flagged it and did not analyse it**, and
**E21** records that this repository contains nothing on lubrication, cold welding or galling.

The specific risks, none quantified here: **fretting** at the pulley wrap under 12 reversing
cycles; **cold welding** of a bare steel cable on a bare steel sheave in vacuum; **lubricant**
selection with no outgassing budget (item 10); **pulley bearing life** at the rope speeds item 15
implies; and a **single tension load path** whose failure is one more of the manifest-forfeiting
elements in `docs/FMEA.md`.

**A27 makes this sharper, not softer.** The actuator trade screened out a rack and pinion
*specifically because* a contacting drive at 16 m/s in vacuum makes E21 load-bearing. **A cable
over a sheave is also a contacting drive at speed**, so item 15 cannot claim the exemption that
screened the rack out — it must answer the same objection.

### 5 — which specific customer has asked for this? **No answer, and the honest one is uncomfortable**

**None. No customer exists and none has been approached.**

`docs/MARKET.md` describes a segment, not a customer. Every cost claim in the project was withdrawn
for lack of a vendor quotation (**E3**). And the strongest technical findings of this review
narrow the addressable set rather than widen it:

- **A24** — the payload ladder closes kill criterion 1 only at **PocketQube** class, two rungs
  below where the repository had been claiming, and those classes have **no corner rails and no
  designed interface**;
- **A21** — at 3U a cold-gas module wins on mass by **7.5×**;
- **A27** — a **~2 kg staged spring** does the job for any mission not needing continuous control;
- **E30** — the reliability case only closes above **93.5 %** per-shot reliability, which is
  unmeasured.

**So the customer question cannot be answered until it is clear what is being sold.** On this
review's evidence that is: *continuous per-shot velocity control, to an operator distributing a
fleet from one release event, who values schedulability over mass.* **That is a narrower product
than "a better deployer", and it is the first time this repository has been able to state it in a
sentence.**

**What would close it:** approach one operator with that sentence and the review responses
attached, and record what they say — including if it is no. **That is not analysis and no further
analysis substitutes for it.**

## What this file changes

**Nothing yet.** It is a triage, not a set of results. Its purpose is to record — before any of
these are worked — which the repository can answer, which it cannot, and which it answers *against
itself*.

Three of the answers above are losses stated plainly: **the cold-gas module beats VOLLEY at 3U by
7.5×** (28), **the satellite leaves permanently magnetised** (9), and **a payload's magnetometer
is unusable inside the deployer** (7). All three predate this review and are in the repository's
own analyses, which is the only reason this file can be written honestly.

**Fourteen open items will be worked in the order of severity above, each with bands declared
before its analysis**, and the two lethal ones first.
