# What would make VOLLEY pointless

[`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) carries the numbered entries and its own live count,
derived by `tools/register_status.py`. **That count is not restated here** — one number in five
places was five chances to drift ([ADR-021](adr/021-freeze-the-register.md)). Most of those
entries are engineering work.
A few are threats to whether the machine has any reason to exist, and they are hard to see when
they sit in a numbered list next to a stale cross-reference.

This file separates them. For each: **the value at which VOLLEY has no reason to exist**, where
it sits today, the margin, and what would close it. Ordered by how close each is to its
threshold, not by discipline.

**Two are close and one may already be crossed at the 3U design point.** That is the reason to
write this down rather than discover it in a review.

---

## 1. Mass per satellite, against the satellite doing it itself

**The sharpest threat, and the one this repository has not previously stated.**

A customer wanting 16.5 m/s has an alternative: put a cold-gas module on the satellite. The
rocket equation is unkind to VOLLEY here.

| | |
|---|---|
| Propellant for 16.5 m/s on a 4 kg 3U, cold gas at Isp 60 s | **0.111 kg** |
| A COTS 3U cold-gas module, wet, including tank, valves and drive | **0.5 to 1.2 kg** |
| VOLLEY's share, 126.6 kg over 12 satellites | **10.55 kg** |
| **Ratio** | **VOLLEY is about 12x heavier for the same delta-v** |

**The warning this paragraph used to carry has come true, and it was low.** It read: *a plausible
20 kg of missing mass takes the figure to 8.08 kg per satellite.* On 2026-08-16
[A46](../validation/A46_enclosure_buildup.md) built the enclosure up from the geometry in
`parameters.json` and found **50.04 kg where an 8.00 kg placeholder stood** — 42 kg, not 20. The
rollup is no longer carrying a parametric lump for the enclosure; it carries five derived lines,
each tracing to a dimension in the parameter file. **Thermal and avionics remain lumps**, and
nothing in the rollup is physically measured.

> **Kill threshold: above roughly 2 kg per satellite, a rational customer buys a propulsion
> module instead.** That threshold is an estimate, from canisterised dispensers at about 2 kg/U
> and cold-gas modules at 0.5 to 1.2 kg. It is not a sourced industry figure and should be
> refined before it carries any more weight than it already does.

**Status at 3U: crossed.** 10.547 kg against a 2 kg threshold.

> ### Two of the three routes out are now closed by measurement, 2026-08-14 (**P59**)
>
> | Route | |
> |---|---|
> | **Architecture** | **Closed by [A35](../validation/A35_constraint_ledger.md).** Every kilogram was attributed to the requirement causing it and **49.23 kg — 58.2 % — survives every deletion of every requirement in all 64 corners.** The deletable fraction caps at **41.8 %**. There is no architecture that reaches 2 kg |
> | **Manifest size** | **Closed by [A36](../validation/A36_magazine_density.md) band 4.** The N → ∞ limit is a healthy **0.954 kg/satellite**, but 2.0 kg is first reached at **N = 116** — and no factorisation of 116 packages inside the 1500 mm track length. The largest manifest that fits is **N = 126**, at **1.941 kg/satellite**, on a **244.6 kg** machine running a **42-hour** campaign |
> | **Smaller payloads** | **Open**, and now the only one |
>
> **The sentence below was written before either run and it is still the answer. It is now the
> *only* answer**, which is a much stronger statement than it was, and it makes **D2** — which
> payload class is the product — the decision the whole criterion rests on.
>
> **The threshold is not being moved.** ~2 kg comes from what canisterised dispensers achieve, and
> a threshold revised after a result is known is not a threshold. The honest options are to change
> the payload class, or to publish the criterion as crossed and say so on the front page.

### What closes it, and it is not an engineering fix

Smaller payloads. The deployer mass is fixed; the number of satellites it carries is not:

| Payload | Volume ratio said | **Designed cell (A24)** | Deployer mass per satellite |
|---|---:|---:|---|
| 3U CubeSat | 12 | **12** | 10.547 kg, **fails** |
| ThinSat | 123 | **NOT ACCOMMODATED** | — |
| 1U | 40 | **36** | **2.125 kg, now fails** |
| TubeSat | 41 | **24** | **3.188 kg, now fails** |
| PocketQube 3P | 108 | **96** | 0.797 kg, passes |
| **PocketQube 1P** | 326 | **288** | **0.266 kg, passes by 2 to 4x** |

> **Corrected again on 2026-08-10, and this time the correction moves the answer.** The counts
> above were volumetric until **A24** built the ladder as an actual design — a fixed cell of
> 340.5 × 100 × 100 mm with class-specific inserts (**ADR-025**). Three consequences:
>
> **1U and TubeSat no longer close this threat.** They were the marginal rungs, and a real
> insert takes both over the line: three 100 mm units plus two dividers fit a 340.5 mm cell with
> 37.5 mm wasted, so 1U gives **36 per load and 2.125 kg**, not 40 and 1.92. A 127 mm TubeSat
> fits twice with 84 mm wasted: **24 and 3.188 kg**, not 41 and 1.88.
>
> **ThinSat is refused outright.** At 114 × 114 × 25.4 mm, two of its dimensions exceed the
> 100 mm cell section in every orientation. **The cassette is 166 mm wide** — a constraint that
> appears nowhere else in this repository, and that a volumetric model structurally cannot find.
>
> **The threat still closes, two rungs lower than claimed**, on the PocketQube classes — which
> are precisely the classes with **no corner rails and no designed interface at all**. And at
> femtosat scale the separation hardware outweighs the satellites (**P44**), so ChipSat is
> **not qualified** for this architecture.

**These counts were wrong here until 2026-07-31 and the correction is downward.** They were
raw volumetric bounds carrying a note that realistic packing is 40 to 60 % of them, and then
quoted unadjusted anyway: PocketQube 1P appeared as ~546 per load and **0.14 kg**, passing by
6x. `analysis/payload_family.py` now calibrates the packing efficiency so the 3U case returns
the twelve the machine is actually laid out for, and applies the same 56.2 % to every class.
The threat still closes, by a smaller margin than was published. See
[`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md).

