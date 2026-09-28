# C0-S3A: archived gravity ingestion and independent force check

Adityavardhan Mishra · 26 September 2026

This prerequisite does not replace the C0-S3 lifetime/coverage contract. The full
GRGM1200A table has now downloaded. Archive its SHA-256, byte count, URL and PDS
label, plus an exact byte-prefix through degree/order 200. Require complete,
unique triangular degree/order coverage and finite coefficients. Use the table
header's own radius and GM together with those coefficients; retain any label
metadata discrepancy explicitly rather than silently substituting a constant.

Implement a separate 4-pi normalized Legendre recurrence for gravitational
potential and a five-point Cartesian derivative (0.1 km step, repeat at 0.05 km).
Compare its acceleration against SHTOOLS MakeGravGridPoint at twenty deterministic
off-axis points, ten each at radius 1838 and 2738 km, evenly spread longitudes and
latitudes from -75 to +75 degrees. Test degree/order 100, 150 and 200. Require
relative vector error <=1e-8 at every point and both derivative step sizes; do
not relax on failure. Use zero rotation rate so no centrifugal term is included.
Check degree-zero acceleration against the analytical central field <=1e-10
relative. Compare genuinely separate recurrence/differencing and library paths.

No orbit lifetime, lunar epoch/frame validation, Earth/Sun perturbation, surface
coverage or mission acceptance follows from these local force checks. DE430
principal-axis orientation compatibility, ephemerides, SRP bounds and all C0-S3
trajectory convergence requirements remain mandatory.
