# First-test procedure · N5-R1

**Pre-test definition, 25 October 2026. No experiment has been performed.** This packet prepares subsequent Gen6 bench work after the completed ACR1 computational study. The numerical criteria in [ACCEPTANCE_R1.json](ACCEPTANCE_R1.json) are fixed before validation data. They are internal dummy/rig criteria, not flight or customer acceptance limits.

## 1. Scope and reference

C01 measures the field and force of a shortened one-period coupon. C02 checks one slow storage-to-pallet custody path and its inhibits. C03 checks a low-energy, ground-supported release and carrier arrest counterpart. These tests distinguish particular assumptions; none alone qualifies the full twelve-payload mechanism.

The [ACR1 geometry](../acr1/cad/release/FINAL_CAD_MANIFEST.json), [source/shot model](../acr1/analysis/COUPLED_SHOT.json), [design budgets](../acr1/analysis/DESIGN_BUDGETS.json) and [release-dynamics physical specification](../acr1_release_dynamics/PHYSICAL_TEST_SPECIFICATION.md) define the parent reference. The latter calls for measured contact, synchronization, actual keeper motion and a separately validated gravity/support model. This packet supplies the first bounded fixture, measurements and numerical decision rules.

The new coupon has six 8 × 90 × 8 mm blocks per array at 60° increments, with 12 mm nominal opposed gap. Its 7 × 80 × 6 mm copper bar is shorter than ACR1's active depth to clear keeper lips. The defined return wire is included in its force prediction. **Do not compare it with the full 216-bar phase coefficient.** The source model is free-space uniform magnetization; support perturbations, actual grade and joint current distribution require correlation.

## 2. Before assembly or power

Use the [BOM](BOM.csv), [definition](DEFINITION.json), [drawing](geometry/C01_fixture_drawing.svg) and [provisional STEP](geometry/C01_coupon_fixture.step). Purchased grades, fastener engagement, the load-cell gantry, insulation, guard and magnet insertion tooling are not released by that geometry. Obtain the actual load-path and material review and record the result before physical assembly. No purchase, fabrication authorization or supplier quotation is supplied here.

The free-space normal-attraction screen predicts approximately 362 N **on each array**. The declared 2× load screen is about 724 N per plate; its equal-share corner compression is about 181 N and keeper-bolt share about 60 N. The simple-beam plate screen predicts about 0.044 mm paired closure. Round the pre-test proof loads upward to 724 N per plate and 61 N per keeper support, with the same dummy contact topology and reviewed equal-share assumptions. After unloading, require permanent gap change plus uncertainty ≤0.02 mm, no joint slip and no cracked or displaced part. These are allocation checks, not a certified joint/lip/fixture solution; the actual review must also address unequal sharing and the lip/fastener load path. Mechanical magnet retention and an anchored guard must remain captive during insertion and inspection; a current limit does not limit the permanent-magnet assembly force.

For C01 use a source with compliance at most 5 V, a separate 4 A limit and an independent 50 ms timer. Bound output stored energy to 0.5 J, and account for at most 2 J total available electrical energy. At the limits, the supply contributes at most 1 J; the remaining reserve is not permission for an unidentified energy source. Verify current/voltage cutoff into a nonmagnetic dummy load first. **Do not connect the 86.4 V ACR1 bank:** its nominal stored energy is 23.328 kJ and it is outside this test definition.

No full-bank hot operation or environmental acceptance is included. The selected cell's standard −40…65°C window and 2.5 V/cell requirement at its 85°C catalog point remain separate source constraints. Any conditional thermal finding above the standard limit requires source-placement/contact and derating disposition before an expanded test.

## 3. C01 fixture assembly and inspection

