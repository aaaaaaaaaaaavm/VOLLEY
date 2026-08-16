"""
VOLLEY | The reservoir between shots, and whether it warms back up.

WHY THIS EXISTS
---------------
P64. A42 found A41's reservoir sized on gas the bottle cannot give back, and the correction
it produced is bounded rather than single-valued: 7.65 L isothermal against 11.25 L adiabatic,
about 1.3 kg of store. One term separates them -- whether the gas left in the bottle recovers
its temperature across the 1200 s cadence of ADR-020. A42 assumed it does not, which is right
for a four-second blowdown and was never argued for the twenty minutes that follow it.

WHAT THIS DOES THAT A42 DID NOT
-------------------------------
A42 carried PRESSURE across shots and recomputed mass at each shot start as p.V/(R.T0). That
is neither limit. This carries MASS AND TEMPERATURE as the state, which is the formulation
that has both limits in it, and relaxes the temperature between shots with a lumped time
constant.

The flow relation is imported from fill_window, not restated. What is added here is the
reservoir temperature, which fill_window holds at T0 throughout.

Bands declared in validation/A43_reservoir_thermal.md at bc572ad, BEFORE this file existed.

Provenance: model output. Ideal gas, constant c_v, lumped reservoir, vessel wall held at the
structure temperature, chamber at T0 as A42 assumed. Nitrogen is a homonuclear diatomic and
is effectively transparent in the infrared, so radiation from the wall does not warm the gas;
in free fall there is no buoyancy-driven convection either, so conduction is the only path
modelled. If that is wrong this run is wrong, and it is the assumption to attack first.
"""
import json
import math
import os

import fill_window as fw

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

CV = fw.R_GAS / (fw.GAMMA - 1.0)          # 742 J/kg.K for nitrogen
T_STRUCT = fw.T0                          # the wall, held at the structure temperature
L_OVER_D = 3.0                            # COPV proportions, for the surface area only
K_N2 = 0.026                              # W/m.K at 300 K and 1 bar. Rises with pressure;
                                          # the sweep spans three decades so the value of this
                                          # constant is not what the answer turns on.
T_FLOOR_K = 150.0                         # band 5
V_SEARCH_STEP = 0.05e-3
V_SEARCH_MAX = 40e-3
T_CAP_S = 1e4                             # fill_window's integrator cap, kept for comparability

H_SWEEP = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, math.inf)


def vessel_area(v_res):
    """Wetted area of a cylinder at the declared proportions. Geometry only."""
    r = (v_res / (2.0 * math.pi * L_OVER_D)) ** (1.0 / 3.0)
    return 2.0 * math.pi * r * r + 2.0 * math.pi * r * (2.0 * L_OVER_D * r)


def conduction_h(v_res):
    """Conduction-only coefficient, k over the cylinder radius. Reported, not selected."""
    r = (v_res / (2.0 * math.pi * L_OVER_D)) ** (1.0 / 3.0)
    return K_N2 / r


def tau(m_res, v_res, h):
    if h <= 0.0:
        return math.inf
    if math.isinf(h):
        return 0.0
    return m_res * CV / (h * vessel_area(v_res))


def fill(m_res, t_res, v_res, orifice_m2, dt=1e-4):
    """One charge, reservoir expanding adiabatically from (m, T). Chamber at T0, as A42.

    Returns (fill_time, m_res, T_res). fill_time is None if the bottle cannot finish.
    """
    m0, t0 = m_res, t_res
    m_ch, t, p_ch = 0.0, 0.0, 0.0
    while p_ch < fw.P_CHARGE and t < T_CAP_S:
        p_res = m_res * fw.R_GAS * t_res / v_res
        if p_res <= p_ch:
            return None, m_res, t_res
        ratio = p_ch / p_res
        # fill_window's relation, evaluated at the reservoir's own temperature rather than T0
        flux = fw.FLUX * math.sqrt(fw.T0 / t_res)
        if ratio <= fw.CRIT:
            flow = fw.CD * orifice_m2 * p_res * flux
        else:
            flow = fw.CD * orifice_m2 * math.sqrt(
                2.0 * fw.GAMMA / (fw.GAMMA - 1.0) * p_res * (p_res / (fw.R_GAS * t_res))
                * max(ratio ** (2.0 / fw.GAMMA)
                      - ratio ** ((fw.GAMMA + 1.0) / fw.GAMMA), 0.0))
        step = min(flow * dt, m_res)
        m_res -= step
        m_ch += step
        t_res = t0 * (m_res / m0) ** (fw.GAMMA - 1.0)      # adiabatic, on mass
        p_ch = m_ch * fw.R_GAS * fw.T0 / fw.V_CHAMBER
        t += dt
        if m_res <= 0.0:
            return None, m_res, t_res
    if t >= T_CAP_S:
        return None, m_res, t_res
    return t, m_res, t_res


def relax(m_res, t_res, v_res, h, dt=fw.CADENCE_S):
    """Constant volume, constant mass. The wall is an infinite reservoir at T_STRUCT."""
    k = tau(m_res, v_res, h)
    if k == 0.0:
        return T_STRUCT
    if math.isinf(k):
        return t_res
    return T_STRUCT + (t_res - T_STRUCT) * math.exp(-dt / k)


def sequence(v_res, orifice_m2, h):
    """Twelve charges off one bottle, with the cadence between them."""
    m_res = fw.P_STORE * v_res / (fw.R_GAS * fw.T0)
    t_res = fw.T0
    out, failed, t_min = [], None, t_res
    for i in range(fw.N_MANIFEST):
        t, m_res, t_res = fill(m_res, t_res, v_res, orifice_m2)
        t_min = min(t_min, t_res)
        out.append(dict(shot=i + 1, fill_s=t, T_after_K=t_res,
                        p_after_bar=m_res * fw.R_GAS * t_res / v_res / 1e5))
        if t is None:
            failed = i + 1
            break
        t_res = relax(m_res, t_res, v_res, h)
    return out, failed, t_min


