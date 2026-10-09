# CAD

> **Current academic configuration: Gen5.** Start with the [eight generated Gen5 STEP
> parts](step/gen5/), [20-instance reference assembly](step/gen5/VOLLEY_Review_Assembly_Gen5.step), [Gen5 renders](renders/gen5/), [dimension sheet](DIMENSIONS.md),
> [configuration hashes](../docs/GEN5_CONFIGURATION_INDEX.json) and
> [freeze-readiness matrix](../docs/GEN5_FREEZE_READINESS.md). The Gen3 Fusion files below
> are historical source geometry used in some mass/FEA records; their age and role must
> accompany any citation. The reference assembly has a [measured side-fed clash](../validation/P116_gen5_assembly_packaging.md): 11 mm width shortfall and track/cassette intersection. It is a controlled review artifact, not an approved integrated design, manufacturing drawing or physical fit test.
>
> The 9.445 kg modeled sled value was adopted from Gen3 solid volumes and tested with
> the A4 CalculiX chassis idealization. It is carried into Gen5; the Gen5 STEP build
> checks dimensions but does not independently recompute an installed mass for all
> hardware. The 126.6 kg dry rollup includes modeled and assumed components, so it
> must not be described as the weight of a complete verified Gen5 CAD assembly.

**Professional CAD handover:** [native FreeCAD 1.0 review document](native/Gen5_Review.FCStd), [eight FreeCAD-exported STEP parts](step/freecad_gen5/), [FreeCAD assembly STEP](step/gen5/VOLLEY_Review_Assembly_FreeCAD_Gen5.step), [read-back and interference report](FREECAD_EXPORT.json), and [three-page CAD review PDF](GEN5_CAD_REVIEW.pdf). The source B-reps were created parametrically in CadQuery and imported into FreeCAD; the imported parts do not contain native FreeCAD feature histories. Both FreeCAD and CadQuery report the same stated side-fed track/cassette clash. The PDF includes a model render and measured section, each labeled by evidence type.

> ## historical study is here too, and it is a different machine
>
> [ADR-032](../docs/adr/032-legacy_study-stage-integrated-gas-store.md). The payload is accelerated
> directly by cold gas along a rail the host stage provides, no mover, no stator, no brake, no
> return stroke. `cad/build_legacy_study.py` generates it from the same `parameters.json`, and it is
> byte-stable across rebuilds like Gen5.
>
> Seven exported parts, and only one of them is inherited: the magazine cassette. A36 and A37 agree from
> opposite directions that the containment is the only subsystem surviving every architecture
> deletion.
>
> | | |
> |---|---|
> | Bore / stroke | 15.805 mm / 8000 mm, A49, the host stage's whole acceleration length |
> | Chamber | 2 L at 22.7258 bar, A41 sized it, ADR-034 set the charge |
> | Reservoir | 3.46 L at 200 bar, A56, sized rather than scaled |
> | Exit velocity | 29.01 m/s at the friction allowance, 11.36 g peak |
>
> Corrected 2026-08-22, [P107](../OPEN_PROBLEMS.md). These three rows read 50 bar, 11.25 L
> and 30.54 m/s at 25 g, the pre-ADR-034 design point. The geometry never moved with them:
> `build_legacy_study.py` reads every one of these from `parameters.json`.
>
> Three things it draws that are not settled, and they are in the script's own header rather
> than only here: the cradle is an envelope, not a design, because A34 says the mechanism
> does not exist and A38's preload is 201.7 N at the 25 g cap against 91.7 at the design point
> (P102); the reservoir is sized but the bottle itself is not designed; and the stage rail is
> a straight extrusion
> of unknown provenance, because no launch provider has agreed to anything.


Fusion 360 CAD for VOLLEY, across nine documents (Track, Stator, Sled, Payload_3U,
Magazine_Cassette, Brake, Interface_ESPA, Enclosure, Assembly), in three generations.

Full generation history, per-file body counts, and the defect list are in
[`CHANGELOG_CAD.md`](CHANGELOG_CAD.md).


## Two implementations of the same geometry

`build_gen5.py` (CadQuery, B-rep, STEP) and `scad/gen5.scad` (OpenSCAD, CSG, STL) build the same
eight documents from the same parameter file and read nothing of each other's.
`tools/compare_scad_cadquery.py` compares them part by part. It found a real defect on its first
run, the sled rollers were outside their channels in every Gen5 STEP ever built, P71,
which no guard here could have caught, because every guard compares a built artifact against
the script that built it. See [`scad/README.md`](scad/README.md).


## Generations

| Folder | What it is | Status |
|---|---|---|
| `step/gen5/` | Generated from `parameters.json`; eight STEP parts with 23 read-back dimension checks and one 20-instance reference assembly | **Current academic geometry**, documented interference and conceptual interfaces |
| `step/gen3/` | Parameter-reconciled Fusion revision, plus `EMOCD_Gen3.step`, a monolithic single-file model (395 solids) holding all nine sub-systems | **Historical mass and FEA source**; not the Gen5 release geometry |
| `step/gen2/` | First structured revision. Mechanism-level detail arrives: single-layer stator, sled Halbach arrays and rollers, magazine escapement and D6 pins, brake ring spring | SUPERSEDED, carries a 360 mm sled chassis where the spec says 488 mm |
| `step/gen1/` | The original CAD, 2021-2025. Structural envelope rather than mechanism model; the geometry `parameters.json` was reverse-engineered from. Includes the pre-split single-file `EMOCD_Deployer_Assembly_Gen1.step` and a second sled revision, `Sled_Gen1b` | SUPERSEDED, heritage only |

