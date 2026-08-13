"""
A30: the transverse edge factor of a finite-width induction secondary.

Bands declared in validation/A30_rail_drive.md at 7df75ac, BEFORE this file existed.

WHAT IS SOLVED
--------------
A linear induction motor makes thrust from TRANSVERSE current in its secondary. In the
thin-sheet quasi-static limit the induced current is described by a stream function psi on
the sheet, with

    laplacian(psi) = sigma_s * dBn/dt,        psi = 0 on the sheet boundary

because no current can cross the edge. Current is K = curl(psi z_hat), i.e.
K_x = dpsi/dy, K_y = -dpsi/dx, and the longitudinal thrust density is K_y * Bn.

**That boundary condition IS the edge effect.** An infinitely wide sheet has no boundary in y,
psi depends on x alone, and the transverse current is unimpeded. A narrow strip must return its
current within its own width, and the loop is dominated by legs that produce no thrust.

The imposed field is one travelling wave, Bn = Bg cos(kx - wt) with k = pi/tau, taken in the
secondary's frame where it moves at the slip velocity. The edge factor reported is

    thrust(finite width) / thrust(infinite width, same sheet conductance, same field)

which is dimensionless, geometric, and independent of Bg, sigma and slip -- so it can be
computed once and applied to any operating point, which is exactly how rail_drive.py uses it.

WHAT IS NOT SOLVED
------------------
The secondary's own reaction field is not modelled. That is how the transverse edge effect is
defined and how Russell & Norsworthy derive their closed form, and it is a further loss in the
same direction, so this result is an UPPER BOUND on the coupling. For a band that can reject an
architecture, an upper bound is the conservative direction.

Provenance: model output. Nothing measured. E4 stands.
"""
import json
import math
import os

import numpy as np

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')


def russell_norsworthy(width, tau):
    """Closed-form transverse edge factor, Russell & Norsworthy 1958, primary over secondary.

    K_R = 1 - tanh(pi c / tau) / (pi c / tau),  c = half width.
    For c << tau this goes as (pi c / tau)^2 / 3 -- the useful current collapses with the
    SQUARE of the width-to-pole-pitch ratio, which is why a narrow secondary is hopeless.
    """
    x = math.pi * (width / 2.0) / tau
    return 1.0 - math.tanh(x) / x


def edge_factor(width, tau, n_per_tau=96, n_y=96):
    """Numerical edge factor, by solving the complex stream-function problem on the sheet.

    THE PHASOR IS THE WHOLE POINT, and the first version of this function did not have it.
    Writing the imposed field as a real cos(kx) makes psi 90 degrees out of phase with it, so
    the time-average thrust <K_y Bn> integrates to exactly zero for every width -- including
    ones Russell & Norsworthy say couple perfectly well. **Band 2 caught that**, which is what
    it was declared for.

    The travelling wave is a spatial phasor Bn = B e^{-jkx} at angular frequency w, so

        laplacian(psi) = j w sigma_s B e^{-jkx},     psi = 0 at y = +- width/2

    and the time-average longitudinal thrust density is 0.5 * Re{K_y conj(Bn)} with
    K_y = -dpsi/dx. Constants are set to unity: the reported quantity is a RATIO against the
    infinitely wide sheet under the same field, so w, sigma_s and B all cancel.

    Solved on a full 2-D grid rather than by reducing to the 1-D y-problem first, so that a
    discretisation error in x has somewhere to show up.
    """
    k = math.pi / tau
    Lx = 2.0 * tau
    nx = int(round(n_per_tau * 2))
    ny = n_y
    dx = Lx / nx
    dy = width / (ny + 1)                       # interior points only; psi = 0 on both edges

    x = (np.arange(nx) + 0.5) * dx
    Bn = np.exp(-1j * k * x)                    # unit amplitude spatial phasor
    rhs = 1j * np.tile(Bn[:, None], (1, ny))    # j*w*sigma_s*Bn, constants set to 1

    # Periodic in x, Dirichlet in y. One tridiagonal solve per x-Fourier mode.
    F = np.fft.fft(rhs, axis=0)
    m = np.arange(nx)
    lam_x = -(2 - 2 * np.cos(2 * np.pi * m / nx)) / dx ** 2
    off = np.full(ny - 1, 1.0 / dy ** 2)
    PSI = np.zeros_like(F)
    for i in range(nx):
        A = (np.diag(np.full(ny, -2.0 / dy ** 2 + lam_x[i]))
             + np.diag(off, 1) + np.diag(off, -1)).astype(complex)
        PSI[i] = np.linalg.solve(A, F[i])
    psi = np.fft.ifft(PSI, axis=0)

    dpsi_dx = (np.roll(psi, -1, axis=0) - np.roll(psi, 1, axis=0)) / (2 * dx)
    Ky = -dpsi_dx
    p_finite = 0.5 * np.real(Ky * np.conj(Bn)[:, None])
    F_finite = float(p_finite.mean() * width)          # thrust per unit length of travel

    # Infinite width: no y dependence, so laplacian -> d2/dx2 and psi = -j*Bn/k^2 exactly.
    # Discretised the same way so the two share their x-discretisation error.
    lam = lam_x
    Fh = np.fft.fft(1j * Bn)
    psi_inf = np.fft.ifft(np.where(lam != 0, Fh / np.where(lam != 0, lam, 1), 0))
    dpsi_inf = (np.roll(psi_inf, -1) - np.roll(psi_inf, 1)) / (2 * dx)
    p_inf = 0.5 * np.real(-dpsi_inf * np.conj(Bn))
    return F_finite / (float(p_inf.mean()) * width)


