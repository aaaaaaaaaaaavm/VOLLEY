# ADR-034: Gen6 spends the stage's whole length, and buys gentleness rather than speed with it

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** I · **Extends:** [ADR-032](032-gen6-stage-integrated-gas-store.md), [ADR-033](033-gen6-trim-stage.md)

## Context

**The request was for a design that is best on velocity, best on acceleration and best on power at
once.** [A49](../../validation/A49_design_surface.md) was run to find out whether such a point
exists, and it answered in two halves.

**The first half is yes.** Band 5 found **14 points out of 63** that beat the adopted Gen6 on exit
velocity, peak acceleration and gas per shot *simultaneously*. "Best overall" is available in
principle, which is not what a reader of A35 or A47 would have predicted.

**The second half is the reason this ADR is not simply "take the best one".** Every one of those
14 points sits at **L = 8.0 m**, which is [A37](../../validation/A37_host_integrated.md)'s entire
usable acceleration length for a large upper stage. **The surface is not a hill with a summit; it
is a line along the far edge of the envelope**, and choosing a point on it is choosing what to
spend the stroke on.

> **Peak acceleration is set by charge pressure alone.** For a closed expansion, peak force occurs
> at the instant of release: **a_peak = p₀·A/m**, which contains no *L*. **Stroke does not soften
> the shot.** It lets the expansion keep working at falling pressure after the peak has already
> happened. A49 band 3 confirmed this to within 0.1 % across the sweep.
>
> So the stroke is not a performance knob. **It is an exchange rate between charge pressure and
> exit velocity**, and the design decision is which currency to hold constant.

## Decision

**Gen6's stroke goes from 2.18 m to 8.0 m, and the charge pressure falls from 50 bar to
22.73 bar.** The exit velocity is held exactly where it was.

| | Gen6 as adopted | **Gen6 at ADR-034** | |
|---|---:|---:|---|
| Stroke | 2.18 m | **8.00 m** | the whole class |
| Charge pressure | 50.0 bar | **22.73 bar** | |
| Exit velocity, at A41's friction allowance | 29.009 m/s | **29.009 m/s** | **held, deliberately** |
| Exit velocity, zero friction | 30.535 m/s | **34.280 m/s** | and see below |
| **Peak acceleration** | 25.00 g | **11.36 g** | **−54.5 %** |
| **Gas per shot** | 112.3 g | **51.0 g** | **−54.5 %** |
| Constant-pressure work ceiling | 2138.6 J | 3567.0 J | +66.8 % |
| Fraction of that ceiling realised | 87.2 % | 65.9 % | **worse** |
| Tube mass | 0.311 kg | 1.140 kg | +0.829 kg |
| Store | 5.38 kg | **3.1216 kg** | **sized** by A56, not scaled — 24 % below this ADR's own estimate |
| Added mass per satellite | 1.403 kg | **1.296 kg** | 1.324 kg with ADR-033's trim stage |

**Velocity is held rather than taken, and that is the substantive choice in this ADR.**

The Pareto front offers **30.97 m/s at 12.5 g** and **52.62 m/s at 30.0 g** on the same 8 m of
stroke. Taking either would raise the headline number. **It would also invalidate every downstream
result in the repository at once** — [A44](../../validation/A44_gen6_dispersion.md)'s dispersion,
[A50](../../validation/A50_campaign_altitude.md)'s campaign, [A15](../../validation/A15_poem_campaign.md)'s
lifetime spread, [A20](../../validation/A20_reachable_envelope.md)'s envelope and
[A52](../../validation/A52_gen6_recoil.md)'s recoil are all computed on 29.009 m/s or its
zero-friction twin. **The velocity increase is available and it is unpriced**, and this ADR
declines to adopt a number whose consequences have not been run.

**What is adopted instead is the half of the trade that costs nothing downstream:** the same
delivered velocity at **45.5 % of the acceleration and 45.5 % of the gas.**

## What this buys that was not asked for

**The payload environment stops being the binding constraint.** 25 g is the payload qualification
cap [A37](../../validation/A37_host_integrated.md) sized its window on, and Gen6 sat exactly on it
with no margin for a customer whose qualification is softer. **11.36 g is 45.5 % of that cap**, so
the acceleration requirement becomes something a customer can be *offered* rather than argued with.

**Gas per shot halves, and gas per shot is what the campaign is metered in.** A campaign of twelve
costs **612.6 g instead of 1347.7 g**. **This is the only axis on which "more efficient in power" has a
defensible Gen6 meaning**, since [A51](../../validation/A51_gen6_power.md) established that Gen6's
electrical draw is **0.26 W averaged and 36 W peak** and was never the constraint.

## What this costs, stated rather than absorbed

**Friction becomes the dominant loss, and it is the one term nobody has measured.**

| | Gen6 as adopted | Gen6 at ADR-034 |
|---|---:|---:|
| Friction work per shot | 181.8 J | **667.2 J** |
| **As a fraction of shot work** | **9.75 %** | **28.39 %** |
| Gap between the two velocity numerators | 5.00 % | **15.38 %** |

