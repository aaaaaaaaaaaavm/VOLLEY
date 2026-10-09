"""Independent limiting-case checks for the restored P113-S11 propagator."""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import finite_burn_departure as fb


def test_coast_preserves_two_body_invariants():
    radius = fb.RE + 450_000.0
    state = np.array([radius, 0., 0., math.sqrt(fb.MU / radius), 358.])
    out = fb.propagate(state, 1900.0, tight=True)
    energy = lambda y: np.dot(y[2:4], y[2:4]) / 2 - fb.MU / np.linalg.norm(y[:2])
    angular_momentum = lambda y: y[0] * y[3] - y[1] * y[2]
    assert abs(energy(out) - energy(state)) < 1e-6
    assert abs(angular_momentum(out) - angular_momentum(state)) < 1e-3
    assert out[4] == state[4]


def test_short_burn_matches_mass_flow_and_acceleration_limit():
    radius = fb.RE + 450_000.0
    state = np.array([radius, 0., 0., math.sqrt(fb.MU / radius), 358.])
    duration, thrust = 0.01, 10.0
    coast = fb.propagate(state, duration, tight=True)
    burn = fb.propagate(state, duration, thrust, 0., tight=True)
    expected_delta_v = thrust * duration / state[4]
    assert abs((burn[2] - coast[2]) - expected_delta_v) < 1e-8
    assert abs(burn[4] - (state[4] - thrust * duration / fb.VE)) < 1e-12
