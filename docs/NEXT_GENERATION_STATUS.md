# VOLLEY configuration status

**25 October 2026.** VOLLEY-G5-ACR1 is the completed integrated computational reference. Gen6 contains separately versioned mixed-size feeder and service studies and the proposed physical development stage.

| Configuration | Role | Evidence boundary |
|:--|:--|:--|
| [VOLLEY-G5-ACR1](../validation/acr1/README.md) | Current integrated academic reference | Twelve 4 kg 3U surrogates; eight native/STEP states, 154 motion/refinement checks and modeled 1–3 m/s cases |
| [Original Gen5](GEN5_TECHNICAL_BASELINE.json) | Historical electromagnetic comparison | Its original speed, mass, geometry and adverse findings retain their source identity |
| [FM08-R3 mixed-size feeder](../validation/selected_feeder/README.md) | Selected guided lead-screw subsystem and design lineage | Two 1U/two 3U surrogates, fixed 1U spacers and indexed receiver; separate geometry from ACR1 |
| [Four/twelve-payload Gen6 capacity studies](../validation/system_feasibility_closure/README.md) | Separate integration and installed-burden investigations | Declared mixed-size manifests and surrogate host assumptions; no approved host envelope |
| [Seven feeder concepts](GEN6_FEEDER_CONCEPT_TRADE.md) | Architecture trade and retained alternatives | Rack-and-pawl runner-up; scores are engineering judgments rather than measured reliability |
| [Lunar and higher-speed programme studies](PROGRAMME_STUDIES_ACR1.md) | Separately identified feasibility and incompatibility findings | Each source package identifies completed calculations and remaining criteria; no achieved hardware capability |

## Current engineering result

ACR1 uses guided pushers, a restrained indexed cradle and a single pallet that remains with the carrier during launch, arrest and return. Represented CAD dry mass is 149.556720 kg; the separate 7 kg electrical/control allowance gives 156.556720 kg device mass for mission accounting. It has no assigned position in CAD inertia.

The same-revision shot model supports 1–3 m/s computational commands, including active source-aware arrest. The complete timestep audit covers the six principal 3 m/s cases. Nominal geometry, numerical checks and catalog-based sizing define the study boundary; physical repeatability, environmental qualification and provider acceptance require subsequent evidence.

## Mission and development boundaries

The current ACR1 comparison uses twelve releases from a generic 500 kg initial wet bus in nominal 500 km SSO. Full position/velocity targets share an epoch 24 hours after the final release. The tested preplanned families show no propellant or initial wet-mass advantage over ideal ground-pretrimmed springs. [Mission evidence](../validation/acr1/mission/MISSION_REPORT.md).

The earlier mixed four-payload mission, original Gen5 campaigns and historical 16.029/12.448 m/s models remain separate studies. They do not set ACR1 commands or demonstrate customer value. Future physical mixed-size handling requires its own interfaces, restraints, motion, source and mass checks. [Prototype review requirements](PROTOTYPE_READINESS.md) identify those evidence stages.
