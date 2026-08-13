"""
A31: does the plate stay in the gap?

Bands declared in validation/A31_plate_drive_normal_force.md at f3b73d6, BEFORE this file
existed.

THE MODEL
---------
Layered media in the plane of travel. Two travelling current sheets at y = +-g/2, air, a
conducting slab of thickness t centred at transverse offset d, air. With x-dependence
e^{-jkx} the vector potential A_z satisfies

    A'' - k^2 A = 0                 in air
    A'' - (k^2 + j w_slip mu0 sigma) A = 0    in the conductor

where w_slip is the frequency the CONDUCTOR sees, i.e. the slip frequency -- the plate is at
rest in its own frame and the wave sweeps past it at the slip velocity.

Force comes from the **Maxwell stress tensor** evaluated on planes just above and below the
plate, so thrust and normal force fall out of one solution instead of two models that could
disagree:

    T_xy = Re{B_x conj(B_y)} / (2 mu0)          shear, i.e. thrust
    T_yy = (|B_y|^2 - |B_x|^2) / (4 mu0)        normal

    F = (stress on the top plane) - (stress on the bottom plane)

WHAT IT CANNOT DO
-----------------
Two-dimensional: infinite in the transverse direction, with A30's edge factor applied as a
scalar afterwards. Rigid, flat, parallel, steady state. See the run sheet.

Provenance: model output. Nothing measured. E4 stands.
"""
import json
import math
import os

import numpy as np

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MU0 = 4e-7 * math.pi

# Geometry, from A30 band 4/5: the widest plate that fits inside a 3U's own 100 mm section.
PLATE_W = 0.090
PLATE_LEN = 0.3405
PLATE_T = 0.003
SIGMA = 2.5e7                  # 6061-T6
TAU = 0.048                    # pole pitch
GAP_MECH = 0.002               # clearance each side
G_TOTAL = 2 * GAP_MECH + PLATE_T
EDGE = None                    # filled from A30's result at import time


def _edge_factor(width=PLATE_W, tau=TAU):
    """A30's measured transverse edge factor, imported rather than restated."""
    import edge_effect
    return edge_effect.edge_factor(width, tau)


def solve(offset=0.0, slip_freq=100.0, K_s=1.0, t=PLATE_T, g=G_TOTAL,
          sigma=SIGMA, tau=TAU):
    """Fields and Maxwell-stress forces per unit area, for a given stator current sheet.

    TWO current sheets, at y = +-g/2, each backed by iron -- a genuinely double-sided machine.
    The first version of this function had ONE sheet and a flux return, which is a
    single-sided machine, and it is one of the two reasons band 5 failed on the first run.

    Boundary conditions, with A = A_z(y) e^{-jkx}:
        H_x = -K_s  just inside the upper sheet          (iron above carries flux at H = 0)
        A, dA/dy continuous at both conductor faces      (aluminium is non-magnetic)
        H_x = +K_s  just inside the lower sheet
    """
    k = math.pi / tau
    w = 2 * math.pi * slip_freq
    gamma = np.sqrt(k * k + 1j * w * MU0 * sigma) if sigma > 0 else complex(k, 0.0)

    y_top, y_bot = offset + t / 2, offset - t / 2
    ys, yb = g / 2, -g / 2

    M = np.zeros((6, 6), dtype=complex)
    r = np.zeros(6, dtype=complex)
    # 0: upper sheet, H_x = -K_s  ->  dA/dy = -mu0 K_s
    M[0, 4], M[0, 5] = k * np.exp(k * ys), -k * np.exp(-k * ys)
    r[0] = -MU0 * K_s
    # 1,2: continuity at y_top  (conductor R1 -> air R2)
    M[1, 2], M[1, 3] = np.exp(gamma * y_top), np.exp(-gamma * y_top)
    M[1, 4], M[1, 5] = -np.exp(k * y_top), -np.exp(-k * y_top)
    M[2, 2], M[2, 3] = gamma * np.exp(gamma * y_top), -gamma * np.exp(-gamma * y_top)
    M[2, 4], M[2, 5] = -k * np.exp(k * y_top), k * np.exp(-k * y_top)
    # 3,4: continuity at y_bot  (air R0 -> conductor R1)
    M[3, 0], M[3, 1] = np.exp(k * y_bot), np.exp(-k * y_bot)
    M[3, 2], M[3, 3] = -np.exp(gamma * y_bot), -np.exp(-gamma * y_bot)
    M[4, 0], M[4, 1] = k * np.exp(k * y_bot), -k * np.exp(-k * y_bot)
    M[4, 2], M[4, 3] = -gamma * np.exp(gamma * y_bot), gamma * np.exp(-gamma * y_bot)
    # 5: lower sheet, H_x = +K_s
    M[5, 0], M[5, 1] = k * np.exp(k * yb), -k * np.exp(-k * yb)
    r[5] = MU0 * K_s

    c = np.linalg.solve(M, r)

    def AB(y, reg):
        a, b = (c[0], c[1]) if reg == 0 else (c[2], c[3]) if reg == 1 else (c[4], c[5])
        p = gamma if reg == 1 else k
        A = a * np.exp(p * y) + b * np.exp(-p * y)
        dA = p * (a * np.exp(p * y) - b * np.exp(-p * y))
        return 1j * k * A, dA                     # B_y = -dA/dx = jkA ; B_x = dA/dy

    eps = 1e-9
    By_t, Bx_t = AB(y_top + eps, 2)
    By_b, Bx_b = AB(y_bot - eps, 0)

    def stress(Bx, By):
        return (np.real(Bx * np.conj(By)) / (2 * MU0),
                (abs(By) ** 2 - abs(Bx) ** 2) / (4 * MU0))

    Txy_t, Tyy_t = stress(Bx_t, By_t)
    Txy_b, Tyy_b = stress(Bx_b, By_b)
    By_mid, _ = AB(offset, 1)
    return dict(thrust_Pa=Txy_t - Txy_b, normal_Pa=Tyy_t - Tyy_b,
                By_top=abs(By_t), By_bot=abs(By_b), By_mid=abs(By_mid))


