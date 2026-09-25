# C0-S2: lunar mission and mechanical concept visual study

Adityavardhan Mishra · 17 September 2026

Criteria declared before implementation. This study supports lunar-first concept
review while detailed native CAD is being prepared. No hardware or lunar lifetime
gate is closed. The mechanical-cell architecture remains distinct from historical
gas Gen6. All geometry not inherited from MC-L2 is a packaging assumption.

## Question and frozen scope

Connect an ideal tangential Earth transfer screen to its implied lunar arrival
speed, then capture into 100 x 100, 100 x 1000, and 100 x 10000 km lunar orbits.
Earth departure altitude 300 km; circular coplanar Moon at 384400 km. Use JPL DE440
GM Earth 398600.435507 and Moon 4902.800118 km^3/s^2. Reference radii 6378.137 and
1737.4 km. At the transfer ellipse apogee use the difference between circular Moon
speed and transfer speed as v-infinity. This patched-conic screen neglects finite
sphere-of-influence geometry and is not an epoch-targeted encounter solution.

Report departure, arrival, capture and optional circularization separately.
Use Isp 220/320 s, retained dry carrier 300 kg, payload 4 kg and manifests 1/4/12.
Keep 200 m/s post-capture reserve as an assumed budget allowance, not a disposal
trajectory. Calculate both launcher-supplied departure and carrier-supplied
departure, with payload retained throughout this sizing screen. No thrust,
restart, tank, dry-mass iteration or engine qualification claim.

Release screen: each of three staging orbits, both apses, relative speeds
-3/-2/-0.5/0/0.5/2/3 m/s, 300 kg retained host and 4 kg payload: 42 cases.
Momentum partition includes host recoil. Report payload and host apsides.
Propagate the nominal 100 x 1000 km perilune +2 m/s case for one original period.
No lifetime, clearance probability, stable formation or frozen-orbit claim.

Create named concept solids for MC-L2 single cell, four-cell bank, lunar carrier
with four-cell bank, and larger-payload pallet. Units mm, +X departure; MC-L2
stroke 80 mm, catch envelope 20 mm, payload proxy 340.5 x 100 x 100 mm. The
300 kg dynamical carrier is unrelated to the placeholder solids' volume.
Keep spring force targets separate from illustrative spring geometry. Use distinct
colors for payload, structure, release path, charger and carrier services.

## Numerical and artifact checks

- Exactly 42 release cases and 18 mass-budget cases (3 orbits x 2 Isp x 3 manifests).
- Momentum residual <= 1e-8 kg m/s; all zero-release apsides within 1e-3 m.
- Capture plus same-perilune circularization equals direct circular capture
  within 1e-9 km/s. Rocket-equation reconstruction relative residual <= 1e-12.
- Independent Cartesian DOP853 integration vs conic position at half-period:
  <= 0.1 m; tighter integration changes endpoint <= 0.01 m. Relative energy
  drift <= 1e-9. All comparisons use consistent km/s units.
- Every STEP shape valid with positive volume; STEP reimport bounding box lengths
  agree within 1e-4 mm. These checks do not imply interference-free mechanisms.
- All plotted numerical data come from the saved result; source/criteria hashes
  recorded. No generated statistic may be labelled measured or qualified.
- Local website visual controls operate without external scripts; readable mobile
  layout, labelled axes/units, visible concept/assumption limits and static fallbacks.

Record failures before repairs; preserve original result and source if numerical
bands fail. Do not loosen bands. External contextual sources: JPL astrodynamic
parameters https://ssd.jpl.nasa.gov/astro_par.html and NASA CAPSTONE mission
https://www.nasa.gov/mission/capstone/ (accessed 17 September 2026).
