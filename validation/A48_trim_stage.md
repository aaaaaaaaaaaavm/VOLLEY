# A48, a motor that steers rather than throws

**Bands declared 2026-08-16, before `analysis/trim_stage.py` existed.**
Verify with `git show --stat <this commit> -- analysis/trim_stage.py`, which must return nothing.

---

## Why this run exists

Asked in review: can Gen6 be gas *and* electromagnetic, each a fail-safe for the other?

The mutual-redundancy form does not survive arithmetic and is recorded as
[PII-20](../docs/VAULT.md) rather than run. For either drive to deploy alone, each must be
sized for the full duty; A35 prices the electromagnetic half at C2 + C3 = 11.54 + 26.35 kg,
which is exactly what ADR-032 deleted. And [A47](A47_gen6_fmea.md) has since shown the payoff
would be small anyway, an entire architecture change moved expected delivery by 0.37
satellites.

But the question contains a better idea than the one it asks. Gen6's largest live defect is
not energy, it is control: [P67](../OPEN_PROBLEMS.md), velocity is committed before the shot,
3σ dispersion is 1.113 %, and 93.4 % of that variance is a seal friction nobody has
measured. A fivefold better transducer moves it 0.008 %. There is no instrumentation route.

Gas is an excellent energy store and cannot servo. A linear motor is a mediocre energy store and
an excellent servo. This run asks what it costs to use each for what it is good at: gas
delivers the energy, a short motor section corrects the velocity it actually produced.

## The machine being priced

A stator section at the muzzle end of the 2.18 m stroke, acting on a magnet set carried by the
carriage, energised only after the gas has finished. It measures exit velocity and adds or removes
the difference from the setpoint. It never throws the payload, it only corrects it.

## Declared inputs

| | Value | Because |
|---|---|---|
| Correction authority | **±3σ of A44's spread**, swept to ±3× that | the loop must cover the error that exists, not an assumed one |
| Payload, exit velocity, shot energy | **A41 and A44, imported** | this run adds a stage, it does not re-derive the shot |
| Trim-stage K<sub>t</sub> | **10.54 N per kA/m**, A2's depth-resolved value | the same motor physics Gen5 used; no new claim |
| Residual after correction | the loop closes to **A28's Gen5 dispersion, 0.0274 m/s** | the target is the precision Gen6 gave up, not a softer one |

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | Imported Gen6 shot energy and dispersion reproduce **1864.8 J** and **1.113 %** exactly | The run is not standing on A41 and A44 |
| **2** | Energy to correct ±3σ is **≤ 5 %** of the shot | The trim stage is not a trim stage; it is a second drive, and PII-20's mass argument applies to it |
| **3** | Trim-stage length is **≤ 15 %** of the 2.18 m stroke | It is not a section at the muzzle, it is the machine |
| **4** | Added mass is **≤ 2.0 kg**, so added mass per satellite stays **≤ 2.0 kg/satellite** | The fix re-crosses the one kill-criterion numerator Gen6 currently passes |
| **5** | Peak electrical power stays **≤ 200 W**, A37's band | The pulse comes back and C3's 26.35 kg with it |
| **6** | Correcting to **0.0274 m/s** — Gen5's dispersion — is achievable inside bands 2–5 | Gen6 cannot be given back the precision it traded, and P67 stands as an architectural cost rather than a fixable one |
| **7** | The result holds when the friction spread is **3× A44's assumption** | The answer depends on a number nobody has measured, which is the defect it exists to fix |
| **8** | Every defect the stage re-opens is **named**, not counted | Magnets return to the moving part; **P34, E35 and the cradle** come back, and a run that reports only the win is not a trade study |

## Predictions

1. **Band 2 passes with room** — correcting a 0.3 m/s error on 4 kg at 29 m/s is order **40 J**
   against 1864.8, roughly 2 %.
2. **Band 5 is the one at risk.** A correction applied over a short section is applied *fast*, and
   power is energy over time. I expect this to be tight or to fail.
3. **Band 6 passes**, because the correction is measured and closed-loop rather than commanded
   open-loop, which is the whole point.
