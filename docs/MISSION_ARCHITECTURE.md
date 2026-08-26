# The mission VOLLEY actually flies

Written 2026-08-22. The one-line description, *an electromagnetic CubeSat deployer*, has been
wrong since [ADR-032](adr/032-gen6-stage-integrated-gas-store.md), and the shorter it gets the
more wrong it is. This file is the operational concept, and it is the thing every other
document in the programme should be read against.

---

## 1. The problem, in one paragraph

A rideshare secondary inherits the orbit of whoever paid for the launch. It is placed where the
primary was going, at the time the primary was going there, with whatever separation velocity the
dispenser was built with, a few tenths of a metre per second, identical for every satellite in the
canister. A constellation operator who wants twelve satellites spread around a plane, or at two
altitudes, or phased apart, either buys a dedicated launch, or puts propulsion on every satellite,
or waits for differential drag to do it over months.

---

## 2. What VOLLEY is

VOLLEY flies as a secondary system integrated with the launch vehicle's final stage.

1. The vehicle flies its primary mission. Nothing about VOLLEY is in that path.
2. The primary spacecraft separates. The primary customer is served, and served first.
3. Only then does VOLLEY's mission begin. The spent stage is not released as debris at that
   moment. Where the vehicle architecture and the mission rules permit it, the stage stays
   powered, navigated, attitude-controlled and commandable, and becomes a temporary orbital
   delivery vehicle.
4. The stage repositions. VOLLEY releases. Coarse orbital placement is the stage's job; the
   commanded per-satellite separation velocity is VOLLEY's.
5. The stage disposes of itself. Passivation and re-entry, on reserve that was budgeted before
   the first satellite left.

> ### The division of labour is the whole architecture
>
> | | |
> |---|---|
> | HOST STAGE | coarse orbital repositioning, altitude, phase, orbital energy, over orbits to days |
> | VOLLEY | fine per-satellite release state, a commanded velocity, per satellite, in seconds |
>
> Neither half is interesting alone. A stage that repositions still drops every satellite at the
> same speed. A deployer with a commanded velocity still only ever launches from wherever the
> primary was going.

---

## 3. Three resources that are not the same thing

This distinction has been collapsed in casual descriptions of the concept and it must not be.

| | What it is | Whose it is |
|---|---|---|
| 1. Host-stage propulsion reserve | Propellant intentionally reserved for post-primary manoeuvres, or characterised residual a host can actually use. Main engine, auxiliary, RCS, it depends entirely on the vehicle | The launch provider's. VOLLEY does not own it and cannot assume it |
| 2. Host-stage attitude, navigation and power | What keeps the stage pointed, located, powered and commandable after passivation would normally have begun | The launch provider's, and A37 counts a stage kept alive as hardware that exists whether or not VOLLEY's rollup counts it |
| 3. VOLLEY's own deployment actuator | The Gen6 cold-gas system, 2.0 L at 22.7258 bar of nitrogen, a free piston, an 8.0 m bore, and the suspended trim stage | VOLLEY's. It is a different fluid system in a different pressure vessel and it never manoeuvres the stage |

Resource 3 produces the payload's local separation condition and nothing else. It cannot raise
an orbit, and 51.0 g of nitrogen per shot is not a propulsion budget.

---

## 4. Two operational modes

### 4.1 Rapid deployment

After primary separation the stage reaches a deployment attitude, VOLLEY fires the manifest over
a short period, each satellite receiving its own commanded velocity, and the mission ends in
passivation and disposal. Stage manoeuvres are minimal or absent.

*This is the mode that works on the widest range of hosts, and it is the one that survives if the
stage cannot restart.*

### 4.2 Distributed orbit delivery

The host stage retains a planned propulsion reserve, performs one or more manoeuvres across
multiple orbits, and VOLLEY deploys groups at the stage states it reaches. Different groups
reach different altitudes, phases and orbital energies. VOLLEY supplies the fine relative
velocity at each release.

What this mode may not claim. *Arbitrary plane changes.* They are priced below and they are
expensive.

---

## 5. Plane changes, priced

Derived here. Arithmetic shown, circular orbit, impulsive burn, `MU` and `RE` from
`analysis/astro.py`. Plane change: Δv = 2 v sin(Δi/2). Coplanar raise: two-impulse Hohmann.

