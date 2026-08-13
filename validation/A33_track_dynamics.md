# A33: the track's dynamic case

**Closes the analysis half of [P36](../OPEN_PROBLEMS.md), open since 2026-08-05.**

`sizing.py::track_first_mode()` checks the track against **one static target — above 70 Hz to
clear the launch primary band.** A17 showed that is necessary and not sufficient: every shot
chirps the force ripple through the modes and the fundamental crossing is amplified **8.18×**,
twelve times per campaign, and **it does not go away with damping** — 6.51 at Q = 20, 8.33 at
Q = 500.

P36 names three things the project does not have. **This sheet addresses the second and third**:

1. a damping specification with a measurement behind it — **still absent, and out of reach here**;
2. **a moving-load model**, since the ripple force travels with the sled and A17's SDOF does not
   represent that;
3. **a dynamic acceptance criterion** beside the static 70 Hz one.

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/track_dynamics.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/track_dynamics.py`, which returns nothing.

## What is being computed, and the mechanism that makes it non-trivial

**The sled is 13.445 kg riding a track whose whole distributed mass is 20 kg.** A mass that large,
moving along a beam, does not leave the beam's modes where it found them: the first mode is
**depressed while the sled is near midspan and recovers as it leaves.** The track's first mode is
therefore **not a number during a shot. It is a function of position.**

Meanwhile A17's ripple chirp sweeps **upward** with velocity, `f = v/λ`. So the excitation rises
while the mode falls, and **where they cross is not where A17's fixed-frequency SDOF put it.**

The transverse path matters too, and it is not obvious: thrust and ripple act **along** the track,
but at the stator plane, which is **offset from the longerons' neutral axis**. That eccentricity
is what converts an axial ripple into a bending moment, and bending is what changes the **12 mm
winding gap** — at **13.1 % of thrust per millimetre**, from `sizing.gap_tolerance()`.

## Acceptance bands

### Band 1 — the modal model reproduces the one this project already publishes

**Band: with the sled absent, the first mode agrees with `sizing.track_first_mode()` to within
2 %, in both the pinned-pinned (48 Hz) and fixed-fixed (109 Hz) cases.**

Everything below is a perturbation of that model. If it does not reproduce the published number,
nothing after it means anything. Third sheet running to carry a verification band first, and the
reason is that the previous three all caught a solver defect.

### Band 2 — the launch case still clears the target it was designed to

**Band: with the sled parked at the breech and twelve satellites stowed, the first mode stays
above the 70 Hz target.**

This is the case `sizing.py`'s target was written for. It has never been evaluated with the
stowed mass actually on the beam.

### Band 3 — the chirp crossing and the mode depression do not coincide

**Quantity:** the ripple-chirp frequency `v(x)/λ` and the position-dependent first mode `f₁(x)`,
both as functions of sled position through the stroke.

**Band: at the position where the chirp crosses the first mode, the mode is within 10 % of its
undepressed value.**

If the crossing happens while the sled is near an anchored end, the mode is barely depressed and
A17's fixed-frequency treatment is adequate. **If the crossing happens near midspan, where the
sled depresses the mode most, then the excitation and the mode move toward each other, the sweep
rate through coincidence is lower than A17 assumed, and the 8.18× amplification is an
underestimate.** **This band may fail, and it is the one that decides whether A17 was
conservative.**

### Band 4 — what the track's motion does to the thrust constant

**Band: peak-to-peak K<sub>t</sub> modulation from track deflection over one stroke is ≤ 0.5 %.**

Computed as the eccentric ripple moment's midspan deflection, amplified by A17's own factor, times
the 13.1 % per millimetre gap sensitivity. Above 0.5 % the track is modulating the machine's own
thrust constant within a shot, which neither `motor_model` nor **A28**'s velocity loop knows about.

### Band 5 — the moving load is not the governing effect

**Band: the sled's exit velocity is below 20 % of the beam's critical speed** `v_cr = 2 f₁ L`.

Below roughly a fifth of critical, a travelling load is quasi-static and the classic moving-load
amplification is small. This is the band that tells us whether the missing moving-load model P36
names is a real gap or a formality.

### Band 6 — the arrest pulse

**Band: peak midspan deflection under the 18.5 kN arrest, applied eccentrically at the brake
station, is ≤ 5 % of the 12 mm winding gap (0.6 mm).**

The arrest is by far the largest force the structure sees in flight, and it acts at the far end of
the beam over about 16 ms — comparable to the mode period.

## What this cannot settle

- **No damping specification.** The project has no measured Q or loss factor for a bolted
  aluminium track, and this sheet does not produce one. **A17's amplification is used as given.**
  P36's first missing item stays missing, and T-2's sine sweep in
  [`../docs/QUALIFICATION_PLAN.md`](../docs/QUALIFICATION_PLAN.md) is where it gets measured.
- **Beam model, not FEA.** Two box longerons as an Euler–Bernoulli beam with a travelling point
  mass. No joints, no brackets, no stator shear lag, no torsion.
- **The eccentricity is a stated assumption.** The offset between the stator plane and the
  longeron neutral axis is not in `cad/parameters.json` as such and is taken from the section
  geometry.
- **Nothing is measured.** **E4** stands.
