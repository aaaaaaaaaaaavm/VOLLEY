# Engineering figure conventions

Figures should make the calculation inspectable. Titles name the physical quantity and case. Axes include units and readable ticks; captions identify the source, model boundary, revision and uncertainty. A photograph, solver screenshot, CAD projection, render and computed plot are different evidence types and are labelled accordingly.

Use a white background for reports, a standard sans-serif face, black text and a small set of colour-accessible line colours. Different line styles or markers should retain meaning in greyscale. Avoid decorative icons, gradients, shadows and large metric panels where a labelled graph or table communicates the result. Use honest aspect ratios, equal scales for geometric comparisons, and a zero origin for ordinary magnitude bars. An inset may expose a short event without concealing the full range.

Numerical convergence is separate from physical uncertainty. Plotting the same result in two colours does not provide independent evidence. A comparison must state whether inputs, epochs, forces and coordinate conventions match. Show unresolved discrepancies and failed cases. A sparse trajectory plot cannot establish continuous collision clearance.

Export plots as editable SVG and PDF with embedded text, plus a readable PNG for repository previews. Inspect the final exports at their intended report or slide size. Retain the source and input table. Native solver logs and source hashes belong with the numerical evidence; a plot of native output is labelled as a computed plot, not a screenshot of a graphical application.

## References

These conventions adapt general scientific publishing guidance; they do not assert venue compliance or agency endorsement.

- [Nature research figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/): axes, units, accessible colours, legible text and editable exports.
- [Nature figure-panel construction](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/): consistent construction and export.
- [NASA display standard, Appendix F](https://www.nasa.gov/reference/appendix-f-vol-2/): meaningful titles, labels and operator-readable displays. Its operational display requirements are contextual guidance here, not a VOLLEY compliance claim.
