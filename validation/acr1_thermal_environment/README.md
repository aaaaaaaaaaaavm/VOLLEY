# ACR1 environmental thermal sensitivity

A separately identified computational study of the ACR1 thermal operating envelope. Read [the report](../../docs/ACR1_THERMAL_ENVIRONMENT.md) for the heat-path requirement, voltage variant, numerical sensitivities and physical acceptance conditions. The accepted ACR1 core is unchanged.

## Reproduce

Python 3.12 was used. Main solver/replay dependencies are NumPy and SciPy; figures also need Matplotlib. Exact captured versions are in `ENVIRONMENT.json`. No network or private workspace is needed for numerical replay: accepted inputs and both radiation resolutions are included.

```bash
python -m pip install -r requirements-python.txt
python check_capture.py
python portable_replay.py
```

The portable replay copies only this study into a fresh temporary directory, reruns all 18 production shot cases, compares their output hash, and reruns the refined hot corrected thermal corner. It uses neither the repository parent nor sibling private analyses.

To regenerate all thermal results, roots, numerical checks and figures, in order:

```bash
python derated_source_variant.py
python thermal_network.py
python thermal_corrections.py
python verify_numerics.py
python portable_replay.py
python make_figures.py
python check_capture.py
```

The 64-point sensitivity sweep and root solves take longer than the quick check. Figure PDF bytes can vary with Matplotlib creation metadata; scientific numeric outputs and figures are checked against their captured source inventory. Regeneration changes captured files; use a disposable copy to preserve the released packet. The original 1 W/K and 2.5 W/K diagnostic results/scripts remain under `results/` and `inputs/` with diagnostic names.

## Optional geometry reconstruction from the public frozen STEP

The solver uses the included CAD caches. Rebuilding them requires CadQuery/OCP plus the extra geometry requirements, and the normal public STEP from the same repository revision:

```bash
python -m pip install -r requirements-geometry.txt
python cad_radiation_geometry.py --step ../acr1/cad/release/VOLLEY_G5_ACR1_home.step --samples 4096 --all-stages
python cad_radiation_geometry.py --step ../acr1/cad/release/VOLLEY_G5_ACR1_home.step --samples 8192 --all-stages
```

`--step` accepts any installation path to the hash-pinned STEP. The BRep contact classifier and deterministic ray seeds are preserved. No geometry rebuilding is required for portable replay. `capture_inputs.py` is the historical acquisition utility: it copies the public core and attempts primary-source downloads; ordinary replay does not run it or need internet access.

## Evidence

- `THERMAL_INPUTS.json`: explicit environment, duty, parameter bands and assumptions.
- `THERMAL_RESULTS.json` and `results/*.json`: six baseline campaigns and 128 sensitivity campaigns; retained hot failure.
- `THERMAL_CORRECTIONS.json`: actual root trials, 3 W/K mass/conductance allocation, both voltage configurations and contact contexts.
- `DERATED_SOURCE_RESULTS.json`: 18 separately named 78.4 V cases; original AST restoration and 30 mV group allowance.
- `NUMERICAL_VERIFICATION.json`: time/ray refinement, independent energy/radiosity checks and retained 2.5 W/K margin diagnostic.
- `PRIMARY_SOURCE_REGISTER.json`, `PRIMARY_FACTS.json`, `INPUT_SOURCE_MANIFEST.json`: source/version/hash identities and truthful access outcomes.
- `PUBLIC_SOURCE_MANIFEST.json`, `CAPTURE_CHECKS.json`, `PORTABLE_REPLAY.json`: frozen-file, source-preservation and portable replay receipts.
- `FIGURE_SOURCE_INVENTORY.json`: scientific plots, exact inputs and hashes.

The computational study is complete within its declared scope. Named materials, actual placement, contamination controls and vacuum/circuit correlation are subsequent physical acceptance requirements.
