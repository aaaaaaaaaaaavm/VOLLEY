# FM08-R3 feeder architecture selection and analytical verification

**Evidence study:** FDR10-R0. **Selection rule:** D27-R2. **Configuration:** two dedicated 1U cells, two dedicated 3U cells and one indexed reusable receiver.

## 1. Design decision

Select a guided lead-screw transfer mechanism for the academic mechanical design baseline. Retain rack-and-pawl transfer as the runner-up. Each storage cell has its own reversible pusher drive and normally retained payload boundaries. The pusher does not pull or command payload deceleration. The receiver far stops are proved closed before the storage gate opens; the continuous capped channel contains low-friction payload drift until sensed seating and verified near-tab capture. The receiver indexes to a cell, establishes docking and empty-receiver proof, accepts the payload within a continuously capped transfer channel with verified far-stop containment, closes its retention features, and permits launch preparation only after the feed pusher has withdrawn, the storage gate is closed and the dock pins are retracted, and the split index-clutch disengagement is independently proved. Return indexing requires external stopped-sled proof and proved clutch reengagement.

The 1U length accommodation is a fixed cassette spacer. It remains in the storage cell. Retractable receiver stops distinguish the 1U aft datum from the 3U envelope, while the leading datum is common. No loose spacer is carried into the launch trajectory.

D27-R2 permits an academic architecture selection using a documented trade, selected-design nominal CAD/STEP, analytical sizing, declared tolerance screens and executable sequencing/fault checks. It supersedes the earlier requirement for complete qualification-level comparison of all seven concepts. The original FDR09 geometries, interference results and contact-model findings remain historical evidence. This selection does not change their results.

## 2. Declared requirements and evidence boundary

| Item | Declared basis |
|---|---|
| Inventory | Two 1U and two 3U passive CubeSat envelopes |
| Common interface | One reusable receiver; fixed leading datum; dedicated storage cells |
| Local transfer | 200 mm in 30 s; triangular speed command |
| Receiver indexing | 900 mm in 20 s; triangular speed command |
| Resistance | 50 N nominal sizing assumption; 100 N adverse screen; neither measured |
| Moving mass | 7.5 kg local / 10 kg receiver sizing assumptions |
| Fault policy | Inhibit release, retain/contain payload, stop, isolate only with independently verified clear path, supervised recovery |
| Prototype environment | Manufacturer ambient catalog references; no flight or vacuum qualification inferred |
| Dynamic evidence | Prescribed kinematics and analytical demands; original unconverged rigid-contact predictions excluded from precision and peak-load acceptance |

These are mechanical design-study requirements. Repeatability, friction, latch engagement, brake dynamics, vibration, thermal-vacuum performance, EMC, host approval and mission reliability require hardware or provider-specific evidence.

## 3. Weighted architecture trade

The scoring dimensions are safety/fault control (35%), packaging/mass (25%), positioning/custody (20%), cycle/power (10%) and manufacturability (10%). Scores are engineering judgments from documented mechanism features and current evidence. They are not reliability measurements or probabilities.

| Rank | Architecture | Safety | Packaging | Positioning | Cycle/power | Manufacture | Weighted / 10 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | lead screw | 8 | 6 | 8 | 6 | 8 | 7.30 |
| 2 | rack pawl | 7 | 7 | 7 | 8 | 7 | 7.10 |
| 3 | spring dual gate | 6 | 8 | 6 | 8 | 8 | 6.90 |
| 4 | belt shuttle | 6 | 8 | 6 | 7 | 7 | 6.70 |
| 5 | indexed drum | 6 | 8 | 6 | 6 | 5 | 6.40 |
| 6 | telescopic | 6 | 7 | 6 | 5 | 5 | 6.05 |
| 7 | pantograph | 5 | 7 | 5 | 5 | 5 | 5.50 |

### Top-three engineering comparison

