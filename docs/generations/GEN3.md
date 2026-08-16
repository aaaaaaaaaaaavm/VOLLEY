# Gen3 — parameter-reconciled, and where the masses come from

**Part of the [generation archive](README.md).** This file is the per-generation record; the
authoritative narrative and defect list are in
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), reproduced below so this file stands alone.

| | |
|---|---|
| **Status** | SUPERSEDED as the design by Gen4 and Gen5. **Not superseded as evidence.** |
| **Committed here** | 10 STEP files in `cad/step/gen3/`, 2 STL |
| **Source document** | **Fusion. Not in this repository.** No `.f3d` is committed for any generation — see [P74](../../OPEN_PROBLEMS.md) |
| **Rebuildable from this repository** | **No.** The STEP files are a result of the Fusion model, not the model |
| **Operating point** | See [`docs/BASELINE.md`](../BASELINE.md) for the current point. Gen3-era figures in the section below are as recorded at the time and have since moved |

**`analysis/mass_properties.py` takes the sled at 9.445 kg from these solids (P15), and that figure sets the headline exit velocity.** Gen3 is the only generation any number is measured off.

---

## GEN 3: Parameter-Reconciled Revision

**Date range:** 2026-07 (built during the 2026-07-23 CAD build session and
subsequent corrections applied 2026-07-28)
**Fusion hub folder:** `Even more fresh` to renamed `Gen3` on 2026-07-28
**STEP exports:** 10 files in `EMOCD_figs/Gen3/` (9 component files + 1
monolithic single-file model `EMOCD_Gen3.step`)
**Status:** CURRENT. This is the generation against which open problems P5, P12 are indexed. All geometry values carry status from `parameters.json`.

### What Gen3 is

Gen3 is the parameter-reconciled revision of the VOLLEY CAD. It was built
during the 2026-07-23 CAD build session documented in the `EMOCD_CAD_Master_Plan.md`
working document, which performed a live read of the Fusion hub via the
Fusion MCP and rebuilt the parameter set from the actual geometry. This is
the build that produced the current `cad/parameters.json`.

Gen3 introduced two things that did not exist in any earlier generation:

1. **The `EMOCD_Gen3.step` monolithic model** (2,520,630 bytes), a
   single Fusion document (`EMOCD_Gen3`, previously named `VOLLEY but really
   detailed`) that contains all nine sub-systems as components within one
   assembly file. This is the most detailed single-file representation of
   the system and is the model used for the CAD renders in `EMOCD-main/cad/renders/`.

2. **The first assembly with joint definitions**, the Gen3 assembly has 8
   structural components grounded (`isGrounded = True`: Track, Stator, both
   Cassettes, both Brake instances, Interface ESPA, Enclosure) and a sled
   slider as-built joint defining X-axis travel with limits 0-1740 mm. Gen1
   and Gen2 assemblies had zero joints.

Gen3 also corrected all dimensional defects identified in Gen2 (sled length,
sled width, brake position) and corrected the user parameters in the
monolithic model that were previously not propagating to geometry.