Use Gen5 for the current design. Use Gen3 only when tracing the earlier volume or A4 FEA evidence.

## What is authoritative here

- `parameters.json` is the geometry source of truth. Every dimension lives here, not
  in Fusion (Fusion user parameters are document-scoped and drift silently across the nine
  documents). Change a value here, then regenerate the affected document from script. If
  the CAD and `parameters.json` disagree, `parameters.json` wins and the CAD is wrong.
- CAD is authoritative for geometry, fit, and interference only.
- `analysis/*.py` remains authoritative for mass and performance. Fusion-computed
  masses are proxies (solid-copper stator, solid-aluminium CubeSats, steel standing in for
  NdFeB) and are deliberately excluded from `parameters.json`. Never quote a
  Fusion-computed mass.

## Historical status note (2026-07-28)

At that date this was first-pass CAD, with no structural or magnetic FEA behind it. Several values were
flagged `PROVISIONAL_PENDING_FEA` in `parameters.json`. Open: the sled chassis mass (P5),
the resulting exit velocity (P8), the ESPA envelope overrun (P9), the incomplete mass
rollup (P10), and the CAD-side geometry defects P14, see `../OPEN_PROBLEMS.md`.

What changed on 2026-07-28. The previously committed `step/*.step` set was a
mixed-generation snapshot matching no single generation, and two of its files were stubs:
the stator export contained one solid rather than 162 conductors, and the ESPA
interface contained one solid rather than a flange ring, hub plate, and four gussets.
It was replaced wholesale by the three audited generations. See `CHANGELOG.md` (CAD2 block)
and `OPEN_PROBLEMS.md` P13.

## Before using any file

1. Gen5 for current geometry; Gen3 for the cited historical mass and FEA input. Gen1 and Gen2 carry known dimensional and mechanism
   defects, listed per file in `CHANGELOG_CAD.md`.
2. Cross-check every dimension against `parameters.json` before quoting it.
3. No uncorrected Fusion masses. The modeled mass authority is `analysis/mass_properties.py`;
   its 126.6 kg rollup includes assumptions and is not a measured or complete installed mass.
4. The sled mass conflict was dispositioned on 2026-07-29. The scripts now carry 9.445 kg from Gen3 solid volumes; after the depth-resolved electromagnetic correction the current modeled speed is **16.029 m/s**. Historical note follows: 20.37 m/s assumed a 4.86 kg sled; the Gen3
   geometry implies ~7.50 kg and a provisional 17.88 m/s. Quote neither without the
   conflict (P5, P8). `validation/A4_sled_structural.md` is the analysis that settles it.
5. The ESPA comparison fails: 1839 mm installed against a quoted ~1270 mm class
   envelope, about 44 % over (P9). No host provider has approved an interface; P12
   records the historical compatibility claim and its correction.
6. The stator layer count is an open design decision. Gen1 built two layers, Gen2 and
   Gen3 one, and `parameters.json` flags it open. The electromagnetic consequence, roughly
   x2 force for the same current against x2 copper mass and winding complexity, has never
   been computed (P14).

> Modelling from this repository? [`../CAD_BRIEF.md`](../CAD_BRIEF.md) is written to be read
> first: coordinate frame, part list and assembly order, critical versus soft dimensions, and a
> table resolving every conflict between files here with the side to build. `DIMENSIONS.md`
> and `BOM.md` below are built from `parameters.json` and `analysis/mass_properties.py`, so
> they cannot drift from their sources.

## Contents

- `parameters.json`, the 9-group geometry parameter set, source of truth
- `CHANGELOG_CAD.md`, generation history, per-file inventories, defect IDs (G1-D*, G2-D*,
  G3-D*), and the cross-generation comparison
- `step/gen1/`, `step/gen2/`, `step/gen3/`, STEP exports from Fusion (`.f3d` is not diffable,
  so STEP is what gets committed)
- `step/gen5/`, built by `build_gen5.py` from `parameters.json`, nothing is drawn, so
  it cannot drift from the parameters, it regenerates byte-identically from a clean clone, and
  `build_gen5.py --check` reads 23 dimensions back out of the built solids and compares them to
  the parameter file. See [ADR-026](../docs/adr/026-cad-built-from-parameters.md).
  It is a geometry and interface model, not a manufacturing model: no fillets, no chamfers,
  no fasteners, no harness routing, no tolerancing. Do not send it to a machine shop; do use it
 to check fit, envelope, clearance and station alignment
- `renders/gen5/` is the current Gen5 presentation set generated from the Gen5 geometry.
  `renders/` and `renders/source/` also retain older Gen4 frames prepared by
  `tools/prepare_renders.py`; those have no matching committed Gen4 STEP export and must
  be captioned as historical. `exploded_view.png` comes from the Gen3 monolithic model.
  No performance number is taken from a render.
- `tools/prepare_renders.py`, which crops the raw frames to content, fits them to a
  publishing box and draws the departure direction on each. The direction is per-render
  because the camera flips between views; P43 is what happens when it is wrong
- `DIMENSIONS.md` and `BOM.md`, built by `tools/make_cad_package.py` from
  `parameters.json` and `analysis/mass_properties.py`. Both are guarded by
  `tools/check_artifacts.py`, so a dimension changed without a regenerate is caught
- `tools/make_cad_package.py`, the generator. Edit the sources and re-run it; never edit
  `DIMENSIONS.md` or `BOM.md` directly

The 2-D magnetic cross-section and its FEMM run sheet live in `../analysis/femm/`.
