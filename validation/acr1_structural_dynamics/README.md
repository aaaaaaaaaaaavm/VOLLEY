# SD01 — ACR1 structural dynamics and conditional airgap

Separate follow-on study using the exact accepted connected-chassis mesh. It leaves the frozen ACR1 engineering/static/ED1 package unchanged.

[Scientific report PDF](STRUCTURAL_DYNAMICS_REPORT.pdf) · [Report source](STRUCTURAL_DYNAMICS_REPORT.md) · [Modal results](MODAL_RESULTS.json) · [Response cases](RESPONSE_RESULTS.json) · [Current-induced normal force](CURRENT_NORMAL_FORCE.json) · [Physics/design-limit comparison](PHYSICS_LIMIT_COMPARISON.json) · [File identities](MANIFEST.json)

## Decisions supported by the calculation

- Actual CalculiX 2.23 extraction: six numerical rigid modes and 40 elastic modes, **131.4105–2052.744 Hz**, on the accepted 112,519-node / 62,198-C3D10 bare chassis. Static gauge constraints are removed for true free-free modes.
- All 54 declared finite principal-3 m/s sensitivities retain conditional paired clearance. The adverse 50 µs refinement leaves **0.282788 mm paired budget**, including the original static/thermal/tolerance allocations and added modal-residual reserve.
- An adverse sustained resonant harmonic has a **64.687 N** conditional normal-force limit at assumed 0.5% damping. A continuous 5% normal-force harmonic exceeds that budget.
- Representative reciprocal current/PM calculations give **7.500 N** maximum absolute ideal-thrust-phase normal force, **29.091 N** at ±5° and **76.687 N** at ±15° phase sensitivity, at the supported maximum 423.199 A. The representative arbitrary-phase envelope is 295.711 N. A station-based continuous-resonance phase-error screen is about ±12.6°.
- Accepted native static nodal extrapolated von Mises peak: **24.662 MPa**. The adverse finite stress bound at 148 declared integration-point monitors, including the accepted hotspot's element, is **59.411 MPa** with 130% monitored DC loading. No alloy/yield/fatigue qualification is assigned.

The ~3.01 kN permanent-magnet pinch remains DC preload. It is not used as a full-amplitude oscillatory input. Current-induced opposed reaction and common-mode reaction are computed separately. Bare chassis and uniform-density mass sensitivities do not represent complete installed sled/payload/stator/host modes. Positive paired budget assumes the original centring allocation and does not prove both actual installed gaps.

## Native and numerical evidence

| File | Actual role |
|:--|:--|
| `runs/free_free/modal.inp` | Exact source nodes/connectivity/stiffness, added declared density, removed six static gauge constraints, modal/stress output requests |
| `runs/free_free/modal.dat` | Actual native eigenvalues, mass-normalized patch modes and monitored integration-point stresses |
| `runs/free_free/SOLVER_STDOUT.txt` | Genuine CalculiX solver output and completed-job receipt |
| `runs/free_free/modal.frd` | Native job geometry exchange; modal result fields are in the DAT, not fabricated GUI output |
| `MODAL_BASIS.npz` | Parsed native modes, exact paired-face interpolation, stress tensors and accepted static-field comparison |
| `SOURCE_SHOT_FORCE.csv` | Captured 2 ms current trace combined with source force/arrest coefficients; switching is unresolved |
| `FINITE_CASES.csv`, `RESPONSE_CURVES.npz` | Actual reduced-model finite histories, sensitivities and clearance/stress bounds |
| `CURRENT_NORMAL_FORCE.json` | Actual split-array vector integration at representative active/arrest stations, with a refined interior and FE-current cross-check |
| `FIGURE_MANIFEST.json` | Source-linked PNG/PDF/editable-SVG figures; numerical plots are not screenshots or measurements |

Convergence checks include 10/20/40-mode static reconstruction, 20/30/40-mode response, 100→50 µs time refinement and independent C3D10 stress recovery against native output. This is one accepted mesh; full assembly modal/stress mesh qualification is not claimed. The representative normal map omits full stroke/phase/brake coverage, AC/reaction fields, detailed cables and calibrated controller errors.

## Reproduce in a disposable repository checkout

The workflow writes new SD01 outputs beside its scripts. Use a separate checkout or full scratch copy; retain accepted captures for comparison. Install `requirements.txt`, CalculiX 2.23, Pandoc/XeLaTeX for the report, and the source raw solver supplement restored by the existing repository materializer.

```bash
python validation/acr1/supplements/materialize.py --output /tmp/volley-acr1-source-raw
python validation/acr1_structural_dynamics/prepare_modal.py --raw /tmp/volley-acr1-source-raw --hotspot-node 2411
```

From `validation/acr1_structural_dynamics/runs/free_free`, run:

```bash
OMP_NUM_THREADS=2 CCX_NPROC_STIFFNESS=2 ccx -i modal > SOLVER_STDOUT.txt 2>&1
```

Then from the repository root:

```bash
python validation/acr1_structural_dynamics/collect_modes.py --raw /tmp/volley-acr1-source-raw
python validation/acr1_structural_dynamics/respond.py
python validation/acr1_structural_dynamics/current_normal_force.py
python validation/acr1_structural_dynamics/make_report.py
```

The vector-current extension executes only representative stations; its recorded runtime is a few minutes here. The native modal run is longer and depends on CPU/memory. Fresh output timestamps differ; scientific comparisons use declared numeric tolerances rather than claiming fresh byte-identical solver files.

For the captured release, run `python validation/acr1_structural_dynamics/check_capture.py`. Native tool input syntax and normalization follow the linked CalculiX 2.23 manual; the vendor manual itself is not redistributed.

## Remaining physical and computational boundary

This screen identifies design limits and required controller/ripple/damping/assembly evidence. It does not close full assembled stator/guide/mount dynamics, discrete attachment modes, a dense normal-force map, mesh-converged global dynamic stress, real material allowables or manufactured/qualified hardware. These remaining calculations and external evidence are explicit; they are not relabelled as completed merely because the finite sensitivity table is positive.
