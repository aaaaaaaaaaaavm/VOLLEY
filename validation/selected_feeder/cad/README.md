# FM08-R3 — Guided lead-screw CubeSat feeder

FM08-R3 is the selected academic design reference for mixed 1U/3U transfer. Four independently gated fixed cassettes feed one receiver. The local mechanism uses a supported 10 × 2 mm lead screw, a rear pusher with rail-contact pads, and twin 8 mm guide shafts. A separate belt drive indexes the receiver; its clutch disengages before the electromagnetic launch sequence.

The retained interface is a passive rectangular CubeSat surrogate. It is not a provider-approved deployer or a demonstrated physical mechanism.

## Mechanical sequence

1. Coast the host and index the empty receiver to the selected cassette. Prove both docking pins engaged and the receiver's far-side stops closed.
2. Verify the selected payload and its cassette. Retract that cassette's launch-restraint pins and lower its storage gate through the dedicated floor slot. Other cassettes remain restrained.
3. Advance the rear pusher 200 mm in a nominal 30 s cycle. The fixed channel caps and receiver far-side stops contain the payload. The 1U dimensional insert remains attached to its cassette.
4. Confirm payload presence and settling. Close the receiver's near-side stops. Prove receiver capture before returning the pusher; the pusher has no pulling capability.
5. Return the pusher, close the empty cassette gate and prove the clear path. Retract the docking pins before receiver indexing.
6. For launch, prove payload capture, host coast and the required interface states; disengage the index clutch and retract the receiver's leading stop. The separate electromagnetic launcher supplies the launch stroke.

A loss of power inhibits further commands and applies the reference brake. A free payload may move inside the closed channel. The design does not claim that a frictionless payload remains at the pusher's instantaneous position, or that an end-stop impact has been qualified. Recovery requires supervised state and path checks.

## Controlled dimensions

| Quantity | Reference value |
|---|---:|
| Stored payloads | Two 1U and two 3U |
| 1U / 3U length | 113.5 / 340.5 mm |
| Common payload cross section | 100 × 100 mm |
| Common leading datum | X = 340.5 mm, local cassette coordinates |
| 1U trailing datum | X = 227 mm |
| Feed / launch axes | Y / X |
| Feed stroke | 200 mm |
| Receiver docking stations | X = 0, 250, 650 and 900 mm |
| Receiver index travel | 900 mm |
| Linear rail length | 1,600 mm |
| Guide shafts | Two Ø8 × 330 mm |
| Guide-bush length | 30 mm |
| Minimum nominal guide-bush end margin | 35 mm |
| Lead screw / reference nut | SPT10x2M nominal 10 × 2 mm / SB3700 nominal Ø19.1 × 19.1 mm |
| Screw bearing-centre span used in the conservative load screen | 350 mm |
| Payload side and upper channel clearance | 2 mm nominal |
| Rail-contact pad elevations | Z = 24–30 and 114–120 mm |
| Reference adapter mounting plane | Z = −140 mm |
| Leading / 1U aft stop retraction | 134 mm vertically |
| Lowest receiver stop position | Z = −114 mm |
| Nominal lower stop-to-mount-plane clearance | 26 mm |

The rail-contact zones assume an 8.5 mm corner-rail width. Their compatibility must be checked against an actual spacecraft interface. The transition seam is 6 mm for 3U and 8 mm for 1U. Including the separate 3.2 mm storage-gate roof slot, the minimum total cap-supported payload depth is 90.8 mm for 3U and 88.8 mm for 1U. This is a nominal geometric containment argument, not a contact-dynamics validation.

## CAD and mass accounting

`release/` contains five complete native FreeCAD/STEP states and nine nominal component native/STEP pairs. `PART_INDEX.json` identifies the component exports; `BOM.csv` identifies the 154 objects in the stowed assembly. Each native feature records its material, role and density. All 154 assembly features contain one connected solid; the fixed cassette gantries include connected floor supports and clevis backstraps.

The stowed represented-material subtotal is **25.3643099253 kg**, with centre of gravity **[592.14192667, 51.90835519, 54.70613394] mm**. Its outer envelope is **1,610 × 877.8 × 388 mm**, or **548.344104 L**. The raised restraint pins increase the working height to **396 mm**; the working allocation is therefore larger than the stowed envelope. These dimensions include the represented catalog envelopes and underfloor adapter space; they are a packaging result, not an approved host allocation.

The subtotal includes the modeled custom solids and density-based bearing/shaft representations. Payload mass, catalog motor/gear/brake/controller masses, sensors, harness, mounting hardware and unselected gate actuators must be accounted for separately. `full_installed_mass_kg` therefore remains null. A zero mass on a catalog or payload envelope means that its mass is excluded from this geometric subtotal; it does not mean massless hardware.

Screw threads, gear teeth, rolling contact, wiring and purchased-component internals are not manufacturing geometry. The FCStd files and STEP solids are geometric design references. They are not a production drawing release.

## Verification evidence

- `GEOMETRY_REPORT.json`: software versions, source hash, five complete assembly audits, export/readback checks and 18 local payload-motion cases.
- `MOTION_VERIFICATION.json`: installed transfer, captured-payload pusher return, two-format receiver indexing, and the rectangular payload launch corridor. This report explicitly distinguishes sampled mechanism checks from the exact rectangular translation envelope.
- `PART_INDEX.json`: nominal part exports and material properties.
- `release/obj/`: native BRep tessellations in millimetres, with source-native hashes and object-role metadata. These are render inputs, not solver screenshots.

Native STEP files are reimported in FreeCAD with a 1 ppm aggregate-volume criterion. The separate CadQuery/OCP import check in `exchange/INDEPENDENT_STEP.json` verifies all five assembly exports against their paired native records. Both use the OpenCASCADE kernel family; this is an exchange check, not independent-kernel certification. Zero nominal intersection does not establish loaded clearance, reliability, a friction coefficient or a measured positioning accuracy.

## Reproduction

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_selected.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 export_details.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 verify_motion.py
# In an environment with CadQuery and OCP installed:
python exchange/readback_step.py release
```

The builder is standalone; it does not import earlier failed feeder geometry. The frozen builder SHA-256 is `6ebbde89b5452a7529a7b860cfcba87afacdf25025d7f6e0e0fb65e2e7bc4b6c`.

## Evidence boundary

This release supports a selected academic mechanism architecture, editable nominal CAD, source-linked component sizing, geometric motion checks and stated fault logic. It does not establish hardware performance, contact-load convergence, flight qualification, provider compliance or an economically justified orbital service. The earlier unconverged rigid-contact model is not used to rate FM08-R3 precision or loads.
