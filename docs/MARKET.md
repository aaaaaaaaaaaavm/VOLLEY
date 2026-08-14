# The market this is aimed at, and where it does not reach

**What this file is.** A positioning argument, written because the technical documents do not
make one and a reader outside the field cannot reconstruct it from a thrust constant. It sits
outside the paper deliberately: an IEEE reviewer expects motivation from the technical gap and
reads a market section as padding, while an aerospace company or a recruiter reads exactly this.

**What it is not.** Evidence about the machine. Every figure below is either a third-party market
projection or a count of what has already flown, and neither says anything about whether VOLLEY
works. The engineering record is [`BASELINE.md`](BASELINE.md) and
[`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md), and the last section here is where this design loses.

---

## 1. Satellites got small, and then they got numerous

The shift is easiest to see in one pair of numbers rather than a history. Over 2026–2035,
Novaspace forecasts **16,900 satellites under 500 kg**, which is about **33 % of everything
launched but roughly 6 % of the launched mass**. Small satellites now dominate the *count* while
large ones still dominate the *tonnage*. The industry did not stop building large spacecraft; it
added an order of magnitude more small ones underneath them.

The installed base is already there. The Nanosats Database lists **more than 4,800 nanosatellites
and CubeSats** as of 1 January 2026, from **88 countries** that have launched and operated one.
Cumulative launches reached **2,714 by 2024**, of which about **95 % reached orbit** (2,381 of
2,505 attempts).

**One number in that database matters more than the totals, and it is the one this project
exists for: about 222 of those spacecraft carry propulsion.** Roughly eight percent. The other
ninety-two go wherever the rideshare put them and stay there.

## 2. The trade that produced the shift, argued rather than asserted

Neither architecture is simply better. They fail differently, and the failure mode is the whole
argument.

| | One large satellite | A constellation of small ones |
|---|---|---|
| Capability per spacecraft | High. Aperture, power and pointing all scale with mass | Low, individually |
| Design life | Long, and the technology is frozen at launch | Short, and the fleet refreshes as units are replaced |
| Upgrade path | None after launch | Continuous, by replacement |
| A single failure | Loses the mission | Degrades the service |
| Revisit and coverage | Limited by one orbit | Set by how the fleet is *distributed* |
| Cost of getting it wrong | Total | Bounded by one unit |

The last two rows are where the deployment problem comes from. A single satellite has no
distribution problem: it goes to its orbit and the mission is defined by that orbit. **A
constellation is only a constellation once its members are separated**, and separation is a
service nobody sells.

## 3. The gap, which is a range of velocity nobody serves

| | What it delivers | What it costs the customer |
|---|---|---|
| Spring deployer (P-POD class and successors) | 1–2 m/s, fixed, one value for every satellite | Nothing. It is the standard interface |
| **This regime** | **2–20 m/s, commanded per satellite** | **Nothing on the satellite** |
| Cold-gas or electric propulsion module | Tens to hundreds of m/s | 0.5–1.2 kg, a pressure vessel, a qualification campaign, range-safety review, and an attitude control system able to point it |
| Orbital transfer vehicle (D-Orbit, Impulse, Momentus, Exolaunch, Launcher/Vast, Exotrail, Bellatrix, Skyroot) | Hundreds to thousands of m/s | A spacecraft's worth of mass, cost and schedule, and the velocity is shared by everything aboard |

The spring standard has not moved in twenty years and delivers a velocity too small to change an
orbit usefully. The propulsive options begin an order of magnitude above what phasing a
constellation needs, and every one of them requires the satellite to *carry* something.

The middle is empty, and the 92 % of flown CubeSats without propulsion are the evidence that it
is: those operators did not decline propulsion because they had no use for orbital control. They
declined it because the smallest available step was a propulsion system.

**One 16.5 m/s ejection multiplies a propulsion-less satellite's orbital lifetime by 1.62 at mean
solar activity, and differential ejection at 2–10 m/s establishes 30° of constellation spacing in
1.4–6.9 days against about 25 days for differential-drag phasing.** Those two numbers are what
the gap is worth, they come from [`RESULTS.md`](RESULTS.md), and the lifetime one has an
independent propagator behind it that **disagrees at low solar activity** — which is why it is
quoted at a stated activity level and not claimed invariant.

**Stated as a ratio against the incumbent** ([A21](../validation/A21_comparators.md)): **7.52×
the orbital lifetime extension of the fastest published spring**, 9.45× against a typical one, at
**mass parity** per satellite — and against a designed inter-satellite differential of **zero**,
which is what a spring can command.

### And the product is not a deployer, it is a delivery vehicle

[`CONCEPT.md`](CONCEPT.md) states the concept this market section was written without: **a spent
upper stage that, after primary separation, repositions on its own reaction control between
altitude shells and fires satellites off at commanded velocities at each, then deorbits.** The
stage is being thrown away regardless; VOLLEY converts that interval into deliveries.

**With the boundary attached**, from [A20](../validation/A20_reachable_envelope.md): altitude
shells cost **27.8 m/s each** and are real propellant; along-track distribution is free and is
VOLLEY's own job; RAAN separation is free from differential J2; **and plane change is excluded
entirely at 133 m/s per degree.** Above ~100 m/s of host budget the *stage* supplies most of the
altitude range, so the honest division is that the host buys range and VOLLEY buys distribution
within it.

### Against transfer vehicles: right-sizing, not superiority

An OTV changes planes, rendezvouses, and delivers hundreds of m/s. **VOLLEY does none of that and
should not claim to.** The argument is that a constellation needing phase and altitude separation
does not need a spacecraft's worth of propulsion to get it, and an OTV makes the customer buy
exactly that — with the Δv shared across everything aboard. **No cost comparison is offered**,
because there is no OTV price here and no quotation for VOLLEY.

## 4. Market size, and why these figures are the weakest thing on this page

**These are third-party market projections, not measurements, and they disagree with each
other.** They are reported here with that disagreement visible, the same way every other number
in this repository carries its provenance.

| Source | CubeSat market 2026 | Projected 2033 | CAGR |
|---|---|---|---|
| Grand View Research | | USD 1.65 B | 15.6 % |
| SkyQuest | | USD 1.83 B | 15.9 % |
| Persistence Market Research | USD 612 M | USD 1.78 B | 16.5 % |
| Research and Markets | USD 593 M | | |
| SNS Insider | | USD 1.98 B | 18.3 % |

A spread of 15.6 to 18.3 % CAGR and USD 1.65 to 1.98 B on the same market in the same year is a
fair indication of how much weight any single one of them will carry. **The useful content is the
direction and the order of magnitude**: a market of hundreds of millions today, growing at
something in the mid-to-high teens, in a segment where the deployment interface has not changed
in twenty years.

Note also what the addressable share of that is. VOLLEY sells to the *deployment* line, not to
the satellite, and that line is a small fraction of the number above. Nothing here has been
built into a revenue model, and doing so would require quotations this project does not have —
`analysis/cost.py` prices the hardware with **no vendor quotation on any line item**.

## 5. Where this loses, taken from the defect list rather than omitted

A market document that argues one way is a brochure. These come from
[`KILL_CRITERIA.md`](KILL_CRITERIA.md) and [`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md):

