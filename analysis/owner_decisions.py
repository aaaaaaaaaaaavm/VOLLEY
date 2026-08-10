"""P29 and P9: price both branches of the two decisions analysis cannot make.

WHAT THIS IS FOR
----------------
docs/PHASE_I_CLOSURE.md section 10 lists four decisions that are the owner's, not the model's.
Two of them block the most downstream work, and neither has ever been costed on both sides:

    P29  is the stator segmented, and how much of it is energised at once?
    P9   does the machine target an ESPA-Grande-class port, or a larger host?

This script does not decide either. It computes what each branch costs, so the choice is
between numbers rather than between descriptions. Nothing here is written to the baseline, and
adopting any branch requires an ADR and a controlled propagation pass.

P29: WHY IT MOVES THREE NUMBERS AT ONCE
---------------------------------------
shot() charges copper loss over the whole 1.30 m winding for the entire stroke. A segmented
long-stator machine energises the section under the mover -- roughly the sled's 340 mm active
length -- and switches segments as it passes. Copper loss scales with energised volume, so it
falls with the energised fraction; efficiency rises with it; and P33's phase inductance scales
with energised length, so the drive design moves too.

P9: WHY SHORTENING IS NOT FREE
------------------------------
Exit velocity is sqrt(2*a*s) at fixed commanded force, so cutting the acceleration zone to fit
a 1270 mm class limit costs velocity as the square root -- and velocity is what the product
claim rests on. The lifetime multiplier and the phasing rate both degrade with it, which is
the part a packaging discussion tends to miss.

Run:  python3 analysis/owner_decisions.py
"""
import json
import math
import os

import astro
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# --- P29 -------------------------------------------------------------------------
# Energised length options. SLED_ACTIVE_LEN is the magnet array, i.e. the section actually
# over the mover; ACCEL_ZONE is the whole winding, which is what the model charges today.
SEGMENT_OPTIONS = [
    ('as modelled: whole winding energised', mm.ACCEL_ZONE, 1),
    ('4 segments, one energised', mm.ACCEL_ZONE / 4, 4),
    ('one segment under the mover', mm.SLED_ACTIVE_LEN, None),
]

# --- P9 --------------------------------------------------------------------------
ENVELOPE_NOW = 1.839            # m, cad/parameters.json installed_closed_mm
ESPA_GRANDE = 1.270             # m, class limit
# Everything in the envelope that is not acceleration zone: coast/trim, arrest section,
# enclosure skin, flange. Held fixed when the accel zone is shortened.
OVERHEAD = ENVELOPE_NOW - mm.ACCEL_ZONE


def p29(Kt):
    rows = []
    for label, length, nseg in SEGMENT_OPTIONS:
        s = mm.shot(Kt, energised=length)
        rg = mm.regen_brake(Kt, s['v_exit'], mm.V0 * (1 - s['sag_pct'] / 100))
        net = s['E_drawn'] - rg['E_recovered']
        # P33's inductance scales with energised length.
        L_uH = 19.70 * length / mm.ACCEL_ZONE
        rows.append(dict(
            option=label, energised_m=length, segments=nseg,
            Q_copper_J=s['Q_copper'], E_drawn_J=s['E_drawn'], E_net_J=net,
            eff_net_pct=s['KE_payload'] / net * 100,
            I_peak_A=s['I_peak'], v_exit=s['v_exit'],
            L_phase_uH=L_uH,
            # Deliberately NOT an ESR ceiling. A10 swept that properly and found 65-68 mohm;
            # a closed-form V^2/4P bound evaluated at exit gives a larger, incomparable
            # number, and publishing it beside A10's would read as a contradiction. What can
            # be said is the direction: less power drawn means less peak current, which
            # relaxes the bank requirement. Quantifying it is an A10 re-run, not arithmetic.
            esr_note='lower peak current relaxes P26; requires an A10 re-run to quantify',
        ))
    return rows


