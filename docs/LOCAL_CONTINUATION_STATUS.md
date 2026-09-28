# Continuation record and recovery boundary

Adityavardhan Mishra · 17 September 2026

## Current disposition — 26 September 2026

The [new engineering checkpoint](CONTINUATION_20260926.md) supersedes the earlier
environment and gravity-download blockers. All six new full-manifest searches
fail; accepted prefixes and lunar force evaluation have separate numerical checks.
No full mission, hardware readiness or new publication is claimed.

## Prior disposition — 25 September 2026

The separately authorized visual publication is complete on GitHub, including
the browser-tested 2D fallback. The source for that fallback is reconciled here.
The new engineering batch stays local pending completion of the agreed work;
local companion synchronization is part of this checkpoint. The sections below
record the earlier 17 September stages and their then-current publication holds.
They are history, not a statement that the later visual publication never occurred.

New P92-S6 derives component loads, screens 20 spring geometries, integrates 162
catch cases and provides nine charger sensitivities. The first measurement budget
fails; P92-S6-R1 doubles gate spacing and passes the calculated budget. No hardware
calibration or shot is claimed. MC-L2-B0 now has a component ledger, draft assembly/
inspection/bench procedure and fail-closed speed-record evaluator. Selected material,
strength, detailed native CAD and actual test evidence remain open.

N6 retains 900 matched-assumption mass break-even cases and a ledger that marks
missing installed masses UNKNOWN. It is not a matched mission maneuver result.
C0-S3 freezes the lunar lifetime/coverage validation contract; coefficient access
timed out and no lifetime propagation was executed. Earlier missing revisions were
searched for in local objects and available archives but remain unrecovered.

Use [component requirements](MC_L2_COMPONENT_REQUIREMENTS.md),
[bench procedure](MC_L2_BENCH_PROCEDURE.md), [installed trade](INSTALLED_TRADE.md)
and [lunar validation contract](../validation/C0_S3_lifetime_coverage.md).

See the [checkpoint and exact verification limits](MC_L2_CHECKPOINT.md).

## Historical local-work boundary — 17 September 2026

At this stage, publication and companion export were held until the full plan
was complete. Local criteria commits preceded new calculations. The programme
was not complete.

## Source available in this working copy

This continuation began at VOLLEY 4335336 and BOLLEY 2f2e625. The newer revisions
previously reported in conversation, including VOLLEY 3f67f28 and BOLLEY ac89d5d,
are absent from the current object databases. Their previously linked recovery
archives are also absent. The cause of this workspace discrepancy is unverified.
I preserve surviving work. I do not claim that missing artifacts were restored,
that earlier tests have been repeated here, or that chat transcripts recover code.

S7, C0-S1 and the earlier S2 cell model remain present. Previously reported S8/S9/
S10, P92-S3/S4, N3/N5 and BOLLEY A6i/A9h outputs must be recovered from the original
archive or deliberately reproduced before they can be cited as current repository
evidence. Their reported findings remain useful leads, not substitute artifacts.

## Newly executed continuation

| Work | Output | Limit |
|---|---|---|
| P92-S5 | 25 mission-cartridge designs and 81 corners each; separate 0.5/1/2/3 m/s force-law candidates | 5 m/s has no candidate under unchanged limits; speed accuracy and hardware remain unverified |
| P113-S11 | 12 finite-burn/slew-constrained single-release studies, with replay and three replan seeds | Eight accepted at assumed 10/100 N; four 1 N searches fail; full manifest and real ADCS remain open |
| A6j-R1 | Seven yoke-only variants rejected | Lower winding stays 0.30 mm above separators, below the 0.5 mm assumed layout margin |
| A6j-R2 | Shared geometry, 0.25 mm winding lift and 2 mm yoke rise; three transverse STEP coupon references | 0.55/0.656 mm modeled clearances; no full winding, terminal or powered-coupon release |
| A6k | Six fresh actual-wire nonlinear meshes; both placements numerically pass | Powered-coupon promotion rejected: lower slot flux balance and upper stationary-core field fail |

Use [mission-cartridge results](MISSION_CARTRIDGES.md),
[finite-burn results](FINITE_BURN_DEPARTURE.md) and the
[current Fusion handoff](CURRENT_CELL_FUSION_HANDOFF.md).
The eight VOLLEY and four BOLLEY targeted tests pass. This does not restate the
previously reported 170-test result as a current full-suite run.

## Remaining work and dependencies

- Restore missing earlier evidence from the original checkpoint, keeping exact
  source identities and failures. Avoid spending resources on duplicate campaigns.
