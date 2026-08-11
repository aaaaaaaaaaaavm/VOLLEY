"""
VOLLEY | The three-dimensional field, and the depth assumption inside Kt.

WHAT IS ACTUALLY BEING TESTED
-----------------------------
motor_model.build_field() already uses magpylib Cuboid sources with the real 90 mm depth, so
the FIELD has always been 3-D and exact -- superposition of closed-form solutions for uniformly
magnetised blocks is exact in free space, and this machine is ironless.

The two-dimensional assumption is not in the field. It is in the thrust integral:

    By = field.getB(np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1))[:, 1]
    ...
    return float((...).sum() * dx * (WIND_THICK / 2) * DEPTH)

thrust_constant() samples By only on the centre plane z = 0, then multiplies by the full
DEPTH as though that value held across the whole 90 mm. It does not. The true depth-averaged
By is lower, so Kt is overstated by some factor, and that factor has never been computed.

If it moves Kt it moves the baseline. Protocol is stop and report, not re-baseline.

Bands declared in validation/A2_field_3d.md at 964af2c, BEFORE this file existed.
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')


def kt_depth_resolved(depth=None, nz=9, nx=240, ny=9, n_wave=7):
    """motor_model.thrust_constant, with By averaged over z instead of sampled at z = 0.

    Deliberately a copy of the original integral with ONE change, so the comparison isolates
    the depth assumption and nothing else. Same winding, same currents, same x and y
    quadrature, same phase search. Setting nz = 1 reproduces the original exactly.
    """
    DEPTH = mm.DEPTH if depth is None else depth
    # Rebuild the field at the requested depth. Everything else follows motor_model.
    LAM, NBLK, TH, GAP, BR, W = mm.LAM, mm.NBLK, mm.TH, mm.GAP, mm.BR, mm.W
    import magpylib as magpy

    def arr(y_face, step):
        mags = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * W
            ang = (90 + step * i * 90) % 360
            pol = [BR * np.cos(np.radians(ang)), BR * np.sin(np.radians(ang)), 0]
            y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
            mags.append(magpy.magnet.Cuboid(polarization=pol, dimension=(W, TH, DEPTH),
                                            position=(x, y_c, 0)))
        return magpy.Collection(mags)

    field = magpy.Collection([arr(+GAP / 2, -1), arr(-GAP / 2, +1)])

    xs = np.linspace(0, LAM, nx, endpoint=False)
    y_nodes, y_weights = np.polynomial.legendre.leggauss(ny)
    ys = y_nodes * mm.WIND_THICK / 2
    if nz == 1:
        z_nodes, z_weights = np.array([0.0]), np.array([2.0])
    else:
        z_nodes, z_weights = np.polynomial.legendre.leggauss(nz)
    zs = z_nodes * DEPTH / 2

    # By on a (nz, ny, nx) grid, then collapse z by Gauss-Legendre into a depth MEAN.
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='xy')
    pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    By3 = field.getB(pts)[:, 1].reshape(X.shape)          # (ny, nx, nz)
    By = (By3 * (z_weights / 2.0)[None, None, :]).sum(axis=2)   # depth mean, (ny, nx)

    belt = LAM / 6
    seq = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]
    ph = np.array([seq[int((x % LAM) // belt)][0] for x in xs])
    sg = np.array([seq[int((x % LAM) // belt)][1] for x in xs])
    dx = LAM / nx

    def thrust(shift, phi, K):
        Byx = np.roll(By, +shift, axis=1)
        te = 2 * math.pi * (shift * dx) / LAM - phi
        i = np.array([math.cos(te), math.cos(te - 2 * math.pi / 3),
                      math.cos(te + 2 * math.pi / 3)])
        Jz = K * i[ph] * sg / mm.WIND_THICK
        return float((y_weights[:, None] * Jz[None, :] * Byx).sum()
                     * dx * (mm.WIND_THICK / 2) * DEPTH)

    phis = np.linspace(0, 2 * math.pi, 144, endpoint=False)
    means = [np.mean([thrust(s, p, 45e3) for s in range(0, nx, 10)]) for p in phis]
    phi_best = phis[int(np.argmax(means))]
    Fs = np.array([thrust(s, phi_best, 45e3) for s in range(0, nx, 5)])
    F_mean = Fs.mean()
    ripple = (Fs.max() - Fs.min()) / 2 / F_mean * 100
    # Normalise EXACTLY as motor_model does -- scale the one-wavelength force by the number
    # of wavelengths under the sled, then divide by the 45 kA/m test sheet current. The first
    # version divided by depth instead and reported Kt 57 % high; band 1 caught it, which is
    # what band 1 is for.
    Kt = F_mean * (mm.SLED_ACTIVE_LEN / LAM) / 45e3 * 1e3      # N per kA/m
    return dict(Kt=Kt, ripple=ripple, F_mean=F_mean, depth=DEPTH, nz=nz)


def far_field(depth, r=0.5, n_wave=7):
    """|B| at r metres along +z, the depth axis the 2-D model has no information about."""
    import magpylib as magpy
    LAM, NBLK, TH, GAP, BR, W = mm.LAM, mm.NBLK, mm.TH, mm.GAP, mm.BR, mm.W

    def arr(y_face, step):
        mags = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * W
            ang = (90 + step * i * 90) % 360
            pol = [BR * np.cos(np.radians(ang)), BR * np.sin(np.radians(ang)), 0]
            y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
            mags.append(magpy.magnet.Cuboid(polarization=pol, dimension=(W, TH, depth),
                                            position=(x, y_c, 0)))
        return magpy.Collection(mags)
    field = magpy.Collection([arr(+GAP / 2, -1), arr(-GAP / 2, +1)])
    B = field.getB([[0.0, 0.0, r]])[0]
    return float(np.linalg.norm(B))


def fundamental(n_wave, nx=480):
    """Fundamental amplitude of By at midgap over the CENTRAL wavelength (band 5)."""
    import magpylib as magpy
    LAM, NBLK, TH, GAP, BR, W, DEPTH = (mm.LAM, mm.NBLK, mm.TH, mm.GAP, mm.BR, mm.W, mm.DEPTH)

    def arr(y_face, step):
        mags = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * W
            ang = (90 + step * i * 90) % 360
            pol = [BR * np.cos(np.radians(ang)), BR * np.sin(np.radians(ang)), 0]
            y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
            mags.append(magpy.magnet.Cuboid(polarization=pol, dimension=(W, TH, DEPTH),
                                            position=(x, y_c, 0)))
        return magpy.Collection(mags)
    field = magpy.Collection([arr(+GAP / 2, -1), arr(-GAP / 2, +1)])
    xs = np.linspace(-LAM / 2, LAM / 2, nx, endpoint=False)
    By = field.getB(np.stack([xs, np.zeros(nx), np.zeros(nx)], 1))[:, 1]
    # Fundamental amplitude by projection onto one period.
    c = 2.0 / nx * np.abs(np.sum(By * np.exp(-2j * np.pi * xs / LAM)))
    return float(c)


def midgap_fundamental_magpy():
    """Band 4's reference quantity: DOUBLE-SIDED FUNDAMENTAL of By at midgap, z = 0."""
    return fundamental(7)


