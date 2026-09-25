# Current release-cell Fusion handoff

## Lunar-first concept models and current motion states

The new packaging references are in `cad/lunar_concept`: single mechanical cell,
four-cell bank, lunar carrier and larger-payload pallet, each STEP plus STL.
See [the visual review](LUNAR_VISUAL_REVIEW.md) and [interactive viewer](lunar.html).
They are editable imported solids, not native Fusion features or detailed parts.
All component dimensions beyond the MC-L2 anchor are provisional envelopes.
The bus/tank deliberately overlap; no model has manufacturing or interference
approval. The earlier 21 missing-CAD items still require your detailed design.

**For the current MC-L2 layout use 0/40/80/100 mm pusher positions:** charged,
midstroke, separation and caught. The 240/260 mm sequence later in this handoff
belongs only to the historical S2 anchor. Do not mix its spring/catcher data into
MC-L2. The illustrated accumulator cylinders are not spring free-length designs.
Return native Fusion, assembly STEP, mass/CG/inertia estimates, parameter ledger,
part status and interference findings. Keep lunar carrier flight hardware separate
from the current cell coupon.

## Current local addition: lower-authority cartridges

Use [P92-S5](MISSION_CARTRIDGES.md) and the
[force-law parameter ledger](../cad/current_cell/MISSION_CARTRIDGES.csv) for
separate 0.5/1/2/3 m/s study cartridges. These do not replace the historical S2
anchor below with a single universal mechanism. The shortest sampled strokes are
20/20/80/120 mm respectively, for a 4 kg payload and 0.25 kg pusher. The 5 m/s
candidate fails the original limits. Each spring geometry, guide, latch, charger,
catcher and force calibration still requires detailed design.

For the first lower-authority motion layout, carry the 2 m/s force-law candidate
as MC-L2: 80 mm working stroke, 106.667 mm charge, aggregate stiffness
1604.108 N/m and nominal initial spring force 171.105 N. This is an adjustable
layout target, not a supplier specification or a proved accuracy claim. Retain the
20 mm catcher as a modeled envelope only; peak force, rebound and shock remain
unclosed. The 0.5 and 1 m/s short-stroke cartridges cannot inherit that catcher
model because their end spring deflection is less than 20 mm.

The existing 21-part missing-CAD ledger remains applicable. Keep charged, release,
catch and charger-clear states; keep the launch restraint separate. Do not model
spring free length as charge deflection.

BOLLEY A6j-R2 uses a 0.25 mm lift of both winding heights and a 2 mm rise of the
back yoke/outer legs while retaining the 4 mm haunch. The separate core and lower/
upper transverse STEP coupons show geometry only. They contain straight conductor
sections, not full turns or terminals. Its fresh field verdict is recorded in
BOLLEY/docs/RECONCILED_WIRE_FIELD.md; no old magnetic pass can be inherited.


Adityavardhan Mishra · 17 September 2026 · layout revision A

**Build an editable mechanism layout tonight, not manufacturing drawings.** The
current cell has no committed detailed solids. The STEP files in `cad/step/gen6`
are the historical gas machine. They are reference evidence, not this assembly.
The current design does not inherit its 8 m guide, pressure vessel or trim stator.

## What to build first

Create `VOLLEY_G6_Mechanical_Cell_A` with separate components and a parametric
timeline. X is the departure direction, Y/Z are transverse. Put the payload's
initial aft contact plane at X=0 and its nominal central axis at Y=Z=0. The pusher
face starts at X=0 and travels in +X. Datum A is the host mounting plane (location
unselected), B the departure axis, C a clocking plane. Do not silently identify
A with the payload contact plane. Retain empty reference components for host
interfaces that have not been supplied.

For the first coupon candidate, model a guided linear spring cassette behind a
symmetric pusher, charged by a motor/lead-screw crosshead with a disengaging
coupling. The charging screw must not be back-driven by the release. Show its
withdrawn/clear state and a sensor proving clearance. Two symmetric spring seats
are a layout option; their total force must equal the one declared spring model.
A separate release latch carries the charged load. A separate ascent restraint
carries launch loads. The catcher holds the pusher after payload separation.

