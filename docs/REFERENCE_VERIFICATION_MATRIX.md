# Current-reference verification and model credibility

I use this matrix to connect the current release-cell questions to evidence and the next closure action. These are review rows, not newly approved flight requirements. A model verification pass does not establish mission acceptance or hardware validity.

| Question / boundary | Current evidence | What it establishes | Missing closure |
|---|---|---|---|
| Is programmable release useful at a declared target? | [S1](DEPARTURE_TRADE.md), [S3](TERMINAL_TIMING.md) | Bounded two-body departure and terminal-state screens | Provider mission, target tolerances and comparator selection |
| Can two payloads share one evolving host? | [S4](MANIFEST_TIMING.md) | 100 tested cases, 44 accepted; no host reset | Full manifest, continuous optimum and disposal reserve |
| Which errors consume terminal bands? | [S5](OPERATIONAL_UNCERTAINTY.md) | Local derivatives with symmetry, convergence and momentum checks | Provider navigation/pointing bounds and covariance |
| What happens when errors act together? | [S6](COMBINED_RELEASE_ERRORS.md) | 512 conditional event corners and nonlinear/linear comparison | Carry host error through later burns; interior/edge extrema and correlations |
| Does an accumulator fit a bounded stroke/load? | [P92-S2](REFERENCE_CELL_MECHANICS.md) | 144 spring/pusher cases; 48 pass the analytical screen | Finite-host coupling, selected component geometry and nonlinear force law |
| Does the pusher stay retained without recontact? | P92-S2 kinetic-energy accounting | Catcher work and ideal average force | Dynamic peak load, damping, rebound, latch shock and debris |
| Is one jam isolated? | [Topology recovery](INSTALLED_BURDEN_AND_FAILURES.md) | Conditional stranded-payload counts | Mechanical isolation, common services and actual failure tests |
| Does the system earn installed burden? | Gen5 frozen ledger; partial BOLLEY ledger | Known partial masses and failed prior mass claim | Complete selected spring comparator, cell/BOM/support and host accounting |
| Can the payload remain unmodified? | [Mission boundary](CONCEPT.md) | Design objective and interface ownership | Actual cradle/contact/retention and customer/provider acceptance |
| Is cadence physically achievable? | S5/S6 timestamp headroom | Difference between scheduled event times | Slew, settling, thermal recovery, clearance and operational permission |
| Are the models independently credible? | Regression/property tests, equation checks, retained failed runs | Internal consistency and limited model-to-model agreement | Independent implementation/review and representative measurements |
| Can a prototype be released to manufacture? | [Prototype readiness](PROTOTYPE_READINESS.md) | Intended package and evidence sequence | Controlled drawings, BOM, tolerances, assembly, inspection and frozen test plan |

## Credibility limits that matter to interpretation

- Mission studies use idealized two-body dynamics, instantaneous separation and declared host control. Numerical convergence does not establish realistic navigation, collision safety or environmental fidelity.
- S5/S6 use the stored S4 campaign. Shared source lineage makes them useful extensions, not independent validation of S4.
- S6 resets to the nominal host state at each event. It must not be renamed a robust campaign solve.
- P92-S2 uses a linear spring, fixed-frame internal motion, constant sliding resistance and ideal catcher work. It cannot establish shock, wear, tip-off, manufacturability or component mass.
- Historical gas-guide contact findings remain attached to their configuration. P103/P108 numerical/contact credibility is still open; a new reference does not erase those failures.
- BOLLEY A9g reuses fixed-MMF field equivalence and ideal current tracking. It does not supply a fresh nonlinear field solution of the actual conductors or a supplier-qualified drive.

## Missing-question audit

The next integrated mission must state the real host, navigation update/latency, attitude recovery law, allowed burns, power/thermal interfaces, collision/keep-out geometry, full manifest order, disposal reserve and off-nominal policy. The next cell must state retention during ascent, accidental energy release, preload verification, lubrication/contamination, temperature range, cycle life, fault isolation and servicing. None can be closed by a more polished render.

I keep P92, P113 and E5 open. External review, supplier evidence, measurement and provider acceptance remain separate from further computation.
