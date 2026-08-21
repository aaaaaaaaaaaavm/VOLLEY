"""A29 field figures, parsed from the OpenFOAM case without OpenFOAM.

WHY THIS EXISTS
---------------
A29 ran, converged and was banded, and nobody has ever looked at the flow. The case is
committed -- polyMesh and the t=1800 fields -- and the report figure it produced is a plot of
forces, not of the field.

The obvious route is postProcess or foamToVTK. postProcess ABORTS in this OpenFOAM 1912 build
with an IOstream error on 'sha1', which is the same class of failure A29 already recorded for
wallShearStress. Rather than fight a broken function-object system, this parses the case
directly: every file in it is ASCII, and cell centres are recoverable from points/faces/owner.

WHAT IT DOES NOT DO
-------------------
It shows the pressure field. It does NOT show viscous drag, because A29 does not have it:
wallShearStress aborts, so the viscous term is BOUNDED by a flat-plate correlation and never
solved. Any figure from this file carries that caveat in its caption.

Run:  python3 validation/cfd/fields.py
"""
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, 'free_fine')
TIME = '1800'
CACHE = os.path.join(HERE, 'field_cache.npz')
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'figures')


def _body(path):
    """Return the text between the FoamFile header and EOF."""
    with open(path, encoding='utf-8', errors='replace') as fh:
        txt = fh.read()
    i = txt.find('}', txt.find('FoamFile'))
    return txt[i + 1:]


def read_points(path):
    t = _body(path)
    nums = re.findall(r'\(([^()]*)\)', t)
    return np.array([[float(x) for x in n.split()] for n in nums], dtype=np.float64)


def read_faces(path):
    """faces is 'N(a b c d)' per line after the count."""
    t = _body(path)
    return [np.fromstring(m, dtype=np.int64, sep=' ')
            for m in re.findall(r'\d+\(([\d\s]+)\)', t)]


def read_labels(path):
    t = _body(path)
    m = re.search(r'\(\s*([\d\s]+?)\s*\)', t, re.S)
    return np.fromstring(m.group(1), dtype=np.int64, sep=' ')


def read_internal_scalar(path):
    t = _body(path)
    m = re.search(r'internalField\s+nonuniform[^(]*\(\s*(.*?)\s*\)\s*;', t, re.S)
    if not m:
        u = re.search(r'internalField\s+uniform\s+([-\d.eE+]+)\s*;', t)
        return float(u.group(1)) if u else None
    return np.fromstring(m.group(1), dtype=np.float64, sep=' ')


def read_internal_vector(path):
    t = _body(path)
    m = re.search(r'internalField\s+nonuniform[^(]*\(\s*(.*?)\s*\)\s*;\s*boundaryField', t, re.S)
    vecs = re.findall(r'\(([^()]*)\)', m.group(1))
    return np.array([[float(x) for x in v.split()] for v in vecs], dtype=np.float64)


def face_centres(points, faces):
    return np.array([points[f].mean(axis=0) for f in faces], dtype=np.float64)


def cell_centres(fc, owner, neighbour, ncells):
    """Cell centre approximated as the mean of its face centres.

    Exact enough for a contour plot and it needs no volume integration.
    """
    acc = np.zeros((ncells, 3), dtype=np.float64)
    cnt = np.zeros(ncells, dtype=np.int64)
    np.add.at(acc, owner, fc[:len(owner)])
    np.add.at(cnt, owner, 1)
    np.add.at(acc, neighbour, fc[:len(neighbour)])
    np.add.at(cnt, neighbour, 1)
    cnt[cnt == 0] = 1
    return acc / cnt[:, None]


