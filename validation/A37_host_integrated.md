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

*(Filled after the run. Nothing above this line changes.)*