### The argument that survives even at 3U, stated after the number and not instead of it

A cold-gas module requires the satellite to **carry propulsion**: a pressure vessel, a
qualification campaign, range-safety review, integration schedule, and an attitude control
system able to point the thruster. VOLLEY requires none of that, because the satellite is never
modified.

For a customer who has already chosen propulsion, VOLLEY loses on mass and should. For the
propulsion-less satellite it targets, which is most 3U rideshare payloads, the comparison is not
available to them at all. **That is a real argument, and it is much weaker than a reader who
found the 8x themselves would allow.**

---

## 2. Envelope: it does not fit the ride it is designed for

| | |
|---|---|
| Closed envelope, longest dimension | **1839 mm** |
| ESPA Grande class limit | ~1270 mm |
| Over | **44 %** |

> **Kill threshold: if it will not fit a rideshare port, the entire hosted-deployer concept has
> no vehicle.** This is binary.

**Status, until 2026-08-10: crossed for ESPA Grande.** 1839 mm against ~1270 mm. The brake sits
beyond the 1500 mm release point and the enclosure must span it, so the length is structural
rather than packaging slack.

**Status now: NOT EVALUABLE, blocked on E5.**
[ADR-023](adr/023-target-host-class.md) re-scoped the target host to a spent upper stage or
hosted platform of POEM class, closing **P9**. **The threshold above is unchanged** — it has not
been weakened, deleted or re-baselined, because re-scoping a target after seeing the geometry
fail is `validation/README.md`'s band rule violated on a threshold instead of a band.

**What changed is which host it is evaluated against, and the honest consequence is that it can
no longer be evaluated at all.** No accommodation envelope for a POEM-class host is public — that
is **E5**, the same undisclosed data that keeps the recoil table parametric. **This design cannot
currently demonstrate that it fits anything.**

> **That is a worse epistemic position than a clean fail against a published number, and it is
> recorded as one.** A decision that converts a measured failure into an unmeasurable unknown is
> not progress. What the re-scope buys is that the project stops carrying a requirement two of its
> own accepted decisions — ADR-002 and ADR-010 — had already abandoned.

**The alternative was priced before it was rejected.** Fitting 1270 mm means a 731 mm acceleration
zone, since the 539 mm of overhead does not shrink, and velocity goes as √s: **16.029 → 12.286 m/s,
−25 %**, lifetime ×1.60 → ×1.43. Repackaging 150 mm of brake recovers about a third of that, and
depends on a layout nobody has drawn against an arrest section **P28** already says is
oversubscribed.

**E5 is now the only thing that can put a number back on this criterion**, and its priority rises
accordingly. A free-flyer removes the constraint entirely, which is one of the arguments for
PII-8.