- **At 3U it loses to a cold-gas module on mass by about 8x.** 7.042 kg of deployer per satellite
  against 0.5–1.2 kg for a module delivering the same velocity. That threshold is **crossed**, and
  the answer is payload class rather than engineering: at PocketQube the machine spends 0.24 kg
  per satellite and wins by 2 to 5x ([`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md)). No cassette,
  cradle or gate exists for any class except 3U.
- **The pulse-power chain does not close on purchasable cells.** The bank is specified at an ESR
  no commercial cell of that capacitance achieves, and the shot fails at a realistic value
  (P26). Fixing it costs four parallel strings, four times the cell cost and mass.
- **The envelope exceeds its target class by 44 %** (P9), which limits what host it can fly on.
- **Nothing has been measured.** Every number in this repository is a model output. Two results
  carry an independent cross-check; one of those, the lifetime invariance, **failed**.
- **The velocity is not the selling point and should not be sold as one.** It is 16.5 m/s, set by
  a qualification limit rather than by the motor, and it does not improve with payload class.
  What is on offer is *programmability* per satellite, which no spring provides.
- **No cost advantage is claimed over anything**, and A21 band 7 records why: `analysis/cost.py`
  carries no vendor quotation on any line item and no price exists here for any alternative.
  Closing that needs **E3**, not analysis.

### The argument at the small end, which is different and stronger

The product is not the same at every payload class, and the repository has not said so:

| Class | What the customer is buying |
|---|---|
| **3U / 6U** | Per-satellite commanded velocity. Mass per satellite is at parity with a dispenser and loses to a propulsion module by 7.5× |
| **1U / PocketQube** | Distribution at volume. Deployer mass per satellite falls by up to 30×, which is where the commercial case actually closes |
| **ChipSat / femtosat** | **A designed dispersion across a swarm.** Individual velocity control stops meaning anything; what matters is the *shape* of the velocity distribution across hundreds of units — and **no other deployer can produce one**, because every alternative gives every unit the same push |

The last row is the strongest claim in this file and the least designed: until 2026-08 no
cassette, cradle or gate existed for any class except 3U.

## 6. What would actually establish the case

In order of how much each would change a reader's mind, and none of it is done:

1. **A measured thrust constant on a bench.** The single largest credibility gap
   ([`PROVENANCE.md`](PROVENANCE.md)); the hardware for it is specified in the B-1 purchase order.
2. **The lifetime multiplier against flown data** rather than against another propagator. A9
   specifies it; its data source is unreachable from this environment.
3. **A small-payload cassette**, which is what converts the strongest commercial number on this
   page from arithmetic into a design.
4. **An operator willing to say what per-satellite phasing is worth to them.** Everything above
   infers demand from the absence of an alternative, and that is an argument, not a data point.

---

## Sources

All accessed 2026-07-31.

- Nanosats Database (Erik Kulu), counts as of 1 January 2026: <https://www.nanosats.eu/>
- Novaspace, *Prospects for the Small Satellite Market*, 11th edition, 16,900 smallsats and the
  33 % / 6 % count-versus-mass split over 2026–2035:
  <https://nova.space/press-release/global-smallsat-deployment-accelerates-with-16900-satellites-projected-through-2035/>
  and <https://spacenews.com/global-smallsat-deployment-accelerates-with-16900-satellites-projected-through-2035/>
- CubeSat market projections: Grand View Research, SkyQuest, Persistence Market Research,
  Research and Markets, SNS Insider, as tabulated. **Vendor market research, not measurement.**
- Cold-gas module masses: published COTS ranges, **not a quotation**
- Orbital transfer vehicle operators: public product pages, listed in VOLLEY-lab's PII-8
- Everything about this machine: `analysis/`, via [`BASELINE.md`](BASELINE.md)
