# A67 — the payload's guided contact state through the 8 m bore

**Closes, if it passes:** the first-order half of [P103](../OPEN_PROBLEMS.md). Gen6 has an axial
model and no lateral or angular one, so it has **no exit attitude at all** — only an exit speed.

> ## BANDS DECLARED 2026-08-22, BEFORE `analysis/guided_contact.py` EXISTS.
>
> Everything below is committed before the script is written, and the script is absent at this
> commit. Verify with `git show --stat <this commit> -- analysis/guided_contact.py`, which must
> return nothing.

---

## Why this run exists, and why it is not waiting for B-2

[P103](../OPEN_PROBLEMS.md) as first written put [P67](../OPEN_PROBLEMS.md)'s measurement first.
**That was wrong about the order.** A contact model's parameters are *identified*, not measured
first and inserted — [`docs/EXTERNAL_EVIDENCE.md`](../docs/EXTERNAL_EVIDENCE.md) records three
separation-dynamics papers that do exactly that, one of them by unscented Kalman filter against a
finite-element collision solve. **So the model is built now on a declared friction bracket, and
B-2 replaces the bracket with a distribution when it lands.**

**What the record has:** [A34](A34_cradle_restitution.md) and [A38](A38_tipoff_at_gen6.md) model
the payload crossing its **cradle clearance** in the first tens of milliseconds.
**What it does not have:** anything at all for the remaining eight metres.

## The geometry this run is about, and the dimension that does not exist

`gen6_drive` gives **bore 15.805 mm over 8000 mm** — an **L/D of 506**. The piston is small and the
tube is very long, so the assembly's angular constraint comes from **two bearing lands a short
distance apart inside a bore whose centreline is not straight**.

> **The piston has no length anywhere in this repository.** A41 allows **1.5 kg** for piston, seals,
> valves and plumbing and designs none of it. **So land separation is not an assumption this run
> may make quietly — it is a design variable this run must sweep**, and band 8 exists to prove the
> answer depends on it.

## Declared inputs, and their brackets

**All declared here, before the script.** Anything not in this table is read live from
`cad/parameters.json` or from an existing results file.

| Input | Nominal | Bracket swept | Where it comes from |
|---|---:|---|---|
| Bore diameter | **15.805 mm** | — | `gen6_drive.bore_mm` |
| Stroke | **8000 mm** | — | `gen6_drive.stroke_mm` |
| Payload + carriage mass | **4.0 kg** | — | the 3U reference payload |
| Charge pressure | **22.7258 bar** | — | `gen6_store.charge_pressure_bar` |
| Chamber volume | **2.0 L** | — | `gen6_store.chamber_volume_l` |
| **Diametral clearance** | **50 µm** | **20 – 200 µm** | *declared here.* A sliding fit in a hard-anodised bore; no repository source, so it is a swept design variable and not a claim |
| **Land separation** | **120 mm** | **40 – 400 mm** | *declared here*, for the reason above |
| **Bore straightness** | **0.5 mm** peak over 8 m | **0.1 – 2.0 mm** | *declared here.* A59 requires seven supports at 1.0 m; the deviation between them is not modelled anywhere |
| **Force-line eccentricity** | **0.1 mm** | **0 – 0.5 mm** | *declared here* |
| **Payload CG offset** | **1.0 mm** | **0 – 5 mm** | *declared here* |
| **Seal friction** | **17.8 N** | **17.8 – 83.4 N** | A61's specification to A41's allowance — **the two ends this project already publishes**, and P67 is what closes the bracket |
| Restitution, aluminium on anodised aluminium | **0.7** | 0.3 – 0.7 | `cradle_restitution.E_ALUMINIUM`, the published range |
| Contact stiffness exponent | **1.5** | — | Hertzian, the Lankarani–Nikravesh form |

**Every bracket above is a declared engineering assumption, not a measurement.** Nothing in this
run is measured, and the six starred rows have no source in this repository — which is itself part
of the result.

## Acceptance bands

