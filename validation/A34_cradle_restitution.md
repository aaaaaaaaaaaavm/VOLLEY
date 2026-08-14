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

> ## Annotated 2026-08-14 by A38. Nothing below is edited.
>
> This run was recorded on 2026-08-13 at the operating point
> [ADR-030](../docs/adr/030-apply-the-depth-resolved-thrust-constant.md) superseded the same day.
> `analysis/cradle_restitution.py` computes its inputs live from `motor_model`, so **the script
> tracked the correction and this record did not.**
>
> | | Recorded here | Current |
> |---|---:|---:|
> | Payload force | 413.2 N | **395.1 N** |
> | Offset moment | 28.92 N·m | **27.65 N·m** |
> | Angular acceleration | 688 rad/s² | **658 rad/s²** |
> | Settling at e = 0.7 | 27.25 ms | **27.88 ms** |
> | Powered stroke | 146.4 ms | **150.1 ms** |
> | Critical restitution | 0.9261 | **0.9263** |
> | Preload per contact | 85.0 N | **81.2 N** |
>
> **Every band below still passes when re-run**, and no verdict changes; the figures are stale by
> about 2.3 %. Found by [A38](A38_tipoff_at_gen6.md) band 1, which exists to catch exactly this.
> Recorded as **P61**.

## Result, 2026-08-13: it settles in 27 ms of a 146 ms stroke, and leaves at zero

`analysis/cradle_restitution.py`, bands committed at `77d45bb` before it existed. Results in
`analysis/results/cradle_restitution.json`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | arrival rate reproduces A23 within 5 % | **0.15 %** | **PASS** |
| 2 | settles inside the 146.4 ms powered stroke at e = 0.7 | **27.25 ms** | **PASS** |
| 3 | residual rate at force removal < 2 °/s | **0.0000 °/s** | **PASS** |
| 4 | critical restitution e\* ≥ 0.80 | **0.9261** | **PASS** |
| 5 | preload within 20 % of A23's 85 N | **85.0 N** | **PASS** |

### The answer

**The payload is resting against its cradle stop long before the force is removed.**

| Restitution | Settling time, worst 2 mm clearance | Residual rate at force removal |
|---:|---:|---:|
| 0.3 | 5.01 ms | **0** |
| 0.5 | 11.68 ms | **0** |
| **0.7** — top of the aluminium range | **27.25 ms** | **0** |
| 0.9 | 105.12 ms | **0** |

**Every plausible restitution settles inside the 146.4 ms powered stroke, and the residual rate
at the instant force is removed is exactly zero for every clearance in A23's table.** The
36–231 °/s arrival is real and it is transient: it is spent in the first tens of milliseconds,
against a stop, while the force that caused it is still holding the payload there.

**Critical restitution is 0.9261** — the value above which bouncing would still be in progress at
force removal. Aluminium-on-aluminium is 0.3–0.7, so the margin is not marginal.

**A23's 36–231 °/s therefore never becomes a release rate**, and kill criterion 4's last open
question resolves in the design's favour rather than against it. The release itself was already
comfortable; the start of the stroke is now shown to be transient rather than persistent.

### Band 5 reproduces A23's preload from a different direction

A23 asserted a cradle preload of **> 85 N per contact**. Computed here independently from the
same moment and geometry — two contacts a half-length either side reacting 28.92 N·m as a couple
— the answer is **85.0 N**. **The requirement stands, and it now has a derivation behind it
rather than only an assertion.**

**That, not the restitution sweep, is what closes P41's analysis half.** The rattle settling is
the reason the design survives *without* the preload; the preload is the reason it does not have
to rely on that.

### Band 1 caught the fifth first-run solver error in five sheets

**Arrival rate came out 56.84 °/s against A23's 36.5 — 55.7 % high — and the preload came out
206.7 N against 85, 143 % high.** One cause: **the lever that takes up the clearance is not the
lever that applies the moment.**

The moment arm is the **70 mm** centre-of-mass offset. The clearance is taken up at the cradle
contacts, which sit at the payload's **ends**, so a rotation moves them by half the payload
length — **170.25 mm**. Using 70 mm for both inflates the angle for a given gap and shrinks the
couple arm for a given force, which is exactly the pair of errors observed.

**Five new solvers in five sheets, five wrong on first run, five caught.** A33's was the only one
whose verification band was missing, and it was added afterwards. This one had a verification band
and it did its job on the first execution.

---

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
