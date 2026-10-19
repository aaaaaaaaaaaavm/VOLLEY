"""Constructive matched four/twelve-release campaign and conditional clearance.

Declared fixed-axis J2, ideal host impulses, surrogate targets and mass proxies.
No measured release accuracy, actual host compatibility or collision probability.
"""

from pathlib import Path
import math, json, itertools, hashlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

H = Path(__file__).resolve().parent
O = H / "release"
O.mkdir(exist_ok=True)
MU = 3.986004418e14
RE = 6378137.0
J2 = 1.08262668e-3
ISP = 220.0
G = 9.80665


def rhs(t, s):
    r = s[:3]
    rr = np.linalg.norm(r)
    q = (r[2] / rr) ** 2
    return np.r_[
        s[3:],
        -MU * r / rr**3
        + 1.5
        * J2
        * MU
        * RE**2
        / rr**5
        * r
        * np.array([5 * q - 1, 5 * q - 1, 5 * q - 3]),
    ]


def arc(state, start, end, step=60):
    s = solve_ivp(
        rhs,
        (start, end),
        state,
        method="DOP853",
        dense_output=True,
        max_step=step,
        rtol=2e-12,
        atol=1e-7,
    )
    if not s.success:
        raise RuntimeError(s.message)
    return s


def construct(N, strategy, step=60, initial_fuel=10.0):
    times = np.linspace(0, 3600, N)
    T = 90000.0
    r = RE + 500000
    inc = math.radians(97.4)
    v = math.sqrt(MU / r)
    s0 = np.array([r, 0, 0, 0, v * math.cos(inc), v * math.sin(inc)])
    reference = arc(s0, 0, T, step)
    masses = [1.33 if i % 2 == 0 else 4.0 for i in range(N)]
    commands = np.linspace(3, 9, N)
    device = (16 if strategy == "spring" else 30) * N / 4
    fuel = float(initial_fuel)
    remaining = sum(masses)
    host = s0.copy()
    host_arcs = []
    satellites = []
    burns = []
    shots = []

    def burn(delta, label):
        nonlocal fuel
        total = 300 + device + remaining + fuel
        dv = float(np.linalg.norm(delta))
        used = total * (-math.expm1(-dv / (ISP * G)))
        if used > fuel:
            raise RuntimeError(
                f"Fuel exhausted at {label}: {used:.6f} kg requested, {fuel:.6f} kg remaining"
            )
        fuel -= used
        burns.append({"event": label, "dv_m_s": dv, "fuel_kg": used})

    def shoot(state, start, end, target):
        def fun(v):
            return arc(np.r_[state[:3], v], start, end, step).y[:3, -1] - target

        res = root(fun, state[3:], tol=1e-10)
        residual = float(np.linalg.norm(fun(res.x)))
        if residual > 1e-3:
            raise RuntimeError("shoot residual " + str(residual))
        return res.x, residual

    for i, t in enumerate(times):
        ref = reference.sol(t)
        tangent = ref[3:] / np.linalg.norm(ref[3:])
        desired = ref.copy()
        desired[3:] += commands[i] * tangent
        target = arc(desired, t, T, step)
        m = masses[i]
        before = 300 + device + remaining + fuel
        u = 2.5 if strategy == "spring" else commands[i] / (1 - m / before)
        if strategy == "volley_3_6":
            u = float(np.clip(u, 3, 6))
        used = 0.0
        for k in range(30):
            M = before - used
            needed = desired[3:] - (1 - m / M) * u * tangent
            dv = np.linalg.norm(needed - host[3:])
            next_used = before * (-math.expm1(-dv / (ISP * G)))
            if abs(next_used - used) < 1e-12:
                break
            used = next_used
        burn(needed - host[3:], "pre " + str(i + 1))
        host[3:] = needed
        M = 300 + device + remaining + fuel
        child = host.copy()
        child[3:] += (1 - m / M) * u * tangent
        parent = host.copy()
        parent[3:] -= (m / M) * u * tangent
        momentum = m * child[3:] + (M - m) * parent[3:] - M * host[3:]
        childarc = arc(child, t, T, step)
        enderr = childarc.y[:, -1] - target.y[:, -1]
        satellites.append((t, childarc))
        shots.append(
            {
                "payload": i + 1,
                "payload_kg": m,
                "release_s": float(t),
                "relative_speed_m_s": u,
                "terminal_position_residual_m": float(np.linalg.norm(enderr[:3])),
                "terminal_velocity_residual_m_s": float(np.linalg.norm(enderr[3:])),
                "momentum_identity_residual_kg_m_s": float(np.linalg.norm(momentum)),
            }
        )
        remaining -= m
        host = parent
        coast_end = t + 20.0
        coast = arc(host, t, coast_end, step)
        host_arcs.append((t, coast_end, coast))
        host = coast.y[:, -1]
        arrival = times[i + 1] if i + 1 < N else t + 600.0
        target_host = reference.sol(arrival)
        vel, residual = shoot(host, coast_end, arrival, target_host[:3])
        burn(vel - host[3:], "transfer " + str(i + 1))
        host[3:] = vel
        transfer = arc(host, coast_end, arrival, step)
        host_arcs.append((coast_end, float(arrival), transfer))
        host = transfer.y[:, -1]
        if i == N - 1:
            burn(target_host[3:] - host[3:], "final host velocity restoration")
            host[3:] = target_host[3:]
            final = arc(host, arrival, T, step)
            host_arcs.append((float(arrival), T, final))

    def host_state(t):
        for a, b, s in host_arcs:
            if a - 1e-8 <= t <= b + 1e-8:
                return s.sol(t)
        raise ValueError(t)

    # Conditional interval lower bound: |a_relative| <=20 m/s² while both radii >RE.
    # Each interval validates that domain from its centre state and the same bound.
    def interval_screen(f, g, start, end, threshold=20.0):
        observed = float("inf")
        lower = float("inf")
        evaluations = 0
        unresolved = 0
        fails = 0
        stack = [(a, min(a + 60, end), 0) for a in np.arange(start, end, 60)]
        while stack:
            a, b, depth = stack.pop()
            mid = (a + b) / 2
            h = (b - a) / 2
            s = f(mid)
            q = g(mid)
            rr = s[:3] - q[:3]
            vv = s[3:] - q[3:]
            d = float(np.linalg.norm(rr))
            observed = min(observed, d)
            evaluations += 1
            radii_ok = all(
                np.linalg.norm(x[:3]) - np.linalg.norm(x[3:]) * h - 5 * h * h > RE
                for x in [s, q]
            )
            bound = (
                d - np.linalg.norm(vv) * h - 10 * h * h - 0.02
            )  # conditional 1cm state error per object
            if radii_ok and bound > threshold:
                lower = min(lower, float(bound))
                continue
            if d < threshold:
                fails += 1
                lower = min(lower, float(bound))
                continue
            if depth >= 12:
                unresolved += 1
                lower = min(lower, float(bound))
                continue
            stack.extend([(a, mid, depth + 1), (mid, b, depth + 1)])
        return {
            "sampled_midpoint_min_m": observed,
            "conditional_lower_bound_m": lower,
            "interval_evaluations": evaluations,
            "observed_violations": fails,
            "unresolved_intervals": unresolved,
            "passes_conditional_20m_screen": fails == 0 and unresolved == 0,
            "assumptions": "1cm numerical state bound per object; fixed J2 point centres, radii validated by interval bound; not physical launch-interface clearance or covariance",
        }

    clear = []
    for i, (t, s) in enumerate(satellites):
        # Host impulses break acceleration continuity: split every such boundary.
        results = []
        for a, b, hs in host_arcs:
            lo = max(a, t + 20)
            if b > lo:
                results.append(interval_screen(s.sol, hs.sol, lo, b))
        clear.append(
            {
                "pair": ["host", i + 1],
                "minimum_evaluated_m": min(
                    x["sampled_midpoint_min_m"] for x in results
                ),
                "conditional_lower_bound_m": min(
                    x["conditional_lower_bound_m"] for x in results
                ),
                "passes": all(x["passes_conditional_20m_screen"] for x in results),
                "evaluations": sum(x["interval_evaluations"] for x in results),
            }
        )
    for (i, (ti, si)), (j, (tj, sj)) in itertools.combinations(
        enumerate(satellites), 2
    ):
        c = interval_screen(si.sol, sj.sol, max(ti, tj), T)
        clear.append({"pair": [i + 1, j + 1], **c})
    sample = []
    for t in range(0, 90001, 60):
        hs = host_state(t)
        for i, (birth, s) in enumerate(satellites):
            if t >= birth:
                sample.append([t, i + 1, *s.sol(t), *hs])
    np.savetxt(
        O / f"{N}_{strategy}_{initial_fuel:g}kg_step{step:g}_states.csv",
        np.array(sample),
        delimiter=",",
        header="t_s,payload,x,y,z,vx,vy,vz,host_x,host_y,host_z,host_vx,host_vy,host_vz",
        comments="",
    )
    return {
        "count": N,
        "strategy": strategy,
        "force_model": "Fixed-axis J2 surrogate, distinct from Earth-orientation harmonization benchmark",
        "device_mass_proxy_kg": device,
        "initial_fuel_kg": initial_fuel,
        "fuel_used_kg": initial_fuel - fuel,
        "total_host_dv_m_s": sum(x["dv_m_s"] for x in burns),
        "maximum_release_m_s": max(x["relative_speed_m_s"] for x in shots),
        "shots": shots,
        "burns": burns,
        "clearance": clear,
        "maximum_terminal_position_residual_m": max(
            x["terminal_position_residual_m"] for x in shots
        ),
        "same_final_host_position_residual_m": float(
            np.linalg.norm(host_arcs[-1][2].y[:3, -1] - reference.y[:3, -1])
        ),
        "assumed_device_plus_consumed_fuel_kg": device + initial_fuel - fuel,
        "initial_device_plus_loaded_fuel_kg": device + initial_fuel,
    }


