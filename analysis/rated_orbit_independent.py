"""Independent two-body cross-check of the Gen5 rated tangential release impulse.

This deliberately does not import astro.py or its boosted_elements() method. A
Cartesian IVP is propagated with adaptive DOP853; orbital elements are recovered
from Cartesian energy and angular momentum. The check is scoped to immediate
post-release geometry. It cannot validate a lifetime, a host burn, or a dispenser.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/results/motor_results.json"
OUTPUT = ROOT / "analysis/results/rated_orbit_independent.json"
FIG = ROOT / "figures/rated_orbit_crosscheck"
MU = 3.986004418e14  # m^3/s^2, same declared Earth parameter as the rated orbit case
R_E = 6378.137e3  # m, equatorial radius used by the rated orbit case
ALT = 450e3  # m, reference circular host orbit, not a provider commitment


def elements(state: np.ndarray) -> tuple[float, float]:
    x, y, vx, vy = state
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    specific_energy = 0.5 * v2 - MU / r
    a = -MU / (2 * specific_energy)
    h = x * vy - y * vx
    e2 = max(0.0, 1 + 2 * specific_energy * h * h / MU**2)
    return a, math.sqrt(e2)


def propagate(dv: float, rtol: float) -> dict[str, float]:
    r0 = R_E + ALT
    v0 = math.sqrt(MU / r0)
    state0 = np.array([r0, 0.0, 0.0, v0 + dv], dtype=float)
    t_period = 2 * math.pi * math.sqrt(r0**3 / MU)

    def rhs(_t: float, z: np.ndarray) -> np.ndarray:
        x, y, vx, vy = z
        rn3 = (x * x + y * y) ** 1.5
        return np.array([vx, vy, -MU * x / rn3, -MU * y / rn3])

    sol = solve_ivp(rhs, (0, 2 * t_period), state0, method="DOP853",
                    rtol=rtol, atol=1e-7, max_step=t_period / 180,
                    t_eval=np.linspace(0, 2 * t_period, 721))
    if not sol.success:
        raise RuntimeError(sol.message)
    a0, e0 = elements(state0)
    a_series = np.array([elements(z)[0] for z in sol.y.T])
    e_series = np.array([elements(z)[1] for z in sol.y.T])
    return {
        "dv_m_s": dv,
        "semi_major_axis_rise_km": (a0 - r0) / 1e3,
        "perigee_altitude_km": (a0 * (1 - e0) - R_E) / 1e3,
        "apogee_altitude_km": (a0 * (1 + e0) - R_E) / 1e3,
        "period_change_s": 2 * math.pi * math.sqrt(a0**3 / MU) - t_period,
        "a_conservation_max_m": float(np.max(abs(a_series - a0))),
        "e_conservation_max": float(np.max(abs(e_series - e0))),
        "steps": len(sol.t),
    }


def main() -> None:
    raw = INPUT.read_bytes()
    rated = float(json.loads(raw)["shot"]["v_exit"])
    coarse = propagate(rated, 1e-9)
    fine = propagate(rated, 1e-11)
    r0 = R_E + ALT
    vc = math.sqrt(MU / r0)
    vis_viva = 1 / (2 / r0 - (vc + rated) ** 2 / MU)
    solver_difference_m = abs(coarse["semi_major_axis_rise_km"] - fine["semi_major_axis_rise_km"]) * 1e3
    independent_identity_m = abs(fine["semi_major_axis_rise_km"] * 1e3 - (vis_viva - r0))
    if fine["a_conservation_max_m"] > 0.02 or solver_difference_m > 0.02 or independent_identity_m > 0.02:
        raise AssertionError("rated two-body propagation fails the 0.02 m numerical consistency band")
    if abs(fine["semi_major_axis_rise_km"] - 28.8) > 0.15:
        raise AssertionError("rated output no longer agrees with the rounded manuscript claim")

    samples = [propagate(float(dv), 1e-10) for dv in (0, 1, 2, 5, 10, rated, 20)]
    result = {
        "status": "PASS_NUMERICAL_TWO_BODY_ONLY",
        "scope": "instantaneous tangential impulse in a 450 km circular Earth orbit; two-body Cartesian propagation",
        "excluded": ["atmospheric lifetime", "finite-duration release", "host recoil or maneuver",
                     "dispersion", "payload loads", "provider orbit or flight compatibility"],
        "motor_result_sha256": hashlib.sha256(raw).hexdigest(),
        "constants": {"mu_m3_s2": MU, "earth_radius_m": R_E, "host_altitude_m": ALT},
        "rated": fine,
        "numerical_check": {"coarse_rtol": 1e-9, "fine_rtol": 1e-11,
                            "semi_major_axis_difference_m": solver_difference_m,
                            "vis_viva_identity_difference_m": independent_identity_m,
                            "pass_band_m": 0.02},
        "impulse_sweep": samples,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(8.6, 4.2), layout="constrained")
    dvs = [x["dv_m_s"] for x in samples]
    rises = [x["semi_major_axis_rise_km"] for x in samples]
    ax.plot(dvs, rises, color="#177a8d", linewidth=2.5, marker="o")
    ax.scatter([rated], [fine["semi_major_axis_rise_km"]], s=130,
               facecolor="#e8aa46", edgecolor="#16283a", linewidth=1.2, zorder=5)
    ax.annotate(f"Gen5 rated model: {rated:.3f} m/s\n+{fine['semi_major_axis_rise_km']:.2f} km",
                (rated, fine["semi_major_axis_rise_km"]), xytext=(-148, 28),
                textcoords="offset points", arrowprops={"arrowstyle": "-", "color": "#526879"},
                bbox={"boxstyle": "round,pad=0.45", "facecolor": "#f5f8fa", "edgecolor": "#d6e1e8"})
    ax.set(xlabel="Prograde release impulse (m/s)", ylabel="Immediate semi-major-axis rise (km)",
           title="Independent Cartesian check of the 450 km reference orbit")
    ax.grid(alpha=0.23)
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.18)
    fig.savefig(FIG.with_suffix(".png"), dpi=180, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print(f"rated rise {fine['semi_major_axis_rise_km']:.6f} km; numerical difference {solver_difference_m:.6g} m")


if __name__ == "__main__":
    main()
