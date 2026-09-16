# Host compatibility: Skyroot and Agnikul reference studies

Updated 2026-09-16. **Neither launcher is established as compatible. No endorsement, provider-supplied interface data or flight allocation is implied.** This document defines questions and decision gates, not approved integration designs.

[Mission sequence](PROGRAMME_EXECUTION.md) · [Current Gen6 reference](GEN6_REFERENCE_ARCHITECTURE.md) · [Host reference cases](HOST_REFERENCE_CASES.md)

## Public evidence, separated from inference

Sources accessed 2026-09-14. Public descriptions are not interface-control documents.

| ID | Public source and bounded statement | What it does not establish |
|---|---|---|
| S1 | [Skyroot launch services](https://www.skyroot.in/launch): Vikram-I is described with a restartable liquid upper stage and kick-stage orbital placement | Usable post-primary propellant, minimum impulse, restart allocation, available volume or acceptance of VOLLEY |
| A1 | [Agnikul products](https://agnikul.in/product/): an optional baby stage is described inside the fairing | Which stage would retain this deployer, its available envelope or orbital lifetime |
| A2 | [Founder announcement](https://www.linkedin.com/posts/srinath-ravichandran-09679a7_agnibaan-madeinindiafortheworld-activity-7427931601675681792-uiIJ): proposed use of the extendable Agnibaan upper stage to host a data-centre module | Successful demonstration of that service, a deployment interface or a manoeuvring capability for secondary delivery |

**Engineering inference:** S1 motivates comparison against host manoeuvres followed by conventional separation. A2 motivates a hosted-function study, but a retained instrument and a released satellite impose different disturbances and hazards. Neither inference supplies numerical host inputs to P113.

## The comparison that can reject VOLLEY

Use the same target states, tolerances, delivery windows, payload classes, manifest and disposal conditions for every alternative. A comparison to one isolated spring is insufficient. Conventional multi-payload carriers and timed releases are controls.

| Alternative | Burdens that must stay in its account |
|---|---|
| Conventional carrier, release timing | All canisters, retention, integration, clearance and achievable state distribution |
| Host manoeuvres plus conventional carrier | Above plus stage propellant, finite burn control, settling, starts and campaign time |
| Host plus current VOLLEY reference | Independent retention, accumulator/actuator, latch, pusher/catcher, support, electronics, recharge energy, recoil, shock/tip-off and common-mode services |
| Host plus banked/shared-path VOLLEY | Same functional boundary, with duplicated/shared hardware and stranded-manifest consequences charged explicitly |
| Host plus historical gas-Gen6 comparator | Pressure system, valves, seals, guide/support, consumables, contact/tip-off and the full installed host burden |
| Host plus BOLLEY | Above as applicable, plus passive payload cage, attachment, magnetic environment and payload acceptance; no unmodified-payload claim |
| Payload propulsion | Complete installed and wet propulsion system, guidance, integration and qualification; only where the mission permits it |

An architecture is rejected for a mission if it cannot satisfy a hard interface or mission constraint. If several satisfy them, retain the resource/risk trade rather than hiding it inside an arbitrarily weighted score. Unknown cost and failure rates remain parameters, not invented vendor quotations or reliability predictions.

## Interface questions, highest leverage first

All numerical answers below are **REQUIRED_FROM_PROVIDER**, not available data. No contact is requested by this document.

| Gate | Required answer | Effect on the design |
|---|---|---|
| Retained body | Which stage/platform remains with the manifest, through which separations? | Defines the actual host, not the whole rocket |
| Accommodation | Usable stowed and operating envelope, mounts, keep-outs and exit cone | Sets cell count/layout and can reject a bank or shared-path arrangement |
| Primary mission protection | Load and disturbance limits, inhibits, permitted deployment events | A secondary function must not compromise primary delivery |
| Orbital work | Permitted manoeuvres, remaining propellant, minimum impulse, start/coast allocation | Determines whether a conventional separator already suffices |
| Release control | Pointing/rate limits, navigation uncertainty, attitude recovery authority | Sets useful release precision, clearing/settling and recoil limits |
| Services | Power/energy, command interface, thermal boundaries, vent/plume constraints | Defines recharge time, shared services, installed hardware and campaign capacity |
| Payload acceptance | Retention, sustained acceleration, shock, tip-off and magnetic limits | Unmodified is an objective, not universal compatibility |
| End of mission | Disposal reserve, contingency policy and retained failed payload treatment | Bounds final deployment and fault responses |

Public estimates may bound a study but cannot change a gate to CONFIRMED. A confirmed interface requires a configuration identifier, source revision and mission scope.

## Packaging is a design gate, not a render

The current clean-sheet reference removes the historical **8 m dependency** from the assumed packaging basis. At the S4 4.569852 m/s study point, a 4 kg payload has 41.77 J ideal kinetic energy and the 10 g constant-acceleration screen is 106.5 mm. Those numbers are physics screens, not a finished cell envelope. Real stroke must include accumulator/pusher geometry, guidance, catcher travel, retention, structure, sensors and tolerances.

The historical approximately 8 m gas guide remains a comparator. Existing [A57](../validation/A57_stage_attitude_packaging.md) exposes end-hardware overrun against that configuration's own assumed length. Do not erase that miss by borrowing a rocket's overall dimensions, and do not transfer it to the compact reference as though the geometries were the same.

For the current reference, compare independent cells, small banks and a shared magazine/path. Each needs its own ascent load path, separation keep-outs, operational alignment, failed-payload handling and mass budget. Count net added host reinforcement, mounts, thermal hardware, harnesses and support equipment once in the installed ledger. Report displaced payload volume/mass capacity separately. Stage credit cannot hide hardware that the host must add.

## Failure exposure: retain safely, recover deliberately

This is an initial hazard checklist, not a complete FMEA or reliability model.

| Fault | Required safety question | Why duplication alone is insufficient |
|---|---|---|
| Controller or power loss | Does every mission phase enter a permitted retained state? | Automatic release may be hazardous during ascent or wrong attitude |
| One cell/pusher jam | Is the affected payload retained without mechanically stranding unrelated cells? | Independent mechanics still share command, power and host state |
| Bank/shared-path jam | How much of the remaining manifest is stranded? | A backup actuator on the same blocked path may not recover anything |
| Latch or unintended release | What independently prevents an uncommanded stroke? | Duplicate commands can share power, software and physical energy paths |
| Bad preload/position/clearance sensing | Can the machine release at the wrong energy or into an occupied path? | Two sensors with a shared reference can fail together |
| Degraded host pointing | Is deployment inhibited until a safe corridor exists? | Nominal departure speed does not establish collision clearance |
| Payload fails to depart | How is retention confirmed before another manoeuvre? | An ambiguous retained mass changes GNC and subsequent operations |

Compute expected delivered payload count and the distribution of stranded payloads only after defining conditional and common-mode failure assumptions. Independence must be justified. Sensitivity to uncertain rates belongs beside any mean value.

## Sequenced work and stop conditions

1. **S1-S4 complete as bounded studies:** single-departure allocation, sequential energy campaigns, single-payload terminal state and two-payload evolving-host timing/order are published. None is full mission closure.
2. **Operational uncertainty next:** declare clearing/settling, navigation, pointing, release-speed/tip-off and host-attitude-recovery terms before extending the solver. A precise mechanism cannot remove common host navigation error.
3. **Installed burden and manifest crossover:** evaluate only manifests that fit the host's mass and volume limits. Include complete installed hardware, displaced capacity, recharge/thermal time and common-mode loss exposure.
4. **Reference-cell falsification:** test whether force-displacement, latch/pusher/catcher behaviour and tolerances can support the mission-derived release-state budget before detailed CAD.
5. **Host review:** resolve the interface questions above before any compatibility claim.
6. **Configuration decision:** retain, modify or reject the current reference based on mission value, installed burden, release evidence and interfaces. The historical gas guide and Gen5 remain in the comparison rather than being erased.

For a temporary propulsion-less constellation, specify mission duration and disposal strategy before calling a lifetime increase beneficial. Longer orbital persistence is not automatically a mission advantage. Large plane changes and arbitrary circular destinations are not free consequences of commanded separation speed.

The useful next provider discussion is a short set of calculated requirements and unresolved interfaces, not a claim that a CAD assembly already fits a launcher.