# Four findings, one unmeasured number

Written 2026-08-06. Phase I's analysis is finished. Looking back across what it produced,
four separate results all turn on the same quantity, and this project has never specified or
measured it: the structural damping of the track.

That convergence is not visible from any one run sheet, which is why this file exists.

---

## The four

| Finding | What it says | Where Q enters |
|---|---|---|
| P36, no dynamic design case | Force ripple amplifies 8.18x at the 109 Hz fixed-fixed mode, twelve times per campaign | A17 swept Q = 20-500 and the answer barely moved |
| P37, retention gates | ~~Random vibration gives 11.7-20.2 kN through pins sized for 5.9 kN~~ RESIZED 2026-08-10 by A22 | ~~Load scales as √Q; margin goes 0.56 to −0.10~~ Margin is now positive across the whole range, +0.45 at Q = 30 |
| A7-R, release tolerance | Full push may act unbalanced for only 50.7 µs before 2 °/s tip-off | The release transient is a structural event on the same track |
| E25 / A13, attitude settling | Ideal rigid-body residual is zero; structural ringing is not modelled | Ringing decay time is Q/πf |

Two are HIGH defects. One is a kill criterion. None can be resolved by more analysis.

> ### One of the four is off the list, 2026-08-10
>
> P37 is resized. A22 took the retention gates from 2 x D6 to 2 x D9 A-286 pins,
> capacity 18.2 to 41.0 kN, margin at Q = 30 from −0.36 to +0.45, and positive across
> the entire Q = 10-30 range for eleven grams. That finding no longer turns on Q.
>
> The other three still do, and the asymmetry below is unchanged: P36 does not scale with Q
> at all, so a low measurement rescues nothing. What has changed is that the measurement is no
> longer holding a *negative margin* hostage, it is holding an amplification factor and two
> unmodelled transients.

## Why Q is the binding unknown and not just an input

`sizing.py::track_first_mode()` gives 48 Hz pinned-pinned and 109 Hz fixed-fixed, and checks them
against one static target, above 70 Hz to clear the launch primary band. That is the right
check for launch and it is the only structural criterion the design has.

Everything above is a *dynamic* question, and each one answers differently depending on Q:

- ~~P37 scales as √Q. At Q = 10 the pins hold with margin 0.56; at Q = 30 they are past
  capacity. There is no analysis that resolves this, only a measurement.~~ Superseded
  2026-08-10 by A22. The load still scales as √Q; the *margin* no longer crosses zero, because
  the pins were resized to carry the Q = 30 case. Analysis did resolve this one, by sizing
  against the conservative end instead of waiting for the measurement.
- P36 does not scale with Q at all, and that is the finding. Amplification moves from 6.51 to
  8.33 between Q = 20 and Q = 500, so it is saturated at the lowest damping anyone would assign
 to bolted aluminium. P36 is bad news regardless of what the measurement returns.
- ~~The two together mean the same test is decisive for both, in opposite directions: a low Q
  rescues P37 and does nothing for P36.~~ P37 no longer needs rescuing. The test is now
  decisive for P36 alone, and P36 is the finding a low Q does *not* help, which makes the
  measurement's expected value lower than this file originally argued, not higher.

## What one test would settle

A modal survey with a damping measurement, on the track structure, at the as-built joint.

`docs/QUALIFICATION_PLAN.md` already specifies T-2 (sine sweep, 5-100 Hz, pre- and
post-signature) as a *signature comparison*. On A17's result that is not sufficient: it needs to
report Q at each mode, and it becomes a pass/fail item rather than a before-and-after
check.

T-1 is the other half. The plan already calls it *"the single most likely qualification
failure"*, on the argument that the as-built joint may sit between pinned and fixed and drop the
mode into the primary band. ~~P37 makes it a predicted failure rather than a ranked risk.~~
Since A22 resized the gates, T-1 is back to being a ranked risk rather than a predicted
failure, the mode question stands, but nothing downstream of it is now sized negative.

## What this does to the roadmap

The next milestone is not another analysis. Every analysis this environment can run has been run,
and four of the results now queue behind one measurement.

The cheapest first step is not the modal survey. It is B-1, a Halbach pair on a gaussmeter,
bill of materials and purchase order already written in `docs/BENCHTOP_TESTS.md`, never ordered.
It does not measure Q. What it does is produce the first measured number in a project whose
standing caveat is E4: nothing built or measured at any scale. The modal survey is the second
step and needs a track to exist.

## A19 ranked it against everything else, 2026-08-10

`validation/A19_sensitivity_ranking.md` swept nine assumed inputs against `v_exit`, net efficiency
and kg per satellite. Structural Q returns exactly zero on all three, it has no path to any
headline number, and a ranking that stopped there would have reported it harmless.

It was the only input on that list that moved a margin of safety through zero. Across its
declared range of Q = 10 to 30 the retention-gate margin went +0.559 to −0.100, while the three
ranked outputs move by single-digit percentages under every input that touches them.

A22 acted on exactly that ranking, and the margin no longer crosses zero: +1.51 at Q = 10 to
+0.45 at Q = 30. A19 said measure Q first because it was holding a negative margin hostage;
resizing the gates released the hostage for eleven grams, which was cheaper than the
measurement.

That asymmetry is the argument this file was written to make, and it now has a number behind
it: the headline results are not what is at risk from the unmeasured damping. The design's
viability is. A19's measurement priority puts Q first for exactly that reason.

## What this file is not

It is not a new result, and nothing in it is measured. It is four existing findings put next to
each other so the shared dependency is visible. If the damping measurement returns a low Q, P37
closes and P36 does not. That asymmetry is the useful thing to know before spending anything.
