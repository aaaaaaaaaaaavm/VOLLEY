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

## Result, 2026-08-13: it centres itself, and A30's thrust was 4.4x optimistic

`analysis/plate_normal_force.py`, bands committed at `f3b73d6` before it existed. Results in
`analysis/results/plate_normal_force.json`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | normal force restoring inside ±1.0 mm | **restoring at every offset** | **PASS** |
| 2 | \|F_normal\| at 0.5 mm ≤ 20 % of thrust | **0.1 %** | **PASS** |
| 3 | thrust at 0.5 mm offset within 10 % | **0.10 %** | **PASS** |
| 4 | thrust within 10 % at 3 mm lateral offset | **1.69 %** | **PASS** |
| 5 | peak thrust in 0.5–1.0 × B²/2μ₀ | **22.9 %** | **FAIL, low** |

### Bands 1–4 — the alignment question is answered, and decisively

**The plate centres itself, and the force doing it is negligible.**

| Offset from centre | Thrust | Net transverse force | Direction |
|---:|---:|---:|---|
| 0.00 mm | 377.5 N | 0.0 N | centred |
| 0.25 mm | 377.4 N | −0.2 N | **restoring** |
| 0.50 mm | 377.1 N | −0.5 N | **restoring** |
| 1.00 mm | 376.0 N | −0.9 N | **restoring** |

A conducting non-magnetic sheet between two travelling fields is pushed **away** from whichever
stator it approaches: the nearer stator induces the larger eddy current, and eddy forces are
repulsive. The equilibrium is stable and the machine holds its own payload centred **with no
bearing at all** — which is the outcome that keeps **E21**'s fretting, cold-welding and
lubricant problem out of this architecture, and it is why A27 screened out the screw drive.

**And the restoring force is 0.1 % of thrust**, so it is not a load case the customer's
satellite has to be qualified for. Band 2 allowed 20 %; the answer is two hundred times inside
it. Thrust is essentially blind to alignment — **0.10 % over half a millimetre of gap error and
1.69 % over three millimetres of lateral error** — so **A28**'s velocity loop is not regulating
against a disturbance it cannot see.

**This was the band most likely to kill the plate drive, and it did the opposite.**

### Band 5 fails low, and it corrects A30 rather than this sheet

**Peak thrust is 22.9 % of the magnetic-pressure ceiling, not the 50–100 % the band required.**

The band is written to catch a solve that exceeds physics *or* falls far short of it. It caught
the second. The machine does not reach B²/2μ₀ at a 7 mm magnetic gap and a 48 mm pole pitch —
the field decays across the gap and the coupling is imperfect long before the ideal thin-sheet
limit applies.

**The consequence lands on A30, not here.** `A30_rail_drive.md` reported the plate making
**1652 N at 0.45 T** by taking the ceiling and applying the edge factor. The layered solve says
**378 N** at the same flux density and geometry — **a factor of 4.4.** That figure is corrected
in place and logged as **P50**. Nothing about A30 band 4 changes: the edge factor is 0.6691 and
that is a separate measurement.

### Band 5 caught two bugs before any of that was readable

**The first run returned a peak thrust of 568 kPa against a 80.6 kPa ceiling — 705 % of
physics.** Two faults, both structural rather than arithmetic:

1. **The model was single-sided.** One current sheet and a flux return is not a double-sided
   machine. It now carries two sheets, each backed by iron, which is what the geometry is.
2. **The flux density was normalised on the wrong surface** — on the field at the plate *with
   the plate present*, which is screened. Demanding 0.45 T there drove the source arbitrarily
   hard. It is now normalised on the **open-gap** field, computed with σ = 0, which is what a
   designer means by airgap flux density.

**Fifth time a declared band has caught a defect in an analysis rather than in the design**, and
the second time today: A30 band 2 caught a solver returning identically zero hours earlier.

### The design sweep, kept separate from the bands

**A failed band is never re-run at a geometry chosen after the fact.** Bands 1–5 stand exactly as
declared, at the geometry A30 implied. The sweep below is separate work asking what *would*
close, and it is reported as a direction rather than as a result.

| B_g | Pole pitch | Clearance | Plate | % of ceiling | Thrust | a/g | v_exit | Plate mass |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.75 T | 48 mm | 2.0 mm | 5 mm | 29.5 % | 1356 N | **31.3 g** | 28.26 m/s | 0.414 kg |
| 0.75 T | 48 mm | 1.5 mm | 5 mm | 26.3 % | 1208 N | **27.9 g** | 26.68 m/s | 0.414 kg |
| **0.75 T** | **48 mm** | **1.5 mm** | **3 mm** | 19.6 % | **900 N** | **21.6 g** | **23.48 m/s** | **0.248 kg** |
| 0.60 T | 48 mm | 2.0 mm | 5 mm | 29.5 % | 868 N | 20.0 g | 22.61 m/s | 0.414 kg |
| 0.60 T | 48 mm | 2.0 mm | 3 mm | 22.8 % | 671 N | 16.1 g | 20.26 m/s | 0.248 kg |

**The best point inside the 25 g payload qualification cap is 900 N, 21.6 g, 23.48 m/s** — on a
**0.248 kg** plate, against Gen5's 16.39 m/s from a 9.445 kg sled. The two rows above it exceed
the cap and are excluded, not quoted.

**Read conservatively, the 0.60 T row is the one to design to**: **20.26 m/s at 16.1 g**, still
24 % faster than Gen5 with a moving mass of 4.25 kg instead of 13.45 kg, and with the flux
density well inside what an iron-cored stator gives without arguing about saturation.

---

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
