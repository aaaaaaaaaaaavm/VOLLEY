# A40, the blowdown transient, and how velocity is commanded

**Bands declared 2026-08-14, before `analysis/blowdown.py` existed.**
Verify with `git show --stat <this commit> -- analysis/blowdown.py`, which must return nothing.

---

## Why this run exists

P60, and [A39](A39_store_trade.md)'s own closing paragraph: *"Gas removes a mass problem and
introduces a fluid-system problem, and this run has sized the first and not the second."*

A39 chose cold gas on a quasi-static argument, swept volume times working pressure equals the
energy needed. It never asked whether the gas can arrive in time. Filling a 0.428 litre
swept volume in a 133 ms stroke is roughly 3 L/s at working pressure, and nothing has
modelled the orifice, the valve, or what the reservoir pressure does while it happens.

Nothing about Gen6's geometry can be drawn until this closes. The bore, the reservoir and the
valve are the first three dimensions in `cad/parameters.json`, and all three come out of here.

## And a second question A39 could not ask

A falling reservoir means every shot is different. A39 sized one 1.71 L bottle for twelve
shots by simple blowdown; if pressure droops, shot twelve is slower than shot one, against a
project whose entire proposition is a velocity commanded per satellite.

So this run also asks how velocity is commanded at all with gas. The candidate is valve
cut-off: open the valve, close it at a commanded time, let the payload coast the rest of the
stroke. That makes velocity a function of *timing* rather than of pressure, which is a digital
quantity and is the same trick the linear motor used with current.

## The design point, from A39

| | |
|---|---:|
| Bore | **15.805 mm**, piston area 1.962 × 10⁻⁴ m² |
| Stroke | **2.18 m** |
| Storage / working pressure | **200 / 50 bar** |
| Reservoir | **1.711 L** |
| Force at working pressure | **981 N** — 25 g on a 4 kg payload |
| Swept volume per shot | **0.428 L** |

## Model, declared before the script

Isentropic choked flow from the reservoir through a fixed orifice into the cylinder, integrated
against the payload's equation of motion. Nitrogen, γ = 1.4, R = 296.8 J/kg·K, 300 K.
Discharge coefficient 0.8. Flow unchokes when the pressure ratio exceeds 0.528 and the
subsonic form is used below that. Reservoir expansion is adiabatic; cylinder filling is
treated as adiabatic with the piston doing work.

Assumptions that make this optimistic, named here: no line losses between reservoir and
orifice, no heat transfer to the walls, no seal friction, no valve opening transient other than
the declared ramp, and an ideal gas throughout. Real cold-gas systems lose to all five.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | With the orifice opened to 100 mm², the model reproduces A39's **32.7 m/s** to **2 %** | The transient model does not contain the quasi-static one, and nothing below is comparable |
| **2** | Peak acceleration at the selected orifice ≤ **25 g** | The payload is over-driven at the start of the stroke, which is where gas is at its worst |
| **3** | Shot 1 exit velocity ≥ **30 m/s** | The gas cannot arrive fast enough, and A37's window was priced on a store that cannot deliver |
| **4** | Selected orifice diameter ≤ **10 mm** | The valve is not an ordinary component |
| **5** | On A39's **1.711 L** reservoir, shot 12 reaches ≥ **95 %** of shot 1 | The store depletes across the manifest and the last satellites are slower than the first |
| **6** | Valve cut-off spans a commandable range: cut-off timing produces exit velocities **monotonically** across at least **20 → 30 m/s** | **Velocity cannot be commanded with gas**, and the project's central claim does not survive the architecture change |
| **7** | A **±1 ms** valve-timing error gives ≤ **1 %** velocity error at the selected point | The commanded velocity is not repeatable, and the ±0.10 km apogee claim goes with it |
| **8** | Gas consumed per shot is within **20 %** of A39's declared swept-volume figure | A39's reservoir sizing was wrong and the mass result moves |

### Band 6 is the one that decides whether Gen6 is VOLLEY

Every previous architecture commanded velocity with current. If gas cannot be commanded,
Gen6 is a fixed-velocity spring with extra steps** — and A21 band 3's finding that a spring's
designed differential is zero would apply to it too.

### Band 5 is where the single-bottle result is most likely to fail

A39 sized the reservoir by simple blowdown arithmetic. A transient will not be kinder.

### Band 2 is where gas is physically worst

A spring's force falls as it extends; gas at constant supply pressure does not, so the risk is
at the start of the stroke where the cylinder volume is smallest and the pressure rises fastest.

## What this run does not do

It does not design a valve, a seal, a regulator or a manifold; does not model temperature drop in
the reservoir across twelve shots in sequence, wall heat transfer, or two-phase behaviour; and does
not check the <= 1 N release residual A34 requires. It answers whether the gas arrives in time,
whether it lasts twelve shots, and whether velocity can be commanded.

