# Lunar release authority and payload-size screen

Generated from `analysis/lunar_release_scaling.py`. **Concept requirements only: no lifetime, selected carrier or flight performance is established.**

126 finite-host release cases and 42 payload-size cases are retained. Negative signed speed means repointing the carrier. It does not mean firing backwards through the same cell.

## Lunar geometry: 4 kg payload, 300 kg retained host

| Staging altitudes (km) | Release apsis | Relative speed (m/s) | Payload perilune (km) | Payload apolune (km) | Host recoil (m/s) |
|---|---|---:|---:|---:|---:|
| 100 x 100 | periapsis | -4.569852 | 79.849 | 100.000 | 0.060130 |
| 100 x 100 | periapsis | 0.000000 | 100.000 | 100.000 | -0.000000 |
| 100 x 100 | periapsis | 4.569852 | 100.000 | 120.432 | -0.060130 |
| 100 x 100 | apoapsis | -4.569852 | 79.849 | 100.000 | 0.060130 |
| 100 x 100 | apoapsis | 0.000000 | 100.000 | 100.000 | -0.000000 |
| 100 x 100 | apoapsis | 4.569852 | 100.000 | 120.432 | -0.060130 |
| 100 x 1000 | periapsis | -4.569852 | 100.000 | 965.899 | 0.060130 |
| 100 x 1000 | periapsis | 0.000000 | 100.000 | 1000.000 | -0.000000 |
| 100 x 1000 | periapsis | 4.569852 | 100.000 | 1034.705 | -0.060130 |
| 100 x 1000 | apoapsis | -4.569852 | 77.068 | 1000.000 | 0.060130 |
| 100 x 1000 | apoapsis | 0.000000 | 100.000 | 1000.000 | -0.000000 |
| 100 x 1000 | apoapsis | 4.569852 | 123.252 | 1000.000 | -0.060130 |
| 100 x 10000 | periapsis | -4.569852 | 100.000 | 9645.768 | 0.060130 |
| 100 x 10000 | periapsis | 0.000000 | 100.000 | 10000.000 | -0.000000 |
| 100 x 10000 | periapsis | 4.569852 | 100.000 | 10374.544 | -0.060130 |
| 100 x 10000 | apoapsis | -4.569852 | 43.619 | 10000.000 | 0.060130 |
| 100 x 10000 | apoapsis | 0.000000 | 100.000 | 10000.000 | -0.000000 |
| 100 x 10000 | apoapsis | 4.569852 | 157.624 | 10000.000 | -0.060130 |

Releasing near perilune principally changes apolune in this collinear screen; near apolune it principally changes perilune. A small perilune margin is sensitive to the sign and error of an apolune release. These geometric ellipses are not demonstrated frozen lunar orbits.

## Carrier responsibility

Ideal impulsive Earth departure from 300 km circular altitude: **3106.4 m/s** to a geocentric ellipse reaching the reference lunar distance. It is not a lunar encounter solution. The separately assumed arrival speeds below are not predictions of that Earth ellipse.

| Staging altitudes (km) | Assumed arrival v-infinity (m/s) | Capture impulse (m/s) | Later circularization at 100 km (m/s) |
|---|---:|---:|---:|
| 100 x 100 | 800 | 811.2 | 0.0 |
| 100 x 100 | 1000 | 883.8 | 0.0 |
| 100 x 1000 | 800 | 657.7 | 153.5 |
| 100 x 1000 | 1000 | 730.3 | 153.5 |
| 100 x 10000 | 800 | 296.6 | 514.6 |
| 100 x 10000 | 1000 | 369.2 | 514.6 |

Capture and orbit reshaping are carrier burns. A few m/s release cannot turn the high ellipse into the 100 km circular orbit. The carrier must first approach the payload’s useful orbit. Progressive burns need a finite-thrust trajectory, restart/endurance and loss budget; subdividing an impulse is not equivalent automatically.

The JSON includes rocket-equation fractions at assumed 220/320 s Isp and a separately assumed 200 m/s allowance. That allowance is not an end-of-life solution. No provider, engine, tank, dry mass or leftover propellant is credited.

## Size scaling at the current study speed

| Payload (kg) | Retained host (kg) | Relative speed (m/s) | Ideal relative energy (J) | Host recoil (m/s) | Fixed-frame peak force at 3 g (N) |
|---:|---:|---:|---:|---:|---:|
| 1 | 300 | 4.569852 | 10.41 | -0.0152 | 29.42 |
| 4 | 300 | 4.569852 | 41.22 | -0.0601 | 117.68 |
| 12 | 300 | 4.569852 | 120.48 | -0.1758 | 353.04 |
| 25 | 300 | 4.569852 | 240.96 | -0.3515 | 735.50 |
| 50 | 300 | 4.569852 | 447.50 | -0.6528 | 1471.00 |
| 100 | 300 | 4.569852 | 783.13 | -1.1425 | 2941.99 |
| 250 | 300 | 4.569852 | 1423.88 | -2.0772 | 7354.99 |

The finite-host energy omits the retained pusher, friction, spring preload and conversion losses. Fixed-frame stroke bounds use the relative speed as the large-host limit: constant force u²/(2a), zero-end-preload linear spring u²/a. Neither is a component selection. Large satellites require attachment-ring/pallet load paths and synchronized force application, not enlarged CubeSat rails.

## Verification

| Check | Result |
|---|---|
| apsidal_reconstruction | PASS |
| capture_energy_sign | PASS |
| case_counts | PASS |
| independent_propagation | PASS |
| invalid_mass_rejected | PASS |
| kinetic_energy | PASS |
| momentum | PASS |
| relative_speed | PASS |
| rocket_equation_limits | PASS |
| tighter_propagation | PASS |
| work_identity | PASS |
| zero_release | PASS |

Independent Cartesian propagation checks three opposite-apsis states, including extreme releases; tighter reruns and energy/momentum/work limits are retained in JSON. Physical stability and useful lifetime remain untested.

[Predeclared criteria](../validation/C0_S1_lunar_release_scaling.md) · [Full results](../analysis/results/lunar_release_scaling.json) · [Lunar programme](LUNAR_VOLLEY_CONCEPT.md)

Sources: [JPL astrodynamic parameters](https://ssd.jpl.nasa.gov/astro_par.html), [NASA Moon facts](https://science.nasa.gov/moon/facts/). Radii and scenario choices are declared assumptions in the run sheet.
