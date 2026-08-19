# A50 — how long the campaign can last, and what altitude it costs

**Bands declared 2026-08-16, before `analysis/campaign_altitude.py` existed.**
Verify with `git show --stat <this commit> -- analysis/campaign_altitude.py`, which must return nothing.

---

## Why this run exists

**Asked directly: the stage should be able to deploy on arrival, *or* stay up for days, weeks or
months and deliver satellites into different orbits as it moves.**

**[E28](../OPEN_PROBLEMS.md) is live and it is exactly this question**, found by accident when two
GMAT runs stopped early:

> *"R2 (350 km, 55.2 deg) and R3 (350 km, 9.6 deg) never reached the declared 90 days: their twelve
> satellites **reentered**, R2 halting at **36 days** with all twelve between 182 and 190 km, R3 at
> **29 days** between 103 and 115 km. Only the 450 km case ran the full 90."*
>
> *"Nothing in this project models campaign mission life … The deployment story — twelve satellites,
> spread in altitude and plane — has always been told without saying how long the fleet exists."*
>
> *"**the plane spread this project is pleased about develops faster there** … **because the same
> drag that separates the nodes is what pulls the satellites down.** The two are not independent
> effects to be traded; they are the same effect."*

**So "a couple of days, weeks or months" is not a free parameter.** It is bought with altitude, and
altitude is bought with propellant the stage may not have.

## Method

**Imported, not restated.** `astro.lifetime` for decay, `reachable_envelope.hohmann_dv` and
`raan_spread_deg` for repositioning and nodal drift. This run adds the coupling between them.

**Two lifetimes are computed, not one.** The **satellites'**, which decides whether a delivery is
worth making, and the **stage's**, which decides whether a later delivery can be made at all. They
have different ballistic coefficients and the stage's is a **declared input**, named in the script,
because no stage mass or area is public — that is **E5**.

**A campaign is scored on satellites still alive at the end**, not on satellites deployed. A
satellite released into an orbit that decays before the campaign finishes was not delivered.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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
   **365° of spread in 29–36 days at 350 km against 367° in 90 days at 450 km** — *both are
   essentially a full revolution.* If spread saturates at 360° regardless, **the plane spread is
   not a constraint at all and the whole trade collapses to satellite survival**, which would make
   the design rule simply *go higher*.
4. **Band 7 passes**, since a 50 km Hohmann leg at LEO is order 14 m/s and A20 swept to 400.
5. **Band 8 will report an altitude the stage can reach but a campaign nobody will pay for**, since
   the constraint becomes stage keep-alive rather than orbital mechanics.

## Result

*Not yet run.*
