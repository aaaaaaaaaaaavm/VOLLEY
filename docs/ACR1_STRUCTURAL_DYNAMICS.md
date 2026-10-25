# ACR1 structural dynamics follow-on evidence

**SD01 — separate study, 25 October 2026.** The [source and native/numerical package](../validation/acr1_structural_dynamics/README.md) adds genuine CalculiX free-free modes, finite shot/brake sensitivity, sustained-resonance limits and a source-based current-induced normal-reaction screen. The [five-page scientific report](../validation/acr1_structural_dynamics/STRUCTURAL_DYNAMICS_REPORT.pdf) includes methods, figures, actual stresses, convergence and remaining scope.

| Result | Interpretation |
|:--|:--|
| 40 elastic modes, 131.4105–2052.744 Hz | Actual accepted bare chassis mesh; six numerical rigid modes excluded; installed assembly/host modes are not inferred |
| 0.282788 mm paired budget after adverse 50 µs finite refinement | Conditional principal-3 m/s case with declared ripple, damping, uniform mass and original tolerance/thermal boundaries |
| 64.687 N sustained resonant normal-force screen at assumed 0.5% damping | Continuous 5% harmonic is adverse and exceeds the budget; finite swept passage is a different load-duration case |
| Representative ideal-phase current-induced normal reaction ≤7.500 N | Split-array J×B reciprocity with actual source field/current arrays; full stroke/phase/brake/AC map remains unverified |
| ±5° / ±15° phase sensitivities: 29.091 / 76.687 N | Controller phase matters; representative continuous-resonance screen is about ±12.6°, not a demonstrated controller specification |
| Native static nodal stress peak 24.662 MPa; finite monitored bound 59.411 MPa | Numerical stress evidence with 148 integration-point monitors; no selected alloy/yield/fatigue or global dynamic qualification |

The permanent-magnet ~3.01 kN array attraction is retained as **DC preload**. It is not invented as a full-amplitude oscillatory force. The current-induced opposite-array and common-mode components are kept separate.

The original [ACR1 engineering package](../validation/acr1/README.md), accepted static/ED1 files and core source identities remain unchanged. The 7 kg power/control allowance remains unplaced in CAD inertia. SD01 does not broaden the original averaged 1–3 m/s result into physical performance or complete assembly qualification.

[Native modal results](../validation/acr1_structural_dynamics/MODAL_RESULTS.json) · [Finite and sustained limits](../validation/acr1_structural_dynamics/RESPONSE_RESULTS.json) · [Current-normal vectors](../validation/acr1_structural_dynamics/CURRENT_NORMAL_FORCE.json) · [Actual input/output inventory](../validation/acr1_structural_dynamics/MANIFEST.json)
