# Gen5, closed

**Phase I closes here.** This page is the whole Gen5 case in one place: what it is, what every
headline number rests on, what failed, and what is deliberately left open. **It is written to be
checked, not to persuade.**

> **Nothing in this project has been built, fired, measured, qualified or flown**, and no result
> here has been reviewed by a third party. Every number is a script output.

<p align="center">
  <img src="../cad/renders/gen5/hero_open.png" alt="VOLLEY Gen5, open" width="100%">
</p>

---

## What Gen5 is

**A magazine-fed electromagnetic deployer that ejects unmodified 3U CubeSats at a commanded
velocity, at a deployment acceleration of 10.07 g.** *That last clause is a property of the
machine, not a statement about any satellite: 25 g is a ceiling this design sets on itself, no
published standard fixes a universal quasi-static qualification level for CubeSats, and payload
structural compatibility is vehicle- and mission-specific and has not been established
([P98](../OPEN_PROBLEMS.md)).* An ironless
double-sided Halbach linear synchronous motor drives a reusable 9.45 kg permanent-magnet sled
along a 1.5 m track — 1.3 m of acceleration and 0.2 m of coast-trim. Twelve satellites feed from
two transverse cassettes. A contactless eddy-current brake arrests the sled; the satellite departs.

**The claim is not electromagnetic launch.** That has been studied at twenty times the velocity.
**The claim is programmable velocity, a satellite that is never modified mechanically and
electrically, and an acceleration at 10.07 g rather than the thousands an armature-based launcher
imposes — all three at once.** *No payload has been mechanically qualified against this machine.*

## Every headline number, and what it rests on

**Nothing in this table is restated by hand.** Each figure lives in
[`BASELINE.md`](BASELINE.md), is regenerated from the scripts, and is checked on every commit by
`tools/make_baseline.py --check`.

| | | |
|---|---:|---|
| Thrust constant | **10.54 N per kA/m**, ±1.01 % ripple | `motor_model.py`. A 2-D meshed FEM agrees with the **centre-plane** constant to **0.03 %** and a 3-D solve with the **field** to 0.059 %; **neither tests the depth average** that took K<sub>t</sub> from 11.03 to 10.54 ([ADR-030](adr/030-apply-the-depth-resolved-thrust-constant.md)) |
| Exit velocity, 3U | **16.029 m/s** | at **10.07 g**, against this design's chosen 25 g ceiling (**P98**) |
| Pulse duration | **162.3 ms** | |
| Energy drawn per shot | **2782 J gross**, 2735 net | 47 J recovered, **3.9 % of sled KE** |
| Electrical-to-payload efficiency | **18.8 %** | net of regeneration |
| Closed-loop dispersion | **0.0274 m/s (3σ)** | ±0.10 km of apogee placement |
| Dry / loaded mass | **126.6 / 174.6 kg** | from CAD solid volumes, not parametric |
| Per 3U satellite | **10.547 kg dry** | **crosses kill criterion 1 at 5.3×** |
| Lifetime multiplier | **×1.6** at mean activity | quoted at a stated activity level, **not claimed invariant** |
| Track first mode | **109.0 Hz** fixed-fixed | |
| Recurring hardware cost | **₹1,345,055 per unit** | **every price assumed** |

## What was verified, and by what

**Three results have genuinely independent cross-checks. Everything else is single-sourced, and
the register says so.**

| | |
|---|---|
| **Halbach field** | Analytic against **magpylib** to three digits, then against a **meshed magnetostatic FEM** — a PDE solve rather than another superposition — agreeing to **0.03 %** on the centre-plane constant, and a 3-D scalar-potential solve agreeing to **0.059 %** on the midgap field. *Both check the field model; the depth-resolved integral itself has no independent 3-D check* |
| **Orbital decay** | Orbit-averaged against an independent **Cowell RK4** propagation to **99.4 %** |
| **Shot circuit** | **ngspice** reproduced the analytic model to 0.03 %, then found a loss the analytic model had no term for — the bank's own series resistance, **86 J a shot** (**P24**) |
| **Structure** | **CalculiX** cleared the chassis on all three bands, which settled the sled at the CAD-derived 9.445 kg and moved the headline to 16.0 m/s |
| **Aerodynamics** | **OpenFOAM** `simpleFoam`, k-ω SST, `snappyHexMesh` off the Gen5 sled STL. **Mesh-converged: 6.3× the cells moves the answer 4.86 %** |
| **Orbit propagation** | **GMAT R2022a**, headless, MSISE90 with 20×20 gravity, lunisolar third bodies and SRP — **and it falsified a claim in this paper's own abstract** |

