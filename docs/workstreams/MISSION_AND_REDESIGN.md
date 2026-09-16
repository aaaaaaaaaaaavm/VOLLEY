# Mission and redesign

## Current position

S1–S4 provide four bounded mission-study layers. P113-S4 is merged with 100 two-payload schedule/order/authority cases; 44 tested campaigns are accepted. The clean-sheet P92 screen carries that result into mechanism physics instead of inheriting a historical speed target.

P113-S5 now adds a first deterministic **local operational-uncertainty sensitivity** around the best tested S4 BOLLEY-screen campaign. All declared numerical checks pass. It does not invent a covariance or a provider capability and it does not close P113/E5/P92. The first release is the tighter event in this nominal campaign: the local linear study allowance is about 0.00155 m/s for release-speed error and 0.0004425 rad (about 0.0254 degrees) for in-plane release-direction error under the existing 10 m / 0.01 m/s terminal bands. Common tangential host-velocity error is comparably restrictive at about 0.00130 m/s. These are **LOCAL_LINEAR_ALLOWANCE** values, not hardware requirements, sensor specifications or demonstrated capability.

The two stored S4 release epochs are 1800 s apart. That gives timestamp headroom above the 30/60/120/300 s markers used in S5, but no slew, settling, thermal recovery or manoeuvre model is attached to those markers. E5/provider data remain required.

The reference carried forward for the next calculations is **independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. At S4's 4.569852 m/s study point, a 4 kg payload needs 41.77 J ideal payload energy; a 10 g constant-acceleration screen is 106.5 mm and 46.6 ms. This is a reference candidate, not selected flight hardware. P92/P113 remain open because installed mass, robust release/navigation uncertainty, clearing/settling, latch/pusher dynamics, repeatability, catcher loads, complete-manifest effects and provider accommodation are not closed.

The historical 8 m gas guide, direct electromechanical pusher, compact gas pusher, frozen Gen5 LSM, banked/shared-path arrangements and BOLLEY remain explicit comparators or backups. No historical mechanism is deleted merely because the reference moved.

## Ordered deliverables and exit conditions

1. **Robust architecture-driving mission requirements.** S5 has exposed local sensitivity. Next declare bounded navigation, pointing, release and clearing/settling cases without pretending they are provider data, then carry them through the evolving-host campaign. Preserve the propulsion-less individual, initial group distribution and replenishment mission hypotheses and add host attitude recovery, installed deployment burden and complete-manifest effects. Target states, windows, tolerances and host limits precede the solver extension.
2. **Installed burden and failure architecture.** Quantify the reference independent cell against banks and the shared magazine. Account for occupied envelope, support structure, containment, actuator/energy storage, power, controls, sensors, thermal hardware, deployment energy, operations, cost assumptions and successfully delivered payloads. Model a blocked path and shared power/control failures. Separate safe retention from recoverable deployment.
3. **Reference-cell falsification.** Before detailed CAD, bound the accumulator force-displacement law and write coupon bands for preload repeatability, latch shock, pusher friction, exit velocity/tip-off and catcher load. Use S5 to identify which release-state terms actually need the tightest experimental attention. A failed band changes the reference rather than widening the band.
4. **Complete campaign comparison.** Springs plus release timing, host manoeuvres, programmable deployment and cooperative BOLLEY under identical targets. Carry changing host mass/recoil/propellant, release-time search and convergence, uncertainty, attitude recovery/settling, resource depletion and final host condition. A feasible state or lower propellant total alone is not superiority.
5. **Provider accommodation.** Calculate geometry, forces/torques, recoil, energy, power, cadence and attitude demands. Request a disposition against a named host configuration; keep public information, study assumptions and missing ICD data distinct.
6. **Configuration decision.** Close or reject the reference only after installed burden and decisive release-cell evidence exist. Record the ADR and P92/P113 dispositions. Do not adopt 29, 89 or 120 m/s without a mission-derived requirement. S4's 4.569852 m/s first release remains a tested campaign result, not a product minimum or optimum.
7. **Scaling and build package.** Compare 2/4/12-cell campaigns, adjacent payload sizes and independent banks. Produce drawings, BOM, assembly/inspection, instrumentation/calibration, uncertainty and acceptance criteria for a named test article. External review and physical testing remain required.

## Boundaries

This stream owns README presentation assets, new mission studies, requirement/configuration ADRs and selected release-cell interfaces. The closure stream can analyze the historical gas design and supply reusable results. Do not combine evidence from different geometries, payload interfaces or force duties without a new validation path.

[P113-S5 uncertainty result](../OPERATIONAL_UNCERTAINTY.md) · [P92 reference-architecture screen](../GEN6_REFERENCE_ARCHITECTURE.md) · [P113-S4 result](../MANIFEST_TIMING.md) · [Programme sequence](../PROGRAMME_EXECUTION.md) · [Coordination](../CONTINUITY.md) · [Closure stream](ENGINEERING_CLOSURE.md)