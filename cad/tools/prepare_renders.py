"""Crop Fusion renders to their content and annotate the deployment direction.

WHY THIS EXISTS
---------------
The Gen1-Gen3 render set was factually wrong in a way that mattered: seq2_midstroke.png and
seq3_release.png -- used in README.md and on the Pages site -- showed the payload departing
THROUGH THE ESPA MOUNTING FLANGE, the face that bolts to the host, and depicted the CubeSat as
a road truck from a sample-asset library. A reader taking those at face value would conclude
the machine fires backwards into its own host. That is P43.

The replacement renders have the geometry right -- the satellite leaves along the track axis,
out the muzzle, away from the flange. This script does the two things that can be fixed outside
Fusion:

  1. CROP to content. The raw frames put the subject in about a quarter of the frame, so at
     GitHub's display width the detail disappears.
  2. ANNOTATE the direction, because the whole point of replacing the old set is a directional
     error, and an image that merely happens to be right is weaker than one that says so.

WHAT IT CANNOT FIX, and needs a re-render in Fusion:
  - Material contrast. Magnets, copper stator, titanium sled and copper fin are all one grey.
  - Render noise. The raytrace has not converged; the speckle is visible.

Run:  python3 cad/tools/prepare_renders.py --src <dir> --out cad/renders
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

PAD = 28                      # px of margin to leave around the cropped content
TARGET_W = 1600               # publishing box, width
TARGET_H = 900                # publishing box, height. Images fit inside; aspect preserved.
BG = (247, 248, 250, 255)
INK = (17, 24, 39, 255)
ACCENT = (11, 105, 212, 255)

# Per-render annotation.
#
# `dir` is which way the payload actually leaves IN THAT FRAME, and it is per-render because the
# camera flips between views. Getting this wrong would reproduce, in the fix, the exact error the
# fix exists to correct -- the first pass drew every arrow leftward and pointed brake.png's arrow
# back into its own machine. Check each render before changing a direction here.
SPEC = {
    "hero_open":       dict(dir="left",  label="deployment: along the track axis, 16.388 m/s"),
    "espa_interface":  dict(dir="left",  label="payload departs AWAY from the ESPA flange"),
    "brake":           dict(dir="right", label="sled arrested by the eddy brake; payload departs"),
    "sled_detail":     dict(dir="left",  label="reusable sled; the magnets never leave the machine"),
    "envelope_closed": dict(dir="left",  label="closed envelope, 1839 mm along the track"),
    # No zone lengths here: this is Gen4 geometry, whose release station is s = 1200 mm against
    # the analysis model's 1500 mm. CHANGELOG_CAD.md forbids a Gen4 performance claim until the
    # partial-overlap calculation is done, and a caption is a claim.
    "track_stator":    dict(dir="right", label="track and stator; the payload leaves this end"),
    "magazine_feed":   dict(dir=None,    label="axial view, down the bore: the payload leaves along this axis"),
}


def content_bbox(im, tol=8):
    """Bounding box of everything that is not background, from the corner colour."""
    rgb = im.convert("RGB")
    bg = rgb.getpixel((2, 2))
    # Difference image, thresholded, then getbbox.
    diff = Image.new("L", rgb.size, 0)
    px, dp = rgb.load(), diff.load()
    w, h = rgb.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if abs(r - bg[0]) > tol or abs(g - bg[1]) > tol or abs(b - bg[2]) > tol:
                dp[x, y] = 255
    return diff.getbbox()


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def prepare(src, dst, name):
    im = Image.open(src).convert("RGBA")
    flat = Image.new("RGBA", im.size, BG)
    flat.alpha_composite(im)

    box = content_bbox(flat)
    if box:
        l, t, r, b = box
        l, t = max(0, l - PAD), max(0, t - PAD)
        r, b = min(flat.width, r + PAD), min(flat.height, b + PAD)
        flat = flat.crop((l, t, r, b))

    # Fit inside a publishing box rather than forcing a width. Forcing the width turned
    # magazine_feed -- a narrow vertical strip once cropped -- into a 1600x4576 tower.
    s = min(TARGET_W / flat.width, TARGET_H / flat.height)
    if s != 1.0:
        flat = flat.resize((max(1, int(flat.width * s)), max(1, int(flat.height * s))),
                           Image.LANCZOS)

    spec = SPEC.get(name, dict(dir=None, label=""))
    bar_h = 74
    f = font(26)

    # The canvas has to hold the caption, not just the picture. Sizing it from the image alone
    # clipped magazine_feed -- a narrow vertical strip -- to "axial view, down the".
    m = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    cap_w = int(m.textlength(spec["label"], font=f)) + 2 * 26 if spec["label"] else 0
    canvas_w = max(flat.width, cap_w)
    ox = (canvas_w - flat.width) // 2

    # Pad with the render's own plate colour, not BG -- otherwise the fill shows as a seam
    # either side of a narrow image.
    plate = flat.convert("RGB").getpixel((1, 1)) + (255,)
    out = Image.new("RGBA", (canvas_w, flat.height + bar_h), BG)
    if ox:
        out.paste(Image.new("RGBA", (canvas_w, flat.height), plate), (0, 0))
    out.alpha_composite(flat, (ox, 0))
    d = ImageDraw.Draw(out)

    y0 = flat.height
    d.line([(0, y0), (out.width, y0)], fill=(226, 232, 240, 255), width=2)

    if spec["label"]:
        d.text((26, y0 + 24), spec["label"], font=f, fill=INK)

    if spec["dir"] in ("left", "right"):
        # Deployment arrow, drawn on the side the payload actually leaves towards.
        ay = int(flat.height * 0.12)
        span = int(flat.width * 0.28)
        fv = font(30)
        if spec["dir"] == "left":
            tip, tail = ox + int(flat.width * 0.05), ox + int(flat.width * 0.05) + span
            head = [(tip, ay), (tip + 24, ay - 13), (tip + 24, ay + 13)]
            tx = tail + 16
        else:
            tip, tail = ox + int(flat.width * 0.95), ox + int(flat.width * 0.95) - span
            head = [(tip, ay), (tip - 24, ay - 13), (tip - 24, ay + 13)]
            tx = tail - 16 - d.textlength("16.388 m/s", font=fv)
        d.line([(tail, ay), (tip, ay)], fill=ACCENT, width=6)
        d.polygon(head, fill=ACCENT)
        d.text((tx, ay - 17), "16.388 m/s", font=fv, fill=ACCENT)

    out.convert("RGB").save(dst, "PNG", optimize=True)
    return out.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for fn in sorted(os.listdir(a.src)):
        if not fn.endswith(".png"):
            continue
        name = os.path.splitext(fn)[0]
        size = prepare(os.path.join(a.src, fn), os.path.join(a.out, fn), name)
        print(f"  {fn:24} -> {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
