# Adityavardhan Mishra

Mechanical engineering student · Spacecraft deployment, engines and systems software

BTech, Symbiosis Institute of Technology, Pune · 2023–2027

I like problems that survive the first calculation. My main project is **VOLLEY**, an investigation into controlled spacecraft departure from a retained orbital host. It began with a mechanism. The work since has been about finding out whether the mission earns that mechanism.

[Explore VOLLEY](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Explore BOLLEY](https://aaaaaaaaaaaavm.github.io/VOLLEY/bolley.html) · [Engineering record](https://github.com/aaaaaaaaaaaavm/VOLLEY) · [Contact](mailto:adityavardhanmishr@gmail.com)

<p align="center"><img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/cad/renders/gen5/hero_open.png" alt="Frozen Gen5 electromagnetic comparison model, not the current release-cell reference" width="100%"></p>

*The image is nominal CAD of the frozen Gen5 comparator. VOLLEY and BOLLEY are computational design studies. Nothing in either project has been built, measured, qualified or flown.*

## Start with the question, then inspect the evidence

| Project | What I am investigating | Useful starting point |
|---|---|---|
| **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | Can provider-hosted control of release velocity, direction and timing earn its installed mass and operating burden? | [Mission and current reference](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/GEN6_REFERENCE_ARCHITECTURE.md) |
| **[BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY)** | Does a passive spacecraft interface justify its mass by letting the launcher remove the moving sled and return mechanism? | [Selected winding and drive](https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md) |
| **[GatewayCX](https://github.com/aaaaaaaaaaaavm/GatewayCX)** | How should ordinary network applications survive long delays and interrupted Earth–Moon links? | [Architecture and executable software evidence](https://github.com/aaaaaaaaaaaavm/GatewayCX#readme) |

## VOLLEY: the mechanism has changed because the results changed

The frozen electromagnetic Gen5 model gives 16.029 m/s at 10.07 g, with a 126.6 kg dry mass. Its mass comparison failed. I retain that design, its nominal CAD, structural and field studies, and the calculations that rejected its original mass claim.

The current reference is an **independent retained release cell with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. The earlier long gas guide remains a comparator. Neither inherits Gen5's evidence.

The mission work compares release authority with host manoeuvres and competent spring/timing alternatives. The two-payload study retained 100 tested campaign cases, 44 of which met its terminal-state bands. Higher available ejection speed did not automatically reduce fuel: three authority screens tied at the same best tested point. That is a bounded result, not an optimum or a provider-approved mission.

What I want a reviewer to inspect:

- [The campaign calculation](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/MANIFEST_TIMING.md): one evolving host, explicit payload order and terminal position/velocity.
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

[VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) holds the authored Gen5 manuscript and generated evidence snapshot. [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) holds the thesis work. [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) preserves exploratory and rejected branches.

[adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) · [LinkedIn](https://www.linkedin.com/in/adityavardhanmishra/) · Pune, India
