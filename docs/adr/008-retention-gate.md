# ADR-008: Retention gate separates ascent preload from the release path

Status: Accepted, Date: 2025, Phase: I

## Context
NanoRacks experienced a deployment failure traced to a ball-lock mechanism carrying ascent
preload through the release path.

## Decision
A one-shot retention gate at each cassette exit carries ascent preload directly into
structure. The escapement is caged behind it and sees none of that load.

## Alternatives
- Release mechanism carries preload. Rejected, this is precisely the failure being
  designed against.
- Pyrotechnic restraint. Rejected: shock next to brittle magnets, and non-pyro release is
  already the fielded standard (`docs/LANDSCAPE.md`).

## Consequences
Deliberately borrows a lesson from someone else's failure, which is the cheapest kind of
engineering evidence available. Costs a separate one-shot mechanism per cassette. The gate
carries 5.9 kN through two D6 A-286 pins at a margin of 1.2 *(resized to D9 in 2026-08-10's amendment below)*: the thinnest margin in the
design, and the reason T-1 vibration is the likeliest qualification failure.

## Validation
`sizing.py` `retention_gate()`. Qualification test T-1.

---

> ## Amended 2026-08-10: the load case was wrong, and the pins are now D9
>
> The margin above was computed against the wrong case. 5.9 kN is a quasi-static 25 g ascent
> load. A18 found the governing case is random vibration through the track's 109 Hz mode,
> 11.7 kN at Q = 10 and 20.2 kN at Q = 30, past the D6 pins' 18.2 kN capacity, i.e. a
> negative margin. That was P37.
>
> [A22](../../validation/A22_gate_resize.md) resized the gate to two D9 A-286 pins. Capacity
> 18.2 to 41.0 kN; margin at Q = 30 −0.36 to +0.45, and positive across the whole
> Q = 10-30 range, for 11 grams. The quasi-static margin this ADR quotes rises to 3.98.
>
> The decision is unaffected, a shear-pin gate carrying preload directly into structure is
> still the right architecture, and splitting the stack across two gates was available and not
> needed. What changed is the case it is sized against. `sizing.py` and
> `cad/parameters.json` both carry D9.
>
> This entry was the thinnest margin in the design and is no longer. The remaining thin
> margins are in `docs/KILL_CRITERIA.md`, not here.
