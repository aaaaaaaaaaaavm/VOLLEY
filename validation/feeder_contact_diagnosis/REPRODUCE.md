This package preserves the failed FCE12 baseline and six completed FCE13 diagnostic runs. The two APGD files are deliberately terminated pilots and contain no valid 26.5 s endpoint. Every completed run's exact native command, environment overrides, wall time, native source hash, executable hash and output hashes are in runs/*.record.json. APGD commands and last complete output times are in runs/*.aborted.json. The old stage2 wrapper expected endpoint metrics after termination and ended with FileNotFoundError; that wrapper error is not a completed native result.

Use the existing Chrono 10.0.0 SDK or an equivalent local build. This workspace's SDK is /workspace/volley-work/native-tools/chrono10/build/cmake; its source and loaded library identities are recorded under references/ and NATIVE_DEPENDENCIES.json. The source, geometry and assumptions are unchanged from the identities recorded with the runs except the explicitly labelled numerical/representation variants. The complete baseline 250 µs CSV matches P3-250 byte for byte. Rebuilding can change executable bytes across toolchains or paths; compare trajectory/metrics and record the new executable identity.

Verify the packaged source/output files from the package root:

```bash
python3 check_capture.py
```

Build in the current workspace:

```bash
/workspace/volley-work/chrono-build-env/lib/python3.12/site-packages/cmake/data/bin/cmake -S . -B build -G Ninja -DCMAKE_MAKE_PROGRAM=/workspace/volley-work/chrono-build-env/bin/ninja -DChrono_DIR=/workspace/volley-work/native-tools/chrono10/build/cmake -DCMAKE_BUILD_TYPE=Release
/workspace/volley-work/chrono-build-env/lib/python3.12/site-packages/cmake/data/bin/cmake --build build -j2
```

Replay the completed diagnostic cases in fresh output directories. The driver refuses to overwrite existing CSVs or completed records. A run executes native steps at the specified timestep with 1 ms controller updates and 10 ms CSV output. It also preserves a diagnostic JSON summarizing all native steps; the solver CSV is sampled at 10 ms.

```bash
FCE_RESULTS_DIR="$PWD/replay-stage1" /workspace/volley-work/runtime-volley-core/bin/python run_selected.py '[["P3-250","3U",0.00025,2000,0,"PSOR",0.1],["W3-250","3U",0.00025,2000,1,"PSOR",0.1]]'
FCE_RESULTS_DIR="$PWD/replay-stage3" FCE_EXE=feeder_bb_probe FCE_SOURCE=feeder_bb_probe.cpp /workspace/volley-work/runtime-volley-core/bin/python run_selected.py '[["B3-250","3U",0.00025,2000,0,"BB",0.1],["B3-125","3U",0.000125,2000,0,"BB",0.1]]'
FCE_RESULTS_DIR="$PWD/replay-stage4" FCE_EXE=feeder_box_probe FCE_SOURCE=feeder_box_probe.cpp /workspace/volley-work/runtime-volley-core/bin/python run_selected.py '[["X3-250","3U",0.00025,2000,0,"PSOR",0.1],["X3-125","3U",0.000125,2000,0,"PSOR",0.1]]'
```

Regenerate comparison tables and the manuscript figure from the supplied completed runs:

```bash
/workspace/volley-work/runtime-volley-core/bin/python analyze_selected.py
MPLCONFIGDIR="$PWD/.mpl-cache" /workspace/volley-work/runtime-volley-core/bin/python make_review.py
```

Source variants: feeder_probe.cpp adds observation and an optional native APGD switch to FCE12; feeder_bb_probe.cpp adds the native BB switch; feeder_box_probe.cpp additionally substitutes the exact box primitive for payload_cell_00.obj. Full CAD mass/inertia, eight external rail cells, drive constraints, sampled control, friction, gravity, guard checks, collision tolerances and endpoint remain as documented. CORE_BOX_EQUIVALENCE.json records corner/plane/volume checks. No physics change or new acceptance limit was introduced.

Solver diagnostic caution: PSOR GetError is a reported normal/joint violation statistic. BB GetError is the absolute projected-gradient norm; its native stopping test divides that norm by the initial-gradient norm. The values are not interchangeable. A full-budget count can include a solve that first meets tolerance on the last iteration. Mixed translational/angular joint residuals are not direct pose-error measurements. No rigid-contact force peak is qualified.
