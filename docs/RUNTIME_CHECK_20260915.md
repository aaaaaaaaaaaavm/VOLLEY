# Local CAD verification incident, 2026-09-15

The terminal-state timing batch's first local verification run passed the orbital
checks and 92 tests, but the CAD artifact gate could not rebuild either generation.
A direct `import cadquery` terminated with a bus error; both rebuild subprocesses
returned -7. No CAD source or geometry changed in this batch.

The checker previously collapsed a failed rebuild and a demonstrated output difference
into the same false return value, then printed STALE for both. It now reports a
configured rebuild failure as UNVERIFIED, retaining its return code and stdout/stderr.
Both STALE and UNVERIFIED still fail the gate. Two added tests exercise a failing
subprocess and verify that unavailable computation cannot become a successful check.
The full test suite subsequently passed all 94 tests.

## Observed resolution

A fresh local installation of the native dependencies, ending with the same declared
CadQuery 2.8.0, cadquery-ocp 7.9.3.1.1 and VTK 9.6.2 versions, restored the import.
Re-running `python3 tools/check_artifacts.py` then rebuilt the Gen5 and Gen6 packages
byte-identically and passed all seven artifact checks. This resolves the observed
verification blockage; the precise underlying cause of the original native crash
was not established. No geometric correction was needed or claimed.

The other local gates passed in the initial run. The later artifact pass resolves
that run's only failed gate. The GitHub orbital/integration workflow does not include
this native CAD rebuild, so its status alone is not evidence of CAD reproducibility.
