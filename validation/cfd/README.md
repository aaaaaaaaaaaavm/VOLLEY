# A29: the ground-test air correction

The machine flies in vacuum. The test happens in a room. Every velocity in this repository
is computed with no aerodynamic drag, and the TRL-5 step in
[`../../docs/QUALIFICATION_PLAN.md`](../../docs/QUALIFICATION_PLAN.md) fires a mass simulator
down a full 1.5 m track at sea level. Nothing said what the air was worth.

Bands are declared in [`../A29_ground_test_air_drag.md`](../A29_ground_test_air_drag.md), committed
at `949fdf4` before this directory existed.

## Running it

```
python3 build_case.py              # writes free/ and channel/ from cad/stl + motor_model
python3 build_case.py --fine       # writes free_fine/ and channel_fine/
./run.sh free                      # blockMesh, snappyHexMesh, decomposePar, simpleFoam
./continue.sh free 400 40          # 400 more iterations, writing every 40, for the average
python3 forces.py free             # drag at the latest time
python3 evaluate.py                # the bands, and the ground-test correction
python3 report.py                  # figures/A29_cfd_report.png
```

`source /usr/share/openfoam/etc/bashrc` first, or use `run.sh`, which does it.

## What is committed and what is not

Committed: the generators, the force integrator, the evaluation, the report figure and the
result JSON. Not committed: the case directories. They are a function of `build_case.py`,
`cad/stl/*.stl` and `analysis/motor_model.py`, all of which are committed, so storing them would
be storing an output of a committed input, the same reasoning that keeps `cad/` deriving rather
than pasting (ADR-015) and that governs `validation/fem3d/`.

## Four things that had to be got right

1. The geometry is the CAD, not a box. `snappyHexMesh` meshes
   `cad/stl/VOLLEY_Sled_Gen5.stl` and `VOLLEY_Payload_3U_Gen5.stl` as generated. The meshed
   wetted area is 0.4173 m² against 0.5612 m² of raw STL surface, the difference is the
   payload, sled interface, which is interior and correctly not wetted.
2. The drag force is integrated here, not read from a function object. This OpenFOAM build
   aborts `forceCoeffs` with an IOstream error before the first iteration. `forces.py` integrates
   `F = ρ Σ p Sf` over the body patch from `constant/polyMesh` and the solved field instead, which
   is a better position: every step between the solve and the coefficient is inspectable.
3. The sign convention, which was wrong first. OpenFOAM boundary normals point out of the
   *fluid*, i.e. into the body, so the body's own outward normal is `-Sf` and the force is
   `+Σ p Sf`. The first attempt used the other sign and returned a negative drag.
   `forces.py` now asserts that drag is positive, because a bluff body in a uniform stream does
   not produce thrust.
4. The work integral is over a profile, not a constant force. The shot is
   position-scheduled, `v = v_target·√(x/L)`, so `v²` is linear in `x` and the drag force is too.
   The work is `F_max·L/2`. Taking `F_max·L` would double the answer.

## Two things this reports rather than hides

The solve does not converge, and it is not supposed to. A steady solver on a massively
separated bluff-body wake plateaus and oscillates; the velocity residuals sit near 10⁻² rather
than falling. The drag is therefore averaged over a window of written iterations, and the
spread across that window is quoted with the mean. Reading a single iteration would report a
sample of the oscillation as though it were an answer.

Viscous drag is bounded, not solved. `wallShearStress` aborts in this build for the same
reason `forceCoeffs` does. Rather than reconstruct a wall shear stress from cell-centre gradients,
a second, weaker solve dressed as a first, the viscous term is a turbulent flat-plate
correlation over the wetted area, and it is labelled as a bound everywhere it is quoted. For a
massively separated bluff body it is a small fraction of the total, and the pressure term, which
dominates, is solved.
