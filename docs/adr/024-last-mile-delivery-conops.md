# ADR-024: VOLLEY is a last-mile delivery vehicle, and the repository should say so

Status: Accepted, Date: 2026-08-10, Phase: I, Extends: ADR-002, ADR-010

## Context

The concept this project was started to pursue is not written down anywhere in it. A search of
every document and of `paper.tex` returns no mention of last-mile delivery, of the host
repositioning between deployments, or of multi-orbit delivery from a single vehicle.

What the repository describes instead is a deployer bolted to a passive host: VOLLEY fires,
the satellites leave, and the host is a mounting surface with a power feed. ADR-002 chose a spent
upper stage as that host, and ADR-010 specified the interface host-agnostically, but both treat
the stage as a place to stand rather than as part of the product.

That is a smaller idea than the one the machine was designed for, and it is why the
repository reads as "a better spring" rather than as what it is.

## Decision

The product is a last-mile delivery vehicle: a spent upper stage that, after primary
separation, repositions on its own reaction-control system between altitude shells and fires
satellites off at individually commanded velocities at each station, then deorbits.

Two configurations are in scope:

1. Hosted, VOLLEY on a spent stage, as above. The stage, its attitude control and its
   disposal burn are paid for by the primary mission.
2. Dedicated, VOLLEY as the sole primary payload of a small launcher, where the whole
   mission is CubeSat distribution.

`docs/CONCEPT.md` states it; `validation/A20_reachable_envelope.md` quantifies the delivery
envelope against a host Δv budget.

## The boundary, fixed here so the framing cannot drift

This is the half that matters, because a delivery claim is easy to overstate.

| Manoeuvre | Cost | In scope? |
|---|---|---|
| Altitude shell change, 50 km | 27.8 m/s, two-burn Hohmann (A20 band 1) | Yes, at a real propellant cost |
| Along-track phase distribution | free, from commanded differential velocity | Yes |
| RAAN separation | free over time, differential J2, A15 measured 367° in 90 days | Yes |
| Inclination change, 1° | 133 m/s, A15 band 8 | No |

Plane change is excluded, permanently and by physics. One shot spent entirely on plane change
buys 0.1229°, confirmed analytically and in GMAT. No document, figure or abstract may imply
that VOLLEY or its host selects an orbit plane. Where planes do separate, it is J2 acting over
the campaign, and that must be described as what it is rather than as a manoeuvre.

> ### Amended 2026-08-10, hours after acceptance, by A20 band 6
>
> Above about 100 m/s of host budget, the stage does most of the delivering. A20 measured the
> host's share of the fleet's altitude extent at 30 % at 50 m/s, 56 % at 100, 75 % at 200 and
> 87 % at 400. Band 6 declared in advance that if this happened it must be stated plainly
> rather than left for a reviewer to find.
>
> So the division of labour is now stated, and it is narrower than this ADR was written:
>
> - The host buys altitude range. VOLLEY buys distribution within it. They are complements,
>   and the product claim must say which does which rather than merging them into "delivery".
> - At zero host budget VOLLEY alone still delivers 117.2 km of altitude extent and 13.2° of
>   RAAN spread over 90 days, so the dedicated configuration stands on its own, and the hosted
>   one is an amplifier rather than a prerequisite.
> - Repositioning is not cheap. 27.8 m/s per 50 km shell, not the ~14 m/s this ADR originally
>   stated, see P40.
>
> The decision is unaffected: the ConOps is still the right framing and the machine still does
> the part no alternative does. What changes is that the *altitude* half of the delivery claim is
> mostly bought with the host's propellant, and saying so is the difference between a positioning
> argument and a brochure.

## Why this framing rather than the deployer framing

1. It is what the machine is for. Programmable per-satellite velocity is only worth building
   if somebody wants satellites in *different* places. Framed as a deployer, the differentiator
   is a bigger number; framed as delivery, it is the reason the product exists.
2. It uses something that is currently thrown away. The stage is deorbited or left to decay
   regardless. Converting that interval into deliveries is the argument that makes VOLLEY's
   marginal cost to a launch defensible.
3. It is the flown precedent, not a proposal. POEM already operates a spent PS4 as a
   stabilised platform with power, navigation, attitude thrusters and controlled reentry.
   Everything the ConOps assumes about the host has been demonstrated by someone; what has not
   been demonstrated is VOLLEY.
4. It positions correctly against transfer vehicles. As a deployer, VOLLEY invites comparison
   with an OTV and loses on Δv by two orders of magnitude. As a right-sized delivery vehicle for
   phase and altitude, the comparison is the correct one and it is favourable.

## What this does not do

- It does not make any new performance claim. No number moves. `v_exit` stays 16.388 m/s.
- It does not establish the host's control authority. The stage Δv budget the envelope is
  computed against is parametric, because POEM-class accommodation and propellant figures are
  undisclosed, E5, the same gap that keeps the recoil table parametric and that ADR-023 left
  kill criterion 2 unevaluable against.
- It does not model the repositioning burns. A20 computes the reachable envelope from a Δv
  budget; it does not design the manoeuvre sequence, the attitude profile during it, or the
  thermal case of a stage loitering for a campaign. Those are unmodelled and named as such.

## Consequences

- `docs/CONCEPT.md` becomes the front-door document, ahead of the motor description.
- `README.md` and `SUMMARY.md` lead with the concept rather than with the linear synchronous
  motor.
- `paper.tex` §VII gains the ConOps framing; the deployment sections should not describe the host
  as passive.
- E5 rises again. It already blocks the recoil table and kill criterion 2; it now also bounds
  the delivery envelope, which makes it the single most valuable external input to the project.

## Validation

A20 quantifies the envelope parametrically. Nothing validates the ConOps itself, and nothing
can until a host operator states a Δv budget and a coast duration. The falsifier is a real
accommodation: if a stage cannot spare tens of m/s for repositioning after its primary mission,
the hosted configuration collapses to single-shell delivery and the dedicated configuration
becomes the only one.
