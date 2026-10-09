# P122 — Gen5 finite-force scenario sensitivity

**Evidence class: deterministic ideal-field scenarios, not measured tolerances, probabilities or a motor rating.**

P121's independently implemented depth-resolved 3-D surface-charge method is
rerun at five geometry cases. The nominal 12 mm magnet-face gap leaves only 1 mm
radial clearance on each side of the modeled 10 mm winding. Widening that gap or
offsetting the copper along the 90 mm depth changes the ideal integrated work.
The 16-node face quadrature and 25 mm station grid are taken from P121's checked
numerical convergence. These are **illustrative perturbations**, not as-built bounds.

| Scenario | Gap | Depth offset | Nominal radial clearance/side | Ideal work | Speed conversion |
|:--|--:|--:|--:|--:|--:|
| nominal 12mm gap | 12 mm | 0 mm | 1 mm | 1041.7 J | 12.448 m/s |
| gap 14mm | 14 mm | 0 mm | 2 mm | 906.7 J | 11.614 m/s |
| gap 16mm | 16 mm | 0 mm | 3 mm | 789.9 J | 10.840 m/s |
| depth offset 5mm | 12 mm | 5 mm | 1 mm | 1001.0 J | 12.203 m/s |
| depth offset 10mm | 12 mm | 10 mm | 1 mm | 961.2 J | 11.958 m/s |

A 14 mm gap changes work by -13.0% and a 16 mm gap
by -24.2% relative to the nominal geometry.
A 5 mm depth offset changes work by -3.9%
and a 10 mm offset by -7.7%.

Because the ironless model is linear, ±10% *assumed* remanence changes ideal work
to 937.6–1145.9 J.
An illustrative ±10% moving-mass range changes only the work-to-speed conversion,
giving 11.869–13.122 m/s at nominal work.
These ranges are not a statistical confidence interval; no supplier or tolerance
distribution has been selected.

![Ideal finite-force sensitivity scenarios](../figures/gen5_finite_force_sensitivity.png)

The 16.029 m/s historical periodic result remains challenged. This sweep does not
supply an achievable revised speed because current rise, commutation, thermal change,
magnet tolerances, friction and release contact remain unsolved. A provider/payload
interface and physical measurements are still required for product readiness.

Reproduce with `python analysis/gen5_finite_force_sensitivity.py`; `--check`
compares a fresh run to this JSON and prose. P121 and geometry hashes are recorded
in the result.
