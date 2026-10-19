"""Event-export derivative of the constructed four/twelve-release campaign.

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

    events = [dict(t_s=0.0,kind="initial",payload=0,delta=[0.0]*3,
                   mass_before_kg=300+device+remaining+fuel,
                   mass_after_kg=300+device+remaining+fuel,payload_kg=0,
                   expected_host=s0.tolist(),target_final=reference.y[:,-1].tolist())]

    def burn(delta, label, event_time):
        nonlocal fuel
        total = 300 + device + remaining + fuel
        dv = float(np.linalg.norm(delta))
        used = total * (-math.expm1(-dv / (ISP * G)))
        if used > fuel:
            raise RuntimeError(
                f"Fuel exhausted at {label}: {used:.6f} kg requested, {fuel:.6f} kg remaining"
            )
        expected_host=host.copy()
        expected_host[3:]+=delta
        events.append(dict(t_s=float(event_time),kind="burn",role=label,payload=0,
                           delta=delta.tolist(),mass_before_kg=total,
                           mass_after_kg=total-used,payload_kg=0,
                           expected_host=expected_host.tolist(),target_final=[0.0]*6))
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
        burn(needed - host[3:], "pre " + str(i + 1), t)
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
        events.append(dict(t_s=float(t),kind="shot",payload=i+1,
                           delta=(u*tangent).tolist(),mass_before_kg=M,
                           mass_after_kg=M-m,payload_kg=m,
                           expected_host=host.tolist(),target_final=target.y[:,-1].tolist()))
        coast_end = t + 20.0
        coast = arc(host, t, coast_end, step)
        host_arcs.append((t, coast_end, coast))
        host = coast.y[:, -1]
        arrival = times[i + 1] if i + 1 < N else t + 600.0
        target_host = reference.sol(arrival)
        vel, residual = shoot(host, coast_end, arrival, target_host[:3])
        burn(vel - host[3:], "transfer " + str(i + 1), coast_end)
        host[3:] = vel
        transfer = arc(host, coast_end, arrival, step)
        host_arcs.append((coast_end, float(arrival), transfer))
        host = transfer.y[:, -1]
        if i == N - 1:
            burn(target_host[3:] - host[3:], "final host velocity restoration", arrival)
            host[3:] = target_host[3:]
            final = arc(host, arrival, T, step)
            host_arcs.append((float(arrival), T, final))

    return dict(count=N,strategy=strategy,initial_fuel_kg=initial_fuel,
                device_mass_proxy_kg=device,fuel_used_kg=initial_fuel-fuel,
                initial_host=events[0]["expected_host"],events=events,
                reference_host_final=reference.y[:,-1].tolist(),
                source_host_final=host_arcs[-1][2].y[:,-1].tolist(),shots=shots,burns=burns)
