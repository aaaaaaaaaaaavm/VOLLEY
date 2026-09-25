# Mission-sized mechanical cartridges

Adityavardhan Mishra · 17 September 2026

I size separate cartridges and retain the original charge, latch and acceleration limits. These are nominal force-law targets for CAD, not selected springs. A corner pass covers sampled contact/load conditions; it does not establish release-speed accuracy.

| Target (m/s) | Stroke (mm) | Stiffness (N/m) | Charge (mm) | Peak latch (N) | Speed range across corners (m/s) |
|---:|---:|---:|---:|---:|---|
| 0.5 | 20 | 1694.108 | 26.667 | 45.176 | 0.4456–0.5460 |
| 1 | 20 | 6416.430 | 26.667 | 171.105 | 0.9401–1.0626 |
| 2 | 80 | 1604.108 | 106.667 | 171.105 | 1.9030–2.1019 |
| 3 | 120 | 1594.108 | 160.000 | 255.057 | 2.8736–3.1391 |
| 5 | — | — | — | — | no candidate within frozen limits |

For moving payload+pusher mass A=m+p and retained base B, the internal reduced mass is μ=AB/(A+B). After an ideal inelastic pusher catch, the final payload/retained-host relative speed is B/(B+p)√(2W/μ). Spring work W=k(cL−L²/2)−fL. The initial spring force is kc and the net endpoint force is k(c−L)−f. The latter must remain positive.

The shortest cartridge is not automatically the smallest installed assembly. Spring solid height/free length, guidance, latch, charger and tolerances still require geometry and component evidence. At low authority the friction and charge errors consume a large fraction of useful energy. Measure these before promising a mission tolerance.

The JSON retains the 20 mm catcher accounting and marks when continued spring contact over that entire catcher stroke is invalid. Low-stroke cartridges need a separately designed shorter catch or a disengaged spring; never reuse the MC-A1 catcher number.

Verification: PASS. Twenty-five designs, 81 corners each; rejected designs retained.

[Criteria](../validation/P92_S5_mission_cartridges.md) · [Results](../analysis/results/mission_cartridges.json) · [CAD force-law ledger](../cad/current_cell/MISSION_CARTRIDGES.csv)
