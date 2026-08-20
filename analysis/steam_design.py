"""A63: the steam design surface. The run A62 should have been.

Bands declared in validation/A63_steam_design_point.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
P90. A62 computed every figure at a 2.0 L chamber -- the volume A41 sized for COLD NITROGEN -- and
concluded steam needs 550 K, breaks A61's seal specification and costs 1.285 kg. The chamber was
never re-optimised for the fluid, and it is the variable steam is most sensitive to.

THE PHYSICS THAT MAKES THE CHAMBER THE LEVER
--------------------------------------------
    T_dry = T_sat(p0 . r^gamma) / r^(gamma-1),    r = V0 / (V0 + A.L)

A larger chamber raises r, which raises the end pressure and therefore the saturation temperature
-- but raises the END TEMPERATURE faster. The two race and the second wins, so T_dry falls toward
its floor, T_sat(p0) itself.

That floor is what the material limits act on, not the expansion.

WHAT A62 DID NOT TRADE
----------------------
A larger chamber costs chamber mass and water per shot, and the store saving is the reason steam
was proposed. A62 asked whether steam works. This asks what it costs.

No steam tables are in this repository. Ideal gas throughout, and the wet region is avoided by
construction rather than modelled. No absorber, coating, insulation or pointing mass is charged,
so every figure FLATTERS steam, as A62's did.

Run:  python3 analysis/steam_design.py
"""
import json
import math
import os

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

R_UNIV, M_STEAM, G_STEAM = 8.314, 0.018, 1.33
M_N2, G_N2 = 0.028, 1.4
S_SOLAR, SIGMA, ALPHA = 1361.0, 5.67e-8, 0.95
H_RAISE = 2.786e6
AL_LIMIT_K, PTFE_LIMIT_K = 473.0, 533.0
G_CAP_PAYLOAD = 25.0
TANK_KG = 0.20
CADENCE_S, N_SHOTS = 1200.0, 12
ECLIPSE_S, ORBIT_S = 35 * 60.0, 93 * 60.0
# baselines: A56's sized nitrogen store, A59's tubes, A41's chamber
N2_VESSEL_KG, N2_GAS_KG, N2_CHAMBER_KG = 0.4703, 0.8131, 0.3382
TUBE_AL_KG, TUBE_STEEL_KG = 1.1404, 3.294
W_TARGET = 2350.0
P_SWEEP_BAR = (8, 10, 12, 14, 15.9, 18, 20, 22.7258, 26, 30, 36, 45)
V_SWEEP_L = (2, 3, 4, 6, 8, 12, 16, 24, 32)


def t_sat(p_pa):
    """Antoine, water. A handbook correlation, not a steam table."""
    return 1730.63 / (8.07131 - math.log10(p_pa / 133.322)) - 233.426 + 273.15


def point(p0, v0):
    """One steam design point: the dry charge temperature, the shot, and what it costs."""
    r = v0 / (v0 + pc.AREA * pc.STROKE)
    p_end = p0 * r ** G_STEAM
    t_dry = t_sat(p_end) / r ** (G_STEAM - 1.0)
    work = p0 * v0 / (G_STEAM - 1.0) * (1.0 - r ** (G_STEAM - 1.0))
    water = p0 * M_STEAM / (R_UNIV * t_dry) * v0
    chamber = pc.chamber_kg(v0, p0)
    tube = TUBE_AL_KG if t_dry <= AL_LIMIT_K else TUBE_STEEL_KG
    e_charge = water * H_RAISE
    p_mean = e_charge / CADENCE_S
    duty = (ORBIT_S - ECLIPSE_S) / ORBIT_S
    ae = t_dry ** 4 * 2.0 * SIGMA / S_SOLAR
    area = p_mean / duty / (ALPHA * S_SOLAR)
    eps = ALPHA / ae
    e_eclipse = eps * SIGMA * area * t_dry ** 4 * ECLIPSE_S
    e_avail = water * N_SHOTS * 4186.0 * (t_dry - 273.15)
    # the mass, all on one page: what steam removes, what it adds
    removed = N2_VESSEL_KG + N2_GAS_KG + N2_CHAMBER_KG
    added = water * N_SHOTS + TANK_KG + chamber + (tube - TUBE_AL_KG)
    return dict(p0_bar=p0 / 1e5, chamber_l=v0 * 1e3, ratio=r, p_end_bar=p_end / 1e5,
                t_dry_K=t_dry, work_J=work, v_exit=math.sqrt(2.0 * work / pc.M_PAY),
                a_peak_g=p0 * pc.AREA / pc.M_PAY / pc.G,
                water_g=water * 1e3, water_campaign_kg=water * N_SHOTS,
                chamber_kg=chamber, tube_kg=tube, tube_penalty_kg=tube - TUBE_AL_KG,
                removed_kg=removed, added_kg=added, net_kg=removed - added,
                mean_power_W=p_mean, alpha_over_eps=ae, absorber_m2=area,
                eclipse_ok=bool(e_eclipse < e_avail))


