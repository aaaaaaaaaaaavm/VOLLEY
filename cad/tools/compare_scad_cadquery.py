"""Compare the OpenSCAD Gen5 model against the CadQuery one, part by part.

WHY THIS EXISTS
---------------
cad/build_gen5.py builds Gen5 with a B-rep kernel; cad/scad/gen5.scad builds it with a CSG
kernel. Neither reads the other, and both read a parameter file built from
cad/parameters.json. Nothing else in this repository has ever checked the geometry a second
way -- parameters.json has been checked against exactly one model built from it.

A disagreement here is one of three things and all three are worth knowing: a bug in the
CadQuery model, a bug in the OpenSCAD model, or an ambiguity in the parameter file that two
readers resolved differently.

Bounding box is exact for both. Volume is exact for the B-rep and tessellated for the CSG,
so cylinders differ by the facet error of $fn -- which is why the tolerance below is a
declared band rather than a bit comparison, and why parts with curved surfaces are marked.

Usage:  python3 cad/tools/compare_scad_cadquery.py
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CQ_STL = os.path.join(HERE, "stl")
SCAD_STL = os.path.join(HERE, "stl", "gen5_scad")

# Declared before the comparison ran.
BBOX_TOL_MM = 0.51        # half a millimetre; facet chords cannot move a planar extent
VOL_TOL_PCT = 2.0         # tessellation of cylinders at $fn=96 against exact B-rep

PARTS = {
    "interface_espa":    ("VOLLEY_Interface_ESPA_Gen5.stl",     True),
    "track":             ("VOLLEY_Track_Gen5.stl",              False),
    "stator":            ("VOLLEY_Stator_Gen5.stl",             False),
    "sled":              ("VOLLEY_Sled_Gen5.stl",               True),
    "magazine_cassette": ("VOLLEY_Magazine_Cassette_Gen5.stl",  True),
    "brake":             ("VOLLEY_Brake_Gen5.stl",              False),
    "payload_3u":        ("VOLLEY_Payload_3U_Gen5.stl",         False),
    "enclosure":         ("VOLLEY_Enclosure_Gen5.stl",          True),
}


def read_stl(path):
    """Return (triangles, is_binary). Handles both encodings."""
    with open(path, "rb") as f:
        head = f.read(5)
        f.seek(0)
        if head == b"solid":
            tris, cur = [], []
            for line in f.read().decode("utf-8", "replace").splitlines():
                s = line.strip().split()
                if s and s[0] == "vertex":
                    cur.append(tuple(float(x) for x in s[1:4]))
                    if len(cur) == 3:
                        tris.append(tuple(cur))
                        cur = []
            return tris
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        tris = []
        for _ in range(n):
            d = struct.unpack("<12fH", f.read(50))
            tris.append(((d[3], d[4], d[5]), (d[6], d[7], d[8]), (d[9], d[10], d[11])))
        return tris


def bbox(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


def volume(tris):
    """Signed tetrahedron sum. Absolute value, since winding may differ between writers."""
    v = 0.0
    for a, b, c in tris:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1])
              - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return abs(v)


def main():
    rows, worst_bbox, worst_vol = [], 0.0, 0.0
    for part, (cq_name, curved) in PARTS.items():
        cq_path = os.path.join(CQ_STL, cq_name)
        sc_path = os.path.join(SCAD_STL, part + ".stl")
        if not (os.path.exists(cq_path) and os.path.exists(sc_path)):
            rows.append(dict(part=part, status="MISSING"))
            continue
        a, b = read_stl(cq_path), read_stl(sc_path)
        ba, bb = bbox(a), bbox(b)
        dbb = max(abs(x - y) for x, y in zip(ba, bb))
        va, vb = volume(a), volume(b)
        dv = abs(va - vb) / va * 100.0 if va else 0.0
        worst_bbox = max(worst_bbox, dbb)
        worst_vol = max(worst_vol, dv)
        rows.append(dict(part=part, curved=curved,
                         bbox_cq=[round(x, 3) for x in ba],
                         bbox_scad=[round(x, 3) for x in bb],
                         bbox_max_delta_mm=round(dbb, 4),
                         vol_cq_mm3=round(va, 1), vol_scad_mm3=round(vb, 1),
                         vol_delta_pct=round(dv, 3),
                         bbox_ok=dbb <= BBOX_TOL_MM, vol_ok=dv <= VOL_TOL_PCT))

    w = max(len(r["part"]) for r in rows)
    print(f"{'part':{w}s} {'bbox dmax':>10s} {'vol CQ':>13s} {'vol SCAD':>13s} "
          f"{'dvol %':>8s}   verdict")
    for r in rows:
        if r.get("status") == "MISSING":
            print(f"{r['part']:{w}s} {'MISSING':>10s}")
            continue
        ok = r["bbox_ok"] and r["vol_ok"]
        mark = "" if not r["curved"] else "  (curved)"
        print(f"{r['part']:{w}s} {r['bbox_max_delta_mm']:10.4f} {r['vol_cq_mm3']:13.1f} "
              f"{r['vol_scad_mm3']:13.1f} {r['vol_delta_pct']:8.3f}   "
              f"{'agree' if ok else 'DISAGREE'}{mark}")

    solved = [r for r in rows if r.get("status") != "MISSING"]
    print(f"\nworst bounding-box delta {worst_bbox:.4f} mm against a {BBOX_TOL_MM} mm band")
    print(f"worst volume delta       {worst_vol:.3f} % against a {VOL_TOL_PCT} % band")
    disagree = [r["part"] for r in solved if not (r["bbox_ok"] and r["vol_ok"])]
    print(f"\n{len(solved) - len(disagree)} of {len(solved)} parts agree"
          + (f"; DISAGREE: {', '.join(disagree)}" if disagree else ""))

    out = dict(comparison="OpenSCAD CSG against CadQuery B-rep, Gen5",
               note="bounding box is exact for both; volume is exact for the B-rep and "
                    "tessellated for the CSG, so curved parts carry facet error at $fn=96. "
                    "Tolerances declared in this file before the comparison ran.",
               bbox_tol_mm=BBOX_TOL_MM, vol_tol_pct=VOL_TOL_PCT,
               worst_bbox_delta_mm=worst_bbox, worst_vol_delta_pct=worst_vol,
               parts=rows)
    path = os.path.join(HERE, "..", "analysis", "results", "scad_cross_check.json")
    with open(os.path.normpath(path), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    return 1 if disagree else 0


if __name__ == "__main__":
    sys.exit(main())