| Altitude | Circular v | 1° plane change | 0.1° plane change | 10 km altitude raise |
|---:|---:|---:|---:|---:|
| 350 km | 7697.0 m/s | 134.3 m/s | 13.4 m/s | 5.71 m/s |
| 500 km | 7612.6 m/s | 132.9 m/s | 13.3 m/s | 5.53 m/s |
| 700 km | 7504.3 m/s | 131.0 m/s | 13.1 m/s | 5.30 m/s |

> One degree of inclination costs about twenty-four times a ten-kilometre altitude change.
> So the distributed mode delivers altitude, phase and orbital energy. It does not deliver
> planes, and any description of VOLLEY that implies otherwise is describing a different vehicle
> with a different propellant budget. *A tenth of a degree is affordable on a modest reserve; a
> degree is a mission of its own.*

Phase is the cheap one and it is free. [A15](../validation/A15_poem_campaign.md) and
[P56](../OPEN_PROBLEMS.md) record it: release timing gives phase at zero Δv, because two
satellites released minutes apart from the same orbit separate in true anomaly by construction.
*That is a scheduling result, not a propulsion one, and it is the least appreciated part of the
architecture.*

---

## 6. Host classes

No launch provider has agreed to anything ([E5](../OPEN_PROBLEMS.md), and it is `HOST_DATA` in
[`COMPUTATIONAL_CLOSURE.md`](COMPUTATIONAL_CLOSURE.md)). So the product's dependency on the host is
made explicit as classes rather than hidden inside one assumed vehicle.

| | Class A | Class B | Class C |
|---|---|---|---|
| | Controlled spent upper stage kept alive as a platform | Restartable upper stage with a planned reserve | Non-restartable host |
| Attitude, navigation, power after primary | yes | yes | limited or none |
| Post-primary orbital manoeuvres | as reserve allows | planned, multiple | none |
| Rapid deployment | yes | yes | yes |
| Distributed delivery | limited by reserve | yes | no |
| Disposal | controlled or natural re-entry | controlled | natural |

The flown precedent for Class A is ISRO's use of spent PS4 stages as POEM orbital platforms.
What the public record establishes: stages have been reused as orbital platforms after the
primary satellite mission; POEM operations begin after satellite separation; attitude
control and navigation are retained; POEM-3 performed post-primary manoeuvres to approximately
350 km; and the stage re-entered rather than remaining as long-lived debris.

> The precedent is that a stage can be kept alive and used. It is not an endorsement, an
> agreement, or a statement that any provider will host this. *Evidence level: public programme
> record. VOLLEY has no relationship with any launch provider or space agency.*

Class C is not a failure case. It is where the majority of hosts probably sit, and VOLLEY
still works there, it delivers commanded per-satellite velocity from wherever the primary went,
which is a smaller product and a real one.

[`HOST_REFERENCE_CASES.md`](HOST_REFERENCE_CASES.md) is the method for mapping a real, publicly
documented propulsion architecture against these three classes, and the reference cases worked
under it. It uses public sources and declared assumptions only, and it closes nothing here: E5
stays open, and a reference case is a study rather than a compatibility finding.

---

## 7. The mission has to end

No architecture is allowed to spend the last kilogram of stage propellant on customers and then
omit disposal. A complete concept of operations includes:

| | Status |
|---|---|
| Disposal reserve, budgeted before the first release | Not modelled. It is an input to the mission planner that does not exist yet |
| Passivation of VOLLEY's own pressure system, venting the reservoir | Not designed. [E32](../OPEN_PROBLEMS.md) is the nearest live entry |
| Controlled or natural re-entry of the stage | Host-dependent, and a Class B property |
| Collision avoidance during the campaign | [E18](../OPEN_PROBLEMS.md): the conjunction covariance is invented and is a live computation item |
| Mission-duration limit | [E28](../OPEN_PROBLEMS.md): campaign life at a real deployment altitude is not modelled |
| Loss of stage control mid-campaign | [E30](../OPEN_PROBLEMS.md)'s forfeiture case, and A47 counts the stage as the one shared element the project cannot engineer around |

Five of those six are live register entries. *The end of the mission is the least modelled part
of it, and this file exists partly to say so in one place.*

---

## 8. What this file is not

It is not a claim that the machine works. Gen6's exit attitude is not established
([P103](../OPEN_PROBLEMS.md)), its seal friction is unmeasured ([P67](../OPEN_PROBLEMS.md)), and
nothing in this project has been built, fired or measured, E4. It is a statement of what
is being designed, so that every other document can be read against a single description of the
mission rather than four different ones.
