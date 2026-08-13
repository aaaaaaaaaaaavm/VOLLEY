"""A29 CFD report figures: convergence, force history, and the surface pressure field.

These are the diagnostics a reader needs in order to decide whether to believe the drag
coefficient, and they live in the run sheet rather than in the paper because that is where
someone checking the work will look. Three panels:

  (a) residual history -- and it does NOT converge, which is the expected behaviour of a
      steady solver on a massively separated wake and is reported rather than hidden;
  (b) drag over the averaging window, with the mean and the spread that goes with it;
  (c) surface pressure coefficient against position, which is where the drag physically
      comes from: a stagnation face, an edge separation, and a base suction.

Usage:  python3 report.py
Out:    figures/A29_cfd_report.png
"""
import json
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

import forces                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 9, 'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 200, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})

FIELDS = ("Ux", "Uy", "Uz", "p", "k", "omega")


def residuals(case):
    out = {f: [] for f in FIELDS}
    it = []
    for name in ("log.simpleFoam", "log.simpleFoam2"):
        path = os.path.join(HERE, case, name)
        if not os.path.exists(path):
            continue
        cur = None
        for line in open(path, errors="ignore"):
            m = re.match(r"^Time = (\d+)", line)
            if m:
                cur = int(m.group(1))
                it.append(cur)
                for f in FIELDS:
                    out[f].append(np.nan)
                continue
            m = re.search(r"Solving for (\w+), Initial residual = ([\d.eE+-]+)", line)
            if m and m.group(1) in out and it:
                out[m.group(1)][-1] = float(m.group(2))
    return np.array(it), {f: np.array(v) for f, v in out.items()}


def surface_cp(case, meta, time=None):
    """Cp on the body, with each face's x-normal, so forward and rearward faces separate.

    Plotting Cp against x alone mixes the stagnation face with the side walls beside it and
    hides the only two places drag actually comes from: the front, pushed on, and the base,
    sucked back.
    """
    path = os.path.join(HERE, case)
    t = forces.latest_time(path) if time is None else time
    pts = forces.read_points(path)
    faces = forces.read_faces(path)
    start, n = forces.patch_range(path, "body")
    owner = forces.read_owner(path)
    pin = forces.read_internal(os.path.join(path, t, "p"))
    p = pin[owner[start:start + n]]
    Sf = forces.area_vectors(pts, faces[start:start + n])
    nx = Sf[:, 0] / np.linalg.norm(Sf, axis=1)
    xc = np.array([pts[f].mean(0)[0] for f in faces[start:start + n]])
    U = meta["U_inf"]
    return xc, p / (0.5 * U * U), nx


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = json.load(open(os.path.join(HERE, "case_meta.json")))
    res = json.load(open(os.path.join(HERE, "..", "..", "analysis", "results",
                                      "cfd_air_drag.json")))

    fig, ax = plt.subplots(1, 3, figsize=(11.0, 3.1),
                           gridspec_kw=dict(wspace=0.30))

    it, r = residuals("free")
    for f, sty in zip(FIELDS, ('-', '-', '-', '--', ':', ':')):
        ax[0].semilogy(it, r[f], sty, lw=1.0, label=f)
    ax[0].set_xlabel("SIMPLE iteration")
    ax[0].set_ylabel("Initial residual")
    ax[0].legend(fontsize=6, ncol=2, frameon=False, loc='upper right')
    ax[0].set_title("(a) it does not converge, and that is the answer", fontsize=8.5)
    ax[0].axvspan(it.max() - 200, it.max(), color='0.88', zorder=0)
    ax[0].text(it.max() - 700, ax[0].get_ylim()[0] * 3, "averaging window",
               fontsize=6.5)

    h = res["history"]["free"]
    t = [x["time"] for x in h]
    d = [x["drag_N"] for x in h]
    ax[1].plot(t, d, "o-", color='k', ms=4, lw=1.2)
    m = float(np.mean(d))
    ax[1].axhline(m, color='0.45', lw=1.0, ls='--')
    ax[1].fill_between([min(t), max(t)], min(d), max(d), color='0.88', zorder=0)
    ax[1].set_xlabel("SIMPLE iteration")
    ax[1].set_ylabel("Drag, N")
    ax[1].set_title(f"(b) mean {m:.3f} N, spread $\\pm${0.5*(max(d)-min(d)):.3f} N",
                    fontsize=8.5)

    xc, cp, nx = surface_cp("free", meta["free"])
    fwd, rev = nx > 0.5, nx < -0.5
    ax[2].plot(xc[abs(nx) <= 0.5] * 1e3, cp[abs(nx) <= 0.5], ".", ms=1.0,
               color='0.7', label="side")
    ax[2].plot(xc[rev] * 1e3, cp[rev], ".", ms=2.0, color='#2b62c1', label="rearward")
    ax[2].plot(xc[fwd] * 1e3, cp[fwd], ".", ms=2.0, color='#c1452b', label="forward")
    ax[2].axhline(0, color='0.5', lw=0.7)
    ax[2].axhline(1, color='0.5', lw=0.7, ls=':')
    ax[2].text(xc.max() * 1e3, 1.03, f"$C_p$ = 1; peak on the body {cp.max():.3f}",
               fontsize=6.5, ha='right')
    ax[2].set_xlabel("Position along the body, mm (flow left to right)")
    ax[2].set_ylabel("$C_p$")
    ax[2].set_ylim(-0.75, 1.15)
    ax[2].legend(fontsize=6.5, frameon=False, loc='lower right', markerscale=3)
    ax[2].set_title("(c) forward faces push, the base sucks, sides do nothing",
                    fontsize=8.5)

    path = os.path.join(OUT, "A29_cfd_report.png")
    fig.savefig(path)
    plt.close(fig)
    print("->", os.path.relpath(path, os.path.join(HERE, "..", "..")))


if __name__ == "__main__":
    main()
