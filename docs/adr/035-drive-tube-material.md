# ADR-035: The drive tube is hard-anodised aluminium, and the piston matches it

Status: Accepted, Date: 2026-08-20, Phase: I, Closes: [P85](../../OPEN_PROBLEMS.md), Rests on: A58, A59, A61, A63

## Context

The tube's material has never been stated. [A59](../../validation/A59_tube_structure.md) band 9
went looking and found `analysis/design_surface.py` computing it at 2700 kg/m³ while
`analysis/precharged.py` sizes the chamber, *the same pressure boundary*, at 7800, and
`cad/parameters.json` naming neither. A49 band 7 passed at 1.140 kg without knowing it was
choosing.

It is a 2.15 kg decision on a machine whose added-mass numerator is 1.2145 kg per satellite.

## What the evidence actually says

Four runs have now touched it and three of them are indifferent.

| | | |
|---|---|---|
| Strength | Hoop stress is 17.96 MPa against a 250 MPa allowable, 13.9x margin. | [A59](../../validation/A59_tube_structure.md) band 1. Indifferent |
| Stiffness | Unsupported first mode 1.67 Hz aluminium against 1.68 steel. E/ρ is nearly identical for both metals | A59. Indifferent |
| Buckling | 19.9 N against 57.7 N, and both fail the unsupported case by 45x and 15x. Support at 1.0 m is required either way | A59 bands 3, 4. Indifferent in kind |
| Thermal | 10.79 µm of differential clearance across the 62.1 K swing if the piston and bore differ; 0.00 µm if they match | [A58](../../validation/A58_chamber_thermal.md) band 6. It is matching that matters, not which |
| Mass | 1.1404 kg against 3.294 kg | A59 band 9. Aluminium, by 2.154 kg, 0.18 kg per satellite |

Nothing structural or thermal prefers steel. Only mass discriminates, and it discriminates
decisively.

## The functional requirement nobody had stated

The tube is not primarily a pressure vessel or a beam. It is a sliding seal bore, and
`cad/build_gen6.py` said so in its own docstring before any of these runs: the 1.0 mm wall *"is set
by handling and by carrying A38's 201.7 N cradle preload."*

So the material question is really a surface question, hardness and galling resistance against
a moving seal, and bare aluminium is a poor bore. *Hard anodising is the standard answer, and
it is what makes this decision available.*

> And the duty is far lighter than it looks. The carriage is not recovered, each of the
> twelve satellites has its own. So every seal makes exactly one 8.0 m pass, and the tube sees
> 96 m of total travel across an entire campaign. A pneumatic cylinder bore is qualified for
> kilometres. Wear is not a constraint here and has never been one.

## Decision

The drive tube is hard-anodised aluminium. The piston is the same alloy, anodised or not as the
seal requires, so the two thermal expansions match.

| | |
|---|---|
| Tube | 1.1404 kg, the figure A49 band 7 passed on and ADR-034's mass argument assumed |
| Differential clearance across the 62.1 K swing | 0.00 µm, A58 band 6 satisfied by matching, not by choosing |
| Bore | unchanged at 15.805 mm. [A61](../../validation/A61_seal_class.md) band 7 found a 16.000 mm ISO 6432 stock bore costs 0.00 % on the *seal specification*, but it moves the charge pressure and every number derived from it, so it is a separate decision and is not bundled here |
| Temperature ceiling this accepts | 473 K |

`cad/parameters.json` gains the material, the density, the surface treatment and the temperature
ceiling, so no future run has to infer them.

## What this costs, stated rather than absorbed

It forecloses steam, and that is the largest thing it does.

[A63](../../validation/A63_steam_design_point.md) swept 108 steam design points and none reaches
473 K, the floor is T_sat(p₀) and every charge pressure that makes 2350 J sits above it. A
473 K tube is a nitrogen tube.

A63's conditional was that if the tube were steel for reasons independent of the fluid, steam
becomes +0.341 kg instead of −1.813. *This ADR is that decision, and it goes the other way, on
mass, which is the only axis that discriminates.* Steam is foreclosed by a decision taken on its
own merits rather than by a judgement about steam.

## Falsifiers

This decision is wrong if any of these turns out true.

1. Hard anodising does not survive the thermal cycling. The bore swings 62.1 K every shot
   ([A58](../../validation/A58_chamber_thermal.md)) and the coating and substrate have different
   expansion coefficients. Twelve cycles is few, but nothing has looked at the coating at all.
2. The coating cannot hold the bore tolerance. Hard anodising grows the surface, and an
   ISO H8 bore that is anodised after honing is not the bore that was honed. A dimension nobody
   has specified.
3. [P89](../../OPEN_PROBLEMS.md)'s 17.8 N seal specification cannot be met against an anodised
   aluminium bore. A61 produced the number against no surface at all. *If a harder bore is needed
 to reach it, this reverses.*
4. A fluid change is forced later. If P86 or a customer requirement pushes the design to a
   working fluid needing more than 473 K, this ADR is what has to move first.

> Falsifier 4 is the one to watch. *This is the first decision in the project that closes a door
> rather than opening one, and it is taken knowing that.*

## Alternatives, and why not

Honed E355 steel. Better bore, worse mass by 2.154 kg, and it keeps steam available. The
mass is 0.18 kg per satellite against a 2.0 kg threshold that is already the project's tightest
number, and A63 found steam is a wash even when the steel is free. Paying 2.154 kg to preserve
a wash is not a trade.

Stainless, for a cryogenic-compatible bore. Same mass objection, and A58 found the gas at
237.9 K, cold, not cryogenic, and 135 K above where nitrogen would condense.

Leave it unstated. What the repository has done for eleven months. A49 band 7 passed on a
number nobody had chosen, and this ADR exists because that was found rather than because it
mattered at the time.
