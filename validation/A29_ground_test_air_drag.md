# A29: what air costs a ground test of exit velocity

**Bears on:** [`../docs/BENCHTOP_TESTS.md`](../docs/BENCHTOP_TESTS.md),
[`../docs/QUALIFICATION_PLAN.md`](../docs/QUALIFICATION_PLAN.md), and **E4** — because the
full-scale ground test is the step that turns this project's headline velocity into a measurement.

**The machine flies in vacuum. The test happens in a room.**

Every velocity in this repository is computed with no aerodynamic drag, because there is none in
orbit. The TRL-5 step in `QUALIFICATION_PLAN.md` is a full 1.5 m track firing a mass simulator
into the eddy brake **in a laboratory at sea level**, and its whole purpose is to compare a
measured exit velocity against the computed one.

**Nothing in this repository says what the air is worth.** A measured velocity compared to
16.388 m/s without an air correction is biased low by an amount nobody has computed, and the
comparison is therefore not a validation of the motor model — it is a validation of the motor
model plus an unquantified error.

> ## BANDS DECLARED 2026-08-13, BEFORE `validation/cfd/` EXISTS.
>
> The case directory and every script in it are absent at this commit. Verify with
> `git show --stat <this commit> -- validation/cfd`, which returns nothing.

## What is being computed

Steady incompressible RANS (`simpleFoam`, OpenFOAM v1912, k-ω SST) around the **Gen5 sled and its
3U payload as generated**, meshed with `snappyHexMesh` from `cad/stl/VOLLEY_Sled_Gen5.stl` and
`cad/stl/VOLLEY_Payload_3U_Gen5.stl`. **No idealised box.** The geometry is the same file the CAD
package ships, so the drag figure cannot describe a different machine from the one being built —
the same rule `validation/fem3d/` follows for the field.

The moving assembly spans **644 mm** along the track, **172 mm** across it and **140 mm** in
depth. Free-stream velocity is the exit velocity, **16.388 m/s**, in air at **1.225 kg/m³** and
**1.5 × 10⁻⁵ m²/s**, giving a Reynolds number of order 10⁵ on the frontal dimension — turbulent,
bluff, separated, and not a regime where a textbook drag coefficient can be trusted to better
than a factor.

Drag is then integrated over the **1.30 m acceleration zone**. Because the profile is
position-scheduled, v² rises linearly with distance and the drag force with it, so the work done
against air is not a constant times the stroke.

## Acceptance bands

**Bands 3, 4 and 5 can fail, and each failure means something different. None of them is edited
after the run.**

### Band 1 — the solve is converged in the mesh, not in the physics

The drag coefficient computed on the fine mesh agrees with the coarse mesh to within **10 %**.

If it does not, the number is a property of the mesh and nothing below it means anything.
**FAIL above 10 %.**

### Band 2 — the answer is physically possible

Drag coefficient referenced to the assembly's **projected frontal area** lies in
**0.7 ≤ C_d ≤ 2.5**.

A rectangular bluff body normal to the flow sits near 1.05–1.2 in free stream and higher under
blockage. **Outside this range the solve is wrong, not the machine** — this band exists for the
same reason the 3-D field solve's did, because a converged run that returns a physically
impossible number reports success.

### Band 3 — a ground test can be corrected rather than evacuated

The exit-velocity deficit from air over the 1.30 m stroke is **below 1.0 % of 16.388 m/s**, i.e.
**below 0.164 m/s**.

**This band may fail.** Above 1 %, air is not a correction applied to a measurement — it is a term
comparable to the design margins, and the ground test would have to be run in a vacuum chamber
that no laboratory-budget plan in this repository contains.

### Band 4 — and the correction is not negligible against what the test measures

The deficit is **at least 10 % of the published closed-loop dispersion, 0.0267 m/s (3σ)** — i.e.
at least **0.00267 m/s**.

**This band may fail, and failing is good news:** below 10 % the air correction is lost inside the
dispersion the test is trying to resolve and can be ignored. Above it, **every ground-test
velocity measurement must carry an air correction or it cannot be compared to the model at all.**
The band is written this way round deliberately — it tests the claim that the correction matters,
not the claim that it is small.

### Band 5 — the stator channel is not just background

C_d computed with the sled confined between the stator plates exceeds the free-stream C_d by at
least **10 %**.

The sled runs inside a 12 mm winding gap between two stator plates, so the flow around it is
confined rather than free. **This band may fail**, and failing means the channel is open enough
that a free-stream coefficient suffices — which is worth knowing, because it is what a reader
would assume without checking.

## What this cannot settle

- **Steady RANS on a body that is accelerating.** The assembly reaches 16.388 m/s over 158.6 ms;
  the solve treats each speed as steady. The quasi-steady assumption is standard for this
  Reynolds number and this acceleration, and it is an assumption, not a result.
- **No moving mesh, no track, no ground effect.** The body is held still in a moving stream. The
  track structure and the room are absent.
- **One atmosphere, one temperature.** Sea level at 20 °C. A test at altitude sees less.
- **Nothing here is measured.** **E4 stands.** This computes a correction to a measurement that
  has not been taken, which is the honest description of what it is for.
- **It says nothing about flight.** In orbit this term is exactly zero. A29 exists only because
  the *test* happens in air, and a result that could not be compared to the model would be a
  wasted test rather than a wrong machine.
