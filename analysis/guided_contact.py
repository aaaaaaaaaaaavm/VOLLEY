"""
VOLLEY | A67: the payload's guided contact state through the 8 m bore.

WHY THIS EXISTS
---------------
Gen6 has an axial model and no lateral or angular one, so it has an exit SPEED and no exit
ATTITUDE. A34 and A38 model the payload crossing its cradle clearance in the first tens of
milliseconds and answer that well. Nothing follows it for the remaining eight metres.

The bore is 15.805 mm over 8000 mm -- an L/D of 506 -- so the assembly's angular constraint
comes from two bearing lands a short distance apart inside a bore whose centreline is not
straight. That is the whole problem, and it is not in any file.

Bands declared in validation/A67_guided_contact.md at 246b7ee, BEFORE this file existed.

WHAT IS MODELLED
----------------
One rigid body -- piston, carriage and payload -- with ten states:

    x, vx            axial
    y, vy, z, vz     lateral, of the centre of mass
    a, wa            rotation about the y axis and its rate
    b, wb            rotation about the z axis and its rate

Small angles throughout: clearances are tens of micrometres over land separations of tens to
hundreds of millimetres, so the angles are of order 1e-4 rad and linearised kinematics are
exact to well beyond the precision of any input here. Roll is uncoupled in this model and is
reported as zero rather than integrated.

Contact is Lankarani-Nikravesh at each land: F = K d^1.5 (1 + 3(1-e^2)/4 * ddot/ddot_minus),
with the approach velocity captured at contact onset. K is not a free parameter -- it is set so
that penetration at the commanded axial force is 5 % of the nominal radial clearance, which is
the conformal-contact statement that a land in a bore is not a Hertzian point.

The bore centreline is a sagging shape between the supports A59 requires at 1.0 m: a sine of
wavelength twice the support pitch, with a declared amplitude and an independent phase in each
lateral axis.

PROVENANCE
----------
Model output. Nothing is measured -- E4. Six of the inputs have no source in this repository and
are declared in the run sheet as swept design variables: clearance, land separation, bore
straightness, force-line eccentricity, payload CG offset and the friction bracket. P67 closes the
friction bracket. P103 owns the rest.
"""
import json
import math
import os

import numpy as np

import cradle_restitution as cr

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
P = json.load(open(os.path.join(os.path.dirname(HERE), "cad", "parameters.json")))
D = P["groups"]["gen6_drive"]
S = P["groups"]["gen6_store"]
SEAL = P["groups"]["gen6_seal"]

GAMMA = 1.4                      # diatomic; A41's closed expansion uses the same
M_BODY = 4.0                     # kg, the 3U reference payload -- A38's M_SAT
I_TRANS = cr.I_PAYLOAD           # kg.m^2, imported not restated
E_REST = cr.E_ALUMINIUM          # published aluminium-on-aluminium top of range
MU_CONTACT = 0.15                # dry anodised aluminium on PTFE-faced land, declared
BORE = D["bore_mm"] / 1e3
AREA = D["piston_area_mm2"] / 1e6
STROKE = D["stroke_mm"] / 1e3
P0 = S["charge_pressure_bar"] * 1e5
V0 = S["chamber_volume_l"] / 1e3
F_CMD = D["commanded_force_N"]
SUPPORT_PITCH = 1.0              # m, A59: seven supports at 1.0 m spacing

# Nominal design point, from the run sheet's declared table.
NOMINAL = dict(clearance_um=50.0, land_sep_mm=120.0, straightness_mm=0.5,
               ecc_mm=0.1, cg_off_mm=1.0, friction_N=SEAL["friction_max_N"], e=E_REST)
BRACKET = dict(clearance_um=(20.0, 200.0), land_sep_mm=(40.0, 400.0),
               straightness_mm=(0.1, 2.0), ecc_mm=(0.0, 0.5), cg_off_mm=(0.0, 5.0),
               friction_N=(SEAL["friction_max_N"], SEAL["friction_allowance_N"]),
               e=(0.3, E_REST))


def contact_stiffness(clearance_m):
    """K such that penetration at the commanded force is 5 % of the radial clearance.

    A land in a bore is a conformal contact, not a Hertzian point, so a textbook sphere-on-flat
    stiffness understates it by orders of magnitude and would let the piston sink through its own
    clearance. Tying K to the clearance states the assumption where it can be seen.
    """
    return F_CMD / (0.05 * clearance_m) ** 1.5


