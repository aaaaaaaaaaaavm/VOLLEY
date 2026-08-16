"""
VOLLEY | Gen6's failure structure, scored on Gen5's basis.

WHY THIS EXISTS
---------------
E30, live since 2026-08-10: a spring dispenser is twelve independent one-shot mechanisms in
parallel and one failure costs one satellite, where VOLLEY is one mechanism in series with
itself cycled twelve times. docs/FMEA.md answered that for Gen5 -- nine of thirteen elements
forfeit the remaining manifest, r >= 0.99326 to match a spring on delivered life. It contains
no mention of Gen6. The architecture changed on 2026-08-14 and the failure analysis did not.

THE MODEL IS IMPORTED, NOT REWRITTEN
------------------------------------
fmea.campaign() and fmea.required_element_r() are used unchanged, with fmea.ELEMENTS
monkey-patched for the Gen6 list. Gen5 and Gen6 are therefore scored by identical arithmetic
and the only thing that differs is what is in the machine. A second model would make the
comparison meaningless.

Bands declared in validation/A47_gen6_fmea.md at HEAD, BEFORE this file existed.

Provenance: model output. No common-cause failures, elements independent, no wear-out, and one
reliability shared across elements -- the same assumptions fmea.py already makes, kept so the
two architectures are comparable rather than because they are right.
"""
import json
import os

import fmea

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# Every Gen5 element, and what ADR-032 does to it. Band 2 requires this to be complete.
FATE = {
    "Sled chassis and rollers":        ("deleted",  "no mover"),
    "Stator winding":                  ("deleted",  "no stator"),
    "Power converter (SiC bridge)":    ("deleted",  "no pulse to switch"),
    "Energy store (bank or flywheel)": ("replaced", "gas reservoir and chamber"),
    "Avionics and shot sequencer":     ("retained", "still one sequencer for twelve shots"),
    "Position sensing / commutation":  ("deleted",  "nothing to commutate; a pressure "
                                                    "transducer replaces it, not a resolver"),
    "Eddy brake":                      ("deleted",  "nothing to arrest"),
    "Sled return":                     ("deleted",  "the carriage is not recovered"),
    "Launch lock release":             ("retained", "one-shot, unchanged"),
    "Cassette follower drive":         ("retained", "magazine unchanged"),
    "Escapement":                      ("retained", "magazine unchanged"),
    "Retention gate (2 x D9 pins)":    ("retained", "magazine unchanged"),
    "Individual release event":        ("replaced", "the cradle, which does not exist"),
}

# Gen6's list. Shared elements forfeit the remaining manifest exactly as Gen5's did.
ELEMENTS_GEN6 = [
    ("Gas reservoir", "shared", 12, "all remaining",
     "One 9.55 L bottle feeds twelve shots. A leak is unrecoverable and A39 recorded gas as "
     "the store that 'leaks; needs a seal that holds from integration to the last shot'"),
    ("Fill valve", "shared", 12, "all remaining",
     "Cycles once per shot. Undrawn -- A41 allows 1.5 kg for piston, seals and valving and "
     "designs none of it"),
    ("Fire valve", "shared", 12, "all remaining", "Ditto"),
    ("Piston and seals", "shared", 12, "all remaining",
     "P67: its friction owns 93.4 % of the velocity dispersion and has never been measured. "
     "The same component is critical on reliability and on precision"),
    ("Chamber", "shared", 12, "all remaining", "2 L pressure vessel, cycled twelve times"),
    ("Avionics and shot sequencer", "shared", 12, "all remaining",
     "Carried across from Gen5 unchanged"),
    ("Host stage keep-alive", "shared", 12, "all remaining",
     "NEW IN GEN6 AND NOT IN GEN5. The machine now depends on a vehicle somebody else owns "
     "staying alive past passivation. No launch provider has agreed to it"),
    ("Launch lock release", "shared", 1, "all", "One-shot, unchanged from Gen5"),
    ("Cassette follower drive", "cassette", 6, "six", "Magazine unchanged"),
    ("Escapement", "cassette", 6, "six", "Magazine unchanged"),
    ("Retention gate (2 x D9 pins)", "cassette", 6, "six", "Magazine unchanged"),
    ("Cradle release", "shot", 1, "one",
     "201.7 N per contact releasing inside 1 N. The mechanism does not exist"),
]

