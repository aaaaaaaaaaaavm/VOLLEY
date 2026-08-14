# ADR-022: The winding is segmented for fault isolation and driven as one section

**Status:** Accepted · **Date:** 2026-08-10 · **Phase:** I · **Closes:** P29

## Context

`paper.tex` §VII states, under redundancy, that *"the winding is segmented so a shorted coil
degrades thrust rather than ending the campaign."* `motor_model.shot()` charges copper loss over
`vol_cu = ACCEL_ZONE × DEPTH × WIND_THICK × FILL` — **the whole 1.30 m winding at full current
density for the entire 157 ms stroke.**

Those two statements are consistent only if "segmented" means fault isolation rather than block
commutation, and **nothing in this repository said which was meant.** `cad/parameters.json`
`groups.stator` records conductor counts and belt geometry and is silent on drive segmentation,
so the CAD could not settle it either. **P29** logged the three possibilities rather than
guessing, because guessing either way would put an unsourced value into the baseline — the defect
class **P24** and **E17** exist to prevent.

**Both branches are now priced.** `analysis/owner_decisions.py` → `results/owner_decisions.json`,
computed by re-running the real pipeline with the energised length as a parameter:

| | Whole winding energised | ~One sled length (340 mm) | 4 segments, one energised |
|---|---:|---:|---:|
| Copper loss per shot | **834.7 J** | 218.3 J | 208.7 J |
| Net energy drawn | **2559 J** | 1913 J | 1903 J |
| **Net efficiency** | **20.99 %** | **28.07 %** | 28.22 % |
| Peak current | **339 A** | 288 A | 287 A |
| **P33 phase inductance** | **19.70 µH** | 5.15 µH | 4.92 µH |
| **Exit velocity** | **16.388 m/s** | **16.388 m/s** | **16.388 m/s** |

**The last row is the one that decides this.** Exit velocity is *identical* across all three,
because the machine commands a force and copper loss is a power draw rather than a thrust
reduction. **Segmentation changes what the shot costs, not what it delivers.** The answer is also
robust to segment count — four segments and one-sled-length land within 0.15 points of each other.

*(P29's own 2026-07-31 estimate of "21.2 % → roughly 24.4 %" is superseded. It predates the
quadrature correction. The computed figure is 28.07 %.)*

## Decision

**The winding is segmented for fault isolation and driven as a single energised section.**
`vol_cu = ACCEL_ZONE` stands. **No baseline value moves.**

The paper's redundancy sentence is correct and is made explicit: the segmentation exists so that
a shorted coil degrades thrust rather than ending the campaign, and it is **not** block
commutation. A reader will otherwise assume block commutation, because that is what a segmented
long-stator machine normally means.

## Why this one

1. **It is the branch that keeps the baseline honest.** The model already computes it, ten
   validations have run against it, and adopting it invalidates nothing. Adopting block
   commutation would move copper loss, efficiency and inductance together and require re-running
   A8, A10, A11 and the drive design.
2. **Efficiency is not a kill criterion. Mass is, and it is already crossed.** Block commutation
   buys 7.09 points of efficiency and costs one inverter per segment or a segment-switching
   assembly, **none of which is in the mass rollup** — and kill criterion 1 is crossed by a factor
   of three at 6.375 kg per satellite against a 2 kg threshold. Buying efficiency with mass is the
   wrong direction for the threat that is actually live. **P10** already records that the rollup
   is missing packaging mass; adding drive hardware before that is closed would make a bad number
   worse for a benefit nothing is asking for.
3. **Nothing in the product argument is efficiency-limited.** The kill criteria are mass,
   envelope, bank sizing, tip-off, attitude rate and whether the Δv is worth anything. Net
   efficiency appears in none of them. A 21 % machine and a 28 % machine sell identically.
4. **It is the conservative direction, and conservatism in a model with no measurements behind it
   is the right default.** E4 stands: nothing here is measured. A model that overstates copper
   loss fails safe.

## What this costs, recorded rather than glossed

**This decision pays 7.09 points of net efficiency and 616 J of copper per shot for drive
simplicity, and that is a real price.** P29's second possibility was that the conservatism might
be genuine engineering judgement *"written down nowhere, which is the same defect class as the
12 mΩ ESR: a value with no provenance."* It is now written down, with both branches costed, which
is the whole of what P29 asked for.

**74 % of the copper dissipates with no field over it.** In an ironless machine the conductors
outside the magnet array carry current and produce no thrust. That is a genuine inefficiency and
this ADR accepts it deliberately, on the grounds above, rather than pretending it is not there.

**`motor_model.shot()` keeps its `energised` parameter**, defaulting to `ACCEL_ZONE`. The default
is now **a recorded decision rather than an unexamined default**, which is the difference P29 was
actually about. The parameter stays so the alternative remains priceable without editing the model.

## What this does not do

- **It does not close P26 or E17.** Lower peak current would relax the bank requirement; this
  branch does not lower it. The 12 mΩ ESR still has no source.
- **It does not make block commutation wrong.** It is available, priced at +7.09 points, and
  belongs in `VOLLEY-lab` as a Phase II item with a stated entry criterion: **it becomes
  attractive if and when the mass rollup closes and efficiency starts binding something.**
- **It does not validate the 20.99 % figure**, which remains a model output like everything else.

## Consequences

- `paper.tex` §VII's redundancy sentence states that the segmentation is for fault isolation and
  that the winding is driven as one section, so the reader cannot infer block commutation.
- **P29 closes.** Both numbers now follow from one stated fact instead of two unstated ones.
- The Phase II entry criterion above goes to `docs/VAULT.md`.

## Validation

None, and none is possible: this is a design decision, not a measurement. What would falsify the
*reasoning* is the mass rollup closing with room to spare, at which point trading mass for
efficiency stops being the wrong direction and this ADR should be revisited.