def required(orifice_m2, h):
    """Smallest reservoir delivering twelve charges. Searched, not asserted."""
    v = 4.0e-3
    while v < V_SEARCH_MAX:
        _, failed, _ = sequence(v, orifice_m2, h)
        if failed is None:
            return v
        v += V_SEARCH_STEP
    return None


def main():
    orifice = math.pi * (fw.ORIFICE_MM / 2e3) ** 2 if hasattr(fw, 'ORIFICE_MM') \
        else math.pi * (1.0 / 2e3) ** 2

    print(f"c_v {CV:.1f} J/kg.K   cadence {fw.CADENCE_S:.0f} s   "
          f"structure {T_STRUCT:.0f} K\n")

    print(f"{'h W/m2K':>9s} {'reservoir L':>12s} {'tau s':>10s} {'T_min K':>9s} "
          f"{'store kg':>9s} {'kg/sat':>8s}")
    sweep = []
    for h in H_SWEEP:
        v = required(orifice, h)
        if v is None:
            sweep.append(dict(h=h, v_l=None))
            print(f"{h:9.1f} {'no solution':>12s}")
            continue
        seq, _, t_min = sequence(v, orifice, h)
        m0 = fw.P_STORE * v / (fw.R_GAS * fw.T0)
        k = tau(m0, v, h)
        store = fw.store_kg(v)
        per_sat = (fw.ADDED_BASE_KG + store) / fw.N_MANIFEST
        sweep.append(dict(h=h, v_l=v * 1e3, tau_s=k, t_min_k=t_min,
                          store_kg=store, per_sat_kg=per_sat,
                          last_fill_s=seq[-1]['fill_s']))
        ks = 'inf' if math.isinf(k) else f"{k:.0f}"
        print(f"{h:9.1f} {v*1e3:12.2f} {ks:>10s} {t_min:9.1f} {store:9.2f} {per_sat:8.3f}")

    iso = next(s for s in sweep if math.isinf(s['h']))
    adi = next(s for s in sweep if s['h'] == 0.0)
    h_cond = conduction_h(adi['v_l'] * 1e-3)
    m_cond = fw.P_STORE * (adi['v_l'] * 1e-3) / (fw.R_GAS * fw.T0)
    tau_cond = tau(m_cond, adi['v_l'] * 1e-3, h_cond)

    print(f"\nconduction-only coefficient at that geometry: {h_cond:.3f} W/m2K, "
          f"tau {tau_cond:.0f} s against a {fw.CADENCE_S:.0f} s cadence")

    # band 8: the same question at two other orifices
    orif = {}
    for d_mm in (0.5, 2.0):
        a = math.pi * (d_mm / 2e3) ** 2
        v = required(a, 0.0)
        orif[d_mm] = v * 1e3 if v else None
    spread = max(abs(v - adi['v_l']) / adi['v_l'] for v in orif.values() if v)

    solved = [s for s in sweep if s['v_l']]
    monotone = all(a['v_l'] >= b['v_l'] - 1e-9
                   for a, b in zip(solved, solved[1:]))
    bands = [
        ('1', "instant relaxation reproduces A42's 7.65 L within 5 %",
         f"{iso['v_l']:.2f} L, {abs(iso['v_l']-7.65)/7.65*100:.1f} % off",
         abs(iso['v_l'] - 7.65) / 7.65 <= 0.05),
        ('2', 'no relaxation requires strictly more than instant relaxation',
         f"{adi['v_l']:.2f} L against {iso['v_l']:.2f} L", adi['v_l'] > iso['v_l']),
        ('3', 'required reservoir monotonically non-increasing in h',
         'monotone' if monotone else 'NOT monotone', monotone),
        ('4', 'every solved point lies within 6.0 - 15.0 L',
         f"{min(s['v_l'] for s in solved):.2f} - {max(s['v_l'] for s in solved):.2f} L",
         all(6.0 <= s['v_l'] <= 15.0 for s in solved)),
        ('5', f'minimum gas temperature >= {T_FLOOR_K:.0f} K at the least favourable h',
         f"{adi['t_min_k']:.1f} K", adi['t_min_k'] >= T_FLOOR_K),
        ('6', f"store at the conservative end <= {fw.BUDGET_KG:.2f} kg",
         f"{adi['store_kg']:.2f} kg", adi['store_kg'] <= fw.BUDGET_KG),
        ('7', f"added mass per satellite there <= {fw.TARGET_KG:.1f} kg",
         f"{adi['per_sat_kg']:.3f} kg", adi['per_sat_kg'] <= fw.TARGET_KG),
        ('8', 'orifice 0.5 and 2.0 mm move the required reservoir by <= 2 %',
         f"{spread*100:.2f} %", spread <= 0.02),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A43', bands_declared_commit='bc572ad',
               note='ideal gas, constant c_v, lumped reservoir, wall held at the structure '
                    'temperature, chamber at T0 as A42 assumed. Conduction only: nitrogen is '
                    'IR-transparent and free fall removes buoyancy convection. No forced '
                    'circulation, no wall thermal mass, no gas recovery from the fired chamber.',
               cv_J_kgK=CV, cadence_s=fw.CADENCE_S, k_n2=K_N2,
               conduction_h_W_m2K=h_cond, conduction_tau_s=tau_cond,
               sweep=sweep, orifice_check_l=orif,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'reservoir_thermal.json'), 'w') as f:
        json.dump(out, f, indent=2, default=str)
        f.write('\n')


if __name__ == '__main__':
    main()
