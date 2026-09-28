# P113-S12: evolving twelve-payload finite-burn screen

Adityavardhan Mishra · 26 September 2026

Frozen before implementation. Extend S11's planar two-body model to twelve
successive 4 kg payloads, a 300 kg dry host and 10 kg initial propellant (358 kg
initial total). Retain 220 s Isp, 2 kg reserve, 100 m/s per-burn limit, 450 s
per-burn duration, 0.5 deg/s slew rate, 0.05 deg/s² acceleration, 30 s settling,
and 10 m / 0.01 m/s terminal-state bands. This is an assumed reference manifest,
not a customer mission or physical attitude-control qualification.

Release payload i at 1200*i seconds, i=1..12, into the 450 km circular orbit
leading the original host by 5*i km of arc. Evaluate all deliveries at 18000 s.
Compare fixed 1 and 2 m/s release speeds at 1, 10 and 100 N thrust, without
changing times or targets between those six cases. Hold installed dry mass equal
only as a controlled sensitivity; do not infer an installed architecture winner.

Plan two fixed-inertial-direction burns per interval with mass flow and finite
host recoil. Carry actual retained state, mass and final release attitude into
the next interval. First attitude alone may be pre-positioned. Include initial,
inter-burn and final slews with settling; burns may not overlap. Seed with a
bounded impulsive transfer and use S11's three direction offsets (0,+0.05,-0.05),
at most 120 evaluations each. Keep all attempts. Stop a nominal campaign at the
first unaccepted delivery, retain that failure, and report remaining manifest
items unserved. A failed bounded search is not a proof of infeasibility.

For each completed nominal manifest, replay its fixed command schedule for all
64 signed corners of initial x/y position (0.1 m), initial vx/vy (0.0001 m/s),
shared release-speed error (0.0005 m/s) and shared release-angle error (0.005 deg).
No probability, covariance, navigation replan or robustness outside those corners
is implied. Carry recoil errors through every release. Report every delivery,
missed count, fuel reserve and worst terminal errors; do not drop failed corners.

Require the 120 km osculating-perigee guard at segment endpoints. This is the
inherited guard, not continuous path, plume or collision clearance. Record that
limitation explicitly. No clearance, real torque/momentum, flexible dynamics,
off-axis release, disposal or epoch-targeted lunar claim is permitted.

Numerical checks: S11 rocket/slew identities; split momentum residual <=1e-6
kg m/s; relative-speed residual <=1e-10 m/s; per-stage and total mass balance
<=1e-8 kg. Replay complete selected manifests using tighter integration and
require every terminal position change <=0.01 m, velocity <=1e-5 m/s and final
host mass change <=1e-8 kg. Preserve failure without changing these bands.
Record source hashes, runtime versions and full input assumptions. Add targeted
regressions for retained-mass accounting and initial-attitude scheduling.

## Verification extension after first campaign — 26 September 2026

The six nominal campaigns at ac7ceef complete 0/3/4/0/4/5 deliveries; none
completes twelve. Consequently the original full-manifest convergence and corner
loops execute zero times. Do not report those empty loops as positive evidence.
Replay each nonempty accepted prefix with tight integration and the same 64
corners, with identical numerical and delivery bands. Label these partial-history
diagnostics explicitly; unserved payloads still fail the complete mission. Preserve
the original result in git. Record why each impulsive seed was rejected instead
of suppressing its reserve failure. No change to targets, timing or constraints.
