# Architecture Decision Records

Required by the Engineering Programme Dossier and the TRB prompt. One file per decision, in a
fixed shape, so a decision can be audited without reading a narrative.

[`../DECISION_LOG.md`](../DECISION_LOG.md) is not superseded. It is the readable history
and remains the better document for understanding *how the project got here*. These records are
the structured view: what was decided, what else was considered, what it costs, and how it gets
validated. Where an ADR has a Context section, that prose usually came from the decision log.

## Template

```
# ADR-NNN, title

Status · Date · Phase
## Context, the forces at play, including what was not known
## Decision, what was decided, stated flatly
## Alternatives, what else was considered, and why it lost
## Consequences, what this costs, including the bad parts
## Validation, how we would find out this was wrong
```

The Consequences and Validation sections are the ones that matter. A record listing only
benefits is advocacy, not a decision record, and one with no validation path violates dossier
§7, every feature needs a path toward validation.

## Index

| ADR | Decision | Status | Phase |
|---|---|---|---|
| [001](001-electromagnetic-deployment.md) | Electromagnetic deployment instead of a spring | Accepted | Concept |
| [002](002-host-is-a-spent-upper-stage.md) | Host is a spent upper stage, not a free-flyer | Accepted | Concept |
| [003](003-linear-synchronous-motor.md) | Linear synchronous motor, not a coilgun | Accepted | Load-bearing |
| [004](004-ironless-stator.md) | Ironless stator | Accepted | I |
| [005](005-eddy-brake-not-regeneration.md) | Eddy-current brake; sled energy is dissipated | Accepted | I |
| [006](006-magnets-ride-the-sled.md) | Magnets ride the sled; the CubeSat is unmodified | Accepted | Load-bearing |
| [007](007-dual-transverse-cassettes.md) | Dual transverse cassettes | Accepted | I |
| [008](008-retention-gate.md) | Retention gate separates preload from release | Accepted | I |
| [009](009-coast-and-trim.md) | Coast-and-trim release zone | Accepted | I |
| [010](010-host-agnostic-interface.md) | Host-agnostic four-item interface | Accepted | I |
| [011](011-publish-publicly.md) | Publish publicly, defects included | Accepted | I |
| [012](012-adopt-measured-sled-mass.md) | Adopt the measured 9.445 kg sled | Accepted | I |
| [013](013-drop-invariance-claim.md) | Drop the lifetime-ratio invariance claim | Accepted | I |
| [014](014-fleet-setpoint-below-ceiling.md) | Fleet setpoint at 98.2 % of the open-loop ceiling | Accepted | I |
| [015](015-derive-not-paste.md) | Derive coupled values; never paste them | Accepted | I |
| [016](016-reconstructed-history.md) | Reconstruct git history with labelled dates | Accepted | I |
| [017](017-four-repositories.md) | Four repositories, two of them generated | Accepted | I |
| [018](018-programme-name.md) | VOLLEY is the programme name; EMOCD_ remains the part prefix | Accepted | Programme |
| [019](019-gen4-open-assembly-before-export.md) | Keep Gen4 open assembly separate from the Phase I baseline | Accepted | Gen4 transition |
| [020](020-inter-shot-cadence.md) | The inter-shot cadence is 1200 s, closing P31 | Accepted | Load-bearing |
| [021](021-freeze-the-register.md) | Freeze the defect register; measurement takes priority | Accepted | I |
| [022](022-stator-segmented-not-block-commutated.md) | Winding segmented for fault isolation, driven as one; closes P29 | Accepted | I |
| [023](023-target-host-class.md) | Target host is a spent upper stage, not an ESPA-Grande port; closes P9 | Accepted | I |
| [024](024-last-mile-delivery-conops.md) | VOLLEY is a last-mile delivery vehicle; plane change excluded | Accepted | I |
| [025](025-fixed-cell-manifest.md) | One cell geometry with class-specific inserts, not a cassette per class | Accepted | I |
| [026](026-cad-built-from-parameters.md) | The CAD is generated from parameters, not drawn | Accepted | I |
| [027](027-designed-velocity-loop.md) | The velocity loop is designed against margins; closes P47 | Accepted | I |
| [028](028-no-latex-in-the-flagship.md) | No LaTeX in the flagship; the manuscript is authored in VOLLEY-paper | Accepted | I |
| [029](029-phase-one-closes-on-gen5.md) | Phase I closes on Gen5; Gen6 is the Phase II design target | Accepted | I |
| [030](030-apply-the-depth-resolved-thrust-constant.md) | Apply the depth-resolved K_t and the three decisions beside it; moves the baseline | Accepted | I |
| [031](031-four-repositories-not-two-phases.md) | Four repositories by role, replacing the two-phase model | Accepted |, |
| [032](032-gen6-stage-integrated-gas-store.md) | Gen6 is a stage-integrated, payload-direct, gas-driven deployer; supersedes the Gen6 of ADR-029 | Accepted |, |
| [033](033-gen6-trim-stage.md) | Gen6 gains a motor that steers rather than throws, adopted with its pulse store unweighed (P77) | Accepted | I |
| [034](034-gen6-long-stroke-design-point.md) | Gen6's stroke becomes the host stage's whole 8.0 m, same velocity, half the acceleration, half the gas, and friction at 28.39 % of shot work (P78, P82, P83) | Accepted | I |
| [035](035-drive-tube-material.md) | The drive tube is hard-anodised aluminium and the piston matches it, closes P85, and forecloses steam | Accepted | I |
| [036](036-seal-specification-and-the-trim-stage.md) | The seal is specified at 17.8 N and the trim stage is suspended rather than built, closes P89, amends ADR-033, defers A66 | Accepted | I |

Every decision in `DECISION_LOG.md` appears above. ADRs 012-018 record decisions that were
never written down anywhere before.
