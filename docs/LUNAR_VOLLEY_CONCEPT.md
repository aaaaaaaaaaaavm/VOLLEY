# Lunar VOLLEY: propulsionless payload delivery concept

Adityavardhan Mishra · 17 September 2026

**Future mission architecture.** This is the most developed future application
of VOLLEY, not the current prototype target. The first ideal requirements screen
has run; no lunar lifetime, flight carrier, engine, provider interface or
unmodified-hardware compatibility is established.

## Current lunar-first visual study

[C0-S2](LUNAR_VISUAL_REVIEW.md) adds a connected ideal transfer/capture screen,
42 two-body release cases, 18 mass-budget cases, concept STEP assemblies and
[interactive orbit/3D views](lunar.html). It does not close useful lifetime,
epoch targeting, finite carrier burns, flight hardware or disposal.

## Mission thesis and allocation

A propulsion-capable common carrier transports mechanically retained satellites
to a useful lunar staging orbit. VOLLEY gives each satellite its commanded final
release velocity, direction and time. Each satellite then operates without
orbit-change propulsion. The carrier remains responsible for transfer, lunar
capture, navigation corrections, pointing and its own end of life, including a
skipped or failed release. VOLLEY remains attached to it.

The preferred study is a carrier delivered toward the Moon by a launch/transfer
service, then capable of lunar capture and orbit shaping. A second study starts
with a payload-hosting stage after its primary LEO delivery. That second branch
must independently close remaining propellant, restartability, thrust, tanks,
long coast survival, navigation, power, thermal control and disposal. The fact
that a stage reaches LEO establishes none of those. A dedicated cislunar OTV is
the later architecture if an adapted stage cannot meet the duty.

## Operational sequence

1. Declare payload mission duration, useful coverage, target orbit family,
   navigation/release accuracy and planned end of life. Include failed payloads.
2. Retain the whole manifest through launch and transfer. If primary LEO cargo
   separates first, update mass/CG/inertia and carrier resource bookkeeping.
3. Execute Earth-orbit raising and transfer injection with all lunar payloads
   retained. Progressive/perigee burns are allowed as a candidate, but require
   finite-thrust trajectory and restart/coast resource analysis.
4. Navigate the encounter and perform lunar capture. Prefer capture into an
   ellipse only if its lower capture cost does not merely move the bill into
   later orbit reshaping and payload lifetime problems.
5. Shape the carrier into the selected deployment orbit. Verify release and
   carrier states against the current navigation uncertainty and resource reserve.
6. Point the cell axis to the required orbital direction. A negative tangential
   release means a carrier attitude change, not a bidirectional pusher. Charge,
   verify inhibits/clearance, release, measure and retain the pusher.
7. Propagate actual recoil, recover attitude, navigate again and replan the next
   release. Repeat for 1, 4 and 12 payload studies; include no-release, jam and
   partial-release histories. Exact navigation from S7 is an optimistic benchmark.
8. Dispose of the carrier on a separately analysed trajectory with sufficient
   reserve even when a shot is skipped. Assess controlled lunar impact, escape,
   Earth return or a defensible disposal orbit case by case. None is the default.
9. Track each payload through its useful period and end of life. A bound
   osculating ellipse at release is not proof it survives or remains useful.

## What the first calculation says

[C0-S1](LUNAR_RELEASE_SCREEN.md) retains 126 release cases and 42 size cases.
For a 4 kg payload and 300 kg retained host, a +4.569852 m/s relative release
near perilune of a 100 x 1000 km staging ellipse produces approximately
100 x 1034.705 km in a two-body model. From a 100 km circular staging orbit,
the same release gives approximately 100 x 120.432 km. This is useful trimming
and phasing authority to investigate, not Earth-to-Moon propulsion.

From a 100 x 10000 km ellipse, a negative release near apolune lowers ideal
perilune from 100 to about 43.619 km. That sensitivity is a reason to study
errors and terrain clearance before preferring apolune deployment. A large
apolune change from a perilune release does not establish a long-lived orbit.

The illustrative carrier numbers are much larger: ideal Earth departure from
300 km circular altitude is about 3.106 km/s; separately assumed lunar arrival
speeds of 0.8–1.0 km/s give about 0.297–0.884 km/s capture impulses across the
three staging examples. Circularizing the 100 x 10000 km ellipse at 100 km
would require another approximately 0.515 km/s. These are distinct ideal
screens, not a connected trajectory or a mission delta-v budget.