- Extend finite-burn control to the full evolving manifest, uncertainty and
  clearance. Provider thrust, attitude torque/momentum, navigation and operating
  permissions remain actual inputs to obtain.
- Turn the MC-L2 2 m/s force-law target into selected springs, guide, latch,
  charger/disengagement and catcher geometry. Off-axis dynamics, impact, rebound,
  tolerance, thermal/material behavior and actual installed accounting remain.
- Complete BOLLEY's same-configuration field/drive/thermal decision, including
  terminal/end geometry, current tracking, hot switching, protection, gap stack
  and electronics/structure mass. A rejected field candidate cannot inherit an
  older pass or become a powered-coupon release.
- AVM's native Fusion model, controlled drawings, BOM, interfaces and assembly/
  inspection work remain necessary. Calibration and independent review are
  required to release a named test article. No hardware measurement exists.
- Preserve the strict no-thruster, mission-limited customer boundary; validate
  actual demand and compare matched competent deployer/host baselines.
- Lunar and larger-payload concepts remain future work with their existing
  readiness gate. Carrier transport/capture, payload useful lifetime and separate
  end of life require connected mission analyses; separation speed cannot replace
  those obligations.
- Companion exports and full publication checks remain held. Do not weaken the
  companion freshness gate or treat a successful local study as programme closure.

## Retained implementation corrections

P92-S5 first reported an erroneous expected corner count of 243 rather than 81
(three values of four independent variables). Its first result is retained; only
the count/report changed. P113-S11 initially failed JSON output because a numerical
Boolean was not converted to a standard Boolean. The failure log is retained and
the same twelve cases were rerun; no acceptance band changed. A6j-R1's geometric
failure was retained before the separately committed R2 change.

## Final scientific disposition of this continuation

P92-S5 and P113-S11 numerical checks pass. A6j-R2 geometric checks pass, including
exact solid distances and the analytical core-volume increment. A6k completes
all six nonlinear meshes: both placements pass numerical checks, while the lower
placement fails slot flux balance (worst sampled mesh 0.094174 versus 0.05) and the
upper placement fails the stationary-core field limit. The selected geometry is
therefore explicitly rejected for powered-coupon promotion. No band was relaxed.

The next BOLLEY design task is a justified change to flux distribution and the
upper core field, followed by a newly declared geometry/drive check. Repeating the
same failed geometry or treating clearance alone as closure is not useful. The
current physical configuration is not a build-ready survivor.

## Verified local checkpoint

VOLLEY's focused continuation checks and eight targeted tests pass. BOLLEY's full
repository integrity check passes for 44 declared result files, including all
nine current tests. VOLLEY link/public-surface/site checks and authorship pass.
The full flagship gate is not claimed passing: the companion check reports stale
exports, which remain deliberately held. No GitHub write or export occurred.

The original P92-S5 count-failure source and A6j-R1 rejected source are preserved
under validation/source in their respective repositories; each matches the
SHA-256 recorded with the failed result. Archive copies are forensic snapshots
and retain their original relative-path assumptions. Restore them to their
original analysis paths in a separate checkout to reproduce the old run.

## Lunar-first visual continuation

C0-S2 adds connected ideal Earth-transfer/implied-arrival/capture accounting,
42 finite-host release cases and 18 carrier mass sensitivities. Numerical checks
pass, with no lunar lifetime or complete mission claim. Four concept STEP/STL
assemblies, five static 3D renders, six SVG/PNG engineering figures and a local
WebGL/orbit explorer are now present. See LUNAR_VISUAL_REVIEW.md and lunar.html.
MC-L2 stays the 80 mm mechanical-cell target; the native detailed CAD is pending.
BOLLEY's website now displays the retained A6k physical failures.

The earlier missing revisions remain unrecovered. The next technical work is
validated high-fidelity lunar lifetime/coverage and an epoch-targeted carrier
trajectory, followed by uncertainty, sequential releases and disposal. Current
cell parts, catcher, installed accounting and BOLLEY magnetic redesign also
remain open. This visual increment does not complete the previous batch.
Actual browser execution remains pending: the environment has no installed
browser and the browser download timed out. Stubbed UI checks cover only control
logic/data; static renders were inspected independently. No GitHub write,
companion export or deployment occurred.

The optional inherited pytest suite was not rerun in this increment because the
current environment has no pytest installation. C0-S2 standalone numerical,
artifact and UI-logic checks ran; no inherited full-suite pass is claimed.
