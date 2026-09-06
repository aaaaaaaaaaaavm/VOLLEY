# A2-R: depth-resolved magnetic constants for the velocity levers

Declared 2026-09-06 before the new evaluator exists or runs. I retain the previous lever results as superseded evidence.

## Question and frozen acceptance

P55 identifies four geometries whose velocity trade still uses centre-plane constants. Re-evaluate each through the Lorentz integral, with no shared empirical correction factor:

- 8 mm magnets, 12 mm gap, 10 mm winding;
- 6 mm magnets, 12 mm gap, 10 mm winding;
- 5 mm magnets, 12 mm gap, 10 mm winding;
- 8 mm magnets, 22 mm gap, 20 mm winding.

Use the current 90 mm depth and 240 axial samples. Compute 9-point and 15-point depth quadrature at 9 thickness points. Each constant must be finite and positive, and the depth-quadrature difference must be at most 0.5 percent relative to the 15-point value. The baseline 9-point value must reproduce the committed motor thrust constant within 0.1 percent. All ten original lever rows must be rerun using their own geometry's 9-point constant, with unchanged mass, current, stroke and energy/ESR logic.

These are numerical consistency/convergence criteria, not new performance acceptance bands. A convergence failure remains a failure. Preserve the original table as history and publish new results separately, then update the current comparison through its generator. No mass saving, manufactured winding or independent 3-D thrust validation is implied.

## Result, 2026-09-06

Declared at commit `e0a3cf611824efe19d045cab4fc73dcdfaa7abca`. All declared consistency checks pass.

| Geometry | 9-point Kt, N per kA/m | 9-versus-15-point difference |
|---|---:|---:|
| baseline | 10.538611 | 0.002027% |
| magnet_6mm | 8.869066 | 0.002997% |
| magnet_5mm | 7.848059 | 0.003496% |
| two_layer | 6.627476 | 0.001489% |

All ten lever rows were recomputed. The thin-magnet and widened-gap corrections are geometry-specific, not a shared scale factor. See [the new result](../analysis/results/velocity_levers_depth.json) and [current trade table](../docs/DESIGN_OPTIONS_exit_velocity.md). Baseline and hardware claims remain unchanged.
