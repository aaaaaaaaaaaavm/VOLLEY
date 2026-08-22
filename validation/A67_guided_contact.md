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