4. **Band 4 passes but not comfortably**, because the magnets and their carriage structure are
   real mass and A35 priced a full mover at 11.54 kg.

## Result

**RUN 2026-08-16. Seven of eight bands pass. Band 5 fails by 139×, and the band was wrong.**

| # | Band | Result | |
|---|---|---|---|
| 1 | imported shot and dispersion reproduce | 1864.8 J, 1.113 % | **PASS** |
| 2 | energy to correct ±3σ ≤ 5 % of the shot | **2.021 %** | **PASS** |
| 3 | trim section ≤ 15 % of the stroke | **1.822 %** | **PASS** |
| 4 | added mass ≤ 2.0 kg, per satellite ≤ 2.0 | **0.340 kg → 1.431 kg/sat** | **PASS** |
| 5 | peak electrical ≤ 200 W | **27 820 W** | **FAIL** |
| 6 | correcting to Gen5's 0.0274 m/s reachable | reachable | **PASS** |
| 7 | holds at 3× the friction spread | 5.53 % stroke, 1.032 kg | **PASS** |
| 8 | every re-opened defect named | 5 named | **PASS** |

### The idea works on every axis except the one I mis-declared

Correcting the full ±3σ costs 37.7 J, 2.021 % of the shot, over 39.7 mm, 1.822 % of the
stroke, for 0.340 kg. Added mass per satellite goes 1.403 to 1.431 kg, still inside the
threshold. At 3x the friction spread it is 5.53 % of the stroke and 1.032 kg, so the answer
does not depend on the number nobody has measured.

**Band 6 is the point of the run: Gen6 can be given back the precision it traded**, because a loop
correcting a *measured* velocity does not care that the gas produced it open-loop.

### Band 5, and the error is mine

A37's 200 W is a *charging* budget, the power drawn from the host over the sixty-second
indexing window. I declared it against an *instantaneous mechanical* power. Those are
different quantities and the comparison was never meaningful.

**The physics is unarguable and does not depend on the band.** At 29 m/s, power is force times
velocity. Correcting 0.323 m/s takes 37.7 J; deliver it over 39.7 mm and it lasts 1.4 ms, so
it is **28 kW while it happens.** Stretching the section to the full 15 % band 3 allows still
leaves 3.3 kW. Reaching 200 W at 29 m/s needs a 6.9 N force and therefore a 5.5 m
section, longer than the stroke. *200 W was unreachable by construction, and I should have
seen that before declaring it.*

**Recorded as a declaration error, and the band stands as failed.** The precedent is A40 band 1,
where the same thing happened and was recorded the same way.

### What band 5 was groping at, and it is real

The trim stage is pulse power. 37.7 J at 28 kW is exactly the shape of requirement C3,
*the energy arrives during the shot*, which A35 prices at 26.35 kg and which ADR-032 deleted.

But at 1/50th of the energy. Gen5's shot is 2782 J; this is 37.7. Whether that store is
grams or kilograms is not answered here, because pulse hardware scales with *current*, not
with energy, and no run has sized it. That is the question that decides the idea, and it needs
its own bands.

### What it re-opens, named rather than counted

- P34, a payload carrying a magnetometer cannot fly in this magazine. Magnets return to
  the moving part, so this defect returns with them.
- E35, the payload's field exposure becomes a design variable again.
- The cradle, the carriage must hold magnets in alignment as well as the payload, and it
  already does not exist.
- A velocity sensor before the trim section, which Gen6 has no equivalent of.
- One more shared element in the FMEA, and [A47](A47_gen6_fmea.md) has just shown that
  shared elements are what cost delivered satellites.

### The predictions

**All four held, and the second was the useful one.** It said band 5 was the one at risk, *"since
a correction applied over a short section is applied fast, and power is energy over time."* That
is exactly why it failed — the prediction was right about the mechanism and I declared the band
anyway.

## What this run does not do

- No pulse-store sizing, which is the open question above.
- Constant K<sub>t</sub> over the section, no end effects, no commutation loss, and an ideal
  velocity measurement. Every one flatters the trim stage.
- The correction is a constant force, not a designed control law. A28 exists for Gen5 and
  there is no equivalent here.
- Nothing is measured, including the friction the stage exists to correct.
