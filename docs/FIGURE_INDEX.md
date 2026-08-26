# Every figure, and what stands behind it

A figure without provenance is decoration. This index gives, for every image this project
publishes: what it shows, the script that draws it, the data it draws from, the claim it
supports, and what class of evidence it is, because a Monte Carlo histogram and a
measurement look identical on a page and are not the same thing.

## Evidence classes, used throughout

| Class | Meaning | How many |
|---|---|---:|
| M | Model output. One script, one physics implementation. Reproducible, not corroborated | most |
| X | Cross-checked. Two independent methods agree, and the agreement is quoted | 3 |
| S | Schematic. A drawing, not a computation. No numbers descend from it | 2 |
| R | Render. A picture of geometry. Carries no result at all | 7 |
| D | Measured data. Something physical was observed | 0 |

> There are no class-D figures in this repository. Nothing has been built, fired or measured
> at any scale, E4. Every plot below is a calculation. That is stated here, once, in the
> index rather than only in a limitations section, because it is the single most important fact
> about all of them.

---

## Paper figures

All are drawn by [`../paper/make_figures.py`](../tools/make_figures.py), which imports
`analysis/` and re-derives nothing. A figure that reimplemented its own physics could drift from
the number it illustrates, which is the defect the generator was written to remove.

| Fig | Shows | Drawn by | From | Supports | Class |
|---|---|---|---|---|:-:|
| D01 | System block diagram: power, control, mechanism, host-interface chains | `legacy/make_diagrams.py` |, | §III architecture | S |
| D02 | Plan-view layout against an ESPA-Grande envelope | `legacy/make_diagrams.py` | `cad/parameters.json` | §III, and kill criterion 2, the figure shows the envelope being exceeded | S |
| F01 | Shot profile: velocity, bank voltage, current | `f01_shot()` | `motor_model.shot(trace=True)` | 16.029 m/s, 162.3 ms, 320 A peak | M |
| F02 | Winding-resolved thrust over one wavelength | `f02_ripple()` | `motor_model.thrust_constant(profile=True)` | K_t = 10.54 N/kA·m, ±1.01 % ripple | X, agrees with a 2-D FEM solve to 0.03 % and a 3-D one to 0.059 % |
| F03 | Closed-loop exit-velocity dispersion, 800 runs | `f03_mc()` | `motor_model.closed_loop_mc()` | 0.0274 m/s (3σ) | M |
| A29-W | Mid-plane slice of kinematic pressure and speed around the Gen5 sled and 3U payload | `validation/cfd/fields.py` | `validation/cfd/free_fine/{constant/polyMesh, 1800/{p,U}}`, 581 779 cells | stagnation at the nose, separation at the shoulders, wake past x = 2.2 m. Pressure only, viscous drag is bounded by a flat-plate correlation, not solved | M |
| A02-F | Halbach airgap field: $B_y$ in the x, y plane, and the profile through the array's 90 mm depth | `analysis/make_field_map.py` | `field_3d.halbach_pair()`, the same builder the thrust integral uses | centre-plane 0.5041 T, depth mean 0.4759 T, ratio 0.9440, the assumption A2 corrected | M |
| A35-L | Constraint ledger: what each requirement is worth alone, and the floor no corner reaches | `analysis/make_ledger_figure.py` | `analysis/results/constraint_ledger.json`, 64 corners | 88.67 kg, 70.06 %, survives every deletion (P95) | M |
| GEN5-X | Blender exploded view of the drive stack: track, stator, sled, payload | `cad/tools/render_blender.py`, view `exploded` | `cad/stl/*_Gen5.stl` | geometry only; offsets are presentation and nothing reads them | S |
| F04 | Orbital lifetime vs deployment altitude | `f04_life()` | `astro.lifetime()` | x1.60 multiplier | M |
| F05 | Constellation seeding vs differential drag | `f05_dragvs()` | `astro` | 30° in 1.4 days vs 25. Caption must name release timing at 468 s as the free baseline (P56) | M |
| F06 | Satellite, stage range over 30 days | `f06_conj()` | `astro.conjunction(trace=True)` | Deployment safety, §V-D | M |
| F07 | Payload family, force-limited above 1U | `f07_family()` | `motor_model.payload_family()` | Table \ref{tab:family}, kill criterion 1 | M |
| F08 | Eddy-brake arrest, taper-limited to 200 g | `f08_brake()` | `motor_model.regen_brake()` + a first-order plate-drag law | Arrest §III-E. The second leg is a first-order law and nothing more, E20 records that no force, time profile for the arrest exists anywhere | M |
| F09 | Tip-off error budget against deployer classes | `f09_tipoff()` | `analysis/tipoff_release.py` | Kill criterion 4. Both the 2 °/s and 5 °/s lines are drawn because they are two different deployers, and the tighter one is the flown figure | M |
| F11 | Solar-activity sweep against GMAT | `f11_uq()` | `astro.lifetime()` + GMAT R2022a | P16. The figure exists to show the static model returns a flat ratio *by construction*; an independent propagator does not | X |
| F12 | Open-loop velocity-loop response, both gains | `f12_bode()` | `analysis/control_design.py` | A28. Margins, the 48-109 Hz mode band, both crossovers | M |
| F13 | Phase margin against transport delay | `f13_latency()` | `analysis/control_design.py` | A28 band 5. The stability floor at 0.35 ms | M |
| shot.gif | The stroke, animated | `tools/make_animation.py` | `motor_model.shot(trace=True)` | Same integrator as F01 | M |

