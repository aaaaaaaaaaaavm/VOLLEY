# ADR-025: one cell geometry, class-specific inserts

Status: Accepted, Date: 2026-08-10, Phase: I, Extends: ADR-002, Evidence: `validation/A24_fixed_cell_manifest.md`

## Context

`KILL_CRITERIA.md` threat 1 is the one that decides whether VOLLEY has a reason to exist: above
roughly 2 kg of deployer per satellite, a rational customer buys a propulsion module instead.
At 3U the machine sits at 6.375 kg, over by 3x.

The repository's answer has been the payload ladder, smaller classes amortise the same 76.5 kg
across more customers, and 1U at 1.913 kg per satellite crosses the threshold. But
`payload_family.py` states plainly what that number is: a volume ratio, calibrated so the 3U case
returns twelve, with the caveat that "no cassette, cradle or gate exists for any class except
3U." An answer of that kind is arithmetic, and a reader is right to discount it.

Two architectures could turn it into a design, and they are not compatible:

1. A per-satellite shoe. Every class gets its own cradle, its own retention and its own
   release. Velocity stays programmable per satellite all the way down the ladder. It also means
   a new pitch, a new gate, a new cradle and a new qualification campaign per class.
2. A fixed cell with inserts. One cell geometry, sized to the 3U slot the machine already
   has. Smaller classes fly in inserts that subdivide the cell. One pitch, one gate, one cradle,
   one campaign. Mixing happens at ground integration.

## Decision

The fixed cell. One cell of 340.5 x 100 x 100 mm on the existing 104 mm pitch, twelve cells
across two cassettes, with transverse dividers subdividing a cell along x and using the cell's
own walls in section. The per-satellite shoe is deferred to Phase II as PII-13, with an entry
criterion: *a customer who needs true per-satellite velocity control below 3U.*

This follows the flown canisterised-dispenser cell model rather than inventing one, and it is the
choice that leaves the retention gate, the escapement and the cradle exactly as A22 and A23 left
them, a fixed cell changes what is *inside* a slot and nothing about the machine around it.

## The cost, stated because it is the point of the ADR

Velocity becomes programmable per _cell_, not per satellite. Everything sharing a cell leaves
on the same shot at the same commanded velocity.

At 3U, cell = satellite and nothing is lost. Below 3U it is a genuine capability reduction,
and it creates a problem the machine does not have today: cell-mates have a designed
differential of exactly zero, so they never separate from each other. A24 band 6 tested the
obvious fix and it failed at femtosat scale, see P44.

## What A24 found, which changed what this ADR can claim

Three classes are refused outright, which a volumetric model structurally cannot discover:

| Class | Why |
|---|---|
| ThinSat | 114 x 114 x 25.4 mm, two dimensions exceed the 100 mm cell section in every orientation |
| 12U | needs 200 mm in both section axes; there is no second cell in y, because the cassette is 166 mm wide |
| 6U, rotated | survives only as 340 x 100 x 200, consuming two whole cells in z |

The cassette width was the binding constraint and it is written down nowhere else, not in
`KILL_CRITERIA.md`, not in `PAYLOAD_CLASSES.md`.

And threat 1 closes two rungs lower than claimed:

| Class | Ladder said | Designed cell | vs 2.0 kg |
|---|---:|---:|---|
| PocketQube 1P | 0.235 | 0.266 | crosses |
| PocketQube 3P | 0.708 | 0.797 | crosses |
| 1U | 1.913 | 2.125 | no longer crosses |
| TubeSat | 1.866 | 3.188 | no longer crosses |

1U was the class the repository leaned on. A real insert fits three 100 mm units plus two
dividers in a 340.5 mm cell and wastes 37.5 mm, giving 36 per load rather than 40, and 2.125 kg,
*above* the threshold. Threat 1 still closes, on the PocketQube classes, but those are the classes
with no corner rails and no designed interface at all.

## Consequences

- Accepted: one gate, one cradle, one pitch, one qualification campaign, and A22/A23's results
  carry across the whole ladder unchanged.
- Accepted: velocity is per cell. Recorded as a capability reduction below 3U, not hidden.
- Accepted: the fixed-cell architecture is qualified for PocketQube 1P and above, and is
  not qualified for ChipSat/femtosat until P44 closes.
- Rejected for Phase I: the per-satellite shoe. Deferred as PII-13.
- Open: the insert presents CubeSat corner rails to the machine and a class-specific interface
 to the satellite. That is assumed possible and has not been designed. No insert exists in CAD.
- Open: "one campaign" is an assertion until a campaign exists. One geometry makes it
  *possible*, not true.
