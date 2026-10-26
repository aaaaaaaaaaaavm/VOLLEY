# VOLLEY — from cassette to orbit

This source package produces the 190-second explanatory film and its three chapter clips. The mechanism is a Blender animation of accepted ACR1 CAD meshes with edited display timing. The deployment comparison is an original principle schematic. The orbital chapter is a separately identified, invariant-checked planar two-body illustration. Current ACR1 command points are 1, 2 and 3 m/s; historical 16.029 m/s and future 1 km/s-and-beyond cases retain separate identities.

## Reproduction

Requirements: Blender 4.3.2, Python 3.12 with NumPy/SciPy/Pillow, ffmpeg and system DejaVu Sans/Bold fonts. Font license accompanies the published repository's visual sources.

The baked `mechanism/VOLLEY_ACR1_operating_cycle.blend` is directly renderable:

```bash
blender -b mechanism/VOLLEY_ACR1_operating_cycle.blend -t 2 -o ./mechanism/frames/ -F JPEG -s 1 -e 1680 -a
python3 mechanism/compose_mechanism.py --root ./mechanism
python3 build_comparison.py
OPENBLAS_NUM_THREADS=1 python3 orbit/physics.py --source-root /path/to/VOLLEY
OPENBLAS_NUM_THREADS=1 python3 orbit/orbit_film.py
python3 orbit/prepare_delivery.py
python3 combine_delivery.py
```

To regenerate the baked animation from the original source, download the accepted scene archive linked in the repository, extract `VOLLEY_G5_ACR1_scientific_views.blend`, then run:

```bash
blender -b -t 2 -P mechanism/animate_mechanism.py -- --source SOURCE.blend --out ./mechanism --build
blender -b -t 2 -P mechanism/finish_render_settings.py -- ./mechanism
```

The scene contains the original 387 represented CAD mesh objects. The animation checks 1,680 display frames for source-plane feeding, unchanged stored inventory, carrier/pallet translation and a clear lift before launch. These animation invariants do not establish contact dynamics or measured performance. Detail omissions and edited timing are recorded in `ANIMATION_PROVENANCE.json`.

The orbital comparison retains a representative 1 m/s spring example and an ideal ground-preset spring with an equal inertial kick. The latter follows the same ideal trajectory. The generic restart-capable upper stage is a surrogate, with no selected vehicle or provider. Orbital plots preserve physical shape; relative-state and altitude views are explicitly magnified. An ellipse is not presented as a newly circularized orbit.

Source geometry and existing computational results retain their repository license and attribution. No supplier image, document or proprietary CAD is redistributed. The film contains English on-screen explanation and timed captions, with no audio.
