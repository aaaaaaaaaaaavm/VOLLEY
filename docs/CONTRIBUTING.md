# Contributing

VOLLEY is an evidence-first design study by Adityavardhan Mishra. I welcome reproducible discrepancies and independent checks.

## Working rules

1. Read [PROVENANCE.md](PROVENANCE.md), [BASELINE.md](BASELINE.md), [OPEN_PROBLEMS.md](../OPEN_PROBLEMS.md) and the applicable run sheet before changing a claim.
2. Declare and commit acceptance criteria before implementing or executing a new analysis. Keep failed bands, original results and withdrawn interpretations visible. A revised question needs a separately dated run.
3. Treat controlled inputs and executable analysis as the source of computed numbers. Check the equation, units, assumptions and model scope independently; agreement between files alone does not establish correctness.
4. Label assumptions, external data, computed results, independent numerical checks and measurements accurately. No hardware measurement exists in this programme.
5. Record substantive corrections in [CHANGELOG.md](../CHANGELOG.md), including the cause and source of truth. Do not silently change the operating point or relax a threshold.
6. The flagship holds engineering evidence. Manuscripts are authored in VOLLEY-paper and VOLLEY-thesis. Fix exported evidence here and regenerate the companions; preserve their authored manuscript directories.

## Reproduce and verify

Use Python 3.12 or newer for the pinned environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
bash tools/verify_all.sh
```

The gate requires a clean committed checkout. `--full` additionally regenerates CAD and selected results; CAD requires the optional dependency documented in [requirements.txt](../requirements.txt). External solver reproduction has separate requirements in [tools/env-setup.sh](../tools/env-setup.sh).

The repository has CI and a property/regression test suite. CI passing establishes only the checks it executes. The single local verification command also checks the README overview and artifact currency. A skipped test is not a pass.

## Coherent publication

Commit the flagship changes, run `python tools/export_companion.py --out ..`, commit generated changes in both companions, then commit the flagship export record. Run the gates before publishing the coherent batch. Do not push an intermediate flagship commit with stale companion payloads.

## Licence and citation

The current licence is [CC BY 4.0](../LICENSE); [LICENSING.md](../LICENSING.md) explains scope and history. Use [CITATION.cff](../CITATION.cff). Describe the work as a computational design study with no experimental validation.
