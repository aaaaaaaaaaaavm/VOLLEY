# Full-text feeder comparison — 19 October 2026

## Review scope and evidence

The publisher PDFs of Zhao et al., *Remote Sensing* 14(17), 4205 (2022), DOI [10.3390/rs14174205](https://doi.org/10.3390/rs14174205), and Zhao et al., *Aerospace* 12(6), 466 (2025), DOI [10.3390/aerospace12060466](https://doi.org/10.3390/aerospace12060466), were obtained in full. Methods, architecture, simulations, experiments and limitations were examined; the 2025 motor-sizing page was also inspected as a rendered page. Both PDFs state CC BY 4.0. Source hashes and page counts are recorded in the accompanying JSON; publisher PDFs are not duplicated in this repository.

This review is limited to these two close works. It does not close the separate end-effect, mission/carrier and broader electromagnetic-launch literature review. Published prototype tests belong to their authors and do not physically validate VOLLEY.

## Quantitative comparison with evidence classes

| Work and location | Result | Evidence and boundary | Consequence for VOLLEY |
|:--|:--|:--|:--|
| 2022 §§2.1–2.3,pp.2–5 | Stacked store, XY magnetic tray transport and four opposed release windows | Proposed system architecture; component prototypes, not a flown campaign | Stacking, programmable electromagnetic ejection and opposing recoil paths are prior art |
| 2022 §5.3,pp.14–16 | 1 kg dummy transfer across about 120 mm in0.409 s; peak0.56 m/s at 5 A | Laboratory transfer between two adjacent cells; horizontal and vertical arrangements | Useful test-observable precedent, not a reliability or zero-g throughput specification |
| 2022 §5.4,pp.17–18 | 0.5–2.5 A gives 1 kg release0.67–1.42 m/s and3 kg release0.40–0.85 m/s | Gravity-compensated laboratory release; reported model errors below 11% | Compare model/measurement separately; do not rank VOLLEY's imposed or ideal speeds against these as hardware |
| 2022 §4.2,pp.10–11 | 0.5 mm centroid-offset cases and angular-speed predictions | Simulation; the cited3°/s criterion is not a universal approved VOLLEY limit | Include COM/force-line offset and contact in future tip-off studies |
| 2022 §5.1,pp.12–13 | Launcher-axis leakage about20.17 mT; conveyer leakage up to about1.62 mT | Their measured fields and their assessment of operation | Do not borrow a universal payload-safe field threshold |
| 2025 §§2.2–2.3,pp.4–11 | Rope-driven stack pusher, spring-ball detents, receiving slides, magnetic capture and planar transport | Detailed proposed/prototype architecture; special spacecraft housing features | Cable-pusher variant belongs in the research comparison; compatibility requires an approved interface |
| 2025 §4.4,pp.20–25 | First-layer pushabout3.05 s, average32.8 mm/s; secondabout2.88 s,35.1 mm/s; contact peaksabout 1200 N | Zero-gravity multibody simulation with stipulated friction/contact parameters | Smooth final seating does not imply low shock; retain transient forces and rebound |
| 2025 §5,pp.25–28 | Aligned/offset laboratory pushesabout 0.20/0.246 s; offset case briefly stalls after contact | Gravity-assisted prototype tests with optical tracking | Do not describe the 32.8 mm/s simulation and fast laboratory test as the same operating result |
| 2025 §6,pp.28–29 | 1U–3U,24U system concept; prototype verifies only part of the complete process | Authors' explicit limitation | No inherited integrated mission, environmental or flight validation |

## Compatibility finding

The 2025 design does not demonstrate transfer of arbitrary unchanged passive CubeSats. Section2.3,pp.8–10 describes grooves on the spacecraft housing, guide/gimbal features and iron patches attracted by receiver magnets. Its simplified 100/200/300 mm body lengths also differ from VOLLEY's113.5/340.5 mm reference lengths. Adopting those features would change the payload-side interface and the agreed passive-spacecraft objective.

VOLLEY may investigate a reusable external carrier or passive insert carrying all added guide/retention features. That is a design hypothesis: the carrier still needs an approved spacecraft contact/load interface, release mechanism, mass accounting and magnetic-exposure analysis. It must not be called ordinary-payload compatible merely because the satellite has no powered electronics added.

## Fault containment and test design

The 2022 paper explicitly identifies lower reliability than conventional deployment when one stuck CubeSat affects subsequent transport routes (§5.4,p.18). This directly supports the existing cell-isolation requirement: leave the failed payload retained, inhibit the common path, and allow other cells only after an independently verified safe-path check. It supplies no numerical failure probability.

The 2025 receiving experiment contains a short stall and multiple contact events before final alignment (§5,pp.26–27). The correct verification targets therefore include first-contact force, impulse, rebound, settling, orientation and subsequent tray clearance. Arrival at the endpoint alone is insufficient. Its simulated1200 N peak would correspond to30.6g if divided by a 4 kg mass; that arithmetic is only a contact-load equivalent, not a measured spacecraft acceleration or applicable qualification limit. Contact duration and force distribution are needed before comparing it with a payload shock specification.

## Model and source checks

- The 2022 paper attributes higher-current force/model differences to armature reaction and release losses (§5.2/5.4). A permanent-field force map alone is insufficient for VOLLEY's eventual current-rated motor claim.
- Its force experiments and release experiment are separately reported. Magnetic leakage measurements cannot establish compatibility for a different spacecraft or motor geometry.
- The 2025 contact/friction parameters are stipulated model inputs (Table4,p.18), including high inter-spacecraft friction coefficients. They are not transferable vacuum tribology measurements for VOLLEY.
- A first natural frequency above an assumed threshold is not a vibration qualification result. The 2025 paper itself later identifies physical sinusoidal/random-vibration and thermal-vacuum work as future validation (§3,pp.12–14).
- Enclosure within a host does not establish zero radiation exposure. VOLLEY must retain a host-specific radiation/electronics assessment rather than importing that assumption.
- In the 2025 motor-sizing text (§4.1,p.15),68.39 N and6 mm imply a simple spool torque of 0.41034Nm or4.184kgf·cm. The page states11.63kgf·cm without a reproducible additional factor in the displayed derivation. Treat this as an unresolved source sizing discrepancy, not a corrected supplier specification. The source's14kgf·cm motor is laboratory hardware, not a vacuum/space-rated VOLLEY selection.

## Engineering changes required by this review

1. Keep spacecraft interface features and any reusable carrier explicitly separate in CAD/BOM/ICD.
2. Add asymmetric pusher force, COM offset, partial gate release and capture impact to the contact-analysis cases.
3. Retain stall, rebound, first-contact and settling histories; require sensor and physical-custody agreement.
4. For a cable-pusher variant, calculate tension throughout the actual stroke, including pulley radii, spool build-up, efficiency, creep, slack and break containment. Near-horizontal cables increase required tension; low actuator count does not eliminate jamming or alignment risk.
5. Include armature reaction or a justified bound in the selected-current electromagnetic calculation.
6. Do not use a comparative claim of storage density, cost, reliability or installed mass until the system boundaries are equal and actual data exist.
7. Preserve all seven present feeder candidates. The rope-pusher mechanism is a source-derived variant within the cable/shuttle research family, not a newly selected baseline or a silent scope replacement.

## Research contribution

The defensible current contribution remains the transparent system-level computational evaluation: failed original geometry and installed burden, coupled host/resource comparison, independently checked numerical cases, and traceable future mechanism requirements. Mixed-size storage and adjustable electromagnetic release alone are not novel. A future validated passive-interface architecture and demonstrated mission value could add a distinct contribution; neither is established by the current models.
