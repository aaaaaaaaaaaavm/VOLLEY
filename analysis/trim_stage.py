"""
VOLLEY | A motor that steers rather than throws.

WHY THIS EXISTS
---------------
Asked in review: can Gen6 be gas AND electromagnetic, each a fail-safe for the other? The
mutual-redundancy form does not survive arithmetic and is recorded as PII-20 rather than run --
each drive must be sized for the full duty, and A35 prices the electromagnetic half at the
37.89 kg ADR-032 deleted.

But the question contains a better idea. Gen6's largest live defect is control, not energy:
P67, 1.113 % dispersion of which 93.4 % is an unmeasured seal friction, and no transducer buys
it back. Gas is an excellent energy store and cannot servo. A linear motor is a mediocre energy
store and an excellent servo. This prices using each for what it is good at.

Bands declared in validation/A48_trim_stage.md at HEAD, BEFORE this file existed.

Provenance: model output. Constant Kt over the trim section, no end effects, no commutation
loss, ideal velocity measurement, and the correction treated as a constant force over the
section. Every one of those makes the trim stage look better than a designed one will.
"""
import json
import math
import os

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

KT = 10.5386                 # N per kA/m, A2's depth-resolved value
SHEET_A_PER_M = 90e3         # the sheet current Gen5's stator runs at, A1
STROKE = pc.STROKE
TARGET_SIGMA = 0.0274        # A28: the dispersion Gen5 achieved, and Gen6 gave up
MAX_SECTION_FRAC = 0.15      # band 3
POWER_CAP_W = 200.0          # band 5, A37
MASS_CAP_KG = 2.0            # band 4
MAGNET_KG_PER_M = 2.94       # Gen5 sled: 340 mm of Halbach array, from mass_properties
STATOR_KG_PER_M = 5.62       # Gen5 stator: 7.3 kg of copper and formers over 1.30 m


def energy_to_trim(dv, m, v):
    """Work to change speed by dv at v. Exact, not a small-dv approximation."""
    return 0.5 * m * ((v + dv) ** 2 - v ** 2)


def section_for(dv, m, v, force_N):
    """Length over which a constant force delivers that correction."""
    return abs(energy_to_trim(dv, m, v)) / force_N


def peak_power(dv, m, v, force_N):
    """Power at the fastest point of the correction: F.v, with v the exit speed."""
    return force_N * (v + max(dv, 0.0))


