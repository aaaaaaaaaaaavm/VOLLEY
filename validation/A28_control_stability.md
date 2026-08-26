# A28: the velocity loop, designed and tested for stability rather than assumed

Raised in external review as essential, and the review is right. `docs/BASELINE.md` publishes
0.027 m/s (3σ) closed-loop dispersion as a headline number. That figure comes from
`motor_model.closed_loop_mc()`, which implements a position-scheduled square-root velocity profile
with proportional velocity feedback at a gain of 3500 and a photogate coast-trim correction.

The gain is asserted. There is no plant model, no transfer function, no gain or phase margin,
no controller sample rate, no sensor dynamics, and no check that the loop bandwidth stays clear of
the track's structural modes. A headline number produced by an undesigned loop is an assumption
wearing a result's clothes.

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/control_design.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/control_design.py`, which returns nothing.

## Result, 2026-08-13: four of six bands fail, and the published gain is unstable

`analysis/control_design.py`, bands committed at `3ae36ad` before it existed. Results in
`analysis/results/control_design.json`. Figures `paper/figures/F12_bode.png` and
`F13_latency.png`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | plant reproduces `motor_model.shot()` within 1 % | **0.0168 %** | **PASS** |
| 2 | published gain: PM ≥ 45°, GM ≥ 6 dB | **−50.4°, −3.86 dB** | **FAIL** |
| 3 | closed-loop bandwidth ≤ 36.3 Hz | **671.0 Hz** | **FAIL** |
| 4 | command ≤ K<sub>RATED</sub> for ≥ 95 % of stroke | **70.3 %** | **FAIL** |
| 5 | PM ≥ 30° at 0.6 ms latency | **−50.4°** | **FAIL** |
| 6 | designed-controller 3σ within 2× of 0.027 m/s | **0.0266 m/s** | **PASS** |

**Bands 2, 3 and 5 were flagged in advance as able to fail. They did, and so did band 4.** The
protocol is a numbered defect, not a widened band: this is **P47**.

### The single fact the whole analysis turns on

`motor_model.closed_loop_mc()` computes its command as

```
Kc = (m_hat * a_ff + Kp * (v_plan - v) * m_hat) / Kt_hat
```

it divides by the modelled thrust constant and multiplies by the modelled mass. Substituted
into the plant `a = Kt · Kc / m`, the machine's Kt/m cancels the controller's, and

$$L(s) = \frac{K_p}{s}\,e^{-s\tau}$$

K<sub>p</sub> is therefore not a current gain. It is an acceleration per unit velocity error,
with units of s⁻¹, and its numeric value IS the gain crossover frequency in rad/s. A gain of
3500 is a crossover at 3500 rad/s = 557 Hz.

This was never written down anywhere. Read as a current gain, which is how a reader would take
it — 3500 looks like an arbitrary but harmless tuning number. Read correctly, it is a bandwidth
specification, and it specifies a bandwidth **five times above the track's first mode.**

### Band 2 — the published gain has negative margins

| At K<sub>p</sub> = 3500 s⁻¹, τ = 0.700 ms | | Band |
|---|---:|---|
| Gain crossover | **557.0 Hz** | — |
| Phase margin | **−50.4°** | ≥ 45° |
| Gain margin | **−3.86 dB** | ≥ 6 dB |

τ = 0.700 ms is 0.6 ms of stated transport delay plus the 0.10 ms half-sample of a
zero-order hold at 5 kHz. Both are pure delays and add.

Closed forms, cross-checked against a brute-force scan. Because |L| = K<sub>p</sub>/ω and
∠L = −90° − ωτ are both monotonic, the crossovers are exact: ω<sub>c</sub> = K<sub>p</sub> and
ω<sub>180</sub> = π/(2τ). `verify_margins()` scans the same L(jω) over 400,000 points and returns
−50.4° and −3.86 dB, agreeing to three significant figures. The closed form is what the sheet
quotes; the scan exists so the closed form is checked rather than trusted.

### Band 3 — the loop has authority exactly where the structure is

Closed-loop −3 dB bandwidth at the published gain is **671 Hz** against a band of 36.3 Hz. The
track's modes are at 48 Hz and 109 Hz, sitting 24 dB inside the loop's control authority.

A17 already found that the force-ripple chirp sweeps through both modes in the first 4-50 ms of
every shot. A controller with 24 dB of authority at those frequencies does not merely fail to
damp them, it is a path from measurement noise into structural excitation. P36 records that the
track has no dynamic design case**, and this band is why that matters rather than being tidiness.

### Band 5 — the stability floor is a third of a millisecond

| Transport delay | Phase margin | Gain margin |
|---:|---:|---:|
| 0.00 ms | +69.9° | +13.04 dB |
| 0.10 ms | +49.9° | +7.02 dB |
| 0.20 ms | +29.8° | +3.50 dB |
| **0.35 ms** | **≈ 0°** | **≈ 0 dB** |
| 0.40 ms | −10.3° | −0.94 dB |
| **0.60 ms (stated assumption)** | **−50.4°** | **−3.86 dB** |
| 1.00 ms | −130.6° | −7.79 dB |

The published gain is marginally stable at a total lag of 449 µs, which is 349 µs of transport
delay once the 100 µs hold is paid. `motor_model.closed_loop_mc()` feeds back the *undelayed*
state, so its simulated loop sits at the 0.00 ms row and is stable, the published dispersion
figure was produced by a loop whose sensor is instantaneous. No sensor is instantaneous, and
E7 records that no sensor has been selected or characterised, so 0.6 ms is a stated assumption
rather than a measurement. The point of the sweep is that the *answer changes sign* inside the
range of plausible assumptions, which is not a condition a design can be left in.

### Band 4 — and the reason the simulation looked fine anyway

The command exceeds K<sub>RATED</sub> for 29.7 % of the stroke at the published gain, against
a band of ≤ 5 %.

This is the part worth dwelling on, because it explains why an unstable loop reported a good
number. The command is clipped to [0, K<sub>RATED</sub>]. Clipping turns a linearly unstable loop
into a bang-bang relay whose average tracks the feedforward term, and the terminal ±0.3 m/s
photogate trim then removes the residual. The simulation's output was dominated by its
saturation limits and its terminal correction, not by its feedback. Nothing in it was wrong; it
simply was not measuring what the number was being cited for.

A number can be reproducible, correctly computed, and still not be a property of a design.

### The designed gain, and what it costs, which is nothing

| | Published | Designed | Band |
|---|---:|---:|---|
| K<sub>p</sub> | 3500 s⁻¹ | **195 s⁻¹** | — |
| Gain crossover | 557.0 Hz | **31.1 Hz** | — |
| Phase margin | −50.4° | **+82.2°** | ≥ 45° |
| Gain margin | −3.86 dB | **+21.2 dB** | ≥ 6 dB |
| Closed-loop bandwidth | 671.0 Hz | **36.3 Hz** | ≤ 36.3 Hz |
| Stroke above rating | 29.7 % | **0.0 %** | ≤ 5 % |
| **3σ dispersion** | 0.0271 m/s | **0.0267 m/s** | within 2× |

`design_gain()` returns 195.2 s⁻¹ as the largest gain simultaneously holding >= 50° of phase
margin at 0.6 ms and bandwidth at or below one third of the first mode. `motor_model.KP_VELOCITY`
is set to 195, rounded down so the implemented gain sits at or below the designed limit.

The gain falls by a factor of 18 and the dispersion does not move, 0.0271 to 0.0267 m/s, both
0.027 to two significant figures. That is the diagnostic result of this whole sheet: the loop
never needed 557 Hz of bandwidth, because **the dispersion is set by the terminal trim and by the
Kt and mass tolerances, not by loop gain. Sensitivity to K<sub>p</sub> across the swept range:

| K<sub>p</sub>, s⁻¹ | f<sub>c</sub>, Hz | PM, deg | GM, dB | BW, Hz |
|---:|---:|---:|---:|---:|
| 50 | 8.0 | 88.0 | 33.04 | 8.2 |
| 100 | 15.9 | 86.0 | 27.02 | 17.1 |
| **195** | **31.1** | **82.2** | **21.21** | **36.3** |
| 250 | 39.8 | 80.0 | 19.06 | 49.1 |
| 500 | 79.6 | 69.9 | 13.04 | 136.0 |
| 1000 | 159.2 | 49.9 | 7.02 | 382.3 |
| 2000 | 318.3 | 9.8 | 1.00 | 565.6 |
| **3500** | **557.0** | **−50.4** | **−3.86** | **671.0** |

### What moved in the baseline, and under which rule

Change-control rule 2 in [`../docs/BASELINE.md`](../docs/BASELINE.md), *a validation outcome
against a band declared before its run* — and rule 1, error correction. Both apply.

| | Before | After |
|---|---:|---:|
| `motor_model` velocity-loop gain | 3500 s⁻¹ | **195 s⁻¹** (`KP_VELOCITY`) |
| Closed-loop dispersion, `BASELINE.md` | 0.0271 m/s | **0.0267 m/s** |

Nothing else moved. K<sub>t</sub> is 11.0258 N/kA·m and v_exit is 16.388 m/s, unchanged,
neither depends on the controller. Validations invalidated: none. No other analysis reads
`closed_loop_mc`; the only consumer is the baseline row. This is stated because P19's lesson is
that a baseline change silently invalidating a validation must be declared at the time, not
discovered later.

### What this still does not settle

- Classical margins on a 158.6 ms trajectory are necessary, not sufficient. The loop runs for
  about 5 time constants at the designed gain. A margin-compliant loop can still track badly.
- **The plant is rigid.** The 48 Hz and 109 Hz modes appear as a frequency the bandwidth is held
  away from, not as a compliant model in the loop. P36 stands.
- The delay is an assumption. E7 stands: no sensor is selected, and the phase margin is a
  function of a number nobody has measured. The sweep is the honest form of that.
- No integral action, no feedforward of ripple. A single proportional term is what the project
  publishes and what was tested. Whether the design *should* carry a PI or a ripple feedforward is
  a Phase II question, not something to slip in alongside a defect fix.

---

## What is being tested

The plant is the sled and payload driven by the linear motor: commanded sheet current *K* produces
force `F = K_t · K`, accelerating `m = M_SLED + M_SAT`. The loop closes on measured velocity. The
stroke lasts 158.6 ms, so this is finite-time trajectory tracking, not steady-state regulation,
and classical margins are necessary rather than sufficient, that limitation is stated in the
results, not discovered afterwards.

## Acceptance bands

**Bands 2, 3 and 5 can fail. If they do, the published dispersion figure is not a property of a
stable design and must be relabelled, not defended.

### Band 1 — the plant reproduces the machine

Open-loop, with feedback disabled, the plant model reproduces `motor_model.shot()`'s exit velocity
to within **1 %**. Imported from `motor_model`, not restated. **FAIL above 1 %.**

### Band 2 — the gain that is already published is stable, with aerospace margins

For the loop as implemented today (proportional velocity feedback, gain 3500), linearised
about the mid-stroke operating point:

Gain margin >= 6 dB and phase margin >= 45°.

These are the conventional servo margins, not values chosen to suit the answer. **This band may
fail, because the gain was never designed against them.

### Band 3 — the loop cannot excite the structure

Closed-loop bandwidth is **at least a factor of 3 below the track's first mode**, which
`analysis/sizing.py` gives as **109 Hz fixed-fixed**: bandwidth **≤ 36.3 Hz**.

A17 already found the force-ripple chirp sweeps from zero through the 48 Hz and 109 Hz modes
inside the first 4-50 ms of every shot. A controller with authority near those frequencies does
not merely fail to help, it drives them. **This band may fail**, and P36 already records that the
track has no dynamic design case.

### Band 4 — the loop is not saturating

Across the Monte Carlo, commanded sheet current stays at or below `K_RATED` for at least 95 % of
the stroke. `motor_model` already raises if the servo saturates on average, because a saturated
loop reports shortfall rather than dispersion; this band tests the same thing per-sample rather
than in the mean.

### Band 5 — the loop survives sensor latency

With a stated sensor and computation latency, phase margin remains >= 30°.

Latency is the dominant phase cost on a 158.6 ms stroke, and E7 records that no sensor has been
selected or characterised. The latency used is therefore a stated assumption, swept rather than
asserted, and the band is on the *result of the sweep at the stated value*. **This band may fail.**

### Band 6 — the published dispersion is reproduced by a designed controller

The 3σ dispersion under a properly designed compensator is within a factor of 2 of the
published 0.027 m/s.

If the designed loop gives materially better dispersion, the published figure is conservative and
that is worth knowing. If it gives materially worse, the published figure is an artefact of an
arbitrary gain and `docs/BASELINE.md` carries a number the design does not support.

## What this cannot settle

- No sensor is selected. E7 stands. Latency, resolution and noise are stated assumptions.
- Classical margins on a finite-time trajectory are necessary, not sufficient. A loop with good
  margins can still track badly over 158.6 ms.
- **The plant is rigid.** Track flexibility is represented only by the mode frequency the bandwidth
  is tested against, not by a compliant model. P36 remains open.
- Nothing here is measured. E4 stands.
