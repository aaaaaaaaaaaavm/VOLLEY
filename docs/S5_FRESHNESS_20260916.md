# S5 numerical freshness repair

CI run 35070120361 failed because `analysis/results/operational_uncertainty.json`
did not match freshly serialized output. The report and SVG were not reported stale.
The same source reproduces byte-for-byte locally with both the initial environment
and the pinned NumPy 2.4.6 / SciPy 1.17.1 dependencies. That narrows the discrepancy
to runner-dependent output, but does not identify its individual floating-point
leaves. I therefore do not claim a measured maximum runner difference.

I extend the existing S2/S3 freshness policy to S5 computed event data: 10 micrometre
position and 0.1 micrometre/second velocity floors. A central finite difference
inherits twice the relevant coordinate floor divided by its declared step. Ratio
diagnostics have a 1e-5 absolute reproduction floor; local allowances use 1e-5
relative and 1e-10 absolute floors. These compare repeated model outputs; they are
not release tolerances. Source hashes, schema, perturbation inputs, masses and all
discrete verification outcomes remain exact. Markdown and SVG must reproduce
the accepted stored numerical payload exactly.

The fresh calculation must independently pass the original S5 nominal propagation,
symmetry, step convergence, momentum and basis bands. Those bands are unchanged.
Regression tests reject changed physics, sources, verdicts, schema and presentation.
The local programme verification command now includes S5, as CI already did.

A green CI run is still required to establish that this repair resolves the observed
failure. It does not validate the model or close P113, E5 or P92.

## Runner verification and S6 follow-up

Run 35152740947 passes the repaired S5 check. Its diagnostics report 174 leaves outside
the generic primitive comparison policy, while all S5-specific reproduction and physical
verification checks pass. The same run stops at S6 freshness: its computed terminal-error
vector had inherited the generic scalar floor instead of the position/velocity floors.

S6 now uses S5's SI-aware comparison for computed state/error data, with exact study
metadata, source hashes, input half-widths, corner coordinates and discrete outcomes.
A regression accepts a 0.5 micrometre position reproduction difference and rejects a
1 micrometre/second velocity corruption, changed source, changed corner input or verdict.
The 10 m / 0.01 m/s mission bands and all nonlinear/linear verification bands are unchanged.
