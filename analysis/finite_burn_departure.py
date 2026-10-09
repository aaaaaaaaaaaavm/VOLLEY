"""Planar finite-burn host propagator for the P113-S11/S12 reference screen.

This is a newly restored implementation. The older S12 JSON names a source file
that was never committed, so that JSON must be regenerated before its campaign
counts are cited as reproducible. Units: m, s, kg, N, radians.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp

from host_reference import G0, MU, RE

ISP_S = 220.0
VE = ISP_S * G0
SLEW_RATE = math.radians(0.5)
SLEW_ACCEL = math.radians(0.05)
SETTLE = 30.0


def slew(start: float, end: float) -> float:
    """Minimum rest-to-rest slew time with bounded rate and acceleration."""
    if not (math.isfinite(start) and math.isfinite(end)):
        raise ValueError("finite attitudes required")
    angle = abs(math.remainder(end - start, 2 * math.pi))
    ramp_angle = SLEW_RATE**2 / SLEW_ACCEL
    if angle <= ramp_angle:
        return 2 * math.sqrt(angle / SLEW_ACCEL)
    return 2 * SLEW_RATE / SLEW_ACCEL + (angle - ramp_angle) / SLEW_RATE


def propagate(state, duration: float, thrust: float = 0.0,
              angle: float = 0.0, *, tight: bool = False):
    """Integrate two-body gravity, fixed-inertial thrust and constant mass flow.

    The five-state vector is x, y, vx, vy, total retained mass. A zero-duration
    segment changes nothing. This planar surrogate has no attitude dynamics,
    flexible structure, plume effects, perturbations or continuous COLA guard.
    """
    y0 = np.asarray(state, dtype=float)
    if y0.shape != (5,) or not np.all(np.isfinite(y0)):
        raise ValueError("finite five-component state required")
    if not all(math.isfinite(x) for x in (duration, thrust, angle)):
        raise ValueError("finite duration, thrust and angle required")
    if duration < 0 or thrust < 0 or y0[4] <= 0:
        raise ValueError("nonnegative duration/thrust and positive mass required")
    burned = thrust * duration / VE
    if burned >= y0[4]:
        raise ValueError("burn exhausts host mass")
    if duration == 0:
        return y0.copy()

    direction = np.array([math.cos(angle), math.sin(angle)], dtype=float)

    def rhs(_t, y):
        r = np.linalg.norm(y[:2])
        if r <= RE:
            raise ValueError("trajectory intersects Earth")
        acceleration = -MU * y[:2] / r**3
        if thrust:
            acceleration += (thrust / y[4]) * direction
        return np.r_[y[2:4], acceleration, -thrust / VE]

    # Tighter replay is a numerical convergence test on the same physics.
    result = solve_ivp(rhs, (0.0, duration), y0, method="DOP853",
                       rtol=2e-12 if tight else 2e-10,
                       atol=1e-12 if tight else 1e-10,
                       max_step=15.0 if tight else 60.0)
    if not result.success:
        raise RuntimeError(result.message)
    out = result.y[:, -1]
    out[4] = y0[4] - burned  # exact constant-flow identity
    return out


def checks() -> dict[str, bool]:
    """Limiting cases independent of any optimized campaign."""
    radius = RE + 450_000.0
    speed = math.sqrt(MU / radius)
    state = np.array([radius, 0.0, 0.0, speed, 358.0])
    period = 2 * math.pi * math.sqrt(radius**3 / MU)
    one_orbit = propagate(state, period, tight=True)
    coast = propagate(state, 100.0)
    burn = propagate(state, 4.0, 10.0, 0.0)
    angle = math.radians(0.1)
    return {
        "identity": bool(np.array_equal(propagate(state, 0.0), state)),
        "coast_mass": bool(coast[4] == state[4]),
        "rocket_mass": bool(abs(burn[4] - (state[4] - 40.0 / VE)) < 1e-12),
        "circular_closure": bool(np.linalg.norm(one_orbit[:2] - state[:2]) < 0.01
                                 and np.linalg.norm(one_orbit[2:4] - state[2:4]) < 1e-5),
        "slew_identity": bool(slew(0.0, 2 * math.pi) == 0.0),
        "slew_symmetry": bool(abs(slew(-angle, angle) - slew(angle, -angle)) < 1e-12),
        "slew_triangle": bool(abs(slew(0.0, angle) -
                                   2 * math.sqrt(angle / SLEW_ACCEL)) < 1e-12),
    }


if __name__ == "__main__":
    for name, passed in checks().items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    if not all(checks().values()):
        raise SystemExit(1)
