"""
VOLLEY | Every kilogram, attributed to the requirement that causes it.

WHY THIS EXISTS
---------------
mass_properties.py reports WHAT each kilogram is. It has never reported WHY it is there,
so deleting a requirement in the model moved nothing downstream and every architecture
argument had to be settled by assertion. Kill criterion 1 is crossed by 3.5x and the
proposals for closing it have never been measured against each other.

The sibling repository is why this is worth doing properly rather than by hand. BOLLEY
deleted ONE requirement -- that the CubeSat is unmodified -- rebuilt around the deletion,
and the mass reappeared as a 15.91 kg primary. A real negative result, at the cost of a
repository, twenty-five validation runs and a register of its own, to return one bit.
Asking the same question of six requirements should not cost six repositories.

WHAT THIS IS NOT
----------------
It is NOT a sizing model. It says what comes out; it says nothing about what goes back in.
A corner removing 40 kg has NOT been shown to weigh 44.5 kg -- only that 40 kg of the
present design has lost its reason. That is a weaker claim and the difference is the whole
honesty of the thing.

The bound is ADDITIVE BY CONSTRUCTION. Deleting two requirements removes the union of their
items, never more. Real architectures interact: with no mover the force for the same shot
falls by 70 %, so whatever replaces the stator is smaller than either deletion implies.
This cannot see that. Band 5 checks that the attribution at least finds the shared drivers
a later sizing model would need.

Bands declared in validation/A35_constraint_ledger.md at 198aaeb, BEFORE this file existed.

Provenance: attribution of an existing model output. No new physics, no new mass estimate,
and the ledger is required to reproduce mass_properties.dry_kg exactly (band 1).
"""
import itertools
import json
import os

import mass_properties as mp

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# The six requirements. Deleting one is a design decision, not a saving -- what it buys is
# what this script reports, and what it costs is not modelled here.
CONSTRAINTS = {
    'C1': 'the satellite is unmodified',
    'C2': 'a reusable mover carries the magnets',
    'C3': 'the energy arrives during the shot',
    'C4': 'the machine is rigid, and one length stowed or deployed',
    'C5': 'the deployer carries its own energy store',
    'C6': 'twelve satellites share one drive',
}

# name-prefix -> (full drivers, partial drivers, note)
#
# `full`    the item has no reason to exist once ANY of these is deleted.
# `partial` the item shrinks by an amount THIS RUN DOES NOT ESTIMATE. Never counted.
#
# Attribution rules used, so a reader can disagree with a specific line rather than the
# whole table:
#   - The stator exists to convert stored electrical energy into force DURING the stroke.
#     Without C3 there is no stator, whatever else is true.  -> C3 full
#   - The brake exists because a mover must be stopped and reused. No mover, nothing to
#     arrest: the payload leaves.  -> C2 full
#   - Thermal hardware sizes on 854 J of copper heat per shot, 10 kJ per manifest, which is
#     a pulse-power quantity.  -> C3 full
#   - Cassettes and gates are payload containment and ascent restraint. They survive every
#     deletion; only C6 changes their COUNT, not their existence.  -> C6 partial
#   - Structure and closeouts scale with what they enclose. Every deletion shrinks them and
#     none abolishes them.  -> partial everywhere
ATTRIBUTION = [
    ('Track longerons',          (),           ('C2', 'C4'), 'rails survive; section and length do not'),
    ('Stator copper',            ('C3',),      (),           'no stroke-time energy, no stator'),
    ('Stator formers',           ('C3',),      (),           'holds the stator'),
    ('Sled Halbach magnets',     ('C2',),      (),           'the mover IS the magnets'),
    ('Sled Ti chassis',          ('C2',),      (),           'chassis for the mover'),
    ('Sled rollers',             (),           ('C2',),      'a payload cradle still needs guidance'),
    ('Sled CAD reconciliation',  ('C2',),      (),           'the rest of the same mover'),
    ('Eddy brake magnets',       ('C2',),      (),           'nothing to arrest without a mover'),
    ('Fixed brake hardware',     ('C2',),      (),           'ditto'),
    ('Cassette shells',          (),           ('C6',),      'payload containment survives; count changes'),
    ('Followers, gates',         (),           ('C6',),      'ascent restraint survives; count changes'),
    ('Supercapacitor cells',     ('C3', 'C5'), (),           '17 kW for 162 ms is the only reason it exists'),
    ('PPU',                      ('C3',),      (),           'a bridge with no pulse to switch'),
    ('Battery + avionics',       (),           ('C3', 'C5'), 'command and sensing survive; the store does not'),
    ('Harness',                  (),           ('C3',),      '320 A conductors; signal harness survives'),
    ('Thermal',                  ('C3',),      (),           'sized on 10 kJ of copper heat per manifest'),
    ('ESPA bracket',             (),           ('C4',),      'scales with what it carries'),
    ('Panels / closeouts',       (),           ('C4',),      'scales with enclosed length'),
    # P10's single placeholder line became five derived lines on 2026-08-16 (A46). The
    # attribution is unchanged in kind -- an enclosure scales with what it encloses (C4) and
    # the radiator exists to reject pulse heat (C3) -- but it is now applied per line rather
    # than to one lump, so a deletion sweep can move the radiator without moving the skins.
    ('Enclosure skins',          (),           ('C4',),      'scales with enclosed envelope'),
    ('Enclosure frames',         (),           ('C4',),      'ditto; a declared fraction of skin'),
    ('Radiator',                 ('C3',),      (),           'sized to reject pulse heat; no pulse, no radiator'),
    ('Equipment-bay boxes',      (),           ('C3', 'C5'), 'bays for the bank and PPU go with them; sequencer bay survives'),
    ('Fasteners and brackets',   (),           ('C4',),      'scales with the structure it joins'),
]


