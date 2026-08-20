"""
VOLLEY | The per-cell ejector, re-asked against pyrotechnic gas generation.

WHY THIS EXISTS
---------------
A53 failed on energy and nothing else. Seven of eight bands passed; band 7 failed because a
spring sized for a clean departure stores 4.5 J and clearing the tube costs 667.2 J at ADR-034's
8.0 m stroke -- a 148x shortfall. P81 carries the consequence, and A47 priced it at +2.27
satellites against +0.37 for the whole Gen5 -> Gen6 change.

A53 closed it as architectural. It was a STORE CHOICE, which is the same mistake A54 made about
the pulse store and A64 corrected by changing technology class rather than design.

Bands declared in validation/A65_pyrotechnic_ejector.md at HEAD, BEFORE this file existed.

Provenance: model output. The gas generator is named as a TECHNOLOGY CLASS -- solid-propellant
automotive restraint inflators -- with published ranges declared at the point of use, the way A39
declared its gas model and A64 its capacitors. No product, supplier or organisation is named.

The zonal cooling treatment is the weakest link and is declared as such in the run sheet: the
sink is taken to reach equilibrium with the whole charge before expansion begins, which is
conservative for work and optimistic for sink mass.
"""
import json
import math
import os

import fmea
import fmea_gen6 as g6
import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# ---- imported from the record, not chosen here -----------------------------------------------
M_PAY, G = pc.M_PAY, pc.G
AREA, STROKE = pc.AREA, pc.STROKE
FRICTION_N = 83.40371375447981      # A41 band 8's allowance, as backup_ejector.py carries it
V_TARGET = 1.5                      # m/s, A53's clearance velocity, for the band 1 anchor
G_CAP_PAYLOAD = 25.0                # A37's payload cap. NOT Gen6's commanded 11.36 g: a backup
                                    # ejector is an off-nominal event.
CHAMBER_L_EXISTING = 2.0            # gen6_store.chamber_volume_l
T_CEILING = 473.0                   # ADR-035, gen6_drive.tube_temperature_ceiling_K
STORE_KG = 3.1216                   # A56's resized store, gen6_store.store_mass_kg
ADDED_BASE_KG = 11.452976           # A37's base, as backup_ejector.py carries it
N_CELLS = 12
TARGET_KG = 2.0
PER_CELL_KG_BAND = 0.25             # A53 band 1's threshold, unchanged

# ---- the technology class, published ranges declared here -------------------------------------
MOL_LO, MOL_HI = 0.5, 0.9           # gas produced per unit
T_GAS_LO, T_GAS_HI = 1000.0, 1400.0  # total gas temperature, tank-test measurement
GENERANT_LO, GENERANT_HI = 0.020, 0.100   # kg of solid generant, driver-side class
R_U = 8.314                         # J/mol.K
M_N2 = 0.028                        # kg/mol, A39's working gas
CP_N2 = pc.GAMMA * 296.8 / (pc.GAMMA - 1.0)   # J/kg.K from A39's R and gamma
CP_SINK = 460.0                     # J/kg.K, steel: chamber_thermal.py MATERIALS['steel']
T_START = 293.0                     # K, the sink before the shot

# DECLARED GUESS, and the largest assumption in this run: initiator, housing, gas path and mount
# per cell. A53 declared 0.12 kg for its latch, guide and baseplate with no derivation; the same
# figure is carried here so the two runs are directly comparable.
HOUSING_KG = 0.12


def sink_kg(n_mol, t_gas, t_out=T_CEILING):
    """Steel heat sink that brings n moles from t_gas to t_out and itself stays under t_out.

    Automotive units already carry a metal filter that collects condensed phase and acts as a
    heat sink; this sizes that part rather than inventing one.
    """
    if t_gas <= t_out:
        return 0.0
    q = n_mol * M_N2 * CP_N2 * (t_gas - t_out)
    return q / (CP_SINK * (t_out - T_START))


def plenum_m3(n_mol, t_out, g_cap=G_CAP_PAYLOAD):
    """Smallest plenum holding the peak acceleration at the cap.

    a_peak = p0*A/m and p0 = nRT/V0, so V0 = nRT*A/(m*g*g_cap). It contains no L.
    """
    return n_mol * R_U * t_out * AREA / (M_PAY * G * g_cap)


def design(n_mol, t_gas, t_out=T_CEILING, g_cap=G_CAP_PAYLOAD):
    """One charge, cooled to t_out, sized to the cap, expanded down the tube."""
    m_sink = sink_kg(n_mol, t_gas, t_out)
    v0 = plenum_m3(n_mol, t_out, g_cap)
    p0 = n_mol * R_U * t_out / v0
    w = pc.work(p0, v0)                       # precharged's closed expansion, unmodified
    net = w - FRICTION_N * STROKE
    m_plenum = pc.chamber_kg(v0, p0)
    return dict(n_mol=n_mol, t_gas=t_gas, t_out=t_out,
                plenum_l=v0 * 1e3, p0_bar=p0 / 1e5,
                a_peak_g=p0 * AREA / M_PAY / G,
                work_J=w, net_J=net,
                v_exit=math.sqrt(2.0 * net / M_PAY) if net > 0 else 0.0,
                gas_kg=n_mol * M_N2, sink_kg=m_sink, plenum_kg=m_plenum)


