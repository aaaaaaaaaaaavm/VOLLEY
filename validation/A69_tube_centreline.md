# A69, what shape the 8 m drive tube is actually in

**Closes, if it passes:** the input [A67](A67_guided_contact.md) band 9 made dominant.
Bore straightness is the largest sensitivity in the guided-contact model and it is currently a
declared bracket with no source.

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/tube_centreline.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/tube_centreline.py`, which must return
> nothing.

## Why this run exists

[A59](A59_tube_structure.md) took the tube structurally and answered stress, buckling and mode
frequency. It computed no shape. A67 then needed a centreline, had none, and declared a
sinusoid of assumed amplitude, *"0.1-2.0 mm over 8 m"*, which is a sensitivity input and not a
design input.

**A67 band 9 then made it the dominant term**, at a Sobol total-order index of **0.894** against
seal friction's 0.141. *A bracket cannot carry that.*

## What is being computed

The deflected centreline of the tube, as a continuous curve, from the loads that actually bend
it, on the geometry `cad/parameters.json` already holds: 8.0 m, 15.805 mm bore, 1.0 mm wall,
aluminium 6061-T6, on seven supports at 1.0 m ([A59](A59_tube_structure.md)).

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

It does not measure a tube, E4, and manufacturing straightness enters as a *declared
tolerance*, not a computed one; what a real 8 m bore can hold is
[`MANUFACTURING.md`](../docs/MANUFACTURING.md)'s to establish. It does not model the supports'
own stiffness beyond a declared value, and it does not couple to the carriage: that is
[A70](A70_guided_contact_derived.md).

---

## Results

RUN 2026-08-22. Eight of eight.

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

The case that fires is 0 g, and the tube's own weight then contributes nothing at all. What is
left is where the supports actually are and how much the tube bows under a temperature
gradient across its diameter, and the second is larger than the first by an order of magnitude
at 2 K.

> **This re-points the problem.** A67 band 9 made bore straightness the dominant input and the
> obvious reading was *manufacturing*. It is not primarily manufacturing and it is not stiffness:
> it is thermal control and support alignment. A stiffer tube buys nothing at 0 g.

**Pressure is not bending.** Hoop stress at the charge is **17.96 MPa** — reproducing A59 band 1
independently, and the bore grows 3.440 µm diametrally, 6.9 % of the nominal clearance.
*It opens the clearance slightly rather than distorting the line.*

---

> ## CORRECTION 2026-08-22, later the same day, P110. The thermal construction was nonphysical.
>
> The results above are superseded. They are kept because the correction has to have something
> to correct.
>
> What was wrong. `orbital_centreline()` built the thermal bow as an independent parabola in
> each support span, reset to zero at every support. A uniform across-diameter gradient imposes a
> uniform curvature on the whole continuous member; imposing it span-by-span put a slope
> discontinuity of κ x span at each of the seven supports. That kinks a continuous aluminium
> tube seven times, and the supports are transverse constraints, not cuts.
>
> What it is now. The gradient enters as an eigenstrain on the continuous beam, element
> load `f_th = ∫Bᵀ EI κ dx = EI κ [0, −1, 0, +1]`, equal and opposite end moments, solved
> together with the support offsets in one compatible solve. Displacement and rotation come out
> continuous and the curvature is finite everywhere.
>
> ### The limiting case the correction is checked against
>
> A simply supported span under uniform imposed curvature has `w_mid = κL²/8` exactly. The
> solver returns 1.250000e−04 m against 1.250000e−04 m, 0.0000 %. *That test did not exist
> before and is now band 1's second half.*
>
> ### What the error was worth
>
> Three-point sagitta over the piston's own length, at a 1 K gradient:
>
> | | 40 mm | 120 mm | 200 mm | 400 mm |
> |---|---:|---:|---:|---:|
> | As first computed, kinked | 12.8 | 37.3 | 60.4 | 109.5 µm |
> | Corrected, continuous | 0.27 | 2.39 | 6.63 | 26.5 µm |
> | Smooth-arc reference, κL²/8 |, | 2.386 |, |, |
>
> The corrected 120 mm figure agrees with the independent closed form to 0.2 %. The original was
> 15.6x too large, and every micrometre of the excess was the artificial kink.
>
> ### Corrected bands, re-run 2026-08-22
>
> **Seven of eight. Band 7 now FAILS and band 4 is now a real test.**
>
> | # | Band | Result | |
> |---|---|---|---|
> | 1 | simple span **and** imposed curvature, both to 0.5 % | 0.0000 % and **0.0000 %** | **PASS** |
> | 2 | mesh converged | 0.27122 → 0.27122 mm | **PASS** |
> | 3 | free–free mode against A59's 1.67 Hz | 1.6729 Hz | **PASS** |
> | 4 | **continuity, actually tested** — slope jump < 1 % of peak slope, curvature within 5× the imposed | **0.7454 %**, ratio **1.00** | **PASS** |
> | 5 | 0 g support sag ≤ 0.1 mm | 0.000000 mm | **PASS** |
> | 6 | pressure bore growth reported | 3.440 µm, 6.9 % | **PASS** |
> | 7 | **solved combined centrelines peak inside 2.0 mm** | **0.0768 to 5.3023 mm** | **FAIL** |
> | 8 | contributions ranked | thermal bow dominates | **PASS** |
>
> **Band 4 was `b4 = True` and is now four computed conditions** — P110. **Band 7 was the sum of
> two scalar peaks and is now the peak of solved centrelines, and on that basis it fails: at 5 K
> the member bows to 5.30 mm, outside the 0.1-2.0 mm bracket [A67](A67_guided_contact.md) swept.
> *A67's Monte Carlo was extrapolating at the hot end.*
>
> ### And one conclusion is withdrawn
>
> "Not primarily manufacturing; thermal control and support alignment dominate" is withdrawn.
> Manufacturing straightness was never in the ranking, so the ranking could not place it.
> `orbital_centreline()` now accepts a declared `straightness_mm` and superposes it, but what an
> 8 m bore can actually hold is not established here and is [`MANUFACTURING.md`](../docs/MANUFACTURING.md)'s.
> *The honest statement is that the ranking excludes manufacturing straightness and therefore
> cannot decide between it and thermal bow.*

---

> ## CORRECTION 2026-08-26, P115. The supports were held by a penalty, and the solve could not carry it.
>
> `beam()` imposed each rigid support as a diagonal penalty of 1e8 times the element stiffness,
> and a prescribed support offset entered as `pen x offset` on the right-hand side. The constraint
> came out satisfied to 1e-17 m and the assembled 1602-DOF system came out at a condition number
> of 8.6e15, against a double-precision epsilon of 2.2e-16. The supports are now imposed by
> eliminating the constrained rows, which leaves cond 4.1e9.
>
> **Only the cases with a prescribed offset moved.** Those are the only ones that put the penalty
> into the right-hand side as well as the diagonal. Self-weight at 1 g, at 0 g and under ascent
> lateral load reproduce to 1e-11 either way, which is why nothing had looked wrong on the machine
> the results were committed from.
>
> ### What moves
>
> | | Was | Is |
> |---|---:|---:|
> | Band 7 range, low end | 0.0768 mm | **0.0769 mm** |
> | Support placement, +/-0.05 mm declared | 0.0768 mm | **0.0769 mm** |
> | Thermal bow at 5 K | 5.3023 mm | 5.3023 mm |
> | Every band verdict | | unchanged |
>
> Seven of eight still, with band 7 still failing at 5.3023 mm against A67's 2.0 mm bracket. The
> 8.5e-4 difference in the support-placement peak is the penalty solve's error, not this one's.
>
> Found because the gates workflow ran on a second machine for the first time and the freshness
> comparison disagreed. [P115](../OPEN_PROBLEMS.md#p115) carries the full account, including the
> first diagnosis of that disagreement, which was wrong and is withdrawn there.
