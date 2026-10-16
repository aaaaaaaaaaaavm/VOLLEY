# Solver and numerical-evidence boundary

Only executions with a declared source, input and captured result are numerical evidence. Preparing a deck, importing a package or passing a parser does not execute a native solver. The dated GMAT run and the new reparse are distinct operations.

| Tool / case | Version basis | Record | Evidence | Limit |
|:--|:--|:--|:--|:--|
| FreeCAD | 1.0 | [record](../cad/GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json) | Native B-rep census; rerun 16 Oct; failed geometry retained | Nominal solids only; no physical fit/loads |
| GMAT | R2026a | [record](../validation/gmat/evidence/A15_R1_NATIVE_CAPTURE.json) | 30 Sep execution; 16 Oct independent raw reparse | Preloaded R1 orbits; not sequential host control; no continuous COLA |
| GMAT historical | R2022a | [record](../validation/results/A5_astro.json) | Older captured decay summary, different speed input | Raw reports not available in current tree; not current 16.029 lifetime proof |
| scikit-fem / gmsh | captured version in result | [record](../validation/results/A1_femm.json) | Actual A1 solver, despite legacy filename; partial bands | Not a native FEMM execution; two field bands fail |
| Depth-resolved surface charge | Python / NumPy | [record](../analysis/results/gen5_finite_force_surface3d.json) | Independent numerical field formulation; captured outputs | Shared geometry/material/ideal phase; not 3D integrated-force FEM |
| DOP853 lifetime | SciPy 1.17.1 | [record](../analysis/results/gen5_lifetime_crosscheck.json) | New 16 Oct numerical cross-check; no historical routine import | Shared static atmosphere, no environment validation |
| Chrono | 10.x requested | [record](../docs/GEN5_UNCERTAINTY_AND_ACCEPTANCE.md) | Unrun pinned compliant-contact case | Geometry/material/preload/contact law not selected |
| Basilisk | 2.12 requested | [record](../docs/GEN6_G0_MISSION_AND_ARTICLE_REQUIREMENTS.md) | Unrun pinned host-control case | Host inertia, actuators and control authority absent |
| Orekit | 13.1.6 requested | [record](../docs/GEN5_ORBIT_AND_MISSION_DISPOSITION.md) | Unrun pinned current lifetime/campaign case | No current native evidence |
| FEMM / pyFEMM | 4.2 / 0.1.3 requested | [record](../validation/results/A1_femm.json) | Unrun pinned native case; A1 used scikit-fem | Native FEMM performance cannot be claimed |
| Elmer | 26.2.1 requested | [record](../docs/GEN5_FREEZE_READINESS.md) | Unrun pinned integrated-force/transient case | Other historical field solves do not satisfy this case |
| ngspice | 47 requested | [record](../validation/spice/emocd_shot.cir) | Historical ideal netlist/captured circuit study; new pinned selected-source case unrun | No supplier-backed winding/inverter/source closure |
| CalculiX / OpenFOAM | historical captured studies | [record](../docs/GEN5_FREEZE_READINESS.md) | Isolated historical structural/flow screens | No same-revision installed Gen5 qualification or full mesh closure |

The requested Chrono, Basilisk, Orekit, FEMM, Elmer and selected-source ngspice cases remain future validation. Their absence is a limitation of the academic study. A historical result from another input or another solver does not close them. No solver entry establishes hardware, payload qualification or provider acceptance.
