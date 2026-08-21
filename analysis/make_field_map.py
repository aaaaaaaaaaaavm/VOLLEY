"""A2/A3 field map: the airgap field that every Gen5 number descends from.

WHY THIS EXISTS
---------------
A2 resolved the Halbach field across the array's 90 mm depth instead of sampling the centre
plane and multiplying by it. That cost Kt 4.42 % -- 11.03 to 10.54 N per kA/m -- and moved
every dependent number. The correction is described in prose in four documents and has never
been drawn.

Geometry comes from field_3d.halbach_pair(), the SAME builder the thrust integral uses, so
this cannot drift from the number it illustrates.

Run:  python3 analysis/make_field_map.py
"""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import field_3d
import motor_model as mm

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')


def main():
    LAM, GAP, DEPTH = mm.LAM, mm.GAP, mm.DEPTH
    field = field_3d.halbach_pair(DEPTH)
    plt.rcParams.update({'font.size': 8, 'figure.dpi': 200, 'savefig.bbox': 'tight'})
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.2),
                           gridspec_kw={'wspace': 0.42})

    # LEFT: By in the x-y plane at mid-depth -- the field the winding sits in.
    nx, ny = 300, 160
    xs = np.linspace(-LAM, LAM, nx)
    ys = np.linspace(-GAP / 2 * 1.05, GAP / 2 * 1.05, ny)
    X, Y = np.meshgrid(xs, ys)
    pts = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1)
    By = field.getB(pts)[:, 1].reshape(X.shape)
    m = np.abs(By).max()
    c = ax[0].contourf(X * 1e3, Y * 1e3, By, levels=np.linspace(-m, m, 41), cmap='RdBu_r')
    ax[0].axhline(+mm.WIND_THICK / 2 * 1e3, color='k', lw=0.7, ls='--')
    ax[0].axhline(-mm.WIND_THICK / 2 * 1e3, color='k', lw=0.7, ls='--')
    ax[0].set_xlabel('x along the track  [mm]')
    ax[0].set_ylabel('y across the gap  [mm]')
    ax[0].set_title(f'$B_y$ at mid-depth, gap {GAP*1e3:.0f} mm\n'
                    f'dashed: the {mm.WIND_THICK*1e3:.0f} mm winding', loc='left', fontsize=8)
    cb = fig.colorbar(c, ax=ax[0], pad=0.03, fraction=0.046)
    cb.set_label('$B_y$  [T]', fontsize=8)
    cb.ax.tick_params(labelsize=7)

    # RIGHT: the depth profile -- the whole point of A2.
    zs = np.linspace(-DEPTH / 2, DEPTH / 2, 121)
    p2 = np.stack([np.zeros(zs.size), np.zeros(zs.size), zs], 1)
    prof = np.abs(field.getB(p2)[:, 1])
    centre = prof[len(prof) // 2]
    ax[1].plot(zs * 1e3, prof, lw=1.6, color='#b4451f')
    ax[1].axhline(centre, color='k', lw=0.8, ls='--')
    ax[1].axhline(prof.mean(), color='#2a6f97', lw=1.2, ls='-')
    ax[1].set_xlabel('z through the array depth  [mm]')
    ax[1].set_ylabel('$|B_y|$ on the centre line  [T]')
    ax[1].set_title(f'Depth profile over {DEPTH*1e3:.0f} mm\n'
                    f'dashed: centre-plane value; solid: depth mean',
                    loc='left', fontsize=8)
    ax[1].text(0.03, 0.08, f'mean / centre = {prof.mean()/centre:.4f}',
               transform=ax[1].transAxes, fontsize=8)
    ax[1].grid(alpha=0.25)

    fig.suptitle('A2/A3  the airgap field, resolved through the array depth rather than '
                 'sampled at the centre plane', fontsize=9, y=1.02)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'A02_field_map.png')
    fig.savefig(path)
    print(f'centre {centre:.4f} T, depth mean {prof.mean():.4f} T, '
          f'ratio {prof.mean()/centre:.4f}')
    print('wrote', path)


if __name__ == '__main__':
    main()
