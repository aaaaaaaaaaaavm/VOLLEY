# Corrected ACR1 static numerical cross-check

This selected supplement compares the bare chassis under the same 3010.480631 N opposed patch load and six numerical 3-2-1 scalar constraints. The primary native ANSYS result reproduces 0.286391914110 mm paired closure (+0.142863% versus the 0.285983349735 mm CalculiX benchmark).

The original native result is hash-pinned in ACR1_STATIC_CROSSCHECK.json. Its workstation/user metadata and the private native projects are not distributed. Solver decks and logs here redact private paths; their mesh, material, load, constraint and numerical result content is preserved. Input directory strings use ./ for portability. Run each level in a separate working directory using MAPDL 2026 R1 or a compatible licensed solver. No new solve was run during independent review.

The three meshes provide sensitivity evidence, not a certified convergence/error bound. Closure is lower Uz minus upper Uz at common XY; the reported maximum is over the declared samples. It does not establish individual assembled-gap margins, physical mount behaviour or hardware qualification. AL_ASSUMED is E=70 GPa, nu=0.33, rho=2700 kg/m3. Point-constraint peak stress is excluded from acceptance.

The figure is a scientific Matplotlib rendering of native-result-derived numerical data, independently read back from the ANSYS RST. It is not a Mechanical GUI screenshot. Modal shape identity/MAC, GUI reopenability and experimental Gen6/MC-L3 models are outside this accepted static supplement.

## Numerical inspection and figures

`python3 check_capture.py` checks the complete supplement identities, native-deck versus exported nodal forces, patch resultants/centroids, closure samples and the existing conditional-clearance formula. It needs only Python's standard library. `python3 plot_crosscheck.py --output /tmp/volley-static-figures` produces the native-data field/profile plot using NumPy and Matplotlib. A new licensed native solve is separate from these captured-output checks.
