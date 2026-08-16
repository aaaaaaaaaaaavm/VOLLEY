> # SUPERSEDED 2026-08-14 by [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
>
> **The rail drive was rejected by its own band** — a measured transverse edge factor of **0.0253**
> against the **0.55** it had been sized on — and the Gen6 it belonged to has since been replaced
> for a different reason: [A35](../validation/A35_constraint_ledger.md) found the mover it
> optimises is 11 % of dry mass.
>
> **Nothing below is edited.** Both records are kept: a variant killed by measurement, inside an
> architecture retired by attribution.

# Gen6: the satellite is the mover, and it already has the hardware

> # REJECTED, 2026-08-13, by A30 band 1.
>
> **The transverse edge factor this document rests on was assumed at 0.55. It is 0.0253** — a
> factor of 22. Four CDS rails at a generous 0.60 T make **41.9 N** against the **413 N** needed
> to reproduce Gen5. No pole pitch rescues it: the edge factor wants the secondary wide against
> the pole pitch, the airgap wants the pole pitch large against the gap, and an 8.5 mm conductor
> in a 10.5 mm effective gap demands both at once.
>
> **The document is kept unedited below**, because this project publishes what it got wrong. It
> named 0.20 as the value at which the idea would be dead, and it named A30 band 1 as the
> cheapest way to find out. Both were right.
>
> **What survived is in the same sheet.** A **90 mm flat plate** — the widest that fits inside a
> 3U's own section — has an edge factor of **0.6691**, makes **378 N at 0.45 T** (A31; the
> 1652 N first reported here assumed the magnetic-pressure ceiling and was 4.4× high, **P50**),
> and weighs
> **0.248 kg**, against 0.5–1.2 kg for the cold-gas module it would replace. **The drive is
> sound; the rail is the wrong conductor.** See [`../validation/A30_rail_drive.md`](../validation/A30_rail_drive.md)
> and **P49**.

**Proposal, 2026-08-13. Sizing exists; no acceptance band has been declared and nothing here is
a validated result.** [`../analysis/rail_drive.py`](../analysis/rail_drive.py),
`analysis/results/rail_drive.json`.

---

## The observation

The **CubeSat Design Specification** has required, since 2003, four **hard-anodised aluminium
corner rails** on every CubeSat ever flown. Their stated purpose is to be pushed and guided by a
deployer.

Look at what that specification actually mandates:

| The CDS requires | Which happens to be |
|---|---|
| Four rails, at the corners, symmetric about the long axis | A **balanced** four-phase coupling geometry |
| Aluminium, 6061 or 7075 | A **conductor**, σ ≈ 2 × 10⁷ S/m |
| Minimum 8.5 mm wide, running the satellite's full length | **116 cm²** of coupling area on a 3U |
| Hard-anodised — an insulating surface over conductive bulk | Irrelevant to eddy currents, and it removes any need for contact |
| Structural: the rails carry the launch load path | Able to take **hundreds of newtons** of distributed shear |

**Every deployer ever built treats those rails as a bearing surface.** P-POD slides on them.
NRCSD slides on them. This project's own cassette, escapement and cradle grip them. Feng's
coilgun ignores them and bolts *aluminium armature coils* onto the payload instead. The Harbin
programme ignores them and drives a conveying platform.

**Nobody has used the rails as the motor's secondary.**

They are, by accident of a twenty-three-year-old mechanical standard, a **linear induction motor
armature that every customer already owns, already qualifies, and already flies.**

---

## What follows if you drive on them

**The satellite becomes the mover. There is no sled.**

And once there is no sled, a chain of this project's most expensive problems stops existing
rather than being solved:

