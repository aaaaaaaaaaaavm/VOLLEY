# D2, and the enclosure panel: the two decisions analysis cannot take

**Written 2026-08-22.** [`STATE_OF_THE_PROJECT.md`](STATE_OF_THE_PROJECT.md) lists ten decisions
nobody has taken and calls **D2** *"the one that changes the most and has been avoided the
hardest."* [`GEN6_CLOSURE.md`](GEN6_CLOSURE.md) puts D2 and the enclosure panel together as step 5
of the order of work and says they are *"together worth more than any analysis on this page."*

**This file does not decide either of them.** It puts each business case beside the other at the
numbers the repository holds today, so that what is left is a preference rather than a
calculation. **Every figure here comes from a committed results file or a run sheet**, and where
one is needed and does not exist, it says so instead.

> **Nothing in this project has been built, fired or measured** — **E4**. Both decisions below are
> taken on model outputs, and choosing between two calculations is not the same as choosing
> between two measurements.

---

## Part 1 — D2: which payload class is the product

### The question is not "which class". It is which of two things to give up

**The threshold is unchanged and is not being moved.** [`KILL_CRITERIA.md`](KILL_CRITERIA.md)
threat 1: above roughly **2 kg of deployer per satellite**, a rational customer buys a propulsion
module instead. That threshold is an estimate from canisterised dispensers at about 2 kg/U and
cold-gas modules at 0.5–1.2 kg, and the kill-criteria file says in its own words that it *"is not
a sourced industry figure."* It is the number the whole decision is measured against, and it is
the softest number in this document.

**Three routes to it are closed and one is open.** [A35](../validation/A35_constraint_ledger.md)
closed architecture: **88.67 kg — 70.06 %** of dry mass survives deleting every requirement in all
64 corners. [A36](../validation/A36_magazine_density.md) closed manifest size: 2.0 kg is first
reached at **N = 116**, and no factorisation of 116 packages inside the track.
**Payload class is what is left**, and that is D2.

### The ladder, re-run at the current rollup

[A24](../validation/A24_fixed_cell_manifest.md)'s **designed cell** — one cell geometry sized to
the 3U slot the machine is already laid out for, smaller classes flying in lengthwise inserts.
Twelve cells, from `analysis/results/cell_manifest.json`, re-run 2026-08-22 at the **126.6 kg**
rollup [A46](../validation/A46_enclosure_buildup.md) produced.

| Class | Per cell | Per load | **Deployer kg per satellite** | Against ~2 kg | Exit velocity |
|---|---:|---:|---:|:--|---:|
| ChipSat / femtosat | 720 | 8640 | **0.015** | closes | 19.1 m/s |
| **PocketQube 1P** | 24 | 288 | **0.440** | **closes** | 18.9 m/s |
| **PocketQube 3P** | 8 | 96 | **1.319** | **closes** | 18.4 m/s |
| 1U CubeSat | 3 | 36 | **3.517** | **crosses** | 17.9 m/s |
| TubeSat | 2 | 24 | **5.275** | crosses | 18.4 m/s |
| **3U CubeSat** | **1** | **12** | **10.550** | **crosses, 5.3×** | **16.0 m/s** |
| ThinSat, 6U, 12U | — | — | — | **not accommodated** | — |

**Two rungs close it, and neither is the one this repository was leaning on.** 1U was the rung —
it read 1.913 kg volumetrically, A24's designed cell took it to 2.125 and over, and at the current
rollup it is **3.517 kg**. *Every figure in this table was three rollup generations stale until it
was re-run to write this file* — [P101](../OPEN_PROBLEMS.md).

Velocities are `payload_family.py`'s. **Going smaller buys almost no velocity**: removing 99.9 % of
the payload is worth 19 %, because the 9.445 kg sled is most of the moving mass.

### What the closing rungs cost, and it is the product's central claim

**A24 states the cost of the fixed cell up front, and it is the whole of D2:**

> *"Velocity becomes programmable per **cell**, not per satellite. Every satellite sharing a cell
> leaves on the same shot at the same commanded velocity. At 3U, cell = satellite and nothing is
> lost."*

**The machine commands twelve velocities. That number does not change with payload class.** What
changes is how many customers are behind each one:

| Class | Satellites sharing one commanded velocity | Distinct velocities per load | Satellites per load |
|---|---:|---:|---:|
| **3U** | **1** | 12 | 12 |
| 1U | 3 | 12 | 36 |
| PocketQube 3P | 8 | 12 | 96 |
| **PocketQube 1P** | **24** | 12 | 288 |

**So D2 is a choice between two failures, not between a failure and a success:**