# Band 8: a small spring per cell, guaranteeing clearance if the drive is dead.
ELEMENTS_GEN6_BACKUP = [
    (n, s, c, cost, note) for (n, s, c, cost, note) in ELEMENTS_GEN6
    if not (s == "shared" and n in ("Gas reservoir", "Fill valve", "Fire valve",
                                    "Piston and seals", "Chamber"))
] + [("Drive, gas or backup ejector", "shot", 1, "one",
      "A per-cell spring makes the drive satellite-forfeiting instead of manifest-forfeiting. "
      "It does not deliver the delta-v, only the clearance")]

TARGET = 7.95      # satellites, fmea.py's delivered-life target


def score(elements):
    saved = fmea.ELEMENTS
    fmea.ELEMENTS = elements
    try:
        shared = [e for e in elements if e[1] == 'shared']
        r_req = fmea.required_element_r(TARGET)
        exp99, _ = fmea.campaign(0.99, 0.99, 0.99)
        exp_req, _ = fmea.campaign(r_req, r_req, r_req)
        return dict(n_elements=len(elements), n_shared=len(shared),
                    shared_names=[e[0] for e in shared],
                    required_r=r_req, expected_at_r99=exp99, expected_at_required=exp_req)
    finally:
        fmea.ELEMENTS = saved


def main():
    gen5 = score(fmea.ELEMENTS)
    gen6 = score(ELEMENTS_GEN6)
    backup = score(ELEMENTS_GEN6_BACKUP)

    print(f"{'':28s} {'elements':>9s} {'shared':>7s} {'required r':>11s} "
          f"{'delivered @ r=0.99':>19s}")
    for name, s in (("Gen5, as published", gen5), ("Gen6", gen6),
                    ("Gen6 + per-cell ejector", backup)):
        print(f"{name:28s} {s['n_elements']:9d} {s['n_shared']:7d} "
              f"{s['required_r']:11.5f} {s['expected_at_r99']:19.3f}")
    print(f"{'a spring dispenser':28s} {'12':>9s} {0:7d} {'--':>11s} "
          f"{12 * 0.99:19.3f}   (each failure costs one)")

    print("\nGen5 elements, and what ADR-032 does to each:")
    for name, scope, cycles, cost, note in fmea.ELEMENTS:
        fate, why = FATE[name]
        print(f"  {fate:9s}  {name:34s} {why}")
    missing = [e[0] for e in fmea.ELEMENTS if e[0] not in FATE]

    print("\nGen6 shared elements -- each forfeits the remaining manifest:")
    for n in gen6['shared_names']:
        print(f"  {n}")

    bands = [
        ('1', "the imported model reproduces Gen5's published 0.99326 within 0.0001",
         f"{gen5['required_r']:.5f}", abs(gen5['required_r'] - 0.99326) <= 1e-4),
        ('2', 'every Gen5 element accounted for as deleted, retained or replaced',
         f"{len(missing)} unaccounted", not missing),
        ('3', 'Gen6 has fewer manifest-forfeiting shared elements than Gen5',
         f"{gen6['n_shared']} against {gen5['n_shared']}", gen6['n_shared'] < gen5['n_shared']),
        ('4', "Gen6's required per-element reliability is lower than Gen5's",
         f"{gen6['required_r']:.5f} against {gen5['required_r']:.5f}",
         gen6['required_r'] < gen5['required_r']),
        ('5', 'expected delivery at r = 0.99 is higher for Gen6',
         f"{gen6['expected_at_r99']:.3f} against {gen5['expected_at_r99']:.3f}",
         gen6['expected_at_r99'] > gen5['expected_at_r99']),
        ('6', "neither architecture reaches a spring's zero shared elements",
         f"Gen5 {gen5['n_shared']}, Gen6 {gen6['n_shared']}",
         gen5['n_shared'] > 0 and gen6['n_shared'] > 0),
        ('7', 'the gas store is counted as manifest-forfeiting',
         'yes' if 'Gas reservoir' in gen6['shared_names'] else 'NO',
         'Gas reservoir' in gen6['shared_names']),
        ('8', 'the per-cell backup ejector is evaluated and its effect reported',
         f"{backup['expected_at_r99']:.3f} against Gen6's {gen6['expected_at_r99']:.3f} "
         f"at r = 0.99", True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A47', bands_declared_commit='HEAD~1',
               note='model imported from fmea.py unchanged; only the element list differs. '
                    'No common-cause failures, elements independent, no wear-out, one '
                    'reliability shared across elements. Same assumptions as fmea.py, kept '
                    'for comparability rather than because they are right.',
               target_satellites=TARGET, gen5=gen5, gen6=gen6, gen6_with_backup=backup,
               gen5_element_fates={k: dict(fate=v[0], why=v[1]) for k, v in FATE.items()},
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'fmea_gen6.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