| Today | Gen6 |
|---|---|
| A **9.445 kg sled** carries the magnets. It is 70 % of the moving mass, so 70 % of the shot energy accelerates hardware that is not the payload | The moving mass is **the 4 kg satellite** |
| That sled must then be **stopped**: an eddy brake absorbing 935 J and putting **18.5 kN** through a structure holding eleven stowed satellites, eleven times (**E34**) | **Nothing to arrest.** No brake |
| The brake sits beyond the release point, and the enclosure must span it — which is *why* the envelope is **1839 mm** against ESPA-Grande's 1270 (**kill criterion 2**) | The machine ends where the stroke ends |
| The sled must be **returned** down 1.5 m of track between shots — the dominant term in the attitude budget (**E24**, **kill criterion 5**) | Nothing returns |
| The payload rides in a cradle with its centre of mass **70 mm off the thrust line**, crossing its clearance at 688 rad/s² and arriving at **36–231 °/s** (**P41**, **kill criterion 4**) | Thrust is applied to **four rails symmetric about the satellite's own axis**. There is no cradle and no clearance to cross |
| Permanent magnets 20 mm from the payload at **442× a magnetometer's full scale**, leaving soft-magnetic parts permanently altered (**E35**, **P34**) | No permanent magnets anywhere. An iron-cored stator has **no residual dipole when off**, so **E33** — the host wheel saturating in 3–7 days — has no source |
| "The satellite is never modified" is a **claim the repository's own evidence contradicts** | It is a **consequence of the topology**. Nothing is attached, nothing is added, nothing is left behind |

---

## Does the physics work

Sized in [`../analysis/rail_drive.py`](../analysis/rail_drive.py) from the goodness-factor form
of a sheet-secondary induction machine, double-sided stators straddling each rail, holding
**G·s = 1** — the machine's own thrust maximum, where thrust sits at the magnetic pressure
B²/2μ₀ independently of speed and the drive holds it by raising frequency and lowering slip.
That is an ordinary variable-frequency schedule, and energising only the section under the
satellite is exactly what **ADR-022**'s segmented stator already provides.

**Design point — modest flux, a realistic 2 mm clearance, and the *worse* of the two rail alloys,
so nothing rests on a customer's metallurgy being lucky:**

| | Today | **Gen6 rail drive** |
|---|---:|---:|
| Moving mass | 13.45 kg | **4.0 kg** |
| Thrust | 1389 N | 513 N |
| Acceleration | 10.1 g | **13.1 g** (cap is 25–30 g) |
| **Exit velocity, 3U** | 16.03 m/s | **18.26 m/s** |
| Stroke time | 162.3 ms | 142 ms |
| **Energy drawn per shot** | 2782 J | **1182 J — 2.4× less** |
| Payload share of energy drawn | 18.8 % | **56.5 %** |
| Drive frequency | — | to 233 Hz |
| **Heat into the customer's rails** | — | **1.7 K** |

**It is faster *and* cheaper in energy, and the reason is the same in both cases: there is no
sled.** Today 70 % of the shot energy goes into a 9.4 kg mover that is then braked away. Here the
only thing accelerated is the thing being delivered.

At 0.60 T the same machine reaches **24.35 m/s at 23.2 g** — still inside the qualification cap,
and close to the 26–35 m/s ceiling [`VELOCITY_CEILING.md`](VELOCITY_CEILING.md) shows is set by
the payload rather than by the motor.

**Thrust is alloy-independent at this operating point.** Only the slip loss changes — 6061 rails
draw 1060 J, 7075 rails 1182 J. A deployer does not get to choose what its customers' rails are
made of, so that insensitivity is worth more than the efficiency it costs.

---

## Why this is the angle, and not just a topology swap

**A spring is a catapult. An OTV is a vehicle. Nobody has built the road.**

Every approach to this problem puts the expensive, heavy, active hardware on the thing that
moves — a sled, an armature, a bus. This inverts it: **the active hardware stays on the stage,
and the moving part is the customer's own satellite, unmodified, riding an interface it was
already required to have.**

Which resolves the argument that started this. **"Unmodified" stops being a marketing position
to defend and becomes a physical property of the drive.** There is no fin to design, no interface
to publish, no adopters to recruit, no second standard competing with the first.

**The container is already there.** The CubeSat rail is the corner casting. Every deployer in
history has built a crane that *lifts* it. This builds the first one that *drives* it.

---

## What would kill it

Stated first, because sizing that clears a requirement by 24 % is not evidence and the failure
modes below are where this actually gets decided.

