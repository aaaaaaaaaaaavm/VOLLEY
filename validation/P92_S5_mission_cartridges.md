# P92-S5: mission-sized cartridges

Adityavardhan Mishra · 17 September 2026

I freeze this new study before implementation. Work stays local; no GitHub writes,
exports or publication until the entire agreed plan is complete. This run starts
from the surviving P92-S2 source. Earlier reported S3/S4 artifacts are unavailable
in this working copy and are not treated as reproduced evidence.

For a 4 kg payload and 0.25 kg retained pusher, use finite base masses 100/300/1000 kg.
Size separate cartridges at final payload/retained-host speeds 0.5/1/2/3/5 m/s,
working strokes 20/40/80/120/240 mm, and end/start compression ratio 0.25.
Nominal sliding friction is 2 N. Test each geometry unchanged with stiffness
0.95/1/1.05, charge error -0.5/0/+0.5 mm, friction 0/2/5 N, and each base mass.
Do not claim one cartridge provides this whole speed range.

Keep the original 10 g peak ceiling, require positive net end force for contact,
charge compression <=320 mm and initial force <=the P92-S2 case-88 latch reference.
Select the shortest stroke passing all tested contact/load/charge corners;
break ties by stored energy. If none passes, retain the rejection. Speed accuracy
is reported, not assumed accepted; no invented manufacturing tolerance is allowed.
Count catcher work from both relative kinetic energy and continued spring drive
through a 20 mm catch. Peak stopping force remains unknown. No supplier spring or
installed mass is inferred from stiffness.

Verification: energy/inverse speed to 1e-8 m/s; independent integrated motion at
nominal selected points agrees to 1e-7 m/s; two-body plus pusher-capture momentum
residual <=1e-8 kg m/s. Deliberate high-friction contact failure must be rejected.
Store all candidates/corners, selected parameters and source hashes.
