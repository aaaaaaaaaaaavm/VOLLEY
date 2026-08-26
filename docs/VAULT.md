# The vault: ideas, and why each one stopped

Everything here would make the design better. Nothing here makes it correct.

This is where concepts live that never became a complete thing, possibilities for the future,
rejected architectures, and the evidence behind both. A vault, not a graveyard
([ADR-031](adr/031-four-repositories-not-two-phases.md)).

It lives in [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab), a repository with no
baseline and no stability promise. It is separate because a soft boundary inside the flagship is
one `git checkout` from becoming an edit to the record.

---

## The one rule

Every entry states why it stopped.

Not "deferred". *Why.* PII-16 carries the measurement that killed it, a transverse edge
factor of 0.0253 against the 0.55 it had been sized on, a factor of 22. PII-17 carries
the mass arithmetic that declined it. PII-1, the project's self-declared strongest idea,
carries the arithmetic showing a lighter mover collapses its own lever.

That is what makes this evidence rather than a pile, and it is the only rule the vault has.

---

## How something leaves the vault

| From to to | Condition |
|---|---|
| vault to main | Its acceptance bands were declared before its script existed, and run |
| main to paper / thesis | Stable, effective and reliable against the problem statement |
| paper / thesis to frozen | Presented or published |

Nothing crosses upward on enthusiasm. An item is not promoted by being interesting. It is
promoted by meeting the criterion it was given, written when it was deferred, not when it is
reviewed, because a criterion written afterwards is written by someone who already knows what
they want the answer to be.

Each entry gets one of three outcomes, recorded here:

| | |
|---|---|
| Promoted | Criterion met. Becomes work in main, gets an ADR, propagates scripts to figures to paper |
| Held | Criterion not yet met. Stays, with the reason recorded |
| Rejected | Criterion shown unreachable, or superseded. Stays, struck through, rejected items are evidence too |

---

## The design target main is working toward

Reset 2026-08-14 by [ADR-032](adr/032-gen6-stage-integrated-gas-store.md).

Gen6 is the payload accelerated directly, by gas, along a rail the host stage provides. No
mover, no pulse-power chain, no brake, no return stroke. Added hardware is 11.45 kg of
containment plus about 3 kg of store, and added mass per satellite is 1.608 kg on a
kick-stage class.

> The previous definition is superseded and is worth stating, because it was the target for one
> day. ADR-029 set Gen6 as *a linear induction drive on a passive aluminium mover*, no magnets,
> a 0.6 kg shuttle, an arrest of 82 J instead of 1938. Its nine measured bands (A30 4-5, A31 1-4,
> A32 1-2) stand as declared. What retired it was not a refutation but
> [A35](../validation/A35_constraint_ledger.md): the mover it optimised is 11 % of dry mass,
> so an architecture built around making it lighter was optimising the wrong term.

Five runs on 2026-08-14 built the replacement, and not one set out to: A35 attributed every
kilogram, A36 closed the manifest route, A37 made the stage the machine, A38 showed tip-off does
not bind, A39 replaced the spring with gas.

It is still a target, not a promotion. Nothing is measured; the fluid system is unsized, the
cradle mechanism does not exist, and no provider has agreed to lend a stage.

---

## Nine entries stopped on 2026-08-14, and for a reason none of them anticipated

> *A35's percentages quoted below are of the 84.53 kg rollup they were computed at. A46 moved it
> to 126.56 kg on 2026-08-16; the attributed kilograms are unchanged and the ordering is unchanged.
> P73.*

