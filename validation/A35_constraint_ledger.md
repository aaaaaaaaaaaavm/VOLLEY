# A35 — the causal mass ledger, and what each constraint is worth

**Bands declared 2026-08-14, before `analysis/constraint_ledger.py` existed.**
Verify with `git show --stat <this commit> -- analysis/constraint_ledger.py`, which must
return nothing.

---

## Why this run exists

`docs/KILL_CRITERIA.md` criterion 1 is crossed by 3.5× and every proposal for closing it has
been argued rather than measured, because `analysis/mass_properties.py` reports **what** each
kilogram is and never **why it is there**. Nineteen line items, no attribution. Delete the sled
in the model and nothing downstream moves, so no architecture question can be answered from it.

**The sibling repository is the reason this is worth doing properly.** BOLLEY deleted one
requirement — that the CubeSat is unmodified — rebuilt the machine around the deletion, and the
mass reappeared as a 15.91 kg primary. That is a genuine negative result, and it cost a
repository, twenty-five validation runs and a register of its own to return one bit of
information. **The same question asked of six requirements at once should not cost six
repositories.**

## What this run is, and what it is NOT

**It is an attribution and an upper bound.** Each line item is tagged with the requirements that
cause it to exist. For any set of deleted requirements, the ledger reports the mass that can no
longer be justified.

**It is NOT a sizing model, and must not be read as one.** It says what comes out. It says
nothing about what has to go back in. A corner that removes 40 kg has not been shown to weigh
44.5 kg — it has been shown that 40 kg of the present design has lost its reason, which is a
different and weaker claim.

**The bound is additive by construction.** Deleting two requirements removes the union of their
items, never more. Real architectures interact — with no mover, the force for the same shot
falls by 70 %, so the drive that replaces the stator is smaller than either deletion implies.
**The lattice cannot see that.** Band 5 tests whether the attribution at least finds the shared
drivers a later sizing model would need.

## The six requirements

| | |
|---|---|
| **C1** | The satellite is unmodified |
| **C2** | A reusable mover carries the magnets |
| **C3** | The energy arrives during the shot |
| **C4** | The machine is rigid, and one length stowed or deployed |
| **C5** | The deployer carries its own energy store |
| **C6** | Twelve satellites share one drive |

Each line item is tagged `full` (the item has no reason to exist without that requirement),
`partial` (it shrinks, by an amount this run does not estimate) or untagged. **`partial` items
are never counted toward a removal bound.**

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | The attributed ledger reproduces `mass_properties.dry_kg` to within **0.01 kg** | Mass was invented or lost in attribution |
| **2** | **Every** line item carries at least one driver or an explicit `survives` tag | Any kilogram is unattributed |
| **3** | Deleting **C1 alone** removes **≤ 15 %** of dry mass | The ledger contradicts BOLLEY, which built this deletion and did not save the mass |
| **4** | Deleting **C3 alone** removes **≥ 25 %** of dry mass | The prediction stated on 2026-08-14 was wrong |
| **5** | At least **three** line items carry **more than one** driver | The requirements are independent, the lattice adds nothing over six separate studies, and no interaction model is possible |
| **6** | **C3** is the single largest one-requirement removal | Some other requirement dominates, and the architecture argument was aimed at the wrong target |
| **7** | No corner removes **> 100 %**, and no `partial` item is counted as `full` | The bound is not a bound |

### Band 3 is the calibration, and it is the one that matters

A ledger that reports large savings from modifying the satellite is a **wrong ledger**, whatever
its arithmetic says, because that architecture has been developed to Gen2.7 in a sibling
repository and the saving did not appear. **Band 3 is this run's only external check** — every
other band tests the model against itself.

### Band 4 is a prediction, recorded so it can fail

Stated 2026-08-14, before the attribution was written: *deleting C3 removes more than 40 % of dry
mass, concentrated in bank, inverter, stator copper, brake and radiator.* **The band is set at
25 %, deliberately below the prediction**, so that the band tests the argument and the prediction
is judged separately and in public.

---

## Results

