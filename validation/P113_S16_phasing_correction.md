# P113-S16: correct the release-timing comparator

**Corrective calculation specified 9 October 2026, after the old A21-R timing argument was identified as invalid.** This is a correction, not a retrospectively predeclared validation of A21-R.

## Scenario

At 450 km circular altitude, an unchanged host carries the same orbital state at every epoch. Release payload A at t=0 and B at t=468 s. Give A the stated tangential relative impulse and B **zero** relative impulse; this isolates the effect of a differential release state. Propagate both in a planar point-mass two-body field to one day after B's release. Compare 0, 1, 2, 10 and 16.029 m/s cases at the same absolute epoch. The 468 s interval is retained solely to test the previously published clock-only claim; it is not a validated operational cadence.

## Declared checks

1. At zero impulse, the two satellites have the same position and velocity at the second release within 1 mm and 1 µm/s. Persistent phase separation after one day must be <0.0001 deg.
2. For nonzero impulses, compare the one-day 10 m/s differential trend with the independent mean-motion estimate from the two post-impulse semi-major axes; agreement within 3 deg. The estimate is only a small-impulse trend, not a replacement for propagation.
3. Recompute the same cases with integration tolerances tightened by two orders of magnitude; endpoint phase change <0.01 deg.
4. Preserve the input state, numerical settings and all phase histories in machine-readable JSON. Graph axes must say that nonzero impulse or another relative-state change is required.

This model excludes drag, maneuvers, host recoil, launch geometry, conjunction safety and payload qualification. Differential drag and spring release need their own matched input cases before a product advantage is claimed.
