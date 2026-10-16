"""Independent orbit-averaged energy/angular-momentum decay integration.

The atmosphere and ballistic coefficient intentionally match the historical
screen. This checks numerical implementation, not atmospheric truth or service
lifetime. No motor, orbit model or historical lifetime routine is imported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/results/gen5_lifetime_crosscheck.json"
MU, RE, YEAR = 3.986004418e14, 6378137.0, 365.25 * 86400
TABLE = np.array([(150, 2.070e-9, 22.523), (180, 5.464e-10, 29.740),
                  (200, 2.789e-10, 37.105), (250, 7.248e-11, 45.546),
                  (300, 2.418e-11, 53.628), (350, 9.518e-12, 53.298),
                  (400, 3.725e-12, 58.515), (450, 1.585e-12, 62.828),
                  (500, 6.967e-13, 63.822), (600, 1.454e-13, 71.835),
                  (700, 3.614e-14, 88.667)])


def integrate(speed: float, nodes: int, rtol: float, scale: float = 1.0) -> dict:
    radius = RE + 450000
    energy = .5 * (np.sqrt(MU / radius) + speed)**2 - MU / radius
    a = -MU / (2 * energy)
    e = 1 - radius / a
    # Midpoint eccentric-anomaly quadrature avoids duplicate periodic endpoints.
    E = (np.arange(nodes) + .5) * (2 * np.pi / nodes)
    cos_E = np.cos(E)

    def rates(_, state):
        axis, ecc = state
        # Trial RK stages may step below the termination surface. Bound only
        # those out-of-domain evaluations so the event can be located safely.
        axis = max(RE + 100000.0, axis)
        ecc = min(.2, max(0.0, ecc))
        r = axis * (1 - ecc * cos_E)
        altitude = np.maximum(120.0, (r - RE) / 1000)
        idx = np.clip(np.searchsorted(TABLE[:, 0], altitude, side="right") - 1, 0, len(TABLE) - 1)
        density = scale * TABLE[idx, 1] * np.exp(-(altitude - TABLE[idx, 0]) / TABLE[idx, 2])
        v = np.sqrt(MU * (2 / r - 1 / axis))
        cos_true = (cos_E - ecc) / (1 - ecc * cos_E)
        weight = 1 - ecc * cos_E  # dt/T = weight dE/(2 pi)
        # Orbit-averaged specific energy loss and eccentricity-vector rate.
        energy_rate = np.mean(-.5 * density * v**3 / 61 * weight)
        axis_rate = 2 * axis**2 / MU * energy_rate
        eccentricity_rate = np.mean(-density * v / 61 * (ecc + cos_true) * weight)
        if state[1] <= 0 and eccentricity_rate < 0:
            eccentricity_rate = 0.0
        return [axis_rate * YEAR, eccentricity_rate * YEAR]

    def reentry(_, state):
        return state[0] * (1 - max(0.0, state[1])) - RE - 120000

    reentry.terminal, reentry.direction = True, -1
    solution = solve_ivp(rates, (0, 40), [a, e], method="DOP853", rtol=rtol,
                         atol=[.001, 1e-12], events=reentry, max_step=.02)
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError("Lifetime integration failed or hit the 40-year cap")
    return {"speed_input_m_s": speed, "lifetime_years": float(solution.t[-1]),
            "quadrature_nodes": nodes, "rtol": rtol, "density_multiplier": scale,
            "evaluations": solution.nfev}


def build() -> dict:
    runs = []
    for nodes, rtol in [(360, 1e-7), (720, 1e-9)]:
        base = integrate(0.0, nodes, rtol)
        for speed in [2.5, 12.448437098832297, 16.029]:
            case = integrate(speed, nodes, rtol)
            case["base_lifetime_years"] = base["lifetime_years"]
            case["lifetime_ratio"] = case["lifetime_years"] / base["lifetime_years"]
            runs.append(case)
    fine = runs[3:]
    changes = [abs(a["lifetime_ratio"] / b["lifetime_ratio"] - 1) for a, b in zip(runs[:3], fine)]
    if max(changes) > .005:
        raise RuntimeError("Lifetime ratio refinement exceeds predeclared 0.5% numerical band")
    return {"status": "NUMERICAL_CROSSCHECK_SHARED_STATIC_ATMOSPHERE_ONLY",
            "inputs": {"altitude_km": 450, "BC_kg_m2": 61, "stop_perigee_km": 120,
                       "speed_meaning": "imposed inertial tangential payload increment; host omitted"},
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "runs": runs, "max_ratio_refinement_fraction": max(changes),
            "numerical_band_fraction": .005,
            "limitations": ["same static density table as the historical model; no independent atmosphere",
                            "uniform density or ballistic-coefficient scaling cannot test solar invariance",
                            "no measured orbit, time-varying space weather, attitude or area distribution",
                            "no proof that the launcher delivers any input speed",
                            "not a GMAT/Orekit lifetime or mission-acceptance result"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    text = json.dumps(data, indent=2) + "\n"
    if args.check:
        old = json.loads(OUT.read_text())
        for a, b in zip(data["runs"], old["runs"]):
            if abs(a["lifetime_ratio"] / b["lifetime_ratio"] - 1) > .0001:
                raise SystemExit("Lifetime crosscheck snapshot differs by >0.01%")
    else:
        OUT.write_text(text)
    print("PASS: shared-atmosphere numerical ratio refinement <0.5%; environmental validation remains open")


if __name__ == "__main__":
    main()
