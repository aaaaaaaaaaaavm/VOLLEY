# A70 — guided contact, on a derived centreline and a verified contact law

**This is a re-run of [A67](A67_guided_contact.md) with two inputs replaced.** A67's bands are not
re-declared and its verdict stands. **These bands are declared before this re-run, and the code
change that makes the re-run possible is committed after them.**

> ## BANDS DECLARED 2026-08-22, BEFORE THE CENTRELINE COUPLING EXISTS.
>
> `analysis/guided_contact.py` exists — it is A67's model. **What does not exist at this commit is
> the coupling that lets it consume [A69](A69_tube_centreline.md)'s centreline**, and that is what
> these bands are declared ahead of. Verify with `git log -1 --format=%H` against the commit that
> adds `bore_from_a69` to that file.

## What changed since A67, and why each change is allowed

| | A67 | **A70** |
|---|---|---|
| **Contact law** | Lankarani–Nikravesh. **A67 band 3 failed**: +13.7 % restitution error at the nominal coefficient, +128 % at 0.3 | **[A68](A68_contact_law.md)'s selection.** LN's error vanishes as e → 1, which is its documented domain limit, and a formulation that does not assume it recovers the coefficient it is given |
| **Bore centreline** | a sinusoid of **declared** amplitude, 0.1–2.0 mm, at twice the support pitch | **[A69](A69_tube_centreline.md)'s computed shape** — the deflected curve of the actual section on its actual supports, with the contributions solved separately |

**Neither replaces a band. Both replace an input**, and A67 is what says they had to be replaced:
its band 3 failure named the law and its band 9 result named the centreline as the dominant
sensitivity at S_T = 0.894.

## Acceptance bands

**Six bands. Bands 2, 3 and 5 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **The coupling is exact.** With A69's shape scaled to zero, the model reproduces A67's zero-straightness case to **0.5 %** on exit velocity | The centreline plumbing changed something it should not have |
| **2** | **Exit angular rate at the orbital centreline ≤ 2.0 °/s** | Gen6 still misses tip-off with a derived shape and a verified law, and **[P108](../OPEN_PROBLEMS.md) survives every objection raised against A67** |
| **3** | **3σ over A69's orbital range ≤ 2.0 °/s** | Same, under the tolerance the structural model actually produces rather than an assumed bracket |
| **4** | **Peak contact normal force ≤ 445.88 N** at the orbital centreline | The guide carries more than the drive pushes with |
| **5** | **The A67 → A70 change in exit angular rate is ≤ 50 %** | The two runs disagree about the machine by more than model form should account for, and the earlier headline must be withdrawn rather than refined |
| **6** | **Energy closes to 0.5 %** | Report-only; the same closure A67 passed |

## What this run does not do

**It does not calibrate against hardware** — **E4**. **It does not model manufacturing
straightness**: A69 computes the *deflected* shape and declares manufacturing tolerance
separately, and what an 8 m bore can actually hold is [`MANUFACTURING.md`](../docs/MANUFACTURING.md)'s
to establish. It does not redesign anything: **no support pitch, land separation, clearance or
bore is changed to make a band pass.**
