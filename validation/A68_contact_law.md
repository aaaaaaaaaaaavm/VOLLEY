# A68 — the contact law, verified, and the model-form uncertainty it carries

**Closes, if it passes:** [A67](A67_guided_contact.md) band 3, which failed — the
Lankarani–Nikravesh implementation returned **+13.7 %** restitution error at the nominal
coefficient and **+128 %** at 0.3.

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/contact_laws.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/contact_laws.py`, which must return
> nothing.

## Why this run exists

**A67 band 3 failed and A67's verdict stands.** This is not a re-run of A67 and it does not
re-evaluate A67's bands. **It asks a different question: which compliant-contact formulation
actually returns the restitution it is given, and how much of A67's headline is model form rather
than physics.**

**A67 said the failure was the known domain limit of Lankarani–Nikravesh** — its damping–restitution
relation is derived assuming most impact energy is stored elastically, which holds as e → 1.
**That is a claim about the law and it is testable.** If it is right, a formulation built for the
low-restitution regime will recover e where LN does not.

**The methodology is the one recorded in [`docs/EXTERNAL_EVIDENCE.md`](../docs/EXTERNAL_EVIDENCE.md):**
contact parameters are *identified by inversion* against a reference, not assumed. Three
formulations are implemented and the third is identified rather than derived.

## The three formulations

| | Damping term | Where it comes from |
|---|---|---|
| **LN** | `1 + 3(1−e²)/4 · δ̇/δ̇⁻` | Lankarani–Nikravesh. **What A67 used** |
| **HC** | `1 + 3(1−e)/(2e) · δ̇/δ̇⁻` | Hunt–Crossley's own coefficient, which does not assume e → 1 |
| **ID** | `1 + χ · δ̇/δ̇⁻`, **χ found by root-finding** so the free-impact restitution equals the declared e | Identified, not derived. *This is the inverse-identification route the separation-dynamics literature uses* |

## Acceptance bands

**Seven bands. Bands 1, 2 and 6 can fail, and a failure of 6 is the most useful outcome.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **ID recovers restitution to 0.5 %** across e ∈ {0.2, 0.3, 0.5, 0.7, 0.9} and v⁻ ∈ {0.05, 0.5, 2.0} m/s | The identification does not converge, and no formulation here is verified |
| **2** | **HC beats LN** at every e below 0.7 | A67's diagnosis — that the failure is LN's domain limit — is wrong, and the error is somewhere else |
| **3** | **All three agree within 2 %** as e → 0.9 | The three are not the same law in the limit where they should be, so at least one is implemented wrongly |
| **4** | **Timestep convergence**: restitution changes by < 0.5 % between h and h/2 at the selected step | The verification is reading its own integrator |
| **5** | **Contact-force convergence**: peak force changes by < 1 % between h and h/2 | Same, for the quantity the structural case depends on |
| **6** | **Model-form spread on the VOLLEY case ≤ 25 %** — exit angular rate at A67's nominal point, computed under all three laws | **The 14.845 °/s is model form, not physics**, and A67's headline must be restated as a range rather than a number. *This band may fail and failing is the result* |
| **7** | **Energy closes to 0.5 %** under each law | Report-only for LN, which A67 already passed; a new law that does not close energy is not a candidate |

## What this run does not do

**It does not change A67's recorded verdict**, re-declare A67's bands, or model VOLLEY's bore.
It does not calibrate against hardware — **E4**. It does not choose the design's restitution: 0.7
remains `cradle_restitution.E_ALUMINIUM`, the published top of the aluminium range.
