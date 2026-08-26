# A44, commanded velocity at Gen6, and what actually sets its spread

**Bands declared 2026-08-16, before `analysis/gen6_dispersion.py` existed.**
Verify with `git show --stat <this commit> -- analysis/gen6_dispersion.py`, which must return nothing.

---

## Why this run exists

The product claim is commanded per-satellite velocity, and at Gen6 that claim is unmodelled.

Gen5 backed it with a designed loop: 0.0274 m/s at 3σ about a 15.8 m/s setpoint, on a gain
designed against phase margin after [A28](A28_control_stability.md) found the previous one crossing
over above both track modes. Gen6 has **[A41](A41_precharged_chamber.md) band 6 — an open-loop
sensitivity of 0.499 % of velocity per 1 % of charge, and nothing else. No sensor, no loop, no
error budget. `precharged.py`'s own header records that it models no temperature effect on
charge** and **no friction**, and A41 band 8 computed a friction *allowance* rather than a friction.

[A43](A43_reservoir_thermal.md) settled the reservoir temperature this run needs as an input, which
is why it comes second.

## The machine, as a control problem

A closed adiabatic expansion of a fixed chamber. The commanded variable is charge pressure;
there is no throttle, no feedback during the stroke, and the shot is over in 133 ms. Whatever
accuracy exists is set *before* the valve opens.

W = p₀V₀/(γ−1)·[1 − (V₀/(V₀+AL))^(γ−1)], imported from `precharged.py`, not restated.

## The terms this run puts in the budget

| | Declared as | Because |
|---|---|---|
| **Charge pressure** | ±0.25 % of full scale, swept to ±0.05 % | an ordinary industrial transducer class; better parts exist and the sweep says what they buy |
| **Payload mass** | ±0.5 % of 4 kg | a satellite is weighed at integration; 20 g is generous for a known article |
| **Seal friction** | ±20 % of A41's **83.4 N** allowance | the allowance is A41's, the spread is not, and no run has ever put a number on it |
| **Chamber temperature at fire** | 250 – 450 K | filling an evacuated vessel from a 300 K source leaves the gas hot; A42 excluded the heat of compression and A43 assumed the chamber sits at 300 K |

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | Zero-friction exit velocity at A41's selected point reproduces **30.535 m/s** within **0.1 %** | The formulation is not A41's and nothing after this is comparable |
| **2** | Open-loop sensitivity reproduces A41 band 6's **0.499 % per 1 %** within **2 %** | Same |
| **3** | **Exit velocity varies by ≤ 0.01 % across a 250 – 450 K chamber temperature sweep at fixed fire pressure** | Firing on *measured chamber pressure* does not remove the thermal term, the fill-to-fire delay enters the velocity budget, and A43's chamber assumption propagates into the claim |
| **4** | **3σ exit-velocity dispersion ≤ 0.5 %** at the declared terms | Gen6 cannot command velocity to a precision comparable with the Gen5 loop it replaces, and the product claim needs restating |
| **5** | The **largest single contributor** is identified and accounts for **≥ 50 %** of the variance | The budget has no dominant term to attack and the result is not actionable |
| **6** | Commanding **20 → 30 m/s** by charge pressure keeps 3σ dispersion ≤ **1.5 %** at every setpoint | Precision collapses away from the design point and the machine is only accurate where it was sized |
| **7** | Friction at A41's **full 83.4 N** allowance costs ≤ **10 %** of exit velocity | The allowance A41 declared is large enough to invalidate its own result |
| **8** | Charge mass per shot at a hot fire is **≥ 25 % below** the 300 K figure A43 used | A43's reservoir is *not* conservative in the way this run expects, and the two results disagree about the gas budget |

## Predictions, recorded before the run

1. **Band 3 passes exactly**, because the adiabatic work integral contains only p₀ and V₀ —
   temperature should cancel outright rather than merely be small. If it does, the thermal
   problem dissolves into a sequencing requirement: measure chamber pressure immediately before
   firing rather than at the end of the fill.
2. **Band 4 fails, and payload mass is why.** Velocity goes as m^−½, so ±0.5 % of mass is ±0.25 %
   of velocity on its own, against a ±0.125 % contribution from a 0.25 % pressure class. I expect
   mass to be the dominant term and the total to land just above 0.5 %.
3. **Band 8 passes**, and A43's 9.55 L is conservative by roughly a quarter, because a chamber
   filled from a 300 K source ends near γ·T₀ and therefore holds less mass at the same pressure.

## Result

**RUN 2026-08-16. Six of eight bands pass. Both failures have the same cause, and it is not the
one this run predicted.

