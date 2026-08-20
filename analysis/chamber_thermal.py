"""A58: the chamber, the tube and the seal across a campaign.

Bands declared in validation/A58_chamber_thermal.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
Nothing in this repository models the chamber thermally. A43 settled the RESERVOIR between shots
and says so. A39 states it designs "no cylinder, valve, seal or latch"; A40 that it does not model
"temperature drop in the chamber".

ADR-034 made both halves of it worse and neither was checked.

TWO OPPOSING EFFECTS, ONE COMPONENT
-----------------------------------
    expansion cools    -22.4 K at 2.18 m  ->  -62.1 K at 8.0 m, taking the gas to -35 C
    friction heats     181.8 J per shot   ->   667.2 J, at 2419 W where the seal is fastest

Both land on the seal -- which owns 98.7 % of the dispersion (A55), is the whole justification for
ADR-033, and has never been measured, specified or given a material. P67 is not a room-temperature
friction measurement.

And P85 sits in the middle: the tube's material is stated nowhere, and the choice is worth about
11 um of clearance across the swing.

DECLARED HANDBOOK VALUES
------------------------
Named at each use, none measured, none vendor-sourced -- the standing A39 gave its gas model. The
seal mass is SWEPT because no seal exists in any file.

Run:  python3 analysis/chamber_thermal.py
"""
import json
import math
import os

import precharged as pc
import gen6_dispersion as gd
import fill_window as fw

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_CHAMBER = 2.0e-3
CADENCE_S = fw.CADENCE_S
N_SHOTS = fw.N_MANIFEST

MATERIALS = {'steel': dict(cp=460.0, alpha=12e-6, tube_kg=3.294),
             'aluminium': dict(cp=900.0, alpha=23e-6, tube_kg=1.1404)}
CHAMBER_KG, CHAMBER_CP = fw.CHAMBER_KG, 460.0        # chamber is steel: precharged::chamber_kg
SEAL_CP = 1500.0
SEAL_MASS_SWEEP = (0.5e-3, 1e-3, 2e-3, 5e-3, 10e-3)
HEAT_OUT_FRAC = (0.0, 0.5, 0.9, 0.99, 0.999)
T_COND_N2_AT_END = 103.0                              # nitrogen at ~10 bar
K_STEEL = 45.0                                        # W/m.K, for the chamber-to-structure path


def gas_state():
    """The expansion, from the design point the parameter file carries."""
    p0, L, g = pc.P_MAX, pc.STROKE, pc.GAMMA
    r = V_CHAMBER / (V_CHAMBER + pc.AREA * L)
    t_end = pc.T0 * r ** (g - 1.0)
    return dict(p0_bar=p0 / 1e5, stroke_m=L, ratio=r,
                t_start_K=pc.T0, t_end_K=t_end, drop_K=pc.T0 - t_end,
                p_end_bar=p0 * r ** g / 1e5,
                mass_kg=p0 * V_CHAMBER / (pc.R_GAS * pc.T0),
                work_J=pc.work(p0, V_CHAMBER, L))


def friction():
    w = gd.FRICTION_N * pc.STROKE
    v = math.sqrt(2.0 * (pc.work(pc.P_MAX, V_CHAMBER, pc.STROKE) - w) / pc.M_PAY)
    return dict(force_N=gd.FRICTION_N, work_J=w, campaign_J=w * N_SHOTS,
                v_exit=v, peak_W=gd.FRICTION_N * v)


def chamber_swing(gas):
    """Wall swing if the residual gas equilibrates with the chamber before venting.

    Upper bound: all of the gas's remaining sensible deficit is taken from the wall, none from
    the structure. The wall then recovers by conduction across the cadence.
    """
    cv = pc.R_GAS / (pc.GAMMA - 1.0)
    q = gas['mass_kg'] * cv * (pc.T0 - gas['t_end_K'])     # J the cold gas can absorb
    swing = q / (CHAMBER_KG * CHAMBER_CP)
    # recovery: lumped conduction through the mount into structure at T0
    r = (3.0 * V_CHAMBER / (4.0 * math.pi)) ** (1.0 / 3.0)
    area = 4.0 * math.pi * r * r
    ua = K_STEEL * area / (2.0 * r)                        # a wall-thickness-scale path
    tau = CHAMBER_KG * CHAMBER_CP / ua
    return dict(q_J=q, swing_K=swing, tau_s=tau,
                residual_K=swing * math.exp(-CADENCE_S / tau))


def seal_rise(work_J, mass_kg, out_frac):
    return work_J * (1.0 - out_frac) / (mass_kg * SEAL_CP)


