# Mission fit and capability boundaries

Adityavardhan Mishra · 17 September 2026

I target the mission space between safe separation and sustained propulsion.
Not every CubeSat needs programmable departure. Conventional calibrated spring
separation can already provide controlled release; the comparison must include
host timing and manoeuvres, attainable accuracy, maturity and full installed cost.
VOLLEY must earn the additional complexity at a declared mission duty.

| Mission need | Baseline to compare | VOLLEY boundary |
|---|---|---|
| Safe departure from an already suitable orbit | Conventional deployer | Additional authority may be unnecessary |
| Different initial phasing for a propulsionless fleet | Calibrated spring, timing and permitted host burns | Test whether individual release conditions improve useful delivery |
| Small achieved-state or schedule changes | Recomputed host manoeuvres and release timing | Bounded recovery must be demonstrated with navigation uncertainty |
| Repeatable multi-payload delivery | Competent dispenser plus evolving host state | Include recoil, fuel, attitude recovery, clearance and faults |
| Continuing stationkeeping or later avoidance | Spacecraft propulsion or other ongoing control | One release event cannot supply continuing control |
| Lunar transfer and capture | Carrier/upper-stage propulsion and navigation | Retain payloads through transport/capture; release only at the designed state |
| Larger spacecraft | Retained pallet or separation ring and host control | New load paths, inertia, synchronization and clearance are required |

## Launch carriage and departure

The launch restraint carries ascent loads through declared mechanical interfaces.
It must stay separate from the energy-storage and release-force path. In orbit,
authorized restraint release, charge verification, charger disengagement, latch
actuation, guided departure and pusher capture are separate states. No vibration
qualification, payload-compatibility approval or hardware test is implied.

## Capability stack

| Layer | Function | Evidence and limit |
|---|---|---|
| 0 | Launch carriage | Retention architecture studies; actual ICD/load qualification open |
| 1 | Safe separation | Mechanical models and interface objective; hardware clearance/tip-off open |
| 2 | Programmable departure | P92-S2/S5 force-law screens; selected hardware and calibrated accuracy open |
| 3 | State-aware trim | S3 terminal-state benchmark; achieved-state covariance/recovery closure open |
| 4 | Manifest control | S4/S7 coupled computations; full finite-burn campaign remains open |
| 5 | Propulsionless orbital shaping | S1–S4 bounded orbital work; no ongoing control after release |
| 6 | Observed shot-to-shot adaptation | Requires observable release residuals, latency, estimator and independent subsequent validation |

[P113-S11](FINITE_BURN_DEPARTURE.md) adds a twelve-case single-release screen
with finite burns, mass flow, slew limits and settling. Eight replanned cases meet
the unchanged terminal bands under assumed 10/100 N thrust. This is not a general
host compatibility result or a complete manifest solve. The source-availability
record governs previously reported studies whose artifacts are currently missing.

## Product discipline

Gen6 should provide the minimum installed complexity needed for the selected
departure authority. [P92-S5](MISSION_CARTRIDGES.md) supplies separate low-authority
cartridge targets. It does not turn one spring into a universal actuator or prove
mass/cost superiority. Charge the complete structure, restraints, latch, pusher,
catcher, charger, sensors, controls, harness, thermal interfaces and host services.
Use useful delivered payloads as the mission denominator and retain failed cases.

The strict target customer operates mission-limited, economically replaceable
satellites with no onboard thrusters, including attitude jets. The payload still
needs attitude control, power, communications and a credible end-of-life case.
Customer demand, useful lifetime and willingness to pay remain to be validated.
