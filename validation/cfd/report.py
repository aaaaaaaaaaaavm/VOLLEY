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
    path = os.path.join(HERE, case)
    t = forces.latest_time(path) if time is None else time
    pts = forces.read_points(path)
    faces = forces.read_faces(path)
    start, n = forces.patch_range(path, "body")
    owner = forces.read_owner(path)
    pin = forces.read_internal(os.path.join(path, t, "p"))
    p = pin[owner[start:start + n]]
    xc = np.array([pts[f].mean(0)[0] for f in faces[start:start + n]])
    U = meta["U_inf"]
    return xc, p / (0.5 * U * U)          # kinematic p, so Cp = p / (0.5 U^2)


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
    ax[0].text(it.max() - 190, ax[0].get_ylim()[0] * 4, "averaging\nwindow", fontsize=6.5)

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

    xc, cp = surface_cp("free", meta["free"])
    ax[2].plot(xc * 1e3, cp, ".", ms=1.2, color='k', alpha=0.35)
    # binned mean, so the structure is legible through the scatter
    bins = np.linspace(xc.min(), xc.max(), 60)
    idx = np.digitize(xc, bins)
    bm = np.array([cp[idx == i].mean() if (idx == i).any() else np.nan
                   for i in range(1, len(bins))])
    ax[2].plot(0.5 * (bins[1:] + bins[:-1]) * 1e3, bm, color='#c1452b', lw=1.6)
    ax[2].axhline(0, color='0.5', lw=0.7)
    ax[2].axhline(1, color='0.5', lw=0.7, ls=':')
    ax[2].text(xc.min() * 1e3 + 5, 1.05, "$C_p$ = 1, stagnation", fontsize=6.5)
    ax[2].set_xlabel("Position along the body, mm (flow left to right)")
    ax[2].set_ylabel("$C_p$")
    ax[2].set_title("(c) stagnation face, edge separation, base suction", fontsize=8.5)

    path = os.path.join(OUT, "A29_cfd_report.png")
    fig.savefig(path)
    plt.close(fig)
    print("->", os.path.relpath(path, os.path.join(HERE, "..", "..")))


if __name__ == "__main__":
    main()
