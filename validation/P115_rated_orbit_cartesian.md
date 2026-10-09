# P115 — rated 450 km orbit geometry cross-check

**Run:** 9 October 2026. **Disposition:** pass for the *instantaneous two-body orbit geometry only*; lifetime and mission delivery remain open.

The [standalone Cartesian propagator](../analysis/rated_orbit_independent.py) reads the exact rated `shot.v_exit` from [`motor_results.json`](../analysis/results/motor_results.json), whose SHA-256 is recorded in its [result JSON](../analysis/results/rated_orbit_independent.json). It does not import `astro.py` or call its `boosted_elements()` method. At the stated 450 km circular reference orbit it integrates the post-release state for two periods using adaptive DOP853, recovers semi-major axis from Cartesian specific energy, checks conservation and repeats at two solver tolerances. It compares the recovered axis with the independent vis-viva identity and the manuscript's rounded 28.8 km claim.

| Quantity | Result |
|:--|--:|
| Input prograde release impulse | 16.029 m/s, model output, not measured |
| Immediate semi-major-axis rise | **28.800775 km** |
| Perigee / apogee altitude | 450.000 / 507.602 km |
| Period increase | 35.564 s |
| Maximum two-orbit semi-major-axis drift | $1.3\times10^{-8}$ m |
| Coarse/fine tolerance axis difference | below printed precision; exact value in JSON |
| Numerical acceptance band | 0.02 m for solver and identity checks |

The [impulse sweep figure](../figures/rated_orbit_crosscheck.svg) includes 0, 1, 2, 5, 10, 16.029 and 20 m/s reference impulses. The sweep is an orbital geometry response, **not** a validated Gen5 command range. This check corroborates the immediate two-body 28.8 km result. It does not rerun the drag lifetime model, validate the 1.60 lifetime multiplier, model a finite release burn, account for host manoeuvres, prove twelve-payload delivery or establish provider compatibility. The older GMAT run is at another operating point; it cannot be relabelled as a current rated-case GMAT check.

Reproduce with `python3 analysis/rated_orbit_independent.py` from any working directory after installing `numpy`, `scipy` and `matplotlib`. The script fails if its numerical consistency band or rounded headline value is not met.
