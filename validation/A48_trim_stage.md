# A48 — a motor that steers rather than throws

**Bands declared 2026-08-16, before `analysis/trim_stage.py` existed.**
Verify with `git show --stat <this commit> -- analysis/trim_stage.py`, which must return nothing.

---

## Why this run exists

**Asked in review: can Gen6 be gas *and* electromagnetic, each a fail-safe for the other?**

**The mutual-redundancy form does not survive arithmetic and is recorded as
[PII-20](../docs/VAULT.md) rather than run.** For either drive to deploy alone, each must be
sized for the full duty; A35 prices the electromagnetic half at **C2 + C3 = 11.54 + 26.35 kg**,
which is exactly what ADR-032 deleted. And [A47](A47_gen6_fmea.md) has since shown the payoff
would be small anyway — an entire architecture change moved expected delivery by **0.37
satellites**.

**But the question contains a better idea than the one it asks.** Gen6's largest live defect is
not energy, it is control: **[P67](../OPEN_PROBLEMS.md)** — velocity is committed before the shot,
3σ dispersion is **1.113 %**, and **93.4 % of that variance is a seal friction nobody has
measured.** A fivefold better transducer moves it **0.008 %**. There is no instrumentation route.

**Gas is an excellent energy store and cannot servo. A linear motor is a mediocre energy store and
an excellent servo.** This run asks what it costs to use each for what it is good at: **gas
delivers the energy, a short motor section corrects the velocity it actually produced.**

## The machine being priced

A stator section at the muzzle end of the 2.18 m stroke, acting on a magnet set carried by the
carriage, energised only after the gas has finished. It measures exit velocity and adds or removes
the difference from the setpoint. **It never throws the payload — it only corrects it.**

## Declared inputs

| | Value | Because |
|---|---|---|
| Correction authority | **±3σ of A44's spread**, swept to ±3× that | the loop must cover the error that exists, not an assumed one |
| Payload, exit velocity, shot energy | **A41 and A44, imported** | this run adds a stage, it does not re-derive the shot |
| Trim-stage K<sub>t</sub> | **10.54 N per kA/m**, A2's depth-resolved value | the same motor physics Gen5 used; no new claim |
| Residual after correction | the loop closes to **A28's Gen5 dispersion, 0.0274 m/s** | the target is the precision Gen6 gave up, not a softer one |

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

*Not yet run.*