| | **Stay at 3U** | **Go to PocketQube** |
|---|---|---|
| Kill criterion 1 | **crossed, 5.3×** | **closes** — 0.440 kg at 1P |
| Commanded velocity per satellite | **kept. Cell = satellite** | **lost. 24 satellites share a shot at 1P, 8 at 3P** |
| Against a canisterised dispenser | **1.758× heavier per satellite** ([P69](../OPEN_PROBLEMS.md)) | *no comparator run exists at this class* |
| CAD, cassette, cost model | **all of it already exists** | **the insert exists as parameters, not as geometry** |
| Qualification | one cell, one campaign | one cell, one campaign — A24's whole design intent |

**The differentiating claim and the criterion that decides whether the product has a reason to
exist are in direct opposition, and every rung that closes one loses the other.**
[A21](../validation/A21_comparators.md) already found that against a spring dispenser the
*commanded differential* is the only surviving argument — a spring's designed differential between
satellites is exactly zero, which is categorical rather than a ratio. **At 1P, VOLLEY's designed
differential between the 24 satellites in a cell is also exactly zero.** It keeps a differential
*between cells* and against a spring that is still twelve settings where there were none.

### Two things that must be said with that table

**The ladder is Gen5's cassette.** `cad/parameters.json` carries `magazine` and `payload_cell` as
Gen5 documents. The `gen6_*` groups define a drive, a store, a seal and a trim section — **there is
no Gen6 magazine and no Gen6 cell in any committed file.** The table above therefore prices D2
against the architecture that has been analysed, not the one currently being designed. *A rung
chosen here does not transfer to Gen6 without a cell geometry that does not exist.*

**Below 3U, satellites sharing a cell never separate from each other.** A24 raises this and does
not solve it. Band 6 failed on exactly the mechanism meant to address it, and
[P44](../OPEN_PROBLEMS.md) records the failure rather than a fix.

### The second numerator, which must be reported with the first

[A37](../validation/A37_host_integrated.md) asked whether the deployer *is* the spent stage rather
than a payload on one, and **A37 band 3 requires both numerators to appear wherever either does.**
That rule binds this file.

| At the Gen6 design point | Per satellite |
|---|---:|
| **Dry mass**, the numerator a customer pays if the deployer is hardware | **10.547 kg** |
| **Added mass**, full credit at [A56](../validation/A56_reservoir_resized.md)'s sized store | **1.2145 kg** |
| **Added mass**, hostile reading of the same credit | **3.0827 kg** |
| Crediting the enclosure alone | 5.3837 kg |

**Kill criterion 1 is crossed on both numerators, not one** —
[P68](../OPEN_PROBLEMS.md), CRITICAL and open. The added-mass case closes at the full credit and
crosses at the hostile one, and the **break-even is 11.0 %**: the credit may fail by that
much before added mass reaches 2.0 kg. [ADR-032](adr/032-gen6-stage-integrated-gas-store.md) declared 30 %.
**The falsifier fires.** **58.6 %** of the credit is the enclosure — one assumption about somebody
else's skin — which is what makes Part 2 a decision and not a detail.

*Any page quoting **1.3173 kg** must say it includes a trim stage
[ADR-036](adr/036-seal-specification-and-the-trim-stage.md) suspended.*

### What decides D2, stated plainly

**Two questions, and neither is an analysis.**

1. **Is the product a velocity or a ride?** If the commanded per-satellite differential is the
   product, **3U is the only class that delivers it** and kill criterion 1 stays crossed at 5.3×
   until something other than payload class moves it — and A35 and A36 have closed the two
   somethings. If the product is cheap access for very small satellites, **PocketQube 1P closes
   the criterion at 0.440 kg** and the differential becomes a per-cell feature.
2. **Which numerator does a customer actually pay?** If the deployer is hardware someone buys and
   flies, it is 10.547 kg. If it is a spent stage that would have been passivated, it is
   1.2145–3.0827 kg. **That is a commercial question about who owns the stage**, and A37 records
   that no launch provider has agreed to keep one alive past passivation.

**What the record supports, and it is a recommendation and not a result:** the honest reading is
that **3U is the demonstrator and a PocketQube-class cell is the product**, because the criterion
that decides whether the machine has a reason to exist closes on one and not the other, and
because the differential survives in a reduced form on both. **Deciding the opposite is defensible
and costs one thing: kill criterion 1 stays crossed, and the front page has to keep saying so.**

### What this decision does not fix

