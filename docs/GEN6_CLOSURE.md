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
| ~~**A57**~~ | ~~Attitude rate and packaging on the stage~~ — **RUN 2026-08-22**, seven of eight, **band 6 fails as declared**, opened **P99** and **P100** | **Both rows close.** Attitude rate is *answered*: **0.0112° per shot** at 300 kg, 0.135° over an uncorrected campaign, at A52's 10.65 mm alignment requirement. Envelope closes as a **measured 200 mm miss** costing **1.2579 %** of exit velocity if the stroke absorbs it. *The run first used a lever arm 15.6× that requirement — **P100** — and no band verdict moved when it was corrected* |
| ~~**A58**~~ | ~~A thermal model of the chamber and reservoir across a campaign~~ — **RUN 2026-08-19**, six of eight, **opened P88** | A43 settled the reservoir between shots; nothing models the chamber, the expansion cooling, or twelve cycles of it |
| ~~**A59**~~ | ~~Structural case for the drive tube and stage rail~~ — **RUN 2026-08-19**, six of nine, opened **P85** | **ADR-034 made this urgent.** The tube is the cylinder *and* the rail, it is now **8.0 m** long at **1.0 mm** wall, and `build_gen6.py` says in its own docstring that neither bending nor alignment is modelled. A49's own note says every omission in it flatters a long tube |
| **A60** | **A second CAD implementation of Gen6** | Gen5 has one and **it found P71 on its first run** — both rollers outside their channels in every STEP ever built. Gen6 has never been checked by anything but the script that built it |

## Category B — bookkeeping

- **Publish P68's honest range wherever added mass appears.** *Done 2026-08-20, and the figures moved:* at **A56's sized store** the full-credit figure is **1.2145 kg** and the hostile one **3.0827 kg** ([A45-R2](../validation/A45R2_stage_credit_resized_store.md)). The 1.296 / 3.164 pair was ADR-034's **scaled** store. **Both ends, everywhere, not the flattering one** — and any page quoting **1.3173** must say it includes a trim stage [ADR-036](adr/036-seal-specification-and-the-trim-stage.md) suspended.
- **Move the headline numbers to Gen6** once A54–A60 land, or **state explicitly that they remain Gen5's.** Today the front page carries Gen5's numbers under a Gen6 design target, which is honest only because it says so.

## Category C — needs a decision from you, and analysis cannot substitute

| | | Cost of not deciding |
|---|---|---|
| **D2 — the payload class** | **P59.** A35 closed the architecture route and A36 closed the manifest route. **Smaller payloads are the only remaining path to kill criterion 1**, and the decision has been deferred since Phase I. **Both cases are written out as of 2026-08-22 — [`D2_DECISION.md`](D2_DECISION.md)** — and the ladder they rest on had to be re-run to write them ([P101](../OPEN_PROBLEMS.md)). **Only the two PocketQube rungs close the criterion, and they close it by giving up the per-satellite differential**: 24 satellites share one commanded velocity at 1P against one at 3U | The criterion stays crossed at **5.3×** and the front page keeps saying so |
| **The enclosure panel** | Monolithic 2 mm at 50.04 kg against honeycomb at 29.98. **20 kg for the price of an ADR** — *and [`D2_DECISION.md`](D2_DECISION.md) prices it: it closes no criterion at any payload class. What it buys is that **58.6 % of the Gen6 stage credit** stops resting on one assumption about somebody else's skin* | Dry mass stays 126.6 kg and every per-satellite figure stays inflated |
| ~~**What replaces the trim stage**~~ | **ANSWERED 2026-08-20.** [A64](../validation/A64_pulse_store_technology.md) priced the store at **~70 g** against A54's 23–37 kg — **P86 closed, ADR-033 falsifier 1 does not fire.** *A61's route, a specified seal that deletes the stage, is still cheaper* |
| ~~superseded~~ | **[A54](../validation/A54_pulse_chain.md) fired ADR-033's falsifier**, and it was never a consequence of the stroke — the store is sized by power, which the stroke does not enter. Two routes: a store technology at **ESR × C ≤ 36.3 ms** against an EDLC's 690–1100 (**one datasheet decides it**), or **withdrawal** — which deletes the commanded-velocity claim. **P86** | Gen6 has no working correction, and the product's central claim is unsupported |
| **Whether any of it survives P67** | If the measured friction is small, the dispersion is not there and **the stage, its store and P86 all close together** | Mass and complexity spent on a problem that may not exist |
| **What "final" means** | Frozen-with-exceptions, as Gen5 was — or a claim that nothing further changes | A claim the evidence does not support |

## Category D — needs hardware or an external party

**This is where "most stable" actually gets decided, and none of it is computation.**

