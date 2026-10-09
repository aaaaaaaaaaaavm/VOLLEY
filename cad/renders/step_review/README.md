# Gen5 and R1 STEP-derived review images

These six JPEGs are **Blender visualizations of STEP B-reps**, tessellated with FreeCAD 1.0. The native FreeCAD documents supply each instance placement and a link to its source STEP part. The exporter reopens every named STEP, checks its volume and placed bounds against the native document, and writes temporary OBJ display meshes. Blender reads those meshes and adds only materials, lights, a floor, cameras and the evidence labels visible on each JPEG. [PROVENANCE.json](PROVENANCE.json) lists the source hashes, included and hidden instances, JPEG hashes and evidence limit for each view.

| Image | What it shows | Evidence boundary |
|:--|:--|:--|
| [Gen5 open reference](gen5_reference_open.jpg) | Twenty-instance reference placement, enclosure hidden | The side-fed track and cassettes still intersect; no physical article |
| [Gen5 closed envelope](gen5_reference_closed.jpg) | Outer reference package | Conceals the known internal clash; no provider envelope approval |
| [Gen5 top view](gen5_fit_plan.jpg) | Track and cassette reference placement, payloads and enclosure hidden | The 11 mm shortfall comes from the [exact-solid audit](../../../validation/P116_gen5_assembly_packaging.md), not image scaling |
| [Gen5 drive detail](gen5_drive_detail.jpg) | Cropped track, stator and sled | No selected winding, control or contact qualification |
| [R1 open candidate](r1_candidate_open.jpg) | Separate widened candidate, enclosure hidden | Scripted routes clear; lift actuator and retention remain undesigned |
| [R1 top view](r1_candidate_plan.jpg) | Candidate cassette and track placement | Unselected geometry, no revised installed mass or host approval |

Regenerate from this repository root with:

```bash
/usr/bin/python3 cad/tools/export_step_view_meshes.py
blender -b --factory-startup -P cad/tools/render_step_review.py -- --mesh-manifest /tmp/volley-step-review-meshes/meshes.json --samples 64
```

The OBJ files in `/tmp` are display meshes; the released geometry remains the source [Gen5 STEP set](../../step/gen5/), [R1 STEP set](../../step/feeder_candidate_r1/) and [FreeCAD review documents](../../native/). The images do not show manufactured surface finish, hardware buildability, moving clearance, tolerances, electrical hardware or payload qualification. The conventional three-dimensional render is evidence of **geometry depiction only**.