| Attribute | Guided lead screw | Rack and pawl | Spring and two gates |
|---|---|---|---|
| Transfer control | Reversible guided pusher; one-way payload transfer to a far receiver stop | Reversible toothed drive; pawl for retention/indexing | Stored-energy push; position depends on gates/governor |
| 50 N feed demand | Source-backed motor/gear sizing at 200 mm / 30 s | Source-backed drive option exists; installed tooth/support detail remains | Existing 15 N end-force assumption fails; spring must be resized |
| Position custody | Capped channel, proved far stops, sensed seating and near capture tabs; rear pusher brake | Requires controlled tooth engagement, anti-backdrive and receiver retainers | Requires two-gate interlocks, governed transfer and stored-energy containment |
| Principal engineering risk | Alignment, lubrication, nut wear, support and brake integration | Backlash, tooth/root load, skipped engagement and pawl jamming | Uncontrolled release, spring-force variation, gate timing and reset energy |
| Packaging and reset | Four local drives; slower but directly reversible reset | Potentially compact and faster, with more local engagement detail | Compact store and low powered-feed demand; rewind and governing add parts |
| Decision | Selected for controllability and available sizing evidence | Retained runner-up | Retained alternative after spring/governor redesign |

### Common-boundary numerical comparison of the top three

All three are evaluated for 200 mm transfer in 30 s with a 7.5 kg moving-mass assumption. The nominal and adverse resistance cases are 50 N and 100 N. The ideal resistance work is respectively 10 J and 20 J; actuator, gearbox, spring hysteresis, reset and control losses are additional.

| Architecture / reference | 50 N motor torque / N·m | 100 N motor torque / N·m | Peak motor speed / rpm | 50 N / 100 N modeled current / A | Interpretation |
|---|---:|---:|---:|---|---|
| Guided 10×2 screw, 9:1 gear | 0.014848 | 0.026275 | 3600.0 | 0.4476 / 0.7237 | Source-based sizing and selected guided CAD |
| Rack, 12 mm pinion, 59.4:1 gear | 0.020219 | 0.040421 | 630.3 | 0.5774 / 1.0653 | Conditional drive reference; teeth/support/retention require detail |
| Spring and two gates | — | — | — | — | Existing 15 N end force reaches 30% / 15% of the two force demands |

The spring requires at least 50 N or 100 N at the low-force end of its stroke, plus inertia and appropriate allowances, corresponding to 35 N or 85 N increases over the historical 15 N assumption. Its stored energy must exceed the 10 J or 20 J resistance-work floor; a governor/capture system must control low-resistance motion, and reset must restore that stored energy. These are redesign requirements, not ratings attributed to a spring that has not been selected. The rack reference passes the same conditional motor screens but does not resolve its mesh, backlash and support details. The selected screw is therefore justified by controllability and available corrected geometry rather than an assertion that the alternatives cannot function.

### Decision sensitivity

The 0.20-point lead over rack and pawl is small. Equal weights produce a three-way tie at 7.20. Safety-emphasis weights favor the lead screw (7.60); packaging/mass-emphasis weights favor spring and two gates (7.30); cycle-emphasis weights favor rack and pawl (7.35). The choice is therefore a defensible engineering compromise for the declared safety-led requirements, rather than a unique numerical optimum.

A reproducible 10,000-scenario perturbation changes each judgment score independently within ±1 point. Winner counts are reported only as sensitivity of the decision to scoring uncertainty; they do not estimate hardware success probability.

| Architecture | Perturbation winner count / 10,000 |
|---|---:|
| lead screw | 6116 |
| rack pawl | 2648 |
| spring dual gate | 931 |
| belt shuttle | 290 |
| indexed drum | 15 |
| telescopic | 0 |
| pantograph | 0 |

## 4. Drive sizing