## What failed

**This section is why the record is worth reading.**

**Three analyses failed outright.** GMAT falsified the lifetime-invariance claim the paper had
offered as its defensible result — ×1.80 at mean and high activity, **×2.074 at low, an 18.5 %
spread against a ≤5 % band**. A13's attitude budget failed two declared peak-rate bands. A45's
stage credit failed three.

**Three times a declared band caught a bug in the analysis rather than in the design.** That is
the mechanism working in the direction nobody plans for.

**And the corrections cost, every time.** The sled went 4.86 → 9.445 kg from CAD solid volumes and
took exit velocity 20.37 → 16.388 m/s with it. A quadrature error took K_t 11.03 → 10.54 and every
dependent number with it. The enclosure was an 8.00 kg placeholder; itemising it gave **50.04 kg**
against an earlier warning that had guessed 20. **Nothing improved. That is what the corrections
cost, and all of it is dated in [`CHANGELOG.md`](../CHANGELOG.md).**

## The kill criteria

**Seven thresholds, three crossed, and no threshold has ever been moved.** A threshold revised
after a result is known is not a threshold. [`KILL_CRITERIA.md`](KILL_CRITERIA.md) carries all
seven with their evidence.

**Criterion 1 is the one that matters: above roughly 2 kg per satellite a rational customer buys a
propulsion module instead.** Gen5 is **10.547 kg**. [A35](../validation/A35_constraint_ledger.md)
attributed every kilogram to the requirement causing it and found **88.67 kg — 70.06 % — survives
the deletion of every requirement in all 64 corners**, so **there is no architecture that reaches
2 kg.** A36 closed the manifest route. **Only a smaller payload class remains, and that decision is
deferred rather than taken.**

## What is deliberately left open

**These are permanent caveats, not debt.** `PHASE_I_CLOSURE.md` §9 declared this end state before
the closure was reached: *"A realistic Phase I close leaves E4 open, categories D and E open with
named owners, and categories A, B and C closed. That is a defensible end state. An empty register
would not be."*

| | |
|---|---|
| **E4** | **Nothing has been built, fired or measured at any scale.** [`FIGURE_INDEX.md`](FIGURE_INDEX.md) classes every figure by evidence type, and **the class for *measured* has zero members.** No analysis on this page changes that |
| **A9** | Decay against flown CubeSats. `celestrak.org` returns **403 at CONNECT** under this environment's network policy — re-tested 2026-08-20, not assumed. The NORAD shortlist is already in the run sheet; this is an afternoon on any unrestricted machine |
| **E18** | Conjunction covariance is invented. Needs a real CDM, which needs an operator relationship |
| **T-1 … T-8** | The qualification campaign. Specified 2026-07-29, **none run, all need hardware** |
| **B-1 … B-4** | The benchtop programme — see below |
| **E5** | Host stage properties. **One data exchange converts this analysis from parametric to specific**, and the paper names it |

### A7 is closed, and not by A7

**[A7](../validation/A7_separation_chrono.md) was specified and correctly never run.** Project
Chrono was unavailable, and — the reason that actually mattered — **the release mechanism it would
have simulated is not defined anywhere in this repository**, and a multibody model of an undefined
mechanism produces a number with no provenance.

**The work went where that argument pointed instead.** A7-R gave the angular-impulse budget
(**1.465 mN·m·s** for a 2 °/s release). [A23](../validation/A23_tipoff_release.md) modelled three
rigid-body stages with the mechanism properties as **swept axes** rather than invented:
**ideal release 0 °/s**, skew tolerance **50.6 µs**, cradle reaction **85.0 N against a 200 N
band**. [A34](../validation/A34_cradle_restitution.md) closed the impact A23 opened — **five of
five**, the rattle settling in **27.25 ms of a 146.4 ms powered stroke** and leaving **exactly zero
residual rate at every clearance**.

> **`PHASE_I_CLOSURE.md` listed A7 as unrun Category A work until 2026-08-20**, ten days after A23
> answered it. **The closure document had a stale gap in itself** — a worse defect than the gap it
> described, because a closure is read as the statement of what remains. Corrected, and recorded
> here rather than quietly.

