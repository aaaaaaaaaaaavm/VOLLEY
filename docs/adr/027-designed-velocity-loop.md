# ADR-027: the velocity loop is designed against margins, not tuned to a number

**Status:** Accepted · **Date:** 2026-08-13 · **Phase:** I · **Governs:** `motor_model.KP_VELOCITY`

## Context

`docs/BASELINE.md` publishes a 3σ closed-loop dispersion as a headline number. Until 2026-08-13
that figure came from `motor_model.closed_loop_mc()` running **proportional velocity feedback at
a gain of 3500**, and the gain had no derivation anywhere in the repository: no plant model, no
transfer function, no gain or phase margin, no controller rate, no sensor model, and no check
against the track's structural modes.

**A28 found the gain to be linearly unstable at any plausible sensor delay.** The controller is
feedback-linearised — it divides the command by the modelled thrust constant and multiplies by
the modelled mass — so the plant's own K_t/m cancels and the loop transfer is

    L(s) = Kp/s · exp(-s·tau)

which makes **Kp the gain crossover frequency in rad/s**, not a current gain. 3500 s⁻¹ is a
crossover at **557 Hz**, five times above the track's 109 Hz first mode, with **−50.4°** of phase
margin and **−3.86 dB** of gain margin at the stated 0.7 ms of total lag.

Two things concealed it. `closed_loop_mc` feeds back the *undelayed* state, so its own loop sits
at zero latency where 3500 does hold +69.9° of margin. And the command is clipped to
`[0, K_RATED]`, which turns a linearly unstable loop into a bang-bang relay whose mean follows the
feedforward term, with the terminal photogate trim removing the residual. **The published number
was dominated by the saturation limits and the terminal correction rather than by the feedback it
was attributed to.**

## Decision

**The velocity-loop gain is a designed quantity with a named constraint set, exposed as
`motor_model.KP_VELOCITY`, and is not to be set by tuning against the dispersion figure.**

The constraint set is:

1. **Phase margin ≥ 50°** at the stated transport delay. Above the 45° band, deliberately, so the
   implemented gain is not sitting on its own acceptance limit.
2. **Closed-loop bandwidth ≤ one third of the track's first mode**, currently 109 Hz → 36.3 Hz.
3. **Commanded sheet current at or below `K_RATED` across the stroke.** A design whose linear
   behaviour depends on its saturation limits is not a designed loop.

`analysis/control_design.py::design_gain()` returns the largest gain satisfying (1) and (2)
simultaneously: **195.2 s⁻¹**. `KP_VELOCITY` is **195**, rounded down so the implemented gain sits
at or below the designed limit rather than exactly on it.

## Alternatives

**Keep 3500 and declare the loop as tested at zero latency.** Rejected. The dispersion figure is
published as a property of the design, and a design whose stability depends on an instantaneous
sensor is not one. The delay is the assumption; the instability is not.

**Keep 3500 and raise the controller rate to buy back phase.** Rejected as insufficient. The
zero-order hold contributes 100 µs of the 700 µs; even an infinitely fast controller leaves the
600 µs transport delay, which alone gives −38° of phase margin at 3500 s⁻¹. The rate is not the
problem, the crossover is.

**Add a notch at 109 Hz and keep the bandwidth.** Rejected for Phase I. A notch is a commitment to
knowing the mode frequency, and `docs/STRUCTURAL_GAP.md` records that the track's Q and modes are
unmeasured. A notch mistuned by 10 % is worse than no notch. This is a legitimate Phase II option
once **B-1** and a modal survey exist, and it is recorded there rather than adopted here.

**Design to the 45° band exactly, maximising gain.** Rejected. The implemented value would then
sit on its own acceptance limit, so any adverse latency at all would fail the band. The 50°
target buys the margin that makes the 45° band meaningful.

## Consequences

**The gain falls by a factor of 18 and the dispersion does not move**, 0.0271 → 0.0267 m/s. That
is the substantive finding: the loop never needed the bandwidth, because the dispersion is set by
the terminal trim and by the K_t and mass tolerances, not by loop gain. Margins go from negative
to **+82.2°** and **+21.2 dB**, and saturation from 29.7 % of the stroke to zero.

**K_t stays 11.0258 N/kA·m and v_exit stays 16.388 m/s.** Neither depends on the controller. Only
the dispersion row of `docs/BASELINE.md` moved, under change-control rules 1 and 2. **No
validation is invalidated** — nothing else in the repository reads `closed_loop_mc`.

**What this decision does not do.** It does not add integral action or ripple feedforward; a
single proportional term is what the project publishes and what was tested, and adding structure
alongside a defect fix would confuse a correction with an improvement. It does not model the
track as compliant — **P36** stands, and the 48 Hz and 109 Hz modes enter only as a frequency the
bandwidth is held away from. It does not select a sensor — **E7** stands, and the 0.6 ms delay is
a stated assumption swept rather than asserted.

**The binding constraint is now item (2), the structural one.** If the track's first mode is ever
measured and comes in lower than 109 Hz, the designed gain falls with it. That coupling is the
reason the constraint is written into the ADR rather than into a comment.

## Validation

**How we would find out this is wrong.**

- **A measured track mode below 109 Hz** invalidates the bandwidth cap and therefore the gain.
  `analysis/sizing.py` gives 109 Hz fixed-fixed from a beam model; a modal survey is the test, and
  **P36** and `docs/STRUCTURAL_GAP.md` carry it.
- **A selected sensor with transport delay above 349 µs** would already have failed the *old*
  gain; for the designed gain the equivalent threshold is 7.96 ms, well outside any plausible
  photogate-plus-microcontroller chain. Measuring the actual chain latency is the test, and
  **E7** carries it.
- **A dispersion measurement that disagrees with 0.027 m/s** would show the model's error budget
  is wrong regardless of the gain. **B-2** — single-coil thrust against K_t — is the first step of
  that, and nothing here substitutes for it. **E4** stands.
- **Bang-bang behaviour surviving into hardware.** If a real drive shows the command riding its
  rating limit across the stroke, the linearisation is not doing what this ADR assumes, most
  likely because the controller's K_t or mass estimate is wrong by more than the ±1.5 % the Monte
  Carlo disperses. `control_design.py::mc_with_gain()` reports the fraction of stroke above rating
  for exactly this reason.
