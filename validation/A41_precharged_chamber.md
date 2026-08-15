# A41 — the pre-charged chamber, and the prediction I got wrong before declaring it

**Bands declared 2026-08-14, before `analysis/precharged.py` existed.**
Verify with `git show --stat <this commit> -- analysis/precharged.py`, which must return nothing.

---

## Why this run exists

**P63.** [A40](A40_blowdown_transient.md) killed the fixed orifice: **4.7 g mean delivered where
25 is needed**, 14.16 m/s against a 30 m/s band. It named three repairs and chose none. This runs
the third — **charge a chamber to a commanded pressure over the sixty seconds already spent
indexing, then fire it as a closed adiabatic expansion.**

**It has no flow-rate problem by construction**, which is the entire failure A40 found. And
velocity becomes a function of **charge pressure**, measured statically before the shot, rather
than of a valve timed to a millisecond — which is what A40 band 7 measured at **10.53 % per ms**.

## The prediction I made, and why it is not the band

Asked what A41 would find in A40, I said: **the seal, because a pre-charged chamber holds 50 bar
between shots and A40 modelled no leakage at all.**

**I checked it before declaring it and it is wrong by six orders of magnitude.** A 4 litre chamber
at 50 bar is 200,000 mbar·L. One percent of that, drooping over ADR-020's 1200 s inter-shot
interval, permits **1.67 mbar·L/s** — against ordinary static seals at **10⁻⁶ to 10⁻⁹**. The
tolerance is enormous because the charge is large and the interval is short.

**The refined version is not much better.** Dynamic seal friction at 32 m/s, also unmodelled by
A40: 5 % of exit velocity costs 194 J over a 2.18 m stroke, which permits **89 N** of friction on
a 15.8 mm bore. Also comfortable.

Both are declared as bands anyway — **a prediction is worth less when it is only recorded after it
survives.**

## What I now think bites, declared before the run

**The pre-charged chamber wastes gas.** It fills a large dead volume that only partly expands, and
what remains at end of stroke is vented:

| | |
|---|---:|
| Charge per shot, 4 L at 50 bar | **200 bar·L** |
| Twelve shots | **2400 bar·L** |
| A39's bottle, 1.711 L at 200 bar | **342 bar·L** |
| Bottle actually needed | **12.0 L at 200 bar** |

**A39's reservoir is seven times too small for this architecture.** It was sized on *swept* volume
at working pressure — 21.4 bar·L a shot — and a pre-charged chamber spends ten times that per
shot to gain a flat force profile.

**So the design variable is chamber volume and it cuts both ways:** a bigger chamber flattens the
expansion and raises exit velocity toward the constant-pressure ceiling, and costs gas
proportionally. **This run sweeps it.**

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | As chamber volume grows the delivered work approaches **p₀·A·L** within **1 %** | The closed-expansion model does not contain the constant-pressure limit A39 assumed, and nothing below is comparable |
| **2** | The selected point delivers **≥ 30 m/s** at a peak acceleration **≤ 25 g** | The architecture does not reach A37's window |
| **3** | Total store — chamber, reservoir, gas and A39's hardware allowance — **≤ 12.55 kg** | It does not fit the kill-criterion budget, and A37 band 5 fails with it |
| **4** | The reservoir sized for **twelve** shots keeps band 3 | **The gas budget is what kills it**, exactly as predicted above, and a flat force profile is unaffordable |
| **5** | Charge pressure produces exit velocity **monotonically** across at least **20 → 30 m/s** | Velocity cannot be commanded, and Gen6 is a fixed-velocity spring |
| **6** | A **±1 %** charge-pressure error gives **≤ 1 %** velocity error | The precision argument for moving control to the charge stroke does not hold |
| **7** | Permissible leak rate for ≤ 1 % droop over 1200 s is **≥ 10⁻⁴ mbar·L/s** | My stated prediction was right after all and the seal is the constraint |
| **8** | Friction budget for ≤ 5 % velocity loss is **≥ 20 N** | The piston seal is tighter than a 15.8 mm bore can give |

### Band 4 is the one that decides the architecture

**Bands 7 and 8 are the prediction, and both are expected to pass by wide margins.** They are here
so that a prediction which fails is on the record as clearly as one that holds. **Band 4 is where
the run is actually at risk**, and it is at risk because of arithmetic done before declaring it
rather than a hunch.

### Band 6 against A40's 10.53 % per ms

If band 6 passes, **commanding velocity by charge pressure is an order of magnitude more precise
than commanding it by valve timing**, and it is a static measurement rather than a transient one.
That is the argument for this architecture over the other two repairs.

## What this run does not do

