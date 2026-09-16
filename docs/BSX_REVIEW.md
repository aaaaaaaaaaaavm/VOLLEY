# BSX review and Gen6 handoff

Reviewed 2026-09-16. I use this as an engineering-conversation entry point. The live-item tables are generated from the register; configuration-specific history is retained rather than rewritten as current hardware.

## What I can defend

VOLLEY Gen5 is a frozen computational baseline with declared failures. Nothing has been built, fired, measured, qualified or flown. The [baseline](BASELINE.md) supplies the operating numbers and [Gen5 closure](GEN5_CLOSURE.md) names their evidence. A passing software gate establishes internal consistency, not flight readiness.

The programme remains provider-hosted control of spacecraft departure conditions: provider-authorised host manoeuvres can supply coarse orbital placement and the deployment system supplies the relative release condition. Host propulsion reserve, restart capability, attitude control, navigation uncertainty, interface limits and disposal authority require provider data.

## Current Gen6 preparation

The clean-sheet reference carried forward for the next calculations is **independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. It is not selected flight hardware. P92/P113 remain open.

1. Turn S1-S4 into architecture-driving uncertainty and clearing/settling requirements before assigning release-cell tolerances.
2. Quantify installed burden and failure topology for independent cells, small banks and the shared magazine/path using one system boundary.
3. Try to falsify the reference before detailed CAD: accumulator force-displacement, preload sensitivity, latch shock, pusher friction/guidance, tip-off, catcher load and cycle life.
4. Carry the surviving reference into a dated P92 configuration decision, then engineer one real cell and scale 2/4/12-cell arrangements.
5. Keep the approximately 8 m gas guide, A72-A74 trim/tube conflict, P103/P108 contact work and pressure-system studies as historical gas-Gen6 evidence. Do not transfer their geometry or failure magnitudes to the compact reference without a new validation path.

The generated live-item table below still reproduces each register entry's recorded next-step wording. P92's legacy row therefore describes the historical gas trim/tube decision that produced A72-A74; the current programme-level P92 path is the clean-sheet reference and its explicit falsifiers in [GEN6_REFERENCE_ARCHITECTURE.md](GEN6_REFERENCE_ARCHITECTURE.md). The register status remains LIVE until its native closure condition is legitimately dispositioned.

## Questions for BSX / host review

- Launch provider: retained post-primary body, usable envelope/mounts/keep-outs, remaining propulsion and restart windows, stage mass properties, attitude authority, navigation uncertainty, power/energy, thermal limits, command access, and disposal/passivation constraints.
- Mechanisms or test team: review independent retention, accumulator/latch/pusher/catcher load paths, release repeatability, shock/tip-off measurement and the smallest useful coupon before a flight-like cell is drawn.
- Payload team: actual retention, acceleration, shock, tip-off, contamination and magnetic limits. Unmodified is a design objective; compatibility is not demonstrated.

## Remaining work by scope

| Scope | Computation | Hardware | Host data | Flight/operations | Decision |
|---|---:|---:|---:|---:|---:|
| GEN6 | 18 | 4 | 5 | 1 | 1 |
| GEN5 | 11 | 0 | 0 | 0 | 3 |
| PROGRAMME | 1 | 0 | 0 | 1 | 6 |

## GEN6 live items

