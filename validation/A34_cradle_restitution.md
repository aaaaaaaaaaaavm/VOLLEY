# A34: does the rattle settle before release?

**Closes the analysis half of [P41](../OPEN_PROBLEMS.md), and with it kill criterion 4's last
open question.**

[A23](A23_tipoff_release.md) found the release itself comfortable — the payload coasts **12.2 ms
with commanded force already at zero**, and at the ~1 N residual that leaves, the mechanism has
250 µs of slack and still lands two orders of magnitude inside the 2 °/s band.

**What A23 could not settle is the start of the stroke.** The payload's centre of mass sits
**70 mm** off the thrust line, so the 413.2 N push applies a **28.92 N·m** moment and an angular
acceleration of **688 rad/s²**. The cradle holds it with clearance, so it crosses that clearance
and **arrives at the far side at 36–231 °/s — 18 to 115× the tip-off band.**

A23 stated the consequence honestly and stopped: *"after impact it rebounds and rattles, and
whether that has settled by release depends on a restitution model this project does not have."*

**This sheet is that model.**

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/cradle_restitution.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/cradle_restitution.py`, which returns nothing.

## What is being computed

A payload bouncing in a clearance under a constant angular acceleration is the **bouncing-ball
problem**: each impact returns a fraction *e* of the approach rate, the moment re-accelerates it
across the gap, and it impacts again sooner and slower.

For arrival rate ω₀ and acceleration α, the flight time after the first impact is 2eω₀/α, and the
series of flights sums to

$$t_{\text{settle}} = \frac{2\omega_0}{\alpha}\cdot\frac{e}{1-e}$$

**which is finite for every e < 1.** So the rattle always settles — the question is only whether
it settles *before the force is removed*, because whatever angular rate survives that moment is
what the satellite leaves with.

The powered stroke is **146.4 ms** (158.6 ms less the 12.2 ms coast). After force removal α = 0,
so nothing further settles: any residual rate persists to release unchanged.

## Acceptance bands

### Band 1 — the impact model reproduces A23

**Band: arrival rate at the first impact agrees with A23's published table to within 5 %**, at the
same clearances, moment and inertia, all imported rather than restated.

Fifth sheet running to carry a verification band, and the fourth in which the previous run's
solver was wrong. A33's beam solver was wrong by a factor of *h* and two bands passed on it
because nothing checked it.

### Band 2 — the rattle settles inside the powered stroke

**Band: at a coefficient of restitution of 0.7 — the top of the published range for
aluminium-on-aluminium — the settling time is below the 146.4 ms powered stroke**, at the worst
clearance in A23's table.

**This band may fail**, and if it does the payload is still bouncing when the force is removed.

### Band 3 — and the residual rate at force removal clears the tip-off band

**Band: the angular rate at the instant force is removed is below 2 °/s**, for restitution up to
0.7 and every clearance in A23's table.

This is the band that decides kill criterion 4. **It may fail**, and a failure is a design
requirement on the cradle, not a widened band.

### Band 4 — the margin, stated as a number rather than a hope

**Quantity:** the critical restitution *e\** above which the rattle does not settle within the
powered stroke.

**Band: e\* ≥ 0.8**, comfortably above the aluminium-on-aluminium range.

An answer near 0.7 would mean the design sits on the edge of a material property nobody has
measured.

### Band 5 — the preload that removes the question

**Quantity:** the cradle contact preload that prevents lift-off entirely, so no clearance is
crossed and no impact occurs.

**Band: it agrees with A23's stated > 85 N per contact to within 20 %**, computed independently
from the same moment and geometry.

If the preload route is what closes P41, the number has to come from somewhere other than the
sheet that first asserted it.

## What this cannot settle

- **Restitution is not measured.** It is swept. No coupon test exists and **E4** stands.
- **Rigid-body impact, one axis.** No contact stiffness, no local deformation, no friction, and
  rotation about one axis only. A real cradle impact is three-dimensional and inelastic in ways a
  scalar *e* does not capture.
- **The clearance is a parameter, not a drawing.** `cad/parameters.json` does not specify a cradle
  fit, which is itself part of why P41 is open.
- **It says nothing about damage.** A 231 °/s arrival is a load case for the satellite's own
  structure as well as a rate, and this sheet computes only the rate.
