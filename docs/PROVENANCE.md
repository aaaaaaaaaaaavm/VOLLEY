# Provenance

Publishing under a personal name requires knowing exactly what stands behind each
claim. This file records that. It is deliberately unflattering.

## Summary

Every calculation, script, figure, and document in this repository is a model output.
Nothing here has been measured. No value has been re-derived by hand or checked against a
second method unless this file says so explicitly.

There is no hardware measurement or third-party review in this project. Finite-element
structural and magnetic analyses, circuit simulation, CFD and orbit-propagation checks
do exist. They are numerical evidence, not experimental validation. The run-specific
limits below and in the validation register govern what each establishes.

## What is model output and unverified

All of the following:

- Every calculation in `analysis/` and `legacy/`
- The coilgun-to-linear-motor trade analysis and its supporting numbers
- All performance figures: thrust constant, exit velocity, efficiency, dispersion
- All astrodynamics: lifetime multipliers, seeding rates, conjunction screening
- All mass, thermal, structural, and electrical budgets
- Every figure and diagram
- The IEEE paper, all verification reports, all research summaries
- The literature review and all citation formatting

## Where a genuine cross-check exists

The independent numerical paths include:

| Claim | Evidence and limit |
|---|---|
| Halbach field | Analytic superposition versus magpylib, 2-D FEM in A1 and the A2 3-D field check. Centre-plane/midgap agreement does not independently validate the complete depth-averaged thrust integral. |
| Orbital decay | Orbit-averaged integration versus Cowell RK4 and GMAT in A5/A15. The solar-activity invariance claim failed; absolute life remains atmosphere-dependent. |
| Pulse circuit | ngspice in A8, including the bank-ESR loss the earlier analytic budget omitted. Component and switching assumptions remain unmeasured. |
| Sled structure | CalculiX A4 under the declared material, mesh and boundary conditions. It does not establish the launch qualification of a payload. |
| Aerodynamics | OpenFOAM A29 with a mesh-convergence study. This does not validate vacuum release contact or tip-off. |

See [GEN5_CLOSURE.md](GEN5_CLOSURE.md) for the frozen baseline evidence and
[COMPUTATIONAL_CLOSURE.md](COMPUTATIONAL_CLOSURE.md) for remaining work. A successful
repository consistency gate is not another independent physical check.

## Errors made and corrected during the work

Recorded because they calibrate how much to trust the rest:

1. Regenerative braking was claimed to arrest the sled. False, braking force is bounded
   by the same thrust constant as acceleration and would need more track than exists.
   Led to the eddy-brake design.
2. Abort was claimed to be available "anytime before release." False, the commit point
   is ~45 % of stroke.
3. The efficiency chain credited 55 % regeneration while the arrest architecture
   dissipates that energy in the brake. Double-counting; efficiency corrected 40 % to 32 %.
4. Two sign errors in the Halbach array convention, caught by empirically probing a
   single array rather than asserting the convention.
5. A retention gate pin was sized at margin 0.5 (inadequate); resized to two D6 pins, and then to two D9 pins in 2026-08-10 after A18 showed the quasi-static sizing case was the wrong one (P37, A22),
   margin 1.2.
6. Found while building this repo: the paper's conjunction minimum (45.3 km) and
   peak current (323 A) both belong to a superseded operating point. See
   `OPEN_PROBLEMS.md` P1 and P2.
7. The ±1.26 % force ripple is a pre-quadrature record. The current figure is ±1.01 %
   (1.0138 % unrounded) from `analysis/motor_model.py`; the 2026-08-03 quadrature correction to
   the winding-thickness integral moved it, and moved K<sub>t</sub> from 11.22 to 10.5386 N per
   kA/m with it. Three occurrences survive in dated records and are annotated in place rather
   than edited: `docs/CROSS_INDUSTRY.md`, `validation/A1_field_femm.md` and
   `docs/VALIDATION_REPORT.md`.

## Source material

Three earlier working documents, a feasibility PDF, a consolidated report, and a
strategy document, were checked against the analysis rather than trusted. They were
sources of claims to check, not sources of truth, and several of their numbers were
found to be wrong or unattributable. They are not included in this repository.

## How to cite this work honestly

This is a design study at TRL 2-3 with no experimental validation. Any publication or
presentation should say so.
