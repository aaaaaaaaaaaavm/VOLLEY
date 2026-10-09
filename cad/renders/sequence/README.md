# Gen5 intended-operations media

This folder contains a Blender animation and review graphics made from the FreeCAD-linked Gen5 STEP review solids. The sequence illustrates a proposed order of operations. It does **not** validate a feeder, moving clearance, contact, electromagnetic drive, payload release or sled brake. The evaluated static side-fed placement already **fails** by 11 mm across the enclosure, with 32,915 mm³ exact-solid track/cassette overlap on each side; see [P116](../../../validation/P116_gen5_assembly_packaging.md).

| File | Purpose |
|:--|:--|
| [Four-stage hero](gen5_operations_hero.png) | Website and repository front-page storyboard |
| [Eight-second MP4](gen5_intended_sequence.mp4) | 128 Blender frames at 16 fps, with stage labels and on-screen caveats |
| [Animated GIF](gen5_intended_sequence.gif) | Inline GitHub preview of the same conceptual motion |
| [1200×630 share card](gen5_social_preview.png) | Website Open Graph preview and a prepared GitHub social-preview asset |
| `step_01.png` through `step_04.png` | Representative frames from the four operations |
| [PROVENANCE.json](PROVENANCE.json) and [MEDIA_MANIFEST.json](MEDIA_MANIFEST.json) | Input identity, hidden and moving components, output hashes |

The four illustrated stages are **store** (twelve conceptual payload envelopes), **handoff** (one payload moves laterally toward the common sled), **accelerate** (sled and payload move down the powered track), and **depart** (payload continues while sled stops). The selected payload and sled use scripted straight-line keyframes. The track, interface, stator, brake, remaining payload proxies and far cassette are static. The outer enclosure and near cassette shell are hidden for visibility. No contact, timing, stiffness, control or force solution is implied by the animation.

## Rebuild

1. Export the source-linked review STEP display meshes with `cad/tools/export_step_view_meshes.py` in FreeCAD. Follow [the STEP view procedure](../step_review/README.md) to produce `meshes.json` and its OBJ files.
2. Run `blender -b --factory-startup -P cad/tools/render_gen5_sequence.py -- --mesh-manifest /path/to/meshes.json`. The script checks OBJ hashes and placed bounds against the FreeCAD manifest before rendering. Frames are written to `/tmp/volley-gen5-sequence-frames` and four representative images to this directory.
3. Encode the numbered frames at 16 fps to H.264 MP4 or GIF with ffmpeg. Run `blender -b --factory-startup -P cad/tools/compose_gen5_sequence.py` to compose the hero and share card from the four stage views.

The two Blender scripts and the `MEDIA_MANIFEST.json` preserve the route from STEP to publication asset. The poster and share card are layout renders; they add no engineering evidence. The STEP document itself is a conceptual reference assembly, not a manufacturing release.