Tip-off ([A23](../validation/A23_tipoff_release.md)'s 36–231 °/s cradle arrival) survives every
class. **E4** survives every class. **E30** — nine of thirteen elements are single-point failures
that forfeit the remaining manifest — is not improved by any of it either. **The machine still
fires twelve times at every class**, so the cycle count that reliability run is built on does not
move; what moves is the value each forfeit destroys. `reliability_architecture.json` records
`n_shots = 12` and one satellite per shot, and **nothing has re-run it against a cell holding
twenty-four.**

---

## Part 2 — The enclosure panel: which failure to carry

### Both options fail the band that was declared for them

[A46](../validation/A46_enclosure_buildup.md) built the enclosure from the geometry in
`cad/parameters.json` after [P10](../OPEN_PROBLEMS.md) had stood for weeks as an **8.00 kg
placeholder with no derivation**. It declared two bands before the script existed, and both failed.

| | Monolithic 2 mm aluminium | Honeycomb sandwich, 3.0 kg/m² |
|---|---:|---:|
| Skins | 32.82 | 18.23 |
| Frames and ribs | 8.20 | 4.56 |
| Radiator | 2.59 | 2.59 |
| Equipment-bay boxes | 1.87 | 1.87 |
| Fasteners and brackets | 4.55 | 2.73 |
| **Total** | **50.04 kg** | **29.98 kg** |
| Band, declared ≤ 8.0 kg | **FAIL** | **FAIL** |

**Only three of the five lines move.** The radiator and the equipment-bay boxes are the same
hardware in both cases; frames and fasteners are declared fractions of the structure, so they
follow the skins down rather than being redesigned.

The sandwich figure moves with one declared input: the sweep runs **21.62 kg at 2.0 kg/m²** to
**38.34 kg at 4.0**. Three of the five inputs behind either case are guesses, and A46 says so.

### What the choice is worth, and what it is not worth

**`cad/parameters.json` specifies 2 mm monolithic aluminium skins**, so **50.04 kg is what the
design as recorded weighs** and the rollup carries it. A honeycomb sandwich is lighter, is what
real spacecraft panels of this size are, and **has never been drawn, specified or costed here**.
Adopting one is an ADR, not a parameter edit.

| The choice buys | |
|---|---|
| **On kill criterion 1 at 3U** | **Nothing that closes it.** [P69](../OPEN_PROBLEMS.md) records the honeycomb case at **8.87 kg per satellite**, ratio **1.48** against a canisterised dispenser, *still failing* — and states plainly: **no enclosure change reaches parity** |
| **On kill criterion 1 at PocketQube** | Nothing that is needed. 0.440 kg already closes it |
| **On the Gen6 added-mass case** | **The exposure, not the mass.** The enclosure is **58.6 %** of the stage credit and its skins are the largest single loss in the hostile reading at **4.92 kg**. A lighter panel is a smaller thing to be wrong about |
| **On the record** | Twenty kilograms of a 126.6 kg rollup, in a document whose enclosure was a placeholder six days ago |

**So the enclosure panel is not the decision it looks like.** It changes no verdict on either
numerator at either payload class. What it changes is **how much of the Gen6 mass case rests on
one assumption about a stage's skin** — and that is the argument for taking it, not the twenty
kilograms.

### What deciding it looks like

**Monolithic, as specified.** No ADR, no change, the rollup stands. The design keeps a skin
specification nobody defends and the front page keeps a dry mass **6.3× the placeholder it
replaced**.

**Honeycomb, by ADR.** One ADR naming the areal density, the sweep it was chosen from, and the fact
that no panel design, no core, no facesheet and no joint exists behind it. **Every per-satellite
figure in the repository moves**, and every one of them still fails at 3U. *The band is not
re-declared and A46's verdict does not change: both cases failed the 8.0 kg band as declared, and a
lighter failure is still a failure.*

**NEEDS SOURCE: what a honeycomb panel of this size actually weighs, from a panel design rather
than an areal density.** Until that exists, choosing honeycomb replaces a heavy number with an
optimistic one, and the repository would be carrying the optimistic one on its front page.

---

## What both decisions have in common

**Neither is blocked by analysis, and both have been open long enough that not deciding is itself
the decision.** The two things that would change either of them are
[P67](../OPEN_PROBLEMS.md) — measuring the seal friction, which
[`B2_ORDER.md`](B2_ORDER.md) now has an order for — and a stage interface nobody outside this
project has agreed to. **Both are Category D. Neither is computation.**

**And the thing this file could not do is worth recording.** Writing it required the payload
ladder, and the ladder had not been re-run since the rollup moved — three vintages of the same
table, disagreeing about every rung, in one repository. **The decision has been avoided for long
enough that its own input went stale underneath it.**
