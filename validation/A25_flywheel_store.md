# A25: a flywheel instead of the supercapacitor bank

**Targets:** **P26** — the bank cannot source the shot on purchasable parts — which
`OPEN_PROBLEMS.md` and `docs/KILL_CRITERIA.md` both treat as the largest live defect in the
project.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/flywheel_store.py` EXISTS.
>
> Everything below is committed before the script is written, and the script is absent at this
> commit. Verify with `git show --stat <this commit> -- analysis/flywheel_store.py`, which
> returns nothing.

## What is being tested, and why it is a Phase I item

**P26 is a property of capacitors, not of the machine.** A10 established that a source of EMF `V`
behind series resistance `R` cannot deliver more than `V²/4R` into any load, so the shot imposes
a **68 mΩ ESR ceiling**. A single commercial string of 32 × 190 F cells is **116–185 mΩ**. Nothing
clears it; three to four parallel strings are required, and that mass lands directly on kill
criterion 1.

Worse, the ceiling *falls* as velocity rises, so it inverts the ranking of every lever in
`DESIGN_OPTIONS_exit_velocity.md`: the two rows that look best electromagnetically are the two
that make the bank hardest to buy.

**A flywheel motor-generator stores the same energy behind a different impedance.** It does not
care what load it feeds, so — unlike everything else considered on 2026-08-10 — **it requires no
architecture change.** The ironless Halbach LSM, the sled, the track, the cassettes, the release
and every one of A1–A24 stand untouched. Only the energy store changes.

This item was extracted from **PII-14**, which was declined for Phase I on margin. It is assessed
here on its own, because it does not depend on any part of that concept.

## Acceptance bands

**Six bands. Bands 4 and 6 can fail, and band 6 failing would end the idea outright.**

### Band 1 — the demand is imported, not restated

Shot energy and peak electrical power are taken from `analysis/motor_model.py` by import and
reproduce `analysis/results/motor_results.json` to **0.00 %**: **2559.5 J net drawn**, and peak
power computed from the same integrator rather than assumed.

Every previous attempt to restate an operating point in a second file produced a fork (P16, P19).
**FAIL on any discrepancy.**

### Band 2 — the rotor is not running at the edge of its material

At the speed required to store **2×** the shot energy in a rotor of **≤ 3 kg**, the rim stress
margin against a stated material allowable is **≥ 3.0**.

`σ ≈ ρv²` for a thin rim. The allowable must be named and its source stated; if the only honest
answer is a textbook value for a generic alloy, that is what gets written. **FAIL below 3.0.**

### Band 3 — the flywheel does not stall itself delivering one shot

Speed droop across a single 158 ms shot is **≤ 30 %**, so the store retains **≥ 49 %** of its
energy and the converter never sees a collapsing source.

This is what sets the oversizing factor, and it is why band 2 sizes for 2× rather than 1×.

### Band 4 — it must actually be lighter than the bank it replaces

Total flywheel system mass — rotor, motor-generator, bearings, containment and converter —
is **≤ the supercapacitor bank mass at the 3-string configuration P26 requires**.

`analysis/mass_properties.py` carries **6.50 kg** for "supercapacitor cells + busbars" at one
string. Three strings is the honest current position under P26.

**This band may fail.** A 33 kW machine plus containment is not light, and containment is not
optional for a rotor at several thousand rpm. If it fails, the flywheel buys impedance and pays
mass, and that trade must be stated rather than hidden.

### Band 5 — the store must not become an attitude problem

Net stored angular momentum of the flywheel assembly is **≤ 0.5 N·m·s**, which for a single rotor
of the required size means **a counter-rotating pair is mandatory, not optional**.

A single rotor at ~6,800 rpm stores of order **7 N·m·s** against a shot angular impulse of
**3.28 N·m·s** at a 50 mm CoM miss. An uncancelled store of that size is a second attitude
problem bolted to the first. **FAIL above 0.5 N·m·s net.**

### Band 6 — the whole point: does it clear the ceiling the bank fails?

The flywheel path's **equivalent series resistance referred to the same node as the bank's**,
including machine winding resistance and converter contribution, is **≤ 68 mΩ** — the ceiling
A10 derived and the bank misses.

**This is the band the exercise exists for, and it may fail.** A rotating machine is not
automatically stiffer than a capacitor: a synchronous machine delivering 347 A has winding
resistance and synchronous reactance of its own, and at 158 ms the reactance is not negligible.
**If band 6 fails, the flywheel does not solve P26 and the idea ends here**, whatever bands 1–5
say.

## What this cannot settle

- **No component is quoted.** Rotor, machine, bearings and converter masses are engineering
  estimates. `analysis/cost.py` already carries no vendor quotation and this adds none.
- **Bearings in vacuum for a multi-thousand-rpm rotor across a multi-year mission** are not
  designed here, and are a credible reason the whole idea fails on reliability rather than physics.
- **Nothing here is a qualification argument.** A spinning rotor through launch is a restraint
  problem this does not address.
- **The comparison is against the bank as the repository models it**, which is itself parametric.
  A better bank model could move the target.