def p9(Kt):
    """What fitting a given envelope costs in velocity and in what the velocity buys."""
    rows = []
    a0 = astro.RE + 450e3
    base_life = astro.lifetime(a0, 0.0)
    # (label, envelope to fit, overhead saved by repackaging). The accel zone is whatever is
    # left: envelope - (overhead - saved). Overhead is coast/trim, arrest section, skin and
    # flange, 539 mm as drawn.
    for label, envelope, saved in [
            ('as designed', ENVELOPE_NOW, 0.0),
            ('fit ESPA Grande, as drawn', ESPA_GRANDE, 0.0),
            ('fit ESPA Grande, 150 mm of overhead repackaged', ESPA_GRANDE, 0.150)]:
        accel = envelope - (OVERHEAD - saved)
        if accel <= 0:
            continue
        old = mm.ACCEL_ZONE
        mm.ACCEL_ZONE = accel
        try:
            s = mm.shot(Kt)
        finally:
            mm.ACCEL_ZONE = old
        dv = s['v_exit']
        # What the velocity buys: lifetime multiplier, and days to phase 30 deg.
        a_b, e_b = astro.boosted_elements(450e3, dv)[:2]
        mult = astro.lifetime(a_b, e_b) / base_life
        rows.append(dict(option=label, envelope_m=envelope, overhead_saved_m=saved,
                         accel_zone_m=accel,
                         v_exit=dv, a_g=s['a_g'], t_ms=s['t_ms'],
                         KE_payload_J=s['KE_payload'],
                         lifetime_multiplier=mult,
                         vs_espa_pct=(envelope - ESPA_GRANDE) / ESPA_GRANDE * 100))
    return rows


def main():
    Kt, _ripple = mm.thrust_constant()
    a = p29(Kt)
    b = p9(Kt)

    print("P29 -- how much stator is energised at once\n")
    print(f"  {'option':38}{'copper J':>10}{'net J':>9}{'eff %':>8}"
          f"{'I pk A':>9}{'L uH':>8}")
    for r in a:
        print(f"  {r['option']:38}{r['Q_copper_J']:10.1f}{r['E_net_J']:9.0f}"
              f"{r['eff_net_pct']:8.2f}{r['I_peak_A']:9.0f}{r['L_phase_uH']:8.2f}")
    base = a[0]
    vs = ', '.join('%.3f' % r['v_exit'] for r in a)
    print(f"\n  exit velocity is IDENTICAL across all three: {vs} m/s")
    print("  segmentation changes what the shot COSTS, not what it delivers.")
    for r in a[1:]:
        print(f"    {r['option']:38} copper -{100*(1-r['Q_copper_J']/base['Q_copper_J']):.1f} %,"
              f" efficiency +{r['eff_net_pct']-base['eff_net_pct']:.2f} pts")

    print("\n\nP9 -- what fitting the envelope costs\n")
    print(f"  {'option':40}{'envelope':>10}{'accel':>8}{'v_exit':>9}"
          f"{'a g':>7}{'KE J':>8}{'life x':>8}")
    for r in b:
        print(f"  {r['option']:40}{r['envelope_m']:10.3f}{r['accel_zone_m']:8.3f}"
              f"{r['v_exit']:9.3f}{r['a_g']:7.2f}{r['KE_payload_J']:8.0f}"
              f"{r['lifetime_multiplier']:8.2f}")
    b0 = b[0]
    for r in b[1:]:
        print(f"\n  {r['option']}: v_exit {b0['v_exit']:.3f} -> {r['v_exit']:.3f} m/s "
              f"({100*(r['v_exit']/b0['v_exit']-1):+.1f} %), "
              f"payload KE {b0['KE_payload_J']:.0f} -> {r['KE_payload_J']:.0f} J, "
              f"lifetime x{b0['lifetime_multiplier']:.2f} -> x{r['lifetime_multiplier']:.2f}")

    res = dict(purpose='decision support for P29 and P9; adopts nothing',
               note='no branch is written to the baseline; adoption requires an ADR',
               p29=a, p9=b, espa_grande_m=ESPA_GRANDE, envelope_overhead_m=OVERHEAD)
    path = os.path.join(RESULTS, 'owner_decisions.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
