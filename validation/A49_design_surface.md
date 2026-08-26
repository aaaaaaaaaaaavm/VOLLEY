# A49, the velocity, acceleration and stroke surface

**Bands declared 2026-08-16, before `analysis/design_surface.py` existed.**
Verify with `git show --stat <this commit> -- analysis/design_surface.py`, which must return nothing.

---

## Why this run exists

Asked directly: make Gen6 best on velocity, on acceleration, and on power, best overall.

Best at everything is not available and this repository says so elsewhere. What is available
is a design point that dominates the current one on several axes at once, and the record contains
a lever nobody has pulled.

[A37](A37_host_integrated.md) swept stage length at a fixed 25 g and let velocity rise,
27.1 m/s at 1.5 m, 38.4 at 3.0, 62.6 at 8.0. The inverse was never asked. Nothing in this
repository has swept the surface the design point actually sits on.

And a spent upper stage is 8 m long. A37's own stage classes say so. Stroke is the one
variable this architecture can spend freely, because the rail is a vehicle that already exists.

## The two things that make this non-obvious

Peak acceleration is not set by stroke. For a closed expansion, peak force is at the instant of
release: a_peak = p₀·A/m, which contains no *L*. Lengthening the tube does not soften the
shot at all, it lets the expansion continue at ever-falling pressure, adding velocity after the
peak has already happened. *To reduce g you must reduce charge pressure, and then you need stroke
to buy the velocity back.* That is the actual trade, and it is two-dimensional.

Work from a fixed charge rises with stroke. The chamber is fixed, so the gas per shot is fixed,
but the expansion extracts more of it: the constant-pressure ceiling p₀·A·L grows linearly.
More stroke means more work from the same gas, an efficiency term, not just a performance one.

## Method

The gas model is imported from `precharged.py`, not restated. What is added is a sweep over
stroke and charge pressure, and the mass and loss terms that grow with either.

Reported at every point: exit velocity, peak g, gas per shot, chamber and reservoir mass, tube
mass, friction work as a fraction of shot work (P67 scaled over a longer stroke), and the
fraction of the constant-pressure ceiling realised.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | At **L = 2.18 m, p₀ = 50 bar** the surface reproduces A41's **30.535 m/s** and **1864.8 J** within 0.1 % | The surface is not standing on A41 and nothing on it is comparable |
| **2** | Work from a fixed charge is **monotonically increasing** in stroke | The efficiency claim above is wrong |
| **3** | Peak acceleration is **independent of stroke** to within 0.1 % at fixed p₀ | The stated physics is wrong, and the trade is not the one this run is built on |
| **4** | Gas per shot is **unchanged** across a stroke sweep at fixed p₀, within 0.1 % | Same |
| **5** | **A point exists that beats the current Gen6 on exit velocity, peak g and gas per shot simultaneously** | **There is no dominating point, "best overall" is not available even in principle, and the answer to the request is no** |
| **6** | Friction work as a fraction of shot work varies by **≤ 2 percentage points** across the stroke sweep | Lengthening the tube makes **P67** relatively worse, and the longer stroke buys performance by making the worst defect worse |
| **7** | Tube mass at **L = 8.0 m** is **≤ 2.0 kg** | The structure eats the store saving |
| **8** | At the recommended point, **added mass per satellite ≤ 2.0 kg** | The design point re-crosses the one kill-criterion numerator Gen6 currently passes |
| **9** | The **Pareto front is published**, not a single point | The run picks the answer instead of showing the trade, which is what was asked for |

## Predictions, with the arithmetic behind them

These are back-of-envelope and were written before the script. If the script disagrees, the
script is right and the misses are recorded.

1. **Band 3 passes exactly, not approximately.** a_peak = p₀A/m has no *L* in it.
2. **Band 5 passes, and comfortably.** Solving the closed-expansion work for 30.535 m/s at
   L = 8 m gives roughly 18 bar, hence a_peak near 9 g against 25, and gas per shot
   near 0.040 kg against 0.1123, about 64 % less gas for the same velocity at a third of
   the acceleration.
3. **Band 6 passes**, because friction work and shot work both scale with *L*, so the ratio is
   roughly invariant.
4. **Band 2 passes**, and the effect is large: the same 2 L / 50 bar charge yields about
   1172 J at 1.3 m and 5171 J at 8.0 m.
5. **Band 7 passes with room** — a 1 mm aluminium wall on a 15.8 mm bore is order **1 kg** at 8 m.

## Result

