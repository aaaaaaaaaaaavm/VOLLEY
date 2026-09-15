# P113-S4: two-payload terminal-state campaign search

Declared 2026-09-15 before `analysis/manifest_timing.py` exists. P113/E5 remain open.

## Question and frozen scope

Does a release-speed choice that saves propellant for one payload also save it when
the same host must deliver a second payload? Compare complete two-payload campaigns,
not the sum of independently initialized single-payload missions.

Reuse S3's 450 km initial circle, planar two-body propagator, constants, three
shooting seeds, 100 m/s transfer-burn ceiling, 120 km perigee guard, 220 s Isp,
300 kg dry host, 10 kg initial fuel, 2 kg reserve, 4 kg per payload, terminal epoch
3600 s and five hypothetical speed screens. Dry mass includes the same placeholder
installation for every screen; no installed-mass advantage is implied.

The two payloads must reach S3's `phase_5km` and `phase_25km` circular targets, each
with position error <=10 m AND velocity error <=0.01 m/s at the common epoch.
This is an illustrative initial-distribution benchmark, not a customer requirement
or a replenishment/coverage/disposal demonstration.

Enumerate both target orders and every increasing pair from [600,1200,1800,2400,3000]
seconds: 10 schedules, 2 orders, 5 screens, exactly 100 top-level case records.
The coarse subset uses [1200,2400]. Every comparator receives the same schedules,
orders and host control authority. No continuous-time optimum is claimed.

At time zero, shoot from the initial host state to the first target position at its
release epoch. Immediately before release, use S3's coupled fuel/recoil solution
to deliver the target velocity. From the actual retained host state after release,
shoot to the second target position at its release epoch. This transfer burn occurs
immediately AFTER the first separation: it cannot act on the detached payload.
At the second release use the same coupled correction/separation solution.
The permitted ideal control schedule therefore contains up to four impulses.
Separate accounting of the two impulses around the first release is mandatory.
There is no settling, clearance, plume or finite-burn claim.

For each accepted first transfer arc, enumerate distinct first-release speeds at
the interval endpoints, midpoint, and S3's locally preferred clipped speed. Fix
each choice using a degenerate interval in S3's separation solver. Fixed 1 m/s has
one choice. For each resulting retained host state, retain all distinct accepted
second transfer arcs found by the same three global Cartesian correction seeds
(0,0), (+20,0), (-20,0) m/s. At the final release S3's locally minimizing scalar
choice is sufficient for that fixed arc because no further delivery is attempted.

Minimize total host fuel over accepted candidates, then earlier first and second
release times, then lexical target order. Report coarse/fine choices, both fixed
orders, first speed, both terminal residuals, per-event masses/burns, final fuel,
all search failures and interrupted campaigns. Also report the best candidate
restricted to S3's local first-speed policy within the same schedule search.
An enumerated improvement is not a proof of global speed or timing optimality.
Endpoint/midpoint grids differ between intervals, so do not assert monotonicity
between physical mechanisms or even between nested speed intervals.

## Frozen verification criteria

1. Independently check every stored accepted transfer arc and delivered payload coast
   with the existing test-only elliptic Kepler implementation: <=0.05 m position and
   <=5e-5 m/s velocity difference from DOP853. Include a noncircular, translated
   starting state to expose a hidden reset to the original circular host.
2. Every accepted campaign delivers both targets within the terminal bands, keeps
   reserve >=2 kg, and preserves the changing manifest. Every burn satisfies the
   rocket equation; final retained mass equals initial mass minus both payloads
   and used fuel within 1e-9 kg. Momentum residual <=1e-6 kg m/s and relative
   velocity residual <=1e-9 m/s at both separations.
3. Second-leg initial position equals the first retained host position and its
   velocity equals first retained velocity plus the second transfer correction,
   within 1e-9 in the stored state components. The second transfer starts with
   the retained mass/fuel, not a fresh host. A deliberately reset-state control fails.
4. Independent exhaustive reduction of candidates reproduces each reported best
   choice. Fine cannot be worse than its coarse subset; the enumerated first-speed
   policy cannot be worse than its included local-only subset when either succeeds.
5. Each screen must have at least one complete successful campaign. If not, report
   the failed reference search; do not move targets or bands. SEARCH_FAILED means
   a bounded search failed, not that the mission is mathematically infeasible.
6. Refuse invalid/nonfinite states, intervals, reversed/equal/out-of-window times,
   unknown/duplicated targets and invalid reserve inputs. Inject solver and reserve
   failures and verify partial events are retained and no success is reported.
7. Freshness requires exact structure, decisions, inputs and source hashes. Reuse
   S2/S3's field-aware numerical tolerances (1e-5 m Cartesian position/error floor,
   1e-7 m/s velocity-vector floor; remaining scalars rtol=1e-12, atol=1e-9).
   Reports reproduce exactly from stored results. Material corruption must fail.

## Outputs and open decisions

`analysis/manifest_timing.py`, `analysis/results/manifest_timing.json`,
`docs/MANIFEST_TIMING.md`, `tests/test_manifest_timing.py` and a generated comparison
figure. Connect reproduction to local and CI gates and export companion evidence.

This adds coupling between deliveries, not a validated speed envelope or mechanism
selection. Larger manifests, unrestricted speed/direction/branch search, navigation
and release uncertainty, J2/drag, host attitude, mechanism energy, installed mass,
failure topology, packaging and provider interfaces remain unresolved. No Gen5
baseline, Gen6 configuration, or open-item disposition changes.
