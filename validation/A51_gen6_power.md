# A51 — what Gen6 actually costs in power, and what efficiency means for a gas machine

**Bands declared 2026-08-16, before `analysis/gen6_power.py` existed.**
Verify with `git show --stat <this commit> -- analysis/gen6_power.py`, which must return nothing.

---

## Why this run exists

**Gen6 has no efficiency figure at all.** Gen5's **18.5 % electrical-to-payload** has no Gen6
equivalent anywhere in the repository, because the energy arrives as compressed gas rather than as
current, and nobody has said what the corresponding measure is.

**And the power figure Gen6 does carry describes a different machine.**
[ADR-032](../docs/adr/032-gen6-stage-integrated-gas-store.md) states charging at **25–131 W,
"which is solar"**. That number is [A37](A37_host_integrated.md)'s `charge_W_60s`, defined in
`analysis/host_integrated.py` as:

```
charge_W_60s = e / 60.0        # e is the SPRING option's shot energy
```

**It is the power needed to wind a spring over a sixty-second indexing window.** Gen6 has no
spring. Its reservoir is filled on the ground to 200 bar, and nothing in the architecture
recompresses gas on orbit. **The figure has been quoted as Gen6's ever since, including four times
on 2026-08-16 in ADR-033, `GENERATIONS.md`, `LINEAGE.md` and the front page.**

## What this run has to decide before it can compute anything

**"Efficiency" is not one quantity for a machine whose energy is lifted rather than generated.**
Four candidates, and the run reports all four rather than choosing one:

| | What it measures | Why it is honest, or is not |
|---|---|---|
| **On-orbit electrical per shot** | valves, sequencer, transducer | The only power the *host* is asked for. Comparable to nothing in Gen5 |
| **Delivered per kg of gas** | J/kg of nitrogen carried | The mass question, which is the one that decides the architecture |
| **Fraction of stored exergy delivered** | payload energy ÷ the work it took to compress the gas | The thermodynamically honest one, and the least flattering |
| **Payload ÷ chamber charge** | expansion efficiency alone | Already implicit in A41's ceiling fraction |

**Gen5's 18.5 % is not a comparator for any of them**, and saying so is part of the deliverable.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The run reproduces A41's shot work **1864.8 J** and A43's store **5.38 kg** exactly | It is not standing on the runs it extends |
| **2** | **On-orbit electrical energy per shot is computed from a named component list** — not assumed | The power claim is replaced by another unsourced number |
| **3** | On-orbit electrical **per shot** is **≤ 5 %** of the shot's mechanical work | The gas architecture is quietly electrical after all, and C3 is back |
| **4** | **All four efficiency measures are reported**, each with its denominator named | The run picks the flattering one |
| **5** | Fraction of stored exergy delivered is **≥ 2 %** | Ground compression is so lossy that the architecture is worse than it looks even as a mass argument |
| **6** | Delivered energy per kg of gas is **≥ 10 kJ/kg** | The gas is not carrying its own weight |
| **7** | The **25–131 W figure is traced to its source and its applicability stated** | The defect that prompted this run is left in place |
| **8** | Peak *electrical* power, as opposed to energy, is reported for the valve actuation | A peak-power claim is made without a peak-power number, which is how A48 band 5 went wrong |

## Predictions

1. **Band 3 passes by a wide margin.** A solenoid valve and a sequencer over a 133 ms shot are
   joules against 1864.8.
2. **Band 5 is the one at risk.** Isothermal compression of nitrogen to 200 bar costs roughly
   *nRT·ln(200)* — order **600 kJ** for the reservoir's gas mass — against twelve shots delivering
   about **22 kJ** of payload energy. **That is a few per cent, and it may fail the band.**
3. **Band 6 passes comfortably**, since a 2 L charge at 50 bar is 0.112 kg delivering 1864.8 J.
4. **Band 7 will find the number wrong rather than merely stale**, and the correction is that Gen6
   asks the host for **almost nothing**, which is a better claim than the one being made.

## Result

*Not yet run.*
