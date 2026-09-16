# P113-S5: local operational-uncertainty sensitivity

Declared 2026-09-16 before `analysis/operational_uncertainty.py` exists. P113 and E5 remain open.

## Question

How strongly do the accepted P113-S4 payload terminal states respond to small errors in the state actually delivered at separation, and which error terms therefore deserve the first mission-derived requirement and coupon measurement?

This is deliberately a **local deterministic sensitivity study**, not a probability-of-success claim and not full robust campaign optimisation. It must not invent launch-provider covariance, attitude authority, clearing time or failure rates. The purpose is to turn the existing 10 m position / 0.01 m/s velocity terminal-state screen into traceable sensitivity coefficients before selecting release-cell tolerances.

## Frozen nominal case

Use the best tested **fine-grid, enumerated, either-order** P113-S4 campaign under the `BOLLEY` release-authority screen from the committed `analysis/results/manifest_timing.json` payload. This screen is used only because S4 reports the same best tested fuel result and first-release speed for BOLLEY, Gen5 and historical gas-Gen6 authority; it is not a BOLLEY hardware selection.

The script must refuse to run if the S4 payload is stale against its source hashes or if the selected campaign is not accepted. Preserve both payload events and their actual release epochs, retained masses, separation vectors and terminal targets.

The existing S3/S4 terminal acceptance bands remain unchanged:

- position error: 10 m;
- velocity error: 0.01 m/s.

These are existing study bands, not provider requirements.

## Perturbations

Apply one term at a time to each accepted payload release state. Use symmetric positive and negative perturbations around the nominal event.

### Common release-state terms

For payload position and velocity, use the local radial/tangential basis at the release epoch:

- host/common position error: ±1 m radial and ±1 m tangential;
- host/common velocity error: ±0.001 m/s radial and ±0.001 m/s tangential.

These perturb the payload state delivered to propagation. They are sensitivity probes, not claimed navigation performance.

### Mechanism-relative terms

Recover the commanded relative-release vector from the S4 separation event.

- release-speed magnitude error: ±0.001 m/s along the commanded release direction;
- in-plane release-direction error: ±0.01 degree rotation at fixed relative-speed magnitude.

For mechanism-relative perturbations, recompute payload and retained-host velocities from the same pre-separation centre-of-mass velocity and masses so total linear momentum is conserved. Do not perturb only the payload and silently discard recoil.

The perturbation magnitudes above are derivative steps. They are not tolerances or proposed requirements.

## Derived quantities

For each payload, perturbation family and sign, propagate the perturbed payload state to the same 3600 s terminal epoch using the existing two-body propagator. Record:

- terminal Cartesian position and velocity error relative to the same target;
- signed component changes and vector-norm changes from the nominal terminal error;
- the **central finite-difference terminal-state sensitivity vector**, `(y_plus - y_minus)/(2h)`, separately for position and velocity, and the norm of each vector per unit perturbation;
- radial/tangential terminal error components;
- for mechanism-relative terms, momentum residual after the perturbed separation reconstruction.

The allowance calculation uses the norm of the central **vector** sensitivity, not the derivative of an error norm. This avoids the undefined cusp that an error norm has at a nearly exact nominal solution.

Also report a **one-at-a-time study allowance** for each scalar perturbation: the smaller of the value implied by the remaining 10 m position margin and the value implied by the remaining 0.01 m/s velocity margin under the local vector sensitivity. Label this `LOCAL_LINEAR_ALLOWANCE`, never `requirement`, `accuracy`, `capability` or `validated tolerance`.

If the nominal event already consumes a material fraction of either terminal band, compute the allowance from the remaining margin rather than the full band. A zero or negative remaining margin yields no local allowance.

## Clearing and settling

Do not invent an attitude-control model in this run. Instead report the actual S4 time intervals between the first release and the next release, and between each release and the terminal epoch. Compare those intervals only to study dead-time markers of 30, 60, 120 and 300 s and label the result `SCHEDULE_HEADROOM_ONLY`.

Passing a marker means only that the timestamp gap exists. It does **not** establish that a host can slew, settle, thermally recover or perform the next manoeuvre inside that interval. E5/provider data remain required for that.

## Verification bands

The run fails its own evidence checks if any of the following occurs:

1. **Nominal reproduction:** propagating the unperturbed stored payload state does not reproduce the stored terminal state within 1e-6 m position and 1e-9 m/s velocity.
2. **Central-difference symmetry:** for each scalar perturbation, the magnitudes of the positive and negative terminal-state changes from nominal differ by more than 5 percent. If the response is too close to numerical zero for this ratio to be meaningful, report it as `NUMERICALLY_SMALL` rather than fail by division noise.
3. **Step-size convergence:** halving every derivative step changes each reported non-small central vector-sensitivity norm by more than 2 percent.
4. **Momentum conservation:** every mechanism-relative perturbed separation has linear-momentum residual greater than 1e-9 kg m/s.
5. **Basis integrity:** radial and tangential basis vectors are unit length and orthogonal to 1e-12.
6. **Freshness:** source hashes for the S4 result, this run sheet and the implementation do not match the generated payload.
7. **Corruption control:** a deliberately corrupted stored terminal state, mass or relative-release vector is not detected by the independent tests.

A failed verification band is retained as a failed run. Do not widen a band after seeing the result.

## Required outputs

`analysis/operational_uncertainty.py` must generate:

- `analysis/results/operational_uncertainty.json` with nominal events, perturbations, sensitivities, local linear allowances, schedule headroom and source hashes;
- `docs/OPERATIONAL_UNCERTAINTY.md` with the bounded result and interpretation limits;
- `figures/operational_uncertainty.svg` showing terminal sensitivity without implying probability distributions;
- `tests/test_operational_uncertainty.py` with independent nominal, basis, momentum, convergence, freshness and corruption checks.

The normal verification path must include a freshness check for these outputs before this batch is called complete.

## What this can and cannot change

This run may tighten or expose the **analysis requirements** that the Gen6 reference cell must later satisfy. It may identify release-speed, direction or common navigation terms as dominant. It may show that the current terminal-state bands are incompatible with plausible future error budgets.

It may **not** close P92, P113 or E5; select a sensor; claim provider compatibility; claim release repeatability; assign a probability of success; or convert a local linear allowance into a hardware requirement without a mission/host decision.

The next robust campaign study must combine these sensitivities with declared navigation/pointing bounds, clearing/settling assumptions, host attitude recovery and installed-system burden. This run exists to make those later assumptions visible rather than burying them inside a Monte Carlo.