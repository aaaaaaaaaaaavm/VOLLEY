# A44 — commanded velocity at Gen6, and what actually sets its spread

**Bands declared 2026-08-16, before `analysis/gen6_dispersion.py` existed.**
Verify with `git show --stat <this commit> -- analysis/gen6_dispersion.py`, which must return nothing.

---

## Why this run exists

**The product claim is commanded per-satellite velocity, and at Gen6 that claim is unmodelled.**

Gen5 backed it with a designed loop: **0.0274 m/s at 3σ about a 15.8 m/s setpoint**, on a gain
designed against phase margin after [A28](A28_control_stability.md) found the previous one crossing
over above both track modes. Gen6 has **[A41](A41_precharged_chamber.md) band 6 — an open-loop
sensitivity of 0.499 % of velocity per 1 % of charge — and nothing else.** No sensor, no loop, no
error budget. `precharged.py`'s own header records that it models **no temperature effect on
charge** and **no friction**, and A41 band 8 computed a friction *allowance* rather than a friction.

[A43](A43_reservoir_thermal.md) settled the reservoir temperature this run needs as an input, which
is why it comes second.

## The machine, as a control problem

A closed adiabatic expansion of a fixed chamber. **The commanded variable is charge pressure**;
there is no throttle, no feedback during the stroke, and the shot is over in 133 ms. Whatever
accuracy exists is set *before* the valve opens.

**W = p₀V₀/(γ−1)·[1 − (V₀/(V₀+AL))^(γ−1)]** — imported from `precharged.py`, not restated.

## The terms this run puts in the budget

| | Declared as | Because |
|---|---|---|
| **Charge pressure** | ±0.25 % of full scale, swept to ±0.05 % | an ordinary industrial transducer class; better parts exist and the sweep says what they buy |
| **Payload mass** | ±0.5 % of 4 kg | a satellite is weighed at integration; 20 g is generous for a known article |
| **Seal friction** | ±20 % of A41's **83.4 N** allowance | the allowance is A41's, the spread is not, and no run has ever put a number on it |
| **Chamber temperature at fire** | 250 – 450 K | filling an evacuated vessel from a 300 K source leaves the gas hot; A42 excluded the heat of compression and A43 assumed the chamber sits at 300 K |

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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
   temperature should cancel outright rather than merely be small. **If it does, the thermal
   problem dissolves into a sequencing requirement**: measure chamber pressure immediately before
   firing rather than at the end of the fill.
2. **Band 4 fails, and payload mass is why.** Velocity goes as m^−½, so ±0.5 % of mass is ±0.25 %
   of velocity on its own, against a ±0.125 % contribution from a 0.25 % pressure class. I expect
   mass to be the dominant term and the total to land just above 0.5 %.
3. **Band 8 passes**, and A43's 9.55 L is conservative by roughly a quarter, because a chamber
   filled from a 300 K source ends near γ·T₀ and therefore holds less mass at the same pressure.

## Result

*Not yet run.*
