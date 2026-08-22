"""
VOLLEY | A68: which compliant-contact law actually returns the restitution it is given.

WHY THIS EXISTS
---------------
A67 band 3 failed. Its Lankarani-Nikravesh implementation returned +13.7 % restitution error at
the nominal aluminium coefficient and +128 % at 0.3, and A67 diagnosed that as the known domain
limit of LN rather than an implementation error. That diagnosis is testable, and this file tests
it: if it is right, a formulation built for the low-restitution regime recovers e where LN does
not, and a formulation whose damping is IDENTIFIED rather than derived recovers it exactly.

Three laws, all of the form F = K d^n (1 + chi * ddot / ddot_minus):

    LN   chi = 3(1 - e^2)/4     Lankarani-Nikravesh (1990), J. Mech. Des. 112(3). What A67 used
    HC   chi = 3(1 - e)/2       Hunt & Crossley (1975), J. Appl. Mech. 42(2), to first order in
                                (1 - e). THERE IS NO e IN THE DENOMINATOR -- P111
    MOD  chi = 3(1 - e)/(2 e)   A relation of the later corrected (1 - e)/e family. NAMED FOR ITS
                                FORM, not for an author: its primary sources have NOT been read,
                                so it is carried as an explicitly unsourced sensitivity candidate
    ID   chi found by root-finding   so the free-impact restitution IS the declared e

ID IS NOT VERIFICATION. It root-finds against the same fixed-step solver, so it can only show the
solver agrees with itself -- that is parameter identification. The verification is impact_ivp(),
an independent adaptive implicit Radau solve of the same problem. P111.

Bands declared in validation/A68_contact_law.md before this file existed.

PROVENANCE
----------
Model output and code verification. Nothing is measured -- E4. The restitution values swept are
cradle_restitution.E_ALUMINIUM's published range and below it; no coefficient here is VOLLEY's.
"""
import math

import numpy as np
from scipy.optimize import brentq

N_EXP = 1.5                       # Hertzian exponent, as A67 declared


def chi_ln(e):
    return 3.0 * (1.0 - e * e) / 4.0


def chi_hc(e):
    """Hunt-Crossley's OWN first-order relation.

    Hunt & Crossley (1975), 'Coefficient of restitution interpreted as damping in vibroimpact',
    J. Appl. Mech. 42(2), give the hysteresis damping factor to first order in (1 - e) as
    lambda = 3k(1 - e)/(2 v_minus), i.e. chi = 3(1 - e)/2. THERE IS NO e IN THE DENOMINATOR.
    """
    return 3.0 * (1.0 - e) / 2.0


def chi_mod(e):
    """A modified hysteresis-damping relation of the chi = a(1 - e)/e family.

    A68 as first published called this 'Hunt-Crossley's own coefficient'. IT IS NOT -- see
    chi_hc above. Relations with e in the denominator belong to the later corrected family
    (Gonthier and others use (1 - e^2)/e; Flores and others use 8(1 - e)/(5e)); the specific
    constant used here is 3/2. P111.

    The primary sources for the later family have NOT been read: publisher records were not
    retrievable, so this function is named for its FORM and not for an author. Its behaviour is
    measured in the run sheet like any other candidate.
    """
    return 3.0 * (1.0 - e) / (2.0 * e)


def impact(chi, K, m, v0, h=2.0e-8, n=N_EXP):
    """One free radial impact. Returns the restitution the law actually delivers.

    Fixed-step RK4 on (d, ddot). The contact is entered at d = 0 with ddot = v0 > 0 (closing),
    and left when d returns to zero. The law's damping term uses the entry velocity, which is
    what ddot_minus means.
    """
    def acc(d, dd):
        if d <= 0.0:
            return 0.0
        return -K * d ** n * max(1.0 + chi * dd / v0, 0.0) / m

    d, dd = 0.0, v0
    for _ in range(4_000_000):
        k1d, k1v = dd, acc(d, dd)
        k2d, k2v = dd + 0.5 * h * k1v, acc(d + 0.5 * h * k1d, dd + 0.5 * h * k1v)
        k3d, k3v = dd + 0.5 * h * k2v, acc(d + 0.5 * h * k2d, dd + 0.5 * h * k2v)
        k4d, k4v = dd + h * k3v, acc(d + h * k3d, dd + h * k3v)
        d += (h / 6.0) * (k1d + 2 * k2d + 2 * k3d + k4d)
        dd += (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        if d <= 0.0 and dd < 0.0:
            return abs(dd) / v0
    raise RuntimeError("impact did not separate")


def peak_force(chi, K, m, v0, h=2.0e-8, n=N_EXP):
    def acc(d, dd):
        if d <= 0.0:
            return 0.0
        return -K * d ** n * max(1.0 + chi * dd / v0, 0.0) / m
    d, dd, pk = 0.0, v0, 0.0
    for _ in range(4_000_000):
        pk = max(pk, K * max(d, 0.0) ** n * max(1.0 + chi * dd / v0, 0.0))
        k1d, k1v = dd, acc(d, dd)
        k2d, k2v = dd + 0.5 * h * k1v, acc(d + 0.5 * h * k1d, dd + 0.5 * h * k1v)
        k3d, k3v = dd + 0.5 * h * k2v, acc(d + 0.5 * h * k2d, dd + 0.5 * h * k2v)
        k4d, k4v = dd + h * k3v, acc(d + h * k3d, dd + h * k3v)
        d += (h / 6.0) * (k1d + 2 * k2d + 2 * k3d + k4d)
        dd += (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        if d <= 0.0 and dd < 0.0:
            return pk
    raise RuntimeError("impact did not separate")


def chi_identified(e, K, m, v0, h=2.0e-8):
    """Find chi so the delivered restitution IS e. This is the identification."""
    if e >= 0.999:
        return 0.0
    lo, hi = 0.0, 20.0
    f = lambda c: impact(c, K, m, v0, h) - e                      # noqa: E731
    if f(hi) > 0.0:
        hi = 200.0
    return brentq(f, lo, hi, xtol=1e-6, rtol=1e-10)


LAWS = {"LN": chi_ln, "HC": chi_hc, "MOD": chi_mod}


def impact_ivp(chi, K, m, v0, n=N_EXP):
    """The same impact through an INDEPENDENT integrator: scipy's adaptive Radau.

    This is what the fixed-step RK4 result is checked against. It is not the same code path,
    not the same order, not the same step control and not the same stiffness treatment. The
    identification routine root-finds against the RK4 solver, so it can never validate it --
    that is parameter identification, not verification, and the run sheet says so.
    """
    from scipy.integrate import solve_ivp

    def f(_t, y):
        d, dd = y
        if d <= 0.0:
            return [dd, 0.0]
        return [dd, -K * d ** n * max(1.0 + chi * dd / v0, 0.0) / m]

    def sep(_t, y):
        return y[0]
    sep.terminal, sep.direction = True, -1
    sol = solve_ivp(f, (0.0, 1.0), [1e-15, v0], method="Radau", events=sep,
                    rtol=1e-11, atol=1e-16, max_step=1e-5)
    return abs(sol.y[1][-1]) / v0
