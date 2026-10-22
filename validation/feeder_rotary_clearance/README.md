# Feeder exit-gate rotary clearance — FM07-R6 candidate

## Engineering result

The R5 gate panel shares a zero-clearance surface with the sled deck at the checked near-closed angles (0–0.5 degrees). Native intersection volume at those samples is zero: this is surface contact, not a demonstrated volumetric collision. The panel's lower edge is raised from z=22.00 to z=22.25 mm and its height reduced from 18.00 to 17.75 mm; its upper edge, hinge, locks and other components remain unchanged.

The R6 candidate passes all four nominal continuous rotary screens: opening and closing, 1U and 3U. The smallest guarded conservative lower bound is **0.009884598 mm** across those angle intervals. It is a computed conservative bound, not a measured or qualified clearance. Eight full native assemblies and two individual gate STEP files passed separate CadQuery readback.

## Method

A rigid rotation through at most half an angular interval moves any gate point by no more than 2 R sin(w/4), where R bounds its radius and w is the full interval width in radians. Native midpoint distance minus this displacement and a 0.00001 mm numerical guard gives the interval lower bound. Adaptive bisection covers every angle for every stationary obstacle. The source-verified coaxial hinge uses rotational invariance. This is a numerical nominal-geometry screen, not a manufacturing tolerance or a formally certified kernel error bound.

## Change verification

The source change is restricted to the gate panel's lower edge/height and revision label. Eight exported states verify that the new gate remains one valid solid, removes 41 mm³ and adds no material outside R5. All other components match R5, and all component pairs have no detected volumetric penetration at those states. Under the unchanged rigid motions, a material subset cannot introduce a new intersection with previously nonintersecting geometry. This inherits only the prior nominal nonpenetration evidence; it does not establish loaded clearance or contact dynamics.

At an assumed steel density of 7850 kg/m³, the material change is a reduction of 0.32185 g per gate. This is a material delta, not an installed-system mass.

## Interpretation and remaining work

The nominal gate/deck rubbing contact is removed in this separate candidate revision. Tolerance stacks, thermal expansion, joint compliance, actuation loads, stress, wear, power-off behavior and multi-cell integration still require their existing checks. FM06/FCE12 contact results do not validate the R6 assembly. No feeder downselect or D27 acceptance follows from this result. R5 and the evaluated Gen5 record remain preserved.

## Evidence and reproduction

- [Captured intervals](CONTINUOUS_ROTARY_CLEARANCE.json) and [checker](check_rotary.py).
- [Native change audit and exports](DELTA_AND_EXPORT.json), [CAD and STEP](cad/), [independent readback](INDEPENDENT_STEP.json).
- [Native-distance and interval figure](figures/rotary_clearance.svg).
- [Preserved R5 evidence](reference_r5/) and [R5 source](reference_r5/mechanism.py).
- FreeCAD runtime: run check_rotary.py and export_delta.py; CadQuery runtime: run readback_step.py. Run write_report.py after the capture and STEP checks. check_capture.py verifies the packaged identities without rerunning CAD.

Figure evidence class: computed native-geometry results. Source: DELTA_AND_EXPORT.json and CONTINUOUS_ROTARY_CLEARANCE.json; configuration FM07-R6-CANDIDATE. No physical measurements.
