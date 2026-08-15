# A40 — the blowdown transient, and how velocity is commanded

**Bands declared 2026-08-14, before `analysis/blowdown.py` existed.**
Verify with `git show --stat <this commit> -- analysis/blowdown.py`, which must return nothing.

---

## Why this run exists

**P60**, and [A39](A39_store_trade.md)'s own closing paragraph: *"Gas removes a mass problem and
introduces a fluid-system problem, and this run has sized the first and not the second."*

A39 chose cold gas on a **quasi-static** argument — swept volume times working pressure equals the
energy needed. It never asked whether the gas can **arrive in time**. Filling a **0.428 litre**
swept volume in a **133 ms** stroke is roughly **3 L/s** at working pressure, and nothing has
modelled the orifice, the valve, or what the reservoir pressure does while it happens.

**Nothing about Gen6's geometry can be drawn until this closes.** The bore, the reservoir and the
valve are the first three dimensions in `cad/parameters.json`, and all three come out of here.

## And a second question A39 could not ask

**A falling reservoir means every shot is different.** A39 sized one 1.71 L bottle for twelve
shots by simple blowdown; if pressure droops, shot twelve is slower than shot one — **against a
project whose entire proposition is a velocity commanded per satellite.**

So this run also asks **how velocity is commanded at all with gas.** The candidate is **valve
cut-off**: open the valve, close it at a commanded time, let the payload coast the rest of the
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
against the payload's equation of motion. **Nitrogen, γ = 1.4, R = 296.8 J/kg·K, 300 K.**
Discharge coefficient **0.8**. Flow unchokes when the pressure ratio exceeds 0.528 and the
subsonic form is used below that. **Reservoir expansion is adiabatic**; cylinder filling is
treated as adiabatic with the piston doing work.

**Assumptions that make this optimistic, named here:** no line losses between reservoir and
orifice, no heat transfer to the walls, no seal friction, no valve opening transient other than
the declared ramp, and an ideal gas throughout. **Real cold-gas systems lose to all five.**

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

Every previous architecture commanded velocity with current. **If gas cannot be commanded,
Gen6 is a fixed-velocity spring with extra steps** — and A21 band 3's finding that a spring's
designed differential is zero would apply to it too.

### Band 5 is where the single-bottle result is most likely to fail

A39 sized the reservoir by simple blowdown arithmetic. **A transient will not be kinder.**

### Band 2 is where gas is physically worst

A spring's force falls as it extends; **gas at constant supply pressure does not**, so the risk is
at the start of the stroke where the cylinder volume is smallest and the pressure rises fastest.

## What this run does not do

It does not design a valve, a seal, a regulator or a manifold; does not model temperature drop in
the reservoir across twelve shots in sequence, wall heat transfer, or two-phase behaviour; and does
not check the ≤ 1 N release residual A34 requires. **It answers whether the gas arrives in time,
whether it lasts twelve shots, and whether velocity can be commanded.**

---

## Results

*(Filled after the run. Nothing above this line changes.)*
