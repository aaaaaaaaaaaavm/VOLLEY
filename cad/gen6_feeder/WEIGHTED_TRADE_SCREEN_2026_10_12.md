# Gen6 feeder: weighted provisional screen

**Decision status: no feed architecture selected.** D10 fixes the weights; D27 requires comparable whole-system evidence before a controlled downselect. The numeric matrix is an explicit, reproducible *ordinal hypothesis*, not measured reliability or hardware performance. [Inputs](trade_screen_inputs.csv), [arithmetic](trade_screen.py) and [output](release/Gen6_Feeder_Provisional_Trade.json) are retained so every score can be challenged or changed.

## Common boundary and evidence

Every candidate must store two passive 1U and two passive 3U payloads in independently retained fixed or moving cells, transfer one at a time into one captive launch carrier, leave all unselected cells locked, and remain contained at any loss of power. A failed cell is isolated and remaining cells continue only after verified path clearance. The host is a generic maneuvering orbital-transfer deck with a **provisional** adapter; no supplier ICD or available envelope is selected. The first laboratory article would measure 3–6 m/s, while the mathematical mission asks for about 7 and 9 m/s commands in two cases. This gap is not resolved by feeder choice.

The [public reference audit](../../docs/GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md) supplies CubeSat mass classes and a mixed-size dispenser precedent. The [one-cell lead-screw reference](README.md) and [integration audit](../GEN6_INTEGRATION_AUDIT_2026_10_12.md) provide actual nominal CAD evidence **only for a proxy lead-screw layout**. R1 exposes a 10 mm unsupported handoff gap; R2 nominally bridges it but has no verified contact, extension sequence or power-off restraint. All other candidate fit, mass and fault scores are concept estimates. No candidate has a four-cell installed BOM or complete motion model.

## Criteria and provisional scores

The five weight groups are fault containment and safety **35%**, packaging and installed mass **25%**, positioning and repeatability **20%**, cycle time and power **10%**, and manufacturability **10%**. Each criterion uses a 1–5 ordinal score: 1 is unfavorable under the stated boundary; 5 is favorable. A one-point interval on *every* unmeasured criterion exposes scoring uncertainty. The intervals are sensitivity bounds, not statistical confidence intervals.

| Candidate | Weighted nominal / 5 | All-scores ±1 interval / 5 | Main basis for the provisional score |
|:--|--:|:--|:--|
| Fixed cells, captive lead screw | 3.650 | 2.650–4.650 | Stored payloads remain fixed; positive, reversible transfer and accessible hard stops. Current CAD is only one 3U cell and fails power-off containment. |
| Fixed cells, spring follower and two gates | 3.075 | 2.075–4.075 | Potentially compact and low transfer-drive energy, but force variation and double-feed/failure of two barriers are unresolved. Spring pressure is not launch restraint. |
| Indexed rack and pawl | 2.925 | 1.925–3.925 | Discrete index and holding datum; partial stroke, bounce, anti-reverse and variable cell pitch add fault paths. |
| Nested telescoping carriage | 2.650 | 1.650–3.650 | Compact stowed length; multiple sliding interfaces and concealed binding/debris complicate repeatability and inspection. |
| Belt or cable shuttle | 2.525 | 1.700–3.525 | Remote actuator and useful travel; slack, wear, particle control and power-off position retention are uncertain. |
| Geneva indexed drum or tray | 2.500 | 1.500–3.500 | Positive dwell is attractive, but moving loaded cells and a shared index fault threaten all releases. |
| Segmented pantograph | 2.325 | 1.500–3.325 | Potential compact vertical stowage, but sequential collapse requires separate latches; near-flat joint force, play and extra transfer pusher remain unresolved. |

These nominal ranks are **not a reliability calculation**. For example, the lead screw's lower bound is below the spring follower's upper bound, so the present evidence does not justify rejecting the latter. An engineering score needs measured or sourced component mass, exact swept volume, pusher force/torque, contact and restraint load, cycle energy and demonstrable fault transitions. A rank computed from unverified assumptions cannot pass D27 by itself.

## Current decision and next comparison

Retain fixed cells with a captive lead screw as the **analysis reference**, the spring follower with dual gate as a **runner-up**, and the pantograph as a **packaging challenger**. This is a comparison order, not a selected production mechanism. Model all three against one released 1U/3U envelope and the same guide, carrier, host adapter and access volume; then apply the five weighted criteria using actual measurements or CAD-derived quantities. The bridge contact and motion sequence, mid-transfer power-off restraint and independent failed-cell isolation are mandatory pass/fail gates before any score can select a baseline. If all candidates fail, the appropriate outcome is no selection and a revised configuration.

The full seven-concept record remains in [the project concept study](../../docs/GEN6_FEEDER_CONCEPT_TRADE.md). Unselected hypotheses are retained in VOLLEY-Labs as research alternatives; no concept is described as rejected until evidence supports that disposition.
