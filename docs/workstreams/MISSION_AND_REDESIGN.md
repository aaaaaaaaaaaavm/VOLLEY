# Mission and redesign

> **Architecture disposition, 2026-09-28:** The separate motor-charged spring-cell bank is withdrawn as VOLLEY's next architecture. It is retained here only as a dated study. Any selection or current-reference wording below describes the former decision and is superseded. A reusable shared launch path with sequential loading is the open design objective; no speed envelope is validated. See [current status](../../docs/NEXT_GENERATION_STATUS.md).


## Current position

S1–S4 provide four bounded mission-study layers. P113-S4 is merged with 100 two-payload schedule/order/authority cases; 44 tested campaigns are accepted. The clean-sheet P92 screen carries that result into mechanism physics instead of inheriting a historical speed target.

P113-S5 now adds a first deterministic **local operational-uncertainty sensitivity** around the best tested S4 BOLLEY-screen campaign. All declared numerical checks pass. It does not invent a covariance or a provider capability and it does not close P113/E5/P92. The first release is the tighter event in this nominal campaign: the local linear study allowance is about 0.00155 m/s for release-speed error and 0.0004425 rad (about 0.0254 degrees) for in-plane release-direction error under the existing 10 m / 0.01 m/s terminal bands. Common tangential host-velocity error is comparably restrictive at about 0.00130 m/s. These are **LOCAL_LINEAR_ALLOWANCE** values, not hardware requirements, sensor specifications or demonstrated capability.

The two stored S4 release epochs are 1800 s apart. That gives timestamp headroom above the 30/60/120/300 s markers used in S5, but no slew, settling, thermal recovery or manoeuvre model is attached to those markers. E5/provider data remain required.

The independent spring-cell reference has been withdrawn. Its S4 study point of 4.569852 m/s for 4 kg needs 41.77 J of ideal payload energy; a 10 g illustrative constant-acceleration stroke is 106.5 mm and lasts 46.6 ms. Those values are a low-speed comparison, not a selected mechanism or speed limit. P92/P113 remain open because installed mass, release/navigation uncertainty, clearing/settling, release dynamics, repeatability, complete-manifest effects and provider accommodation are not closed.

The historical 8 m gas guide, direct electromechanical pusher, frozen Gen5 model, banked/shared-path arrangements and BOLLEY remain trade cases under distinct payload interfaces. No mechanism is selected by the existing two-payload screen.

## Ordered deliverables and exit conditions

1. **Robust architecture-driving mission requirements.** S5 has exposed local sensitivity. Next declare bounded navigation, pointing, release and clearing/settling cases without pretending they are provider data, then carry them through the evolving-host campaign. Preserve the propulsion-less individual, initial group distribution and replenishment mission hypotheses and add host attitude recovery, installed deployment burden and complete-manifest effects. Target states, windows, tolerances and host limits precede the solver extension.
2. **Installed burden and failure architecture.** Compare a shared feeder/release path with independent cells, banks and an ordinary dispenser. Count occupied volume and retained spent hardware, support, containment, drive energy, power, controls, sensors, thermal hardware, operations, cost assumptions and successfully delivered payloads. Model blocked paths and shared power/control failures. Separate safe retention from recoverable deployment.
3. **Mechanism falsification.** Before detailed CAD, define comparable force/travel and loader/release fault tests for candidate shared drives. Retain spring-cell preload, latch, pusher and catcher tests only as comparator evidence. Freeze acceptance criteria before testing, and do not widen a failed band to promote a candidate.
4. **Complete campaign comparison.** Springs plus release timing, host manoeuvres, programmable deployment and cooperative BOLLEY under identical targets. Carry changing host mass/recoil/propellant, release-time search and convergence, uncertainty, attitude recovery/settling, resource depletion and final host condition. A feasible state or lower propellant total alone is not superiority.
5. **Provider accommodation.** Calculate geometry, forces/torques, recoil, energy, power, cadence and attitude demands. Request a disposition against a named host configuration; keep public information, study assumptions and missing ICD data distinct.
6. **Configuration decision.** Select a mechanism only after matched installed burden, full-manifest mission value and discriminating release/feed evidence exist. Record the ADR and P92/P113 dispositions. Do not adopt 29, 89 or 120 m/s without payload and mission requirements. S4's 4.569852 m/s first release is a bounded campaign result, not a product limit.
7. **Scaling and build package.** Compare 2/4/12-payload campaigns across shared and banked layouts and adjacent payload sizes. Produce drawings, BOM, assembly/inspection, instrumentation/calibration, uncertainty and acceptance criteria for a named test article. External review and physical testing remain required.

## Boundaries

This stream owns presentation, mission studies, requirements, architecture decisions and eventual release/feed interfaces. The closure stream can analyze historical designs and supply reusable results. Do not combine evidence from different geometries, payload interfaces or force duties without a new validation path.

[P113-S5 uncertainty result](../OPERATIONAL_UNCERTAINTY.md) · [P92 reference-architecture screen](../LEGACY_STUDY_REFERENCE_ARCHITECTURE.md) · [P113-S4 result](../MANIFEST_TIMING.md) · [Programme sequence](../PROGRAMME_EXECUTION.md) · [Coordination](../CONTINUITY.md) · [Closure stream](ENGINEERING_CLOSURE.md)
