"""A21: VOLLEY against the alternatives, on identical axes.

Bands declared in validation/A21_comparators.md at 881c260, before this file existed.

WHY
---
The repository compares VOLLEY to alternatives in SUMMARY.md, LANDSCAPE.md and MARKET.md, each
on different axes with a different headline, and none of them computes the comparison. Two
specific defects motivated this:

  1. The headline everywhere is "6.6x the fastest published spring", a ratio of VELOCITIES.
     Nobody buys velocity. What a customer gets is orbital lifetime and phase separation, and
     lifetime extension is SUPERLINEAR in delta-v in this regime -- so the velocity ratio
     understates the machine.

  2. Superiority over orbital transfer vehicles on cost has been asserted informally. There is
     no OTV price anywhere in this repository and no vendor quotation on any line of cost.py.
     Band 7 requires every cost comparison to return NOT COMPUTED so the gap is recorded in the
     output rather than merely left unasked.

Losses are computed and reported on the same footing as wins. At 3U the cold-gas module beats
VOLLEY on mass by roughly 8x, and a spring beats it on maturity by TRL 9 against 2-3.

COMPARATOR FIGURES ARE CLASS FIGURES, NOT QUOTATIONS, AND NAME NO MANUFACTURER.

Run:  python3 analysis/comparators.py
"""
import json
import math
import os

import astro
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

ALT_M = 450e3
INC_DEG = 51.6

# Class figures, already used in docs/KILL_CRITERIA.md. No manufacturer is named.
SPRING_DV_LOW, SPRING_DV_TYP, SPRING_DV_FAST = 1.0, 2.0, 2.5   # m/s
DISPENSER_KG_PER_U = 2.0        # canisterised class figure
COLDGAS_KG_LOW, COLDGAS_KG_HIGH = 0.5, 1.2
DRAG_DAYS_30DEG = 25.0          # astro.py model output, NOT the flown result -- see E16
PHASE_TARGET_DEG = 30.0
G_CAP = 25.0                    # g, the payload qualification ceiling


def lifetime_multiplier(dv):
    """Orbital lifetime at dv, relative to unboosted. Imported physics, not restated."""
    base = astro.lifetime(astro.RE + ALT_M, 0.0)
    a, e = astro.boosted_elements(ALT_M, dv)[:2]
    return astro.lifetime(a, e) / base


def days_to_phase(dv_differential, target_deg=PHASE_TARGET_DEG):
    """Days for two satellites separated by dv_differential to drift target_deg apart.

    A along-track velocity difference changes the semi-major axis and hence the period; the
    phase difference accumulates as the period difference integrates.
    """
    r = astro.RE + ALT_M
    a0 = r
    a1 = astro.boosted_elements(ALT_M, dv_differential)[0]
    n0 = math.sqrt(astro.MU / a0 ** 3)
    n1 = math.sqrt(astro.MU / a1 ** 3)
    dn = abs(n0 - n1)
    if dn == 0:
        return float('inf')
    return math.radians(target_deg) / dn / 86400.0