def per_cell_kg(d, generant_kg=GENERANT_LO):
    return generant_kg + d['plenum_kg'] + d['sink_kg'] + HOUSING_KG


# A47's model with the pyrotechnic device as a shot-scope element that can itself fail. Same
# shape as fmea_gen6.ELEMENTS_GEN6_BACKUP: it deletes nothing the gas drive needs, it makes the
# drive satellite-forfeiting by giving every cell its own way out.
ELEMENTS_GEN6_PYRO = [
    e for e in g6.ELEMENTS_GEN6
    if not (e[1] == "shared" and e[0] in ("Gas reservoir", "Fill valve", "Fire valve",
                                          "Piston and seals", "Chamber"))
] + [("Drive, gas or pyrotechnic ejector", "shot", 1, "one",
      "A per-cell gas generator makes the drive satellite-forfeiting instead of manifest-"
      "forfeiting. One-shot, which the carriage already is, and it cannot be tested before "
      "flight, which the spring could have been")]

UNPRICED = [
    "range safety: twelve initiators on a launch vehicle is a licensing question, not an "
    "engineering one, and no file in this repository has ever priced it",
    "ordnance handling: integration, transport and storage all change category",
    "shelf life: a generant has one, and the standby interval runs from integration to the "
    "last shot -- the same problem A39 recorded against gas and A53 against a held spring",
    "hazard classification for twelve units in one magazine, including sympathetic initiation",
    "a fired generator cannot be tested before flight; a spring could have been proof-loaded",
    "the zonal cooling model assumes sink equilibrium inside a ~30 ms discharge and nothing "
    "here establishes that it is reached",
]


