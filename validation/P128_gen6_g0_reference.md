# P128 — Gen6 G0 surrogate mission and first-article requirement screen

**Evidence class:** preliminary, reproducible requirement calculation. No customer, provider, hardware or delivery capability has approved it.

Four identical 4 kg 3U payload surrogates start from a 450 km circular orbit on an assumed 300 kg base host. They are assigned distinct **immediate semimajor-axis rise targets** at one reference epoch. This is a requirements screen, **not** a four-release trajectory: the host and payload states after each event, collision avoidance and disposal have not been propagated.

| Axis-rise target | Ideal inertial prograde increment | No-burn relative release at 30 kg study device | ±1 km axis margin if all error is tangential | Ideal mean load over 1.3 m |
|--:|--:|--:|--:|--:|
| 5 km | 2.795 m/s | 2.827 m/s | 0.558 m/s | 0.31 g |
| 10 km | 5.585 m/s | 5.648 m/s | 0.557 m/s | 1.25 g |
| 15 km | 8.369 m/s | 8.464 m/s | 0.556 m/s | 2.81 g |
| 20 km | 11.149 m/s | 11.276 m/s | 0.555 m/s | 4.99 g |

The 30 kg device is **only a recoil calculation input**, not a CAD or mass estimate. A host burn can replace some relative speed. The ideal mean load excludes force ripple, rail contact and release shock. The ±1 km axis tolerance is a deliberately loose trial band; it does not define a complete delivered orbital state.

## Error allocation trial

At the 20 km endpoint, the smaller-side tangential margin is 0.555 m/s. The following **absolute worst-case trial allocations** sum to 0.55 m/s: host navigation 0.10, host control/recoil 0.10, release magnitude 0.15, release direction projection 0.10, and epoch/propagation/tracking 0.10 m/s. This leaves only 0.005 m/s in this one-dimensional screen. They are proposed budgets to challenge, **not measured 3σ performance, a covariance budget, or an approved requirement**. Cross-track, radial, along-track, collision and disposal limits remain open.

## What the one-event mass proxy permits

A spring-class comparator uses four assumed 6 kg units at 2.5 m/s. Both sides carry the same 300 kg base host, four payloads, 220 s host Isp, ideal host preburn and 2 kg fuel reserve. Fuel is re-solved for **one 20 km event only**, so these values must not size a four-shot tank.

| Relative release | Maximum device for equal device + one-event fuel | Fuel at parity | Host preburn at parity |
|--:|--:|--:|--:|
| 2.5 m/s | 24.00 kg | 3.378 kg | 8.678 m/s |
| 3.0 m/s | 24.08 kg | 3.300 kg | 8.184 m/s |
| 6.0 m/s | 24.55 kg | 2.830 kg | 5.219 m/s |
| 11.2 m/s | 25.37 kg | 2.013 kg | 0.079 m/s |

The spring-class device is 24.0 kg; its one-event loaded fuel is 3.378 kg. Release impulse buys only a small mass allowance here. **Mass parity is a benchmark, not a necessary product condition**: a buyer could pay for delivery accuracy, schedule or payload-side savings, but none has been demonstrated or priced. A four-payload Gen6 design should not inherit Gen5's 126.562 kg ledger or quietly count an integrated host structure as mass-free.

## First instrumented article decision

Propose a restrained, reusable-carrier **single-payload 4 kg dummy** rig with commanded 3–6 m/s release and instrumented current, force, speed/vector, contact, brake temperature and host reaction. This is a first measurement range; it does not promise the 11.3 m/s no-burn 20 km endpoint or a sequential feeder. At 6 m/s over a fully usable 1.3 m ideal stroke, mean load is 1.41 g and payload kinetic energy is 72 J before losses. Mechanical containment and an abort state must precede powered shots. A four-slot feed/retention prototype follows only after this single-payload model and test agree within declared bands. Keep 1 km/s in a separate payload/stroke research branch.

**G0 disposition: partial, not passed.** The state is only semimajor axis and the host, payload, interface authority, buyer, deadline, full error covariance, disposal and alternatives' priced terms are unselected. The next decision is to obtain or openly surrogate those inputs before promoting an architecture.

![Gen6 G0 target and mass screen](../figures/gen6_g0_reference.svg)

Reproduce with `python3 analysis/gen6_g0_reference.py`; `--check` verifies the captured data, report and vector figure. P124's result hash is recorded in the JSON.