def main():
    gas, fric = gas_state(), friction()
    print(f"A58 chamber thermal. {gas['stroke_m']:.1f} m at {gas['p0_bar']:.4f} bar\n")
    print(f"  expansion: {gas['t_start_K']:.0f} -> {gas['t_end_K']:.1f} K "
          f"({gas['t_end_K']-273.15:+.1f} C), drop {gas['drop_K']:.1f} K, "
          f"p {gas['p0_bar']:.2f} -> {gas['p_end_bar']:.2f} bar")
    print(f"  against nitrogen condensing at ~{T_COND_N2_AT_END:.0f} K: "
          f"{gas['t_end_K']-T_COND_N2_AT_END:.1f} K of margin\n")
    print(f"  friction: {fric['force_N']:.1f} N x {gas['stroke_m']:.1f} m = "
          f"{fric['work_J']:.1f} J/shot, {fric['campaign_J']:.0f} J over {N_SHOTS}, "
          f"peak {fric['peak_W']:.0f} W\n")

    tubes = {}
    for name, m in MATERIALS.items():
        rise = fric['campaign_J'] / (m['tube_kg'] * m['cp'])
        tubes[name] = dict(tube_kg=m['tube_kg'], cp=m['cp'], campaign_rise_K=rise,
                           per_shot_K=rise / N_SHOTS)
        print(f"  tube, {name:10s} {m['tube_kg']:6.3f} kg -> "
              f"{rise:5.2f} K over the campaign, {rise/N_SHOTS:4.2f} K per shot")

    ch = chamber_swing(gas)
    print(f"\n  chamber: {CHAMBER_KG:.4f} kg absorbs {ch['q_J']:.0f} J -> "
          f"{ch['swing_K']:.2f} K swing, tau {ch['tau_s']:.0f} s, "
          f"{ch['residual_K']:.4f} K left after {CADENCE_S:.0f} s")

    print(f"\n  differential clearance across a {gas['drop_K']:.1f} K swing on a "
          f"{pc.BORE*1e3:.3f} mm bore:")
    pairs = {}
    for a in MATERIALS:
        for b in MATERIALS:
            d = pc.BORE * abs(MATERIALS[a]['alpha'] - MATERIALS[b]['alpha']) * gas['drop_K']
            pairs[f'{a}_piston_in_{b}_bore'] = d * 1e6
            print(f"    {a:10s} piston in {b:10s} bore: {d*1e6:6.2f} um")
    matched = max(v for k, v in pairs.items() if k.split('_')[0] == k.split('_')[3])
    dissimilar = max(pairs.values())

    print(f"\nband 8, seal temperature rise per shot (K):")
    print(f"  {'seal g':>8}" + ''.join(f"{f'{f*100:.1f}% out':>12}" for f in HEAT_OUT_FRAC))
    seal_rows = []
    for m in SEAL_MASS_SWEEP:
        rises = [seal_rise(fric['work_J'], m, f) for f in HEAT_OUT_FRAC]
        seal_rows.append(dict(mass_g=m * 1e3, rises_K=rises))
        print(f"  {m*1e3:8.1f}" + ''.join(f"{r:12.1f}" for r in rises))
    worst_seal = seal_rise(fric['work_J'], min(SEAL_MASS_SWEEP), 0.0)
    best_seal = seal_rise(fric['work_J'], max(SEAL_MASS_SWEEP), 0.0)
    # the requirement band 8 exists to state: heat that must leave for a 50 K rise
    need_out = {m * 1e3: 1.0 - 50.0 * m * SEAL_CP / fric['work_J'] for m in SEAL_MASS_SWEEP}

    bands = [
        ('1', f"gas stays >= 50 K above nitrogen condensing at {T_COND_N2_AT_END:.0f} K",
         f"{gas['t_end_K']:.1f} K, {gas['t_end_K']-T_COND_N2_AT_END:.1f} K of margin",
         gas['t_end_K'] - T_COND_N2_AT_END >= 50.0),
        ('2', 'tube campaign rise <= 15 K in either material',
         ', '.join(f"{k} {v['campaign_rise_K']:.2f} K" for k, v in tubes.items()),
         all(v['campaign_rise_K'] <= 15.0 for v in tubes.values())),
        ('3', 'chamber wall swing per shot <= 20 K',
         f"{ch['swing_K']:.2f} K", ch['swing_K'] <= 20.0),
        ('4', 'chamber recovers to within 5 K across the cadence',
         f"{ch['residual_K']:.4f} K left, tau {ch['tau_s']:.0f} s",
         ch['residual_K'] <= 5.0),
        ('5', 'seal rise per shot <= 50 K across the whole swept mass range',
         f"{best_seal:.1f} to {worst_seal:.1f} K adiabatic",
         worst_seal <= 50.0),
        ('6', 'differential clearance <= 5 um for the specified pairing',
         f"matched {matched:.2f} um, dissimilar {dissimilar:.2f} um -- "
         f"AND THE REPOSITORY SPECIFIES NEITHER (P85)",
         dissimilar <= 5.0),
        ('7', 'friction heating and expansion cooling do not cancel',
         f"friction {fric['campaign_J']:.0f} J in, gas absorbs "
         f"{ch['q_J']*N_SHOTS:.0f} J out over the campaign -- net "
         f"{'HEATING' if fric['campaign_J'] > ch['q_J']*N_SHOTS else 'COOLING'}",
         abs(fric['campaign_J'] - ch['q_J'] * N_SHOTS) / fric['campaign_J'] > 0.25),
        ('8', 'REPORT: seal rise against mass and heat-out fraction',
         f"{len(SEAL_MASS_SWEEP)}x{len(HEAT_OUT_FRAC)}; for a 50 K rise a 2 g seal must shed "
         f"{need_out[2.0]*100:.2f} % of its friction heat during the stroke", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A58', bands_declared_commit='HEAD~1',
               note='Lumped masses, adiabatic bounds, one conduction path. No FEA, no CFD, no '
                    'contact model. Handbook c_p and alpha, declared in the run sheet, none '
                    'measured. NEEDS SOURCE: seal mass and material -- no seal exists in any '
                    'file, so it is swept. The seal friction changing with the seal temperature '
                    'is the coupling that would matter most and is NOT computed.',
               gas=gas, friction=fric, tubes=tubes, chamber=ch,
               clearance_um=pairs, matched_um=matched, dissimilar_um=dissimilar,
               seal_sweep=seal_rows, heat_out_fracs=list(HEAT_OUT_FRAC),
               heat_out_needed_for_50K=need_out,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'chamber_thermal.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
