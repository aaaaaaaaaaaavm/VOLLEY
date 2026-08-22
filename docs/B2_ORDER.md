# B-2: the seal friction order

**Written 2026-08-22.** [`B1_ORDER.md`](B1_ORDER.md) is the order for the field measurement.
**This is the order for the other one** — the seal friction that
[P67](../OPEN_PROBLEMS.md) has made the single highest-leverage unknown in the programme.

> **Why this exists as an order rather than a procedure.** B-1 had a method since 2026-07-29 and a
> bill of materials since 2026-07-30, and was not ordered for six weeks. *A procedure invites more
> analysis. A purchase order invites a purchase.* This file is written the same way and for the
> same reason.

**What it changes.** [ADR-036](adr/036-seal-specification-and-the-trim-stage.md) **suspended a
subsystem** rather than guess this number. Five decisions wait on it, and it is the only
measurement in the programme that can *delete* work rather than add it.

| Measured friction | Consequence |
|---|---|
| **≤ 17.8 N** | **P88 closes**, the trim stator is unnecessary, **ADR-033 is amended out**, and A66 is never written |
| **17.8 – 22.3 N** | The stator is still unnecessary, but **the seal does not survive its own heat** — P88 stays open |
| **> 22.3 N** | **The stator is needed.** ADR-036 falsifier 1 fires, ADR-033 stands, and **A66/P92 becomes the next run with nothing in front of it** |

**The threshold is coarse, and that is the good news.** This is not a precision measurement. It
asks which side of **17.8 N** and **22.3 N** a number falls on, and the current published
dispersion descends from an *allowance* of **83.4 N** — **4.68× the specification.** A crude test
discriminates.

---

## 1. What to buy

**Total envelope: ₹8,000 – ₹26,000.** Every figure is an estimate, **not a quotation**, and no
line item here has been priced by a supplier. `analysis/cost.py` carries no quotation either
(**E16**); this file does not change that.

### 1.1 The cylinder — buy the stock bore, and this is already settled

**A pneumatic cylinder to ISO 6432, 16 mm bore, ≥ 100 mm stroke, spring-return or double-acting.**

**[A61](../validation/A61_seal_class.md) band 7 already checked that this substitution is free.**
The design draws **15.805 mm**; the ISO 6432 stock size is **16.000 mm**; the shift in the required
friction fraction is **0.00 %**. *The bore does not need to be special and buying a special one
would be the expensive mistake.*

- **Seal type matters more than the cylinder.** Ask the supplier which seal is fitted. The class
  the design assumes is **spring-energised graphite-filled PTFE**; ordinary nitrile is a different
  material with different breakaway behaviour, and a nitrile result does not answer P67.
- **Buy three, not one.** Shot-to-shot spread is half the question — P67 asks for
  *"a measured or supplier-bounded seal friction, **with a shot-to-shot spread**"* — and
  unit-to-unit spread is the cheaper half of it.
- Estimated **₹1,500 – ₹4,000** for three.

### 1.2 The instrument — the binding requirement is sample rate, not accuracy

**A load cell or force gauge reading to at least 50 N, logging at ≥ 500 Hz.**

**Accuracy is not the constraint.** The thresholds are 17.8 and 22.3 N and the allowance is
83.4 N; a gauge good to ±1 N resolves all three comfortably. **What matters is capturing
*breakaway* separately from *running* friction**, and breakaway is a transient — a 1 Hz handheld
gauge will report neither.

- A logging load cell with a USB or serial output, **₹4,000 – ₹15,000**.
- **A crank-driven or dropped-mass pull is acceptable.** A servo test stand is not required and
  buying one would be the second expensive mistake.
- Estimated **₹4,000 – ₹15,000**.

### 1.3 Fixture and consumables

Rod-end clevis, a rigid mount, the lubricant the supplier specifies (**and a dry sample: space
seals are not oiled**), and a dial indicator for stroke position. **₹2,500 – ₹7,000.**

---

## 2. The measurement, and the bands