def main():
    global V_G_CAP
    V_G_CAP = math.sqrt(2 * G_CAP * 9.81 * mm.ACCEL_ZONE)
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        motor = json.load(f)
    dv_volley = motor['shot']['v_exit']
    with open(os.path.join(RESULTS, 'payload_family.json'), encoding='utf-8') as f:
        fam = json.load(f)
    kg_per_sat = next(c['kg_per_satellite'] for c in fam['classes']
                      if c['tag'] == '3U CubeSat')

    mult = {k: lifetime_multiplier(v) for k, v in
            (('spring_low', SPRING_DV_LOW), ('spring_typ', SPRING_DV_TYP),
             ('spring_fast', SPRING_DV_FAST), ('volley', dv_volley))}
    ext = {k: v - 1.0 for k, v in mult.items()}          # extension over unboosted

    ratio_fast = ext['volley'] / ext['spring_fast']
    ratio_typ = ext['volley'] / ext['spring_typ']

    # A spring's DESIGNED differential is zero: every satellite gets the same nominal push.
    # Any spread is manufacturing scatter, which cannot be commanded or predicted per unit.
    spring_differential = 0.0
    volley_differential = dv_volley

    rows = [
        dict(option='Spring deployer (canisterised class)',
             dv_m_s=SPRING_DV_FAST, lifetime_multiplier=mult['spring_fast'],
             designed_differential_m_s=spring_differential,
             days_to_30deg=None, deployer_kg_per_3U=DISPENSER_KG_PER_U * 3,
             satellite_carries='nothing', host_provides='one deploy signal',
             schedulable=True, maturity='TRL 9, thousands deployed'),
        dict(option='VOLLEY',
             dv_m_s=dv_volley, lifetime_multiplier=mult['volley'],
             designed_differential_m_s=volley_differential,
             days_to_30deg=days_to_phase(10.0), deployer_kg_per_3U=kg_per_sat,
             satellite_carries='nothing', host_provides='150-300 W, serial link, firing window',
             schedulable=True, maturity='TRL 2-3, nothing measured'),
        dict(option='Differential drag',
             dv_m_s=0.0, lifetime_multiplier=1.0,
             designed_differential_m_s=0.0,
             days_to_30deg=DRAG_DAYS_30DEG, deployer_kg_per_3U=0.0,
             satellite_carries='nothing, but needs attitude authority to modulate area',
             host_provides='nothing', schedulable=False,
             maturity='flown on a 12-satellite constellation'),
        dict(option='Cold-gas module (carried by the satellite)',
             dv_m_s=dv_volley, lifetime_multiplier=mult['volley'],
             designed_differential_m_s=dv_volley,
             days_to_30deg=days_to_phase(10.0),
             deployer_kg_per_3U=(COLDGAS_KG_LOW + COLDGAS_KG_HIGH) / 2,
             satellite_carries='0.5-1.2 kg, pressure vessel, qualification, range safety',
             host_provides='nothing', schedulable=True, maturity='COTS, flown'),
    ]

    coldgas_mid = (COLDGAS_KG_LOW + COLDGAS_KG_HIGH) / 2
    coldgas_ratio = kg_per_sat / coldgas_mid
    mass_ratio_vs_dispenser = kg_per_sat / (DISPENSER_KG_PER_U * 3)
    drag_ratio = DRAG_DAYS_30DEG / days_to_phase(10.0)

    bands = {
        '1_lifetime_ratio_vs_fastest_spring': dict(
            value=ratio_fast, band='>= 5x', passed=ratio_fast >= 5.0),
        '2_lifetime_multiplier_vs_astro': dict(
            value=mult['volley'], band='1.62 +/- 0.02',
            passed=abs(mult['volley'] - 1.62) <= 0.02),
        '3_spring_designed_differential': dict(
            value=spring_differential, band='exactly 0',
            passed=spring_differential == 0.0),
        '4_mass_parity_vs_dispenser': dict(
            value=mass_ratio_vs_dispenser, band='within +/-25 %',
            passed=abs(mass_ratio_vs_dispenser - 1.0) <= 0.25),
        '5_coldgas_loss_at_3U': dict(
            value=coldgas_ratio, band='VOLLEY loses by >= 5x',
            passed=coldgas_ratio >= 5.0),
        '6_phase_vs_drag': dict(
            value=drag_ratio, band='>= 10x faster', passed=drag_ratio >= 10.0),
        '7_cost_comparison': dict(
            value='NOT COMPUTED', band='must return NOT COMPUTED',
            reason='no vendor quotation for VOLLEY (cost.py), no price for any alternative; '
                   'closing this needs E3, not another analysis',
            passed=True),
    }

    print("A21 comparators. All figures are class figures; no manufacturer is named.\n")
    print("  lifetime extension over unboosted, at 450 km:")
    for k in ('spring_low', 'spring_typ', 'spring_fast', 'volley'):
        dv = {'spring_low': SPRING_DV_LOW, 'spring_typ': SPRING_DV_TYP,
              'spring_fast': SPRING_DV_FAST, 'volley': dv_volley}[k]
        print(f"    {k:12} {dv:7.3f} m/s  x{mult[k]:.4f}  = {ext[k]*100:+6.2f} %")
    print(f"\n  VOLLEY / fastest spring = {ratio_fast:.2f}x   "
          f"VOLLEY / typical spring = {ratio_typ:.2f}x")
    print(f"  (velocity ratio for comparison: {dv_volley/SPRING_DV_FAST:.2f}x)")

    print(f"\n  30 deg of phase: VOLLEY {days_to_phase(10.0):.2f} d at 10 m/s differential, "
          f"drag {DRAG_DAYS_30DEG:.0f} d  -> {drag_ratio:.1f}x")
    print(f"  mass per 3U satellite: VOLLEY {kg_per_sat:.3f} kg, dispenser class "
          f"{DISPENSER_KG_PER_U*3:.1f} kg -> ratio {mass_ratio_vs_dispenser:.3f}")
    print(f"  cold gas at 3U: VOLLEY loses by {coldgas_ratio:.1f}x  (declared as a loss)")

    print("\nbands:")
    for k, v in bands.items():
        print(f"  {k:36} {'PASS' if v['passed'] else 'FAIL'}")

    # REPORT, not a band. docs/REVIEW_RESPONSES.md used to paste this table by hand, so it
    # kept the operating point it was written at while astro.py moved underneath it. A table
    # that is read off a result cannot do that.
    superlinearity = []
    for dv, label in ((SPRING_DV_TYP, 'spring, typical'),
                      (SPRING_DV_FAST, 'spring, fastest published'),
                      (dv_volley, 'VOLLEY, rated shot'),
                      (V_G_CAP, 'the 25 g payload cap')):
        gain = (lifetime_multiplier(dv) - 1.0) * 100.0
        superlinearity.append(dict(dv_m_s=dv, label=label, lifetime_gain_pct=gain,
                                   gain_per_m_s=gain / dv))
    apogee_km = (astro.boosted_elements(ALT_M, dv_volley)[0]
                 * (1 + astro.boosted_elements(ALT_M, dv_volley)[1]) - astro.RE) / 1e3
    print("\nlifetime gain is superlinear in dv:")
    for r in superlinearity:
        print(f"  {r['dv_m_s']:6.3f} m/s  {r['lifetime_gain_pct']:7.1f} %  "
              f"{r['gain_per_m_s']:5.2f} %/m/s   {r['label']}")
    print(f"  one shot raises apogee to {apogee_km:.1f} km")

    out = dict(analysis='A21', bands_declared_commit='881c260',
               superlinearity=superlinearity, apogee_after_shot_km=apogee_km,
               note='class figures only; no manufacturer named; no cost comparison computed',
               lifetime_multipliers=mult, lifetime_extensions=ext,
               ratio_vs_fastest_spring=ratio_fast, ratio_vs_typical_spring=ratio_typ,
               velocity_ratio=dv_volley / SPRING_DV_FAST,
               days_to_30deg_volley=days_to_phase(10.0), days_to_30deg_drag=DRAG_DAYS_30DEG,
               kg_per_3U_volley=kg_per_sat, kg_per_3U_dispenser=DISPENSER_KG_PER_U * 3,
               coldgas_loss_ratio=coldgas_ratio, rows=rows, bands=bands)
    path = os.path.join(RESULTS, 'comparators.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
