# VOLLEY

**Programmable CubeSat deployment from a controlled upper stage.**

I am developing a deployer that gives each secondary payload a chosen release velocity after the
primary mission. The host supplies coarse orbital placement where its capability and mission
rules permit; VOLLEY supplies the individual separation condition. Keeping the payload
mechanically and electrically unmodified is the design objective. Compatibility is not yet demonstrated.

**Computational design study. Nothing has been built, fired, measured, qualified or flown.**

[Start with the evidence](docs/GEN5_CLOSURE.md) · [Current work](docs/STATE_OF_THE_PROJECT.md) ·
[Prototype programme](docs/PROTOTYPE_READINESS.md) · [CAD](cad/README.md) ·
[IEEE-formatted manuscript](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)

![Mission and evidence boundary](figures/V00_system_overview.svg)

This overview is generated from committed inputs by `tools/make_repo_overview.py`.
Gen5 and Gen6 share a mission; they do not share a completed evidence base.

## Two configurations, different maturity

| | Gen5: frozen electromagnetic baseline | Gen6: active gas-driven investigation |
|---|---|---|
| Drive | Ironless double-sided Halbach linear synchronous motor and reusable sled | Closed gas expansion along an approximately 8 m stage-integrated guide |
| Purpose in this record | Reproducible comparison case and manuscript baseline | Investigate removal of the full pulse chain, sled, brake and return stroke |
| Release velocity | **16.029 m/s**, model output at the frozen point | **29.009 m/s**, a design-point calculation, not established integrated performance |
| Evidence | Field, structural, circuit, orbit and other numerical studies with run-specific limitations | Gas/campaign studies and geometry; unresolved guide-contact and release-state prediction |
| Principal limits | Failed mass comparison, pulse-store feasibility and payload magnetic environment | Contact-model credibility, velocity accuracy, conducting-tube/trim interaction and actual host interfaces |
| Design status | Frozen with explicit exceptions | Not frozen; trim stage suspended |

<table>
<tr>
<td width="50%"><img src="cad/renders/gen5/hero_open.png" alt="Gen5 electromagnetic assembly with enclosure open"></td>
<td width="50%"><img src="cad/renders/gen6/hero_open.png" alt="Gen6 stage-integrated gas architecture study"></td>
</tr>
<tr><td><b>Gen5 geometry.</b> The analysed electromagnetic comparison case.</td><td><b>Gen6 geometry.</b> An architecture study, not a released manufacturing assembly.</td></tr>
</table>

The [baseline](docs/BASELINE.md) owns Gen5 numbers. The [live register](OPEN_PROBLEMS.md) owns
limitations. Historical renders and earlier generations are indexed in [GENERATIONS.md](docs/GENERATIONS.md).

## What the work has established

- The frozen Gen5 model produces a commanded release condition. Its net electrical-to-payload
  efficiency is **18.8%** and its modelled dry mass is **126.6 kg**. Those figures include assumptions
  and do not establish a purchasable, qualified system.
- Independent numerical paths exist for selected field, structure, circuit and orbit questions.
  Their scope is listed in [PROVENANCE.md](docs/PROVENANCE.md). Agreement is a cross-check, not an experiment.
- The mass comparison and original constellation-phasing argument failed. A spring and release
  timing remain legitimate controls in the mission trade. [The exceptions](docs/GEN5_CLOSURE.md)
  are part of the result.
- A nominally consistent model can still be physically wrong. The guide/contact work found
  geometry and contact-law problems that require further analysis before a tip-off prediction
  can support a build decision.

<p align="center">
<img src="figures/A02_field_map.png" width="32%" alt="Computed depth-resolved magnetic field">
<img src="figures/F01_shot.png" width="32%" alt="Modelled Gen5 shot histories">
<img src="figures/A35_ledger.png" width="32%" alt="Mass attributed to requirements">
</p>

These are numerical results from the committed analysis, not measurements. The
[figure index](docs/FIGURE_INDEX.md) and run sheets provide the source and limits.

## What controls the next build decision

1. **Useful release velocity.** Resolve P113 against host-provided orbital energy, spring release
   and release timing. More velocity must earn its mass and integration cost.
   [The departure-state screen](docs/DEPARTURE_TRADE.md) begins that comparison;
   [host compatibility](docs/HOST_COMPATIBILITY.md) separates public evidence from missing interfaces.
   [Sequential allocation](docs/CAMPAIGN_ALLOCATION.md) adds host propagation and propellant accounting;
   [programme execution](docs/PROGRAMME_EXECUTION.md) records the architecture decision gates.
   [Terminal-state timing](docs/TERMINAL_TIMING.md) compares identical position/velocity targets
   and release-time searches for one payload; it does not establish a manifest optimum.
