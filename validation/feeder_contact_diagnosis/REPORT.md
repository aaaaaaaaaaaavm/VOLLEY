FCE13 targeted contact-convergence diagnosis — 22 October 2026

Decision: the existing 0.05 mm COM and 0.05° orientation criteria remain FAILED. No solver or representation correction is qualified for adoption. The original FCE12 failure is preserved. All results apply to FM06-R1 only; they do not validate FM07-R6, rate rigid-contact forces, select a feeder, or constitute outside expert review.


The six new completed native Chrono 10/Bullet runs reached the same 26.5 s endpoint without domain exit or sequence abort. Zero gravity, restitution 0, assumed friction 0.1, payload mass 4 kg, 1 ms sampled PD control, ideal prismatic guides and actuator caps remain as in FCE12. The exact box-core variant changes collision representation only; all masses, inertias, dimensions, eight rail cells and physical inputs remain fixed.


| Comparison | Final COM Δ [mm] | Final angle Δ [deg] | Net impulse Δ [N s] | Positive work Δ [%] |
|---|---:|---:|---:|---:|
| FCE12 1U PSOR | 1.508584 | 0.639678 | 0.000244921 | 0.000276 |
| FCE12 3U PSOR | 1.466380 | 0.232303 | 0.000775079 | 0.012691 |
| 3U PSOR 2k → 4k | 0.828321 | 0.209219 | 0.000747669 | 0.004609 |
| 3U cold → warm PSOR | 1.736801 | 0.497359 | 0.000357336 | 0.003432 |
| 3U BB 250 → 125 µs | 1.926456 | 0.120098 | 0.000735673 | 0.030001 |
| 3U box core 250 → 125 µs | 0.716162 | 0.564333 | 0.000841226 | 0.012631 |
| 3U mesh → box core at 125 µs | 0.755420 | 0.603748 | 0.000602051 | 0.000060 |


All listed endpoint comparisons fail at least one retained pose criterion; all listed work differences are below the existing 1% work screen. Small work differences do not establish pose or load convergence. Net contact impulse is integrated at every native step, but it includes cancellation; no impulse acceptance limit was invented. It is not an integrated absolute load or force rating.


The instrumented 250 µs PSOR baseline CSV is byte-identical to FCE12-05. It uses all 2,000 iterations in 1,936 of 106,000 steps and reaches a maximum native reported error 0.654381 versus its 1e-7 stopping tolerance. Of 46 sampled full-budget solves, 45 occur during 5–10 s feed deceleration. At 10 s the original 3U timestep pair already differs 1.549519 mm/0.853163°. Ideal guide constraints remain present; original baseline fork off-axis drift is subnanometre. The measured sensitivity begins before receiver capture.


Warm starting still uses the full budget during 2,444 steps and changes final pose 1.736801 mm/0.497359°. Native BB uses its full 2,000 iteration budget during 7,028/106,000 and 4,424/212,000 steps. Its 250 → 125 µs result still fails 1.926456 mm/0.120098°. PSOR GetError measures its reported normal/joint violation and omits tangent components from that stopping statistic. BB exposes an absolute projected-gradient norm while stopping on its norm relative to the initial gradient. These errors have different meanings; full-budget counts do not prove every final iteration missed tolerance. Neither solver establishes every solve as converged here.


Representation is a demonstrated sensitivity: core 00 is exactly an 8-vertex, 12-triangle box. CORE_BOX_EQUIVALENCE.json verifies all corners, face planes and volume. At 250 µs, replacing it with a native box gives a byte-identical full CSV. At 125 µs, that equivalent representation changes final pose 0.755420 mm/0.603748°. Its own timestep pair fails 0.716162 mm/0.564333°. This demonstrates sensitivity to contact manifold representation with unchanged input geometry. It does not establish an upper error bound or isolate a unique root cause. The original planar gap controls detect all imposed 10/100/500/1,000 µm overlaps with worst error 4.273 nm and correctly reject 10/100 µm separated controls. Those controls do not certify moving or rotated contact manifolds.


Friction remains an uncalibrated physical assumption. Existing 500 µs 3U sensitivities at µ=0 and µ=0.3 change final pose 0.839301 mm/0.736022° and 0.877083 mm/0.213657° from µ=0.1. They are sensitivities, not nominal corrections. Under the unchanged undamped zero-g model, FCE12 final speeds at 250/125 µs are 0.187322/0.007801 mm/s (1U) and 0.091251/0.114192 mm/s (3U). Continuing residual motion makes endpoint phase relevant; no damping or settling time was added to force a pass. Stage velocities and vector impulse differences are in COMPARISONS.json.


The unpreconditioned APGD pair was terminated as a bounded pilot after an observed 91 s: last complete CSV times were 0.85 s and 0.34 s, far short of 26.5 s. Its partial outputs, commands and source identities are retained and excluded from convergence results.


| Completed native run | Change from FCE12 | Wall time [s] | Full-budget steps |
|---|---|---:|---:|
| P3-250 | instrumentation only | 88.142 | 1936 |
| W3-250 | warm start | 93.571 | 2444 |
| B3-250 | native BB, 250 µs | 167.507 | 7028 |
| B3-125 | native BB, 125 µs | 181.734 | 4424 |
| X3-250 | exact box core, 250 µs | 122.902 | 1936 |
| X3-125 | exact box core, 125 µs | 141.458 | 742 |


The observed pose discrepancies measure sensitivity to the tested alternatives; they are not certified bounds on the exact solution. No true-solution error bound is established. The blocking criterion remains a common-endpoint refinement pair satisfying both 0.05 mm and 0.05° after contact representation and solver errors are controlled. Rigid NSC peaks remain unrated. Geometry/contact applicability, physical correlation, full release/reset and installed actuation remain outside this contact subcycle.


Files: SUMMARY.json gives the decision and numbers; COMPARISONS.json gives stage pose/velocity and impulse/work differences; SOLVER_PHASES.json gives sampled solve diagnostics; runs/*.record.json contains exact native commands, settings, wall times and output hashes; runs/*.solver.csv and*.solver.json preserve diagnostics; BASELINE_HASHES.json preserves original source/results/geometry hashes; references/SOURCES.json identifies the inspected native solver/collision sources. baseline/PROTOCOL.json preserves the unchanged criteria. See REPRODUCE.md for exact commands.

