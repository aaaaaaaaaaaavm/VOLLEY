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

> ### Corrected 2026-08-26, the same day it was first published
>
> An independent review of the first revision found a materially misleading orbital
> interpretation and five weaker defects. All are fixed here and the corrections are listed in
> full at the end of this file. The one that changed a published number: the first revision
> computed a total two-impulse Hohmann budget and then read it in prose as what a single burn
> does. Those differ by about a factor of two, and section 9 now keeps five separate quantities
> apart that the first revision collapsed into one.

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
4. Run the first-order propulsion and orbital model from those declared inputs, and actually
   sweep every sensitivity that was declared.
5. Read the result as a statement about the assumptions, not about the engine.
6. Write down which provider datum would replace each assumption, marked engine-level or
   stage-level, so the study can be corrected rather than re-derived.

Steps 4 and 6 are the ones the first revision got wrong. It declared a 15 to 30 kN thrust
sensitivity and never swept it, and its replacement table did not say which team owns each row.

---

## 4. Evidence rules

Every claim carries one of these classes, and they are not mixed.

| Class | What it means |
|---|---|
| COMPANY_PRIMARY | Read directly on the company's own site or its own post |
| COMPANY_RELEASE_RELAYED | Company-issued release text, reaching this file through a wire service or an outlet rather than from the company's own property |
| TOOL_VENDOR_TECHNICAL | A design-tool vendor publishing about the company's own design work |
| THIRD_PARTY_TECHNICAL | An independent technical source with its own engineering content |
| SECONDARY_REPORTING | A press or trade report relaying a claim it did not verify |
| ASSUMPTION | A VOLLEY reference assumption. No source. It exists so the arithmetic has somewhere to start |

Three rules on top of the classes.

**A claim about a subsystem is not a claim about the system.** A demonstrated ignition subsystem
says what the igniter does. It says nothing about the engine around it, and the engine says
nothing about the stage around that.

**A relay is named as a relay.** The first revision marked several rows COMPANY_STATED when the
company's own page had not been read. Those rows are now COMPANY_RELEASE_RELAYED or
SECONDARY_REPORTING, which is what they were.

