# P130 — matched four-release full-state campaign

**Status:** constructive J2 surrogate with ideal instantaneous control. Both options reach the **same four full-state targets** at the P129 common epoch. This is not a global optimum, mission approval, or achieved mechanism capability.

## Fairer control construction

Starting with P129's identical payload, host, target, time and gravity inputs, both options use the **same permitted control schedule**: one ideal host burn immediately before each release and one ideal host transfer burn immediately after each release except the last. A three-axis J2 shooting calculation makes each subsequent host arrival coincide with the reference release position; the pre-release burn then gives the payload the target departure velocity, with ejection recoil and expended propellant included. This is a fixed-time feasible construction, not the fuel-minimum campaign or an operational guidance solution. It resolves P129's intentionally weak local-velocity spring comparison.

| Payload | VOLLEY commanded relative m/s | Spring relative m/s | VOLLEY terminal position m / velocity m/s | Spring terminal position m / velocity m/s |
|:--|--:|--:|--:|--:|
| 1U-A | 3.011 | 2.500 | 0.0000 / 0.000000 | 0.0000 / 0.000000 |
| 3U-A | 5.058 | 2.500 | 0.0000 / 0.000000 | 0.0000 / 0.000000 |
| 1U-B | 7.027 | 2.500 | 0.0000 / 0.000000 | 0.0000 / 0.000000 |
| 3U-B | 9.106 | 2.500 | 0.0000 / 0.000000 | 0.0000 / 0.000000 |

| Assumed architecture | Host Δv sum | Host fuel consumed | Assumed installed device | Initial device + consumed fuel |
|:--|--:|--:|--:|--:|
| Commanded VOLLEY | 0.096 m/s | 0.0154 kg | 30 kg | 30.0154 kg |
| Fixed 2.5 m/s spring | 21.580 m/s | 3.2977 kg | 16 kg | 19.2977 kg |

At these assumed masses, commanded release saves **3.2823 kg** of ideal host fuel but starts with **14 kg** more installed device. Its device-plus-consumed-fuel burden is **10.7177 kg higher**. This does **not** close a product benefit. Power, spacecraft impacts, cost and reliability are unpriced. The break-even installed-mass premium under this narrow fuel-only measure is no more than 3.2823 kg, far below the assumed 14 kg premium.

## Spring speed sensitivity

The published NRCSD 0.5–2.0 m/s is an **ISS deployer payload-survival requirement**, not this hypothetical SSO spring's rating. The 2.5 m/s nominal value is a study input. This sweep tests input sensitivity without claiming that any named dispenser performs at each speed.

| Fixed spring study speed, m/s | Host fuel, kg | Host Δv sum, m/s |
|--:|--:|--:|
| 0.5 | 5.4194 | 35.516 |
| 1.0 | 4.8903 | 32.032 |
| 2.0 | 3.8294 | 25.064 |
| 2.5 | 3.2977 | 21.580 |
| 3.0 | 2.7651 | 18.096 |

## One-at-a-time release error sensitivity

With the nominal host burns held fixed, a **+0.1 m/s relative release-speed error** or a **+1° pitch error** is injected separately at each shot. The table gives 3-D position difference at the common epoch in km. These arbitrary perturbations are illustrative, not measured dispersions, probabilities, customer tolerances or a guidance covariance budget. They show why perfect mathematical terminal matching is not an accuracy claim.

| Payload | VOLLEY +0.1 m/s | Spring +0.1 m/s | VOLLEY +1° | Spring +1° |
|:--|--:|--:|--:|--:|
| 1U-A | 27.15 | 27.15 | 0.10 | 0.08 |
| 3U-A | 26.54 | 26.53 | 0.07 | 0.04 |
| 1U-B | 25.95 | 25.95 | 0.14 | 0.05 |
| 3U-B | 25.32 | 25.31 | 0.22 | 0.06 |

Halving RK4 step from 10 to 5 s changes the two case fuel totals by no more than 0.00000000 kg; maximum inter-release arrival position residual is 0.000037 m, and all four terminal full-state residuals are below 0.000000 m and 0.000000000 m/s. These are numerical checks, **not** guidance/navigation error bounds. The chosen 3–9 m/s surrogate release commands are unproven; 9 m/s is beyond the proposed 3–6 m/s single-dummy first article.

The named [1U, 3U, dispenser and host-service references](../docs/GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md) support only class context, not an applicable provider ICD. The comparison still needs independently specified customer states and tolerances, installed masses from a real design/BOM, finite-burn and attitude constraints, covariance, collision/disposal and an optimization over schedule and direction. Spring plus host can hit these four targets mathematically, so P129's large spring residuals must **not** be used as evidence of VOLLEY advantage.

![Matched full-state campaign resource comparison](../figures/gen6_matched_campaign.svg)

Reproduce with `python3 analysis/gen6_matched_campaign.py`; use `--check` for the captured report, figure and JSON. Input and source hashes are in the JSON.
