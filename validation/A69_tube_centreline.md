# A69 — what shape the 8 m drive tube is actually in

**Closes, if it passes:** the input [A67](A67_guided_contact.md) band 9 made dominant.
**Bore straightness is the largest sensitivity in the guided-contact model and it is currently a
declared bracket with no source.**

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/tube_centreline.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/tube_centreline.py`, which must return
> nothing.

## Why this run exists

[A59](A59_tube_structure.md) took the tube structurally and answered stress, buckling and mode
frequency. **It computed no shape.** A67 then needed a centreline, had none, and declared a
sinusoid of assumed amplitude — *"0.1–2.0 mm over 8 m"* — which is a sensitivity input and **not a
design input**.

**A67 band 9 then made it the dominant term**, at a Sobol total-order index of **0.894** against
seal friction's 0.141. *A bracket cannot carry that.*

## What is being computed

**The deflected centreline of the tube, as a continuous curve, from the loads that actually bend
it**, on the geometry `cad/parameters.json` already holds: **8.0 m, 15.805 mm bore, 1.0 mm wall,
aluminium 6061-T6**, on **seven supports at 1.0 m** ([A59](A59_tube_structure.md)).

| Contribution | Modelled as |
|---|---|
| **Support-induced sag** | Euler–Bernoulli beam on seven supports, self-weight, both in a 1 g build orientation and at 0 g |
| **Manufacturing straightness** | a declared tolerance envelope added to the deflected shape, **not confused with it** |
| **Support placement and angular alignment** | each support offset by a declared tolerance |
| **Internal pressure** | the bore's radial growth at the charge pressure, and whether it is uniform along the length |
| **Thermal distortion** | a longitudinal gradient across A58's swing, with the tube free to grow at one end |
| **Ascent quasi-static load** | lateral acceleration on the supported beam, as a separate case |

## Acceptance bands

**Eight bands. Bands 3, 5 and 7 can fail.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Beam solver verification.** A uniformly loaded simply supported span reproduces `5wL⁴/384EI` to **0.5 %** | The solver is wrong before any VOLLEY geometry enters it |
| **2** | **Mesh convergence.** Peak deflection changes by < 0.5 % between N and 2N elements | The shape is reading the discretisation |
| **3** | **A59 regression.** The first free–free mode reproduces A59's **1.67 Hz** unsupported figure to **5 %** | This model and A59 disagree about the same tube |
| **4** | **Every case returns a continuous centreline** with position and slope at any x, exported for the contact model | The output is a scalar again, which is the defect this run exists to remove |
| **5** | **The 0 g support sag is ≤ 0.1 mm**, the lower end of A67's declared bracket | The tube's own weight in orbit is not negligible against the clearance, and the straightness budget is structural before it is manufacturing |
| **6** | **Pressure-induced bore growth is reported** and compared against the 50 µm nominal diametral clearance | Report-only, but a growth of clearance order changes the contact problem |
| **7** | **The combined worst-case centreline deviation is inside A67's swept bracket, 0.1–2.0 mm** | **A67's sensitivity sweep did not cover the real range**, and its Monte Carlo is extrapolating |
| **8** | **The contributions are reported separately and ranked** | Report-only. A single combined number would repeat A59's mistake |

## What this run does not do

**It does not measure a tube** — **E4** — and manufacturing straightness enters as a *declared
tolerance*, not a computed one; what a real 8 m bore can hold is
[`MANUFACTURING.md`](../docs/MANUFACTURING.md)'s to establish. It does not model the supports'
own stiffness beyond a declared value, and it does not couple to the carriage: **that is
[A70](A70_guided_contact_derived.md).**
