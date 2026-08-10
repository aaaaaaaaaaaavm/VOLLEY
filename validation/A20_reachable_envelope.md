# A20: what a last-mile delivery vehicle can actually reach, against a host Δv budget

**Closes:** nothing. **Quantifies** the ConOps adopted in **ADR-024**, and advances **PII-6**
(reachable-domain analysis), deferred since 2026-07-31.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/reachable_envelope.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> The script is absent at this commit and that absence is checkable.

## The question

`docs/CONCEPT.md` claims that a spent stage carrying VOLLEY can reposition between altitude
shells on its own reaction-control system and deliver satellites to each. **That claim has a
budget in it that nobody has stated**, because POEM-class propellant and control authority are
undisclosed (**E5**).

So the analysis is parametric in the one number that is missing: **given a host Δv budget, what
set of orbits can twelve satellites be placed into?**

## What is being combined

Three mechanisms, and they are not interchangeable:

| Mechanism | Who pays | What it produces |
|---|---|---|
| **Host repositioning** | host RCS propellant | altitude shells |
| **VOLLEY's shot** | host electrical power, 2.56 kJ net | along-track velocity difference, per satellite |
| **Differential J2** | nobody — it is free | RAAN separation, over the campaign |

**Plane change is excluded** and the sheet does not report it as reachable at any budget. A15
band 8 established 133 m/s per degree; a stage with 200 m/s of RCS could buy 1.5° of inclination
and would have nothing left to reposition with. That trade is computed and reported **so the
exclusion is demonstrated rather than asserted**.

## Method

- Host Δv budget swept over **{0, 25, 50, 100, 200, 400} m/s**.
- Repositioning by **two-burn Hohmann transfer** between circular shells; cost per shell change
  computed, not assumed.
- At each shell, twelve shots at commanded velocities across VOLLEY's range, using
  `astro.boosted_elements` — imported, not restated.
- RAAN spread from differential nodal regression over a stated campaign duration, using
  `astro.py`'s own J2 rate.
- Orbital constants and the atmosphere model come from `analysis/astro.py` by import. The
  operating point comes from `motor_results.json`.

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **Δv to change altitude shell by 50 km**, two-burn Hohmann at 450 km | **10–20 m/s** | if it falls outside, the textbook Hohmann relation is not being computed correctly; suspect the script before the physics |
| 2 | **Shells reachable at a 100 m/s host budget**, 50 km apart | **≥ 4** | below this the hosted configuration is barely a delivery vehicle and the ConOps in ADR-024 is overstated |
| 3 | **Altitude extent of the delivered fleet at 100 m/s**, highest apogee minus lowest perigee | **≥ 250 km** | the whole point of repositioning is that it beats what one shot's ±59 km can do; below 250 km it does not earn the propellant |
| 4 | **Inclination reachable at 400 m/s**, spending the entire budget on plane change | **≤ 3.5°** | tests the exclusion. A larger figure would mean plane change is cheaper than A15 band 8 established and one of the two is wrong |
| 5 | **RAAN spread over the campaign at zero host budget** | **≥ 5°** | the free mechanism must still work with no propellant at all, or the dedicated configuration has no distribution story |
| 6 | **Fraction of the delivery envelope attributable to the host rather than to VOLLEY**, at 100 m/s | **report**; no pass/fail | if the host does most of the work, VOLLEY is a release mechanism on a transfer vehicle, and that should be said plainly rather than discovered by a reviewer |

### Band 6 is the uncomfortable one and it is declared deliberately

**If a 100 m/s host budget dominates the reachable envelope, then the product is the stage and
VOLLEY is its dispenser.** That would not invalidate the machine, but it would change what the
project is selling, and it is exactly the kind of result that is easy to leave uncomputed.

It is declared as **report** rather than pass/fail because there is no defensible threshold — the
honest output is the ratio itself.

### Band 2 and band 3 are the ones that carry ADR-024

If either fails, the hosted configuration is not a delivery vehicle in any meaningful sense and
`docs/CONCEPT.md` must be rewritten to say so. **A miss is a P-item, not a widened band.**

## What happens at each outcome, fixed now

1. **Band 1 fails.** Arithmetic error. Stop and fix before reading anything else.
2. **Band 2 or 3 fails.** The hosted ConOps narrows to single-shell delivery with the dedicated
   configuration as the only multi-orbit route. ADR-024 gains an amendment; `CONCEPT.md` §3.1 is
   corrected.
3. **Band 4 fails.** A15 band 8 and this analysis disagree about plane change. Suspect this
   script first, since A15's figure was confirmed twice.
4. **Band 5 fails.** The free mechanism does not work at the campaign duration assumed, and the
   RAAN claim in `CONCEPT.md` §4 must be withdrawn.
5. **Band 6 shows the host dominating.** Say so, in `CONCEPT.md` and in `MARKET.md`, in the same
   sentence as the claim it qualifies.

**No band may be widened after the run.**

## Provenance

**This analysis is parametric in the host Δv budget and cannot be otherwise**, because no
POEM-class accommodation figure is public. Every number it produces is conditional on a budget
that E5 would supply. That conditionality is the result, not a caveat on it.

Nothing here is measured. The repositioning manoeuvres are two-burn impulsive transfers with no
attitude profile, no finite-burn losses, no thermal case for a loitering stage, and no propellant
margin. **A stage that must hold attitude and thermal control for a multi-week campaign is a
problem this project has not modelled at all**, and it is named here rather than left out.
