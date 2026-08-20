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

---

## Result

**RUN 2026-08-19. Eight of nine bands pass. The saving ADR-034's mass argument rests on is real
and slightly better than the ADR claims — and the one failure is inherited from A43 rather than
created by the resizing.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A43's 9.55 L at 50 bar | **9.550 L** | **PASS** |
| 2 | the search floor is below the answer | 0.50 L against 3.460 and 9.550 | **PASS** |
| 3 | reservoir at 22.7258 bar ≤ 6.0 L | **3.460 L** | **PASS** |
| 4 | conduction τ ≥ 5× the cadence | **7.39×** | **PASS** |
| 5 | sized store ≤ the 4.10 kg ADR-034 quotes | **3.1216 kg** | **PASS** |
| 6 | added mass per satellite ≤ 2.0 kg | **1.3093 kg** | **PASS** |
| **7** | last fill inside the 10 s window | **11.516 s** | **FAIL** |
| 8 | minimum reservoir temperature > 150 K | **161.3 K** | **PASS** |
| 9 | reservoir and store against charge pressure | 7 points, 2.14 → 9.55 L | **REPORT** |

**Band 1 reproduced A43 exactly** — 9.550 L, and its **17 460 s** conduction time constant with it.

### The reservoir, resized

| | A43, 50 bar | **Adopted, 22.7258 bar** | |
|---|---:|---:|---|
| **Reservoir** | 9.550 L | **3.460 L** | **−63.8 %** |
| Vessel | 1.2980 kg | **0.4703 kg** | |
| Gas | 2.2442 kg | **0.8131 kg** | |
| **Store** | **5.3804 kg** | **3.1216 kg** | **−42.0 %** |
| Added mass per satellite | 1.4976 kg | **1.3093 kg** | |

**The reservoir falls further than the gas does.** Gas per shot fell **54.55 %** and the bottle
fell **63.8 %**, because a lower target pressure lets the bottle be drawn further down before it
can no longer fill the chamber. **That is a favourable nonlinearity nobody had claimed**, and it is
why the prediction of ~4.3 L came in at 3.46.

> ### ADR-034's store figure was pessimistic, not optimistic
>
> **The ADR quotes ≈ 4.10 kg from [A49](A49_design_surface.md)'s gas-ratio scaling and flags it in
> falsifier 2 as an estimate that might not hold. It holds, and with 0.98 kg to spare.**
>
> **A sized store is 3.1216 kg.** Falsifier 2 asked whether *"a resized reservoir does not come in
> near the scaled estimate"* — it comes in **24 % below** it, because scaling by gas ratio missed
> the nonlinearity above.
>
> **ADR-034's mass argument is stronger than ADR-034 claimed**, and **P82 closes.**

### A43's central finding survives, with half the margin

**A43's result was never a volume. It was that the bottle does not warm back up** — conduction
through stagnant nitrogen against the 1200 s cadence of ADR-020.

| | A43, 50 bar | Adopted |
|---|---:|---:|
| Conduction time constant | 17 460 s | **8 873 s** |
| **Against the 1200 s cadence** | **14.55×** | **7.39×** |

**A smaller bottle relaxes faster and the margin halves, exactly as predicted, and 7.39× is still
nowhere near closing.** *The no-relaxation figure remains the physically right end rather than
merely the conservative one, and it is not pressure-dependent within this range.*

**The gas gets colder, though.** Minimum reservoir temperature falls **201.9 → 161.3 K**, against
A43's declared 150 K floor. **Band 8 passes by 11.3 K.** At 15 bar it fails outright at 143.7 K —
band 9's first row — so **the floor is a real boundary on how far the charge pressure can be
lowered**, and it sits between 15 and 20 bar.

### The one failure is A43's, not ADR-034's

**Band 7 fails at 11.516 s against the 10 s window.** *It also fails at A43's own point, at
14.391 s* — which this run reports because it computed both.

> **[A42](A42_fill_window.md)'s "4.14 s through a 1 mm orifice, and filling is not the constraint"
> is the FIRST fill, from a full bottle.** By shot twelve the bottle is depleted, the pressure
> ratio has collapsed and the same orifice takes three times as long. **Nothing had looked at the
> last fill.**
>
> **The resizing improves it** — 14.391 → 11.516 s — because a smaller bottle at the same storage
> pressure holds its ratio better. **It does not fix it.**

**This is a defect in the fill design, not in the store sizing**, and the escape is arithmetic
rather than architectural: A42 established the orifice moves the required reservoir by **0.00 %**,
so **a larger orifice buys fill time for no mass.** Recorded as **P87**.

### Band 9 — the store against charge pressure

| bar | Reservoir | Store | Per satellite | τ / cadence | Min T |
|---:|---:|---:|---:|---:|---:|
| 15.0 | 2.140 L | 2.632 kg | 1.2685 kg | 5.37× | **143.7 K — below the floor** |
| 20.0 | 2.980 L | 2.944 kg | 1.2945 kg | 6.69× | 155.9 K |
| **22.7258** | **3.460 L** | **3.122 kg** | **1.3093 kg** | **7.39×** | **161.3 K** |
| 25.0 | 3.880 L | 3.277 kg | 1.3223 kg | 7.98× | 165.7 K |
| 30.0 | 4.860 L | 3.641 kg | 1.3526 kg | 9.27× | 174.8 K |
| 40.0 | 7.030 L | 4.446 kg | 1.4197 kg | 11.86× | 189.5 K |
| 50.0 | 9.550 L | 5.380 kg | 1.4976 kg | 14.55× | 201.9 K |

**A future design point can be read straight off this**, which matters because **P86** may move the
charge pressure — and the **150 K floor between 15 and 20 bar is the boundary it must respect.**

## Consequences

- **P82 closes.** The reservoir is **3.460 L**, the store **3.1216 kg**, and both are written to
  `cad/parameters.json`. ADR-034 falsifier 2 does not fire.
- **A second instance of P84 was found and repaired** before this run — `fill_window.py`.
- **P87 opens**: the last fill does not fit the window, at either charge pressure.
- **A43's conclusion stands** and is now known not to be pressure-dependent above 20 bar.

## What this run did not settle

- **It does not re-open A43's conduction-only thermal model**, which A43 itself says is the
  assumption to attack first.
- **It does not size a real vessel.** A39's **PV/W = 15 000 m** underestimates real 1.7 L / 200 bar
  vessels **4–6×** by A39's own admission. **The absolute store mass is soft; the ratio between two
  charge pressures is much firmer, and the ratio is what this run is for.**
- **It does not recover the gas the fired chamber vents**, which is still unmodelled.
- **E4 stands.** Nothing here is measured.