| Entry | Next step class | Action that would move it |
|---|---|---|
| [P57](../OPEN_PROBLEMS.md) | COMPUTATION | read the voice-coil deployer in full and record it in PRIOR_ART under that file's five fields |
| [P67](../OPEN_PROBLEMS.md) | HARDWARE | measure the seal friction -- B-2 |
| [P68](../OPEN_PROBLEMS.md) | HOST_DATA | a real stage interface: what a provider will actually credit |
| [P75](../OPEN_PROBLEMS.md) | COMPUTATION | a Gen6 reliability architecture, the way A47 did Gen5 |
| [P78](../OPEN_PROBLEMS.md) | HARDWARE | it resolves with P67; the friction share is what is unmeasured |
| [P79](../OPEN_PROBLEMS.md) | COMPUTATION | A76 has falsified inclination as the residual's cause; the reference orbits' own provenance is the next thing to check |
| [P81](../OPEN_PROBLEMS.md) | COMPUTATION | an ejector concept that clears the tube on the energy available |
| [P87](../OPEN_PROBLEMS.md) | COMPUTATION | re-plan the campaign fill schedule against the window |
| [P88](../OPEN_PROBLEMS.md) | HARDWARE | the seal's own conduction path, measured |
| [P91](../OPEN_PROBLEMS.md) | COMPUTATION | a pressure vessel design that meets A53's per-cell mass |
| [P92](../OPEN_PROBLEMS.md) | DECISION | A74 has stated the requirement and eliminated every local fix; which of ADR-033 and ADR-035 yields is a programme choice |
| [P94](../OPEN_PROBLEMS.md) | HOST_DATA | a published control authority for a real stage |
| [P99](../OPEN_PROBLEMS.md) | HOST_DATA | a real host wheel, or a host that does not need one |
| [P103](../OPEN_PROBLEMS.md) | COMPUTATION | A67 has run; what is left is roundness, stick-slip, inertia variation, tube compliance and a contact law that passes its own restitution check |
| [P108](../OPEN_PROBLEMS.md) | COMPUTATION | A71 posed the convergence problem properly and did not solve it: raise the penalty stiffness until peak penetration is under 10 % of the clearance and re-converge in tolerance, or replace the penalty with a stabilised constraint formulation, or make the piston compliant so the contact stiffness is physical |
| [E30](../OPEN_PROBLEMS.md) | FLIGHT_OPS | published dispenser deployment counts and failure records |
| [E31](../OPEN_PROBLEMS.md) | HOST_DATA | the launch-interface position of an actual provider |
| [E32](../OPEN_PROBLEMS.md) | COMPUTATION | design the ascent inhibit and its fault logic |
| [E28](../OPEN_PROBLEMS.md) | COMPUTATION | campaign mission life at a real deployment altitude |
| [P117](../OPEN_PROBLEMS.md) | COMPUTATION | A73 has derived the constant; A55's re-run waits on P92's trade |
| [P118](../OPEN_PROBLEMS.md) | COMPUTATION | A72 has integrated it; what remains is the same fix trade P92 owns, now with numbers in it |
| [E3](../OPEN_PROBLEMS.md) | COMPUTATION | select components from public vendor data instead of parametric masses |
| [E4](../OPEN_PROBLEMS.md) | HARDWARE | build something |
| [E5](../OPEN_PROBLEMS.md) | HOST_DATA | host stage propellant, authority and restart constraints |
| [E6](../OPEN_PROBLEMS.md) | COMPUTATION | uncertainty range from a variable atmosphere, not a single multiplier |
| [E7](../OPEN_PROBLEMS.md) | COMPUTATION | select a sensor from public data and use its stated noise |
| [E11](../OPEN_PROBLEMS.md) | COMPUTATION | public material screening -- ASTM E595 class data for the Gen6 BOM |
| [E16](../OPEN_PROBLEMS.md) | COMPUTATION | a reference audit against publisher records |
| [E18](../OPEN_PROBLEMS.md) | COMPUTATION | a conjunction covariance from a defensible public source |

## GEN5 live items

| Entry | Next step class | Action that would move it |
|---|---|---|
| [P14](../OPEN_PROBLEMS.md) | DECISION | keep Gen4 or declare Gen5 the only generation -- D8 |
| [P18](../OPEN_PROBLEMS.md) | COMPUTATION | model the four effects, or bound them and say so |
| [P30](../OPEN_PROBLEMS.md) | DECISION | the band stands as declared; what changes is what is claimed from it |
| [P32](../OPEN_PROBLEMS.md) | DECISION | D8 |
| [P33](../OPEN_PROBLEMS.md) | COMPUTATION | compute the winding inductance |
| [P34](../OPEN_PROBLEMS.md) | COMPUTATION | a magnetically screened cell, or a declared exclusion |
| [P36](../OPEN_PROBLEMS.md) | COMPUTATION | a dynamic design case for the track |
| [P45](../OPEN_PROBLEMS.md) | COMPUTATION | flywheel specific energy from flown units |
| [P52](../OPEN_PROBLEMS.md) | COMPUTATION | segment handover through the track mode |
| [E33](../OPEN_PROBLEMS.md) | COMPUTATION | magnet tolerance and the residual dipole |
| [E34](../OPEN_PROBLEMS.md) | COMPUTATION | a shock response spectrum at the cassette interface |
| [E35](../OPEN_PROBLEMS.md) | COMPUTATION | vary the payload field exposure as a design variable |
| [E24](../OPEN_PROBLEMS.md) | COMPUTATION | attitude disturbance from magazine indexing |
| [E25](../OPEN_PROBLEMS.md) | COMPUTATION | attitude restoration and structural settling |

## PROGRAMME live items

| Entry | Next step class | Action that would move it |
|---|---|---|
| [P44](../OPEN_PROBLEMS.md) | FLIGHT_OPS | femtosat deployer masses actually flown |
| [P59](../OPEN_PROBLEMS.md) | DECISION | D2: which payload class is the product |
| [P69](../OPEN_PROBLEMS.md) | DECISION | the comparison stands; what changes is what is claimed |
| [P74](../OPEN_PROBLEMS.md) | DECISION | export the Fusion documents, or declare Gen5 the only geometry -- D8 |
| [P113](../OPEN_PROBLEMS.md) | COMPUTATION | the required release-velocity envelope as a function of how much orbital energy the host supplies |
| [E9](../OPEN_PROBLEMS.md) | DECISION | design 6U/12U or withdraw them |
| [E14](../OPEN_PROBLEMS.md) | DECISION | file or let it go -- D5 |
| [E15](../OPEN_PROBLEMS.md) | DECISION | fund it or scope it -- D10 |

## Reproduce

Run `python tools/make_bsx_review.py --check` and `bash tools/verify_all.sh` from a clean committed checkout. The scripts report skipped or unavailable checks. See [CONTRIBUTING.md](CONTRIBUTING.md) for dependencies and companion publication order. [BSX_PORTFOLIO_AUDIT.md](BSX_PORTFOLIO_AUDIT.md) records the repositories and checks covered by this review.