def main():
    fails = pc.check_against_parameters()
    if fails:
        raise SystemExit(f"design-point drift: {fails}")

    # band 1: the register's own arithmetic
    e_tube = FRICTION_N * STROKE
    e_spring = 0.5 * M_PAY * V_TARGET ** 2

    print(f"A65 pyrotechnic per-cell ejector. Stroke {STROKE:.2f} m, bore {pc.BORE*1e3:.3f} mm, "
          f"swept {AREA*STROKE*1e3:.4f} L")
    print(f"  friction work over the stroke   {e_tube:9.2f} J   (P81 carries 667.2)")
    print(f"  a 1.5 m/s spring stores         {e_spring:9.2f} J   (A53 carries 4.5)")
    print(f"  shortfall                       {e_tube/e_spring:9.1f}x  (P81 carries 148)\n")

    lo = design(MOL_LO, T_GAS_LO)
    hi = design(MOL_HI, T_GAS_HI)
    m_lo = per_cell_kg(lo)
    total_lo = m_lo * N_CELLS
    per_sat = (ADDED_BASE_KG + STORE_KG + total_lo) / N_CELLS

    print(f"{'':26s} {'bottom of class':>16s} {'top of class':>14s}")
    rows = [('charge, mol', 'n_mol', '{:.2f}'), ('gas temperature K', 't_gas', '{:.0f}'),
            ('cooled to K', 't_out', '{:.0f}'), ('sink kg', 'sink_kg', '{:.4f}'),
            ('plenum L', 'plenum_l', '{:.4f}'), ('p0 bar', 'p0_bar', '{:.2f}'),
            ('peak g', 'a_peak_g', '{:.2f}'), ('work J', 'work_J', '{:.1f}'),
            ('net of friction J', 'net_J', '{:.1f}'), ('exit m/s', 'v_exit', '{:.2f}'),
            ('plenum vessel kg', 'plenum_kg', '{:.4f}')]
    for label, key, fmt in rows:
        print(f"{label:26s} {fmt.format(lo[key]):>16s} {fmt.format(hi[key]):>14s}")

    print(f"\nper cell at the bottom of the class, {GENERANT_LO*1e3:.0f} g generant:")
    print(f"  generant  {GENERANT_LO:.4f}   plenum {lo['plenum_kg']:.4f}   "
          f"sink {lo['sink_kg']:.4f}   housing {HOUSING_KG:.4f} (declared guess)")
    print(f"  total per cell {m_lo:.4f} kg   x12 {total_lo:.4f} kg   "
          f"per satellite {per_sat:.4f} kg")

    pyro = g6.score(ELEMENTS_GEN6_PYRO)
    plain = g6.score(g6.ELEMENTS_GEN6)
    print(f"\nA47 re-run, the ejector a shot-scope element that can fail:")
    print(f"  Gen6 alone      {plain['expected_at_r99']:.3f} satellites at r = 0.99")
    print(f"  Gen6 + pyro     {pyro['expected_at_r99']:.3f}")

    # band 10: the whole published class
    print("\nband 10, the published class:")
    print(f"  {'mol':>5s} {'T gas K':>8s} {'plenum L':>9s} {'p0 bar':>8s} {'sink kg':>8s} "
          f"{'work J':>8s} {'exit m/s':>9s} {'per cell kg':>12s} {'plenum<=2L':>11s}")
    sweep = []
    for n_mol in (0.5, 0.6, 0.7, 0.8, 0.9):
        for t_gas in (1000.0, 1200.0, 1400.0):
            d = design(n_mol, t_gas)
            mc = per_cell_kg(d)
            ok = d['plenum_l'] <= CHAMBER_L_EXISTING
            sweep.append(dict(d, per_cell_kg=mc, plenum_within=ok))
            print(f"  {n_mol:5.1f} {t_gas:8.0f} {d['plenum_l']:9.4f} {d['p0_bar']:8.2f} "
                  f"{d['sink_kg']:8.4f} {d['work_J']:8.1f} {d['v_exit']:9.2f} {mc:12.4f} "
                  f"{'yes' if ok else 'NO':>11s}")

    top_usable = hi['plenum_l'] <= CHAMBER_L_EXISTING and hi['a_peak_g'] <= G_CAP_PAYLOAD + 1e-6

    bands = [
        ('1', 'reproduces the register: 667.2 J of friction work and a 4.5 J spring, within 1 %',
         f"{e_tube:.1f} J and {e_spring:.1f} J",
         abs(e_tube - 667.2) / 667.2 <= 0.01 and abs(e_spring - 4.5) / 4.5 <= 0.01),
        ('2', 'bottom of the class, cooled to the ceiling, exceeds 667.2 J over the 8.0 m stroke',
         f"{lo['work_J']:.1f} J, {lo['work_J']/e_tube:.2f}x", lo['work_J'] > e_tube),
        ('3', f'the plenum the {G_CAP_PAYLOAD:.0f} g cap requires is <= the existing '
              f'{CHAMBER_L_EXISTING:.1f} L chamber',
         f"{lo['plenum_l']:.4f} L", lo['plenum_l'] <= CHAMBER_L_EXISTING),
        ('4', f'per-cell mass <= {PER_CELL_KG_BAND:.2f} kg (A53 band 1, unchanged)',
         f"{m_lo:.4f} kg", m_lo <= PER_CELL_KG_BAND),
        ('5', f'twelve of them keep added mass per satellite <= {TARGET_KG:.1f} kg',
         f"{total_lo:.4f} kg total, {per_sat:.4f} kg/sat", per_sat <= TARGET_KG),
        ('6', f'gas entering the tube <= ADR-035\'s {T_CEILING:.0f} K, with the sink costed in '
              f'band 4',
         f"{lo['t_out']:.0f} K on a {lo['sink_kg']*1e3:.1f} g sink",
         lo['t_out'] <= T_CEILING and lo['sink_kg'] > 0.0),
        ('7', 'exit velocity firing alone, after friction, >= 1.0 m/s',
         f"{lo['v_exit']:.2f} m/s", lo['v_exit'] >= 1.0),
        ('8', 'A47 re-run with the device able to fail returns >= 9.0 satellites at r = 0.99',
         f"{pyro['expected_at_r99']:.3f}", pyro['expected_at_r99'] >= 9.0),
        ('9', 'the unpriced costs are named and not counted as a pass',
         f"{len(UNPRICED)} named", len(UNPRICED) >= 5),
        ('10', 'REPORT: the published class, and whether its top is usable',
         f"{len(sweep)} points; top of class "
         f"{'usable' if top_usable else 'NOT usable at the cap'}", None),
    ]
    print()
    for n, text, got, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f"  {n:>2s}  {mark:6s} {text}")
        print(f"        {got}")

    print("\nunpriced, named and not counted as a pass:")
    for u in UNPRICED:
        print(f"  - {u}")

    out = dict(
        analysis='A65', bands_declared_commit='HEAD~1',
        note='model output. The gas generator is a TECHNOLOGY CLASS -- solid-propellant '
             'automotive restraint inflators -- with published ranges declared at the point of '
             'use: %.1f-%.1f mol per unit, %.0f-%.0f K total gas temperature, %.0f-%.0f g of '
             'solid generant. No product, supplier or organisation is named. Housing is a '
             'DECLARED GUESS of %.2f kg per cell with no derivation, carried from A53 so the two '
             'runs compare. The zonal cooling treatment assumes the sink reaches equilibrium '
             'with the whole charge before expansion begins.'
             % (MOL_LO, MOL_HI, T_GAS_LO, T_GAS_HI, GENERANT_LO * 1e3, GENERANT_HI * 1e3,
                HOUSING_KG),
        friction_work_J=e_tube, spring_J=e_spring, shortfall=e_tube / e_spring,
        bottom_of_class=lo, top_of_class=hi, top_of_class_usable=bool(top_usable),
        per_cell_kg=m_lo, total_kg=total_lo, per_satellite_kg=per_sat,
        housing_kg=HOUSING_KG, generant_kg=GENERANT_LO,
        a47_gen6=plain['expected_at_r99'], a47_with_pyro=pyro['expected_at_r99'],
        unpriced=UNPRICED, sweep=sweep,
        bands=[dict(n=n, band=t, got=g,
                    passed=(None if o is None else bool(o))) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'pyro_ejector.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
