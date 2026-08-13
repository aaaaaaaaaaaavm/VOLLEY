# A28: the velocity loop, designed and tested for stability rather than assumed

**Raised in external review as essential, and the review is right.** `docs/BASELINE.md` publishes
**0.027 m/s (3σ)** closed-loop dispersion as a headline number. That figure comes from
`motor_model.closed_loop_mc()`, which implements a position-scheduled square-root velocity profile
with **proportional velocity feedback at a gain of 3500** and a photogate coast-trim correction.

**The gain is asserted.** There is no plant model, no transfer function, no gain or phase margin,
no controller sample rate, no sensor dynamics, and no check that the loop bandwidth stays clear of
the track's structural modes. **A headline number produced by an undesigned loop is an assumption
wearing a result's clothes.**

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/control_design.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/control_design.py`, which returns nothing.

## What is being tested

The plant is the sled and payload driven by the linear motor: commanded sheet current *K* produces
force `F = K_t · K`, accelerating `m = M_SLED + M_SAT`. The loop closes on measured velocity. The
stroke lasts **158.6 ms**, so this is finite-time trajectory tracking, not steady-state regulation,
and classical margins are necessary rather than sufficient — that limitation is stated in the
results, not discovered afterwards.

## Acceptance bands

**Bands 2, 3 and 5 can fail. If they do, the published dispersion figure is not a property of a
stable design and must be relabelled, not defended.**

### Band 1 — the plant reproduces the machine

Open-loop, with feedback disabled, the plant model reproduces `motor_model.shot()`'s exit velocity
to within **1 %**. Imported from `motor_model`, not restated. **FAIL above 1 %.**

### Band 2 — the gain that is already published is stable, with aerospace margins

For the loop **as implemented today** (proportional velocity feedback, gain 3500), linearised
about the mid-stroke operating point:

**Gain margin ≥ 6 dB and phase margin ≥ 45°.**

These are the conventional servo margins, not values chosen to suit the answer. **This band may
fail**, because the gain was never designed against them.

### Band 3 — the loop cannot excite the structure

Closed-loop bandwidth is **at least a factor of 3 below the track's first mode**, which
`analysis/sizing.py` gives as **109 Hz fixed-fixed**: bandwidth **≤ 36.3 Hz**.

**A17 already found the force-ripple chirp sweeps from zero through the 48 Hz and 109 Hz modes
inside the first 4–50 ms of every shot.** A controller with authority near those frequencies does
not merely fail to help, it drives them. **This band may fail**, and P36 already records that the
track has no dynamic design case.

### Band 4 — the loop is not saturating

Across the Monte Carlo, commanded sheet current stays **at or below `K_RATED` for at least 95 % of
the stroke**. `motor_model` already raises if the servo saturates on average, because a saturated
loop reports shortfall rather than dispersion; this band tests the same thing per-sample rather
than in the mean.

### Band 5 — the loop survives sensor latency

With a stated sensor and computation latency, phase margin remains **≥ 30°**.

Latency is the dominant phase cost on a 158.6 ms stroke, and **E7 records that no sensor has been
selected or characterised**. The latency used is therefore a stated assumption, swept rather than
asserted, and the band is on the *result of the sweep at the stated value*. **This band may fail.**

### Band 6 — the published dispersion is reproduced by a designed controller

The 3σ dispersion under a properly designed compensator is within a **factor of 2** of the
published **0.027 m/s**.

If the designed loop gives materially better dispersion, the published figure is conservative and
that is worth knowing. **If it gives materially worse, the published figure is an artefact of an
arbitrary gain** and `docs/BASELINE.md` carries a number the design does not support.

## What this cannot settle

- **No sensor is selected.** E7 stands. Latency, resolution and noise are stated assumptions.
- **Classical margins on a finite-time trajectory are necessary, not sufficient.** A loop with good
  margins can still track badly over 158.6 ms.
- **The plant is rigid.** Track flexibility is represented only by the mode frequency the bandwidth
  is tested against, not by a compliant model. P36 remains open.
- **Nothing here is measured.** E4 stands.
