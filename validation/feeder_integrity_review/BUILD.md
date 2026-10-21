# Reproduction and captured-input boundaries

## Lightweight integrity check

Run `python check_capture.py` from this directory. It verifies SHA-256 identities and selected independent mechanical relations. It does not silently regenerate native binary documents or declare engineering acceptance from matching hashes.

## Native CAD and exchange files

The captured geometry was generated with FreeCAD 1.0.0/OpenCascade 7.8.1. With FreeCAD's Python libraries available, run `build_native.py`, `check_sweeps.py`, `physical_interlocks.py`, `check_receiver_gap.py`, `metrology.py`, `export_parts.py` and `export_surfaces.py`. Native document regeneration may change metadata; supplied identities refer to the reviewed capture.

Run `check_step.py` in a separate CadQuery 2.8/OpenCascade 7.9 environment. `capture_native.py cad/FM06_3U_transfer.FCStd figures/FreeCAD_FM06_transfer.png` requires a genuine Qt/Coin display. The capture program does not fabricate application chrome. Blender Workbench images are CAD renders, separately identified by `figures/BLENDER_PROVENANCE.json`.

The 1U and 3U models are dedicated research assemblies. They are not one demonstrated universal receiver. Parts retain assembly coordinates and simplified hardware envelopes. Native solids, valid exchange files and zero nominal penetration do not establish manufacturability or clearance under load.

## Component linear-static studies

FLR01 uses Gmsh 4.14.1 and CalculiX 2.23. The portable generation programs are under `receiver/fea/`; set `CCX` to the CalculiX executable if it is not on PATH. Geometry uses millimetres, force newtons and stress MPa. Both receiver bores are fully clamped and homogeneous steel stiffness is assumed. This boundary is an idealized component fixture; it is not a bound on assembled stiffness. Earlier captured metadata using the word “overstiff” must be read with this correction.

The package includes forty historical FLR01 receiver summaries plus twelve actual-FM06 FLR03 summaries, original raw-file hashes, and six complete finest-3U input/DAT/log captures. It does not include all fifty-two raw output files. `COMPONENT_GEOMETRY_LINEAGE.json` checks the actual FM06 receiver and tine material against current STEP geometry; the earlier FM03 crossbar is a different revision. Compressed `*.inp.gz` and `*.dat.gz` contain the exact solver text, without edits. Decompress an input and run `ccx -i split` or `ccx -i one_dog` in its case directory.

FLR02 is under `tine/`. All four unit-load input/DAT captures are supplied. Their native source runners and generated STEP retain captured identities. Use a Python environment with NumPy and Gmsh; the portable runner resolves CalculiX through `CCX`/PATH. Source-portability changes are listed in `PORTABILITY.json`. Mesh convergence of an isolated component does not validate its real support or material strength.

`guide_play.py` needs NumPy and SciPy. `fit_sensitivity.py` uses the Python standard library. `schedule.py` consumes the supplied unchanged finite-burn schedule inputs. Its auxiliary motions assume constant speed; the native contact subcycle uses different rest-to-rest trajectories and does not replace the full handling schedule.

## Native rigid contact

Project Chrono 10.0.0 was built from the official tagged source with Eigen 3.4.0, GCC 14.2 and CMake 3.30.5. Source download identities are in `contact/SOURCE_DOWNLOADS.json`. The lightweight captured-result check does not require Chrono. A native rerun requires its core library and development configuration:

```sh
cmake -S contact -B contact/build -DChrono_DIR=/path/to/chrono/build/cmake
cmake --build contact/build
```

`contact/campaign/INPUTS.json` specifies each case and the exact executed source/executable identities. `contact/captured/feeder_surface.cpp` is the executed source. The readable build source has formatting-only changes checked by lexical token comparison. The original run records retain execution-machine paths as provenance, not as portable installation instructions. The native runtime syntax is:

```text
feeder_surface geometry_dir output.csv mass_kg friction restitution gravity_m_s2 dt_s feed_cap_N guide_drag_N yaw_deg iterations feed_time_s mode guard_mm
```

For example, `geometry_dir` is `contact_geometry_surfaces/3U`, and `mode` is `none`, `jam` or `stuck_pin`. The executable uses the Bullet collision backend and Chrono NSC/PSOR solver. Connected triangle meshes are represented by Chrono's triangle contact proxies; this is not a GImpact/BVH validation claim. The 10 µm numerical skin and 5 µm tessellation target do not represent physical coating thickness or allowable interference.

The guide constraints and full-state feedback are ideal model assumptions. Motor force limits, resistance, friction, restitution and capture bands are declared study inputs. The record does not select a sensor, controller, mechanism actuator, space lubricant or installed brake. Hard-contact peak forces are not accepted structural design loads without a converged and physically correlated contact model.

## Source references

- [CubeSat Design Specification, revision 14.1](https://www.cubesat.org/cubesatinfo): reference rail geometry and deployer interface context; not provider approval.
- [Project Chrono 10.0.0 source](https://github.com/projectchrono/chrono/tree/10.0.0) and [documentation](https://api.projectchrono.org/): rigid dynamics, constrained mechanisms and contact.
- [Gmsh reference manual](https://gmsh.info/doc/texinfo/gmsh.html): tetrahedral meshing and finite-element export.
- [CalculiX documentation](https://www.dhondt.de/): native structural analysis and input/output conventions.
- [FreeCAD](https://www.freecad.org/) and [CadQuery](https://cadquery.readthedocs.io/): parametric geometry and independent exchange readback.

External software and reference dimensions support the methods. They do not constitute testing or endorsement of this mechanism.
