# P121 — independent depth-resolved 3-D magnetic force cross-check

**Evidence class: numerical magnetic model, not 3-D FEM, measured thrust or a selected motor rating.**

The ironless, uniformly magnetized Gen5 cuboids are represented as magnetic surface
charges with density `M·n`. A separate implementation integrates the finite 90 mm
depth of each face in closed form and the short face dimension by Gauss-Legendre
quadrature, then integrates `J×B` in all 162 drawn stator belts. It does not call
magpylib for the calculated field. It shares the geometry, remanence, material law,
current sheet and ideal independent phase assumption with P118. Agreement checks
the field mathematics and finite-stator integration, not those shared inputs.

For air points, the evaluated field is `B_y = (1/4π) Σ (B_r·n) ∫∫ (y-y')/R³ dA`.
The source-depth integral uses the finite limits `−D/2` and `D/2`; it is not a
centre-plane field multiplied by depth. The winding cross-section uses (3,3,5)
Gauss nodes in belt width, gap thickness and array depth.

| Face quadrature | Ideal work | Speed conversion |
|:--|--:|--:|
| 10 | 1041.74 J | 12.448 m/s |
| 16 | 1041.74 J | 12.448 m/s |
| 24 | 1041.74 J | 12.448 m/s |

The 16-to-24-node face work change is 0.00002%; halving the 25 mm
station spacing changes work by 0.0960%.
Increasing cross-sectional quadrature from (3,3,5) to (5,5,7) changes three
sampled station forces by at most 0.369%.
Seven air-field probes, including points 0.10 and 0.50 m off the depth face,
differ from the analytic cuboid law by at most 0.00002%.

The final 3-D surface result is **1041.7 J ideal work**, equivalent
to **12.448 m/s** for the assumed moving mass.
P118's analytic cuboid integral is 1041.7 J; the work
difference is 4.35e-08%. P119's 2-D FEM omits
depth end effects and is a separate trend check. None is an achieved release speed.

![Independent 3-D surface-charge force overlay](../figures/gen5_finite_force_surface3d.png)

**Remaining decisive gates:** voltage-limited switched winding and inverter with selected
parts; force/load/contact across release and arrest; feed and retention geometry;
installed mass and a complete mission comparison. Physical validation remains unrun.

Reproduce with `python analysis/gen5_finite_force_surface3d.py` after installing
`requirements.txt`. `--check` compares regenerated numbers and prose to the captured
JSON and report. Source, geometry and reference hashes are in the JSON.
