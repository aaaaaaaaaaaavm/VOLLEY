"""
VOLLEY | A flywheel motor-generator as the shot energy store, against P26.

WHY THIS EXISTS
---------------
P26 is the largest live defect in the project: the supercapacitor bank cannot source the shot
on purchasable parts. A10's result is that a source of EMF V behind series resistance R cannot
deliver more than V^2/4R into any load, which imposes a 68 mohm ESR ceiling. A single commercial
string of 32 x 190 F cells is 116-185 mohm, so three to four parallel strings are needed and
that mass lands on kill criterion 1.

The ceiling FALLS as velocity rises, which is why it inverts the ranking of every lever in
docs/DESIGN_OPTIONS_exit_velocity.md.

**P26 is a property of capacitors, not of the machine.** A flywheel stores the same energy
behind a different impedance and does not care what load it feeds -- so unlike everything else
considered on 2026-08-10 it needs NO architecture change. The LSM, sled, track, cassettes and
release all stand, and so does every one of A1-A24.

Bands declared in validation/A25_flywheel_store.md at d254759, BEFORE this file existed.

Provenance: model output, not independently re-derived. No component is quoted.
"""
import json
import math
import os

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

ESR_CEILING = 0.068          # ohm, A10. The ceiling the bank misses.
V_BUS = 96.0                 # V, the bank's rated bus, kept so the comparison is like-for-like
BANK_KG_PER_STRING = 6.50    # mass_properties.py, 'Supercapacitor cells + busbars'
BANK_STRINGS = 3             # the honest current position under P26

# Rotor: a thin steel rim, the conservative choice. sigma ~= rho * v^2 for a thin rim.
RHO_STEEL = 7800.0           # kg/m^3
SIGMA_ALLOW = 500e6          # Pa. Textbook yield for a medium-strength alloy steel, NOT sourced
                             # from a datasheet. Named here because band 2 requires it to be.
ROTOR_KG = 3.0               # band 2 sizes within this
OVERSIZE = 2.0               # store 2x the shot, so band 3's droop stays bounded

# Machine and converter, engineering estimates. Every one of these is an assumption.
MG_KG_PER_KW = 0.30          # kg/kW for a high-speed PM machine, rotor+stator+housing
BEARING_KG = 0.8
CONTAINMENT_FRACTION = 1.0   # containment mass as a fraction of rotor mass. Not optional.
CONVERTER_KG_PER_KW = 0.10
R_WINDING = 0.020            # ohm, phase resistance referred to the DC node
R_CONVERTER = 0.015          # ohm, switch + bus contribution


def demand():
    """Shot energy and peak electrical power, imported rather than restated (band 1).

    Peak power is taken at the bank's own node as V_bus * I_peak, using the integrator's
    own I_peak rather than a separate estimate -- that is the node A10's ESR ceiling is
    defined at, so the comparison is like-for-like by construction.
    """
    tr = mm.shot(mm.thrust_constant()[0], trace=True)
    with open(os.path.join(RESULTS, 'motor_results.json')) as fh:
        res = json.load(fh)
    return res['E_drawn_net_J'], V_BUS * tr['I_peak'], res


def rotor(E_store):
    """Size a thin-rim rotor for E_store, and report the stress margin (band 2)."""
    # E = 0.5 I w^2, I = m r^2 for a thin rim, v = w r  ->  E = 0.5 m v^2
    v_tip = math.sqrt(2 * E_store / ROTOR_KG)
    sigma = RHO_STEEL * v_tip ** 2
    margin = SIGMA_ALLOW / sigma
    return dict(rotor_kg=ROTOR_KG, E_store_J=E_store, v_tip_m_s=v_tip,
                sigma_Pa=sigma, margin=margin)


def droop(E_store, E_shot):
    """Speed droop across one shot (band 3). w goes as sqrt(E)."""
    E_after = E_store - E_shot
    ratio = math.sqrt(max(E_after, 0.0) / E_store)
    return dict(E_after_J=E_after, speed_ratio=ratio, droop_pct=100 * (1 - ratio),
                energy_retained_pct=100 * E_after / E_store)


def system_mass(P_peak_kW):
    """Everything the store weighs (band 4), against the bank it replaces.

    A counter-rotating pair is mandatory under band 5, but it SPLITS the duty rather than
    duplicating it: two rotors each storing half the energy, two machines each handling half
    the power. The first version of this function doubled a full-size rotor and a full-power
    machine, which sized a pair that stores and delivers twice what the shot needs -- and
    failed band 4 by 16.9 kg on that basis. Same class of error as the A20 apsides bug: the
    band is not being moved, the model was wrong.
    """
    n = 2                                        # counter-rotating pair
    rotor_each = ROTOR_KG / n                    # the pair stores the same total energy
    mg_each = MG_KG_PER_KW * (P_peak_kW / n)     # the pair delivers the same total power
    conv = CONVERTER_KG_PER_KW * P_peak_kW       # one converter, sized for the whole shot
    cont_each = CONTAINMENT_FRACTION * rotor_each
    total = n * (rotor_each + cont_each + mg_each + BEARING_KG) + conv
    bank = BANK_KG_PER_STRING * BANK_STRINGS
    return dict(rotor_kg=n * rotor_each, containment_kg=n * cont_each, mg_kg=n * mg_each,
                bearings_kg=n * BEARING_KG, converter_kg=conv,
                total_kg=total, bank_kg=bank, delta_kg=total - bank)


