# Tests that discriminate the remaining release models

**Prepared 25 October 2026.** This is a test specification, not an authorized build, purchase, provider exchange or record of measurements. Physical limits must come from the chosen spacecraft/host ICD; the numerical pose screens below do not supply them.

## 1. Measure the contact model before using a predicted tip-off rating

Use the actual rail-end/pad materials, finishes, contact geometry and preload. Measure axial force versus relative displacement and unloading hysteresis over the source-relevant range, including the modeled 26.8635 N maximum payload reaction. Repeat with four, two and one effective rail contacts and controlled contact-height/COM offsets. Measure friction under the actual normal load and release speed; measure rebound and ring-down rather than selecting damping to make the result settle. Include temperature/lubricant/vacuum conditions required by the eventual application.

The discriminating measurements are compliance, load sharing, contact impulse, unloaded residual deformation and material/interface restitution. MuJoCo acceleration-stiffness values are not directly material N/m values. Correlate a measured contact experiment in the solver before mapping them to the release model. Reserve separate data for validation after fitting; do not fit and validate against the same trace.

## 2. Verify the nominal mechanical departure sequence

Use the same captive pallet, rear pads, cap gaps, forekeeper ramp and geometry revision. Instrument carrier position/velocity, individual keeper displacement, rear-pad force and motor/source signals on one synchronized clock. Verify the 12 mm keeper opening is complete by carrier-aft X1495 mm, before X1500 mm release, and confirm that the pallet remains with the carrier through arrest.

Use calibrated stereo imaging or equivalent pose metrology to recover payload position/orientation and six-state departure motion. A proposed 20 kframe/s witness gives 50 µs timing intervals comparable to the principal event refinements; spatial calibration and exposure must resolve the model differences being tested. A separate time-of-flight baseline is needed for velocity uncertainty. Specify camera scale, synchronization and beam spacing from the uncertainty budget; frame rate alone is not velocity accuracy.

Ground suspension or planar air bearings introduce constraints and forces. Measure and include them in the counterpart model. A planar rig can discriminate yaw/contact timing but cannot certify out-of-plane six-DOF release. A full six-DOF conclusion needs appropriate microgravity or independently bounded gravity-compensation effects.

## 3. Adverse and model-discrimination cases

Compare aligned launch-ready conditions with measured offsets/tilts, known initial rates, asymmetric rail preload and partial keeper opening. A partial-opening branch should first demonstrate detection and inhibited launch using controlled low-energy mechanism motion. It must not be treated as an acceptable commanded high-speed release.

Record first and last rear contact, later floor/cap/keeper impulses, rebound, payload tip-off vector and closest subsequent clearance through carrier arrest. Track capture and release observables separately; endpoint arrival is insufficient. Continue through powered return only when an actual return profile and safe departure corridor are defined. The present numerical study stops before that phase.

At each operating point retain repeated shots, raw sensor traces, calibration records, zero/load checks, environmental state and initial assembly pose. Report sample distributions and uncertainty only after actual repeated trials; a deterministic parameter sweep is not a repeatability distribution. Resolve single-cell/whole-system shared-path exposure separately from per-shot variability.

## 4. Acceptance and decision

Before tests, obtain approved payload shock, sustained load, magnetic exposure, tip-off and velocity/state tolerances, and host attitude/recoil/corridor requirements. Freeze analysis and comparison metrics before reading validation data. Report results against those requirements with instrument uncertainty and missed-event limits.

A useful discriminating outcome can be a no-go: observed keeper contact, pad-asymmetry response or recontact inconsistent with the model identifies which assumption must change. Successful nominal shots alone cannot establish worst-case safety or flight qualification. This specification closes test preparation, not physical validation.
