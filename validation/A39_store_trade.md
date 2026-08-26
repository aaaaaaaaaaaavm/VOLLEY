# A39, the energy store at metre-scale strokes

**Bands declared 2026-08-14, before `analysis/store_trade.py` existed.**
Verify with `git show --stat <this commit> -- analysis/store_trade.py`, which must return nothing.

---

## Why this run exists

**P60.** [A37](A37_host_integrated.md) bands 4 and 8 failed. Once the stage supplies the structure
and the pulse chain is deleted, the energy store becomes the binding constraint, 26.16 kg of
spring steel at an 8 m stroke, **78.5 % of everything added.** Band 4 was the falsification test
[A35](A35_constraint_ledger.md) declared and left open, and it says the mass *relocated* rather
than left.

[A38](A38_tipoff_at_gen6.md) has since established that tip-off does not bind, its ceiling is
30.9 g against a 25 g qualification cap, so the acceleration is free and the store is the only
thing left setting the design point.

## The budget, and where each number comes from

| | |
|---|---:|
| Added base — containment, A37 and A36 agreeing from opposite directions | **11.45 kg** |
| Kill criterion 1 at 12 satellites | 2.0 kg × 12 = **24.00 kg** |
| **Budget for store + mechanism** | **12.55 kg** |
| A35's falsifier, the looser of the two | **14.26 kg** |
| A37's feasible window | **1.83–2.18 m, 30.0–32.7 m/s** |
| Acceleration cap | **25 g** (qualification), tip-off permits 30.9 |

## What is traded, and what is excluded

Steel spring, at the 300 J/kg `analysis/actuator_trade.py` already declares as the upper end
for spring steel. Cold gas, which A37 deliberately excluded and which this run exists partly to
size. Keeping the linear synchronous motor, as the control.

Three options are screened out by runs already on the record and are carried in the table with
their reason, so the trade cannot be read as having considered only two:

| | Screened by |
|---|---|
| Lead screw | [A27](A27_actuator_trade.md) — DN limit exceeded 8×, whirling 36× |
| Rack and pinion | A27 — contact drive at full speed in vacuum, **E21** |
| Flywheel through a cable or drum | `VOLLEY-lab` PII-14 — `m_eff = I/r²` refers rotating inertia straight onto the moving mass |

## The gas model, declared before the script

This is where this run can be wrong, so every assumption is stated here rather than in the
code. None is measured and none is vendor-sourced.

| | Value | Note |
|---|---|---|
| Vessel figure of merit | **PV/W = 15 000 m** | Conservative end of the modern composite range |
| Storage pressure | **200 bar** | |
| Working pressure at the piston | **50 bar** | Regulated; blowdown to this floor |
| Cylinder allowable stress | **500 MPa**, safety factor 2 | Steel tube in hoop |
| Minimum practical wall | **1.0 mm** | Hoop stress alone gives far less and cannot be built |
| Gas density at storage | **235 kg/m³** | Nitrogen-class at 200 bar |
| Piston, seals, regulator, valving | **1.5 kg** fixed allowance | **The largest guess in this run** |

The reservoir is sized for the whole manifest, not per shot. If one bottle runs twelve shots,
the wind mechanism the spring needs is replaced by a valve, and that, not the store mass alone,
is what the trade is really about.

Mechanism, for the spring: `max(2.0 kg, 0.60 × store)`, unchanged from A37 so the two runs
compare. It remains a declared assumption with no derivation.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | The steel-spring row reproduces A37's store + mechanism at A37's selected point to **1 %** | The model is not the one that produced A37 and nothing below is comparable — the A38 band 1 lesson applied deliberately |
| **2** | At least one store keeps **store + mechanism ≤ 12.55 kg** at **≥ 30 m/s** | Nothing fits the kill-criterion budget at the velocity A37's window needs, and Gen6 has no design point |
| **3** | The selected store is inside **A35's 14.26 kg falsifier** | The mass relocated after all, and A35's C3 result does not mean what it appeared to |
| **4** | The selected store reaches **≥ 35 m/s** while still inside the falsifier | **The velocity goal has no headroom.** A store that fits only at the bottom of A37's window means the design is at its limit the day it is drawn |
| **5** | **Every** screened-out option carries the run that screened it | The trade looks narrower than the record supports |
| **6** | The control — keeping the LSM — **exceeds** the 12.55 kg budget | The trade is rigged: if the incumbent fits, there was nothing to decide |
| **7** | The selected store holds its energy from launch through the campaign **without active maintenance**, or the row names what maintains it | An unstated standby requirement is hiding in the answer |

### Band 4 is the one that decides the shape of Gen6

A store that fits at 30 m/s and busts at 33 is a design with no margin on the only claim A21-R left
standing. **Band 4 asks for headroom, not feasibility.**

