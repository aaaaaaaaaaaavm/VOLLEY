# VOLLEY

### Commanded electromagnetic CubeSat deployment

VOLLEY combines restrained CubeSat storage, guided feed, a captive transfer pallet and a reusable electromagnetic launch sled on a maneuvering host. The current **VOLLEY-G5-ACR1** academic reference carries **twelve 4 kg 3U envelope surrogates** and evaluates commanded release settings of **1, 2 and 3 m/s** over **1.300 m** powered travel.

[Project website](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Current engineering package](validation/acr1/README.md) · [CAD and STEP](cad/README.md) · [Numerical evidence](docs/CURRENT_NUMERICAL_EVIDENCE.md)

<p><a href="docs/assets/acr1/polish/assembly_hero.png"><img src="docs/assets/acr1/polish/assembly_hero.webp" alt="CAD-derived render of all 387 represented VOLLEY Gen5 ACR1 parts in the home pose; teal marks the selected feed and captive-pallet path." width="760"></a></p>

*CAD-derived Blender render · ACR1 home pose · all 387 represented objects present. Teal identifies the selected feed/pallet path; surface colours are display choices. [View provenance](docs/assets/acr1/polish/POLISH_PROVENANCE.json).*

[Guided-feed close-up](docs/assets/acr1/polish/feeder_detail_annotated.png) · [Four-state custody sequence](docs/assets/acr1/polish/operating_sequence.png) · [Caption and visibility notes](docs/assets/acr1/polish/CAPTIONS.md)


[Watch the complete storage-to-orbit film](https://aaaaaaaaaaaavm.github.io/VOLLEY/delivery-film.html) · [Download MP4](docs/films/delivery-journey/film.mp4) · [Editable film sources](docs/downloads/VOLLEY_delivery_film_sources.zip)

## How the machine works

Two fixed six-cell banks retain the payloads individually. Guided lead-screw pushers transfer one satellite to the indexed captive cradle. The cradle docks a reusable pallet to the launch sled and withdraws before arming. The sled accelerates the payload; release cams open the restraint, active electromagnetic arrest stops the retained sled, and the pallet returns with it. The executable sequence requires custody, path, source and brake proofs before launch.

[Eight native/STEP assembly states](validation/acr1/cad/release/FINAL_CAD_MANIFEST.json) · [Installed motion verification](validation/acr1/cad/release/MOTION_VERIFICATION.json) · [Command and fault specification](validation/acr1/analysis/TRANSFER_INTERLOCKS.json)

[Dimensioned drawing set](cad/drawings/acr1/ACR1_DRAWING_SET.pdf) · [Drawing, BOM and inspection index](docs/ACR1_DRAWING_INDEX.md)

## What this revision delivers

| Current ACR1 result | Evidence and interpretation |
|:--|:--|
| Eight FreeCAD/STEP states; 154 accepted motion checks | Nominal geometry, custody and installed motion/refinement; independent STEP readback |
| Supported commands 1–3 m/s | Eighteen averaged source/release/arrest cases across nominal/adverse source and 3/20/100 µH sensitivities |
| 149.556720 kg CAD dry mass | Plus a separate 7.000 kg installed power/control allocation; mission device mass 156.556720 kg |
| Twelve releases from a 500 km nominal SSO host | Common position/velocity target epoch 24 h after final release; nine independent Orekit replays |
| Same-target spring comparison | No propellant or initial wet-mass advantage over the ideal ground-pretrimmed spring comparator in the tested preplanned cases |

[Configuration and resource basis](validation/acr1/ENGINEERING_DEFINITION_R1.json) · [Coupled model and audit](validation/acr1/verification/COUPLED_SHOT_REVIEW.md) · [Mission findings](validation/acr1/mission/MISSION_REPORT.md)

These are computational design results. The project has no measured release performance or flight qualification. Catalog ratings, synthetic mission targets and tolerance/material allocations retain their declared boundaries. The additional 7 kg is included in mission mass and has no spatial assignment in CAD inertia.

## Reproduce and inspect

The self-contained [ACR1 package](validation/acr1/README.md) includes exact sources, inputs, all eight native/STEP states, result JSON, mission command/replay outputs, software locks and hash manifests. Its portable runner executes selected examples in a new scratch directory.

```bash
python3 validation/acr1/check_capture.py
python3 validation/acr1/reproduce.py interlocks --output /tmp/volley-acr1-interlocks
python3 tools/prepublish_gate.py --all
```

The interlock example needs only Python 3.12; scientific/native examples have their own [pinned dependencies and instructions](validation/acr1/REPRODUCTION.md). Large raw solver supplement availability is recorded explicitly in its asset inventory. Vendor documents are linked to their publishers.

## Extended engineering studies

[ANSYS–CalculiX chassis cross-check](docs/ACR1_ANSYS_CROSSCHECK.md) · matched 3.01048 kN opposed-patch loads, three mesh levels and independently read native results.

[Structural modes and motor normal reaction](docs/ACR1_STRUCTURAL_DYNAMICS.md) · [Native release/contact dynamics](docs/ACR1_RELEASE_DYNAMICS.md) · [Thermal interfaces and source derating](docs/ACR1_THERMAL_ENVIRONMENT.md) · [Finite-host lunar campaigns](docs/PROGRAMME_STUDIES_ACR1.md) · [First-test procedures and fixture STEP](docs/ACR1_FIRST_TEST_PACKAGE.md)

These separately identified studies add native solver histories, refinement, resource flowdown and a concrete path to subsequent measurements. Their operating conditions and source identities accompany each result.

### Partial-occupancy mission comparison

The [two/four-payload supplement](validation/acr1_partial_occupancy/REPORT.md) adds 28 finite-force candidate trajectories and 17 native Orekit replays. Its [common-case tables](validation/acr1_partial_occupancy/technical/README.md) compare two, four and twelve deployments while retaining the complete hardware mass. The accepted twelve-payload academic issue remains unchanged.

[Higher-speed design constraints and Gen6 attached-shoe trade](docs/HIGHER_SPEED_DESIGN_SPACE.md) · unchanged-configuration screen and separately identified research bounds.

## Engineering lineage

Original Gen5's 12.448 m/s finite-geometry screen, 16.029 m/s periodic model, 126.562 kg represented dry mass and original 11 mm packaging shortfall remain **historical, separately identified evidence**. The FM08 mixed-size lead-screw subsystem and seven-concept ranking explain architecture development; they do not replace the integrated ACR1 twelve-3U geometry.

[Original Gen5 technical record](docs/GEN5_TECHNICAL_BASELINE.json) · [Earlier FM08 feeder and trade](validation/selected_feeder/README.md) · [Pre-ACR1 front page](README_PRE_ACR1_2026-10-23.md) · [Research archive](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)

## Project editions

[Thesis: report and presentation](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) · [Paper: manuscript and methods](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) · [Labs: alternatives and investigations](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)

The manuscript remains IEEE-formatted and unsubmitted; a venue is unselected. Mixed-size Gen6, lunar, higher-speed and hardware-development studies retain their own identities and acceptance criteria. The current engineering release does not imply programme-wide completion.