---

## 3. The bank cannot source the shot

| | |
|---|---|
| Hard ceiling on bank ESR | **65 mΩ** |
| A single string of 32 × 190 F cells | **116 to 185 mΩ** |

> **Kill threshold: if no purchasable bank can deliver the pulse, there is no machine.**

**Status: crossed as designed.** Open as **P26**, with four parallel strings costed at PII-7:
closes it with roughly 2x margin, at four times the cells, mass and cost. **Fixable, but the fix
lands on threat 1**, since four times the bank mass raises the mass per satellite that is already
failing at 3U.

---

## 4. Tip-off at release

If the satellite leaves tumbling faster than it can detumble, the customer has lost the mission,
and no customer accepts that risk twice.

> **Kill threshold: tip-off above 2 °/s per axis**, the flown NRCSD figure.

**Resolved 2026-07-31, and the resolution made the threshold harder.** This entry used to say the
run sheet declared ≤5 °/s citing NRCSD-E while a sibling NRCSD ICD said 2 °/s, and that the
discrepancy had to be settled first. **There was no discrepancy — they are two different
deployers.** NRCSD is the internal one, flown through the ISS airlock hundreds of times, at
**< 2 °/s/axis**. NRCSD-E is the external Cygnus-mounted one at < 5 °/s/axis, a figure its own
publisher describes as pending further testing.

So the band was set against the looser comparator, from the provisional document, with no record
that the tighter flown number existed. **A7's band is now 2 °/s** and is 2.5x harder to pass than
it was. See **P30**.

**Status, until 2026-08-10: unmodelled.** A7 is specified and not run; E7 is open.

**Status now: MODELLED, and the risk moved.**
[`../validation/A23_tipoff_release.md`](../validation/A23_tipoff_release.md) modelled the release
rather than bounding it, and the answer is not the one A7-R implied.

**The release itself is comfortable.** Acceleration ends at 1300 mm and release is at 1500 mm, so
the payload coasts **12.2 ms with the commanded force already at zero**. At the ~1 N residual that
leaves, the mechanism has **250 µs of slack and still lands two orders of magnitude inside the
2 °/s band**. A7-R's 50.7 µs was a full-push worst case that does not occur.

**The risk is the clearance take-up, and it is new.** Under the 28.92 N·m offset moment the
payload accelerates across its cradle clearance at 688 rad/s² and **arrives at 36–231 °/s
depending on the fit — 18 to 115 times the band.** After impact it rebounds and rattles, and
whether that has settled by release depends on a restitution model this project does not have.

> **A34 closed this on 2026-08-13, and the threshold did not move.** The rattle settles after
> **27.25 ms of a 146.4 ms powered stroke** at the top of the aluminium restitution range, and the
> **residual angular rate at force removal is exactly zero** for every clearance A23 tabulated —
> so the 36–231 °/s arrival is transient and never becomes a release rate. Critical restitution
> is **0.9261** against an aluminium range of 0.3–0.7. The cradle preload is now **derived** at
> **85.0 N per contact** rather than asserted. **The mechanism still does not exist**, and
> restitution is swept rather than measured. `validation/A34_cradle_restitution.md`.

> **The threshold is unchanged and is not passed.** Tip-off is no longer *unmodelled*, but it is
> **not demonstrated below 2 °/s either** — it is now a stated requirement on a cradle preload
> (> 85 N per contact) and a release residual (≤ 1 N), against a mechanism that does not exist.
> Logged as **P41**. The payload's centre of mass sitting 70 mm off the thrust line is still the
> term that drives all of it; A23 band 5 prices removing it at a cut from 70 mm to **3.5 mm**.

---

## 5. Attitude rate at the moment of firing

The 0.0274 m/s dispersion claim assumes the host is pointing where the model says. Twelve
satellites index across two transverse cassettes between shots, moving kilograms of mass around
the structure.

> **Kill threshold: residual attitude rate at trigger above what the servo can null.** Above it,
> the deterministic-placement claim collapses, and deterministic placement is the entire
> differentiator against a spring.

**Status: MODELLED 2026-07-31 as A13, CORRECTED 2026-08-03, and it still FAILS.** Open as
**E24**.

**The indexing is fine and the sled return is not.** Advancing a satellite one cassette pitch
moves 4 kg; returning the 9.445 kg sled down 1.5 m of track is the term that dominates, and it was
in no budget anywhere in this repository until A13 ran.

