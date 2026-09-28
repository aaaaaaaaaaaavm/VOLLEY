# P92-S6: MC-L2 component and instrumented-coupon requirements

Adityavardhan Mishra · 25 September 2026

Freeze before implementation. This is a requirements and sizing study, not a
manufacturing release. Keep P92-S5 limits and all 81 MC-L2 corners unchanged.
Separate flight finite-base release from a rigidly mounted bench fixture.

Evaluate two parallel round-wire compression springs. Use illustrative G=79 GPa
and density=7850 kg/m3; neither is a certified material selection. Sweep wire
diameter 1.5/2/2.5/3/3.5 mm and spring index 6/8/10/12. Solve active turns from
aggregate stiffness; require >=3 active turns, outer diameter <=50 mm, free
length <=250 mm, and 15% charge-travel reserve above solid. Use two inactive
end coils. Report Wahl-corrected peak stress, mass, pitch, and slenderness; do
not apply an invented strength allowable. Guided springs are mandatory; no
buckling or fatigue pass follows from this screen. Select minimum calculated
wire mass among geometric survivors only. Preserve rejected candidates.

Derive latch load, energy, pusher catch work and stroke from all S5 corners.
Show constant and linearly increasing absorber-force models, continuing spring
work and friction; catch integration must reproduce energy to 1e-6 J. A 1.5x
energy allocation is a bench planning assumption, not a safety certification.
Peak loads cannot be inferred from mean loads without an explicit force law.
For charger lead 1/2/4 mm and efficiency .2/.4/.6, report torque at maximum
charge load and charge time at 60 rpm. No motor or screw is selected.

Derive fixed-base bench speed separately. Predeclare characterization criteria:
20 nominal shots; each within 0.10 m/s of its own measured-input energy model;
shot-to-shot sample standard deviation <=0.03 m/s. These are coupon planning
limits, not customer requirements. No powered test is authorized by this study.
Velocity measurement expanded uncertainty target <=0.01 m/s; two gates 0.10 m
apart, spacing uncertainty <=0.10 mm and interval uncertainty <=10 us (standard
uncertainties); combine by root sum square then use k=2. Use a 6 m/s instrument
range. Measured spring force curve, friction, mass, calibration and dimensional
inspection are mandatory before any test can pass.

Verify inverse spring stiffness relative error <=1e-12, catch analytic vs ODE
work <=1e-6 J, finite-to-fixed-base speed limit <=1e-6 m/s at B=1e12 kg,
monotonic torque/lead, positive reserves, and retention of all failed candidates.
Store source hashes and machine-readable loads. Missing hardware evidence must
remain missing; fixture proof loads require structural review and containment.
