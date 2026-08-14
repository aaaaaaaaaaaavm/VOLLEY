# A37 — the stage as the deployer, and the falsification test A35 is owed

**Bands declared 2026-08-14, before `analysis/host_integrated.py` existed.**
Verify with `git show --stat <this commit> -- analysis/host_integrated.py`, which must return
nothing.

---

## Why this run exists

Two runs have closed two of the three routes to kill criterion 1.
[A35](A35_constraint_ledger.md): 49.23 kg survives every requirement deletion in all 64 corners.
[A36](A36_magazine_density.md) band 4: the divisor reaches 2 kg only at N ≈ 116, which does not
package. **P59** records that only a payload-class change remains.

**A third possibility was never analysed: that the deployer is not carried by a stage but *is* one.**
[ADR-023](../docs/adr/023-target-host-class.md) already re-scoped the host to a restartable upper
stage and dropped envelope compliance; [ADR-024](../docs/adr/024-last-mile-delivery-conops.md)
wrote the last-mile concept. Neither took the last step: **after the primary separates, the spent
stage stops being the mounting surface and becomes the machine** — its structure the track, its
array the supply, its residual propellant the repositioning budget.

This run also **settles the falsification test declared in A35** and left open. That test was:
*deleting "the energy arrives during the shot" removes more than 40 % of dry mass; the falsifier is
that its replacement weighs more than 60 % of what came out.* A35 measured the removal at
**23.76 kg**. Band 4 below measures the replacement.

## The honesty problem this run must not fall into

The tempting move is that a stage is sunk cost, so the criterion should count only added hardware —
which takes 7.042 kg/satellite to something near 1.2 and closes a criterion two runs have failed.

**That is structurally identical to the metric substitution this project has already flagged and
declined**, where *Δv per kilogram per satellite* flatters the design by 5.4× and was recorded in
`CHANGELOG.md` as exactly the sort of number a project reaches for once the plain one stops being
kind.

**So three rules bind this run, and bands 1–3 enforce them mechanically:**

1. **The threshold does not move.** ~2 kg stands, from what canisterised dispensers achieve.
2. **Both numerators are always reported together.** Added mass per satellite may never appear
   without dry mass per satellite beside it.
3. **Nothing is credited to the stage without naming the subsystem that provides it.** A stage kept
   alive, powered, pointed and manoeuvring through a campaign [A36](A36_magazine_density.md) puts
   at up to 42 hours is not a passivated stage, and the difference is hardware that exists whether
   or not this rollup counts it.

## Stage classes, by dimension only

No vendor, programme or organisation is named. Classes are defined by usable acceleration length,
and **the usable fraction is an assumption with no derivation** — tankage, engine and avionics bays
are not available to a track.

| Class | Usable acceleration length |
|---|---|
| Small kick stage | **1.5 m** |
| Medium restartable upper stage | **3.0 m** |
| Large upper stage | **8.0 m** |

## Stores traded

**Steel spring** at 300 J/kg usable, the figure `analysis/actuator_trade.py` already declares as
the upper end for spring steel, and **the existing linear synchronous motor as the control.**

**Gas is deliberately excluded and recorded as an entry criterion for a later run.** Sizing a
pressure vessel needs a mass-fraction figure this project does not hold, and a store invented to
win a trade is worse than a store left out of it.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Added + stage-provided reproduces the A35 ledger total to **0.01 kg**, with **no item unassigned** | Mass is invented or lost in the reassignment |
| **2** | **Every** stage-provided item names the stage subsystem that provides it | The stage is being treated as free |
| **3** | The run reports **added mass per satellite and dry mass per satellite together**, and the 2.0 kg threshold is applied unchanged to both | The criterion has been quietly re-specified rather than re-argued |
| **4** | **The A35 falsifier.** Energy store + wind mechanism + latch + safing ≤ **14.26 kg** at the selected point | **The mass relocated rather than left**, the pulse was a symptom, and A35's C3 result does not mean what it appeared to |
| **5** | Added mass per satellite ≤ **2.0 kg** at N = 12 on **at least one** stage class | Host integration does not close kill criterion 1 either, and no route remains but payload class |
| **6** | The selected point delivers **≥ 30 m/s** at **≤ 25 g** | Stage length does not convert into the velocity that A21-R showed is the only differentiated claim |
| **7** | Peak electrical ≤ **200 W** | The pulse has not actually been deleted at metre-scale strokes |
| **8** | The energy store is ≤ **50 %** of total added mass | This is a spring-design problem wearing a deployer's clothes, and the trade should be run as one |

### Band 4 is the one that decides whether A35 meant anything

It is the only band here that can invalidate an earlier result. The store scales as **v²** —
514 J is 1.7 kg of spring steel, 2943 J at 3 m of stroke is **9.8 kg** — so the falsifier tightens
exactly as the velocity goal is pursued. **A comfortable pass at 16 m/s and a failure at 38 m/s is
a real possibility and would be the most useful outcome this run can produce.**

### Band 5 is the headline and band 8 is the warning

If added mass per satellite closes and the store is most of it, the honest description is not
*a deployer that closes kill criterion 1* but *a spring that needed a stage to hold it*, and the
next run is a store trade rather than a deployer design.

## What this run does not do