| # | Band | Result | |
|---|---|---|---|
| 1 | zero-friction velocity reproduces 30.535 m/s within 0.1 % | **30.535 m/s**, 0.001 % off | **PASS** |
| 2 | sensitivity reproduces 0.499 % per 1 % within 2 % | **0.499 %** | **PASS** |
| 3 | velocity varies ≤ 0.01 % across 250–450 K | **0.000000 %** | **PASS** |
| 4 | 3σ dispersion ≤ 0.5 % | **1.113 %** | **FAIL** |
| 5 | largest contributor owns ≥ 50 % of the variance | **friction, 93.4 %** | **PASS** |
| 6 | 20 → 30 m/s keeps 3σ ≤ 1.5 % everywhere | **2.290 % at 20 m/s** | **FAIL** |
| 7 | full 83.4 N allowance costs ≤ 10 % of velocity | **5.00 %** | **PASS** |
| 8 | hot-fire charge mass ≥ 25 % below the 300 K figure | **28.6 %** | **PASS** |

### The error budget, and the prediction it broke

| Term | 3σ alone | Share of variance |
|---|---:|---:|
| **Seal friction**, ±20 % of the allowance | **0.3115 m/s** | **93.4 %** |
| Payload mass, ±0.5 % | 0.0725 m/s | 5.1 % |
| Charge pressure, ±0.25 % FS | 0.0399 m/s | 1.5 % |

Prediction 2 said payload mass would dominate and named ±0.25 % of velocity as its
contribution. It is 5.1 % of the variance and the prediction was wrong. Seal friction owns the
budget by a factor of eighteen.

And buying a better sensor buys nothing:

| Transducer class | 3σ dispersion |
|---|---:|
| 0.25 % FS | 1.109 % |
| 0.10 % FS | 1.102 % |
| 0.05 % FS | **1.101 %** |

A fivefold improvement in the instrument moves the answer by 0.008 %. There is no
instrumentation route to the claim.

### What actually sets Gen6's precision

**A seal friction that has never been measured, specified, or designed.** A41 band 8 computed an
*allowance*, the machine tolerates up to 83.4 N, and no run since has put a number on what
the friction *is* or how much it varies shot to shot. This run evaluated at the allowance ceiling,
which is the conservative end, and the spread of ±20 % about it is this run's assumption and
nobody's measurement.

**So band 4's failure is conditional, and the condition is the point.** If friction sits near
A41's ceiling with any meaningful spread, Gen6 cannot command velocity to a precision comparable
with the Gen5 loop it replaces. If it sits far below, it can. Nothing in this repository
distinguishes those two cases, and the Gen5 machine did not have this problem because a motor
under closed-loop control corrects a friction it does not have to predict.

**Band 6 fails for the same reason, and shows the shape of it.** Friction is a fixed force, so its
share of the commanded work grows as the setpoint falls: 1.041 % at 30 m/s, 2.290 % at 20 m/s.
Precision is worst exactly where the customer asking for a small trim would use it.

### Band 3, and the one thing that got simpler

Temperature cancels outright, 0.000000 %. The adiabatic work integral contains only p₀ and
V₀, so at a *fixed fire pressure* the chamber's temperature does not appear in the velocity at all.

That turns the thermal problem into a sequencing requirement: measure chamber pressure
immediately before firing, not at the end of the fill. Do that and the fill-to-fire delay, the
heat of compression A42 excluded, and A43's 300 K chamber assumption all drop out of the velocity
budget together. This is the cheapest good news in the Gen6 record and it costs one sensor
placement.

### Band 8, and a credit back to A43

A chamber filled from a 300 K source ends near γ·T₀ = 420 K, holding 80.22 g at 50 bar
against 112.31 g at 300 K, 28.6 % less gas per shot. [A43](A43_reservoir_thermal.md)
sized the reservoir with the chamber at 300 K, so its 9.55 L is conservative by roughly a
quarter if the shot is fired hot. *Not applied.* Firing hot and firing cold are different
sequencing choices and neither has been decided; the credit is recorded, not spent.

### The rated velocity is a zero-friction number

30.535 m/s is the frictionless figure, and it is what `cad/parameters.json` carries and what
ADR-032 quotes. At A41's own full tolerable friction the same charge gives 29.009 m/s. Both are
real, one is the ceiling and one is the floor, and neither should be quoted alone. P67.

## What this run does not do

- No blow-by past the piston, no valve dynamics, no residual pressure ahead of the piston.
- Friction is Coulomb and constant over the stroke. Real seal friction varies with pressure,
  velocity and temperature, and a stick-slip breakaway is not modelled at all.
- The three error terms are independent Gaussians. Systematic drift and shot-to-shot
  correlation are not modelled.
- **No sensor exists.** Band 3's conclusion is a requirement on a transducer nobody has selected.
- Nothing here is measured, and the term that owns 93 % of the answer is the one that has
  never been measured at all.