The local reference is FAULHABER 3242G024BX4 with 32GPT 9:1 gearing and MC5005S control. The common receiver uses a toothed-belt indexer with a 12 mm pitch-radius pulley and a split clutch. It uses the same motor family with nominal 59:1 gearing (actual ratio 59.4). The higher receiver ratio replaces the earlier 29.7 option to provide useful nominal torque margin and accommodate the declared 100 N adverse screen. Catalog motor continuous torque is 0.0418 N·m. Gear efficiency is assumed to be 0.50; published maximum efficiency is not a guaranteed lower bound.

For a triangular speed law, peak acceleration is 4s/T² and peak speed is 2s/T. Screw raising torque uses the trapezoidal-thread equation with a 9 mm mean diameter, 2 mm lead, 15° half-flank angle, assumed friction coefficient 0.15 and an additional 0.015 N·m bearing-drag allowance. Reflected rotor and gear input inertia are included. Each case is evaluated at 1,001 time stations.

| Motion | Resistance / N | Time / s | Peak motor torque / N·m | Peak motor speed / rpm | Peak modeled current / A | Shaft speed / rpm | Declared sizing screens |
|---|---:|---:|---:|---:|---:|---:|---|
| local feed | 50 | 30 | 0.014848 | 3600.0 | 0.4476 | 400.0 | Pass |
| local feed | 100 | 30 | 0.026275 | 3600.0 | 0.7237 | 400.0 | Pass |
| common receiver | 50 | 20 | 0.020381 | 4254.2 | 0.5813 | 71.6 | Pass |
| common receiver | 100 | 20 | 0.040583 | 4254.2 | 1.0693 | 71.6 | Pass |

The checked limits are motor continuous torque, the ambient 24 V torque-speed line, gear input speed, gear output torque/power, controller continuous current, and the supplier-based screw-nut load/speed screen. The 400 rpm local screw speed is below the 1,000 rpm conservative nut screen; 100.007 N peak axial load is below its 155 N study limit. This does not establish lubrication life or space suitability.

## 5. Static and tolerance screens

A pinned-pinned Euler screen for the 7.4 mm screw root over a 350 mm supported span gives 2371.9 N critical load, a capacity-to-study-load ratio of 23.72 at the 100 N adverse transfer condition. Calculated axial shortening is 0.00407 mm. The end support is idealized; bearing alignment and fatigue are separate hardware details.

Two 6 mm restraint pins, each in double shear with ideal equal load sharing, and four 5 mm bearing lugs are screened using declared 50 MPa allowable shear/bearing stresses. These values are study assumptions, not certified material allowables. The payload force is applied to the retained carrier interface; spacecraft rails/contact surfaces and host fasteners require their own local load assessment.

| Provisional acceleration | 6 kg payload force / N | Pin capacity / applied load | Lug bearing capacity / applied load |
|---:|---:|---:|---:|
| 5 g | 294.200 | 19.221 | 20.394 |
| 10 g | 588.399 | 9.611 | 10.197 |
| 25 g | 1470.997 | 3.844 | 4.079 |

Including a 7.5 kg retained payload-and-carrier study mass at 25 g gives 1838.747 N and a pin capacity-to-load ratio of 3.075. These are preliminary static checks; load sharing, local contact, bending, joints and fatigue remain outside the simple pin/lug equations.

The corridor screen starts with a 2 mm nominal side/top allowance. It conservatively sums a 0.25 mm manufacture/assembly stack, 0.1° relative yaw over a 170.25 mm half-length, differential thermal expansion over 200 mm for 60 K with 11 µm/(m·K) CTE mismatch, and simply supported 8 mm steel guide deflection. It applies to the declared channel direction; it does not qualify bearing fits, end barriers, payload acceptance gauges or an unspecified host thermal field.

| Total transverse study load / N | Guide deflection / mm | Summed consumption / mm | Remaining nominal allowance / mm |
|---:|---:|---:|---:|
| 10 | 0.0931 | 0.7722 | 1.2278 |
| 50 | 0.4655 | 1.1446 | 0.8554 |
| 75 | 0.6982 | 1.3773 | 0.6227 |

