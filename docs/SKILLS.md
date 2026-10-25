# Engineering methods and evidence

**25 October 2026 — VOLLEY-G5-ACR1.** This page maps the methods used in the completed computational design study to their inspectable source and results. The reference contains twelve nominal 4 kg 3U surrogates and a modeled 1–3 m/s operating range.

[Current package and reproduction](../validation/acr1/README.md) · [Numerical findings](CURRENT_NUMERICAL_EVIDENCE.md) · [Evidence provenance](PROVENANCE.md)

## Current computational methods

| Method | ACR1 evidence | What it establishes |
|:--|:--|:--|
| Parametric mechanism CAD and neutral exchange | [Native/STEP inventory](../validation/acr1/cad/release/FINAL_CAD_MANIFEST.json), [independent readback](../validation/acr1/verification/FINAL_STEP_READBACK_SUMMARY.json) | Eight assembly states checked by separate import paths; native and neutral models share the Open CASCADE kernel family. |
| Installed motion and custody | [Motion verification](../validation/acr1/cad/release/MOTION_VERIFICATION.json), [final refinement](../validation/acr1/cad/release/FINAL_REFINEMENT_VERIFICATION.json), [interlocks](../validation/acr1/analysis/TRANSFER_INTERLOCKS.json) | 154 accepted motion/refinement cases and an executable command/proof specification for guided feed, pallet capture, release, arrest and return. |
| Finite electromagnetic force | [Finite motor](../validation/acr1/analysis/FINITE_MOTOR.json), [actual-current comparison](../validation/acr1/analysis/CURRENT_FIELD_FORCE.json) | Position-dependent permanent-field integration; the actual DC conductor-current check differs by −0.1718% at one interior station. This is a numerical comparison under shared field assumptions. |
| Source-coupled dynamics and energy accounting | [Coupled shot](../validation/acr1/analysis/COUPLED_SHOT.json), [equation/timestep audit](../validation/acr1/verification/COUPLED_SHOT_REVIEW.md) | Launch, unilateral payload separation, regenerative limits and retained-sled arrest. Six principal 3 m/s cases receive the 20-to-5 µs audit using the production solver with independent review and work-balance reconstruction. |
| Actual-chassis structural analysis | [Chassis review](../validation/acr1/verification/CHASSIS_ACTUAL_REVIEW.md), [design budgets](../validation/acr1/analysis/DESIGN_BUDGETS.json) | Connected-solid linear elasticity and a declared 1.3× load sensitivity; 0.264111 mm individual-face design budget under the stated centring/tolerance allocations. |
| Thermal and contact-energy bounds | [Design budgets](../validation/acr1/analysis/DESIGN_BUDGETS.json) | Current-history-based conductor heating and explicit surrogate stiffness/inertia bounds; local mesh observations and assumed load sharing retain their limits. |
| Actuator and installed-resource sizing | [Feed](../validation/acr1/analysis/FEEDER_SIZING.json), [lift](../validation/acr1/analysis/LIFT_SIZING.json), [resource ledger](../validation/acr1/analysis/RESOURCE_LEDGER.json) | Catalog-based coast sizing and explicit mass allowances. CAD dry mass is 149.556720 kg; the separate 7 kg electrical/control allocation has no assigned CAD position. |
| Matched orbital delivery and native replay | [Mission report](../validation/acr1/mission/MISSION_REPORT.md), [native checks](../validation/acr1/mission/NATIVE_REPLAY_CHECKS.json) | Twelve synthetic full-state targets at a common epoch, changing mass/recoil and nine Orekit replay cases. The tested families show no propellant or initial wet-mass advantage over ideal ground-pretrimmed springs. |
| Reproduction and source identity | [Portable examples](../validation/acr1/REPRODUCTION.md), [payload manifest](../validation/acr1/MANIFEST.json), [software lock](../validation/acr1/release/SOFTWARE_ENVIRONMENT.json) | Inspectable input/source/output identities and bounded replay commands; omitted large solver assets and required native dependencies are identified. |

## Historical methods and design lineage

[Original Gen5 baseline](BASELINE.md), [earlier verification records](../validation/README.md), [GMAT studies](../validation/gmat/), [circuit studies](../validation/spice/) and [decision records](adr/) retain their original configurations. The [FM08-R3 mixed-size feeder](../validation/selected_feeder/README.md) records the preceding mechanism selection. Its geometry and the original Gen5 speed, mass and fit results do not describe ACR1.

[Related-work review](RELATED_WORK.md) distinguishes retrieved primary sources, selected full-text readings and unresolved leads. Third-party experiments support their own interfaces and conditions; their measured performance is not assigned to VOLLEY.

## Evidence boundary

The record demonstrates computational engineering methods and their declared numerical checks. Physical release performance, measured tolerances, reliability, environmental qualification and provider acceptance remain subsequent evidence stages. Source and software/license credits remain with the linked records. Authorship and contribution credits follow the respective academic and source records.
