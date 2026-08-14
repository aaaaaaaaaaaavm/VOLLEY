# VOLLEY-lab

**The vault: ideas that never became a complete thing, and why each one stopped.**

<!-- PROGRAMME-HEADER-START -->
| Repository | Role | You are here |
|---|---|---|
| [VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY) | Main: the authoritative engineering record. Improved continuously |  |
| [VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) | The concept at its most reliable, as a conference contribution. **Frozen when published** |  |
| [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) | The same concept as a full submission. **Frozen when presented** |  |
| **[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)** | The vault: ideas that never became a complete thing, and why each stopped | ← |
<!-- PROGRAMME-HEADER-END -->

> ## Nothing here should be cited
>
> No baseline, no stability promise, no acceptance bands. Numbers on these pages may be
> wrong, half-finished or abandoned mid-thought. The engineering record is
> [VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY), and where anything here disagrees
> with it, **it is right and this is not**.

## What this repository is for

Every project accumulates work that was real but did not finish: an architecture that was
priced and declined, a scaling study that answers a question nobody has asked yet, a
measurement that killed something. Most of it is deleted, and the reasoning is lost with it.

**This is where that work is kept instead.** It is a vault, not a graveyard — the difference
is that a vault is organised for retrieval.

The main record stays clean because this exists. A research track kept *inside* it is one
`git checkout` from becoming an edit to the record; a separate repository is a wall rather
than a line on the floor.

## The one rule

**Every entry states why it stopped.**

Not "deferred" — *why*, with the number that decided it. The rail-drive entry upstream carries
the transverse edge factor of **0.0253** that killed it, against the **0.55** it had been sized
on. PII-14 below carries the drivetrain inertia that eats its own gain. PII-19 carries the **11 %**
that made a whole architecture the wrong answer. **That is what makes this evidence rather than a
pile**, and it is the only rule here.

> ### Nine entries stopped together on 2026-08-14
>
> [ADR-032](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/adr/032-gen6-stage-integrated-gas-store.md)
> made the payload accelerate directly, by gas, along a rail the spent stage provides — and
> **deleted the subsystem that nine vault entries improve.** No mover, so PII-1, PII-2, PII-17 and
> PII-18 have nothing to act on; no stator, so PII-3 and PII-12; no bank, so **PII-7**, which was
> P26, the largest live defect the project carried; no envelope and no track, so PII-4 and PII-11.
>
> **Not one was refuted.** Each is a correct optimisation of a part that stopped existing, and
> **PII-1's own arithmetic is why the mover went**. The full list is in the main repository's
> [`docs/VAULT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/VAULT.md).
>
> **PII-8 gains.** Its hardest problem was airgap straightness over a deployed structure, and the
> new architecture has no airgap.

An entry without a reason is not deferred. It is abandoned with extra steps.

## What is here

Long-form entries live in this repository. The complete register — every entry, its status
and its entry criterion — is kept in the main repository so the numbering cannot fork:
**[`docs/VAULT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/VAULT.md)**.

| | |
|---|---|
| [**PII-8** — VOLLEY as a free-flyer](PII-8_free_flyer.md) | A long deployed track and release at perigee reaches TLI and Mars-class C3 without exceeding CubeSat qualification. **Stopped by three problems named in the file**: airgap straightness at 0.7–2 ppm over a deployed structure, a 294 kJ shot against a bank that already fails at 2.88 kJ, and whether 25 g survives review as a *sustained* load |
| [**PII-9** — the lunar case](PII-9_lunar.md) | Where this technology has always belonged, and the mass driver it descends from. 1.33 MJ/kg to lunar orbit, so 15 kW launches a tonne a day. **Stopped by having no host**: it describes a different programme, not this one. The payload is ore, so the g-limit governing the whole design disappears |
| [**PII-11** — a deployable track, and the side-rail layout](PII-11_deployable_track.md) | A telescoping track long enough to accelerate *and* regeneratively arrest reaches **48 % electrical-to-payload efficiency**, deletes the eddy brake and stows inside the ESPA Grande envelope the main design misses by 44 %. The only option that improves velocity and envelope together. **Stopped by type, not by number**: a deployable structure is an architecture change however good its numbers are |
| [**PII-14** — a cable-driven gondola on a deployed truss](PII-14_cable_driven_gondola.md) | Propulsion off the vehicle onto a cable, energy from a flywheel. **Stopped by the assumption inside its own headline**: +49.7 % assumed a drivetrain with zero rotating inertia, and a real one gives +15 to +30 %, possibly zero — in exchange for deleting the linear synchronous motor and the 24 validations behind it. Its two dead ends are recorded too, because both will otherwise be re-proposed |
| [**PII-19** — the induction-drive Gen6](PII-19_induction_drive_gen6.md) | A linear induction drive on a 0.25 kg passive plate instead of a 9.445 kg magnet sled. **It was the main repository's design target for one day.** **Stopped by attribution, not refutation**: A35 measured the mover it optimises at **11 % of dry mass**, so the whole synthesis is a careful, banded, correct optimisation of the wrong term. Its nine measured bands stand |
| [`notes/`](notes/) | Unstructured, date-stamped, finished by nobody |

**PII-11 is the one that is hardest to leave shut**, because unlike the others it improves the
machine actually being built rather than describing a different one. That is exactly why it
needs a gate.

## How something leaves

| From → to | Condition |
|---|---|
| **vault → main** | Its acceptance bands were declared **before its script existed**, and run |
| **main → paper / thesis** | Stable, effective and reliable against the problem statement |
| **paper / thesis → frozen** | Presented or published |

**Nothing crosses upward on enthusiasm.** An item is promoted by meeting the criterion it was
given — written when it was deferred, not when it is reviewed, because a criterion written
afterwards is written by someone who already knows what they want the answer to be.

## What does not belong here

**Corrections.** If something in the main repository is *wrong*, fix it there. The distinction
is by type, not by convenience: a tedious bookkeeping error belongs upstream, and a fascinating
architecture belongs here.

## Adding an entry

Name it. State what it buys, with a number. Say why it is improvement rather than correction.
Then write its entry criterion **before you stop thinking about it** — and when it stops, write
down what stopped it.

## Licence

**CC BY 4.0** — full text in [`LICENSE`](LICENSE), attribution form in [`NOTICE`](NOTICE).
Attribution requires credit, a link to the licence, and **an indication of whether changes were
made**.

**Not retroactive:** snapshots taken before this change remain available under the MIT licence
they carried at the time, retained at [`LICENSE-MIT-superseded`](LICENSE-MIT-superseded).

This repository carries copies of VOLLEY analysis code under `reference/volley/`. CC BY 4.0 does
not license patent rights, which is why a patent-granting licence was not used here.
