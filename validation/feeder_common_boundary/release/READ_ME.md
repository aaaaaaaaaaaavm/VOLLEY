# Seven-feeder common-boundary development comparison

Evidence date: 22 October 2026. Configuration: FDR09-R1, with a separate lead-screw R2 correction.

## Scope and accounting

The manifest contains two 1U and two 3U passive-spacecraft surrogates. All concepts use four independently housed payloads and one common reusable receiver. Six fixed-cell concepts have four local feeds and 900 mm receiver travel on 1,600 mm rails; the drum retains a distinct index/extraction arrangement. The common outer handling envelope uses two passive 1U inserts of 0.185933 kg each. Packing density is not optimized.

| Concept | CAD material [kg] | Listed catalog options [kg] | Conditional local cycle [s] | Mandatory eligibility |
|:--|--:|--:|--:|:--|
| Captive lead screw | 18.606 | 4.230 | 30 | Ineligible |
| Spring / dual gate | 18.915 | 6.002 | 5 | Ineligible |
| Rack / pawl | 18.618 | 5.830 | 5 | Ineligible |
| Indexed drum | 14.821 | 1.932 | 15 | Ineligible |
| Pantograph | 18.060 | 6.002 | 60 | Ineligible |
| Nested telescope | 18.132 | 4.230 | 15 | Ineligible |
| Belt shuttle | 17.915 | 5.830 | 5 | Ineligible |

CAD values are represented-material density estimates. Catalog options include listed motors, gearheads, controllers and brakes as applicable; they are not integrated or qualified. Missing hardware and source mass properties remain unknown. The two columns do not establish a complete installed-system mass, CG or inertia. Cycle options are candidate operating points, not accepted complete cycles or common throughput requirements. No weighted ranking is justified while mandatory gates remain unpassed.

## Geometry and contact scope

The revised arrest plunger reaches the rack root/flank with zero nominal penetration and 1 mm retracted tooth clearance. Its guide has 0.15 mm nominal side clearance and 0.2 mm forward tooth backlash. Preload, release response, tooth load capacity and joint retention remain unverified. Rack/belt drive pads establish geometric contact only. The telescope uses displacement laws 0, u/2 and u with a 20 mm minimum overlap; synchronization, loaded stops and retained component intersections remain unresolved.

The passive 1U insert establishes the common leading datum at X = 340.5 mm. It transfers with its dedicated spacecraft and must remain captive during payload release and empty return. Positive insert lock/return custody is not established. Shared fork/clamp contacts have zero nominal penetration in the checked capture pose. Side gates remain open until fork withdrawal; the earlier simultaneous closure counterexample is preserved in the source record.

## Retained findings

- The 15 N spring end force does not overcome the 20/50 N resistance screens.
- The pantograph output connection has a 35.5 mm gap.
- Telescopic pad/tube intersections remain in the native audit.
- The R1 shared payload sweep intersects parked shafts/capture racks for six fixed-cell concepts; the lead screw and belt have additional transmission conflicts.
- Drum index joints, extraction and continuous rotation remain unproven; its zero sampled corridor intersections do not establish eligibility.
- The 3U, 0.5° tolerance corner has negative study clearance.

The separate lead R2 correction trims guides and capture racks, shortens the screw blank, shifts its end bearing and relieves the guide-bearing housing. The checked rectangular payload sweep changes from eight intersections to zero; the identified 16.176779 mm³ housing overlap becomes zero. The corrected custom-material subtotal is 18.492547 kg. A 0.25 mm radial screw-bearing gap remains. Full bearing support, loaded/tolerance/fault behavior, complete carriage motion, insert custody and installed hardware are not accepted.

## Source and verification

`REVIEW.json`, `COMPARISON.csv`, `D27_GATES.json`, `BOM.csv`, `FULL_RAIL_SWEEP.json`, `INSERT_INTERFACE.json` and `LEAD_TRIM_R2.json` preserve the numerical decisions and geometry findings. `INDEPENDENT_STEP.json`, one directory above, records separate imports of the current exchanges. The supplied source and nominal geometry are not manufacturing drawings, flight qualification or reliability measurements.

Use a Python environment with the recorded FreeCAD installation for native rebuilds:

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_comparison.py
python3 actuator_screen.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 check_insert_interface.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 check_full_rail.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_lead_trim_R2.py
python3 assemble_evidence.py
```

Run these commands from the study root. The builder resumes existing per-candidate evidence; `--candidate NAME` isolates one concept and `--force` regenerates it. `BUILD_RUNTIMES.json` preserves actual commands and run times. The engineering prose is edited for this distribution; numerical JSON and native captures remain canonical. The retained original spring serialization failure and sampled surface checks do not change functional clearance criteria.
