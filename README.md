# VOLLEY

VOLLEY investigates a host-mounted system that releases multiple ordinary CubeSats sequentially, using one reusable launch path and a loading mechanism. The intended benefit is a commanded relative departure speed for each spacecraft. Avoiding a propulsion unit or special powered interface on each payload remains an objective subject to payload and provider review.

**Gen6 is in development. No mechanism, speed range or flight configuration has been selected or validated.** The earlier independent mechanical-cell bank and the gas-guide layout are unselected studies. Neither establishes the shared reload path, low spent mass or broad shot-to-shot speed control sought for VOLLEY.

The [September 2026 engineering record correction](docs/REPAIR_NOTICE_2026-09-28.md) explains why the former selection was withdrawn and which questions remain open.

Nothing in this project has been built, fired, measured, qualified or flown. The calculations and CAD are studies under stated inputs, not product specifications.

## Design question

The launcher would accept a CubeSat, retain it safely, command its departure condition, release it, and repeat with the next CubeSat. The loading, jam recovery, retention, pusher arrest, payload contact and host interfaces have not been demonstrated. The physical lower and upper speed limits are open. The requested 1–2, 30–40 and approximately 100 m/s examples are points for investigation; none is an established common-hardware capability.

For a 4 kg payload, the ideal kinetic energy is 2 J at 1 m/s, 1,800 J at 30 m/s, 3,200 J at 40 m/s and 20,000 J at 100 m/s. At a hypothetical constant 10 g, 100 m/s needs about 51 m of acceleration distance. Real peak contact load, drive loss, feeder mass and host packaging make the problem harder. No universal CubeSat acceleration rating authorizes any of these points.

## What the record establishes

- [Gen5](docs/GEN5_CLOSURE.md) is a frozen electromagnetic *model* with a magazine concept, not a physical performance baseline. Its calculated 16.029 m/s and 126.6 kg are specific to that old configuration. The mass is not a complete installed-system comparison.
- [S4](docs/MANIFEST_TIMING.md) is a two-payload ideal mission screen. Its best sampled point near 4.57 m/s cannot set the product's maximum speed or choose its mechanism.
- [S12](docs/MANIFEST_FINITE_BURN.md) tested six twelve-payload screens; none delivered the full manifest, and the best tested case delivered 5/12. These bounded failures do not prove every possible mission infeasible, but they block a completed-manifest benefit claim.
- A short motor-charged spring cell is a low-speed comparator. Its electric motor charges a spring; the spring supplies the release force. It is not an electromagnetic payload drive or a reusable shared launcher.
- The historical gas guide, BOLLEY's cooperative electromagnetic interface, and ordinary spring dispensers remain separate comparators. Each requires a matched full-system and mission trade.

The [provenance](docs/PROVENANCE.md), [open problems](OPEN_PROBLEMS.md), [validation register](validation/README.md) and [programme status](docs/NEXT_GENERATION_STATUS.md) describe the evidence and unresolved conditions. Older reports and scripts remain available as configuration-specific historical calculations; their former selection language is withdrawn.

## Next decision

Compare a shared electromagnetic guide and feeder, other shared drives, small banks, the historical gas and spring studies, and a conventional dispenser under the **same** payload, host, manifest, failure assumptions and complete installed-system accounting. Require a named payload load case and host interface before claiming a velocity envelope or flight compatibility. A physical, calibrated multi-shot demonstration is needed before any performance or reliability claim.
