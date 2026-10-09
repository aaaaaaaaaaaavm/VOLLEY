"""Finite-array, finite-stator Gen5 3-D Lorentz-force screen.

This integrates the existing analytic 3-D cuboid field through every drawn stator
belt and the actual finite 162-belt length. It is independent of the periodic
wavelength *scaling* used by motor_model.thrust_constant(), but shares its
magnet material and analytic field law. It is NOT an independent 3-D FEM solve.
The phase is optimized at every station, making the work/speed an optimistic
geometric upper bound, not an achieved controlled shot.
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
import magpylib

import field_3d
import motor_model as mm

ROOT = Path(__file__).resolve().parents[1]
PARAM = ROOT / "cad/parameters.json"
OUT = ROOT / "analysis/results/gen5_finite_force_map.json"
FIG = ROOT / "figures/gen5_finite_force_map.png"
REPORT = ROOT / "validation/P118_gen5_finite_force_map.md"


def configuration() -> dict:
    g = json.loads(PARAM.read_text())["groups"]
    stator, sled = g["stator"], g["sled"]
    assert stator["conductor_count"] == 162
    assert stator["belt_pitch"] == 8.0 and stator["belt_width"] == 7.0
    assert stator["active_span_end"] == 1296
    assert sled["halbach_array_x_start"] == 230
    assert sled["halbach_array_x_end"] == 570
    assert abs(sled["halbach_array_width_y"] / 1000 - mm.DEPTH) < 1e-12
    assert abs((stator["belt_z_max"] - stator["belt_z_min"]) / 1000 - mm.WIND_THICK) < 1e-12
    return g


def force_at(field, belt_centers, displacement: float, order=(3, 3, 5), xwidth=0.007) -> float:
    """Positive ideal force with independent phase optimization at one station.

    motor_model axes: x travel, y air-gap, z array depth. CAD swaps y and z;
    dimensions are reconciled explicitly in configuration(). The sign of the
    Lorentz cross-product changes with winding polarity; phase optimization
    selects the positive-travel sense.
    """
    nx, ny, nz = order
    gx, wx = np.polynomial.legendre.leggauss(nx)
    gy, wy = np.polynomial.legendre.leggauss(ny)
    gz, wz = np.polynomial.legendre.leggauss(nz)
    thick = mm.WIND_THICK
    depth = mm.DEPTH
    array_center = 0.400 + displacement  # CAD x=230..570 mm at displacement zero.
    X = belt_centers[:, None, None, None] + xwidth * gx[None, :, None, None] / 2 - array_center
    Y = thick * gy[None, None, :, None] / 2
    Z = depth * gz[None, None, None, :] / 2
    points = np.empty((len(belt_centers), nx, ny, nz, 3))
    points[..., 0] = X
    points[..., 1] = Y
    points[..., 2] = Z
    by = field.getB(points.reshape(-1, 3))[:, 1].reshape(len(belt_centers), nx, ny, nz)
    volume_integral = np.einsum("ijkl,j,k,l->i", by, wx, wy, wz) * xwidth * thick * depth / 8
    seq = ((0, 1), (2, -1), (1, 1), (0, -1), (2, 1), (1, -1))
    phases = np.array([0.0, -2 * np.pi / 3, 2 * np.pi / 3])
    coeff = sum(sign * v * np.exp(1j * phases[phase])
                for i, v in enumerate(volume_integral)
                for phase, sign in (seq[i % 6],))
    return float(0.9 * mm.K_RATED / thick * abs(coeff))


def build(step=0.025, order=(3, 3, 5)) -> dict:
    g = configuration()
    field = field_3d.halbach_pair(mm.DEPTH, n_wave=7)
    stator = g["stator"]
    belts = (np.arange(stator["conductor_count"]) * stator["belt_pitch"]
             + stator["belt_width"] / 2) / 1000
    positions = np.linspace(0, mm.ACCEL_ZONE, round(mm.ACCEL_ZONE / step) + 1)
    forces = np.array([force_at(field, belts, float(s), order) for s in positions])
    work = float(np.trapezoid(forces, positions))
    midpoint_positions = (positions[:-1] + positions[1:]) / 2
    midpoint_forces = np.array([force_at(field, belts, float(s), order) for s in midpoint_positions])
    fine_positions = np.sort(np.r_[positions, midpoint_positions])
    fine_forces = np.empty(len(fine_positions))
    fine_forces[::2], fine_forces[1::2] = forces, midpoint_forces
    fine_work = float(np.trapezoid(fine_forces, fine_positions))
    moving_mass = mm.M_SAT + mm.M_SLED
    upper_speed = math.sqrt(2 * work / moving_mass)
    nominal_kt, _ = mm.thrust_constant()
    periodic_force = 0.9 * mm.K_RATED * nominal_kt
    convergence = []
    for s in (0.2, 0.8, 1.0):
        coarse = force_at(field, belts, s, (3, 3, 5))
        fine = force_at(field, belts, s, (5, 5, 7))
        convergence.append(dict(displacement_m=s, coarse_N=coarse, fine_N=fine,
                                relative_change=abs(fine - coarse) / max(fine, 1e-9)))
    full_pitch_reference = force_at(field, belts, 0.2, (5, 5, 7), xwidth=0.008)
    # Stator reference ends at 1.296 m; after 1.066 m displacement the
    # entire magnet array (CAD x=0.230..0.570 m) lies beyond that end.
    no_geometric_overlap_after = stator["active_span_end"] / 1000 - 0.230
    return dict(status="MODEL_SCREEN_NOT_FEM_OR_HARDWARE_VALIDATION",
                method="3-D analytic cuboid field; volume-integrated J cross B in finite stator belts; ideal phase at every station",
                software_versions=dict(python=platform.python_version(),numpy=np.__version__,
                                       matplotlib=matplotlib.__version__,magpylib=magpylib.__version__),
                parameter_sha256=hashlib.sha256(PARAM.read_bytes()).hexdigest(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                model_3d_field_source="analysis/field_3d.py; same analytic field law as motor_model.py",
                cad_to_field_axes="CAD y=depth, z=gap; field model y=gap, z=depth",
                magnetic_length_m=7 * mm.LAM, cad_array_length_m=g["sled"]["halbach_array_length"] / 1000,
                stator_belt_end_m=belts[-1] + 0.0035,
                declared_stator_active_end_m=stator["active_span_end"] / 1000,
                no_array_stator_overlap_after_m=no_geometric_overlap_after,
                nominal_periodic_force_N=periodic_force,
                full_pitch_hypothetical_force_N=full_pitch_reference,
                nominal_reported_exit_m_s=16.029,
                ideal_finite_stator_work_J=work,
                station_refined_work_J=fine_work,
                station_refinement_relative_change=abs(fine_work - work) / fine_work,
                ideal_finite_stator_exit_upper_m_s=upper_speed,
                moving_mass_kg=moving_mass,
                caveats=["Phase optimized independently at each x; no switching, voltage or current dynamics",
                         "Magnetization field shares motor_model analytic cuboid source; no independent 3-D FEM",
                         "CAD magnet length 340 mm versus seven modeled 48 mm wavelengths = 336 mm",
                         "No feeder, recoil, friction, stator segmentation, thermal or magnetic saturation"],
                quadrature_order=list(order),
                convergence=convergence,
                positions_m=positions.tolist(), forces_N=forces.tolist())


def plot(data: dict) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=150)
    ax.plot(data["positions_m"], data["forces_N"], color="#147a8c", lw=2,
            label="Finite 3-D analytic field, ideal phase")
    ax.axhline(data["nominal_periodic_force_N"], color="#b25829", lw=1.5, ls="--",
               label="Periodic force used by rated shot")
    ax.axvline(data["no_array_stator_overlap_after_m"], color="#a72d37", lw=1.2, ls=":",
               label="CAD magnet array beyond stator")
    ax.set(xlabel="Sled displacement from CAD reference pose (m)", ylabel="Integrated forward force (N)",
           title="Gen5 finite-array force screen — ideal phase, no circuit limits")
    ax.set_xlim(0, mm.ACCEL_ZONE)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=.22)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG)
    plt.close(fig)


def report(d: dict) -> str:
    v = max(x["relative_change"] for x in d["convergence"])
    return "\n".join([
        "# P118 — finite Gen5 3-D integrated-force map", "",
        "**Status: analytic field/geometry screen, not an independent 3-D FEM or physical validation.**",
        "The code integrates J×B over the 162 finite stator belts using the existing exact cuboid field",
        "and optimizes phase at every station. This is optimistic because switching, voltage, current,",
        "friction and thermal limits are omitted. It removes the periodic-infinite-stator scaling",
        "used for the rated shot while keeping the same magnetic material/field source.", "",
        f"CAD places the magnet array at 0.230–0.570 m and the declared active stator ends at 1.296 m.",
        f"After {d['no_array_stator_overlap_after_m']:.3f} m travel their geometric overlap vanishes,",
        "before the rated 1.300 m acceleration travel ends. The 336 mm modeled magnetic length",
        "differs from the 340 mm CAD envelope by 4 mm.", "",
        f"Finite-force ideal work: **{d['ideal_finite_stator_work_J']:.1f} J**; associated",
        f"optimistic exit speed: **{d['ideal_finite_stator_exit_upper_m_s']:.3f} m/s** for",
        f"{d['moving_mass_kg']:.3f} kg moving mass. Periodic rated model reports",
        f"{d['nominal_reported_exit_m_s']:.3f} m/s and assumes approximately",
        f"{d['nominal_periodic_force_N']:.1f} N throughout. The finite map must not silently",
        "replace that baseline: it is a **finding requiring model and configuration disposition**.", "",
        f"At 0.2 m travel, hypothetically filling the entire 8 mm belt pitch gives",
        f"{d['full_pitch_hypothetical_force_N']:.1f} N instead of the drawn 7 mm copper belt's",
        f"{d['convergence'][0]['fine_N']:.1f} N. Thus the periodic model's continuous-sheet",
        "assumption also masks the 1 mm insulation gap; this diagnostic is not a new winding.", "",
        f"Cross-sectional quadrature convergence at three stations changes force by at most {100*v:.3f}%",
        "between (3,3,5) and (5,5,7) points. Halving the 25 mm station step changes",
        f"integrated work by {100*d['station_refinement_relative_change']:.3f}%. Independent FEM",
        "remains an open check. The shared cuboid field law means agreement with the old",
        "field is not independent validation.", "",
        "![Finite force map](../figures/gen5_finite_force_map.png)", "",
        "Reproduce with `python analysis/gen5_finite_force_map.py` in an environment with the declared dependencies. Inputs,",
        "software and source hashes are in `analysis/results/gen5_finite_force_map.json`.", "",
    ])


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    d = build()
    rendered = json.dumps(d, indent=2) + "\n"
    prose = report(d)
    if args.check:
        ok = OUT.exists() and OUT.read_text() == rendered and REPORT.exists() and REPORT.read_text() == prose
        print("P118 current" if ok else "P118 STALE")
        return 0 if ok else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    REPORT.write_text(prose)
    plot(d)
    print(f"P118 ideal finite work {d['ideal_finite_stator_work_J']:.1f} J; upper speed {d['ideal_finite_stator_exit_upper_m_s']:.3f} m/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