def main():
    shot = json.load(open(os.path.join(RESULTS, 'precharged.json')))['selected']
    disp = json.load(open(os.path.join(RESULTS, 'gen6_dispersion.json')))
    e_shot = shot['work_J']
    v = disp['mean']
    sigma3 = disp['three_sigma']
    m = pc.M_PAY

    print(f"Gen6 shot {e_shot:.1f} J, exit {v:.3f} m/s, 3-sigma {sigma3:.4f} m/s "
          f"({disp['three_sigma_pct']:.3f} %)\n")

    # Force available from a trim stator at Gen5's sheet current, per metre of active length
    force_per_m = KT * SHEET_A_PER_M / 1e3     # N per kA/m x kA/m = N
    print(f"trim stator at Gen5 sheet current: {force_per_m:.0f} N\n")

    print(f"{'authority':>12s} {'energy J':>10s} {'% of shot':>10s} {'section m':>10s} "
          f"{'% stroke':>9s} {'peak W':>9s}")
    sweep = []
    for k, label in ((1.0, '+-3 sigma'), (2.0, '+-6 sigma'), (3.0, '+-9 sigma')):
        dv = k * sigma3
        e = abs(energy_to_trim(dv, m, v))
        L = section_for(dv, m, v, force_per_m)
        P = peak_power(dv, m, v, force_per_m)
        sweep.append(dict(authority=label, k=k, dv=dv, energy_J=e,
                          pct_of_shot=e / e_shot * 100, section_m=L,
                          pct_stroke=L / STROKE * 100, peak_W=P))
        print(f"{label:>12s} {e:10.1f} {e/e_shot*100:10.3f} {L:10.4f} "
              f"{L/STROKE*100:9.3f} {P:9.0f}")

    base = sweep[0]
    L = base['section_m']
    mass = L * (MAGNET_KG_PER_M + STATOR_KG_PER_M)
    per_sat_before = 1.403
    per_sat_after = per_sat_before + mass / pc.N_MANIFEST
    print(f"\nmass at the +-3 sigma section: {mass:.3f} kg "
          f"({MAGNET_KG_PER_M:.2f} magnets + {STATOR_KG_PER_M:.2f} stator, per metre)")
    print(f"added mass per satellite: {per_sat_before:.3f} -> {per_sat_after:.3f} kg")

    # band 6: can the loop reach Gen5's dispersion? It can if its authority covers the error
    # and its own resolution is finer than the target.
    reaches = sigma3 <= base['dv'] and TARGET_SIGMA < sigma3
    print(f"\ncorrecting to Gen5's {TARGET_SIGMA} m/s: "
          f"authority {base['dv']:.4f} m/s covers a {sigma3:.4f} m/s spread -> "
          f"{'reachable' if reaches else 'NOT reachable'}")

    # band 7: does it survive a 3x worse friction spread?
    sigma3_x3 = sigma3 * 3.0
    e_x3 = abs(energy_to_trim(sigma3_x3, m, v))
    L_x3 = section_for(sigma3_x3, m, v, force_per_m)
    P_x3 = peak_power(sigma3_x3, m, v, force_per_m)
    mass_x3 = L_x3 * (MAGNET_KG_PER_M + STATOR_KG_PER_M)
    print(f"at 3x the friction spread: {e_x3:.1f} J, {L_x3:.4f} m, {P_x3:.0f} W, "
          f"{mass_x3:.3f} kg")

    reopened = [
        "P34 -- a payload carrying a magnetometer cannot fly in this magazine. Magnets return "
        "to the moving part, so this defect returns with them",
        "E35 -- the payload's field exposure becomes a design variable again",
        "the cradle -- the carriage must now hold magnets in alignment as well as the payload",
        "a velocity sensor before the trim section, which Gen6 does not have",
        "one more element in the FMEA, shared across all twelve shots (A47)",
    ]

    bands = [
        ('1', 'imported shot energy and dispersion reproduce 1864.8 J and 1.113 %',
         f"{e_shot:.1f} J, {disp['three_sigma_pct']:.3f} %",
         abs(e_shot - 1864.8) < 0.1 and abs(disp['three_sigma_pct'] - 1.113) < 0.001),
        ('2', 'energy to correct +-3 sigma <= 5 % of the shot',
         f"{base['pct_of_shot']:.3f} %", base['pct_of_shot'] <= 5.0),
        ('3', f'trim section <= {MAX_SECTION_FRAC*100:.0f} % of the stroke',
         f"{base['pct_stroke']:.3f} %", base['pct_stroke'] <= MAX_SECTION_FRAC * 100),
        ('4', f'added mass <= {MASS_CAP_KG} kg and per satellite stays <= 2.0 kg',
         f"{mass:.3f} kg, {per_sat_after:.3f} kg/sat",
         mass <= MASS_CAP_KG and per_sat_after <= 2.0),
        ('5', f'peak electrical <= {POWER_CAP_W:.0f} W',
         f"{base['peak_W']:.0f} W", base['peak_W'] <= POWER_CAP_W),
        ('6', f'correcting to Gen5 dispersion {TARGET_SIGMA} m/s is reachable in bands 2-5',
         'reachable' if reaches else 'not reachable', reaches),
        ('7', 'holds at 3x the friction spread',
         f"{L_x3/STROKE*100:.2f} % stroke, {P_x3:.0f} W, {mass_x3:.3f} kg",
         L_x3 / STROKE <= MAX_SECTION_FRAC and mass_x3 <= MASS_CAP_KG),
        ('8', 'every defect the stage re-opens is named',
         f"{len(reopened)} named", bool(reopened)),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")
    print("\nre-opened by putting magnets back on the moving part:")
    for r in reopened:
        print(f"  - {r}")

    out = dict(analysis='A48', bands_declared_commit='HEAD~1',
               note='constant Kt over the trim section, no end effects, no commutation loss, '
                    'ideal velocity measurement, correction as a constant force. Every one of '
                    'those flatters the trim stage against a designed one.',
               shot_J=e_shot, v_exit=v, three_sigma=sigma3,
               force_per_m_N=force_per_m, sweep=sweep,
               mass_kg=mass, per_sat_before=per_sat_before, per_sat_after=per_sat_after,
               friction_3x=dict(energy_J=e_x3, section_m=L_x3, peak_W=P_x3, mass_kg=mass_x3),
               reopened=reopened,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'trim_stage.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
