# Where this project actually stands

Written 2026-08-13. Four questions a reviewer, a referee or a hiring manager will ask, answered
in one place: what decisions are still unmade, what is wrong or weak, what could kill it, and
what fixes each.

Nothing here is new evidence. It is the disposition layer over three files that already exist,
[`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) (numbered defects),
[`KILL_CRITERIA.md`](KILL_CRITERIA.md) (thresholds) and [`VAULT.md`](VAULT.md) (deferred
work), plus the decisions that have no home in any of them because only the author can take
them. Every number is carried from a file that already holds it.

---

## 1. Decisions nobody has taken

These are not engineering problems. No analysis closes them, and each has been open long
enough that the not-deciding is itself a decision.

| # | The decision | Why it is still open | What it blocks | Cost of deciding wrong |
|---|---|---|---|---|
| D1 | Order B-1, a gaussmeter and eight magnetised blocks, ₹22,000-52,000, bill of materials written since 2026-07-30 | Never ordered. [ADR-021](adr/021-freeze-the-register.md) made it the top of the roadmap and it stayed there | E4. Every number in the repository descends from a field model checked only calculation-against-calculation | Low. The instrument is reusable and the magnets are the sled's own class |
| D2 | Which payload class is the product | Every CAD file, cassette and cost model is 3U. 3U fails kill criterion 1 at 10.547 kg/satellite on dry mass. Both business cases are now written side by side in [`D2_DECISION.md`](D2_DECISION.md), 2026-08-22, at a payload ladder re-run for the purpose ([P101](../OPEN_PROBLEMS.md)). Two things it settles: the only designed classes that close the criterion are the two PocketQube rungs, 0.440 and 1.319 kg, *1U does not, at 3.517*, and the closing rungs cost the per-satellite differential, because 24 satellites share one commanded velocity at 1P and one shares it at 3U. On added mass the criterion is crossed on both numerators ([P68](../OPEN_PROBLEMS.md)), full credit 1.2145 against a hostile 3.0827 kg | The market case, the CAD, the qualification plan, and what B-2 should measure | High. It is the difference between refining a design and starting a different one |
| D3 | Apply or hold the K_t correction (P46) | A2 computed K_t as 4.42 % high, 10.5386 to 10.5386 N/kA·m, moving v_exit 16.029 to 16.029 m/s. Computed and held, not applied | Whether the published design point is the best known one. Every downstream number descends from it | Medium. Applying it moves ~20 published figures; not applying it means the repository publishes a number it knows is beaten |
| D4 | ~~Submit to IEEE, or publish openly~~ DECIDED 2026-08-22: CC BY 4.0, everywhere. The hold was placed on 2026-08-10 against an IEEE copyright transfer *on acceptance*, and no venue has been selected, so there was nothing to hold against. [P106](../OPEN_PROBLEMS.md) is what forced it: `VOLLEY-paper` shipped the MIT text as `LICENSE` while its own `NOTICE` and `LICENSING.md` said CC BY 4.0 and pointed at that file. A repository may not make two incompatible statements about its own licence. `LICENSE-MIT-superseded` is still shipped under its own name, because the repository was MIT for a period and deleting that would erase history rather than supersede it. *If a venue is selected and requires a transfer, that is a decision taken then, on the accepted version* | Done | Low, and it was a *divergence being carried* rather than a position |
| D5 | File a US provisional, or let it go | The design is publicly disclosed, so an Indian filing is foreclosed. 35 USC 102(b)(1) leaves a US provisional possible until roughly August 2027 | Nothing technical. Everything commercial | High and one-way. The date passes whether or not it is decided |
| D6 | Accept the envelope as not-evaluable, or chase E5 | [ADR-023](adr/023-target-host-class.md) re-scoped the host to a POEM-class stage, which converted a clean 44 % fail against ESPA-Grande into an unmeasurable unknown, no accommodation envelope for that class is public | Kill criterion 2, and whether the machine can be shown to fit anything | Medium. One data exchange with one launch provider settles it |
| D7 | Buy the bank that can source the shot, or accept P26 | The 65 mΩ ESR ceiling is crossed as designed (116-185 mΩ). PII-7 prices four parallel strings: closes it with ~2x margin at 4x the cells, mass and cost | Kill criterion 3, and the fix lands on kill criterion 1, which is already failing | Medium. The fix is known; what is unknown is whether the mass is affordable |
| D8 | Keep Gen4, or declare Gen5 the only generation | Gen4 exists only inside Fusion, has never been exported, and its stations do not match the parameters every published number rests on (P32, P39). Gen5 is generated and does match | Which geometry the renders and the build package describe | Low, and overdue |
| D9 | ~~Fix the wiki, or retire it~~ DECIDED 2026-08-22: retired. [`wiki/Home.md`](../wiki/Home.md) is now a deprecation stub pointing at the repository, and `wiki/README.md` forbids restoring content there. The stub still has to be published, GitHub does not expose wiki repositories through its API, so it needs a machine with ordinary push credentials | Nothing internal. It was the most public surface with the worst numbers | Done, except the publish step |
| D10 | Fund it, or scope it to what one person can build (E15) | No sponsorship. The full-scale 1.5 m track is a laboratory-budget item; the qualification campaign is not | Everything past TRL 4 | High. It decides whether Phase II is a build or a paper |

The pattern worth naming: D1, D8 and D9 are cheap, unblocked and have been open longest.
D2 is the one that changes the most and has been avoided the hardest, the repository has
computed the payload ladder twice and never chosen a rung.

---

## 2. Everything wrong, weak, or unfinished

Grouped by what kind of thing it is, because the register's numbering mixes categories and a
reader cannot otherwise tell a wrong number from a missing subsystem.

### 2.1 The design is predicted to fail, or is not designed at all

| Item | What is wrong | Severity |
|---|---|---|
| E30 | Nine of thirteen elements are single-point failures that forfeit the remaining manifest. A spring dispenser forfeits one satellite. Below r = 0.99326 per element per cycle the machine delivers less total value than a spring | Fatal if unmet |
| E34 | The brake puts 18.5 kN through the structure eleven times while eleven satellites are still stowed. A stowed CubeSat is qualified to 25 g and launch random vibration, not to a 200 g arrest | Fatal if unmet |
| E33 | Magnet tolerance leaves a residual dipole that saturates a 15 N·m·s wheel in 3.0-7.5 days with the machine idle | Fatal if unmet |
| P41 | The payload slams into its cradle at the start of every shot at 36-231 °/s, 18 to 115x the 2 °/s tip-off comparator. Whether it has settled by release needs a restitution model this project does not have | High |
| P36 | The track has no dynamic design case. A17 said it needs one; A28 has now made the loop bandwidth depend on a mode frequency nobody has measured | High |
| P28 | The regen stator and the eddy fin do not both fit the arrest section | Medium |
| E24 / E25 | Attitude: the declared peak-rate bands fail, and attitude restoration depends on a controller and schedule that do not exist | Medium |
| E9 | 6U and 12U are force-limited, not designed, they exist as a scaling law, not as hardware | Bounded scope |

### 2.2 Published numbers that are wrong, stale or unsupported

| Item | What is wrong |
|---|---|
| P46 | K_t is 4.42 % high. The published 10.5386 is a centre-plane value; the depth-resolved figure is 10.5386. Correction computed and held (D3) |
| P47 | *(corrected 2026-08-13)* The published velocity-loop gain was linearly unstable, 557 Hz crossover, −50.4° phase margin. Now designed at 195 s⁻¹ |
| P32 | The working Gen4 geometry has no corresponding operating point, it releases at s = 1200 mm where `analysis/` assumes 1500 mm |
| P33 | The paper credits a winding inductance nobody had computed |
| P10 | Enclosure, radiator and packaged avionics are absent from the mass rollup. The 126.6 kg is therefore a floor, and kill criterion 1 is computed from it |
| P35 | The GMAT script generator is pinned to a superseded operating point |
| P38 / P39 / P20 / P14 / E16 | Records that disagree with their own sources: a paper claim its validation had falsified, companions that were not a function of the commit they claimed, a mis-specified reference plane, untracked CAD defects, reference hygiene |

### 2.3 Assumptions doing load-bearing work, unmeasured

| Item | The assumption | What rests on it |
|---|---|---|
| E4 | Nothing has been built, fired or measured at any scale | Every number in the repository |
| E3 | Component masses are parametric, unchecked against vendor data, spread perhaps ±15 % | The 126.6 kg, and therefore kill criterion 1 |
| E7 | Sensor noise, latency and resolution are assumed, no sensor is selected | The 0.0274 m/s dispersion, and now the loop's phase margin |
| E5 | Host stage mass, control authority and accommodation envelope are undisclosed | Kill criteria 2 and 6, the recoil table, and A15 Case B |
| E6 | Absolute orbital lifetimes are uncertain; the multiplier is not invariant across solar activity (P16) | The x1.60 headline |
| E18 | The conjunction covariance is invented | A6, and any collision-probability statement |
| E11 | No contamination or outgassing analysis exists | Payload compatibility, and any flight approval |
|, | Structural Q is unmeasured; every Miles-equation result is quoted at an assumed Q | P37, E10, and the gate sizing that resolved them |

### 2.4 Weaknesses in the idea itself, not in the execution

These would remain true even if every item above were closed.

1. The velocity is small. 16.0 m/s buys x1.60 of orbital life and 0.12° of plane change. Plane change is *never* a product feature at 133 m/s per degree, 8.1x the entire shot.
2. The mass is fixed and the payload is not. The deployer costs what it costs whether it carries 12 satellites or 288. Every economic argument is really an argument about how many customers divide 126.6 kg.
3. It replaces twelve independent one-shot mechanisms with one twelve-cycle mechanism. That is the architecture's defining trade and it is a *reliability* trade, made in the wrong direction, bought back only by cycle life nobody has measured.
4. A spring can reach this velocity. A ~1.8 kg staged spring delivers comparable Δv. It fails only in that its velocity is built in rather than commanded. Commandability is the whole product, not speed.
5. The satellite is not, in fact, unmodified. It is modified magnetically, invisibly, and without the customer knowing (E35).
6. There is no customer. No operator has been asked whether a commanded per-satellite orbit change is worth 10.55 kg of deployer per satellite, 1.758x a dispenser. *This line used to say "schedulable fleet distribution" at 6.4 kg: the schedulability framing was withdrawn by P56 and the mass by P69, and the question it asks is unchanged and still unasked.* No analysis substitutes for asking.

---

## 3. What could kill it, and what contradicts a published claim

### 3.1 The five most likely to be design-fatal

Carried unchanged from [`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md)'s lethality ranking, confirmed
2026-08-10. E30, E4, E33, E34, E35, in that order. Each entry there states the failure it
would cause and what would settle it either way.

