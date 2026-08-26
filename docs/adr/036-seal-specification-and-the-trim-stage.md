# ADR-036: The seal is specified at 17.8 N, and the trim stage is suspended rather than built

Status: Accepted, Date: 2026-08-20, Phase: I, Amends: [ADR-033](033-gen6-trim-stage.md), Closes: [P89](../../OPEN_PROBLEMS.md), Rests on: A55, A58, A61

## Context

No new analysis was performed for this decision. [A61](../../validation/A61_seal_class.md) ran
it on 2026-08-20 with its bands declared first, and band 3 passed. What follows is the decision
A61 earned and did not have the authority to take.

[ADR-033](033-gen6-trim-stage.md) added a motor to correct a dispersion. A61 found that the
dispersion is a property of a seal nobody has chosen, and that choosing one moves the whole
chain:

| | A41's allowance, 18.71 % | At A61's 5.00 % |
|---|---:|---:|
| Friction work per shot | 667.2 J | 178.4 J |
| Friction share of shot work | 28.39 % | 7.59 % |
| 3σ dispersion | 3.9798 % | 0.9051 % |
| Authority needed | 1.1543 m/s | 0.2982 m/s, below A48's original 0.323 |
| Section | 144.0 mm | 41.6 mm |

And the requirement that actually binds is tighter still. A61 band 6 *failed*, and the failure
is the finding: a 2 g seal must stay within 50 K of its own friction heating,
[A58](../../validation/A58_chamber_thermal.md) band 5, P88, which needs 4.00 %, 17.8 N,
against the 5.00 % at which the trim stage stops earning its mass.

> So any seal that survives its own heat also makes the trim stage unnecessary. The two
> requirements are not in tension; one strictly implies the other, and the 5.00 % column above
> is therefore the conservative end of this decision rather than its premise.

## The thing nobody had noticed, in A61's own words

> *"The project has been sized, since A41, against the worst common seal class, and nobody ever
> chose it. A55's dispersion, A54's store, A58's seal heating and A49's band 6 failure all descend
> from a number declared as an allowance."*

83.4 N is a ceiling, not a prediction. It is the most friction A41 declared the design could
tolerate. Every headline that descends from it is therefore an upper bound presented as a design
point, including the 3.9798 % this repository now publishes as Gen6's dispersion, and the
144.01 mm section [A55](../../validation/A55_trim_authority.md) sized to correct it.

A design sized against its own worst case is not conservative if it then buys hardware to fix the
worst case. *It is paying twice for a number it has never measured.*

## Decision

Three parts, and the third is the one that costs something.

1. The seal specification is adopted: 4.00 % of p₀·A, 17.8 N, set by the thermal case. It
   enters `cad/parameters.json` as a real parameter group rather than living in a run sheet. This
   closes [P89](../../OPEN_PROBLEMS.md) and is required whichever way part 3 goes.
2. The 83.4 N allowance is retained as the allowance it always was, and every figure derived
   from it is to be read as an upper bound. It is not deleted: until P67 returns, the bound
   is the only honest number for a worst-case argument.
3. Work on the trim stage is suspended. No CAD, no pulse-store integration, no
   [A66](../../OPEN_PROBLEMS.md). The section stays in `parameters.json` at A55's 144.01 mm as
   the worst-case sizing, and nothing further is spent on it until P67 says whether it is needed.

The stage is not deleted. Deleting it on a specification would repeat exactly what ADR-033 did
in the other direction, *adopting before the falsifier was answered*, and this project has
already recorded that as a defect once.

## What suspension is worth, stated rather than absorbed

| | |
|---|---|
| [P92](../../OPEN_PROBLEMS.md) does not need to be run now | A stator that may not be built does not need its coupling through a conducting tube computed. The entry stays live and A66 stays unwritten |
| The pulse store stays unintegrated | [A64](../../validation/A64_pulse_store_technology.md) sized it at ~70 g. It does not need to become hardware yet |
| [P34](../../OPEN_PROBLEMS.md) and E35 stay in limbo | The magnets return *only if* the stage is built. Neither defect can be closed or dismissed until P67, and a magnetometer-carrying customer cannot be answered either way today |
| The commanded-velocity claim is unresolved | At 0.9051 % the stage is unnecessary and the declared 0.5 % band is still missed. *Unnecessary and sufficient are different words and this ADR does not conflate them* |

> That last row is the honest limit of this decision. A61 band 3 asked whether the stage beats
> A48's ±0.323 m/s of authority. It did not ask whether the product meets its spec, and it does
> not. *Deleting the trim stage would make Gen6 cheaper and would not make it accurate.*

## Falsifiers

This decision is wrong if any of these turns out true.

1. P67 measures friction above 22.3 N. Then the trim stage is needed, suspension cost time, and
   ADR-033 stands unamended.
2. No seal class reaches 4.00 % dry, in vacuum, at −35 °C. A61 places 4.00 % inside a filled
   PTFE glide ring's 2-10 % handbook range *but not at its loose end*, and explicitly does not
   claim any class achieves it.
3. A customer requires the declared 0.5 % band. Then the stage returns regardless of what the
   seal weighs or what it costs, because at 0.9051 % the open-loop machine does not meet it.
4. The thermal case is wrong. A58 band 5's 50 K limit on a 2 g seal is what sets 4.00 % over
   5.00 %. If that limit is loose, the binding requirement changes and so does the specification.

## Alternatives, and why not

Delete the trim stage now. Rejected: it rests on a specification, not a measurement, and
falsifier 1 is a bench test away. The saving is real and it will still be there after P67.

Build the trim stage at 144.01 mm. Rejected: it sizes hardware against A41's ceiling, which
A61 has now shown is 4.7x looser than what the seal must achieve for unrelated thermal reasons.
It is the most expensive way to be wrong.

Run A66 first. Rejected: computing how well a stator couples through the tube is only worth
doing for a stator that is going to exist. P92 stays live precisely so this is not forgotten.
