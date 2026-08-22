# A71 — a numerically converged guided-contact solution

**Closes, if it passes:** the numerical half of [P108](../OPEN_PROBLEMS.md).
[A67](A67_guided_contact.md) produced a result at one step size, [A68](A68_contact_law.md) found a
**65 %** model-form spread in it, and [A70](A70_guided_contact_derived.md)'s retest on the
corrected centreline moved from **44.17 to 17.14 °/s** when the step was quartered. **No physical
statement can rest on any of those.**

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/guided_contact_ivp.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/guided_contact_ivp.py`, which must return
> nothing.

## The numerical problem, stated

**The contact is persistent, not impulsive.** The eccentric gas moment and the bore curvature press
the piston lands against the wall and hold them there; A67 counted 25–39 *onsets* over 0.42 s, but
between them the lands are in continuous sliding contact. **A penalty contact in persistent sliding
behaves as a very stiff spring**, and A67's explicit fixed-step RK4 was integrating a
~1.8 kHz contact oscillation with a step chosen from a stability estimate rather than from an
accuracy requirement.

**Three things follow, and the bands below test all three.**

1. **A stiff, adaptive, implicit integrator is the right tool**, not a smaller explicit step.
2. **The penalty stiffness is a numerical device.** In persistent contact the physical answer must
   be *insensitive* to `K` once penetration is small against the clearance. **That insensitivity
   is the convergence test for a penalty method**, and it is a stronger test than a step sweep.
3. **The peak penalty force is not a physical observable.** It is the product of an arbitrary
   stiffness and a penetration that goes to zero as the stiffness rises. **Contact impulse and
   normal load averaged over the contact are observables; the instantaneous peak is not**, and
   this run says so rather than quoting one.

## Acceptance bands

**Eight bands. Bands 2, 3, 5 and 7 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Rigid-limit regression.** With zero clearance forcing — straight bore, no eccentricity, no CG offset — exit velocity reproduces `exit_velocity_m_s_at_friction_allowance` = **29.01 m/s** to **1 %** | The implicit model does not contain the 1-DOF one |
| **2** | **Tolerance convergence.** Exit angular rate changes by **< 2 %** between `rtol = 1e-8` and `1e-9`, at fixed `K` | The integrator tolerance still controls the answer |
| **3** | **Stiffness insensitivity.** Exit angular rate changes by **< 5 %** across **K spanning two decades**, with peak penetration ≤ 10 % of the radial clearance at the stiffest | The answer is a property of the penalty parameter and not of the machine. **This is the band that matters** |
| **4** | **Energy closes to 1 %** at the converged point | Energy is being created or destroyed |
| **5** | **Two formulations agree within 25 %** — the [A68](A68_contact_law.md) laws, at the same converged settings | Model form still dominates and no physical statement is available |
| **6** | **Contact impulse is reported and the instantaneous peak force is not quoted as physical** | Report-only, and it is the honesty band |
| **7** | **Exit angular rate at the nominal point ≤ 2.0 °/s** | Gen6 misses tip-off on a converged solution — **and unlike A67, that would be a physical statement** |
| **8** | **Land separation swept only inside the geometrically admissible region** — A70's map, so ≤ 200 mm at 1 K | The sweep includes configurations whose piston cannot pass the bore |

## What this run does not do

**It does not calibrate against hardware** — **E4**. It does not model stick-slip, roundness,
inertia variation or tube compliance; those are [P103](../OPEN_PROBLEMS.md)'s second-order set. It
does not redesign anything, and **no parameter is changed to make a band pass.**


---

## Results

**RUN 2026-08-22. Two PASS, three FAIL, three NOT EVALUABLE.** *The run did not converge, and that
is the result.*

`analysis/guided_contact_ivp.py`, bands committed before it existed.

| # | Band | Result | |
|---|---|---|---|
| 1 | rigid-limit regression to 1 % | **28.8216 against 29.01 m/s, -0.650 %** | **PASS** |
| 2 | tolerance convergence < 2 % between 1e-8 and 1e-9 | **12.4 %** | **FAIL** |
| 3 | stiffness insensitivity < 5 % over two decades, penetration <= 10 % | **8.3 % over ONE decade; 28.6 % penetration** | **FAIL** |
| 4 | energy closes to 1 % | **+1.51 %** at rtol 1e-8 | **FAIL** |
| 5 | two formulations agree within 25 % | not reached | **NOT EVALUABLE** |
| 6 | contact impulse reported, peak penalty force not quoted as physical | **3.11 N.s** at rtol 1e-8 | **PASS** |
| 7 | converged exit angular rate <= 2.0 deg/s | bands 2-4 must pass first | **NOT EVALUABLE** |
| 8 | land sweep inside the admissible region | not reached | **NOT EVALUABLE** |

### The convergence evidence, in full

**Tolerance sweep**, nominal point, A69's corrected centreline, 1 K gradient:

| `rtol` | Exit angular rate | Peak penetration | Accepted steps |
|---|---:|---:|---:|
| 1e-7 | 62.875 deg/s | 40.98 % of clearance | 16 813 |
| 1e-8 | **52.895** | 45.25 % | 31 667 |
| 1e-9 | **46.335** | 54.62 % | 49 202 |

**Stiffness sweep**, at `rtol` = 1e-8:

| `K` | Exit angular rate | Peak penetration | Accepted steps |
|---|---:|---:|---:|
| nominal | 52.895 deg/s | 45.25 % | 31 667 |
| **x10** | **48.500** | **28.63 %** | 96 675 |
| x100 | *not run - the step count exceeded what this analysis can afford* | | |

**The second decade was not run and the band fails without it**: the spread over the decade that
*was* run is **8.3 %** against a 5 % criterion, and the penetration at the stiffer point is
**28.6 %** against a 10 % one. *Neither sub-criterion is met, so the missing decade cannot change
the verdict - but the shortfall is recorded rather than presented as a completed sweep.*

### What this establishes, and it is narrow

**The rate falls monotonically as the solution is resolved more accurately - 62.9, 52.9, 46.3 -
and the penetration rises as it does.** *That is the signature of a solution still under-resolved,
and it bounds nothing.* **No exit angular rate is quoted from this run.** Band 7 is NOT EVALUABLE
rather than failed, because a band cannot be judged against a number that does not exist.

**Band 4 also fails, at +1.51 %.** Small, but above the declared 1 %, and at penetrations of tens
of percent of the clearance the contact stores and returns a non-negligible amount of work.
*Both failures point the same way: the contact is not a small perturbation at this stiffness.*

### The diagnosis, stated so the next run can be designed against it

**Penetration of 28-55 % of the radial clearance is the problem.** A penalty contact stands in for
a rigid one only while the penetration is small against the geometry it replaces. **At 45 % it is
not a contact model, it is a soft bumper**, and no integrator tolerance repairs that.

**Three routes, all computation, none tried here:**

1. **Raise `K` until penetration is <= 10 %, then re-converge in tolerance at that stiffness** -
   the direct route, and the one whose cost stopped this run.
2. **Replace the penalty with a constraint** - a stabilised index-3 contact formulation, where the
   land is on the bore or off it and there is no penetration to resolve.
3. **A compliant piston.** If the land may deflect, the contact stiffness is a physical number
   rather than a numerical parameter, and the convergence question changes character.

**[P108](../OPEN_PROBLEMS.md) is not closed and the 2.0 deg/s band is not evaluated.**

### What did improve

**[P112](../OPEN_PROBLEMS.md).** The lateral bore lookup wrapped the rear land to the far end of
the tube: penetration at the nominal point was **1192 %** of the clearance before that was found
and **45 %** after. **The earlier solver blocker was substantially a geometry error**, and what
remains is a genuine, well-posed numerical-method problem.

> **No result file is committed for this run.** The runner was stopped before it wrote one, and
> the numbers above are from the completed sweeps rather than from a JSON. *A run sheet without a
> results file is a gap, and it is recorded as one rather than filled by hand.*
