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

---

## Results

**RUN 2026-08-22. Eight of eight.**

`analysis/tube_centreline.py` and `analysis/run_a69.py`. Results in
`analysis/results/tube_centreline.json`.

| # | Band | Result | |
|---|---|---|---|
| 1 | simple span reproduces 5wL⁴/384EI to 0.5 % | **0.0000 %** | **PASS** |
| 2 | mesh converged between N and 2N | 0.27122 → 0.27122 mm | **PASS** |
| 3 | free–free first mode reproduces A59's 1.67 Hz to 5 % | **1.6729 Hz** | **PASS** |
| 4 | a continuous centreline is returned and exported | 801 nodes, position and slope | **PASS** |
| 5 | 0 g support sag ≤ 0.1 mm | **0.000000 mm** | **PASS** |
| 6 | pressure bore growth reported against the clearance | **3.440 µm, 6.9 %** | **PASS** |
| 7 | combined worst case inside A67's 0.1–2.0 mm bracket | **0.2425 to 0.9052 mm** | **PASS** |
| 8 | contributions reported separately and ranked | ascent dominates | **PASS** |

### The finding: in orbit, structure contributes nothing and temperature contributes everything

| Contribution | Peak deviation | |
|---|---:|---|
| Ascent lateral, 6 g declared | **1.6273 mm** | *not during a shot* |
| **Thermal bow, 5 K across the diameter** | **0.8284 mm** | **the largest in-flight term** |
| Self-weight, 1 g bench | 0.2712 mm | *not during a shot* |
| **Support placement, ±0.05 mm declared** | **0.0768 mm** | the other in-flight term |
| **Self-weight, 0 g** | **0.0000 mm** | **exactly zero** |

**The case that fires is 0 g, and the tube's own weight then contributes nothing at all.** What is
left is **where the supports actually are** and **how much the tube bows under a temperature
gradient across its diameter** — and the second is larger than the first by an order of magnitude
at 2 K.

> **This re-points the problem.** A67 band 9 made bore straightness the dominant input and the
> obvious reading was *manufacturing*. **It is not primarily manufacturing and it is not stiffness:
> it is thermal control and support alignment.** A stiffer tube buys nothing at 0 g.

**Pressure is not bending.** Hoop stress at the charge is **17.96 MPa** — reproducing A59 band 1
independently — and the bore grows **3.440 µm diametrally, 6.9 % of the nominal clearance.**
*It opens the clearance slightly rather than distorting the line.*