## 6. Power loss, containment and recovery

The design does not use screw self-locking as a safety argument. A normally engaged brake retains the rear pusher boundary, while fixed channel caps, rear containment and proved far receiver stops bound possible payload drift. Power loss invokes stop-and-contain with supervised recovery. The payload may coast inside that volume; the model does not establish its deceleration, impact load or final pose. The reference 0.12 N·m brake exceeds the ideal frictionless backdrive torque of 0.04934 N·m at 155 N by a factor of 2.43. The receiver separately uses a 2 N·m static-brake reference (BXW-05-10L), exceeding the 100 N × 12 mm pulley radius = 1.2 N·m static holding demand by a factor of 1.67. These are static holding comparisons only; shaft adapters, response, impact, wear and thermal-vacuum performance remain hardware verification tasks.

Peak prescribed feed speed is 13.333 mm/s. Travel during an assumed 50 ms sensing/control latency is 0.667 mm and moving kinetic energy is 0.000667 J. These describe the prescribed pusher motion. They are not bounds on a freely coasting payload impact, an emergency stopping distance or a measured contact load.

A bridge jam inhibits every operation using the shared transfer path. A retained failed cell may be isolated only after independent path-clearance proof and explicit supervised recovery. No automatic continuation is permitted after power restoration or contradictory sensors.

## 7. Executable sequence and fault logic

The stdlib state model executes a persistent four-cell campaign with continuous transfer-volume containment and verified seated capture, docking proof, empty-receiver proof, storage-gate closure, release inhibition, single-release behavior, empty-carrier return, home proof and guarded next-cell reset. A separate persistent campaign isolates one securely retained failed cell after explicit proofs and processes the remaining three cells. Clutch disagreement inhibits operation; launch cannot arm with an engaged or unproved clutch. Empty return cannot index until clutch engagement and external launch-module stopped status are proved. The receiver FAR-side stops are independently proved closed before the storage gate opens. PROVE_SEATED is an external seating/settling proof; CAPTURE denotes verified NEAR-tab closure before pusher withdrawal. No simulated pusher position substitutes for that payload proof. Fixed 1U spacers remain in their cells. The model does not claim to emulate actual sensors or qualify software for flight.

| Check group | Enumerated cases | Result |
|---|---:|---|
| Persistent 4-cell campaign with empty return and reset | 4 | Pass |
| Fault injection at every campaign phase including return | 920 | Pass |
| Unsafe commands and unsupervised recovery rejected | 27600 | Pass |
| Every command applied at every campaign state | 3999 | Pass |
| Repeated release cannot double feed | 10 | Pass |
| Failed-cell and bridge-isolation guards | 2 | Pass |
| Blind next-cell reset and missing proof rejection | 16 | Pass |
| Occupied receiver cannot be accepted as returned empty | 144 | Pass |
| Verified-path failed-cell isolation then persistent remaining campaign | 1 | Pass |
| Coast-only transfer, far-stop proof and host-off launch interlock | 3 | Pass |
| Five-second host-off guard, premature-arm rejection and restart reset | 10 | Pass |
| Index-clutch disengagement before launch and proved engagement before return | 68 | Pass |
| Continuous containment, far-stop proof and sensed seating before capture | 44 | Pass |

All 32,821 enumerated logic cases pass. Injected events include power loss, jam, sensor disagreement, timeout and a double-feed request throughout the persistent four-cell campaign, including empty return and reset. An open-gate, unseated or transfer-volume fault cannot be cleared by a software path-clear assertion. Recovery requires a mechanically retained cell behind a closed gate or a proved receiver clamp; otherwise supervised retrieval and fresh position evidence are required. Physical latch engagement and truthful independent sensor agreement are explicit contracts of this logic model, not results established by it.

The expanded twelve-cell manifest repeats [1U, 3U, 1U, 3U] three times. One persistent inventory executes all twelve releases, returns and guarded resets; 98,325 enumerated logic cases pass. A separate fault campaign isolates one retained cell and processes the remaining eleven. These logical checks complement the separate detailed CAD, installed-mass and mission evidence.