# A70: the centreline may come from A69's structural solve instead of the declared sinusoid.
# _A69 holds (x, y_normalised, dy/dx_normalised); `amp` then scales a real shape rather than
# setting the amplitude of an assumed one. None of A67's results used this path.
_A69 = None


def bore_from_a69(dT_K=2.0, seed=20260822):
    """Load A69's orbital centreline and normalise it to unit peak. Returns its peak, in metres."""
    global _A69
    import tube_centreline as tc
    x, y, _off, _k = tc.orbital_centreline(dT_K=dT_K, seed=seed)
    pk = float(np.abs(y).max())
    yn = y / pk
    dy = np.gradient(yn, x)
    _A69 = (x, yn, dy)
    return pk


def bore_shape(x, amp, phase):
    """Centreline offset and slope at x, for one lateral axis.

    Without A69 loaded this is the sinusoid A67 declared: amplitude `amp`, wavelength twice the
    support pitch. With A69 loaded it is A69's own shape, scaled to `amp`; `phase` then selects
    the second lateral axis by shifting a quarter of the tube's length, because a real bore has
    no reason to be identically shaped in y and z.
    """
    if _A69 is None:
        k = 2.0 * math.pi / (2.0 * SUPPORT_PITCH)
        return amp * np.sin(k * x + phase), amp * k * np.cos(k * x + phase)
    xs, yn, dy = _A69
    shift = 0.0 if phase == 0.0 else 0.25 * xs[-1]
    xq = np.mod(x + shift, xs[-1])
    return amp * np.interp(xq, xs, yn), amp * np.interp(xq, xs, dy)


def rhs(st, prm, onset):
    """Ten derivatives, vectorised over the ensemble. `onset` holds ddot_minus per land."""
    x, vx, y, vy, z, vz, a, wa, b, wb = st
    c, s_half, amp, ey, ez, gy, gz, f_seal, K, e = prm
    dyn = np.zeros_like(st)

    # --- gas: closed adiabatic expansion, the Level-0 law A41 declared ---
    p = P0 * (V0 / (V0 + AREA * np.maximum(x, 0.0))) ** GAMMA
    Fg = p * AREA

    fx = Fg.copy()
    my = (ez - gz) * Fg
    mz = -(ey - gy) * Fg

    # --- seal friction: axial, on the piston axis ---
    moving = np.tanh(vx / 1e-3)                      # smooth sign, avoids chatter at v=0
    ff = -f_seal * moving
    fx += ff
    my += -gz * ff
    mz += gy * ff

    peak_N = np.zeros_like(x)
    for i, s in enumerate((+1.0, -1.0)):
        si = s * s_half
        xi = x + si
        yb, ybp = bore_shape(xi, amp, 0.0)
        zb, zbp = bore_shape(xi, amp, 0.5 * math.pi)
        # land centre, on the piston axis: CG minus the CG offset, plus the rotation term
        dy = (y - gy) + si * b - yb
        dz = (z - gz) - si * a - zb
        r = np.sqrt(dy * dy + dz * dz) + 1e-18
        d = r - c
        hit = d > 0.0
        # land lateral velocity, including the bore centreline sliding beneath it
        vyl = vy + si * wb - ybp * vx
        vzl = vz - si * wa - zbp * vx
        ddot = (dy * vyl + dz * vzl) / r
        # d = r - c, so ddot > 0 IS compression. onset[i] holds the approach rate captured
        # when the gap closed, and is positive by construction.
        #
        # A68 replaced the literal Lankarani-Nikravesh coefficient here with chi, carried in the
        # parameter tuple, because A67 band 3 showed LN does not return the restitution it is
        # given below e -> 1. `e` in this array is now the DAMPING COEFFICIENT chi, not the
        # restitution; pack() converts one to the other by whichever law is selected.
        damp = 1.0 + e * ddot / onset[i]
        N = np.where(hit, K * np.maximum(d, 0.0) ** 1.5 * np.maximum(damp, 0.0), 0.0)
        peak_N = np.maximum(peak_N, N)
        ny, nz = -dy / r, -dz / r
        Ny, Nz = N * ny, N * nz
        fx += -MU_CONTACT * N * moving
        my += -si * Nz - gz * (-MU_CONTACT * N * moving)
        mz += si * Ny + gy * (-MU_CONTACT * N * moving)
        dyn[3] += Ny / M_BODY
        dyn[5] += Nz / M_BODY

    dyn[0], dyn[2], dyn[4] = vx, vy, vz
    dyn[1] = fx / M_BODY
    dyn[3] += 0.0
    dyn[6], dyn[8] = wa, wb
    dyn[7] = my / I_TRANS
    dyn[9] = mz / I_TRANS
    return dyn, peak_N


