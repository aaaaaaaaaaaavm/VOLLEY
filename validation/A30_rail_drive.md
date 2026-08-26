# A30: can an induction drive couple to what the satellite already has?

Entry criterion for [PII-16](../docs/VAULT.md) and the whole of
[`../docs/GEN6_RAIL_DRIVE.md`](../docs/GEN6_RAIL_DRIVE.md).

`analysis/rail_drive.py` sizes a linear induction drive coupling to the CubeSat Design
Specification's four aluminium corner rails, and it clears the thrust requirement, but only
because it assumes a transverse edge-effect derating of 0.55, which the file declares at the
top as its dominant assumption and the proposal names as the thing that would kill it.

This sheet is that assumption, tested.

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/edge_effect.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/edge_effect.py`, which returns nothing.

## Result, 2026-08-13: the rail is 22x too narrow, and the drive is fine

`analysis/edge_effect.py`, bands committed at `7df75ac` before it existed. Results in
`analysis/results/edge_effect.json`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | CDS rail edge factor ≥ 0.35 | **0.0253** | **FAIL** |
| 2 | numeric agrees with Russell–Norsworthy within 25 % | **+1.0 %** | **PASS** |
| 3 | rails make ≥ 413 N at ≤ 0.60 T | **41.9 N** | **FAIL** |
| 4 | 90 mm plate edge factor ≥ 0.55 | **0.6691** | **PASS** |
| 5 | that plate weighs < 0.5 kg | **0.248 kg** | **PASS** |

### Band 1 — PII-16 is rejected

`analysis/rail_drive.py` assumed 0.55. The answer is 0.0253, a factor of 22 out.

| | |
|---|---:|
| Edge factor, 8.5 mm CDS rail at a 48 mm pole pitch | **0.0253** |
| Assumed by the sizing that made the proposal look viable | 0.55 |
| Thrust on four rails at **0.60 T** — a high flux density, chosen to be generous | **41.9 N** |
| Thrust required to reproduce Gen5's 10.5 g on a 3U | 413 N |
| **Short by** | **a factor of 10** |

The entry criterion for PII-16 is not met and the architecture is rejected. No pole pitch
rescues it, and the reason is a contradiction rather than a shortfall: the edge factor wants the
secondary wide compared with the pole pitch, and the airgap wants the pole pitch large
compared with the gap. With an 8.5 mm conductor and a ~10.5 mm effective magnetic gap, those
two demand τ ≪ 8.5 mm and τ ≫ 10.5 mm at the same time. There is no design point between
them.

For c ≪ τ the factor collapses as (πc/τ)²/3, with the square of the width-to-pole-pitch
ratio. A narrow secondary is not slightly worse. It is quadratically worse.

### Band 2 caught a bug in this analysis, which is why it was declared

The first run of `edge_effect.py` returned an edge factor of 0.0000 for every geometry,
including the 90 mm plate, which Russell, Norsworthy puts at 0.66. A number that is zero for a
case known to couple well is not a small answer, it is a wrong one.

The cause: the imposed field was written as a real `cos(kx)`. That makes the stream function 90°
out of phase with it, so the time-average thrust `⟨K_y·B_n⟩` integrates to exactly zero for
every width. The travelling wave has to be carried as a spatial phasor `B e^{−jkx}`, with
thrust `½ Re{K_y · conj(B_n)}`. With the phasor restored the solver agrees with the closed form
to 1.0 %.

**This is the fourth time a declared band has caught a bug in the analysis rather than a problem
in the design, after A19, A20 and A2. It is also the second time in this repository that a
solver has returned identically zero, converged cleanly, and reported success; the first was the
3-D magnetostatic solve in `validation/fem3d/`.

**What band 2 does and does not check.** The numerical solve discretises the same
boundary-value problem Russell & Norsworthy solved in closed form, so agreement validates the
discretisation, not the physics. It is not an independent physical method, and it is not
offered as one.

### Bands 4 and 5 — the drive is sound; the rail is the wrong conductor

**This distinction is the entire value of having declared band 4 in advance**, and it is why a
failure here produces a direction rather than only a rejection.

| 90 mm flat plate, 3 mm thick, inside a 3U's own 100 mm section | |
|---|---:|
| Edge factor at a 48 mm pole pitch | **0.6691** — 26× the rail |
| Thrust at only **0.45 T** over 306 cm² | ~~1652 N~~ → **378 N**, corrected by A31 (**P50**) |
| Against the 413 N requirement | **short at 0.45 T; closes at 0.60–0.75 T** — A31's sweep |
| Mass | **0.248 kg** |
| A COTS 3U cold-gas module delivering the same Δv | 0.5–1.2 kg |

A quarter-kilogram of plain aluminium beats the lightest propulsion module on the market by
2x. The thrust figure quoted here took the magnetic-pressure ceiling and applied the edge
factor; A31's layered solve puts it at 378 N, a factor of 4.4 lower, and the design closes at
0.60-0.75 T rather than 0.45 T. Corrected as P50; the edge factor itself is unaffected. The linear induction drive, no sled, no
brake, no arrest section, no cradle, is intact. What fails is the belief that an interface which
already exists happened to be the right shape.

**Band 5 is the design rule that matters more than any of the thrust numbers.** An interface the
customer must carry is worth carrying only if it costs them less than the propulsion module it
replaces. At 0.248 kg it does, by a factor of two to five.

---

## The physics being tested, stated precisely

A linear induction motor makes thrust from transverse current induced in its secondary. In a
wide sheet that current crosses under the pole and returns longitudinally, roughly a pole pitch
away, so the return path is cheap. In a secondary narrower than the pole pitch, the useful
transverse leg is short and the return legs are long, so the loop is dominated by resistance
that produces no thrust.

The transverse edge factor is the ratio of the thrust a finite-width secondary produces to
the thrust an infinitely wide one of the same conductance would produce under the same imposed
field. It is a purely geometric penalty, and the CDS rail is 8.5 mm wide against a pole pitch
of 36-48 mm.

## Acceptance bands

**Band 1 can fail, and if it does the proposal is rejected rather than re-scoped.** That is the
point of running it first and the reason PII-16 was logged as a proposal rather than adopted.

### Band 1 — the transverse edge factor on a CDS corner rail

Quantity: thrust on the real 8.5 mm rail geometry divided by thrust on an infinitely wide
secondary of identical sheet conductance, identical imposed travelling field, identical pole
pitch and identical slip. Dimensionless, in [0, 1].

**Band: ≥ 0.35.**

`rail_drive.py` assumes 0.55. `GEN6_RAIL_DRIVE.md` states that at 0.20 the design point falls to
187 N and the idea is dead. 0.35 is the midpoint of the range the proposal itself named as the
live/dead boundary, and it is set here before the answer is known.

**FAIL below 0.35.** A failure is not a reason to lower the band, change the pole pitch until the
band passes, or re-scope the claim. It is a rejected architecture, and the entry criterion for
PII-16 is not met.

### Band 2 — an independent check on band 1

**Band: the numerical result agrees with the Russell–Norsworthy closed-form transverse edge
factor to within 25 %, evaluated at the same width-to-pole-pitch ratio.

Russell and Norsworthy's 1958 result is the standard closed form for exactly this geometry. A
numerical answer that disagrees with it materially is a broken solver, not a discovery, this is
the same reasoning as A2 band 1, which caught a 57 % error in a new integral before the headline
was read off it.

### Band 3 — the consequence, at an achievable flux density

**Band: at the edge factor band 1 measures, with airgap clearance 2.0 mm and airgap flux density
no greater than 0.60 T, the drive produces >= 413 N on a 3U, the thrust Gen5 delivers, and
therefore the minimum at which Gen6 is not a downgrade.

**This band may fail even if band 1 passes**, because band 1 is a ratio and this is a force.

### Band 4 — is there a secondary geometry that does work

Quantity: the same edge factor, computed for a flat plate secondary of width 90 mm, the
widest that fits inside a 3U's 100 mm section, at the same pole pitch.

**Band: ≥ 0.55.**

This band exists so that a band 1 failure produces a *direction* rather than only a rejection.
The edge factor rises with width, and the question a failure immediately raises is how wide a
secondary has to be before an induction drive is worth building. **If band 1 fails and band 4
passes, the conclusion is that the drive is sound and the CDS rail is the wrong conductor,
which is a different finding from the drive being unsound, and the two must not be confused.

### Band 5 — and what such a plate would cost the customer

**Band: a plate meeting band 4, sized to carry the thrust of band 3, has a mass below 0.5 kg** —
the lower bound of the COTS cold-gas module range the mass-per-satellite kill criterion measures
against.

This is the design rule the whole payload-interface question turns on: an interface the
customer must carry is only worth carrying if it costs less than the propulsion module it
replaces. Below 0.5 kg it does. Above 1.2 kg it does not, at any performance.

## What this cannot settle

- **The reaction field is not modelled.** Band 1 measures the *geometric* edge factor in the
  thin-sheet quasi-static limit, which is how the transverse edge effect is defined and how
  Russell, Norsworthy derive it. The secondary's own field distorting the airgap flux is a
  separate penalty, in the same direction, and is not included. The result is therefore an
  upper bound on the coupling**, which is the conservative direction for a band that can reject.
- No end effect. The longitudinal entry and exit effects of a short primary are not modelled
  and are a further loss.
- Nothing is measured. E4 stands. This is a computation about a machine that does not
  exist, coupling to a rail nobody has instrumented.