### Coast-only transfer and launch interlocks

Payload transfer is thrust-off/coast only. An empty receiver can be docked and its far stops proved before a release opportunity, but the storage gate cannot open while thrust is active. A burn starting during open-gate transfer inhibits operation. The payload may move freely inside the closed transfer volume under low friction; final seating and settling must be sensed before the near capture tabs close and the pusher returns. Launch arming and release additionally require at least 5 s of uninterrupted verified host thrust-off status, a new stable-attitude proof and split-clutch disengagement proof. The one-second model clock resets after a burn restart. The matched feeder timeline must provide a coast window; no feed-during-burn claim is made.

## 8. Feeder subcycle duration and resource accounting

A conservative local feed-and-return allocation is 60 s and receiver index-and-return allocation is 40 s. With an assumed 8 s total gate/latch/seating allocation, the modeled feeder subcycle is 108 s per payload or 432 s for four payloads. Electromagnetic launch, braking, orbit-target waiting, host attitude recovery and charging are outside that feeder-only allocation.

For the twelve-cell extension, the full receiver travel is 3,500 mm. Retaining the same prescribed peak speed gives 77.778 s per full-stroke index. The conservative feeder-only allocation becomes 223.556 s per payload and 2682.667 s for twelve. This is a conditional sizing allocation. It assumes seating is proved within the allocated dwell and external launch/braking completes separately; a seating timeout aborts the cycle. It is not a measured throughput or a complete coupled mission timeline.

The five primary controller standby currents sum to 7.2 W at 24 V. Four local motor/gear/controller/static-brake reference sets total 3.064 kg; a receiver set using the 59.4 gearbox and 2 N·m static-brake option totals 1.409 kg, giving a 4.473 kg primary-drive catalog subtotal. Gate/receiver-retainer actuation, brackets, connectors, harness and thermal mounts must remain separately identified in the CAD/BOM accounting. Catalog mass is not additional CAD solid mass where an envelope already represents the same part.

## 9. Evidence disposition

The selected design is a computationally documented academic mechanism with a declared nominal operating case and bounded adverse screens. Original FM06-R1 rigid-contact endpoint convergence remains unestablished. Those runs are not used to claim release accuracy, contact-force peaks, latch loads or FM08-R3 dynamic validation. No experimental test, qualification, supplier confirmation, provider approval or independent technical endorsement is implied.

## 10. Reproduction and sources

Run `python verify_feeder.py --no-plots` for the deterministic stdlib calculations and logic checks. Run `python verify_feeder.py` with Matplotlib installed for publication plots. `check_capture.py` verifies capture hashes and repeats the stdlib calculations in a temporary directory. Geometry and STEP readback are provided by the companion FM08-R3 CAD evidence package.

- FAULHABER 3242 BX4 motor data: https://www.faulhaber.com/fileadmin/Import/Media/EN_3242_BX4_DFF.pdf
- FAULHABER 32GPT gearhead data: https://www.faulhaber.com/fileadmin/Import/Media/EN_32GPT_FMM.pdf
- FAULHABER MC5005S controller data: https://www.faulhaber.com/fileadmin/Import/Media/EN_MC5005S_DFF.pdf
- Thomson lead-screw reference: https://www.thomsonlinear.com/downloads/screws/Neff_LeadScrews_bruk.pdf. The prior source capture records the public catalog page review and the direct-download restriction; no local PDF hash is invented.
- Miki Pulley spring-actuated brake catalog: https://www.mikipulley-us.com/documents/Catalog/Catalog_Spring_Actuated_Brake.pdf

The lawful catalog metadata and parameter capture are in `catalog_reference.json`. No manufacturer PDF redistribution license is inferred. All calculations distinguish supplier values, geometric dimensions and declared study assumptions.
