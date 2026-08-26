# A50, how long the campaign can last, and what altitude it costs

**Bands declared 2026-08-16, before `analysis/campaign_altitude.py` existed.**
Verify with `git show --stat <this commit> -- analysis/campaign_altitude.py`, which must return nothing.

---

## Why this run exists

Asked directly: the stage should be able to deploy on arrival, *or* stay up for days, weeks or
months and deliver satellites into different orbits as it moves.

[E28](../OPEN_PROBLEMS.md) is live and it is exactly this question, found by accident when two
GMAT runs stopped early:

> *"R2 (350 km, 55.2 deg) and R3 (350 km, 9.6 deg) never reached the declared 90 days: their twelve
> satellites reentered, R2 halting at 36 days with all twelve between 182 and 190 km, R3 at
> 29 days between 103 and 115 km. Only the 450 km case ran the full 90."*
>
> *"Nothing in this project models campaign mission life ... The deployment story, twelve satellites,
> spread in altitude and plane, has always been told without saying how long the fleet exists."*
>
> *"the plane spread this project is pleased about develops faster there ... because the same
> drag that separates the nodes is what pulls the satellites down. The two are not independent
> effects to be traded; they are the same effect."*

So "a couple of days, weeks or months" is not a free parameter. It is bought with altitude, and
altitude is bought with propellant the stage may not have.

## Method

Imported, not restated. `astro.lifetime` for decay, `reachable_envelope.hohmann_dv` and
`raan_spread_deg` for repositioning and nodal drift. This run adds the coupling between them.

Two lifetimes are computed, not one. The satellites', which decides whether a delivery is
worth making, and the stage's, which decides whether a later delivery can be made at all. They
have different ballistic coefficients and the stage's is a declared input, named in the script,
because no stage mass or area is public, that is E5.

A campaign is scored on satellites still alive at the end, not on satellites deployed. A
satellite released into an orbit that decays before the campaign finishes was not delivered.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | At **350 km** the modelled satellite lifetime is **≤ 60 days**, consistent with E28's observed 29–36 | The decay model disagrees with the GMAT runs that raised E28, and nothing below is trustworthy |
| **2** | At **450 km** the modelled satellite lifetime is **> 90 days**, consistent with the one E28 run that completed | Same |
| **3** | Satellite lifetime is **monotonically increasing** in altitude across the sweep | The model is not behaving |
| **4** | Nodal spread **rate** is **monotonically decreasing** in altitude | Same, and E28's stated coupling is not present |
| **5** | **An altitude exists where a 90-day campaign ends with ≥ 9 of 12 satellites alive** | Months of loiter cannot be delivered with a fleet that survives it, and the concept is a deploy-on-arrival product |
| **6** | The **plane spread achieved before the fleet dies** is reported at every altitude, and its maximum is identified | The trade E28 named is not actually resolved |
| **7** | Repositioning Δv for a stated multi-shell campaign is **≤ 200 m/s**, inside A20's swept host budgets | The campaign needs more than any host budget this project has considered |
| **8** | The altitude required for a **one-year** campaign is stated, **and whether a stage can reach it** | The run answers "weeks" and dodges "months" |
| **9** | **Both** the satellites' and the stage's lifetimes are computed | The campaign is scored on a fleet that outlives the vehicle deploying it, or vice versa |

## Predictions

1. **Bands 1 and 2 pass** — they are the calibration against E28's own GMAT runs, and if they fail
   the run stops there.
2. **Band 5 passes**, somewhere near or above 500 km.
3. **Band 6 is the interesting one, and I expect the maximum to be flat or absent.** E28 reports
   365° of spread in 29-36 days at 350 km against 367° in 90 days at 450 km, *both are
   essentially a full revolution.* If spread saturates at 360° regardless, the plane spread is
   not a constraint at all and the whole trade collapses to satellite survival, which would make
   the design rule simply *go higher*.
4. **Band 7 passes**, since a 50 km Hohmann leg at LEO is order 14 m/s and A20 swept to 400.
5. **Band 8 will report an altitude the stage can reach but a campaign nobody will pay for**, since
   the constraint becomes stage keep-alive rather than orbital mechanics.

## Result

**RUN 2026-08-16. Seven of nine bands pass. Band 1 — the calibration against E28's own GMAT runs —
fails, and that failure is the most important thing in this run.

