---
title: "VOLLEY Gen5 — computational evidence review"
subtitle: "Fixed academic configuration and negative design findings"
author: "VOLLEY engineering record"
date: "9 October 2026"
header-includes:
  - \usepackage{graphicx}
---

# Abstract

Gen5 is a fixed computational study of a sequential electromagnetic deployer for twelve 3U CubeSats. At its rated modeled point the machine gives 16.029 m/s exit speed and 10.068 g peak acceleration, with a 126.6 kg dry mass estimate. This report gathers the electromagnetic, power, dynamics, orbit, mass, CAD and mission evidence into a claim-by-claim review. It records both favorable numerical outputs and decisive failures: 10.547 kg of modeled deployer per 3U customer fails two mass comparisons; a side-fed CAD reference arrangement has an 11 mm width shortfall and exact-solid interference; and none of six sampled finite-burn twelve-payload campaigns delivers all twelve. The current rated immediate two-body orbit change has an independent Cartesian check, while the current 1.60 lifetime multiplier has no independent rated-case rerun. Published tests of related devices support assumptions and context; **VOLLEY itself has no built, fired, measured, qualified or flown hardware**.

# 1. Configuration and evidence classes

**New finite-geometry disposition.** The historical 16.029 m/s rating in the table below assumes periodic force over the 1.3 m powered stroke. A [finite-array/stator 3-D analytic integration](../validation/P118_gen5_finite_force_map.md) gives 1.042 kJ ideal work and a 12.448 m/s geometry-only speed under optimal phase with circuit losses omitted. The modeled magnet array has no direct stator overlap after 1.066 m travel. This challenges the rated performance claim and is not an independent FEM or hardware validation. The [unselected R1 FreeCAD feeder candidate](../cad/FEEDER_CANDIDATE_R1.pdf) clears twelve scripted envelope routes in a widened 570 mm enclosure, but no actuator, restraint or revised installed-system budgets exist. A [matched reference mission](../docs/MATCHED_MISSION_REFERENCE.md) includes dispenser mass and host recoil; no sampled twelve-shot option closes. These findings have not been rolled into the original rated shot, mass or lifetime models.

![Finite analytic force map](../figures/gen5_finite_force_map.png)

![Matched reference mission](../figures/matched_mission_reference.png)

![Unselected R1 geometry section](../figures/gen5_feeder_candidate_r1.png)

The [configuration index](../docs/GEN5_CONFIGURATION_INDEX.json) hashes the eight source STEP parts, the FreeCAD exports and native document, geometry parameters, governing model code and result files. Its status is `COMPUTATIONAL_DESIGN_REVIEW_CANDIDATE`; identity of files is not proof that an equation or material assumption is correct. The reference host is a 450 km circular orbit with a tangential prograde impulse for the orbital comparison, not a provider-approved mission. No named flight CubeSat, provider ICD or full installed system exists.

This report distinguishes **model output**, **independent numerical cross-check**, **prior-art support**, and **physical measurement**. The last class is empty for Gen5. A plot exported by a Python model is not a screenshot of a solver or an experimental trace. The CAD views are B-rep visualizations. The [figure evidence index](../docs/FIGURE_INDEX.md) and individual run sheets identify each image's source.

# 2. Rated machine and electrical result

| Quantity | Rated model value | Boundary |
|:--|--:|:--|
| Exit speed, 3U | 16.029 m/s | Historical periodic-model operating point, challenged by finite geometry |
| Peak acceleration | 10.068 g | Payload load not qualified |
| Gross / net electrical draw | 2782.391 / 2735.3 J | Coupled circuit/dynamics model |
| Net electrical-to-payload efficiency | 18.79% | Modeled recovery and losses |
| Closed-loop exit-speed dispersion | 0.0274 m/s, 3σ | Simulated sensor/uncertainty assumptions |
| Modeled dry / loaded mass | 126.6 / 174.6 kg | Assumed and geometry-derived lines mixed |

The shot trace below comes from `analysis/motor_model.py` and the checked-in model result. It is not an oscilloscope capture. The field plot is from the declared analytical field builder; separate 2-D and 3-D checks agree on *selected field quantities*, not on the complete depth-integrated thrust constant. Hot winding resistance, inverter switching, full bank supplier data and protection remain unresolved.

\begin{center}
\includegraphics[width=0.74\linewidth]{../figures/F01_shot.png}\\
\small Figure 1. Modeled rated shot profile; source: motor model, evidence class M.
\end{center}

\begin{center}
\includegraphics[width=0.73\linewidth]{../figures/A02_field_map.png}\\
\small Figure 2. Calculated Gen5 magnetic field; this does not measure integrated thrust.
\end{center}

A separate [rated energy and mass algebra audit](../validation/P117_rated_energy_mass_audit.md) reproduces the 4.000 kg/payload inference, 513.858 J payload kinetic energy, 1.30075 m constant-acceleration equivalent stroke, and rounded brake/recovery identities from the captured JSON. It also finds **124.488 J (4.47%) of gross draw unitemized** after the reported kinetic energies, copper heat and bank ESR are subtracted. That remainder is an unresolved accounting item, not an inferred new component loss; no claim of a fully closed electrical loss budget follows from these checks.