Numbering note: there is no F10. It was withdrawn and the gap is left rather than
renumbered, so a reference to F10 in any older document resolves to nothing instead of silently
to the wrong figure.

### The build stamps

`figures/BUILD.json` and `BUILD_anim.json` record the operating point each figure set was
drawn from, plus a digest of `analysis/results/motor_results.json`. A rebuild whose PNGs come
out byte-identical leaves nothing in git, so commit times alone cannot distinguish "not
rebuilt" from "rebuilt, unchanged". The stamps are what `tools/check_artifacts.py` compares.
They previously held only a hand-picked subset of the operating point and so could not see the
2026-08-13 controller change at all; the digest closes that.

---

## Renders

Seven images under `cad/renders/`, produced in Fusion from the Gen4 assembly and processed by
`cad/tools/prepare_renders.py` (crop, fit to 1600 x 900, departure arrow).

> These are class R and they carry a disclosure. Gen4 has never been exported, and its
> stations do not match the parameters the published numbers rest on, it releases at
> s = 1200 mm where `analysis/` assumes 1500 mm (P32, P43). The renders therefore show
> geometry that no committed file matches. They are kept because they are the only visual
> record of the assembly, and the mismatch is stated wherever they appear rather than left for a
> reader to find. The geometry that *is* committed and *does* match is Gen5, generated by
> `cad/build_gen5.py`, and it has no renders.

---

## Validation artefacts that are not figures

These are results in the same sense, and a referee will want them in the same list.

| Artefact | What it is | Where | Class |
|---|---|---|:-:|
| `analysis/results/*.json` | Every computed value, 33 files. `docs/BASELINE.md` is generated from them and `make_baseline.py --check` verifies 23 of them against the scripts on every commit | `analysis/results/` | M |
| 2-D magnetostatic FEM | FEMM/`skfem` solve of the array, agreeing with the analytic model to 0.03 %, the figure after the 2026-08-03 quadrature correction, which found both implementations sharing an invalid winding-thickness rule; the pre-correction agreement was 0.07 % and did not test that rule | `validation/A1_field_femm.md` | X |
| 3-D magnetostatic FEM | `getdp` reduced-scalar-potential solve, 274,105 DoF on a 315,370-node tetrahedral mesh, agreeing with magpylib to 0.059 % | `validation/fem3d/` | X |
| Structural FEM | CalculiX solve of the sled chassis | `validation/A4_sled_structural.md` | M |
| Independent propagator | GMAT R2022a against `astro.py`, and it falsified a claim in the paper's own abstract (P16) | `validation/gmat/` | X |
| CFD | `simpleFoam` external aerodynamics of the Gen5 sled and payload, for the ground-test air correction | `validation/cfd/`, A29 | M |
| 27 run sheets | Every analysis, each with its acceptance bands declared and committed before its script existed | `validation/` |, |

---

## How a result gets into this repository

The order is fixed and the first step is the one that matters.

1. Bands are declared and committed before the script exists. Verified by
   `git show --stat <band commit> -- <script>` returning nothing. A band names the plane, the
   quantity and, where two references are possible, both of them, because A1's row failed for
   exactly that ambiguity.
2. The script is written and run.
3. A missed band produces a numbered defect, never a widened band. No band in this
   repository has ever been edited after its run. Two are recorded as *badly chosen* and left
   exactly as declared, with the reason written beside them.
4. Results land in `analysis/results/*.json`, and every document that quotes them is
   generated from those files or checked against them.
5. Figures are regenerated from the scripts, never redrawn, and stamped.
6. The paper is rebuilt last. Scripts, then figures, then paper, never the reverse.

This has caught, so far: a minimum-separation figure wrong by 5.7x, an inter-array force
37 % high, a thrust constant 57 % high inside a new analysis, an invariance claim in
the paper's own abstract, a 3-D field solve that converged cleanly and returned exactly
zero, and a published control gain that was linearly unstable. None of those was found by
the tool that produced them. All were found by a number being compared to something declared in
advance.

---

## What this index deliberately does not do

It does not rank the figures by how convincing they are. The evidence class does that, and
the honest reading of the class column is that this project has no measurements. Adding one
is what `docs/B1_ORDER.md` exists for, and it costs about ₹22,000.
