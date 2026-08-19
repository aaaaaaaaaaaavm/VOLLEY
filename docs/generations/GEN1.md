# Gen1 — the geometric ancestor

**Part of the [generation archive](README.md).** This file is the per-generation record; the
authoritative narrative and defect list are in
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), reproduced below so this file stands alone.

| | |
|---|---|
| **Status** | SUPERSEDED by Gen2. Retained as design heritage and geometric ancestor reference. |
| **Committed here** | 11 STEP files in `cad/step/gen1/`, no STL |
| **Source document** | **Fusion. Not in this repository.** No `.f3d` is committed for any generation — see [P74](../../OPEN_PROBLEMS.md) |
| **Rebuildable from this repository** | **No.** The STEP files are a result of the Fusion model, not the model |
| **Operating point** | See [`docs/BASELINE.md`](../BASELINE.md) for the current point. Gen1-era figures in the section below are as recorded at the time and have since moved |

Do not cite Gen1 dimensions without cross-checking `cad/parameters.json`.


## What this generation assumed about the host

**It assumed the host was **a mounting surface with a power feed.** Gen1 carries its own track, structure, enclosure and energy store; nothing is expected of the vehicle underneath it beyond a place to bolt to.**

[ADR-002](../adr/002-host-is-a-spent-upper-stage.md) had already chosen a spent upper stage as that host **in 2023**, but as somewhere to stand rather than as part of the machine. Gen1's geometry reflects that: everything is aboard.

*The through-line across all six is [`../LINEAGE.md`](../LINEAGE.md).*

---

## GEN 1: OG CAD

**Date range:** 2021-2025 (exact build history not reconstructed)
**Fusion hub folder:** `OG CAD` to renamed `Gen1` on 2026-07-28
**STEP exports:** 11 files in `EMOCD_figs/Gen1/`
**Status:** SUPERSEDED. Retained as design heritage and geometric ancestor
reference only. Do not cite Gen1 dimensions without cross-checking against
`cad/parameters.json`.

### What Gen1 is

