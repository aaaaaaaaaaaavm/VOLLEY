# Archived lunar gravity force validation — C0-S3A

Adityavardhan Mishra · 26 September 2026

The complete GRGM1200A table was downloaded (88,059,844 bytes) and hashed. An exact degree/order-200 prefix and PDS label are retained with the reproducible retrieval URL. The parser validates all 20,300 coefficient records through degree 200.

An independently coded normalized Legendre potential and five-point Cartesian derivative were compared against SHTOOLS at twenty off-axis points, three degree limits and two derivative step sizes: 120 comparisons. Maximum relative vector error: 3.471e-11; limit 1e-8. Central-field check maximum: 4.359e-12; limit 1e-10.

Force-check disposition: PASS. Units are km, seconds, km³/s² and km/s² consistently; no centrifugal term is included.

The coefficient header gives GM=4902.8001224453001 km³/s² and radius=1738 km. The earlier contract quoted GM=4902.80011526323 from metadata. These differ; this force check uses the table header with its own coefficients, and preserves the earlier contract. Orientation compatibility and the discrepancy must be reviewed before a mission propagation.

This validates local gravity evaluation only. No 90-day orbit, DE430 orientation, Earth/Sun perturbation, surface access, SRP bound or lunar lifetime has been validated. The C0-S3 mission gate remains open.

[Criteria](../validation/C0_S3A_gravity_ingestion.md) · [Full comparisons](../analysis/results/lunar_gravity_check.json) · [Data manifest](../validation/data/lunar/grgm1200a_manifest.json)
