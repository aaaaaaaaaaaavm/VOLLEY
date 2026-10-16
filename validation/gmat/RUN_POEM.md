# Run the A15 orbital screen in GMAT

This run checks a specified set of twelve payload orbits after ideal instantaneous releases. It does not simulate a loading mechanism, a release force history, or a host that changes state after each shot. The current reproducible R1 input uses a 4 kg payload, a 300 kg retained host, a 16.029 m/s *relative* separation speed, and shots spaced 1200 s apart.

The earlier A15 report used a 16.388 m/s input and reported a 367° RAAN spread. That number is not a valid circular spread. Its R2022a report files are absent from this checkout, so those verdicts remain historical, unverified claims. The current R2026a R1 raw reports and review are in the [versioned audit bundle](https://drive.google.com/file/d/1aHwr5eszoDd9ywXlpL9qCrOCdsdMIxqD/view). R2 and R3 orbit definitions still lack verified provenance.

## Generate the inputs

From the repository root:

```sh
python validation/gmat/build_poem_campaign.py
```

The generator reads `analysis/results/motor_results.json`. It writes the current speed and twelve initial states into `validation/results/A15_poem_campaign.json` and GMAT scripts into `validation/gmat/output/`. These regenerated inputs were state-reconstruction checked on 16 October 2026; no new native run is claimed. The states account for the host's orbital position at each scheduled shot and split relative speed between payload and retained host by momentum conservation. They preload post-release orbits at a common epoch. That construction is an input approximation, not a sequential host propagation.

Run the state reconstruction check before GMAT:

```sh
python validation/gmat/test_orbit_state.py
```

The test checks the twelve release states against independently reconstructed two-body states. It cannot test perturbations, release contact, or host recovery.

## Execute R1

Use the `GmatConsole` or `GmatConsole.exe` from GMAT R2026a. Replace the executable path for your installation:

```sh
GmatConsole --run validation/gmat/output/a15_poem_r1.script
```

The generated script contains absolute output paths, so regenerate it on the computer that will run GMAT. Retain the console log, GMAT log, generated script, and all twelve files under `validation/gmat/output/r1/`. Confirm that all twelve report files have synchronized timestamps and that the final timestamp is 1 April 2027 for the default 90-day case. A process exit code alone is not a result check.

## Read the native reports

```sh
python validation/gmat/parse_poem_campaign.py
```

This parser reads the twelve R1 reports and writes `validation/results/A15_R1_gmat_r2026a_review.json`. It reports sampled separation, inclination and altitude values, and the shortest circular RAAN span. It does not accept an `--analysis` argument. `parse_reports.py` belongs to a different study and must not be used for A15.

For the audited 2026-09-30 R1 run, the twelve reports each had 59,590 data rows. The initial inclination, altitude-extent and RAAN-offset checks and the final circular RAAN-spread check met their stated numerical thresholds. The nearest separation at the 90-day report samples was 247 m. A separate five-second GMAT window around that encounter found 190 m at a sample and about 180 m by linear interpolation. The sparse remainder of the 90-day reports does not establish continuous clearance above 100 m. The semimajor-axis comparison only checks the generated GMAT input. Keep the full band-6 verdict unresolved.

The report does not close the coupled deployment task. It holds the host at 300 kg for each constructed shot and does not propagate host recoil, mass depletion, navigation, manoeuvres, or actual release timing through the campaign. Do not use R2 or R3 to make mission claims until their reference orbits and native outputs are checked.

## Archived run identity

[Native capture manifest](evidence/A15_R1_NATIVE_CAPTURE.json) records input/log/raw-report hashes for the 30 September execution. The archived raw reports were reparsed on 16 October. Regeneration today does not make that archived run a new execution. The captured result is in [the local JSON](../results/A15_R1_gmat_r2026a_review.json), with [fine-window results](../results/A15_R1_FINE_WINDOW_RESULT.json).
