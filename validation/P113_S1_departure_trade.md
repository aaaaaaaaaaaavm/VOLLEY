# P113-S1: allocation of a single departure impulse

Criteria declared 2026-09-14 before `analysis/departure_trade.py` exists.
This is a bounded contribution to P113, not closure of P113 or E5.

## Question and model boundary

At a common release position, how much signed tangential velocity must the host
supply before a conventional separation envelope suffices? The target is an ellipse
with one apsis at the initial circular reference altitude and the other at the
specified altitude. Both raising and lowering are included. This is an instantaneous
allocation comparison, not a propagated multi-payload campaign or a claim that
different circular destinations can be reached in one release.

Host impulse h occurs immediately before release at that same position. M is the
retained host mass, including remaining payloads and deployer; m is the released mass.
For signed relative separation speed u, momentum conservation gives
payload increment d = h + M/(M+m) u, and host increment h - m/(M+m) u.
The host can choose any h in [-B, B]. This optimistic control assumption excludes
minimum impulse bit, finite burns, pointing, restart, coast and disposal constraints.
Class C uses B=0; nonzero budgets are reference sweeps for classes A/B, not provider data.

For a required d, achievable magnitudes of u range from
max(0, |d|-B)(M+m)/M to (|d|+B)(M+m)/M. Intersect this interval
with the assumed release-speed interval. Both release directions are permitted.
A zero-width intersection at a boundary is accepted. Numerical tolerance is 1e-10 m/s.

## Inputs, all study assumptions except constants and labelled design points

- Reference altitudes: 450 and 500 km; opposite-apsis offsets: -100, -50, 0,
  +10, +50, +100, +200 km. Earth radius and gravitational parameter are imported
  from the existing `host_reference` module.
- Retained host masses: 100, 300, 1000 kg; released payload: 4 kg.
- Host impulse budget B: 0, 2, 10, 30, 100 m/s, symmetric signed bounds.
- Assumed minimum relative speed: 0.5 m/s for every screen. This is NOT an
  established lower controllable limit, nor proof of collision clearance.
- Optimistic maximum-speed screens: spring reference 2 m/s (assumed comparator),
  BOLLEY reference 11.8, Gen5 reference 16.029, Gen6 reference 29.009 m/s
  (rounded published design points, NOT verified operating envelopes).
  Exploratory 100 and 120 m/s screens are hypotheses only.
- Geometric lower bounds: 8 m stroke and 25 g assumed acceleration ceiling.
  Neither is a provider envelope or payload qualification limit.

No hardware mass, cost, reliability or manoeuvre count is inferred from screen coverage.
Do not rank architectures by the number of sweep cells covered.

## Frozen verification criteria

1. For nonzero offsets, reconstruct both apsides from Cartesian specific energy
   and angular momentum; absolute altitude error <= 1e-6 km. At zero offset,
   check circular speed and radius instead of an ill-conditioned eccentricity.
2. Momentum residual <= 1e-8 kg m/s and relative-speed residual <= 1e-10 m/s
   for every selected screen point. Payload increment must equal target d within
   1e-10 m/s, with |h| <= B + 1e-10 and release speed inside its declared interval.
3. Independent interval-union formulation in tests agrees with magnitude-interval
   feasibility for all sweep cells, plus random bounded cases using a fixed seed.
4. No-host allocation agrees with u=d(M+m)/M within 1e-10 m/s where feasible.
   Increasing B cannot remove coverage; increasing maximum speed cannot remove it.
5. Circular destination at a radius different from the release radius is refused
   for this single-event model. Nonfinite values, nonpositive masses, negative
   budgets, invalid speed intervals and nonpositive target altitude are refused.
6. Kinematic bounds reproduce v^2/(2a) and v^2/(2L) in SI units, with 100 m/s
   at 25 g requiring 20.3943242596 m within 1e-8 m.
7. Regeneration is deterministic. `--check` refuses missing/stale output without
   writing it. Output records input and source SHA-256 hashes. Tests mutate a
   result to show that freshness checking fails, not merely that it can pass.

## Interpretation criteria, not verification bands

- If the spring reference covers a target, no additional *departure-state reach*
  is credited to VOLLEY for that cell. This does not prove a spring mission wins
  on total resources or that the host manoeuvre is operationally available.
- If only a larger screen covers it, label CONDITIONAL_REACH_EXTENSION, not
  feasible mission or selected architecture. Controllability and integration remain open.
- If none covers it, retain the uncovered cell.
- The zero-offset, zero-budget case cannot supply a nonzero tangential separation
  while exactly preserving the circular target. Retain that negative control.
- Generated report and JSON must explicitly retain P113/E5 as open. No Gen5/Gen6
  design point, acceptance band or existing result is changed by this study.

## Planned outputs

`analysis/results/departure_trade.json`, generated `docs/DEPARTURE_TRADE.md`, and
`tests/test_departure_trade.py`. Provider requirements and uncomputed campaign work
are documented separately from numerical results.
