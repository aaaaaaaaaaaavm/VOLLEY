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

*(Filled after the run. Nothing above this line changes.)*
