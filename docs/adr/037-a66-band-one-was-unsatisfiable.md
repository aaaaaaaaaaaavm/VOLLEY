# ADR-037: A66's first band was unsatisfiable by a correct implementation, and is withdrawn rather than widened

Status: Accepted, Date: 2026-08-30, Phase: I, Rests on: [A66](../../validation/A66_tube_shielding.md)

## Context

I declared A66's six bands in `e05551b`, before `analysis/tube_shielding.py` existed, and band 1
reads:

> The sheet model returns transmission 1.000 and zero induced loss at zero conductivity, and
> reproduces the analytic thin-sheet transmission for a travelling wave to **0.5 %** across at
> least two decades of sheet conductance.

The run in `af526a0` failed it at 1.4874 %.

My standing rule is that a band is never edited after a result. That rule exists to stop me
moving a target I have already missed, and it is not in question here. What is in question is
whether this particular row was a target at all.

## What the failure actually is

A66 computes the transmission twice. The sheet route lumps the wall into a surface current and is
exact only in the limit of a vanishing wall at fixed sheet conductance. The slab route resolves
the field through the thickness by matching `A` and `∂A/∂y` at both interfaces and makes no
thin-wall assumption. Band 1 compared them and required 0.5 %.

The two are approximations of different order in the wall thickness, so their disagreement is not
free to be small. It is set by the geometry. The test that settles it is to hold the sheet
conductance `σd` at the design value, 35 000 S, and shrink `d`: a correct thin-sheet
implementation must converge on a correct slab implementation, and the rate is the diagnostic.

| Wall `d` | `kd` | sheet | slab | disagreement |
|---|---|---|---|---|
| 1.0 mm | 0.13090 | 0.79851939 | 0.81057568 | 1.487373 % |
| 0.5 mm | 0.06545 | 0.79851939 | 0.80468736 | 0.766505 % |
| 0.25 mm | 0.03272 | 0.79851939 | 0.80163926 | 0.389186 % |
| 0.1 mm | 0.01309 | 0.79851939 | 0.79977607 | 0.157129 % |
| 0.05 mm | 0.00654 | 0.79851939 | 0.79914920 | 0.078810 % |
| 0.01 mm | 0.00131 | 0.79851939 | 0.79864559 | 0.015801 % |
| 0.001 mm | 0.00013 | 0.79851939 | 0.79853201 | 0.001581 % |

Every halving of `d` halves the disagreement and every tenth of `d` divides it by ten, to four
figures, across three decades. That is clean first-order convergence, which is the order the
thin-sheet truncation has, and it is the strongest statement available that *both* routes are
implemented correctly. Neither is wrong. The 1.4874 % is the thin-sheet approximation's own
truncation error at the wall VOLLEY actually has, where `kd` is 0.131 and not small.

## The defect in the band

**No correct implementation could have passed it.** A 0.5 % tolerance was set below a truncation
error that the geometry fixes at 1.49 %, so the only code that could have satisfied band 1 was
code in which the two routes shared an error — which is precisely what band 6 exists to detect.
Passing band 1 would have required failing the thing band 1 was written to protect.

Underneath that is a smaller mistake I should name, because it is the reusable one. The row asks
two different questions in one sentence. *Does the code satisfy the limits it must satisfy* is a
property of the implementation, checkable exactly. *Do two methods of different order agree at a
particular geometry* is a question about the physics of that geometry, and its answer is a number
the geometry hands you, not a standard the code can meet. I wrote the second and called it
verification. Band 6 already owned the second, at 10 %, and it passes.

## Decision

Band 1 as declared is **withdrawn as defective**. It is not widened, not re-scoped and not
rewritten in place: the row stays on the run sheet in the words it was frozen in, beside the run
that failed it, and `af526a0` keeps that run untouched.

A replacement, band 1R, is declared in its own commit before `analysis/tube_shielding.py` is
touched again, and it tests the property the table above measures rather than the magnitude of a
disagreement:

1. at zero conductivity the slab's conductive transmission is unity and its total transmission
   equals `exp(-kd)` exactly, to 1e-12 — unchanged, and it passed;
2. at fixed sheet conductance `σd`, the slab converges on the sheet as `d` shrinks, reaching
   agreement within 0.01 % by `d` = 1e-3 mm;
3. the observed convergence order over that sequence is first order to within 0.05.

A wrong implementation of either route breaks the limit or breaks the order. This is a harder gate
than the one it replaces, not a softer one, and unlike the one it replaces it can be met.

## What this does not do

It does not touch bands 2 through 6, which stand as declared. Band 6 still asks the cross-method
question at the design point, at 10 %, and it is now the only band that asks it.

It does not rescue band 3. The section as drawn delivers 0.9356 m/s of the 1.1543 m/s it was
sized for, that band fails, and [P92](../../OPEN_PROBLEMS.md) is real.

It does not open a register entry. [ADR-021](021-freeze-the-register.md) admits a numbered entry
for a model defect that changes hardware behaviour, a defect that makes a published deliverable
wrong, or a validation band miss. The band-3 miss is P92, which is already open and is what A66
was written to answer. The band-1 miss is against a band that is being withdrawn before the run
sheet carries any result at all, so numbering it would record the register's own bookkeeping, and
the freeze bars that. I am recording the choice here so it is visible rather than silent.

## The rule I am taking from it

A verification band states a limit or an identity the implementation must satisfy, or a
convergence order it must exhibit. It does not state a tolerance on the gap between two
approximations of different order, because that gap belongs to the geometry and the geometry was
not consulted when the tolerance was chosen.
