# ADR-010: Host-agnostic four-item interface

Status: Accepted, Date: 2026-07, Phase: I

## Context
The paper was written host-specific, around POEM. That made it read as an ISRO proposal rather
than a deployer design.

## Decision
Specify the interface generically, mass and control authority, a 150-300 W recharge feed, a
serial command link, an authorised firing window, and treat POEM and Vikram-1 as worked
examples.

## Alternatives
- Stay host-specific. Rejected: ties the concept's fate to one vehicle.
- Fully abstract, no examples. Rejected: unfalsifiable, and loses the most concrete
  engineering in the paper.

## Consequences
Widens the addressable host set and makes the work legible to any launch provider. Costs
specificity: the recoil table stays parametric because the OAM's mass and control authority
are not public (E5).

> Amended 2026-08-10. This interface specifies only one of its two directions.
>
> Every one of the four items above says what VOLLEY asks of a host, and the paper's
> magnetic keep-out radius does the same. Nothing here states what the deployer does to the
> satellite it is carrying, and that is not a gap in the wording, it is a missing half of the
> interface. A deployer has two interfaces, and only the outward one was ever written.
>
> The inward one is now specified in
> [`../PAYLOAD_ENVIRONMENT.md`](../PAYLOAD_ENVIRONMENT.md): the payload envelope sits at
> 611x magnetometer full scale at its near face and 3.4x at its far face, the field does
> not fall below Earth's own until z = 332 mm against an envelope ending at 120 mm, and the
> exposure is continuous rather than per-shot because the array is a permanent magnet.
>
> This qualifies the project's central claim. "The satellite is never modified" is true
> mechanically and electrically. It is not established magnetically: a saturated magnetometer
> recovers, but remanent magnetisation of soft-magnetic parts does not, and which one applies
> depends on a payload materials list this project does not have (P34, still open).
>
> The decision above is unaffected, specifying the interface generically was right, and a
> payload environment specification is *more* host-agnostic than a keep-out radius, not less.
> What changes is that the interface is now four items outward and one specification inward.

## Validation
The interface is exercised against two real vehicles in the paper. One data exchange,
stage mass, thruster impulse budget, coast duration, converts it from parametric to specific.