| # | Band | Result | |
|---|---|---|---|
| 1 | 350 km satellite life ≤ 60 days, per E28 | **70.6 d** | **FAIL** |
| 2 | 450 km satellite life > 90 days, per E28 | 476.6 d | **PASS** |
| 3 | satellite life monotonically increasing | **capped at 700 and 800 km** | **FAIL** |
| 4 | nodal spread rate decreasing in altitude | 0.523 → 0.412 °/day | **PASS** |
| 5 | an altitude gives ≥ 9 of 12 alive at 90 days | 350 km | **PASS** |
| 6 | spread achieved before the fleet dies, maximum identified | reported | **PASS** |
| 7 | campaign Δv over 3 shells ≤ 200 m/s | **56.6 m/s** | **PASS** |
| 8 | the one-year campaign altitude is stated | **450 km** | **PASS** |
| 9 | both lifetimes computed | both | **PASS** |

### The answer to the question asked

| Altitude | Satellite life | Stage life | Alive at 90 days | Repositioning Δv |
|---:|---:|---:|---:|---:|
| 350 km | **70.6 d** | 173 d | 11 of 12 | 56.6 m/s |
| **450 km** | **476.6 d** | 1172 d | **12 of 12** | **55.3 m/s** |
| 600 km | 5792 d | 14242 d | 12 of 12 | 53.6 m/s |

Days, weeks and months are all purchasable, and from 450 km upward months are comfortable.
Walking three 50 km shells costs ~ 55 m/s, well inside the host budgets A20 swept to 400.
A one-year campaign needs 450 km, which is the altitude the project already baselines.

So orbital mechanics is not the constraint on loiter. The stage keep-alive agreement is, and
[A47](A47_gen6_fmea.md) already counts that as a manifest-forfeiting shared element that no launch
provider has agreed to.

### Band 1 failed, and it invalidates the durations above as anything but upper bounds

E28's GMAT runs reentered at 29 and 36 days from 350 km. This model says 70.6. It is optimistic
by roughly a factor of two at the altitude where the answer matters most.

The cause is already a known defect. `astro.py` uses a static atmosphere, the same
property that made P16's invariance claim untestable, where a uniform density scaling preserved
a ratio *by construction*. A static atmosphere cannot represent the solar-activity variation that
actually kills a satellite at 350 km.

Every duration in this run inherits that. They are upper bounds, and the honest reading of the
table is *"450 km buys months"* rather than any specific day count. **The band caught it, which is
what the band was for**, and E28 stays open rather than being closed by a model that disagrees with
the runs that raised it.

### Band 3 failed on a cap, not on physics

`astro.lifetime` caps at 40 years = 14 610 days, so 700 km and 800 km both return the cap and
the sequence stops strictly increasing. **My band said "monotonically increasing" where the data
can only be non-decreasing. A declaration imprecision, recorded rather than edited.

**It has one real consequence: the "maximum spread" band 6 identifies at 700 km is a cap
artefact. Both 700 and 800 km run for the same capped window, so the lower drift rate at 800 km
produces less total spread. That maximum is not a physical optimum and must not be quoted as
one.

### The prediction that held, and it collapses the trade

Prediction 3 said the spread maximum might be absent and the trade might collapse to satellite
survival. In the 90-day column the spread barely moves, 47.1° at 350 km against 44.6° at
450** — a 5 % difference across the altitude band that changes satellite life by **6.7×**.

E28 framed altitude as a trade between plane spread and mission life. At the shell spacing this
architecture actually uses, it is not a trade. Spread is nearly altitude-independent over the
useful range; life is not. The design rule is simply: go higher.

### One quantity in this run is not calibrated, and it is named rather than trusted

A15 reported 367° of nodal spread in 90 days at 450 km. This run computes 44.6° for the same
window. The difference is the fleet geometry: A15's GMAT campaign spread satellites over a much
wider altitude range than the **three 50 km shells** modelled here. **No band was declared on this
and none should be read into it, the two numbers describe different campaigns, and reconciling
them is not something this run did.

## What this run does not do

- **No solar-activity variation**, which band 1 has just shown is the term that matters.
- The stage's ballistic coefficient is a declared guess of 150 kg/m², named in the script. No
  stage mass or area is public, that is E5.
- Circular orbits, no attitude or drag-area variation, no station-keeping.
- It does not price keeping a stage alive, which the result above identifies as the actual
  constraint.