def momentum(E_store, r=0.10):
    """Stored angular momentum, and what a counter-rotating pair leaves (band 5)."""
    I = ROTOR_KG * r * r
    w = math.sqrt(2 * E_store / I)
    H_single = I * w
    # A matched counter-rotating pair cancels to first order; residual is the speed mismatch
    # the controller can hold. 1 % is an assumption and is flagged as one.
    residual = 0.01 * H_single
    return dict(r_m=r, I_kg_m2=I, rpm=w * 60 / (2 * math.pi),
                H_single_N_m_s=H_single, H_pair_residual_N_m_s=residual)


def impedance():
    """Equivalent series resistance of the flywheel path, referred to the bank's node (band 6)."""
    R = R_WINDING + R_CONVERTER
    return dict(R_winding=R_WINDING, R_converter=R_CONVERTER, R_total=R,
                ceiling=ESR_CEILING, headroom=ESR_CEILING - R,
                P_max_W=V_BUS ** 2 / (4 * R))


def bands(d):
    out = []
    E_shot, P_peak, res = d['E_shot'], d['P_peak'], d['res']
    b1 = abs(E_shot - res['E_drawn_net_J']) < 1e-9
    out.append(('1', 'demand imported, not restated',
                f"{E_shot:.1f} J net, {P_peak/1000:.1f} kW peak, from motor_model", b1))
    b2 = d['rotor']['margin'] >= 3.0
    out.append(('2', 'rim stress margin >= 3.0',
                f"tip {d['rotor']['v_tip_m_s']:.0f} m/s, sigma {d['rotor']['sigma_Pa']/1e6:.0f} MPa, "
                f"margin {d['rotor']['margin']:.2f}", b2))
    b3 = d['droop']['droop_pct'] <= 30.0
    out.append(('3', 'speed droop over one shot <= 30 %',
                f"{d['droop']['droop_pct']:.1f} %, {d['droop']['energy_retained_pct']:.0f} % "
                f"energy retained", b3))
    b4 = d['mass']['total_kg'] <= d['mass']['bank_kg']
    out.append(('4', 'lighter than the 3-string bank it replaces',
                f"{d['mass']['total_kg']:.1f} kg against {d['mass']['bank_kg']:.1f} kg "
                f"({d['mass']['delta_kg']:+.1f} kg)", b4))
    b5 = d['mom']['H_pair_residual_N_m_s'] <= 0.5
    out.append(('5', 'net stored angular momentum <= 0.5 N.m.s',
                f"single rotor {d['mom']['H_single_N_m_s']:.2f}, counter-rotating pair residual "
                f"{d['mom']['H_pair_residual_N_m_s']:.3f}", b5))
    b6 = d['imp']['R_total'] <= ESR_CEILING
    out.append(('6', f'series resistance <= the {ESR_CEILING*1e3:.0f} mohm ceiling the bank fails',
                f"{d['imp']['R_total']*1e3:.0f} mohm, headroom {d['imp']['headroom']*1e3:+.0f} mohm, "
                f"P_max {d['imp']['P_max_W']/1e3:.0f} kW", b6))
    return out


if __name__ == '__main__':
    E_shot, P_peak, res = demand()
    E_store = OVERSIZE * E_shot
    d = dict(E_shot=E_shot, P_peak=P_peak, res=res,
             rotor=rotor(E_store), droop=droop(E_store, E_shot),
             mass=system_mass(P_peak / 1000.0), mom=momentum(E_store), imp=impedance())

    print(f"shot draws {E_shot:.1f} J net, peak {P_peak/1000:.1f} kW")
    print(f"store sized at {OVERSIZE:.0f}x = {E_store:.0f} J\n")
    r, m = d['rotor'], d['mass']
    print(f"rotor  {r['rotor_kg']:.1f} kg, tip {r['v_tip_m_s']:.0f} m/s, "
          f"{d['mom']['rpm']:.0f} rpm, stress margin {r['margin']:.2f}")
    print(f"droop  {d['droop']['droop_pct']:.1f} % over one shot\n")
    print("system mass:")
    for k in ('rotor_kg', 'containment_kg', 'mg_kg', 'bearings_kg', 'converter_kg'):
        print(f"   {k:16s} {m[k]:6.2f} kg")
    print(f"   {'TOTAL':16s} {m['total_kg']:6.2f} kg  against a {m['bank_kg']:.1f} kg bank "
          f"({m['delta_kg']:+.2f})\n")
    i = d['imp']
    print(f"series resistance {i['R_total']*1e3:.0f} mohm against a {ESR_CEILING*1e3:.0f} mohm "
          f"ceiling -> V^2/4R = {i['P_max_W']/1e3:.0f} kW deliverable\n")

    # The band failed by 1.1 kg. Before writing that up, find out what it turns on --
    # a band miss is only informative if you know which assumption owns it.
    print("what band 4 turns on:")
    print(f"  {'MG_KG_PER_KW':>16s}  {'total kg':>9s}  {'vs 3-string 19.5':>17s}  {'vs 4-string 26.0':>17s}")
    for kgkw in (0.30, 0.25, 0.20, 0.15):
        globals()['MG_KG_PER_KW'] = kgkw
        m2 = system_mass(P_peak / 1000.0)
        print(f"  {kgkw:16.2f}  {m2['total_kg']:9.2f}  {m2['total_kg']-19.5:+16.2f}  "
              f"{m2['total_kg']-26.0:+16.2f}")
    globals()['MG_KG_PER_KW'] = 0.30
    print()

    print("bands:")
    res_b = bands(d)
    for n, name, detail, ok in res_b:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    os.makedirs(RESULTS, exist_ok=True)
    d.pop('res')
    d['bands'] = [dict(band=n, name=nm, detail=dt, pass_=ok) for n, nm, dt, ok in res_b]
    json.dump(d, open(os.path.join(RESULTS, 'flywheel_store.json'), 'w'), indent=2)
    print("\n-> results/flywheel_store.json")
