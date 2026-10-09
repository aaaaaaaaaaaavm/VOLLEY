# Figure evidence index

A figure without provenance is decoration. This index covers the manuscript and
presentation figures and names their evidence class. Other mission illustrations
and historical drawings have their own captions at point of use. A Monte Carlo
histogram and a measurement can look identical; their evidence classes cannot.

## Evidence classes, used throughout

| Class | Meaning | How many |
|---|---|---:|
| M | Model output. One script, one physics implementation. Reproducible, not corroborated | most |
| X | Cross-checked. Two independent methods agree on the stated quantity; the scope is quoted | selected figures |
| S | Schematic. A drawing, not a computation. No numbers descend from it | 2 |
| R | Render. A picture of geometry. Carries no result at all | Gen5 and historical sets |
| D | Measured data. Something physical was observed | 0 |

> There are no class-D figures in this repository. Nothing has been built, fired or measured
> at any scale, E4. Every plot below is a calculation. That is stated here, once, in the
> index rather than only in a limitations section, because it is the single most important fact
> about all of them.

---

## Paper and flagship figures

The manuscript's numbered plots are drawn by the paper companion's `paper/make_figures.py`
from its local `analysis/` snapshot. The flagship keeps copies for engineering review.
New mission figures below name their own local generator.

| Fig | Shows | Drawn by | From | Supports | Class |
|---|---|---|---|---|:-:|
| V00 | Flagship overview: mission chain, Gen5 frozen baseline, historical study design target and their separate evidence boundaries | `tools/make_repo_overview.py` | `motor_results.json`, `sizing.json`, the validation run-sheet register | README orientation only; every number remains sourced elsewhere | M |
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
| F05 | Relative-impulse phasing vs differential drag | `f05_dragvs()` | `astro` and assumed drag case | A 30° model comparison after an actual relative-state change; waiting alone between zero-impulse releases from an unchanged host does not create persistent phase | M |
| F06 | Satellite, stage range over 30 days | `f06_conj()` | `astro.conjunction(trace=True)` | Deployment safety, §V-D | M |
| F07 | Payload family, force-limited above 1U | `f07_family()` | `motor_model.payload_family()` | Table \ref{tab:family}, kill criterion 1 | M |
| F08 | Eddy-brake arrest, taper-limited to 200 g | `f08_brake()` | `motor_model.regen_brake()` + a first-order plate-drag law | Arrest §III-E. The second leg is a first-order law and nothing more, E20 records that no force, time profile for the arrest exists anywhere | M |
| F09 | Tip-off error budget against deployer classes | `f09_tipoff()` | `analysis/tipoff_release.py` | Kill criterion 4. Both the 2 °/s and 5 °/s lines are drawn because they are two different deployers, and the tighter one is the flown figure | M |
| F11 | Solar-activity sweep against GMAT | `f11_uq()` | `astro.lifetime()` + GMAT R2022a | P16. The figure exists to show the static model returns a flat ratio *by construction*; an independent propagator does not | X |
| F12 | Open-loop velocity-loop response, both gains | `f12_bode()` | `analysis/control_design.py` | A28. Margins, the 48-109 Hz mode band, both crossovers | M |
| F13 | Phase margin against transport delay | `f13_latency()` | `analysis/control_design.py` | A28 band 5. The stability floor at 0.35 ms | M |
| shot.gif | The stroke, animated | `tools/make_animation.py` | `motor_model.shot(trace=True)` | Same integrator as F01 | M |
| P113-S12 | Accepted delivery prefix in six finite-burn twelve-payload screens | `tools/plot_manifest_finite_burn.py` | `analysis/results/manifest_finite_burn.json` | 0/3/4/0/4/5 accepted; no sampled full-manifest closure | M |
| Gen5 mass decision | Dry mass per 3U against two separate mass screens | `tools/plot_gen5_decision.py` | `mass_properties.json` and declared approximate comparators | 10.55 kg/3U; fails both stated comparisons | M |
| Gen5 energy accounting | Rated shot gross, modeled recovery, net and payload kinetic energy | `tools/plot_gen5_decision.py` | `motor_results.json` | 514 J payload out of 2735 J net; grey balance is not an itemized loss budget | M |
| P113-S16 | Same-epoch phasing after a 468 s wait with first-payload differential impulses | `analysis/phasing_reference.py` | `phasing_reference.json`, two-body initial states | Zero impulse stays at zero relative phase; nonzero curves require a relative-state change | M |
| P115 | Current rated prograde impulse versus immediate 450 km orbit geometry | `analysis/rated_orbit_independent.py` | Cartesian DOP853 propagation and vis-viva identity | 16.029 m/s input gives 28.800775 km axis rise; lifetime and mission excluded | X, two-body orbit quantity only |
| P116 | Gen5 side-fed transverse assembly section | `cad/plot_review_packaging.py` | `cad/REVIEW_ASSEMBLY.json` and `cad/parameters.json` | 11 mm width shortfall and exact-solid track/cassette overlap in the reference placement | X, CadQuery/FreeCAD overlap agree |

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

The [Gen5 render set](../cad/renders/gen5/) illustrates the evaluated electromagnetic
geometry; the [Gen5 STEP parts](../cad/step/gen5/) and `cad/build_gen5.py` define its
reproducible model. The [historical study render set](../cad/renders/legacy_study/)
illustrates an unselected gas-guide comparison. Both are class R: a visual fit to CAD,
not evidence of manufacture, motion, tolerance or host accommodation. Earlier Gen4
images in the record remain historical and must not be used as Gen5 geometry.

---

## Validation artefacts that are not figures

These are results in the same sense, and a referee will want them in the same list.

| Artefact | What it is | Where | Class |
|---|---|---|:-:|
| `analysis/results/*.json` | Captured model outputs. `docs/BASELINE.md` checks 23 named headline fields against source scripts; it is not a check of every result file | `analysis/results/` | M |
| 2-D magnetostatic FEM | FEMM/`skfem` solve of the array, agreeing with the analytic model to 0.03 %, the figure after the 2026-08-03 quadrature correction, which found both implementations sharing an invalid winding-thickness rule; the pre-correction agreement was 0.07 % and did not test that rule | `validation/A1_field_femm.md` | X |
| 3-D magnetostatic FEM | `getdp` reduced-scalar-potential solve, 274,105 DoF on a 315,370-node tetrahedral mesh, agreeing with magpylib to 0.059 % | `validation/fem3d/` | X |
| Structural FEM | CalculiX solve of the sled chassis | `validation/A4_sled_structural.md` | M |
| Independent propagator | GMAT R2022a against `astro.py`, and it falsified a claim in the paper's own abstract (P16) | `validation/gmat/` | X |
| CFD | `simpleFoam` external aerodynamics of the Gen5 sled and payload, for the ground-test air correction | `validation/cfd/`, A29 | M |
| Validation run sheets | Named acceptance bands, limitations and failed outcomes; the restored P113-S11 implementation is explicitly post-result and must not be described as predeclared | `validation/` | M |

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
