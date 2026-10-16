# P134 — independent numerical static-atmosphere lifetime screen

Run `python3 analysis/gen5_lifetime_crosscheck.py --check`. This DOP853 integration
uses orbit-averaged specific-energy and eccentricity-vector rates with midpoint
anomaly quadrature, rather than calling `astro.lifetime` or its stepping loop.
Inputs are a 450 km circular starting orbit, ballistic coefficient 61 kg/m²,
mean static exponential atmosphere and a stop at 120 km perigee. The imposed
inertial tangential speed is an input, not a physical launcher output.

The numerical acceptance band is a 0.5% maximum lifetime-ratio change after
360-to-720-node and rtol 1e-7-to-1e-9 refinement. The observed maximum is
0.000145%. The fine base lifetime is 1.303955 years. At imposed 2.5, 12.448437
and 16.029 m/s, the ratios are 1.082110, 1.451222 and 1.602165.

This reproduces the historical 1.60 ratio under the shared atmosphere. It does
not establish real lifetime, solar-activity invariance, a current GMAT/Orekit
lifetime result, host acceptability, or an achieved release speed. Atmospheric
model-form uncertainty remains unbounded by this calculation.

[Source](../analysis/gen5_lifetime_crosscheck.py) ·
[Results](../analysis/results/gen5_lifetime_crosscheck.json) ·
[Mission and interpretation](../docs/GEN5_ORBIT_AND_MISSION_DISPOSITION.md).