This selects a **layout candidate**, not a purchased spring, flight mechanism or
closed P92 architecture. Compression-spring buckling/solid height and motor
backdrive remain reasons to reject it. If the linear spring is too long, compare a
rotary accumulator or constant-force arrangement using a new declared force law.
Do not fold the spring graphically and keep its old stiffness.

## One coherent numerical layout anchor

Use case **88 (zero-based index)** in
`analysis/results/reference_cell_mechanics.json`, P92-S2. It is an analytical
fixed-frame case, not a supplier part or a mission requirement. Do not combine
minimum stroke from one case with minimum latch force from another.

| Parameter | Layout value | Status / interpretation |
|---|---:|---|
| Payload mass | 4 kg | Study assumption; dummy must have measured mass/CG/inertia |
| Payload envelope X/Y/Z | 340.5 / 100 / 100 mm | Existing project proxy only; replace with actual payload ICD, rails and protrusions |
| Working pusher stroke | 240 mm | Selected analytical layout case |
| Pusher mass | 0.25 kg | Assumption to be replaced by an allocated mass model |
| Relative-speed study point | 4.569852 m/s | Mission-screen point; fixed-frame speed in this internal model |
| Aggregate spring stiffness | 934.532 N/m | Analytical target, not a catalog specification |
| Initial/final compression | 320 / 80 mm | Deflection, NOT spring free length |
| Initial/final spring force | 299.050 / 74.763 N | Latch/catcher sizing input; no safety factor applied |
| Assumed sliding friction | 2 N | Not measured |
| Peak acceleration | 7.127 g | This case only; 10 g is a study ceiling, not qualification |
| Initial stored spring energy | 47.848 J | Includes retained end preload |
| Catcher kinetic energy | 2.610 J | Pusher-only model; does not include full release transients |
| Catcher travel sensitivity | 5 / 10 / 20 mm | Mean force 522.089 / 261.044 / 130.522 N; peak unknown |
| Nominal catcher travel for layout | 20 mm | Editable scenario, not selected damper performance |

The payload proxy plus working travel already sweeps 580.5 mm in X. The spring,
catcher, restraints, structure and clearances add to that. Do not promise a 240 mm
complete deployer. Spring free length must exceed maximum deflection plus solid
height and compression margin; none is selected. Low-speed operation needs its
own preload/friction/contact study, not simply scaling this case's preload knob.

`cad/current_cell/FUSION_PARAMETERS.csv` is a manual parameter-entry ledger, not a
claim that Fusion imports this format natively. Names with TBD have no released
value. Leave reference sketches unconstrained only where explicitly marked TBD.

## Complete missing-CAD ledger

Every row below is absent as a detailed current-cell part. A study sketch is not
closure. Keep each item separate so replacements do not destroy the assembly.

