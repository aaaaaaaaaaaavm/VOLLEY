# C0-S1: lunar release and payload-size feasibility screen

Adityavardhan Mishra · 2026-09-17

Commit these criteria before creating or executing the implementation. This is
an early requirements screen, not the full lunar programme or a flight design.

## Declared question and inputs

Can the existing few-metres-per-second release study meaningfully trim lunar
orbits without being mistaken for lunar transfer/capture propulsion? What grows
when the payload mass grows? Retain every tested case, including surface-crossing
or unbound results. No orbital lifetime or frozen-orbit claim is permitted.

Use two-body point-mass dynamics, impulsive collinear separation and exact finite
payload/retained-host momentum partition. Lunar GM = 4902.800118 km^3/s^2 and
Earth GM = 398600.435507 km^3/s^2 from JPL DE440's astrodynamic parameter page.
Use spherical lunar radius 1737.4 km and Earth radius 6378.137 km as declared
engineering reference assumptions, not terrain. Earth-Moon distance 384400 km
is a reference distance, not an ephemeris or encounter solution.

Lunar staging altitudes: 100 x 100, 100 x 1000 and 100 x 10000 km. Evaluate both
apses, retaining the duplicate circular-limit cases as checks. Payload = 4 kg;
retained host = 100, 300, 1000 kg; signed relative release speed = -4.569852054443217,
-2, -0.5, 0, 0.5, 2, 4.569852054443217 m/s. Negative requires carrier repointing;
there is no assumed reverse firing through a cell. Total: 126 release cases.
Record payload and carrier elements, momentum/energy residuals, and separate
bound/above-reference-surface classifications. A geometrically bound result is
not a mission pass.

Compare same-perilune transfers to a 100 km circular orbit using vis-viva.
Screen an ideal impulsive Earth departure from 300 km circular altitude to an
ellipse with apogee at the reference lunar distance. Separately ASSUME lunar
arrival v-infinity of 0.8 and 1.0 km/s and compute capture into the three staging
ellipses. These are not one connected Earth-Moon trajectory. Tabulate rocket
equation propellant fractions at assumed Isp 220 and 320 s; no engine selection,
dry-mass closure or low-thrust equivalence. Add a separately labelled 200 m/s
contingency/disposal allowance only as sensitivity, not a disposal solution.

Payload-size screen: 1, 4, 12, 25, 50, 100, 250 kg; relative speed 0.5, 2 and
4.569852054443217 m/s; retained host 300 and 1000 kg. Record finite-host momentum
and energy (42 cases). Show fixed-frame, massless-pusher stroke lower bounds at
3 g and 10 g and distinguish constant-force from zero-end-preload linear spring
(twice the ideal stroke). These are study accelerations, not payload ratings.
No cost, mass efficiency, supplier readiness or scalable flight design is inferred.

## Numerical acceptance, frozen before execution

- Exact case counts and finite inputs/outputs; nonpositive mass rejected.
- Separation momentum residual <= 1e-8 kg m/s; relative speed <= 1e-10 m/s.
- Added total kinetic energy equals 0.5*reduced_mass*u^2 within 1e-5 J,
  allowing subtraction of large orbital kinetic energies.
- Zero release reproduces each staging pair within 1e-3 m in apsidal radii.
- Circular speed/period and vis-viva agree with direct energy/angular momentum
  element reconstruction; apsidal-radius residual <= 1e-3 m.
- Independent Cartesian DOP853 propagation of the 100 x 1000 km staging orbit
  at zero and both extreme releases (300 kg host) reaches the opposite apsis
  after a half period within 0.1 m and 1e-4 m/s of the element solution.
  Tightening tolerance must change position < 0.01 m and velocity < 1e-5 m/s.
- Fixed-frame constant-force work and spring work reproduce commanded kinetic
  energy to relative 1e-12; linear-spring zero-preload stroke is twice the ideal.
- Negative/zero burn rocket-equation limits and capture energy signs checked.
- Require exact stored inputs, cases, classifications and source hashes; numerical
  JSON rerun tolerance 1e-9 relative/1e-7 absolute, generated text exact from stored
  data. All verification booleans must be true. Do not widen these bands after a
  failure; record and investigate the cause.

## What this cannot establish

Lunar harmonic gravity, Earth/Sun perturbations, epoch/orientation, navigation
covariance, radiation pressure, terrain clearance, useful lifetime, collisions,
capture burn execution, thrust/restarts/boil-off, thermal endurance, payload
communications/attitude control, and both carrier/payload disposal remain open.
No source in this study authorizes a provider interface or a flight mission.

Sources: https://ssd.jpl.nasa.gov/astro_par.html ;
https://science.nasa.gov/moon/facts/ (accessed 2026-09-17).
