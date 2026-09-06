# A24-R: current-reference manifest agreement

Declared 2026-09-06 before the new evaluator exists or runs. I retain A24's original band 1 and its failed 6.375 kg literal unchanged.

## Question and frozen acceptance

Does the fixed-cell 3U calculation agree with the current independent payload-family calculation after the enclosure correction?

1. The 3U fixed-cell count must equal 12 and the current payload-family 3U count.
2. Its kg per satellite must agree within 1 percent with the current payload-family 3U output. This is the original tolerance, now tied to a named live source rather than a stale literal.
3. Both generators must reproduce their committed inputs to this comparison. Preserve A24 bands 2-6 and report their existing verdicts separately; they are not re-declared or overwritten by A24-R.

A pass closes P54's stale-reference comparison only. It does not close the mass kill criterion, select D2, or erase A24 band 6. Results belong in a new `analysis/results/cell_manifest_reference.json`.

## Result, 2026-09-06

Declared at commit `e0a3cf611824efe19d045cab4fc73dcdfaa7abca`. Both generators reproduced before this comparison. Count: 12 in both. Fixed-cell mass: 10.55 kg/satellite; current reference: 10.55 kg/satellite; relative difference: 0.000000000%. Both current-reference checks pass. Original A24 bands 1 and 6 remain failed. The new result is [cell_manifest_reference.json](../analysis/results/cell_manifest_reference.json).
