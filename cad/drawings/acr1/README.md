# Controlled ACR1 drawing source

See the [drawing index](../../../docs/ACR1_DRAWING_INDEX.md) for all six editable SVG/PDF sheets, sources, units, material/tolerance boundaries and reproduction.

The geometry comes from actual frozen native BRep with FreeCAD 1.0.0 TechDraw projection. `D02` is a true planar section. SVG linework uses a 0.04 mm source deflection request; no physical clearance validation is inferred from projection discretization. All dimensions refer to the exact ACR1 parameters/native bounds, with density, tolerance and thermal assumptions explicitly retained.

`BOM_HOME.csv` lists all 387 native home parts. `MASS_PROPERTIES.json` retains accepted properties for all eight states. `INSPECTION_PLAN.csv` is a proposed inspection procedure, with every actual-result field marked **NOT_PERFORMED**. The 7 kg unplaced power/control allocation is excluded from CAD CG/inertia.

These are academic engineering outline and preliminary assembly/inspection sheets. They are not released manufacturing instructions, supplier approval, measured fit or physical qualification. No general manufacturing tolerance, material grade/temper, fastening torque or unspecified supplier interface is assigned.