> ## THESE BANDS ARE DECLARED BEFORE THE CYLINDER IS ORDERED, 2026-08-22.
>
> **The same rule as every run sheet in `validation/`**: the acceptance criteria are committed
> before the data exists. **No band may be widened after a result is known.** A measurement whose
> criteria are chosen after seeing the number is worth what an analysis with the same habit is
> worth, which is nothing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| **1** | **Breakaway friction**, dry, at ambient, three units | **report; ≥ 3 units, ≥ 10 pulls each** | A single pull is an anecdote. The spread is the deliverable |
| **2** | **Running friction** over the stroke, same units | **report, with the 3σ spread** | This is the term A44 found carries **93.4 %** of Gen6's dispersion variance |
| **3** | **Which side of 17.8 N** the running friction falls | **decides ADR-036** | *This is the whole purpose.* It is a discrimination, not a value |
| **4** | **Which side of 22.3 N** | **decides whether A66 is ever written** | See the table above |
| **5** | **Unit-to-unit spread** ≤ 20 % of the mean | **≤ 20 %** | A44 swept ±20 % of the allowance and got 0.3115 m/s at 3σ. Above 20 % the dispersion claim is worse than modelled |
| **6** | **Speed dependence** across the achievable range | **report the trend and the range tested** | The design's mean piston speed is **17.1 m/s** and its peak is **34.3 m/s**. **A bench pull will not reach either.** Band 8 is why this is still worth doing |
| **7** | **Ambient against the design's 22.73 bar** side load | **report; state whether the rig pressurised** | Friction rises with the pressure that loads the seal against the bore. An unpressurised pull is a **lower bound**, and must be reported as one |
| **8** | **Does this measurement discriminate, or only bound?** | **state the answer explicitly, before quoting bands 3 and 4** | **The band that constrains the author.** See below |

### Band 8 is the one that decides whether the rest is worth anything

**An air-side, low-speed, possibly unpressurised bench pull is a *different* measurement from a
16 mm PTFE seal at 22.73 bar and 17 m/s in vacuum.** It is not a cheaper version of the right
measurement, and this file will not pretend otherwise.

**What it can still do:** if the measured running friction is, say, **8 N**, then the design point
sits comfortably under 17.8 N *unless* speed and vacuum together more than double it — and the
result discriminates. If it comes back at **19 N**, it lands between the thresholds and
discriminates nothing, because the corrections could push it either way.

**So band 8 requires the answer to be written down before bands 3 and 4 are quoted anywhere.**
The honest outcomes are:

1. **Well below 17.8 N** → the specification is likely met; **ADR-036 can be resolved on a stated
   margin**, and the margin is stated.
2. **Well above 22.3 N** → the stator is needed; **A66 is written**; vacuum and speed corrections
   would only make it worse, so the direction is safe.
3. **Anywhere near either threshold** → **the bench test has not answered P67**, it goes on the
   record as not having answered it, and the vacuum test is what is needed. *This is a real
   possible outcome and it is declared in advance so it cannot be argued away afterwards.*

---

## 3. What to do with the result

**Write it as `validation/B2_seal_friction.md`** with these bands copied in unchanged, the raw
pulls committed as CSV, and the verdict against each. **Then, and only then**, resolve ADR-036.

**It changes the category of evidence, not its degree.** `docs/FIGURE_INDEX.md`'s `measured`
evidence class has **zero members**, and it has been the honest description of this project since
it started. **B-1 or B-2, whichever lands first, ends that** — and the day it does,
[`E4`](../OPEN_PROBLEMS.md) stops being true and every page that says *"nothing has been built,
fired or measured"* has to be corrected in the same commit.

> **Do not let that correction be a celebration.** One measured component is one measured
> component. **The machine remains unbuilt**, and the sentence that replaces E4 should say so.

---

## Provenance

Thresholds from [ADR-036](adr/036-seal-specification-and-the-trim-stage.md) and
`analysis/results/seal_class.json` — **17.8352 N** at the thermal specification and **22.294 N** at
the trim-unnecessary fraction, both at the 15.805 mm bore and 22.7258 bar charge. Bore
substitution from [A61](../validation/A61_seal_class.md) band 7. Dispersion share from
[A44](../validation/A44_gen6_dispersion.md). Piston speeds derived from
`gen6_drive.exit_velocity_m_s_zero_friction` and `stroke_mm`.

**Every price in section 1 is an estimate and no supplier has quoted any of it.**
