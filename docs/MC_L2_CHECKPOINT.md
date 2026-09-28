# MC-L2 requirements checkpoint — 25 September 2026

Adityavardhan Mishra

## Delivered

- P92-S6: twenty geometric spring screens, 81 unchanged release corners,
  162 ideal catcher integrations and nine charger sensitivities. Original limits
  retained. Spring material/strength, fatigue and supplier selection are open.
- MC-L2-B0 draft bench article record, component ledger, assembly/inspection and
  instrumented procedure; twenty-shot measured-data acceptance evaluator.
- P92-S6-R1: 200 mm gate spacing closes the calculated uncertainty budget.
  Original 100 mm failure preserved; physical calibration remains unperformed.
- N6: 900 installed-burden sensitivities, with losses retained and missing actual
  masses explicitly unknown. No cost or matched-mission benefit claim.
- C0-S3: lunar lifetime/coverage validation contract. Numerical execution blocked
  by gravity/ephemeris access and missing mission inputs.
- Local generated companion payloads synchronized without changing their authored
  manuscripts. New engineering remains unpublished.

## Verification and its limits

Fourteen targeted tests pass: six new evaluator tests plus eight existing S5/S11
continuation tests. New component, instrument and installed-trade reproducibility
checks pass. Links, authorship, site routes, public surfaces and companion
freshness pass. Lunar visual artifact/data and UI-logic checks also pass; this
checkpoint did not repeat the earlier live-browser test.

The full offline gate returned failure. The current runtime is NumPy 2.3.5,
SciPy 1.17.0, Matplotlib 3.10.8 and CadQuery 2.7.0, versus repository pins
2.4.6/1.17.1/3.11.1/2.8.0. magpylib and pymsis are missing; pytest/hypothesis are
missing, so the optional broad test suite is skipped. An attempted installation
could not resolve magpylib. Four inherited SVG reproduction checks differ and
historical Gen5/Gen6 CAD rebuilding differs. These differences remain unresolved;
version mismatch is a plausible cause, not a proved diagnosis. No gate or artifact
was changed to hide them. The working tree stayed clean after the full run.

Exact outputs: [full verification](../validation/logs/2026-09-25_full_verification.txt)
and [targeted verification](../validation/logs/2026-09-25_targeted_verification.txt).

## Next closure work

1. Restore the pinned analysis/CAD/test environment and diagnose inherited SVG/
   CAD reproduction differences before treating the whole repository as green.
2. Replace spring geometry screening with supplier/material evidence and reviewed
   strength/dwell/fatigue results. Select guide, latch, charger coupling and a real
   catcher force law. Native CAD, controlled drawings and populated BOM follow.
3. Obtain host/payload ICDs and real control authority; extend finite-duration
   burns to the evolving complete manifest with uncertainties and clearance.
4. Obtain archived gravity, orientation and ephemeris data; run C0-S3. Define
   useful payload coverage and an epoch-targeted arrival before mission credit.
5. Independently review and assemble the named coupon, calibrate instruments,
   measure friction/force law and perform the approved characterization. No
   physical test or manufacturing release is implied by this checkpoint.

BOLLEY retains its failed actual-field disposition. Nothing here changes that
branch's geometry, drive/thermal validity or powered-coupon status. Earlier
missing revisions remain unrecovered and are not counted as current evidence.
