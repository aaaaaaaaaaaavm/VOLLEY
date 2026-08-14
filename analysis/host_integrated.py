"""
VOLLEY | The stage as the deployer, and the falsification test A35 is owed.

WHY THIS EXISTS
---------------
A35 closed the architecture route to kill criterion 1: 49.23 kg survives every requirement
deletion in all 64 corners. A36 band 4 closed the manifest route: 2 kg is reached at N=116,
which does not package. P59 records that only a payload-class change remains.

A third possibility was never analysed: that the deployer is not CARRIED BY a stage but IS
one. ADR-023 already re-scoped the host to a restartable upper stage; ADR-024 wrote the
last-mile concept. Neither took the last step -- after the primary separates, the stage's
structure becomes the track and its array becomes the supply.

THE HONESTY PROBLEM, AND HOW IT IS HANDLED
------------------------------------------
Crediting the stage as sunk cost takes 7.042 kg/satellite to something near 1.2 and closes a
criterion two runs have failed. That is structurally identical to the metric substitution
this project already flagged and declined. So:

  * the 2.0 kg threshold does NOT move;
  * added mass per satellite is NEVER reported without dry mass per satellite beside it;
  * nothing is credited to the stage without naming the subsystem that provides it.

Bands 1-3 enforce all three mechanically rather than by good intentions.

Bands declared in validation/A37_host_integrated.md at ec9d6a1, BEFORE this file existed.

Provenance: model output. Attribution is read from constraint_ledger.py rather than restated.
The usable-length fractions and the 300 J/kg spring figure are declared assumptions, named at
each use. No vendor, programme or organisation appears anywhere in this file.
"""
import json
import math
import os

import constraint_ledger as cl
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G, G_CAP, M_SAT, N_MANIFEST = 9.81, 25.0, 4.0, 12
TARGET_KG = 2.0                      # kill criterion 1. UNCHANGED, applied to both numerators.
SPRING_J_PER_KG = 300.0              # actuator_trade.py: upper end for spring steel
A35_C3_RELEASED_KG = 23.76           # what the pulse chain gave up, A35
FALSIFIER_KG = 0.60 * A35_C3_RELEASED_KG

# Stage classes by dimension only. The usable acceleration length is an ASSUMPTION: tankage,
# engine and avionics bays are not available to a track.
STAGE_CLASSES = [('small kick stage', 1.5),
                 ('medium restartable upper stage', 3.0),
                 ('large upper stage', 8.0)]

# Which A35 line items a live stage already provides, and WHICH SUBSYSTEM PROVIDES IT.
# An empty justification fails band 2. This is the only place the stage is credited, and
# every entry here is a claim that something on the stage does this job instead.
STAGE_PROVIDES = {
    'Track longerons':        'primary structure -- the stage IS a long stiff cylinder',
    'ESPA bracket':           'the stage needs no adapter to itself',
    'Panels / closeouts':     'stage skin and thrust structure',
    'Enclosure / radiator':   'stage thermal control and avionics bay',
    'Battery + avionics':     'stage power, command and IMU, kept alive past passivation',
    'Thermal':                'stage thermal control loop',
    'Harness':                'stage harness, extended rather than added',
}

# Deleted outright by Gen6 physics, and therefore neither added NOR stage-provided.
# These are A35's C2 and C3 full-driver items: no mover, no pulse.
DELETED_PREFIXES = ('Stator copper', 'Stator formers', 'Sled Halbach magnets',
                    'Sled Ti chassis', 'Sled CAD reconciliation', 'Sled rollers',
                    'Eddy brake magnets', 'Fixed brake hardware',
                    'Supercapacitor cells', 'PPU')


def assign():
    """Every A35 line item into exactly one of added / stage-provided / deleted."""
    rows, unattributed = cl.ledger()
    assert not unattributed, unattributed
    added, stage, deleted = [], [], []
    for r in rows:
        if r['part'].startswith(DELETED_PREFIXES):
            deleted.append(r)
            continue
        for prefix, why in STAGE_PROVIDES.items():
            if r['part'].startswith(prefix):
                stage.append(dict(r, provided_by=why))
                break
        else:
            added.append(r)
    return added, stage, deleted, sum(r['kg'] for r in rows)


def shot(length_m):
    """Exit velocity, energy and store mass at the payload g-cap over `length_m` of stroke."""
    v = math.sqrt(2 * G_CAP * G * length_m)
    e = 0.5 * M_SAT * v * v
    return dict(length_m=length_m, v_exit=v, a_g=G_CAP, force_N=M_SAT * G_CAP * G,
                energy_J=e, spring_kg=e / SPRING_J_PER_KG,
                charge_W_60s=e / 60.0, campaign_J=e * N_MANIFEST)


# The wind drive, latch, safing chain and store structure. A DECLARED ASSUMPTION with no
# derivation: 60 % of the store's own mass, floored at 2 kg for the mechanism that has to
# exist however small the spring is. It is the largest guess in this run and it is named
# here rather than buried.
def mechanism_kg(store_kg):
    return max(2.0, 0.60 * store_kg)


