"""
VOLLEY | A71: the guided-contact problem, solved with a stiff adaptive integrator.

WHY THIS EXISTS
---------------
A67 gave one number at one step size. A68 found a 65 % model-form spread in it. A70's retest on
the corrected centreline moved 44.17 -> 17.14 deg/s when the step was quartered. None of those is
a physical statement.

The contact here is PERSISTENT, not impulsive: the eccentric gas moment and the bore curvature
hold the lands against the wall. A penalty contact in persistent sliding is a very stiff spring,
and an explicit fixed-step method integrates its oscillation rather than the motion. The right
tools are an implicit adaptive integrator and a stiffness sweep -- because for a penalty method
the convergence test that matters is that the answer does NOT depend on the penalty parameter.

The damping term is smooth and needs no contact-onset state machine: with d = r - c,

    F = K d^n (1 + chi * ddot / v_ref)     clamped at F >= 0

v_ref is a DECLARED velocity scale, not a captured impact velocity, which is what makes the right
hand side continuous and integrable by Radau. chi comes from A68/P111.

Bands declared in validation/A71_guided_contact_converged.md before this file existed.

PROVENANCE
----------
Model output. Nothing measured -- E4. The peak penalty force is NOT reported as a physical
observable: it is an arbitrary stiffness times a penetration that vanishes as the stiffness rises.
Contact impulse is.
"""
import math
import os

import numpy as np
from scipy.integrate import solve_ivp

import guided_contact as g
import tube_centreline as tc

RESULTS = g.RESULTS
V_REF = 0.05                      # m/s, declared damping reference scale
N_EXP = 1.5


def _shape(dT_K, seed=20260822):
    """Two INDEPENDENT lateral centrelines, y and z.

    A real bore has no reason to be identically shaped in two axes, and the earlier device -- one
    shape shifted by a quarter of the length -- had a worse problem than being unphysical: it was
    evaluated with a modulo, so the rear land at x < s_half WRAPPED to the far end of the tube,
    where the overhang deflection is large. That is what drove megaNewton contact forces in A70's
    dynamics. Two seeds, and clamped interpolation, remove both faults.
    """
    x, y, th, _o, _k = tc.orbital_centreline(dT_K=dT_K, seed=seed)
    _x2, y2, th2, _o2, _k2 = tc.orbital_centreline(dT_K=dT_K, seed=seed + 7919)
    return x, y, th, y2, th2


def make_rhs(prm, shape):
    c, s_half, ey, ez, gy, gz, f_seal, K, chi, mu = prm
    xs, ys, ths, ys2, ths2 = shape
    Lmax = xs[-1]

    def bore(xq, axis):
        q = min(max(xq, 0.0), Lmax)          # clamp: the tube ends, it does not wrap
        if axis:
            return np.interp(q, xs, ys2), np.interp(q, xs, ths2)
        return np.interp(q, xs, ys), np.interp(q, xs, ths)

    def rhs(_t, st):
        x, vx, y, vy, z, vz, a, wa, b, wb = st
        p = g.P0 * (g.V0 / (g.V0 + g.AREA * max(x, 0.0))) ** g.GAMMA
        Fg = p * g.AREA
        fx = Fg
        my = (ez - gz) * Fg
        mz = -(ey - gy) * Fg
        moving = math.tanh(vx / 1e-3)
        ff = -f_seal * moving
        fx += ff
        my += -gz * ff
        mz += gy * ff
        ay = az = 0.0
        for s in (+1.0, -1.0):
            si = s * s_half
            xi = x + si
            yb, ybp = bore(xi, 0)
            zb, zbp = bore(xi, 1)
            dy = (y - gy) + si * b - yb
            dz = (z - gz) - si * a - zb
            r = math.hypot(dy, dz) + 1e-18
            d = r - c
            if d <= 0.0:
                continue
            vyl = vy + si * wb - ybp * vx
            vzl = vz - si * wa - zbp * vx
            ddot = (dy * vyl + dz * vzl) / r
            N = K * d ** N_EXP * (1.0 + chi * ddot / V_REF)
            if N <= 0.0:
                continue
            ny, nz = -dy / r, -dz / r
            ay += N * ny / g.M_BODY
            az += N * nz / g.M_BODY
            fx += -mu * N * moving
            my += -si * N * nz - gz * (-mu * N * moving)
            mz += si * N * ny + gy * (-mu * N * moving)
        return [vx, fx / g.M_BODY, vy, ay, vz, az, wa, my / g.I_TRANS, wb, mz / g.I_TRANS]
    return rhs


