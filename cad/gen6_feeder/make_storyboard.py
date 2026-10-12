#!/usr/bin/env python3
"""Assemble four labeled Blender CAD-state renders into a static storyboard."""
from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
names = ("00_stowed", "01_transfer_armed", "02_mid_transfer", "03_seated")
tiles = []
for name in names:
    path = HERE / "release" / f"Gen6_Feed_{name}_STEP_derived.jpg"
    with Image.open(path) as im:
        tiles.append(ImageOps.fit(im.convert("RGB"), (1200, 675)))
canvas = Image.new("RGB", (2400, 1350), (11, 24, 38))
for tile, xy in zip(tiles, ((0,0), (1200,0), (0,675), (1200,675))):
    canvas.paste(tile, xy)
out = HERE / "release" / "Gen6_Feed_One_Cell_Storyboard.jpg"
canvas.save(out, quality=91, subsampling=0)
print(out)
