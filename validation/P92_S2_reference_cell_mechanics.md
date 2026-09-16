# P92-S2: mechanical accumulator and catcher screen

Declared 2026-09-16 before implementation or execution. Starting source: `682498b10b6e7182fe672b523f2eac51ddeb1ead`.

I test the independent motor-charged retained-cell reference using a linear unloading spring, guided pusher and local catcher. This is an analytical sizing screen, not component selection or nominal CAD. The payload is 4 kg and target relative release speed is the first event of the accepted S4 fine-grid BOLLEY-authority campaign. The host recoil definition stays separate from internal payload/pusher motion.

## Declared grid and assumptions

Use pusher masses 0.10/0.25/0.50 kg, working strokes 0.08/0.12/0.16/0.24 m, end/start spring-force ratios 0/0.25/0.50/0.75 and constant sliding resistance 0/2/5 N. Spring work supplies kinetic energy of payload plus pusher and sliding work. The pusher and payload remain in contact until exit; flag negative endpoint net force as inadmissible under that assumption. A 10 g peak payload acceleration is a study ceiling, not a spacecraft acceptance specification.

Report spring stiffness, initial/final compression, peak latch force, initial/end acceleration and stored energy. Report ideal catcher average force and energy for stopping distances 5/10/20 mm; peak force, rebound, damping and shock remain unmodelled. Charging efficiencies 0.5/0.7/0.9 are explicit assumptions, applied to initial spring energy; no recovery credit. Report 12-shot stored-energy/charging totals, without claiming installed mass or flight duty.

## Frozen verification and decision rule

- Exactly 144 mechanical cases. Retain rejected cases and reasons.
- Independent work integration must reproduce the kinetic-plus-friction work to relative 1e-10 and absolute 1e-9 J.
- Independent reconstruction of exit speed must agree to 1e-9 m/s.
- Candidate feasibility requires peak net acceleration <=10 standard gravities and nonnegative endpoint net force. No candidate is selected by this study; report the feasible envelope.
- Catcher kinetic energy is pusher kinetic energy only. Check its mass ratio to payload kinetic energy to relative 1e-12.
- At a force ratio of zero and zero friction, minimum stroke must be twice the constant-acceleration ideal stroke. This independent limiting case must reproduce to 1e-12 m.
- Exact source hashes, finite data and regression/corruption checks are required.

I will use the result to write a coupon specification and failure checklist. Measurement uncertainty, force law, preload drift, friction scatter, latch release, separation/tip-off and catcher dynamics remain experiments. Installed mass cannot be inferred from stored energy alone. P92 remains open.
