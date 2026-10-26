# VOLLEY Gen5 ACR1 — polished CAD render derivative

Blender 4.3.2 Workbench restyles the accepted scientific scene. No CAD mesh coordinates, object transforms, mechanism design or physics inputs change. Charcoal/ivory styling and one teal accent distinguish the selected feed/pallet path. Exact input pins, cameras, shown/hidden part names and geometry identity checks accompany each view.

The input is the existing `downloads/VOLLEY_G5_ACR1_editable_scene.zip` from the Main VOLLEY site. Extract its `VOLLEY_G5_ACR1_scientific_views.blend` beside these scripts. `SOURCE_PINS.json` records the archive/scene SHA-256 and frozen native-state identities. This derivative distributes the editable camera/style/visibility script rather than duplicating the full accepted raw scene.

```sh
blender -b -t 4 -P polish_acr1.py -- --source VOLLEY_G5_ACR1_scientific_views.blend --output . --preview
blender -b -t 4 -P polish_acr1.py -- --source VOLLEY_G5_ACR1_scientific_views.blend --output .
python3 compose_editorial.py
```

Editorial composition needs Pillow and system DejaVu Sans fonts. Captions and numbered source-target markers are composed after rendering; they are not hardware. Blender can optionally save a compressed editable derivative with `--save-scene`.

Use `assembly_hero.png` or its WebP alternative for a landscape overview; `feeder_detail_annotated.png` for the guided-feed explanation; and `operating_sequence.png` for the custody route. Preserve their captions, omission disclosures and source-provenance link when integrating them. Alt text should say CAD-derived render and name the source pose or isolated subassembly. The report and presentation PDFs remain their exact submitted editions.
