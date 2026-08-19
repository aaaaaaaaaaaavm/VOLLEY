# A56 — the reservoir at the charge pressure ADR-034 actually adopted

**Bands declared 2026-08-19, before `analysis/reservoir_resized.py` existed.**
Verify with `git show --stat <this commit> -- analysis/reservoir_resized.py`, which must return nothing.

---

## Why this run exists

**[P82](../OPEN_PROBLEMS.md).** [ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) dropped
the charge pressure from **50 bar to 22.7258 bar** and cut gas per shot by **54.55 %**. The
reservoir did not move: `cad/parameters.json` still carries **9.55 L at 200 bar**, which
[A43](A43_reservoir_thermal.md) sized around refills at 50 bar.

**And the store mass ADR-034 quotes is not a sized store.** It is
[A49](A49_design_surface.md)'s gas-ratio scaling of A43's 5.38 kg — **≈ 4.10 kg** — which the ADR
says in its own falsifier 2. **The reservoir saving is the whole of ADR-034's mass argument**,
because the tube itself grew **0.311 → 1.140 kg**.

**A second instance of [P84](../OPEN_PROBLEMS.md) was found starting this run.**
`analysis/fill_window.py` — which `reservoir_thermal.py` imports — still declared
`P_CHARGE = 50e5`. The first repair covered `precharged.py` and stopped there. *That is repaired
in the commit before this one, with A42's own point frozen so its run sheet stays reproducible.*

## What A43 established, and what carries over

**A43's finding was not a volume. It was that the bottle does not warm back up.**

> Conduction through stagnant nitrogen gives a time constant of **17 460 s** against the
> **1200 s** cadence of ADR-020. Nitrogen is a homonuclear diatomic and effectively transparent in
> the infrared, so the wall does not radiate into it; in free fall there is no buoyancy-driven
> convection. **Conduction is the only path**, and it is far too slow. So the **no-relaxation**
> figure is the physically right end rather than merely the conservative one.

**That argument is about the gas, not the pressure, so it should survive the change** — but the
time constant scales with the reservoir's own size, and **the reservoir is about to get smaller.**
*A smaller bottle relaxes faster.* **Whether it relaxes fast enough is the question this run
exists to ask**, and it is not obvious in advance.

## A limitation of A43's script that this run has to fix first

**`required()` searches upward from a 4.0 L floor** — set when the answer was around 9 L. At the
new charge pressure a trial run returns **4.0 L for both orifice sizes**, which is the floor
itself. **The search cannot see below its own starting point**, so A43's script as written cannot
resolve the new answer. *The floor is lowered here and the fact that it was binding is reported
rather than quietly stepped around.*

## The prediction, recorded before the run

**Gas per shot falls 54.55 %, so I expect the required reservoir to fall by roughly the same
share** — near **4.3 L** against 9.55 — and the store with it, to something near **3.1 kg**
against 5.38.

**And I expect A43's central finding to survive**: that the bottle still does not relax inside the
cadence, so the no-relaxation figure stays the right one. **A smaller bottle has a shorter time
constant, but it is starting from 17 460 s against 1200** — an order and a half of margin, which a
factor-of-two size change should not close.

**If the relaxation finding flips, ADR-034 gets a mass saving it has not been credited with**, and
A43's conclusion becomes pressure-dependent rather than physical.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | At **50 bar** the model reproduces A43's **9.55 L** no-relaxation figure within 2 % | The model is not A43's and nothing below is comparable to it |
| **2** | The search floor is **below the resolved answer** at both charge pressures | The result is the floor rather than the requirement, which is the defect this run had to fix first |
| **3** | Required reservoir at **22.7258 bar** is **≤ 6.0 L** | The saving ADR-034's mass argument rests on is not there |
| **4** | The conduction time constant at the resized reservoir still exceeds the **1200 s** cadence by **≥ 5×** | **A43's central finding is pressure-dependent**, the bottle does relax, and the no-relaxation figure was the wrong end all along |
| **5** | Sized store mass at the resized reservoir is **≤ 4.10 kg** — the figure ADR-034 quotes from A49's scaling | **ADR-034's store figure was optimistic**, and its per-satellite number moves |
| **6** | Added mass per satellite with the sized store stays **≤ 2.0 kg** | The design re-crosses the one kill-criterion numerator Gen6 passes |
| **7** | Twelve charges complete off the resized bottle with the **last fill inside the 10 s window** A42 declared | The bottle runs out or the fill stops fitting the cadence, which is what P64 caught A41 doing |
| **8** | The minimum reservoir temperature stays above the **150 K** floor A43 declared | The gas is approaching condensation and the ideal-gas model stops being the right one |
| **9** | **REPORT, no pass/fail.** Required reservoir and store mass against charge pressure, swept, so a future design point can be read off it | — |

## What this run will not do

- **It does not re-open A43's thermal model.** Conduction-only, lumped reservoir, wall at the
  structure temperature, ideal gas, constant c_v. **A43 says its conduction-only assumption is the
  one to attack first and that is still true.**
- **It does not recover the gas vented from the fired chamber.** The changelog notes that the
  chamber vents a full charge every shot and nothing models recovering it.
- **It does not size a real vessel.** The store mass uses A39's **PV/W = 15 000 m** figure of
  merit and A39's own run sheet says real 1.7 L / 200 bar vessels are **underestimated 4–6×** by
  it. **The absolute store mass is soft; the ratio between two charge pressures is much firmer.**
- **E4 stands.** Nothing here is measured.
