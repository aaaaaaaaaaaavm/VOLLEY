# Gen6 one-cell track/feed integration R1

**Status:** unselected geometry revision, 12 October 2026. The evaluated Gen5 solids and the two earlier Gen6 studies are retained unchanged. This revision joins one passive 3U feeder cell to first-article Candidate A in one FreeCAD assembly. It is neither a selected feeder nor a manufacturing or flight release.

## Why this revision exists

The feeder-only and first-article-only checks each reported zero nominal overlap inside their own models. [The cross-assembly audit](release/Original_Cross_Assembly_Interference.json) shows that placing those source geometries together creates seven intersecting part pairs in the armed state and eight at mid-transfer for either drive candidate. Some are duplicate proxies for the same intended cradle or guide. Three interactions require actual geometry change: the transfer bridge intersects the first-article left guide by **34,050 mm³**; the mid-transfer 3U box intersects it by **74,910 mm³**; and a cassette end stop intersects the carrier pusher by **1,800 mm³**. The seated spacecraft proxies also duplicate one another; their 3,405,000 mm³ overlap is not two physical spacecraft.

## Nominal corrective geometry

R1 splits a 340.5 mm section of the left guide into a lifting segment. It moves 140 mm above its launch position during transfer, leaving 10 mm vertical clearance above the 100 mm spacecraft box. The transfer bridge now terminates at the outside edge of the guide corridor, leaving a **10 mm unsupported lateral gap** while the guide is raised. The two cassette end-stop proxies stop at the cassette edge rather than entering the carrier path. One payload box and one set of cradle/track supports appear in the combined assembly.

The [FreeCAD builder](build.py) saves four native FCStd state models and STEP compounds, and checks every pair of 27 named solids at each state. It samples the 200 mm transfer at 81 stations, 2.5 mm apart, with the guide and gate raised. All four states and the sampled transfer have **zero exact-solid intersection in this nominal geometry**. The [independent STEP readback](release/Gen6_Integrated_R1_STEP_Verification.json) finds 27 valid solids and zero intersecting pairs in every exported state. These results are conditional geometry checks. They do not prove a continuous swept volume, manufacturing fit, or safe contact.

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_integration_r1/audit_original.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_integration_r1/build.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_integration_r1/verify_step.py
```

## Open integration conditions

- The 10 mm bridge-to-support transition needs a payload rail/contact definition and worst-case sag/deflection check. Nominal face contact is not a load path.
- The lifted guide has no actuator, bearings, stop, power-off return, launch lock or position proof. It cannot be counted as a working restraint.
- A partly transferred payload is not positively contained on power loss. The selected policy is shot inhibit and supervised recovery, but hardware implementing it does not exist.
- The feeder pusher is a solid envelope. Its screw, nut, drive, bearing, jam torque, pressure on approved spacecraft contact faces and retraction sensor are not designed.
- One 3U cell is modeled. The selected next study requires two 1U and two 3U fixed cells, passive inserts, two-sided or staggered packaging, independent cell isolation and a provisional host adapter.
- Tolerance, thermal growth, launch deflection, structural modes, magnetic exposure, brake capture, return, fasteners, harness and provider limits are not closed. No mass/CG/inertia ledger has been recalculated for this revision.

The [integration audit](../GEN6_INTEGRATION_AUDIT_2026_10_12.md) maps these issues to the authoritative private blackbook checklist. A nominal intersection fixed here does not close the feeder architecture or validate Gen5.