1. Inspect both plates, four 28 mm corner spacers and the keeper strips against the drawing. Check the four Ø8.5 corner holes and all keeper holes. Record material, actual dimensions, fastener grade/engagement and the reviewed load path; do not infer them from appearance.
2. Mark each block's magnetization vector before insertion. With field axes X travel / Y gap / Z depth, use upper angles 90−60i degrees and lower angles 90+60i degrees, i = 0…5. CAD uses X travel / Y depth / Z gap. An ordinary four-block 90° Halbach sequence is a different article.
3. Use the reviewed captive insertion/jacking method and mechanical keeper lips. Keep the plates positively separated by the corner spacers. Record actual block seating and polarity. Adhesive alone is not the modeled retention method.
4. Inspect the **loaded** inner-face gap at each block and both depth ends: 11.9–12.1 mm after measurement uncertainty. Record the sign convention and probe active-volume offset. No powered measurement proceeds if the gap or retention is unproved.
5. Install the insulated copper bar on a force-decoupled, guided support. Its active ends are Y±40 mm. Route the return at Y±90 mm and Xbar+100 mm. The far return has an electrical terminal break; arrange paired source leads outside the strong field, with measured/bounded lead and support bias no greater than 0.0005 N.
6. Ensure the force sensor sees the complete current loop's X force and is isolated from the much larger array-normal reaction. Confirm travel stops and no rubbing through the planned X positions. Inspect clearance at the retaining lips; the bar itself ends before them.

A fixture drawing cannot close any of these as-built checks. Leave the inspection record blank until actual inspection.

## 4. Calibration and synchronized recording

| Channel | Calibration and allocated uncertainty | Acquisition |
|---|---|---|
| Signed normal field | Zero away from magnets; reference-field or traceable probe calibration; active-volume position ≤0.1 mm. Combined expanded uncertainty U95 ≤0.02 T. Record range, orientation and temperature coefficient. | Three unpowered repetitions at X = −20, −12, −4, 4, 12, 20 mm |
| X force | Five increasing/decreasing traceable load points over the used ±0.30 N region; zero before/after every pulse group. U95 ≤0.002 N, zero shift ≤0.001 N. Characterize lead stiffness and sensor cross-axis response. | ≥1 ksample/s; use the settled middle portion of the ≤50 ms pulse; retain raw transient |
| Current and voltage | Calibrated shunt/meter, four-wire connection where applicable; current U95 ≤1% of reading. Verify saturation, offset, pulse width and integral of V·I. | ≥10 ksample/s on common clock |
| Slow mechanism position | Calibrated scale/encoder; U95 ≤0.02 mm for custody dwell. Optical proof of both independent capture channels. | ≥1 ksample/s for motion/proof channels |
| C03 speed | Independent optical-gate baseline 200 mm, baseline error bound ≤1 mm; each event timestamp bound ≤0.1 ms. Cross-check with calibrated video. | At 0.2 m/s, allocated U95 about 0.0012 m/s; criterion ≤0.002 m/s |
| C02 push / C03 brake and drag | Separate ranges: 0–100 N push, 0–5 N brake (U95 ≤0.05 N), and 0–1 N drag (U95 ≤0.02 N). The guarded brake interval must stay within 1.5–2 N. | Common-clock slow recording; do not overload the ±1 N coupon cell |
| C03 relative pose/contact | Calibrated scale for carrier/payload coordinates; U95 of relative aft coordinate ≤10 mm. Rear-contact force U95 ≤0.05 N; event threshold 0.2 N. | ≥1 ksample/s through 6 s; identify missed/saturated events |
| Temperature | Calibrated contact probe on conductor and magnet support; record ambient before each run. | Begin at 18–22°C; stop conductor current at 40°C |

The [prediction file](PREDICTIONS.json) computes an RSS allocation using independent rectangular error terms and coverage factor 2. These are design budgets, not calibration certificates or a statistical repeatability result. Add actual certificate, alignment, hysteresis, drift, finite bandwidth and timing terms before reporting U95. Correlated systematic terms require covariance or conservative addition; do not apply RSS automatically.

The normal-field comparison uses signed CAD-Z field, not the vector magnitude. At zero-crossing points use the absolute floor in the criterion. Force is **Kloop × measured signed current**; include the return contribution. The main field model predicts about −0.044900 N/A at X−20 mm and +0.067845 N/A at X+4 mm. Current reversal is part of the predefined matrix, not a post-test choice.

