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

    LN   chi = 3(1 - e^2)/4          Lankarani-Nikravesh. What A67 used
    HC   chi = 3(1 - e)/(2 e)        Hunt-Crossley's own coefficient, no e -> 1 assumption
    ID   chi found by root-finding   so the free-impact restitution IS the declared e

ID is the route the separation-dynamics literature uses -- contact parameters identified against a
reference rather than assumed. Here the reference is the definition of restitution itself, which
makes the identification exact and cheap; against hardware it would be a measured coefficient.

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


LAWS = {"LN": chi_ln, "HC": chi_hc}
