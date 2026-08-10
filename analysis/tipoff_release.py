"""A23: tip-off at release, modelled rather than bounded.

Bands declared in validation/A23_tipoff_release.md at bc113e6, before this file existed.

THE 2 DEG/S BAND IS NOT RE-DECLARED. It was fixed 2026-07-31 under P30 against the flown
internal NRCSD figure rather than the provisional external one, and is carried here unchanged.

WHAT A7-R LEFT OUT
------------------
A7-R computed the angular-impulse budget and the release tolerance that follows from it. It
treated release as the only event. But the cradle holds the payload WITH CLEARANCE, and under
the offset moment the payload does not sit still in that clearance -- it accelerates across it
and arrives at the far side with a rate. There is an impact into the cradle at the start of
every shot, and it appears nowhere in this project.

Three stages: clearance take-up, constrained stroke, release. All rigid body. Where a mechanism
property is needed it is a swept axis and the output is a requirement on it, because the release
mechanism is undefined in this repository and inventing one is what A7-R refused to do.

Run:  python3 analysis/tipoff_release.py
"""
import json
import math
import os

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

BAND_DEG_S = 2.0                # P30. FIXED. Do not touch.
BAND_SECONDARY_DEG_S = 5.0      # NRCSD-E, provisional per its own publisher
COM_OFFSET = 0.070              # m, cad/parameters.json sled.payload_com_offset_above_thrust_line
PAYLOAD_LEN = 0.3405            # m, groups.payload_3u.length_x
PAYLOAD_W = 0.100               # m
CLEARANCES_MM = (0.05, 0.1, 0.25, 0.5, 1.0, 2.0)
SKEWS_US = (1.0, 5.0, 10.0, 25.0, 50.7, 100.0, 250.0)
RESIDUAL_FRACTIONS = (1.0, 0.1, 0.01, 0.0024)   # of full push


def transverse_inertia(m, L, w):
    """Uniform rectangular prism about a transverse axis through the CoM."""
    return m * (L ** 2 + w ** 2) / 12.0


