# What only a human can do

Written 2026-08-22. Everything here is blocked on something that is not another analysis.
If an item's honest next step is *model it*, *simulate it*, *compute it* or *select it from public
data*, it belongs in [`COMPUTATIONAL_CLOSURE.md`](COMPUTATIONAL_CLOSURE.md) instead, that file
carries 17 such items and this one carries none.

---

## Physical measurement

| | Entry | Prerequisite | Deliverable | Feeds back into |
|---|---|---|---|---|
| Seal friction | [P67](../OPEN_PROBLEMS.md) | [`B2_ORDER.md`](B2_ORDER.md), bands 1-14 already declared, including bands 13 and 14 which make the rig measure the seal rather than the assembly | Breakaway and running friction, three units, >=10 pulls each, with the matched-tare difference and its 3σ spread | `gen6_seal.friction_max_N`; decides ADR-036 and whether the trim stage returns |
| Seal thermal survival | [P88](../OPEN_PROBLEMS.md) | P67 first | Conduction path measured at representative ΔT | A58's 50 K limit |
| Nothing has been built | [E4](../OPEN_PROBLEMS.md) |, | Any measured quantity at all | Every figure in the repository is a model output until this moves |
| Bore straightness, roundness, cylindricity | P103 / A69 | An 8 m tube exists | As-built centreline over 8 m | A69's declared straightness input, currently a bracket |
| Contact stiffness and damping | P103 / A71 | A guided-ejection article | Identified contact parameters | A71's penalty stiffness, currently a numerical parameter |
| Structural damping | P36 | Hardware | Measured modal damping | A59, A69 |

## Procurement and machining

| | Entry | Deliverable |
|---|---|---|
| B-2 rig: ISO 6432 cylinder x3, logging load cell >=500 Hz | P67 | ₹8,000-26,000, all estimated, nothing quoted |
| B-1 rig: gaussmeter + magnets | D1 / E4 | ₹22,000-52,000 |
| An 8 m honed and hard-anodised bore | P103 | The single largest manufacturing question, and `MANUFACTURING.md` is still a Gen5 document |
| Pressure vessels, chamber and reservoir | P91 | No vessel calculation exists; see the build package §9 |

## Laboratory testing

Proof and burst, leak rate, pressure-cycle life, seal wear, valve life, guided ejection ·
payload acceleration and tip-off, interface SRS and shock, random vibration, sine ·
thermal vacuum, low-temperature operation, contamination and outgassing measurement ·
EMC if the trim stage returns, magnetic cleanliness if magnets return, multi-shot campaign
reliability. None of these is scheduled and [`QUALIFICATION_PLAN.md`](QUALIFICATION_PLAN.md) is
still Gen5's.

## Launch-provider data

| | Entry | Why a human is required |
|---|---|---|
| Stage propellant reserve, Isp, restart count and constraints | [E5](../OPEN_PROBLEMS.md) | Not public. One conversation replaces a parametric sweep |
| Host control authority | [P94](../OPEN_PROBLEMS.md) | A13 band 5 passed on an authority E5 says does not exist |
| A real host reaction wheel, or a host that needs none | [P99](../OPEN_PROBLEMS.md) | One shot's angular momentum exceeds the only wheel ever named |
| What a provider will actually credit against the stage | [P68](../OPEN_PROBLEMS.md) | 58.6 % of the Gen6 mass case rests on it |
| Launch-interface compliance position | [E31](../OPEN_PROBLEMS.md) |, |
| Mechanical interface, envelope, mounting |, | Build package §7, `HOST_DEPENDENT` |

## Flight and operations

| | Entry |
|---|---|
| Published dispenser deployment counts and failure records | [E30](../OPEN_PROBLEMS.md), the required *r* is computed at 0.99326; what it *is* needs operational history |
| Femtosat deployer masses actually flown | [P44](../OPEN_PROBLEMS.md) |
| Actual conjunction screening | E18's covariance is computable; screening is operational |
| Flight demonstration | E4 |

## Expert review, safety approval, integration

Independent technical review of the manuscript, range-safety and pressure-system approval ·
launch-provider safety review, flight integration. No result here has been reviewed by a third
party.

## Human design decisions no analysis settles

| | Entry |
|---|---|
| D2, which payload class is the product | [`D2_DECISION.md`](D2_DECISION.md) writes both cases; the decision is the author's |
| The enclosure panel | 50.04 vs 29.98 kg; closes no criterion at any class |
| D1, D5, D8, D10 | Order B-1, file a US provisional, keep Gen4 or not, fund it or scope it |
| Whether "final" means frozen-with-exceptions | [`STATE_OF_THE_PROJECT.md`](STATE_OF_THE_PROJECT.md) |
