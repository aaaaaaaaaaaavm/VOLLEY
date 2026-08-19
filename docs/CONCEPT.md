# What VOLLEY actually is: a last-mile delivery vehicle, not a bigger spring

> ## Extended 2026-08-14 by [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
>
> **This file already had the idea and stopped one step short of it.** §2 argues that a spent
> stage is a waste rather than a necessity, and then treats it as a *host* — something VOLLEY is
> mounted on.
>
> **ADR-032 takes the step: the stage is not the host, it is the machine.** Its structure is the
> rail, its skin and avionics are the enclosure, and the deployer is what gets added —
> **11.45 kg of containment and about 3 kg of gas store.**
>
> Four constraints dissolve rather than improve: the 44 % envelope overrun (nothing is stowed), the
> deployable-structure precision that killed PII-8 and PII-11 (no airgap, so millimetres rather
> than ppm), the supercapacitor bank no supplier sells, and the acceleration length that
> capped velocity at 1.30 m.
>
> **What it does not dissolve** is that no launch provider has agreed to any of it. Everything
> below stands; the concept is the same and the vehicle it runs on has moved from *beside the
> stage* to *the stage*.

**Written 2026-08-10.** This repository has always described the machine and rarely the
concept. Every document opens with a linear synchronous motor and works outward, which is the
right order for an engineer and the wrong order for anyone asking why the thing should exist.

**The idea came first and it is not about the motor.**

---

## 1. The problem, in one sentence

**A rideshare CubeSat does not choose its orbit. It inherits whoever paid for the launch.**

The spring that ejects it delivers 1–2 m/s, which exists to create clearance from the stage, not
to change an orbit. Satellites carrying propulsion can correct for this. **About 222 of the 4,800+
catalogued nanosatellites do — roughly eight percent.** The other ninety-two percent go where the
manifest put them and stay there.

That is not a deployment problem. It is a **distribution** problem, and a constellation is only a
constellation once its members are distributed.

## 2. The idea: the stage that was going to burn up anyway

A launch vehicle's upper stage does its job in about ten minutes and then becomes debris. It is
deorbited, or it is left to decay. Either way the mass, the structure, the attitude control and
the residual propellant are thrown away.

**POEM is the proof that this is a waste rather than a necessity.** It is a spent PSLV fourth
stage operated as a stabilised platform after its job is done, with power, navigation, attitude
thrusters and a controlled reentry at the end. The precedent for stage reuse is flown.

**VOLLEY is what you put on it to make the reuse worth something.**

> ### The concept, stated plainly
>
> **After the primary payload separates, the spent stage stops being debris and becomes a
> last-mile delivery vehicle.** It repositions on its own reaction-control system between
> deployments — altitude shell to altitude shell — and at each station VOLLEY fires satellites
> off it at individually commanded velocities. When the magazine is empty the stage makes its
> final burn and reenters.
>
> The satellites are never modified. Nothing is bolted to them, plated onto them, or wired into
> them. They arrive as they would have arrived at a spring, and they leave at a velocity chosen
> for each one.

This is the difference between a *deployer* and a *delivery vehicle*. A deployer releases
satellites where the host already is. A delivery vehicle takes them somewhere.

## 3. Two configurations

### 3.1 Hosted — VOLLEY on a spent stage

The stage is doing something it was going to do anyway: exist in orbit for a while and then
deorbit. VOLLEY converts that interval into deliveries.

| Phase | What happens |
|---|---|
| Primary separation | The stage's contracted job ends |
| Station 1 | Attitude hold; VOLLEY fires *n* satellites at commanded velocities |
| Reposition | RCS burn to the next altitude shell |
| Stations 2…*k* | Repeat until the magazine is empty |
| Disposal | Final burn, controlled reentry |

**The economics of this are unusual and worth stating.** The stage, its attitude control and its
disposal burn are all paid for by the primary mission. VOLLEY's marginal cost to the launch is
its own mass and the recharge feed. **It is a payload that rides for the price of a payload and
delivers like a transfer vehicle over a narrow band.**

### 3.2 Dedicated — VOLLEY as the whole payload

