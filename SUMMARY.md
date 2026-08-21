# VOLLEY: one page

**Adityavardhan Mishra** · Dept. of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune
· [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com)
· [full repository](https://github.com/aaaaaaaaaaaavm/VOLLEY)

---

## Where the design is going, in one paragraph

**Everything below describes Gen5, which is the measured baseline and the record of what a
self-contained deployer costs.** On 2026-08-14 five analyses replaced the design target
([ADR-032](docs/adr/032-gen6-stage-integrated-gas-store.md)): **Gen6 is the payload accelerated
directly, by gas, along a rail the spent stage provides.** No mover, no pulse-power chain, no
brake, no return stroke. **29.75 kg is deleted, 43.33 kg becomes stage structure, 11.45 kg of
containment and ~3 kg of gas store remain** — added mass per satellite **1.608 kg** against an
unchanged 2 kg threshold, while **dry mass per satellite still crosses at 10.547 kg** and both are
reported together. Nothing in it is measured, the fluid system is unsized, and no launch provider
has agreed to lend a stage.

---

## The idea

Rideshare CubeSats inherit the orbit of whoever paid for the launch. Spring deployers release
them at **1-2 m/s**, which is far too little to change that orbit; orbital transfer vehicles
can change it, but they cost hundreds of m/s of propulsion and a spacecraft to carry it.
Between those sits an unserved regime.

**VOLLEY is a magazine-fed linear synchronous motor** that mounts on a rideshare upper stage
and ejects **unmodified** 3U CubeSats, no armature, no plating, no electrical interface on
the customer satellite, at a **velocity programmable per satellite**. Twelve satellites feed
from two transverse cassettes onto a reusable permanent-magnet sled running a 1.5 m ironless
double-sided Halbach track, arrested by a contactless eddy brake and powered from a
supercapacitor bank.

One shot buys a propulsion-less satellite **1.60x its orbital lifetime**, or seeds 30° of
a **28.8 km rise in semi-major axis** and **+60.2 % of orbital life**, which no amount of waiting and no spring at any preload can reach (A21-R bands R5, R6). Phase spacing is *not* the claim: 30° of in-track separation costs **468 seconds of waiting** between releases and no velocity at all (**P56**).

> **The comparison that matters, computed rather than quoted** ([A21](validation/A21_comparators.md)).
> Against the fastest published spring VOLLEY is 6.4× on *velocity* — but **7.33× on orbital
> lifetime extension**, because lifetime is superlinear in Δv (+60.2 % against +8.2 %); against a
> typical 2 m/s spring it is **9.45×**. **But read that ratio with E30 attached:** 7.33× is a
> ratio of *gains*, and on **delivered orbital life** the ratio is **1.495×** — which is the
> number a risk-weighted comparison uses, because a satellite that is never released delivers
> nothing. Deployer mass per 3U satellite is **1.758× a
> canisterised dispenser**, 10.547 kg against ~6 kg — **A21 band 4 failed on 2026-08-16 and the
> parity claim is withdrawn** (P69). And a spring's **designed
> differential between satellites is exactly zero**, so a spring-deployed fleet phases only by
> drag — 25 days, unschedulable — against VOLLEY's **1.38 days**.
>
> **Where it loses, on the same footing:** a cold-gas module beats VOLLEY on mass at 3U by
> **8.3×**; a spring beats it on maturity by TRL 9 against TRL 2–3. **No cost comparison is
> made against anything** — there is no vendor quotation on any line of `analysis/cost.py`.

## The numbers, with their caveats attached

| | | |
|---|---|---|
| Exit velocity, 3U | **16.0 m/s at 10.1 g** | **6.4x the fastest published spring** (NRCSD-E specifies 0.5-2.5 m/s; the widely quoted "8x" is against 2 m/s and is the softer comparison). The ceiling is the payload's g-limit, not the machine: 25.3 m/s at the 25 g cap, see [`VELOCITY_CEILING.md`](docs/VELOCITY_CEILING.md). From a sled mass computed from CAD solid volumes (9.445 kg), not estimated, the earlier 4.86 kg parametric estimate gave 20.4 m/s |
| Velocity dispersion | **0.0274 m/s (3σ)** | Closed-loop, at a 15.8 m/s setpoint. Rests on *assumed* sensor noise (E7), the differentiator, and the least validated part |
| Thrust constant | **10.54 N per kA/m** | Winding-resolved, and **independently computed by a meshed magnetostatic FEM to 0.03 %**, a PDE solve, not another superposition |
| Energy per shot | **2.78 kJ gross, 2.74 kJ net**, 18.8 % electrical-to-payload net of regeneration | Under one watt-hour. 47 J of the sled's 1213 J comes back through the **39 mm** regenerative section ADR-030 left after P28; the brake takes the other **1162 J**. [A11](validation/A11_regen_braking.md) measured 291.4 J against the 240 mm section that decision removed — **P97** |
| System mass | **126.6 kg dry**, 174.6 kg loaded | **10.55 kg of deployer per 3U satellite**, the same class as canisterized dispensers at ~2 kg/U |
| Under ADR-032 | **11.45 kg added**, the rest deleted or supplied by the stage | **1.608 kg per 3U satellite added** — the 2 kg threshold is unchanged and dry mass still crosses it |
| Recurring hardware | ~₹1.35 M per unit, ₹112 k per satellite | **Every price assumed, no quotations.** Useful part: avionics + energy storage are ~42 % of cost and the magnet set only ~5 %, which holds even at 2x price errors |
| Envelope | 1839 mm closed | **Exceeds the ESPA-Grande class by ~44 %.** Open packaging problem (P9) |

> **Open as of 2026-07-30:** the supercapacitor bank is modelled at an ESR no commercial cell
> of that capacitance achieves, and the shot does not close at a realistic value (**P26**). The
> velocity and dispersion figures are unaffected, the bank sizing is. Not quietly re-sized.

**Maturity: TRL 2-3. Nothing has been built, fired, or measured.** **Twenty-four run sheets**
exist, each against an acceptance band declared *before* the run — and the results are mixed on
purpose:

| | |
|---|---|
| **A5 FAILED** | an independent propagator falsified an invariance claim that was in the paper's own abstract (P16) |
| **A12** | found the inter-array force feeding the structural FEA **37 % high** — and that the explanation first written for it was backwards |
| **A6** | returned three rows **void**: the quantity they tested does not exist at these separations |
| **A13 FAILED / corrected** | transient return rate still misses rows 3 and 4, but the ideal residual rate is zero; the former 18.1 s cadence floor is superseded, while attitude restoration and structural settling remain open (E25) |
| A1, A4, A10, A11, A12 | passed, partially or fully, with every miss logged; the ngspice A8 run now predates the corrected operating point |

**A9 (decay against flown CubeSats) is outstanding**, and it is the only analysis anywhere in this
project that compares the model against something that actually happened — blocked by network
policy rather than by difficulty. **A7** is superseded in substance by **A23**, which modelled the
release rather than bounding it, though the multibody run A7 specifies has still never happened.

| | |
|---|---|
| **A22** | resized the retention gates from D6 to **D9** after A18 found the sizing case was wrong; margin at Q = 30 goes **−0.36 → +0.45** for **11 g**, and no longer depends on the unmeasured damping |
| **A23** | found the release itself is comfortable — 12.2 ms of coast at zero force — but that the payload **arrives in its cradle at 36–231 °/s**, 18–115× the tip-off band, which nothing had modelled (**P41**) |
| **A20** | priced the delivery envelope: **27.8 m/s per 50 km shell**, and above ~100 m/s of host budget the *stage* supplies most of the altitude range, not VOLLEY |
| **A21** | replaced the headline: **7.33×** a spring on lifetime extension, not 6.4× on velocity — and **withdrew any cost claim**, since no line of `cost.py` carries a quotation |

## Where it sits against what flies

| | Î”v | Programmable | Satellite mods | Status |
|---|---|---|---|---|
| Spring deployers, P-POD, ISIPOD, **Dhruva DSOD** | 1-2 m/s | no | none | flown, thousands deployed |
| **VOLLEY** | 16.0 m/s | **yes** | **none** | design study |
| Transfer vehicles, ION, Vigoride | 100s m/s | yes | mounting | flown, commercial |

Dhruva Space's DSOD is the closest comparator and it already flies, space-qualified on
PSLV-C53 and C55, non-pyrotechnic release, and instrumented to *measure* ejection velocity on
orbit. What it cannot do is exceed 2 m/s or vary velocity per satellite. That gap is the
entire argument for this machine, and it is narrower than "electromagnetic beats springs".

## Host integration, worked against real vehicles

The interface asks four things of any host: mass and control authority, a 150-300 W recharge
feed, a serial command link, and an authorized firing window.

- **ISRO's POEM** is the flown precedent, a spent PS4 operated as a three-axis-stabilized
  hosted platform, retired by controlled reentry. Its zero-debris closeout is the regulatory
  template.
- **Skyroot's Vikram-1** carries a restartable Orbit Adjustment Module stage-tested through
  more than a thousand pulses. A loaded VOLLEY is **34 %** of the published 350 kg LEO
  capacity, falling to **22 %** and **13 %** on the announced 550 kg and 900 kg variants, so
  early flights are dedicated demonstrations and later ones ordinary manifest items.

> **Campaign mission life, added 2026-08-06.** A GMAT propagation of the full twelve-satellite
> campaign reaches 90 days at 450 km but only **29 to 36 days at 350 km**, where the satellites
> reenter. POEM missions have operated near 350 km, so a campaign hosted there is a **month-long**
> product. Logged as **E28**; nothing in this project previously modelled campaign duration.

Recoil is the satellite's momentum only, **64.1 N·s** per shot, nulled by a few grams of cold
gas.

## How far along it actually is

**Four subsystems are frozen as designs and analysed against bands declared before the
analyses ran** — stator, sled, magazine, host interface. **Three are frozen but under-analysed**
— track, avionics, payload cell. **The brake is genuinely provisional**: its pole plates were
lightened on structural reasoning alone and no magnetic sizing has been done. **The energy store
is a known negative result with a candidate fix** — the supercapacitor bank cannot source the
shot on purchasable parts (P26), and a flywheel clears the ceiling at mass parity (A25).

**Most of what remains is computation, not metal**, and that cuts both ways: the design is
further along than a TRL label suggests, and *"everything computable is done"* is **not yet
true**. [`docs/BUILD_READINESS.md`](docs/BUILD_READINESS.md) says which is which, subsystem by
subsystem, and names the least finished one rather than leaving it to be found.

**Nothing has been built, fired, or measured at any scale.** Twenty-four validation runs exist;
**zero measurements** do. The field model has only ever been checked *analytic against
analytic*. The order that changes that costs **₹22,000**, has had a bill of materials since
2026-07-30, and has not been placed —
[`docs/B1_ORDER.md`](docs/B1_ORDER.md).

## What makes this repository worth opening

Every defect found in this work is published, numbered, and tracked, including the ones that
damage its own claims. Acceptance bands are declared in writing **before** each analysis runs,
so a failure cannot be rationalised afterwards. Four errors were found in the paper by
rebuilding its analysis from scratch. An independent propagator (GMAT) then **falsified a
claim in the paper's own abstract**, and that is recorded as P16 rather than quietly dropped.
The scripts are authoritative over the paper, never the reverse.

**Three times a declared band has caught a bug in the analysis rather than a problem in the
design** (A19, A20, A2) — most recently a 57 % normalisation error that would otherwise have
been reported as a plausible-looking result. That is what declaring bands first is for, and it
is the strongest evidence here that the numbers were not fitted to the conclusion.

**[`docs/BUILD_READINESS.md`](docs/BUILD_READINESS.md)**: subsystem by subsystem, what is settled and whether the rest needs computation or metal
**[`docs/PROGRAMME.md`](docs/PROGRAMME.md)**: the four repositories of this programme
**[`docs/BASELINE.md`](docs/BASELINE.md)**: what is frozen, and what may move it
**[`docs/GEN4_STATUS.md`](docs/GEN4_STATUS.md)**: what exists in the provisional open assembly, and what is not yet calculated
**[`docs/ROADMAP.md`](docs/ROADMAP.md)**: what happens next, and when
**[`docs/HISTORY.md`](docs/HISTORY.md)**: the project since 2021, and how this git history was built
**[`docs/QUALIFICATION_PLAN.md`](docs/QUALIFICATION_PLAN.md)**: the test campaign, specified
**[`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md)**: every known defect
**[`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md)**: every claim, independently checked where possible
**[`docs/PROVENANCE.md`](docs/PROVENANCE.md)**: read this before citing anything
