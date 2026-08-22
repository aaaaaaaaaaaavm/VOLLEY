"""
VOLLEY | A69: the shape the 8 m drive tube is actually in.

WHY THIS EXISTS
---------------
A59 took the tube structurally and answered stress, buckling and mode frequency. It computed no
SHAPE. A67 then needed a centreline, had none, and declared a sinusoid of assumed amplitude --
and A67 band 9 made that assumption the dominant input in the whole guided-contact model, at a
Sobol total-order index of 0.894 against seal friction's 0.141.

A bracket cannot carry that. This computes the curve.

WHAT IT SOLVES
--------------
Euler-Bernoulli beam, 2-node Hermite elements, on the geometry cad/parameters.json holds: 8.0 m,
15.805 mm bore, 1.0 mm wall, aluminium 6061-T6, on the seven supports at 1.0 m A59 requires.
Supports are modelled as rigid transverse restraints with a declared placement tolerance.

Contributions are solved SEPARATELY and reported ranked, because A59's single combined number is
the defect this run exists to remove:

    self-weight, 1 g build orientation      the tube on a bench
    self-weight, 0 g                        the tube in orbit, which is the case that fires
    support placement tolerance             each support offset by a declared amount
    ascent lateral quasi-static             a declared launch case
    thermal bow                             an across-diameter gradient over A58's swing
    internal pressure                       radial bore growth, which is not bending

PROVENANCE
----------
Model output. Nothing is measured -- E4. Manufacturing straightness is NOT computed here: it
enters as a declared tolerance envelope and what a real 8 m bore can hold is MANUFACTURING.md's
to establish.

Bands declared in validation/A69_tube_centreline.md before this file existed.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
P = json.load(open(os.path.join(os.path.dirname(HERE), "cad", "parameters.json")))
D = P["groups"]["gen6_drive"]
S = P["groups"]["gen6_store"]

BORE = D["bore_mm"] / 1e3
WALL = D["tube_wall_mm"] / 1e3
OD = BORE + 2.0 * WALL
L = D["stroke_mm"] / 1e3
RHO = D["tube_material_density_kg_m3"]
E_MOD = 68.9e9                    # Pa, 6061-T6, handbook, declared at the point of use
NU = 0.33
ALPHA = 23.6e-6                   # 1/K, 6061-T6
G = 9.81
SUPPORT_PITCH = 1.0               # m, A59
SUPPORTS = tuple(float(i) for i in range(1, 8))          # seven, at 1.0 m
SUPPORT_TOL_MM = 0.05             # declared placement tolerance, per support
ASCENT_LATERAL_G = 6.0            # declared launch quasi-static case
THERMAL_DT_K = (1.0, 2.0, 5.0)    # across-diameter gradient, swept

I_SEC = math.pi * (OD ** 4 - BORE ** 4) / 64.0
A_SEC = math.pi * (OD ** 2 - BORE ** 2) / 4.0
MASS_PER_M = RHO * A_SEC


def beam(n_el, loads_per_m, support_x, support_y=None, kappa_th=0.0):
    """Hermite beam on rigid transverse supports, with an optional imposed thermal curvature.

    A uniform across-diameter temperature gradient imposes a uniform curvature on the WHOLE
    continuous member, not an independent bow in each span. In a displacement formulation that
    enters as an eigenstrain: the element load vector for a constant imposed curvature k is

        f_th = integral( B^T EI k ) dx  =  EI k [0, -1, 0, +1]

    -- equal and opposite end moments. The supports then constrain w only, so displacement AND
    rotation come out continuous and the curvature is finite everywhere. The earlier
    construction imposed a parabola per span and reset it at every support, which put a slope
    discontinuity of k*span at each one and kinked a continuous aluminium tube seven times.
    That is P110.
    """
    x = np.linspace(0.0, L, n_el + 1)
    le = L / n_el
    ndof = 2 * (n_el + 1)
    K = np.zeros((ndof, ndof))
    F = np.zeros(ndof)
    ke = (E_MOD * I_SEC / le ** 3) * np.array([
        [12, 6 * le, -12, 6 * le],
        [6 * le, 4 * le ** 2, -6 * le, 2 * le ** 2],
        [-12, -6 * le, 12, -6 * le],
        [6 * le, 2 * le ** 2, -6 * le, 4 * le ** 2]])
    for e in range(n_el):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(d, d)] += ke
        w = loads_per_m
        F[d] += w * le * np.array([0.5, le / 12.0, 0.5, -le / 12.0])
        if kappa_th:
            F[d] += E_MOD * I_SEC * kappa_th * np.array([0.0, -1.0, 0.0, 1.0])
    # rigid supports by penalty, with an optional prescribed offset
    pen = E_MOD * I_SEC / le ** 3 * 1e8
    sy = support_y if support_y is not None else [0.0] * len(support_x)
    for sx, off in zip(support_x, sy):
        j = 2 * int(round(sx / le))
        K[j, j] += pen
        F[j] += pen * off
    u = np.linalg.solve(K, F)
    return x, u[0::2], u[1::2]


def verify_simple_span(n_el=200):
    """A uniformly loaded simply supported span against 5wL^4/384EI. Band 1."""
    span, w = 1.0, MASS_PER_M * G
    x = np.linspace(0.0, span, n_el + 1)
    le = span / n_el
    ndof = 2 * (n_el + 1)
    K = np.zeros((ndof, ndof)); F = np.zeros(ndof)
    ke = (E_MOD * I_SEC / le ** 3) * np.array([
        [12, 6 * le, -12, 6 * le], [6 * le, 4 * le ** 2, -6 * le, 2 * le ** 2],
        [-12, -6 * le, 12, -6 * le], [6 * le, 2 * le ** 2, -6 * le, 4 * le ** 2]])
    for e in range(n_el):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(d, d)] += ke
        F[d] += w * le * np.array([0.5, le / 12.0, 0.5, -le / 12.0])
    pen = E_MOD * I_SEC / le ** 3 * 1e8
    K[0, 0] += pen; K[ndof - 2, ndof - 2] += pen
    u = np.linalg.solve(K, F)
    got = abs(u[0::2]).max()
    want = 5.0 * w * span ** 4 / (384.0 * E_MOD * I_SEC)
    return got, want, abs(got - want) / want


def case_self_weight(g_level, n_el=800):
    return beam(n_el, MASS_PER_M * g_level, SUPPORTS)


def case_support_tolerance(n_el=800, seed=20260822):
    rng = np.random.default_rng(seed)
    off = rng.uniform(-SUPPORT_TOL_MM, SUPPORT_TOL_MM, len(SUPPORTS)) / 1e3
    return beam(n_el, 0.0, SUPPORTS, support_y=off), off


def thermal_bow(dT):
    """Uniform across-diameter gradient bows the tube at constant curvature.

    kappa = alpha * dT / OD. Between supports the sagitta is kappa * pitch^2 / 8.
    """
    kappa = ALPHA * dT / OD
    return kappa, kappa * SUPPORT_PITCH ** 2 / 8.0


def pressure_bore_growth():
    """Hoop stress and the diametral growth it produces. Not bending -- clearance."""
    p = S["charge_pressure_bar"] * 1e5
    sigma_h = p * BORE / (2.0 * WALL)
    eps = sigma_h * (1.0 - NU / 2.0) / E_MOD
    return sigma_h, BORE * eps


def free_free_first_mode(n_el=400):
    """Unsupported first bending mode, for the A59 regression. Band 3."""
    le = L / n_el
    ndof = 2 * (n_el + 1)
    K = np.zeros((ndof, ndof)); M = np.zeros((ndof, ndof))
    ke = (E_MOD * I_SEC / le ** 3) * np.array([
        [12, 6 * le, -12, 6 * le], [6 * le, 4 * le ** 2, -6 * le, 2 * le ** 2],
        [-12, -6 * le, 12, -6 * le], [6 * le, 2 * le ** 2, -6 * le, 4 * le ** 2]])
    me = (MASS_PER_M * le / 420.0) * np.array([
        [156, 22 * le, 54, -13 * le], [22 * le, 4 * le ** 2, 13 * le, -3 * le ** 2],
        [54, 13 * le, 156, -22 * le], [-13 * le, -3 * le ** 2, -22 * le, 4 * le ** 2]])
    for e in range(n_el):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(d, d)] += ke
        M[np.ix_(d, d)] += me
    from scipy.linalg import eigh
    w2 = eigh(K, M, eigvals_only=True)
    # A free-free beam has two rigid-body modes at zero. Discretisation puts them at small but
    # non-zero eigenvalues, so filtering on 1e-6 returns numerical dust rather than the first
    # elastic mode. Drop the two rigid modes explicitly.
    w2 = np.sort(w2[w2 > 0.0])[2:]
    return math.sqrt(w2[0]) / (2.0 * math.pi)


def centreline(name="orbit"):
    """The curve the contact model consumes: y(x) and dy/dx, as callables.

    'orbit' is the case that fires: zero gravity, so the tube's own weight contributes nothing
    and the shape is support placement plus whatever manufacturing leaves. That is the finding.
    """
    n_el = 800
    if name == "bench":
        x, w, th = case_self_weight(1.0, n_el)
    elif name == "ascent":
        x, w, th = case_self_weight(ASCENT_LATERAL_G, n_el)
    else:
        (x, w, th), _ = case_support_tolerance(n_el)
    return x, w, th


def verify_imposed_curvature(n_el=400):
    """Limiting case: a SIMPLY SUPPORTED single span under uniform imposed curvature k.

    Closed form: w(x) = k x (span - x) / 2, so midspan = k span^2 / 8. This is the check the
    audit asked for, and it is independent of anything about VOLLEY.
    """
    span, kappa = 1.0, 1.0e-3
    n = n_el
    le = span / n
    ndof = 2 * (n + 1)
    K = np.zeros((ndof, ndof)); F = np.zeros(ndof)
    ke = (E_MOD * I_SEC / le ** 3) * np.array([
        [12, 6 * le, -12, 6 * le], [6 * le, 4 * le ** 2, -6 * le, 2 * le ** 2],
        [-12, -6 * le, 12, -6 * le], [6 * le, 2 * le ** 2, -6 * le, 4 * le ** 2]])
    for e in range(n):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(d, d)] += ke
        F[d] += E_MOD * I_SEC * kappa * np.array([0.0, -1.0, 0.0, 1.0])
    pen = E_MOD * I_SEC / le ** 3 * 1e8
    K[0, 0] += pen; K[ndof - 2, ndof - 2] += pen
    u = np.linalg.solve(K, F)
    got = abs(u[0::2]).max()
    want = kappa * span ** 2 / 8.0
    return got, want, abs(got - want) / want


def sagitta_over(x, y, land_sep_m, n=4000):
    """Three-point mismatch a two-land rigid piston sees. Differentiation-free."""
    a = land_sep_m / 2.0
    xi = np.linspace(a, L - a, n)
    return float(np.abs(np.interp(xi, x, y)
                        - 0.5 * (np.interp(xi - a, x, y) + np.interp(xi + a, x, y))).max())


def orbital_centreline(dT_K=2.0, n_el=800, seed=20260822, straightness_mm=0.0):
    """The shape that actually fires, as ONE compatible structural solution.

    0 g, so self-weight contributes nothing. The remaining terms are solved TOGETHER in a single
    beam solve -- support offsets as prescribed displacements and the thermal gradient as an
    imposed curvature on the continuous member -- rather than added as scalar peaks. Optional
    manufacturing straightness is superposed as a declared shape, and is DECLARED, not computed.
    """
    rng = np.random.default_rng(seed)
    off = rng.uniform(-SUPPORT_TOL_MM, SUPPORT_TOL_MM, len(SUPPORTS)) / 1e3
    kappa = ALPHA * dT_K / OD
    x, w, th = beam(n_el, 0.0, SUPPORTS, support_y=off, kappa_th=kappa)
    if straightness_mm:
        # A declared manufacturing bow: a single half-wave over the length, the shape a honed or
        # gun-drilled tube is specified against. Amplitude declared, not derived.
        w = w + (straightness_mm / 1e3) * np.sin(math.pi * x / L)
    return x, w, th, off, kappa
