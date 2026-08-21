# The velocity ceiling, and why a bigger number would be a worse result

This is the argument the whole architecture rests on. It is written down here because it is the
easiest thing in the project to lose sight of, and because the exit velocity has moved twice
downward while this constraint never moved at all.

## The constraint

Under constant acceleration over a stroke `L`,

```
v = sqrt(2 a L)
```

`L` is set by the host envelope. **`a` is set by the payload, not by the machine** — but by *which*
payload, and against what, is the part this page got wrong for months.

> ## Correction, 2026-08-21: the ceiling is chosen, not derived. **P98**
>
> This page used to read: *"A CubeSat built to the CubeSat Design Specification qualifies to
> roughly 14 g quasi-static; NASA GEVS protoflight random vibration integrates to 14.1 g rms,
> whose 3-sigma envelope bounds the launch load near 42 g. This design caps at 25 g, leaving
> margin against the qualification environment rather than consuming it."*
>
> **Every step of that is a category error.** `g_rms` is the root-mean-square of a stationary
> random process over a broadband spectrum. Three times it is a peak-response estimate *for that
> process*, not a quasi-static limit load, and a structure qualified to a random-vibration
> spectrum is not thereby qualified to a sustained 160 ms acceleration of the same nominal
> magnitude. **The "14 g quasi-static" figure was 14.1 g rms with its units quietly changed.**
>
> **And no replacement exists.** The CubeSat Design Specification does not publish a universal
> quasi-static qualification level; it defers test levels to the launch provider, so they vary by
> vehicle and by mission. This repository holds no launch-vehicle user guide and no
> payload-specific load case.
>
> **What is true:** 25 g is a ceiling *this project chose*, and everything downstream — the
> retention chain, the cradle preload, the abort logic, the payload-family table, A27, A38, A63,
> A65 — is sized against it consistently. **It is a requirement, not a capability**, and it must
> never be quoted as evidence that any satellite is qualified for it.

**25 g is this design's own ceiling.** The table below prices velocity against it and against
nothing else; the two rows that referenced a CubeSat qualification level are removed rather than
restated, because there is no source for them.

| Acceleration | Over the 1.30 m acceleration zone |
|---|---|
| **10.07 g, as designed** | **16.0 m/s** |
| **25 g, the chosen design ceiling** | **25.3 m/s** |

**The machine is not velocity-limited. It is mass-limited.** It currently runs at 10.07 g against
its own 25 g ceiling, using 40 % of that headroom, because the sled measured 9.445 kg
rather than the 4.86 kg assumed (P15). Recovering velocity means removing sled mass or raising
thrust. It does not mean accepting more g, and there is no version of this machine where it does.

**Whether a 10.07 g, 162 ms event is acceptable to any particular satellite is a payload-specific
structural question**, settled by that satellite's own qualified load environment and an
integration review. Neither exists here, and **no payload has been mechanically qualified against
this machine.**

## What 200 m/s would cost

Electromagnetic launchers reaching hundreds of m/s are real, and one targets this exact
application. Feng, Yang & Wu reach **321.56 m/s** over a 3.9 m barrel. They do it by putting
**1352 g mean and roughly 3060 g peak** into a purpose-built 20 kg body — **two orders of
magnitude above this design's own ceiling**, and far above the sustained loads small spacecraft
structures are ordinarily built for. *No published standard fixes the CubeSat number that would
make this a ratio (**P98**); what can be said is the order of magnitude.*

Held to this design's 25 g ceiling instead:

| To reach 200 m/s at | Track required |
|---|---|
| **25 g, this design's ceiling** | **81.5 m** |
| 1352 g, Feng's regime | 1.5 m |

Against a 1.5 m machine on a rideshare envelope already 44 % over its target class (P9), 81.5 m
is not a design option. **The choice is not between 16.5 and 200 m/s. It is between an
unmodified satellite and a purpose-built one**, and ADR-003 made that choice deliberately.

## The claim this supports

The headline is not a number. It is:

> **The highest exit velocity reachable over a stroke that fits a rideshare host, while holding
> the payload to a single-digit multiple of g.**

*It used to read "the highest exit velocity an unmodified CubeSat can survive". Nothing here
establishes what a CubeSat survives — **P98** — and the claim is narrowed to what the machine does
rather than to what the payload tolerates.*

That is defensible against a reader who knows Feng's work, in a way "16.0 m/s" alone is not. It
also explains why the two numbers are not comparable: Feng sells velocity to a payload built to
take it, and this sells velocity to a payload that cannot be touched.

**A higher headline reached by exceeding the g-limit would be a worse result**, because it would
require the satellite to be modified or qualified specially, and that is the entire thing this
machine exists to avoid.

## Where the ceiling can legitimately move

Three levers, in `DESIGN_OPTIONS_exit_velocity.md`, and only one raises the ceiling itself:

| | Effect |
|---|---|
| **Sled mass, thrust, two-layer stator** | Move the design *toward* the ceiling. Nothing here exceeds 25.3 m/s at 1.30 m |
| **Momentum-transfer release** (PII-1) | Payload and sled need not separate at the same speed. Raises payload velocity without raising the g it sees during the stroke |
| **Stroke length** | The only lever that raises the ceiling. Costs envelope, and P9 is already the binding packaging constraint |

Everything else is a payload property, and payload properties are not ours to change.

## The one place the ceiling does not apply

A free-flyer is not bound by a rideshare envelope, so `L` becomes a design variable rather than a
constraint. At 25 g, a 100 m deployed track gives 222 m/s and a 300 m track 384 m/s, **without
exceeding this design's own acceleration ceiling at any point**. Feng's velocity, reached by distance instead of
by acceleration.

That is a Phase II programme direction with three unsolved problems in front of it, and it is
recorded in the lab repository rather than here. It is noted on this page only so nobody reads
"25.3 m/s" as a permanent limit on the technology. It is a limit on **this machine, on this
envelope**, which is a different statement.

## Sources

- CubeSat Design Specification, Rev. 14 — **for the interface, not for a load level.** It defers
  test levels to the launch provider and publishes no universal quasi-static case (**P98**)
- NASA GEVS, GSFC-STD-7000, protoflight random vibration — **a random-vibration spectrum.** Its
  `g_rms` is not a quasi-static limit load and is not used as one here (**P98**)
- Feng, Yang & Wu (2025), accelerations *derived here* from their published force and mass
  figures; see [`PRIOR_ART.md`](PRIOR_ART.md)
- Stroke and acceleration-zone geometry: `cad/parameters.json`
- Exit velocity: `analysis/motor_model.py`, reproduced in `analysis/results/motor_results.json`