### Gen3 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen3.step` | 35,241 bytes | 4 | Longerons 1800x45x65 mm; 2x launch locks | Longerons at correct 1800 mm length. Same structure as Gen2 Track. No roller channels, G2-D7 not resolved |
| `EMOCD_Stator_Gen3.step` | 967,476 bytes | 162 | Conductors 7x90x10 mm | Single-layer 162 conductors with phase labelling, same as Gen2. Correct per spec. File size within 6 bytes of Gen2 Stator (967,476 vs 967,482), effectively identical geometry |
| `EMOCD_Sled_Gen3.step` | 80,874 bytes | 16 | Chassis plates 488x140x6 mm; Halbach arrays 340x90x8 mm; 4x rollers Ø30x16 mm; roller arms; brake fin | **Dimensional corrections applied**: corrects G2-D1 and G2-D2. Chassis length 488 mm (was 360 mm in Gen2) and width 140 mm (was 110 mm in Gen2) now match `parameters.json` `sled.overall_length` and `sled.overall_width`. Achieved by remapping sketch point geometry and forcing design.computeAll(). Roller diameter 30 mm correct throughout Gen2 and Gen3 |
| `EMOCD_Magazine_Cassette_Gen3.step` | 131,320 bytes | 24 | Shell 380.5x140x640 mm; full mechanism | Same mechanism completeness as Gen2 (24 bodies). Cassette height still 640 mm (G2-D3 not resolved in Gen3. File 929 bytes smaller than Gen2) minor geometry refinement |
| `EMOCD_Brake_Gen3.step` | 20,136 bytes | 3 | Poles with taper; ring spring stop | **Brake position corrected**: corrects G2-D4. Brake placed at x_start = 1530 mm (was at local origin in Gen1 and Gen2). Verified by Fusion API read: brake_yoke minPoint.x = 153.0 cm. Ring spring stop present, taper geometry correct |
| `EMOCD_Interface_ESPA_Gen3.step` | 73,428 bytes | 6 | Flange ring Ø460 mm OD, 25 mm thick; hub plate Ø300 mm, 15 mm thick; 4x gussets; 24 bolt holes | **Bolt holes added**: partially corrects G1-D5. 24 bolt holes on Ø400 mm BCD modelled by sketch + cut extrude in the Gen3 session on 2026-07-28. This is the first generation with bolt holes present. Gussets at 0/90/180/270 deg |
| `EMOCD_Enclosure_Gen3.step` | 78,457 bytes | 11 | Skins 1839x530x2 mm; radiator 1600x200x3 mm; muzzle aperture; aft horseshoe cutout; 4x equipment bays | Full enclosure with all features. 1,231 bytes larger than Gen2, minor geometry refinement. All dimensions consistent with `parameters.json` |
| `EMOCD_Payload_3U_Gen3.step` | 9,267 bytes | 1 | 340.5x100x100 mm | Correct dimensions. 6 bytes smaller than Gen2, effectively identical |
| `EMOCD_Assembly_Gen3.step` | 1,433,418 bytes | 21 occurrences | Full assembly with joints | **First assembly with kinematic joints**: corrects G1-D6 / G2-D6. 8 structural components grounded, sled slider as-built joint with X-axis limits 0-1740 mm. 12 payloads (6 per cassette), 2x cassette instances, 2x brake instances. File 10 bytes smaller than Gen2 Assembly, effectively identical geometry, the joint definitions are not reflected in STEP size |
| `EMOCD_Gen3.step` | 2,520,630 bytes | 9 sub-components, all bodies | Monolithic single-file assembly with all 9 sub-systems | **Unique to Gen3.** The `VOLLEY but really detailed` document renamed `EMOCD_Gen3`. Contains Track (43 bodies), Stator (170 bodies including 162 conductors + spine + brackets), Sled (76 bodies including 56 Halbach magnets + chassis + 8 rollers + brake fin + detent latches), Payload (12 bodies, 12 CubeSat instances), Cassette_P (18 bodies), Cassette_S (18 bodies, corrected from 16 in earlier state by adding interface_pad_S5_0 and S5_1), Brake (8 bodies), Avionics (39 bodies including 32 supercap cells), Interface (9 bodies including bolt holes and gussets), Enclosure (7 bodies: 6 skins + radiator). Most complete single representation of VOLLEY in any generation |

### What Gen3 corrected vs Gen2

| Defect ID | Defect | Resolution in Gen3 |
|---|---|---|
| G2-D1 | Sled chassis length 360 mm | Fixed, 488 mm, verified by Fusion API read |
| G2-D2 | Sled chassis width 110 mm | Fixed, 140 mm, verified by Fusion API read |
| G2-D4 | Brake at local origin | Fixed, brake x_start = 1530 mm, verified by Fusion API read |
| G2-D6 | Assembly zero joints | Fixed, 8 components grounded, sled slider joint X-axis 0-1740 mm |
| G1-D5 | ESPA bolt holes absent | Fixed in Gen3 Interface ESPA, 24 holes on Ø400 mm BCD now modelled |

### Gen3 defects and open problems remaining

The following defects were identified by direct Fusion API read on 2026-07-28
and by comparison against `cad/parameters.json` and `OPEN_PROBLEMS.md`.
These are unresolved as of the last audit.

