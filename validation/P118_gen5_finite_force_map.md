# P118 — finite Gen5 3-D integrated-force map

**Status: analytic field/geometry screen, not an independent 3-D FEM or physical validation.**
The code integrates J×B over the 162 finite stator belts using the existing exact cuboid field
and optimizes phase at every station. This is optimistic because switching, voltage, current,
friction and thermal limits are omitted. It removes the periodic-infinite-stator scaling
used for the rated shot while keeping the same magnetic material/field source.

CAD places the magnet array at 0.230–0.570 m and the declared active stator ends at 1.296 m.
After 1.066 m travel their geometric overlap vanishes,
before the rated 1.300 m acceleration travel ends. The 336 mm modeled magnetic length
differs from the 340 mm CAD envelope by 4 mm.

Finite-force ideal work: **1041.7 J**; associated
optimistic exit speed: **12.448 m/s** for
13.445 kg moving mass. Periodic rated model reports
16.029 m/s and assumes approximately
1327.9 N throughout. The finite map must not silently
replace that baseline: it is a **finding requiring model and configuration disposition**.

At 0.2 m travel, hypothetically filling the entire 8 mm belt pitch gives
1318.2 N instead of the drawn 7 mm copper belt's
1169.0 N. Thus the periodic model's continuous-sheet
assumption also masks the 1 mm insulation gap; this diagnostic is not a new winding.

Cross-sectional quadrature convergence at three stations changes force by at most 0.369%
between (3,3,5) and (5,5,7) points. Halving the 25 mm station step changes
integrated work by 0.096%. Independent FEM
remains an open check. The shared cuboid field law means agreement with the old
field is not independent validation.

![Finite force map](../figures/gen5_finite_force_map.png)

Reproduce with `python analysis/gen5_finite_force_map.py` in an environment with the declared dependencies. Inputs,
software and source hashes are in `analysis/results/gen5_finite_force_map.json`.