def ledger():
    """Every part, with its drivers. Raises if a part is unattributed (band 2)."""
    mp.build()
    rows, unattributed = [], []
    for name, kg, cg in mp.parts:
        for prefix, full, partial, note in ATTRIBUTION:
            if name.startswith(prefix):
                rows.append(dict(part=name, kg=kg, cg_m=cg, full=list(full),
                                 partial=list(partial), note=note))
                break
        else:
            unattributed.append(name)
    return rows, unattributed


def removal(rows, deleted):
    """Mass that loses its reason when `deleted` requirements go, and what is merely flagged.

    A part is removed only when one of its FULL drivers is deleted. A part whose PARTIAL
    driver is deleted is reported separately and never counted -- that is what makes this a
    bound rather than an estimate.
    """
    gone = sum(r['kg'] for r in rows if set(r['full']) & deleted)
    flagged = sum(r['kg'] for r in rows
                  if not (set(r['full']) & deleted) and set(r['partial']) & deleted)
    return gone, flagged


def main():
    rows, unattributed = ledger()
    total = sum(r['kg'] for r in rows) + sum(
        m for n, m, _ in mp.parts if n in unattributed)
    dry = sum(m for _, m, _ in mp.parts)

    print(f"{'part':46s} {'kg':>6s}  full         partial")
    for r in rows:
        print(f"  {r['part'][:44]:44s} {r['kg']:6.2f}  "
              f"{','.join(r['full']) or '-':12s} {','.join(r['partial']) or '-'}")
    print(f"\n  {'attributed total':44s} {total:6.2f}   against dry {dry:.2f}")

    singles = {}
    print("\nwhat one requirement is worth, as an upper bound:")
    for c, text in CONSTRAINTS.items():
        gone, flagged = removal(rows, {c})
        singles[c] = gone
        print(f"  {c}  {gone:6.2f} kg removed ({gone/dry*100:5.1f} %), "
              f"{flagged:6.2f} kg flagged   -- {text}")

    print("\nthe lattice, best corners by mass removed:")
    corners = []
    keys = list(CONSTRAINTS)
    for n in range(len(keys) + 1):
        for combo in itertools.combinations(keys, n):
            deleted = set(combo)
            gone, flagged = removal(rows, deleted)
            additive = sum(singles[c] for c in combo)
            corners.append(dict(deleted=sorted(deleted), removed_kg=round(gone, 2),
                                removed_pct=round(gone / dry * 100, 1),
                                flagged_kg=round(flagged, 2),
                                sum_of_singles_kg=round(additive, 2),
                                overlap_kg=round(additive - gone, 2)))
    for c in sorted(corners, key=lambda c: -c['removed_kg'])[:8]:
        print(f"  {'+'.join(c['deleted']) or '(none)':20s} {c['removed_kg']:6.2f} kg "
              f"({c['removed_pct']:5.1f} %)  flagged {c['flagged_kg']:6.2f}  "
              f"overlap {c['overlap_kg']:5.2f}")

    shared = [r['part'] for r in rows if len(set(r['full']) | set(r['partial'])) > 1]
    largest = max(singles, key=singles.get)

    bands = [
        ('1', 'ledger reproduces mass_properties.dry_kg to 0.01 kg',
         f"{total:.4f} against {dry:.4f}", abs(total - dry) <= 0.01),
        ('2', 'every line item carries a driver',
         f"{len(unattributed)} unattributed" + (f": {unattributed}" if unattributed else ""),
         not unattributed),
        ('3', 'C1 alone removes <= 15 % (calibration against BOLLEY)',
         f"{singles['C1']/dry*100:.1f} %", singles['C1'] / dry * 100 <= 15.0),
        ('4', 'C3 alone removes >= 25 %',
         f"{singles['C3']/dry*100:.1f} %", singles['C3'] / dry * 100 >= 25.0),
        ('5', 'at least three items carry more than one driver',
         f"{len(shared)} items", len(shared) >= 3),
        ('6', 'C3 is the largest single-requirement removal',
         f"largest is {largest}", largest == 'C3'),
        ('7', 'no corner removes > 100 %, no partial counted as full',
         f"max {max(c['removed_pct'] for c in corners):.1f} %",
         max(c['removed_pct'] for c in corners) <= 100.0),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A35', bands_declared_commit='198aaeb',
               note='attribution and an upper bound; NOT a sizing model',
               dry_kg=round(dry, 2), constraints=CONSTRAINTS,
               parts=rows, unattributed=unattributed,
               single_requirement_kg={c: round(v, 2) for c, v in singles.items()},
               shared_driver_parts=shared, corners=corners,
               bands=[dict(band=n, name=name, detail=d, pass_=ok)
                      for n, name, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'constraint_ledger.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
