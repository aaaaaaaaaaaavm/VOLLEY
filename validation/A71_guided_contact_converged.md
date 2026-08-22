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
