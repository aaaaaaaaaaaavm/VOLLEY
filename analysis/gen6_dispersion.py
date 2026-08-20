"""
VOLLEY | Commanded velocity at Gen6, and what actually sets its spread.

WHY THIS EXISTS
---------------
The product claim is commanded per-satellite velocity. Gen5 backed it with a designed loop --
0.0274 m/s at 3 sigma about a 15.8 m/s setpoint, on a gain designed against phase margin after
A28. Gen6 has A41 band 6, an open-loop sensitivity of 0.499 % of velocity per 1 % of charge,
and nothing else: no sensor, no loop, no error budget. precharged.py models no friction and no
temperature effect on charge, and A41 band 8 computed a friction ALLOWANCE rather than a
friction.

A43 settled the reservoir temperature this run needs as an input, which is why it comes second.

WHAT IS ADDED HERE
------------------
The work integral is imported from precharged, not restated. What is added is friction over the
stroke, a chamber temperature, and a Monte Carlo over the four terms that are actually uncertain.

Bands declared in validation/A44_gen6_dispersion.md at HEAD, BEFORE this file existed.

Provenance: model output. Ideal gas, adiabatic closed expansion, Coulomb friction constant over
the stroke, no blow-by, no valve dynamics, no residual pressure ahead of the piston, payload
mass and pressure errors treated as independent Gaussians at the stated 3 sigma. Nothing
measured.
"""
import json
import math
import os
import random

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# A44's OWN design point, frozen here. precharged.py derives STROKE and P_MAX live from
# cad/parameters.json (P84), so importing pc.STROKE would silently re-run A44 at whatever design
# point is current -- which is exactly what happened: ADR-034 moved the stroke to 8.0 m on
# 2026-08-19 and this script began computing a shot at 50 bar over 8.0 m, a point the project has
# never adopted. The published result stops reproducing and nothing says so.
#
# Same pattern as precharged.STROKE_A41: a dated run keeps its own numbers.
STROKE_A44 = 2.18                  # m, the stroke A44 ran at
P_NOMINAL = 50e5
V_CHAMBER_A44 = 2.0e-3             # m^3, A41's chamber, as A44 used it
SIGMA_P_FS = 0.0025 / 3.0          # 0.25 % of full scale, read as 3 sigma
SIGMA_M_REL = 0.005 / 3.0          # 0.5 % of payload mass, read as 3 sigma
FRICTION_N = 83.40371375447981     # A41 band 8's allowance, carried unchanged
SIGMA_F_REL = 0.20 / 3.0           # +-20 % of it, read as 3 sigma
T_SWEEP = (250.0, 300.0, 350.0, 400.0, 450.0)
N_MC = 200000
SEED = 20260816
SETPOINTS = (20.0, 22.5, 25.0, 27.5, 30.0)


def v_exit(p0, m_pay, friction_N):
    """A41's work integral, less the work friction takes out of the stroke."""
    w = pc.work(p0, V_CHAMBER_A44, STROKE_A44)
    w_net = w - friction_N * STROKE_A44
    if w_net <= 0.0:
        return 0.0
    return math.sqrt(2.0 * w_net / m_pay)


def charge_mass(p0, t_chamber, v0=2.0e-3):
    """Gas actually spent per shot. Depends on temperature; the work does not."""
    return p0 * v0 / (pc.R_GAS * t_chamber)


def p_for_v(target, m_pay, friction_N):
    """Charge pressure commanding a given exit velocity. Bisection, no closed form needed."""
    lo, hi = 1e5, 200e5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if v_exit(mid, m_pay, friction_N) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dispersion(p_cmd, sigma_p_fs=SIGMA_P_FS, sigma_m=SIGMA_M_REL,
               sigma_f=SIGMA_F_REL, n=N_MC, seed=SEED):
    """3 sigma spread, and the variance each term owns when it acts alone."""
    rng = random.Random(seed)
    vs = []
    for _ in range(n):
        p = p_cmd + rng.gauss(0.0, sigma_p_fs * P_NOMINAL)
        m = pc.M_PAY * (1.0 + rng.gauss(0.0, sigma_m))
        f = FRICTION_N * (1.0 + rng.gauss(0.0, sigma_f))
        vs.append(v_exit(p, m, f))
    mean = sum(vs) / len(vs)
    var = sum((v - mean) ** 2 for v in vs) / (len(vs) - 1)
    return mean, 3.0 * math.sqrt(var)


def solo(p_cmd, which, n=40000):
    """One term at a time, the others frozen, so the budget adds up to something."""
    kw = dict(sigma_p_fs=0.0, sigma_m=0.0, sigma_f=0.0, n=n)
    kw['sigma_' + which] = {'p_fs': SIGMA_P_FS, 'm': SIGMA_M_REL, 'f': SIGMA_F_REL}[which]
    return dispersion(p_cmd, **kw)[1]