---

## Results

**RUN 2026-08-14. Three of eight bands pass. The fixed-orifice architecture fails, and one of the
five failures is a badly designed band rather than the physics.**

| # | Band | Result | |
|---|---|---|---|
| 1 | wide orifice reproduces A39's 32.7 m/s within 2 % | **59.47 m/s** | **FAIL** |
| 2 | peak acceleration ≤ 25 g | 25.00 g | **PASS** *(by construction — the orifice is bisected on it)* |
| 3 | shot 1 ≥ 30 m/s | **14.16 m/s** | **FAIL** |
| 4 | orifice ≤ 10 mm | **0.71 mm** | **PASS** |
| 5 | shot 12 ≥ 95 % of shot 1 | **95.5 %** — 13.52 against 14.16 m/s | **PASS** |
| 6 | cut-off spans 20 → 30 m/s monotonically | **1.4 → 8.4 m/s**, monotonic | **FAIL** |
| 7 | ±1 ms timing gives ≤ 1 % velocity error | **10.53 %** | **FAIL** |
| 8 | gas per shot within 20 % of A39 | **3.39 g against 24.02** | **FAIL** |

### The physics, in one line

A fixed orifice cannot hold force over a 2.18 m stroke. The cylinder is smallest at the start,
so pressure peaks there; as the piston runs away the volume grows faster than the orifice can fill
it and the force collapses.

| | |
|---|---:|
| Mean acceleration needed for 32.7 m/s over 2.18 m | **25.0 g** |
| Mean acceleration actually delivered | **4.7 g** |
| Peak, at the very start | 25.00 g |

Bands 3, 6, 7 and 8 are all that one fact. Cut-off can only subdivide a 14 m/s shot; ±1 ms is 10 %
because at a 6 ms cut-off the payload has barely moved; and 3.39 g of gas is consumed because the
cylinder never approaches working pressure.

### Band 1 failed because I declared it wrong, and the failure is informative anyway

The band assumed that opening the orifice wide gives A39's quasi-static case. **It does not.** A
wide orifice fills the cylinder toward reservoir pressure, 200 bar on this piston is 3924 N,
100 g, and the model returns 59.47 m/s accordingly.

A39's 32.7 m/s assumed 50 bar held *at the piston throughout*. That is a regulator. A39 never
said so and this run did not model one, so the two are different machines and the band compared
them as if they were the same. **The band stands as failed and the error is mine**, and what it
exposes is worth more than the band was: **A39's 1.5 kg "piston, seals, regulator and valving"
allowance is not a rounding item. It is the component the whole result depends on, and A39 priced
it without knowing that.

### What survives, and it is not nothing

**Band 5 passes: one 1.71 L bottle does run twelve shots**, with 4.5 % velocity droop from
reservoir depletion. That was the result most likely to fail on a transient and it held.

**Band 4 passes by a wide margin**: 0.71 mm of orifice, against a 10 mm limit. **Flow area was
never the problem. The problem is that a fixed area cannot track a growing volume.

### What A39's result now rests on

Not refuted, but conditional. Cold gas at 2.98 kg assumed a regulated 50 bar at the piston.
This run shows the unregulated version delivers 4.7 g mean where 25 is needed. So the architecture
needs a regulator that holds 50 bar while flowing ~0.36 kg/s and settles inside a 133 ms stroke,
and that component is unpriced. P63.

### Three repairs, named and not chosen

Each is a different machine and each needs its own bands:

1. A regulator, as A39 implicitly assumed. Reopens the hardware allowance and asks whether a
   regulator with that response is inside 1.5 kg.
2. A profiled orifice, flow area opening as the piston travels, cam- or piston-position-driven,
   so area tracks volume. No fast feedback needed.
3. A pre-charged chamber. Charge a fixed volume to a commanded pressure over the 60 s
   already spent indexing, then fire it as a closed adiabatic expansion. No flow-rate problem
   exists at all, and velocity is commanded by charge pressure rather than by valve timing,
   which is the *"charge slowly, fire fast"* principle the whole architecture was built on. A
   first-order check says a 25 g start caps it near 25 m/s at equal chamber and swept volume, so
   the expansion ratio is the design variable and it is not free.

Option 3 is the one this failure points at, and it is not adopted here. It is a different run.

## What this run does not do

Unchanged from the declaration: no valve, seal, regulator or manifold is designed; no line losses,
wall heat transfer, seal friction, reservoir cooling across a sequence, or two-phase behaviour; and
A34's <= 1 N release residual is not checked. Every one of those omissions makes the numbers above
optimistic, and they still fail.
