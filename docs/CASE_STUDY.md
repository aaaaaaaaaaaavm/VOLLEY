# The case for VOLLEY

**Written for an operator, not for a reviewer.** Every number traces to an analysis in this
repository, and the losses are stated in the same voice as the wins — because an operator who
finds the losses themselves will discount the wins too.

> **The product, in one sentence.**
> **Continuous per-shot velocity control, to an operator distributing a fleet from one release
> event, who values schedulability over mass.**
>
> That sentence is narrower than "a better CubeSat deployer", and it is narrow **because** of what
> the analysis found rather than in spite of it. Everything below either supports it or bounds it.

---

## 1. The customer, concretely

**Not** a single CubeSat buying a ride. For one satellite going where the launch was going anyway,
a spring is the correct answer and this project does not dispute it — see §5.

**The customer is an operator placing a fleet into one plane, who needs it usable on a schedule.**
Specifically, someone for whom all three of these are true:

1. **Several satellites, one release event.** The value is *differential* velocity between
   satellites, and a single satellite has nothing to be differential against.
2. **Along-track distribution matters, and when it completes matters.** If the constellation can
   take a month to drift into place, drag is free and VOLLEY is unjustifiable.
3. **The satellites carry no propulsion.** About 92 % of flown CubeSats do not. If they have
   propulsion, they can phase themselves and the deployer is irrelevant.

**No such customer has been approached.** That is the honest state (review item 5), and it is the
single largest open item in this project that no further analysis can close.

---

## 2. The worked case

**Twelve 3U satellites, one plane, 30° spacing, from one release event at 450 km.**

| Distribution method | Time to 30° of phase |
|---|---:|
| **Differential drag** — what a spring-deployed fleet must use | **25.0 days** |
| Commanded differential, 2 m/s | 6.9 days |
| Commanded differential, 5 m/s | 2.8 days |
| **Commanded differential, 10 m/s** | **1.4 days** |

*(`analysis/astro.py`, `seeding()`.)*

**The constellation is usable roughly 24 days sooner.** That is the product. It is not a velocity
number and not an efficiency number — it is a **schedule** number, and it is the only axis on
which nothing else available competes.

**And each satellite lives longer**, because lifetime extension is superlinear in Δv:

| | Orbital life at 450 km | Fleet, 12 satellites |
|---|---:|---:|
| No deployer boost | 1.30 yr | 15.7 yr |
| Spring, 2.5 m/s | 1.41 yr | 16.9 yr |
| **VOLLEY, 16.388 m/s** | **2.11 yr** | **25.3 yr** |

**+49 % of orbital life per satellite**, on hardware the customer does not modify.

**Two ways to read that ratio, and the honest one is the second.** On *lifetime extension* — the
gain against an unboosted satellite — VOLLEY is **7.52×** a spring. On **delivered orbital life**,
which is what a risk-weighted comparison uses, it is **1.495×**. Both are true. The second is the
one an operator should plan with.

---

## 3. Why the alternatives do not do this job

**Each of these is a real competitor and each beats VOLLEY somewhere.** They are listed with the
axis they win on, not without it.

| Alternative | Where it beats VOLLEY | Why it cannot do *this* job |
|---|---|---|
| **Spring dispenser** | **Maturity (TRL 9 vs 2–3), reliability, simplicity.** A ~1.8 kg spring reaches the same 16.4 m/s within the g-cap (A27) | **Its designed differential is exactly zero.** Every satellite gets the same push, so the fleet can only phase by drag — 25 days, and not schedulable |
| **Differential drag** | **Free**, and it has flown on a 12-satellite constellation | 25 days, and it needs differential ballistic coefficient — attitude control or deployable area — **which is itself a satellite modification** |
| **Cold-gas module** | **Mass, by 7.5× at 3U** (A21, declared as a loss before the run) | Puts a **pressure vessel, a propulsion system and a regulatory path on the customer's satellite.** VOLLEY's whole proposition is that the satellite carries nothing |
| **Orbital transfer vehicle** | **Δv, by hundreds of m/s.** It can change plane; VOLLEY cannot at any price (133 m/s per degree) | **Over-specified for a job needing ~16 m/s**, and it makes the customer buy a spacecraft. Right-sizing is the argument, not superiority |

