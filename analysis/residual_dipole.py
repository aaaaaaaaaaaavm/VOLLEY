"""
VOLLEY | The array's residual magnetic dipole, and the secular torque it puts on the host.

WHY THIS EXISTS
---------------
Review item 11. E29 covers the shot's MECHANICAL angular impulse. Nothing covers the MAGNETIC
one: a permanent-magnet array sitting in Earth's field experiences tau = m x B continuously,
whether or not the machine is firing, for the whole mission.

An ideal Halbach array over a whole number of wavelengths has ZERO net moment -- the block
magnetisations rotate through 360 degrees and sum to nothing. So the interesting quantity is
not the ideal residual, it is what MAGNET TOLERANCE leaves behind, because that does not cancel.

Provenance: model output. Block geometry and Br from cad/parameters.json via motor_model.
Tolerance figures are class values for sintered NdFeB, named at use, not a supplier spec.
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MU0 = 4 * math.pi * 1e-7

# Class tolerances for sintered NdFeB. Named per validation/README's external-value rule.
TOL_BR = 0.02          # +/- 2 % on remanence, typical catalogue grade spread
TOL_ANGLE_DEG = 2.0    # +/- 2 deg on magnetisation direction, typical

B_EARTH_LEO = 30e-6    # T, representative magnitude at 450 km
ORBIT_S = 5600.0
WHEEL_N_M_S = 15.0     # the ESPA-class wheel E29 uses


def block_moment():
    V = mm.W * mm.TH * mm.DEPTH
    return mm.BR * V / MU0, V


def ideal_residual(n_wave=7):
    """Vector sum of every block's moment, with no tolerance. Should be ~0."""
    m_blk, _ = block_moment()
    tot = np.zeros(3)
    for y_face, step in ((+mm.GAP / 2, -1), (-mm.GAP / 2, +1)):
        for i in range(n_wave * mm.NBLK):
            ang = math.radians((90 + step * i * 90) % 360)
            tot += m_blk * np.array([math.cos(ang), math.sin(ang), 0.0])
    return tot


def tolerance_residual(n_wave=7, trials=4000, seed=20260810):
    """Monte Carlo: what tolerance leaves behind when the ideal cancellation is imperfect."""
    rng = np.random.default_rng(seed)
    m_blk, _ = block_moment()
    n_blk = 2 * n_wave * mm.NBLK
    mags = []
    for _ in range(trials):
        tot = np.zeros(3)
        for y_face, step in ((+mm.GAP / 2, -1), (-mm.GAP / 2, +1)):
            for i in range(n_wave * mm.NBLK):
                ang = math.radians((90 + step * i * 90) % 360)
                ang += math.radians(rng.normal(0, TOL_ANGLE_DEG / 3))   # 3-sigma = tol
                m = m_blk * (1 + rng.normal(0, TOL_BR / 3))
                tot += m * np.array([math.cos(ang), math.sin(ang), 0.0])
        mags.append(np.linalg.norm(tot))
    mags = np.array(mags)
    return dict(n_blocks=n_blk, m_block=m_blk,
                mean=float(mags.mean()), p50=float(np.percentile(mags, 50)),
                p95=float(np.percentile(mags, 95)), p99=float(np.percentile(mags, 99)),
                max=float(mags.max()))


def torque_budget(m_res):
    tau = m_res * B_EARTH_LEO
    per_orbit = tau * ORBIT_S
    return dict(m_A_m2=m_res, tau_N_m=tau, H_per_orbit=per_orbit,
                orbits_to_saturate=WHEEL_N_M_S / per_orbit if per_orbit else float('inf'),
                days_to_saturate=(WHEEL_N_M_S / per_orbit) * ORBIT_S / 86400
                if per_orbit else float('inf'))


if __name__ == '__main__':
    m_blk, V = block_moment()
    print(f"block {mm.W*1e3:.0f} x {mm.TH*1e3:.0f} x {mm.DEPTH*1e3:.0f} mm, "
          f"Br {mm.BR} T -> {m_blk:.3f} A.m^2 each\n")
    ideal = ideal_residual()
    print(f"IDEAL residual over 7 whole wavelengths: {np.linalg.norm(ideal):.3e} A.m^2 "
          f"(numerically zero, as a Halbach must be)\n")

    tol = tolerance_residual()
    print(f"WITH TOLERANCE (+/-{TOL_BR*100:.0f} % Br, +/-{TOL_ANGLE_DEG:.0f} deg axis, "
          f"{tol['n_blocks']} blocks, 4000 trials):")
    for k in ('mean', 'p50', 'p95', 'p99', 'max'):
        print(f"   {k:>5s}  {tol[k]:8.3f} A.m^2")

    print(f"\nSECULAR TORQUE in a {B_EARTH_LEO*1e6:.0f} uT field, and what it does to a "
          f"{WHEEL_N_M_S:.0f} N.m.s wheel:\n")
    print(f"{'residual':>10s} {'torque N.m':>12s} {'H per orbit':>13s} {'orbits':>9s} {'days':>8s}")
    out = {}
    for lab in ('p50', 'p95', 'p99'):
        b = torque_budget(tol[lab]); out[lab] = b
        print(f"{lab:>10s} {b['tau_N_m']:12.3e} {b['H_per_orbit']:13.4f} "
              f"{b['orbits_to_saturate']:9.1f} {b['days_to_saturate']:8.1f}")
    print("\n   (worst case: no orbital averaging credited. A body-fixed dipole in a rotating")
    print("    field averages partially, so these are an upper bound -- and the bound is the")
    print("    number that decides whether the ACS can hold the campaign.)")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(m_block_A_m2=m_blk, ideal_residual=float(np.linalg.norm(ideal)),
                   tolerance=tol, B_earth_T=B_EARTH_LEO, wheel_N_m_s=WHEEL_N_M_S,
                   budget=out), open(os.path.join(RESULTS, 'residual_dipole.json'), 'w'),
              indent=2)
    print("\n-> results/residual_dipole.json")