def main():
    r_n2 = 2.0e-3 / (2.0e-3 + pc.AREA * pc.STROKE)
    w_n2 = pc.P_MAX * 2.0e-3 / (G_N2 - 1.0) * (1.0 - r_n2 ** (G_N2 - 1.0))
    v_n2 = math.sqrt(2.0 * w_n2 / pc.M_PAY)
    n2_water_equiv = pc.P_MAX * M_N2 / (R_UNIV * pc.T0) * 2.0e-3 * N_SHOTS

    grid = [point(p * 1e5, v * 1e-3) for p in P_SWEEP_BAR for v in V_SWEEP_L]
    a62 = point(pc.P_MAX, 2.0e-3)

    print(f"A63 steam design surface. {pc.STROKE:.1f} m stroke, {len(grid)} points\n")
    print(f"  nitrogen baseline: {w_n2:.0f} J, {v_n2:.2f} m/s, "
          f"{n2_water_equiv*1e3:.0f} g of gas over the campaign")
    print(f"  A62's point, 2.0 L at {a62['p0_bar']:.4f} bar: "
          f"T_dry {a62['t_dry_K']:.0f} K, {a62['work_J']:.0f} J\n")

    feasible = [q for q in grid if q['work_J'] >= W_TARGET and q['a_peak_g'] <= G_CAP_PAYLOAD]
    ptfe = [q for q in feasible if q['t_dry_K'] <= PTFE_LIMIT_K]
    alu = [q for q in feasible if q['t_dry_K'] <= AL_LIMIT_K]
    savers = [q for q in ptfe if q['net_kg'] > 0]

    print(f"  {len(feasible)} points make {W_TARGET:.0f} J inside the {G_CAP_PAYLOAD:.0f} g cap")
    print(f"  {len(ptfe)} of them stay inside filled PTFE's {PTFE_LIMIT_K:.0f} K")
    print(f"  {len(alu)} reach aluminium's {AL_LIMIT_K:.0f} K")
    print(f"  {len(savers)} of the PTFE set are a net mass SAVING\n")

    # selected: of the PTFE-feasible set, the lightest net; ties to the faster shot
    sel = max(ptfe, key=lambda q: (q['net_kg'], q['v_exit'])) if ptfe else None

    print(f"  {'bar':>8}{'cham L':>8}{'T_dry':>7}{'work J':>8}{'v m/s':>7}{'a g':>7}"
          f"{'water g':>9}{'chamber':>9}{'tube':>7}{'net kg':>9}")
    for q in sorted(ptfe, key=lambda x: -x['net_kg'])[:14]:
        print(f"  {q['p0_bar']:8.2f}{q['chamber_l']:8.0f}{q['t_dry_K']:7.0f}{q['work_J']:8.0f}"
              f"{q['v_exit']:7.2f}{q['a_peak_g']:7.2f}{q['water_g']:9.1f}"
              f"{q['chamber_kg']:9.3f}{q['tube_kg']:7.2f}{q['net_kg']:+9.3f}")

    if sel:
        print(f"\n  selected: {sel['p0_bar']:.2f} bar, {sel['chamber_l']:.0f} L -> "
              f"{sel['t_dry_K']:.0f} K, {sel['work_J']:.0f} J, {sel['v_exit']:.2f} m/s, "
              f"{sel['a_peak_g']:.2f} g")
        print(f"    removes {sel['removed_kg']:.3f} kg (COPV {N2_VESSEL_KG:.3f} + gas "
              f"{N2_GAS_KG:.3f} + old chamber {N2_CHAMBER_KG:.3f})")
        print(f"    adds    {sel['added_kg']:.3f} kg (water {sel['water_campaign_kg']:.3f} + tank "
              f"{TANK_KG:.2f} + chamber {sel['chamber_kg']:.3f} + steel tube "
              f"{sel['tube_penalty_kg']:.3f})")
        print(f"    NET     {sel['net_kg']:+.3f} kg, before any absorber or insulation")
        print(f"    solar: {sel['mean_power_W']:.1f} W, alpha/eps {sel['alpha_over_eps']:.1f}, "
              f"absorber {sel['absorber_m2']:.4f} m2, eclipse "
              f"{'survives' if sel['eclipse_ok'] else 'FREEZES'}")

    bands = [
        ('1', "reproduces A62's 550 K and 2397 J at 2.0 L within 1 %",
         f"{a62['t_dry_K']:.0f} K, {a62['work_J']:.0f} J",
         abs(a62['t_dry_K'] - 550) / 550 <= 0.01 and abs(a62['work_J'] - 2397) / 2397 <= 0.01),
        ('2', 'nitrogen baseline reproduces 2350 J and 34.28 m/s within 1 %',
         f"{w_n2:.0f} J, {v_n2:.2f} m/s",
         abs(w_n2 - 2350) / 2350 <= 0.01 and abs(v_n2 - 34.28) / 34.28 <= 0.01),
        ('3', f'a point exists with T_dry <= {PTFE_LIMIT_K:.0f} K delivering >= {W_TARGET:.0f} J',
         f"{len(ptfe)} points", bool(ptfe)),
        ('4', f'a point exists with T_dry <= {AL_LIMIT_K:.0f} K delivering >= {W_TARGET:.0f} J',
         f"{len(alu)} points", bool(alu)),
        ('5', f'the selected point stays within the {G_CAP_PAYLOAD:.0f} g payload cap',
         f"{sel['a_peak_g']:.2f} g" if sel else 'no point', bool(sel)),
        ('6', 'net mass at the selected point is a saving',
         f"{sel['net_kg']:+.3f} kg" if sel else 'no point',
         bool(sel and sel['net_kg'] > 0)),
        ('7', f"campaign water <= nitrogen's {n2_water_equiv*1e3:.0f} g",
         f"{sel['water_campaign_kg']*1e3:.0f} g" if sel else 'no point',
         bool(sel and sel['water_campaign_kg'] <= n2_water_equiv)),
        ('8', f'the selected shot delivers >= {v_n2:.2f} m/s',
         f"{sel['v_exit']:.2f} m/s" if sel else 'no point',
         bool(sel and sel['v_exit'] >= v_n2)),
        ('9', 'solar closes: alpha/eps <= 20, absorber <= 0.25 m2, survives eclipse',
         f"{sel['alpha_over_eps']:.1f}, {sel['absorber_m2']:.4f} m2, "
         f"{'survives' if sel['eclipse_ok'] else 'freezes'}" if sel else 'no point',
         bool(sel and sel['alpha_over_eps'] <= 20 and sel['absorber_m2'] <= 0.25
              and sel['eclipse_ok'])),
        ('10', 'REPORT: the surface, Pareto set published',
         f"{len(grid)} points, {len(ptfe)} inside PTFE, {len(savers)} of those a saving", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A63', bands_declared_commit='HEAD~1',
               note='Ideal gas, no steam tables. The wet region is avoided by construction rather '
                    'than modelled. No absorber, coating, insulation, plumbing or pointing mass is '
                    'charged, so every figure FLATTERS steam, as A62 did. Dispersion, trim '
                    'authority, pulse store and the A61 seal specification all still carry '
                    "nitrogen's numbers. No product, compound or supplier is named.",
               nitrogen=dict(work_J=w_n2, v_exit=v_n2, campaign_gas_kg=n2_water_equiv),
               a62_point=a62, n_grid=len(grid), n_feasible=len(feasible),
               n_inside_ptfe=len(ptfe), n_inside_aluminium=len(alu), n_saving=len(savers),
               selected=sel, ptfe_set=sorted(ptfe, key=lambda x: -x['net_kg'])[:20],
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'steam_design.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
