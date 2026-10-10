# VOLLEY · one-page review

**Gen5 is the current computational evaluation; Gen6 is future scaling research.** The proposed system would feed ordinary 3U CubeSats through one reusable host-mounted electromagnetic launch path and command a departure condition for each. The current academic work evaluates a specified Gen5 reference, including failed criteria. Its final freeze is open. Nothing has been built, fired, measured, qualified or flown.

![Four STEP-derived Blender views of intended Gen5 operations](cad/renders/sequence/gen5_operations_hero.png)

*Store → handoff → accelerate → depart is the intended sequence. The reference fit fails; feed, contact and brake dynamics are unverified. [Animation and provenance](cad/renders/sequence/README.md).*

## Decisive review results

| Question | Result | Interpretation |
|:--|--:|:--|
| Reference side-fed CAD fit | **11 mm short**; 32,915 mm³ overlap per cassette | Failed exact-solid placement, not a tolerance-ready assembly |
| Modeled dry mass per carried 3U | **10.55 kg** | Fails the approximately 6 kg canister comparator and study's 2 kg/customer screen |
| Finite-geometry force screen | **12.448 m/s** ideal-phase shot equivalent | Challenges historical 16.029 m/s periodic model; not a selected motor rating |
| Independent 2-D finite-element screen | **1.082 kJ** ideal in-plane work | Numerical method check with stated limits, not physical validation |
| Matched twelve-shot mission | **No sampled case closes** | Bounded assumed-host comparison, not proof that every possible mission fails |

[Full computational report](reports/GEN5_COMPUTATIONAL_REVIEW.pdf) · [FreeCAD/STEP report](cad/GEN5_CAD_REVIEW.pdf) · [Validation register](validation/README.md) · [Open review gates](docs/GEN5_FREEZE_READINESS.md) · [Market and spacecraft fit](MARKET_AND_CUSTOMER_FIT.md).

## What follows

R1 is an **unselected widened geometry candidate** with twelve scripted 3U envelope routes cleared; actuator, restraint, tolerances, installed mass and host fit remain open. Gen6 is the proposed **first instrumented prototype programme** for a mission-derived command range; 1 km/s is separate long-range research, not an achieved release speed. A named payload and provider interface, complete mechanism and budgets, fair mission comparison, independent review and future instrumented hardware tests are needed before a product claim. [Current status](docs/NEXT_GENERATION_STATUS.md) · [prototype-to-flight gates](docs/GEN6_PROTOTYPE_TO_FLIGHT_ROADMAP.md).

The [thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis), [IEEE-formatted paper companion](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) and [lab vault](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) are each self-contained. The paper has not been submitted; no IEEE venue is selected.
