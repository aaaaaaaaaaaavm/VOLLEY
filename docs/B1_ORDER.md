# B-1: the order

Written 2026-08-10. [`BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md) specifies B-1 as an experiment.
This file is the order, what to ask for, how to ask for it so the parts arrive usable, what
to check on arrival, and what to do the afternoon they land.

> Why this exists as a separate file. B-1 has had a method since 2026-07-29 and a bill of
> materials since 2026-07-30, and has not been ordered. A procedure invites more analysis. A
> purchase order invites a purchase. [ADR-021](adr/021-freeze-the-register.md) made this the top
> of the roadmap.

What it changes. Every headline number in this project descends from a field model that has
only ever been checked analytic against analytic, a decaying-wave model against magpylib,
which is two implementations of the same physics. A gaussmeter is a different *kind* of evidence.
E4, nothing built, fired or measured at any scale, stops being true the day this is read.
That is a change of category, not of degree, and nothing else available does it.

---

## 1. What to buy

Total envelope: ₹22,000,  ₹52,000. Every figure is an estimate, not a quotation. The
instrument dominates and is the only line worth shopping hard.

### 1.1 The magnets, the line most likely to go wrong

A Halbach wavelength needs four blocks magnetised in four different directions. In practice
that is two part numbers, ordered four times each.

| | Block | Magnetisation axis | Qty | Est. INR |
|---|---|---|---:|---|
| Type A | 12 x 8 x 90 mm, N45SH | through the 8 mm thickness | 4 | 2,000-4,000 |
| Type B | 12 x 8 x 90 mm, N45SH | along the 12 mm length | 4 | 2,000-4,000 |

Dimensions from `cad/parameters.json`: 48 mm wavelength over four blocks = 12 mm each, magnet
thickness 8 mm, array depth 90 mm. Each block ~ 8.64 cm³, about 65 g; eight ~ 520 g.

> The failure mode, stated because it is near-certain otherwise. A supplier given
> "12 x 8 x 90 mm, N45SH" and nothing else will magnetise through the largest face, it is the
> default tooling orientation. That yields eight identical blocks and no Halbach array, and
> the mistake is invisible on arrival because the blocks look correct and are correctly
> magnetised, just not on the axis needed. State the axis explicitly, per part number, with the
> sketch in §2, and require the supplier to confirm it in writing before production.

### 1.2 The instrument, the binding requirement is range, not resolution

| Item | Spec | Qty | Est. INR |
|---|---|---:|---|
| Digital teslameter, transverse Hall probe | 1 T minimum range, 2 % accuracy or better | 1 | 15,000-45,000 |

1 T range is binding. The model predicts 0.694 T at midgap. Most inexpensive instruments
sold as "gauss meters" are 200 mT full scale, which saturates and reads nothing useful at the one
station that matters most.

The probe must be transverse (field normal to the probe face) and thin enough to enter a
12 mm gap with the array assembled, check the stated probe thickness against the gap before
ordering, including its protective sheath.

Borrow before buying. Any university or industrial materials lab with a magnetics bench has
one. Borrowing removes roughly two thirds of the total cost and is the single largest saving
available on this order.

### 1.3 Fixture and consumables

| Item | Spec | Qty | Est. INR |
|---|---|---:|---|
| Aluminium plate, fixture | 200 x 150 x 10 mm | 2 | 1,500 |
| Non-magnetic fasteners | A4 / 316 stainless, M6 | 10 | 500 |
| Printed spacers | PETG or nylon, 12.0 mm nominal plus a shim set | set | 500 |
| Feeler gauges | 0.05,  1.00 mm | 1 set | 700 |

Nothing ferromagnetic anywhere in the fixture. A4/316 stainless is the specification, not
"stainless", several common stainless grades are magnetic and will both perturb the field and
be pulled into the gap.

### 1.4 Sourcing

Specify to the spec above and request quotations from three suppliers, comparing on
magnetisation-axis confirmation first and price second. Custom-magnetised NdFeB blocks in ones
and twos are a routine order for any sintered-magnet manufacturer, and quantity-of-eight orders
are usually quoted within a few days.

*Supplier names are deliberately not carried in this repository.* Send the same specification to
each and compare, which is better ordering practice than a named vendor anyway.

---

## 2. The magnetisation sketch to send with the order

Include this with the enquiry. It is the difference between an array and eight paperweights.

```
One wavelength, 48 mm, four blocks of 12 mm. Arrows = magnetisation direction.
Block face shown is 12 mm (along array) x 8 mm (thickness). Depth 90 mm into page.

        block 1        block 2        block 3        block 4
      +---------+    +---------+    +---------+    +---------+
      |    ^    |    |    -->  |    |    v    |    |  <--    |
      |    |    |    |         |    |    |    |    |         |
      +---------+    +---------+    +---------+    +---------+
        TYPE A         TYPE B         TYPE A         TYPE B
      through 8mm    along 12mm     through 8mm    along 12mm
      (up)           (forward)      (down)         (backward)
       <------------------ 48 mm wavelength ------------------>

Type A and Type B differ ONLY in magnetisation axis. Same block dimensions.
Within a type, the two blocks are the SAME part, installed rotated 180 degrees.
So: 4 off Type A, 4 off Type B  =  8 blocks  =  one wavelength, double-sided.
```

Quotation request wording, to paste:

> Eight sintered NdFeB blocks, grade N45SH, each 12.0 x 8.0 x 90.0 mm.
> Four magnetised through the 8 mm dimension. Four magnetised along the 12 mm
> dimension. The magnetisation axis differs between the two groups and is critical to the
> application; blocks magnetised through the 90 mm or the largest face are not usable.
> Please confirm the magnetisation axis for each group in writing before production, and mark
> the polarity on each block or on its packaging.
> Nickel plating standard. Please quote unit and lot price, lead time, and tolerance on
> dimensions and on Br.

---

## 3. Receiving inspection, before anything is assembled

Do this before the blocks go anywhere near each other. Once a pair closes across 12 mm it is
not coming apart by hand, and a wrongly magnetised block discovered at that point has already
cost the fixture.

1. Confirm the axis on every block, individually. Suspend a small compass or a second small
   magnet on a thread and bring it near each face in turn. The attracting/repelling axis is the
   magnetisation axis. Sort into Type A and Type B piles and count them: four and four.
2. If all eight behave identically, the order was magnetised on one axis, the §1.1 failure
   mode. Stop, photograph, and return them. Do not attempt to build an array from it.
3. Measure one block's dimensions against 12.0 x 8.0 x 90.0 mm and record the deviation. The
   band budget assumes ±0.1 mm on thickness; a larger deviation is not disqualifying but must be
   recorded, because it feeds the gap.
4. Check the probe enters a 12 mm slot with its sheath on, before assembly rather than after.

---

## 4. Safety, this is the hazard, quantified

The two arrays attract. Over one wavelength at the design gap, Maxwell stress on 48 x 90 mm at
0.694 T gives

```
F = B²A / 2μ₀ = 0.694² × 0.0043 / (2 × 4π × 10⁻⁷) ≈ 828 N
```

About 84 kgf across a 12 mm gap, on brittle sintered NdFeB. Nothing else on this bench stores
that much energy. It is not a handling inconvenience.

- Build the fixture so the gap is set by a captive spacer that cannot be removed while the
  magnets are mounted. Shim outward from a closed stack, never inward by hand.
- Never approach the gap from open. Fingers out of the plane of the gap during assembly.
- Design the fixture for 828 N even though the real figure is likely nearer 600 N, the P17
  correction (the flat-plate formula runs ~37 % high) is in the conservative direction here, and
  over-building an aluminium bracket costs nothing.
- Eye protection. Sintered NdFeB shatters, and the fragments travel.

---

## 5. The trap that produces a false falsification

If a two-block pair is built rather than a full four-block wavelength, which
`BENCHTOP_TESTS.md` allows as the cheaper option, the orientation is ambiguous in the one way
that matters:

| Two-block arrangement | Mean \|B<sub>y</sub>\| at midgap |
|---|---:|
| Polarizations facing each other across the gap | 0.00000 T, cancels exactly |
| Polarizations both the same direction | 0.32861 T |

Built the first way the rig reads zero field, which looks exactly like a falsified model rather
than a reversed magnet. `verify_field.py` probes for the correct convention automatically on the
four-block array, so this trap exists only on the bench.

Build the four-block wavelength if the budget stretches at all. It is what
`verify_field.py` actually models, and it removes this trap entirely.

---

## 6. The measurement, and the bands

The bands below were declared 2026-07-30 and derived 2026-08-06, before any hardware exists.
They are restated here unchanged and may not be edited after a reading.

Assemble at the 12 mm design gap in the non-conductive fixture. Traverse the probe on the
centreline and behind the back face. Record: peak field in the gap, and field at 10, 20 and
50 mm behind the back face.

| Row | Model says | Rig contributes | Accept if |
|---|---:|---:|---|
| Peak gap field | 0.694 T | 4.4 % | within ±15 % to 0.590,  0.798 T |
| Winding mean \|B\| | 0.552 T | 4.5 % | within ±15 % to 0.469,  0.635 T |
| Stray at 10 mm | 22.7 mT | 3.7 % | within ±20 % to 18.1,  27.2 mT |
| Stray at 20 mm | 4.33 mT | 4.2 % | within ±40 % to 2.60,  6.06 mT |
| Stray at 50 mm | 0.38 mT | 3.3 % | order of magnitude only |

The bands are three to ten times wider than the rig's own error, and that is correct. A
declared band must cover *model* error, which is the thing under test. What the budget
establishes is the other half: the rig is not the limiting factor. A reading outside ±15 %
cannot be blamed on shim stack or magnet grade, because those together account for 4.5 %. That is
what makes a failure interpretable on the day.

The far-field bands widen deliberately. Those are small differences of large numbers,
`RESULTS.md` already calls them the least trustworthy rows in the repository, and they were wrong
in the published paper once (P3). A 50 mm reading within a factor of two is a pass. The
model does not deserve better than that.

---

## 7. What to do with the result

Record it against the bands as declared, including if it fails, especially if it fails.

- Results to `validation/results/B1_field.json`, same format as the analysis outputs, alongside
  instrument make and range, probe type, measured gap, ambient temperature, and the
  receiving-inspection notes from §3.
- A `CHANGELOG.md` entry with cause, before/after, and the item it moves.
- A miss produces a numbered defect, not a widened band, and under ADR-021 a band miss is
  one of the three things that may still open a register entry.

What it closes. The field model behind every headline number (E1, and the analytic-only
half of E2), and the keep-out figures in P3. What it does not close is E4 in full:
this is one sub-scale, ambient, single-article experiment. `QUALIFICATION_PLAN.md` is what
qualification requires.

But the difference between a design study with no measurements and one with one is not a
matter of degree.

---

## Provenance

Method, bands and safety figure from [`BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md); band derivation
from `validation/bench/bench_predict.py` to `validation/results/bench_predictions.json`, which
imports `verify_field.py` and `motor_model.py` rather than reimplementing the geometry.
Dimensions from `cad/parameters.json`. Prices are estimates, not quotations, and the same
caveat `analysis/cost.py` carries applies with more force here where quantities are ones and twos.