| | |
|---|---|
| **A seal specification** | **[A61](../validation/A61_seal_class.md) produced one: 17.8 N, 4.00 % of the piston pressure force, with the thermal case binding.** `cad/parameters.json` still carries no seal. **P89** — and it is one line of specification that closes **P88** and deletes **P86**'s requirement |
| **P67 — measure the seal friction** | **It owns 98.7 % of the dispersion, it is ADR-033's whole justification, and it can delete the trim stage rather than validate it.** Still the single highest-leverage action in the record — and [A58](../validation/A58_chamber_thermal.md) showed it is a harder test than described: **at −35.2 °C, on a seal dissipating 667.2 J per stroke at 2419 W, over 8.0 m, twelve times.** A room-temperature coefficient on a short rig does not answer it (**P88**). **And it now has a number to be measured against — 17.8 N (P89) — rather than nothing** |
| **The cradle** | 201.7 N per contact releasing inside ≤ 1 N, now holding magnets in alignment too. **It does not exist in any file.** Kill criterion 4 stays *modelled, not demonstrated* until it does. *The 201.7 N is A38's figure at the 25 g cap; at ADR-034's design point the requirement is **91.7 N** — [P102](../OPEN_PROBLEMS.md) — and the higher number is left standing as the conservative one* |
| **The eight metres after the cradle** — **[P103](../OPEN_PROBLEMS.md), and it is LIVE** | **Nothing models them.** [A34](../validation/A34_cradle_restitution.md) and [A38](../validation/A38_tipoff_at_gen6.md) model the payload crossing its cradle clearance; there is no contact state along the bore, no straightness or roundness, no force-line eccentricity and no payload centre-of-mass offset anywhere in the record, so **Gen6 has no exit angular or lateral state at all**. **The nearest published work makes precisely those the dominant terms in release attitude** — [`EXTERNAL_EVIDENCE.md`](EXTERNAL_EVIDENCE.md). *This is a calibrated model behind a measurement, not a measurement: **B-2 is still first**, and bands 9–14 were added to it so the pulls it produces can serve as calibration rather than as one number* |
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
rather than add it. **It has an order as of 2026-08-22 — [`B2_ORDER.md`](B2_ORDER.md) — with its
bands declared before the cylinder is bought.** **It now governs five open decisions rather than four** — ADR-034's design
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
**Both business cases are now written side by side, 2026-08-22 —
[`D2_DECISION.md`](D2_DECISION.md).** It does not decide either, and it removes the arithmetic
from both: **D2 is a choice between closing kill criterion 1 and keeping the commanded
per-satellite velocity**, and the enclosure panel changes no verdict on either numerator at any
payload class. **Writing it found that the payload ladder the decision turns on had never been
re-run after A46** — three vintages of one table, disagreeing about every rung
([P101](../OPEN_PROBLEMS.md)).

**6. ~~A56, A57, A58~~ — all three have run.** A56 and A58 on 2026-08-19, **A57 on 2026-08-22.** The store is **3.1216 kg**,
24 % below the figure ADR-034 quoted (**P82 closes**), and the bulk thermal case is comfortable
while **the seal cannot absorb its own friction** (**P88**). **A57 closed both NEEDS SOURCE rows**, and its most useful
output was not either of them: **the lever arm dominates the attitude result and the architecture
barely enters it.** The run first said Gen6 was 2.33× worse than Gen5 per shot and, at each
architecture's own arm, it is about a seventh — **P100**. **P99** is what it opened.

**7. A60, the second implementation.** Do it *last*, when the design has stopped moving, because
its value is catching what the first implementation got wrong and it should check the final
geometry. **ADR-034 is a reminder that the design has not stopped moving.**

> **Amended 2026-08-22: A60 was carrying a load it cannot lift.** It was the planned answer to
> "how do we stop getting these wrong", and it is the wrong shape for the defects actually
> occurring. **P83, P84, P96, P97 and P100 — five entries in ten days — are all two files
> disagreeing about a shared quantity.** A second CAD implementation catches *geometry* errors, of
> the kind A60 found in Gen5 as P71; it catches none of those five.
>
> **`tools/check_crossrefs.py` is the right shape**, and it exists now: eighteen declared pairs, each
> with the reason they must agree, and two pairs recorded as deliberately excluded because they
> are meant to differ. **Replayed against all seven historical defects, it catches all seven.**
>
> **A60 keeps its place and loses its overload.** It is still worth doing, still last, and it is
> now expected to find geometry rather than to prevent propagation failures it never could.

**8. Then freeze — with the exceptions named**, exactly as Phase I did.

## What this does not buy

**Kill criterion 1 stays crossed** unless D2 changes the payload class. **E30 stays open** unless
the ejector is built, not merely designed. **And E4 stays open regardless.** A frozen Gen6 is a
design whose computation is finished and whose evidence has not started.
