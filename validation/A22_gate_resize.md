# A22: resize the retention gates against the case that actually governs them

**Closes:** **P37**, and the analysis half of **E10**. Both are currently *predicted failures*.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/gate_sizing.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written,
> and the script is absent at this commit.

## Result, 2026-08-10: six of six, and the fix is 11 grams

`analysis/gate_sizing.py`, bands committed at `bc113e6` before it existed. Results in
`analysis/results/gate_sizing.json`.

### Band 1: the load model reproduces A18 exactly

| Q | This script | A18 band 9 | Error |
|---:|---:|---:|---:|
| 10 | 11.69 kN | 11.69 kN | **0.000 %** |
| 20 | 16.53 kN | 16.53 kN | **0.000 %** |
| 30 | 20.24 kN | 20.24 kN | **0.000 %** |

Because `phase1_closeout.e10`'s own relation is imported rather than reimplemented. **PASS.**

### The chosen fix: two D9 pins instead of two D6

| | Baseline | **Chosen** |
|---|---|---|
| Gates per cassette | 1 | 1 — unchanged |
| Pins | 2 × D6 | **2 × D9** |
| Capacity | 18.2 kN | **41.0 kN** |
| MoS at Q = 30 | **−0.36** | **+0.45** |
| MoS at Q = 10 | +0.31 | +1.51 |
| Quasi-static, 25 g | +1.21 | **+3.98** |
| Added mass | — | **+11 g per cassette** |
| Governing mode | — | pin shear, not bearing |

**The entire fix is three millimetres of pin diameter and eleven grams.** Capacity goes as d², so
6 → 9 mm is 2.25× the shear area, and it converts a negative margin at Q = 30 into +0.45.

**No intermediate restraint is needed.** The second lever — splitting the stack across two gates —
was in the allowed space and is not required, which is the better answer: it leaves the magazine
architecture alone.

**26 of 30 candidates in the space pass.** The four that fail are all at two pins:

| Candidate | Capacity | MoS at Q = 30 |
|---|---:|---:|
| 2 × D6 — **as designed today** | 18.2 kN | **−0.357** |
| 2 × D7 | 24.8 kN | **−0.125** |
| 2 × D8 | 32.4 kN | +0.143 — below the 0.20 target |
| **2 × D9** | **41.0 kN** | **+0.447** |

**D8 misses the target by 0.06 and is worth naming**, because it is the more standard size and a
reader will ask. If a 0.15 margin at Q = 30 were acceptable it would do; the band said 0.20 and
the band was declared first. **3 × D8 also passes at +0.71** and is the alternative if D9 stock is
awkward — the selection rule picked minimum change, not minimum risk.

### Band 3, 4, 5, 6

- **Band 3 PASS.** +11 g against a 400 g budget. The fix costs kill criterion 1 essentially
  nothing, which is the outcome the budget was set to force.
- **Band 4 PASS.** Quasi-static MoS goes 1.21 → 3.98. Nothing regresses.
- **Band 5 PASS.** MoS stays positive across the whole sweep, **+0.45 at Q = 30 to +1.51 at
  Q = 10**. **The design no longer depends on where Q lands**, which is the point of the exercise
  — A19 found Q was the only assumed input moving a margin through zero, and it no longer does.
- **Band 6 REPORT: pin shear governs**, 41.0 kN against a bearing capacity of 52.2 kN on a 4 mm
  frame. Resizing pins for shear was the right fix rather than the wrong one.

> ### A definitional discrepancy, found while doing this and worth recording
>
> **A18 and `sizing.py` report margins of safety against different things.** A18 band 9 quotes
> MoS at Q = 30 as **−0.10**, computed as capacity/load − 1. `sizing.py::retention_gate` applies a
> **1.4 design factor** and reports capacity/(1.4·load) − 1, which gives **−0.36** for the same
> hardware and the same load.
>
> **Both are correct and they are not the same quantity.** This sheet uses the factored form,
> because it is how the gate was originally sized and because dropping a design factor while
> resizing would be a silent relaxation. The unfactored figure is the more optimistic one, and
> **P37's −0.10 is therefore the kinder of the two readings of the same failure.**

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
