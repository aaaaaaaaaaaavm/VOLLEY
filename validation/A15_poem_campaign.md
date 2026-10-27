# A15: twelve-payload orbital screen

**Status: R1 rerun in GMAT R2026a on 30 September 2026; partial evidence.** This study tests orbital outcomes for twelve specified post-release states. It does not simulate a sequence of physical launches from a changing host. The raw R1 reports, scripts, logs and independent review (retained separately) are retained together. [Run instructions](gmat/RUN_POEM.md) identify the current generator and parser.

The previous A15 report used a 16.388 m/s input and treated a 367° raw RAAN difference as fleet plane spread. A circular spread cannot exceed 360°. That report also relied on a generator with a mixed kilometre/SI mean-motion calculation and a mean anomaly written as GMAT true anomaly. Its R2022a raw output is absent from the checked repository, so the earlier numerical verdicts cannot be verified or reused. The earlier report is retained outside this publication candidate for provenance. This file records the corrected 16.029 m/s R1 run only.

## What was run

The R1 reference orbit begins at 450 km altitude and 51.6° inclination. The generator uses twelve 4 kg payloads, a fixed 300 kg retained host and a commanded 16.029 m/s payload-to-host relative separation speed. Its ideal momentum split gives the payload a 15.818092 m/s inertial increment and the host a 0.210908 m/s recoil for each isolated shot. The generator places the host at its calculated orbital position every 1200 s, creates each payload's two-body post-release state, then rewinds the mean anomaly to a common epoch. GMAT propagates those twelve initialized spacecraft for 90 days with a 20×20 Earth gravity field, lunar and solar point masses, SRP and MSISE90 drag.

The generated states omit cumulative host recoil, mass depletion and control recovery. Backward initialization omits J2 and drag during up to 3 h 40 min before the last shot. R2 and R3 have unverified reference orbits and have not been rerun in this repair.

## Current R1 readout

GMAT completed 1 January through 1 April 2027. Each of the twelve synchronized reports has 59,590 rows. The stated bands are kept visible, including checks that are still open.

| Band | Question | Stated threshold | Current R1 result | Reading |
| --- | --- | ---: | ---: | --- |
| 1 | Largest initial inclination change | ≤0.13° | 0.105108° | Meets the numerical threshold for this input set. |
| 2 | Initial apogee-to-perigee altitude extent | ≥100 km | 113.094037 km | Meets the numerical threshold. |
| 3 | Largest initial RAAN offset | ≤0.75° | 0.146582° | Meets the numerical threshold. |
| 4 | Shortest circular RAAN span at 90 days | ≥5° | 14.558545° | Meets the numerical threshold. The old 367° figure is withdrawn. |
| 5 | Semimajor-axis comparison | ≤0.5% | 2.88×10⁻⁹% | Checks that GMAT read the generated initial state. It is not an independent physics test. |
| 6 | Minimum continuous inter-payload separation | >100 m | 247 m at sparse 90-day samples; 190 m at five-second samples around one encounter | Open across the full 90 days. |
| 7 | Twelve-shot timing | 4 h allocated window | 4 h including a final slot; 3 h 40 min first to last shot | The two durations answer different questions. |
| 8 | Host plane-change capability | Report requirement | No named host authority or propellant budget | Capability verdict void. |

The 90-day reports have gaps as large as 163.769 s. Their nearest sampled pair is 11/12 on 9 January at 00:42:48.599 UTC. A second native run with a five-second maximum step from 00:28:48 to 00:57:36 UTC that day found 190.149944 m at a sample. Linear interpolation of the adjacent relative positions gives 180.285836 m. That local rerun does not exclude a closer approach elsewhere in the 90-day span. A continuous-clearance verdict needs a campaign-wide bound or event search tied to the native force model.

The first focused run accidentally propagated an additional 8.04 days and ended on 17 January. Its failed script and logs are preserved in the audit bundle. The corrected script requests a further 0.02 days and ends on 9 January; only the corrected window supports the local readout above.

## What the result can support

The current run shows that a corrected set of preloaded R1 orbits yields the four reported numerical orbit bands under the stated force model. It gives no evidence of a working launcher, approved payload acceleration or interface, host-controlled sequence, safe full-campaign separation, 90-day lifetime for R2/R3, or a market advantage. Those questions remain separate project tasks. A15 cannot close the coupled 2/4/12-payload mission gate on its own.
