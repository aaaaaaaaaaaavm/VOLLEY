# Gen2 — the first structured revision

**Part of the [generation archive](README.md).** This file is the per-generation record; the
authoritative narrative and defect list are in
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), reproduced below so this file stands alone.

| | |
|---|---|
| **Status** | SUPERSEDED by Gen3. |
| **Committed here** | 9 STEP files in `cad/step/gen2/`, no STL |
| **Source document** | **Fusion. Not in this repository.** No `.f3d` is committed for any generation — see [P74](../../OPEN_PROBLEMS.md) |
| **Rebuildable from this repository** | **No.** The STEP files are a result of the Fusion model, not the model |
| **Operating point** | See [`docs/BASELINE.md`](../BASELINE.md) for the current point. Gen2-era figures in the section below are as recorded at the time and have since moved |

Retained as the intermediate record showing the move from structural proxies to mechanism-level detail.


## What this generation assumed about the host

**It assumed the host was **the same — a mounting surface.** The structured revision changed how the machine was drawn, not what it assumed about the vehicle.**

The self-contained assumption is inherited unexamined, which is the normal thing for a revision to do.

*The through-line across all six is [`../LINEAGE.md`](../LINEAGE.md).*

---

## GEN 2: First Structured Revision

**Date range:** 2025-2026-07 (built iteratively; exact commit dates not
reconstructed)
**Fusion hub folder:** `Fresh` to renamed `Gen2` on 2026-07-28
**STEP exports:** 9 files in `EMOCD_figs/Gen2/`
**Status:** SUPERSEDED by Gen3. Retained as intermediate reference showing
the transition from structural proxy models to mechanism-level detail.

### What Gen2 is

Gen2 is the first structured revision of the VOLLEY CAD, built after the
coilgun-to-LSM decision was finalised and after `cad/parameters.json` was
established as the governing source of truth. All nine documents were built
as separate Fusion files from the outset, each corresponding to one row in
`parameters.json` `documents`.

Gen2 corrected the major structural proxy issues in Gen1, sled mechanism
completeness, stator layer count, magazine mechanism detail, brake ring
spring stop. It is the first generation that can be called a mechanism-level
model rather than a structural envelope. The `_FRESH` suffix used during
build was informal, it meant "freshly built from parameters" as opposed to
the legacy organic Gen1 geometry. Renamed `_Gen2` on 2026-07-28.

Gen2 did not resolve all defects. Several parameter mismatches carried
forward from Gen1 (longeron overall width, brake local-origin placement,
sled sketch parametric driving) and were only corrected in Gen3. The
assembly in Gen2 still had zero joints, carrying G1-D6 forward.

