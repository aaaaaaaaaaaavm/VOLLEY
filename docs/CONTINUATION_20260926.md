# Engineering continuation — 26 September 2026

Adityavardhan Mishra

## What this checkpoint establishes

The pinned analysis, verification and CAD environment is restored. The inherited
SVG, historical CAD and missing-package failures recorded on 25 September clear
under NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.1 and CadQuery 2.8.0. The first
pinned run passes the inherited scientific checks and 168 tests. Its companion
check correctly fails after new criteria are committed; exports are refreshed
only after this checkpoint is committed. No prior failure log is overwritten.

P113-S12 extends the planar finite-burn model to an evolving twelve-payload
manifest, including initial, inter-burn and final attitude transitions, propellant
use, finite-host recoil and retained state. The reference starts at 358 kg: 300 kg
dry host, 10 kg fuel and twelve 4 kg payloads. It uses matched release times and
targets for fixed 1/2 m/s separation at 1/10/100 N thrust.

**All six full-manifest searches fail.** Successful delivery counts are 0/3/4
at 1 m/s and 0/4/5 at 2 m/s. The low-thrust cases miss the first delivery at the
450 s burn ceiling. Later failures include terminal misses/reserve violations
and unavailable reserve-feasible impulsive seeds. These are bounded searches,
not proofs that another control or schedule cannot work. Unserved payloads are
retained in the mission denominator. No architecture advantage is established.

The four accepted prefixes were replayed at all 64 signed error corners each.
Only 16/16/24/24 corners retain all prefix deliveries within the unchanged terminal
bands. Worst sampled terminal position errors are about 28.3 to 31.8 m, above the
10 m limit. These counts are not probabilities. Tight integration changes terminal
position by at most 0.000876 m and velocity by less than 1e-6 m/s; bookkeeping and
momentum checks pass. No complete twelve-payload trajectory was verified.

C0-S3A acquires the complete 88,059,844-byte GRGM1200A table, records its hash, and
archives the exact degree/order-200 prefix, label and source manifest. A separate
normalized Legendre potential with Cartesian differencing agrees with SHTOOLS at
120 comparisons, worst relative vector error 3.471e-11 against a 1e-8 limit.
The table-header GM differs from the label's metadata; both values are preserved.
This check uses the table-header GM and is not a lunar lifetime result.

## Decisions and remaining dependencies

- Keep MC-L2-B0 as the current mechanical coupon planning package. Existing spring
  geometry, loads, instrument revision and procedure are retained. A supplier
  material/strength/dwell/fatigue review, selected guide/latch/charger/catcher,
  measured friction and force law, and native CAD/drawings/BOM are still required.
- Do not accept the present full manifest or claim robust delivery. Allocate real
  host thrust, torque/momentum, navigation and mission schedule before another
  campaign. Assess feedback replanning, continuous clearance and installed mass;
  do not enlarge the propellant budget or relax terminal bands merely to pass.
- Continue the lunar branch from the archived force model, not the ideal explorer.
  DE430-compatible orientation, Earth/Sun ephemerides, independent trajectory
  checks, 100/150/200 convergence, SRP bounds, surface events and event-refined
  coverage remain open. A real target, useful-coverage limits, arrival epoch,
  payload covariance and disposal requirement remain unallocated.
- BOLLEY A6j-R2/A6k stays rejected for powered-coupon promotion. The existing stop
  decision remains in force: a geometry change must address both failed field
  bands before drive/thermal hardware promotion. No repeated same-geometry solve
  or inherited field pass is used to claim closure.
- Independent review, physical instrument calibration, assembly and measured shots
  remain necessary. None is replaced by these calculations.

New engineering is committed locally. The previously authorized visual site is
separate; this checkpoint does not claim a new GitHub publication or deployment.

[Manifest results](MANIFEST_FINITE_BURN.md) ·
[Gravity validation](LUNAR_GRAVITY_VALIDATION.md) ·
[Component and bench checkpoint](MC_L2_CHECKPOINT.md)

## Final verification receipt

At flagship faebb37 the complete offline gate exits zero, all checks pass, 174
properties/regressions pass, and the tracked working tree stays clean. Exact output
is retained in [the integrated log](../validation/logs/2026-09-26_integrated.txt).
The later packaging-only change includes core, test and CAD dependency pins in
the thesis export; previously that package shipped analysis/CAD without those
files. The final export is checked against every manifest source by byte hash.
All 17 authored/non-generated companion files checked before export remain
unchanged. No engineering acceptance band was relaxed. Computational checks
passing does not change the six failed full-manifest outcomes.