## 5. C01 field and force runs

Complete the readiness/inspection/calibration record. Scan the six field stations three times without current. Then measure X = −20 and +4 mm at signed currents −4, −2, −1, +1, +2 and +4 A, five repetitions each. Retain all 60 pulse records. Verify ambient/temperature, zero, gap and source energy before each group. The true measured current belongs in the comparison; a setpoint alone is insufficient.

For field, accept only when `|Bmeas−Bpred| + U95 ≤ max(0.02 T, 15%|Bpred|)`. For force use `|Fmeas−Kloop·Imeas| + Uresidual ≤ max(0.005 N, 15%|Kloop·Imeas|)`, with `Uresidual = sqrt(Uforce² + (Kloop·Ucurrent)²)` for independent terms; include covariance or conservative bounds where needed. Br = 1.32 T ±3% is an input allocation: without a material certificate or an independently identified remanence, retain results as characterization rather than a validated nominal-model pass.

If uncertainty overlaps the band, record **inconclusive** and rework metrology. A residual outside the band after calibration checks is a failed correlation, preserved against the frozen model. Stop on fixture movement, rubbing, loss of retention, exceeded energy/current/time/temperature, sensor overload or unexpected force sign. Do not raise the limits to obtain a favorable trace.

## 6. C02 one-cell transfer and custody proof

Use the actual selected ACR1 pusher, pallet feet, capture caps, two keyed pallet locks, lift grip pins and keeper interfaces. Hold the receiver at one fixed level for the first test. A single-cell support and protective enclosure remain required fixture details; the full 784 mm vertical lift and twelve-cell sequence are excluded. Ground gravity and friction are measured loads, not the orbit-coast sizing case.

Use an inert 4.000 ±0.005 kg, 340.5 ×100 ×100 mm surrogate with identified contact faces. With source power disconnected, verify each holder and the independent proof channels. A handwheel or external actuator must be force limited: ≤25 N commissioning push, immediate stop if force reaches 30 N. Transfer 250 mm in at least 40 s with speed ≤11.71875 mm/s. Manual bounded motion does not validate the exact quintic servo profile or catalog motor dynamics.

Establish receiving containment before pusher withdrawal. At docking, land the feet, close/lock the upper caps, insert both bayonet shafts 12 mm and rotate 90°. Prove capture before withdrawing both lift grips 26 mm. Hold each critical custody state for 10 s under the 4 kg gravity load and a separately applied 20 N horizontal proof load in ±X/±Y. Accept only with ≤0.1 mm motion after uncertainty and no loss of custody. This is a first bench proof, not a launch-restraint load test.

Replay all 24 nominal command/proof transitions with motion/current inhibited; mechanically witness only the slow transfer and pallet custody states in C02. The firing/arrest/return transitions in this replay are controlled logic inputs, not completed mechanical shots. Use the [source state specification](../acr1/analysis/TRANSFER_INTERLOCKS.json). Inject power-loss indication, jam, sensor disagreement, timeout, false host-coast proof, one missing capture proof, home-pin-not-clear and half-open keeper. A logical proof test may use controlled sensor inputs; distinguish it from an actual mechanical fault experiment. Positive launch permission must remain false whenever a required proof is absent. Fault reset requires independently re-proved custody and clear path. No automatic continuation around a jam is accepted.

For partial keeper opening, use a 6 mm mechanical witness and demonstrate detection/inhibit with the drive disabled. **No dynamic half-keeper catch is authorized by this packet.** The numerical fault angular rate is solver/contact sensitive and is not a hardware rating.

## 7. C03 low-energy planar release/arrest counterpart

