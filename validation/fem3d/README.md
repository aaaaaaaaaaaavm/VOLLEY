# A2 band 4: the independent 3-D solve

**The one band in [`../A2_field_3d.md`](../A2_field_3d.md) that was declared and not run.**

`E2` objects that this project's field model has only ever been checked *analytic against
analytic* — a closed-form wave model against magpylib, "neither solving a field equation". This
directory is the answer: a meshed 3-D magnetostatic PDE solve, compared against magpylib on
identical geometry.

## Running it

```
python3 build_mesh.py     # gmsh: 3 wavelengths, both arrays, in an air box
python3 make_pro.py       # generates halbach3d.pro from magnetisation.json
getdp halbach3d.pro -msh halbach3d.msh -solve Sol -pos Line
python3 compare_band4.py  # the band 4 comparison
```

## What is committed and what is not

**Committed:** the generators, the generated `.pro`, `magnetisation.json`, and the result.
**Not committed:** `halbach3d.msh` (109 MB) and the getdp working files. They are a function of
`build_mesh.py` and `analysis/motor_model.py`, both of which are committed, so storing them would
be storing an output of a committed input — the same reasoning that keeps `cad/` deriving rather
than pasting (ADR-015).

## Three things that had to be got right

1. **Geometry is imported from `motor_model`, never re-entered**, so the FEM and the analytic
   model cannot describe different machines.
2. **μ_r = 1 throughout**, which is what magpylib assumes. The comparison is therefore between
   two *methods*, not between two material models.
3. **Magnetisation is derived from each block's centroid**, not from its position in a sorted
   list. Both arrays occupy the same x positions, so ordering by x alone pairs them ambiguously
   and would have given one array the other's pattern.

## The bug that made the first solve wrong, and reported success anyway

**The first run converged cleanly and returned a field of exactly zero at every sampled point.**
The solver reported no error at any stage; the residual fell from 150.2 to 4e-13; the log was
clean. Two probes located it:

| Probe | phi |
|---|---:|
| in the air gap | **0** |
| inside a magnet | **1470.69** |

A potential that is nonzero in the magnets and identically zero in the air is not a plausible
field. **`gmsh.model.getBoundary()` on the air volume returns the six outer box faces *and* every
magnet-air interface** — twenty-four magnets' worth of internal surfaces. Tagging all of them as
`Outer` pinned `phi = 0` on every magnet surface, and since the air carries no source, `phi` is
then identically zero throughout the air **by uniqueness**. The solver was solving exactly the
problem it was given, and the problem was wrong.

The fix selects only the faces whose bounding boxes lie on the air box extremes, and **asserts
that exactly six are found**, so a geometry change fails loudly instead of silently returning a
zero field again.

**What caught it was checking the value against physical expectation** — midgap should be of
order 0.7 T, and 0.00000 is not a small number, it is a wrong one. Nothing in the toolchain
objected. This is the same reasoning as the acceptance bands: a run completing is not a run being
right.

## Two environment traps

- **The packaged getdp 3.2.0 is built without Gmsh support** and cannot read MSH4. `build_mesh.py`
  writes MSH 2.2 for this reason.
- **A uniform mesh fine enough for the gap fills the whole air box.** Refinement is confined to a
  box around the arrays; without it the mesh came out at 3,305 nodes, far too coarse to resolve
  the field it exists to measure.