if __name__ == '__main__':
    out = {}
    print("A2: the depth assumption inside Kt\n")

    base = kt_depth_resolved(nz=1)
    print(f"centre-plane only (reproduces motor_model): Kt = {base['Kt']:.4f} N/kA.m")
    ref_kt, ref_ripple = mm.thrust_constant()
    print(f"motor_model.thrust_constant():               Kt = {ref_kt*1e3:.4f} N/kA.m")
    print(f"   reproduction error {100*abs(base['Kt']-ref_kt*1e3)/(ref_kt*1e3):.3f} %\n")

    res = kt_depth_resolved()
    ratio = res['Kt'] / base['Kt']
    print(f"depth-resolved, 90 mm:  Kt = {res['Kt']:.4f} N/kA.m")
    print(f"RATIO depth-resolved / centre-plane = {ratio:.4f}\n")

    deep = kt_depth_resolved(depth=0.900)
    deep1 = kt_depth_resolved(depth=0.900, nz=1)
    conv = deep['Kt'] / deep1['Kt']
    print(f"band 1, DEPTH = 900 mm: ratio {conv:.4f} (should approach 1.000)\n")

    ff_real, ff_deep = far_field(mm.DEPTH), far_field(0.900)
    print(f"band 3, |B| at 500 mm on +z: real {ff_real:.3e} T, deep {ff_deep:.3e} T, "
          f"ratio {ff_real/ff_deep:.4f}\n")

    f7, f21 = fundamental(7), fundamental(21)
    print(f"band 5, fundamental at centre: 7 waves {f7:.5f} T, 21 waves {f21:.5f} T, "
          f"ratio {f7/f21:.5f}\n")

    bands = [
        ('1', 'depth-resolved integral converges to centre-plane at 900 mm',
         f"ratio {conv:.4f}", bool(abs(conv - 1.0) <= 0.01)),
        ('2', 'Kt(depth-resolved)/Kt(centre-plane) >= 0.95',
         f"{ratio:.4f}", bool(ratio >= 0.95)),
        ('3', 'far field at 500 mm <= 0.60x the infinite-depth case',
         f"{ff_real/ff_deep:.4f}", bool(ff_real / ff_deep <= 0.60)),
        ('5', '7-wavelength array within 2 % of 21 at its centre',
         f"{f7/f21:.5f}", bool(abs(f7 / f21 - 1.0) <= 0.02)),
    ]
    print("bands (4 is the getdp cross-check, run separately):")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(Kt_centre_plane=base['Kt'], Kt_depth_resolved=res['Kt'], depth_factor=ratio,
               Kt_motor_model=ref_kt * 1e3,
               convergence_900mm=conv, far_field_real_T=ff_real, far_field_deep_T=ff_deep,
               fundamental_7=f7, fundamental_21=f21,
               midgap_fundamental_T=midgap_fundamental_magpy(),
               bands=[dict(band=n, name=nm, detail=d, pass_=ok) for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(out, open(os.path.join(RESULTS, 'field_3d.json'), 'w'), indent=2)
    print("\n-> results/field_3d.json")