This is a separate ground-rig case. It does not replay the 3 m/s electromagnetic launch or validate LSM braking. Use the source carrier/pallet/cam geometry, measured carrier mass 13.1278 ±0.05 kg and the 4 kg surrogate. A rolling or planar air-bearing support must give measured payload drag **plus uncertainty ≤0.1 N** across the complete corridor. Ordinary sliding at illustrative μ=0.1 gives 3.923 N and fails this condition. Include support forces and constrained axes in the counterpart model.

Use a calibrated external bench brake with **total opposing carrier force, including guide/support drag, 1.5–2 N**, an independently proved passive catcher of at least 1 J capacity, a guarded corridor and a separate emergency stop. The source remains unpowered. The external bench brake is test equipment, not a selected substitute for ACR1 LSM arrest. Define all added guide, support and catcher geometry before execution; the C01 STEP is not a drawing of this full rig.

First conduct disabled-drive pull-through and keeper/cam witness checks. Verify 12 mm opening is complete by carrier-aft X1495 mm, before X1500 mm release. Both the inspection uncertainty and the full 5 mm margin must be accounted for. Commission at 0.05 and 0.1 m/s; then run ten final nominal trials at **0.195–0.205 m/s**. Bound loaded mechanical energy to 0.5 J. Never use an intentionally obstructed keeper for the dynamic trial.

Record carrier and payload coordinates, keeper displacements, rear force, support/brake force and speed on one clock through 6 s. The source payload aft starts 64 mm ahead of carrier aft; the clearance criterion is an absolute **payload-aft minus carrier-aft coordinate**, not an ambiguous displacement from zero. Require stop distance +U95 ≤0.210 m and relative aft coordinate −U95 ≥0.5245 m by 6 s, with no detected keeper/pallet recontact. The latter includes 10 mm beyond the represented 0.5145 m source extent; an actual added obstacle farther downstream invalidates that envelope.

The nominal counterpart predicts 0.3426 J loaded kinetic energy, 0.2626 J retained-carrier energy and 0.1750 m stopping distance at 1.5 N. With 0.1 N payload drag it predicts about 0.639 m relative aft coordinate at 6 s, including the initial 64 mm offset. These are analytic rig predictions, not measured release performance. Actual measured inputs must be characterized on commissioning data, then frozen before the separate final validation trials.

Stop immediately on recontact ≥0.2 N, a missing event/proof, speed/energy/drag/brake limit violation, approaching the catcher limit, unproved clearance or loss of synchronization. Do not continue through powered return: the present computational departure study and this test stop before that phase.

## 8. Contact compliance, uncertainty and later tests

The source four-rail axial stiffness is 51.817 MN/m; 26.8635 N compresses it only about **0.518 µm**. Calipers, millimetre scales and ordinary video cannot validate that compliance or its 6.96 µJ stored-energy/tip-off bound. To attempt correlation, require displacement U95 ≤0.05 µm, identified pads/rail finish/preload, a 0–27 N force calibration, four/two/one-contact cases and separate fit/validation traces. If that metrology is unavailable, retain compliance as unmeasured; C02/C03 do not close the contact-parameter or physical-repeatability criterion.

The source specification's 20 kframe/s example concerns finer release-event discrimination. The slower first-rig measurements above use a different temporal scale. They do not resolve the original 5–25 µs dynamics or establish full six-DOF tip-off, vacuum friction, hot operation, endurance, environmental qualification or provider acceptance. Those retain their existing source-specific requirements.

## 9. Record and disposition

Use the header-only [time-series template](templates/raw_timeseries.csv), [run record](templates/run_record.json) and [inspection template](templates/inspection.csv). Preserve instrument files, calibration certificates, initial-state photographs, as-built dimensions, all adverse trials and the original model/criteria hashes. Empty templates are not data.

A pre-test calibration/identification dataset may determine the rig's measured inputs. Freeze those inputs before viewing separate validation data; do not fit and validate on the same trace. Report each trial as pass, inconclusive, failed or stopped with the actual uncertainty and scope. A successful limited coupon or planar trial supplies no full-system or flight acceptance. Any change to geometry, model or limits creates a new issue without deleting the original result.
