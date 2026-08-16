# What stands between Gen6 and being the frozen baseline

**Asked directly: make Gen6 the final and most stable version. This is what that costs.**

**It is written to the same categories Phase I used to freeze Gen5** — closable by analysis,
bookkeeping, needs a decision, needs hardware or an external party, blocked, cannot close — because
that instrument worked once and a different one would not be comparable.

---

## First, what "frozen baseline" actually means here

**Gen5 earned the label on five properties**, and Gen6 currently has two of them.

| | Gen5 | Gen6 |
|---|---|---|
| Built by a script from `parameters.json` | **yes** | **yes** |
| Rebuilds byte-identically from a clean clone | **yes** | **yes** |
| Every headline number computed against it | **yes** | **no** — the numbers are still Gen5's |
| A second implementation checking the first | **yes** — and it found **P71** | **no** |
| The analyses behind it | ~24 run sheets, structural FEA, circuit simulation, CFD, a designed control loop | **A35–A48**, no FEA, no circuit model, no CFD |

**And one property neither has: anything measured.** **E4** is open, and no amount of what follows
changes that.

> **"Final" is a stronger word than this project has used before.** Phase I did not declare Gen5
> final; it declared it **frozen with three kill criteria crossed and stated as such.** The honest
> target for Gen6 is the same: **frozen, with its exceptions named on the front page** — not a
> claim that nothing further will change.

---

## Category A — closable by analysis, and nothing else is needed

**Seven runs. All computation. This is the part that can start now.**

| | | Why it matters |
|---|---|---|
| **A49** | **Weigh the pulse chain** — 37.7 J at 28 kW: store, switch, conductors | **P77**, and ADR-033's first falsifier. If it exceeds the 0.340 kg section it feeds, the trim stage costs more than it corrects and ADR-033 reverses |
| **A50** | **Recoil and angular impulse at Gen6** | Two of the four **NEEDS SOURCE** rows in `KILL_CRITERIA.md`. Recoil scales with impulse and the impulse has roughly doubled. **E29** is the same question and is live |
| **A51** | **Design the per-cell backup ejector** — mass, volume, its own failure rate | **P75**. A47 priced it at **+2.27 satellites** against the architecture change's **+0.37**. It is the highest-value change identified anywhere in the record |
| **A52** | **Attitude rate and packaging on the stage** | The remaining two **NEEDS SOURCE** rows |
| **A53** | **A thermal model of the chamber and reservoir across a campaign** | A43 settled the reservoir between shots; nothing models the chamber, the expansion cooling, or twelve cycles of it |
| **A54** | **A second CAD implementation of Gen6** | Gen5 has one and **it found P71 on its first run** — both rollers outside their channels in every STEP ever built. Gen6 has never been checked by anything but the script that built it |
| **A55** | **Structural case for the drive tube and stage rail** | The tube is the cylinder *and* the rail, carrying 201.7 N of cradle preload. `build_gen6.py` says in its own docstring that neither is modelled |

## Category B — bookkeeping

- **Publish P68's honest range wherever added mass appears** — 1.431 kg is the full-credit figure and **3.299 kg** is the hostile one. Both, everywhere, not the flattering one.
- **Move the headline numbers to Gen6** once A49–A55 land, or **state explicitly that they remain Gen5's.** Today the front page carries Gen5's numbers under a Gen6 design target, which is honest only because it says so.

## Category C — needs a decision from you, and analysis cannot substitute

| | | Cost of not deciding |
|---|---|---|
| **D2 — the payload class** | **P59.** A35 closed the architecture route and A36 closed the manifest route. **Smaller payloads are the only remaining path to kill criterion 1**, and the decision has been deferred since Phase I | The criterion stays crossed at **5.3×** and the front page keeps saying so |
| **The enclosure panel** | Monolithic 2 mm at 50.04 kg against honeycomb at 29.98. **20 kg for the price of an ADR** | Dry mass stays 126.6 kg and every per-satellite figure stays inflated |
| **Whether the trim stage survives P67** | If the measured friction is small, ADR-033 is unnecessary and **P77 closes for free** | Mass and complexity spent on a problem that may not exist |
| **What "final" means** | Frozen-with-exceptions, as Gen5 was — or a claim that nothing further changes | A claim the evidence does not support |

## Category D — needs hardware or an external party

**This is where "most stable" actually gets decided, and none of it is computation.**

| | |
|---|---|
| **P67 — measure the seal friction** | A bench test on a piston seal at 50 bar in vacuum, with a shot-to-shot spread. **It owns 93.4 % of the dispersion, it is ADR-033's whole justification, and it can delete the trim stage rather than validate it.** The single highest-leverage action in the entire Gen6 record |
| **The cradle** | 201.7 N per contact releasing inside ≤ 1 N, now holding magnets in alignment too. **It does not exist in any file.** Kill criterion 4 stays *modelled, not demonstrated* until it does |
| **The piston, seals, valves and plumbing** | A41 allows 1.5 kg and designs none of it |
| **A stage** | No launch provider has agreed to keep one alive past passivation. **A47 counts this as manifest-forfeiting**, and it is the one shared element the project cannot engineer around |
| **E4 / B-1** | Nothing built, fired or measured. Note that **B-1 as specified is a Halbach-array measurement**, and Gen6 has no Halbach arrays except the trim stage's — so **the order itself needs restating for this architecture** |

## Category E — blocked

- **P57**, the voice-coil deployer, needs institutional access.
- **P62**, the wiki, needs a push this environment refuses.
- **P74**, the Fusion documents, needs an export nobody has done.

## Category F — cannot close, and should not be claimed

**E4.** Until something is built, every number in this repository is a model output. **Freezing
Gen6 does not change that and must not be presented as if it did.**

---

## The order I would do it in

**1. Measure the seal friction (P67).** It is Category D, it is cheap, and it can *delete* work
rather than add it — if the friction is small, the trim stage, its pulse store, P77 and ADR-033
all close together. **Doing analysis before this measurement risks pricing hardware for a problem
that is not there.**

**2. A49, the pulse chain.** If P67 cannot be run first, this is the one that decides whether
ADR-033 stands. It is a day of work and it is a falsifier.

**3. A51, the per-cell ejector.** Highest value per unit effort in the record: **six times the
reliability gain of the entire architecture change.**

**4. Decide D2 and the enclosure panel.** Two decisions, both yours, together worth more than any
analysis on this page — one is the only route to kill criterion 1, the other is 20 kg.

**5. A50, A52, A53, A55** — close the four NEEDS SOURCE rows and give Gen6 the structural and
thermal work Gen5 has.

**6. A54, the second implementation.** Do it *last*, when the design has stopped moving, because
its value is catching what the first implementation got wrong and it should check the final
geometry.

**7. Then freeze — with the exceptions named**, exactly as Phase I did.

## What this does not buy

**Kill criterion 1 stays crossed** unless D2 changes the payload class. **E30 stays open** unless
the ejector is built, not merely designed. **And E4 stays open regardless.** A frozen Gen6 is a
design whose computation is finished and whose evidence has not started.