Gen1 is the original set of Fusion 360 documents built to establish the
physical envelope and structural concept of VOLLEY. It is the first complete
3D realisation of the system and is the geometric source from which
`EMOCD-main/cad/parameters.json` was reverse-engineered by direct read of
the live Fusion model on 2026-07-23 (`parameters.json` `_PROVENANCE`
section, method: "Rebuilt by reading the nine-document Autodesk Fusion model
directly").

Gen1 is therefore the **geometric ancestor** of the entire parameter set.
However, it does not faithfully represent the current design in several
areas: it reflects design decisions that were later reversed, and several
sub-systems were built as structural proxies rather than detailed mechanism
models.

### Gen1 file inventory (verified by direct Fusion API read, 2026-07-28)

| File | STEP size | Bodies read | Key geometry | Notes |
|---|---|---|---|---|
| `EMOCD_Track_Gen1.step` | 47,302 bytes | 8 | Longerons 1800x20x65 mm; 4x GuideRail 1800x8x22 mm; 2x LaunchLock 20x10x28 mm | Longeron length correct at 1800 mm. Longeron web only 20 mm wide, no outrigger structure, roller channels, or cross-tie frames present |
| `EMOCD_Stator_Gen1.step` | 1,954,907 bytes | 324 | Conductors 7x90x10 mm each | **Two-layer winding**: Belt_Top and Belt_Bottom groups, 162 conductors per layer = 324 total. Contradicts `parameters.json` `stator.layer_count_decision: "OPEN — single vs two-layer … Single layer as drawn."` Gen1 implemented two layers; this was unresolved at build time. The large STEP file size (1.95 MB vs ~9 KB for the repo export) reflects the full 324-body geometry |
| `EMOCD_Sled_Gen1.step` | 30,359 bytes | 5 | Chassis plates 488x140x6 mm; webs 488x6x140 mm; backstop 8x140x140 mm | **Chassis structural box only.** No Halbach arrays, no rollers, no brake fin. This is a structural proxy, geometry and fit only. The 488x140 mm footprint and 6 mm chassis plate thickness are correct per spec |
| `EMOCD_Sled_Gen1b.step` | 50,130 bytes | ~16 | Chassis + partial sled detail | **Duplicate sled document**: a later revision of the Gen1 sled with more detail than `Sled_Gen1` but less than Gen2. Included rollers and additional bodies not in `Sled_Gen1`. Named `Gen1b` to disambiguate. Not in `EMOCD-main/cad/step/` |
| `EMOCD_Magazine_Cassette_Gen1.step` | 89,234 bytes | 16 | Shell 380.5x166x690 mm; septum 350x1x620 mm; follower plate 380.5x158x6 mm; gate frame 10x580x140 mm; 6x divider plates | Shell dimensions correct. Silicon-steel septum present at 1 mm. **Missing: D6 shear pins, escapement fingers, SMA pin puller.** Includes 6x internal satellite divider plates (340x126x2 mm) that are not in `parameters.json`, these appear to be an early non-parametric approach to satellite slot separation, later superseded by the escapement mechanism |
| `EMOCD_Brake_Gen1.step` | 22,915 bytes | 4 | Poles: BrakePole_Top_Main 180x90x15 mm, BrakePole_Top_Taper 30x90x15 mm (x2 for bottom) | Pole plate thickness 15 mm correct. Taper entry 30 mm correct. **Missing ring spring stop** (`parameters.json` `brake.ring_spring_stop = true`). **Modelled at x = 0 (local origin)**: not placed at assembly x = 1530 mm |
| `EMOCD_Interface_ESPA_Gen1.step` | 77,997 bytes | 6 | Flange ring 25x460x460 mm; hub plate 15x300x300 mm; 4x gussets | Flange OD 460 mm, thickness 25 mm, and hub plate 300 mm diameter all correct. **Bolt holes absent**: 24x M9 on Ø400 mm BCD not modelled |
| `EMOCD_Enclosure_Gen1.step` | 72,627 bytes | 11 | Skins: 1839x530x2 mm (top, bottom, sides); aft horseshoe 2 mm; muzzle panel 2 mm; radiator 1600x200x3 mm; 4x equipment bays | **Most complete Gen1 document.** All dimensions match `parameters.json` precisely. All four equipment bays present (supercap bank, PPU/SiC, avionics sequencer, IMU). Radiator, muzzle aperture panel, and aft horseshoe cutout all present |
| `EMOCD_Payload_3U_Gen1.step` | 30,613 bytes | 1 | 340.5x100x100 mm solid | Correct dimensions per `parameters.json` `payload_3u`. Solid aluminium proxy, real 3U flight mass is 4 kg, not Fusion-computed value |
| `EMOCD_Assembly_Gen1.step` | 229,550 bytes | | Full 9-document assembly | Post-split assembly referencing all component documents. **Zero joints**: all occurrences grounded, no kinematic definition. No sled slider joint, no payload joints |
| `EMOCD_Deployer_Assembly_Gen1.step` | 246,874 bytes | | Legacy single-file assembly | **SUPERSEDED single-file model** built before the nine-document split. Carried unsaved modifications at time of audit (2026-07-23 CAD Master Plan). Not present in `EMOCD-main/cad/step/`, the only Gen1 file with no repo counterpart. Retained for heritage only. Must not be edited |

### Gen1 known defects

The following defects were identified by direct Fusion API read on 2026-07-28
and by comparison against `cad/parameters.json`. This is the complete list,
nothing is inferred or estimated.

| ID | File | Defect | Consequence | Fixed in |
|---|---|---|---|---|
| G1-D1 | Sled | Missing Halbach arrays, rollers, brake fin | Sled is structural proxy only, no electromagnetic or dynamic geometry | Gen2 |
| G1-D2 | Stator | 324 bodies (two-layer) vs single-layer repo spec | Contradicts `parameters.json` `stator.layer_count_decision` which states single-layer as drawn | Gen2 |
| G1-D3 | Magazine | Missing D6 shear pins, escapement fingers, SMA pin puller | Gate release mechanism incomplete | Gen2 |
| G1-D4 | Brake | Missing ring spring stop | Arrest mechanism incomplete, only eddy poles present | Gen2 |
| G1-D5 | Interface ESPA | Bolt holes absent | 24x M9 on Ø400 mm BCD not modelled | Not resolved in Gen2 or Gen
| G1-D5 | Interface ESPA | Bolt holes absent | 24x M9 on Ø400 mm BCD not modelled | Not resolved in Gen2 or Gen3, bolt holes remain absent across all generations. Open geometry gap |
| G1-D6 | Assembly | Zero joints, static pile of grounded occurrences | No kinematic definition. No sled slider, no payload cradle joint | Gen3 assembly partially, 8 components grounded, sled slider added via as-built joint |
| G1-D7 | Deployer_Assembly_v1 | Open with unsaved modifications at time of 2026-07-23 audit | Risk of incorrect geometry being committed if saved | Closed without saving on 2026-07-23. Not touched since |
| G1-D8 | Track | Longeron web only 20 mm wide vs 205 mm overall width spec | No roller channels, no outrigger structure, no cross-tie frames | Gen2 added frame ties and outrigger posts. Gen3 extended further |
| G1-D9 | Sled | Chassis plate parameters not parametrically driven | Face offsets applied via direct edit did not persist across timeline recompute | Addressed in Gen3 by sketch geometry remapping |
| G1-D10 | Brake | Placed at local origin (x = 0) not at assembly x = 1530 mm | Brake appears at breech end in assembly, incorrect position relative to release point at x = 1500 mm | Gen3, brake moved to x_start = 1530 mm |
| G1-D11 | Magazine | 6x internal divider plates present but not in parameters.json | Non-parametric satellite separation approach, superseded by escapement mechanism | Gen2, dividers removed, escapement fingers and gate mechanism added |

---

---

## Why this generation was superseded

See the following generation's file and
[`cad/CHANGELOG_CAD.md`](../../cad/CHANGELOG_CAD.md), which records what each revision corrected.
**Nothing in this file is restated from memory** — the section above is the changelog's own text.
