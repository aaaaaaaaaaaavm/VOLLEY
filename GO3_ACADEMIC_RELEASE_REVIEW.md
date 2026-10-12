# Go 3 academic release review — 12 October 2026

**Disposition: review candidate, not an engineering or flight design freeze.** The completed Gen5 research result is an adverse system-level computational finding for the specified twelve-3U configuration. Gen6 P130–P132 are a separately identified, post-study mission and first-article screen. This record is a claim checklist for a college examiner, an IEEE reviewer and a deployment-mechanism engineer. It is not an independent third-party review.

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

## Three reviewer passes

| Reader | Strongest current point | Likely decisive criticism | Evidence needed for a stronger decision |
|:--|:--|:--|:--|
| College panel | Traceable negative result, model cross-checks, native CAD, source-linked report and presentation | A chaptered report and figures do not convert conditional calculations into a finished functioning product; specific college format and signed review may still be required | Final college template, signed authorship/guide review, one controlled PDF/deck/artifact hash set and clear oral defense of the three adverse Gen5 findings |
| IEEE reviewer | Falsifiable system-level finding, finite-force correction and prior-art-aware comparison | Closest sources and novelty need full-text treatment; component, uncertainty, mission and independent validation gaps limit generality | Venue selection, focused contribution statement, quantitative prior-art table, reproducible uncertainty and independent technical review |
| Aerospace integration engineer | Failed mass and fit criteria are disclosed; Gen6 has two native geometry alternatives and a matched mission | Neither generation has a selected safe release chain, installed source/brake/BOM, payload limits or approved host ICD; no measured reliability | G0 customer/interface need, G1 complete architecture, G2 coupled/rated models, G3 contained calibrated hardware tests before any flight-oriented rating |

No numeric score is awarded here: three hypothetical scores would imply external evaluations that have not happened. A 25+/30 *computational-study* assessment remains a target, not a verified score; a 25+/30 flight-product assessment would require physical and provider evidence outside this release.

## Release gates and residual risks

1. **Academic presentation:** supported as a computational study with negative selection findings. Use the current manuscript/report/deck and cite the exact model and assumption for every number.
2. **Final Gen5 academic freeze:** **open**. The full Gen5 C-00–C-20 register still records unresolved electromagnetic, mechanism, structural, thermal, mission and host criteria. A formal freeze needs a controlled exception decision and one final claim-to-artifact/hash sweep; it must not imply passed hardware validation.
3. **IEEE submission:** **open**. The manuscript is IEEE-formatted, but no venue is selected or independent peer review complete. Formatting, length and supplementary evidence are venue-specific.
4. **Gen6 build release:** **open**. Candidate A is only an analysis lead and B is a live challenger. Neither has a complete part list, selected circuit, restraint, contact path, carrier capture or brake.
5. **Flight/product claim:** **open**. No VOLLEY hardware, repeated release data, environmental qualification, customer/provider acceptance or flight data exist.

The next high-value package is a named customer/host/interface and tolerance contract, followed by a complete source-rated G1 design with a matched installed-resource decision. If the design cannot beat the competent spring-plus-host option on a real delivery job, retain that finding and stop rather than increase release-speed claims.
