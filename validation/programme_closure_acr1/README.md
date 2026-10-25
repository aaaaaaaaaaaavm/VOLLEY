# Programme calculations linked to ACR1

This package adds numeric host demand, matched installed-mass necessary bounds,
distinct lunar starting-energy budgets, signed lunar release maps, inverse
release covariance requirements, and engine-only lunar disposal with failed
payloads retained. The near-term ACR1 machine and the independent lunar surrogate
have different identifiers and mass ledgers.

Read [the study report](../../docs/PROGRAMME_STUDIES_ACR1.md),
[frozen study inputs](study_inputs.json), [numerical results](STUDY_RESULTS.json),
[native lifetime results](LUNAR_NATIVE_RESULTS.json),
[native disposal results](DISPOSAL_NATIVE_RESULTS.json), and
[navigation requirements](NAVIGATION_REQUIREMENTS.json).

The [coupled lunar campaign](CAMPAIGN_REPORT.md) now records the actual
7,152-candidate order/direction search, 20 finite-host policy/authority/fault cases,
independent native host replay and 24 perturbed payload lifetime runs. The
[C7 requirement flowdown](C7_HARDWARE_REQUIREMENTS.md), [H0 numeric demand
sheet](H0_DEMAND_SHEET.md), [H5 questions](H5_PROVIDER_QUESTIONS.md) and
[notional interfaces](H5_INTERFACE_SKETCH.md) connect those outcomes to the
original hardware and external-interface tasks.

Existing [native lunar coast](../lunar_native_coast/README.md),
[navigation sensitivity](../system_feasibility_closure/LUNAR_NAVIGATION_SENSITIVITY.json)
and [ACR1 mission](../acr1/mission/README.md) evidence is reused. The current run
extends coast evidence to signed release vectors and finite engine-only disposal.
It does not replace the prior 180-day outcomes with a shorter success horizon.

Verify exact supplied files and independent invariants:

```bash
python check_capture.py
python reproduce_and_compare.py
python reproduce_campaign.py
```

Reproduce arithmetic, finite-burn two-body targeting, covariance and figures:

```bash
python -m pip install -r requirements-python.txt
python complete_studies.py
python navigation_requirements.py
python build_report.py
python lunar_campaign.py
python campaign_report.py
```

`complete_studies.py --no-plots` skips figure creation. The scientific style is an
exact copy of the repository's shared style. Matplotlib may need a writable
`MPLCONFIGDIR` in restricted environments. The report builder writes only the
source-derived figures here and `docs/PROGRAMME_STUDIES_ACR1.md`.

Native reproduction needs a separate GMAT R2026a installation, GRGM900C,
DE421 ephemerides and the lunar SPICE PCK/frame files distributed with it. No
third-party solver, gravity or ephemeris binaries are included here. Runtime and
data hashes are pinned in `native/SOURCE_IDENTITY.json`.

For a new installation, use the portability adapter. It accepts an executable
path or command and a normal GMAT distribution root, writes a new startup file
with writable output paths, and leaves every captured source/report unchanged:

```bash
python replay_native_portable.py --gmat /path/to/GMAT/bin/GmatConsole \
  --gmat-root /path/to/GMAT --script campaign_native/point_mass.script \
  --output-dir /path/to/new-replay
```

`GMAT_CONSOLE` and `GMAT_ROOT` environment selectors can replace those CLI
arguments. `--gravity` can select a different coefficient file explicitly. The
required distribution inputs are `data/gravity/luna/grgm900c.cof`,
`data/planetary_ephem/de/leDE1900.421`, the lunar SPICE PCK/frame files under
`data/planetary_coeff/`, `data/time/tai-utc.dat`, and
`bin/gmat_startup_file.txt`. Their captured hashes and the actual R2026a console
build identity are in `native/SOURCE_IDENTITY.json`; no private workspace path is
needed to execute the adapter or numerical generators. A different runtime is
recorded as different evidence in the replay receipt.

The actual [portable replay capture](portable_replay_capture/REPLAY_RECEIPT.json)
records a cold point-mass replay with bit-identical decompressed numerical output
and an unchanged original source hash. Its translated script/startup/log remain
separately identified; they do not replace or relabel the original executed
capture. Other accepted scripts in `native/`, `disposal_native/`,
`campaign_native/` and `campaign_disposal/` can be selected with `--script`.

Initial-state arithmetic retains the declared lunar parameter
4902.800118 km³/s². Native GRGM900C dynamics use the potential-file parameter
4902.79996708864 km³/s² and 1738 km harmonic reference radius; the separate stop
sphere is 1737.4 km. These model constants have distinct roles. SPICE/MOON_PA is
the adopted coefficient frame, with the physical alignment limitation retained
from the existing native coast study.

```bash
python lunar_native.py --gmat /path/to/GmatConsole \
  --gravity /path/to/data/gravity/luna/grgm900c.cof --run
python disposal_native.py --gmat /path/to/GmatConsole \
  --gravity /path/to/data/gravity/luna/grgm900c.cof
python campaign_native.py --gmat /path/to/GmatConsole \
  --gravity /path/to/data/gravity/luna/grgm900c.cof
python campaign_disposal.py --gmat /path/to/GmatConsole \
  --gravity /path/to/data/gravity/luna/grgm900c.cof
```

The native runners reuse existing `.txt.gz` reports. To independently recompute,
use a separate copy of this package and remove its `native/` and
`disposal_native/` output directories first. Scripts retain the actual absolute
runtime paths from capture; regeneration replaces them from the supplied runtime
path. The GMAT distribution data layout must be preserved. Runtime plugin warnings
for unused Python/MATLAB/visualization plugins are recorded in genuine logs; the
native console mission completions and raw histories are the evidence of runs.

The 30-day lunar criterion is a sampled 20 km spherical altitude floor. Native
sphere stops are distinct from terrain impacts, useful service or accepted
disposal. Engine thrust/Isp, navigation bands and hardware allocations are declared
study assumptions. A controlled impact site, actual engine, customer/host
interfaces, material measurements, perturbed covariance and independent human
review remain external or unfinished. The operational lunar campaign is now
computed with an imposed post-arrest source-calibrated point release; physical
pulse/contact dynamics and demonstrated host control authority remain separate
acceptance gates. Its native open-loop host drift also exceeds the assumed
standalone navigation bands, so full-campaign precision is not claimed.

[Criterion recommendations](CRITERION_RECOMMENDATIONS.json) cover the 40 existing
programme rows. They are bounded evidence assessments; no tracker state is changed
by this package.

[FIGURE_SOURCE_INVENTORY.json](FIGURE_SOURCE_INVENTORY.json) maps all three plot
families to their actual sources, data, styles, evidence roles and output hashes.
After an authorized package edit, regenerate that inventory and the package-local
manifest with `python freeze_manifest.py`, then rerun `python check_capture.py`.
