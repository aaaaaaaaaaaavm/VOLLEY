# P113-S3: terminal state and release-time search

Declared 2026-09-15 before `analysis/terminal_timing.py` exists. P113/E5 remain open.

## Question and boundaries

Can a programmable release interval reduce host propellant relative to fixed or
adjustable springs when all alternatives deliver the same position AND velocity
at the same epoch, and receive the same release-time search?

One 4 kg payload, planar two-body gravity, initially circular 450 km host. At t=0
an instantaneous planar host burn selects a transfer arc. At release time tau a
second host burn and collinear relative release produce the desired payload state.
The payload then coasts without propulsion to T=3600 s. Out-of-plane components
are identically zero by construction, not an inclination-change capability.

For each tau solve a two-component shooting boundary problem: the host's position
must equal the target orbit's position at tau. Use SciPy root (hybr) on initial
velocity corrections from seeds (0,0), (+20,0), (-20,0) m/s. Require solver success
AND position residual <=0.001 m; propagate with existing S2 DOP853 settings.
Do not claim all Lambert branches are found. Failed searches remain SEARCH_FAILED,
not mathematically infeasible. Refuse initial burns >100 m/s and arcs violating
S2's bound/prograde/120 km perigee guard. No finite-burn or collision claim follows.

At release align the relative impulse with target velocity minus transfer velocity.
All comparators receive this ideal pointing authority. Select magnitude nearest
the no-second-burn requirement within the assumed interval. Permit a signed second
host correction along that axis, solve its propellant mass loss and recoil together.
At zero velocity deficit choose prograde as the release axis. Propagate the resulting
payload to T and evaluate its full Cartesian residual, not only energy.

## Frozen illustrative inputs

- Same constants, Isp=220 s, dry mass=300 kg, initial fuel=10 kg, reserve=2 kg,
  payload=4 kg and five speed screens as S2. All installation and control assumptions
  remain hypothetical; in particular 0.5 m/s is not a measured minimum.
- Three terminal targets: 450 km circle 5 km ahead of the unperturbed host;
  450 km circle 25 km ahead; 460 km circle at the unperturbed host's terminal angle.
  Ahead is arc length at the 450 km radius. Circular target speed follows its radius.
  Analytic circular propagation fixes every target at all epochs from that terminal state.
- Release-time grid: 150,300,...,3000 s (20 points). Coarse subset: multiples of 300 s.
  Same permitted timing and host controls for all screens. No prescribed order advantage.
- Mission acceptance: terminal position norm <=10 m and velocity norm <=0.01 m/s;
  fuel reserve respected. These are assumed study requirements, not customer requirements.
- Objective: minimize total host propellant over successful candidate arcs on the stated
  grid. Break exact ties by earlier release. Report coarse and fine results, not a global
  optimum, convergence claim, manifest crossover or selected mechanism.
- Every target/time/screen combination has a record, including rejected candidates:
  3*20*5=300 rows. Retain per-seed search status and all distinct accepted transfer arcs.

## Frozen verification criteria

1. Independently propagate accepted transfer arcs and payload coasts using elliptic
   Kepler elements/eccentric anomaly. Agree with integration within 0.05 m and
   5e-5 m/s. Check circular propagation separately without dividing by eccentricity.
2. A known circular no-transfer boundary recovers initial correction norm <=1e-6 m/s.
   An independently constructed noncircular arc is recoverable from the seed search.
3. Every successful delivery meets terminal mission bands above; root residual alone
   cannot authorize success. Same-energy wrong-phase and wrong-velocity controls fail.
4. Both burns obey the rocket equation; mass accounting error <=1e-9 kg; separation
   momentum residual <=1e-6 kg m/s and relative-velocity error <=1e-9 m/s.
5. At least one reference mission has a successful candidate for every screen. If not,
   record failure of the reference search; do not move targets/seeds/bands to obtain it.
6. Exhaustive reduction of recorded candidates agrees with reported selections; fine
   grid cannot be worse than its exact coarse subset when either has successful rows.
   No monotonic claim across different physical mechanisms or speed limits is required.
7. Invalid/nonfinite inputs, invalid intervals, negative time, solver failure, reserve
   violation and material stale-output injection are refused explicitly.
8. Deterministic inputs and output schema, exact source hashes; numerical freshness
   tolerance rtol=1e-12, atol=1e-9 as S2, not a physical acceptance band. Markdown must
   reproduce exactly from accepted stored JSON. P113/E5 remain open in every report.

## Outputs and exclusions

`analysis/terminal_timing.py`, `analysis/results/terminal_timing.json`,
`docs/TERMINAL_TIMING.md`, `tests/test_terminal_timing.py`.
Independent Kepler checking belongs in the test harness. Reuse the existing integrator
and constants; do not introduce a new astrodynamics dependency for this bounded case.

This is a single-payload timing benchmark. Complete manifests, shared power/energy,
installation mass, pointing/slew/settling, minimum impulse, release dispersion, J2/drag,
clearance, passivation and provider permission remain separate requirements.

Sources reviewed for formulation/API, not validation of this implementation:
- ESA Flight Dynamics, Lambert boundary problem and branch choice:
  https://godot.io.esa.int/docs/tutorials2/fundamentals/astro/03-lambert-problems.html
- SciPy root API, success and termination status:
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html
  Execution uses the repository's pinned SciPy version, not the online latest release.


## Implementation review, 2026-09-15

The first six-test run failed the known circular boundary control (five tests passed).
The root search used the near-zero initial velocity correction as its unknown. Its
relative-step termination returned unsuccessful searches for a boundary whose physical
position residual was already small. The failed test is retained in
`P113_S3_initial_check.txt`. No reference target or acceptance band was changed.

The corrected implementation searches in absolute orbital velocity coordinates with
exactly the same physical seeds, then subtracts the initial circular velocity when
reporting the correction. The root termination tolerance is 1e-11. Both solver success
and the original 0.001 m boundary residual remain required. This is a conditioning fix,
not permission to accept a failed solver or to declare missing branches infeasible.

All selected release times in the initial reference results lay at the latest permitted
time, 3000 s. Report that boundary condition prominently: these searches do not bracket
an interior optimum, and equal coarse/fine values do not establish timing convergence.


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

Completion, 2026-09-15: run 34928809087 showed the vector policy omitted scalar
velocity-error norms and burn magnitudes. They now receive the same 1e-7 m/s
freshness floor. Conservation residuals and discrete verdicts remain strict;
no physical acceptance criterion changes. The observed failing pairs are retained
in regression tests and the incident record.