2. **A credible exit-state envelope.** Resolve P103/P108: corrected guide shape, contact-law
   verification, penetration/convergence, friction, inertia and tolerance effects.
3. **One coherent Gen6 configuration.** A72–A74 do not support treating the present magnetic
   secondary and conducting tube as a solved combination. Resolve P92 before promoting a trim design.
4. **A complete prototype package.** Selected parts, load paths, clearances, full mass and energy
   budgets, fault response, drawings, assembly instructions and an instrumented test plan.

[PROTOTYPE_READINESS.md](docs/PROTOTYPE_READINESS.md) defines the work packages and their exit
products for VOLLEY and BOLLEY. [COMPUTATIONAL_CLOSURE.md](docs/COMPUTATIONAL_CLOSURE.md)
counts the active Gen6 analysis backlog. Neither document declares the work complete.

## Review routes

| What you want to inspect | Start here |
|---|---|
| The concept and current state | [CONCEPT](docs/CONCEPT.md), [STATE_OF_THE_PROJECT](docs/STATE_OF_THE_PROJECT.md) |
| The frozen result and its failures | [BASELINE](docs/BASELINE.md), [GEN5_CLOSURE](docs/GEN5_CLOSURE.md) |
| Source and limits of a claim | [PROVENANCE](docs/PROVENANCE.md), [validation](validation/README.md), [OPEN_PROBLEMS](OPEN_PROBLEMS.md) |
| Mechanical design and remaining build work | [CAD](cad/README.md), [BUILD_READINESS](docs/BUILD_READINESS.md), [Gen6 handoff](docs/GEN6_FUSION_BUILD_PACKAGE.md) |
| Host requirements and mission value | [MISSION_ARCHITECTURE](docs/MISSION_ARCHITECTURE.md), [HOST_REFERENCE_CASES](docs/HOST_REFERENCE_CASES.md), [CASE_STUDY](docs/CASE_STUDY.md) |
| Experiments and qualification planning | [BENCHTOP_TESTS](docs/BENCHTOP_TESTS.md), [QUALIFICATION_PLAN](docs/QUALIFICATION_PLAN.md) |
| Decisions and earlier configurations | [LINEAGE](docs/LINEAGE.md), [DECISION_LOG](docs/DECISION_LOG.md), [GENERATIONS](docs/GENERATIONS.md) |
| A short account of my engineering work | [SUMMARY](SUMMARY.md), [SKILLS](docs/SKILLS.md) |

## Reproduce

Use Python 3.12 or newer and a full-history clone. The companion provenance check needs the
recorded export commit in the local history.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
bash tools/verify_all.sh
```

Run from a clean committed checkout. The command checks repository consistency and the numerical
checks it lists; it does not rerun every external solver or certify the design. Missing checks
must remain visible. CAD and external solver setup are described in [CONTRIBUTING.md](docs/CONTRIBUTING.md)
and [tools/env-setup.sh](tools/env-setup.sh).

## The programme

| Repository | Role |
|---|---|
| **VOLLEY** | Flagship engineering record and unmodified-payload design objective |
| [BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY) | Sister project: passive spacecraft interfaces in exchange for different launcher machinery |
| [VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) | Authored Gen5 manuscript and exported reproducibility evidence |
| [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) | Gen5 submission material and exported evidence |
| [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) | Stopped alternatives and the conditions for reopening them |

The long-form account previously on this page remains in
[the preceding revision](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/67939b7cbef9e2414226f683ebc12f2b6bf01088/README.md).
It is a historical snapshot; the current evidence routes above govern present claims.

## Author and use

**Adityavardhan Mishra** · Mechanical Engineering, Symbiosis Institute of Technology, Pune.
Project begun April 2021. [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com)

I welcome independent reproduction, design review and prototype collaboration. Please identify
the configuration and run when reporting a discrepancy.

[CC BY 4.0](LICENSE). See [NOTICE](NOTICE), [LICENSING.md](LICENSING.md) and [CITATION.cff](CITATION.cff)
for attribution and scope. Historical snapshots retain the terms under which they were released.
