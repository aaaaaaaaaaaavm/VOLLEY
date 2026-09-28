# C0-S3: lunar lifetime and coverage validation contract

Adityavardhan Mishra · 25 September 2026

Freeze before implementation. No lunar lifetime or useful-coverage acceptance is
permitted from the ideal two-body release explorer. Required data: archived
GRGM1200A fully normalized coefficients (not Bouguer coefficients), DE430-compatible
Moon principal-axis orientation and Earth/Sun ephemerides; retain versions and
hashes. Model lunar gravity to at least degree/order 100 with 100/150/200
convergence studies, Earth/Sun differential third-body gravity, orientation and
surface intersection. Add solar radiation pressure and optical/area/mass bounds
before payload lifetime promotion. A force model lacking these inputs is a
baseline diagnostic only.

Screen 100x100 and 100x1000 km initial altitude orbits, inclinations 30/60/90 deg,
RAAN and argument-of-perilune phases 0/90/180/270 deg, releases 0/1/2/3 m/s with
finite-host recoil, and initial phase/epoch uncertainty. Mission horizon is a
90-day study assumption, not a customer lifetime. Surface crossing is a failed
case, not removal from the denominator. A surviving 90-day run proves survival
only under that modeled horizon and configuration; it is not infinite stability.

Before promotion, require force checks against an independent implementation,
relative acceleration error <=1e-8 at 20 off-axis points; two-body conservation
relative error <=1e-9; halved max-step changes minimum altitude <=0.1 km; increasing
gravity from 150 to 200 changes minimum altitude <=1 km over the horizon. If
convergence fails, retain failure and expand resolution without relaxing bands.
An epoch-targeted carrier arrival and actual payload covariance remain separate
prerequisites; arbitrary rotating axes must not be labeled real lunar epochs.

Coverage must state target coordinates, minimum elevation, sensor footprint,
resolution, illumination and communications restrictions. First geometric view
screen: explicitly assumed 10-degree minimum elevation at a declared lunar
surface site, event-refined rise/set times, no interval inferred merely from
coarse samples. Report longest outage and total access alongside survival;
never equate visible surface fraction with useful science or communications.
Mission-specific limits remain unallocated and block a mission acceptance.

Current acquisition attempt on 25 September 2026: the coefficient file request
failed with proxy CONNECT timeout. No coefficients or ephemerides were received.
The PDS label was read and establishes GRGM1200A reference radius 1738.0 km,
GM 4902.80011526323 km^3/s^2, fully normalized coefficients and the DE430
principal-axis frame. These metadata alone cannot substitute for the data.

Sources:
- https://pds-geosciences.wustl.edu/grail/grail-l-lgrs-5-rdr-v1/grail_1001/shadr/gggrx_1200a_sha.lbl
- https://pds-geosciences.wustl.edu/grail/grail-l-lgrs-5-rdr-v1/grail_1001/shadr/gggrx_1200a_sha.tab
- https://ntrs.nasa.gov/citations/20230010615

Disposition: BLOCKED_DATA_AND_MISSION_INPUTS; no lifetime calculation executed.
