# MC-L2 component requirements — P92-S6

Adityavardhan Mishra · 25 September 2026

This is an analytical procurement and coupon-planning package. No part has been
purchased, certified, strength-approved or tested. MC-L2 remains an 80 mm stroke,
4 kg payload, 0.25 kg pusher candidate. Every original S5 corner is retained.

| Derived requirement | Value | Disposition |
|---|---:|---|
| Maximum sampled latch load | 180.502 N | Unfactored working load; stress/contact review open |
| Maximum stored energy | 9.6719 J | Containment and charging review input |
| Maximum sampled initial acceleration | 4.3308 g | Same analytical S5 model |
| Maximum pusher catch absorption | 1.1319 J | Includes continued spring drive |
| Catch planning energy | 1.6978 J | Explicit 1.5x allocation, not proof certification |
| Constant absorber force | 84.892 N | Ideal assumed law |
| Linear absorber full-stroke peak | 169.785 N | Ideal assumed law; 20 mm envelope |
| Fixed-base bench nominal speed | 1.987637 m/s | Compare bench measurements to this model |
| Finite-host final relative speed | 2.000000 m/s | Includes host recoil and pusher capture |

Twenty spring geometries were screened, with all rejected candidates in the JSON.
The lowest wire-mass geometric survivor uses two springs: 1.50 mm
wire, 18.00 mm mean diameter, 10.688 active
turns each, 19.031 mm solid height and 142.273 mm free
length. Pair wire mass is 0.02035 kg and calculated maximum
Wahl shear stress is 1372.1 MPa. **This is not a strength pass
or supplier selection.** Fractional active turns require manufacturer interpretation.
Guide friction, pitch effects, fatigue, stress relaxation, end seating, tolerances
and material allowables remain open. Free-length/diameter ratio is 7.90;
positive guidance is mandatory. Wire mass omits guides and seats. The spring's
distributed moving mass is absent from S5 and needs dynamic calibration.

Rate per spring is Gd⁴/(8D³Na), solid height is (Na+2)d, and free length includes
1.15 times maximum charge travel above solid. Wahl factor is
(4C−1)/(4C−4)+0.615/C. Material modulus/density are illustrative assumptions.
A supplier must return certified material, rate tolerances, set/dwell data and
force-versus-length measurements. Manufacturer reference:
[Lee Spring compression design](https://www.leespring.com/learn-about-compression-springs).

The 162 catch integrations stop inside the envelope and close energy. They do
not establish rebound performance: the spring still pushes after the ideal stop.
An anti-rebound lock must capture and retain the pusher. Shock response depends
on the real force law and compliance. Nine charger lead/efficiency cases retain
load, torque and time. Torque excludes guide losses beyond the stated efficiency,
acceleration and gearbox starting behavior; the screw must disengage before release.

**Measurement requirement failed at full instrument range.** With 0.10 mm standard
gate-spacing uncertainty and 10 µs standard interval uncertainty, expanded speed
uncertainty at 6 m/s is 0.01399 m/s,
above 0.01 m/s. Keep that failure. At the same interval uncertainty, gate spacing
must be known to at most 0.0578 mm
standard uncertainty, or redesign gate spacing/timing and review the budget.
No experimental result exists; the planned 20-shot acceptance remains unexecuted.

[Criteria](../validation/P92_S6_test_article.md) ·
[All numerical cases](../analysis/results/test_article_requirements.json) ·
[Bench procedure](MC_L2_BENCH_PROCEDURE.md) · [Component ledger](MC_L2_COMPONENT_LEDGER.csv)