It designs no chamber, valve, seal or fill circuit. It does not model gas recovery after the shot
— **venting is assumed, and recovering the residual is the obvious repair if band 4 fails.** No
temperature effect on charge pressure, no fill-time check against the indexing window, no
two-phase behaviour, and A34's ≤ 1 N release residual is unchecked. **Every omission makes this
optimistic.**

---

## Results

**RUN 2026-08-14. Eight of eight bands pass. All three of my predictions were wrong.**

| # | Band | Result | |
|---|---|---|---|
| 1 | large-chamber limit approaches p₀·A·L within 1 % | 2139 against 2139 J | **PASS** |
| 2 | ≥ 30 m/s at ≤ 25 g | **30.54 m/s at 25.00 g** | **PASS** |
| 3 | total store ≤ 12.55 kg | **4.66 kg** | **PASS** |
| 4 | the twelve-shot reservoir keeps band 3 | 6.0 L, 1.41 kg of gas | **PASS** |
| 5 | charge pressure spans 20 → 30 m/s monotonically | **16.7 → 30.5 m/s** | **PASS** |
| 6 | ±1 % charge gives ≤ 1 % velocity error | **0.499 %** | **PASS** |
| 7 | permissible leak ≥ 10⁻⁴ mbar·L/s | **0.83 mbar·L/s** | **PASS** |
| 8 | friction budget ≥ 20 N | **83.4 N** | **PASS** |

### The chamber sweep, and why it has an optimum

| Chamber | Exit | Reservoir | Gas | **Store total** |
|---:|---:|---:|---:|---:|
| 0.5 L | 26.16 m/s | 1.50 L | 0.35 kg | 2.29 kg |
| 1.0 L | 28.80 | 3.00 | 0.70 | 3.08 |
| **2.0 L** | **30.54** | **6.00** | **1.41** | **4.66** |
| 4.0 L | 31.55 | 12.00 | 2.82 | 7.82 |
| 8.0 L | 32.11 | 24.00 | 5.64 | 14.15 |
| 64.0 L | 32.62 | 192.00 | 45.12 | 102.67 |

**Velocity saturates and gas does not.** The expansion flattens toward the constant-pressure
ceiling of **2139 J — 32.7 m/s, which is exactly A39's assumption** — while the charge, and so the
reservoir, grows linearly with chamber volume. **Doubling from 2 L to 4 L buys 1.0 m/s and costs
3.2 kg.** The selected point is 2 L at 50 bar.

### Against A39's regulator, and against A40's valve

| | |
|---|---|
| Store mass | **4.66 kg**, against A39's regulated estimate of 2.98 |
| Exit velocity | **30.54 m/s**, against A40's fixed-orifice 14.16 |
| **Added mass per satellite** | **(11.45 + 4.66) / 12 = 1.343 kg** against a 2.0 kg threshold |
| Velocity precision | **0.499 % per 1 % of charge pressure** |

**A37's selected point was 1.608 kg/satellite at 27.1 m/s. This is 1.343 kg at 30.54 m/s** — better
on both, and reached without a regulator, without a flow-rate problem and without a valve timed to
a millisecond.

**Band 6 is the argument for this architecture.** A40 measured valve timing at **10.53 % of
velocity per millisecond**. Charge pressure gives **0.499 % per 1 %**, and it is a **static**
measurement taken before the shot rather than a transient one during it — which is exactly the
precision case made for moving control onto the charge stroke.

### All three predictions failed, and that is the record

| Predicted | Declared tolerance | Actual | |
|---|---|---|---|
| **The seal** would bite | ≥ 10⁻⁴ mbar·L/s | **0.83** | wrong by ~4 orders |
| Refined: **friction** at 32 m/s | ≥ 20 N | **83.4 N** | wrong by 4× |
| Then: **the gas budget** | ≤ 12.55 kg | **4.66 kg** | wrong by 2.7× |

The seal and friction predictions were checked and corrected **before** the bands were declared,
and are recorded in the declaration above. **The gas-budget prediction was not** — it was made in
the declaration, in confidence, and it is wrong because it assumed the 4 L chamber rather than
letting the sweep find the optimum. **At 4 L the store is 7.82 kg and the prediction would have
looked much closer to right.**

> **Three predictions, three failures, on a run where every band passed.** The bands were right and
> the intuition behind them was not, three times in a row, which is the same pattern this
> architecture has shown since A35. **It is an argument for declaring bands, not for trusting the
> person declaring them.**

### What this does not settle

No chamber, valve, seal or fill circuit is designed. **Gas recovery is not modelled** — the
residual 43 bar in the chamber is vented, and recovering it is the obvious lever if the reservoir
ever needs to shrink. No temperature effect on charge pressure, and **no check that a 2 L chamber
can be filled to 50 bar inside the indexing window**, which is now the first thing A42 should ask.
A34's ≤ 1 N release residual is still unchecked against a 202 N preload.
