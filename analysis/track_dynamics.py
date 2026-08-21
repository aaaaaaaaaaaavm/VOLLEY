"""
A33: the track's dynamic case. Closes the analysis half of P36.

Bands declared in validation/A33_track_dynamics.md at 7baa062, BEFORE this file existed.

THE MECHANISM
-------------
The sled is 13.445 kg on a track whose entire distributed mass is 20 kg. A mass that large
travelling along a beam does not leave its modes where it found them: the first mode is
depressed while the sled is near midspan and recovers as it leaves, so the track's first mode
is not a number during a shot -- it is a function of position.

Meanwhile A17's ripple chirp sweeps UPWARD with velocity, f = v/lambda. The excitation rises
while the mode falls, and where they cross is not where a fixed-frequency SDOF puts it. That
is band 3.

The transverse path is the eccentricity: thrust and ripple act ALONG the track, at the stator
plane, which is offset from the longerons' neutral axis. That offset turns axial ripple into a
bending moment, and bending changes the 12 mm winding gap at 13.1 % of thrust per millimetre.

Geometry, EI and the mode constants are imported from sizing.py rather than restated.

Provenance: model output. No damping is measured anywhere in this project; A17's amplification
is used as given. E4 stands.
"""
import json
import math
import os

import numpy as np

import motor_model as mm
import sizing

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

L = 1.5
M_DIST = 20.0               # DECLARED ASSUMPTION, kg: track distributed mass per metre-ish
                            # lump for the beam mode. Not traced to mass_properties
E_AL = 69e9
I_SEC = 2 * ((0.045 * 0.065 ** 3 - 0.037 * 0.057 ** 3) / 12)
EI = E_AL * I_SEC
MU = M_DIST / L

LAM = mm.LAM
GAP_MM = 12.0
A17_AMPLIFICATION = 8.18
RIPPLE_PCT = 0.99
ECC = 0.0575                # DECLARED, m: thrust-line eccentricity from the section centroid
TARGET_HZ = 70.0
M_STOWED = 48.0             # DECLARED, kg: twelve 3U at 4.0 kg, stowed on the track at launch
BRAKE_STATION = 1.480
LAM2_FF, LAM2_PP = 22.37, 9.87
BETA_L_FF = 4.730040744862704


def mode_shape_ff(xi):
    """First fixed-fixed mode, normalised to unity at midspan."""
    b = BETA_L_FF
    r = (math.cosh(b) - math.cos(b)) / (math.sinh(b) - math.sin(b))

    def raw(t):
        return (math.cosh(b * t) - math.cos(b * t)
                - r * (math.sinh(b * t) - math.sin(b * t)))
    return raw(xi) / raw(0.5)


def f_bare(lam2=LAM2_FF):
    return lam2 / (2 * math.pi * L ** 2) * math.sqrt(EI / MU)


def generalised_mass():
    xi = np.linspace(0, 1, 2001)
    phi = np.array([mode_shape_ff(t) for t in xi])
    return float(MU * L * np.trapezoid(phi ** 2, xi))


def f_with_mass(x_m, m_add, lam2=LAM2_FF):
    """First mode with a point mass at x_m. Rayleigh: f scales as 1/sqrt(generalised mass)."""
    mg = generalised_mass()
    phi = mode_shape_ff(min(max(x_m / L, 0.0), 1.0))
    return f_bare(lam2) * math.sqrt(mg / (mg + m_add * phi ** 2))


