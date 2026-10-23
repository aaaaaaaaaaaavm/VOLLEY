# Literature and reference evidence

This document identifies the literature and public references supporting the present study, with the scope of review stated for each source. It is a focused evidence summary, not a systematic review of electromagnetic launch, linear machines, orbital transport or space mechanisms. Bibliographic leads alone do not support performance, compatibility or novelty claims.

## Closest feeder studies: full-text review

The publisher PDFs of the following two works were reviewed on 19 October 2026. The [detailed review](FEEDER_FULL_TEXT_REVIEW_2026_10_19.md) records section/page locations, experimental and numerical distinctions, limitations and engineering implications. [Source identities](FEEDER_FULL_TEXT_SOURCES.json) record PDF hashes and page counts. Published tests are evidence for the authors' prototypes; they do not physically validate VOLLEY.

| Source | Evidence established by the review | Consequence for VOLLEY |
|:--|:--|:--|
| Zhao et al., “Design and Analysis of a New Deployer for the In-Orbit Release of Multiple Stacked CubeSats,” *Remote Sensing* 14(17), 4205 (2022), [doi:10.3390/rs14174205](https://doi.org/10.3390/rs14174205) | Stacked storage, planar electromagnetic transport and opposing release windows; component laboratory tests. A 1 kg dummy transfers about 120 mm in 0.409 s. Gravity-compensated releases span 0.67–1.42 m/s for 1 kg and 0.40–0.85 m/s for 3 kg. | These architectural elements are prior art. Retain force-line/COM offset, magnetic exposure and stuck-payload path isolation as verification concerns. The results establish neither integrated flight operation nor VOLLEY release performance. |
| Zhao et al., “Simulation Analysis and Experimental Verification of the Transport Characteristics of a High-Volume CubeSat Storage Device,” *Aerospace* 12(6), 466 (2025), [doi:10.3390/aerospace12060466](https://doi.org/10.3390/aerospace12060466) | Rope-driven stack pusher, detents, receiver guides and magnetic capture. Zero-gravity simulation gives about 3.05 s first-layer travel, 32.8 mm/s average speed and contact peaks around 1200 N. Separate gravity-assisted laboratory pushes take about 0.20/0.246 s; the offset case briefly stalls. | Keep simulation and prototype results distinct. The design uses spacecraft housing grooves and iron patches, so it does not demonstrate transfer of arbitrary unchanged passive CubeSats. Retain contact, rebound, settling and interface checks. |

The 2025 prototype verifies part of the proposed process. Its stipulated contact/friction parameters are not measured vacuum tribology inputs for VOLLEY. A reusable external carrier remains an interface hypothesis requiring the existing contact, retention, release, mass and magnetic-exposure assessments. The source's unresolved motor-sizing discrepancy is documented in the detailed review; no corrected supplier rating is inferred.

## Payload and host references: bounded public-source checks

The [Gen6 public reference audit](GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md) records the documents, verified datums, revisions and limits for the surrogate payload/host study. Its checks do not constitute a comprehensive review of each source or an integration approval.

| Reference | Supported use | Boundary |
|:--|:--|:--|
| Cal Poly CubeSat Design Specification Rev. 14.1 (2022) | Generic class envelopes; 1U ≤ 2 kg and 3U ≤ 6 kg. | Actual allowable mass and fit require the dispenser/provider interface. |
| NanoRacks NRCSD IDD, NR-NRCSD-S0003 Rev. – | A real mixed-size dispenser interface; stated 0.5–2.0 m/s deployment survival and up to 5°/s/axis tip-off. | These are NRCSD interface values, not universal limits or approval of VOLLEY's study speeds. |
| SwissCube project and MinXSS mission paper | Named 1U/3U spacecraft precedents. | The study's 1.33/4 kg masses are surrogates, not the actual masses or qualifications of those spacecraft. |
| D-Orbit ION service description | Public precedent for propulsion-enabled orbital transport and commanded deployment services. | It supplies no usable host mass, propulsion, trajectory, price or ICD values for the mathematical surrogate; it is not a selected provider. |

## Space-mechanism references: selected passages

The [mechanism source record](../validation/feeder_release_review/comparison_reference/RESEARCH_SOURCES.json) identifies *Liquid Lubrication for Space Applications*, NASA TM-105198 ([NTRS record](https://ntrs.nasa.gov/citations/19920022596)), and the *46th Aerospace Mechanisms Symposium Proceedings* ([NTRS record](https://ntrs.nasa.gov/citations/20220006415)), with full-text hashes. Only selected relevant passages were reviewed. This is not an exhaustive handbook or proceedings review. Mechanism-specific friction, lubricant performance, loads, life and qualification results are not transferred to VOLLEY.

## Claim boundary

The present contribution is the traceable computational evaluation and its explicit engineering limitations. Stacked storage and adjustable electromagnetic release alone do not establish novelty. Comparative claims about reliability, storage density, cost, installed mass or delivered accuracy require equal system boundaries and supporting data. The selected FM08-R3 architecture is supported by its own [FDR10 trade and design evidence](../validation/selected_feeder/README.md). Literature informs the choice; it does not qualify an interface or establish provider acceptance. The original all-seven qualification prerequisite has been replaced by the declared academic D27-R2 selection boundary.

## Finite-array end effects and actuator precedent

The [targeted source review](END_EFFECT_AND_ACTUATOR_REVIEW_2026_10_22.md) checks selected methods/results/conclusion passages from the nine-page Japanese original of Yamaguchi and Morishita, DOI 10.1541/ieejias.143.570. The English translation is DOI 10.1002/eej.23450. The source uses a 2D model and compares it with 2D JMAG. Its ripple-cancellation arrangement assumes integer magnetic-period length, air-core coils and energized coverage extending one pole pitch beyond each field end. It supplies no universal end-effect correction, finite-width 3D validation or hardware demonstration. VOLLEY must retain its own finite-geometry and real-winding evidence boundaries.

The close double-magnetic-circuit CubeSat actuator study, DOI 10.1109/TIE.2021.3134060, remains metadata/abstract-only after bounded publisher, repository and open-access-location checks. No numerical force-density, interface, measured accuracy or passive-spacecraft compatibility claim is borrowed from it. This unresolved full-text review remains a research dependency rather than a completed verification.

## Selected-drive primary references — 23 October 2026

The selected feeder uses ambient industrial references for sizing. The Thomson primary catalog (printed pp. 11–12) gives the SB3700 nut 310 N dynamic capacity at 500 rpm under its stated lubricated/ambient/duty conditions, 1550 N static capacity, and a 7.4 mm root reference for SPT10×2M. Its approximate speed/load derating is kept separate from space tribology. The selected analytical screen uses a conservative 155 N ceiling at up to 1000 rpm; catalog capacity is not transferred as a vacuum-qualified load.

FAULHABER 3242 BX4, 32GPT and MC5005S primary sheets supply reference motor, gearbox and controller values. Miki Pulley's spring-actuated brake catalog supplies static holding options. [Source metadata, captured identities and calculations](../validation/selected_feeder/verification/catalog_reference.json) distinguish supplier values from assumed efficiency, friction, loads and thermal conditions.

The 23 October bounded access check again found no lawful open full text for DOI 10.1109/TIE.2021.3134060. Its contribution remains abstract-only; no quantitative performance is imported. Public orbital-service descriptions establish the service category but do not supply a matched customer trajectory, installed mass or price for a numerical performance comparison.