It does not design a stage interface, model the attitude control a live stage needs through a
42-hour campaign, price the debris-mitigation case for keeping a stage manoeuvring, or address
**availability** — a different stage every launch multiplies the interface problem rather than
solving it. **Tip-off is untouched**: [A23](A23_tipoff_release.md)'s 36–231 °/s cradle arrival
survives every architecture on this page and gets worse with acceleration.

---

## Results

**RUN 2026-08-14. Six of eight bands pass. Bands 4 and 8 fail, and the failure is the result.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reassignment reproduces the ledger to 0.01 kg | 84.5316 against 84.5316 | **PASS** |
| 2 | every stage-provided item names its subsystem | 0 unjustified | **PASS** |
| 3 | both numerators reported, threshold unchanged | dry **7.044**, added **4.442 kg** | **PASS** |
| 4 | A35 falsifier: store + mechanism ≤ 14.26 kg | **41.86 kg** at the selected point | **FAIL** |
| 5 | added mass/satellite ≤ 2.0 kg on some class | **1.608 kg** | **PASS** |
| 6 | ≥ 30 m/s at ≤ 25 g | 62.6 m/s at 25 g | **PASS** |
| 7 | peak electrical ≤ 200 W | 131 W | **PASS** |
| 8 | store ≤ 50 % of added mass | **78.5 %** | **FAIL** |

### Where the 84.53 kg goes

| | |
|---|---:|
| **Deleted by Gen6 physics** — no mover, no pulse | **29.75 kg** |
| **Provided by a live stage**, each item naming its subsystem | **43.33 kg** |
| **Added — what the machine still costs** | **11.45 kg** |

The entire added base is **cassette shells (8.85 kg) and followers, gates and escapements
(2.60 kg)**. Nothing else survives as a cost. **A36's containment floor and this run's added base
are the same 11.45 kg**, arrived at from opposite directions.

### Band 5 passes, and it is the largest result this project has produced

| Stage class | L | v | store + mech | **added kg/satellite** | charge |
|---|---:|---:|---:|---:|---:|
| **small kick stage** | 1.5 m | 27.1 m/s | 7.85 kg | **1.608 kg** | 25 W |
| medium restartable upper stage | 3.0 m | 38.4 m/s | 15.70 kg | 2.262 kg | 49 W |
| large upper stage | 8.0 m | 62.6 m/s | 41.86 kg | 4.442 kg | 131 W |

**On the small class, added mass per satellite is 1.608 kg against an unchanged 2.0 kg threshold.
Kill criterion 1 closes at 3U, without changing payload class** — the route P59 recorded as the
only one left is no longer the only one.

**Both numerators, as band 3 requires:** dry mass per satellite remains **7.044 kg and crosses**.
Nothing about that has changed and it is not being withdrawn. What has changed is that a second,
differently-argued numerator exists, and **both are reported wherever either is.**

### Bands 4 and 8 fail because the store scales as v², and that is now the binding constraint

The run sheet predicted this shape: *"A comfortable pass at 16 m/s and a failure at 38 m/s is a real
possibility and would be the most useful outcome this run can produce."*

**Stage length is free. The spring that exploits it is not.** Store mass goes as v², so the 8 m
class needs **26.16 kg of spring steel** and the store becomes 78.5 % of everything added.

**And the selection rule was badly designed.** No declared class satisfied every band, so the
script fell back to maximum velocity — the worst case for bands 4 and 8. At the *small* class the
falsifier passes comfortably at 7.85 kg. **The bands are evaluated as declared and the failure
stands**, but its proximate cause is a fallback rule, not the physics, and that is recorded rather
than glossed.

### The window the three declared classes bracket without containing

*Derived after the run from its own outputs. Not a band, and not to be read as one.*

Every declared band is satisfied for **L between 1.83 m and 2.18 m — 30.0 to 32.7 m/s** — at
about **1.83 kg/satellite**, a **10.5 kg** store and **33 W**. The three classes declared were
1.5 m, 3.0 m and 8.0 m. **None lies inside the window.** 1.5 m misses only on velocity; 3.0 m
misses on mass, falsifier and store fraction.

**No stage class was added after the run**, and none will be. The window is reported so the next
run can declare its classes against it rather than around it.

### What this means

1. **The stage does not solve the mass problem — it deletes it.** 43.33 kg becomes someone else's
   structure and 29.75 kg stops existing. What remains is containment, which no architecture can
   remove.
2. **The binding constraint has moved from mass to energy storage.** Every previous run was about
   where the kilograms live. This one says the next question is a store trade, at metre-scale
   strokes, and **band 8's failure is the warning the run sheet declared in advance**: this is
   becoming a spring-design problem wearing a deployer's clothes.
3. **Velocity and kill criterion 1 are now in direct tension**, priced for the first time. 27 m/s
   closes the criterion; 38 m/s does not. Where to sit on that curve is a product decision.

### What is still not priced, and every omission flatters this run

Stage **availability** — a different stage each launch multiplies the interface problem rather than
solving it. Attitude control and power through a campaign A36 puts at up to 42 hours, against a
vehicle designed to be passivated. The debris-mitigation case for keeping a stage manoeuvring.
Gas stores, excluded deliberately. The mechanism model is **60 % of store mass floored at 2 kg**,
a declared assumption with no derivation and the largest guess in this run.
**Tip-off is untouched:** A23's 36–231 °/s survives every architecture here and worsens with
acceleration.
