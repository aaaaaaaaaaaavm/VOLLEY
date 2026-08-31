"""A74: what the drive tube has to become, stated as a requirement rather than a material.

A66 priced the attenuation, A72 integrated the drag and found ADR-033's carriage-borne secondary
and ADR-035's aluminium wall mutually exclusive. Two of P92's three candidate fixes are already
gone -- a section local to the stator does nothing about a brake that acts over the whole stroke.
This file takes the third and inverts the question.

WHY A REQUIREMENT AND NOT A SCREEN
----------------------------------
Screening materials means importing a conductivity and a density per candidate, and this
repository owns exactly one of each. Six more would be six handbook numbers carried at face value
into a conclusion, and E11 already records public material screening as its own open item. So this
computes what the tube must satisfy, from models the repository already has, and leaves the search
to E11 and E3. NO NEW MATERIAL DATA ENTERS THIS FILE.

Everything numerical is imported. `tube_shielding` owns the drag ratio and the transmission;
`array_drag` owns bands 3R and 4R and the shot integration. Band 1 checks the import by identity
against A72's committed result, which is the only honest meaning of verification here: this file
is not a second method and does not claim to be.

Bands declared in validation/A74_tube_conductance_requirement.md before this file existed.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, 'results')
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import tube_shielding as ts                          # noqa: E402
import array_drag as ad                              # noqa: E402

SIGMA_AL = ts.SIGMA_AL
WALL_M = ts.WALL_M
SD_AL = SIGMA_AL * WALL_M                            # 35 000 S
K_WAVE = ts.k_wave()                                 # 130.9 m^-1
BORE_R_M = ts.BORE_M / 2.0
FIELDS = ad.FIELDS

# A59: the hoop stress at 17.96 MPa against 250 allowable means 0.16 mm of wall holds the gas.
# The 1.0 mm as drawn is set by handling and by A38's 201.7 N cradle preload, per the docstring
# in cad/build_gen6.py. 0.16 mm is therefore the floor thinning could reach on pressure alone,
# and it is already below what the part is drawn for.
WALL_PRESSURE_FLOOR_M = 0.16e-3
STEEL_PENALTY_KG = 2.154                             # A59 band 9, A63, ADR-035
N_MANIFEST = 12

A66 = json.load(open(os.path.join(RESULTS, 'tube_shielding.json')))
A72 = json.load(open(os.path.join(RESULTS, 'array_drag.json')))
A73 = json.load(open(os.path.join(RESULTS, 'trim_secondary.json')))


def band1_verification():
    """Identity against A66's and A72's committed results, not a second opinion.

    This file imports A72's own functions. Re-deriving them here and calling the agreement a
    cross-check would be two wrappers around one expression, which A66 band 1R was written to
    forbid. What CAN be checked is that the import is live: that calling those functions now
    reproduces the numbers `array_drag.json` publishes.
    """
    breakeven = ts.breakeven_b_net()
    worst = min(A72['ladder'], key=lambda r: r['force_over_parity'])
    lf = ad.length_for_force(worst['b_gap_T'])
    lp = ad.length_for_parity(worst['b_gap_T'])
    out = {
        'breakeven_now_T': breakeven,
        'breakeven_published_T': A66['breakeven_b_net_T'],
        'breakeven_rel': abs(breakeven - A66['breakeven_b_net_T']) / A66['breakeven_b_net_T'],
        'ratio_now': lf / lp,
        'ratio_published': worst['force_over_parity'],
        'ratio_rel': abs(lf / lp - worst['force_over_parity']) / worst['force_over_parity'],
        'at_field_T': worst['b_gap_T'],
    }
    out['pass_'] = out['breakeven_rel'] <= 1e-9 and out['ratio_rel'] <= 1e-9
    return out


def max_conductance_for(field_T, which, lo=1.0, hi=SD_AL, n_scan=40):
    """The largest sheet conductance at which A72's band passes at this field.

    `which` is 'parity' or 'stall'. Both lengths grow as the wall gets less conducting while
    L_force does not move at all, so the margin is monotone in sigma*d over this range and a
    plain bisection is safe -- unlike the array-length search inside A72, where it was not.
    """
    target = ad.length_for_force(field_T)

    def margin(sd):
        f = ad.length_for_parity if which == 'parity' else ad.length_for_stall
        got = f(field_T, sigma=sd / WALL_M, d=WALL_M)
        return (4.0 if got is None else got) - target      # positive = the band passes

    if margin(hi) > 0.0:
        return {'sigma_d_S': None, 'note': 'aluminium already passes at this field'}
    if margin(lo) <= 0.0:
        return {'sigma_d_S': None, 'note': 'no conductance in the search range passes'}
    sd = ad._bisect(margin, lo, hi, tol=1e-4)
    return {'sigma_d_S': sd, 'fraction_of_aluminium': sd / SD_AL,
            'sigma_S_m_at_1mm': sd / WALL_M,
            'aluminium_wall_that_would_give_it_m': sd / SIGMA_AL}


def liner_for_unit_ratio(field_T):
    """Liner thickness that brings A66's drag-to-thrust ratio to one, and what it costs.

    A liner lines the bore, so the magnets shrink to fit and their surface moves `t` further from
    BOTH the wall and the winding outside it. The field at each falls as exp(-k t), and the ratio
    carries one power of it, not two -- the drag falls as B_net^2 and the thrust as B_net, and the
    ratio is their quotient. So t = ln(ratio) / k.
    """
    b_net = field_T * abs(ts.transmission_slab()[0])
    ratio = ts.drag_over_thrust(b_net)
    if ratio <= 1.0:
        return {'field_T': field_T, 'ratio': ratio, 'liner_m': 0.0, 'fits_bore': True,
                'magnet_radius_left_m': ts.GAP_RADIUS_M}
    t = math.log(ratio) / K_WAVE
    return {'field_T': field_T, 'ratio': ratio, 'liner_m': t,
            'fits_bore': t < BORE_R_M,
            'bore_radius_m': BORE_R_M,
            'magnet_radius_left_m': (ts.BORE_M / 2.0 - 0.1e-3) - t}


def build():
    b1 = band1_verification()

    requirement = []
    for b in FIELDS:
        requirement.append({'b_gap_T': b,
                            'parity': max_conductance_for(b, 'parity'),
                            'stall': max_conductance_for(b, 'stall')})

    liners = [liner_for_unit_ratio(b) for b in FIELDS]
    liner_all = all(l['fits_bore'] for l in liners)
    liner_any = any(l['fits_bore'] for l in liners)

    # band 4: can thinning aluminium alone meet the requirement, at a thickness A59 admits
    strictest = [r['parity']['sigma_d_S'] for r in requirement if r['parity']['sigma_d_S']]
    sd_needed = min(strictest) if strictest else None
    wall_needed = sd_needed / SIGMA_AL if sd_needed else None
    thinning_ok = bool(wall_needed is not None and wall_needed >= WALL_PRESSURE_FLOOR_M)

    per_sat_now = A73['best']['per_satellite_at_section_kg']
    per_sat_steel = per_sat_now + STEEL_PENALTY_KG / N_MANIFEST

    bands = [
        {'band': '1', 'name': 'verification: the imported model reproduces A72 committed result',
         'detail': f"break-even {b1['breakeven_rel']:.1e}, worst ratio {b1['ratio_rel']:.1e}, "
                   f"both against 1e-9",
         'pass_': b1['pass_']},
        {'band': '2', 'name': 'REPORT: the largest sheet conductance at which A72 3R and 4R pass',
         'detail': '; '.join(
             f"{r['b_gap_T']:.2f} T parity "
             + ('none' if r['parity']['sigma_d_S'] is None
                else f"{r['parity']['sigma_d_S']:.1f} S")
             + ', stall '
             + ('none' if r['stall']['sigma_d_S'] is None
                else f"{r['stall']['sigma_d_S']:.1f} S")
             for r in requirement),
         'pass_': None},
        {'band': '3', 'name': 'a non-conducting liner brings the drag-to-thrust ratio to one '
                              'within the bore',
         'detail': f"needs {min(l['liner_m'] for l in liners)*1e3:.2f} to "
                   f"{max(l['liner_m'] for l in liners)*1e3:.2f} mm across the ladder against a "
                   f"{BORE_R_M*1e3:.4f} mm bore radius; fits at "
                   f"{sum(1 for l in liners if l['fits_bore'])} of {len(liners)} fields",
         'pass_': liner_all},
        {'band': '4', 'name': 'thinning the aluminium wall alone meets the requirement at a '
                              'thickness A59 admits',
         'detail': (f"needs {wall_needed*1e6:.1f} um against a {WALL_PRESSURE_FLOOR_M*1e6:.0f} um "
                    f"pressure floor and a 1000 um wall as drawn"
                    if wall_needed else "no conductance in range passes at any field"),
         'pass_': thinning_ok},
        {'band': '5', 'name': 'REPORT: the mass of the one lower-conductivity metal already priced',
         'detail': f"steel is +{STEEL_PENALTY_KG:.3f} kg on a shared tube, "
                   f"+{STEEL_PENALTY_KG/N_MANIFEST:.4f} kg per satellite, taking A73's "
                   f"{per_sat_now:.4f} kg to {per_sat_steel:.4f} kg against a 2.0 kg ceiling",
         'pass_': None},
    ]

    return {
        'analysis': 'A74',
        'bands_declared_commit': 'c4611a5, before this file existed',
        'note': ('The tube conductance requirement, inverted from A66 and A72 rather than screened '
                 'against a material table. No new material data. E4: nothing measured.'),
        'inputs': {'sigma_d_aluminium_S': SD_AL, 'wall_m': WALL_M, 'k_wave_per_m': K_WAVE,
                   'bore_radius_m': BORE_R_M,
                   'wall_pressure_floor_m': WALL_PRESSURE_FLOOR_M,
                   'steel_penalty_kg': STEEL_PENALTY_KG,
                   'per_satellite_now_kg': per_sat_now},
        'verification': b1,
        'requirement': requirement,
        'liner': {'per_field': liners, 'fits_at_every_field': liner_all,
                  'fits_at_some_field': liner_any},
        'thinning': {'sigma_d_needed_S': sd_needed, 'wall_needed_m': wall_needed,
                     'pressure_floor_m': WALL_PRESSURE_FLOOR_M,
                     'factor_below_floor': (WALL_PRESSURE_FLOOR_M / wall_needed
                                            if wall_needed else None)},
        'steel': {'penalty_kg': STEEL_PENALTY_KG,
                  'per_satellite_kg': per_sat_steel,
                  'within_2kg': bool(per_sat_steel <= 2.0)},
        'bands': bands,
    }


def main():
    r = build()
    print(f"A74 tube conductance requirement, aluminium at 1.0 mm is "
          f"{r['inputs']['sigma_d_aluminium_S']:.0f} S")
    b1 = r['verification']
    print(f"  verification against A72 committed result: break-even {b1['breakeven_rel']:.1e}, "
          f"worst ratio {b1['ratio_rel']:.1e}")
    print("\n  field    band 3R needs           band 4R needs          as an aluminium wall")
    for row in r['requirement']:
        p = row['parity']['sigma_d_S']
        s = row['stall']['sigma_d_S']
        wall = f"{row['parity']['aluminium_wall_that_would_give_it_m']*1e6:.1f} um" if p else "-"
        print(f"  {row['b_gap_T']:5.2f} T  "
              + (f"{p:9.1f} S ({p/r['inputs']['sigma_d_aluminium_S']*100:5.3f} %)" if p
                 else "     none            ")
              + "   "
              + (f"{s:9.1f} S ({s/r['inputs']['sigma_d_aluminium_S']*100:5.3f} %)" if s
                 else "     none            ")
              + f"   {wall}")
    print("\n  field    liner for ratio = 1    fits the bore")
    for l in r['liner']['per_field']:
        print(f"  {l['field_T']:5.2f} T  ratio {l['ratio']:5.2f}, needs "
              f"{l['liner_m']*1e3:6.2f} mm   {'yes' if l['fits_bore'] else 'NO'}")
    t = r['thinning']
    if t['wall_needed_m']:
        print(f"\n  thinning aluminium: {t['wall_needed_m']*1e6:.1f} um needed against a "
              f"{t['pressure_floor_m']*1e6:.0f} um pressure floor, "
              f"{t['factor_below_floor']:.1f}x below it")
    print("\nbands:")
    for b in r['bands']:
        v = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}: {v}  {b['name']}\n            {b['detail']}")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(r, open(os.path.join(RESULTS, 'tube_requirement.json'), 'w'), indent=2)
    print("\n-> results/tube_requirement.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
