# ACR1 controlled engineering outline drawings

**VOLLEY-G5-ACR1, drawing revision A — 25 October 2026.** These A3 engineering outline/interface sheets derive from the frozen native BRep and accepted numerical ledgers. They support the academic configuration, assembly planning and subsequent inspection preparation. Manufacturing fits, material grades, fastener torques and supplier interfaces that lack source evidence remain unassigned.

| Sheet | Controlled content | Editable SVG | PDF |
|:--|:--|:--|:--|
| D01 | Complete home-state plan/side projections and dimensioned 2250 × 1240 × 1348.9 mm native envelope | [SVG](../cad/drawings/acr1/D01_general_arrangement.svg) | [PDF](../cad/drawings/acr1/D01_general_arrangement.pdf) |
| D02 | True native X=400 mm motor section; magnet/winding faces, rail datums and active stroke | [SVG](../cad/drawings/acr1/D02_motor_section.svg) | [PDF](../cad/drawings/acr1/D02_motor_section.pdf) |
| D03 | Actual south-bank level-0 cell, guides/pusher and indexed lift interfaces | [SVG](../cad/drawings/acr1/D03_feed_lift_interfaces.svg) | [PDF](../cad/drawings/acr1/D03_feed_lift_interfaces.pdf) |
| D04 | Retained sled/pallet projections; bayonet/grip dimensions and custody sequence | [SVG](../cad/drawings/acr1/D04_pallet_sled_interfaces.svg) | [PDF](../cad/drawings/acr1/D04_pallet_sled_interfaces.pdf) |
| D05 | Project datums, explicit existing tolerance budgets and proposed assembly/inspection sequence | [SVG](../cad/drawings/acr1/D05_tolerance_assembly_inspection.svg) | [PDF](../cad/drawings/acr1/D05_tolerance_assembly_inspection.pdf) |
| D06 | Exact accepted native mass/CG/inertia, density classes and preliminary fabrication boundary | [SVG](../cad/drawings/acr1/D06_mass_materials.svg) | [PDF](../cad/drawings/acr1/D06_mass_materials.pdf) |

[Combined six-sheet PDF](../cad/drawings/acr1/ACR1_DRAWING_SET.pdf) · [Editable projection source](../cad/drawings/acr1/build_drawings.py) · [Projection/source capture](../cad/drawings/acr1/PROJECTION_CAPTURE.json) · [Complete 387-part home BOM](../cad/drawings/acr1/BOM_HOME.csv) · [All eight-state mass/CG/inertia groups](../cad/drawings/acr1/MASS_PROPERTIES.json) · [Proposed inspection plan](../cad/drawings/acr1/INSPECTION_PLAN.csv) · [Drawing identities/checks](../cad/drawings/acr1/MANIFEST.json)

## Geometry and units

FreeCAD 1.0.0 reads the exact frozen home native file. TechDraw performs hidden-line projections of the actual selected solids; the motor view is an actual planar BRep section. Exported visible curves are approximated with a declared maximum 0.04 mm source chord deflection for editable SVG linework. Dimension annotations come from the native envelope and frozen parameter/budget records. Dimensions govern the drawing; these are outline sheets, with visible edges shown and hidden detail omitted for legibility.

Coordinates are millimetres in the ACR1 system. The preliminary project reference scheme is mounting plane Z=−150, firing direction +X and median plane Y=0. It does not define a provider-approved mounting pattern. Reference catalog/actuator envelopes remain reference envelopes wherever actual supplier interfaces are unselected.

## Tolerances, materials and mass

The declared per-face magnetic stack retains **0.264111 mm** residual after the existing nominal gap, 130% load-screen closure and guide/flatness/assembly/thermal allocations. The cradle endwall stack retains **0.054840 mm** in the existing 60 K differential-temperature case. These values are design allocations and model results; they are not measured manufacturing capability or a blanket fit class. D05 and the source budgets retain the numerical assumptions.

Materials retain the frozen density classes rather than invented alloy/temper or supplier approvals. The represented native dry mass is **149.556720 kg**. Its home CG and full tensor come from the accepted ledger. The separate **7 kg power/control allocation has no assigned spatial location and is excluded from CAD CG/inertia**; it is included in mission device mass, 156.556720 kg. Loaded represented native mass, 197.556720 kg, therefore differs from the loaded mission device mass, 204.556720 kg.

The inspection CSV explicitly records **NOT_PERFORMED**. It prepares dimensional/custody/material/mass checks for a later real build. No physical inspection, qualification, manufactured release or measurement is inferred from these drawings.

## Rebuild and verify

Use an interpreter configured for FreeCAD 1.0.0 / Part / TechDraw Inkscape for PDF export and Poppler (`pdfunite`, `pdfinfo`, `pdftotext`) for assembly/checks:

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3.13 cad/drawings/acr1/build_drawings.py
python3 cad/drawings/acr1/check_drawings.py
```

The first command shows the installed Debian layout used for this capture; another platform can invoke the same script with its FreeCAD-configured Python. The source does not rewrite the native CAD or accepted analysis outputs. Existing earlier Gen5/Gen6 drawings remain separately identified history. The [current engineering package](../validation/acr1/README.md) contains the native/STEP states and source evidence.
