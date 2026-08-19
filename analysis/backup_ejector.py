"""
VOLLEY | The per-cell backup ejector, designed rather than priced.

WHY THIS EXISTS
---------------
A47 found it worth six times the entire architecture change: Gen5 to Gen6 moved expected
delivery by 0.37 satellites, and a per-cell ejector moves it by 2.27, because it changes the
structure rather than the count -- a mechanism in every cell makes the drive satellite-
forfeiting instead of manifest-forfeiting, which is the only move that touches what E30 says.

A47 priced its EFFECT and did not design it. P75 says so. This asks what it weighs, whether it
fits the cell, and whether it can actually do the job.

Bands declared in validation/A53_backup_ejector.md at HEAD, BEFORE this file existed.

Provenance: model output. Spring energy density from actuator_trade.py's upper end for spring
steel, which flatters a real spring. The latch and guide mass is a DECLARED guess, named below.
Friction is A41's allowance over the full remaining stroke, which is the pessimistic reading and
is stated as such.
"""
import json
import os

import fmea
import fmea_gen6 as g6

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

M_PAY = 4.0
V_TARGET = 1.5                # m/s, the clearance velocity a spring dispenser class gives
SPRING_J_PER_KG = 300.0       # actuator_trade.py, upper end for spring steel
LATCH_GUIDE_KG = 0.12         # DECLARED GUESS per cell: latch, guide rail, baseplate. No
                              # derivation. It is the largest assumption in this run.
N_CELLS = 12
STROKE_M = 2.18               # gen6_drive
FRICTION_N = 83.40371375447981   # A41 band 8's allowance
PITCH_Z_MM = 104.0            # magazine.satellite_pitch_z
SHOT_J = 1864.8
ADDED_BASE_KG = 11.452976
STORE_KG = 5.38
TARGET_KG = 2.0


def spring_kg(energy_J):
    return energy_J / SPRING_J_PER_KG


def clearance_energy():
    """Kinetic energy for a clean 1.5 m/s departure."""
    return 0.5 * M_PAY * V_TARGET ** 2


def tube_clearing_energy():
    """Work to push the payload the length of the tube against the seal.

    This is the pessimistic reading and it is the honest one: if the drive is dead, the payload
    is in a 2.18 m sealed tube with the piston behind it, and something has to move both.
    """
    return FRICTION_N * STROKE_M


def main():
    e_clear = clearance_energy()
    e_tube = tube_clearing_energy()
    m_spring_clear = spring_kg(e_clear)
    m_spring_tube = spring_kg(e_tube)

    print(f"clearance energy, 1.5 m/s on {M_PAY:.0f} kg      {e_clear:9.2f} J  "
          f"-> {m_spring_clear*1e3:7.1f} g of spring")
    print(f"energy to clear {STROKE_M:.2f} m of sealed tube  {e_tube:9.2f} J  "
          f"-> {m_spring_tube*1e3:7.1f} g of spring")
    print(f"  ratio                                {e_tube/e_clear:9.1f}x\n")

    per_cell_clear = m_spring_clear + LATCH_GUIDE_KG
    per_cell_tube = m_spring_tube + LATCH_GUIDE_KG
    total_clear = per_cell_clear * N_CELLS
    total_tube = per_cell_tube * N_CELLS

    print(f"{'':28s} {'per cell':>10s} {'x12':>9s} {'kg/sat after':>14s}")
    for label, pc_, tot in (("clearance only", per_cell_clear, total_clear),
                            ("clearing the tube", per_cell_tube, total_tube)):
        per_sat = (ADDED_BASE_KG + STORE_KG + tot) / N_CELLS
        print(f"{label:28s} {pc_:9.3f}  {tot:8.3f}  {per_sat:13.3f}")

    per_sat_clear = (ADDED_BASE_KG + STORE_KG + total_clear) / N_CELLS
    per_sat_tube = (ADDED_BASE_KG + STORE_KG + total_tube) / N_CELLS

    # band 5 and 6: A47's model with the ejector as a shot-scope element that can itself fail
    backup = g6.score(g6.ELEMENTS_GEN6_BACKUP)
    plain = g6.score(g6.ELEMENTS_GEN6)
    print(f"\nA47 re-run with the ejector as a shot-scope element that can fail:")
    print(f"  Gen6 alone                {plain['expected_at_r99']:.3f} satellites at r = 0.99")
    print(f"  Gen6 + ejector            {backup['expected_at_r99']:.3f}")

    # does the ejector fit the cell it must live in?
    spring_len_mm = 60.0     # DECLARED: a compressed coil for this energy, order 60 mm
    fits = spring_len_mm <= PITCH_Z_MM

    bands = [
        ('1', f'ejector mass per cell at {V_TARGET} m/s <= 0.25 kg',
         f"{per_cell_clear:.3f} kg", per_cell_clear <= 0.25),
        ('2', 'twelve ejectors <= 3.0 kg and per satellite stays <= 2.0 kg',
         f"{total_clear:.3f} kg, {per_sat_clear:.3f} kg/sat",
         total_clear <= 3.0 and per_sat_clear <= TARGET_KG),
        ('3', f'fits inside the existing {PITCH_Z_MM:.0f} mm cell pitch',
         f"{spring_len_mm:.0f} mm", fits),
        ('4', 'stored energy <= 2 % of the gas shot',
         f"{e_clear/SHOT_J*100:.3f} %", e_clear / SHOT_J <= 0.02),
        ('5', 'A47 re-run confirms >= 9.0 satellites at r = 0.99',
         f"{backup['expected_at_r99']:.3f}", backup['expected_at_r99'] >= 9.0),
        ('6', "the ejector's own failure rate is included as a shot-scope element",
         'included' if any(e[1] == 'shot' for e in g6.ELEMENTS_GEN6_BACKUP) else 'NOT',
         any(e[1] == 'shot' for e in g6.ELEMENTS_GEN6_BACKUP)),
        ('7', f'firing alone clears the tube at >= 1.0 m/s',
         f"needs {e_tube:.1f} J, has {e_clear:.1f} J", e_clear >= e_tube),
        ('8', 'the standby problem is stated',
         'stated: held compressed from integration to the last shot', True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A53', bands_declared_commit='HEAD~1',
               note='spring energy density from actuator_trade.py upper end, which flatters a '
                    'real spring. Latch and guide mass is a declared guess of %.2f kg per cell '
                    'with no derivation and is the largest assumption here. Friction is A41 band '
                    "8's ALLOWANCE over the full remaining stroke -- the pessimistic reading, "
                    'and P67 has never measured it.' % LATCH_GUIDE_KG,
               clearance_J=e_clear, tube_clearing_J=e_tube, ratio=e_tube / e_clear,
               per_cell_clearance_kg=per_cell_clear, per_cell_tube_kg=per_cell_tube,
               total_clearance_kg=total_clear, total_tube_kg=total_tube,
               per_sat_clearance=per_sat_clear, per_sat_tube=per_sat_tube,
               a47_gen6=plain['expected_at_r99'], a47_with_ejector=backup['expected_at_r99'],
               latch_guide_kg=LATCH_GUIDE_KG, spring_len_mm=spring_len_mm,
               standby='a spring held compressed from integration to the last shot; A39 recorded '
                       'the same class of problem against the gas option',
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'backup_ejector.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
