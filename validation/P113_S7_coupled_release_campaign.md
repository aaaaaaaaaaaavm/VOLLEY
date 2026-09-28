# P113-S7: coupled two-release state-error and navigation-policy screen

Declared 2026-09-17 before implementation or execution. Starting main:
`aac3871fcc32851cede03b977933a79ef3461f5e`.

## Question and scope

Does propagating the first release's actual retained-host state into the next
transfer change the second payload's terminal error, and what does idealized
navigation-based replanning buy relative to replaying fixed commands?

This is the first bounded N1 increment, not completion of N1. Keep the S4 planar
Earth two-body model, 4 kg payloads, 300 kg assumed installed dry host, 10 kg
propellant, 2 kg protected reserve, 220 s Isp, 3600 s terminal epoch and unchanged
10 m / 0.01 m/s terminal bands. Use the same target order (phase_5km then phase_25km)
and releases at 1200 and 3000 s for all comparators. Freeze each first-release
speed at the best accepted S4 candidate for that schedule, not a new optimization.

Compare S4 fixed_1, spring_screen and bolley_screen authority intervals. The last
is a hypothetical wider-authority comparator, not proven BOLLEY or current-cell
performance. Gen5 and historical gas-Gen6 tied that wider screen in this schedule
and need not be duplicated. No installed hardware ranking is permitted.

## Timeline and policies

Start with the published first transfer and first pre-release correction charged
to host mass/fuel. Apply the common state error once immediately before the first
release. Apply relative-release error with finite-host momentum conservation.
Propagate the actual retained host throughout; never replace it with a nominal
state at the second event.

Evaluate transfer-start delays of 0 and 120 s after first separation, keeping the
second release at 3000 s. Build a new nominal second-transfer command for the
120 s delay, preserving the first event. Delay is a coast-time assumption, not
evidence of clearance, plume safety or attitude settling. Pre-release impulses
remain ideal and instantaneous; no hardware or provider capability is implied.

Policies:
1. REPLAY: replay nominal inertial second-transfer and pre-release burn vectors
   and the nominal relative release vector; only the imposed release biases vary.
2. EXACT_NAV_REPLAN: at the delayed transfer epoch observe the actual host state
   exactly and shoot to the same second target position; at second release use
   the exact actual state for the pre-release correction and release command.
   Navigation has no latency, measurement noise or execution error. This is an
   optimistic control benchmark, not an operational navigation solution.

A local shooting solve may start from the nominal departure velocity; accept it
only with solver success, position residual <=0.001 m, correction <=100 m/s and
adequate reserve. Missing roots are SEARCH_FAILED, not proofs of infeasibility.
Record root diagnostic and actual resource history. Charge every impulse using
the rocket equation at the current mass. Track total host delta-v, propellant,
remaining reserve and ideal payload-relative release kinetic energy separately.
The latter is not motor input energy or an installed power budget.

## Frozen sampled experiment

Six illustrative shared-error half-widths, inherited from S6:
radial/tangential initial position 0.1 m each; radial/tangential initial velocity
0.0001 m/s each; release-speed bias 0.0005 m/s; release-angle bias 0.005 degrees.
State axes are frozen at the nominal first event. Release biases are applied in
each command's local direction and are identical across both releases in this
shared-calibration family.

For each screen/policy/delay run one zero-error case and all 64 sign corners at
multipliers 1, 2 and 5. Also run 16 release-only corners at multiplier 1 with
independent speed/angle signs for event 1 and event 2 and zero common-state error.
Exactly 3*2*2*(1+3*64+16) = 2508 attempted histories. Retain interrupted histories,
search failures, mission failures and all sampled inputs. These deterministic
samples neither bound the continuous error domain nor define a probability.

## Verification criteria, frozen before execution

- Zero-delay zero-error REPLAY reproduces the stored S4 terminal states within
  0.001 m and 0.000001 m/s, and fuel within 0.00000001 kg.
- Every separation conserves momentum to <=1e-8 kg m/s and relative velocity to
  <=1e-9 m/s. Mass bookkeeping closes to <=1e-9 kg.
- Energy and angular momentum are checked on coast segments only, not across
  burns or releases: fractional drift <=1e-8.
- Independently coded fixed-step RK4 at 5 s and 2.5 s checks the nominal delayed
  coast/transfer segments against the adaptive solve. At 2.5 s, disagreement
  <=0.01 m and <=0.00001 m/s; step halving reduces resolved discrepancies.
- A tighter adaptive solve checks zero and all-positive multiplier-5 histories
  for all screen/policy/delay combinations: terminal differences <=0.01 m and
  <=0.00001 m/s, fuel <=0.000001 kg; discrete outcomes must agree.
- An analytic circular-orbit propagation limit and zero-duration coast check
  are required. A deliberate first-release perturbation must survive into the
  second host state under replay; a reset-to-nominal implementation must fail.
- Invalid/nonfinite inputs, corrupt S4 hashes and reserve exhaustion must fail
  explicitly, never be converted into a successful delivery.
- Sources, exact inputs, policy names, sample identifiers and verdicts must
  match exactly in freshness checks. Computed numerical reproducibility floors:
  0.0001 m for position components/norms, 0.0000001 m/s for velocities, 1e-8 kg
  for fuel/mass, with relative tolerance 1e-10. Presentation regenerates exactly
  from the accepted stored JSON. Floors are numerical, not physical bands.

Verification failures block credit for the new result; retain the output and
cause. Mission failures are valid outcomes and must not be hidden by requiring
a successful mission in the software gate. Do not change the experiment or
thresholds after examining results; corrections require a dated explanation.

## Outputs and next dependencies

Executable analysis, full JSON histories/provenance, generated report/figure,
meaningful conservation/independent-control/fault tests and normal freshness
gates. Synchronize companion evidence from a clean committed source.

P113, E5 and P92 remain open. Still required for N1: noisy/correlated navigation
updates, finite burns/attitude recovery, clearance/recontact, complete energy
and disposal/contingency sizing, bounded 4/12-payload campaigns and replenishment.
C0–C2/L0–L2 lunar requirements screening remains separate and must precede any
claim that N2 dimensions satisfy a lunar mission. No interview feedback has been
supplied and none is assumed.

