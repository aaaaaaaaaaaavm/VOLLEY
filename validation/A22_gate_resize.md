# A22: resize the retention gates against the case that actually governs them

**Closes:** **P37**, and the analysis half of **E10**. Both are currently *predicted failures*.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/gate_sizing.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written,
> and the script is absent at this commit.

## The defect being fixed

`sizing.py::retention_gate()` sizes the gate against a **quasi-static 25 g ascent load**:

    F = 24 kg x 25 g = 5.89 kN, two D6 A-286 pins, capacity 18.2 kN, MoS 1.2

**A18 band 9 showed that is the wrong load case.** Miles' equation on the GEVS protoflight
spectrum (0.16 g²/Hz) through the track's 109 Hz fixed-fixed mode gives a 3σ load of:

| Q | 3σ load | vs the 5.89 kN sized for | MoS at 18.2 kN capacity |
|---:|---:|---:|---:|
| 10 | 11.7 kN | 1.98× | 0.56 |
| 20 | 16.5 kN | 2.80× | **0.10** |
| 30 | 20.2 kN | 3.43× | **−0.10** |

**The pins are not necessarily undersized. The load case was.** 5.89 kN is quasi-static;
random vibration through a lightly damped mode is a different problem, and the claimed MoS 1.2
collapses to 0.10 at Q = 20 and goes negative at Q = 30.

**Q is unmeasured** — `docs/STRUCTURAL_GAP.md` records four separate findings turning on it — so
**this analysis sizes against Q = 30**, the conservative end of the range A18 swept. Sizing
against a Q the project has never measured, at the *optimistic* end, would be the same error in a
new place.

## The design space, and the three levers

| Lever | Effect | Cost |
|---|---|---|
| **Pin diameter** | capacity ∝ d² | larger bosses, gate frame, mass |
| **Pin count** | capacity ∝ n | more holes in the same frame |
| **Driven mass per gate** | load ∝ m — intermediate restraint splits the stack | a septum-level tie, and the septa already exist (1 mm silicon steel, `groups.magazine`) |

**Mode tuning is deliberately not a lever.** Miles gives load ∝ √(f<sub>n</sub>·Q), so *raising*
the mode raises the load, and lowering it runs into the > 70 Hz launch requirement
`sizing.py::track_first_mode` already enforces. The √ dependence makes it weak in both directions.

**Mass is a constraint, not a free variable.** Kill criterion 1 is crossed by a factor of three,
so a fix that solves a structural problem by adding kilograms trades a live threat for a
predicted one. Band 3 bounds it.

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **The script reproduces A18 band 9's loads** at Q = 10, 20, 30 | **11.7 / 16.5 / 20.2 kN, within 2 %** | a fork between this script and `phase1_closeout.py::e10`, which is the P19 failure mode. Suspect this script |
| 2 | **A design exists in the allowed space with MoS ≥ 0.2 at Q = 30**, against a design factor of 1.4 on the 3σ load | **yes** | if nothing in the space passes, the gate concept is wrong and the cassette needs a different restraint architecture, not bigger pins. That is a **HIGH** finding, not a resize |
| 3 | **Mass added by the chosen fix**, per cassette | **≤ 0.40 kg** | above this the fix is being bought from kill criterion 1, which is already crossed. A heavier fix must be reported as a trade rather than adopted |
| 4 | **The chosen design still passes the original quasi-static case** at 25 g with the existing 1.4 factor | **MoS ≥ 1.2**, i.e. no worse than today | a fix that solves the random case and regresses the static one is not a fix |
| 5 | **Sensitivity of the chosen design to Q** | **MoS ≥ 0 across Q = 10 to 30** | the design must not depend on Q landing low. Q is unmeasured; a design that passes only at Q = 10 has assumed the measurement |
| 6 | **Pin shear is the governing failure mode**, against bearing on the boss and tension in the frame | **report** | if bearing governs instead, resizing pins for shear fixes the wrong thing |

### Band 2 is the one that decides whether this is a resize or a redesign

The allowed space is bounded deliberately: **pin diameter ≤ 10 mm, pin count ≤ 4, and up to one
intermediate restraint per cassette.** Beyond that the gate stops being a gate.

**If nothing in that space reaches MoS 0.2 at Q = 30, the answer is not a bigger pin.** It is that
a single one-shot gate carrying a six-satellite stack through random vibration is the wrong
architecture, and that would be a new HIGH defect rather than a closure.

### Band 5 exists because of what A19 found

A19 ranked structural Q as the only assumed input that moves a margin of safety **through zero**,
while returning exactly zero on every headline number. **The whole point of this resize is to stop
that being true.** A design that passes at Q = 10 and fails at Q = 30 has not removed the
dependency, it has renamed it.

## What happens at each outcome, fixed now

1. **Band 1 fails.** Stop. The load model disagrees with the published A18 result.
2. **Band 2 fails.** A new HIGH defect: the retention architecture, not the pins. `KILL_CRITERIA.md`
   and `STRUCTURAL_GAP.md` both need it, and the Gen5 magazine design in WS3/WS4 has to carry it.
3. **Band 3 fails.** Report the mass cost against kill criterion 1 explicitly and let the trade be
   visible; do not adopt silently.
4. **Band 4 fails.** Reject that candidate and pick another from the space.
5. **Band 6 shows bearing governing.** Size against bearing and re-run; the pin-shear resize would
   have been the wrong fix.

**No band may be widened after the run.** A miss produces a numbered defect, not a revised target.

## Provenance

Loads from `analysis/phase1_closeout.py::e10` by import — the same function A18 ran — rather than
reimplemented. Geometry and materials from `cad/parameters.json` `groups.magazine`. A-286 shear
allowable is taken as 0.6 × tensile, the same class assumption `sizing.py` already uses, and it is
an assumption rather than a datasheet value.

**Nothing here is measured**, and the GEVS spectrum is a specification envelope rather than a
measured environment for any specific vehicle. **T-1 remains the test that settles this**, and
`docs/QUALIFICATION_PLAN.md` already calls it the single most likely qualification failure.
