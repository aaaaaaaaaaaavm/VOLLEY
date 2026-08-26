# A21-R, release timing as the free baseline for phase, and what survives it

**Bands declared 2026-08-14, before `analysis/comparators.py` gained a release-timing row.**
Verify with `git show <this commit> -- analysis/comparators.py`, which must show no change to
that file.

> ## This is a re-declaration, not an edit
>
> **[A21](A21_comparators.md)'s seven bands stand exactly as declared and all seven passed.**
> Band 3 asserted that *a spring's designed differential velocity is zero*. That is true, it was
> measured, and nothing here contradicts it.
>
> What A21 did not ask is whether differential velocity is the only way to obtain phase
> spacing, and the claim built on top of it, that a spring "cannot achieve 30° of phase by
> design" — does not follow from band 3 and is false. **The band was right and the conclusion
> drawn from it was wrong. A21-R adds the comparator A21 never declared. It does not touch A21.

---

## Why this run exists

P56. The front door, `SUMMARY.md`, `docs/CONCEPT.md`, `docs/LANDSCAPE.md` and the manuscript
compare 30° of constellation phase spacing against differential drag at ~25 days, and describe
it as unreachable with a spring.

Satellites released at different times from the same host arrive at different true anomalies in
the same orbit, at zero Δv. The comparator was never declared and never computed, and this
project's own adopted cadence, [ADR-020](../docs/adr/020-inter-shot-cadence.md), 1200 s between
shots, already produces phase separation before the motor does anything.

Found by a literature check, not by a reviewer, which is the only reason it is being fixed
before publication rather than after.

## What is being compared

| | Mechanism | What sets the spacing |
|---|---|---|
| **Release timing** | wait between shots; the host carries the next satellite along its orbit | the clock |
| **Commanded differential** | different exit velocity → different semi-major axis → different period | the motor |
| **Differential drag** | different ballistic coefficient → different decay rate | attitude, over weeks |

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | In-track angular rate at 450 km agrees with the two-body period to **≤ 0.1 %** | The baseline is computed wrong and everything below is worthless |
| **2** | Time to 30° by **release timing alone** is **≤ 1 %** of the time by commanded differential | The free baseline is not materially faster, and the published claim survives |
| **3** | The adopted **1200 s** cadence yields **≥ 60°** of in-track separation per shot | ADR-020 does not already exceed the spacing the claim celebrates |
| **4** | Under commanded differential, the in-track phase rate at the moment 30° is reached is **non-zero** — the spacing **does not hold** | Commanded differential gives a static offset after all, and release timing has no advantage in kind |
| **5** | After timed release, semi-major axis equals the host's to **≤ 1 m**; after a commanded shot it differs by **≥ 1 km** | **The claim that survives does not survive.** This is the positive result: timing cannot change an orbit and Δv can |
| **6** | Orbital lifetime after timed release is **within 0.1 %** of the host's, and after a commanded shot is **≥ 50 % greater** | Lifetime extension is reachable without the machine |

### Band 5 and band 6 are the point of this run

Bands 2–4 are expected to embarrass the published claim. **Bands 5 and 6 are the ones that decide
whether the project has a product at all. If timed release could also change the orbit, there
would be nothing left. It cannot, and these bands are where that is measured rather than asserted.

### What this run does not do

It does not price **plane** spacing, which is [A15](A15_poem_campaign.md) band 4's nodal-drift
result and a different question. It does not model station-keeping, drag differences between
satellites, or the host's own drift. A propulsion-less satellite cannot null a drift it is
given**, and that asymmetry is the substance of band 4, not a limitation of the model.

---

## Results

**RUN 2026-08-14. Six of six bands pass. The published claim does not survive; the design does.**

| # | Band | Result | |
|---|---|---|---|
| R1 | in-track rate agrees with two-body to ≤ 0.1 % | **0.0641 °/s** | **PASS** |
| R2 | timing ≤ 1 % of commanded time | **0.39 %** | **PASS** |
| R3 | 1200 s cadence ≥ 60° per shot | **76.9°** | **PASS** |
| R4 | commanded offset does not hold | **21.75 °/day, constant** | **PASS** |
| R5 | only Δv changes the orbit | timed **0.0 m**, commanded **28 801 m** | **PASS** |
| R6 | only Δv changes the lifetime | timed **×1.0000**, commanded **×1.602** | **PASS** |

`analysis/comparators.py` was changed by addition only, the diff deletes no line, so A21's
seven bands are provably untouched.

### 30° of phase costs 468 seconds and nothing else

| | |
|---|---:|
| By **waiting** between releases | **468 s — 7.8 minutes** |
| By commanded differential, 10 m/s | 119 174 s — **1.38 days** |
| By differential drag | ~25 days |

255x faster than the mechanism the repository sells, and free. And
[ADR-020](../docs/adr/020-inter-shot-cadence.md)'s adopted 1200 s cadence already delivers
76.9° per shot, two and a half times the target, before the motor is energised.

The claim that a spring "cannot achieve 30° of phase by design" is false. A spring and a clock
achieve it. A21 band 3 measured that a spring's *designed differential* is zero, which is true;
the error was inferring that phase spacing therefore requires differential velocity.

### And release timing is not merely cheaper, it is better

Band R4: a commanded differential sets a **rate**, not an offset. At 10 m/s the phase drifts at
21.75 °/day and never stops. The design passes *through* 30° at 1.38 days and keeps going, and
a satellite with no propulsion cannot null a drift it has been given.

Timed release sets an offset in the same orbit, with zero relative rate. It holds indefinitely.

> For a string-of-pearls constellation, the free method produces the better result. That is
> the uncomfortable form of this finding and it should be stated that way rather than softened.

### What survives, measured rather than asserted

Bands R5 and R6 are why this run exists.

| | Timed release | Commanded shot |
|---|---:|---:|
| Change in semi-major axis | **0.0 m** | **28 801 m** |
| Orbital lifetime | **×1.0000** | **×1.602** |

A clock cannot change an orbit. Only Δv can. Raised apogee, +60.2 % of orbital life against a
spring's +8.2 %, and placement into a chosen altitude shell are unreachable by waiting, by drag,
or by any spring at any preload.

The differentiator is orbit change, and the repository has been leading with phase change,
the one claim of the two that a clock deletes.

### Consequences

1. Every statement of the phase claim is restated as orbit change, with release timing named as
   the correct free baseline for phase. P56.
2. The superlinearity of lifetime in Δv becomes the headline argument rather than a supporting
   one: +6.5 % at 2 m/s, +8.2 % at 2.5, +60.2 % at 16.029, +103.8 % at the 25 g cap.
3. It argues for more velocity, not less. Phase spacing needed only a differential and would
   have justified a far smaller machine. Orbit change scales with absolute Δv, so the design point
   moves the other way.

### Limitations

Plane spacing is not priced here — that is [A15](A15_poem_campaign.md) band 4's nodal drift, a
different question. Station-keeping, inter-satellite drag differences and the host's own drift are
not modelled. The drift asymmetry in R4 is a property of propulsion-less payloads, not of this
model.
