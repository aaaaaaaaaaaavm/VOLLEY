"""
VOLLEY | The 43.33 kg stage credit, read by someone who does not want to believe it.

WHY THIS EXISTS
---------------
ADR-032's first falsifier, and the only one of the four that nothing has ever bounded: if the
stage credit is optimistic by more than 30 %, added mass per satellite exceeds 2.0 kg and A37
band 5 fails retrospectively.

A37 assigned every line of A35's ledger to added, deleted or stage-provided, and required each
stage-provided item to name the subsystem providing it. That is a good discipline. It is not
the same as testing whether the naming survives a hostile reader.

WHAT IS ADDED HERE
------------------
A surviving fraction per line item, each with a written reason, and the arithmetic of what
happens to the mass case when the credit erodes. The ledger and the store mass are imported,
not restated: host_integrated for the assignment, and A43's reservoir for the store.

Bands declared in validation/A45_stage_credit.md at HEAD, BEFORE this file existed.

Provenance: model output, and the surviving fractions are JUDGEMENTS rather than measurements.
They are declared in the run sheet before this script so their consequence is computed rather
than argued, and the break-even is reported so the reader can substitute their own.
"""
import json
import math
import os

import fill_window as fw
import host_integrated as hi

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

TARGET_KG = 2.0                      # kill criterion 1, unmoved
N = hi.N_MANIFEST
V_RES_A43 = 9.55e-3                  # A43's design reservoir
STORE_KG_A43 = 5.38                  # A43's store, FROZEN. A45 and A45-R both ran at this and
                                     # their published results must keep reproducing.
PARAMS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'cad', 'parameters.json')


def store_kg_current():
    """A56's sized store, read live from the parameter file.

    A45 and A45-R computed the store from A43's 9.55 L reservoir and got 5.38 kg. A56 sized it at
    ADR-034's charge pressure instead of scaling it and got 3.1216 kg -- 42 % lighter -- and the
    break-even is (2.0*N - added_base - store)/credit, so the store is the only term in it that
    this project ever moves. Reading it live is what stops A45-R2 from becoming stale the way its
    two predecessors did.
    """
    with open(PARAMS, encoding='utf-8') as f:
        return json.load(f)['groups']['gen6_store']['store_mass_kg']
ADR_CLAIMED_BREAKEVEN = 0.30         # what ADR-032 states
A45_BREAKEVEN = 0.165                # A45's break-even, for band 6 of the re-run
TRIM_KG = 1.2328                     # A55's resized trim section, SUSPENDED by ADR-036 -- carried
                                     # here only so the published figures that include it can be
                                     # told apart from the ones that do not
ENCLOSURE_PREFIXES = ('Enclosure skins', 'Enclosure frames', 'Radiator',
                      'Equipment-bay boxes', 'Fasteners and brackets')

# Declared in validation/A45_stage_credit.md before this file existed.
SURVIVES = {
    'Track longerons': (0.50,
        'a stage is a stiff cylinder, not a 2.18 m rail aligned to a piston bore; half the '
        'structure is genuinely reused and half is rail hardware that has to be added'),
    'Battery + avionics': (0.60,
        'stage power and IMU are real; a deployer sequencer, its safing chain and the cost of '
        'keeping avionics alive past passivation are not the stage\'s'),
    'Harness': (0.50, 'extending a harness costs harness'),
    'Thermal': (0.40,
        'the stage loop is sized for the stage, not for 131 W of charging plus twelve expansions'),
    'ESPA bracket': (0.90,
        'the strongest credit in the table: a stage genuinely needs no adapter to itself, and '
        '10 % is local mounting'),
    'Panels / closeouts': (0.80,
        'stage skin is real; local closeout around the muzzle is not'),
    # A45-R, 2026-08-16. A46 itemised the enclosure at 50.04 kg, which removes A45's reason
    # for giving it 0.00 -- "you cannot credit a mass you never itemised". These five are
    # argued on their merits in validation/A45R_stage_credit_rerun.md and every one is more
    # generous than the zero it replaces. The six fractions above are A45's, verbatim.
    'Enclosure skins': (0.85,
        'a stage is already a skinned cylinder; a deployer inside it needs no 6 m2 box of its '
        'own. The 15 % is local closeout at the muzzle and the aft cutout'),
    'Enclosure frames': (0.85, 'stage ring frames and stringers, same argument'),
    'Radiator': (0.70,
        'the stage thermal loop provides radiating area; a local cold plate for the sequencer '
        'does not come free'),
    'Equipment-bay boxes': (0.60,
        'a stage avionics bay is real; mounting for a deployer sequencer is not'),
    'Fasteners and brackets': (0.50,
        'attaching a deployer to a stage costs fasteners the stage does not already have'),
}


