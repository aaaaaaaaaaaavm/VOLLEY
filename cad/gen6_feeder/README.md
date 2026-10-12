# Gen6 fixed-cassette feeder, one-cell study

**Status:** unselected mechanism study for one inert 3U envelope. This is a separate Gen6 geometry revision. It is not a Gen5 repair, manufacturing release, qualified restraint, or four-satellite magazine.

The [cycle and fault record](cycle_and_faults.md) defines the state sequence and the condition that must precede a powered shot. The [concept decision](concept_decision.md) compares fixed-cassette transfer drives using the same criteria. The reference drive is a captive lead-screw pusher; its thread, motor, bearings, latch, sensor, structural rating and space compatibility are **not** modeled.

The [FreeCAD builder](build.py) creates editable Part primitives in four transfer-state documents. It exports STEP and a JSON report containing exact-solid overlap, clearance and export readback checks. All dimensions are in millimetres. The surrogate spacecraft is a 340.5 × 100 × 100 mm box, not a real CubeSat interface.

The [Blender review images](release/) are labeled renders of geometry tessellated from the saved FreeCAD state documents, with per-part mesh hashes and bounds verified before rendering. They are not tool screenshots or test observations.

![Four-state one-cell feeder geometry storyboard, from STEP-checked FreeCAD geometry. This does not depict a working drive or restraint.](release/Gen6_Feed_One_Cell_Storyboard.jpg)

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_feeder/build.py
python3 cad/gen6_feeder/tolerance_screen.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_feeder/export_meshes.py
blender -b --factory-startup -P cad/gen6_feeder/render.py
python3 cad/gen6_feeder/make_storyboard.py
```

## Study boundaries

- The original Gen5 cassette/track conflict remains a failed criterion of the evaluated Gen5 configuration.
- The study begins with one fixed side cassette. A four-cell 1U/3U layout is future work.
- The cassette gate lifts clear of the transfer corridor in the model. Its actuator, fail-safe return, debris behavior and launch lock are unknown.
- The cradle side guide retracts during transfer. The reference model has no selected launch restraint or proof of power-loss containment during a partly transferred payload.
- The static solids are envelope and contact proxies. A zero-overlap result is only a nominal geometry screen; it is not a tolerance, load, jam, thermal, shock or reliability result.
- The [interval sensitivity screen](release/Gen6_Feed_Assumed_Tolerance_Screen.json) uses declared hypothetical dimensional perturbations. Its positive clearance numbers are conditional on those assumptions and do not cover thermal growth, launch deflection or real spacecraft tolerance.

The exit criterion for this study is a useful, inspectable geometry and a precise list of what prevents a feed-ready or flight-ready claim. It does not close the feeder design by itself.