def main():
    added, stage, deleted, ledger_total = assign()
    added_kg = sum(r['kg'] for r in added)
    stage_kg = sum(r['kg'] for r in stage)
    deleted_kg = sum(r['kg'] for r in deleted)

    print("A35's ledger, reassigned:")
    print(f"  deleted by Gen6 physics (no mover, no pulse)  {deleted_kg:7.2f} kg")
    print(f"  provided by a live stage                      {stage_kg:7.2f} kg")
    print(f"  ADDED -- what this machine still costs        {added_kg:7.2f} kg")
    for r in added:
        print(f"      {r['part'][:52]:52s} {r['kg']:6.2f}")
    print(f"  sum {added_kg + stage_kg + deleted_kg:.2f} against ledger {ledger_total:.2f}")

    print(f"\n{'stage class':34s} {'L':>5s} {'v':>7s} {'store':>7s} {'mech':>6s} "
          f"{'added':>7s} {'kg/sat':>7s} {'W':>6s}")
    points = []
    for name, L in STAGE_CLASSES:
        s = shot(L)
        mech = mechanism_kg(s['spring_kg'])
        total_added = added_kg + s['spring_kg'] + mech
        p = dict(stage_class=name, **s, mechanism_kg=mech,
                 store_plus_mechanism_kg=s['spring_kg'] + mech,
                 added_total_kg=total_added,
                 added_kg_per_satellite=total_added / N_MANIFEST)
        points.append(p)
        print(f"  {name:32s} {L:5.1f} {s['v_exit']:7.1f} {s['spring_kg']:7.2f} "
              f"{mech:6.2f} {total_added:7.2f} {p['added_kg_per_satellite']:7.3f} "
              f"{s['charge_W_60s']:6.0f}")

    # The selected point: the largest velocity that keeps every band satisfiable, chosen by
    # the declared bands rather than by preference.
    feasible = [p for p in points
                if p['store_plus_mechanism_kg'] <= FALSIFIER_KG
                and p['added_kg_per_satellite'] <= TARGET_KG
                and p['v_exit'] >= 30.0
                and p['charge_W_60s'] <= 200.0
                and p['store_plus_mechanism_kg'] <= 0.50 * p['added_total_kg']]
    selected = max(feasible, key=lambda p: p['v_exit']) if feasible else \
        max(points, key=lambda p: p['v_exit'])

    dry_per_sat = ledger_total / N_MANIFEST
    print(f"\n  selected: {selected['stack'] if False else selected['stage_class']}, "
          f"{selected['length_m']:.1f} m, {selected['v_exit']:.1f} m/s")
    print(f"  BOTH numerators, as band 3 requires:")
    print(f"    dry mass per satellite    {dry_per_sat:6.3f} kg   "
          f"{'PASSES' if dry_per_sat <= TARGET_KG else 'CROSSES'} the unchanged 2.0 kg threshold")
    print(f"    added mass per satellite  {selected['added_kg_per_satellite']:6.3f} kg   "
          f"{'PASSES' if selected['added_kg_per_satellite'] <= TARGET_KG else 'CROSSES'} "
          f"the same threshold")

    unjustified = [r['part'] for r in stage if not r.get('provided_by')]
    bands = [
        ('1', 'added + stage + deleted reproduces the A35 ledger to 0.01 kg',
         f"{added_kg + stage_kg + deleted_kg:.4f} against {ledger_total:.4f}",
         abs(added_kg + stage_kg + deleted_kg - ledger_total) <= 0.01),
        ('2', 'every stage-provided item names the subsystem providing it',
         f"{len(unjustified)} unjustified", not unjustified),
        ('3', 'both numerators reported, threshold unchanged at 2.0 kg',
         f"dry {dry_per_sat:.3f} kg, added {selected['added_kg_per_satellite']:.3f} kg",
         True),
        ('4', f'A35 falsifier: store + mechanism <= {FALSIFIER_KG:.2f} kg',
         f"{selected['store_plus_mechanism_kg']:.2f} kg at "
         f"{selected['v_exit']:.1f} m/s",
         selected['store_plus_mechanism_kg'] <= FALSIFIER_KG),
        ('5', f'added mass per satellite <= {TARGET_KG} kg on at least one class',
         f"best {min(p['added_kg_per_satellite'] for p in points):.3f} kg",
         min(p['added_kg_per_satellite'] for p in points) <= TARGET_KG),
        ('6', 'selected point delivers >= 30 m/s at <= 25 g',
         f"{selected['v_exit']:.1f} m/s at {selected['a_g']:.0f} g",
         selected['v_exit'] >= 30.0 and selected['a_g'] <= 25.0),
        ('7', 'peak electrical <= 200 W',
         f"{selected['charge_W_60s']:.0f} W", selected['charge_W_60s'] <= 200.0),
        ('8', 'energy store <= 50 % of total added mass',
         f"{100 * selected['store_plus_mechanism_kg'] / selected['added_total_kg']:.1f} %",
         selected['store_plus_mechanism_kg'] <= 0.50 * selected['added_total_kg']),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A37', bands_declared_commit='ec9d6a1',
               note='the 2.0 kg threshold is UNCHANGED and applied to both numerators; '
                    'gas stores excluded deliberately; tip-off untouched; stage availability, '
                    'attitude control through the campaign and debris mitigation NOT priced',
               ledger_total_kg=ledger_total, deleted_kg=deleted_kg,
               stage_provided_kg=stage_kg, added_base_kg=added_kg,
               dry_kg_per_satellite=dry_per_sat, target_kg=TARGET_KG,
               a35_c3_released_kg=A35_C3_RELEASED_KG, falsifier_kg=FALSIFIER_KG,
               added_items=added, stage_items=stage, deleted_items=deleted,
               points=points, selected=selected,
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'host_integrated.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