| ID / component | Model tonight | Inputs that block a released drawing |
|---|---|---|
| MC01 master skeleton | Axis, contact/release/catch planes, keep-out bodies | Host ICD and real payload envelope |
| MC02 payload dummy | Proxy envelope, separate ballast/CG placeholders | Payload rail/tab/contact permissions and inertia range |
| MC03 base and cell frame | Parametric load-path envelope | Ascent/load cases, modes, mount spacing, wall/rib sizing |
| MC04 guidance | Two opposed guide placeholders with editable bearing stations | Friction, alignment, vacuum tribology, contact stress |
| MC05 pusher | Symmetric contact plate, bearing attachment and latch interface | Contact pads, CG offset, stiffness and tip-off allocation |
| MC06 accumulator cassette | Spring seats, guides and full compressed/free envelopes | Actual springs, fatigue/dwell/buckling/solid height |
| MC07 preload carriage | Slider with measured charge-position datum | Adjustment resolution, backlash and calibrated force law |
| MC08 charger | Motor/gearbox/lead-screw reference components | Part numbers, torque/speed/efficiency, thermal duty |
| MC09 charger disengagement | Coupling withdrawn and engaged configurations | Release clearance, failed engagement and load isolation |
| MC10 release latch | Envelope plus loaded/released swept volumes | Geometry, contact stress, shock, repeatability, actuator |
| MC11 ascent restraint | Separate load-path concept and released clearance | Launch loads and inhibited-state requirements |
| MC12 catcher | 20 mm editable stopping envelope, replaceable absorber | Peak load, pulse shape, rebound, vacuum/material data |
| MC13 anti-rebound lock | Captive pawl/stop envelope and access | Positive retention after catch, wear and recontact tests |
| MC14 exit guard/door | Open position entirely outside departure corridor | Need for door, sweep, interlock and payload protrusions |
| MC15 state sensing | Charge, latch, coupling, payload-clear and caught mounts | Accuracy, bandwidth, independence and environmental parts |
| MC16 harness/electronics | Routing corridors, service loops and connector zones | Driver, inhibit circuit, EMI and selected connectors |
| MC17 thermal interfaces | Reserved straps/pads and contact faces | Dissipation, dwell and environmental temperatures |
| MC18 cell-to-bank mounts | Replaceable repeated interface skeleton | Stiffness, tolerances, alignment and jam isolation |
| MC19 bank-to-host mounts | Reference datums and load arrows | Provider mechanical/thermal/electrical ICD |
| MC20 fasteners/access | Access cylinders and assembly sequence | Selected fasteners, preload/locking and inspection |
| MC21 coupon fixture | Reaction frame, load cell and velocity-gate references | Facility loads, instrument ranges/calibration, containment |

## Fusion sequence and deliverables

1. Enter declared parameters; create skeleton and datum planes before solids.
2. Build payload dummy and pusher, join pusher with a slider. Check 0, midstroke,
   240 mm release and 260 mm post-catch layout positions.
3. Add spring/charger/latch swept envelopes. Verify charged, uncharged and charger
   disconnected states. Use reference bodies for all unselected hardware.
4. Add guide/frame load paths, independent ascent retention and catcher lock.
5. Show the payload leaving while the pusher is retained. Test all door, latch,
   charger and harness keep-outs through the sequence, not only at endpoints.
6. Pattern **two cells first**, then 4 and 12 as packaging studies. Do not fix bank
   pitch until exit clearance, mounts, access, heat paths and host envelope exist.
7. Export native F3D/F3Z, assembly STEP, per-part STEP for newly defined parts,
   parameter ledger, named-view images, interference findings, BOM with unknowns,
   and a short assembly sequence. Keep proxy mass out of the real mass total.

Required views: full assembly, longitudinal section, charged state, released
state, caught pusher, latch/charger clearance, two-cell jam isolation, exploded
assembly, host interface and instrumented coupon. No cosmetic finish is needed
before the load paths and motion are clear.

## Existing CAD and BOLLEY companion work

The download pack inventories every committed VOLLEY STEP by generation. Gen5's
eight STEP parts are the frozen EM comparison set; Gen6's seven are the gas set;
Gen1/2/3 are heritage. None is a new mechanical-cell assembly. No native Fusion
file for this new cell is available to hand over.

For BOLLEY use `cad/exports/gen3_12turn/Bolley_Gen3_STEP.zip` from BOLLEY main
`2f2e6250dedd54b32e467209a4f1dd74e1fe03c1`, not the older four-turn package.
The four nominal solids are the 12-turn cell, ABC module, full-face winding and
full-face core/winding. Actual leads/terminals, insulation, bus joints, ribbon
lay-up, lane root attachment, adjustable cassette, containment, cooling, sensor
mounts, gate/latch, fasteners and the 0.20 mm gap tolerance scheme remain work.
The inherited C1 four-turn wording is historical; do not route a four-turn coil
into the selected twelve-turn assembly. A5h nominal geometry is not actual-field,
hot-switching or manufacturing closure.

Priority tonight: one intelligible VOLLEY cell and its motion study. BOLLEY
terminal routing and tolerance sketches are the next CAD task, not a reason to
polish an entire speculative OTV.
