# FM08-R3 selected feeder — analytical and sequencing evidence

**Selected architecture:** guided lead-screw pusher transfer from four fixed, independently retained cells to one indexed reusable receiver. **Receiver indexer:** toothed belt with a 12 mm pitch-radius pulley and split clutch. **Runner-up:** rack and pawl. FDR10-R0 records the D27-R2 academic selection.

The engineering note is [REPORT.md](REPORT.md). The architecture trade and motion plots are in [results](results/). The editable FreeCAD/STEP assembly, part exports and actual nominal collision checks are a separate companion CAD package.

## Reproduce

```sh
python check_capture.py
python verify_feeder.py --no-plots
python build_report.py
```

The first command verifies the supplied hashes, independently substitutes the declared analytical quantities, and repeats all numerical/logic output in a clean temporary directory using only Python's standard library. Matplotlib is required only to regenerate the PNG/SVG figures:

```sh
python verify_feeder.py
```

## Interpretation

- Engineering judgment scores select an architecture under declared safety-led weights. Weight sensitivity and ranking reversals are retained.
- Drive sizing uses ambient manufacturer data and assumed resistance/efficiency. It does not establish installed thermal-vacuum capability.
- Static, tolerance and logic checks apply to stated model assumptions. The fault model executes a persistent four-cell campaign including empty return and guarded reset, and verifies interlock contracts, not actual sensors or latch reliability.
- The earlier FM06-R1 rigid-contact convergence result remains unestablished. It is not used to claim FM08-R3 precision or contact-force acceptance.
- Payload containment uses a continuously capped channel, proved far receiver stops, a braked rear pusher boundary and verified near capture tabs after sensed seating. The pusher does not pull or decelerate a free payload. Transfer is coast-only; drift, impact and settling are not predicted. No qualified ratchet or dynamic stopping distance is invented.

The 1U spacer is fixed in its cassette and stays out of the launch path. The nominal feed is 200 mm / 30 s; the receiver indexing reference is 900 mm / 20 s. The feeder-only four-payload allocation is 432 s, excluding launch, braking, charging, host recovery and orbital targeting waits.
