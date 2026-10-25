# VOLLEY-G5-ACR1 engineering package

**Current academic reference, captured 24–25 October 2026.** Twelve 4 kg 3U envelope surrogates occupy two fixed six-cell banks. Guided lead-screw pushers feed a vertical captive cradle; one reusable pallet transfers to the retained launch sled, which accelerates, releases the payload, arrests and returns. The pallet remains with the sled.

| Quantity | Current evidence |
|:--|:--|
| Commanded powered travel | 1.300 m |
| Supported modeled commands | 1, 2 and 3 m/s; 18 nominal/adverse source and 3/20/100 µH cases |
| Geometry | Eight frozen FreeCAD/STEP states; 154 accepted installed-motion/refinement cases |
| Represented CAD dry mass | 149.556720 kg |
| Installed power/control allocation | Additional 7.000 kg; no assigned position in CAD inertia |
| Device mass used by mission | 156.556720 kg; loaded device 204.556720 kg |
| Retained sled with pallet | 13.127806 kg |
| Mission | Twelve releases from one 500 km nominal SSO host; common full-state epoch 24 h after final release |
| Independent mission replay | Nine Orekit cases; numerical agreement under the common fixed-axis J2 model |

Original Gen5 (126.562 kg / historical 12.448 and 16.029 m/s screens) and the FM08 mixed-size subsystem remain separately identified historical studies. Their operating points do not describe ACR1.

## Inspect the evidence

- [Configuration and mass definition](ENGINEERING_DEFINITION_R1.json), [assembly parameters](cad/PARAMETERS.json), [installed-resource ledger](analysis/RESOURCE_LEDGER.json).
- [Eight-state inventory](cad/release/FINAL_CAD_MANIFEST.json), [native home assembly](cad/release/VOLLEY_G5_ACR1_home.FCStd), [home STEP](cad/release/VOLLEY_G5_ACR1_home.step). Every state has its native/STEP/JSON sibling in `cad/release/`.
- [Motion capture](cad/release/MOTION_VERIFICATION.json), [final refinement](cad/release/FINAL_REFINEMENT_VERIFICATION.json), [independent STEP readback](verification/FINAL_STEP_READBACK_SUMMARY.json), [mass/CG/inertia](verification/MASS_CG_INERTIA_SUMMARY.json).
- [Coupled source/release/arrest cases](analysis/COUPLED_SHOT.json), [equation and timestep audit](verification/COUPLED_SHOT_REVIEW.md), [winding](cad/WINDING_INTERFACE.json), [design budgets](analysis/DESIGN_BUDGETS.json), [interlocks](analysis/TRANSFER_INTERLOCKS.json).
- [Same-target mission findings](mission/MISSION_REPORT.md), [input/target map](mission/README.md), [native replay checks](mission/NATIVE_REPLAY_CHECKS.json), [software and jar lock](mission/SOFTWARE_LOCK.json).
- [Scientific software capture](release/SOFTWARE_ENVIRONMENT.json), [exact promotion identities](PROMOTION_ORIGIN.json), [public payload manifest](MANIFEST.json).

The full mission comparison finds **no propellant or initial wet-mass advantage over the ideal ground-pretrimmed spring comparator** in these preplanned targets. The 84.556720 kg retained-device penalty is included explicitly. Failed 4.5/6 m/s investigations stay in the shot output; they do not expand the supported range.

## Reproduce a short example

From the repository root, with Python 3.12:

```bash
python3 validation/acr1/check_capture.py
python3 -m venv .venv-acr1
.venv-acr1/bin/python -m pip install -r validation/acr1/requirements.txt
.venv-acr1/bin/python validation/acr1/reproduce.py interlocks --output /tmp/volley-acr1-interlocks
```

The example exercises actual nominal, missing-proof and custody-fault cases in the executable state specification. `reproduce.py` copies the public payload into the requested new directory, runs there and writes a receipt, leaving the checked captures intact. Use a fresh output directory for each run.

```bash
.venv-acr1/bin/python validation/acr1/reproduce.py shot --output /tmp/volley-acr1-shot
.venv-acr1/bin/python validation/acr1/reproduce.py mission --output /tmp/volley-acr1-mission
.venv-acr1/bin/python validation/acr1/reproduce.py native --download-jars --output /tmp/volley-acr1-native
```

`shot` recomputes the averaged source/motor/release/arrest cases from captured finite-force and resistance inputs. `mission` recomputes the synthetic targets and bounded policy set. `native` requires Java 21 and verifies each Orekit/Hipparchus jar against the published lock before executing the independent replay; `--jars /path/to/jars` uses an existing matching installation. Replays use frozen mission command CSVs unless the scratch mission outputs are deliberately substituted. Full examples are longer than the state-specification example.

## Native and secondary model rebuilds

FreeCAD **1.0.0 / OpenCASCADE 7.8.1** is required for native construction. Run `cad/build_acr1.py --state home --audit`, then the other seven states named in `FINAL_CAD_MANIFEST.json`, using a Python interpreter configured to import FreeCAD and Part. Run `cad/verify_motion.py` and `cad/verify_final_refinement.py` in a disposable package copy. Preserve the baseline-pallet and final-refinement inputs; rebuilding current geometry alone does not recreate the historical baseline source lock.

The field, conduction and structural sources and captured results accompany this package. Optional Gmsh **4.13.1**, scikit-fem **12.0.2**, meshio **5.3.5** and CalculiX **2.23** are recorded dependencies. Raw large meshes and full solver files are included as **two exact byte parts in this repository**, each below 30 MB. [SUPPLEMENT_ASSETS.json](SUPPLEMENT_ASSETS.json) gives the part, original archive and all 60 member identities. A fresh clone restores them locally with the standard-library materializer; no private Drive or external release download is required. Mesh-dependent full reruns need these restored files and are not covered by the short example. [Reproduction boundaries](REPRODUCTION.md) identifies exact source acquisition and portable adapters.

## Restore the repository-contained raw solver files

```bash
python3 validation/acr1/supplements/materialize.py --verify-only
python3 validation/acr1/supplements/materialize.py --output /tmp/volley-acr1-raw
```

The first command verifies both parts, the complete 48,246,658-byte archive and all 60 decompressed member hashes without extracting. The second restores the original relative file tree in a scratch directory, retaining identical existing files and refusing to overwrite any nonmatching file. Archive paths, duplicate entries and symlinks are checked before extraction. For a full mesh-dependent rebuild, copy the ACR1 source package into a new scratch directory and use that directory as `--output`; accepted repository captures stay intact. The original archive SHA256 remains `53caa2eb6cb82566ebeb12587b15b676c749a3ce602aa96949390e06e464e217`.

## Scientific and licensing boundary

These are computational design results. Geometry/readback share the OpenCASCADE kernel family; the timestep audit shares the production simulation; Orekit replay supplies a separate implementation with the same J2 assumptions. Ambient catalog components, tolerance/load allocations, synthetic targets and prescribed control policies do not establish measured release precision, reliability, environmental qualification or provider approval. The 7 kg allowance is included in mission mass and is excluded from the represented CAD spatial inertia.

Project-created source, CAD and results follow the repository [license](../../LICENSE) and [attribution](../../NOTICE). Vendor PDFs, full extracted vendor text, private plans and correspondence are excluded. Manufacturer URLs, factual parameter selections and original source hashes are retained for provenance. Obtain third-party documents from their publishers under their own terms.