Three of the five need metal, not computation. E30 needs a cycle-life test, E4 needs a
gaussmeter, E34 needs a shock response spectrum. Only E35 and part of E33 close by calculation.

### 3.2 Thresholds already crossed

[`KILL_CRITERIA.md`](KILL_CRITERIA.md) holds these in full. Three of seven are crossed at the 3U
design point:

| | Threshold | Where it sits | State |
|---|---|---|---|
| 1. Mass per satellite | ~2 kg | 10.547 kg dry at 3U; 1.608 kg added under ADR-032 | Crossed on dry mass. Closes on added mass (A37 band 5), with both reported together and the threshold unmoved. P59 stays LIVE |
| 2. Envelope | fits a rideshare port | 1839 mm vs ~1270 mm | Dissolved under ADR-032, nothing is stowed. Stands as crossed for Gen5 |
| 3. Bank ESR | 65 mΩ | 116-185 mΩ | Crossed as designed for Gen5. Ceases to exist under ADR-032, 25-131 W needs no bank (A39) |
| 4. Tip-off | 2 °/s | release fine; cradle arrival 355 °/s at 25 g, residual zero | Not demonstrated, and A38 shows raising acceleration does not worsen it. Ceiling 30.9 g |
| 5. Attitude at trigger | servo-nullable | bands fail on transient peak rate | Not demonstrated |
| 6. Host recoil | host accepts it | 64.1 N·s/shot; ~125 at the Gen6 point | Healthy, and it scales linearly with velocity |
| 7. Is the velocity worth anything | beats drag or propulsion | +28.8 km of semi-major axis, x1.60 of orbital life | Survives on orbit change. The phasing claim it used to rest on was false (P56) |