def open_gap_field(K_s=1.0, **kw):
    """Peak flux density at the plate's own plane with the plate ABSENT.

    THIS is what a designer means by airgap flux density, and normalising on it is the second
    fix band 5 forced. The first version scaled on the field at the plate WITH the plate
    present -- which is screened, so demanding 0.45 T there drove the source arbitrarily hard
    and produced a thrust seven times the magnetic-pressure ceiling.
    """
    kw = dict(kw)
    kw['sigma'] = 0.0
    return solve(K_s=K_s, **kw)['By_mid']


def at_flux(Bg, **kw):
    """Rescale to a target OPEN-GAP flux density. Fields are linear in K_s, stresses
    quadratic, so one solve and a scale factor is exact and assumes no winding design."""
    ref = open_gap_field(**{k: v for k, v in kw.items() if k != 'slip_freq'})
    K = Bg / ref if ref > 0 else 0.0
    r = solve(K_s=K, **kw)
    r['K_s'] = K
    r['Bg_open'] = Bg
    return r


if __name__ == '__main__':
    import edge_effect
    EDGE = _edge_factor()
    A_plate = PLATE_W * PLATE_LEN
    Bg = 0.45
    print("A31: the plate in the gap\n")
    print(f"plate      {PLATE_W*1e3:.0f} x {PLATE_LEN*1e3:.1f} x {PLATE_T:.3f} m, "
          f"{A_plate*1e4:.0f} cm2, edge factor {EDGE:.4f} (A30)")
    print(f"gap        {GAP_MECH*1e3:.1f} mm clearance each side, "
          f"{G_TOTAL*1e3:.1f} mm total magnetic gap, pole pitch {TAU*1e3:.0f} mm\n")

    # Band 5 first: find the slip that maximises thrust, and check it against the ceiling.
    fs = np.logspace(0, 3.3, 160)
    th = [at_flux(Bg, slip_freq=f)['thrust_Pa'] for f in fs]
    i = int(np.argmax(th))
    f_opt, p_peak = float(fs[i]), float(th[i])
    ceiling = Bg * Bg / (2 * MU0)
    print(f"BAND 5  peak thrust {p_peak/1e3:.2f} kPa at {f_opt:.0f} Hz slip; "
          f"ceiling B^2/2mu0 = {ceiling/1e3:.2f} kPa  ->  {100*p_peak/ceiling:.1f} % of it")

    # Bands 1-3: sweep the transverse offset at the optimum slip.
    print(f"\n{'offset':>8} {'thrust kPa':>11} {'normal kPa':>11} {'F_x, N':>8} "
          f"{'F_y, N':>8} {'F_y/F_x':>8}  direction")
    rows = []
    for d_mm in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
        d = d_mm * 1e-3
        r = at_flux(Bg, offset=d, slip_freq=f_opt)
        Fx = r['thrust_Pa'] * A_plate * EDGE
        Fy = r['normal_Pa'] * A_plate * EDGE
        rows.append(dict(offset_mm=d_mm, thrust_Pa=r['thrust_Pa'],
                         normal_Pa=r['normal_Pa'], Fx_N=Fx, Fy_N=Fy))
        direction = ('centred' if d_mm == 0 else
                     'RESTORING' if Fy < 0 else 'DESTABILISING')
        print(f"{d_mm:7.2f}mm {r['thrust_Pa']/1e3:11.3f} {r['normal_Pa']/1e3:11.3f} "
              f"{Fx:8.1f} {Fy:8.1f} {abs(Fy)/max(abs(Fx),1e-9):8.3f}  {direction}")

    c0, c05 = rows[0], [r for r in rows if r['offset_mm'] == 0.5][0]
    stable = all(r['Fy_N'] < 0 for r in rows if r['offset_mm'] > 0)
    ratio = abs(c05['Fy_N']) / abs(c0['Fx_N'])
    dth = 100 * abs(c05['Fx_N'] - c0['Fx_N']) / abs(c0['Fx_N'])

    # Band 4: lateral in-plane misalignment reduces the overlap, so re-run A30's edge model.
    import edge_effect
    edge_off = edge_effect.edge_factor(PLATE_W - 0.003, TAU)
    dlat = 100 * abs(edge_off - EDGE) / EDGE
    print(f"\nBAND 4  3 mm lateral offset: overlap {PLATE_W*1e3:.0f} -> "
          f"{(PLATE_W-0.003)*1e3:.0f} mm, edge factor {EDGE:.4f} -> {edge_off:.4f} "
          f"({dlat:.2f} % thrust change)")

    b = {
        '1': ('normal force is restoring at every offset inside +-1.0 mm',
              'restoring' if stable else 'DESTABILISING', bool(stable)),
        '2': ('|F_normal| at 0.5 mm <= 20 % of thrust', f"{100*ratio:.1f} %",
              bool(ratio <= 0.20)),
        '3': ('thrust at 0.5 mm offset within 10 % of centred', f"{dth:.2f} %",
              bool(dth <= 10.0)),
        '4': ('thrust within 10 % at 3 mm lateral offset', f"{dlat:.2f} %",
              bool(dlat <= 10.0)),
        '5': ('peak thrust in (0.5, 1.0) x B^2/2mu0',
              f"{100*p_peak/ceiling:.1f} % of ceiling",
              bool(0.5 <= p_peak / ceiling <= 1.0)),
    }
    print("\nbands:")
    for kk in sorted(b):
        name, detail, ok = b[kk]
        print(f"  band {kk}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")
    print(f"\nthrust at centre, with the A30 edge factor applied: {c0['Fx_N']:.0f} N "
          f"({c0['Fx_N']/4.248/9.81:.1f} g on a 3U carrying its plate)")

    # The band-5 shortfall is a design question, not a solver fault: the machine reaches only
    # a fraction of the magnetic-pressure ceiling at this gap and pole pitch. Sweep for what
    # does close, kept separate from the bands so a failed band is never quietly re-run at a
    # geometry chosen after the fact.
    print("\nDESIGN SWEEP -- separate from the bands above, which stand as declared")
    print(f"  {'Bg':>5} {'tau':>6} {'clear':>6} {'t':>5} {'%ceil':>6} {'F,N':>7} "
          f"{'a/g':>5} {'v,m/s':>7} {'plate':>7}")
    sweep, best = [], None
    for Bg_i in (0.45, 0.60, 0.75):
        for tau_i in (0.048, 0.072):
            for clr in (0.0015, 0.002):
                for t_i in (0.003, 0.005):
                    g_i = 2 * clr + t_i
                    E_i = edge_effect.edge_factor(PLATE_W, tau_i)
                    th_i = max(at_flux(Bg_i, slip_freq=f, g=g_i, t=t_i,
                                       tau=tau_i)['thrust_Pa']
                               for f in np.logspace(0, 3, 90))
                    m_i = 4.0 + PLATE_W * PLATE_LEN * t_i * 2700
                    F_i = th_i * A_plate * E_i
                    a_i = F_i / m_i / 9.81
                    v_i = math.sqrt(2 * F_i / m_i * 1.30)
                    row = dict(Bg=Bg_i, tau=tau_i, clearance=clr, thickness=t_i,
                               pct_ceiling=100 * th_i / (Bg_i ** 2 / (2 * MU0)),
                               F_N=F_i, a_g=a_i, v_exit=v_i,
                               plate_kg=PLATE_W * PLATE_LEN * t_i * 2700)
                    sweep.append(row)
                    if a_i <= 25.0 and (best is None or v_i > best['v_exit']):
                        best = row
    for row in sorted(sweep, key=lambda r: -r['v_exit'])[:6]:
        print(f"  {row['Bg']:5.2f} {row['tau']*1e3:5.0f}mm {row['clearance']*1e3:5.1f}mm "
              f"{row['thickness']*1e3:4.1f}mm {row['pct_ceiling']:5.1f}% {row['F_N']:7.0f} "
              f"{row['a_g']:5.1f} {row['v_exit']:7.2f} {row['plate_kg']:6.3f}kg")
    print(f"\n  best inside the 25 g qualification cap: {best['F_N']:.0f} N, "
          f"{best['a_g']:.1f} g, {best['v_exit']:.2f} m/s at Bg {best['Bg']} T, "
          f"tau {best['tau']*1e3:.0f} mm, {best['thickness']*1e3:.0f} mm plate "
          f"({best['plate_kg']:.3f} kg)")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(plate_w=PLATE_W, plate_len=PLATE_LEN, plate_t=PLATE_T,
                   gap_mech=GAP_MECH, tau=TAU, sigma=SIGMA, Bg=Bg, edge_factor=EDGE,
                   f_opt_Hz=f_opt, peak_kPa=p_peak/1e3, ceiling_kPa=ceiling/1e3,
                   offset_sweep=rows, thrust_centre_N=c0['Fx_N'],
                   design_sweep=sweep, design_point=best,
                   bands=[dict(band=kk, name=b[kk][0], detail=b[kk][1], passed=b[kk][2])
                          for kk in sorted(b)]),
              open(os.path.join(RESULTS, 'plate_normal_force.json'), 'w'), indent=2)
    print("-> results/plate_normal_force.json")
