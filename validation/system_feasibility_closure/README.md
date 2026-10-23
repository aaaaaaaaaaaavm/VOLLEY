# Selected-feeder capacity and system-resource assessment

This standalone computational package accompanies the selected FM08-R3 guided
lead-screw feeder. It contains an actual twelve-cell scaling assembly with one
receiver, conditional finite-force orbital campaigns, analytical resource bounds
and parametric lunar navigation sensitivity. The evaluated Gen5 record remains
separate and unchanged.

The selected pusher operates within continuously capped channels against a
receiver far-side stop. It contains the payload but cannot pull or enforce
deceleration of a freely moving payload. Nominal feed/index handling is reserved
inside host zero-force coast windows. End-stop impact and sensed settling remain
physical-validation requirements; nominal kinematic geometry is not a contact
dynamics acceptance.

The material and catalog-option ledger is partial. The 10/25/50 kg omitted-equipment
allowances are sensitivity assumptions. No complete installed mass, measured
release precision, selected host, useful lunar lifetime or flight qualification
is established by this package. `REPORT.md` and its PDF state the applicable
model boundaries and quantitative findings.

`source_inputs/` preserves the source-revision records and prior-study inputs
used for provenance. Current selected-feeder results are the SYS-01, LNS-01,
CAP-12 and FBR-02 outputs in the package root; archived FBR-01 proxies are not
current installed hardware ratings.

## Verify captured evidence

```bash
python3 check_capture.py
```

The standard-library checker verifies captured hashes, reduced-mass energy,
charging identities, numerical-study counts, geometry identities and native-run
consistency. It does not rerun FreeCAD, orbital targeting or physical tests.

Run rebuilding commands in a separate copy of the captured package. Native CAD
and PDF metadata can change on regeneration; the recorded hashes identify the
reviewed captured files, while numerical comparisons establish recalculation
consistency.

## Recalculate the sensitivity studies

```bash
python3 system_screens.py
python3 lunar_navigation_sensitivity.py
python3 plot_screens.py
```

NumPy is required for the lunar sensitivity calculation; Matplotlib is required
for scientific plots. `SYSTEM_SCREENS.json` contains explicit efficiency,
charging, acceleration, thermal and attitude-response assumptions.
`LUNAR_NAVIGATION_SENSITIVITY.json` contains the assumed covariance bands,
sample counts and finite-difference derivative checks. Their figures are derived
scientific plots, not application screenshots or experimental data.

## Rebuild the actual twelve-cell assembly

Use FreeCAD's Python modules with the copied, hash-identified selected source:

```bash
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_twelve.py \
  --source source_inputs/build_selected_R3.py
PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 extract_native_mass.py \
  --source source_inputs/build_selected_R3.py \
  --native cad_twelve/FM08_R3_twelve_cell_stowed.FCStd
python3 check_step_exchange.py
```

The final command uses CadQuery/OCC to read the STEP exports separately and
check BRep validity, solid counts and volume consistency. This checks numerical
exchange within the Open CASCADE kernel family; it is not independent-kernel
certification. Native assemblies, STEP files, material mass/CG/inertia and
nominal interference findings are retained in `cad_twelve/` and
`TWELVE_ASSEMBLY_REPORT.json`.

## Retarget and replay the orbital cases

```bash
python3 mission/run_selected_matrix.py \
  --four-report source_inputs/FOUR_ASSEMBLY_REPORT.json \
  --twelve-report TWELVE_MASS_LEDGER.json \
  --catalog-reference source_inputs/SELECTED_CATALOG_OPTIONS.json
python3 mission/export.py
python3 mission/replay_and_check.py --classpath '/path/to/locked/orekit/jars/*'
python3 plot_integration.py
```

The public dependency versions and hashes are in `mission/SOFTWARE_LOCK.json`.
Java 21 and SciPy are required. The FBR-02 targeter is a recorded derivative of
FBR-01, adding a five-second zero-force pre-release guard. The original FBR-01
targeter is retained in `source_inputs/FBR01_target.py`. The same full-state
targets, epoch and relative release vectors are supplied to both architectures;
conventional spring controls are also evaluated without imposing VOLLEY's
specific feeder handling time.

Native Orekit CSVs and console logs are genuine software outputs. Frozen-command
probes vary force, release speed, initial position and actual 3U mass. Their
terminal errors are deterministic sensitivities rather than calibrated flight
delivery statistics. Source, software and artifact identities accompany the
captured outputs.
