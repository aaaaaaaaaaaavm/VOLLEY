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

Not "deferred" — *why*, with the number that decided it. The rail-drive entry carries the
transverse edge factor of **0.0253** that killed it, against the **0.55** it had been sized
on. The cable gondola carries the drivetrain inertia that eats its own gain. **That is what
makes this evidence rather than a pile**, and it is the only rule here.

An entry without a reason is not deferred. It is abandoned with extra steps.

## What is here

Long-form entries live in this repository. The complete register — every entry, its status
and its entry criterion — is kept in the main repository so the numbering cannot fork:
**[`docs/VAULT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/VAULT.md)**.

| | |
|---|---|
| [**PII-8** — VOLLEY as a free-flyer](PII-8_free_flyer.md) | A long deployed track and release at perigee reaches TLI and Mars-class C3 without exceeding CubeSat qualification. **Stopped by three problems named in the file**: airgap straightness at 0.7–2 ppm over a deployed structure, a 294 kJ shot against a bank that already fails at 2.88 kJ, and whether 25 g survives review as a *sustained* load |
| [**PII-9** — the lunar case](PII-9_lunar.md) | Where this technology has always belonged, and the mass driver it descends from. 1.33 MJ/kg to lunar orbit, so 15 kW launches a tonne a day. **Stopped by having no host**: it describes a different programme, not this one. The payload is ore, so the g-limit governing the whole design disappears |
| [**PII-11** — a deployable track, and the side-rail layout](PII-11_deployable_track.md) | A telescoping track long enough to accelerate *and* regeneratively arrest reaches **48 % electrical-to-payload against 18.5 %**, deletes the eddy brake and stows at 1150 mm. The only option that improves velocity and envelope together. **Stopped by type, not by number**: a deployable structure is an architecture change however good its numbers are |
| [**PII-14** — a cable-driven gondola](PII-14_cable_driven_gondola.md) | Propulsion off the vehicle and onto a cable, energy from a flywheel. A 2 kg gondola reaches **24.5 m/s in the existing 1.30 m track** — *if the drivetrain has no rotating inertia*. **Stopped by `m_eff = I/r²`**: at 7.4 kg of referred inertia the entire gain is gone |
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