**No cost comparison is offered against any of them.** Every cost claim in this project was
withdrawn for lack of a vendor quotation (E3). An operator should assume VOLLEY is more expensive
than a spring until shown otherwise.

---

## 4. What it costs the customer

| | |
|---|---|
| **Satellite modification** | **None mechanically** — no armature, no plating, no electrical interface |
| **Magnetic environment** | **Severe, and currently a real cost.** 61 mT at the near face — **611× a magnetometer's full scale.** A magnetometer cannot be used inside the deployer, and **soft-magnetic parts leave permanently magnetised** |
| **Acceleration** | **10.53 g**, against the 25 g CubeSat Design Specification cap — 42 % of it |
| **Deployer mass per satellite** | **6.375 kg at 3U.** A cold-gas module is 0.5–1.2 kg |
| **Maturity** | **TRL 2–3. Nothing has been built, fired or measured at any scale** |

**The magnetic environment is the item an operator should press hardest on**, and there is a known
fix that is not yet in the design: **E35** shows that moving the payload to **400 mm** of standoff
puts the field **below Earth's own**, which removes both problems at once. Until that is designed,
the "never modified" claim is compromised — the satellite *is* modified, magnetically and
invisibly.

---

## 5. Where this argument stops

**Stated here rather than left to be discovered.**

- **At 3U against a cold-gas module, VOLLEY loses on mass by 7.5×.** The answer is smaller
  classes — but **A24 found the payload ladder closes kill criterion 1 only at PocketQube scale**,
  two rungs lower than this project used to claim, and those classes have no corner rails and no
  designed interface yet.
- **Reliability is unproven and the bar is specific.** The architecture puts twelve satellites
  behind one shared mechanism: **nine of thirteen elements forfeit the remaining manifest on a
  single failure**, against zero for a spring dispenser. **The design needs r ≥ 0.99326 per
  element per cycle** to beat a spring on delivered life. **r is unmeasured.** Until it is
  measured, this project cannot claim to beat a spring, and does not.
- **The bank cannot source the shot on purchasable cells** (P26). A flywheel clears the ceiling
  (A25) at mass parity, and is not designed.
- **The thrust constant is 4.42 % optimistic** (P46) and the correction is computed and held
  pending an independent check.
- **The campaign window is short.** At a real POEM altitude, mission life is **29–36 days**
  (E28), and a launch interface imposes a **seven-day hold** before secondary deployments (E31).

**None of these is hidden in an appendix.** They are in `OPEN_PROBLEMS.md` with numbers, and the
same discipline that produced the wins above produced these.

---

## 6. What would have to be true

For an operator to buy this, four things must become true, in this order:

1. **A measured thrust constant.** Everything descends from a field model checked only
   *analytic against analytic*. [`B1_ORDER.md`](B1_ORDER.md) is a ₹22,000 bench experiment that
   changes the category of evidence. **It has not been ordered.**
2. **A measured per-shot reliability**, from cycle-life testing of the escapement, gate and sled.
   This is the number the whole comparison against a spring turns on.
3. **The payload separated from the magnets**, so "never modified" is true rather than nearly true.
4. **One operator's answer to the sentence at the top of this file** — including if it is no.

**Items 1 and 2 are metal. Item 3 is design. Item 4 is a conversation.** No further analysis
substitutes for any of them, and this repository has reached the point where more analysis is the
wrong thing to do next.

---

## The one-paragraph version

*A fleet of propulsion-less CubeSats released from a single rideshare must either accept the orbit
it inherits or wait about a month for atmospheric drag to spread it along track. VOLLEY replaces
the spring with a linear motor that gives every satellite a separately commanded exit velocity, so
a twelve-satellite plane reaches 30° of spacing in **1.4 days instead of 25**, and each satellite
gains **49 % of orbital life**, without carrying propulsion, a pressure vessel, or any
modification. It is heavier than a cold-gas module, less mature than a spring, and has never been
built. What it offers that neither can is a constellation that is usable on a schedule.*