On a small launcher, VOLLEY *is* the mission. The vehicle's job is to put one 126.6 kg machine
into a parking orbit; the machine then distributes its manifest. There is no primary customer
whose orbit everyone else inherits, because there is no primary customer.

This is the configuration where the phrase that started the project applies most literally: the
launcher delivers the cannon, and the cannon delivers the satellites.

### 3.3 Two operating modes, and they cut across both configurations

**Hosted and dedicated is *where* the machine sits. This is *when* it fires**, and the difference
matters more to a customer than the configuration does.

| | **Deploy-on-arrival** | **Loiter-and-distribute** |
|---|---|---|
| **What happens** | All twelve out shortly after insertion, then disposal | The stage stays up, repositions between altitude shells on residual propellant, and fires at each station |
| **What the customer buys** | Twelve satellites in one orbit at commanded velocities | Twelve satellites across **several** orbits from one launch |
| **What it asks of the stage** | Minutes to hours of life past its contracted job | **Weeks to months**, and an owner willing to grant them |
| **What ends it** | The disposal burn | **Drag** — and see below |

**Loiter-and-distribute is the mode this concept exists for**, and it is the one
[ADR-002](adr/002-host-is-a-spent-upper-stage.md) pointed at in 2023 when it made the stage the
host rather than a free-flyer.

> **The boundary on it is measured, not assumed, and it is tighter than it looks.**
>
> **Altitude repositioning is cheap. Plane change is not** — **133 m/s per degree**, A15 band 8,
> against a whole shot of 16 m/s. The concept is altitude shells plus J2 doing the plane work over
> time, not a vehicle that flies to arbitrary orbits.
>
> **And duration is bought with altitude.** **E28** found the fleet reenters in **29–36 days at
> 350 km**, with only the 450 km case surviving 90.
>
> **[A50](../validation/A50_campaign_altitude.md) modelled it on 2026-08-16.** Satellite life is
> **476.6 days at 450 km**, and walking three 50 km shells costs **≈ 55 m/s** — inside every host
> budget A20 swept. **Days, weeks and months are all purchasable from 450 km upward, and orbital
> mechanics is not the constraint on loiter. The stage keep-alive agreement is.**
>
> **And E28's central trade turns out not to be one.** Across 350 → 450 km the 90-day plane spread
> moves **47.1° → 44.6°, about 5 %, while satellite life changes by 6.7×.** At the shell spacing
> this architecture uses, spread is nearly altitude-independent and life is not — **so the design
> rule is simply to go higher.**
>
> **Read those durations as upper bounds.** A50's decay model gives **70.6 days at 350 km** against
> the 29–36 the GMAT runs observed, because `astro.py`'s atmosphere is static — **P79**. E28 stays
> open until the model is checked against a variable atmosphere.

## 4. What the concept can and cannot do, quantified

**The honest boundary matters more than the pitch**, and this project has already established
both halves of it.

| Manoeuvre | Cost | Available? |
|---|---|---|
| **Altitude shell change**, 50 km | **27.8 m/s**, two-burn Hohmann at LEO | **Yes**, but it is a real propellant bill — see A20 |
| **Phase / along-track spacing** | free; it is what differential velocity produces | **Yes** — this is VOLLEY's own job |
| **RAAN separation** | free, over time, from differential J2 | **Yes** — A15 measured **367°** of nodal spread in 90 days |
| **Inclination change**, 1° | **133 m/s** — A15 band 8 | **No.** 8.1× VOLLEY's entire shot, and beyond a spent stage's RCS |

**Plane change is not on the menu and this project says so everywhere.** One shot spent entirely
on plane change buys **0.1229°**, confirmed twice — once analytically and once in GMAT. Any
framing that implies orbit-plane selection is false.

**What is on the menu is altitude, phase, and — given time — RAAN.** The last one is the
interesting result: `validation/A15_poem_campaign.md` found that satellites left at different
semi-major axes decay at different rates, their nodes regress at different rates, and the spread
compounds. **367° of relative nodal position over 90 days**, from a perturbation the deployer does
not control and does not pay for.

