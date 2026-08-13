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

## Result, 2026-08-13: the correction is 5.1 mm/s, and two bands fail

`validation/cfd/`, result in `analysis/results/cfd_air_drag.json`, figures
[`cfd/figures/A29_cfd_report.png`](cfd/figures/A29_cfd_report.png) and
`paper/figures/F14_airdrag.png`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | fine and coarse mesh agree within 10 % | *running* | — |
| 2 | 0.7 ≤ C_d ≤ 2.5 | **0.523** | **FAIL** |
| 3 | deficit below 1.0 % of v_exit | **0.0312 %** | **PASS** |
| 4 | deficit ≥ 10 % of the 0.0267 m/s dispersion | **19.2 % of it** | **PASS** |
| 5 | channel C_d exceeds free-stream C_d by ≥ 10 % | **−12.7 %** | **FAIL** |

### The answer the test needs

| | |
|---|---:|
| Drag at exit velocity, free stream | **1.734 N**, spread ±0.144 N over the averaging window |
| Work against air over the 1.30 m stroke | **1.127 J** |
| Exit velocity, vacuum → sea-level air | **16.3880 → 16.3829 m/s** |
| **Deficit** | **5.116 mm/s (0.0312 %)** |
| Against the 3σ dispersion the test exists to resolve | **19.2 % of it** |
| As a servo command instead | **1.734 N, 0.125 % of the 1389 N shot** |

**A full-scale ground test can be run in air and does not need a vacuum chamber.** But
**every velocity it measures must carry the correction**, because 5.1 mm/s is a fifth of the
dispersion the test is there to resolve. A measurement compared to 16.388 m/s without it is
being compared to the wrong number by an amount comparable to the quantity being measured.

**Bands 3 and 4 together are the useful result**, and they point in opposite directions on
purpose: band 3 says the term is small, band 4 says it is not small *enough to ignore*. Either
alone would have been misleading.

**One thing the bands do not ask, stated because a reader will.** The bands measure the
**open-loop** deficit, which is what a raw shot comparison sees. A servo tracking the velocity
profile nulls it instead, and it appears as **1.734 N of extra commanded force — 0.125 % of the
shot** — rather than as velocity error. So a *closed-loop* ground test measures the right
velocity and hides the air in the current trace; an *open-loop* one measures 5.1 mm/s slow. Which
of those a test is depends on how it is run, and the run sheet in
[`../docs/QUALIFICATION_PLAN.md`](../docs/QUALIFICATION_PLAN.md) does not currently say.

### Band 2 fails, and the solve is not what is wrong

C_d = **0.523** against a declared floor of 0.7 — 0.419 of pressure drag solved plus 0.104 of
viscous bound.

**The band was declared against a solid bluff body and the assembly is not one.** A rectangular
body normal to the flow sits near 1.05–1.2, and that is where 0.7 came from. What the CFD is
actually resolving is a **stepped** body: the 3U payload leads with a 100 × 100 mm face, and the
sled behind it is wider — 172 × 140 mm — so a large part of the reference frontal area sits in
the payload's own wake. Referencing a coefficient to an area that is partly shadowed gives a
coefficient below the textbook value for the shape it was compared against.

**Three checks say the solve is right and the band was the wrong shape of question:**

| Check | Result |
|---|---|
| Peak C_p anywhere on the body | **0.975** — a stagnation point should approach 1.000, and it does |
| Meshed wetted area vs raw STL surface | **0.4173 m² of 0.5612 m²** — the difference is the payload–sled interface, interior and correctly not wetted |
| Where the drag comes from | Forward faces **+0.233**, base suction **+0.156**, sides **+0.001** — the classic bluff-body split, and the sides contributing nothing is the signature of a fully separated flow rather than a meshing artefact |

**The band is left exactly as declared and is not re-run.** Recorded here so the next sheet does
not repeat it: **a drag band must name the reference area and the shape it is being compared
against**, because a drag coefficient without its reference area is not a number. Logged as
**P48**.

### Band 5 fails in the opposite direction to the one predicted, and that is a finding

The band predicted the stator plates would **raise** C_d by at least 10 % through confinement.
They **lower** it by **12.7 %** — 0.457 in the channel against 0.523 in free stream, with a
tighter spread (±3.5 % against ±8.3 %).

**The plate is acting as a splitter, not as a wall.** It sits in the mid-plane the sled straddles,
and a splitter plate in the near wake is a textbook way of *suppressing* wake oscillation and
raising base pressure — which is exactly what the reduced spread says is happening.

**The consequence is the useful part: the free-stream figure is the conservative one.** A ground
test corrected with the free-stream C_d over-corrects by 13 %, i.e. by 0.6 mm/s, which is
comfortably inside the dispersion. **The correction should be quoted from the free case**, and
that is a conclusion the band's failure produced rather than obstructed.

### What the solver does not do, reported rather than smoothed

**The solve does not converge, and it is not supposed to.** Velocity residuals fall three orders
in the first 300 iterations and then **plateau near 5 × 10⁻² and oscillate**, which is what a
steady solver does on a massively separated bluff-body wake — the flow it is being asked to hold
still is not steady. Pressure and turbulence residuals sit near 2 × 10⁻³.

**So the drag is a windowed mean, not a reading.** Five written iterations spanning 160 SIMPLE
steps: **1.734 N ± 0.144 N, an 8.3 % peak-to-mean spread.** A single iteration would have
reported 1.601 N or 1.889 N with equal confidence, and the first attempt at this sheet did read
one iteration — 1.946 N, 12 % high. The spread is quoted with every mean in this sheet for that
reason.

**Viscous drag is bounded, not solved.** `wallShearStress` aborts in this OpenFOAM build with the
same IOstream error as `forceCoeffs`. Rather than rebuild a wall shear stress from cell-centre
gradients — a second, weaker solve dressed as a first — the viscous term is Schlichting's
turbulent flat-plate correlation over the meshed wetted area, **C_f = 0.074 Re_L^(−1/5) =
0.00501**, giving 0.344 N. It is **17.7 % of the total** and is labelled a bound everywhere it
appears. The pressure term, which dominates, is solved.

**And the drag force is integrated here, not read from a function object.** `forceCoeffs` aborts
too, so `validation/cfd/forces.py` integrates **F = ρ Σ p S_f** over the body patch directly from
`constant/polyMesh` and the solved field. That is a stronger position than the function object,
not a weaker one: every step between the solve and the coefficient is inspectable. **The first
attempt returned a negative drag** — the sign convention inverted, because OpenFOAM's boundary
normals point out of the *fluid* and therefore into the body. `forces.py` now asserts drag is
positive, since a bluff body in a uniform stream does not produce thrust.

---

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
