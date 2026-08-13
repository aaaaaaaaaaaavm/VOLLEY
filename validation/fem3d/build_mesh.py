"""A2 band 4: 3-D magnetostatic mesh of the double-sided Halbach array, for getdp.

Geometry is read from motor_model so the FEM and the analytic model cannot describe
different machines. Three wavelengths, both arrays, in an air box; the field is sampled on
the centre wavelength, where band 5 already showed the array is effectively infinite.
"""
import os
import sys

import gmsh

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "analysis"))
import motor_model as mm  # noqa: E402

N_WAVE = 3
W, TH, GAP, DEPTH = mm.W, mm.TH, mm.GAP, mm.DEPTH   # 12, 8, 12, 90 mm in metres
NBLK = mm.NBLK
LAM = mm.LAM

# Air box: generous compared with the array so the far boundary does not load the solution.
PAD_X, PAD_Y, PAD_Z = 3 * LAM, 8 * GAP, 1.5 * DEPTH


def main(out):
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("halbach3d")
    occ = gmsh.model.occ

    mags = []                      # (tag, block index i, array sign)
    for sgn, step in ((+1, -1), (-1, +1)):
        y0 = (GAP / 2) if sgn > 0 else (-GAP / 2 - TH)
        for i in range(N_WAVE * NBLK):
            x = (i - N_WAVE * NBLK / 2) * W
            t = occ.addBox(x, y0, -DEPTH / 2, W, TH, DEPTH)
            mags.append((t, i, step))

    Lx = N_WAVE * NBLK * W + 2 * PAD_X
    air = occ.addBox(-Lx / 2, -(GAP / 2 + TH + PAD_Y), -(DEPTH / 2 + PAD_Z),
                     Lx, 2 * (GAP / 2 + TH + PAD_Y), DEPTH + 2 * PAD_Z)
    occ.synchronize()

    # Embed the magnets in the air region so the mesh is conformal across every interface.
    out_dt, _ = occ.fragment([(3, air)], [(3, t) for t, _, _ in mags])
    occ.synchronize()

    vols = [t for d, t in gmsh.model.getEntities(3)]
    # The air volume is the one with the largest bounding box.
    def span(v):
        b = gmsh.model.getBoundingBox(3, v)
        return (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2])
    air_v = max(vols, key=span)
    mag_v = [v for v in vols if v != air_v]

    # Physical groups: one per magnet so each can carry its own magnetisation direction.
    gmsh.model.addPhysicalGroup(3, [air_v], 1000, name="Air")
    # Both arrays occupy the same x positions, so ordering by x alone pairs them ambiguously.
    # Each magnet's block index and array are recovered from its centroid instead, and the
    # magnetisation is written out beside the mesh so the .pro cannot disagree with it.
    import json
    import math
    mags_out = {}
    for k, v in enumerate(sorted(mag_v, key=lambda v: (gmsh.model.getBoundingBox(3, v)[0],
                                                       gmsh.model.getBoundingBox(3, v)[1]))):
        b = gmsh.model.getBoundingBox(3, v)
        xc, yc = (b[0] + b[3]) / 2, (b[1] + b[4]) / 2
        i = int(round(xc / W + N_WAVE * NBLK / 2 - 0.5))
        step = -1 if yc > 0 else +1                      # matches build_field's (+GAP/2,-1)
        ang = math.radians((90 + step * i * 90) % 360)
        gmsh.model.addPhysicalGroup(3, [v], 2000 + k, name=f"Mag{k}")
        mags_out[2000 + k] = dict(i=i, step=step,
                                  M=[mm.BR / (4e-7 * math.pi) * math.cos(ang),
                                     mm.BR / (4e-7 * math.pi) * math.sin(ang), 0.0])
    json.dump(dict(n_wave=N_WAVE, Br=mm.BR, mags=mags_out),
              open(os.path.join(os.path.dirname(out), "magnetisation.json"), "w"), indent=1)
    surf = [t for d, t in gmsh.model.getBoundary([(3, air_v)], oriented=False)]
    gmsh.model.addPhysicalGroup(2, surf, 3000, name="Outer")

    # A uniform mesh fine enough for the gap would fill the whole air box, so refinement is
    # confined to a box around the arrays and the gap between them. Everything outside it is
    # only there to keep the far boundary off the solution.
    fine = gmsh.model.mesh.field.add("Box")
    gmsh.model.mesh.field.setNumber(fine, "VIn", TH / 6)
    gmsh.model.mesh.field.setNumber(fine, "VOut", LAM / 2)
    gmsh.model.mesh.field.setNumber(fine, "XMin", -N_WAVE * NBLK * W / 2 - W)
    gmsh.model.mesh.field.setNumber(fine, "XMax", N_WAVE * NBLK * W / 2 + W)
    gmsh.model.mesh.field.setNumber(fine, "YMin", -(GAP / 2 + TH) * 1.6)
    gmsh.model.mesh.field.setNumber(fine, "YMax", (GAP / 2 + TH) * 1.6)
    gmsh.model.mesh.field.setNumber(fine, "ZMin", -DEPTH / 2 * 1.3)
    gmsh.model.mesh.field.setNumber(fine, "ZMax", DEPTH / 2 * 1.3)
    gmsh.model.mesh.field.setNumber(fine, "Thickness", LAM)
    gmsh.model.mesh.field.setAsBackgroundMesh(fine)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
    gmsh.model.mesh.generate(3)
    # MSH2, not MSH4: the packaged getdp 3.2.0 is built without Gmsh support and can
    # only read the legacy format natively.
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write(out)
    n = gmsh.model.mesh.getNodes()[0].size
    print(f"magnet volumes {len(mag_v)}, air volume {air_v}, nodes {n}")
    gmsh.finalize()
    return len(mag_v)


if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    n = main(os.path.join(d, "halbach3d.msh"))
    print("-> halbach3d.msh")
