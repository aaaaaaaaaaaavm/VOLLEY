# Review responses

**A reviewer's register, answered or conceded, question by question.**

Thirty-five questions. Items 1–3, 7–8, 14–16 and 20–21 were raised in review by a former ISRO
scientist; the remainder is the register a reviewer of that background would be expected to
bring, written down in advance rather than waited for.

> **The honest aggregate, before any individual answer:**
>
> | | Count | Meaning |
> |---|---:|---|
> | **Answered** | **11** | An analysis or document exists, with a band declared before it ran |
> | **Partial** | **10** | Something exists; it does not fully answer the question as asked |
> | **Open** | **14** | **Nothing in this repository addresses it** |
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

**Closing it:** an FMEA with the jam case explicitly enumerated, a stated
single-failure-loses-N figure, and either a recovery mode or an accepted-risk statement with the
number attached. **None of this exists.**

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

### 30. Do launch vehicle ICDs even permit deployment at 16 m/s? — **OPEN, and it may be decisive**

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
| **10** | Contamination and outgassing from rails, bearings, cable, brake | **E11** (no contamination or outgassing analysis) and **E21** (nothing on lubrication, cold welding or galling) — both open | High |
| **11** | Does the array's residual dipole produce a secular magnetic torque on the host, and can the ACS null it? | **E29** covers the shot's *mechanical* angular impulse. The **magnetic** dipole torque is not modelled at all | High |
| **12** | Shock spectrum at the payload interface, at release and at brake engagement | A23 covers release *kinematics*; `grep -ri "shock spectrum"` returns nothing | High |
| **15** | Why not an LSM-driven tug beneath the track, cable-and-pulley to the carriage, EMALS-like with reversed tug motion? | **PII-14** assessed a cable-driven gondola on 2026-08-10 and declined it on margin — but that concept moves the motor *off* the vehicle entirely. **The tug variant, where the LSM stays and only the coupling changes, was not assessed** | Medium |
| **16** | Would separating the mover from the payload sled reduce field exposure and simplify the sled? | PII-11's side-rail layout and PII-14 both touch it. **Neither computes the field-exposure benefit**, which is the point of the question given 611× | **High** — it may be the cheapest fix to 7 and 9 |
| **18** | Why a linear motor at all, rather than a lead screw, rack-and-pinion, or staged spring? | Nothing. `grep -ri "lead screw"` and `"rack and pinion"` both return zero | **High** — an unmade top-level trade |
| **19** | Cable in vacuum: fretting, cold welding, lubricant, pulley bearing life at 16.4 m/s, single load path | PII-14 flags it as unresolved; E21 covers tribology generally | Medium — only bites if a cable architecture is adopted |
| **20** | How reliable is a system with this many failure points? | Nothing. No FMEA, no fault tree, no parts count | **High** |
| **22** | Sled jam loses the campaign | **Nothing** — see above | **Lethal** |
| **25** | Radiation and single-event-effect qualification for the SiC drive | Nothing | High |
| **26** | Multipaction and Paschen breakdown in the windings during ascent depressurisation | Nothing. **A 96 V bank switching hundreds of amps through a winding in a depressurising volume is a textbook Paschen case** | High |
| **30** | Do LV ICDs permit deployment at 16 m/s? | **Nothing** — see above | **Lethal** |

---

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