**What the first version of A13 got wrong.** It read the peak angular momentum of a mass *while
it was moving* as a residual host rate *after* it stopped, which violates angular-momentum
conservation in its own ideal rigid-body model. A rigid host counter-rotates during the move and
returns to zero rate when the mass stops. What it keeps is an **attitude offset**, not a rate.

| Host | Index peak | Return peak | Residual ideal rate | Worst-case offset |
|---|---:|---:|---:|---:|
| 200 kg | 0.0195 °/s | **0.4427 °/s** | 0 | 1.367° |
| 500 kg | 0.0060 °/s | **0.1362 °/s** | 0 | 0.421° |

**The declared bands still fail**, on transient peak rate rather than residual: rows 3 and 4 are
**FAIL**, row 5 passes *only inside the ideal rigid-body model* because structural ringing is not
modelled (**E25**), and row 7 is **VOID** — there is no attitude controller, thruster geometry or
propellant model from which to compute a propellant change.

**The cadence conclusion that used to sit here is withdrawn.** The 8.2 s rate-null time, the
18.1 s cadence floor, the 6.9 s return optimum and the counter-mass recommendation all followed
from the residual-rate error and do not survive it. Attitude restoration now depends on a
controller and a schedule that this project has not specified, so there is no floor to quote.

**What the threshold turns on is still a number nobody has written down.** The repository carries
**two** inter-shot intervals — 10–20 s in the paper, 1200 s in `astro.py`'s conjunction model —
and never reconciles them (**P31**). That contradiction is untouched by the correction, and it
still decides whether this failure is operationally significant or a rounding error.

---

## 6. Host recoil

64.1 N·s per shot, **0.769 kN·s** for a full manifest, about 0.37 kg of
hydrazine-class propellant for the host to null.

> **Kill threshold: if a host will not accept the momentum and the pointing disturbance, nobody
> flies it.**

**Status: quantified and modest.** The fuel bill is independent of host mass; host mass sets the
per-shot rate disturbance. This is the healthiest item on the list, and it is here because it is
a customer decision rather than an engineering one.

---

## 7. Whether 16.5 m/s is worth anything

The threat behind all the others. If the delta-v does not buy something a customer wants, the
mass, the envelope and the bank are all irrelevant.

| What one shot buys | | |
|---|---|---|
| Orbital lifetime | ×1.60 at mean activity | **not invariant across solar activity** (P16) |
| Constellation phasing, 30° | 1.4 to 6.9 days | against **25 days** by differential drag |
| Apogee placement | ±0.10 km | from the closed-loop dispersion |
| **Plane change** | **0.12°** | **effectively nil** |

> **Kill threshold: if differential drag or onboard propulsion delivers the same outcome, there
> is no product.**

**Status: survives, narrowly, on one axis.** The phasing case is strong: 18x faster than drag,
and drag cannot be scheduled. The lifetime case is modest. **The plane-change ceiling of 0.12°
means VOLLEY cannot change orbit in the way "deployment at a chosen orbit" might suggest**, and
any framing implying otherwise is wrong.

> **The plane-change row now has two independent confirmations**, added 2026-08-10.
> [`../validation/A15_poem_campaign.md`](../validation/A15_poem_campaign.md) band 1 measured
> **0.1229°** in GMAT, and band 8 computes the same ceiling in closed form from
> Δv = 2·v·sin(Δi/2). The exchange rate at POEM circular velocity is **133 m/s per degree**, so
> one degree costs **8.1× the entire shot**. The 0.12° figure in the table above was an estimate
> when it was written; it is now a propagated result and a closed-form one that agree.

> **And the host cannot rescue it either.** A15's Case B asked what a host plane-change
> manoeuvre would cost. It is **VOID as a capability claim** — POEM's control authority is
> undisclosed (E5) — but the exchange rate holds regardless of who spends it. A plane change
> worth having costs one to two orders of magnitude more Δv than VOLLEY delivers, from a host
> that would have to already possess it. **There is no configuration of this architecture in
> which plane change becomes a product feature**, and the threshold above should be read with
> that settled rather than pending.

---

---

## Where Gen6 stands against these seven

**Added 2026-08-16.** [ADR-032](adr/032-gen6-stage-integrated-gas-store.md) moved the design target
on 2026-08-14 and this file did not follow it, so for two days the document that exists to say what
would make the project pointless described a machine the project had stopped building. That is the
failure this file was written to prevent.