### Gen2 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen2.step` | 35,670 bytes | 4 | Longerons 1800x45x65 mm; 2x launch locks | Longerons at correct 1800 mm length. Width grown to 45 mm (vs 20 mm in Gen1), wider web section. No roller channels or guide flanges yet. File is smaller than Gen1 Track despite more detail, different sketch approach |
| `EMOCD_Stator_Gen2.step` | 967,482 bytes | 162 | Conductors 7x90x10 mm | **Single-layer, 162 conductors**: corrects G1-D2. Belt sequence A+/C−/B+/A−/C+/B− with phase labelling per conductor. STEP file approximately halved in size vs Gen1 (967 KB vs 1.95 MB) reflecting the single-layer correction |
| `EMOCD_Sled_Gen2.step` | 80,554 bytes | 16 | Chassis plates 360x110x6 mm; Halbach arrays upper/lower 340x90x8 mm; 4x rollers 30x16x30 mm (Ø30 mm); 4x roller arms; brake fin 120x80x4 mm | **Mechanism-level sled**: corrects G1-D1. Halbach arrays, rollers, roller arms, and brake fin all present. **However:** chassis length is 360 mm (should be 488 mm per parameters.json) and width is 110 mm (should be 140 mm). These dimensional errors were identified in the Gen2-to-Gen3 audit and corrected in Gen3. Roller diameter already correct at 30 mm |
| `EMOCD_Magazine_Cassette_Gen2.step` | 132,249 bytes | 24 | Shell 380.5x140x640 mm; septum 350x1x620 mm; follower plate + leadscrew; escapement fingers x2; gate frame + D6 pins x2; SMA pin puller; follower motor | **Full mechanism model**: corrects G1-D3 and G1-D11. D6 shear pins present, escapement fingers present, SMA pin puller present, follower motor present. Gate frame and retention mechanism complete. Divider plates from Gen1 removed. Cassette height 640 mm vs 690 mm in parameters.json, 50 mm short |
| `EMOCD_Brake_Gen2.step` | 20,143 bytes | 3 | Pole upper 170x90x30 mm; pole lower 170x90x30 mm; ring spring stop 30x90x92 mm | **Ring spring stop added**: corrects G1-D4. Both poles present with taper geometry. Brake placed at local origin, G1-D10 not yet corrected |
| `EMOCD_Interface_ESPA_Gen2.step` | 73,434 bytes | 6 | Flange ring 25x460x460 mm; hub plate 15x300x300 mm; 4x gussets | Same as Gen1 interface geometry. Bolt holes still absent, G1-D5 not corrected. Gusset geometry refined |
| `EMOCD_Enclosure_Gen2.step` | 77,268 bytes | 11 | Skins 1835x2 mm; radiator 1600x200x3 mm; 4x equipment bays | Enclosure present and correct. All dimensions consistent with parameters.json. 4 equipment bays (supercap, PPU, avionics, IMU) all present. Essentially identical to Gen1 Enclosure in content |
| `EMOCD_Payload_3U_Gen2.step` | 9,273 bytes | 1 | 340.5x100x100 mm | Correct dimensions. File size much smaller than Gen1 (9 KB vs 30 KB), simplified solid proxy. Same geometry, leaner model |
| `EMOCD_Assembly_Gen2.step` | 1,433,428 bytes | 21 occurrences | Full assembly: track, stator, sled, 2x cassettes, brake x2, 12x payload, enclosure, ESPA | Assembly references v2/v4 versions of component documents (not the v1 files audited above, newer saved versions in hub). 12 payloads present (6 per cassette). **Zero joints**: G1-D6 not corrected in Gen2. All occurrences ungrounded at this stage |

### What Gen2 corrected vs Gen1

| Defect ID | Defect | Resolution in Gen2 |
|---|---|---|
| G1-D1 | Sled missing Halbach arrays, rollers, brake fin | Fixed, all mechanism bodies present in Gen2 Sled (16 bodies) |
| G1-D2 | Stator two-layer (324 bodies) | Fixed, single-layer 162 conductors with phase labelling |
| G1-D3 | Magazine missing pins, escapement, SMA puller | Fixed, all mechanism bodies present (24 bodies total) |
| G1-D4 | Brake missing ring spring stop | Fixed, ring spring stop body present |
| G1-D11 | Magazine non-parametric divider plates | Fixed, dividers removed, replaced by escapement mechanism |

### Gen2 defects carried forward to Gen3

| ID | File | Defect | Evidence |
|---|---|---|---|
| G2-D1 | Sled | Chassis length 360 mm vs 488 mm spec | Verified by Fusion API read: chassis_plate_upper 360x110x6 mm |
| G2-D2 | Sled | Chassis width 110 mm vs 140 mm spec | Verified by Fusion API read: chassis_plate_upper 360x110x6 mm |
| G2-D3 | Magazine | Cassette height 640 mm vs 690 mm spec | Verified by Fusion API read: Shell_Front 380.5x4x640 mm |
| G2-D4 | Brake | Placed at local origin, not x = 1530 mm assembly position | Verified by Fusion API read: brake_yoke x_start = 30 mm not 1530 mm |
| G2-D5 | Interface ESPA | Bolt holes absent | Not modelled in any generation |
| G2-D6 | Assembly | Zero joints, no kinematic definition | Verified by Fusion API read: root.joints.count = 0 |
| G2-D7 | Track | No roller channels or guide flange geometry | Track is longerons and launch locks only |

---

---

## Why this generation was superseded

See the following generation's file and
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), which records what each revision corrected.
**Nothing in this file is restated from memory** — the section above is the changelog's own text.
