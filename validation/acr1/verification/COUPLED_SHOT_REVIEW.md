# Frozen coupled shot review

All six 3 m/s cases pass at a 5 µs integration step using the frozen production source, output and four inputs. The nominal/adverse cases sample 3, 20 and 100 µH. This is an implementation and numerical sensitivity review of the averaged model.

| Case | L [µH] | Stop position [m] | Peak mean phase current [A] | Peak cell voltage [V] |
|---|---:|---:|---:|---:|
| Nominal | 3 | 1.507288637 | 248.717 | 2.700000000 |
| Nominal | 20 | 1.507288637 | 248.717 | 2.725424467 |
| Nominal | 100 | 1.507288964 | 249.246 | 2.798824717 |
| Adverse | 3 | 1.507333466 | 423.129 | 2.700000000 |
| Adverse | 20 | 1.507333468 | 423.132 | 2.899987398 |
| Adverse | 100 | 1.507278013 | 420.040 | 2.899999962 |

Refining 20→5 µs changes stop position by at most 0.000669872 mm and peak current by 0.070212 A. Maximum total electrical energy residual is 0.00246665 J. The independently computed reduced-mass kinetic-energy change plus friction agrees with signed motor work within 6.3e-12 J.

The rear-contact release event follows the electrical brake command and occurs when its normal reaction reaches zero. The attached and detached reduced masses are used on their respective sides of that event.

The Thevenin source root and both source-power limits were checked. For regeneration, `Pdc ≥ Vlimit × (Vc − Vlimit) / Rsource`, with `Vlimit = 92.8 V`, enforces the 2.9 V per-cell terminal cap. Source power remains below the positive budget, regeneration remains within its voltage budget, and zero requested q voltage is feasible in every limited step. Maximum actual modulation is 0.958316 of the ideal SVPWM ceiling.

The model uses mean dq current with explicit PWM ripple bounds. It does not resolve transistor switching. Catalog ratings and declared parasitic/loss allocations retain the production model’s scope. This review does not establish whole-product or hardware qualification.

Production source SHA256: `560088cb2a05e270b621700df4de1598cb209237b726bd5569e639c5a0f38155`
Production output SHA256: `176f0e325089c5b3798407810fc6d147398c1b939bedf74ea4baf9fa6061d2e1`
Snapshot: `verification/coupled_shot_snapshots/560088cb2a05e270/01aac645e7ba951a`