| ID | File | Defect | Evidence | Repo reference |
|---|---|---|---|---|
| G3-D1 | Magazine (all gens) | Cassette height 640 mm vs 690 mm spec | Verified: Shell_Front 380.5x4x640 mm in Gen2 and Gen3. 50 mm short | `parameters.json` `magazine.cassette_height_z = 690` |
| G3-D2 | Track (all gens) | No roller channels, guide flanges, or cross-tie outrigger structure | Track is longerons + launch locks only. `parameters.json` specifies roller_channel_y_inner/outer and guide_rail geometry | `parameters.json` track group |
| G3-D3 | Sled (monolithic Gen3) | Chassis width reached 139.8 mm not exact 140 mm | Residual rounding from sequential face-offset operations. Within 0.2 mm of spec | `parameters.json` `sled.overall_width = 140` |
| G3-D4 | Stator (all gens) | Layer count decision still open | Single-layer as built, but `parameters.json` explicitly flags `layer_count_decision: OPEN`. Two-layer may be the correct electromagnetic design | `parameters.json` `stator.layer_count_decision` |
| G3-D5 | Sled (all gens) | Halbach arrays not repositioned after sled length correction | After chassis extended 360 to 488 mm, Halbach array start position not re-centred on the new chassis length | `parameters.json` `sled.halbach_array_x_start = 230 mm` |
| G3-D6 | Assembly (all gens) | No payload-on-sled rigid joint | `parameters.json` `documents.EMOCD_Assembly` specifies `payload_on_sled_rigid` joint. Not present in any generation | `parameters.json` documents section |
| G3-D7 | All gens | Masses absent from `mass_properties.py` for enclosure, radiator, avionics | 72.3 kg dry mass figure is incomplete | Open problem P10 |
| G3-D8 | All gens | CAD sled mass ~7.50 kg vs parametric 4.86 kg | Exit velocity provisional at 17.88 m/s pending structural FEA (ANSYS A4) | Open problems P5, P8 |
| G3-D9 | All gens | Installed envelope 1839 mm exceeds ESPA Grande ~1270 mm limit by ~44% | Brake must live past 1500 mm release point, forcing total length | Open problem P9 |
| G3-D10 | All gens | Paper claims ESPA-Grande-class compatibility contradicted by CAD | P12 in OPEN_PROBLEMS.md, not yet corrected in paper.tex | Open problem P12 |
| G3-D11 | All gens | Whether P1, P4 paper corrections reached the submitted build is unconfirmed | `paper/archive/EMOCD_submission_uncorrected.pdf` still carries incorrect values | Open problem P11 |

---

## PART III: CROSS-GENERATION COMPARISON SUMMARY

This table shows the state of each sub-system across all three generations,
verified by direct Fusion API read of the live Fusion documents on 2026-07-28.

