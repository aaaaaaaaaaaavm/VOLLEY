"""A2 band 4: getdp 3-D FEM against magpylib, on the quantity the band names.

BAND (declared 2026-08-10 at 964af2c, before any of this existed):
  peak |B_y| at midgap (y = 0), on the plane z = 0, over one 48 mm wavelength, taken as the
  DOUBLE-SIDED FUNDAMENTAL AMPLITUDE -- not the single-sided reference, and not the raw peak.
  Agreement within 5 %.

Both alternatives are named because A1's row failed for exactly this ambiguity and P20 exists
to stop it recurring.

The two methods are compared on IDENTICAL geometry -- three wavelengths, both arrays, sampled
on the centre wavelength -- so the comparison is between a meshed PDE solve and analytic
superposition, and not between two different machines.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "analysis"))
import motor_model as mm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
N_WAVE = json.load(open(os.path.join(HERE, "magnetisation.json")))["n_wave"]
LAM = mm.LAM


def fundamental(xs, By):
    """Amplitude of the LAM-periodic fundamental by projection onto one period."""
    n = len(xs)
    return float(2.0 / n * abs(np.sum(By * np.exp(-2j * np.pi * xs / LAM))))


def magpy_reference(n_wave=N_WAVE, nx=240):
    import magpylib as magpy
    W, TH, GAP, BR, DEPTH, NBLK = mm.W, mm.TH, mm.GAP, mm.BR, mm.DEPTH, mm.NBLK

    def arr(y_face, step):
        out = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * W
            ang = np.radians((90 + step * i * 90) % 360)
            pol = [BR * np.cos(ang), BR * np.sin(ang), 0]
            y_c = y_face + (TH / 2 if y_face > 0 else -TH / 2)
            out.append(magpy.magnet.Cuboid(polarization=pol, dimension=(W, TH, DEPTH),
                                           position=(x, y_c, 0)))
        return magpy.Collection(out)

    field = magpy.Collection([arr(+GAP / 2, -1), arr(-GAP / 2, +1)])
    xs = np.linspace(-LAM / 2, LAM / 2, nx, endpoint=False)
    By = field.getB(np.stack([xs, np.zeros(nx), np.zeros(nx)], 1))[:, 1]
    return xs, By


def fem_result(path):
    """getdp SimpleTable: x y z bx by bz (one row per sample point)."""
    d = np.loadtxt(path)
    if d.ndim == 1:
        d = d[None, :]
    xs, By = d[:, 0], d[:, 4]
    order = np.argsort(xs)
    xs, By = xs[order], By[order]
    # getdp's OnLine includes both endpoints. x = -LAM/2 and x = +LAM/2 are the same
    # point of a LAM-periodic field, so keeping both weights one phase twice in the
    # projection. Drop the duplicate; the sample set is then a full period exactly once,
    # matching the reference's endpoint=False grid.
    if len(xs) > 1 and abs((xs[-1] - xs[0]) - LAM) < 1e-9:
        xs, By = xs[:-1], By[:-1]
    return xs, By


if __name__ == "__main__":
    xf, Byf = fem_result(os.path.join(HERE, "b_midgap.txt"))
    xm, Bym = magpy_reference()
    f_fem, f_mag = fundamental(xf, Byf), fundamental(xm, Bym)
    err = 100 * (f_fem - f_mag) / f_mag
    peak_fem, peak_mag = float(np.abs(Byf).max()), float(np.abs(Bym).max())

    print(f"geometry: {N_WAVE} wavelengths, both arrays, sampled on the centre wavelength")
    print(f"  getdp samples {len(xf)}, magpylib samples {len(xm)}\n")
    print(f"{'quantity':44s} {'getdp':>12s} {'magpylib':>12s} {'error':>9s}")
    print(f"{'DOUBLE-SIDED FUNDAMENTAL of By at midgap':44s} {f_fem:12.5f} {f_mag:12.5f} "
          f"{err:8.3f} %")
    print(f"{'(raw peak |By|, the OTHER reference, for scale)':44s} {peak_fem:12.5f} "
          f"{peak_mag:12.5f} {100*(peak_fem-peak_mag)/peak_mag:8.3f} %")
    ok = abs(err) <= 5.0
    print(f"\nband 4: {'PASS' if ok else 'FAIL'}  (|error| <= 5 % on the fundamental)")
    json.dump(dict(n_wave=N_WAVE, fundamental_getdp_T=f_fem, fundamental_magpylib_T=f_mag,
                   error_pct=err, raw_peak_getdp_T=peak_fem, raw_peak_magpylib_T=peak_mag,
                   band4_pass=bool(ok)),
              open(os.path.join(HERE, "band4_result.json"), "w"), indent=2)
    print("-> band4_result.json")
