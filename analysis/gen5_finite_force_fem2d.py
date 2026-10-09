"""Independent 2-D magnetostatic finite-array force screen for Gen5.

The field is solved from the vector-potential PDE on a triangular mesh with
scikit-fem. The finite stator Lorentz integration uses the P118 belt geometry.
This is a method check of the *in-plane* field and finite-stator force shape,
not a 3-D force validation: the 90 mm magnet-depth end effect is absent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from importlib.metadata import version

from skfem import Basis, BilinearForm, ElementTriP1, LinearForm, MeshTri, asm, condense, solve
from skfem.helpers import dot, grad

import motor_model as mm
import field_3d

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/results/gen5_finite_force_fem2d.json"
FIG = ROOT / "figures/gen5_finite_force_fem2d.png"
FIELD_FIG = ROOT / "figures/gen5_fem2d_field.png"
REPORT = ROOT / "validation/P119_gen5_finite_force_fem2d.md"
MU0 = 4e-7 * math.pi
NU0 = 1 / MU0
N_BLOCKS = 7 * mm.NBLK
X_BOX = 0.42
Y_BOX = 0.08


@BilinearForm
def stiffness(u, v, w):
    return NU0 * dot(grad(u), grad(v))


@LinearForm
def magnet_source(v, w):
    return NU0 * (w.brx * grad(v)[1] - w.bry * grad(v)[0])


def field_solution(dx: float, x_box: float = X_BOX, y_box: float = Y_BOX):
    """Solve B=curl(Az) for both 7-wave arrays in a bounded air domain."""
    nx = round(2 * x_box / dx)
    ny = round(2 * y_box / dx)
    mesh = MeshTri.init_tensor(np.linspace(-x_box, x_box, nx + 1),
                               np.linspace(-y_box, y_box, ny + 1))
    center = mesh.p[:, mesh.t].mean(axis=1)
    x, y = center
    index = np.floor((x + N_BLOCKS * mm.W / 2) / mm.W).astype(int)
    in_x = (index >= 0) & (index < N_BLOCKS)
    upper = (y > mm.GAP / 2) & (y < mm.GAP / 2 + mm.TH)
    lower = (y < -mm.GAP / 2) & (y > -mm.GAP / 2 - mm.TH)
    brx = np.zeros(mesh.nelements)
    bry = np.zeros(mesh.nelements)
    for selected, step in ((in_x & upper, -1), (in_x & lower, +1)):
        angle = np.deg2rad((90 + step * index[selected] * 90) % 360)
        brx[selected] = mm.BR * np.cos(angle)
        bry[selected] = mm.BR * np.sin(angle)
    basis = Basis(mesh, ElementTriP1())
    n_q = basis.X.shape[1]
    matrix = asm(stiffness, basis)
    source = asm(magnet_source, basis,
                 brx=np.repeat(brx[:, None], n_q, axis=1),
                 bry=np.repeat(bry[:, None], n_q, axis=1))
    az = solve(*condense(matrix, source, D=basis.get_dofs()))
    return mesh, az


def sample_by(mesh, az, x, y, x_window=X_BOX, y_window=Y_BOX):
    """Piecewise-constant P1 By; use zero outside the sampling window."""
    x, y = np.broadcast_arrays(np.asarray(x), np.asarray(y))
    output = np.zeros(x.size)
    xx, yy = x.ravel(), y.ravel()
    inside = (np.abs(xx) < x_window - 1e-9) & (np.abs(yy) < y_window - 1e-9)
    if not inside.any():
        return output.reshape(x.shape)
    if inside.sum() > 500:
        indices = np.flatnonzero(inside)
        for chunk in np.array_split(indices, math.ceil(len(indices) / 500)):
            output[chunk] = sample_by(mesh, az, xx[chunk], yy[chunk], x_window, y_window)
        return output.reshape(x.shape)
    element = mesh.element_finder()(xx[inside], yy[inside])
    tri = mesh.t[:, element]
    x1, y1 = mesh.p[0, tri[0]], mesh.p[1, tri[0]]
    x2, y2 = mesh.p[0, tri[1]], mesh.p[1, tri[1]]
    x3, y3 = mesh.p[0, tri[2]], mesh.p[1, tri[2]]
    det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    output[inside] = -((y3 - y1) * (az[tri[1]] - az[tri[0]])
                       - (y2 - y1) * (az[tri[2]] - az[tri[0]])) / det
    return output.reshape(x.shape)


def force_map(mesh, az, positions, x_window=X_BOX, y_window=Y_BOX):
    """Ideal phase at each position, same winding convention as P118."""
    stator = json.loads((ROOT / "cad/parameters.json").read_text())["groups"]["stator"]
    belts = (np.arange(stator["conductor_count"]) * stator["belt_pitch"]
             + stator["belt_width"] / 2) / 1000
    gx, wx = np.polynomial.legendre.leggauss(3)
    gy, wy = np.polynomial.legendre.leggauss(3)
    by_weight = wx[None, :, None] * wy[None, None, :]
    offsets = 0.007 * gx / 2
    yy = mm.WIND_THICK * gy / 2
    seq = ((0, 1), (2, -1), (1, 1), (0, -1), (2, 1), (1, -1))
    phases = (0.0, -2 * np.pi / 3, 2 * np.pi / 3)
    harmonic = np.array([sign * np.exp(1j * phases[phase])
                         for i in range(len(belts))
                         for phase, sign in (seq[i % 6],)])
    forces = []
    for s in positions:
        local_x = belts[:, None, None] + offsets[None, :, None] - (0.400 + s)
        local_y = np.broadcast_to(yy[None, None, :], (len(belts), 3, 3))
        by = sample_by(mesh, az, np.broadcast_to(local_x, local_y.shape), local_y,
                       x_window, y_window)
        belt_integral = (by * by_weight).sum(axis=(1, 2)) * 0.007 * mm.WIND_THICK * mm.DEPTH / 4
        forces.append(float(0.9 * mm.K_RATED / mm.WIND_THICK
                            * abs(np.dot(belt_integral, harmonic))))
    return np.asarray(forces)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    # The fine grid is aligned to the 12 mm magnet width, 8 mm thickness and 12 mm gap.
    # The coarse grid gives an explicit discretization sensitivity, not a pass band.
    positions = np.linspace(0, mm.ACCEL_ZONE, 53)
    runs = []
    for dx in (0.003, 0.002, 0.001):
        mesh, az = field_solution(dx)
        forces = force_map(mesh, az, positions)
        work = float(np.trapezoid(forces, positions))
        runs.append(dict(dx_m=dx, nodes=int(mesh.nvertices), triangles=int(mesh.nelements),
                         force_N=forces.tolist(), work_J=work,
                         ideal_speed_m_s=math.sqrt(2 * work / (mm.M_SAT + mm.M_SLED)),
                         midgap_by_T=float(sample_by(mesh, az, np.array([mm.LAM / 8]),
                                                         np.array([0.0]))[0])))
    # A second air box moves the artificial A_z=0 boundary outward while
    # keeping the same 0.42 m force-sampling window and 2 mm resolution.
    outer_mesh, outer_az = field_solution(0.002, 0.55, 0.12)
    outer_forces = force_map(outer_mesh, outer_az, positions)
    outer_work = float(np.trapezoid(outer_forces, positions))
    outer_wide_forces = force_map(outer_mesh, outer_az, positions, 0.55, 0.12)
    outer_wide_work = float(np.trapezoid(outer_wide_forces, positions))
    reference = json.loads((ROOT / "analysis/results/gen5_finite_force_map.json").read_text())
    analytic_midgap = float(field_3d.halbach_pair(mm.DEPTH).getB([mm.LAM / 8, 0, 0])[1])
    result = dict(status="INDEPENDENT_2D_FEM_SCREEN_NOT_3D_OR_HARDWARE_VALIDATION",
                  method="scikit-fem P1 Az magnetostatic PDE; finite 7-wave arrays and 162-belt Lorentz integral; ideal phase",
                  software_versions=dict(python=platform.python_version(), numpy=np.__version__,
                                         scipy=scipy.__version__, scikit_fem=version("scikit-fem")),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  parameters_sha256=hashlib.sha256((ROOT / "cad/parameters.json").read_bytes()).hexdigest(),
                  boundary=dict(x_half_width_m=X_BOX, y_half_width_m=Y_BOX,
                                Az_outer_boundary_zero=True,
                                field_outside_sampling_window_set_zero=True,
                                larger_box_x_half_width_m=0.55,
                                larger_box_y_half_width_m=0.12,
                                larger_box_work_J=outer_work,
                                box_work_change_fraction=(outer_work-runs[1]["work_J"])/outer_work,
                                larger_sampling_window_work_J=outer_wide_work,
                                truncation_work_fraction=(outer_wide_work-outer_work)/outer_wide_work),
                  omitted=["90 mm depth end effect", "circuit and switching limits",
                           "friction and structural/contact dynamics", "nonlinear magnet material"],
                  positions_m=positions.tolist(), runs=runs,
                  mesh_work_change_fraction=(runs[-1]["work_J"] - runs[-2]["work_J"]) / runs[-1]["work_J"],
                  analytic_3d_work_J=reference["ideal_finite_stator_work_J"],
                  analytic_midgap_by_T=analytic_midgap,
                  fine_mesh_midgap_relative_error=abs(runs[-1]["midgap_by_T"]-analytic_midgap)/abs(analytic_midgap))
    rendered = json.dumps(result, indent=2) + "\n"
    report = "\n".join([
        "# P119 — independent 2-D finite-array force screen", "",
        "**Evidence class: exploratory 2-D finite-element model; not a 3-D force or hardware validation.**", "",
        "The finite 7-wavelength, double-sided Halbach array is solved as a triangular-mesh",
        "magnetostatic vector-potential problem using scikit-fem P1 elements. Magnet remanence,",
        "gap and dimensions match `cad/parameters.json` and `analysis/motor_model.py`. The",
        "resulting field is integrated through the 162 drawn stator belts with the P118 phase",
        "convention, selecting ideal phase independently at each 25 mm position. The PDE solver",
        "does not use magpylib's cuboid field law; the geometry and material assumptions are shared.", "",
        f"The 1 mm mesh has {runs[-1]['nodes']:,} nodes and {runs[-1]['triangles']:,} triangles.",
        f"Its ideal work is **{runs[-1]['work_J']:.1f} J**, or **{runs[-1]['ideal_speed_m_s']:.3f} m/s**",
        "when converted with the same 13.445 kg moving-mass assumption. This is a 2-D result",
        "with no magnet-depth end effect, circuit loss, friction or contact dynamics.",
        f"P118's 3-D analytic screen gives {reference['ideal_finite_stator_work_J']:.1f} J; the",
        "methods agree on the substantial end-of-stator force decline, but the absolute works",
        "are not identical models and must not be averaged into a selected speed rating.", "",
        "| Mesh size | Nodes | Ideal work | Speed conversion |", "|:--|--:|--:|--:|",
        *[f"| {r['dx_m']*1000:.0f} mm | {r['nodes']:,} | {r['work_J']:.1f} J | {r['ideal_speed_m_s']:.3f} m/s |" for r in runs],
        "",
        f"The 2-to-1 mm work change is {100*abs(result['mesh_work_change_fraction']):.2f}%. ",
        f"At 2 mm, enlarging the air box from ±0.42×0.08 m to ±0.55×0.12 m changes work by",
        f"{100*abs(result['boundary']['box_work_change_fraction']):.4f}%; expanding the force",
        f"sampling window changes it by {100*abs(result['boundary']['truncation_work_fraction']):.4f}%.",
        f"At x=6 mm, midgap B_y is {runs[-1]['midgap_by_T']:.6f} T versus",
        f"{analytic_midgap:.6f} T from magpylib (difference {100*result['fine_mesh_midgap_relative_error']:.2f}%).",
        "These are numerical diagnostics set out with this exploratory run, not pre-registered",
        "acceptance bands or measured magnetic-field accuracy.", "",
        "![Independent 2-D finite-force plot](../figures/gen5_finite_force_fem2d.png)", "",
        "![Solved 2-D field near the magnet arrays](../figures/gen5_fem2d_field.png)", "",
        "The complete 3-D integrated force, a coupled winding/inverter trajectory, feed and",
        "release contact, and actual payload/host limits remain open. The field plot is a",
        "software-generated solver visualization, not an interactive GUI screenshot.", "",
        "Reproduce with `python analysis/gen5_finite_force_fem2d.py` after installing",
        "`requirements-dev.txt`. Result, software, source and parameter hashes are in",
        "`analysis/results/gen5_finite_force_fem2d.json`.", "",
    ])
    if args.check:
        fresh = OUT.exists() and OUT.read_text() == rendered and REPORT.exists() and REPORT.read_text() == report
        print("P119 current" if fresh else "P119 STALE")
        return 0 if fresh else 1
    OUT.write_text(rendered)
    REPORT.write_text(report)
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=150)
    for run, label in zip(runs, ("2-D FEM, 3 mm", "2-D FEM, 2 mm", "2-D FEM, 1 mm")):
        ax.plot(positions, run["force_N"], label=label)
    ax.plot(reference["positions_m"], reference["forces_N"], label="3-D analytic, 90 mm depth", ls="--")
    ax.set(xlabel="Sled displacement from reference pose (m)",
           ylabel="Ideal forward force (N)",
           title="Finite-array force: independent 2-D FEM versus 3-D analytic screen")
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG)
    plt.close(fig)
    xs = np.linspace(-0.19, 0.19, 321)
    ys = np.linspace(-0.026, 0.026, 141)
    xx, yy = np.meshgrid(xs, ys)
    by = sample_by(mesh, az, xx, yy)
    fig, ax = plt.subplots(figsize=(9, 3.3), dpi=150)
    img = ax.pcolormesh(xx * 1000, yy * 1000, by, shading="auto",
                        cmap="RdBu_r", vmin=-0.75, vmax=0.75)
    fig.colorbar(img, ax=ax, label="Solved B_y (T)")
    ax.set(xlabel="Local array x (mm)", ylabel="Air-gap y (mm)",
           title="Gen5 finite Halbach array: 2-D FEM field section")
    ax.axhline(6, color="black", lw=0.6, alpha=0.6)
    ax.axhline(-6, color="black", lw=0.6, alpha=0.6)
    fig.tight_layout()
    fig.savefig(FIELD_FIG)
    plt.close(fig)
    print(f"2-D FEM work {runs[-1]['work_J']:.1f} J; mesh change "
          f"{result['mesh_work_change_fraction']*100:.2f}%; analytic 3-D {result['analytic_3d_work_J']:.1f} J")


if __name__ == "__main__":
    main()
