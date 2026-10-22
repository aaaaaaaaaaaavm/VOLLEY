# Seven-feeder common-boundary development study

FDR09 compares seven four-payload concepts using two passive 1U and two passive 3U envelope surrogates and one reusable receiver. Ten native FreeCAD/STEP pairs cover seven R1 candidates, a separate lead-screw R2 correction and two insert coupons. No architecture passes all mandatory acceptance gates.

- [Engineering report and comparison](release/READ_ME.md)
- [Machine-readable comparison](release/REVIEW.json) and [BOM](release/BOM.csv)
- [Mandatory eligibility assessment](release/D27_GATES.json)
- [R2 correction and support checks](release/LEAD_TRIM_R2.json)
- [Separate STEP readback](INDEPENDENT_STEP.json)
- [Source, output and software identities](MANIFEST.json)

![Partial mass accounting for the common four-payload boundary](comparison_mass.png)

The CAD material subtotal and listed catalog options do not establish full installed mass, CG or inertia. Catalog options are unintegrated and unqualified. R2 clears only the checked nominal rectangular payload corridor and identified housing overlap; loaded support, complete carriage motion, tolerances, faults and insert custody remain acceptance requirements. R1, R2 and FM07-R6 are distinct revisions.

## Reproduction

Run `python3 check_capture.py` to verify captured source/result identities and the retained eligibility decision. Native geometry regeneration requires the recorded FreeCAD environment; commands are given in the engineering report. `python3 make_comparison_figure.py` regenerates the comparison plot using Matplotlib and the local JSON.

Separate CadQuery/OpenCascade import records cover the ten current STEP files. The importer uses the same kernel family; it is not an independent-kernel certification. Supplier reading copies remain in the private source archive. Public source records retain URLs, hashes and derived values. The original spring serialization diagnostic is preserved, with its sampled surface/bounding-box evidence and explicit 1 ppm exchange-volume criterion. That numerical criterion is separate from functional clearance acceptance.