## Why high ellipse, frozen orbit and disposal remain open

Use high-fidelity lunar gravity, epoch/orientation, Earth/Sun perturbations,
radiation pressure, terrain and navigation/release uncertainty to evaluate each
candidate. Sweep mission durations initially at 7/30/90/180 days as **study
choices**, not customer requirements or promised lifetimes. Test useful
coverage, eclipses, communications, impact/escape and conjunctions. A frozen
orbit label may be used only after that configuration and its dispersions are
shown to meet the declared lifetime/usefulness requirements.

The payload has no correction burn after release. If the delivery box cannot
fit a useful survivable orbit, change the carrier staging orbit, tighten measured
release/navigation performance, accept a shorter useful mission, or reject the
propulsionless mission. Do not quietly add payload thrusters and call the
original requirement met. Lunar end of life cannot be borrowed from LEO drag.

## Reuse versus modification

| Element | Reuse hypothesis | What must be changed or verified |
|---|---|---|
| Spring/pusher/catcher principle | Same operating chain may work in both environments | Thermal-vacuum force/friction, dwell/creep, contamination, shock, rebound and cycles |
| Cell load paths | Reuse only if launch/transfer/payload loads fit the same envelope | Revised mounts, retention loads, thermal distortion and qualification |
| Charging electronics/sensors | Same commands and interfaces may survive | Radiation, long coast, power/duty, sensing drift and autonomous inhibited states |
| Navigation/control | Retain command/state-machine logic | Lunar navigation, pointing, release covariance, timing, host recovery |
| Payload cassette | Reuse actual compatible payload ICD | Lunar payload thermal/communications/attitude system may require a different envelope |
| Carrier | No automatic reuse of a LEO host | Restart/thrust, tanks/propellant, capture, power, communications, navigation and disposal |

“Minimal modification” is credible as a goal for the **mechanical module**.
It is not credible as a statement about a complete lunar delivery system or an
arbitrary LEO CubeSat. Keep the current coupon host-neutral and parameterized;
reserve sensor access, thermal interfaces and replaceable mount datums. Do not
add heavy lunar-only hardware to the LEO article before a requirement justifies it.

## Detailed work gates and exit products

| Gate | Work / exit product | Status |
|---|---|---|
| C0 requirements | Customer mission, payload bus capabilities, lifetime/end-of-life and no-propulsion definition | Definition drafted; customer values unconfirmed |
| C1 carrier budget | Connected Earth-Moon trajectory, launcher contribution, capture/shaping/disposal, wet/dry masses, thrust/endurance | Ideal first screen only |
| C2 deployment map | Epoch/orbit/apsis/direction/release authority and no-benefit regions | Two-body screen complete; high fidelity open |
| C3 lifetime | Gravity fidelity/convergence, perturbations, terrain, coverage and useful-duration dispersions | Not run |
| C4 delivery uncertainty | Navigation/attitude/timing plus measured mechanism distributions and correlations | Not run; no measured mechanism data |
| C5 campaign | Sequential 1/4/12 manifest, finite burns/recovery, thermal/energy, failed shots | Not run for lunar environment |
| C6 end of life | Separate payload and carrier cases, skipped shot, dead payload, missed burn | No selected solution |
| C7 hardware deltas | Reuse/modify/reject matrix with loads, parts, interfaces and test consequences | Preliminary matrix only |
| L0–L6 carrier trade | Provider/engine source cards, interface facts, matched mission accounting and stage selection | No provider selected; unknowns retained |

The next decisive calculation is a useful-lifetime map for candidate deployment
orbits, followed by connected carrier budgets. Greater release velocity is not
the default remedy. Detailed lunar hardware development is gated by the current
LEO prototype review package, then by the survival of these lunar requirements.

## Sources and evidence class

The calculation uses [JPL DE440 gravity parameters](https://ssd.jpl.nasa.gov/astro_par.html).
[NASA Moon facts](https://science.nasa.gov/moon/facts/) supplies general environmental
context; spherical radii and scenarios are declared assumptions in the run sheet.
[NASA's small-spacecraft mechanisms survey](https://www.nasa.gov/smallsat-institute/sst-soa/structures-materials-and-mechanisms/)
is comparison background, not certification of a VOLLEY interface. All sources
accessed 17 September 2026. No supplier or orbit-lifetime result is implied by
these references. All new numerical claims trace to the executable C0-S1 output.
