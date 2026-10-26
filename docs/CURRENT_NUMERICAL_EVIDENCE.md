# Current numerical evidence — VOLLEY-G5-ACR1

**Core captured 24–25 October 2026; supplements extend through 26 October.** The [self-contained current package](../validation/acr1/README.md) is the engineering reference. Each result applies to its exact geometry, model and declared assumptions. Source locks and output hashes distinguish executed evidence from prepared inputs.

| Method | Current captured result | Boundary |
|:--|:--|:--|
| FreeCAD 1.0.0 / OpenCASCADE 7.8.1 | [Eight frozen native/STEP states](../validation/acr1/cad/release/FINAL_CAD_MANIFEST.json), [154 motion/refinement cases](../validation/acr1/cad/release/MOTION_VERIFICATION.json), [STEP readback](../validation/acr1/verification/FINAL_STEP_READBACK_SUMMARY.json) | Nominal geometry and prescribed motion; readback shares the kernel family |
| Native BOM and inertia ledger | [149.556720 kg dry represented geometry](../validation/acr1/verification/MASS_CG_INERTIA_SUMMARY.json); [7 kg separate installed allocation](../validation/acr1/analysis/RESOURCE_LEDGER.json) | Allocation has no CAD spatial assignment; no measured installed mass |
| Finite-geometry magnetic / conduction / averaged dq-source model | [Coupled release/arrest cases](../validation/acr1/analysis/COUPLED_SHOT.json), [equation and timestep audit](../validation/acr1/verification/COUPLED_SHOT_REVIEW.md) | Eighteen supported 1/2/3 m/s nominal/adverse source and inductance cases; 4.5/6 m/s investigations retain failures; no transistor switching or physical correlation |
| CalculiX 2.23 elastic chassis model | [Actual-source structural result](../validation/acr1/verification/CHASSIS_ACTUAL_REVIEW.md) and [secondary budgets](../validation/acr1/analysis/DESIGN_BUDGETS.json) | Declared mesh, linear elasticity, load/material/tolerance assumptions; no environmental qualification |
| Deterministic custody state specification | [Interlock source and results](../validation/acr1/analysis/TRANSFER_INTERLOCKS.json) | Missing-proof/fault logic; no measured sensor or hardware reliability |
| SciPy targeting and Orekit 13.1.6 replay | [Synthetic twelve-release mission](../validation/acr1/mission/MISSION_REPORT.md), [nine native replays](../validation/acr1/mission/NATIVE_REPLAY_CHECKS.json) | Shared fixed-axis J2, point releases and declared policies; numerical agreement is not physical delivery precision |

The mission includes the current 156.556720 kg device mass. Its tested preplanned targets show no propellant or initial wet-mass advantage over the ideal ground-pretrimmed spring comparator. No global optimization or unique inflight-retasking benefit is established.

## Extended analyses and first-test definition

Separate supplements extend the ACR1 reference without altering its accepted CAD, source model or ED1 document bytes.

| Study | Result and source | Applicable interpretation |
|:--|:--|:--|
| Structural dynamics, SD01 | [Native modes, finite forcing and normal-reaction report](ACR1_STRUCTURAL_DYNAMICS.md) | Forty elastic modes; conditional finite-load clearance and phase-dependent sustained-force limits |
| Local release and arrest | [42 native MuJoCo runs and refinement](ACR1_RELEASE_DYNAMICS.md) | Nominal local egress, contact sensitivities and keeper-catch behavior for the represented surfaces/history |
| Environment and source derating | [Coupled radiation/conduction, repeated duty and voltage variant](ACR1_THERMAL_ENVIRONMENT.md) | Declared thermal interfaces and electrical configuration control the usable temperature envelope |
| Finite-host lunar programme | [Campaign, covariance, native lifetimes and disposal](PROGRAMME_STUDIES_ACR1.md) | Same-source geometry/resource flowdown with explicitly separate lunar orbit and host assumptions |
| Partial-occupancy missions | [Two/four-payload finite-force study](../validation/acr1_partial_occupancy/REPORT.md) | Twenty-eight new candidate trajectories and seventeen native Orekit replays; full retained hardware, same-size 3U surrogates and frozen target subsets |
| Subsequent Gen6 first measurements | [Procedure, provisional STEP, instruments and predeclared criteria](ACR1_FIRST_TEST_PACKAGE.md) | Unfunded pre-test engineering definition; templates contain no measured data |

## Reproduce and inspect history

[Portable examples, dependencies and identity checks](../validation/acr1/README.md#reproduce-a-short-example) · [Raw supplement availability](../validation/acr1/SUPPLEMENT_ASSETS.json) · [Pre-ACR1 solver index](CURRENT_NUMERICAL_EVIDENCE_PRE_ACR1_2026-10-23.md) · [Immutable original Gen5 boundary](SOLVER_EVIDENCE_BOUNDARY.md)

Original Gen5, FM08, Chrono contact and earlier orbital captures retain their original numerical findings and limits. The unconverged historical Chrono model provides no accepted final-pose or peak-contact-load rating for ACR1. Native FEMM/Elmer, selected-source switching simulation, full installed-spacecraft dynamics and measured atmospheric lifetime retain their own model and correlation requirements. The supplements above identify the actual added methods, results and applicable boundaries.

## Higher-speed design constraints

The separate [unchanged-configuration screen](HIGHER_SPEED_DESIGN_SPACE.md) contains22 higher-target cases and4 timestep refinements. It establishes source/arrest design constraints and a distinct Gen6 flyaway-shoe trade. Current ACR1 command points remain1,2 and3m/s. Requested speeds and hypothetical altered configurations are not operating ratings.
