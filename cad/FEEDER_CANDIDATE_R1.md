# R1 feeder geometry candidate — unselected

**This is a separate geometry experiment, not a change to the evaluated Gen5 inputs or an accepted feeder.**
It retains the eight Gen5 source parts except the enclosure and cassettes, which are modeled
as new STEP parts. The 3U proxies translate from six side cells into a central vertical
lift corridor, then descend to the first release height. The supports are conceptual guides;
actuation and launch retention are not designed.

External width grows from 530 to 570 mm, giving
9.5 mm cassette-to-inner-skin clearance
and 5.0 mm cassette-to-track clearance per side.
Exact static track/cassette overlap is {'1': 0.0, '-1': 0.0} mm³.
The simple aluminium-skin mass increment is 0.99 kg,
not a revised installed-system mass. The new enclosure also changes host accommodation.

Sampled routes clear: 12 / 12.
Each axis-aligned horizontal and vertical translation also clears a conservative full
340.5 × 100 × 100 mm swept box against the listed fixed parts. This does not include
tolerances, the moving lift/gripper, dynamics, cycle life, safety or launch loads.

![R1 geometry section](../figures/gen5_feeder_candidate_r1.png)

This is a parameter-derived section, not a CAD GUI or solver screenshot. The native
FreeCAD review document is `cad/native/Feeder_Candidate_R1.FCStd`; its 21 named
instances and FreeCAD-exported assembly STEP have read-back and interference results in
`cad/FREECAD_FEEDER_R1.json`. Imported B-reps have no native feature histories.

## Open design gates

- no actuator, lift carriage or motor package
- no launch retention gate or load path
- no fastener/harness/thermal/tolerance clearance
- no provider ICD or named payload
- larger enclosure invalidates Gen5 mass, structural and host envelopes
- rigid swept-envelope screen excludes dynamics, elastic deflection and fault cases

The STEP part and assembly exports, hashes and every collision result are in
`cad/FEEDER_CANDIDATE_R1.json`. The source is `cad/build_feeder_candidate_r1.py`.