**The retrieval limit is stated exactly.** Every source below is identified by title and URL, and
none of them could be retrieved directly: the network policy of the machine this study was run on
returns a 403 policy denial on connection to each host, and that has been re-tested on 2026-08-26.
What reached this file is what search-result summaries of those pages returned. Every row
therefore carries a retrieval column, and no row is marked COMPANY_PRIMARY, because none was read
on the company's own property. A reader with unrestricted access should treat the table as a set
of citations to check rather than as a verified record. This is the same limitation A9 and the
`celestrak.org` row in [`EXTERNAL_EVIDENCE.md`](EXTERNAL_EVIDENCE.md) already carry.

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
| Reaction control for fine manoeuvres | section 10, and it turns out to be the load-bearing one |
| Electrical power and communications | keeping VOLLEY commandable for the length of the campaign |
| Structural interface and VOLLEY mounting | [E31](../OPEN_PROBLEMS.md) |
| Collision avoidance during the campaign | [E18](../OPEN_PROBLEMS.md) |
| Disposal reserve and passivation | section 16, and [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 7 |

So the question this file asks is not whether a given engine can fly VOLLEY. It is:

> What would an upper stage built around a propulsion system of this class have to provide,
> before the distributed-delivery mission could be planned against it?

---

## 6. Reference case 1, ANYA-class semi-cryogenic propulsion in an assumed restartable Class-B stage

The first worked case is a hypothetical stage built around the ANYA engine platform, which
Thrustworks Dynetics develops and describes publicly. It is used here because its public record
is unusually specific for an engine at this stage of development: a stated thrust class, a stated
propellant family, a stated architecture, and a separately reported ignition-system test campaign.

Two scoping rules hold for the whole section.

**The stage is assumed, not described.** No such stage exists publicly. Restartability, tankage,
propellant management, coast capability and disposal are all VOLLEY assumptions about a
hypothetical vehicle, and none of them is a property of any engine or any company.

**ANYA-class means the thrust and propellant class, not the engine.** No figure computed in this
file is a statement about ANYA's performance, and section 7 records exactly what the public record
does and does not establish.

### The reference architecture

```
PRIMARY ASCENT
  -> PRIMARY PAYLOAD SEPARATION            the primary customer is served, and served first
  -> POST-PRIMARY STAGE MODE               stage stays powered, navigated and commandable
  -> MAIN-ENGINE RESTART, ASSUMED          post-primary restart is a VOLLEY assumption about a
                                           hypothetical stage. Nothing public establishes
                                           whole-engine or stage-level restart for this case
  -> COARSE REPOSITION                     two impulses, apogee raise then circularisation
  -> ENGINE SHUTDOWN
  -> COAST / SETTLE / NAVIGATION           attitude and state established before release
  -> VOLLEY DEPLOYMENT BATCH               commanded per-satellite release velocity
  -> SAFE SEPARATION                       range and geometry established before the next burn
  -> NEXT RESTART -> NEXT REPOSITION -> NEXT BATCH
  -> DISPOSAL RESERVE                      ring-fenced before the first satellite left
  -> FINAL DISPOSAL BURN
  -> PASSIVATION
```

This maps to Class B, and the mapping is a study rather than a finding. An ANYA-class propulsion
system is examined here inside an assumed Class-B stage, under declared assumptions.

The two systems stay separate at every step. The engine changes the stage's orbit. VOLLEY
produces each satellite's release state relative to the stage. VOLLEY does not command the
engine, the engine is no part of Gen6's cold-gas deployment system, and neither substitutes for
the other.

---

## 7. Public facts, their sources, and what each one is worth

Every row states the claim as the source states it, not as VOLLEY would like to read it. The
retrieval column says how the text reached this file: `SEARCH_SUMMARY` means the page itself could
not be opened, and the claim comes from a search-result summary of it.

### Sources

| | Source | Title | URL |
|---|---|---|---|
| S1 | Thrustworks Dynetics, company site | Thrustworks Dynetics, Learn. Innovate. Implement. Repeat | https://thrustworksdynetics.in/ |
| S2 | SoftInWay, tool vendor, startup programme page | Designing a Turbopump with AxSTREAM: Inside Thrustworks Dynetics' ANYA Rocket Engine | https://www.softinway.com/startup/ |
| S3 | YourStory, July 2026 | Thrustworks Dynetics wants to supply its engines to India's rocket industry | https://yourstory.com/2026/07/thrustworks-dynetics-rocket-engines-india |
| S4 | Electronics For You | Advanced Liquid Rocket Engines For Space And Defence Applications By Thrustworks | https://www.electronicsforu.com/india-corner/advanced-liquid-rocket-engines-for-space-defence-applications-thrustworks |
| S5 | openPR, company release on a wire | India's First Resonance-Based Rocket Ignition System Successfully Tested by Thrustworks Dynetics | https://www.openpr.com/news/4405926/india-s-first-resonance-based-rocket-ignition-system |
| S6 | Raksha Anirveda | Deep-Tech Startup Thrustworks Dynetics Test-Fires India's First Resonance-Based Rocket Ignition System | https://raksha-anirveda.com/deep-tech-startup-thrustworks-dynetics-test-fires-indias-first-resonance-based-rocket-ignition-system/ |
| S7 | idrw.org | Pune-Based Thrustworks Dynetics Unveils India's First Resonance Ignition System at TRL 6 | https://idrw.org/pune-based-thrustworks-dynetics-unveils-indias-first-resonance-ignition-system-at-trl-6/ |
| S8 | Indian Defence News, August 2026 | Thrustworks Dynetics Validates India's First Resonance Ignition System With KeroLOX Hot-Fire Tests | https://www.indiandefensenews.in/2026/08/thrustworks-dynetics-validates-indias.html |

None of S1 to S8 could be opened directly. Each host returns a 403 policy denial to the network
this study was run on, re-tested 2026-08-26.

### Claims

| Claim | Source | Evidence class | Retrieval | Used as model input? |
|---|---|---|---|---|
| ANYA is a modular, 3D-printed semi-cryogenic liquid rocket engine platform | S1, S3, S4 | SECONDARY_REPORTING of company positioning | SEARCH_SUMMARY | context only. Semi-cryogenic is an architecture family and does not by itself fix the propellant pair |
| The platform is described at a 20 kN thrust class | S2, S4 | TOOL_VENDOR_TECHNICAL, corroborated by SECONDARY_REPORTING | SEARCH_SUMMARY | yes, as the thrust class. Neither source states whether 20 kN is sea-level or vacuum thrust |
| The engine is LOX and kerosene | S2 | TOOL_VENDOR_TECHNICAL, from the turbopump design publication | SEARCH_SUMMARY | yes. This row, and not the semi-cryogenic row, is what fixes the propellant family for the model |
| Turbopump design work for ANYA was performed with a commercial turbomachinery design suite, with the company's own turbomachinery engineers | S2 | TOOL_VENDOR_TECHNICAL | SEARCH_SUMMARY | no. It establishes a turbopump-fed architecture in development, and no performance figure |
| The platform is designed for rapid customization, so a customer takes a configuration rather than commissioning a bespoke engine | S1, S3 | SECONDARY_REPORTING of company positioning | SEARCH_SUMMARY | no. It is why a platform is worth studying as a class rather than as one engine |
| Thrust-to-weight ratio exceeding 110 | S4 | SECONDARY_REPORTING | SEARCH_SUMMARY | no |
| Reusable | S1, S4 | SECONDARY_REPORTING of company positioning | SEARCH_SUMMARY | no. Reusability is a recovery-and-refurbishment property and is not an on-orbit restart claim |
| Thrust vectoring capability | S4 | SECONDARY_REPORTING | SEARCH_SUMMARY | no |
| Engine subsystems have passed rapid start-stop testing | S4 | SECONDARY_REPORTING | SEARCH_SUMMARY | no. Subsystem start-stop is not engine restart and is not stage restart |
| Specific impulse and chamber pressure are not publicly disclosed | S4 | SECONDARY_REPORTING, which states the performance figures are undisclosed | SEARCH_SUMMARY | not applicable. This is the absence section 8 stands in for |
| A resonance ignition system was validated in three consecutive KeroLOX hot-fire tests | S5, S6, S8 | COMPANY_RELEASE_RELAYED | SEARCH_SUMMARY | no |
| Those ignition tests ran at an operating pressure of 5.08 bar gauge | S5, S8 | COMPANY_RELEASE_RELAYED | SEARCH_SUMMARY | no. This is an igniter test pressure. It is NOT an engine chamber pressure and must never be quoted as one |
| The igniter has zero moving parts and is driven entirely by internal propellant pressure | S5, S6, S8 | COMPANY_RELEASE_RELAYED | SEARCH_SUMMARY | no |
| The ignition architecture enables multiple restarts in vacuum using only onboard propellants, reported in some outlets as unlimited | S5, S6, S8 | COMPANY_RELEASE_RELAYED | SEARCH_SUMMARY | no. See the distinction below. This is the single most important row in the table |
| The ignition system is integrated into the ANYA platform | S5, S6 | COMPANY_RELEASE_RELAYED | SEARCH_SUMMARY | no |
| A technology readiness level of 6 is claimed for the ignition system | S7 | SECONDARY_REPORTING | SEARCH_SUMMARY | no. TRL is self-assessed unless an external body assigns it, and no assigning body is named |

### The distinction the whole study depends on

> An igniter that restarts repeatedly is not an engine that restarts repeatedly, and neither is a
> stage that restarts repeatedly.
>
> The public claim is about the ignition subsystem: no moving parts, driven by propellant
> pressure, repeatable in vacuum. Taken at face value it removes one specific historical restart
> limit, the consumable pyrotechnic cartridge or the spark system and its power.
>
> Whole-engine restart additionally depends on turbomachinery restart and spin-up, thermal cycling
> of the chamber and nozzle, valve cycle life, propellant conditioning, feed-line chill-down,
> inlet conditions at ignition, and the ignition sequence itself. Stage restart then adds tank
> state, ullage, propellant settling, oxidiser management and the stage's own command authority.
>
> Converting the igniter claim into an engine or stage claim would be the largest single error
> available in this file, and it is the error this paragraph exists to prevent. Whole-engine
> restart is not publicly established for this case, and the restart budget in section 8 is a
> VOLLEY assumption about a hypothetical stage.

### On "reusable", "3D printed", "high thrust-to-weight" and "TRL 6"

Recorded above with their provenance rather than treated as design parameters. They are company
positioning statements relayed by trade press, and none is a qualified figure from a test report.
No number in this file descends from any of them.

---

## 8. Assumption ledger

Everything the public record does not supply, declared before the arithmetic and carried into
`analysis/host_reference.py` as named constants.

> Every value in the Baseline column below except thrust and propellant is a VOLLEY reference
> assumption. None of them is attributed to any engine, any stage or any provider. 300 s is not
> ANYA's specific impulse. 1000 kg is not an ANYA stage mass. 2 s is not ANYA's minimum burn. Four
> restarts is not ANYA's restart rating. These are numbers this project chose so that the model
> would run, and every one of them is wrong by an unknown amount.

| Quantity | Baseline | Sensitivity | Swept? | Status |
|---|---|---|---|---|
| Thrust | 20 kN | 15 to 30 kN | yes, section 10 | PUBLIC class figure, condition unstated. The range is a VOLLEY assumption |
| Propellant | LOX / kerosene | fixed for this case | not applicable | PUBLIC, from S2 |
| Vacuum specific impulse | 300 s | 285 to 320 s | yes, section 9 | VOLLEY ASSUMPTION. No public figure exists |
| Deep throttling | none credited | 100 % down to 10 % | yes, section 10, hypothetical only | UNKNOWN. Nothing public establishes a throttle envelope |
| Post-primary ignition budget | 4 | 2 to 8 | tested against, section 11 | VOLLEY ASSUMPTION. No public engine restart rating exists |
| Contingency ignition | +1 | | not applicable | VOLLEY ASSUMPTION |
| Minimum stable useful burn | 2 s | 0.5 to 5 s | yes, sections 10 and 11 | VOLLEY ASSUMPTION. No public figure exists |
| Minimum coast between burns | 10 min | 2 to 30 min | scenario, section 12 | VOLLEY ASSUMPTION. No public figure exists |
| Post-primary campaign duration | 4 h | 1 to 12 h | scenario, section 14 | VOLLEY ASSUMPTION. No public cryogenic coast limit exists |
| Reference post-primary stage mass | 1000 kg | 500 to 3000 kg | yes, sections 9 and 10 | VOLLEY ASSUMPTION. No public stage exists to have a mass |
| Usable post-primary propellant | 150 kg | not swept | no | VOLLEY ASSUMPTION |
| Disposal reserve | 20 % of usable post-primary propellant | 10 to 30 % | yes, section 16 | VOLLEY ASSUMPTION, a reserve policy and not a disposal guarantee |
| Reference altitude | 500 km circular | not swept for the propulsion tables | no | VOLLEY ASSUMPTION, chosen to match MISSION_ARCHITECTURE.md section 5 |
| Ascent starts before primary separation | 1 | not swept | no | ILLUSTRATIVE for this case. The ascent profile is a vehicle property |
| Plane-change mission | excluded, priced only | | not applicable | ARCHITECTURE RULE, from MISSION_ARCHITECTURE.md section 5 |

---

## 9. First-order model, and five quantities that are not the same

`analysis/host_reference.py`. Two-body and impulsive for the orbital results; constant thrust and
constant specific impulse for the propulsion results. No gravity loss, no steering loss, no
throttle penalty on specific impulse, no shutdown transient. Closed forms plus one bisection. It
is not a trajectory tool and must not be read as one.

```
g0   = 9.80665 m/s^2                          standard gravity, exact by definition
mdot = F / (Isp * g0)                         mass flow
dv   = Isp * g0 * ln(m0 / mf)                 rocket equation
mp   = m0 * (1 - exp(-dv / (Isp * g0)))       propellant for a manoeuvre
tb   = mp / mdot                              burn duration
dv(t)= Isp * g0 * ln(m0 / (m0 - mdot * t))    what a burn of length t buys

single prograde impulse from a circular orbit, by vis-viva:
  v  = sqrt(mu/r0) + dv
  eps= v^2/2 - mu/r0        a = -mu/(2 eps)        r_apogee = 2a - r0
  perigee stays at r0. APOGEE rises. The orbit is no longer circular.

two-impulse Hohmann between circular orbits, both impulses reported separately, and the
inverse solved by bisection rather than by scaling a single case linearly.
```

> ### The five quantities
>
> 1. **One single prograde impulse.** Raises apogee, leaves perigee where it was.
> 2. **Total mission dv.** The sum of every impulse in the campaign.
> 3. **First Hohmann impulse.** Raises apogee to the target radius.
> 4. **Second Hohmann impulse.** Circularises there.
> 5. **Final circular altitude.** What 3 and 4 together deliver.
>
> At 500 km a 40.3 m/s single burn raises apogee by 147.5 km. The same 40.3 m/s spent as a
> complete two-impulse Hohmann raises the CIRCULAR altitude by 73.4 km. The first revision of
> this file computed the second quantity and described it in prose as the first.

<!-- HOST_REFERENCE:MASS_FLOW:BEGIN -->
At 20 kN and an assumed 300 s, mass flow is 6.80 kg/s.
<!-- HOST_REFERENCE:MASS_FLOW:END -->

Burn duration, seconds, if a manoeuvre budget were spent as one continuous burn, at the assumed
300 s specific impulse. The column headings are TOTAL manoeuvre budgets, not single impulses.

<!-- HOST_REFERENCE:BURN_GRID:BEGIN -->
| Stage mass | 5 m/s | 10 m/s | 20 m/s | 40 m/s | 100 m/s |
|---:|---:|---:|---:|---:|---:|
| 500 kg | 0.12 | 0.25 | 0.50 | 0.99 | 2.46 |
| 1000 kg | 0.25 | 0.50 | 1.00 | 1.99 | 4.92 |
| 2000 kg | 0.50 | 1.00 | 1.99 | 3.97 | 9.83 |
| 3000 kg | 0.75 | 1.50 | 2.99 | 5.96 | 14.75 |
<!-- HOST_REFERENCE:BURN_GRID:END -->

Propellant, kilograms, over the same grid:

<!-- HOST_REFERENCE:PROPELLANT_GRID:BEGIN -->
| Stage mass | 5 m/s | 10 m/s | 20 m/s | 40 m/s | 100 m/s |
|---:|---:|---:|---:|---:|---:|
| 500 kg | 0.85 | 1.70 | 3.39 | 6.75 | 16.7 |
| 1000 kg | 1.70 | 3.39 | 6.78 | 13.5 | 33.4 |
| 2000 kg | 3.40 | 6.79 | 13.6 | 27.0 | 66.8 |
| 3000 kg | 5.09 | 10.2 | 20.3 | 40.5 | 100.3 |
<!-- HOST_REFERENCE:PROPELLANT_GRID:END -->

Specific impulse across its declared range, at the reference stage mass and a 20 m/s budget:

<!-- HOST_REFERENCE:ISP_SENSITIVITY:BEGIN -->
| Specific impulse | Propellant for a 20 m/s budget at 1000 kg | Burn duration if spent as one burn |
|---:|---:|---:|
| 285 s | 7.13 kg | 1.00 s |
| 300 s | 6.78 kg | 1.00 s |
| 320 s | 6.35 kg | 1.00 s |
<!-- HOST_REFERENCE:ISP_SENSITIVITY:END -->

Propellant moves by about six per cent across the range and burn duration does not move at all to
three figures. That is not a coincidence: propellant scales as 1/Isp and so does mass flow, so
burn duration for a given manoeuvre and stage mass is very nearly independent of specific impulse.

> The softest assumption in the ledger has almost no influence on the result that matters.
> Section 10's finding does not rest on the 300 s figure, which is worth knowing because that
> figure is the one a propulsion engineer is most likely to be able to correct.

---

## 10. The minimum-burn problem

The principal result, computed rather than assumed. The question is whether a main engine of this
thrust class can command the small manoeuvres a distributed-delivery campaign needs, or only the
large ones.

Two orbital readings of the same dv floor, kept apart:

<!-- HOST_REFERENCE:MINIMUM_BURN:BEGIN -->
| Stage mass | Assumed minimum burn | Single-burn dv floor, m/s | Apogee rise from that burn, km | Circular raise the same dv would buy as a full two-burn transfer, km | Overshoot vs a 5 m/s total budget | Overshoot vs the first impulse of that budget | Burn the first impulse actually needs, s |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 500 kg | 2 s | 81.1 | 301.1 | 148.9 | 16.2x | 32.4x | 0.062 |
| 1000 kg | 2 s | 40.3 | 147.5 | 73.4 | 8.1x | 16.1x | 0.125 |
| 2000 kg | 2 s | 20.1 | 73.0 | 36.4 | 4.0x | 8.0x | 0.250 |
| 3000 kg | 2 s | 13.4 | 48.5 | 24.2 | 2.7x | 5.3x | 0.375 |
<!-- HOST_REFERENCE:MINIMUM_BURN:END -->

What shorter burns would buy, if the engine could hold them:

<!-- HOST_REFERENCE:SHORT_BURNS:BEGIN -->
| Burn | 500 kg | 1000 kg | 2000 kg | 3000 kg |
|---:|---:|---:|---:|---:|
| 0.5 s | 20.1 | 10.0 | 5.0 | 3.3 |
| 1 s | 40.3 | 20.1 | 10.0 | 6.7 |
| 2 s | 81.1 | 40.3 | 20.1 | 13.4 |
| 5 s | 207.1 | 101.7 | 50.4 | 33.5 |
<!-- HOST_REFERENCE:SHORT_BURNS:END -->

### The fine end, split into the impulses an engine has to command

A shell change is two burns, not one. This is the table the first revision did not have, and its
absence is what let a total budget be described as a single burn.

<!-- HOST_REFERENCE:FINE_MANOEUVRES:BEGIN -->
| Circular raise at 500 km | Total dv, m/s | First impulse, m/s | Second impulse, m/s | First burn, s | Second burn, s | Transfer arc, min |
|---:|---:|---:|---:|---:|---:|---:|
| 5 km | 2.765 | 1.383 | 1.383 | 0.069 | 0.069 | 47.3 |
| 10 km | 5.528 | 2.764 | 2.763 | 0.138 | 0.138 | 47.4 |
| 25 km | 13.797 | 6.902 | 6.895 | 0.345 | 0.344 | 47.4 |
| 50 km | 27.520 | 13.772 | 13.747 | 0.687 | 0.686 | 47.6 |
<!-- HOST_REFERENCE:FINE_MANOEUVRES:END -->

A 10 km raise at 500 km costs 5.528 m/s in total, and that total is two nearly equal impulses of
about 2.76 m/s. At the reference stage each is a burn of 0.138 s. The first revision said this
manoeuvre needed "roughly a quarter of a second", which was the burn for the whole budget spent
at once, and about double what either actual impulse requires.

### Thrust sensitivity, the declared 15 to 30 kN range actually swept

<!-- HOST_REFERENCE:THRUST_SWEEP:BEGIN -->
| Thrust | Mass flow, kg/s | dv floor at 2 s, m/s | Apogee rise from that one burn, km | Circular raise if that dv were a full two-burn budget, km | Burn for 2.5 m/s, s | for 5 m/s | for 10 m/s | for 20 m/s |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 kN | 5.10 | 30.2 | 110 | 55 | 0.167 | 0.333 | 0.666 | 1.329 |
| 20 kN | 6.80 | 40.3 | 148 | 73 | 0.125 | 0.250 | 0.499 | 0.997 |
| 30 kN | 10.20 | 60.6 | 224 | 111 | 0.083 | 0.167 | 0.333 | 0.664 |
<!-- HOST_REFERENCE:THRUST_SWEEP:END -->

The conclusion survives the whole declared range. Even at 15 kN, the bottom of the range, a 2 s
burn on the reference stage cannot command less than 30.2 m/s, which is 6.0 times a 5 m/s total
budget and about 12 times the first impulse of one. Thrust does not rescue the fine end; it only
changes how badly it is overshot.

### What would rescue it, expressed as a question a propulsion engineer can answer

The inversion: for each fine manoeuvre and each candidate minimum stable burn, what is the largest
thrust that still lets the first impulse fit inside that burn? Read as a fraction of the 20 kN
class figure, it is the required throttle depth.

<!-- HOST_REFERENCE:THRUST_REQUIREMENT:BEGIN -->
| Manoeuvre | First impulse, m/s | if minimum burn is 0.5 s | if minimum burn is 1 s | if minimum burn is 2 s | if minimum burn is 5 s |
|---:|---:|---:|---:|---:|---:|
| 2.5 m/s total | 1.250 | 2.50 kN (12.5 %) | 1.25 kN (6.2 %) | 0.62 kN (3.1 %) | 0.25 kN (1.2 %) |
| 5 m/s total | 2.500 | 5.00 kN (25.0 %) | 2.50 kN (12.5 %) | 1.25 kN (6.2 %) | 0.50 kN (2.5 %) |
| 10 m/s total | 5.002 | 9.99 kN (50.0 %) | 5.00 kN (25.0 %) | 2.50 kN (12.5 %) | 1.00 kN (5.0 %) |
<!-- HOST_REFERENCE:THRUST_REQUIREMENT:END -->

And the same question from the other side, as a hypothetical throttle sweep. This is not a
capability of any engine. Nothing public establishes a throttle envelope for this case, and the
model holds specific impulse constant while throttling, which is optimistic because a real engine
loses specific impulse when deeply throttled.

<!-- HOST_REFERENCE:THROTTLE:BEGIN -->
| Hypothetical throttle setting | Thrust | dv floor at 2 s, m/s | Apogee rise from that burn, km | Circular raise the same dv would buy as a full two-burn transfer, km |
|---:|---:|---:|---:|---:|
| 100 % | 20.0 kN | 40.3 | 147.5 | 73.4 |
| 75 % | 15.0 kN | 30.2 | 110.1 | 54.8 |
| 50 % | 10.0 kN | 20.1 | 73.0 | 36.4 |
| 25 % | 5.0 kN | 10.0 | 36.3 | 18.1 |
| 10 % | 2.0 kN | 4.0 | 14.5 | 7.2 |
<!-- HOST_REFERENCE:THROTTLE:END -->

Read this table against the last one rather than on its own. At 10 % thrust the 2 s floor falls
to 4.00 m/s, which does clear a 5 m/s total budget spent as a single burn, but it is still 3.2
times the 1.25 m/s first impulse of a 2.5 m/s shell change and 1.6 times the 2.50 m/s first
impulse of a 5 m/s one. Deep throttling narrows the gap and does not by itself close it, and the
required-thrust table above is the more useful statement of the same result: reaching the first
impulse of a 5 m/s manoeuvre in a 2 s burn needs 1.25 kN, which is 6.2 % of the class figure.

### What this says

Under the declared assumptions a main engine of this thrust class is a coarse actuator across the
entire declared thrust range. The overshoot narrows with stage mass and with throttle
depth, and closing it needs both together: 1.25 kN held for 2 s, or 5.00 kN held for 0.5 s, either
of which is a deeper throttle than anything public establishes for this class.

So the architecture that falls out is a three-way split rather than a two-way one:

| | |
|---|---|
| Main engine | coarse orbital-energy change, shell to shell, tens of m/s and up |
| Reaction control or auxiliary stage propulsion | small corrections, settling, attitude, the metres-per-second end |
| VOLLEY | the final commanded per-satellite release state |

That was not the expected answer, and it means the host requirement list in section 5 has a
load-bearing row the engine discussion does not touch at all: a Class-B host needs usable reaction
control, and its authority is [P94](../OPEN_PROBLEMS.md), already live and already `HOST_DATA`.

Three ways this conclusion could still be wrong, each of them a provider datum: the minimum stable
burn could be far below 0.5 s; the engine could throttle far more deeply than 10 % without losing
specific impulse; or the stage could be much heavier than 3000 kg. The tables above are built so
that a reader who knows any of those can read the answer off them directly.

---

## 11. Mission cases

Disposal reserve is ring-fenced first. Customer manoeuvres spend what is left. At the assumed
150 kg usable and 20 % reserve, that leaves 120 kg for customers.

Each reposition leg is a circular-to-circular shell change, so each leg is two ignitions. The
ignition column counts ignitions, not legs, and the two differ by about a factor of two.

<!-- HOST_REFERENCE:MISSION_CASES:BEGIN -->
| Case | Reposition legs | Reposition ignitions | Post-primary ignitions required | Total dv, m/s | Propellant, kg | Margin on the customer budget, kg | Inside the assumed 4-ignition budget |
|---|---:|---:|---:|---:|---:|---:|---|
| A, rapid deployment, no post-primary main-engine burn | 0 | 0 | 0 | 0 | 0.0 | 120.0 | yes |
| B, moderate distributed delivery | 3 | 6 | 7 | 60 | 20.2 | 99.8 | NO, over by 3 |
| C, upper-bound sensitivity | 5 | 10 | 11 | 200 | 65.7 | 54.3 | NO, over by 7 |
<!-- HOST_REFERENCE:MISSION_CASES:END -->

**Case A is the one that matters most to the architecture.** It uses no post-primary main-engine
ignition at all, and it works on every host class including C. VOLLEY does not require a
restartable host to exist, and every capability discussed in this file is an extension of a
product that already functions without it. That is easy to lose sight of in a document about
engines.

**Case B and Case C both exceed the assumed ignition budget.** Case B needs 7 post-primary
ignitions against an assumed budget of 4, and Case C needs 11. This is the sharpest finding in
the study and the first revision did not have it, because it counted repositioning legs as
ignitions and so understated both cases by about half.

> On the declared assumptions, the binding constraint on a distributed campaign is the number of
> post-primary main-engine ignitions the stage can be qualified for. It binds before propellant
> does and before any of the pacing scenarios in section 12 do. That makes qualified restart count
> the single most valuable provider datum in section 19, and it is a datum that belongs to the
> engine team rather than to the stage team.

Three ways the ignition count could come down, none of which this file can choose: reposition with
a single apogee-raising burn and accept an elliptical stage orbit, which changes what the customer
is sold; use reaction control for the circularisation impulse, which is section 10's split applied
again; or perform fewer, larger shell changes, which is section 13.

### Propellant is not the constraint here, on these assumptions

Case B spends 20.2 kg of a 120 kg customer allocation, and even Case C spends 65.7 kg. That is a
statement about the assumed 150 kg usable propellant and nothing else. A stage with a tenth of
that assumption would invert it, and no public figure exists for what a real stage would carry.

---

## 12. Campaign pacing, as scenarios rather than as a bound

One part of campaign duration is a physical two-body result: the transfer arc from the first
impulse to the second is half the transfer-ellipse period, and at these altitudes it is about
47 minutes. Everything else is a scheduling assumption.

<!-- HOST_REFERENCE:PACING:BEGIN -->
| Case | Legs | Transfer arc per leg, min | Transfer arcs only, h | Assumed coast floor, h | Half-orbit per leg, h | One orbit per leg, h | Two orbits per leg, h |
|---|---:|---:|---:|---:|---:|---:|---:|
| B | 3 | 47.5 | 2.37 | 0.50 | 2.4 | 4.7 | 9.5 |
| C | 5 | 47.7 | 3.97 | 0.83 | 3.9 | 7.9 | 15.8 |
<!-- HOST_REFERENCE:PACING:END -->

The first revision called one orbit per leg "the real pace" and concluded from it that time was
the binding constraint. That was too strong, and it is withdrawn. One orbital period per leg is an
illustrative scheduling case, not a lower bound: a Hohmann transfer reaches the opposite apsis in
about half an orbit, some phasing operations need several orbits, and some deployment sequences
could occur before a full orbit elapses.

What the table supports is narrower and still useful: under the illustrative one-orbit-per-leg
case, campaign duration reaches 4.7 h for Case B and 7.9 h for Case C, so it passes the assumed 4 h
campaign reference before propellant becomes limiting. Under the half-orbit case it does not.
That is a tension between two VOLLEY assumptions, exposed by declaring both, and it is not a
finding about any engine.

The real pacing problem belongs to a mission planner this repository does not have, and it depends
on manoeuvre geometry, target state, navigation, attitude settling, safe separation, plume
constraints, collision avoidance, host command rules and provider operations. None of those
numbers is invented here.

---

## 13. Reposition-count scaling

Not an equal-mission batching comparison. Each row holds 20 m/s per reposition fixed, so a row
with more repositions also buys more total orbital separation, and the rows do not deliver the
same mission.

<!-- HOST_REFERENCE:REPOSITION_SCALING:BEGIN -->
| Deployment states | Satellites per state | Reposition legs | Total dv, m/s | Cumulative circular raise, km | Propellant, kg | One orbit per leg, h |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 1 | 11 | 220 | 399 | 72.1 | 17.3 |
| 4 | 3 | 3 | 60 | 109 | 20.2 | 4.7 |
| 3 | 4 | 2 | 40 | 73 | 13.5 | 3.2 |
| 2 | 6 | 1 | 20 | 36 | 6.8 | 1.6 |
<!-- HOST_REFERENCE:REPOSITION_SCALING:END -->

The first revision presented this table as evidence that batching "wins". It is not, and that
claim is withdrawn. Comparing a campaign that reaches 220 m/s of cumulative separation against one
that reaches 60 m/s tells you nothing about grouping efficiency, because the customer is not
buying the same thing in the two cases.

What the table does show, parametrically, is that more distinct deployment states cost more
ignitions, more propellant, more thermal cycles and more propellant-management events, roughly in
proportion. That is worth knowing and it is not an optimisation.

> **A fair batching trade is left explicitly open.** It would hold the delivered orbital-state
> distribution constant and vary only how satellites are grouped into deployment batches, which
> requires a mission planner with target states, timing and a cost function. That is
> [P113](../OPEN_PROBLEMS.md), and this file does not attempt it.

What batching does not cost is the product. VOLLEY supplies a commanded velocity per satellite
inside every batch, so satellites released together still separate from each other, and
[A15](../validation/A15_poem_campaign.md) and [P56](../OPEN_PROBLEMS.md) record that release
timing alone gives in-track phase at zero dv.

---

## 14. Cryogenic coast and ignition accounting

### The oxidiser sets the campaign limit

Kerosene storage over hours is straightforward. Liquid oxygen is not, and it drives heat leak,
boil-off, tank pressure and venting, stratification, slosh, restart inlet conditions and
feed-line chill-down. For a stage that must restart after coasting, the oxidiser's thermal state
at ignition decides whether the restart is available at all.

Nothing public establishes an ANYA-class cryogenic coast capability, and this file does not invent
one. What can be said parametrically:

| Campaign duration | What it would allow, on the assumptions above | What it needs |
|---|---|---|
| 1 h | roughly one reposition and deploy leg | little coast management |
| 4 h | Case B under the one-orbit pacing case, marginally | a stated boil-off rate and tank pressure history |
| 12 h | Case C with margin | active or passive thermal control and a vent policy, both stage design |

None of the three can be chosen from public data. What would settle it is a stage-level cryogenic
design limit, and it is a provider datum in section 19.

> A campaign lasting several days must not be claimed for an ANYA-class reference stage from the
> present public evidence, and this file does not claim it. The multi-day distributed campaign in
> [A50](../validation/A50_campaign_altitude.md) is a Class-A study on a stage with no cryogenic
> oxidiser, and it does not transfer here.

### Start against restart, counted properly

If the engine has already fired during ascent or injection, the first post-primary ignition is a
restart and not a start. Several different counts are involved and they are routinely conflated.

<!-- HOST_REFERENCE:RESTART_ACCOUNTING:BEGIN -->
| Count | Case B | Established by public evidence? |
|---|---:|---|
| Reposition legs | 3 | no |
| Ignitions per leg, circular to circular | 2 | two-body result, not a provider figure |
| Reposition ignitions | 6 | no |
| Disposal ignition | 1 | no |
| Post-primary ignitions required | 7 | no |
| Assumed post-primary ignition budget | 4 | no, and this case needs more than it |
| Contingency ignitions reserved | 1 | no |
| Ascent starts, illustrative for this case | 1 | no, and the ascent profile is a vehicle property |
| Total engine starts, illustrative | 8 | no |
| Igniter cycles, at least | 8 | three, on the ground, for the subsystem alone |
| Full-engine thermal cycles | 8 | no |
<!-- HOST_REFERENCE:RESTART_ACCOUNTING:END -->

Two things that table is careful about. The disposal burn is an ignition and is counted as one, so
a campaign planned around three shell changes needs seven post-primary ignitions rather than
three, and a mission that budgets ignitions by counting deployment legs will be short at exactly
the moment it cannot afford to be. And the ascent start is illustrative for this reference case
rather than a vehicle fact: a different ascent profile changes the total-start row and none of the
post-primary rows.

The igniter row is the only one with any public evidence behind it, and it is a ground count on a
subsystem. Igniter cycles are not engine restart life.

---

## 15. Deployment and plume sequencing

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
about 1.7 km per minute, which makes range the easy part of the problem. And the transfer arc in
section 12 puts about 47 minutes between the two impulses of a shell change, which is time the
sequence can use.

---

## 16. Disposal reserve

No reference mission spends the last of the stage's propellant on customers. The reserve is
ring-fenced first and the campaign is planned against what remains.

The two dv columns are sequential and not independent. Customer dv is what the customer allocation
buys starting from the full stage mass. Reserve dv is what the ring-fenced remainder buys after
the customer allocation has been spent, from the lighter mass state disposal actually happens at.
Reading the reserve as a burn from initial mass would overstate it.

<!-- HOST_REFERENCE:DISPOSAL:BEGIN -->
| Reserve | Reserve mass, kg | Customer mass, kg | Customer dv from full stage mass, m/s | Stage mass at disposal, kg | Reserve dv from that mass, m/s |
|---:|---:|---:|---:|---:|---:|
| 10 % | 15.0 | 135.0 | 427 | 865 | 51 |
| 20 % | 30.0 | 120.0 | 376 | 880 | 102 |
| 30 % | 45.0 | 105.0 | 326 | 895 | 152 |
<!-- HOST_REFERENCE:DISPOSAL:END -->

> A percentage reserve is a budgeting rule and not a disposal capability. Whether 102 m/s actually
> deorbits the stage depends on the orbit it ends the campaign in, the stage's ballistic
> coefficient and the applicable disposal rule, none of which is specified here. This table says
> what is held back. It does not say that disposal is achievable, and no row in it should be read
> as a compliance statement.

Every case in section 11 fits inside the 20 % reserve with margin, which says more about the
assumed 150 kg than about any engine.

---

## 17. Plane change stays priced and stays excluded

Re-derived in `analysis/host_reference.py` rather than quoted, and it reproduces
[`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 5. The 10 km figure is the TOTAL
two-impulse cost, and both impulses are given separately so that the total can never again be
mistaken for a single burn.

<!-- HOST_REFERENCE:PLANE_CHANGE:BEGIN -->
| Altitude | Circular v, m/s | 1 degree of inclination, m/s | 0.1 degree, m/s | 10 km raise, total, m/s | first impulse, m/s | second impulse, m/s | Ratio, 1 degree to 10 km |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 350 km | 7697.0 | 134.3 | 13.4 | 5.71 | 2.86 | 2.86 | 23.5 |
| 500 km | 7612.6 | 132.9 | 13.3 | 5.53 | 2.76 | 2.76 | 24.0 |
| 700 km | 7504.3 | 131.0 | 13.1 | 5.30 | 2.65 | 2.65 | 24.7 |
<!-- HOST_REFERENCE:PLANE_CHANGE:END -->

One degree of inclination costs about twenty-four times a ten-kilometre altitude change. On the
assumed 120 kg customer allocation a single degree at 500 km would consume roughly a third of it,
and the campaign would end with one plane and no shells.

> The existence of a 20 kN engine is not a reason to widen the product into arbitrary plane
> changes. The architecture rule stands: distributed delivery supplies altitude, phase and orbital
> energy. A restartable host makes the coplanar campaign better and does not make the plane change
> affordable.

---

## 18. Result

Under the declared assumptions, an ANYA-class semi-cryogenic propulsion system is a useful Class-B
reference case for VOLLEY's distributed-delivery architecture. The public record establishes a
customizable 20 kN LOX/kerosene engine platform, a turbopump-fed architecture in development, and
a repeatedly fired resonance ignition subsystem. It does not establish the whole-engine restart,
stage restart, coast, throttling, propellant-management or disposal envelope needed to claim
compatibility. Those remain explicit provider-data inputs.

Four things the study produced, which are properties of the declared assumptions rather than of
any engine:

1. **A main engine of this thrust class is a coarse actuator, across the whole declared thrust
   range.** At 15, 20 and 30 kN the smallest manoeuvre a 2 s burn can command on the reference
   stage is 30.2, 40.3 and 60.6 m/s. A 10 km shell change needs two impulses of 2.76 m/s, each a
   0.138 s burn. Fine stage corrections belong to reaction control, and the three-way split in
   section 10 is the cleaner architecture.
2. **Post-primary ignition count binds before propellant or time.** Counting each shell change as
   the two-impulse transfer it is, Case B needs 7 post-primary ignitions and Case C needs 11,
   against an assumed budget of 4. Qualified restart count is the most valuable single provider
   datum in this study.
3. **The softest assumption matters least.** Specific impulse across 285 to 320 s moves propellant
   by about six per cent and burn duration not at all, so the main conclusion does not rest on the
   number a reviewer is most likely to be able to correct.
4. **Propellant has margin and campaign duration is scenario-dependent.** Both are statements
   about the assumed 150 kg usable propellant and the assumed pacing, not about any vehicle.

### What is not concluded

This file does not say that ANYA is compatible with VOLLEY, that any provider will power VOLLEY,
that VOLLEY will use any named engine, that ANYA supports any number of restarts, that ANYA has a
300 s specific impulse or any particular chamber pressure, that an ANYA-class stage can remain in
orbit for any particular duration, that whole-engine or stage restart has been demonstrated, that
any company has reviewed or approved this concept, or that any collaboration or partnership
exists. None of those is established and several are not the kind of claim public information can
establish.

### What it changes in the repository, which is one thing

[P113](../OPEN_PROBLEMS.md) is opened: how the orbital work divides between host and deployer has
never been computed, and it sets VOLLEY's release-velocity requirement.

> The reference-host exercise reveals P113 and does not resolve it. A real answer needs
> mission-level optimisation across host manoeuvre, release velocity, deployment timing, target
> orbit states, host class, the reaction-control and main-engine split, propellant, campaign
> duration and disposal. That belongs in a future mission planner.
>
> A lower release velocity would reduce chamber pressure, acceleration, contact severity and
> tip-off sensitivity, which makes this trade a tempting route to making
> [P108](../OPEN_PROBLEMS.md) look smaller without answering it. **Nothing in this file lowers the
> Gen6 requirement, and P108 is unresolved.** The tip-off magnitude is not established, A72 has
> not been run, and the coupled trade is recorded for computation on its own merits, later and
> separately.

Gen6's design point is unchanged at 29.009 m/s. The Fusion package in
[`GEN6_FUSION_BUILD_PACKAGE.md`](GEN6_FUSION_BUILD_PACKAGE.md) remains the current CAD handoff.

---

## 19. What provider data would replace, and who owns each row

The practical reason the document exists. A reviewer who knows the real numbers should be able to
correct rows rather than reconstruct the study, and the Owner column says which team can answer.

| Model quantity | Assumed baseline | Sensitivity | Why it matters | Replacing datum | Owner | Consequence if materially different |
|---|---|---|---|---|---|---|
| Vacuum specific impulse | 300 s | 285 to 320 s | propellant budget for the whole campaign | design-point or certified vacuum Isp | engine | small. Propellant moves about 6 %, burn duration does not move |
| Thrust condition | 20 kN, condition unstated | 15 to 30 kN | which figure the model should use | vacuum thrust at the design mixture ratio | engine | moderate. Changes the dv floor proportionally, not the conclusion |
| Minimum stable useful burn | 2 s | 0.5 to 5 s | the whole of section 10 | demonstrated or qualified minimum burn duration | engine, controls and transient | large. At full thrust the first impulse of a 5 m/s shell change is a 0.125 s burn, so a minimum burn at or below that would let the main engine command the fine end directly |
| Throttle range and minimum power level | none credited | 100 to 10 %, hypothetical | whether the main engine can reach small manoeuvres at all | qualified throttle envelope, with the Isp penalty at each setting | engine, controls | large. Deep throttling plus a short minimum burn removes the need for the three-way split |
| Engine restart life | 4 assumed, 1 contingency | 2 to 8 | the binding constraint in section 11 | demonstrated or qualified restart count, and what limits it | engine, cycle and qualification | largest. Below 7 the moderate campaign does not close as modelled |
| Restart dwell and coast requirement | 10 min | 2 to 30 min | campaign sequencing | restart thermal and propellant-conditioning envelope | engine plus stage feed and thermal | moderate |
| Maximum coast duration | 4 h reference | 1 to 12 h | whether a multi-orbit campaign closes at all | stage cryogenic design limit and boil-off rate | stage, tank and thermal | large |
| Post-primary stage mass | 1000 kg | 500 to 3000 kg | every table in sections 9 and 10 | actual stage dry and wet mass at primary separation | stage | large. Heavier stages narrow the overshoot without closing it |
| Usable post-primary propellant | 150 kg | not swept | the customer allocation | reserved or characterised residual a provider will commit | stage and mission | large. This is the number that decides whether propellant is a constraint |
| Settling and ullage requirement | unknown | | whether a restart can be commanded in free fall | ullage requirement and settling method | stage, propellant management | unknown until supplied |
| Reaction-control authority and minimum impulse bit | unknown | | section 10's three-way split, and [P94](../OPEN_PROBLEMS.md) | RCS thrust, authority and minimum impulse bit | stage | large. This is what actually performs the fine manoeuvres |
| Disposal reserve policy | 20 % assumed | 10 to 30 % | mission closure | provider mission policy and reserve rule | provider and mission | moderate |
| Plume exclusion geometry | unknown | | safe restart after a deployment | plume and contamination constraint, with its half-angle | engine and integration | unknown until supplied |
| Host structural interface | unknown | | whether VOLLEY mounts at all, [E31](../OPEN_PROBLEMS.md) | interface control data | vehicle and integration | unknown until supplied |
| Post-primary command authority | assumed available | | whether the stage takes commands after passivation would normally begin | operations policy, telemetry and command availability | vehicle avionics and operations | binary. Without it, only Case A survives |

Five of those rows are engine-level and the rest are stage, vehicle or mission-level. An engine
engineer can close the first five and should not be expected to close the others.

None of these is closed by this file, and [E5](../OPEN_PROBLEMS.md) stays open. Public company
information can establish an engine class, a nominal thrust, a propellant family, a modularity
claim and the existence of an ignition technology. It cannot establish stage propellant reserve,
host control authority, restart qualification, coast limit or flight interface, and those are what
the mission needs.

---

## 20. Template for future reference cases

Any further case is added to this file under the same headings. It does not get its own document,
because a per-provider document is how a methodology turns into a catalogue.

Populate every field, and write UNKNOWN rather than leaving one blank. A blank reads as an
oversight and UNKNOWN reads as a finding.

| Field | What to record |
|---|---|
| Propulsion type | cycle, feed system, propellant family, and which source establishes the propellant pair |
| Thrust | value, whether sea-level or vacuum, and whether stated or inferred |
| Specific impulse | value and condition, or UNKNOWN |
| Restart capability | stated at which level: igniter, engine or stage. These are three different claims and must not be merged |
| Minimum impulse or minimum burn | value, or UNKNOWN, and its effect on the fine end of the manoeuvre range |
| Throttle | envelope, minimum power level and the Isp penalty, or UNKNOWN |
| Stage mass | dry and wet at primary separation, or UNKNOWN |
| Usable post-primary propellant | reserved or characterised residual, or UNKNOWN |
| Reaction-control authority | type, authority, minimum impulse bit |
| Coast lifetime | maximum coast before restart is unavailable, and what limits it |
| Propellant management | ullage, settling, pressurisation, thermal control |
| Disposal | reserve policy, and whether controlled re-entry is achievable from the campaign's end orbit |
| Structural interface | mounting provision for a hosted system, and its published interface data |
| Deployment constraints | plume exclusion, contamination, minimum range and time after release |
| Source confidence | the evidence class and the retrieval method of every row above, using section 4's classes |
| Host class mapped | A, B or C, stated as a study under declared assumptions rather than as a compatibility finding |

Then run `analysis/host_reference.py` with the case's constants and regenerate this document's
blocks. Report the minimum-burn table and the ignition accounting first: those were the two most
informative outputs for the one case run so far, and the two the first revision got wrong.

---

## 21. Corrections

The first revision of this file was published and reviewed on 2026-08-26. Six defects were found.
All are corrected above. The full record is in [`../CHANGELOG.md`](../CHANGELOG.md).

| | What was wrong | What it is now |
|---|---|---|
| 1 | A total two-impulse Hohmann budget was scaled linearly and called an "equivalent altitude step", then read in prose as what a single burn does. The two differ by about a factor of two | Single-impulse apogee rise is computed by vis-viva, the Hohmann inverse is solved by bisection, and both are reported side by side with the total and the two impulses kept separate |
| 2 | "The mission's fine end needs a burn of roughly a quarter of a second" quoted the total budget as one burn | A 10 km raise is 2.764 + 2.763 m/s, and each impulse is a 0.138 s burn at the reference stage |
| 3 | One orbit per leg was called "the real pace" and used to conclude that time was the binding constraint | It is an illustrative scheduling case among three, the transfer arc is separated out as the only physical duration, and the conclusion is withdrawn |
| 4 | A fixed-dv-per-reposition table was presented as evidence that batching "wins", comparing campaigns that deliver different missions | Renamed reposition-count scaling, the claim is withdrawn, and a fair equal-mission batching trade is left explicitly open under P113 |
| 5 | A 15 to 30 kN thrust sensitivity was declared in the ledger and never swept | Swept, and the ledger now carries a "Swept?" column so an unswept sensitivity is visible |
| 6 | Repositioning legs were counted as ignitions, understating the post-primary ignition requirement by about half, and a generic `restarts` field was ambiguous between legs and ignitions | An explicit schema counts legs, impulses per leg, reposition ignitions, disposal ignitions and the post-primary total, and both Case B and Case C are now shown to exceed the assumed ignition budget |

Defect 1 is the one that changed a published number. Defect 6 changed a published conclusion.

---

## Reproducibility

Every computed number in this file comes from `analysis/host_reference.py`, which reads no
network, imports no deployer model, and writes `analysis/results/host_reference.json`.

**How the gate works, stated exactly.** Every table above sits between
`<!-- HOST_REFERENCE:TAG:BEGIN -->` and `<!-- HOST_REFERENCE:TAG:END -->` markers and is generated
by the script. `python3 analysis/host_reference.py --write-doc` writes them; `--check-doc`
regenerates each block and compares the exact text, reporting the first differing line. Because
the label and the value are regenerated together, the gate detects a correct value placed beside
the wrong label and a stale value left in the right row, neither of which the first revision's
gate could see. That gate only asked whether each formatted number appeared somewhere in the file.

**Made to fail on purpose.** A gate is a claim until it has been shown to fail, so nine faults
were injected and the gate was required to catch each one.

| Injected | Caught |
|---|---|
| A correct row moved beside the wrong label, two rows of the minimum-burn table swapped | yes, naming the first differing line |
| A stale value left in the correct row while the correct value appears elsewhere in the file | yes. The old presence-only gate passed this |
| Reference stage mass changed from 1000 to 1200 kg | yes, eight blocks, and the block that could not be generated is named rather than crashing |
| Specific impulse changed from 300 to 310 s | yes, eleven blocks |
| Thrust changed from 20 to 22 kN | yes, eight blocks |
| Minimum burn changed from 2 to 1.5 s | yes, three blocks |
| Reference altitude changed from 500 to 550 km, an orbital result | yes, six blocks |
| A mission-case leg changed from 20 to 25 m/s | yes, the mission-case block |
| Impulses per reposition leg changed from 2 to 1, the restart-count field | yes, the mission-case block |

**What the gate does not cover, stated as plainly.** The markers hold the tables, and the tables
are 12 per cent of this file. Everything else is prose, and prose that restates a generated number
is not compared against anything. Three further faults were injected to establish where the edge
is: a figure altered in a sentence, a unit changed in a sentence, and a verdict word changed in a
sentence. The gate passes all three, because none of them is inside a block.

That is the surface [P114](../OPEN_PROBLEMS.md#p114) lived on. The number in the table was a
correct total and the sentence beside it read that total as one burn, and no gate can catch a
sentence that is wrong about what a correct number means. Sentences here are the author's
responsibility, and the file is written so that a number appearing in prose also appears in a
generated block, where it can be checked.

`--self-test` checks twenty-five identities, including that the rocket equation and the burn-time
inverse agree, that mass flow reproduces thrust from the definition of specific impulse, that a
zero impulse raises apogee by nothing, that the single-burn apogee conserves angular momentum
against a direct vis-viva reconstruction, that apogee rise is monotonic in dv, that the two
Hohmann impulses sum to the total, that the Hohmann inversion round-trips, that a single impulse
always raises apogee by more than the same dv buys as a complete circular transfer, that customer
and reserve dv compose, that ignition accounting closes for every case, and that the plane-change
re-derivation reproduces [`MISSION_ARCHITECTURE.md`](MISSION_ARCHITECTURE.md) section 5.

Sources are references. Calculations run from committed assumptions, and no gate in this
repository reaches the public internet.