Three of the seven were Gen5 problems that ADR-032 deletes rather than solves, which is a
different and weaker kind of good news than solving them. Criterion 1 is the one that matters and
it is not declared met, a second numerator argued on its merits is not the criterion being
passed, and the whole result rests on 43.33 kg credited to a stage nobody has agreed to lend.

### 3.3 Statements the project makes that its own evidence contradicts

This is the section a referee will go to first.

| The claim | Where it is made | What contradicts it | Status |
|---|---|---|---|
| "An unmodified CubeSat" | Abstract, README, requirements | E35: the payload sits 20 mm from the array at 442x a magnetometer's full scale, continuously, and soft-magnetic parts leave permanently magnetised | Live. §VII of the paper now concedes the claim "holds mechanically and electrically... but is not established magnetically." The abstract and README still say it flatly |
| "Compatible with any restartable stage or hosted platform" | Abstract, conclusion | Kill criterion 2: no accommodation envelope for that host class is public, so the 1839 mm length cannot be shown to fit anything | Live and disclosed, §V-E says so; the abstract does not |
| "7.3x the extension a spring delivers" | Abstract | That ratio compares *gains*. On delivered orbital life it is 1.50 once per-shot reliability is weighted | Resolved, both figures now carried together everywhere |
| "0.0274 m/s dispersion" attributed to closed-loop control | Abstract, §V-A, conclusion | P47: the loop was unstable and the figure came from saturation limits plus a terminal trim | Resolved 2026-08-13, gain redesigned, figure unchanged at two significant figures, §IV-D states the history |
| K_t = 10.54 N per kA/m | Everywhere | P46: the depth-resolved value is 10.5386, 4.42 % lower | Live and disclosed, held under D3 |
| "A reusable sled" implying a reusable machine | Architecture | E30: nine of thirteen elements forfeit the whole remaining manifest on a single failure | Live. Stated in §VIII, absent from the abstract |
| "Cheaper than an OTV" | *nowhere* | No vendor quotation exists on any line of `cost.py`, and no OTV price appears in the repository | Correctly absent. Verified by grep before each release |

