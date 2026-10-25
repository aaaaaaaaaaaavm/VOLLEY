# VOLLEY G5 ACR1 mechanical capture

The selected native source is frozen by `CONTROLLED_SOURCE_LOCK.json` (builder `e1179e8862821862db7649bfac1aa2ba660526dfc5f3f5edc229532b75da52c8`). Each exported state records all six source hashes, a native BOM, connected-solid status, interference results, and a count of the one physical pallet.

## Selected mechanism

Two installed six-level banks use guided, positively driven pushers to move one 3U spacecraft onto the lift's captive pallet. The central cassette corridor is 100 mm on either side of Y0. The outboard pusher straps clear their front shaft supports. The Z lift carries the pallet, X end frames, and independently retracting Y keepers. Continuous end-frame clearances are 0.5 mm from the nominal payload and relevant sled corner hardware.

The pallet has a Y0 crossbar, interleaved contact pads, four 8 mm feet, and two outboard lift-grip interfaces. Its feet land on carrier top Z30 while its payload contact surfaces remain at Z46. The pallet stays on the carrier through launch, arrest, and return. There is no horizontal pallet withdrawal screw or guide mechanism. The old `withdrawn` filename identifies the pose with the lift grip pins withdrawn; it contains no horizontal pallet motion.

The four overhead Y keepers retract upward by 110 mm. Their 3 mm rods run in 3.2 mm guides. A central 12 mm OD by 160 mm actuator and 3.8 mm OD guided push/pull route are explicitly modeled reference allocations; a self-locking screw and normally applied holding brake are required. Purchased hardware, load/life qualification, and sensing remain selection interfaces.

## Capture sequence

1. Land the pallet feet while both outboard lift pins remain engaged.
2. Close the upper carrier capture caps and engage their independent lock pins.
3. Insert both pallet lock shafts 12 mm, then rotate their 12 by 4 mm heads by 90 degrees above the pallet.
4. Verify carrier capture before opening the overhead Y keepers and retracting the two lift grips by 26 mm.
5. Raise the lift and end frames clear. Return and pallet pickup use the reverse custody sequence after the carrier home interface is indexed.

The pallet locks are at carrier-local X40 and X468, Y−90. Their 6 mm shafts pass through 6.2 mm carrier-web bores. Heads stow at Z32–35, below the pallet underside Z38, and capture at Z44–47. Each pallet entry is a 13 by 5 mm key slot plus a 7 mm shaft circle; the rotated heads retain the pallet positively in Z. These locks do not cross the existing home-index lug at home X220/Z36. That separate 6 mm host-pin interface must be retracted before carrier translation.

## Launch geometry

The 16 mm carrier plates, 20 mm negative web, 42 discrete 8 mm magnets per array, 216 winding bars, reversed C series return, and 21 mm² minimum return necks are retained. Two local 6.2 mm web holes are present in the exact final chassis BREP for structural review. The final BREP SHA256 is `d4b53d520c1bc0d33c1c36c29dddeb775d0b4147ec24dbb342a4fc43e97460a1`.

The spring-closed forekeepers open 12 mm through fixed 50 mm travel ramps, finishing at carrier aft X1495, 5 mm before release at X1500. Their open inner edge is |Y|54, providing 4 mm payload side clearance. Spring references specify 5 N preload and 0.5 N/mm rate. Rounded followers are modeled explicitly. This motion uses a passive cam and needs no instantaneous screw opening.

Forward pallet grip ears are trimmed to Z45.5, 0.5 mm below the payload flight plane. Payload departure is checked to 600 mm relative advance. The carrier plus pallet reaches X2224.5 at the allocated arrest endpoint, inside the 2250 mm rail. Arrest and return use the same LSM. Unexcited auxiliary poles and a copper fin are preserved only in the private `archived_auxiliary_brake` variant and have no selected braking function or force credit.

## Evidence boundary

`MOTION_VERIFICATION_BASELINE_PALLET.json` contains 143 passing native nominal poses. `FINAL_REFINEMENT_VERIFICATION.json` proves the final pallet is a strict material subset, closed locks are identical, restored web material clears a conservative envelope of the entire carrier travel, and new open-lock material stays separate from every lifted lower region. It also directly checks the final seven insertion/rotation poses and twelve payload departures. Eight obsolete longer-stroke lock poses are superseded; 135 carried poses plus 19 final direct poses give 154 accepted poses in `MOTION_VERIFICATION.json`.

These are nominal geometry and reference-component checks. The motion baseline is sampled, not a general continuous collision solver. Provider fit, loaded contact behavior, actuator selection, manufacturing tolerances, environmental qualification, and flight qualification are not established by this capture.
