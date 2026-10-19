"""Matched Earth-pole/gravity configuration cross-check; independent Cartesian ODE."""

from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.integrate import solve_ivp

H = Path(__file__).resolve().parent


def native(name):
    return np.array(
        [
            [float(x) for x in l.split()]
            for l in (H / name).read_text().splitlines()
            if l.strip() and l.strip()[0].isdigit()
        ]
    )


def orekit(name):
    a = np.genfromtxt(H / name, delimiter=",", names=True)
    return np.column_stack([a[n] for n in a.dtype.names])


def analyze():
    g = native("gmat_J2_continuous.txt")
    p = native("gmat_J2_pole.txt")
    o = orekit("orekit_matched_native.csv")
    f = orekit("orekit_matched_native_15.csv")
    assert g.shape == o.shape == f.shape == (2881, 7)
    pole = p[:, 9:12] / np.linalg.norm(p[:, 9:12], axis=1)[:, None]
    t = g[:, 0]
    state = g[:, 1:] * 1000
    mu = 3.986004415e14
    re = 6378136.3
    j2 = math.sqrt(5) * 4.8416539e-4

    def rhs(ti, z):
        r = z[:3]
        rr = np.linalg.norm(r)
        k = np.array([np.interp(ti, p[:, 0], pole[:, i]) for i in range(3)])
        k /= np.linalg.norm(k)
        dot = r @ k
        acc = -mu * r / rr**3 + 1.5 * j2 * mu * re**2 / rr**5 * (
            (5 * (dot / rr) ** 2 - 1) * r - 2 * dot * k
        )
        return np.r_[z[3:], acc]

    sol = solve_ivp(
        rhs,
        (t[0], t[-1]),
        state[0],
        method="DOP853",
        t_eval=t,
        rtol=2e-13,
        atol=1e-8,
        max_step=15,
    )
    assert sol.success
    dr = np.linalg.norm(o[:, 1:4] - state[:, :3], axis=1)
    dv = np.linalg.norm(o[:, 4:7] - state[:, 3:], axis=1)
    ref = np.linalg.norm(f[:, 1:4] - o[:, 1:4], axis=1)
    ind = np.linalg.norm(sol.y[:3].T - o[:, 1:4], axis=1)
    np.savetxt(
        H / "residuals.csv",
        np.c_[t, dr, dv, ref, ind],
        delimiter=",",
        header="t_s,gmat_orekit_position_m,gmat_orekit_velocity_m_s,orekit_step_refinement_m,scipy_orekit_position_m",
        comments="",
    )
    ablation = {}
    for label, am, ar, aj, tilt in [
        (
            "original_axis_gravity_and_repeated_stops",
            3.986004418e14,
            6378137.0,
            1.08262668e-3,
            False,
        ),
        ("matched_constants_fixed_axis_repeated_stops", mu, re, j2, False),
        ("matched_axis_and_constants_repeated_stops", mu, re, j2, True),
    ]:

        def old_rhs(ti, z):
            r = z[:3]
            rr = np.linalg.norm(r)
            k = (
                np.array([np.interp(ti, p[:, 0], pole[:, i]) for i in range(3)])
                if tilt
                else np.array([0.0, 0.0, 1.0])
            )
            k /= np.linalg.norm(k)
            dot = r @ k
            return np.r_[
                z[3:],
                -am * r / rr**3
                + 1.5
                * aj
                * am
                * ar**2
                / rr**5
                * ((5 * (dot / rr) ** 2 - 1) * r - 2 * dot * k),
            ]

        prev = solve_ivp(
            old_rhs,
            (p[0, 0], p[-1, 0]),
            p[0, 1:7] * 1000,
            method="DOP853",
            t_eval=p[:, 0],
            rtol=2e-13,
            atol=1e-8,
            max_step=30,
        )
        assert prev.success
        ablation[label] = float(
            np.linalg.norm(prev.y[:3].T - p[:, 1:4] * 1000, axis=1).max()
        )
    ablation["matched_axis_constants_continuous_arc"] = float(dr.max())
    d = {
        "case": "450 km; 51.6 deg; imposed 16.029 m/s relative input, 4/300 kg finite-host split; not motor rating",
        "gravity": {
            "mu_m3_s2": mu,
            "radius_m": re,
            "normalized_C20": -4.8416539e-4,
            "J2": j2,
            "pole": "GMAT EarthFixed z exported in EarthMJ2000Eq every 60s; linear vector interpolation, renormalized",
            "pole_tilt_initial_deg": float(np.rad2deg(np.arccos(pole[0, 2]))),
            "orientation_boundary": "Shared prescribed pole input; not independent validation of Earth orientation or EOP",
        },
        "gmat_version": "R2026a",
        "orekit_version": "13.1.6",
        "duration_s": 86400,
        "native_rows": len(t),
        "max_gmat_orekit_position_m": float(dr.max()),
        "terminal_gmat_orekit_position_m": float(dr[-1]),
        "max_gmat_orekit_velocity_m_s": float(dv.max()),
        "max_orekit_step_refinement_m": float(ref.max()),
        "max_independent_cartesian_position_m": float(ind.max()),
        "diagnostic_ablation_m": ablation,
        "interpretation": [
            "Earth pole/gravity configuration explains dominant kilometre-scale discrepancy",
            "Repeated GMAT stop/restart commands contribute decimetre-scale numerical history differences; continuous accepted-step reports avoid those repeated commands",
            "Remaining millimetre-scale inter-code residual includes representation/numerical effects; not isolated entirely to one source",
            "Finite epoch representation can affect millimetre-scale comparisons; observed residual is reported without claiming physical flight accuracy",
            "No atmospheric lifetime, actual release, coupled-host or continuous mission-clearance validation follows",
        ],
    }
    d["source_sha256"] = {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()
        for f in H.iterdir()
        if f.is_file()
        and f.suffix in [".java", ".script", ".txt", ".csv"]
        and f.name != "residuals.csv"
    }
    (H / "RESULTS.json").write_text(json.dumps(d, indent=2) + "\n")
    return d


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