if __name__ == "__main__":
    rows = []
    for n in [4, 12]:
        for strategy in ["spring", "volley_3_6", "volley_unrestricted"]:
            try:
                d = construct(n, strategy)
                d["status"] = "COMPUTED_IDEAL_IMPULSE_CASE"
                rows.append(d)
                print(
                    n,
                    strategy,
                    "fuel",
                    d["fuel_used_kg"],
                    "max speed",
                    d["maximum_release_m_s"],
                    "clearance failed",
                    sum(
                        not x.get(
                            "passes", x.get("passes_conditional_20m_screen", False)
                        )
                        for x in d["clearance"]
                    ),
                    flush=True,
                )
            except RuntimeError as error:
                rows.append(
                    {
                        "count": n,
                        "strategy": strategy,
                        "status": "FAILED",
                        "reason": str(error),
                    }
                )
                print(n, strategy, "FAILED", error, flush=True)
    (O / "RESULTS.json").write_text(
        json.dumps(
            {
                "evidence": "Constructive coupled ideal-impulse surrogate; not customer mission/hardware validation",
                "target_definition": "Reference-host prograde increments linearly 3–9m/s; 0–3600s releases; common 90000s epoch; final host restored at4200s",
                "mass_basis": "300kg host dry,10kg fuel,Isp220s; device proxies 30/16kg per4 payloads, not a designed installed mass",
                "clearance_boundary": "Conditional interval bound for nominal point centres after20s host guard; assumed1cm state error, not navigation covariance or launch-interface proof",
                "limitations": [
                    "Finite burns, slew/settling, plume and actual host control not modeled",
                    "Capsule/contact/motor errors not measured; nominal commands are imposed inputs",
                    "Customer target states and actual installed mass/source/cost remain unknown",
                ],
                "cases": rows,
                "source_sha256": hashlib.sha256(
                    Path(__file__).read_bytes()
                ).hexdigest(),
            },
            indent=2,
        )
        + "\n"
    )
