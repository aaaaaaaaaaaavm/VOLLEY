"""A62: steam as the working fluid, with the water heated by being in space.

Bands declared in validation/A62_steam_working_fluid.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
A39 traded a steel spring, cold gas and keeping the motor, and screened a lead screw, a rack and
pinion and a flywheel. It never considered a HEATED WORKING FLUID.

The proposal is water stored at low pressure, raised to steam by SOLAR FLUX ALONE -- no resistive
heater, no electrolysis, no combustion -- and fired as the same closed adiabatic expansion A41
specified. The gun is unchanged; only the fluid and how it is charged differ.

WHY IT IS WORTH COMPUTING
-------------------------
Steam's molecular weight is 18 against nitrogen's 28 and its gamma is 1.33 against 1.4, so the same
charge pressure is reached with less mass AND the pressure falls more slowly through the stroke.
Both point the same way, and the 200 bar COPV disappears.

WHAT HAS TO BE TRUE
-------------------
    it must not condense in the tube      two-phase expansion is less repeatable, and A55 found
                                          dispersion is what this architecture can least afford
    the sun must reach that temperature   T = (alpha/eps . S / 2 sigma)^0.25; a plain black
                                          surface at 1 AU reaches only 331 K
    the machine must survive it           the tube, the chamber, and the seal A61 just specified
    it must survive eclipse               ~35 min dark in ~93, and water freezes at 273 K

NO STEAM TABLES ARE IN THIS REPOSITORY. Ideal gas throughout, stated at each use, and the wet case
is bounded rather than computed -- which is why band 4 asks what superheat avoids it entirely.
No absorber, coating, insulation, plumbing or pointing mass is counted, so every figure below
FLATTERS steam.

Run:  python3 analysis/steam_fluid.py
"""
import json
import math
import os

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_CHAMBER = 2.0e-3
R_UNIV = 8.314
S_SOLAR = 1361.0
SIGMA = 5.67e-8
M_STEAM, G_STEAM = 0.018, 1.33
M_N2, G_N2 = 0.028, 1.4
H_RAISE = 2.786e6                 # J/kg, sensible + latent + superheat. Handbook. NEEDS SOURCE.
AL_LIMIT_K, STEEL_LIMIT_K, PTFE_LIMIT_K = 473.0, 700.0, 533.0
TANK_KG = 0.20                    # a declared guess, and said to be one
ECLIPSE_S, ORBIT_S = 35 * 60.0, 93 * 60.0
ALPHA = 0.95
CADENCE_S = 1200.0
N_SHOTS = 12
# A56's sized store, and A59's two tube candidates
STORE_KG, VESSEL_KG, GAS_KG = 3.1216, 0.4703, 0.8131
TUBE_AL_KG, TUBE_STEEL_KG = 1.1404, 3.294
AE_SWEEP = (1.0, 2.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0)


def t_sat_water(p_pa):
    """Antoine, water. Handbook correlation, not a steam table."""
    mmhg = p_pa / 133.322
    return 1730.63 / (8.07131 - math.log10(mmhg)) - 233.426 + 273.15


def shot(gamma, molar_mass, t_charge):
    """The same closed adiabatic expansion A41 specified, with the fluid made explicit."""
    p0, L = pc.P_MAX, pc.STROKE
    r = V_CHAMBER / (V_CHAMBER + pc.AREA * L)
    w = p0 * V_CHAMBER / (gamma - 1.0) * (1.0 - r ** (gamma - 1.0))
    rho = p0 * molar_mass / (R_UNIV * t_charge)
    return dict(gamma=gamma, t_charge_K=t_charge, ratio=r, work_J=w,
                density_kg_m3=rho, charge_kg=rho * V_CHAMBER,
                v_exit=math.sqrt(2.0 * w / pc.M_PAY),
                p_end_bar=p0 * r ** gamma / 1e5,
                t_end_K=t_charge * r ** (gamma - 1.0))


def equilibrium_T(alpha_over_eps):
    """Flat absorber at 1 AU, absorbing one side and radiating two."""
    return (alpha_over_eps * S_SOLAR / (2.0 * SIGMA)) ** 0.25


def alpha_over_eps_for(t_target):
    return t_target ** 4 * 2.0 * SIGMA / S_SOLAR