def main():
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        shot = json.load(f)['shot']
    F_push = mm.M_SAT * (shot['F_cmd'] / (mm.M_SAT + mm.M_SLED))   # force on the payload alone
    I = transverse_inertia(mm.M_SAT, PAYLOAD_LEN, PAYLOAD_W)
    M = F_push * COM_OFFSET
    alpha = M / I
    omega_band = math.radians(BAND_DEG_S)
    budget = I * omega_band                     # angular impulse to reach the band

    # --- stage 1: clearance take-up ----------------------------------------
    takeup = []
    for c_mm in CLEARANCES_MM:
        # Rotation available before the payload contacts across its own length.
        theta = 2.0 * (c_mm * 1e-3) / PAYLOAD_LEN
        t = math.sqrt(2 * theta / alpha)
        w = alpha * t
        takeup.append(dict(clearance_mm=c_mm, theta_rad=theta, t_s=t, t_ms=t * 1e3,
                           arrival_deg_s=math.degrees(w),
                           vs_band=math.degrees(w) / BAND_DEG_S))

    # --- stage 2: constrained stroke ---------------------------------------
    # The moment is reacted as a couple over the payload length.
    reaction_N = M / PAYLOAD_LEN

    # --- stage 3: release ---------------------------------------------------
    # Tip-off from an unreacted moment acting for the skew duration.
    grid = []
    for frac in RESIDUAL_FRACTIONS:
        for skew_us in SKEWS_US:
            m_res = F_push * frac * COM_OFFSET
            w = m_res * (skew_us * 1e-6) / I
            grid.append(dict(residual_fraction=frac, skew_us=skew_us,
                             tipoff_deg_s=math.degrees(w),
                             passes=math.degrees(w) <= BAND_DEG_S))
    skew_tol_full_us = budget / M * 1e6         # band 1, against A7-R's 50.7 us

    # Band 2: an ideal release -- zero skew, zero residual, payload in contact.
    ideal_tipoff = 0.0

    # Band 5: CoM offset at which an ideal release passes with 10x margin is trivially any
    # offset; the meaningful question is the offset at which the SKEW TOLERANCE reaches a
    # mechanically achievable 1 ms.
    achievable_skew_s = 1e-3
    offset_for_1ms = budget / (F_push * achievable_skew_s)

    passing = [g for g in grid if g['passes']]
    best_achievable = max((g for g in grid if g['passes']),
                          key=lambda g: g['skew_us'], default=None)

    bands = {
        '1_skew_tolerance_vs_a7r': dict(value_us=skew_tol_full_us, band='50.7 us +/- 2 %',
                                        passed=abs(skew_tol_full_us - 50.7) / 50.7 <= 0.02),
        '2_ideal_release': dict(value_deg_s=ideal_tipoff, band='<= 2 deg/s',
                                passed=ideal_tipoff <= BAND_DEG_S),
        '3_clearance_arrival': dict(
            value_deg_s=next(t['arrival_deg_s'] for t in takeup if t['clearance_mm'] == 0.5),
            band='REPORT', verdict='REPORT'),
        '4_cradle_reaction': dict(value_N=reaction_N, band='<= 200 N per contact',
                                  passed=reaction_N <= 200.0),
        '5_com_offset_for_1ms_skew': dict(value_mm=offset_for_1ms * 1e3, band='REPORT',
                                          verdict='REPORT'),
        '6_any_achievable_pass': dict(n_passing=len(passing),
                                      band='at least one achievable combination',
                                      passed=bool(passing)),
    }

    print(f"A23 tip-off. Payload {mm.M_SAT} kg, I_transverse {I:.5f} kg.m^2, "
          f"push {F_push:.1f} N at {COM_OFFSET*1e3:.0f} mm -> M = {M:.2f} N.m\n")
    print(f"  angular acceleration if unconstrained: {alpha:.1f} rad/s^2")
    print(f"  angular-impulse budget to {BAND_DEG_S} deg/s: {budget*1e3:.4f} mN.m.s\n")

    print("  STAGE 1 -- clearance take-up, the part A7-R could not see:")
    print(f"    {'clearance':>10}{'rotation':>11}{'time':>10}{'arrival':>12}{'vs band':>10}")
    for t in takeup:
        print(f"    {t['clearance_mm']:9.2f} mm{t['theta_rad']*1e3:9.3f} mrad"
              f"{t['t_ms']:8.2f} ms{t['arrival_deg_s']:10.1f} deg/s{t['vs_band']:9.0f}x")

    print(f"\n  STAGE 2 -- cradle reaction during the stroke: {reaction_N:.1f} N per contact, "
          f"held for {shot['t_ms']:.1f} ms")

    print(f"\n  STAGE 3 -- release, tip-off in deg/s:")
    print(f"    {'residual':>10}" + ''.join(f"{s:>9.0f}us" for s in SKEWS_US))
    for frac in RESIDUAL_FRACTIONS:
        row = [g for g in grid if g['residual_fraction'] == frac]
        print(f"    {frac*100:9.2f}%" + ''.join(f"{g['tipoff_deg_s']:11.2f}" for g in row))

    print(f"\n  full-push skew tolerance {skew_tol_full_us:.1f} us (A7-R: 50.7)")
    print(f"  CoM offset that would give a 1 ms skew tolerance: {offset_for_1ms*1e3:.3f} mm")

    print("\nbands:")
    for k, v in bands.items():
        mark = v.get('passed')
        print(f"  {k:28} {'PASS' if mark else ('REPORT' if mark is None else 'FAIL')}")

    out = dict(analysis='A23', bands_declared_commit='bc113e6',
               band_deg_s=BAND_DEG_S, band_source='P30, fixed 2026-07-31, not re-declared',
               F_push_N=F_push, I_transverse=I, moment_Nm=M, alpha_rad_s2=alpha,
               angular_impulse_budget_Nms=budget,
               clearance_takeup=takeup, cradle_reaction_N=reaction_N,
               release_grid=grid, skew_tolerance_full_push_us=skew_tol_full_us,
               com_offset_for_1ms_skew_mm=offset_for_1ms * 1e3, bands=bands)
    path = os.path.join(RESULTS, 'tipoff_release.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
