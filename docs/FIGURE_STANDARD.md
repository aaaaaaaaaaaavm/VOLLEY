# Scientific figures and engineering documentation

Revision 2 · 19 October 2026

## Scope

These conventions apply to current reports, manuscripts, presentations, repository pages, diagrams, plots, CAD views and solver reports. Adoption is not a declaration that every retained historical asset has passed visual review. A frozen technical record remains identifiable; a restyled edition has its own path and provenance. Agency guidance is a reference, not endorsement, qualification or approval.

## Evidence before presentation

- State the question, configuration, source revision, assumptions and acceptance criterion before presenting the result.
- Distinguish an analytical estimate, numerical screen, converged simulation, CAD geometry, measured test and operational observation. One cannot substitute for another.
- Identify actual software/version, input, command, raw output and coordinate/unit conventions. Native solver output plotted elsewhere is a computed plot, not an application screenshot.
- Show failed cases, unresolved discrepancies and omitted components. Numerical convergence is separate from physical uncertainty and model validation.
- A numerical score based on ordinal assumptions is not measured reliability. A nominal collision check is not a full-motion, tolerance or contact proof.

## Figures

Use a white report background, restrained colour-accessible palette, standard embedded fonts and meaningful line/marker distinctions in greyscale. Avoid ornamental gradients, shadows, oversized numbers and decorative cards in scientific figures. A structural diagram or workflow should show actual relationships and labelled boundaries.

Axes carry physical quantities and units. State frame, epoch and reference when they affect interpretation. Ordinary magnitude bars start at zero. Explain logarithmic, truncated or secondary axes. Use equal scales for geometry. Describe decimation, interpolation and missing data. Do not use a smooth path to imply uncomputed collision clearance.

Use sequential perceptually ordered maps for magnitude and a justified diverging map for signed deviations. Do not use a rainbow scale to decorate scalar data. Plot uncertainty with a stated definition and provenance; assumed sensitivity bands are not confidence intervals.

At intended publication size, target 8–10 pt figure text, at least 7 pt for secondary annotations, and consistent line widths; inspect exceptions rather than shrinking whole figures into unreadability. Prefer approximately 90 mm single-column or 180 mm two-column figure widths where the eventual venue permits. Department and selected-venue requirements take precedence. Slides need their own legibility inspection at projected size.

Retain an editable SVG or native vector source and PDF for line art; supply PNG previews. Embed PDF fonts and retain SVG text. Use at least 300 dpi for ordinary raster figure export at final size; screenshots retain their genuine native resolution. A higher dpi tag cannot add missing information. JPEG is suitable for photographs and some rendered CAD previews, not small text or precision line drawings.

## Captions and provenance

A technical caption states: (1) what is shown, (2) configuration and operating conditions, (3) source/model and evidence class, (4) uncertainty or sampling convention, and (5) the conclusion and its limit. Define panel letters, symbols and abbreviations. Record source and output hashes for released figure sets. Keep internal instructions, deadlines, scoring aspirations and private correspondence outside reviewer-facing documents.

Example: “Computed payload/host state difference after an imposed relative release. Orekit 13.1.6, stated central/J2 model and initial state; one-minute output samples. The numerical refinement bounds solver sensitivity for this model and does not establish physical release accuracy.”

## CAD, STEP, images and animation

Identify configuration/revision, units, coordinate datum, scale, section plane and hidden components. Use orthographic dimensioned views for interface evidence and perspective renders for orientation. Show storage, swept motion, handoff and safe-state envelopes. Indicate contact intended by design and quantify interference separately. Drawings need datums, tolerances, materials, finish and assembly notes appropriate to their release maturity.

A render is labelled as a render; a STEP-derived projection as such; a genuine application screenshot names the application and case. Do not synthesize application chrome or imply that an animation verifies mechanism motion. Retain the native CAD and STEP readback report alongside geometry-derived claims. Do not invent manufacturability or qualification from visual completeness.

## Reports and papers

Use a controlled terminology and symbol list, SI units with explicit conversions, justified significant figures and consistent frame/velocity definitions. Define every equation variable and cite the source or derivation. Separate requirements, assumptions, methods, results, discussion and conclusions. Tables identify units, evidence level and missing entries; use “not evaluated” rather than zero for missing results.

Each headline value traces to one configuration and result artifact. Compare alternatives on the same payload, epoch, mission outcome and installed-resource boundary. References support the specific claim and relevant edition; product marketing is not independent test evidence. Abstract and conclusion must agree with adverse findings. Manuscripts, deck and repository pages identify their evidence cutoff.

## Review and release

Run source/hash, link, export and build checks. Inspect actual figures, PDFs and slides at intended size; check clipping, text overlap, colour/greyscale readability and caption accuracy. Verify rendered web/mobile views. Mechanical checks cannot award scientific credibility or substitute for independent technical review. Every migration not yet inspected stays open in the private project register.

## References

- [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- [Nature panel construction](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
- [NASA display guidance, Appendix F](https://www.nasa.gov/reference/appendix-f-vol-2/) — operational display context, not manuscript or flight compliance.
