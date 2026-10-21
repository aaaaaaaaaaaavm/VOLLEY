# VOLLEY

### Commanded CubeSat deployment: a computational feasibility study

VOLLEY investigates a host-mounted electromagnetic launcher that feeds passive CubeSats into a reusable sled and commands a separate departure state for each release. The intended service is mixed-size deployment from a maneuvering orbital-transfer host, assessed against spring deployment with the same host assistance.

[Project website](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Engineering report](reports/GEN5_COMPUTATIONAL_REVIEW.pdf) · [CAD and STEP](cad/README.md) · [Validation index](validation/README.md)

![STEP-derived Blender storyboard of intended storage, transfer, acceleration and departure](cad/renders/sequence/gen5_operations_hero.png)

*Conceptual operating sequence rendered from STEP geometry; motion shown is illustrative. [Animation and source geometry](cad/renders/sequence/README.md).*

## Study configuration

**Gen5** is the fixed evaluated configuration: twelve 4 kg 3U payloads, a 1.3 m powered stroke and a reusable carrier. Its technical evidence snapshot is retained with the assessed design criteria. **Gen6** is a separate development study for passive 1U and 3U spacecraft, initially two of each, with a twelve-payload expansion assessed separately.

The Gen6 mission reference uses a generic maneuvering OTV in approximately 500 km sun-synchronous orbit. Four releases occur within one orbital period; full position and velocity targets are evaluated at a common epoch 24 hours after the last release. Host maneuvers and their resource costs are included for both deployment policies. These are declared surrogates, not provider-approved interfaces.

## Engineering evidence

![FM06-R1 transfer assembly, rendered from native FreeCAD geometry in Blender Workbench](validation/feeder_integrity_review/figures/FM06_Technical_transfer.png)

*FM06-R1 nominal transfer configuration. Editable geometry, STEP exchanges, calculations and native solver records are included in the [engineering package](validation/feeder_integrity_review/README.md).*

| Evidence | Published result | Interpretation |
|:--|:--|:--|
| Native geometry | 30 assembly poses and 70 individual STEP exchanges | Nominal, prescribed-motion geometry checks |
| Current receiver fixtures | 12 native finite-element analyses | 0.05998 mm mean loaded-face displacement for the 3U one-dog 1000 N ideal fixture |
| Transfer tine | Four native unit-load meshes | 0.010145 mm/N finest-mesh mean compliance under the stated clamp and material assumptions |
| Contact representation | 12 native cases, 14 planar controls and 84 full-solid poses | Calibrated numerical representation; final-state accuracy remains unaccepted |
| Orbital campaign | 18 targeted schedules and 46 native Orekit replays | Matched finite-force host-control and resource comparisons |

[Native FreeCAD](validation/feeder_integrity_review/cad/FM06_3U_transfer.FCStd) · [Assembly STEP](validation/feeder_integrity_review/cad/FM06_3U_transfer.step) · [Part index](validation/feeder_integrity_review/parts/INDEX.json) · [Load/contact report](validation/feeder_integrity_review/FEEDER_INTEGRITY_REVIEW.pdf)

## Matched orbital delivery

![Finite-force host schedules and propellant comparison](validation/finite_burn_review/figures/force_fuel_trade.png)

The finite-burn study compares the same constructed terminal states and resource boundary. Under the declared twelve-release 35%/35% policy, the spring input requires 33.83 N peak and 23.12 kg propellant; the imposed VOLLEY release input requires 18.00 N and 6.12 kg. With a common 100 N limit and 30 kg propellant allowance, both policies reach the constructed translational targets. The assumed VOLLEY device-mass premium exceeds its propellant saving in this comparison.

[Method, inputs and native outputs](validation/finite_burn_review/README.md) · [Engineering report](validation/finite_burn_review/FINITE_BURN_CAMPAIGN_REVIEW.pdf) · [Native replay and command sensitivity](validation/native_campaign_review/README.md)

## Electromagnetic and system findings

<p><img src="figures/gen5_finite_force_surface3d.png" alt="Depth-resolved three-dimensional force cross-check" width="49%"> <img src="figures/gen5_one_event_installed_burden.svg" alt="Matched one-event installed device and propellant burden" width="49%"></p>

| Gen5 quantity | Result and boundary |
|:--|:--|
| Ideal finite-geometry release screen | 12.448 m/s, with ideal phase and assumed electrical conditions; no component-rated speed |
| Historical periodic-force model | 16.029 m/s; retained as a model comparison |
| Historical modeled dry mass | 126.562 kg, or 10.547 kg per 3U slot |
| Evaluated packaging | 11 mm cassette/track width shortfall; full exact-solid dispositions are retained |
| One-event resource comparison | The evaluated device-mass premium exceeds the modeled propellant saving |

The [finite-force analyses](validation/P121_gen5_finite_force_surface3d.md), [mass/energy audit](validation/P133_gen5_evidence_audit.md), [CAD assessment](cad/GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.md) and [technical configuration record](docs/GEN5_TECHNICAL_BASELINE.json) define the scope of these results.

## Evidence boundaries

This is a computational design study. No physical prototype, measured release performance or flight qualification is claimed. Fixture compliance uses idealized supports and material assumptions. The [FCE12 contact study](validation/feeder_contact_verification/README.md) checks the collision representation against analytical controls and 84 native-solid poses. Final-state and contact-force refinement remain sensitive; no precision or design-load rating follows. Installed actuation, complete release/reset and mixed-size system integration remain development requirements. All seven feeder architectures remain unselected.

## Research and development

The [feeder trade](docs/GEN6_FEEDER_CONCEPT_TRADE.md) compares lead-screw, escapement, rack/pawl, indexed tray/drum, pantograph, telescoping and belt/cable approaches. Safety, retention, integration, mass, motion and fault evidence govern downselection. A 1 km/s-class release is a separate long-range scaling objective.

## Reproducibility

Captured studies include source inputs, solver versions, raw outputs, figures and hash manifests. Their local README files specify the required software and replay commands. Native CAD requires FreeCAD; STEP provides the neutral geometry exchange. Blender assets are identified as renders.

Run `python tools/prepublish_gate.py --all` for publication checks and `python tools/check_public.py` for current public-value consistency. The engineering analyses have their own verification commands.

## Project editions

[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY) · [Thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) · [Paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) · [Labs](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)

Each edition contains its own evidence and documentation. Historical work remains traceable through dated studies and Git history.
