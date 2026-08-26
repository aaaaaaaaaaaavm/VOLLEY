# Reference host cases for distributed orbital delivery

Opened 2026-08-26. This is a public-data reference-host study. Published facts are separated
from declared assumptions throughout. No provider engineering data is used, no provider has
supplied anything, and no compatibility claim is made anywhere in this file.

[`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) defines three host classes and says that no
launch provider has agreed to anything ([E5](../OPEN_PROBLEMS.md)). That leaves the host side of
the architecture described entirely in the abstract. This file is the method for taking one
actual, publicly documented propulsion architecture and asking what a stage built around it would
have to supply before it could fly the distributed-delivery mission, and it records the answer
in a form that a propulsion or launch-vehicle engineer can correct row by row.

The method is the deliverable. The first worked case is an example of the method, not the
subject of the file.

---

## 1. Purpose

Three questions, in order, and only the third is about any particular engine.

1. What does VOLLEY need from a host, stated as requirements rather than as a vehicle?
2. How would a reader decide whether a given real architecture meets them?
3. What happens when that procedure is run against one publicly documented case?

The answer to question 3 is never "yes" or "no". Public information about a propulsion system
cannot establish stage-level capability, and the useful output is a list of the specific numbers
a provider would have to supply, each with what it currently stands in for.

> ### What this file is not
>
> It is not a compatibility declaration, a launcher selection, an integration agreement, a
> partnership, provider-supplied host data, or a flight proposal. VOLLEY has no relationship with
> any launch provider, propulsion supplier or space agency, and nothing here creates one.

---

## 2. Host classes, carried forward unchanged

From [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 6. This file adds no classes
and changes none of them.

| | Class A | Class B | Class C |
|---|---|---|---|
| | Controlled spent upper stage kept alive as a platform | Restartable upper stage with a planned reserve | Non-restartable host |
| Attitude, navigation, power after primary | yes | yes | limited or none |
| Post-primary orbital manoeuvres | as reserve allows | planned, multiple | none |
| Rapid deployment | yes | yes | yes |
| Distributed delivery | limited by reserve | yes | no |
| Disposal | controlled or natural re-entry | controlled | natural |

Class A has a flown precedent in ISRO's use of spent PS4 stages as POEM orbital platforms, and
that precedent is recorded in the mission-architecture file with its evidence level. Class B has
no precedent recorded in this repository, which is why it is the class this file works.

Class C is the case VOLLEY has to survive, and it does. Nothing below is a requirement for VOLLEY
to exist.

---

## 3. Evaluation method

The same six steps for every case, in this order. Reordering them is how a study talks itself
into a conclusion.

1. Collect the public record and classify every claim by evidence class before using any of it.
2. Separate what the public record establishes about the engine from what it does not establish
   about the stage.
3. Declare every model input that the public record does not supply, as a VOLLEY assumption,
   with a sensitivity range, before any arithmetic runs.
4. Run the first-order propulsion model from those declared inputs.
5. Read the result as a statement about the assumptions, not about the engine.
6. Write down which provider datum would replace each assumption, so the study can be corrected
   rather than re-derived.

Step 6 is the one that makes the study worth publishing. A reader who knows the real numbers
should be able to reply by correcting rows.

---

## 4. Evidence rules

Every claim carries one of these classes, and they are not mixed.

| Class | What it means |
|---|---|
| COMPANY_STATED | The company states it publicly, in its own material or its own posts |
| COMPANY_TECHNICAL_PUBLICATION | A technical publication authored or co-authored by the company, or by a tool vendor writing about the company's own design work |
| THIRD_PARTY_TECHNICAL | An independent technical source with its own engineering content |
| SECONDARY_REPORTING | A press or trade report relaying a claim it did not verify |
| ASSUMPTION | A VOLLEY reference assumption. No source. It exists so the arithmetic has somewhere to start |

Two rules on top of the classes.

**A claim about a subsystem is not a claim about the system.** A demonstrated ignition subsystem
says what the igniter does. It says nothing about the engine around it, and the engine says
nothing about the stage around that.

**A retrieval limit is stated rather than hidden.** The primary pages below could not be
retrieved directly on the machine this study was run on, the same limit A9 and the
`celestrak.org` row in [`EXTERNAL_EVIDENCE.md`](EXTERNAL_EVIDENCE.md) already record. What is
recorded here is what search-result summaries of those pages returned, so every row's evidence
class is capped accordingly and says so. That is a weaker footing than a page read in full, and a
reader with access to the primary pages should treat the table as a draft to be corrected rather
than as a verified record.

---

## 5. What a Class-B host must supply

An engine is not a host. Even a propulsion system that restarts perfectly leaves every item below
unanswered, and each of them belongs to the stage rather than to the engine.

| | What VOLLEY needs it for |
|---|---|
| Propellant tanks and residual accounting | whether a post-primary reserve exists at all |
| Propellant management, pressurisation, ullage and settling | whether a restart can be commanded in free fall |
| Cryogenic thermal management | how long the campaign can last before the oxidiser decides it |
| Engine feed system and chill-down | the interval between restarts |
| Restart sequencing and command authority after primary separation | whether the stage will still take commands |
| Guidance, navigation and control | where the stage thinks it is when VOLLEY fires |
| Attitude control and its authority | [P94](../OPEN_PROBLEMS.md), and [A52](../validation/A52_gen6_recoil.md)'s requirement that the thrust line pass within 10.7 mm of the host centre of mass |
| Reaction control for fine manoeuvres | section 10 below, and it turns out to be the load-bearing one |
| Electrical power and communications | keeping VOLLEY commandable for the length of the campaign |
| Structural interface and VOLLEY mounting | [E31](../OPEN_PROBLEMS.md) |
| Collision avoidance during the campaign | [E18](../OPEN_PROBLEMS.md) |
| Disposal reserve and passivation | section 15, and [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 7 |

So the question this file asks is not whether a given engine can fly VOLLEY. It is:

> What would an upper stage built around a propulsion system of this class have to provide,
> before the distributed-delivery mission could be planned against it?

---

## 6. Reference case 1, an ANYA-class restartable semi-cryogenic stage

The first worked case is a stage built around the ANYA engine platform, which Thrustworks
Dynetics develops and describes publicly. It is used here because its public record is unusually
specific for an engine at this stage of development: a stated thrust class, a stated propellant
family, a stated architecture, and a separately reported ignition-system test campaign.

Throughout this section, *ANYA-class* means a propulsion system of the thrust and propellant
class the public record describes. It does not mean ANYA, and no figure computed in this file is
a statement about ANYA's performance.

### The reference architecture

```
PRIMARY ASCENT
  -> PRIMARY PAYLOAD SEPARATION            the primary customer is served, and served first
  -> POST-PRIMARY STAGE MODE               stage stays powered, navigated and commandable
  -> ANYA-CLASS RESTART                    first post-primary ignition, which is a restart
  -> COARSE REPOSITION                     altitude, phase, orbital energy
  -> ENGINE SHUTDOWN
  -> COAST / SETTLE / NAVIGATION           attitude and state established before release
  -> VOLLEY DEPLOYMENT BATCH               commanded per-satellite release velocity
  -> SAFE SEPARATION                       range and geometry established before the next burn
  -> NEXT RESTART -> NEXT REPOSITION -> NEXT BATCH
  -> DISPOSAL RESERVE                      budgeted before the first satellite left
  -> FINAL DISPOSAL BURN
  -> PASSIVATION
```

This maps to Class B, and the mapping is a study rather than a finding. An ANYA-class restartable
stage is examined here as a Class-B reference architecture under declared assumptions.

The two systems stay separate at every step. The engine changes the stage's orbit. VOLLEY
produces each satellite's release state relative to the stage. VOLLEY does not command the
engine, the engine is no part of Gen6's cold-gas deployment system, and neither substitutes for
the other.

---

## 7. Public facts, and what each one is worth

Every row states the claim as the source states it, not as VOLLEY would like to read it.

| Claim | Public source | Evidence class | Used as model input? |
|---|---|---|---|
| ANYA is a modular semi-cryogenic liquid rocket engine platform | company material and company posts, relayed by trade and press coverage | COMPANY_STATED, via SECONDARY_REPORTING | yes, as the propellant family |
| The platform is described at a 20 kN thrust class | company material, relayed by trade and press coverage | COMPANY_STATED, via SECONDARY_REPORTING | yes, as the thrust class. The source does not state whether 20 kN is sea-level or vacuum thrust |
| Propellants are LOX and kerosene | company material; the ignition tests are reported as KeroLOX | COMPANY_STATED, via SECONDARY_REPORTING | yes, as the propellant family only |
| The platform is designed for rapid customization, so a customer takes a configuration rather than commissioning a bespoke engine | company material, relayed in a July 2026 trade profile | COMPANY_STATED, via SECONDARY_REPORTING | no. It is why a platform is worth studying as a class rather than as one engine |
| Turbopump design work for ANYA was performed with a commercial turbomachinery design suite, published by that tool vendor | tool-vendor technical article about the company's own design work | COMPANY_TECHNICAL_PUBLICATION | no. It establishes a turbopump-fed architecture in development, and no performance figure |
| Thrust-to-weight ratio exceeding 110 | company material, relayed by trade coverage | COMPANY_STATED, via SECONDARY_REPORTING | no |
| Reusable | company material, relayed by trade coverage | COMPANY_STATED, via SECONDARY_REPORTING | no. Reusability is a recovery-and-refurbishment property and is not an on-orbit restart claim |
| 3D printed | company material, relayed by trade coverage | COMPANY_STATED, via SECONDARY_REPORTING | no |
| Thrust vectoring capability | trade coverage | SECONDARY_REPORTING | no |
| Engine subsystems have passed rapid start-stop testing | trade coverage | SECONDARY_REPORTING | no. Subsystem start-stop is not engine restart and is not stage restart |
| A resonance ignition system was validated in three consecutive KeroLOX hot-fire tests | company announcement, relayed by several outlets, August 2026 | COMPANY_STATED, via SECONDARY_REPORTING | no |
| Those ignition tests ran at an operating pressure of 5.08 bar gauge | company announcement, relayed by several outlets | COMPANY_STATED, via SECONDARY_REPORTING | no. This is an igniter test pressure and is not an engine chamber pressure |
| The igniter has zero moving parts and is driven entirely by internal propellant pressure | company announcement, relayed by several outlets | COMPANY_STATED, via SECONDARY_REPORTING | no |
| The igniter enables repeated restarts, reported as unlimited and including in vacuum | company announcement, relayed by several outlets | COMPANY_STATED, via SECONDARY_REPORTING | no. See the distinction below. This is the single most important row in the table |
| The ignition system is integrated into the ANYA platform | company announcement | COMPANY_STATED, via SECONDARY_REPORTING | no |
| A technology readiness level of 6 is claimed for the ignition system | trade coverage | SECONDARY_REPORTING | no. TRL is self-assessed unless an external body assigns it |
| Specific impulse and chamber pressure are not publicly disclosed | trade coverage states the performance figures are not disclosed | SECONDARY_REPORTING | not applicable. This is the absence that section 8 stands in for |

### The distinction the whole study depends on

> An igniter that restarts repeatedly is not an engine that restarts repeatedly, and neither is a
> stage that restarts repeatedly.
>
> The public claim is about the ignition subsystem: no moving parts, driven by propellant
> pressure, repeatable. Taken at face value, it removes one specific historical restart limit,
> the consumable pyrotechnic cartridge or the spark system and its power.
>
> Whole-engine restart additionally depends on turbomachinery restart and spin-up, thermal cycling
> of the chamber and nozzle, valve cycle life, propellant conditioning, feed-line chill-down,
> inlet conditions at ignition, and the ignition sequence itself. Stage restart then adds tank
> state, ullage, propellant settling, oxidiser management and the stage's own command authority.
>
> Converting the igniter claim into an engine or stage claim would be the largest single error
> available in this file, and it is the error this paragraph exists to prevent.

### On "reusable", "3D printed" and "high thrust-to-weight"

These are recorded above with their provenance rather than treated as design parameters. They are
company positioning statements relayed by trade press, and none of them is a qualified figure
from a test report. No number in this file descends from any of them.

---

## 8. Assumption ledger

Everything the public record does not supply, declared before the arithmetic and carried into
`analysis/host_reference.py` as named constants.

> Every value in the Baseline column below except thrust and propellant is a VOLLEY reference
> assumption. None of them is attributed to any engine, any stage or any provider. 300 s is not
> ANYA's specific impulse. 1000 kg is not an ANYA stage mass. 2 s is not ANYA's minimum burn. 4
> restarts is not ANYA's restart rating. These are numbers this project chose so that the model
> would run, and every one of them is wrong by an unknown amount.

| Quantity | Baseline | Sensitivity | Status |
|---|---|---|---|
| Thrust | 20 kN | 15 to 30 kN | PUBLIC class figure, condition unstated. Sensitivity is a VOLLEY assumption |
| Propellant | LOX / kerosene | fixed for this case | PUBLIC |
| Vacuum specific impulse | 300 s | 285 to 320 s | VOLLEY ASSUMPTION. No public figure exists |
| Deep throttling | none credited | optional sensitivity only | UNKNOWN. Nothing public establishes a throttle envelope |
| Planned post-primary restarts | 4 | 2 to 8 | VOLLEY ASSUMPTION. No public engine restart rating exists |
| Contingency restart | +1 | | VOLLEY ASSUMPTION |
| Minimum stable useful burn | 2 s | 0.5 to 5 s | VOLLEY ASSUMPTION. No public figure exists |
| Minimum coast between burns | 10 min | 2 to 30 min | VOLLEY ASSUMPTION. No public figure exists |
| Post-primary campaign duration | 4 h | 1 to 12 h | VOLLEY ASSUMPTION. No public cryogenic coast limit exists |
| Reference post-primary stage mass | 1000 kg | 500 to 3000 kg | VOLLEY ASSUMPTION. No public stage exists to have a mass |
| Usable post-primary propellant | 150 kg | not swept | VOLLEY ASSUMPTION |
| Disposal reserve | 20 % of usable post-primary propellant | 10 to 30 % | VOLLEY ASSUMPTION |
| Plane-change mission | excluded, priced only | | ARCHITECTURE RULE, from MISSION_ARCHITECTURE.md section 5 |
| Deployment mode | batches | 2, 3, 4 and 12 compared | VOLLEY ASSUMPTION |

---

## 9. First-order propulsion model

`analysis/host_reference.py`. Constant thrust, constant specific impulse, impulsive-equivalent,
no gravity loss, no steering loss, no throttling. Closed forms only, no solver, no fitted
constant.

```
g0   = 9.80665 m/s^2                          standard gravity, exact by definition
mdot = F / (Isp * g0)                         mass flow
dv   = Isp * g0 * ln(m0 / mf)                 rocket equation
mp   = m0 * (1 - exp(-dv / (Isp * g0)))       propellant for a manoeuvre
tb   = mp / mdot                              burn duration
dv(t)= Isp * g0 * ln(m0 / (m0 - mdot * t))    what a burn of length t buys
```

At 20 kN and an assumed 300 s, mass flow is 6.80 kg/s.

Burn duration, seconds, at the assumed 300 s specific impulse:

| Stage mass | 5 m/s | 10 m/s | 20 m/s | 40 m/s | 100 m/s |
|---:|---:|---:|---:|---:|---:|
| 500 kg | 0.12 | 0.25 | 0.50 | 0.99 | 2.46 |
| 1000 kg | 0.25 | 0.50 | 1.00 | 1.99 | 4.92 |
| 2000 kg | 0.50 | 1.00 | 1.99 | 3.97 | 9.83 |
| 3000 kg | 0.75 | 1.50 | 2.99 | 5.96 | 14.75 |

Propellant, kilograms, over the same grid at 300 s:

| Stage mass | 5 m/s | 10 m/s | 20 m/s | 40 m/s | 100 m/s |
|---:|---:|---:|---:|---:|---:|
| 500 kg | 0.85 | 1.70 | 3.39 | 6.75 | 16.7 |
| 1000 kg | 1.70 | 3.39 | 6.78 | 13.5 | 33.4 |
| 2000 kg | 3.40 | 6.79 | 13.6 | 27.0 | 66.8 |
| 3000 kg | 5.09 | 10.2 | 20.3 | 40.5 | 100.3 |

Across 285, 300 and 320 s the propellant for a 20 m/s manoeuvre on a 1000 kg stage moves from
7.13 to 6.78 to 6.35 kg, and the burn duration stays at 1.00 s to three figures in all three
cases. That is not a coincidence: propellant scales as 1/Isp and so does mass flow, so burn
duration for a given manoeuvre and stage mass is very nearly independent of specific impulse.

> The softest assumption in the ledger is the one with the least influence on the result that
> matters. The 300 s figure moves propellant mass by about six per cent across its range and
> moves burn duration by almost nothing, so section 10's finding does not rest on it.

---

## 10. The minimum-burn problem

This is the principal result of the study, and it was computed rather than assumed. The question
is whether a 20 kN engine can command the small manoeuvres a distributed-delivery campaign needs,
or only the large ones.

What the assumed 2 s minimum stable burn buys, per stage mass, against a 5 m/s fine manoeuvre:

| Stage mass | Minimum burn | Smallest commandable manoeuvre | Equivalent altitude step at 500 km | Overshoot against 5 m/s | Burn needed for 5 m/s |
|---:|---:|---:|---:|---:|---:|
| 500 kg | 2 s | 81.1 m/s | 147 km | 16.2x | 0.12 s |
| 1000 kg | 2 s | 40.3 m/s | 73 km | 8.1x | 0.25 s |
| 2000 kg | 2 s | 20.1 m/s | 36 km | 4.0x | 0.50 s |
| 3000 kg | 2 s | 13.4 m/s | 24 km | 2.7x | 0.75 s |

What shorter burns buy, at the 1000 kg reference:

| Burn | 500 kg | 1000 kg | 2000 kg | 3000 kg |
|---:|---:|---:|---:|---:|
| 0.5 s | 20.1 m/s | 10.0 m/s | 5.0 m/s | 3.3 m/s |
| 1 s | 40.3 | 20.1 | 10.0 | 6.7 |
| 2 s | 81.1 | 40.3 | 20.1 | 13.4 |
| 5 s | 207.1 | 101.7 | 50.4 | 33.5 |

### What this says

At the declared reference point a 20 kN engine is a coarse actuator and nothing else. On a
1000 kg stage the smallest manoeuvre a 2 s burn can command is 40 m/s, which is a 73 km altitude
step. The mission's fine end, a 10 km shell adjustment at about 5.5 m/s, needs a burn of roughly
a quarter of a second, which is below any minimum burn this study is willing to assume.

The overshoot closes with stage mass and never disappears. Even at 3000 kg the floor is 13.4 m/s,
2.7 times the fine manoeuvre.

So the architecture that falls out is a three-way split rather than a two-way one:

| | |
|---|---|
| Main engine, ANYA-class | coarse orbital-energy change, shell to shell, tens of m/s and up |
| Reaction control or auxiliary stage propulsion | small corrections, settling, attitude, the metres-per-second end |
| VOLLEY | the final commanded per-satellite release state |

This is a cleaner architecture than the one the study started with, and it was not the expected
answer. It also means the host requirement list in section 5 has a load-bearing row that the
engine discussion does not touch at all: a Class-B host needs usable reaction control, and its
authority is [P94](../OPEN_PROBLEMS.md), which is already live and already `HOST_DATA`.

Three ways this conclusion could be wrong, each of them a provider datum: the minimum stable burn
could be far below 2 s; the engine could throttle deeply; or the stage could be much heavier than
1000 kg. The table above is built so that a reader who knows any of those three can read the
answer off it directly.

---

## 11. Mission cases

Disposal reserve is removed first. Customer manoeuvres spend what is left. At the assumed 150 kg
usable and 20 % reserve, that leaves 120 kg for customers.

| Case | Post-primary restarts | Total dv | Propellant | Margin against the 120 kg budget |
|---|---:|---:|---:|---:|
| A, rapid deployment | 0 | 0 | 0 kg | 120 kg |
| B, moderate distributed delivery | 3 | 60 m/s | 20.2 kg | 99.8 kg |
| C, upper-bound sensitivity | 5 | 200 m/s | 65.7 kg | 54.3 kg |

**Case A matters most.** It uses no post-primary restart at all, and it works on every host class
including C. VOLLEY does not require a restartable host to exist, and every capability discussed
in this file is an extension of a product that already functions without it. That is the finding
this study most needed to confirm and it is easy to lose sight of in a document about engines.

**Case B** is three 20 m/s repositions with a deployment batch after each. On the declared
assumptions propellant is not the binding constraint, at 17 % of the customer budget. Time is.

**Case C** is a longer campaign at 40 m/s per leg. It is not a recommended mission. It exists to
show which constraint starts to bind first as the campaign grows, and the answer is not propellant.

### The constraint that binds first is time, and it is not the restart interval

The assumed 10 minute coast between burns makes case B a 30 minute campaign, which is misleading.
A phasing or altitude campaign is paced by the orbit, not by the engine: at 500 km the orbital
period is 94.6 minutes, and each reposition-and-deploy leg realistically occupies at least one
orbit for navigation, attitude and safe separation.

| Case | Coast floor at 10 min per restart | Paced at one orbit per leg |
|---|---:|---:|
| B | 0.5 h | 4.7 h |
| C | 0.8 h | 7.9 h |

Case B at one orbit per leg already exceeds the 4 h campaign reference in the assumption ledger.
That is a tension between two VOLLEY assumptions rather than a finding about any engine, and it
is exactly the kind of thing a declared ledger is supposed to expose. What resolves it is a
stage cryogenic coast limit, which is section 13 and which nobody has published.

### Plane change stays priced and stays excluded

Re-derived in `analysis/host_reference.py` rather than quoted, and it reproduces
[`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 5 exactly.

| Altitude | Circular v | 1 degree of inclination | 0.1 degree | 10 km coplanar raise | Ratio |
|---:|---:|---:|---:|---:|---:|
| 350 km | 7697.0 m/s | 134.3 m/s | 13.4 m/s | 5.71 m/s | 23.5 |
| 500 km | 7612.6 m/s | 132.9 m/s | 13.3 m/s | 5.53 m/s | 24.0 |
| 700 km | 7504.3 m/s | 131.0 m/s | 13.1 m/s | 5.30 m/s | 24.7 |

One degree of inclination costs about twenty-four times a ten-kilometre altitude change. On the
assumed 120 kg customer budget a single degree at 500 km would consume roughly a third of it, and
the campaign would end with one plane and no shells.

> The existence of a 20 kN engine is not a reason to widen the product into arbitrary plane
> changes. The architecture rule stands: distributed delivery supplies altitude, phase and orbital
> energy. A restartable host makes the coplanar campaign better and does not make the plane
> change affordable.

---

## 12. Batch deployment

Twelve satellites, 20 m/s per reposition, no burn needed before the first batch.

| Batches | Satellites per batch | Restarts | Total dv | Propellant | Coast floor |
|---:|---:|---:|---:|---:|---:|
| 12 | 1 | 11 | 220 m/s | 72.1 kg | 1.8 h |
| 4 | 3 | 3 | 60 m/s | 20.2 kg | 0.5 h |
| 3 | 4 | 2 | 40 m/s | 13.5 kg | 0.3 h |
| 2 | 6 | 1 | 20 m/s | 6.8 kg | 0.2 h |

Burning between every satellite costs 72.1 kg against 20.2 kg for four batches, which is 60 % of
the assumed customer budget against 17 %, for eleven restarts against three. Paced at one orbit
per leg it is a 17 hour campaign against a 4.7 hour one, and it puts eleven thermal cycles and
eleven propellant-management cycles through a stage nobody has designed.

The comparison is deliberately posed to be unfair to batching: it holds the per-burn manoeuvre
fixed, so more burns buy more total separation as well as costing more. Batching still wins, and
it wins on every axis at once.

> What batching does not cost is the product. VOLLEY supplies a commanded velocity per satellite
> inside every batch, so satellites released together still separate from each other. Batching
> reduces the number of distinct stage orbits, not the number of distinct satellite trajectories.
> [A15](../validation/A15_poem_campaign.md) and [P56](../OPEN_PROBLEMS.md) already record that
> release timing alone gives in-track phase at zero dv.

---

## 13. Cryogenic coast and restart accounting

### The oxidiser sets the campaign limit

Kerosene storage over hours is straightforward. Liquid oxygen is not, and it drives heat leak,
boil-off, tank pressure and venting, stratification, slosh, restart inlet conditions and
feed-line chill-down. For a stage that must restart after coasting, the oxidiser's thermal state
at ignition is the thing that decides whether the restart is available.

Nothing public establishes an ANYA-class cryogenic coast capability, and this file does not invent
one. What can be said parametrically:

| Campaign duration | What it would allow, on the assumptions above | What it needs |
|---|---|---|
| 1 h | roughly one reposition and deploy leg | little coast management |
| 4 h | case B, at one orbit per leg, marginally | a stated boil-off rate and tank pressure history |
| 12 h | case C with margin | active or passive thermal control and a vent policy, both stage design |

None of the three can be chosen from public data. What would settle it is a stage-level cryogenic
design limit, and it is a provider datum in section 17.

> A campaign lasting several days must not be claimed for an ANYA-class reference stage from the
> present public evidence, and this file does not claim it. The multi-day distributed campaign in
> [A50](../validation/A50_campaign_altitude.md) is a Class-A study on a stage with no cryogenic
> oxidiser, and it does not transfer here.

### Start against restart, counted properly

If the engine has already fired during ascent or injection, the first post-primary ignition is a
restart and not a start. Four different counts are involved and they are routinely conflated.

| Count | Case B, on the declared assumptions | Established by public evidence? |
|---|---:|---|
| Total engine starts across the flight | 5: one ascent start, three repositions, one disposal burn | no |
| Post-primary restarts | 4, which is three repositions plus the disposal burn, and the ledger holds one more in contingency | no |
| Resonance igniter cycles | at least 5, one per start, and more if any start sequence retries | three, on the ground, for the subsystem alone |
| Full-engine thermal cycles | 5 | no |

Note that the disposal burn is a restart and is counted as one. A campaign planned against three
repositions needs four post-primary ignitions, not three, and a mission that budgets restarts by
counting deployment legs will be one short at exactly the moment it cannot afford to be.

The igniter row is the only one with any public evidence behind it, and it is a ground count on a
subsystem. Igniter cycles are not engine restart life, and the assumed four planned restarts plus
one contingency stand in for a qualified restart count that does not exist publicly.

---

## 14. Deployment and plume sequencing

A satellite released from VOLLEY must not be followed immediately by a large engine restart. The
released satellite is close, slow relative to the stage, and has no propulsion of its own. What
the sequence needs, and none of it exists yet:

| Requirement | Status |
|---|---|
| Minimum time between last release and next ignition | HOST_DATA, and a mission-planner input that does not exist |
| Minimum range at ignition | HOST_DATA, follows from release velocity and the time above |
| Plume exclusion cone and its half-angle | HOST_DATA. A property of the engine and nozzle, not computable here |
| Contamination limit for the released spacecraft | HOST_DATA, and a customer requirement as much as a host one |
| Conjunction geometry across the campaign | [E18](../OPEN_PROBLEMS.md), live, and the covariance behind it is currently invented |
| Stage attitude before ignition | [P94](../OPEN_PROBLEMS.md) and [P99](../OPEN_PROBLEMS.md), both live |

No plume impingement distance is stated in this file, and none should be inferred from it.
Inventing one would be worse than leaving it blank, because a blank is visibly a gap and a number
is not.

Two things can be said without provider data. The released satellite's separation velocity is
VOLLEY's own and is known: at Gen6's current design point it is 29.009 m/s, so range grows by
about 1.7 km per minute, which makes range the easy part of the problem. And batching helps here
too, because it reduces the number of times the sequence has to be executed at all.

---

## 15. Disposal reserve

No reference mission spends the last of the stage's propellant on customers. The reserve is
removed first and the campaign is planned against what remains.

At the assumed 150 kg usable post-primary propellant and 1000 kg stage:

| Reserve | Reserve mass | Customer mass | Customer dv available | dv held for disposal |
|---:|---:|---:|---:|---:|
| 10 % | 15.0 kg | 135.0 kg | 427 m/s | 51 m/s |
| 20 % | 30.0 kg | 120.0 kg | 376 m/s | 102 m/s |
| 30 % | 45.0 kg | 105.0 kg | 326 m/s | 152 m/s |

> A percentage reserve is a budgeting rule and not a disposal capability. Whether 102 m/s actually
> deorbits the stage depends on the orbit it ends the campaign in, the stage's ballistic
> coefficient and the applicable disposal rule, none of which is specified here. This table says
> what is held back. It does not say that disposal is achievable, and no row in it should be read
> as a compliance statement.

Every case in section 11 fits inside the 20 % reserve with margin, which says more about the
assumed 150 kg than about any engine.

---

## 16. Result

Under the declared assumptions, an ANYA-class restartable semi-cryogenic propulsion system is a
useful Class-B reference case for VOLLEY's distributed-delivery architecture. The public record
establishes a customizable 20 kN LOX/kerosene engine platform and a repeatedly fired resonance
ignition subsystem. It does not establish the stage-level restart, coast, throttling,
propellant-management or disposal envelope needed to claim compatibility. Those remain explicit
provider-data inputs.

Three things the study itself produced, which are properties of the assumptions rather than of any
engine:

1. At this thrust class the main engine is a coarse actuator. On a 1000 kg stage the smallest
   manoeuvre a 2 s burn can command is 40 m/s. Fine stage corrections need reaction control, and
   the three-way split in section 10 is the cleaner architecture for it.
2. Batching wins on every axis. Four batches against one burn per satellite is 20.2 kg against
   72.1 kg, three restarts against eleven, and it costs nothing the customer buys.
3. Propellant is not the binding constraint on a moderate campaign. Time is, and the limit is
   cryogenic rather than propulsive.

### What is not concluded

This file does not say that ANYA is compatible with VOLLEY, that any provider will power VOLLEY,
that VOLLEY will use any named engine, that ANYA supports four restarts, that ANYA has a 300 s
specific impulse, that an ANYA-class stage can remain in orbit for four hours, that any company
has reviewed or approved this concept, or that any collaboration or partnership exists. None of
those is established and several of them are not the kind of claim public information can
establish.

### What it changes in the repository, which is one thing

[P113](../OPEN_PROBLEMS.md) is opened: how the orbital work divides between host and deployer has
never been computed, and it sets VOLLEY's release-velocity requirement. A capable Class-B host
performs more of the orbital-energy change, which may mean VOLLEY needs a smaller commanded
release velocity than Gen6's current 29.009 m/s.

> That entry is written with a warning attached, and the warning belongs here too. A lower release
> velocity would reduce chamber pressure, acceleration, contact severity and tip-off sensitivity,
> which makes this trade a tempting route to making [P108](../OPEN_PROBLEMS.md) look smaller
> without answering it. **Nothing in this file lowers the Gen6 requirement, and P108 is
> unresolved.** The tip-off magnitude is not established, A72 has not been run, and the coupled
> trade is recorded for computation on its own merits, later and separately.

Gen6's design point is unchanged. The Fusion package in
[`GEN6_FUSION_BUILD_PACKAGE.md`](GEN6_FUSION_BUILD_PACKAGE.md) remains the current CAD handoff.

---

## 17. What provider data would replace

The point of the file. A reviewer who knows the real numbers should be able to correct rows here
rather than reconstruct the study.

| Unknown | Current assumption | Why it matters | What provider data replaces it |
|---|---|---|---|
| Vacuum specific impulse | 300 s | propellant budget for the whole campaign | design-point or certified vacuum Isp |
| Thrust condition | 20 kN, condition unstated | whether the class figure is the one the model should use | vacuum thrust at the design mixture ratio |
| Minimum stable burn | 2 s | the minimum-impulse result in section 10, which is the study's main finding | demonstrated or qualified minimum burn duration |
| Throttle range | none credited | whether the main engine can reach small manoeuvres at all | qualified throttle envelope and its minimum power level |
| Engine restart life | 4 planned, 1 contingency | campaign architecture and batch count | demonstrated or qualified restart count, and what limits it |
| Coast interval between restarts | 10 min | campaign sequencing | restart thermal and propellant-conditioning envelope |
| Maximum coast duration | 4 h reference | whether a multi-orbit campaign closes at all | stage cryogenic design limit and boil-off rate |
| Post-primary stage mass | 1000 kg | burn duration and every table in section 9 | actual stage dry and wet mass at primary separation |
| Usable post-primary propellant | 150 kg | the customer budget | reserved or characterised residual a provider will commit |
| Settling and ullage requirement | unknown | whether a restart can be commanded in free fall | ullage requirement and settling method |
| Disposal reserve | 20 % assumed | mission closure | provider mission policy and reserve rule |
| Plume exclusion | unknown | safe restart after a deployment | plume and contamination constraint, and its geometry |
| Attitude control authority | unknown | [P94](../OPEN_PROBLEMS.md), and A52's 10.7 mm alignment requirement | RCS authority, and its minimum impulse bit |
| Host structural interface | unknown | [E31](../OPEN_PROBLEMS.md), whether VOLLEY mounts at all | interface control data |
| Post-primary command authority | assumed available | whether the stage takes commands after passivation would normally begin | operations policy and telemetry and command availability |

None of these is closed by this file, and [E5](../OPEN_PROBLEMS.md) stays open. Public company
information can establish an engine class, a nominal thrust, a propellant family, a modularity
claim and the existence of an ignition technology. It cannot establish stage propellant reserve,
host control authority, restart qualification, coast limit or flight interface, and those are
what the mission needs.

---

## 18. Template for future reference cases

Any further case is added to this file under the same headings. It does not get its own document,
because a per-provider document is how a methodology turns into a catalogue.

Populate every field, and write UNKNOWN rather than leaving one blank. A blank reads as an
oversight and UNKNOWN reads as a finding.

| Field | What to record |
|---|---|
| Propulsion type | cycle, feed system, propellant family |
| Thrust | value, and whether sea-level or vacuum, and whether stated or inferred |
| Specific impulse | value and condition, or UNKNOWN |
| Restart capability | stated at which level: igniter, engine or stage. These are three different claims |
| Minimum impulse or minimum burn | value, or UNKNOWN, and its effect on the fine end of the manoeuvre range |
| Throttle | envelope and minimum power level, or UNKNOWN |
| Stage mass | dry and wet at primary separation, or UNKNOWN |
| Usable post-primary propellant | reserved or characterised residual, or UNKNOWN |
| Attitude authority | RCS type, authority, minimum impulse bit |
| Coast lifetime | maximum coast before restart is unavailable, and what limits it |
| Propellant management | ullage, settling, pressurisation, thermal control |
| Disposal | reserve policy, and whether controlled re-entry is achievable from the campaign's end orbit |
| Structural interface | mounting provision for a hosted system, and its published interface data |
| Deployment constraints | plume exclusion, contamination, minimum range and time after release |
| Source confidence | the evidence class of every row above, using section 4's classes |
| Host class mapped | A, B or C, and stated as a study under declared assumptions rather than as a compatibility finding |

Then run `analysis/host_reference.py` with the case's constants, and report the minimum-burn table
first. It has been the most informative output for the one case run so far, and it is the output
least sensitive to the assumption most likely to be wrong.

---

## Reproducibility

Every computed number in this file comes from `analysis/host_reference.py`, which reads no
network, imports no deployer model, and writes `analysis/results/host_reference.json`. It is
covered by [`tools/check_results_fresh.py`](../tools/check_results_fresh.py), so a change to the
script that does not reach this document is caught on the next commit.

The script's self-test checks nine identities: that the rocket equation and the burn-time inverse
agree, that mass flow reproduces thrust from the definition of specific impulse, that burn time
rises with stage mass, that propellant falls as specific impulse rises, that delivered dv rises
with burn length, that reserve plus customer propellant equals the usable total on every row, that
customer dv falls as reserve rises, that the inverted minimum burn reproduces the manoeuvre it was
solved for, and that the plane-change re-derivation reproduces
[`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 5 to within 0.1 m/s.

Sources are references. Calculations run from committed assumptions, and no gate in this
repository reaches the public internet.
