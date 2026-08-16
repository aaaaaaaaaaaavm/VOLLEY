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
ADR_CLAIMED_BREAKEVEN = 0.30         # what ADR-032 states

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
    'Enclosure / radiator': (0.00,
        'you cannot credit a mass you never itemised. P10 records this as a parametric lump '
        'never built up from line items, and the dry mass as a floor rather than a total; '
        'deleting it as stage-provided converts an admitted unknown into a saving'),
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
    store = fw.store_kg(V_RES_A43)
    unjustified = [r['part'] for r in items if r['survives'] is None]

    print(f"A37 stage credit {total:.2f} kg, added base {base:.2f} kg, "
          f"store {store:.2f} kg (A43)\n")

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

    # P10's lump alone
    p10 = next(r for r in items if r['part'].startswith('Enclosure / radiator'))
    p10_only = (base + p10['kg'] + store) / N
    print(f"P10's {p10['kg']:.2f} kg lump alone: {p10_only:.3f} kg per satellite "
          f"({p10['kg']/total*100:.1f} % of the credit)")

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

    bands = [
        ('1', "line items reproduce A37's 43.33 kg to 0.01 kg",
         f"{total:.4f} kg", abs(total - 43.33) <= 0.01),
        ('2', "at the full credit, per satellite reproduces A43's 1.403 kg within 0.5 %",
         f"{nominal:.3f} kg, {abs(nominal-1.403)/1.403*100:.2f} % off",
         abs(nominal - 1.403) / 1.403 <= 0.005),
        ('3', 'every item carries a surviving fraction with a written reason',
         f"{len(unjustified)} unjustified", not unjustified),
        ('4', f'hostile reading keeps per satellite <= {TARGET_KG} kg',
         f"{hostile:.3f} kg", hostile <= TARGET_KG),
        ('5', f"removing P10's lump alone keeps per satellite <= {TARGET_KG} kg",
         f"{p10_only:.3f} kg", p10_only <= TARGET_KG),
        ('6', f"uniform break-even >= {ADR_CLAIMED_BREAKEVEN*100:.0f} %, as ADR-032 states",
         f"{be*100:.1f} %", be >= ADR_CLAIMED_BREAKEVEN),
        ('7', 'per satellite monotone decreasing in surviving fraction',
         'monotone' if monotone else 'NOT monotone', monotone),
        ('8', 'largest single contributor to credit loss identified',
         f"{biggest['part'][:40]} at {biggest['kg']*(1-biggest['survives']):.2f} kg", True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A45', bands_declared_commit='HEAD~1',
               note='the surviving fractions are JUDGEMENTS, not measurements. They are declared '
                    'in the run sheet before this script so their consequence is computed rather '
                    'than argued, and the break-even is reported so a reader can substitute '
                    'their own. The 2.0 kg threshold is unmoved.',
               credit_total_kg=total, added_base_kg=base, store_kg=store,
               nominal_per_sat=nominal, hostile_per_sat=hostile,
               credit_lost_kg=lost, credit_lost_pct=lost / total * 100,
               p10_only_per_sat=p10_only, p10_kg=p10['kg'],
               breakeven_fraction=be, adr_claimed_breakeven=ADR_CLAIMED_BREAKEVEN,
               largest_loss=biggest['part'],
               items=items, curve=curve,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'stage_credit.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