**RUN 2026-08-14. Seven of seven bands pass. The prediction attached to band 4 was wrong.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces `dry_kg` to 0.01 kg | 84.5316 against 84.5316 | **PASS** |
| 2 | every item attributed | 0 unattributed | **PASS** |
| 3 | C1 alone removes ≤ 15 % | **0.0 %** | **PASS** |
| 4 | C3 alone removes ≥ 25 % | **28.1 %** | **PASS** |
| 5 | ≥ 3 items with multiple drivers | 4 items | **PASS** |
| 6 | C3 is the largest single removal | largest is C3 | **PASS** |
| 7 | bound is a bound | max corner 41.8 % | **PASS** |

### What one requirement is worth

| | Removed | Flagged | |
|---|---:|---:|---|
| **C3** the energy arrives during the shot | **23.76 kg (28.1 %)** | 16.00 kg | stator, formers, bank, PPU, thermal |
| **C2** a reusable mover carries the magnets | **11.54 kg (13.6 %)** | 7.28 kg | magnets, chassis, both brake lines |
| **C5** the deployer carries its own energy store | 6.50 kg (7.7 %) | 5.50 kg | the bank, shared with C3 |
| **C1** the satellite is unmodified | **0.00 kg** | 0.00 kg | — |
| **C4** rigid, one length | 0.00 kg | 29.33 kg | all of it structural, none abolished |
| **C6** twelve share one drive | 0.00 kg | 11.45 kg | containment survives; only the count moves |

### The four findings

**1. The prediction failed, by a wide margin.** Stated before the run: *deleting C3 removes more
than 40 % of dry mass.* It removes **28.1 %**. Even crediting half the 16.00 kg flagged — which
this run is not entitled to do — it reaches about 37 %. **The band was set at 25 % precisely so
the argument and the prediction could be judged separately, and the argument survives while the
prediction does not.**

**2. C1 costs nothing, and that is not the same as saying BOLLEY was wrong.** No item in this
ledger exists *because* the satellite is unmodified. The sled is attributed to **C2** — the choice
that a reusable mover carries the magnets — and C1 only *implies* C2 when nothing else can carry
them. **C1's cost is entirely mediated.** That is the most contestable line in the attribution and
a reader is invited to disagree with it specifically. It is also exactly consistent with the
sibling result: deleting C1 and C2 together is worth 13.6 % here, and BOLLEY's primary grew back
to 15.91 kg because it kept **C3**, which this run finds is the requirement that was costing the
mass all along.

**3. The lattice saturates at 41.8 %, and this is the important number.**
**49.23 kg — 58.2 % of dry mass — survives every deletion of every requirement, in every
combination.** Structure, containment, brackets, closeouts, harness and avionics are `partial`
against everything: they scale, and nothing abolishes them.

**At 49.23 kg over twelve satellites that is 4.10 kg each — still twice kill criterion 1.**

> **No combination of requirement deletions closes kill criterion 1.** The criterion is not
> reachable by architecture at all, on this ledger. That is a harder result than any of the
> individual figures and it was not expected.

**4. The one divisor nobody has pulled.** The surviving mass is per *machine*, not per satellite.
At twenty-four satellites the same 49.23 kg is **2.05 kg each**, and the criterion closes — even
allowing the containment lines to grow with the manifest, it lands near 2.5 kg. **Magazine density
is the only lever in this run that reaches the criterion**, it is outside the physics entirely,
and it has never been studied. It needs its own sizing run and its own bands; nothing here sizes it.

### Limitations, restated because the findings above are easy to over-read

- **This is a bound, not a sizing model.** 41.8 % of the present design loses its reason at the
  best corner. Nothing here says what the replacement weighs.
- **`partial` is never counted**, so C4 and C6 score zero despite carrying 29.33 kg and 11.45 kg
  of flagged mass between them. **The deployable track cannot be evaluated by this method** — all
  of its mass is structural and structure only ever scales.
- **The requirements are treated as independent and are not.** C1 implies C2; C5 is a consequence
  of C3. A dependency graph would change the single-requirement column and would not change
  finding 3, which is where the value is.
- The 8.00 kg enclosure line is still the P10 placeholder with no derivation behind it, and it
  is 9.5 % of the total.
