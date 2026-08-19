# Gen4 — the last one drawn by a person

**Part of the [generation archive](README.md).** The full configuration record is
[`docs/GEN4_STATUS.md`](../GEN4_STATUS.md), which this file does not duplicate.

| | |
|---|---|
| **Status** | **PROVISIONAL, SUPERSEDED.** Adopted 2026-08-03 by [ADR-019](../adr/019-gen4-open-assembly-before-export.md); superseded as the design by Gen5 |
| **Committed here** | **No STEP. No STL. Nothing.** The render set in `cad/renders/` is all that exists of it |
| **Source document** | `EMOCD_Gen4_Open v7` in Fusion. **Not in this repository** — see [P74](../../OPEN_PROBLEMS.md) |
| **Rebuildable from this repository** | **No.** Neither the model nor an export of it is here |
| **Export gate** | **Deliberately closed.** ADR-019 records that Gen4 does not become the committed geometry until it is exported and reconciled. It never was |

## Why it exists

Gen3 accelerated through a uniform 1.30 m stator and released at 1500 mm using a **parametric**
sled. Gen4 rebuilt the assembly around the **actual 488 mm sled** and gave the eddy brake a
physical interaction interval, without extending the track or presenting an enclosure as the
primary public model.

## The problem it left behind, still open

**Gen4's stations are not the analysis model's.**

| | Gen4 | `analysis/` assumes |
|---|---:|---:|
| Release station | **s = 1200 mm** | 1500 mm |
| Sled stow | s = 300 mm | — |
| Halbach array leaves the stator edge | s = 1051.5 mm | — |

**So no performance number in this repository is taken from Gen4, and none should be.** That is
**P43**, and it is why the renders carry a caption saying they show geometry no file in
`cad/step/` matches.

## What is published from it anyway

**The render set on the front page.** Seven shots, cropped and annotated by
[`cad/tools/prepare_renders.py`](../../cad/tools/prepare_renders.py) from the uncropped frames in
`cad/renders/source/`. **They are the most-viewed artifact this project has**, and until
2026-08-16 they advertised an exit velocity withdrawn twice — **P72**, now read from
`analysis/results/motor_results.json` at render time rather than typed in.

## Why it was superseded

**Not because it was wrong.** Because it could not be checked. Nine hand-maintained Fusion
documents, no export, and stations that disagree with the analysis are exactly the failure
`cad/parameters.json` warns about in its own header. **Gen5 is the answer**, and
[ADR-026](../adr/026-cad-built-from-parameters.md) is the decision:
[GEN5.md](GEN5.md).

## What this generation assumed about the host

**It assumed the host was **the same, and for the last time.** Nine Fusion documents of a fully self-contained machine — track, stator, sled, brake, magazine, enclosure.**

Gen4 is the high-water mark of the deployer-as-passenger idea. Everything after it moves the other way.

*The through-line across all six is [`../LINEAGE.md`](../LINEAGE.md).*
