# A23: tip-off at release, modelled rather than bounded

**Closes:** nothing outright. **Converts** `docs/KILL_CRITERIA.md` §4 from *unmodelled* to a
quantified requirement on a mechanism that does not yet exist, and advances **E7**.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/tipoff_release.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written,
> and the script is absent at this commit.
>
> **The 2 °/s band is not being re-declared.** It was fixed on 2026-07-31 under **P30**, against
> the flown internal NRCSD figure rather than the provisional external one, and **it is carried
> here unchanged.** Nothing in this sheet may move it.

## What A7-R established, and what it left out

A7 was specified against Project Chrono, which is unavailable, and the release mechanism it would
simulate **is undefined in this repository**. A7-R therefore computed the *tolerance* the
mechanism must hold rather than inventing one:

> The payload CoM sits **70 mm** off the thrust line, so the 413.2 N push produces a **28.92 N·m**
> moment about it. The angular-impulse budget to stay inside 2 °/s is **I·ω = 1.465 mN·m·s** on a
> transverse inertia of 0.042 kg·m². **The full push may act unbalanced for only 50.7 µs.**

That is a correct and useful bound. **What it does not model is the stroke.**

## The thing nobody has modelled: the payload has to take up its clearance first

The cradle holds the payload **with clearance**. Under a 28.92 N·m moment the payload does not sit
still in that clearance — **it accelerates across it and arrives at the far side with a rate.**

    alpha = M / I = 28.92 / 0.042 = 688 rad/s^2

Crossing a clearance angle θ takes √(2θ/α), and the payload arrives at ω = αt. **For any plausible
cradle clearance that arrival rate is far above 2 °/s**, which means the release rate is not the
only question — there is an impact into the cradle at the start of every shot, and it is a load
case on the payload's own rails that appears nowhere in this project.

**This is the half A7-R could not see**, because it treated release as the only event.

## Method

Three stages, all rigid-body, all numpy:

1. **Clearance take-up.** Angular acceleration under the offset moment, time and arrival rate at
   contact, swept over cradle clearance.
2. **Constrained stroke.** With the payload pressed into contact, the moment is reacted as a
   couple over the payload length; report the reaction force the cradle carries for 158.6 ms.
3. **Release.** Parametric in the mechanism, because the mechanism is undefined: sweep the
   **time skew** between the two constraint points releasing, and the **residual force** at
   release, and report the tip-off rate for each. The 2 °/s contour is the requirement the
   mechanism must meet.

**Nothing is invented.** Where a mechanism property is needed, it is a swept axis and the output
is a requirement on it.

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **Release skew tolerance for the full push**, reproducing A7-R | **50.7 µs ± 2 %** | a fork with A7-R's published bound; suspect this script |
| 2 | **Tip-off with an ideal release** — zero skew, zero residual, payload in contact | **≤ 2 °/s** | if even a perfect release fails, the *geometry* is wrong, not the mechanism, and the 70 mm CoM offset is the defect |
| 3 | **Arrival rate at clearance take-up**, for a 0.5 mm cradle clearance | **report**; expected to exceed 2 °/s by a large factor | this is a new load case either way. A figure near 2 °/s would mean the effect is benign and the sheet says so |
| 4 | **Cradle reaction force during the constrained stroke** | **≤ 200 N per contact** | above this the cradle is a structural member carrying a couple for 158.6 ms and needs its own sizing, which nothing has done |
| 5 | **CoM offset at which an ideal release passes 2 °/s with 10× margin** | **report** | gives the design target for a CoM-alignment fix, which is the alternative to a tighter mechanism |
| 6 | **Whether any combination of skew and residual in the swept space passes 2 °/s** | **yes**, at some achievable tolerance | if nothing achievable passes, tip-off is a kill criterion that the current release concept cannot meet, and that is a **HIGH** finding |

### Band 2 is the one that separates a mechanism problem from a geometry problem

**If an ideal release still tips the payload past 2 °/s, no mechanism can save it.** The fix would
have to be the 70 mm offset itself — a cradle that aligns the payload CoM with the thrust line, or
a push that is applied through the CoM rather than along the axis.

**Band 5 exists to price that fix in advance**, so the answer is available whichever way band 2
lands.

### Band 6 is written to be able to fail loudly

A release skew tolerance of tens of microseconds is **already demanding** for a mechanical
release. If the swept space shows the requirement is tighter than any achievable one-shot
mechanism, that is not a caveat — it is a statement that **kill criterion 4 cannot be met by this
release concept**, and `KILL_CRITERIA.md` §4 would move from *unmodelled* to *crossed*.

## What happens at each outcome, fixed now

1. **Band 1 fails.** Stop; reconcile with A7-R before reading anything else.
2. **Band 2 fails.** A new numbered defect against the payload CoM offset. The release mechanism
   stops being the long pole and the cradle geometry becomes it.
3. **Band 4 fails.** The cradle needs structural sizing it has never had; open it as an item.
4. **Band 6 fails.** `KILL_CRITERIA.md` §4 moves to **crossed**, and that is the most serious
   outcome available from this sheet. It would make a guided or constrained release, or a CoM-
   aligned cradle, a Phase I design requirement rather than a Phase II improvement.

**No band may be widened after the run**, and **the 2 °/s figure may not be touched at all.**

## What this cannot establish

**A7 remains unrun as specified.** This is a rigid-body model with no contact mechanics, no
structural compliance, no friction model at the rails, and no multibody solver behind it. It
computes what a mechanism must achieve; it does not verify that any mechanism achieves it, and it
cannot substitute for the Chrono run A7 asks for or for T-5 on hardware.

**The release mechanism is still undefined.** That is the honest state, and this sheet's output is
a specification for it rather than an analysis of it.