def main():
    p0 = pc.P_MAX
    n2 = shot(G_N2, M_N2, pc.T0)

    # band 4: the charge temperature that keeps the whole expansion dry
    r = n2['ratio']
    p_end = p0 * r ** G_STEAM
    t_sat_end = t_sat_water(p_end)
    t_dry = t_sat_end / r ** (G_STEAM - 1.0)
    st = shot(G_STEAM, M_STEAM, t_dry)

    print(f"A62 steam. {pc.STROKE:.1f} m at {p0/1e5:.4f} bar, ratio {r:.4f}\n")
    print(f"  {'':<22}{'nitrogen':>12}{'steam':>12}")
    for lab, k, f in (('charge T K', 't_charge_K', '12.0f'), ('gamma', 'gamma', '12.2f'),
                      ('density kg/m3', 'density_kg_m3', '12.2f'),
                      ('charge g', 'charge_kg', '12.1f'), ('work J', 'work_J', '12.0f'),
                      ('v_exit m/s', 'v_exit', '12.2f'),
                      ('p end bar', 'p_end_bar', '12.2f'), ('T end K', 't_end_K', '12.0f')):
        a = n2[k] * (1e3 if k == 'charge_kg' else 1)
        b = st[k] * (1e3 if k == 'charge_kg' else 1)
        print(f"  {lab:<22}{format(a, f)}{format(b, f)}")
    print(f"\n  steam condenses below {t_sat_end:.0f} K at the {p_end/1e5:.2f} bar it ends at,")
    print(f"  so the charge must start at {t_dry:.0f} K ({t_dry-273.15:.0f} C) to stay dry")
    print(f"    aluminium useful to {AL_LIMIT_K:.0f} K -> {'OK' if t_dry <= AL_LIMIT_K else 'EXCEEDED'}")
    print(f"    filled PTFE to      {PTFE_LIMIT_K:.0f} K -> {'OK' if t_dry <= PTFE_LIMIT_K else 'EXCEEDED'}")
    print(f"    steel to            {STEEL_LIMIT_K:.0f} K -> {'OK' if t_dry <= STEEL_LIMIT_K else 'EXCEEDED'}")

    e_charge = st['charge_kg'] * H_RAISE
    p_mean = e_charge / CADENCE_S
    duty = (ORBIT_S - ECLIPSE_S) / ORBIT_S
    ae_needed = alpha_over_eps_for(t_dry)
    eps = ALPHA / ae_needed
    area = p_mean / duty / (ALPHA * S_SOLAR)
    print(f"\n  {st['charge_kg']*1e3:.1f} g x {H_RAISE/1e6:.3f} MJ/kg = {e_charge/1e3:.1f} kJ "
          f"-> {p_mean:.1f} W over the {CADENCE_S:.0f} s cadence")
    print(f"  passive equilibrium needs alpha/eps >= {ae_needed:.1f} "
          f"(eps = {eps:.3f} at alpha {ALPHA})")
    print(f"  absorber {area:.4f} m2 at a {duty*100:.0f} % sunlit duty cycle "
          f"({math.sqrt(area)*100:.0f} cm square)")

    # band 9: eclipse. The store radiates from the same absorber at the same emissivity.
    q_loss = eps * SIGMA * area * t_dry ** 4
    e_eclipse = q_loss * ECLIPSE_S
    water_campaign = st['charge_kg'] * N_SHOTS
    # heat available in the stored water before it reaches freezing
    e_available = water_campaign * 4186.0 * (t_dry - 273.15)
    print(f"\n  eclipse: radiates {q_loss:.1f} W for {ECLIPSE_S/60:.0f} min = {e_eclipse/1e3:.1f} kJ")
    print(f"    the {water_campaign*1e3:.0f} g of stored water holds {e_available/1e3:.1f} kJ "
          f"above freezing -> {'SURVIVES' if e_eclipse < e_available else 'FREEZES'}")

    # band 8: the mass, counting the tube the temperature forces
    tube = TUBE_AL_KG if t_dry <= AL_LIMIT_K else TUBE_STEEL_KG
    store_saving = (VESSEL_KG + GAS_KG) - (water_campaign + TANK_KG)
    tube_penalty = tube - TUBE_AL_KG
    net = store_saving - tube_penalty
    print(f"\n  mass: store saving {store_saving:+.3f} kg "
          f"(vessel {VESSEL_KG:.3f} + gas {GAS_KG:.3f} out, water {water_campaign:.3f} "
          f"+ tank {TANK_KG:.2f} in)")
    print(f"        tube forced to {'steel' if tube == TUBE_STEEL_KG else 'aluminium'}: "
          f"{tube_penalty:+.3f} kg")
    print(f"        NET {net:+.3f} kg, before any absorber, coating, insulation or pointing")

    print(f"\nband 10, passive equilibrium against alpha/eps:")
    sweep = []
    for ae in AE_SWEEP:
        t = equilibrium_T(ae)
        sweep.append(dict(alpha_over_eps=ae, T_K=t, dry=bool(t >= t_dry)))
        print(f"    {ae:5.1f} -> {t:5.0f} K  {'dry' if t >= t_dry else ''}")

    bands = [
        ('1', "nitrogen baseline reproduces 2350 J and 51.0 g within 1 %",
         f"{n2['work_J']:.0f} J, {n2['charge_kg']*1e3:.1f} g",
         abs(n2['work_J'] - 2350) / 2350 <= 0.01
         and abs(n2['charge_kg'] * 1e3 - 51.0) / 51.0 <= 0.01),
        ('2', 'steam delivers >= 100 % of nitrogen shot work',
         f"{st['work_J']/n2['work_J']*100:.2f} %", st['work_J'] >= n2['work_J']),
        ('3', 'steam charge mass <= 60 % of nitrogen',
         f"{st['charge_kg']/n2['charge_kg']*100:.1f} %",
         st['charge_kg'] <= 0.60 * n2['charge_kg']),
        ('4', f'charge temperature to stay dry <= {AL_LIMIT_K:.0f} K',
         f"{t_dry:.0f} K", t_dry <= AL_LIMIT_K),
        ('5', 'reachable passively with alpha/eps <= 20',
         f"needs {ae_needed:.1f}", ae_needed <= 20.0),
        ('6', 'absorber area <= 0.25 m2',
         f"{area:.4f} m2", area <= 0.25),
        ('7', f"within filled PTFE's {PTFE_LIMIT_K:.0f} K limit, so A61's 17.8 N spec survives",
         f"{t_dry:.0f} K against {PTFE_LIMIT_K:.0f} K", t_dry <= PTFE_LIMIT_K),
        ('8', 'net mass is a saving once the tube material is counted',
         f"{net:+.3f} kg", net > 0.0),
        ('9', 'the store survives 35 min of eclipse without freezing',
         f"loses {e_eclipse/1e3:.1f} kJ against {e_available/1e3:.1f} kJ available",
         e_eclipse < e_available),
        ('10', 'REPORT: equilibrium temperature against alpha/eps',
         f"{len(AE_SWEEP)} points, {sweep[0]['T_K']:.0f} to {sweep[-1]['T_K']:.0f} K", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A62', bands_declared_commit='HEAD~1',
               note='Ideal gas throughout -- NO STEAM TABLES are in this repository -- and the wet '
                    'case is bounded rather than computed, which is why band 4 asks what superheat '
                    'avoids it. Enthalpy to raise a charge, material limits and the tank allowance '
                    'are handbook or declared guesses: NEEDS SOURCE. No absorber, coating, '
                    'insulation, plumbing or sun-pointing mass is counted, so every figure here '
                    'FLATTERS steam. No product, compound or supplier is named.',
               nitrogen=n2, steam=st, t_sat_at_end_K=t_sat_end, t_dry_K=t_dry,
               energy_per_charge_J=e_charge, mean_power_W=p_mean,
               alpha_over_eps_needed=ae_needed, emissivity=eps,
               absorber_m2=area, duty_cycle=duty,
               eclipse_loss_J=e_eclipse, eclipse_available_J=e_available,
               water_campaign_kg=water_campaign, tube_forced_kg=tube,
               store_saving_kg=store_saving, tube_penalty_kg=tube_penalty, net_kg=net,
               ae_sweep=sweep,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'steam_fluid.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
