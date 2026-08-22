# A70 — guided contact, on a derived centreline and a verified contact law

**This is a re-run of [A67](A67_guided_contact.md) with two inputs replaced.** A67's bands are not
re-declared and its verdict stands. **These bands are declared before this re-run, and the code
change that makes the re-run possible is committed after them.**

> ## BANDS DECLARED 2026-08-22, BEFORE THE CENTRELINE COUPLING EXISTS.
>
> `analysis/guided_contact.py` exists — it is A67's model. **What does not exist at this commit is
> the coupling that lets it consume [A69](A69_tube_centreline.md)'s centreline**, and that is what
> these bands are declared ahead of. Verify with `git log -1 --format=%H` against the commit that
> adds `bore_from_a69` to that file.

## What changed since A67, and why each change is allowed

| | A67 | **A70** |
|---|---|---|
| **Contact law** | Lankarani–Nikravesh. **A67 band 3 failed**: +13.7 % restitution error at the nominal coefficient, +128 % at 0.3 | **[A68](A68_contact_law.md)'s selection.** LN's error vanishes as e → 1, which is its documented domain limit, and a formulation that does not assume it recovers the coefficient it is given |
| **Bore centreline** | a sinusoid of **declared** amplitude, 0.1–2.0 mm, at twice the support pitch | **[A69](A69_tube_centreline.md)'s computed shape** — the deflected curve of the actual section on its actual supports, with the contributions solved separately |

**Neither replaces a band. Both replace an input**, and A67 is what says they had to be replaced:
its band 3 failure named the law and its band 9 result named the centreline as the dominant
sensitivity at S_T = 0.894.

## Acceptance bands

**Six bands. Bands 2, 3 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **The coupling is exact.** With A69's shape scaled to zero, the model reproduces A67's zero-straightness case to **0.5 %** on exit velocity | The centreline plumbing changed something it should not have |
| **2** | **Exit angular rate at the orbital centreline ≤ 2.0 °/s** | Gen6 still misses tip-off with a derived shape and a verified law, and **[P108](../OPEN_PROBLEMS.md) survives every objection raised against A67** |
| **3** | **3σ over A69's orbital range ≤ 2.0 °/s** | Same, under the tolerance the structural model actually produces rather than an assumed bracket |
| **4** | **Peak contact normal force ≤ 445.88 N** at the orbital centreline | The guide carries more than the drive pushes with |
| **5** | **The A67 → A70 change in exit angular rate is ≤ 50 %** | The two runs disagree about the machine by more than model form should account for, and the earlier headline must be withdrawn rather than refined |
| **6** | **Energy closes to 0.5 %** | Report-only; the same closure A67 passed |

## What this run does not do

**It does not calibrate against hardware** — **E4**. **It does not model manufacturing
straightness**: A69 computes the *deflected* shape and declares manufacturing tolerance
separately, and what an 8 m bore can actually hold is [`MANUFACTURING.md`](../docs/MANUFACTURING.md)'s
to establish. It does not redesign anything: **no support pitch, land separation, clearance or
bore is changed to make a band pass.**

---

## Results

**RUN 2026-08-22. Two of six pass and four are NOT EVALUABLE.** *That is not a pass and it is not
a failure; it is a run that could not answer four of its own questions, recorded as such.*

| # | Band | Result | |
|---|---|---|---|
| 1 | coupling exact when the shape is scaled to zero, 0.5 % | **0.0000 %** | **PASS** |
| 2 | exit angular rate at the orbital centreline ≤ 2.0 °/s | — | **NOT EVALUABLE** |
| 3 | 3σ over A69's orbital range ≤ 2.0 °/s | — | **NOT EVALUABLE** |
| 4 | peak contact normal force ≤ 445.88 N | — | **NOT EVALUABLE** |
| 5 | A67 → A70 change ≤ 50 % | — | **NOT EVALUABLE** |
| 6 | energy closes to 0.5 % | gas work 2350.2 J | **PASS** |

### Why four bands cannot be answered

**A69's centreline is a piecewise field with curvature jumps at every support.** A67's sinusoid is
analytic and infinitely smooth; the real shape is not. **The penalty contact solver does not
converge on it at any step this analysis can afford** — a step **forty times** below the one A67's
own convergence study settled on still did not complete a single case, and the runs that do
complete return contact forces of 10¹² N, which are integrator divergence and not physics.

**This is a solver limitation and it is stated as one.** It is not evidence that the machine jams,
and it is not evidence that it does not. *A67's numbers stand as A67's, on A67's assumed shape.*

### What this run does deliver, and it needs no solver at all

**The geometric question comes before the dynamic one: can a rigid piston with two lands physically
pass through this bore?** That is a three-point mismatch — the deviation of the centreline at the
mid-point from the mean of the two land positions — and it is computed directly from A69's curve
with no differentiation and no integration.

**Three-point sagitta, in µm, against a nominal radial clearance of 25.0 µm:**

| Across-diameter gradient | 40 mm | 80 mm | **120 mm** | 200 mm | 400 mm |
|---|---:|---:|---:|---:|---:|
| **0 K** — support placement only | 0.0 | 0.2 | **0.4** | 1.2 | 4.4 |
| **0.5 K** | 6.4 | 12.7 | **18.7** | **30.7** ✗ | **56.5** ✗ |
| **1.0 K** | 12.8 | **25.1** ✗ | **37.3** ✗ | **60.4** ✗ | **109.5** ✗ |
| **2.0 K** | **25.7** ✗ | **50.2** ✗ | **74.7** ✗ | **119.9** ✗ | **215.3** ✗ |

> ## The design point does not admit its own piston at a one-kelvin gradient
>
> **At the nominal 120 mm land separation and 50 µm diametral clearance, a 1 K across-diameter
> temperature gradient puts the bore 37.3 µm out of line over the piston's own length — 1.5× the
> radial clearance.** The piston cannot pass. **At 2 K nothing passes at any land separation
> tested.**
>
> **And the trade runs the wrong way.** [A67](A67_guided_contact.md) band 8 found that *longer*
> land separation reduces exit angular rate. **Longer lands also jam sooner** — 400 mm is
> inadmissible at half a kelvin. *Angular constraint and geometric admissibility are in direct
> opposition, and nothing in the record had priced that.*

**This is a hard constraint, not a sensitivity.** It does not depend on the contact law, the
integrator, the friction, the eccentricity or the restitution. **It is the geometry of a rigid
body in a curved tube**, and the only inputs are A69's computed centreline and
`gen6_drive.bore_mm`.

### What it does not say

**It does not say Gen6 fails.** It says **this configuration** — 15.805 mm bore, 50 µm diametral
clearance, a rigid two-land piston at 120 mm, seven supports at 1.0 m, at a 1 K gradient — does
not admit its own piston. **Every one of those is a design variable and none has been chosen
against this constraint**, because until now the constraint was not known.
**No parameter is being changed here to make a band pass**, and the redesign
[P109](../OPEN_PROBLEMS.md) names is deliberately left to be done as design rather than as a fix
inside a validation run.

### What is still open in this run

**Bands 2–5 need a contact solver that survives a piecewise centreline.** The candidates are a
smoothed centreline representation with continuous curvature, an implicit or stiff integrator, or
a compliant piston that does not need to be rigid. **All three are computation and none is
hardware** — this run is recorded as not having answered them.
