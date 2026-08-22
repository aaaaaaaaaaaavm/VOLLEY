# Gen5 — the frozen baseline

**Part of the [generation archive](README.md).** Adopted by
[ADR-026](../adr/026-cad-built-from-parameters.md).

| | |
|---|---|
| **Status** | **FROZEN BASELINE.** Superseded as the *design target* by Gen6 on 2026-08-14 ([ADR-032](../adr/032-gen6-stage-integrated-gas-store.md)); **not superseded as the frozen computational baseline** |
| **Committed here** | **8 STEP** in `cad/step/gen5/`, **8 STL** in `cad/stl/` |
| **Source document** | **[`cad/build_gen5.py`](../../cad/build_gen5.py), in this repository** |
| **Rebuildable from this repository** | **Yes, byte-identically**, from a clean clone |
| **Second implementation** | **[`cad/scad/gen5.scad`](../../cad/scad/gen5.scad)** — the same eight documents in a CSG kernel, checked against the B-rep part by part |

## What it is

**The first generation a script can rebuild.** Eight documents built from
[`cad/parameters.json`](../../cad/parameters.json): ESPA interface, track, stator, sled, magazine
cassette, brake, 3U payload proxy, enclosure.

It incorporates Gen4's recorded stations — release s = 1200 mm, brake entry s = 1222 mm, the
488 mm sled — **so it depends on no unexported document.**

## The operating point

| | | Source |
|---|---|---|
| Exit velocity, 3U | **16.029 m/s at 10.07 g** | `analysis/motor_model.py` |
| Thrust constant | 10.54 N per kA/m, ±1.01 % ripple | A1, A2 |
| Closed-loop dispersion | **0.0274 m/s (3σ)** at a 15.8 m/s setpoint | A28 |
| Dry / loaded mass | **126.6 kg / 174.6 kg** | `analysis/mass_properties.py` |
| Per 3U satellite | **10.547 kg dry** | `analysis/payload_family.py` |

## Known defects

| | |
|---|---|
| **P71** | **Both sled rollers were outside their channels in every Gen5 STEP ever built** — one inboard in the stator gap, one outboard of the longeron, the sled asymmetric about y = 0. Corrected 2026-08-16. **Found by the second implementation, not by any guard here**, because every guard compares a built artifact against the script that built it |
| **P46** | K<sub>t</sub> is a centre-plane value and overstates thrust by 4.42 %. Computed and held, not applied |
| **P26** | No purchasable supercapacitor bank sources the shot. **Moot for Gen6**, live for Gen5 |
| **P9 / envelope** | 1839 mm against roughly 1270 mm of ESPA Grande, over by 44 % |

## What it is not

**A geometry and interface model, not a manufacturing model.** No fillets, fasteners, harness
routing or tolerancing exist in it, and `parameters.json` carries no tolerances to give them.
**That is why Gen4's renders look more finished** — someone drew detail into Fusion that no
parameter describes.

## Why it was superseded as the target

**Three kill criteria crossed**, and [ADR-032](../adr/032-gen6-stage-integrated-gas-store.md)
deletes the subsystems two of them were about rather than meeting them. **Gen5 remains the
frozen computational baseline and the record of what a self-contained deployer costs**: [GEN6.md](GEN6.md).

## What this generation assumed about the host

**Mission role of the host: an ACTIVE POST-PRIMARY ORBITAL DELIVERY PLATFORM.**
**Mechanical integration: LOW — a self-contained deployment machine carried aboard it.**

**Those are two answers and Gen5 needs both**, because a single sentence about "the host" has been
read as a passive-host assumption and that is not what Gen5 is.

**Gen5's concept of operations, in the order it happens:**

1. the launch vehicle completes its primary ascent;
2. **the primary spacecraft separates** — the primary customer is served first;
3. the post-primary phase begins, and **the stage remains controlled where host capability allows
   it**;
4. the stage may coast or reposition between deployment events — **parametrically, because
   [E5](../../OPEN_PROBLEMS.md) means no host propulsion figure exists**;
5. **Gen5 produces each satellite's commanded local separation state** using its own track,
   linear synchronous drive, sled, supercapacitor bank, eddy brake and magazine;
6. the host provides the orbital platform and the coarse mission-level positioning;
7. the stage proceeds to disposal, passivation and re-entry.

> **So Gen5 is not an electromagnetic dispenser bolted to a passive ring.** It is **a
> self-contained electromagnetic last-mile deployment mechanism operating aboard a post-primary
> upper-stage delivery platform** — the same mission Gen6 flies, implemented with far more of the
> machinery carried by VOLLEY itself.
>
> **That duplication is the weakness Gen6 attacks**, and it is a weakness of the *integration*,
> not of the concept of operations.

**And it is where the cost of the assumption became measurable.** [A46](../../validation/A46_enclosure_buildup.md) built the enclosure from its own geometry and found **50.04 kg against an 8.00 kg placeholder** — a skin, a radiator and an avionics bay that a spent stage already carries. *The largest single mass in the machine was a duplicate of something the host already had.*

*The through-line across all six is [`../LINEAGE.md`](../LINEAGE.md).*