1. **The edge-effect derating is the whole result.** An 8.5 mm rail against a 48 mm pole pitch
   gives the induced current a short, high-resistance transverse return path. `rail_drive.py`
   assumes **0.55** and says so at the top of the file. **If the true figure is 0.2, the design
   point falls to 187 N and the idea is dead.** This is the first thing A30 must settle, and a
   3-D eddy-current solve is what settles it — the same class of computation
   [`../validation/fem3d/`](../validation/fem3d/) already does for the magnetostatic case.
2. **The airgap is set by somebody else's tolerances.** 2 mm of clearance around a 340 mm
   satellite whose rail flatness and straightness are specified loosely. Thrust falls with the
   square of nothing — it falls through the goodness factor, which is inverse in the effective
   gap. A guided channel helps; a rail out of tolerance still jams a 2 mm slot.
3. **It only works on payload classes that have CDS rails — and those are the classes whose
   economics do not close.** Kill criterion 1 fails at 3U and closes only at PocketQube, which
   has a *different* rail standard. **This is the sharpest tension in the proposal** and it is
   not resolved by making the machine better. It is decision **D2** in
   [`STATE_OF_THE_PROJECT.md`](STATE_OF_THE_PROJECT.md), still unmade.
4. **Slip loss lands in the customer's structure.** 1.7 K is comfortable, but it is 1.7 K into a
   hard-anodised structural member on somebody else's spacecraft, and it is heat this project
   would be putting there without a thermal interface agreement. It needs to be in a payload
   interface document, not in a repository.
5. **Normal forces.** A double-sided stator straddling a rail balances its attraction by
   symmetry only while it is centred. Off-centre, the net force is large and destabilising.
   Whether that is a bearing problem or a design-killer is unknown.
6. **Retention during launch still needs a mechanism.** The drive removes the cradle, the
   detent and the brake. It does **not** remove the need to hold twelve satellites through
   launch random vibration, so the gates and escapements — and **E30**'s remaining shared
   elements — stay.

---

## What it does to the register, if it survives

**Not claimed as closed. Listed as what the proposal would have to be measured against.**

| Entry | Today | Under Gen6 |
|---|---|---|
| **E30** — 9 of 13 elements forfeit the remaining manifest, #1 on the lethality ranking | Sled, brake, sled return and cradle are four of the shared nine | Those four have no counterpart. The element count needs recomputing, not assuming |
| **E34** — 18.5 kN through eleven stowed satellites, #4 | Brake | **No brake** |
| **E33** — residual dipole saturates the host wheel in 3–7 days, #3 | Permanent magnets on the sled | **No permanent magnets** |
| **E35 / P34** — the payload is magnetically modified, #5 | 442× magnetometer full scale at 20 mm | Iron-confined stator field, no magnets |
| **Kill criterion 3** — bank ESR crossed at 116–185 mΩ against a 65 mΩ ceiling | 2782 J per shot | **1182 J**, and peak power falls with it. May close on one string instead of four |
| **Kill criterion 2** — envelope 44 % over | Brake sits beyond release | Machine ends at the stroke |
| **P28**, **E24**, **P41** | Arrest section, sled return, cradle | No counterpart |
| **Kill criterion 1** — 10.547 kg per satellite | | **Improves but does not close.** Roughly −12 kg of sled, brake and bank against maybe +4 kg of stator iron |

---

## The next artefact

**A30, with its bands declared before the script exists**, as every analysis in this repository
has been:

1. **The edge-effect factor**, from a 3-D transient eddy-current solve on the real rail
   geometry. Band on the derating, because that is what the whole result scales on.
2. **Thrust against airgap**, swept across the CDS rail tolerance rather than at one nominal.
3. **Rail temperature rise**, against a stated payload thermal interface limit.
4. **Normal force against lateral offset**, which decides whether this needs a bearing or a
   redesign.
5. **A recomputed E30 element list**, which is the only one of the five that bears on the
   lethality ranking.

**Nothing above should move the Gen5 baseline.** Gen5 is generated, checked and current;
Gen6 is a proposal with one sizing script behind it. **The right next step is A30 band 1** — and
if the edge factor comes in low, this document is what a rejected idea looks like when it was
written down honestly.
