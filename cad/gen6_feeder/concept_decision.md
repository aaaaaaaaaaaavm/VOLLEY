# Fixed-cassette transfer concept decision, revision 0

The selected *packaging focus* is separate fixed side cassettes. No feed mechanism is selected for hardware. The comparison below ranks what to model first, not flight worthiness. The same 3U transfer, independent stored-payload restraint, power-off retention and single-feed requirement apply to every concept.

| Candidate | Moving payload storage | Transfer actuator and extra devices | Main failure path | Study order |
| --- | --- | --- | --- | --- |
| Captive lead-screw pusher | Fixed | One screw shuttle, guide, hard stops, gate, cradle restraint | Screw/guide stall or partial transfer | **First geometry reference**: reversible positive displacement and inspectable travel |
| Spring follower plus two gates | Fixed, spring-loaded | Captured spring, two independent barriers, transfer guide | Double feed or residual spring load after a gate fault | Second: compare genuinely lower actuator burden against more difficult isolation |
| Rack-pawl index plus short pusher | Indexed cassette | Pawl, anti-reverse, pitch adaptation, pusher | Partial stroke and wrong-cell position | Later, if cell packaging demands indexing |
| Geneva/indexed tray | Moving loaded cells | Index drive, detent, transfer pusher | One jam blocks all cells; more moving launch mass | Later, if side-by-side width cannot fit |
| Segmented pantograph/scissor | Moving platforms | Multiple joints, sequential latches, final pusher | Near-flat force amplification, joint play, latch sequence | Keep as package-efficiency challenge case; ordinary scissor motion does **not** give one-at-a-time collapse |
| Telescoping carriage | Moving nested stages | Captive stages, bearings, pusher | Binding, hidden debris, backlash | Later, if verified stowage advantage is substantial |

No numeric reliability, mass or volume rank is assigned without the corresponding CAD and component data. A simple-looking mechanism can still fail the single-feed and power-off containment tests. The pantograph earns selection only if an actual layout shows enough volume or mass benefit to offset its additional joints, locks and final transfer pusher.

| Candidate | Likely package pressure | Additional joints/locks | Single-feed isolation | Power-off retention | Mixed 1U/3U extension | Verification burden |
| --- | --- | --- | --- | --- | --- | --- |
| Captive lead screw | Side width and screw stroke | Low to moderate | One locked cell at a time, if selector is independent | Requires a separate positive restraint | Distinct fixed cells and one transfer datum | Inspectable stroke, but jam and screw life must be tested |
| Spring/two gates | Spring stroke within each cassette | Two barriers per transfer path | Needs a physical escapement proving one payload only | Requires separate restraint; spring is not one | Size-specific cassettes/adapters | Gate timing, force variation and double-feed testing |
| Rack-pawl | Pitch and index stroke | Pawl, anti-reverse and pusher | Position must be independently confirmed | Captured pawl is insufficient as launch restraint | Variable pitch complicates indexing | Partial-stroke and tooth-fault campaigns |
| Indexed tray | Rotation/translation envelope | Index detent plus pusher | One shared transfer window | Every loaded cell needs an independent lock | Can carry mixed-size trays | Shared jam and moving-payload launch loads |
| Segmented pantograph | Potentially compact collapsed height | Many hinges and sequential locks | Must prove only selected platform moves | Each platform needs its own lock | Platforms can differ in height | Joint play, latch sequence and near-flat force |
| Telescoping carriage | Compact stowed length | Nested sliding stages and stops | Selection mechanism still needed | Every stored payload needs its own lock | Size-specific cells/stages | Binding, debris and backlash inside hidden stages |

These are qualitative engineering hypotheses to guide the next model. The table does not establish comparative mass, probability of failure or lifetime.

## Decision gates

1. Confirm the payload contact/keep-out envelope and allowed load from a named interface; the public 3U box is only a surrogate.
2. Make a complete single-cell transfer and restraint layout with actual moving solids, including a captured pusher, closed barrier and safe state after interruption.
3. Sweep all motion and tolerance extremes, not just five carrier stations; calculate actuator force, jam torque and contact loads.
4. Extend the selected design to two 1U and two 3U cells, then reconcile installed mass, CG, inertia and harness.
5. Test a physical article repeatedly before any equivalence to an established deployer is claimed.

For the final Gen5 black book, this is a Gen6 future-work decision record. The Gen5 feeder remains absent, and the modeled Gen6 reference must not be shown as a completed Gen5 subsystem.