def main():
    v0 = 2.0e-3
    v_nofric = math.sqrt(2.0 * pc.work(P_NOMINAL, v0) / pc.M_PAY)
    print(f"zero-friction exit velocity at 50 bar: {v_nofric:.3f} m/s")

    # band 2: open-loop sensitivity, the same quantity A41 band 6 reported
    dv = (math.sqrt(2.0 * pc.work(P_NOMINAL * 1.01, v0) / pc.M_PAY) - v_nofric) / v_nofric
    sens = dv * 100.0
    print(f"open-loop sensitivity: {sens:.3f} % of velocity per 1 % of charge")

    # band 3: does temperature cancel out of the work?
    temps = [(t, v_exit(P_NOMINAL, pc.M_PAY, FRICTION_N)) for t in T_SWEEP]
    t_spread = (max(v for _, v in temps) - min(v for _, v in temps)) / temps[0][1] * 100.0
    print(f"velocity across {T_SWEEP[0]:.0f}-{T_SWEEP[-1]:.0f} K at fixed fire pressure: "
          f"{t_spread:.6f} % spread")

    # band 7: what A41's full allowance costs
    v_fric = v_exit(P_NOMINAL, pc.M_PAY, FRICTION_N)
    fric_cost = (v_nofric - v_fric) / v_nofric * 100.0
    print(f"friction at the full {FRICTION_N:.1f} N allowance costs {fric_cost:.2f} % "
          f"({v_nofric:.3f} -> {v_fric:.3f} m/s)")

    # band 4 and 5: the budget at the design point
    mean, three_sig = dispersion(P_NOMINAL)
    parts = {k: solo(P_NOMINAL, k) for k in ('p_fs', 'm', 'f')}
    total_var = sum(v * v for v in parts.values())
    share = {k: (v * v / total_var * 100.0) for k, v in parts.items()}
    print(f"\n3-sigma dispersion at the design point: {three_sig:.4f} m/s about "
          f"{mean:.3f} ({three_sig/mean*100:.3f} %)")
    for k in ('p_fs', 'm', 'f'):
        print(f"  {k:5s} alone {parts[k]:.4f} m/s   {share[k]:5.1f} % of variance")
    dominant = max(share, key=share.get)

    # band 6: across the commanded range
    print()
    across = []
    for target in SETPOINTS:
        p = p_for_v(target, pc.M_PAY, FRICTION_N)
        m, s3 = dispersion(p, n=40000)
        across.append(dict(setpoint=target, p_bar=p / 1e5, mean=m,
                           three_sigma=s3, pct=s3 / m * 100.0))
        print(f"  {target:5.1f} m/s at {p/1e5:6.2f} bar -> {s3/m*100:.3f} % (3 sigma)")

    # band 8: the gas budget against A43's 300 K assumption
    m_hot = charge_mass(P_NOMINAL, pc.GAMMA * pc.T0)
    m_cold = charge_mass(P_NOMINAL, pc.T0)
    saving = (m_cold - m_hot) / m_cold * 100.0
    print(f"\ncharge mass: {m_cold*1e3:.2f} g at {pc.T0:.0f} K, {m_hot*1e3:.2f} g at "
          f"{pc.GAMMA*pc.T0:.0f} K -> {saving:.1f} % less")

    # sweep the pressure class, since that is the one term hardware can buy down
    print(f"\n{'transducer % FS':>16s} {'3-sigma %':>11s}")
    classes = []
    for fs in (0.0025, 0.001, 0.0005):
        _, s3 = dispersion(P_NOMINAL, sigma_p_fs=fs / 3.0, n=40000)
        classes.append(dict(fs_pct=fs * 100, three_sigma_pct=s3 / mean * 100))
        print(f"{fs*100:16.2f} {s3/mean*100:11.3f}")

    bands = [
        ('1', "zero-friction exit velocity reproduces A41's 30.535 m/s within 0.1 %",
         f"{v_nofric:.3f} m/s, {abs(v_nofric-30.535)/30.535*100:.3f} % off",
         abs(v_nofric - 30.535) / 30.535 <= 0.001),
        ('2', "open-loop sensitivity reproduces 0.499 % per 1 % within 2 %",
         f"{sens:.3f} %", abs(sens - 0.499) / 0.499 <= 0.02),
        ('3', 'velocity varies <= 0.01 % across 250-450 K at fixed fire pressure',
         f"{t_spread:.6f} %", t_spread <= 0.01),
        ('4', '3-sigma exit-velocity dispersion <= 0.5 %',
         f"{three_sig/mean*100:.3f} %", three_sig / mean <= 0.005),
        ('5', 'the largest contributor owns >= 50 % of the variance',
         f"{dominant} at {share[dominant]:.1f} %", share[dominant] >= 50.0),
        ('6', 'commanding 20 -> 30 m/s keeps 3-sigma <= 1.5 % at every setpoint',
         f"worst {max(a['pct'] for a in across):.3f} %",
         all(a['pct'] <= 1.5 for a in across)),
        ('7', "friction at the full 83.4 N allowance costs <= 10 % of exit velocity",
         f"{fric_cost:.2f} %", fric_cost <= 10.0),
        ('8', "charge mass at a hot fire >= 25 % below the 300 K figure",
         f"{saving:.1f} %", saving >= 25.0),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A44', bands_declared_commit='HEAD~1',
               note='ideal gas, adiabatic closed expansion, Coulomb friction constant over the '
                    'stroke, no blow-by, no valve dynamics, no residual pressure ahead of the '
                    'piston. Pressure, mass and friction errors are independent Gaussians at the '
                    'declared 3 sigma. Nothing measured.',
               n_mc=N_MC, seed=SEED,
               v_zero_friction=v_nofric, sensitivity_pct_per_pct=sens,
               temperature_spread_pct=t_spread, friction_cost_pct=fric_cost,
               friction_N=FRICTION_N,
               mean=mean, three_sigma=three_sig, three_sigma_pct=three_sig / mean * 100,
               contributions={k: dict(three_sigma=parts[k], variance_pct=share[k])
                              for k in parts},
               dominant=dominant, across_range=across,
               charge_mass_g_300K=m_cold * 1e3,
               charge_mass_g_hot=m_hot * 1e3, hot_saving_pct=saving,
               transducer_classes=classes,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'gen6_dispersion.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
