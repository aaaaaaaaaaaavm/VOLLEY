# Gen6 mixed-size feeder: concept trade, not a selected mechanism

**12 October 2026 — ideation record.** The service study uses two passive 1U and two passive 3U CubeSats. The existing Gen6 FreeCAD/STEP first article contains only one restrained 3U dummy; it has no feeder. Gen5's original side cassettes overlap its track and are 11 mm too wide for their reference enclosure. The wider Gen5 R1 revision clears scripted paths, but has no actuator, positive launch restraint, tolerance closure, or source-rated system mass. These are separate generations and geometry revisions; neither is a working magazine.

**Reference packaging focus:** separate, fixed cassettes beside the launch rail. This chooses the first envelope to study, not the transfer actuator or a final G1 architecture. The number of cells per side, cassette orientation and host envelope remain design variables; the Gen5 11 mm clash must not be inherited.

## Split the task before choosing a mechanism

The magazine has five jobs: **retain** every spacecraft through host launch and coast; **select exactly one**; **move it slowly into the carrier/cradle** without touching forbidden faces; **prove it is seated** and seal the magazine before the shot; and **recover safely** if any step stalls or loses power. The reusable carrier then accelerates, releases the spacecraft at a defined contact edge, is captured by the brake, and returns to its loading datum. The feeder must never be able to open two payloads to the launch path together.

An intended cycle is: carrier homed and brake latched → selected cell isolated while all others stay independently locked → transfer path and clearance checked → one spacecraft pushed into the cradle → seated/latched condition sensed by independent means → feeder pusher withdrawn and magazine barrier shut → shot permitted → carrier captured and settled → reset. At every intermediate step, loss of power must leave the satellite and moving hardware contained. The exact latch and sensor design is open.

## Candidate mechanisms

| Concept and familiar analogy | How it would work here | Main strength | Main risk for VOLLEY |
|:--|:--|:--|:--|
| **Fixed individual cartridges + lead-screw pusher**, like a drawer or machine-tool axis | Dedicated 1U/3U cells hold each satellite; one captured screw-driven shuttle or one small screw per cell pushes the selected satellite transversely into a common cradle. Hard stops and position switches define travel. | Simple positive displacement, can stop/reverse, clear load path and inspectable travel. | Screw, nut and guide can jam; multi-cell selection and alignment add mass and width. |
| **Spring follower + escapement**, like a PEZ dispenser | A captured follower gently presents the next satellite; a two-barrier gate admits only one to a transfer shuttle. Mixed lengths require separate size-specific cells or pitch adapters. | Passive presentation force; a small actuator need only release a gate. | A spring is not a launch restraint. Force changes with travel; double feed and jam at the gate must be structurally impossible, not just prevented in software. |
| **Indexed rack and pawl**, like a ratchet jack | One stroke advances a captive elevator/cartridge by exactly one bay pitch and a hard pawl locks the new datum; a short pusher performs the final handoff. | Discrete positions and mechanically held index. | Pawl tooth damage, bounce, partial strokes, and variable 1U/3U pitch need careful anti-reverse and independent retention. |
| **Cam/Geneva indexed drum or tray**, like a film/projector indexer | A small carousel or translated tray brings a locked 1U/3U cell to one transfer window, then dwells on a positive detent while a short pusher loads the sled. | The index and dwell are mechanically distinct; one common transfer axis. | Rotating or shifting loaded spacecraft adds launch restraints, envelope and inertia; a stalled index can block all four shots. |
| **Pantograph/scissor elevator**, the proposed concept | Separate platforms or nested links lower one stored spacecraft to the transfer plane; a short horizontal pusher loads the cradle. All platforms end collapsed at the bottom. | Compact stowage and potentially one repeated motion for several levels. | A normal scissor lift moves its levels together; sequential collapse requires latches or additional links. Near-flat scissor angles raise actuator force, joint play and sensitivity to friction. Platforms still need independent launch restraints and a separate final transfer pusher. |
| **Nested telescoping carriage**, like a camera lens or antenna mast | Captive nested guide stages extend/retract to move a selected cell to the handoff plane. | Compact stowed length and direct motion. | Stiction, binding under thermal distortion, multi-stage backlash and hard-to-inspect internal debris. |
| **Belt/cable or chain shuttle**, like a printer feed/plotter carriage | An endless drive indexes a payload tray, then presents one satellite to a transverse pusher. | Actuator can be remote from the crowded transfer zone. | Tension, slack, vacuum-compatible wear, particulate generation and loss of positive position after a drive fault. |

Microgravity rules out gravity-only feeding. None of the analogies makes a terrestrial mechanism space-qualified; each needs its own launch, vacuum, thermal, shock, cleanliness and cycle evidence.

## First comparison to model

Treat the **fixed-cartridge, lead-screw shuttle** as the reference for analysis, because it gives positive, reversible transfer and keeps stored payloads still. Compare it against the **spring-follower/two-barrier gate** for lowest-part-count presentation and the **segmented pantograph** for package efficiency. This is a study order, not an architecture selection. The pantograph becomes attractive only if its measured volume/mass saving outweighs its added joints, latches, compliance and fault paths.

Hold each satellite in its own launch-rated cell, whether the feed drive is active or passive. A spring can present a payload after command but cannot be the sole restraint. A barrier between the magazine and carrier must stay shut during the powered shot; the cradle needs an unambiguous seated datum, and the carrier needs a capture/brake state before another feed command. A mechanically captured pusher is preferable to one that can become another free object.

## Selection evidence to generate

1. **Interface sketch and envelope:** separate 1U and 3U rail/contact zones, spacecraft keep-out faces, cell pitch, transfer plane, cassette and guide width. Re-check Gen5's 526 mm internal width/537 mm side-feed conflict only as a historical warning; choose a fresh Gen6 envelope and host accommodation.
2. **State diagram and interlocks:** one-at-a-time selection, power-off state, aborted transfer, jam recovery, failed sensor, partial shot, carrier-not-home, and manual-safe reset. At least one barrier should be mechanically closed when the shot is enabled.
3. **Editable mechanism CAD and STEP:** model actual latches, cam/pawl/screw, bearings, shuttle, pusher, stops, cell doors, 1U/3U fixtures, brake boundary and host mounts. Check full swept solids, not only five carrier stations.
4. **Mechanical checks:** launch restraint load path, pusher contact and tip-off, buckling and bearing forces, joint play, thermal expansion and tolerance stacks, moving clearance with deflection, and jam force/torque margins.
5. **Installed-system trade:** actuator, guides, locks, electronics, sensors, harness, fasteners and margins belong in mass/CG/inertia, power and reliability. P131's ~9.93 kg is only frame/guide/carrier material and leaves ~9.35 kg under one *surrogate* device-plus-fuel parity ceiling for every omitted item, including the feeder.
6. **Failure evidence:** a failure mode/effects table, containment argument and repeatability plan. Bench testing, environmental qualification and provider approval are future work; no current CAD view demonstrates P-POD-class reliability.

The next CAD deliverable should be a **one-cell transfer demonstrator** for a passive 3U dummy with positive restraint, handoff and recovery, before a four-cell mixed-size magazine. It can be designed now with FreeCAD and analyzed computationally. A physical article and measured reliability remain unfunded and unperformed.