def gaps(st, prm):
    """Penetration and approach rate at both lands, for the onset tracker."""
    x, vx, y, vy, z, vz, a, wa, b, wb = st
    c, s_half, amp, ey, ez, gy, gz, f_seal, K, e = prm
    out = []
    for s in (+1.0, -1.0):
        si = s * s_half
        xi = x + si
        yb, ybp = bore_shape(xi, amp, 0.0)
        zb, zbp = bore_shape(xi, amp, 0.5 * math.pi)
        dy = (y - gy) + si * b - yb
        dz = (z - gz) - si * a - zb
        r = np.sqrt(dy * dy + dz * dz) + 1e-18
        vyl = vy + si * wb - ybp * vx
        vzl = vz - si * wa - zbp * vx
        out.append((r - c, (dy * vyl + dz * vzl) / r))
    return out


def safe_step(prm, per_period=110.0):
    """Step size from the stiffest contact in the ensemble.

    A penalty contact has its own natural period, and RK4 diverges rather than degrading if the
    step does not resolve it. Contact stiffness rises as K d^0.5, so the binding case is the
    smallest clearance in the batch: K is tied to it, and so is the penetration at which the
    force is developed.

    110 is not a guess. A step-size study on the nominal case, in the results file as
    `convergence`, gives 8.79 deg/s at 4e-5, 9.55 at 2e-5, 15.10 at 1e-5, then 14.880, 14.877,
    14.879 and 14.876 at 5e-6, 2.5e-6, 1.25e-6 and 6.25e-7. The answer is converged below 5e-6
    and WRONG BY 40 % at 2e-5, which is the step a first attempt would reach for. 110 periods
    puts the nominal case at 5e-6.
    """
    c, K = prm[0], prm[8]
    d_ref = 0.05 * c
    k_lin = 1.5 * K * np.sqrt(d_ref)
    return float((2.0 * math.pi * np.sqrt(M_BODY / k_lin) / per_period).min())