**The seven thresholds below are unchanged.** Not one has been revised, and none will be revised
because a result came back against it. What follows is only where the *other* architecture sits
against them.

**Read the whole column before the good rows in it.** Gen6 improves four of the seven, and it
improves three of those **by deleting the subsystem the threshold was about** rather than by
meeting it. A criterion that no longer applies has not been passed.

| | Gen5, the measured baseline | Gen6 | |
|---|---|---|---|
| **1. Mass per satellite** | **10.547 kg**, crossed 5.3× | **10.547 kg on dry mass, crossed** — and **1.2145 to 3.0827 kg on added mass** at A56's sized store, the range [A45-R2](../validation/A45R2_stage_credit_resized_store.md) found when the stage credit is read hostilely. *The 1.296–3.164 published until 2026-08-20 was ADR-034's scaled store* | **Crossed on dry mass always, and on added mass as soon as P10's unmodelled lump is not credited to the stage. P59 and P68 both LIVE** |
| **2. Envelope** | 1839 mm against ~1270, over by 44 % | **Does not apply as stated** — Gen6 is a rail on an 8 m stage, not a payload in a rideshare port. **At ADR-034 the rail is 8.2 m against A37's 8.0 m usable acceleration length** | **PARTIAL**: the 200 mm overrun is stated, but no envelope analysis exists at Gen6 |
| **3. Bank ESR** | crossed; 65 mΩ ceiling against 116–185 available | **Dissolved.** There is no bank. A51 measures the electrical demand at **0.26 W average, 36 W peak** | **Deleted, not solved.** P26 is moot for Gen6 and stands for Gen5 |
| **4. Tip-off** | modelled at 85.0 N of cradle preload, mechanism absent | **A38: raising acceleration does not make it worse.** Preload is now **201.674 N per contact**, still releasing inside **≤ 1 N** | **Not demonstrated.** The mechanism still does not exist |
| **5. Attitude rate at firing** | quantified | unchanged in kind; the indexing mass move is the same problem on a larger vehicle | NEEDS SOURCE: not re-run at Gen6 |
| **6. Host recoil** | 64.1 N·s per shot | **116.03 N·s per shot — 1.81×**, 1407.9 N·s over the campaign, **0.653 kg** of propellant to null ([A52](../validation/A52_gen6_recoil.md)) | **Answered.** The interface requirement follows: **the thrust line must pass within 10.7 mm of the host centre of mass**, against Gen5's 19.5 mm |
| **7. Is the Δv worth anything** | 16.029 m/s | **34.280 m/s** zero-friction, **29.009** at the friction allowance, on ADR-034's design point | The one row Gen6 improves by doing more, not less. **ADR-033 restores the *commandability* the Δv is sold on** |

**Two rows still want a source, and they are not bookkeeping.** Envelope and attitude rate were
both quantified for Gen5 and neither has been recomputed for the architecture now carried as the
design target. **Recoil was the third and [A52](../validation/A52_gen6_recoil.md) closed it on
2026-08-19** — at 1.81× rather than the "roughly doubled" this paragraph guessed at.

**Criterion 1 is the one that matters and it has not moved.** Both numerators are reported wherever
either appears, the 2.0 kg threshold is untouched, and the honest options remain what they were:
change the payload class, or publish the criterion as crossed. Gen6 does not change that sentence.

## What this list says, taken together

**The 3U configuration as designed fails three thresholds**: mass per satellite, envelope, and
bank sizing. Two have identified fixes that make the third worse, since a bigger bank and a
repackaged envelope both add mass. **Gen6 removes two of the three by removing the subsystems
they were about**, and leaves the first exactly where it was — see the section above.

**The payload ladder is the only change that improves all three at once.** Smaller satellites
divide the fixed deployer mass across more customers, and the mass argument reverses from an 8x
loss to a 6x win. That is why [`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md) is the highest-value
work available, ahead of any velocity recovery.

**Nothing here is fatal to the concept**, and two items are close enough to the line that they
should be treated as design drivers rather than open problems. That distinction is what this
file exists to make.

---

## Provenance

Every threshold above is either computed in `analysis/`, taken from a published standard, or
labelled as an estimate. **The 2 kg per satellite figure in threat 1 is an estimate**, and it is
the one doing the most work, so it is the one most worth refining. Cold-gas module masses are
from published COTS ranges rather than a specific quotation.
