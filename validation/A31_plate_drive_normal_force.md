# A31: does the plate stay in the gap?

**The band that decides whether the plate drive is a design or another rejected proposal.**

[A30](A30_rail_drive.md) bands 4 and 5 established that a **90 mm × 340 mm × 3 mm aluminium
plate** has an edge factor of **0.6691**, makes **1652 N at 0.45 T**, and weighs **0.248 kg** —
half the lightest cold-gas module it would replace. That is two measured bands, and it is exactly
as many as the CDS-rail proposal had before A30 band 1 killed it.

**What A30 did not touch is whether a 3 mm plate will stay centred in a ~7 mm magnetic gap while
1652 N is applied to it.** A double-sided stator balances its own attraction only while the plate
is centred. If the equilibrium is unstable, the plate clamps to one stator and the architecture
needs a bearing system it does not currently have — and a bearing at 18 m/s is **E21**'s fretting,
cold-welding and lubricant problem, which is what screened out the screw drive in A27.

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/plate_normal_force.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/plate_normal_force.py`, which returns nothing.

## What is being computed

A layered-media solution of the double-sided machine in the plane of travel: two travelling
current sheets at y = ±g/2, air, a conducting slab of thickness t at transverse offset δ, air.
With x-dependence e^(−jkx) the vector potential satisfies A″ − k²A = 0 in air and
A″ − (k² + jωμ₀σ)A = 0 in the conductor, and the force on the plate is the **Maxwell stress
integrated on planes just above and below it** — which gives thrust and normal force from the
same solution rather than from two models that could disagree.

Offset is swept. The sign of the normal force is the question: **repulsion from the nearer stator
restores the plate to centre; attraction takes it to the wall.**

## Acceptance bands

**Band 1 can fail and, if it does, the plate drive is rejected exactly as the rail drive was.**

### Band 1 — the equilibrium is stable

**Quantity:** net transverse force on the plate at an offset of **+0.5 mm** from centre, positive
sign meaning *away from centre*.

**Band: the force is restoring — it acts toward the centre.**

A conducting non-magnetic sheet between two travelling fields should be pushed away from
whichever stator it approaches, because the nearer stator induces the larger eddy current and
eddy forces are repulsive. **That is the expectation, and expectations are what bands exist to
test.** If the force is destabilising, no amount of stator design fixes it and the architecture
carries a bearing at 18 m/s.

**FAIL if the net force is destabilising at any offset inside ±1.0 mm.**

### Band 2 — and the restoring force is not itself a structural problem

**Band: the magnitude of the net transverse force at 0.5 mm offset is ≤ 20 % of the longitudinal
thrust at the same operating point.**

A restoring force is only useful if the plate and its mounting can carry it. Above 20 % of
thrust it stops being centring and becomes a load case the customer's satellite has to be
qualified for, which is a different product.

### Band 3 — thrust survives the offset

**Band: longitudinal thrust at 0.5 mm transverse offset is within 10 % of the centred value.**

If thrust is strongly offset-dependent, the closed-loop velocity control of **A28** is regulating
against a disturbance it cannot observe, and the 0.0267 m/s dispersion does not survive.

### Band 4 — and it survives lateral misalignment too

**Quantity:** thrust with the plate displaced **3 mm in-plane**, across its width, reducing the
overlap with the stator.

**Band: within 10 % of the aligned value.**

3 mm is a plausible accumulation of satellite mounting tolerance, insert clearance and magazine
indexing repeatability. This band uses A30's edge-factor solver at the reduced overlap, so it
inherits that model's limits.

### Band 5 — the solve does not exceed physics

**Band: peak thrust per unit area, maximised over slip, does not exceed B_g²/2μ₀, and reaches at
least 50 % of it.**

The magnetic pressure is the hard ceiling for any induction machine. Exceeding it means the
layered solve is wrong; falling far below it at the *optimum* slip means the geometry is not
being driven where it works. This is the same role A30 band 2 played, and A30 band 2 is why this
sheet exists at all — it caught a solver returning identically zero for every geometry.

## What this cannot settle

- **Two dimensions, not three.** The layered solve is infinite in the transverse direction; the
  edge factor from A30 is applied to it as a scalar. Normal force has its own edge behaviour that
  this does not capture.
- **Rigid, parallel, flat.** A 340 mm plate that is bowed, or mounted with a few tenths of a
  degree of tilt, sees a gap that varies along its length. Not modelled.
- **No transient.** The plate enters and leaves the stator, and entry is where a destabilising
  transverse impulse would do its damage. Steady state only.
- **Nothing is measured.** **E4** stands.
