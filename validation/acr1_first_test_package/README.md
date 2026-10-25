# ACR1 first-test package · N5-R1

**25 October 2026 · pre-test engineering definition.** This package prepares subsequent Gen6 bench measurements after the completed ACR1 computational study. It contains a source-based magnetic coupon prediction, provisional fixture geometry, a bill of materials, assembly/inspection and calibration procedures, and numerical accept/rework/stop rules. No apparatus has been built, purchased, booked or tested by this package.

[Procedure and calibration](TEST_PROCEDURE.md) · [Printable procedure](TEST_PROCEDURE.pdf) · [Frozen criteria](ACCEPTANCE_R1.json) · [BOM](BOM.csv) · [Planned runs](PLANNED_MATRIX.csv) · [Material differences](MATERIAL_FINDINGS.md) · [Predictions](PREDICTIONS.json) · [Fixture drawing](geometry/C01_fixture_drawing.svg) · [Provisional STEP](geometry/C01_coupon_fixture.step)

| First-test scope | Useful evidence | Boundary |
|:--|:--|:--|
| C01: one-wavelength field/force coupon | Signed field, force/current and return-wire contribution | Six 8 mm blocks per side; 80 mm active conductor; not the full ACR1 motor |
| C02: one-cell slow transfer and custody | Capture before release of the previous holder; missing-proof inhibits | Fixed-level 4 kg dummy; not ground lift or launch qualification |
| C03: 0.2 m/s planar release/arrest counterpart | Keeper opening, rear unloading, low-drag egress and external-brake stop | Measured ground support and a separate bench brake; no LSM rating or six-DOF tip-off claim |

The drawing/STEP contains 53 valid provisional solids derived from controlled ACR1 block/copper dimensions and explicit new support allocations. It omits certified joints, gantry, guard, connectors and the complete C02/C03 fixtures. Geometry and a simple beam screen do not authorize assembly or energization. Actual load-path, material, guard, calibration and inspection gates remain conditions for any later experiment.

The [existing release-test specification](../acr1_release_dynamics/PHYSICAL_TEST_SPECIFICATION.md) controls the broader contact/pose question. The [legacy bench plan](../../docs/BENCHTOP_TESTS.md) and [qualification plan](../../docs/QUALIFICATION_PLAN.md) supply test-method history, not current coupon predictions or provider limits. In particular, their four-block wavelength and auxiliary eddy brake are not the ACR1 source definition.

## Inspect or reproduce

Run `python3 validation/acr1_first_test_package/check_package.py` from the repository root. It checks exact source/packet identities, source-derived arithmetic, empty data templates and provisional STEP framing. It does not run an experiment.

The magnetic prediction uses NumPy 2.4.6 and Magpylib 5.2.3 with Python 3.12, importing the unchanged [ACR1 field function](../acr1/analysis/finite_motor.py). Run `predict.py` only in a disposable copy when revising the prediction; the captured outputs and specification lock preserve the present pre-test issue. Fixture generation uses CadQuery, with the actual version recorded in [geometry checks](geometry/GEOMETRY_CHECK.json). The editable scripts accompany the neutral STEP.

[Source identities](SOURCE_IDENTITIES.json) tie the packet to the inspected parent records. [Specification lock](SPEC_LOCK.json) and [packet manifest](MANIFEST.json) identify this issue. The [header-only templates](templates/raw_timeseries.csv) and [unperformed run record](templates/run_record.json) contain no measured results. A changed article, input or limit gets a distinct issue with separate identification and validation data.

Project-created source and geometry follow the repository [license](../../LICENSE) and [notice](../../NOTICE). Manufacturer references remain factual catalog selections or requirements; no third-party document or supplier quote is redistributed here.