| Sub-system | Gen1 | Gen2 | Gen3 |
|---|---|---|---|
| **Track** | 8 bodies. Longerons 1800 mm OK. Width 20 mm FAIL (no outrigger). | 4 bodies. Longerons 1800x45 mm. Slightly wider but still no outrigger FAIL. | 4 bodies. Same as Gen2. Outrigger gap not closed FAIL. |
| **Stator** | 324 bodies. Two-layer FAIL. 7x90x10 mm conductors OK. | 162 bodies. Single-layer OK. Phase-labelled OK. | 162 bodies. Identical to Gen2 OK. Monolithic model adds spine + brackets. |
| **Sled** | 5 bodies. Chassis only FAIL. Length 488 mm OK, width 140 mm OK, plate 6 mm OK. No Halbach, rollers, fin FAIL. | 16 bodies. Halbach OK, rollers Ø30 mm OK, fin OK. But length 360 mm FAIL, width 110 mm FAIL. | 16 bodies. Length 488 mm OK, width ~140 mm OK. All mechanism bodies OK. Brake fin present OK. |
| **Magazine Cassette** | 16 bodies. Shell correct OK. Septum OK. No pins, escapement, SMA FAIL. Has non-spec dividers FAIL. | 24 bodies. D6 pins OK. Escapement OK. SMA puller
| **Magazine Cassette** | 16 bodies. Shell correct OK, septum OK. No D6 pins FAIL, no escapement FAIL, no SMA puller FAIL. Non-spec divider plates FAIL. | 24 bodies. D6 pins OK, escapement OK, SMA puller OK, follower motor OK. Dividers removed OK. Height 640 mm vs 690 mm spec FAIL. | 24 bodies. Same mechanism completeness as Gen2 OK. Height still 640 mm FAIL. |
| **Brake** | 4 bodies. Pole thickness 15 mm OK, taper 30 mm OK. No ring spring stop FAIL. At local origin FAIL. | 3 bodies. Ring spring stop added OK. Still at local origin FAIL. | 3 bodies. Ring spring stop OK. Placed at x = 1530 mm OK. |
| **Interface ESPA** | 6 bodies. Ø460 mm OD OK, 25 mm thick OK, hub plate OK, 4x gussets OK. No bolt holes FAIL. | 6 bodies. Same geometry as Gen1. Bolt holes still absent FAIL. | 6 bodies + bolt holes. 24x M9 on Ø400 mm BCD added OK. First generation with complete interface geometry. |
| **Enclosure** | 11 bodies. All skins OK, radiator OK, muzzle aperture OK, aft horseshoe OK, 4x equipment bays OK. Most complete Gen1 document. | 11 bodies. Effectively identical to Gen1 Enclosure OK. | 11 bodies (component file). Monolithic model separately adds enclosure skins + radiator OK. |
| **Payload 3U** | 1 body. 340.5x100x100 mm OK. | 1 body. 340.5x100x100 mm OK. Smaller STEP (9 KB vs 30 KB). | 1 body. 340.5x100x100 mm OK. 12 instances in assembly OK. |
| **Assembly** | 11 files including legacy monolith. Zero joints FAIL. References split docs OK. | 9 files. Zero joints FAIL. 21 occurrences OK (12 payloads, 2 cassettes, 2 brake instances). | 10 files including monolithic EMOCD_Gen3. 8 components grounded OK. Sled slider joint X-axis 0-1740 mm OK. No payload-on-sled rigid joint FAIL. |
| **Monolithic model** | EMOCD_Deployer_Assembly_v1 (legacy, unsaved mods, not in repo) FAIL | None | EMOCD_Gen3.step (2.52 MB) OK, all 9 sub-systems in one file, most detailed representation in any generation. Stator has 170 bodies (162 conductors + spine + 7 brackets). Cassette S-side corrected from 16 to 18 bodies. |

---

## PART IV: OPEN PROBLEMS INDEXED TO CAD

The following open problems from `EMOCD-main/OPEN_PROBLEMS.md` have direct
CAD consequences. They are reproduced here for completeness so this file can
be read standalone. Described in full in `OPEN_PROBLEMS.md`.