**RUN 2026-08-16. Seven of nine bands pass. Band 5 — the one that could have answered the request
with a no — passes fourteen times over. Bands 1 and 6 fail, and both failures are informative.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A41's 30.535 m/s and 1864.8 J | **29.009 m/s**, 1864.8 J | **FAIL** |
| 2 | work from a fixed charge rises with stroke | 1171.9 → 5170.8 J | **PASS** |
| 3 | peak g independent of stroke | **deviation 0.000000 g** | **PASS** |
| 4 | gas per shot unchanged across stroke | deviation 0.000 mg | **PASS** |
| 5 | **a point beats Gen6 on velocity, g and gas at once** | **14 of 63 points** | **PASS** |
| 6 | friction fraction varies ≤ 2 points | **9.25 % → 12.90 %** | **FAIL** |
| 7 | tube mass at 8 m ≤ 2.0 kg | 1.140 kg | **PASS** |
| 8 | added mass per satellite ≤ 2.0 kg | **1.296 kg** | **PASS** |
| 9 | Pareto front published | 9 points | **PASS** |

### The answer to the question that was asked

Yes, a better point exists, and there are fourteen of them. Holding the velocity Gen6 already
delivers and spending stroke on gentleness instead:

| Stroke | Charge | **Peak g** | Gas per shot | vs Gen6 |
|---:|---:|---:|---:|---:|
| 1.30 m | 76.43 bar | 38.22 | 171.7 g | +52.9 % |
| **2.18 m — Gen6 today** | **50.00 bar** | **25.00** | **112.3 g** | — |
| 4.00 m | 32.52 bar | 16.26 | 73.0 g | −35.0 % |
| 6.00 m | 25.84 bar | 12.92 | 58.0 g | −48.3 % |
| **8.00 m** | **22.73 bar** | **11.36** | **51.0 g** | **−54.5 %** |

The same exit velocity at 45 % of the acceleration on 45 % of the gas. Added mass per satellite
falls 1.403 to 1.296 kg, because the store shrinks with the charge faster than the tube grows.

And if velocity is wanted instead of gentleness, the front runs to 52.62 m/s at 8 m and 60 bar
against Gen6's 29.009. The best single point on velocity-per-g is 8 m at 25 bar: 30.97 m/s at
12.50 g on 56.2 g of gas, which beats today's design on all three simultaneously.

### Why stroke is the lever, in two facts the sweep confirms

Peak acceleration does not depend on stroke at all, deviation 0.000000 g across 1.3 to 8.0 m.
a_peak = p₀A/m, and there is no *L* in it. Lengthening the tube softens nothing. What it does
is let the expansion continue after the peak, adding velocity at falling pressure. *To reduce g you
drop the charge pressure, and stroke is what buys the velocity back.*

Work from a fixed charge rises with stroke: 1171.9 J at 1.3 m to 5170.8 J at 8.0 m, on
identical gas. That is 4.4x the work from the same 2 L at 50 bar, and it is why the gas column
above falls so fast.

### Band 6 failed, and my prediction was backwards

I predicted the friction fraction would be roughly invariant, reasoning that friction work and
shot work both scale with *L*. They do not. Friction work scales *linearly*; shot work
saturates toward the constant-pressure ceiling. So friction grows faster than the shot does:

| | 1.3 m | 2.18 m | 8.0 m |
|---|---:|---:|---:|
| Ceiling realised | 91.9 % | 87.2 % | **65.9 %** |
| **Friction share of the shot** | **9.25 %** | 9.75 % | **12.90 %** |

This is the real cost of the long-stroke direction, and it is P67 getting worse. The defect
that already owns 93.4 % of the dispersion also takes a growing share of the energy as the tube
lengthens. A longer machine is more sensitive to a seal nobody has measured, not less.

### Band 1 failed on a definition, and the definition is P67

Work matches A41 exactly, 1864.8 J. Velocity does not: 29.009 against 30.535.

A41's figure is zero-friction. This surface includes friction, so it lands on A44's
with-friction number instead. *The band asked the surface to reproduce a figure computed without a
term the surface contains.* **My declaration error**, in the same family as A48 band 5 and A40
band 1 — and it is the third time this project has recorded that **30.535 m/s is a number with a
condition attached that keeps getting dropped.

**The band stands as failed.** The prediction that went with it — 18 bar and 9 g — was computed
against the zero-friction 30.535 and so is low; the with-friction answer is 22.73 bar and
11.36 g. Directionally right, both magnitudes out by about a quarter, for the same reason.

## What this run does not do

- It does not size a store. The 4.10 kg at the recommended point is A43's store scaled by
  the gas ratio, an estimate, not a sized design, and it is labelled as one in the JSON.
- No bending, no alignment tolerance, no dynamic seal behaviour. An 8 m tube on a stage has a
  straightness requirement this run does not state and cannot meet by assumption.
- The 8 m stage is A37's largest class and no launch provider has agreed to any of it.
- **Friction is Coulomb and constant**, which band 6 has just shown is the term that matters most.
