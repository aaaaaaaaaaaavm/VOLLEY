# VOLLEY

### A computational design study for sequential CubeSat deployment

VOLLEY studies a host-mounted electromagnetic machine that would feed ordinary 3U CubeSats through one reusable launch path and command an individual departure speed for each release. **Gen5 is the fixed academic design baseline.** Gen6 is a separate, future scaling programme toward a 1 km/s-class objective; it has no selected mechanism or validated performance.

![Conceptual host and sequential departures](docs/assets/hero_departure.svg)

*Mission concept illustration. No host, launch provider, CubeSat, flight interface or trajectory has been approved for this design.*

**Read first:** [Gen5 technical closure](docs/GEN5_CLOSURE.md) · [Full baseline](docs/BASELINE.md) · [Evidence provenance](docs/PROVENANCE.md) · [Open problems](OPEN_PROBLEMS.md) · [CAD](cad/README.md) · [Validation](validation/README.md)

> **Evidence status, October 2026.** This is a complete *computational design study*, with a fixed configuration, documented methods, reproducible outputs and explicit failed criteria. It is **not** a complete physical product. No VOLLEY article has been built, fired, measured, qualified or flown; no complete installed-system or provider-specific interface has been validated. Published work on related systems is prior art and a source of assumptions, not a physical test of Gen5.

## One machine, one evaluated configuration

Gen5 uses a 1.5 m track (1.3 m powered stroke), double-sided ironless Halbach linear synchronous drive, reusable permanent-magnet sled, eddy-current arrest, capacitor pulse store and a conceptual twelve-payload magazine. The satellite is intended to remain mechanically and electrically unmodified. The modeled acceleration is **10.07 g**, but that value does not qualify any real payload.

<p align="center"><img src="cad/renders/gen5/hero_open.png" alt="Rendered Gen5 electromagnetic deployer, open configuration" width="68%"><br><sub>Gen5 CAD rendering; geometry and mass model, not fabricated hardware.</sub></p>

| Gen5 model output | Result | Evidence boundary |
|:--|--:|:--|
| 3U exit speed | **16.029 m/s** | Calculated shot, not measured or a demonstrated command range |
| Peak modeled acceleration | **10.07 g** | Payload-specific qualification remains open |
| Dry / loaded mass | **126.6 / 174.6 kg** | CAD-derived design mass; not complete installed-system mass |
| Electrical-to-payload efficiency | **18.8%** | Circuit and mechanics model, net of modeled recovery |
| Closed-loop exit-speed dispersion | **0.0274 m/s, 3σ** | Simulation with assumed sensor noise; not measured repeatability |
| Mass per carried 3U | **10.547 kg** | **Fails** the study's 2 kg/satellite economic screen by about 5.3× |

Values and definitions are in [the baseline](docs/BASELINE.md); scripts and machine-readable outputs are in [analysis](analysis/) and [validation](validation/). The [Gen5 closure](docs/GEN5_CLOSURE.md) records corrections and failed bands as part of the result.

## See the evidence, including what failed

<p align="center"><img src="figures/A02_field_map.png" alt="Calculated magnetic airgap field" width="32%"> <img src="figures/F01_shot.png" alt="Calculated Gen5 shot history" width="32%"> <img src="figures/A35_ledger.png" alt="Requirement-attributed mass floor" width="32%"></p>

*Field model → modeled shot → mass verdict. The 2-D and 3-D field comparisons check selected field quantities; they do not independently validate the full depth-integrated thrust or hardware performance. The mass ledger leaves **88.67 kg (70.06%)** in its most favorable evaluated requirement-deletion corner, so the evaluated corners cannot meet the mass screen. [Methods and limits](docs/GEN5_CLOSURE.md).*

| Question | Best available answer | Where to inspect it |
|:--|:--|:--|
| Does the field model agree with other methods? | Analytic field compared with magpylib and meshed 2-D/3-D field solves; checks apply to stated field quantities. | [A1](validation/A1_field_femm.md), [validation register](validation/README.md) |
| Does the electrical shot model agree with circuit simulation? | ngspice cross-check also exposed an omitted bank resistance loss. | [Gen5 closure](docs/GEN5_CLOSURE.md), [validation register](validation/README.md) |
| Does the CAD survive all criteria? | No. The revised enclosure is **50.04 kg**; dry mass and per-payload mass exceed the study screen. | [CAD record](cad/README.md), [mass ledger](validation/A35_constraint_ledger.md) |
| Does a complete twelve-payload mission close? | No complete delivery in the six sampled finite-burn cases; best case delivered **5/12**. This is a bounded screen, not an impossibility proof. | [Finite-burn study](docs/MANIFEST_FINITE_BURN.md) |
| Has the concept been independently tested? | Selected numerical cross-checks exist. Hardware, host integration, release reliability and payload compatibility remain untested. | [Provenance](docs/PROVENANCE.md), [open problems](OPEN_PROBLEMS.md) |

<p align="center"><img src="figures/manifest_timing.svg" alt="Bounded two-payload mission timing screen" width="49%"> <img src="figures/operational_uncertainty.svg" alt="Operational uncertainty study" width="49%"></p>

*These are model studies with stated assumptions. The sampled 4.57 m/s two-payload point is a mission-screen result, not a launcher maximum or a validated setting. [Timing assumptions](docs/MANIFEST_TIMING.md) · [Uncertainty study](docs/OPERATIONAL_UNCERTAINTY.md).*

## Inspect the hardware definition

<p align="center"><img src="cad/renders/gen5/exploded.png" alt="Exploded Gen5 CAD model" width="49%"> <img src="figures/D02_layout.png" alt="Gen5 layout drawing" width="49%"></p>

The [Gen5 STEP parts](cad/step/gen5/), [renders](cad/renders/gen5/), [layout](figures/D02_layout.png) and [CAD audit](cad/README.md) are reviewable design artifacts. They establish a modeled geometry and expose packaging and load-path questions. They are not manufacturing drawings, tolerance stacks, an approved ICD or proof of buildability.

## From study to product

![Sequence from host preparation to repeated release](docs/assets/mission_sequence.svg)

The sequence above is the product intent. The decisive next gates are a named host and deployment ICD; complete installed mass and thermal, power and structural budgets; feeder, retention, recoil and jam-recovery design; payload-specific loads; uncertainty and full-manifest mission closure; then representative calibrated multi-shot hardware testing. The [gap register](OPEN_PROBLEMS.md) keeps failed and unrun items visible.

For **Gen6**, the 1 km/s-class goal is only a research target. Ideal constant-acceleration scaling gives about **5.1 km of stroke at 10 g** or **204 m at 250 g** for 1 km/s, before losses, arrest, thermal design or payload qualification. A radically different payload class, host or architecture may be required. [Scaling illustration](docs/assets/scaling.svg) · [programme decisions](docs/PROGRAMME_EXECUTION.md).

## Explore the programme

| Repository | What a reader gets |
|:--|:--|
| **This repository** | Full engineering record, code, results, CAD, validation and unresolved defects |
| [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) | Self-contained final-year manuscript, college review material and local evidence package |
| [VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) | Self-contained IEEE-formatted manuscript and reproducibility package; venue not yet selected |
| [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) | Explored, rejected or gated alternative architectures and the reasons they stopped |

**Reproduce and audit:** [verification entry point](tools/verify_all.sh) · [figure index](docs/FIGURE_INDEX.md) · [literature](docs/LITERATURE.md) · [prior art](docs/PRIOR_ART.md) · [change history](CHANGELOG.md). Review acceptance bands and failures before citing any headline number.
