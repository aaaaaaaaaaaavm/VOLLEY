# Gen6 G1 first-article CAD envelope, revision 0

**Status:** two unselected, parametric FreeCAD 1.0 envelope candidates. This is a mechanical packaging and necessary-resource study for a **single inert 4 kg 3U dummy**, not the four-slot 1U/3U service machine or a design release. No real CubeSat, launch provider or host interface has approved it.

| Candidate | Moving drive element | Native model | STEP review export | STEP-derived Blender view |
|:--|:--|:--|:--|:--|
| A | Captured permanent-magnet armature proxy | [FreeCAD](release/Gen6_G1_A_Envelope.FCStd) | [STEP](release/Gen6_G1_A_Envelope.step) | [JPEG](release/Gen6_G1_A_STEP_derived.jpg) |
| B | Captured conductive-plate armature proxy | [FreeCAD](release/Gen6_G1_B_Envelope.FCStd) | [STEP](release/Gen6_G1_B_Envelope.step) | [JPEG](release/Gen6_G1_B_STEP_derived.jpg) |

The native FreeCAD files contain **editable Part::Box primitives** grouped as fixed structure, captured carrier, spacecraft surrogate and unrated envelopes. [Source code](build.py) and [key parameters](parameters.json) create them. They are not dimensioned production sketches; dimensions for frame members and contact proxies that are not in the parameter file remain explicit in the builder. The STEP files were exported by FreeCAD, read back as solids, and compared by total volume. The [machine-readable FreeCAD report](release/Gen6_G1_Envelope_Report.json) gives each part's proxy volume/mass, five nominal stroke checks and source/export hashes. A separate [FreeCAD mass/CG/inertia ledger](release/Gen6_G1_Partial_Mass_CG_Inertia.json) computes the partial dry geometry and a 4 kg assigned dummy at start and stroke end; it excludes all unrated installed hardware. [P131](../../validation/P131_gen6_go2_article_bounds.md) gives the independent analytic speed, brake, mass and tolerance screens.

The coordinate system is millimetres: **x** is release direction, **y** lateral, **z** upward. The nominal 3U envelope is 340.5 × 100 × 100 mm and starts at x=170 mm. An open 1,800 mm ladder frame carries a 110 mm guide corridor; a captured carrier and contact-face proxy traverse a 1,300 mm powered stroke. A separate 200 mm brake *envelope* follows the drive. At the end of the powered stroke the 3U nose has passed the frame end, while its tail remains in the guide. The model stops at that event: free flight, contact loss and carrier arrest are not simulated.

Nominal side gap is 5 mm per side; armature-to-primary gap is 2 mm. The report checks exact-solid intersection at 0, 325, 650, 975 and 1,300 mm of commanded travel. **Zero nominal intersection is not a tolerance, mechanism, dynamic-release or safety demonstration.** The support lips are geometric contact proxies, not detailed rail bearings. The static brake solid represents occupied space; it has no load path, magnetic design, absorber or reset. The primary solid is a coil-space envelope with no copper, switching or thermal design.

The ~9.93 kg partial material estimate counts only simple aluminium frame/guide/carrier volumes and one armature material proxy. It **excludes** the 4 kg dummy, primary copper/laminations, inverter, source, launch restraint, payload contact hardware, bearings, brake, thermal parts, controls, harness, host mounting and margins. It is neither an installed mass nor the 30 kg P130 assumption. Material densities are declared study values in [parameters.json](parameters.json), not a sourced procurement specification.

## Reproduce

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_first_article/build.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_first_article/mass_properties.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_first_article/export_meshes.py
blender -b --factory-startup -P cad/gen6_first_article/render.py
python3 analysis/gen6_go2_article_bounds.py --check
```

The Blender pipeline tessellates the saved **native FreeCAD solids**, verifies every imported mesh's hash and bounding box, and colors/labels them for review. Lighting, text and camera are presentation elements; the JPEGs are not screenshots of a working mechanism. Regeneration can change binary file hashes due to CAD container metadata; check geometry, volumes and current hash ledger together.

## Required before G1 selection

1. Obtain a real payload/host/provider interface or preserve explicit surrogates and set an allowed load, contact and magnetic-exposure budget.
2. Model actual restraint, pusher/contact, guide bearing, carrier brake/capture, abort, jam recovery and launch load path in controlled native CAD and drawings.
3. Select rated windings, inverter, source and cooling for both candidates; couple 3-D force to electrical and thermal dynamics and count every installed item.
4. Run moving-clearance/tolerance, structure, tip-off, brake and contact analyses on the actual design. Verify sourceable components, their lead times and procurement mass.
5. Rerun the same four-release mission with the selected device mass, delivered-state error, host operations and failure modes. A candidate with no installed-resource benefit can still be valuable for schedule or accuracy only with a measured or customer-priced service reason.