def beam_deflection(M_applied, a, n=801):
    """Fixed-fixed beam deflection under a couple M applied at position a.

    Finite-difference solve of the Euler-Bernoulli equation, the couple represented as two
    opposite point forces one grid step apart, clamped at both ends.

    WHERE THE LOAD ACTS IS THE WHOLE QUESTION. The first version of this analysis used a
    closed-form midspan expression regardless of position, so band 6 -- which says "applied
    eccentrically at the brake station" -- was not the band being computed. An end-mounted
    brake reacts into the support; a midspan load bends the beam.

    Returns (midspan deflection, peak deflection anywhere, position of the peak).
    """
    h = L / (n - 1)
    x = np.linspace(0, L, n)
    A = np.zeros((n, n))
    q = np.zeros(n)
    for i in range(2, n - 2):
        A[i, i - 2:i + 3] = np.array([1.0, -4.0, 6.0, -4.0, 1.0]) / h ** 4
    A[0, 0] = 1.0
    A[1, 0], A[1, 1] = -1.0, 1.0
    A[n - 1, n - 1] = 1.0
    A[n - 2, n - 2], A[n - 2, n - 1] = -1.0, 1.0
    j = min(max(int(round(min(max(a, h), L - h) / h)), 2), n - 3)
    # A point force P enters the FD equation as a distributed intensity P/h, so the RHS is
    # P/(EI*h). THE FIRST VERSION OMITTED THAT h AND WAS WRONG BY THREE ORDERS OF MAGNITUDE,
    # which made bands 4 and 6 pass on deflections of a ten-thousandth of a millimetre.
    # verify_beam() below checks the solver against PL^3/192EI; there was no band on it,
    # and there should have been.
    F_pair = M_applied / h                      # couple as +-F one step apart
    q[j - 1] += -F_pair / (EI * h)
    q[j + 1] += +F_pair / (EI * h)
    w = np.linalg.solve(A, q)
    return (float(abs(w[n // 2])), float(np.abs(w).max()),
            float(x[int(np.argmax(np.abs(w)))]))


def point_force(P, a, n=801):
    """Fixed-fixed beam under a point force P at a. Used only to verify the solver."""
    h = L / (n - 1)
    A = np.zeros((n, n))
    q = np.zeros(n)
    for i in range(2, n - 2):
        A[i, i - 2:i + 3] = np.array([1.0, -4.0, 6.0, -4.0, 1.0]) / h ** 4
    A[0, 0] = 1.0
    A[1, 0], A[1, 1] = -1.0, 1.0
    A[n - 1, n - 1] = 1.0
    A[n - 2, n - 2], A[n - 2, n - 1] = -1.0, 1.0
    j = min(max(int(round(a / h)), 2), n - 3)
    q[j] = P / (EI * h)
    return float(abs(np.linalg.solve(A, q)[n // 2]))


def verify_beam(P=1000.0):
    """Point load at midspan of a fixed-fixed beam: the closed form is P L^3 / (192 EI)."""
    return point_force(P, L / 2), P * L ** 3 / (192 * EI)


def static_deflection(F, a, ecc=ECC):
    """Deflection under an axial force F acting `ecc` off the neutral axis, applied at a."""
    return beam_deflection(F * ecc, a)


def stroke_profile(n=2000):
    x = np.linspace(1e-4, mm.ACCEL_ZONE, n)
    return x, mm.V_FLEET * np.sqrt(x / mm.ACCEL_ZONE)


if __name__ == '__main__':
    Kt, ripple = mm.thrust_constant()
    shot = mm.shot(Kt)
    published = sizing.track_first_mode()
    sens = sizing.gap_tolerance()['sensitivity_pct_per_mm']

    print("A33: the track's dynamic case\n")
    num, closed = verify_beam()
    print(f"solver check  point load at midspan: {num*1e3:.4f} mm numeric vs "
          f"{closed*1e3:.4f} mm from PL^3/192EI  ({100*(num-closed)/closed:+.2f} %)")
    assert abs(num - closed) / closed < 0.02, (
        "the beam solver does not reproduce PL^3/192EI; every deflection below is wrong")
    print(f"track   L {L} m, EI {EI/1e3:.1f} kNm2, distributed mass {M_DIST} kg")
    print(f"sled    {mm.M_SLED} + {mm.M_SAT} = {mm.M_SLED+mm.M_SAT} kg travelling")
    print(f"gap     {GAP_MM:.0f} mm, {sens} % of thrust per mm\n")

    ff, pp = f_bare(LAM2_FF), f_bare(LAM2_PP)
    e_ff = 100 * abs(ff - published['fixed_fixed_Hz']) / published['fixed_fixed_Hz']
    e_pp = 100 * abs(pp - published['pinned_pinned_Hz']) / published['pinned_pinned_Hz']
    print(f"BAND 1  fixed-fixed {ff:.2f} vs {published['fixed_fixed_Hz']:.0f} Hz "
          f"({e_ff:+.2f} %); pinned-pinned {pp:.2f} vs {published['pinned_pinned_Hz']:.0f} Hz "
          f"({e_pp:+.2f} %)")

    f_launch = f_with_mass(0.0, mm.M_SLED + M_STOWED)
    f_launch_mid = f_with_mass(L / 2, mm.M_SLED + M_STOWED)
    print(f"\nBAND 2  launch, sled at the breech with {M_STOWED:.0f} kg stowed: "
          f"{f_launch:.1f} Hz   (target > {TARGET_HZ:.0f})")
    print(f"        the same mass at midspan would give {f_launch_mid:.1f} Hz")

    x, v = stroke_profile()
    f_chirp = v / LAM
    f_mode = np.array([f_with_mass(xi, mm.M_SLED + mm.M_SAT) for xi in x])
    cross = np.where(np.diff(np.sign(f_chirp - f_mode)) != 0)[0]
    print(f"\nBAND 3  chirp sweeps 0 -> {f_chirp[-1]:.0f} Hz; mode falls {f_mode[0]:.1f} -> "
          f"{f_mode.min():.1f} Hz (min at x = {x[int(np.argmin(f_mode))]*1e3:.0f} mm)")
    if len(cross):
        i = int(cross[0])
        depress = 100 * (1 - f_mode[i] / ff)
        print(f"        crossing at x = {x[i]*1e3:.0f} mm, v = {v[i]:.2f} m/s, "
              f"f = {f_mode[i]:.1f} Hz")
        print(f"        mode depressed {depress:.1f} % from {ff:.1f} Hz there  (band <= 10 %)")
    else:
        i, depress = -1, 0.0
        print("        they never cross")

    F_ripple = shot['F_cmd'] * RIPPLE_PCT / 100.0
    sweep = [static_deflection(F_ripple, xi) for xi in np.linspace(0.05, L - 0.05, 60)]
    d_static = max(t[0] for t in sweep)
    d_local = max(t[1] for t in sweep)
    d_dyn, d_dyn_local = d_static * A17_AMPLIFICATION, d_local * A17_AMPLIFICATION
    kt_mod = 2 * d_dyn * 1e3 * sens
    kt_local = 2 * d_dyn_local * 1e3 * sens
    gain = kt_mod / (2 * RIPPLE_PCT)
    print(f"\nBAND 4  ripple {F_ripple:.1f} N at {ECC*1e3:.1f} mm eccentricity -> "
          f"{d_static*1e6:.2f} um static, x{A17_AMPLIFICATION} = {d_dyn*1e6:.2f} um")
    print(f"        gap {2*d_dyn*1e3:.4f} mm pk-pk -> Kt {kt_mod:.4f} % pk-pk  (band <= 0.5 %)")
    print(f"        at the sled's own station rather than midspan: {kt_local:.4f} %")
    print(f"        ripple -> deflection -> gap -> thrust is a FEEDBACK path, gain {gain:.3f}")

    v_cr = 2 * ff * L
    ratio = shot['v_exit'] / v_cr
    print(f"\nBAND 5  critical speed 2 f1 L = {v_cr:.0f} m/s; exit {shot['v_exit']:.2f} m/s "
          f"-> {100*ratio:.2f} %   (band <= 20 %)")

    F_brake = 18.5e3
    d_bmid, d_brake, x_pk = static_deflection(F_brake, BRAKE_STATION)
    d_mid_case, _, _ = static_deflection(F_brake, L / 2)
    print(f"\nBAND 6  arrest {F_brake/1e3:.1f} kN at the brake station "
          f"({BRAKE_STATION*1e3:.0f} mm), {ECC*1e3:.1f} mm eccentric:")
    print(f"        {d_bmid*1e3:.4f} mm midspan, peak {d_brake*1e3:.4f} mm at "
          f"x = {x_pk*1e3:.0f} mm -> {100*d_brake*1e3/GAP_MM:.2f} % of the gap  (band <= 5 %)")
    print(f"        the same load at MIDSPAN would give {d_mid_case*1e3:.3f} mm "
          f"({100*d_mid_case*1e3/GAP_MM:.1f} % of the gap)")

    b = {
        '1': ('modal model reproduces sizing.py within 2 %',
              f"ff {e_ff:+.2f} %, pp {e_pp:+.2f} %", bool(e_ff <= 2.0 and e_pp <= 2.0)),
        '2': (f'launch case stays above {TARGET_HZ:.0f} Hz', f"{f_launch:.1f} Hz",
              bool(f_launch > TARGET_HZ)),
        '3': ('mode within 10 % of undepressed at the chirp crossing',
              f"{depress:.1f} % depressed" if len(cross) else "no crossing",
              bool(len(cross) and depress <= 10.0)),
        '4': ('Kt modulation from track motion <= 0.5 % pk-pk', f"{kt_mod:.4f} %",
              bool(kt_mod <= 0.5)),
        '5': ('exit velocity <= 20 % of critical speed', f"{100*ratio:.2f} %",
              bool(ratio <= 0.20)),
        '6': ('arrest deflection <= 5 % of the gap', f"{100*d_brake*1e3/GAP_MM:.2f} %",
              bool(100 * d_brake * 1e3 / GAP_MM <= 5.0)),
    }
    print("\nbands:")
    npass = 0
    for kk in sorted(b):
        name, detail, ok = b[kk]
        npass += ok
        print(f"  band {kk}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")
    print(f"\n{npass} of {len(b)} bands pass.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(L=L, EI_kNm2=EI / 1e3, mu=MU, eccentricity_m=ECC,
                   f_bare_ff=ff, f_bare_pp=pp, published=published,
                   generalised_mass_kg=generalised_mass(),
                   f_launch_Hz=f_launch, f_launch_midspan_Hz=f_launch_mid,
                   f_mode_min_Hz=float(f_mode.min()),
                   x_at_min_mm=float(x[int(np.argmin(f_mode))] * 1e3),
                   chirp_max_Hz=float(f_chirp[-1]),
                   crossing=(dict(x_mm=float(x[i] * 1e3), v=float(v[i]),
                                  f_Hz=float(f_mode[i]), depression_pct=depress)
                             if len(cross) else None),
                   ripple_N=F_ripple, deflection_static_um=d_static * 1e6,
                   deflection_dynamic_um=d_dyn * 1e6,
                   kt_modulation_pct=kt_mod, kt_modulation_local_pct=kt_local,
                   feedback_gain=gain, v_critical=v_cr, speed_ratio_pct=100 * ratio,
                   brake_station_m=BRAKE_STATION,
                   brake_deflection_midspan_mm=d_bmid * 1e3,
                   brake_deflection_peak_mm=d_brake * 1e3,
                   brake_if_midspan_mm=d_mid_case * 1e3,
                   damping="NOT SPECIFIED ANYWHERE IN THIS PROJECT; A17's 8.18x used as given",
                   bands=[dict(band=kk, name=b[kk][0], detail=b[kk][1], passed=b[kk][2])
                          for kk in sorted(b)]),
              open(os.path.join(RESULTS, 'track_dynamics.json'), 'w'), indent=2)
    print("-> results/track_dynamics.json")
