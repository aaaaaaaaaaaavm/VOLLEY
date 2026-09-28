# MC-L2-B0: instrumented coupon procedure, draft A

Adityavardhan Mishra · 25 September 2026

**Disposition: review package only; hardware test release withheld.** This names
the intended article and makes its acceptance repeatable. It does not mean that
an article exists. Complete the component ledger, drawings and facility review
before assembly or stored-energy operation. Current concept solids are packaging
references and must not be treated as released machining drawings.

## Article and configuration record

Use article ID MC-L2-B0 plus a serial number. Record the exact source commit,
drawing revisions, each part/lot, spring certificates, measured pusher/payload
mass and CG, guide alignment, latch, disengagement mechanism, catcher, fixture,
instrument serials, calibration dates, ambient conditions and operator. Identify
every substitution as a new configuration. Keep launch restraint and release
latch separate. The 4 kg payload is a captive dummy in the reviewed test enclosure;
flight payload rails and mounts remain an external ICD dependency.

## Inspection and release gates

1. Independent reviewer signs structural fixture, mounts, stops and containment
   against the declared stored energy and all reviewed reaction loads. The
   numerical planning allocation is not a proof-test authorization.
2. Inspect springs individually: wire/diameter/turns/free length, seating, force
   at charged and released lengths and at intermediate deflections. Measure
   loading/unloading hysteresis and permanent set. Record actual force curves;
   reject using catalog nominal stiffness as a measured curve.
3. Inspect all swept clearances at pusher positions 0, 40, 80 and 100 mm, including
   latch, screw coupling, cables, guide seats and catcher. Hand-traverse unloaded.
   Record minimum clearances and measurement uncertainty; no arbitrary clearance
   becomes an accepted tolerance without the drawing review.
4. Measure breakaway and moving friction through the stroke with the real guide,
   orientation and lubrication. Use traceable force and position sensors. Confirm
   measured moving mass; include spring inertia in the dynamic model if material.
5. Verify physical charger disengagement and independent clearance indication.
   A software command is not evidence of clearance. Demonstrate blocked-release
   behavior for missing charge, latch, enclosure or coupling-clear signals with
   energy isolated. Define manual safe recovery before enabling stored energy.
6. Verify positive pusher capture and anti-rebound retention without a payload
   first under the approved incremental-energy commissioning plan. Inspect wear
   and catcher travel after each commissioning event. No full-charge operation
   until the responsible reviewer signs the actual commissioning results.

## Instrument plan and the retained uncertainty failure

Two exit gates measure dummy translation after pusher separation. R1 changes
spacing from 100 to 200 mm. With standard spacing uncertainty 0.10 mm and interval
uncertainty 10 us, RSS propagation and coverage factor 2 give expanded uncertainty
0.006997 m/s at 6 m/s, below the unchanged 0.01 m/s target. These are required
instrument capabilities, not calibration results. Allocate the remaining budget
to alignment, trigger threshold, target edges and sampling; measure them. The
100 mm design's 0.013994 m/s failure remains archived.

Use synchronized pusher position, gate timestamps, latch/coupling states and
catcher load/acceleration channels. Select force bandwidth and sampling from an
observed low-energy transient and a reviewed anti-aliasing study; no invented
sample rate certifies peak shock. Video or a third gate supplies an independent
velocity check. A single axial gate pair cannot measure tip-off: track at least
two dummy fiducials with calibrated imaging, record angular rate and flag the
missing mission tip-off acceptance allocation.

## Nominal characterization

After commissioning and calibration, execute twenty consecutive nominal shots
of the SAME configuration. Do not discard outliers. Record each raw file's hash,
input measurements, model-predicted speed, measured speed and uncertainty,
pusher capture, peak/impulse, stroke, reset behavior and post-shot inspection.
The fixed fixture's nominal ideal speed is 1.987637 m/s, not the finite-host
2.000000 m/s; recompute from measured work and mass for each configuration.

For this coupon planning gate, every shot must be within 0.10 m/s of its own
measured-input energy prediction, and the sample standard deviation of measured
speeds must be <=0.03 m/s. Expanded velocity uncertainty must be <=0.01 m/s.
A missing calibration, missing raw file or unreviewed configuration blocks a pass
regardless of speed. Evaluate with `python analysis/bench_acceptance.py run.json`.
The input format is in `validation/bench/MC_L2_RUN_TEMPLATE.json`; empty fields
are deliberate, and the template must fail. Model bias, repeatability, catch,
tip-off and fixture safety are separate decisions; a speed pass is not article
release. No physical tests have been performed.

## Stops and disposition

Stop the sequence for failed capture, recontact, unexpected motion, damaged
parts, lost sensor synchronization, exceeded reviewed force/travel/temperature
or failed interlock. Isolate energy by the reviewed procedure before inspection.
Retain every failed shot and deviation. A changed spring, catcher or gate setup
requires a new configuration and documented rerun scope. Thermal/vacuum, dwell,
cycle-life, vibration/shock and off-axis campaigns remain separate future gates.