So the delivery envelope is: **a set of altitude shells reachable by the stage's own RCS, a
commanded along-track distribution within each shell, and plane separation that develops for
free over the campaign.** `validation/A20_reachable_envelope.md` quantifies it against a host Δv
budget.

## 5. Why this is not an orbital transfer vehicle, and should not claim to be

An OTV carries satellites to a destination using hundreds to thousands of m/s of propulsion. It
changes planes. It rendezvouses. **VOLLEY does none of that and cannot.**

**The argument is right-sizing, not superiority.** A constellation that needs its members spread
in phase and altitude does not need a spacecraft's worth of propulsion to do it — and an OTV
makes the customer buy exactly that, plus its mass, cost and schedule, with the Δv shared across
everything aboard. **VOLLEY is sized for the job that is actually being asked for**, and the job
is smaller than the tool the market currently offers for it.

`docs/LANDSCAPE.md` puts it correctly: not the same market.

## 6. Why not just use a spring

Because a spring gives every satellite the same push, and **distribution requires a
*difference*.**

| | Spring | VOLLEY |
|---|---|---|
| Velocity | 1–2 m/s, one value for every satellite | **16.029 m/s**, commanded per cell |
| Designed differential between satellites | **zero** — any spread is manufacturing scatter | up to the full range, resolvable to 0.0274 m/s (3σ) |
| Orbital lifetime extension | +6.5 % at 2 m/s, +8.2 % at 2.5 m/s | **+60.2 %** |
| 30° of in-track phase | **468 s of waiting — free** | 468 s of waiting, identically. **No advantage (P56)** | 1.4 days at 10 m/s of commanded differential |
| Deployer mass per 3U satellite | ~6 kg, canisterised class | **10.547 kg** |

**The lifetime figure is the one to read, not the velocity ratio.** VOLLEY is 6.4× a spring on
raw Δv but **7.3–9.2× on what that Δv actually buys**, because lifetime extension is superlinear
in this regime. And the differential row has no ratio at all: it is a capability springs do not
have, at any price.

**Mass is at parity.** That is the part that surprises people — a magazine-fed electromagnetic
launcher lands in the same kilograms-per-satellite class as a canister of springs.

> **Where it loses, because a page that only argues one way is a brochure.** A spring is TRL 9
> with thousands of deployments; VOLLEY is TRL 2–3 with **nothing built or measured (E4)**. A
> spring asks its host for one deploy signal; VOLLEY asks for 150–300 W, a serial link and an
> authorised firing window. A spring has one failure mode; VOLLEY has a motor, a bank, a sled, an
> escapement and a gate. At 3U a customer who is willing to modify their satellite can fit a
> 0.5–1.2 kg cold-gas module and beat VOLLEY on mass by about 8×.

## 7. How the payload class changes the product

The argument is not the same at every size, and that is worth saying because the repository's
economics turn on it.

| Class | What the customer is buying |
|---|---|
| **3U / 6U** | Per-satellite commanded velocity. Low count, high value each. Mass per satellite is at parity with a dispenser and loses to a propulsion module |
| **1U / PocketQube** | Distribution at volume. Deployer mass per satellite falls by up to 30×, which is where the commercial argument actually closes |
| **ChipSat / femtosat** | **A designed dispersion across a swarm.** Individual velocity control stops being meaningful; what matters is the *shape* of the velocity distribution across hundreds of units — and no other deployer can produce one, because every alternative gives every unit the same push |

`docs/PAYLOAD_CLASSES.md` carries the numbers. The ladder is the strongest commercial argument in
the project and it is the least designed: until 2026-08 no cassette, cradle or gate existed for
any class except 3U.

---

## What this document is not

**Evidence.** Nothing here is measured. The concept rests on a machine that exists as models and
CAD, and `OPEN_PROBLEMS.md` lists what is still open about it. The delivery envelope in §4 is
computed from `analysis/astro.py`; the comparison in §6 from [`../validation/A21_comparators.md`](../validation/A21_comparators.md); the
plane-change ceiling from `validation/A15_poem_campaign.md`, which is the one row here an
independent propagator has confirmed.

**What would have to happen before any of this flies is a build-readiness question, and it is
answered subsystem by subsystem in the Phase I close rather than here.**