The honest summary of this table: every contradiction is disclosed *somewhere* in the
repository. Several are disclosed only in a limitations section while the abstract states the
unqualified version. That gap is the most reviewable weakness the project currently has, and
it is a writing problem, not an engineering one.

---

## 4. What fixes each of these, in the order worth doing

### Tier 0, cheap, unblocked, and long overdue

| | Action | Closes | Effort |
|---|---|---|---|
| 0.1 | Order B-1. | Changes E4 from true to false, the category of evidence, not its degree | ₹22,000, one afternoon |
| 0.2 | Qualify the abstract's three unqualified claims to match what §V-E and §VII already concede: "unmodified" to mechanically and electrically; "compatible with any stage" to against an interface, envelope pending; add the shared-failure exposure already in §VIII | Three of the seven contradictions above | One editing pass, no new analysis |
| 0.3 | Retire or regenerate the wiki. | D9, and the worst public numbers | Hours |
| 0.4 | Declare Gen5 the only generation, close Gen4's export gate permanently | P32, P39, D8 | One ADR |

### Tier 1, computation, no hardware, closes live threats

| | Action | Closes |
|---|---|---|
| 1.1 | Carry a longitudinal payload standoff into `cad/parameters.json` and recompute the field at the real station. 251 mm makes a magnetometer usable; 400 mm puts the payload below Earth's own field | E35, P34, and makes the "unmodified" claim *true* rather than qualified |
| 1.2 | Shock response spectrum at the cassette interface for the 200 g arrest, against a stated payload shock qualification level | E34, or forces the arrest cap down, which is itself the answer |
| 1.3 | Cut the payload CoM offset from 70 mm toward 3.5 mm (A23 band 5 already priced it), and specify the cradle preload > 85 N and release residual <= 1 N | P41, and kill criterion 4 |
| 1.4 | Apply P46 and re-baseline, or write the ADR that says why not | D3, P46 |
| 1.5 | Compliant-track model with the 48 Hz and 109 Hz modes inside the loop, not merely beside it | P36, and validates ADR-027's binding constraint |
| 1.6 | Close the mass rollup, enclosure, radiator, packaged avionics | P10, and puts a real number on kill criterion 1 |

### Tier 2, needs metal

| | Action | Closes |
|---|---|---|
| 2.1 | Cycle-life test of escapement, retention gate and sled to twelve cycles with margin | E30, the top of the lethality ranking, and the only thing that can |
| 2.2 | Measure each magnet's moment and axis on receipt, compute the assembled residual instead of assuming a distribution. Same instrument as B-1 | E33 |
| 2.3 | Modal survey of the track, giving a measured Q and first mode | Structural Q, P37, E10, and ADR-027's gain |
| 2.4 | B-2, single-coil thrust against K_t | The design point itself |

### Tier 3, decisions, not work

D2 first. Until the payload class is chosen, Tier 1 and Tier 2 are being spent on a
configuration that fails its own mass threshold by 3x. Then D5 (the provisional, which has a
date on it), D6 (one data exchange), D7 and D10.

---

## What this file is not

It is not a plan. [`ROADMAP.md`](ROADMAP.md) and
[`PHASE_I_CLOSURE.md`](PHASE_I_CLOSURE.md) hold sequencing, and
[`BUILD_READINESS.md`](BUILD_READINESS.md) holds subsystem-by-subsystem readiness.

It is not authoritative over any entry it references. Where this file summarises a defect, the
numbered entry is the authority on its own content.

It adds no new evidence. Every figure above is carried from a file that already holds it, and
where a number would be needed and does not exist, the row says so rather than estimating.