def integrate(prm, h=None, t_max=1.2):
    """Fixed-step RK4 to the end of the stroke, vectorised over the ensemble."""
    if h is None:
        h = safe_step(prm)
    n = prm[0].size
    st = np.zeros((10, n))
    # Seat the piston in the bore at x = 0, aligned with the local centreline. Starting at the
    # global origin puts the lands a bore-sag outside their own clearance before the first step,
    # which is not an initial condition -- it is a crash.
    c, s_half, amp = prm[0], prm[1], prm[2]
    gy, gz = prm[5], prm[6]
    yb0, ybp0 = bore_shape(np.zeros(n), amp, 0.0)
    zb0, zbp0 = bore_shape(np.zeros(n), amp, 0.5 * math.pi)
    st[2] = yb0 + gy                 # CG lateral = axis + CG offset
    st[4] = zb0 + gz
    st[8] = ybp0                     # b: rotation about z, aligning the axis with dy_b/dx
    st[6] = -zbp0                    # a: rotation about y, aligning with dz_b/dx
    onset = [np.full(n, 1e-3), np.full(n, 1e-3)]        # ddot_minus, POSITIVE = closing
    live = np.ones(n, dtype=bool)
    peak = np.zeros(n)
    impulse = np.zeros(n)
    hits = np.zeros(n)
    e_fric = np.zeros(n)
    e_cont = np.zeros(n)
    exit_st = np.zeros((10, n))
    diverged = np.zeros(n, dtype=bool)
    was = [np.zeros(n, dtype=bool), np.zeros(n, dtype=bool)]
    t = 0.0
    while t < t_max and live.any():
        # contact-onset capture, once per outer step
        for i, (d, dd) in enumerate(gaps(st, prm)):
            now = d > 0.0
            fresh = now & (~was[i])
            onset[i] = np.where(fresh, np.maximum(dd, 1e-4), onset[i])
            hits += fresh & live
            was[i] = now
        k1, N1 = rhs(st, prm, onset)
        k2, _ = rhs(st + 0.5 * h * k1, prm, onset)
        k3, _ = rhs(st + 0.5 * h * k2, prm, onset)
        k4, _ = rhs(st + h * k3, prm, onset)
        step = (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        st = np.where(live, st + step, st)
        peak = np.where(live, np.maximum(peak, N1), peak)
        impulse = np.where(live, impulse + N1 * h, impulse)
        e_fric = np.where(live, e_fric + prm[7] * np.abs(st[1]) * h, e_fric)
        e_cont = np.where(live, e_cont + MU_CONTACT * N1 * np.abs(st[1]) * h, e_cont)
        # Divergence guard. A sample that leaves the bore by more than a bore diameter, or goes
        # non-finite, has failed numerically rather than physically. It is frozen and COUNTED --
        # a silently NaN sample would poison every statistic downstream.
        bad = live & (~np.isfinite(st).all(axis=0)
                      | (np.abs(st[2]) > BORE) | (np.abs(st[4]) > BORE))
        if bad.any():
            st[:, bad] = np.nan_to_num(st[:, bad], nan=0.0, posinf=0.0, neginf=0.0)
            diverged |= bad
            live = live & ~bad
        done = live & (st[0] >= STROKE)
        exit_st[:, done] = st[:, done]
        live = live & ~done
        t += h
    exit_st[:, live] = st[:, live]                       # any that never finished
    return exit_st, peak, impulse, hits, e_fric, e_cont, live, diverged, h


CHI = {"LN": lambda e: 3.0 * (1.0 - e * e) / 4.0,
       "HC": lambda e: 3.0 * (1.0 - e) / (2.0 * e)}


def _chi(law, e):
    """Damping coefficient from restitution. `law` is a name, a callable, or a number."""
    if isinstance(law, str):
        return CHI[law](e)
    if callable(law):
        return np.atleast_1d(law(e))
    return np.full_like(e, float(law))
LAW = "HC"      # A68: HC returns restitution to -0.4 % at the nominal e where LN returns +13.7 %


def pack(clearance_um, land_sep_mm, straightness_mm, ecc_mm, cg_off_mm, friction_N, e, law=None):
    """Ten parameter arrays in the order rhs() unpacks them.

    The last element is the DAMPING COEFFICIENT, converted from the restitution by the selected
    law. A68 is the run that chose it.
    """
    a = np.atleast_1d
    c = a(clearance_um) / 2.0 / 1e6                       # radial, from diametral
    return (c, a(land_sep_mm) / 2.0 / 1e3, a(straightness_mm) / 1e3,
            a(ecc_mm) / 1e3, np.zeros_like(a(ecc_mm)),
            a(cg_off_mm) / 1e3, np.zeros_like(a(cg_off_mm)),
            a(friction_N), contact_stiffness(c),
            _chi(law if law is not None else LAW, a(e)))


def run(law=None, **kw):
    q = dict(NOMINAL); q.update(kw)
    prm = pack(law=law, **q)
    ex, peak, imp, hits, ef, ec, stalled, diverged, h = integrate(prm)
    rate = np.degrees(np.hypot(ex[7], ex[9]))
    return dict(v_exit=ex[1], v_lat=np.hypot(ex[3], ex[5]), rate_deg_s=rate,
                pitch_deg=np.degrees(ex[6]), yaw_deg=np.degrees(ex[8]),
                peak_N=peak, impulse_Ns=imp, hits=hits, e_fric=ef, e_cont=ec,
                stalled=stalled, diverged=diverged, h=h, x_end=ex[0])


def gas_work(x=STROKE):
    """Integral of p A dx for the closed adiabatic expansion, in closed form."""
    return P0 * V0 / (GAMMA - 1.0) * (1.0 - (V0 / (V0 + AREA * x)) ** (GAMMA - 1.0))
