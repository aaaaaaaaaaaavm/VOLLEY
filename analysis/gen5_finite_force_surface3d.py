"""Independent depth-resolved Gen5 3-D surface-charge force cross-check.

Uniformly magnetized, ironless cuboids can be represented by magnetic surface
charge sigma_m = M dot n. This evaluates B_y in air from those charged faces,
integrating the finite 90 mm depth analytically and the short face dimension
by Gauss-Legendre quadrature. It does not call magpylib for the calculated
field. The 162-belt Lorentz integral uses the same stated ideal-phase and
geometry assumptions as P118, independently implemented here.

The method is a linear-material 3-D field cross-check, NOT finite-element
analysis, a selected winding/inverter, or hardware validation.
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

import field_3d
import motor_model as mm

ROOT = Path(__file__).resolve().parents[1]
PARAM = ROOT / "cad/parameters.json"
REFERENCE = ROOT / "analysis/results/gen5_finite_force_map.json"
OUT = ROOT / "analysis/results/gen5_finite_force_surface3d.json"
REPORT = ROOT / "validation/P121_gen5_finite_force_surface3d.md"
FIG = ROOT / "figures/gen5_finite_force_surface3d.png"


def charged_lines(order: int, gap_m: float | None = None) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Face charge nodes after exact integration across magnet depth.

    In air B = mu0 H and sigma_m = (B_r/mu0) dot n, so mu0 cancels. The
    coefficient below is the remanent polarization component divided by 4pi.
    The source representation differs from the analytic cuboid field law.
    """
    nodes, weights = np.polynomial.legendre.leggauss(order)
    gap = mm.GAP if gap_m is None else gap_m
    if gap <= mm.WIND_THICK:
        raise ValueError("magnet gap must exceed the winding thickness")
    n_blocks = 7 * mm.NBLK
    faces = []
    for gap_face, rotation_step in ((gap / 2, -1), (-gap / 2, 1)):
        y_center = gap_face + (mm.TH / 2 if gap_face > 0 else -mm.TH / 2)
        for i in range(n_blocks):
            x_center = (i - n_blocks / 2 + 0.5) * mm.W
            angle = math.radians((90 + rotation_step * i * 90) % 360)
            components = (("x", mm.BR * math.cos(angle)),
                          ("y", mm.BR * math.sin(angle)))
            for axis, polarization in components:
                if abs(polarization) < 1e-12:
                    continue
                for sign in (-1, 1):
                    if axis == "x":
                        source_x = np.full(order, x_center + sign * mm.W / 2)
                        source_y = y_center + mm.TH * nodes / 2
                        width = mm.TH
                    else:
                        source_x = x_center + mm.W * nodes / 2
                        source_y = np.full(order, y_center + sign * mm.TH / 2)
                        width = mm.W
                    coefficient = sign * polarization * width * weights / (8 * math.pi)
                    faces.append((source_x, source_y, coefficient))
    return faces


