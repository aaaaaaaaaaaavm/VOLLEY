# Adityavardhan Mishra

Mechanical engineering student · Spacecraft deployment, engines and systems software

BTech, Symbiosis Institute of Technology, Pune · 2023–2027

I like problems that survive the first calculation. My main project is **VOLLEY**, an investigation into controlled spacecraft departure from a retained orbital host. It began with a mechanism. The work since has been about finding out whether the mission earns that mechanism.

[Explore VOLLEY](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Explore BOLLEY](https://aaaaaaaaaaaavm.github.io/VOLLEY/bolley.html) · [Engineering record](https://github.com/aaaaaaaaaaaavm/VOLLEY) · [Contact](mailto:adityavardhanmishr@gmail.com)

<p align="center"><img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/cad/renders/sequence/gen5_operations_hero.png" alt="Four STEP-derived Blender views showing intended Gen5 operations; the evaluated reference fit and 3U mass criteria fail" width="100%"></p>

*The storyboard is conceptual motion from FreeCAD-linked STEP geometry, not a mechanism test. The current Gen5 academic evaluation fails its reference fit and 3U installed-mass criteria; final freeze is open. Nothing in VOLLEY or BOLLEY has been built, measured, qualified or flown. [Watch the eight-second Gen5 sequence](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/cad/renders/sequence/gen5_intended_sequence.mp4).*

## Start with the question, then inspect the evidence

| Project | What I am investigating | Useful starting point |
|---|---|---|
| **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | Can provider-hosted control of release velocity, direction and timing earn its installed mass and operating burden? | [Current status](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/NEXT_GENERATION_STATUS.md) |
| **[BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY)** | Does a passive spacecraft interface justify its mass by letting the launcher remove the moving sled and return mechanism? | [Selected winding and drive](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md) |
| **[GatewayCX](https://github.com/aaaaaaaaaaaavm/GatewayCX)** | How should ordinary network applications survive long delays and interrupted Earth–Moon links? | [Architecture and executable software evidence](https://github.com/aaaaaaaaaaaavm/GatewayCX#readme) |

## VOLLEY: evaluate one configuration, then decide what follows

Gen5 is the controlled computational configuration for academic review. Its historical periodic model returned **16.029 m/s at 10.07 g** and a **126.6 kg** modeled dry mass. A finite-geometry force screen challenges that speed with an ideal-phase **12.448 m/s** result; neither is a demonstrated release setting. The modeled **10.55 kg per 3U** fails the installed-mass screen, and the side-fed reference STEP assembly has an **11 mm width shortfall**. The final freeze remains open while these and other verification items are resolved or dispositioned.

**Gen6 is future scaling research toward a 1 km/s-class objective.** No mechanism, payload class or speed range is selected or validated. The independent motor-charged spring-cell bank and long gas guide remain unselected historical studies.

The mission work compares release authority with host manoeuvres and competent spring/timing alternatives. A historical two-payload screen found accepted cases under its assumptions, but the later matched twelve-shot reference does **not** close in any sampled case. Neither study establishes product value or a provider-approved mission.

What I want a reviewer to inspect:

- [The matched mission reference](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/MATCHED_MISSION_REFERENCE.md): one declared host, payload and target compared across release concepts.
- [The open-problem register](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/OPEN_PROBLEMS.md): corrections and failed claims remain visible.
- [The evidence boundary](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/PROVENANCE.md): model output, cross-checks, nominal CAD and missing measurement are kept distinct.
- [The reproduction route](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/CONTRIBUTING.md): acceptance criteria before execution, source hashes and executable checks.

The host supplies navigation, attitude control and permitted manoeuvres. The deployer supplies a release condition. It does not provide continuing stationkeeping or collision avoidance after the spacecraft leaves.

## BOLLEY: test the neighbouring premise

<p align="center"><img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/BOLLEY/main/cad/renders/gen3/01_gen3_hero.png" alt="BOLLEY Gen3 nominal Fluxrelay assembly" width="100%"></p>

BOLLEY gives the payload a modelled 0.37136 kg passive magnetic/copper interface while retaining the powered windings and electronics on the launcher. The current 4 kg reference duty is 11.8 m/s over 0.90 m at at most 8 g nominal.

The electrical partition moved from four turns at 380 A to twelve turns at 126.667 A. The first twelve-turn fit failed its copper-volume check; the failure is preserved. The later detailed winding passes its nominal CAD bands, while field distribution, hot switching, manufacturing tolerances and installed mass still need closure.

[Current BOLLEY evidence](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md) · [What remains unresolved](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/OPEN_PROBLEMS.md)

## Smaller tools extracted from the work

| Repository | Reusable capability |
|---|---|
| [Pulsed Linear Motor Design Lab](https://github.com/aaaaaaaaaaaavm/pulsed-linear-motor-design-lab) | Force, stroke, moving-mass and source-impedance screens |
| [Orbital Deployment Trade Study](https://github.com/aaaaaaaaaaaavm/orbital-deployment-trade-study) | Two-body release, recoil and phase-drift comparisons |
| [Engineering Evidence Toolkit](https://github.com/aaaaaaaaaaaavm/engineering-evidence-toolkit) | Source, result, link and artifact consistency checks |
| [constraint-floor](https://github.com/aaaaaaaaaaaavm/constraint-floor) | Requirement-attributed mass lower bounds |
| [parametric-cad-evidence-pipeline](https://github.com/aaaaaaaaaaaavm/parametric-cad-evidence-pipeline) | Parameter-to-artifact provenance and build manifests |
| [spacecraft-separation-dynamics](https://github.com/aaaaaaaaaaaavm/spacecraft-separation-dynamics) | Impulse, recoil, tip-off and internal-mass screens |
| [gatewaycx-bearer-sdk](https://github.com/aaaaaaaaaaaavm/gatewaycx-bearer-sdk) | Bearer adapters and conformance checks |
| [disruption-network-lab](https://github.com/aaaaaaaaaaaavm/disruption-network-lab) | Scheduled-contact delivery experiments |
| [scientific-run-registry](https://github.com/aaaaaaaaaaaavm/scientific-run-registry) | Content-addressed computational runs and lineage |

These are narrow tools with explicit assumptions. Software tests and model agreement do not establish hardware performance.

## Beyond the repositories

I contributed to Team THRUST's payload-deployment work for the payload that placed second in the SDL Payload Challenge at IREC 2025. I work on Formula Student powertrain, motorcycle engines and ECU calibration, and run Poona Motor Club. Reverse-engineering Powertronic's map format led me to build a dual-map editor.

My engineering work uses Python for numerics and traceability, parametric CAD, field and structural solvers, and independent checks of equations and units. [The skills evidence map](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/SKILLS.md) points to the actual files.

[VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) holds the standalone IEEE-formatted Gen5 manuscript and evidence package; it has not been submitted. [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) holds the standalone college review, report, presentation and local evidence. [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) preserves exploratory and rejected branches.

[adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) · [LinkedIn](https://www.linkedin.com/in/adityavardhanmishra/) · Pune, India