The vault's one rule is that every entry states why it stopped. These nine stopped the same
way, and the reason is worth stating once rather than nine times: [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
deletes the subsystem each of them improves. Not one was refuted. Each was a correct optimisation
of a part that no longer exists.

| | Improves | Why it stopped |
|---|---|---|
| PII-1 | the release, by a momentum-conserving kick off the mover | Δv = √(2EM/(m(M+m))) and the lever is *M*. With no mover, M = 0 and the kick delivers nothing. The project's self-declared strongest idea is deleted by arithmetic it wrote itself |
| PII-2 | the sled chassis, by ribbing it | No sled |
| PII-3 | K<sub>t</sub>, by a two-layer stator | No stator |
| PII-4 | the envelope, by repackaging 1839 mm | No envelope, the stage is the structure |
| PII-7 | the supercapacitor bank, by four parallel strings | No bank. This is P26, the largest live defect this project carried, and Gen6's answer is an architecture A51 measures at 0.26 W average *(A39's 25-131 W was the spring option's figure, P80)* |
| PII-11 | the track, by making it deployable | The stage is already deployed, already long, and already straight |
| PII-12 | copper loss, by block commutation | No stator |
| PII-17 | the mover, by letting it depart with the satellite | No mover |
| PII-18 | the mover, by making it a 0.25 kg shuttle | No mover |

They are not struck through and not deleted. Each records a real analysis at a real operating
point, and PII-1's arithmetic is the reason the mover went, it is the entry that measured how
much of the machine existed to serve the sled. A vault whose entries disappear when the design
moves is a graveyard.

Three entries survive untouched and one gains: PII-5 and PII-6 are astrodynamics and are
independent of the drive; PII-9's lunar case never depended on this architecture; and PII-8, the
free-flyer, gets closer, its hardest problem was airgap straightness over a deployed structure,
and ADR-032 has no airgap.

---

## Deferred items

### PII-1: Momentum-transfer release

> SUPERSEDED IF PII-18 IS PROMOTED, 2026-08-13. The lever here *is* the mover's mass:
> Δv = √(2EM/(m(M+m))). On PII-18's 0.6 kg shuttle the same 41.8 J buys 1.65 m/s instead of
> 3.83, and matching the original costs 225 J. PII-18 reaches the same exit velocity by not
> putting the energy into a sled at all, and adds no mechanism to the release path, which is
> this entry's own stated reason for deferring. See [`GEN6_ARCHITECTURE.md`](GEN6_ARCHITECTURE.md).
> Recorded as an interaction, not as a status change: the gate below still applies.

The strongest idea in the project, and it defers.

Sled and payload need not separate at the same speed. A momentum-conserving spring push at the
end of the stroke recovers the entire velocity shortfall for 41.8 J against a 2881 J shot
(1.5 %), and brake duty *falls* because the sled leaves slower. Against stroke-lengthening,
which needs 673 mm more envelope on a machine already 44 % over ESPA, this needs 43 mm of
guided rail.

Re-run 2026-07-31 with regeneration in the model, and the two compound. Regeneration takes a
fixed ~296 J over the 240 mm of regen stator whatever speed the sled enters at, so the kick and
the recovery act on different terms rather than competing. Together they take
electrical-to-payload efficiency from 18.5 % to 31.8 % and brake duty from 1268 J with
neither to 711 J with both. That is past the 31.5 % the superseded 4.86 kg design claimed, on a
sled twice the mass.

Held at the 25 g qualification limit the kick is 15.6 ms over 42.7 mm at 981 N, an ordinary
spring, not a shock event. Full working in
[`DESIGN_OPTIONS_exit_velocity.md`](DESIGN_OPTIONS_exit_velocity.md).

> Entry criterion. A7 (separation and tip-off) must run and show that a guided release
> through 43 mm of relative travel holds tip-off inside the band. ~~against its correctly
> sourced value, the run sheet declares <=5 °/s citing NRCSD-E while the sibling NRCSD ICD
> says 2 °/s, and that must be resolved first.~~ Resolved 2026-07-31: no conflict, two
> different deployers. The band is now the flown NRCSD figure of 2 °/s rather than the
> provisional NRCSD-E 5 °/s, which makes this criterion materially harder (P30). Plus a mechanism concept that resets twelve
> times and has a safing path for a cocked 45 J spring through the existing three-inhibit
> chain.

Why it is not Phase I: it adds a mechanism to the release path, the one place ADR-008
deliberately removed complexity, and it would reopen the tip-off claim, which is already the
least validated part of the design.

### PII-2: Rib-stiffened chassis

A4 shows the drawn plate passes with a 17x stress margin, so mass can come out. Uniform
thinning is nearly worthless, deflection goes as 1/t³, the budget is spent near 5.5 mm for
0.30 kg, worth about 0.2 m/s. Real reduction needs section depth, and nobody has designed
one, which is why the 60 % pocketing row in `DESIGN_OPTIONS_exit_velocity.md` is unsupported.

> Entry criterion. A rib-stiffened design that meets A4's three declared bands, 0.025 mm
> airgap closure per plate, 587 MPa allowable, first mode > 200 Hz, at a mass whose exit
> velocity beats 16.029 m/s by more than the ±20 % uncertainty on K<sub>t</sub>. Anything
> inside that uncertainty is not yet a demonstrated gain.

### PII-3: Two-layer stator (G3-D4)

Gen1 built two layers (324 conductors), Gen2 and Gen3 one (162). The decision is flagged open
in `cad/parameters.json` and sits upstream of K<sub>t</sub>. Doubling the winding widens
the magnetic gap 12 to 22 mm and drops K<sub>t</sub> from 11.03 to 7.33 N per kA/m, but sheet
current doubles at unchanged current density: 20.61 m/s at a 7.50 kg sled, J still
21 A/mm². The stator does not ride the sled, so its copper costs dry mass, not velocity.

> Entry criterion. A1 must run first, this trades one K<sub>t</sub> against another, and
> both are currently checked only analytic-against-analytic. Then PII-7 must be settled, and
> that is now a gate rather than a caution. `analysis/velocity_levers.py` computes the bank ESR
> ceiling for every lever by bisecting the real integrator: two-layer draws 597 A and drops
> the ceiling from 66 to 39 mohm, which needs four parallel strings with no margin, and with
> 40 % pocketing it is 637 A and 36 mohm. The electromagnetic case for two-layer is the best in
> the table and its power-system case is the worst. PII-3 may not be reviewed before PII-7
> closes.

### PII-4: Envelope repackaging (P9)

The closed envelope is 1839 mm against ESPA Grande's ~1270 mm (44 % over) because the
brake sits beyond the 1500 mm release point and the enclosure must span it. Options: shorten
the track, repackage the brake, or accept a host that does not impose the envelope.

> Entry criterion. Owner decision on target host class, which is not an engineering
> question. If ESPA Grande is retained, a packaging concept that fits ~1270 mm without
> reducing stroke below what the velocity claim needs.

> The owner decision was made 2026-08-10: [ADR-023](adr/023-target-host-class.md) re-scopes to
> a spent upper stage, and ESPA-Grande compliance is not a requirement. So the entry criterion
> above is satisfied in the direction that does not require repackaging, and PII-4 narrows
>, it is no longer about fitting 1270 mm. It becomes live again only if a host accommodation
> envelope arrives (E5) that 1839 mm does not fit either, which is ADR-023's stated falsifier.
> The priced alternative is on record: fitting 1270 mm costs 25 % of exit velocity.

Note: ~~P9 stays open as a Phase I *defect*~~, P9 closed 2026-08-10 by ADR-023. The paper
states the overrun honestly and now also states the re-scope and its cost. Kill criterion 2 is
not thereby passed; it is `NOT EVALUABLE` pending E5.

### PII-12: Block-commutated stator (P29)

`analysis/owner_decisions.py` priced it against the branch [ADR-022](adr/022-stator-segmented-not-block-commutated.md)
adopted. Energising roughly one sled length instead of the whole 1.30 m winding takes copper loss
from 834.7 J to 218 J, net efficiency from 18.47 % to 28.07 %, phase inductance from
19.70 µH to 5.15 µH, and peak current from 320 A to 288 A. Exit velocity does not
change at all, force is commanded, so copper loss is a power draw and not a thrust reduction.

It was not adopted because it costs an inverter per segment or a segment-switching assembly,
none of which is in the mass rollup, and mass per satellite is crossed by a factor of three
while net efficiency appears in no kill criterion.

> Entry criterion. P10 closes with margin, the enclosure, radiator and packaged avionics
> land in the rollup and per-satellite mass has room in it, or some claim becomes
> efficiency-limited, which nothing currently is. Until one of those, 7 points of efficiency
> bought with drive hardware is the wrong trade for the threat that is live.

### PII-5: Variable-shape atmosphere in `astro.py`

P16's root cause: solar activity enters as a uniform density scale and ballistic coefficient
enters the same multiplicative slot, so neither sweep can move the ratio it claims to test.
The model's arithmetic is not wrong; its parameterisation cannot express the effect being
claimed.

> Entry criterion. A5 re-run at the current operating point, plus GMAT at BC 40 and 90 to
> establish what the true BC dependence actually is. Replacing the atmosphere before knowing
> that would be fixing a model against an unmeasured target.

Phase I keeps the honest version: quote the multiplier at a stated activity level and claim
no invariance. That is already done.

### PII-6: Reachable-domain analysis

The strongest single thing the prior-art review turned up. Feng et al. compute a 3-D envelope of
the orbits one shot makes available, reconstructed with an alpha-shape algorithm. This project
reports a scalar lifetime multiplier, which answers a smaller question: how much longer does the
satellite stay up, rather than where can it be put.

Their method is better, and [`PRIOR_ART.md`](PRIOR_ART.md) says so rather than working around it.
A deployer whose selling point is a programmable per-satellite velocity should be able to state
what that velocity buys as a region, not a number.

> Entry criterion. A5 re-run at the current operating point first. A reachable domain built on
> a superseded delta-v would be an elaborate way to publish a stale result, and P19 already records
> one of those.

Not Phase I. The scalar multiplier is correct, sourced and cross-checked against GMAT. It is
narrower than the alternative, which makes the envelope an improvement rather than a correction,
and `docs/BASELINE.md`'s rule puts improvements here.

### PII-7: A bank that can actually source the shot (P26)

Phase I if the programme wants a defensible rated point; Phase II only because the current
one is honestly labelled as not closing. A10 established a hard ceiling of 65 mohm on bank
ESR, and a single string of 32 x 190 F cells gives 116 to 185 mohm.

Parallel strings divide resistance and multiply capacitance. The bank is priced in
`analysis/cost.py` at INR 240,000 for 32 cells, so each added string costs the same again:

| Strings | Cells | Bank C | Bank ESR | Against the 65 mohm ceiling | Bank cost |
|---|---|---|---|---|---|
| 1, as designed | 32 | 5.9 F | 116-185 mohm | fails, 1.8-2.8x over | INR 240 k |
| 2 | 64 | 11.9 F | 58-93 mohm | marginal, fails at the pessimistic end | INR 480 k |
| 3 | 96 | 17.8 F | 39-62 mohm | closes, no margin | INR 720 k |
| 4 | 128 | 23.8 F | 29-46 mohm | closes with roughly 2x margin | INR 960 k |
| 6 | 192 | 35.6 F | 19-31 mohm | comfortable | INR 1.44 M |

Four strings is the first row that closes at the pessimistic ESR with margin left for
temperature and ageing, both of which move ESR the wrong way. It costs four times the cells
and four times the bank mass, against a mass rollup that already excludes the enclosure,
radiator and avionics (P10), and a cost model in which the bank is already the second largest
line at 17.8 %.

The alternatives, neither costed here:

- Accept a lower rated point. Lower commanded force lowers peak power, which raises the
  ESR ceiling. This trades exit velocity for a buildable bank and needs the trade curve
  computed before it can be argued.
- Change technology. Lithium-ion capacitors trade ESR for energy density; a battery plus a
  small capacitor front end moves the pulse burden elsewhere. The reading gap that blocked this
  is now closed: `LITERATURE.md`'s pulsed-power cluster went from 2 entries to 29 on
  2026-07-31, covering ESR definition and measurement, ageing and derating, pulse-forming
  networks, and lithium-ion capacitors including one flown system (NESSIE, 2013). None of it has
  been *read* yet, and the entry criterion below is unchanged by that.

> Entry criterion. ~~The pulsed-power literature gap filled first~~ (done 2026-07-31,
> 29 entries), then that cluster actually read, and then a cell selected from a manufacturer
> datasheet rather than a distributor listing, with DC ESR at the operating temperature and
> its derating with age. Two things the new reading list already flags make this sharper: the
> published end-of-life criterion for these parts is a two-fold ESR increase, and operation
> to −40 °C can double ESR without shortening life. A10's ceiling has no room for either.
> A bank chosen on an interpolated ESR would repeat the error that produced P26.

Why this is not simply Phase I. It is a sizing decision with a 4x cost and mass
consequence, and the honest Phase I position is the one now published: the rated point assumes
a bank that cannot be bought, and that is stated rather than quietly re-sized.

### PII-12, PII-13: the per-satellite shoe, and swarm dispersion

Both are deferred by ADR-025, which chose a fixed cell with class-specific inserts over a
per-satellite shoe.

| | |
|---|---|
| PII-12 | The per-satellite shoe. Every class gets its own cradle, retention and release, so velocity stays programmable per satellite all the way down the ladder instead of per cell. The cost is a new pitch, a new gate, a new cradle and a new qualification campaign per class, which is exactly what ADR-025 declined to spend in Phase I. Entry criterion: a customer who needs true per-satellite velocity control below 3U. Nothing else opens it |
| PII-13 | Designed dispersion across a swarm (P44). A24 band 6 failed at femtosat scale: 720 ChipSats in one cell need 719 shim interfaces, 7.19 kg of separation hardware for 3.6 kg of satellites. The mechanism is twice the mass of what it acts on. The finding is that the *requirement* is wrong at that scale, 8640 femtosats do not want 10 m of pairwise separation in 120 s, they want a velocity distribution produced once at cell level. Different mechanism, different acceptance argument. Entry criterion: P44, and a femtosat customer. Until then the fixed cell is qualified for PocketQube 1P and above and not for ChipSat |

> PII-13 is the one worth watching, because it is the only item in the programme that a
> *market* argument points at rather than an engineering one: `docs/MARKET.md` argues that a
> designed dispersion across a swarm is a product no spring and no OTV can offer, since every
> alternative gives every unit the same push. That argument currently has no mechanism behind
> it, and P44 is the measurement that says so.

---

### PII-16: the satellite's own CDS rails as the motor secondary, REJECTED 2026-08-13

Full proposal: [`GEN6_RAIL_DRIVE.md`](GEN6_RAIL_DRIVE.md). Sizing in
`analysis/rail_drive.py`. No band declared, nothing validated.

The CubeSat Design Specification has mandated four hard-anodised aluminium corner rails on every
CubeSat since 2003. Every deployer built since treats them as a bearing surface. They are also,
by accident, 116 cm² of standardised, structural, conductive, axially symmetric linear
induction motor secondary that every customer already owns and already qualifies.

Drive on them and the satellite becomes the mover: no sled, therefore no brake, therefore no
arrest section, no sled return and no cradle. First-principles sizing at a modest 0.45 T, a
realistic 2 mm clearance and the worse of the two rail alloys gives 513 N, 13.1 g, 18.26 m/s
on 1182 J, faster than Gen5 on 2.4x less energy, because the moving mass is 4 kg instead of
13.45 kg.

Entry criterion A30 band 1 was run and FAILED: the edge factor is 0.0253, not the 0.55
assumed, a factor of 22, and four rails make 41.9 N against 413 N required. The architecture
is rejected (P49). What survived is band 4: a 90 mm plate is at 0.6691 and weighs 0.248 kg.

Original entry criterion, as declared: The transverse edge-effect derating, assumed at 0.55,
is what the entire result scales on, and a 3-D transient eddy-current solve is what settles it.
If it comes in near 0.2 the idea is dead, and that is the cheapest possible way to find out.

The tension that is not resolved by making the machine better: the drive works only on
classes that carry CDS rails, and kill criterion 1 fails at 3U and closes only at PocketQube,
which has a different rail standard. That is decision D2, not an analysis.

### PII-18: the plate as a reusable shuttle, the catapult, with a quarter-kilo carriage

Proposed 2026-08-13. Not sized beyond the arithmetic below, and it inherits nine measured bands
rather than needing them re-run.

PII-16 put the conductor on the satellite's own rails and died on the edge factor. PII-17
put it on the satellite as a fin and was declined on mass, because the fin carried magnets.
A30/A31 measured that the right conductor is a 90 mm plate weighing 0.248 kg. This entry asks
the obvious next question: *does the plate have to be on the satellite at all?*

It does not. A plate that stays with the machine is a shuttle, which is exactly the
architecture the operational shipboard launcher uses (`PRIOR_ART.md` §2b) and exactly what Gen5's
sled already is. The only thing that made Gen5's sled 9.445 kg was carrying permanent magnets
and surviving the brake that carrying them made necessary.

| Mover | Mass | Energy to arrest at 20.26 m/s | |
|---|---:|---:|---|
| Gen5 sled, Halbach + Ti chassis | 9.445 kg | 1938 J | 200 g arrest, 18.5 kN through eleven stowed satellites (E34) |
| Plate bolted to the satellite (Gen6a) | 0.248 kg |, | departs; nothing to arrest, but the customer pays and classes without room are excluded |
| Plate as a reusable shuttle | 0.398 kg | 82 J | 23.7x less |
| Shuttle + pusher + latch, generous | 0.600 kg | 123 J | 15.7x; at a 200 g arrest that is 1177 N over 105 mm |

What this buys over Gen6a, and it is a lot. The satellite is unmodified again, no plate,
no consumable, no interface to publish and no adopters to recruit, so decision D2 dissolves:
every payload class works, including the PocketQube classes that are the only ones where kill
criterion 1 closes, because a small satellite rides a carrier that *is* the shuttle. And there
are still no permanent magnets anywhere, so E33 and E35 stay dissolved.

What it costs. The brake comes back, at 1/16th to 1/24th the energy. The return stroke comes
back, at 1/24th the mass, so E24's dominant attitude term shrinks by the same factor rather
than vanishing.

The geometry question that decides it. A single fin below the satellite reinstates P41's
centre-of-mass offset, which is the whole tip-off problem. Twin fins straddling the satellite,
running in two stator channels, put the thrust line through the satellite's own axis and remove
it. That doubles the plate mass to about 0.5 kg and doubles the thrust with it. Nobody has
drawn it.

Entry criterion: A31's bands 1-4 and A32's bands 1-2 transfer unchanged, because the plate is
the same object in the same gap. What does not transfer is the retention, the release and the
twin-fin geometry, and P52, the 30 % segment-handover ripple, is topology-level and applies
to every variant here.

### PII-17: the mover departs with the satellite

Considered and not recommended in the naive form, recorded because the reasoning is worth
keeping. If the mover is integrated into the satellite as a fin or keel carrying the Halbach
array, the sled and brake disappear, but the array's mass moves onto the *customer's* budget:
6.04 kg at the full 340 mm array, 3.20 kg at 170 mm, against a COTS cold-gas module at
0.5-1.2 kg for the same Δv. VOLLEY would then be competing with cold gas on cold gas's own
ground and losing 3-6x, and kill criterion 1's only escape clause, *"VOLLEY requires none of
that, because the satellite is never modified"*, is lost with it. Recoil also rises 74 % at a
170 mm array, since the whole moving mass departs instead of the sled's share returning through
the brake.

What the idea is right about is that dropping "unmodified" re-opens the topology trade, and
the topology that wins when the payload can carry something is the one where the payload carries
the *cheap passive half*. Taken to its conclusion, that is PII-16, where the payload carries
nothing at all because the passive half is already bolted to it.

> ### The vault re-read 2026-08-20, and one blocker turned out to be doing three jobs
>
> [`EXTERNAL_EVIDENCE.md`](EXTERNAL_EVIDENCE.md) has the full map. The finding worth carrying
> here: PII-8, PII-9 and PII-14 each stopped partly on *"the capacitor bank cannot source
> this"*. [ADR-032](adr/032-gen6-stage-integrated-gas-store.md) deleted the bank and
> [A64](../validation/A64_pulse_store_technology.md) re-priced what replaced it, so one
> retirement quietly retired a blocker in three entries, and none had been re-read since.
>
> | | |
> |---|---|
> | PII-8 | The only live route back in the vault. Airgap and bank blockers both gone. What remains is a standards question the entry cites against itself, the CubeSat quasi-static case near 14 g against tables computed at 25 g, and the thermodynamic velocity ceiling of a gas expansion, which nothing in this programme computes. [`VELOCITY_CEILING.md`](VELOCITY_CEILING.md) treats the ceiling as payload-limited because for a motor that is the only ceiling there is |
> | PII-9 | Structurally shut, and it reached ADR-033's principle first. *"Centrifuge for bulk velocity, linear motor for precision"*, written 2026-07-31, sixteen days before ADR-033 adopted *"gas supplies the energy, the motor supplies the control"* with a different bulk store. Two unrelated stores, same conclusion |
> | PII-21 | Reopens on a catalogue lookup. A59 left the tube on two numbers, density and service temperature, so screening alloy classes against T_sat(p₀) is a cheap run, not the open materials question the entry called it |
>
> A stop is not scripture. An entry can be wrong about why it stopped, and the commonest way
> is that the thing blocking it stopped existing.

### PII-8 to PII-11: recorded in the lab, not here

Four items live in [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) rather than this
file, because they are programme directions and scaling studies rather than deferred fixes to
this design. The flagship stays authoritative for PII numbering, so they are listed here to
stop the numbers forking, which they briefly did.

| | |
|---|---|
| PII-8 | VOLLEY as a free-flyer. A long deployed track plus release at perigee reaches TLI and Mars-class C3 without exceeding CubeSat qualification. Three unsolved problems in front of it: airgap straightness at 0.7 to 2 ppm over a deployed structure, a 294 kJ shot against a bank that already fails at 2.88, and whether 25 g survives review as a *sustained* load rather than a transient |
| PII-9 | The lunar case. Where this technology has always belonged, and the O'Neill mass driver it descends from. 1.33 MJ/kg to lunar orbit, so 15 kW launches a tonne a day. The payload is ore, so the g-limit that governs this entire design disappears |
| PII-10 | Magazine indexing disturbance (E24). Designing an indexing sequence that minimises attitude disturbance. The *bookkeeping* half is an error correction and belongs upstream in Phase I; only the optimisation belongs in the lab |
| PII-11 | [A deployable track, and the side-rail layout](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/PII-11_deployable_track.md). A telescoping track long enough to accelerate *and* regeneratively arrest the sled reaches 48 % electrical-to-payload efficiency against 18.5 %, deletes the eddy brake, closes P28, and stows at 1150 mm, inside the ESPA Grande envelope this design misses by 44 %. The only option in the programme that improves velocity and envelope together. The side-rail half loses on thrust in every variant priced and is there because it drives the tip-off moment to zero |

| PII-14 | [A cable-driven gondola on a deployed truss](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/PII-14_cable_driven_gondola.md). Propulsion moved off the vehicle onto a cable, energy from a flywheel, a permanently-locked deployed truss, and a tensioned wire as the running surface. A 2 kg gondola carries no magnets, no chassis resisting 2.69 kN, and no brake fin, so it reaches 24.5 m/s in the existing 1.30 m track, if the drivetrain has no rotating inertia. It does. `m_eff = I/r²` adds directly to the moving mass, a 34 kW machine at a 100 mm drum is 1-5 kg of it before the drum or any gearbox, and at 7.4 kg the entire gain is gone. Assessed and declined for Phase I on 2026-08-10, +15 to +30 % velocity, uncertain, against deleting the LSM and the 24 validations behind it. Entry criterion: a computed drivetrain inertia budget showing m_eff <= 2 kg, and a Phase I baseline that has been measured rather than modelled. The flywheel it split out is closed, 2026-08-20: that half was a Phase I candidate against P26, the question is now Gen6's pulse store, and [A64](../validation/A64_pulse_store_technology.md) answered it at ~70 g on published capacitor data. *A rotating machine with bearings, containment and 7.15 N·m·s of stored angular momentum does not beat that, and the momentum is a disturbance in a machine whose shot already dumps 3.28 N·m·s* |

| PII-15 | SUPERSEDED IF PII-18 IS PROMOTED, 2026-08-13, its only claimed benefit is shortening the machine, and spending the qualification margin Gen5 leaves idle does the same for free: 850 mm at 16.1 g against 1300 mm at 10.1 g, with no cable over a sheave. See [`GEN6_ARCHITECTURE.md`](GEN6_ARCHITECTURE.md). An LSM tug reeved to a separate payload carriage. Distinct from PII-14: the linear motor stays, only the coupling changes. A reeving ratio *n* moves the carriage *n* times the tug's distance, and divides the tug's 9.445 kg by *n²*, so 2:1 halves the acceleration zone, 1.30 m to 0.65 m, for 4 % of exit velocity. That is the only lever found that shortens the machine without lengthening anything else, against P9's 44 % envelope overrun. And it separates the payload from the magnets longitudinally at the same time, which is E35's fix. Costs, none analysed: a cable and pulleys in vacuum (E21, and A27 screened out a rack for exactly this), a second guided body, and a single tension load path that becomes another manifest-forfeiting element in `docs/FMEA.md`. Entry criterion: E35 shows separation is required, and a vacuum cable/sheave life case exists |

> Entry criterion for PII-8, PII-9 and PII-11: none, deliberately. None is a candidate for
> this baseline. The correct outcome for the thesis is that all stay closed until the Phase I
> deliverables ship, and the flagship currently has three crossed kill criteria, one failed
> validation and no measured number.
>
> PII-11 is the one that will be hardest to leave shut, because unlike the others it improves
> the machine that is actually being built rather than describing a different one. That is exactly
> why it needs the gate: `docs/BASELINE.md` puts architecture changes in Phase II by type, and
> a deployable structure is an architecture change however good its numbers are.

---

### PII-21: water as the working fluid, in three forms, STOPPED 2026-08-20

Pressurised water, solar steam, and electrolysis to H₂/O₂, each replacing the cold nitrogen
ADR-032 adopted. Three branches, stopped three unrelated ways, and the full entry is
[`VOLLEY-lab` PII-21](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/PII-21_water_working_fluids.md).

| | |
|---|---|
| Pressurised liquid water | 2 L compressed by 22.73 bar stores 2.35 J against the 2350 the shot needs, short by 1001x. Bulk modulus 2.2 GPa. *Not an engineering shortfall; the wrong physics for a gun* |
| Electrolysis to H₂/O₂ | Excellent energy case, ~8.5 g of water per campaign, stopped on architecture. A ~3000 K chamber beside eleven stowed unmodified satellites, two pressure vessels back, an igniter as a new manifest-forfeiting element, and ignition timing and mixture ratio replacing a charge pressure A44 measured commanding at 0.499 % per 1 % |
| Steam | Run twice. [A62](../validation/A62_steam_working_fluid.md) screened it at *nitrogen's* design point and was wrong to, P90, and [A63](../validation/A63_steam_design_point.md) swept 108 points |

What A63 found is worth keeping. The heating works: 57.3 W, α/ε 6.4 inside the
selective-coating class, no concentrator and no sun-tracking, a 27 cm absorber that survives
eclipse. The fluid is better: 101.98 % of the work on 35.1 % of the charge mass. The shot is
gentler: 34.33 m/s at 10.00 g against 11.36. And the seal specification survives, 43 of
108 points sit inside filled PTFE's limit.

> Then the bore temperature settles it. The floor on the charge temperature is T_sat(p₀), and
> every charge pressure that makes 2350 J puts it above aluminium's 473 K. Zero of 108 points
> reach it. The steel tube that forces costs 2.154 kg, larger than everything water removes,
> and none of the 43 feasible points is a saving.

A63 left one conditional: if the tube were steel for reasons independent of the fluid, steam
becomes +0.341 kg. [ADR-035](adr/035-drive-tube-material.md) decided that on 2026-08-20 and it
went to aluminium, because A59 found strength, stiffness and buckling all indifferent between the
metals and only mass discriminated.

Steam is foreclosed by a decision taken on its own merits rather than by a judgement about steam,
and ADR-035 falsifier 4 says so.

### PII-22: the pyrotechnic drive, which is A65's result read past its own scope, OPENED 2026-08-20

[A65](../validation/A65_pyrotechnic_ejector.md) was scoped to a backup ejector and produced a
number that does not stay inside that scope.

| | |
|---|---:|
| Gas drive, rated exit velocity | 29.01 m/s |
| Pyrotechnic charge, smallest in the published class, firing alone | 28.85 m/s |

A device sized to rescue a dead drive reproduces the drive. *If a per-cell gas generator can
deliver the shot, the reservoir, the fill valve, the fire valve, the chamber and the 3.1216 kg store
all stop being necessary, five of the seven shared elements [A47](../validation/A47_gen6_fmea.md)
counts, in an architecture whose shared elements are the whole of what E30 is about.*

A65 refused to chase it and said so in the run sheet. The sizing there is deliberately a
*backup* sizing carried on top of a store that stays, and its mass table keeps the store in.
Reading a result past the question it was asked is how A62 went wrong, and that is recorded as
P90.

What it would have to beat, and none of it is priced here:

- The gas store charges slowly from solar and is refillable in principle. A generant is not.
  Twelve charges is twelve charges, and the campaign is over.
- Commanded velocity. A44 measured charge pressure commanding exit velocity at 0.499 % per
  1 %. A solid charge has no equivalent knob, the same objection that stopped PII-21's
  electrolysis branch, and it attacks the claim the product is sold on.
- [P91](../OPEN_PROBLEMS.md)'s 185 g, which A65 left open on the backup version and which gets
  worse, not better, if the device has to do the whole job.
- Everything A65 named and did not pay for: range safety, ordnance handling, shelf life, hazard
  classification for twelve units in one magazine, and a charge that cannot be proof-tested before
  flight.

> Entry criterion: [P67](../OPEN_PROBLEMS.md) measured, and a commanded-velocity mechanism for a
> solid charge that A44's sensitivity model can be run against. *Without the second, this is a
> deployer that cannot command what it deploys at, and Gen6's central claim is exactly that it can.*

### PII-20: gas and electromagnetic as mutual fail-safes, DECLINED 2026-08-16, not run

Proposed in review: build both drives, size each for the full duty, and let either deploy the
manifest if the other fails.

It is declined on arithmetic, before any analysis, and the arithmetic is A35's.

Mass. For either drive to deploy alone, each must carry the full duty. A35 prices the
electromagnetic half at C2 + C3 = 11.54 + 26.35 = 37.89 kg, the reusable mover, and the
requirement that the energy arrive during the shot. That is precisely what ADR-032 deleted.
Re-adding it beside the 5.38 kg gas store puts added mass per satellite at roughly 4.6 kg
against an unmoved 2.0 kg threshold, so it re-crosses the one numerator Gen6 currently passes.

The redundancy does not buy what it looks like it buys. Of Gen5's nine manifest-forfeiting
elements the drive is three. The sequencer, launch lock, magazine follower, escapement,
retention gate and cradle stay single-path, and [A47](../validation/A47_gen6_fmea.md) has since
measured what that ceiling is worth: an entire architecture change moved expected delivery from
6.620 to 6.992 satellites. Spending 37.89 kg to duplicate three of eight shared elements buys
less than that.

And the two drives interfere. To be motor-driven the carriage must carry magnets, *that is
the 11.54 kg mover*. To be gas-driven it must seal against a tube. A carriage doing both is
heavier than either, and both modes degrade: gas exit velocity goes as 1/√m and motor
acceleration as 1/m. Each backup taxes the primary on every shot it does not fire.

Half-sizing is not a fail-safe. Size each at 50 % and a failure leaves 71 % of velocity,
since *v* ∝ √*E*. That is a degraded mode bought at nearly full mass, guaranteeing neither.

> What the question was actually reaching for, and both are now run.
>
> The control half became [A48](../validation/A48_trim_stage.md), gas for energy, a short
> motor section for the velocity it actually produced. 2.021 % of the shot, 1.822 % of the
> stroke, 0.340 kg, and it gives back the precision Gen6 traded. It fails on peak power against
> a band that should not have been declared, and its open question is what a 37.7 J at 28 kW
> store weighs.
>
> The fail-safe half became [A47](../validation/A47_gen6_fmea.md) band 8, and the answer is
> not a second drive. A per-cell backup ejector, a 1-2 m/s spring guaranteeing clearance,
> takes expected delivery from 6.992 to 9.261 satellites at *r* = 0.99. Six times the
> architecture change, because it converts the drive from manifest-forfeiting to
> satellite-forfeiting, which is the only move that touches what E30 says.

Entry criterion. A pulse store sized for 37.7 J at 28 kW, weighed; and a measured seal
friction (P67) showing the correction is needed at all. If the friction turns out small, the
trim stage has nothing to correct and this whole branch closes.

## Review log

| Boundary | Date | Outcomes |
|---|---|---|
| *(none yet)* | | First boundary opens after thesis submission |

## Adding an item

Name it, state what it buys with a number, say why it is improvement rather than
correction, and write its entry criterion before you stop thinking about it. An item without
a criterion is not deferred, it is abandoned with extra steps.