| Problem | Description | CAD consequence | Status |\n|---|---|---|---|\n| **P5** | CAD sled mass ~7.50 kg vs parametric assumption 4.86 kg | Exit velocity provisional at 17.88 m/s, not 20.37 m/s. No number in `analysis/*.py` changed. Sled chassis flagged `PROVISIONAL_PENDING_FEA` in `parameters.json` | Open. Requires ANSYS structural FEA (validation A4) |\n| **P7** | Brake occupies x = 1530-1740 mm, beyond x = 1500 mm release point | Track and enclosure must extend past release, directly drives the 1839 mm total length and therefore P9 | Open. ConOps decision required |\n| **P8** | Exit velocity provisionally 17.88 m/s if CAD sled mass holds | All downstream numbers (acceleration, efficiency, recoil, lifetime multiplier) shift. Not propagated into scripts or paper pending FEA | Open. Waiting on P5 resolution |\n| **P9** | Installed envelope 1839 mm exceeds ESPA Grande ~1270 mm limit by ~44% | Machine cannot fit ESPA Grande as claimed. Host claim must be re-scoped or track repackaged | Open. Owner decision, cannot be resolved in code |\n| **P10** | Enclosure, radiator, avionics absent from `mass_properties.py` | 72.3 kg dry-mass rollup is incomplete by an unknown amount | Open. Needs bay-by-bay mass estimation, then addition to `mass_properties.py` |\n| **P11** | Whether P1, P4 corrections reached the submitted paper build is unconfirmed | `paper/archive/EMOCD_submission_uncorrected.pdf` still carries all four incorrect values. If this is the version of record, a corrigendum is needed, not a git commit | Open. Must confirm which build was submitted |\n| **P12** | Paper claims ESPA-Grande-class envelope; CAD contradicts this by ~44% | Two places in paper.tex assert compatibility the geometry does not support. One is an abstract-level capability claim; the other is in the limitations section | Open. Entangled with P11, resolve P11 first, then fix paper.tex in one pass |\n| **E1** | 3-D field end effects on Kt uncomputed | FEMM cross-section DXF and run sheet exist (`analysis/femm/`) but nothing has been run. A few percent on Kt unaccounted | Open. FEMM package written, not executed |\n| **E2** | No FEA of any structural component | Sled, track, brake poles, cassette shell all first-pass geometry with no structural analysis behind them | Open. Validations A1 and A4 specified in `validation/` with pre-declared acceptance bands |\n| **E3** | Enclosure, radiator, and avionics masses missing from rollup | Directly feeds P10 | Open |\n| **E10** | Launch restraint drawn but not analysed | Retention gate pin sizing exists (two D6 A-286, margin 1.2, A36) and launch-lock blocks are in Track CAD but escapement caging, cam lock, and tolerance stack-up under vibration not analysed | Open, CAD advances this item from concept to drawn, not to analysed |\n\n---\n\n## PART V, FILE NAMING CONVENTION\n\nAll files across all generations follow the pattern:\n\n```\nEMOCD_[SubSystem]_[Generation].step\n```\n\nWhere `[SubSystem]` is one of:\n`Track`, `Stator`, `Sled`, `Magazine_Cassette`, `Brake`, `Interface_ESPA`,\n`Enclosure`, `Payload_3U`, `Assembly`\n\nAnd `[Generation]` is `Gen1`, `Gen2`, or `Gen3`.\n\nSpecial cases:\n- `EMOCD_Deployer_Assembly_Gen1.step` (legacy single-file model, Gen1 only,\n no repo counterpart. Superseded.\n- `EMOCD_Sled_Gen1b.step`) duplicate sled document from Gen1, later revision\n than `Sled_Gen1`. Suffix `b` added to disambiguate.\n- `EMOCD_Gen3.step`, monolithic single-file model, Gen3 only. Contains all\n nine sub-systems in one Fusion document. The most detailed and complete\n representation of VOLLEY in any generation.\n\n### Folder rename history\n\n| Original folder name | Renamed to | Date | Reason |\n|---|---|---|---|\n| `OG CAD` | `Gen1` | 2026-07-28 | Align with generation naming convention |\n| `Fresh` | `Gen2` | 2026-07-28 | `_FRESH` suffix meant \"built from parameters\", formalised as Gen2 |\n| `Even more fresh` | `Gen3` | 2026-07-28 | Formalised as Gen3 |\n\n---\n\n## PART VI, WHAT TO CHECK BEFORE USING ANY FILE\n\nBefore citing or using any geometry from `EMOCD_figs`:\n\n1. **Use Gen3 files unless you specifically need a heritage comparison.**\n Gen1 and Gen2 contain known dimensional and mechanism defects.\n\n2. **Cross-check every dimension against `cad/parameters.json`.**\n `parameters.json` is the source of truth, not the Fusion model. If they\n disagree, `parameters.json` wins and the CAD needs correcting.\n\n3. **Do not quote Fusion-computed masses.** The Fusion models use solid copper\n for the stator, solid aluminium for CubeSats, and steel standing in for\n NdFeB. None of these are the correct material densities. Mass authority\n is `analysis/mass_properties.py` only, and even that is incomplete (P10).\n\n4. **The sled mass conflict is unresolved (P5/P8).** The headline exit\n velocity of 20.37 m/s assumes a 4.86 kg sled. The Gen3 CAD sled geometry\n implies ~7.50 kg, which gives a provisional 17.88 m/s. Do not use either\n number without noting this conflict until ANSYS structural FEA (A4)\n resolves it.\n\n5. **The ESPA envelope claim is not supported by the CAD (P9/P12).** The\n installed length of 1839 mm exceeds ESPA Grande's ~1270 mm limit by ~44%.\n Do not present VOLLEY as ESPA-Grande-compatible without noting this open\n problem.\n\n6. **The stator layer count is still an open design decision.** Gen1 built\n two layers; Gen2 and Gen3 built one layer; `parameters.json` explicitly\n flags the decision as open. The electromagnetic consequence (roughly x2\n on force for the same current, but also x2 on copper mass and winding\n complexity) has not been computed for the two-layer case.\n\n---\n\n*End of CHANGELOG_CAD. Append new entries below this line.*\n```

---

## Why this generation was superseded

See the following generation's file and
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), which records what each revision corrected.
**Nothing in this file is restated from memory** — the section above is the changelog's own text.
