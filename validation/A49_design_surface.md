# A49 — the velocity, acceleration and stroke surface

**Bands declared 2026-08-16, before `analysis/design_surface.py` existed.**
Verify with `git show --stat <this commit> -- analysis/design_surface.py`, which must return nothing.

---

## Why this run exists

**Asked directly: make Gen6 best on velocity, on acceleration, and on power — best overall.**

**Best at everything is not available and this repository says so elsewhere.** What is available
is a design point that dominates the current one on several axes at once, **and the record contains
a lever nobody has pulled.**

**[A37](A37_host_integrated.md) swept stage length at a fixed 25 g and let velocity rise** —
27.1 m/s at 1.5 m, 38.4 at 3.0, 62.6 at 8.0. **The inverse was never asked.** Nothing in this
repository has swept the surface the design point actually sits on.

**And a spent upper stage is 8 m long.** A37's own stage classes say so. **Stroke is the one
variable this architecture can spend freely**, because the rail is a vehicle that already exists.

## The two things that make this non-obvious

**Peak acceleration is not set by stroke.** For a closed expansion, peak force is at the instant of
release: **a_peak = p₀·A/m**, which contains no *L*. **Lengthening the tube does not soften the
shot at all** — it lets the expansion continue at ever-falling pressure, adding velocity after the
peak has already happened. *To reduce g you must reduce charge pressure, and then you need stroke
to buy the velocity back.* **That is the actual trade, and it is two-dimensional.**

**Work from a fixed charge rises with stroke.** The chamber is fixed, so the gas per shot is fixed,
but the expansion extracts more of it: the constant-pressure ceiling **p₀·A·L** grows linearly.
**More stroke means more work from the same gas** — an efficiency term, not just a performance one.

## Method

**The gas model is imported from `precharged.py`, not restated.** What is added is a sweep over
stroke and charge pressure, and the mass and loss terms that grow with either.

Reported at every point: exit velocity, **peak** g, gas per shot, chamber and reservoir mass, tube
mass, **friction work as a fraction of shot work** (P67 scaled over a longer stroke), and the
**fraction of the constant-pressure ceiling realised**.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

**These are back-of-envelope and were written before the script. If the script disagrees, the
script is right and the misses are recorded.**

1. **Band 3 passes exactly, not approximately.** a_peak = p₀A/m has no *L* in it.
2. **Band 5 passes, and comfortably.** Solving the closed-expansion work for 30.535 m/s at
   **L = 8 m** gives roughly **18 bar**, hence a_peak near **9 g** against 25, and gas per shot
   near **0.040 kg** against 0.1123 — **about 64 % less gas for the same velocity at a third of
   the acceleration.**
3. **Band 6 passes**, because friction work and shot work both scale with *L*, so the ratio is
   roughly invariant.
4. **Band 2 passes**, and the effect is large: the same 2 L / 50 bar charge yields about
   **1172 J at 1.3 m and 5171 J at 8.0 m.**
5. **Band 7 passes with room** — a 1 mm aluminium wall on a 15.8 mm bore is order **1 kg** at 8 m.

## Result

*Not yet run.*
