# Gen4 Fusion CAD design

Part of the [generation archive](README.md). The full configuration record is
[`docs/GEN4_STATUS.md`](../GEN4_STATUS.md), which this file does not duplicate.

| | |
|---|---|
| Status | PROVISIONAL, SUPERSEDED. Adopted 2026-08-03 by [ADR-019](../adr/019-gen4-open-assembly-before-export.md); superseded as the design by Gen5 |
| Committed here | Render set in `cad/renders/`; no STEP or STL export from this revision is committed |
| Source document | `EMOCD_Gen4_Open v7` in Fusion. Not in this repository, see [P74](../../OPEN_PROBLEMS.md) |
| Rebuildable from this repository | No. The Fusion source documents and their exports are not committed here |
| Export gate | Deliberately closed. ADR-019 records that Gen4 does not become the committed geometry until it is exported and reconciled. It never was |

## Why it exists

Gen3 accelerated through a uniform 1.30 m stator and released at 1500 mm using a parametric
sled. Gen4 rebuilt the assembly around the actual 488 mm sled and gave the eddy brake a
physical interaction interval, without extending the track or presenting an enclosure as the
primary public model.

## The problem it left behind, still open

Gen4's stations are not the analysis model's.

| | Gen4 | `analysis/` assumes |
|---|---:|---:|
| Release station | s = 1200 mm | 1500 mm |
| Sled stow | s = 300 mm |, |
| Halbach array leaves the stator edge | s = 1051.5 mm |, |

So no performance number in this repository is taken from Gen4, and none should be. That is
P43, and it is why the renders carry a caption saying they show geometry no file in
`cad/step/` matches.

## What is published from it anyway

The render set on the front page. Seven shots, cropped and annotated by
[`cad/tools/prepare_renders.py`](../../cad/tools/prepare_renders.py) from the uncropped frames in
`cad/renders/source/`. They are the most-viewed artifact this project has, and until
2026-08-16 they advertised an exit velocity withdrawn twice, P72, now read from
`analysis/results/motor_results.json` at render time rather than typed in.

## Why it was superseded

Gen4 is a substantial Fusion CAD design. The project did not commit a STEP export from that
revision, and its modeled stations differ from the analysis assumptions. Those are traceability
and reconciliation gaps in this repository, not a judgment about the quality of the Fusion work.
[ADR-026](../adr/026-cad-built-from-parameters.md) records the later choice to build the
[Gen5 comparison geometry](GEN5.md) from committed parameters.

## What this generation assumed about the host

It assumed the host was the same, and for the last time. Nine Fusion documents of a fully self-contained machine, track, stator, sled, brake, magazine, enclosure.

Gen4 is the high-water mark of the deployer-as-passenger idea. Everything after it moves the other way.

*The through-line across all six is [`../LINEAGE.md`](../LINEAGE.md).*