## The handoff to hardware

**`B-1` — a Halbach pair on a gaussmeter, ₹22,000, one afternoon — is the cheapest path to the
first measured number in this project.** [`B1_ORDER.md`](B1_ORDER.md) is a purchase order rather
than a procedure, deliberately: *"A procedure invites more analysis. A purchase order invites a
purchase."* **It has not been ordered.**

> ### The benchtop programme belongs to Gen5, and that is worth stating plainly
>
> **All four specified tests validate subsystems Gen6 deleted** — **B-1** and **B-2** the motor,
> **B-3** the capacitor bank, **B-4** the eddy brake. [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
> removed all four on 2026-08-14.
>
> **That is not a reason to skip them. It is the reason they are Gen5's closure rather than Gen6's
> start.** B-1 changes **E4** from true to false — *a change of category, not of degree* — and it
> measures the field model that every Gen5 number in the table above descends from.

## Phase I is closed

**The last item was found while writing this page, which is the argument for writing it.**

**The paper's system mass was 50 % low, in its own abstract** — 84.5 kg against the repository's
126.6. [A46](../validation/A46_enclosure_buildup.md) itemised the enclosure on 2026-08-16, an
**8.00 kg placeholder becoming 50.04 kg**, and the arithmetic names the cause exactly:
**84.5 − 8.00 + 50.04 = 126.54.**

**Fixing it exposed more than the entry described.** The payload-family table was stale in **every
column, not just mass** — its velocities sat at the **pre-ADR-030** operating point, so the 3U row
read **16.4 m/s at 10.5 g** against the paper's own rated point of **16.0 at 10.1** stated two
paragraphs earlier. **The table contradicted its own paper.** And it was internally inconsistent:
seven rows 76.5-based, the 3U row alone 84.5-based.

**All of it is regenerated from `payload_family.json` and both PDFs are rebuilt and verified.**
[P93](../OPEN_PROBLEMS.md) is closed.

> **The audit that opened P93 checked thirteen headline scalars and passed eleven. It could not see
> the table** — the prose carries 16.0 and the table carried 16.4. *The right number in the wrong
> place hides the wrong number in the right one.*

## Gen6, and why it is not in the paper

**On 2026-08-14 the design target changed.** [ADR-032](adr/032-gen6-stage-integrated-gas-store.md)
made the payload accelerate directly, by cold gas, along a rail a spent upper stage provides — **no
mover, no stator, no capacitor bank, no brake, no return stroke.**

**Gen5 remains the entire technical contribution of the paper and thesis, and that is deliberate.**
Nothing in Gen6 is measured, its cradle mechanism does not exist, no launch provider has agreed to
lend a stage, and [ADR-036](adr/036-seal-specification-and-the-trim-stage.md) suspended its trim
stage on 2026-08-20 pending a seal friction nobody has measured. **A paper reports what has been
analysed to a declared standard, not what looks best this week.**

**Gen6 is documented in full in this repository** — [`generations/GEN6.md`](generations/GEN6.md),
ADRs 032 through 036, and the register — **and it is future work.**

## Where the rest of the programme lives

| | |
|---|---|
| [**VOLLEY-lab**](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) | **The vault.** Ideas that never became a complete thing, each with the number that stopped it — and where Gen6's own future work is parked |
| [**VOLLEY-paper**](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) | Gen5 as a conference contribution. **Frozen when published** |
| [**VOLLEY-thesis**](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) | The same work as a full submission, with its defect register attached |
| [**engineering-evidence-toolkit**](https://github.com/aaaaaaaaaaaavm/engineering-evidence-toolkit) | The consistency checks, extracted. Its own badge reads **"scope: consistency, not validation"** — *that distinction is this project's thesis in miniature* |
| [**pulsed-linear-motor-design-lab**](https://github.com/aaaaaaaaaaaavm/pulsed-linear-motor-design-lab) | The drive-side analysis as a standalone reference |
| [**orbital-deployment-trade-study**](https://github.com/aaaaaaaaaaaavm/orbital-deployment-trade-study) | The orbital case as a standalone reference |

---

**Register at closure: 133 numbered entries, 53 live, 45 corrected and retained, 35 closed.
64 run sheets covering 61 analyses across A1–A65 — A3, A26, A57 and A60 were numbered and never
written — each against a band declared in writing before its script existed.
Nothing has been validated by hardware.**
