# Gen6 — the current design target

**Part of the [generation archive](README.md).** Adopted 2026-08-14 by
[ADR-032](../adr/032-gen6-stage-integrated-gas-store.md).

| | |
|---|---|
| **Amended** | **2026-08-16 by [ADR-033](../adr/033-gen6-trim-stage.md)** — a 39.7 mm trim stator at the muzzle. **Gas for the energy, a motor for the control** |
| **Status** | **CURRENT DESIGN TARGET.** Not a baseline — **nothing in it is measured**, and Gen5 remains what every headline number is computed against |
| **Committed here** | **6 STEP** in `cad/step/gen6/`, **6 STL** in `cad/stl/` |
| **Source document** | **[`cad/build_gen6.py`](../../cad/build_gen6.py), in this repository** |
| **Rebuildable from this repository** | **Yes, byte-identically** |
| **Second implementation** | **None.** Gen5 has one; Gen6 does not, and the defect that found in Gen5 (**P71**) is the argument for building one |

## What it is, and how it differs in kind

**The payload is accelerated directly by cold gas along a rail a spent upper stage provides.**

**No mover. No stator. No supercapacitor bank. No power electronics. No eddy brake. No return
stroke.** 29.75 kg deleted outright, 43.33 kg reassigned to the stage, and charging is
**25–131 W**, which is solar.

| Part | Governing parameters |
|---|---|
| Drive tube | bore **15.805 mm**, stroke **2180 mm**, wall 1.0 mm |
| Carriage | rides the tube; carries the cradle interface. **Not recovered** |
| Chamber | **2.0 L at 50 bar**, nitrogen, fired as a closed adiabatic expansion |
| Reservoir | **9.55 L at 200 bar** — the no-relaxation figure, which A43 showed is the physically right end |
| **Trim stator** | **39.7 mm at x = 2140.3**, energised after the gas has finished. **0.340 kg.** Corrects ±0.323 m/s — it never throws the payload |
| Stage rail | the host-provided structure everything mounts to |
| Magazine cassette | carried across from Gen5's cell geometry |

## The operating point

| | | |
|---|---|---|
| Exit velocity | **30.535 m/s at 25 g** | **zero-friction.** At A41's full tolerable friction, **29.009 m/s** — **P67** |
| Stroke | 2.18 m | |
| Dispersion, 3σ | **1.113 % open-loop** | **0.0274 m/s closed**, with the trim stage — ADR-033. 93.4 % of the open-loop variance is seal friction |
| Added mass per satellite | **1.431 kg** with the trim stage | **1.403–3.271 kg** once the stage credit is read hostilely — **P68** |
| Store | 5.38 kg | chamber, vessel, gas and A39's 1.5 kg hardware allowance |

## The five runs that built it, none of which set out to

| | |
|---|---|
| **A35** | attributed every kilogram to its cause. **49.23 kg survives every requirement deletion in all 64 corners** |
| **A36** | closed the manifest route — 2.0 kg/satellite first reached at N = 116, which does not package |
| **A37** | made the stage the machine |
| **A38** | showed tip-off does not bind at 25 g |
| **A39** | replaced the spring with gas |

**And four more to get the store right:** **A40 killed the fixed-orifice implementation** at
14.16 m/s against a 30 m/s band; A41 specified the pre-charged chamber; A42 found its reservoir
sized on gas the bottle cannot give back; **A43 found the bottle does not warm back up** —
17 460 s against a 1200 s cadence.

## Known defects, and they are the largest the project carries

| | |
|---|---|
| **P67** | Precision rests on a **seal friction nobody has measured**, and no transducer buys it back |
| **P68** | **ADR-032's first falsifier has fired.** Break-even on the stage credit is **8.4 %, not the 30 % the ADR states**, and **58.6 % of that credit is the enclosure** — a skin belonging to a vehicle nobody has agreed to lend |
| **P59** | Kill criterion 1 is unreachable by architecture and by manifest size. Gen6 does not change that |

## What does not exist

**The pulse store for the trim stage** — 37.7 J at 28 kW, unsized and unweighed, and ADR-033's
first falsifier. **The cradle** — 201.7 N per contact of preload releasing inside a ≤ 1 N
residual, with no mechanism in any file, and it must now hold magnets in alignment too. **The piston, seals, valves and plumbing** — A41 allows 1.5 kg and designs
none of it. **And the stage**: no launch provider has agreed to keep one alive past passivation.

**Three of Gen5's crossed kill criteria are dissolved by Gen6 rather than passed.** A criterion
that no longer applies has not been met, and [`docs/KILL_CRITERIA.md`](../KILL_CRITERIA.md) says
so in those words.
