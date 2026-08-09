# Four findings, one unmeasured number

**Written 2026-08-06.** Phase I's analysis is finished. Looking back across what it produced,
**four separate results all turn on the same quantity, and this project has never specified or
measured it: the structural damping of the track.**

That convergence is not visible from any one run sheet, which is why this file exists.

---

## The four

| Finding | What it says | Where Q enters |
|---|---|---|
| **P36** — no dynamic design case | Force ripple amplifies **8.18×** at the 109 Hz fixed-fixed mode, twelve times per campaign | A17 swept Q = 20–500 and the answer barely moved |
| **P37** — retention gates | Random vibration gives **11.7–20.2 kN** through pins sized for 5.9 kN | Load scales as √Q; margin goes 0.56 → −0.10 across Q = 10–30 |
| **A7-R** — release tolerance | Full push may act unbalanced for only **50.7 µs** before 2 °/s tip-off | The release transient is a structural event on the same track |
| **E25 / A13** — attitude settling | Ideal rigid-body residual is zero; **structural ringing is not modelled** | Ringing decay time is Q/πf |

**Two are HIGH defects. One is a kill criterion. None can be resolved by more analysis.**

## Why Q is the binding unknown and not just an input

`sizing.py::track_first_mode()` gives 48 Hz pinned-pinned and 109 Hz fixed-fixed, and checks them
against **one static target** — above 70 Hz to clear the launch primary band. That is the right
check for launch and it is the only structural criterion the design has.

Everything above is a *dynamic* question, and each one answers differently depending on Q:

- **P37 scales as √Q.** At Q = 10 the pins hold with margin 0.56; at Q = 30 they are past
  capacity. There is no analysis that resolves this — only a measurement.
- **P36 does not scale with Q at all**, and that is the finding. Amplification moves from 6.51 to
  8.33 between Q = 20 and Q = 500, so it is saturated at the lowest damping anyone would assign
  to bolted aluminium. **P36 is bad news regardless of what the measurement returns.**
- The two together mean **the same test is decisive for both**, in opposite directions: a low Q
  rescues P37 and does nothing for P36.

## What one test would settle

**A modal survey with a damping measurement**, on the track structure, at the as-built joint.

`docs/QUALIFICATION_PLAN.md` already specifies **T-2** (sine sweep, 5–100 Hz, pre- and
post-signature) as a *signature comparison*. On A17's result that is not sufficient: it needs to
report **Q at each mode**, and it becomes a **pass/fail item** rather than a before-and-after
check.

**T-1** is the other half. The plan already calls it *"the single most likely qualification
failure"*, on the argument that the as-built joint may sit between pinned and fixed and drop the
mode into the primary band. **P37 makes it a predicted failure rather than a ranked risk.**

## What this does to the roadmap

The next milestone is not another analysis. Every analysis this environment can run has been run,
and **four of the results now queue behind one measurement.**

The cheapest first step is not the modal survey. It is **B-1** — a Halbach pair on a gaussmeter,
bill of materials and purchase order already written in `docs/BENCHTOP_TESTS.md`, never ordered.
It does not measure Q. What it does is produce **the first measured number in a project whose
standing caveat is E4: nothing built or measured at any scale.** The modal survey is the second
step and needs a track to exist.

## What this file is not

It is not a new result, and nothing in it is measured. It is four existing findings put next to
each other so the shared dependency is visible. **If the damping measurement returns a low Q, P37
closes and P36 does not.** That asymmetry is the useful thing to know before spending anything.
