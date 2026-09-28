# VOLLEY: next-generation product and growth path

Adityavardhan Mishra · 17 September 2026

## Product and customer

VOLLEY is a carrier-hosted system for controlling the departure conditions of
satellites. The carrier performs shared transport and large orbit changes; each
release controls the final separation time, direction and velocity. The current
engineering question is whether that extra control earns its installed cost,
mass, volume and operating burden against a conventional deployer plus host
manoeuvres and timing. It is not assumed to win.

The near-term target customer is the operator of **low-cost, factory-produced,
mission-limited, propulsionless satellite fleets**. Satellites are replenished
as batches, designed for a defined useful mission and a credible end of life.
Examples to investigate are short-duration sensing campaigns, technology tests,
and replenishable observation or communication nodes. These are customer
hypotheses, not confirmed customers, forecasts or evidence of profitable demand.

Propulsionless means **no onboard thrusters after separation, including attitude jets**. It does not
remove payload attitude control, power, communications, thermal control,
navigation support, autonomous safe modes or mission-specific end-of-life
hardware. Expendable means a planned finite service life, not uncontrolled
abandonment. Disposal is a mission requirement from the beginning. Lifetime,
trackability and conjunction response constrain the accessible customers.
A permanently precise formation or arbitrary later manoeuvre cannot be promised
by a one-time release. Removing satellite thrusters transfers some burden to
carrier navigation, release accuracy, orbit selection and replenishment logistics.

## Current architecture decision

Carry forward modular, independently retained mechanical release cells. Charge
a spring/other mechanical accumulator slowly from the electrical bus; measure
charge state; isolate the charger; release an independent latch; accelerate a
guided pusher; separate the payload; capture and lock the pusher locally. Each cell
contains its own mechanical departure path. Shared power, control and host
navigation remain common-mode services.

The first CAD candidate is a guided linear spring cassette, adjustable preload,
symmetric pusher and disconnected motor/lead-screw charger, as specified in the
[Fusion handoff](CURRENT_CELL_FUSION_HANDOFF.md). It is a bench-layout decision;
no spring, bearing, motor, latch or damper is selected for flight. [P92-S2](REFERENCE_CELL_MECHANICS.md)
and [S7](COUPLED_RELEASE_CAMPAIGN.md) bound why this is worth evaluating. They do
not establish installed superiority or a final velocity requirement.

Keep direct electromechanical push and compact gas as fallback architectures.
Keep conventional spring/timing as the baseline, Gen5 and gas Gen6 as historical
comparators, and BOLLEY as a separate cooperative-interface path. If a simpler
spring gives the same mission outcome for less installed burden, choose it.

## Cost, volume and mass discipline

- Standardize cell datums, sensor logic, commands, service connectors and test
  procedures; use replaceable size-specific cassettes and restrained payload
  adapters. Commonality is an interface strategy, not one oversized universal cell.
- Start with a single coupon, then two independently serviceable cells. Compare
  repeated cells against small shared banks before committing a 12-cell structure.
- Place the force path close to the payload CG; count pusher, catcher, guides,
  restraints, actuators, sensors, harness, electronics, heat paths, fasteners and
  host reinforcement. Exclude reference bodies from mass totals, never real parts.
- Track recurring parts/assembly/test cost separately from development, tooling,
  qualification and integration. Do not advertise a price without quotations.
- Compare installed kg, occupied/keep-out volume, bus power/energy, manoeuvre fuel,
  assembly hours and cost per **successfully delivered mission payload**. Include
  payload adapters and carrier services on both sides of every comparison.

## Scaling mechanics and limits

For payload mass m, retained host mass M and payload/host relative exit speed u:

\[
\Delta v_p={M\over M+m}u,\qquad
\Delta v_h=-{m\over M+m}u,\qquad
J={mM\over m+M}u,\qquad
E_{rel}={1\over2}{mM\over m+M}u^2.
\]

These are free two-body impulsive limits, excluding retained-pusher dynamics and
losses. In the large-host fixed-frame limit, constant-force stroke is
s >= u²/(2a); a zero-end-preload linear spring needs s >= u²/a at the same peak
acceleration. Spring work is k(x_initial²-x_final²)/2. Charger input also pays
friction and conversion losses; catcher sizing follows retained moving mass and
its stopping law. Tip-off depends on angular impulse, approximately
Delta omega = I^-1 (r_contact x J), not exit speed alone.

The [126-case lunar / 42-case size screen](LUNAR_RELEASE_SCREEN.md) demonstrates
why host mass cannot be ignored. At u=4.569852 m/s, a 100 kg payload on a 300 kg
retained carrier receives 3.427389 m/s while the carrier recoils 1.142463 m/s.
A larger satellite is therefore not a CubeSat scaled uniformly in CAD.

| Family | Intended study | Mechanism/interface consequence | Present status |
|---|---|---|---|
| CubeSat cells | 1–12 kg mass studies; actual U-size/ICD selected separately | Replaceable rail/tab-compatible cassette, low tip-off pusher | Current prototype-preparation direction |
| Small-satellite pallets | 25–100 kg illustrative masses | Load-bearing pallet or separation ring; symmetric/synchronized push points | Future scaling study only |
| Larger payload berths | 100–250 kg illustrative masses | Dedicated cradle, ascent restraint, substantial recoil and flexible-body checks | Future concept; no mass or speed rating |
| Dedicated VOLLEY OTV | One carrier, several individually released payloads | Propulsion, tanks, ADCS, navigation, power/thermal, flight software and operations | Far-future system concept |

## Roadmap with distinct claims

First deliver the named LEO cell/coupon package: selected parts, finite-host
release model, installed accounting, tolerances, drawings, assembly/inspection,
instrumented tests and independent review. Next demonstrate a multi-cell host
campaign and reproducible releases physically. In parallel, early lunar and
larger-payload calculations may identify interface requirements without expanding
the current hardware article.

The most ambitious next branch is [lunar delivery](LUNAR_VOLLEY_CONCEPT.md).
Detailed lunar development begins after the current prototype design-review
package satisfies its named exit criteria. A dedicated OTV, larger payload
berths, multi-destination delivery and possible carrier reuse follow only if
mission demand, burden and operations justify them. Replenishment is a new
manifest delivery mission; it does not imply on-orbit docking or reloading.
Those are separate far-future capabilities with no present evidence.
