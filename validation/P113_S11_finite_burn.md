# P113-S11: finite-burn and slew-constrained departure

Adityavardhan Mishra · 17 September 2026

I retain P113-S3's 450 km initial orbit, 300 kg dry host, 10 kg fuel, 4 kg
payload, 220 s Isp, 2 kg reserve and phase_5km terminal target at 3600 s.
Terminal acceptance remains 10 m and 0.01 m/s. Release times are 1200/1800 s;
relative release speeds are fixed 1/2 m/s. Host thrust assumptions are 1/10/100 N.
This is a planar deterministic single-payload study with a fixed inertial release
axis taken from the matching S3 impulsive solution; no navigation covariance,
body-flexibility, plume or collision closure is claimed.

Plan two constant-inertial-direction finite burns. First starts at t=0; second
ends early enough to turn to the release axis and settle for 30 s before release.
A rest-to-rest slew uses assumed maximum rate 0.5 deg/s and acceleration
0.05 deg/s^2; use triangular/trapezoidal duration, not instantaneous pointing.
First attitude is pre-positioned. Require enough time between burns to slew and
settle. Thrust magnitude is fixed and mass flow is F/(Isp*g0). Bound each burn
at 450 s and its integrated ideal impulse at 100 m/s. Keep fuel reserve and
perigee >=Earth radius+120 km at all propagated segment endpoints.

Start from S3 equivalent impulses. Compare finite-burn replay to bounded
least-squares replanning of two angles and two durations (3 declared direction
seeds: nominal, +0.05/-0.05 rad, -0.05/+0.05 rad; max 120 evaluations each).
Keep misses and service/reserve failures. No global optimum/infeasibility claim.
Numerical verification: tighter propagation changes terminal position <=0.01 m
and velocity <=1e-5 m/s for selected solutions; independent zero-gravity rocket
identity <=1e-8 m/s and mass <=1e-9 kg; zero-duration burn is identity;
finite-duration high-thrust convergence to impulse, and slew-limit identities.
Store complete attempts, constraints and source hashes. No GitHub publication.
