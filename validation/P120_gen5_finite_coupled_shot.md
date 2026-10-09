# P120 — finite-force shot with assumed bank and copper branches

**Exploratory coupled model, not a selected motor rating or flight-power design.**

P118's position-dependent ideal-phase force replaces the constant historical
force in a mover/capacitor/ESR time integration. Both branches retain the old
assumed 96 V, 6 F, 12 mΩ source, 95% converter, 200 W auxiliaries and 0.9×140 kA/m
sheet current. One branch energizes the full 1.3 m winding as the historical shot
does; the other uses a hypothetical 0.34 m active copper length. Neither branch
specifies real switching, device ratings, selected cells or winding segmentation.

| Assumed energized length | Exit speed | Gross capacitor draw | Copper heat | Peak bank current | Time |
|:--|--:|--:|--:|--:|--:|
| 1.30 m | 12.448 m/s | 2098.6 J | 927.3 J | 208.2 A | 176.2 ms |
| 0.34 m | 12.448 m/s | 1394.4 J | 242.5 J | 162.8 A | 176.2 ms |

The full-winding branch ends at 92.28 V and its bank energy
ledger residual is 0.00000 J. Halving the time step
changes its speed by 0.0000 m/s and gross
draw by 0.11 J. The electrical result is
conditional on a bank and converter with no supplier-backed implementation.

![Finite-force bank and speed histories](../figures/gen5_finite_coupled_shot.png)

The old 16.029 m/s, 2.782 kJ, 47 J regeneration, brake duty and 0.0274 m/s
dispersion must not be reused as outputs of this finite-force run. This model does
not calculate the release-contact state, new brake entry or mission closure.

Reproduce with `python analysis/gen5_finite_coupled_shot.py`; run with
`--check` to compare the report and JSON to a fresh calculation.