def main():
    mesh = os.path.join(CASE, 'constant', 'polyMesh')
    print('parsing mesh ...')
    points = read_points(os.path.join(mesh, 'points'))
    faces = read_faces(os.path.join(mesh, 'faces'))
    owner = read_labels(os.path.join(mesh, 'owner'))
    neighbour = read_labels(os.path.join(mesh, 'neighbour'))
    print(f'  {len(points)} points, {len(faces)} faces, {len(owner)} owner, '
          f'{len(neighbour)} neighbour')

    p = read_internal_scalar(os.path.join(CASE, TIME, 'p'))
    U = read_internal_vector(os.path.join(CASE, TIME, 'U'))
    ncells = len(p)
    print(f'  {ncells} cells, |U| range {np.linalg.norm(U, axis=1).min():.2f} '
          f'to {np.linalg.norm(U, axis=1).max():.2f}')

    fc = face_centres(points, faces)
    cc = cell_centres(fc, owner, neighbour, ncells)
    np.savez_compressed(os.path.join(HERE, 'field_cache.npz'),
                        cc=cc, p=p, U=U)
    print(f'wrote {os.path.join(HERE, "field_cache.npz")}')


def wake_figure():
    """Mid-plane slice of p and |U|, from the cache main() writes."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.tri import Triangulation
    d = np.load(CACHE)
    cc, p, U = d['cc'], d['p'], d['U']
    sp = np.linalg.norm(U, axis=1)
    plt.rcParams.update({'font.size': 8, 'figure.dpi': 200, 'savefig.bbox': 'tight'})

    XL, XR, YB, YT = -0.6, 2.2, -0.6, 0.6
    band = np.abs(cc[:, 2]) < 0.02
    crop = band & (cc[:, 0] > XL) & (cc[:, 0] < XR) & (cc[:, 1] > YB) & (cc[:, 1] < YT)
    x, y, pv, sv = cc[crop, 0], cc[crop, 1], p[crop], sp[crop]
    print('slice cells', crop.sum())

    tri = Triangulation(x, y)
    # The solid body leaves a HOLE with no cell centres in it. Detect the hole on a fine grid
    # rather than by edge length: the mesh is graded, so a length threshold that clears the body
    # also deletes the whole far field, which is what the first attempt did.
    NB = 110
    hx = np.linspace(XL, XR, NB + 1)
    hy = np.linspace(YB, YT, NB + 1)
    H, _, _ = np.histogram2d(x, y, bins=[hx, hy])
    cx = x[tri.triangles].mean(axis=1)
    cy = y[tri.triangles].mean(axis=1)
    ix = np.clip(np.searchsorted(hx, cx) - 1, 0, NB - 1)
    iy = np.clip(np.searchsorted(hy, cy) - 1, 0, NB - 1)
    near = (cx > -0.02) & (cx < 0.70) & (np.abs(cy) < 0.12)
    tri.set_mask(near & (H[ix, iy] == 0))

    fig, ax = plt.subplots(2, 1, figsize=(7.2, 5.4), sharex=True)
    c0 = ax[0].tricontourf(tri, pv, levels=np.linspace(-140, 140, 57), cmap='RdBu_r', extend='both')
    ax[0].set_ylabel('y  [m]')
    ax[0].set_title('Kinematic pressure  $p/\\rho$  [m$^2$/s$^2$]', loc='left')
    fig.colorbar(c0, ax=ax[0], pad=0.01, fraction=0.028)

    c1 = ax[1].tricontourf(tri, sv, levels=np.linspace(0, 22, 45), cmap='viridis', extend='max')
    ax[1].set_xlabel('x  [m]   (flow left to right)')
    ax[1].set_ylabel('y  [m]')
    ax[1].set_title('Speed  $|U|$  [m/s]', loc='left')
    fig.colorbar(c1, ax=ax[1], pad=0.01, fraction=0.028)

    for a in ax:
        a.set_aspect('equal')
        a.set_xlim(XL, XR)
        a.set_ylim(-0.4, 0.4)

    fig.suptitle('A29  Gen5 sled and 3U payload, mid-plane ($z=0$), fine mesh, $t=1800$',
                 fontsize=9, y=0.97)
    out = os.path.join(OUT, 'A29_wake.png')
    fig.savefig(out)
    print('wrote', out)


if __name__ == '__main__':
    if not os.path.exists(CACHE):
        main()
    wake_figure()
