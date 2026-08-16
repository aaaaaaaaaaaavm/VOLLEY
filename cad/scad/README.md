# The OpenSCAD model, and why there are two

`cad/build_gen5.py` builds Gen5 with **CadQuery**, a B-rep kernel, and exports STEP.
`gen5.scad` builds the same eight documents with **OpenSCAD**, a CSG kernel, and exports STL.

**Neither reads the other.** Both read `parameters.scad`, which is built from
`cad/parameters.json` by `cad/tools/make_scad_params.py` — OpenSCAD has no JSON parser, and a
second model that *pasted* its dimensions would be a second place for them to be wrong, which is
the opposite of what a cross-check is for. ADR-015: derive, never paste.

## Why it exists

Everywhere else this project checks a result by computing it a second way — the analytic Halbach
field against magpylib, both against a meshed FEM, orbit-averaged decay against Cowell RK4. **The
geometry never had that treatment.** `parameters.json` had been checked against exactly one model
built from it, and every guard in `tools/` compares a built artifact either against the
parameter file or against a rebuild of itself. Both agree by construction, because both descend
from the same script.

## What it found on the first run

**Two disagreements, and they were different kinds of thing.**

**One was a real defect in the CadQuery model — [P71](../../OPEN_PROBLEMS.md).** The sled rollers
were placed with a one-sided extrude and a half-width offset, as though the extrude were symmetric.
It is not. The +y roller sat at y 54–70 against a channel at 70–86, entirely inboard, in the stator
gap; the −y roller sat at −102 to −86, entirely outboard. **The sled was asymmetric about y = 0**,
and `build_gen5.py --check` passed throughout, because it verifies extents and station positions
and a part misplaced inside an unchanged envelope satisfies both.

**One was a bug in this model**, caught the same way: the track longeron read a parameter that does
not exist, OpenSCAD evaluated it as `undef`, and the beam silently vanished — 88 % of the part's
volume, with no error. That is a real hazard of this tool and it is recorded here rather than
quietly fixed.

## Running it

```bash
python3 cad/tools/make_scad_params.py                     # regenerate from parameters.json
openscad -D 'PART="sled"' -o out.stl cad/scad/gen5.scad   # one part
bash cad/tools/render_scad.sh --headless                  # the PNG set
python3 cad/tools/compare_scad_cadquery.py                # the cross-check
```

`PART` is any of the eight documents, `mechanism` (everything the enclosure hides), or `all`.

## What neither model is

**A geometry and interface model, not a manufacturing model.** No fillets, fasteners, harness
routing or tolerancing exist in either, and `parameters.json` carries no tolerances to give them.
The comparison uses declared tolerances — 0.51 mm on bounding box, 2 % on volume — because
bounding box is exact for both kernels while volume is exact for the B-rep and tessellated for the
CSG, so curved parts carry facet error at `$fn = 96`.

**`compare_scad_cadquery.py` is a tool, not an analysis run.** Its tolerances were written with it,
not declared in advance in a run sheet, so it carries no acceptance bands and is not numbered as an
A-series run. The defect it found stands on its own: a roller outside its channel is wrong at any
tolerance.