def field_by(points: np.ndarray, faces: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    """Compute 3-D B_y at air points; integrate source depth in closed form.

    For rho^2=(x-xs)^2+(y-ys)^2, the depth integral of 1/R^3 is
    [t/(rho^2 sqrt(rho^2+t^2))] between t=-D/2-z and t=D/2-z.
    """
    result = np.zeros(len(points))
    for start in range(0, len(points), 2500):
        sample = points[start:start + 2500]
        by = np.zeros(len(sample))
        z = sample[:, 2, None]
        high = mm.DEPTH / 2 - z
        low = -mm.DEPTH / 2 - z
        for source_x, source_y, coefficient in faces:
            dx = sample[:, 0, None] - source_x[None, :]
            dy = sample[:, 1, None] - source_y[None, :]
            rho2 = dx * dx + dy * dy
            if np.any(rho2 < 1e-20):
                raise ValueError("surface-charge field sampled on a source line")
            depth_integral = (high / np.sqrt(rho2 + high * high)
                              - low / np.sqrt(rho2 + low * low)) / rho2
            by += np.sum(coefficient[None, :] * dy * depth_integral, axis=1)
        result[start:start + len(sample)] = by
    return result


def belt_geometry() -> np.ndarray:
    stator = json.loads(PARAM.read_text())["groups"]["stator"]
    if (stator["conductor_count"], stator["belt_pitch"], stator["belt_width"]) != (162, 8.0, 7.0):
        raise ValueError("controlled 162-belt Gen5 geometry changed")
    return (np.arange(162) * stator["belt_pitch"] + stator["belt_width"] / 2) / 1000


def force_at(displacement: float, faces, belts: np.ndarray,
             volume_order: tuple[int, int, int] = (3, 3, 5),
             depth_offset_m: float = 0.0) -> float:
    """Integrate J_z B_y in the drawn belt volumes at ideal independent phase."""
    nx, ny, nz = volume_order
    gx, wx = np.polynomial.legendre.leggauss(nx)
    gy, wy = np.polynomial.legendre.leggauss(ny)
    gz, wz = np.polynomial.legendre.leggauss(nz)
    x = belts[:, None, None, None] + 0.007 * gx[None, :, None, None] / 2 - (0.400 + displacement)
    y = mm.WIND_THICK * gy[None, None, :, None] / 2
    z = mm.DEPTH * gz[None, None, None, :] / 2 + depth_offset_m
    points = np.empty((len(belts), nx, ny, nz, 3))
    points[..., 0] = x
    points[..., 1] = y
    points[..., 2] = z
    by = field_by(points.reshape(-1, 3), faces).reshape(len(belts), nx, ny, nz)
    belt_integral = (np.einsum("ijkl,j,k,l->i", by, wx, wy, wz)
                     * 0.007 * mm.WIND_THICK * mm.DEPTH / 8)
    sequence = ((0, 1), (2, -1), (1, 1), (0, -1), (2, 1), (1, -1))
    phases = (0.0, -2 * math.pi / 3, 2 * math.pi / 3)
    real = imag = 0.0
    for i, integral in enumerate(belt_integral):
        phase, sign = sequence[i % 6]
        real += sign * integral * math.cos(phases[phase])
        imag += sign * integral * math.sin(phases[phase])
    return float(0.9 * mm.K_RATED / mm.WIND_THICK * math.hypot(real, imag))


def calculate() -> dict:
    belts = belt_geometry()
    positions = np.linspace(0, mm.ACCEL_ZONE, 53)
    runs = []
    for order in (10, 16, 24):
        faces = charged_lines(order)
        forces = [force_at(float(s), faces, belts) for s in positions]
        work = float(np.trapezoid(forces, positions))
        runs.append(dict(face_quadrature_order=order, positions_m=positions.tolist(),
                         forces_N=forces, ideal_work_J=work,
                         ideal_speed_conversion_m_s=math.sqrt(2 * work / (mm.M_SAT + mm.M_SLED))))
    faces = charged_lines(24)
    half_positions = np.sort(np.r_[positions, (positions[1:] + positions[:-1]) / 2])
    half_forces = [force_at(float(s), faces, belts) for s in half_positions]
    refined_work = float(np.trapezoid(half_forces, half_positions))
    volume_checks = []
    for s in (0.2, 0.8, 1.0):
        low = force_at(s, faces, belts, (3, 3, 5))
        high = force_at(s, faces, belts, (5, 5, 7))
        volume_checks.append(dict(displacement_m=s, base_N=low, refined_N=high,
                                  relative_change=abs(high-low)/high))
    probes = np.array([[0.006, 0, 0], [0.012, 0, 0], [0.006, 0, 0.035],
                       [0.006, 0.004, 0], [0.024, -0.004, -0.035],
                       [0.006, 0, 0.100], [0.006, 0, 0.500]])
    surface_probes = field_by(probes, faces)
    analytic_probes = field_3d.halbach_pair(mm.DEPTH, n_wave=7).getB(probes)[:, 1]
    reference = json.loads(REFERENCE.read_text())
    fine_work = runs[-1]["ideal_work_J"]
    return dict(status="INDEPENDENT_3D_SURFACE_CHARGE_MODEL_NOT_FEM_OR_HARDWARE_VALIDATION",
                method="3-D magnetic surface-charge quadrature; exact depth integral; finite 162-belt JxB; ideal phase",
                software_versions=dict(python=platform.python_version(), numpy=np.__version__,
                                       matplotlib=matplotlib.__version__),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                parameters_sha256=hashlib.sha256(PARAM.read_bytes()).hexdigest(),
                reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
                assumptions=dict(ironless=True, uniform_remanence_T=mm.BR,
                                 magnet_depth_m=mm.DEPTH, moving_mass_kg=mm.M_SAT+mm.M_SLED,
                                 sheet_current_A_per_m=0.9*mm.K_RATED,
                                 stator_belts=len(belts), ideal_phase_at_each_position=True),
                runs=runs, station_refined_work_J=refined_work,
                station_refinement_fraction=abs(refined_work-fine_work)/refined_work,
                volume_checks=volume_checks,
                field_probes=[dict(point_m=p.tolist(), surface_By_T=float(b), analytic_By_T=float(a),
                                   relative_difference=abs(float(b-a))/max(abs(float(a)), 1e-12))
                              for p,b,a in zip(probes,surface_probes,analytic_probes)],
                reference_analytic_work_J=reference["ideal_finite_stator_work_J"],
                work_difference_fraction=(fine_work-reference["ideal_finite_stator_work_J"])/fine_work,
                caveats=["Magnet and stator geometry/material inputs shared with P118",
                         "Independent field formulation, but not an independent geometry measurement",
                         "Uniform magnetization and linear free space; no iron or nonlinear material",
                         "Phase reoptimized at each position; no selected winding, switching or voltage limit",
                         "No friction, contact, brake, thermal, host or physical test"])


def report(d: dict) -> str:
    fine = d["runs"][-1]
    face_change = abs(fine["ideal_work_J"]-d["runs"][-2]["ideal_work_J"])/fine["ideal_work_J"]
    field_max = max(p["relative_difference"] for p in d["field_probes"])
    volume_max = max(p["relative_change"] for p in d["volume_checks"])
    return "\n".join([
        "# P121 — independent depth-resolved 3-D magnetic force cross-check", "",
        "**Evidence class: numerical magnetic model, not 3-D FEM, measured thrust or a selected motor rating.**", "",
        "The ironless, uniformly magnetized Gen5 cuboids are represented as magnetic surface",
        "charges with density `M·n`. A separate implementation integrates the finite 90 mm",
        "depth of each face in closed form and the short face dimension by Gauss-Legendre",
        "quadrature, then integrates `J×B` in all 162 drawn stator belts. It does not call",
        "magpylib for the calculated field. It shares the geometry, remanence, material law,",
        "current sheet and ideal independent phase assumption with P118. Agreement checks",
        "the field mathematics and finite-stator integration, not those shared inputs.", "",
        "For air points, the evaluated field is `B_y = (1/4π) Σ (B_r·n) ∫∫ (y-y')/R³ dA`.",
        "The source-depth integral uses the finite limits `−D/2` and `D/2`; it is not a",
        "centre-plane field multiplied by depth. The winding cross-section uses (3,3,5)",
        "Gauss nodes in belt width, gap thickness and array depth.", "",
        "| Face quadrature | Ideal work | Speed conversion |", "|:--|--:|--:|",
        *[f"| {r['face_quadrature_order']} | {r['ideal_work_J']:.2f} J | {r['ideal_speed_conversion_m_s']:.3f} m/s |"
          for r in d["runs"]], "",
        f"The 16-to-24-node face work change is {100*face_change:.5f}%; halving the 25 mm",
        f"station spacing changes work by {100*d['station_refinement_fraction']:.4f}%.",
        f"Increasing cross-sectional quadrature from (3,3,5) to (5,5,7) changes three",
        f"sampled station forces by at most {100*volume_max:.3f}%.",
        f"Seven air-field probes, including points 0.10 and 0.50 m off the depth face,",
        f"differ from the analytic cuboid law by at most {100*field_max:.5f}%.", "",
        f"The final 3-D surface result is **{fine['ideal_work_J']:.1f} J ideal work**, equivalent",
        f"to **{fine['ideal_speed_conversion_m_s']:.3f} m/s** for the assumed moving mass.",
        f"P118's analytic cuboid integral is {d['reference_analytic_work_J']:.1f} J; the work",
        f"difference is {100*abs(d['work_difference_fraction']):.2e}%. P119's 2-D FEM omits",
        "depth end effects and is a separate trend check. None is an achieved release speed.", "",
        "![Independent 3-D surface-charge force overlay](../figures/gen5_finite_force_surface3d.png)", "",
        "**Remaining decisive gates:** voltage-limited switched winding and inverter with selected",
        "parts; force/load/contact across release and arrest; feed and retention geometry;",
        "installed mass and a complete mission comparison. Physical validation remains unrun.", "",
        "Reproduce with `python analysis/gen5_finite_force_surface3d.py` after installing",
        "`requirements.txt`. `--check` compares regenerated numbers and prose to the captured",
        "JSON and report. Source, geometry and reference hashes are in the JSON.", "",
    ])


def plot(d: dict) -> None:
    reference = json.loads(REFERENCE.read_text())
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=150)
    fine = d["runs"][-1]
    ax.plot(fine["positions_m"], fine["forces_N"], lw=2.3, color="#005f73",
            label="Independent 3-D surface-charge integral")
    ax.plot(reference["positions_m"], reference["forces_N"], lw=1.8, ls="--",
            color="#bb3e03", label="3-D analytic cuboid integral")
    ax.set(xlabel="Sled displacement from reference pose (m)",
           ylabel="Ideal forward force (N)",
           title="Gen5 finite-array 3-D force methods — ideal phase, no circuit limits")
    ax.set_ylim(bottom=0)
    ax.grid(alpha=.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG, metadata={"Software": "VOLLEY P121 model, not measured data"})
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    rendered = json.dumps(result, indent=2) + "\n"
    prose = report(result)
    if args.check:
        current = OUT.exists() and OUT.read_text() == rendered and REPORT.exists() and REPORT.read_text() == prose
        print("P121 current" if current else "P121 STALE")
        return 0 if current else 1
    OUT.write_text(rendered)
    REPORT.write_text(prose)
    plot(result)
    print(f"P121 3-D surface work {result['runs'][-1]['ideal_work_J']:.1f} J; "
          f"P118 analytic work {result['reference_analytic_work_J']:.1f} J")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
