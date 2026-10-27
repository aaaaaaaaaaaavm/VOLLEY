> **Historical study record — ACR1 public reference:** [VOLLEY-G5-ACR1](validation/acr1/README.md) is the current integrated academic reference. Values/status below retain their dated study/configuration meaning and do not set ACR1 operating points.

# Go 3 academic release review — 12 October 2026

**Disposition: review candidate, not an engineering or flight design freeze.** The completed Gen5 research result is an adverse system-level computational finding for the specified twelve-3U configuration. Gen6 P130–P132 are a separately identified, post-study mission and first-article screen. This record maps historical technical claims to their source artifacts.

## What a reader may conclude

| Claim | Artifact to inspect locally | What the artifact establishes | What remains open |
|:--|:--|:--|:--|
| Gen5 historical 16.029 m/s | `analysis/results/motor_results.json`; P117, P118 | A periodic-force model result and its energy arithmetic | Selected winding, inverter, source and measured exit speed; P118 challenges the value |
| Finite Gen5 force | P118–P122; `analysis/results/gen5_finite_force_map.json` | Ideal 1.042 kJ integrated work; 12.448 m/s geometry-only speed; independent numerical checks under shared assumptions | Voltage/current-limited, temperature-dependent 3-D force along the actual stroke and release |
| Gen5 packaging | P116; `cad/native/Gen5_Review.FCStd`; Gen5 STEP assembly | 11 mm side-fed width shortfall and exact-solid interference for the evaluated placement | A complete, toleranced feed, restraint, release, return and brake revision |
| Gen5 installed mass | A35 and P123; `analysis/results/mass_properties.json` | 126.6 kg modeled dry rollup and 10.547 kg per carried 3U; preset criterion fails | Reconciled as-built bill of materials and any credible lighter complete design |
| Orbital utility | P115 and matched mission reference | Immediate 28.800775 km axis change for an *assumed* historical input; no sampled 12-shot campaign closes | Current-speed lifetime rerun, host operations, covariance and provider-approved mission |
| Gen6 four-state service | P130; `analysis/results/gen6_matched_campaign.json` | Both ideal commanded and spring-plus-host constructions reach the same four surrogate states; assumed device-plus-fuel burden favors springs by 10.7177 kg | Customer targets, tolerances, finite burns, installed masses, cost and reliability |
| Gen6 article geometry | P131; `cad/gen6_first_article/release/` | Two editable FreeCAD/STEP partial envelopes; five nominal stations clear and assumed 0.7° yaw clashes | Actual drive, contact, feeder, restraint, brake, complete swept path and provider fit |
| Gen6 energy and metrology | P132; `analysis/results/gen6_go2_power_instrument_screen.json` | Ideal 6 m/s mechanical and conditional 818 J bus-energy floor at assumed 10% efficiency | Selected circuit, rated parts, heat path, sensor covariance and calibrated shots |

P130's mathematical terminal residuals are **not** precision evidence. The study itself shows that an illustrative +0.1 m/s release error changes the one-day terminal position by roughly 25–27 km. The 3–6 m/s first-article measurement band does not cover P130's approximately 7 and 9 m/s commands. The 19.282 kg Gen6 mass-parity ceiling is a narrow device-plus-consumed-fuel proxy with assumed comparator masses, not a customer requirement.

## Technical interpretation

These are historical configuration-specific computational results. The current integrated reference is Gen5 ACR1; later geometry and source-coupled results retain their own source identities. Physical qualification and provider acceptance require subsequent measurements and interface evidence.