**Nine bands. Bands 5, 6, 7 and 8 can fail, and failing is a result about the machine.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Axial regression.** Perfectly straight bore, zero eccentricity, friction at A41's allowance: exit velocity reproduces `exit_velocity_m_s_at_friction_allowance` = **29.01 m/s** to **1 %** | The 6-DOF model does not contain the 1-DOF one, and nothing downstream can be trusted |
| **2** | **Symmetry.** With every eccentricity, straightness and offset set to zero, all four lateral/angular exit states are below **1e-9** of their own scales | A sign error or an asymmetry in the contact implementation |
| **3** | **Contact-law verification.** A free radial impact at 0.05–2.0 m/s returns the declared restitution to **5 %** | The Lankarani–Nikravesh implementation is wrong, independently of VOLLEY |
| **4** | **Energy closes.** Gas work = payload kinetic energy + friction dissipation + contact dissipation, to **0.5 %** | Energy is being created or lost, which invalidates every exit state |
| **5** | **Nominal tip-off.** At the nominal row of the table above, exit angular rate ≤ **2.0 °/s** | The design point does not meet the tip-off band [A38](A38_tipoff_at_gen6.md) band 2 was declared against and [A23](A23_tipoff_release.md) quotes as the tighter flown figure |
| **6** | **Guide loads stay below the drive.** Peak contact normal force ≤ **445.88 N**, the commanded axial force | The guide is carrying more than the machine is pushing with, and the bore is a structural problem before it is a kinematic one |
| **7** | **Monte Carlo.** Over the declared brackets, **3σ exit angular rate ≤ 2.0 °/s** | Tip-off is not met under tolerance, and the machine needs geometry it does not have |
| **8** | **The answer depends on land separation.** Sweeping 40–400 mm moves 3σ exit angular rate by **more than 5 %** | The model is not sensitive to the geometry that provides the angular constraint, so it is measuring something other than guided contact — **the anti-self-deception band** |
| **9** | **Sensitivity is reported and the dominant input named** | Report-only. A sweep that cannot say which input controls the answer has not earned the run |

### What this run does not do

**It does not calibrate against hardware** — nothing is measured, **E4**. It does not consume a
deformed bore centreline from a structural solve: the straightness bracket is declared, not
derived, and **coupling it to the tube's own deflection is separate work that P103 names**. It does
not model the cradle release, which is [A34](A34_cradle_restitution.md)'s and stands. It does not
model the seal as anything but a friction force and a radial preload. It does not model stick-slip;
B-2 band 11 is what would justify adding it.

---

## Results

**RUN 2026-08-22. Six of nine. Bands 3, 5 and 7 fail, and band 5 is the result.**

`analysis/guided_contact.py` and `analysis/run_a67.py`, bands committed at `246b7ee` before either
existed. Results in `analysis/results/guided_contact.json`.

| # | Band | Result | |
|---|---|---|---|
| 1 | axial regression against the 1-DOF model, 1 % | **29.0088 against 29.0100 m/s** | **PASS** |
| 2 | symmetry: zero forcing gives zero lateral and angular state | 0.00e+00 | **PASS** |
| 3 | contact law returns the declared restitution, 5 % | **worst 128.1 %** | **FAIL** |
| 4 | energy closes to 0.5 % | **+0.2964 %** | **PASS** |
| 5 | **nominal exit angular rate ≤ 2.0 °/s** | **14.845 °/s** | **FAIL** |
| 6 | peak contact normal force ≤ 445.88 N | **225.8 N** | **PASS** |
| 7 | **Monte Carlo 3σ exit angular rate ≤ 2.0 °/s** | **52.33 °/s**, p99.7 **57.08** | **FAIL** |
| 8 | land separation moves the answer by more than 5 % | **97.3 %** over 40–400 mm | **PASS** |
| 9 | sensitivity reported and the dominant input named | **bore straightness** | **PASS** |

### Band 5 is the finding: Gen6 does not meet tip-off, and it is not close

**14.845 °/s at the nominal point, against the 2.0 °/s band** [A38](A38_tipoff_at_gen6.md) band 2
was declared against and [A23](A23_tipoff_release.md) quotes as the tighter flown deployer figure.
**That is 7.4× over.** Under the declared tolerance brackets the 3σ figure is **52.3 °/s — 26×
over**, and the whole Monte Carlo distribution sits above the band: **the median sample is
19.4 °/s** and **the best sample in 271 is not inside 2.0 °/s.**

> **A38 answered the cradle and this answers the bore, and they do not agree about the machine.**
> A38's residual rate at force removal is **exactly zero** for every clearance — and it is right,
> because the rattle settles against a stop while the force still holds the payload. **Then the
> payload spends 0.42 s traversing eight metres of a bore that is not straight**, and picks up an
> angular rate the cradle model cannot see. *Kill criterion 4 has been answered against the wrong
> 27 milliseconds.*

### Band 9: bore straightness dominates, and it is not a tolerance detail

**Sobol total-order indices**, 288 samples, `calc_second_order=False`:

| Input | S_T | S_1 |
|---|---:|---:|
| **bore straightness** | **0.894 ± 0.454** | 0.588 |
| land separation | 0.257 ± 0.150 | 0.394 |
| payload CG offset | 0.175 ± 0.162 | −0.022 |
| seal friction | 0.141 ± 0.210 | −0.069 |
| force-line eccentricity | 0.108 ± 0.072 | −0.066 |
| clearance | 0.099 ± 0.071 | −0.056 |
| restitution | 0.086 ± 0.074 | 0.082 |