# 3. Orbit, timing and complete-manifest checks

For a 450 km circular host reference, a 16.029 m/s instantaneous tangential impulse gives a **28.800775 km** semi-major-axis rise in the [separate Cartesian DOP853 propagation](../validation/P115_rated_orbit_cartesian.md). The two-body numerical band is 0.02 m and passes. This confirms immediate orbital geometry at the modeled release speed. It does not independently establish the stated **1.60 lifetime multiplier**, which depends on a static atmosphere at mean activity and has no current rated-case independent rerun. It does not establish thrust, finite release duration or host acceptability.

\begin{center}
\includegraphics[width=0.78\linewidth]{../figures/rated_orbit_crosscheck.png}\\
\small Figure 3. Independent two-body geometry response; sweep points are not a Gen5 command envelope.
\end{center}

Timing alone from an unchanged host with zero relative release impulse creates no persistent same-epoch phase offset. The prior 468-second/30-degree claim is withdrawn. The six sampled finite-burn campaigns with a twelve-payload manifest return accepted prefixes of **0, 3, 4, 0, 4 and 5**; no sample delivers all twelve. These are bounded surrogate cases with assumed host thrust and rules, not a proof that no mission can close. Spring impulse, spring plus host manoeuvres, onboard propulsion and orbital transport still require matched provider/payload mission comparison.

# 4. Mass and CAD decision

The modeled dry mass is **126.6 kg**, including an A46 enclosure build-up, assumed components, and a 9.445 kg sled from historical Gen3 solid volumes. For twelve 3U payloads this is **10.547 kg per customer**. It misses the project's approximately 2 kg/customer economic screen and is **1.758 times** an approximate 6 kg/3U spring-canister comparator, outside a separate ±15% parity band. The 64-corner mass ledger's most favorable evaluated requirement-deletion case remains 88.67 kg. These comparisons are screening assumptions, not supplier quotes.

The [FreeCAD 1.0 CAD review](../cad/GEN5_CAD_REVIEW.pdf) releases a native `.FCStd` document, eight FreeCAD-exported STEP parts and a 20-instance assembly STEP. The side-fed reference placement fails: 526 mm internal width versus 537 mm for track and cassettes before clearance. Both CadQuery and FreeCAD find **32,915 mm³** exact-solid track/cassette overlap per side. The clash is left in the native project for inspection. It may be remedied only by a new feeder/enclosure configuration and renewed analysis; the existing design cannot be called mechanically complete.

\begin{center}
\includegraphics[height=0.38\textheight]{../figures/gen5_packaging_section.png}\\
\small Figure 4. Dimension-derived cross-section and exact-solid clash. Reference placement, not a production drawing.
\end{center}

# 5. Evidence closure and review decision

The [C-00–C-20 freeze register](../docs/GEN5_FREEZE_READINESS.md) is the authority for each unresolved question. A dated clean-snapshot gate run passed 148 tests and left tracked files clean; that gate does not rerun all native FEM, SPICE, GMAT or CAD studies, and companion files were unavailable inside that isolated snapshot. The present P115 and P116 checks reduce uncertainty on immediate two-body orbit geometry and expose a mechanical packaging failure. They do not close independent full-depth force, installed bank/inverter design, release contact, brake arrest/reset, moving-load structure, magnetic payload compatibility, thermal cycling, provider integration, disposal or complete mission delivery.

The college rubric calls for achievement of objectives, technical quality, validation, documentation and demonstration. It offers special recognition for a working prototype; it does not make a prototype a stated prerequisite for all 40 final marks. A professional final review should demonstrate the reproducible models and native CAD, show the failed criteria prominently, and explain what a later physical programme must measure. A literature analogy or polished render must not be described as a Gen5 physical validation.

**Release decision:** Gen5 is a documented computational design study with an unresolved internal performance discrepancy and negative 3U mass/fit findings. It is **not** a complete deployer product, a provider-approved flight design, or a final evidence freeze. Gen6's 1 km/s-class objective remains a distinct research direction; it cannot repair a failed Gen5 criterion by changing the label.

# Reproduce and audit

From a clean checkout, install the pinned or declared Python dependencies, run `./tools/verify_all.sh`, then inspect its report and the exact source/result hashes. Rebuild the new orbit figure with `python3 analysis/rated_orbit_independent.py`. Rebuild the Gen5 STEP parts with `python3 cad/build_gen5.py --check`, the reference assembly with `python3 cad/build_review_assembly.py`, and the native handover with `/usr/bin/python3 cad/freecad_export_review.py` on FreeCAD 1.0. See [P115](../validation/P115_rated_orbit_cartesian.md), [P116](../validation/P116_gen5_assembly_packaging.md), the [CAD PDF](../cad/GEN5_CAD_REVIEW.pdf) and the [market/customer audit](../MARKET_AND_CUSTOMER_FIT.md) for source-specific limits.