**A49 band 6 failed on exactly this** and the failure is recorded as **P78**: friction scales
linearly with contact length while shot work saturates, so a longer tube makes **P67** relatively
worse. At the adopted point **more than a quarter of the gas work is spent on a seal coefficient
that has never been measured on hardware.**

**This is the honest shape of the decision: the point is better on every axis that was asked about
and worse on the axis the repository is least able to defend.**

Three further consequences, each recorded as a defect rather than absorbed here:

| | |
|---|---|
| ~~**P82**~~ | ~~The reservoir is still 9.55 L, sized for 50 bar refills~~ — **CLOSED 2026-08-19 by [A56](../../validation/A56_reservoir_resized.md).** Sized at 22.73 bar it is **3.460 L and 3.1216 kg**, **24 % below** the scaled estimate. *The saving is larger than this ADR claimed* |
| **P83** | ADR-033's trim stage carries **0.323 m/s** of authority, sized against A44's dispersion at a **9.75 %** friction share. At **28.39 %** neither A44 nor A48 has been re-run, and the stage may be under-authority against the dispersion this ADR creates |
| **The rail** | 8.0 m of stroke plus end hardware makes the rail **8.2 m** against A37's **8.0 m** usable acceleration length. **The point consumes the entire class and overruns it by 200 mm.** There is no smaller stage this design point fits |

## Falsifiers

**This decision is wrong if any of these turns out true.**

1. **The measured seal friction is materially higher than A41's allowance.** At 2.18 m that cost
   5.00 % of exit velocity; at 8.0 m it costs 15.38 %, and the sensitivity to the unmeasured
   coefficient roughly triples with it. **P67** is the measurement, and it now governs the design
   point itself rather than a correction to it.
2. ~~**A resized reservoir does not come in near the scaled estimate.**~~ **ANSWERED 2026-08-19 by
   [A56](../../validation/A56_reservoir_resized.md), and it does not fire.** A sized store is
   **3.1216 kg on a 3.460 L reservoir**, which is **24 % below** the ≈ 4.10 kg quoted above — the
   bottle falls **63.8 %** where the gas falls 54.55 %, because a lower target pressure lets it be
   drawn further down. **The mass argument is stronger than this ADR claimed. P82 closed.**
3. **The trim stage cannot cover the wider dispersion.** ADR-033 exists because Gen6 cannot command
   velocity open-loop. If the correction authority has to grow with friction, the pulse store
   ADR-033 never weighed grows with it. **P83, feeding ADR-033 falsifier 1.**
4. **No stage of this class is available.** Every dominating point needs the full 8.0 m. On A37's
   3.0 m class the same charge pressure gives **19.7 g** and the gas saving falls to 21.1 %.
   **This design point has no fallback on a smaller host** — where ADR-032's architecture did.
5. **The 200 mm overrun proves real.** If end hardware cannot live outside the usable acceleration
   length, the stroke shortens and the point moves off the surface A49 published.

> ### The velocity that was not taken
>
> **A reader who wanted the request answered literally should know what was left on the table.**
> **30.97 m/s at 12.5 g and 56.2 g of gas** dominates the adopted Gen6 on all three axes at once
> and is only 6.8 % above the velocity adopted here.
>
> **It is not taken because taking it silently would make eight run sheets wrong**, and this
> repository's rule is that a number moves when its consequences have been run, not when it looks
> better. **The follow-on is named: re-run A44, A50, A52 and A15 at 30.969 m/s, then decide.**

## Alternatives, and why not

**Take the maximum-velocity point, 52.62 m/s at 30 g.** It exceeds the 25 g payload qualification
cap, although [A38](../../validation/A38_tipoff_at_gen6.md)'s tip-off ceiling of **30.9 g** would
permit it. **A band was not widened to admit it** — 25 g is a payload limit, not a preference, and
the tip-off ceiling being higher does not raise it.

**Take an intermediate stroke.** 4.0 m gives 16.26 g and a 35.0 % gas saving, and fits A37's 3.0 m
class no better than 8.0 m does. **The stroke either fits the large class or it does not**, and
inside that class there is no reason to leave length unspent.

**Keep 2.18 m and raise pressure.** Peak acceleration rises with pressure at 1:1 and A38's cap is
already met exactly. **There is no headroom in this direction at all.**

**Do nothing.** Defensible, and it was the state of the repository this morning. It leaves Gen6
sitting exactly on the payload acceleration cap with a full gas bill, when the host supplies six
more metres of rail free.

## Verification

- [A49](../../validation/A49_design_surface.md), seven of nine bands. **Band 1 and band 6 failed**;
  band 1 is recorded as a declaration error (a with-friction surface compared against A41's
  zero-friction 30.535 m/s) and band 6 as **P78**, the real finding above.
- `cad/parameters.json` carries both velocity numerators and the constant-pressure bound.
- `cd cad && python3 build_gen6.py --check` reads the geometry back against them.