**The confidence intervals are wide and several first-order indices are negative**, which is what
288 samples buys and is reported rather than hidden — *a negative S₁ is an estimator artefact and
says the sample is too small for the first-order split.* **The total-order ranking is robust
enough to act on: straightness is first and land separation is second, and every quantity the seal
contributes is below both.**

> **This reverses the intuition the programme has been running on.** [P67](../OPEN_PROBLEMS.md)
> owns 93.4 % of the *velocity* dispersion and is the highest-leverage measurement in the record —
> and it is **fourth** here. **The thing that decides whether the payload leaves straight is the
> straightness of eight metres of tube**, which is a manufacturing problem
> ([`MANUFACTURING.md`](../docs/MANUFACTURING.md) does not yet contain it) and not a seal problem.

### Band 8 passes, and the sweep is the design output the record did not have

**The piston has no length in this repository.** A41 allows 1.5 kg for piston, seals, valves and
plumbing and designs none of it, so land separation was swept rather than assumed:

| Land separation | Exit angular rate | Peak contact |
|---:|---:|---:|
| 40 mm | 13.942 °/s | 452.7 N |
| 80 mm | **11.285 °/s** | 316.7 N |
| 120 mm — nominal | 14.845 °/s | 225.8 N |
| 200 mm | **10.219 °/s** | 29.5 N |
| 300 mm | 7.525 °/s | *52.9 kN — numerically suspect* |
| 400 mm | 8.496 °/s | *197 kN — numerically suspect* |

**Longer lands are better and none of them is good enough.** Over the four points that are
numerically clean the spread is **45 %**, so band 8 passes on those alone and does not depend on
the two suspect ones. *No land separation in the swept range brings 14.8 °/s to 2.0.*

### Band 3 fails, and it conditions bands 5 and 7 without overturning them

**The contact law returns too little dissipation, and the error grows as restitution falls:**

| Declared e | Returned | Error |
|---:|---:|---:|
| 0.7 — the nominal aluminium figure | 0.796 | **+13.7 %** |
| 0.5 | 0.725 | +45.0 % |
| 0.3 | 0.684 | **+128.1 %** |

**The result is velocity-independent across 0.05–2.0 m/s**, which is what the Lankarani–Nikravesh
form is designed to be, so this is not a rate-dependent implementation error. **It is the known
domain limit of the law itself**: LN's damping–restitution relation is derived assuming most of
the impact energy is stored elastically, which holds as e → 1 and degrades as e falls.
**The band was declared at 5 % across 0.3–0.7 and it fails. It is not being moved**, and the run
is recorded as failing it.

**What it does and does not do to the headline.** Under-dissipation means residual motion is
**overstated**, so 14.845 °/s is **conservative** rather than optimistic. **A 13.7 % error at the
nominal restitution cannot account for a 7.4× miss**, and band 9 puts restitution last with
S_T = 0.086. *The conclusion survives the verification failure; the precision of the number does
not.* **Nothing downstream may quote 14.845 °/s to more than two significant figures until the
contact law is replaced or the band is met.**

### What is not trustworthy in this run, stated plainly

**Peak contact force in the tails.** The Monte Carlo maximum is **995.9 kN**, and the 300 and
400 mm land-sweep points return 52.9 kN and 197 kN. Those are penalty-contact numerical
excursions, not forces. **The divergence guard catches a sample that leaves the bore and does not
catch one whose contact force spikes while it stays inside** — 13 of 288 samples diverged and 4
stalled, and they are excluded from the statistics, but the peak-force tail is still contaminated.
**Band 6 is evaluated where it was declared, at the nominal point, and it passes at 225.8 N.**
*Peak contact force under tolerance is an open question this run does not answer.*

**The step size, and why it is in the results file.** The answer is **wrong by 40 % at h = 2×10⁻⁵**
— the step a first attempt reaches for — and converged below 5×10⁻⁶:

| h (s) | 4e-5 | 2e-5 | 1e-5 | 5e-6 | 2.5e-6 | 1.25e-6 | 6.25e-7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| rate °/s | 8.786 | 9.551 | 15.098 | **14.880** | **14.877** | **14.879** | **14.876** |

**Everything above runs at 110 steps per contact period**, which puts the nominal case at 5×10⁻⁶.

### What this run does not answer

**It does not calibrate against hardware.** **E4** — nothing is measured, and the six declared
brackets are engineering assumptions with no source in this repository. **It does not consume a
deformed bore centreline from a structural solve**: the straightness bracket is declared, and
**band 9 has just made that the most important input in the model**, so coupling it to A59's own
tube deflection is now the highest-value remaining work rather than a refinement.
**It does not model stick-slip**, and B-2 band 11 is what would justify adding it.
