# Reproduction boundary and public adapters

The original accepted engineering files remain byte identified in `PROMOTION_ORIGIN.json`. `MANIFEST.json` identifies this public package, including its portable runner. A capture check verifies stored identities and recorded acceptance criteria; a reproduction run executes a stated model. Neither implies physical correlation.

| Entry point | Required inputs and actual boundary |
|:--|:--|
| `reproduce.py interlocks` | Standard-library state/fault specification; independent missing-proof and custody cases; no sensor/hardware measurement |
| `reproduce.py shot` | Captured native home BOM, finite-force/arrest map and phase-A resistance; recomputes the averaged model, not field/FEA inputs |
| `reproduce.py mission` | Local `mission/provenance/target.py`, coupled-shot calibration and synthetic full-state targeting; NumPy/SciPy required |
| `reproduce.py native` | Java 21, exact locked Orekit/Hipparchus jars and frozen commands; scratch adapter replaces only the original jar-directory selector |
| `analysis/design_budgets.py` | Included phase-A/B/C current arrays and native chassis-review output; analytical/material assumptions remain explicit |
| `analysis/lift_sizing.py` | Factual catalog JSON plus publisher text acquisition described below; exact original text hash retained in captured output |
| Native CAD and FE mesh rebuild | FreeCAD/Part runtime, recorded baseline solids, optional solver dependencies and raw supplement; no clean-machine full native rebuild is asserted |

Run source scripts in a disposable copy. Several original scripts intentionally write their result JSON adjacent to source. The runner handles this for its four documented examples. Original native replay commands and legacy provenance records contain execution-time filesystem paths; those paths identify historical execution and are not required by the portable entry points.

## Publisher-controlled documents

No vendor PDF or complete extracted vendor text is redistributed. `sources/feeder_catalog_reference.json` and `analysis/POWER_COMPONENT_REFERENCE.json` contain factual reference values, source URLs and captured hashes. Supplier geometry/rating/environmental acceptance remains outside the computational screen.

The original lift screen hashes `sources/faulhaber_ratios.txt`, although its ratio 19.8 is an explicit numeric input. To regenerate its original receipt, obtain **EN_GEARHEADS_REDUCTION_RATIOS.pdf** from the Faulhaber URL in the catalog JSON (captured PDF SHA256 `0a103da9576a4c440b6b7fef21da5f1bbaf789d3a70790e7ffd43a77ac32f9ba`), extract text using `pdftotext -layout`, and place it at that path in a scratch copy. Text extraction versions can change byte hashes without changing the declared ratio. A different source revision must be recorded as such; do not silently substitute a changed vendor document and claim the original input identity.

## Raw supplements and checks

`SUPPLEMENT_ASSETS.json` records the exact two repository-contained byte parts, complete archive identity and the 60 original raw conductor/structural file identities. Both parts are smaller than 30 MB. They restore the exact original archive without private Drive access or a release-asset URL; `download_url` is deliberately null because repository-contained parts are the active distribution.

```bash
python3 validation/acr1/supplements/materialize.py --verify-only
python3 validation/acr1/supplements/materialize.py --output /tmp/volley-acr1-raw
```

The standard-library materializer checks both part hashes/sizes, the assembled 48,246,658-byte ZIP SHA256 and every decompressed member before writing. It rejects paths outside the requested scratch root, symlinks, duplicate/unknown entries and unsupported entry types. Any nonmatching existing destination aborts the preflight; matching files are retained. New files are committed exclusively and never replace existing files. `--verify-only` performs all content checks without extracting.

For a full native/mesh-dependent reproduction, first copy `validation/acr1` into a new scratch package directory, then materialize with that directory as `--output`. The restore adds the original raw files alongside the already supplied source/results. The Git payload retains all eight native/STEP states, all mission raw command/replay data, accepted result JSON and current arrays needed by the secondary budgets. A full physics rerun remains separate from distribution verification and the short example. The original archive hash and every scientific raw-file hash are unchanged.

The frozen mission narrative used “measured” to refer to numerically sampled model outputs. Public prose uses “computed” to avoid implying physical measurements. This wording correction changes no numerical output. Public documentation adapters and their original hashes are recorded in the promotion origin ledger.
