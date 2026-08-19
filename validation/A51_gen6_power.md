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

**RUN 2026-08-16. Seven of eight bands pass. Band 3 fails, my prediction about it was wrong, and
the band was measuring the wrong ratio.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A41 and A43 | 1864.8 J, 5.38 kg | **PASS** |
| 2 | electrical from a named component list | 5 components | **PASS** |
| 3 | on-orbit electrical ≤ 5 % of shot work | **16.718 %** | **FAIL** |
| 4 | all four measures reported | 4 | **PASS** |
| 5 | ≥ 2 % of stored exergy delivered | **3.36 %** | **PASS** |
| 6 | ≥ 10 kJ/kg of gas | 16.60 kJ/kg | **PASS** |
| 7 | the 25–131 W figure traced | traced | **PASS** |
| 8 | peak electrical reported | 36.0 W | **PASS** |

### Band 7 first, because it is the reason this run exists

**ADR-032 states Gen6's charging as "25 to 131 W, which is solar". The figure is not Gen6's.**

It is `analysis/host_integrated.py`'s `charge_W_60s = e / 60.0`, where *e* is **the spring
option's** shot energy — the power to wind a spring over a sixty-second indexing window. **Gen6 has
no spring, and its reservoir is filled on the ground to 200 bar.** Nothing in the architecture
recompresses gas on orbit.

**What Gen6 actually asks the host for:**

| | |
|---|---:|
| Electrical energy per shot | **311.76 J** |
| **Average power over a 1200 s cadence** | **≈ 0.26 W** |
| Peak instantaneous | **36.0 W** |

**The real number is about a hundredth of the one being claimed**, and the claim was wrong in the
*conservative* direction — which is unusual enough to be worth saying. **Recorded as P80.**

### Band 3 failed, and the band compared the wrong two things

**16.718 % against a 5 % band.** But the composition says what is really going on:

| | |
|---:|---|
| 1.20 J | fire valve, 24 W for 50 ms |
| **99.36 J** | fill valve, 24 W across A42's **4.14 s** fill |
| 30.00 J | pressure transducer, held through the indexing window |
| **180.00 J** | shot sequencer, held through the indexing window |
| 1.20 J | cradle release |

**The shot itself costs 2.4 J — 0.13 % of its own mechanical work.** Everything else is
**housekeeping across a sixty-second window**, and dividing sixty seconds of housekeeping by a
133 ms shot's energy will always look bad without meaning much.

**My prediction said band 3 would pass by a wide margin, and my error was the same as the band's**
— I was thinking of the shot and the band was measuring the cycle. **The band stands as failed**,
and the useful figure is the average power above.

### The four measures, each with its denominator named

| Measure | Value | Denominator |
|---|---:|---|
| On-orbit electrical / shot work | 16.718 % | what the **host** is asked for |
| Delivered per kg of gas | **16.60 kJ/kg** | the mass question |
| Campaign / compression exergy | **3.36 %** | thermodynamically honest, ground energy included |
| Shot work / chamber *pV* | 18.65 % | the expansion alone |

**Gen5's 18.5 % electrical-to-payload is not a comparator for any of them**, and the near-coincidence
with the last row is exactly that — a coincidence of two different quantities.

**Band 5 passed at 3.36 %, and it is the least flattering figure here.** Compressing the
reservoir's 1.41 kg of nitrogen to 200 bar costs roughly **666 kJ** on the ground against
**22.4 kJ** delivered to twelve payloads. **Isothermal compression is an idealisation that
flatters it** — a real multi-stage compressor is worse.

## What this run does not do

- **No datasheet backs any component draw.** All five are declared representative figures, which
  is **E3** — no vendor quotation exists anywhere in this project.
- **No thermal path for the compressor**, and no ground-support power budget.
- **It does not price keeping the sequencer alive between shots across a months-long campaign**,
  which [A50](A50_campaign_altitude.md) has just made a live question.