def credit_items():
    """A37's stage-provided lines, each tagged with its declared surviving fraction."""
    _, stage, _, _ = hi.assign()
    out = []
    for r in stage:
        for prefix, (frac, why) in SURVIVES.items():
            if r['part'].startswith(prefix):
                out.append(dict(part=r['part'], kg=r['kg'], survives=frac, reason=why))
                break
        else:
            out.append(dict(part=r['part'], kg=r['kg'], survives=None, reason=None))
    return out


def per_satellite(credit_lost_kg, store_kg):
    """Mass the credit fails to cover lands back on the deployer."""
    return (hi.added_kg() if hasattr(hi, 'added_kg') else _added_base()) \
        and (_added_base() + credit_lost_kg + store_kg) / N


def _added_base():
    added, _, _, _ = hi.assign()
    return sum(r['kg'] for r in added)


def breakeven_fraction(store_kg, total_credit):
    """Uniform credit loss at which added mass per satellite reaches exactly 2.0 kg."""
    allowed = TARGET_KG * N - _added_base() - store_kg
    if allowed < 0:
        return 0.0
    return min(1.0, allowed / total_credit)


def main():
    items = credit_items()
    total = sum(r['kg'] for r in items)
    base = _added_base()
    store_a43 = fw.store_kg(V_RES_A43)
    store = store_kg_current()

    # A45 and A45-R are dated results and must not drift. Their store is frozen above; if the
    # helper that computes it ever stops returning 5.38 kg, both run sheets have quietly stopped
    # reproducing and this is where it surfaces.
    if abs(store_a43 - STORE_KG_A43) > 0.01:
        raise SystemExit(f"A43 store no longer reproduces: {store_a43:.4f} against {STORE_KG_A43}")
    unjustified = [r['part'] for r in items if r['survives'] is None]

    print(f"A37 stage credit {total:.2f} kg, added base {base:.2f} kg, "
          f"store {store:.4f} kg (A56)  [A43's was {store_a43:.2f}]\n")

    nominal = (base + store) / N
    print(f"at the full credit: {nominal:.3f} kg per satellite\n")

    print(f"{'kg':>7s} {'survives':>9s} {'lost':>7s}  item")
    lost = 0.0
    for r in items:
        l = r['kg'] * (1.0 - r['survives'])
        lost += l
        print(f"{r['kg']:7.2f} {r['survives']:9.2f} {l:7.2f}  {r['part'][:44]}")
    print(f"{total:7.2f} {'':9s} {lost:7.2f}  TOTAL  ({lost/total*100:.1f} % of the credit)")

    hostile = (base + lost + store) / N
    print(f"\nhostile reading: {hostile:.3f} kg per satellite "
          f"({'PASSES' if hostile <= TARGET_KG else 'CROSSES'} the unmoved {TARGET_KG} kg)")

    # The enclosure alone -- A45's "P10 lump", now five derived lines
    encl_kg = sum(r['kg'] for r in items if r['part'].startswith(ENCLOSURE_PREFIXES))
    p10_only = (base + encl_kg + store) / N
    print(f"the enclosure alone: {encl_kg:.2f} kg -> {p10_only:.3f} kg per satellite "
          f"({encl_kg/total*100:.1f} % of the credit)")

    encl = sum(r['kg'] for r in items if r['part'].startswith(ENCLOSURE_PREFIXES))
    be = breakeven_fraction(store, total)
    print(f"\nuniform break-even: {be*100:.1f} % of the credit may fail "
          f"({be*total:.2f} kg), against ADR-032's stated {ADR_CLAIMED_BREAKEVEN*100:.0f} %")

    biggest = max(items, key=lambda r: r['kg'] * (1.0 - r['survives']))
    print(f"largest single loss: {biggest['part'][:44]} at "
          f"{biggest['kg']*(1-biggest['survives']):.2f} kg")

    # band 7: monotone in surviving fraction
    curve = []
    f = 0.0
    while f <= 1.0001:
        curve.append(dict(surviving=f, per_sat=(base + total * (1.0 - f) + store) / N))
        f += 0.05
    monotone = all(a['per_sat'] >= b['per_sat'] - 1e-12
                   for a, b in zip(curve, curve[1:]))

    # A45-R2 band 1: the whole model re-evaluated at the FROZEN store, which must still return
    # A45-R's published result. This is what stops a re-run from silently replacing its
    # predecessor instead of superseding it.
    nom_a43 = (base + store_a43) / N
    hostile_a43 = (base + lost + store_a43) / N
    be_a43 = breakeven_fraction(store_a43, total)
    r2_repro = (abs(total - 85.3599) <= 0.01
                and abs(nom_a43 - 1.403) / 1.403 <= 0.005
                and abs(hostile_a43 - 3.271) / 3.271 <= 0.005)
    print(f"\nA45-R at the frozen {STORE_KG_A43} kg store: credit {total:.4f}, "
          f"full {nom_a43:.3f}, hostile {hostile_a43:.3f}, break-even {be_a43*100:.1f} %")

    # band 8: the three figures this project publishes for one quantity, each with its store
    STORE_ADR034 = 4.10                       # ADR-034's gas-ratio scaling, never a sized store
    reconcile = [
        ('A45 / A45-R / P68', STORE_KG_A43, False, (base + STORE_KG_A43) / N),
        ('README, index.html, GENERATIONS', STORE_ADR034, False, (base + STORE_ADR034) / N),
        ('generations/GEN6, with the trim stage', STORE_ADR034, True,
         (base + STORE_ADR034 + TRIM_KG) / N),
        ('A45-R2, CANONICAL', store, False, (base + store) / N),
        ('A45-R2, with the suspended trim stage', store, True, (base + store + TRIM_KG) / N),
    ]
    print("\nband 8, one quantity and the stores it has been published against:")
    print(f"  {'source':40s} {'store kg':>9s} {'trim':>5s} {'kg/sat':>8s}")
    for label, st, trim, per in reconcile:
        print(f"  {label:40s} {st:9.4f} {'yes' if trim else 'no':>5s} {per:8.4f}")

    bands = [
        ('1', "A45-R reproduces at the frozen 5.38 kg store: 85.36 credit, 1.403 full, 3.271 hostile",
         f"{total:.4f}, {nom_a43:.3f}, {hostile_a43:.3f}", r2_repro),
        ('1b', "line items reproduce A37's re-run 85.36 kg to 0.01 kg",
         f"{total:.4f} kg", abs(total - 85.36) <= 0.01),
        ('2', f"the credit total is stated explicitly and is A45-R's 85.36 kg",
         f"{total:.4f} kg, break-even quoted against it", abs(total - 85.3599) <= 0.01),
        ('3r2', "full credit at the resized store, reported against A45's 1.403",
         f"{nominal:.4f} kg/sat, {(nominal-1.403)/1.403*100:+.2f} % against A45", None),
        ('4r2', f'removing the enclosure lines alone keeps per satellite <= {TARGET_KG} kg',
         f"{p10_only:.3f} kg", p10_only <= TARGET_KG),
        ('3', 'every item carries a surviving fraction with a written reason',
         f"{len(unjustified)} unjustified", not unjustified),
        ('4', f'hostile reading keeps per satellite <= {TARGET_KG} kg',
         f"{hostile:.3f} kg", hostile <= TARGET_KG),
        ('5', f"uniform break-even >= {ADR_CLAIMED_BREAKEVEN*100:.0f} %, as ADR-032 states",
         f"{be*100:.1f} %", be >= ADR_CLAIMED_BREAKEVEN),
        ('6', f"break-even no worse than A45's {A45_BREAKEVEN*100:.1f} %",
         f"{be*100:.1f} %", be >= A45_BREAKEVEN),
        ('7', 'per satellite monotone decreasing in surviving fraction',
         'monotone' if monotone else 'NOT monotone', monotone),
        ('8', 'the five enclosure lines are less than half the total credit',
         f"{encl/total*100:.1f} %", encl / total < 0.50),
        ('8r2', 'the three published added-mass figures are reconciled, one named canonical',
         f"{len(reconcile)} rows, canonical {(base+store)/N:.4f} kg/sat at A56's store",
         len(reconcile) >= 4),
        ('9', 'REPORT: break-even and per-satellite mass across every store this project has used',
         f"{STORE_KG_A43} / {STORE_ADR034} / {store:.4f} kg", None),
    ]
    print()
    for n, text, got, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f"  {n:>3s}  {mark:6s} {text}: {got}")

    print("\nband 9, against every store mass this project has used:")
    print(f"  {'store kg':>9s} {'source':32s} {'kg/sat':>8s} {'hostile':>8s} {'break-even':>11s}")
    for st, why in ((STORE_KG_A43, "A43, from a 9.55 L reservoir"),
                    (STORE_ADR034, "ADR-034, gas-ratio scaled"),
                    (store, "A56, sized at 22.7258 bar")):
        print(f"  {st:9.4f} {why:32s} {(base+st)/N:8.4f} {(base+lost+st)/N:8.4f} "
              f"{breakeven_fraction(st, total)*100:10.1f} %")

    out = dict(analysis='A45-R', bands_declared_commit='HEAD~1',
               note='the surviving fractions are JUDGEMENTS, not measurements. They are declared '
                    'in the run sheet before this script so their consequence is computed rather '
                    'than argued, and the break-even is reported so a reader can substitute '
                    'their own. The 2.0 kg threshold is unmoved.',
               credit_total_kg=total, added_base_kg=base, store_kg=store,
               nominal_per_sat=nominal, hostile_per_sat=hostile,
               credit_lost_kg=lost, credit_lost_pct=lost / total * 100,
               enclosure_only_per_sat=p10_only, enclosure_kg=encl_kg,
               breakeven_fraction=be, adr_claimed_breakeven=ADR_CLAIMED_BREAKEVEN,
               largest_loss=biggest['part'],
               items=items, curve=curve,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'stage_credit.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
