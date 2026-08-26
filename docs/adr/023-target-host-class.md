# ADR-023: The target host is a spent upper stage, not an ESPA-Grande port

Status: Accepted, Date: 2026-08-10, Phase: I, Closes: P9

## Context

The closed installed envelope is 1839 x 530 x 940 mm (`cad/parameters.json`). The 1839 mm
length exceeds the ~1270 mm ESPA-Grande longest-dimension class by 44 %, because the brake
lives past the 1500 mm release point and the enclosure spans it.

This is `docs/KILL_CRITERIA.md` threat 2, and it is recorded there as crossed. The length is
structural rather than packaging slack, so it does not come out by tidying.

The alternative was priced before choosing. `analysis/owner_decisions.py`: the overhead that
is not acceleration zone, coast/trim, arrest section, skin, flange, is 539 mm and does not
shrink, so fitting a 1270 mm envelope means cutting the acceleration zone to 731 mm. Exit velocity
goes as √s at constant commanded force:

| | Envelope | Accel zone | Exit velocity | Payload KE | Lifetime multiplier |
|---|---:|---:|---:|---:|---:|
| As designed | 1839 mm | 1300 mm | 16.388 m/s | 537 J | x1.62 |
| Fit ESPA Grande, as drawn | 1270 mm | 731 mm | 12.286 m/s (−25.0 %) | 302 J | x1.44 |
| Fit ESPA Grande, 150 mm repackaged | 1270 mm | 881 mm | 13.495 m/s (−17.7 %) | 364 J | x1.49 |

## Decision

The target host class is a restartable upper stage, kick stage, or hosted orbital platform,
POEM class. ESPA-Grande envelope compliance is not a requirement of this design.

The ESPA bolt pattern remains the mechanical interface. That is a mounting standard and is
unaffected; what is being given up is compliance with the *port envelope* of an ESPA-Grande
rideshare slot, which is a different thing. The deployer mounts on a stage, not in a port.

## Why this one

1. It is what the accepted architecture already says. ADR-002 put the host as a spent
   upper stage in 2023 and ADR-010 specified the interface host-agnostically. `paper.tex` §VII
   works POEM as the flown precedent. The ESPA-Grande requirement was a leftover from an earlier
   framing and had already been contradicted by two accepted decisions. Making it explicit
   removes an inconsistency rather than creating a concession.
2. Shortening spends the headline number to enter a market the architecture was not designed
   for. −25 % of exit velocity is the largest single degradation available to this design, and
   velocity is what every product claim rests on: the phasing case, the lifetime multiplier, and
   the comparison against a spring. The 6.6x spring comparator becomes about 5x.
3. It does not fix the threat that is actually closest. Kill criterion 1, mass per satellite,
   is crossed by a factor of three, and a shorter track helps it only marginally while making the
   product weaker. `PAYLOAD_CLASSES.md`, smaller payloads, remains the only change that improves
   several thresholds at once.
4. The repackaging option is not available to be chosen yet. Saving 150 mm of overhead needs a
   brake layout nobody has drawn, and P28 already records that the regen stator and the eddy
   fin do not both fit the 339 mm arrest section. Choosing a branch that depends on undrawn
   geometry would be deciding with a guess inside it.

## What this costs, stated plainly

The ESPA-Grande port population is given up. It is the largest standardised secondary-payload
port class in service, and this design will not fit one. Any market sizing that assumed those
ports is wrong and must be re-scoped, `docs/MARKET.md` should be read against this decision.

## What this does NOT do, and this is the important part

It does not make kill criterion 2 pass. Re-scoping the target after seeing that the geometry
fails is exactly the move this project forbids everywhere else, it is `validation/README.md`'s
band rule, applied to a threshold instead of a band. The criterion is not weakened, deleted, or
re-baselined.

What changes is which host the criterion is evaluated against, and the honest consequence is that
it can no longer be evaluated at all right now:

> Kill criterion 2 moves from CROSSED to NOT EVALUABLE. The threshold, *"if it will not fit a
> rideshare port, the entire hosted-deployer concept has no vehicle"*, stands unchanged. But
> no accommodation envelope for a POEM-class host is public, which is E5, the same
> undisclosed data that keeps the recoil table parametric. Until a host provides stage mass,
> accommodation envelope and control authority, this design cannot demonstrate that it fits
> anything. That is a worse epistemic position than a clean fail against a published number, and
> it is recorded as such rather than as a resolution.

A decision that converts a measured failure into an unmeasurable unknown is not progress, and
this ADR does not claim it is. What it buys is that the project stops carrying a requirement two
of its own accepted decisions had already abandoned.

## Consequences

- `paper.tex`'s driving-requirements list drops ESPA-Grande envelope compliance and states the
  target host class instead. The layout figure caption and the limitations section follow.
- `KILL_CRITERIA.md` threat 2 is rewritten to NOT EVALUABLE, blocked on E5, with the original
  crossed-against-ESPA-Grande finding retained above it as the record.
- E5 rises in priority. It was already named in the paper as the single data exchange that
  converts the analysis from parametric to specific; it is now also the only thing that can put a
  number back on kill criterion 2.
- `cad/parameters.json`'s `espa_grande_conflict` note stays as the record of what was found, with
  its disposition now pointing here.
- P9 closes as a decision. The envelope question it asked is answered; the fit question it
  implied is now E5's.

## Validation

None. This is a product-definition decision. The falsifier is a host accommodation envelope: if
one arrives and 1839 mm does not fit it either, this decision bought nothing and the machine
shortens after all.
