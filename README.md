# VOLLEY
### Commanded electromagnetic CubeSat deployment

**One host. Sequential deployment. A commanded release for each spacecraft.**

VOLLEY combines individually restrained satellite storage, guided feed and a reusable electromagnetic launch sled. The host provides the major orbital manoeuvres; VOLLEY supplies the local departure condition. **Gen5 ACR1** brings the storage-to-release cycle into one computational engineering reference, with native CAD, STEP assemblies, coupled motor/source calculations and matched orbital delivery studies.

[Explore the project](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Watch the deployment film](https://aaaaaaaaaaaavm.github.io/VOLLEY/delivery-film.html) · [Engineering package](validation/acr1/README.md) · [CAD and drawings](cad/README.md)

<p><a href="docs/assets/acr1/polish/assembly_hero.png"><img src="docs/assets/acr1/polish/assembly_hero.webp" alt="VOLLEY Gen5 ACR1 assembly: two satellite storage banks beside a central transfer and launch mechanism" width="900"></a></p>

*CAD-derived Blender render · Gen5 ACR1 home state. Teal identifies the feed and captive-pallet path. [Geometry and render provenance](docs/assets/acr1/polish/POLISH_PROVENANCE.json).*

| Reference configuration | Gen5 ACR1 |
|:--|:--|
| Payload manifest | Twelve 4 kg 3U envelope surrogates |
| Evaluated release commands | **1, 2 and 3 m/s** |
| Powered travel | **1.300 m** |
| Architecture | Two fixed six-cell banks; guided lead-screw feed; indexed lift; captive pallet and retained magnetic carrier |
| Installed mass basis | **149.557 kg** represented dry CAD + **7 kg** electrical/control allowance |
| Mission reference | Manoeuvring host in nominal 500 km SSO; common target-state epoch 24 hours after the final release |

## From storage to commanded release

1. **Retain** each satellite independently in its storage cell.
2. **Feed** the selected payload into the guided transfer cradle.
3. **Dock** the captive pallet to the launch carrier and prove receiving custody.
4. **Accelerate** using the finite linear synchronous motor and local energy source.
5. **Release** the satellite at the commanded departure condition.
6. **Arrest and recover** the retained carrier and pallet for the next cycle.

<p><a href="docs/assets/acr1/polish/operating_sequence.png"><img src="docs/assets/acr1/polish/operating_sequence.webp" alt="Four CAD-derived states showing storage, guided feed, pallet handoff and carrier launch" width="900"></a></p>

*CAD-derived operating sequence. The animation explains the mechanism; the linked motion and interlock records contain its computational checks.*

[Feeder detail](docs/assets/acr1/polish/feeder_detail_annotated.png) · [Native assembly states](validation/acr1/cad/release/FINAL_CAD_MANIFEST.json) · [Motion checks](validation/acr1/cad/release/MOTION_VERIFICATION.json) · [Command and fault specification](validation/acr1/analysis/TRANSFER_INTERLOCKS.json)

## Engineering results

| Study | Result | Inspect |
|:--|:--|:--|
| Mechanical integration | Eight native/STEP assembly states; 154 accepted sampled motion/refinement cases | [CAD exchange and verification](validation/acr1/cad/release/) |
| Launch and recovery | Eighteen source-coupled cases across nominal/adverse source conditions and 3/20/100 µH sensitivities | [Coupled shot and numerical audit](validation/acr1/verification/COUPLED_SHOT_REVIEW.md) |
| Chassis response | Matched ANSYS/CalculiX bare-chassis static comparison: 0.143% primary peak-displacement difference | [Loads, meshes and native-result readback](docs/ACR1_ANSYS_CROSSCHECK.md) |
| Orbital delivery | Twelve-release, common-target campaigns with changing host mass and recoil; nine native Orekit replay cases | [Mission study](validation/acr1/mission/MISSION_REPORT.md) |
| Installed-resource trade | Target-dependent service value; the tested preplanned cases favour ideal ground-pretrimmed springs on fuel and initial wet mass | [Same-target comparison](validation/acr1/mission/MISSION_RESULTS.csv) |

The study evaluates the complete retained-carrier system boundary, including its installed burden. It is a **computational design study**; measured release distributions, environmental qualification and provider acceptance belong to physical development. Each linked analysis states its assumptions and numerical checks.

## CAD, source and reproducibility

[Dimensioned A3 drawing set](cad/drawings/acr1/ACR1_DRAWING_SET.pdf) · [Drawing/BOM index](docs/ACR1_DRAWING_INDEX.md) · [Numerical methods](docs/SKILLS.md) · [Reproduction guide](validation/acr1/REPRODUCTION.md)

```bash
python3 validation/acr1/check_capture.py
python3 validation/acr1/reproduce.py interlocks --output /tmp/volley-acr1-interlocks
```

The engineering package contains configuration parameters, native CAD/STEP states, source, captured numerical outputs, software identities and manifests. The interlock example uses Python 3.12; native and scientific examples list their additional dependencies.

## Research beyond the academic reference

Higher-speed launchers and alternative payload interfaces are evaluated as separate configurations. The [research overview](docs/HIGHER_SPEED_DESIGN_SPACE.md) connects the current-model speed envelope, published experimental comparison, new 10 m/s designs and ideal lunar-delivery calculations. These studies preserve the Gen5 reference and its **1–3 m/s** evaluated command cases.

[Structural dynamics](docs/ACR1_STRUCTURAL_DYNAMICS.md) · [Release dynamics](docs/ACR1_RELEASE_DYNAMICS.md) · [Thermal study](docs/ACR1_THERMAL_ENVIRONMENT.md) · [First-test fixtures and procedures](docs/ACR1_FIRST_TEST_PACKAGE.md)

## Explore the project

| Repository | Purpose |
|:--|:--|
| **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | Integrated system, engineering results, CAD and project website |
| **[VOLLEY Labs](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)** | Research experiments, mechanism alternatives and design lineage |
| **[VOLLEY Thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis)** | Standalone academic report, presentation and supporting engineering record |
| **[VOLLEY Paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)** | IEEE-formatted manuscript, local methods, data and reproduction |

[Design history](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) · [Scientific figure conventions](docs/FIGURE_STANDARD.md) · [Citation](CITATION.cff) · [Licensing](LICENSING.md)