### Band 6 exists because this trade has an obvious answer

The incumbent has already been deleted by A35 and A37, so a trade that "discovers" it should lose is
worth nothing. Band 6 makes the control's failure an explicit result rather than an assumption.

### Band 7 is where gas is most likely to lose

A spring holds its energy indefinitely and a gas store leaks. If gas wins on mass and loses on
standby, that is the finding, and it belongs in the table rather than in a footnote.

## What this run does not do

It does not design a cylinder, a valve, a seal or a latch; does not model blowdown transients,
temperature effects on stored pressure, or the release-residual requirement A34 puts at <= 1 N; and
does not price qualification of a pressure vessel. It compares stores on mass and standby at a
declared operating point, and every assumption above makes gas look better than a detailed design
will.

---

## Results

**RUN 2026-08-14. Seven of seven bands pass. Gas wins by a factor of four, and A35's falsifier
settles.

| # | Band | Result | |
|---|---|---|---|
| 1 | spring reproduces A37 to 1 % | 41.80 against 41.86 kg | **PASS** |
| 2 | some store ≤ 12.55 kg at ≥ 30 m/s | **2.98 kg** | **PASS** |
| 3 | selected inside the 14.26 kg falsifier | **2.98 kg** | **PASS** |
| 4 | selected reaches ≥ 35 m/s inside it | **96.0 m/s** | **PASS** |
| 5 | screened-out options each cite their run | 3 of 3 | **PASS** |
| 6 | the control exceeds the budget | LSM **23.76 kg** | **PASS** |
| 7 | standby named | leaks; needs a seal that holds to the last shot | **PASS** |

### At 32.7 m/s, the top of A37's window

| | store | mechanism | **total** | busts the budget at |
|---|---:|---:|---:|---:|
| Steel spring | 7.13 | 4.28 | **11.41 kg** | 34.3 m/s |
| **Cold gas** | 0.63 | 2.34 | **2.98 kg** | **89.4 m/s** |
| Keep the LSM *(control)* | 23.76 | — | **23.76 kg** | fails at every velocity |

Gas detail: 15.8 mm bore, 1.00 mm wall, 0.84 kg of cylinder, and a 1.71 litre reservoir
0.233 kg of vessel plus 0.402 kg of gas, for all twelve shots.

### The reason gas wins is not energy density

It is that one bottle runs the manifest. A spring stores 7.13 kg of energy and then needs
4.28 kg of mechanism to re-arm it twelve times. Gas separates the store from the actuator, so
re-arming is a valve.

> The spring's problem was never storing the energy. It was having to be cocked twelve times.

### A35's falsification test settles, and it passes

A35 predicted that deleting the pulse would remove more than 40 % of dry mass, measured 28.1 %,
and declared: *the falsifier is that its replacement weighs more than 60 % of what came out*,
14.26 kg of the 23.76 kg released.

The replacement weighs 2.98 kg. The mass did not relocate. A35's result means what it
appeared to mean**, and A37 bands 4 and 8 failed against a store that was the wrong store.

### And the binding constraint moves again, to stroke length

Gas fits the budget out to 89.4 m/s, which at the 25 g cap needs 18.8 m of stroke. No stage
class in A37 offers that. Mass has stopped being the constraint on velocity and stage length has
become it, which is a much better problem, and the one your reframe was aimed at.

### Where this is most likely wrong, and by how much

The run sheet declared that every assumption favours gas. Checking that honestly:

| | Stated | Likely | Effect |
|---|---|---|---|
| **Reservoir vessel** | 0.233 kg at PV/W = 15 000 m | Real 1.7 L / 200 bar vessels are **1–1.5 kg** | **Underestimated 4–6×** |
| **Hardware allowance** | 1.5 kg, the run's largest guess | could be 3–4 kg | Over half the total |
| **Cylinder wall** | 1.0 mm minimum, hoop needs 0.16 | must also serve as rail and take A38's **202 N** preload | Not modelled |

Corrected for all three, gas lands near 6 kg, still inside the 12.55 kg budget, still beating
the spring by ~2×, and still passing every band. **The conclusion survives the assumptions being
wrong by factors of several, which is the only reason it is worth reporting at this level of
detail.

What is not survivable by arithmetic is the blowdown transient: filling a 0.43 litre swept
volume in a 133 ms stroke means roughly 3 L/s at working pressure through a regulator, and
nothing here models it. That, and the seal, are where gas will actually be decided.

### What this does not answer

No cylinder, valve, seal or latch is designed. No blowdown transient, no temperature effect on
stored pressure, no pressure-vessel qualification, and no check against A34's <= 1 N release
residual. Gas removes a mass problem and introduces a fluid-system problem, and this run has
sized the first and not the second.
