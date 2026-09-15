# Mission freshness across numerical runners

The first S3 CI run, 34927959627, stopped at the earlier S2 freshness check although
the same committed source passed locally. Diagnostic run 34928298955 reported 34
S2 leaves and 718 S3 leaves outside the generic scalar reproduction tolerance.

Examples from that run:

| Quantity | Stored | Runner | Approximate difference |
|---|---:|---:|---:|
| S2 case 81, event 7, host y position (m) | 501575.2002926287 | 501575.2002932258 | 0.60 micrometres |
| S2 case 172, event 7, host y position (m) | 521938.8843038563 | 521938.8843045336 | 0.68 micrometres |
| S3 case 5, terminal position error (m) | 0.0001134847994889407 | 0.00011390616641796057 | 0.42 micrometres |

A component-relative tolerance with a 1e-9 m absolute floor was inappropriate for
an orbit whose Cartesian components cross zero. The same position discrepancy was
accepted far from an axis and rejected near it. Small norms of differences between
large coordinates also do not reproduce to arbitrary relative precision.

## Correction and limits

Use SI-aware absolute freshness floors: 1e-5 m for position components and position
error norms; 1e-7 m/s for velocity/correction vector components. These are respectively
100 and 500 times tighter than the strictest applicable S3 boundary/independent
propagation limits. Retain generic scalar rtol=1e-12, atol=1e-9 elsewhere. Retain exact
input/source metadata, schema and discrete decisions. This is a reproducibility
budget, not a change to mission or numerical verification acceptance.

Tests exercise axis crossings, the observed residual pair, a 0.01 m corruption,
a 0.001 m/s corruption, changed fuel and flipped acceptance. Reports and figures
must still regenerate exactly from the accepted stored numerical payload. Physical
verification independently checks the fresh calculation against frozen criteria.

`tools/diagnose_mission_freshness.py` reports field paths before the slower gates
when another runner disagrees. A remaining difference must be investigated; the
comparison does not round away decisions or substitute a successful check for a
physical validation experiment.
