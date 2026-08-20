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
| The analyses behind it | ~24 run sheets, structural FEA, circuit simulation, CFD, a designed control loop | **A35–A53**, no FEA, no circuit model, no CFD |

**And one property neither has: anything measured.** **E4** is open, and no amount of what follows
changes that.

> **"Final" is a stronger word than this project has used before.** Phase I did not declare Gen5
> final; it declared it **frozen with three kill criteria crossed and stated as such.** The honest
> target for Gen6 is the same: **frozen, with its exceptions named on the front page** — not a
> claim that nothing further will change.

---

## Category A — closable by analysis, and nothing else is needed

> **Rewritten 2026-08-19.** This section previously listed **A49–A55** against a provisional
> numbering made before the design surface existed. **Five of those runs have since happened and
> took different numbers**, and one of them — the design surface — was not on the list at all. What
> follows is the actual state, not the plan.

**What has run since this file was written:**

| | | What it did |
|---|---|---|
| **[A49](../validation/A49_design_surface.md)** | the velocity/acceleration/stroke surface | **7 of 9.** Found 14 dominating points and produced [ADR-034](adr/034-gen6-long-stroke-design-point.md). Band 6 failed and is **P78** |
| **[A50](../validation/A50_campaign_altitude.md)** | the campaign with altitude free | Satellite life **476.6 d at 450 km**; three 50 km shells for **≈ 55 m/s**. Opened **P79**; **E28** stays open until the decay model meets a variable atmosphere |
| **[A51](../validation/A51_gen6_power.md)** | power and efficiency end to end | **7 of 8. 311.76 J/shot, 0.26 W average, 36 W peak.** Traced the repeated "25–131 W" to a spring figure — **P80** |
| **[A52](../validation/A52_gen6_recoil.md)** | recoil and angular impulse | **7 of 7.** 116.03 N·s/shot, **1.81×** Gen5. Answered **E29** and closed a NEEDS SOURCE row: **the thrust line must pass within 10.7 mm of the host centre of mass** |
| **[A53](../validation/A53_backup_ejector.md)** | the per-cell backup ejector | **7 of 8.** Band 7 failed by **40.4×** at 2.18 m and by **148×** at ADR-034's 8.0 m — **P81**. The highest-value reliability change in the record does not fit the architecture |

**What is still Category A, renumbered to what is actually free:**

| | | Why it matters |
|---|---|---|
| ~~**A54**~~ | ~~Weigh the pulse chain~~ — **RUN 2026-08-19**, one of eight, **closed P77, opened P86** | **P77**, and ADR-033's first falsifier. If it exceeds the 0.340 kg section it feeds, the trim stage costs more than it corrects and ADR-033 reverses |
| ~~**A55**~~ | ~~Re-run A44 and A48 at ADR-034's friction share~~ — **RUN 2026-08-19**, four of nine, **closed P83 and P84** | **P83 and P84.** The trim authority was sized at a **9.75 %** friction share and the design point now runs at **28.39 %** — and the scripts still read the old stroke, so A44 and A48 are answering a superseded question. Both are new, both HIGH, and ADR-034 created them |
| ~~**A56**~~ | ~~Re-run A43 at 22.73 bar~~ — **RUN 2026-08-19**, eight of nine, **closed P82**, opened **P87** | **P82.** The store saving is the whole of ADR-034's mass argument and it is currently a gas-ratio scaling. Carries **P84**'s repair: `precharged.py` reads the design point rather than declaring it |
| **A57** | **Attitude rate and packaging on the stage** | The two remaining **NEEDS SOURCE** rows in `KILL_CRITERIA.md`. Recoil was the third and A52 closed it |
| **A58** | **A thermal model of the chamber and reservoir across a campaign** | A43 settled the reservoir between shots; nothing models the chamber, the expansion cooling, or twelve cycles of it |
| ~~**A59**~~ | ~~Structural case for the drive tube and stage rail~~ — **RUN 2026-08-19**, six of nine, opened **P85** | **ADR-034 made this urgent.** The tube is the cylinder *and* the rail, it is now **8.0 m** long at **1.0 mm** wall, and `build_gen6.py` says in its own docstring that neither bending nor alignment is modelled. A49's own note says every omission in it flatters a long tube |
| **A60** | **A second CAD implementation of Gen6** | Gen5 has one and **it found P71 on its first run** — both rollers outside their channels in every STEP ever built. Gen6 has never been checked by anything but the script that built it |

## Category B — bookkeeping

