# P113-S6: conditional combined release-error envelope

Declared 2026-09-16 before implementation or execution. Starting source: `682498b10b6e7182fe672b523f2eac51ddeb1ead`.

I retain the accepted S4 two-event campaign and S5 propagation, target states and 10 m / 0.01 m/s terminal bands. I ask whether simultaneous bounded errors consume those bands. This is a conditional event screen: each event begins from its stored nominal host state. It does not propagate the first event's host error into the second event's manoeuvre, and cannot close robust campaign performance.

## Frozen experiment

The six illustrative half-widths are radial and tangential common position 0.1 m each, radial and tangential common velocity 0.0001 m/s each, relative release speed 0.0005 m/s and relative release angle 0.005 degrees. These are study assumptions, not provider specifications or measured distributions. Evaluate all 64 sign corners at multipliers 0, 1, 2 and 5 for each of the two events. Retain every corner, including failures. Rotate and scale relative velocity with finite host recoil, then apply common position/velocity error to both bodies.

Direct nonlinear propagation is authoritative for the sampled corners. Compare it with the sum of S5 central vector derivatives. The sampled corners are not a proof of the continuous box's nonlinear maximum. Report the triangle-inequality bound of the local linear model separately.

## Verification and disposition, frozen before execution

- Zero-error reproduction: <=1e-6 m and <=1e-9 m/s from S5 nominal terminal state.
- Mechanism momentum residual: <=1e-9 kg m/s before the common-state offsets.
- Finite results, exactly 512 evaluated corners, unchanged target definitions and exact source hashes.
- Linear/direct agreement at multiplier 1: <=max(0.05 m, 2% of the direct position-error norm), and <=max(0.00005 m/s, 2% of the direct velocity-error norm). A failed comparison rejects linear prediction for this box; it does not discard nonlinear corners.
- Mission bands remain 10 m and 0.01 m/s. Report accepted counts and worst sampled errors at every multiplier; do not require a passing mission outcome to accept a correctly executed experiment.
- Compare the 1,800 s release gap against declared 30/60/120/300 s reserved intervals arithmetically only. No attitude settling, collision clearance or thermal-recovery model is implied.

Outputs: executable source, JSON with provenance and all cases, generated report, corruption/conservation/zero-error tests and a normal freshness gate. P113, E5 and P92 remain open regardless of this result.