RAIL_W = 0.0085          # m, CDS corner rail minimum width
PLATE_W = 0.090          # m, widest flat plate fitting inside a 3U's 100 mm section
CUBESAT_LEN = 0.3405     # m
RHO_AL = 2700.0


if __name__ == '__main__':
    print("A30: transverse edge factor of a finite-width induction secondary\n")
    print(f"{'secondary':>26} {'width':>8} {'tau':>7} {'w/tau':>7} {'numeric':>9} "
          f"{'Russell':>9} {'diff':>7}")
    rows = []
    for name, w in (("CDS corner rail", RAIL_W), ("flat plate, 3U section", PLATE_W)):
        for tau in (0.036, 0.048):
            num = edge_factor(w, tau)
            rn = russell_norsworthy(w, tau)
            d = 100 * (num - rn) / rn
            rows.append(dict(secondary=name, width_m=w, tau_m=tau, numeric=num,
                             russell_norsworthy=rn, diff_pct=d))
            print(f"{name:>26} {w*1e3:6.1f}mm {tau*1e3:5.0f}mm {w/tau:7.3f} {num:9.4f} "
                  f"{rn:9.4f} {d:6.1f} %")

    rail = [r for r in rows if r['width_m'] == RAIL_W and r['tau_m'] == 0.048][0]
    plate = [r for r in rows if r['width_m'] == PLATE_W and r['tau_m'] == 0.048][0]

    # Band 3: the consequence for thrust, at the edge factor band 1 actually measures.
    MU0 = 4e-7 * math.pi
    def thrust(Bg, edge, area):
        return Bg * Bg / (2 * MU0) * edge * area
    A_rail = 4 * RAIL_W * CUBESAT_LEN
    A_plate = PLATE_W * CUBESAT_LEN
    F_rail = thrust(0.60, rail['numeric'], A_rail)
    F_plate = thrust(0.45, plate['numeric'], A_plate)

    # Band 5: what a plate meeting band 4 costs the customer. 3 mm is the thickness the
    # goodness factor wants at this pole pitch; it is also structurally sane as a mounting
    # plate, and it is the number the mass rests on.
    t_plate = 0.003
    m_plate = PLATE_W * CUBESAT_LEN * t_plate * RHO_AL

    print(f"\nassumed by rail_drive.py: 0.55")
    print(f"BAND 1  CDS rail at 48 mm pole pitch: {rail['numeric']:.4f}   (band >= 0.35)")
    print(f"BAND 2  against Russell-Norsworthy {rail['russell_norsworthy']:.4f}: "
          f"{rail['diff_pct']:+.1f} %   (band within 25 %)")
    print(f"BAND 3  rails at 0.60 T, {A_rail*1e4:.1f} cm2: {F_rail:.1f} N   (band >= 413 N)")
    print(f"BAND 4  90 mm plate at 48 mm pole pitch: {plate['numeric']:.4f}   (band >= 0.55)")
    print(f"BAND 5  that plate, {t_plate*1e3:.0f} mm thick: {m_plate:.3f} kg   (band < 0.5 kg)")
    print(f"        for scale, it makes {F_plate:.0f} N at only 0.45 T over "
          f"{A_plate*1e4:.0f} cm2")

    b = {
        '1': ('CDS rail edge factor >= 0.35', f"{rail['numeric']:.4f}",
              bool(rail['numeric'] >= 0.35)),
        '2': ('numeric agrees with Russell-Norsworthy within 25 %',
              f"{rail['diff_pct']:+.1f} %", bool(abs(rail['diff_pct']) <= 25.0)),
        '3': ('rails make >= 413 N at <= 0.60 T', f"{F_rail:.1f} N", bool(F_rail >= 413.0)),
        '4': ('90 mm plate edge factor >= 0.55', f"{plate['numeric']:.4f}",
              bool(plate['numeric'] >= 0.55)),
        '5': ('that plate weighs < 0.5 kg', f"{m_plate:.3f} kg", bool(m_plate < 0.5)),
    }
    print("\nbands:")
    for kk in sorted(b):
        name, detail, ok = b[kk]
        print(f"  band {kk}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(sweep=rows, rail=rail, plate=plate,
                   rail_area_m2=A_rail, plate_area_m2=A_plate,
                   rail_thrust_N_at_0p60T=F_rail, plate_thrust_N_at_0p45T=F_plate,
                   plate_thickness_m=t_plate, plate_mass_kg=m_plate,
                   assumed_by_rail_drive=0.55,
                   bands=[dict(band=kk, name=b[kk][0], detail=b[kk][1], passed=b[kk][2])
                          for kk in sorted(b)]),
              open(os.path.join(RESULTS, 'edge_effect.json'), 'w'), indent=2)
    print("\n-> results/edge_effect.json")