- **Publish P68's honest range wherever added mass appears** — at ADR-034, **1.296 kg** is the full-credit figure and **3.164 kg** is the hostile one. Both, everywhere, not the flattering one.
- **Move the headline numbers to Gen6** once A54–A60 land, or **state explicitly that they remain Gen5's.** Today the front page carries Gen5's numbers under a Gen6 design target, which is honest only because it says so.

## Category C — needs a decision from you, and analysis cannot substitute

| | | Cost of not deciding |
|---|---|---|
| **D2 — the payload class** | **P59.** A35 closed the architecture route and A36 closed the manifest route. **Smaller payloads are the only remaining path to kill criterion 1**, and the decision has been deferred since Phase I | The criterion stays crossed at **5.3×** and the front page keeps saying so |
| **The enclosure panel** | Monolithic 2 mm at 50.04 kg against honeycomb at 29.98. **20 kg for the price of an ADR** | Dry mass stays 126.6 kg and every per-satellite figure stays inflated |
| **What replaces the trim stage** | **[A54](../validation/A54_pulse_chain.md) fired ADR-033's falsifier.** Three routes: a store at **23.2 kW/kg** (not in the record), a **shorter stroke** off A49's published surface (needs no new data), or **withdrawal** — which deletes the commanded-velocity claim. **P86** | Gen6 has no working correction, and the product's central claim is unsupported |
| **Whether any of it survives P67** | If the measured friction is small, the dispersion is not there and **the stage, its store and P86 all close together** | Mass and complexity spent on a problem that may not exist |
| **What "final" means** | Frozen-with-exceptions, as Gen5 was — or a claim that nothing further changes | A claim the evidence does not support |

## Category D — needs hardware or an external party

**This is where "most stable" actually gets decided, and none of it is computation.**

| | |
|---|---|
| **P67 — measure the seal friction** | A bench test on a piston seal at 22.73 bar in vacuum, with a shot-to-shot spread. **It owns 93.4 % of the dispersion, it is ADR-033's whole justification, and it can delete the trim stage rather than validate it.** The single highest-leverage action in the entire Gen6 record |
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

**Updated 2026-08-19, after A49–A53 and ADR-034.**

**1. Measure the seal friction (P67).** It is Category D, it is cheap, and it can *delete* work
rather than add it. **It now governs five open decisions rather than four** — ADR-034's design
point, ADR-033's trim stage, P77's pulse store, P81's ejector, and P83's authority — because
ADR-034 took friction from 9.75 % to **28.39 %** of shot work. **The single highest-leverage action
in the record, and ADR-034 raised its leverage.**

**2. ~~A55, re-run A44 and A48 at the new friction.~~ RUN 2026-08-19.** Four of nine. **The trim
section was 3.57× under-authority and is resized 39.7 → 144.01 mm**, and `precharged.py` now
derives the design point with a gate that fails on drift. **P83 and P84 both close.** What it did
*not* do is aggravate P77 — peak power moved 2.8 %. If the authority has to grow, ADR-033's unweighed pulse store grows with it.

**3. ~~A54, the pulse chain.~~ RUN 2026-08-19.** One of eight. **ADR-033's first falsifier fired**:
the store weighs **23.44–37.36 kg** against the 1.2328 kg section, and the trim stage asks for
**93.3 % of the peak current** of the chain ADR-032 deleted. **P77 closes, P86 opens**, and what is
left is a decision rather than an analysis.

**4. ~~A59, the structural case.~~ RUN 2026-08-19.** Six of nine. **The tube buckles under its own
shot reaction by 45×** and needs **seven supports at 1.0 m spacing**, which cost **99.7 g** — the
mass worry that put this run first was unfounded. **What it found instead is P85**: the tube's
material is stated nowhere, and it is 1.140 kg in aluminium against 3.294 in steel.

**5. Decide D2 and the enclosure panel.** Two decisions, both yours, together worth more than any
analysis on this page — one is the only route to kill criterion 1, the other is 20 kg.

**6. ~~A56~~, A57, A58** — **A56 ran 2026-08-19**: the store is **3.1216 kg**, 24 % below the
figure ADR-034 quoted, and **P82 closes.** A57 and A58 still owe the two NEEDS SOURCE rows and the
thermal work Gen5 has.

**7. A60, the second implementation.** Do it *last*, when the design has stopped moving, because
its value is catching what the first implementation got wrong and it should check the final
geometry. **ADR-034 is a reminder that the design has not stopped moving.**

**8. Then freeze — with the exceptions named**, exactly as Phase I did.

## What this does not buy

**Kill criterion 1 stays crossed** unless D2 changes the payload class. **E30 stays open** unless
the ejector is built, not merely designed. **And E4 stays open regardless.** A frozen Gen6 is a
design whose computation is finished and whose evidence has not started.
