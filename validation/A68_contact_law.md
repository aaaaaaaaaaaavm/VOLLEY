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

---

## Results

**RUN 2026-08-22. Six of seven. Band 6 fails and it is the result.**

`analysis/contact_laws.py` and `analysis/run_a68.py`. Results in `analysis/results/contact_laws.json`.

| # | Band | Result | |
|---|---|---|---|
| 1 | ID recovers restitution to 0.5 % | **worst 0.000 %** | **PASS** |
| 2 | HC beats LN at every e below 0.7 | LN worst **236.1 %**, HC worst **17.2 %** | **PASS** |
| 3 | all three agree within 2 % as e → 0.9 | LN 0.9132, HC 0.8999, ID 0.9000 | **PASS** |
| 4 | restitution converges, 0.5 % between h and h/2 | 0.700000 → 0.700000 | **PASS** |
| 5 | peak force converges, 1 % between h and h/2 | 41 283.53 → 41 283.53 N | **PASS** |
| 6 | **model-form spread on the VOLLEY case ≤ 25 %** | **65.8 %** — 8.954 to 14.845 °/s | **FAIL** |
| 7 | energy closes to 0.5 % under each law | worst **+0.3221 %** | **PASS** |

### A67's diagnosis was right, and band 2 is how it was tested

**The restitution error vanishes as e → 1**, which is the signature of Lankarani–Nikravesh's own
derivation and not of an implementation error:

| Declared e | **LN** | **HC** | **ID** |
|---:|---:|---:|---:|
| 0.9 | +1.5 % | −0.0 % | 0.00 % |
| 0.7 — the nominal aluminium figure | **+13.7 %** | **−0.4 %** | 0.00 % |
| 0.3 | **+128.1 %** | −9.8 % | 0.00 % |
| 0.2 | **+236.1 %** | −17.2 % | 0.00 % |

**HC is the formulation this project should have been using**, and identification recovers the
coefficient exactly at every restitution and impact velocity tested. *ID's χ at the nominal
restitution is **0.6348**, against LN's 0.3825 and HC's 0.6429 — LN under-damps by 40 %.*

### Band 6 fails, and it is what A67's headline needed

**The same VOLLEY case, the same geometry, the same everything except the damping term:**

| Law | Exit angular rate | Peak contact | Contacts |
|---|---:|---:|---:|
| **LN — what A67 used** | **14.845 °/s** | 225.8 N | 39 |
| **HC** | **8.954 °/s** | 298.3 N | 25 |

**65.8 % spread.** **So A67's 14.845 °/s is substantially model form, and the band declared to
catch that caught it.** *The correct statement of A67's result is a range with a model-form
component, not a number.*

> **What does not move.** **Both laws put the exit angular rate far above the 2.0 °/s band** — 4.5×
> at the friendlier one. **The finding survives the model-form uncertainty; the precision of the
> figure does not**, and [P108](../OPEN_PROBLEMS.md) is restated accordingly rather than withdrawn.

---

> ## CORRECTION 2026-08-22, later the same day — **P111**. The damping relation was misattributed.
>
> **The results above are kept and one of their labels is wrong.**
>
> **What this run called *"Hunt–Crossley's own coefficient"* — `χ = 3(1−e)/(2e)` — is not
> Hunt–Crossley's.** Hunt & Crossley (1975), *Coefficient of restitution interpreted as damping in
> vibroimpact*, J. Appl. Mech. **42**(2), give the hysteresis damping factor to first order in
> (1−e) as **λ = 3k(1−e)/(2v⁻)**, i.e. **χ = 3(1−e)/2 — with no `e` in the denominator.**
> Relations carrying `e` in the denominator belong to the **later corrected family**, and the
> constant used here is 3/2.
>
> **The primary sources for that later family have not been read** — publisher records were not
> retrievable — so the implementation is now named **`MOD`, for its form, and not for an author.**
> *A68 as first published attached an author's name to a formula that author did not write, and
> then reasoned from the attribution.*
>
> ### And the reasoning that rested on it was wrong
>
> A68 claimed HC *"does not assume e → 1"*. **It does.** Both are first-order-in-(1−e) relations
> and both degrade the same way:
>
> | Declared e | **LN** | **HC — actual** | **MOD** | **ID** |
> |---:|---:|---:|---:|---:|
> | 0.9 | +1.5 % | **+1.0 %** | −0.0 % | 0.000 % |
> | 0.7 | +13.7 % | **+9.7 %** | −0.4 % | 0.000 % |
> | 0.5 | +45.0 % | **+32.6 %** | −2.5 % | 0.000 % |
> | 0.3 | +128.1 % | **+93.8 %** | −9.8 % | 0.000 % |
> | 0.2 | +236.1 % | **+173.4 %** | −17.2 % | 0.000 % |
>
> **Band 2 as declared still passes** — HC's error is below LN's at every e under 0.7 — **but it
> passes for a different reason than the run sheet gave.** The formulation that actually holds at
> low restitution is the `(1−e)/e` family, and calling it Hunt–Crossley concealed that.
>
> ### The identification is not validation, and now there is something that is
>
> **`ID` root-finds χ using the same fixed-step RK4 solver until that solver returns the requested
> e. That cannot validate the solver** — it is parameter identification, and A68 presented it as
> if it were verification.
>
> **An independent integrator has been added.** `impact_ivp()` solves the same impact with
> **scipy's adaptive implicit Radau**, at `rtol = 1e-11`, with an event-terminated separation —
> a different code path, order, step control and stiffness treatment. **At every identified χ it
> agrees with the RK4 result to 0.000 %.** *That is the verification; the identification is not.*
>
> ### The VOLLEY model-form spread, with all three correctly named
>
> | Law | Exit angular rate | Peak contact | Contacts |
> |---|---:|---:|---:|
> | **LN** | 14.845 °/s | 225.8 N | 39 |
> | **HC — actual** | **12.390 °/s** | 277.1 N | 36 |
> | **MOD** | 8.954 °/s | 298.3 N | 25 |
>
> **Band 6's 65.8 % spread is unchanged**, because the extremes are unchanged. **What changes is
> that the spread is now across three sourced formulations rather than two, one of them
> misnamed.** *The band still fails and the failure still means the magnitude is unresolved.*
