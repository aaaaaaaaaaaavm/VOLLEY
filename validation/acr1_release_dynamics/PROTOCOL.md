# Bounded release/arrest dynamics protocol

The controlling configuration is VOLLEY-G5-ACR1. This work supplements its accepted ED1/core records without altering them. It does not reuse FM06-R1 contact geometry or transfer the failed Chrono contact-convergence results to this configuration.

## Model and source boundaries

- Native MuJoCo 3.3.7 evolves a six-degree-of-freedom 4 kg payload with exact uniform-box surrogate inertia for 340.5 × 100 × 100 mm. These are the same surrogate dimensions/inertias as the accepted energy calculation, not measured spacecraft properties.
- The carrier and finite host translate along X; their masses are read from the unchanged source case. Their rotations and Y/Z motion are ideal constraints. This is not a full host attitude recovery model.
- The unchanged averaged electrical/force source is instrumented only to record every 5 µs force step. Two 3 m/s, 20 µH source histories cover nominal and adverse source conditions. The source hash and exact instrumentation substitution are retained. Perturbed contact forces do not feed back into the electrical/controller model.
- The study starts 1 ms before the source rear-unload event. The cam has already completed its nominal 12 mm opening 5 mm before release. Fully open keeper tabs are represented; a declared half-opening fault changes one tab's position to 6 mm. No new mechanism is selected.
- The native calculation runs for a common 0.35 s window through arrest and subsequent free coast. The source ends at its first low-speed turnaround. Powered empty return, initial launch, feeder capture, host collision corridor and elastic spacecraft modes are outside the calculation.

## Collision representation

Rectangular collision members are derived from exact box arguments in the controlling CAD builders: designated rear pads and supports, carrier seats, complete pallet rectangular members and upper grip faces, closed caps and fixed guide faces, side pillars, forekeeper tabs and front supports. Dimensions and source functions are exported in GEOMETRY_AND_INPUTS.json. Remote shaft/lock bores and round drives are omitted or conservatively filled only where they do not change the nearest nominal contact surface. The pallet end blocks are retained because their upper face is only 0.5 mm below the nominal payload and could affect departure recontact.

This is a documented collision-surface subset, not a tessellation of the whole CAD assembly or a universal collision-clearance proof. A partition test divides identical contact boxes into two boxes with exactly the same union to expose contact-manifold representation sensitivity. Single-rear-pad cases are deliberate contact-active-set sensitivities, not an alternate CAD design or a manufactured tolerance statement.

No hidden gravity, global damping or settling phase is added. MuJoCo direct contact parameters use acceleration stiffness/damping, not material stiffness in N/m. Constant impedance is 0.95. Friction 0/0.1/0.3, direct stiffness 1e5/1e6/1e7 s⁻², and zero/underdamped/critical reference damping are explicit unmeasured sensitivities. None is presented as calibrated restitution, vacuum tribology or the accepted rail axial stiffness.

## Numerical checks declared before campaign interpretation

1. Common-endpoint refinements: 100, 50 and 25 µs for all nine cases; 12.5 µs for aligned, yaw and half-keeper witnesses.
2. Newton 100/200 iterations, a CG algorithm check, and exact-union box partition checks on aligned and half-keeper cases.
3. No-contact translation/rotation control with analytic straight-line position and conserved momentum/angular momentum.
4. For every run, report total X momentum, payload contact-force linear and angular impulse balance, native generalized/contact-force agreement, solver iteration use and warnings. Contact work/dissipation must be distinguished from numerical energy error.
5. Source timings, final velocity/attitude, transverse motion, rear load/unload episodes, post-source-release absolute contact impulse, maximum numerical overlap and final geometric egress are retained. Native penalty-contact peaks are unrated.

The earlier FCE numerical pose differences of 0.05 mm and 0.05° are displayed as inherited reference screens, not new payload accuracy or qualification limits. Refinement and solver agreement measure numerical consistency of this model. Physical repeatability and actual contact parameters require correlation with an instrumented article.

## Primary solver references

[MuJoCo 3.3.7 modeling: solver/contact parameters](https://mujoco.readthedocs.io/en/3.3.7/modeling.html#solver-parameters) and [constraint model](https://mujoco.readthedocs.io/en/3.3.7/computation/index.html#constraint-model) identify the direct-parameter convention and regularized soft-contact scope. The source code and version of the engine are separate from the VOLLEY electromagnetic model.