def observables(prm, shape, st):
    """Contact normal load and penetration at a state -- for impulse and the penetration check."""
    c, s_half, ey, ez, gy, gz, f_seal, K, chi, mu = prm
    xs, ys, ths, ys2, ths2 = shape
    Lmax = xs[-1]
    x, vx, y, vy, z, vz, a, wa, b, wb = st
    tot, pen = 0.0, 0.0
    for s in (+1.0, -1.0):
        si = s * s_half
        q = min(max(x + si, 0.0), Lmax)
        yb, ybp = np.interp(q, xs, ys), np.interp(q, xs, ths)
        zb, zbp = np.interp(q, xs, ys2), np.interp(q, xs, ths2)
        dy = (y - gy) + si * b - yb
        dz = (z - gz) - si * a - zb
        r = math.hypot(dy, dz) + 1e-18
        d = r - c
        if d <= 0.0:
            continue
        vyl = vy + si * wb - ybp * vx
        vzl = vz - si * wa - zbp * vx
        ddot = (dy * vyl + dz * vzl) / r
        N = K * d ** N_EXP * (1.0 + chi * ddot / V_REF)
        if N > 0.0:
            tot += N
            pen = max(pen, d)
    return tot, pen


def pack(clearance_um=None, land_sep_mm=None, ecc_mm=None, cg_off_mm=None,
         friction_N=None, e=None, law="MOD", K_scale=1.0, mu=None):
    q = dict(g.NOMINAL)
    for k, v in (("clearance_um", clearance_um), ("land_sep_mm", land_sep_mm),
                 ("ecc_mm", ecc_mm), ("cg_off_mm", cg_off_mm),
                 ("friction_N", friction_N), ("e", e)):
        if v is not None:
            q[k] = v
    c = q["clearance_um"] / 2.0 / 1e6
    K = float(g.contact_stiffness(np.array([c]))[0]) * K_scale
    chi = float(np.atleast_1d(g.CHI[law](np.atleast_1d(q["e"])))[0])
    return (c, q["land_sep_mm"] / 2.0 / 1e3, q["ecc_mm"] / 1e3, 0.0,
            q["cg_off_mm"] / 1e3, 0.0, q["friction_N"], K, chi,
            g.MU_CONTACT if mu is None else mu)


def run(dT_K=1.0, rtol=1e-8, atol=1e-12, method="Radau", straight=False, **kw):
    prm = pack(**kw)
    if straight:
        xs = np.linspace(0.0, g.STROKE, 801)
        z = np.zeros_like(xs)
        shape = (xs, z, z, z, z)
    else:
        shape = _shape(dT_K)
    rhs = make_rhs(prm, shape)
    xs0, ys0, ths0, ys2, ths2 = shape
    st0 = np.zeros(10)
    # Seat the piston with its REAR land at x = 0: the body reference starts one half-separation
    # in, so neither land is ever outside the tube.
    st0[0] = prm[1]
    st0[2] = float(np.interp(st0[0], xs0, ys0)) + prm[4]
    st0[4] = float(np.interp(st0[0], xs0, ys2)) + prm[5]
    st0[8] = float(np.interp(st0[0], xs0, ths0))
    st0[6] = -float(np.interp(st0[0], xs0, ths2))

    def stop(_t, s):
        return s[0] - g.STROKE
    stop.terminal, stop.direction = True, 1
    sol = solve_ivp(rhs, (0.0, 2.0), st0, method=method, events=stop,
                    rtol=rtol, atol=atol, dense_output=False)
    st = sol.y[:, -1]
    # impulse and peak penetration from the solver's own accepted steps
    imp, pen, load = 0.0, 0.0, []
    for i in range(sol.y.shape[1]):
        N, d = observables(prm, shape, sol.y[:, i])
        load.append(N)
        pen = max(pen, d)
    t = sol.t
    if len(t) > 1:
        imp = float(np.trapezoid(load, t)) if hasattr(np, "trapezoid") else float(
            np.trapz(load, t))
    W = g.gas_work(min(st[0], g.STROKE))
    ke = 0.5 * g.M_BODY * st[1] ** 2
    return dict(v_exit=float(st[1]), v_lat=float(math.hypot(st[3], st[5])),
                rate_deg_s=float(math.degrees(math.hypot(st[7], st[9]))),
                pitch_deg=float(math.degrees(st[6])), yaw_deg=float(math.degrees(st[8])),
                x_end=float(st[0]), t_end=float(sol.t[-1]),
                impulse_Ns=imp, peak_penetration_m=pen,
                peak_penetration_frac_clearance=pen / prm[0],
                mean_contact_N=float(np.mean([v for v in load if v > 0])) if any(
                    v > 0 for v in load) else 0.0,
                steps=int(sol.y.shape[1]), status=int(sol.status),
                gas_work_J=W, ke_J=ke,
                energy_gap_pct=100.0 * (W - ke - prm[6] * min(st[0], g.STROKE)) / W)
