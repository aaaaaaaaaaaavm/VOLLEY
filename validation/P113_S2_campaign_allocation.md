# P113-S2: sequential orbital-energy delivery and host resources

Declared 2026-09-14 before `analysis/campaign_allocation.py` exists.
P113 and E5 remain open. This study cannot select Gen6 or establish compatibility.

## Decision and boundary

Compare equal manifests, scheduled release times and target specific orbital energies
using a fixed spring speed, an adjustable spring screen and larger adjustable screens.
Propagate a planar point-mass host under two-body gravity between instantaneous events.
Carry propellant consumption, remaining payload mass and separation recoil through
every event. A target specifies semi-major axis, NOT a circular destination, coverage,
formation, apsis orientation or collision-safe trajectory. No payload propulsion is used.

Release occurs along the local prograde or retrograde transverse direction. Radial
velocity is unchanged. At radius r with radial velocity vr, target transverse speed is
sqrt(mu*(2/r - 1/a_target) - vr^2). Refuse non-real or non-prograde target solutions.
For each shot choose the signed allowed relative speed nearest the no-burn requirement.
This minimizes the immediate absolute host velocity correction in this bounded domain;
it is a greedy policy, NOT a globally optimal campaign or a fair ranking of hardware.
Directions and speeds may be selected without slew or control penalties in this screen.

For pre-burn mass W, exhaust velocity ve and signed host correction h, post-burn mass
is W'=W*exp(-abs(h)/ve). Solve target_vt = current_vt + h + (1-m/W')*u.
After release, host transverse speed is target_vt-u and host mass is W'-m.
Dry host mass includes an assumed common deployment installation. Different hardware
masses, mechanism consumables and electrical energy are NOT supplied or priced here.
Store post-burn and post-release masses separately. Refuse fuel use into the reserve.

## Frozen illustrative inputs

- Earth constants from `host_reference`; initially circular 450 km, planar prograde.
- Host dry mass including an equal placeholder installation: 300 kg; initial fuel 10 kg;
  protected fuel reserve 2 kg; Isp 220 s. These are assumptions, not provider data.
- Payload 4 kg each; manifest N = 1, 4, 12; release spacing 600 or 3600 s.
- First release at t=0; campaign ends at the last scheduled release, with no disposal burn.
- Missions: COMMON_ENERGY, all targets a=RE+460 km; ENERGY_LADDER, targets evenly
  spaced from RE+440 km to RE+480 km (N=1 uses RE+460 km).
- Screens: fixed signed magnitude 1 m/s; adjustable magnitudes [0.5,2], [0.5,11.8],
  [0.5,16.029], [0.5,29.009] m/s. The intervals are hypothetical controllability,
  not measured hardware envelopes. Either release direction is allowed for every screen.
- Re-run each case with an assumed maximum permitted burn count of 0, 2 and 12.
  A correction <=1e-8 m/s counts as zero; this is a numerical threshold, not engine MIB.
- Reject any host coast whose osculating perigee is below 120 km before propagation.
  This conservative mathematical guard is not a disposal or collision safety criterion.
- DOP853 with rtol=1e-11, position atol=1e-5 m, velocity atol=1e-8 m/s.
  Reference checks use tighter tolerance and an independent Kepler-element propagation.

## Frozen verification criteria

1. Circular one-period propagation closes position within 0.01 m, velocity within
   1e-5 m/s. Noncircular checks against independent elliptic Kepler propagation agree
   within 0.05 m and 5e-5 m/s over the declared 600/3600 s coasts.
2. Specific energy and angular momentum relative drift <=1e-9 on unforced coasts.
3. Every successful event meets target semi-major axis within 0.01 m, separation
   momentum residual <=1e-6 kg m/s and signed relative speed residual <=1e-9 m/s.
4. Rocket-equation mass accounting and initial-minus-delivered-minus-used-fuel identity
   agree within 1e-9 kg; reserve violations reject the event without consuming mass.
5. With a zero host correction and known u, recover the finite-recoil target exactly
   within 1e-8 m/s. Include single-payload, depleted-budget and infeasible target controls.
6. Invalid/nonfinite states, masses, Isp, times, intervals and unavailable target energy
   are refused. Propagation failure cannot return success. Retain partial deliveries and
   their specific stopping reason; do not average failed missions into complete results.
7. Deterministic JSON and Markdown include input/source hashes, all 180 cases and
   event histories. Read-only freshness checking detects missing or altered outputs.
8. No result is labelled flight feasible, collision safe, optimum, mass crossover or
   a selected design. Compare complete cases only; state omissions beside the table.

## Outputs and remaining work

`analysis/campaign_allocation.py`, `tests/test_campaign_allocation.py`,
`analysis/results/campaign_allocation.json`, `docs/CAMPAIGN_ALLOCATION.md`.
The campaign is an energy-target resource screen. Finite burns, achievable minimum
impulse, attitude recovery, thermal/electrical stores, release dispersions, safe
clearance, J2/drag, complete target-state constraints, installed hardware and reliability
remain separate work before a mechanism decision. No existing acceptance band changes.


## Implementation review addendum, 2026-09-14

The criteria above were committed before implementation and remain unchanged.
The initial implementation's byte-only JSON freshness check repeated the portability
risk already documented in `tools/check_results_fresh.py`. Before publication, the
checker was changed to require exact input/source metadata, schema and discrete
values, and numeric case agreement at rtol=1e-12, atol=1e-9. At this study's position,
velocity and mass scales this is tighter than the frozen propagation/event verification
limits; it is a reproducibility tolerance, not a relaxed physical acceptance band.
The Markdown and SVG must exactly regenerate from the accepted stored JSON. Tests
inject a sub-tolerance perturbation and a 0.01 kg corruption, and refuse NaN/schema drift.
Same-environment regeneration must still be byte deterministic. The SVG is an added
presentation of existing cases; no additional physical conclusion is introduced.


## Cross-runner freshness addendum, 2026-09-15

GitHub run 34928298955 exposed sub-micrometre coordinate and position-residual
changes that exceeded the generic scalar freshness comparison. Reproduction now uses
an absolute 1e-5 m floor for Cartesian position components and position-error norms,
and 1e-7 m/s for Cartesian velocity and correction-vector components. Other scalar
comparisons retain rtol=1e-12, atol=1e-9; structure, decisions and input/source metadata
remain exact. The positional floor is 100 times tighter than S3's 0.001 m root check;
the velocity floor is 500 times tighter than its 5e-5 m/s independent-propagation check.
No physical acceptance band, target, search seed or speed interval changes.
See `docs/MISSION_FRESHNESS_20260915.md` in the flagship for the incident record.
