# Installed-system break-even — N6

Adityavardhan Mishra · 25 September 2026

This is a 900-case sensitivity, not a completed installed mass estimate or proof of product advantage. Twelve identical 4 kg propulsionless payloads and a 300 kg retained baseline (including the conventional deployer) define both sides. All candidate increments are assumed differences above that baseline. Extra cell structure, controls, harness, launch restraint and host modifications must fit inside the stated increment; they are never implicitly free.

Baseline wet mass = 348 exp((common Δv + avoided Δv)/(g₀Isp)); candidate wet mass = (348 + ΔM) exp(common Δv/(g₀Isp)). This places all burns before release and carries all payload mass throughout. It cannot represent a sequential manifest with evolving mass. The exact break-even avoided Δv is g₀Isp ln(1+ΔM/348). A saved release impulse is not automatically avoided host Δv.

| Increment per cell (kg) | Shared increment (kg) | Total increment (kg) | Break-even at 60 s (m/s) | At 220 s | At 320 s |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 2 | 5 | 8.39 | 30.78 | 44.77 |
| 0.5 | 5 | 11 | 18.31 | 67.14 | 97.66 |
| 1 | 5 | 17 | 28.06 | 102.90 | 149.67 |
| 2 | 10 | 34 | 54.85 | 201.11 | 292.53 |

Higher-Isp hosts save less propellant per avoided m/s, so more avoided Δv is needed to repay added dry mass. Common host burns multiply both wet masses: they increase the magnitude of the gain or loss but do not change this simplified break-even threshold. Negative and zero-benefit cases remain in the JSON.

The release cells must demonstrate an actual matched-mission maneuver saving before any row becomes an evidenced benefit. No supplier cost, launch price, mission success probability or complete installed mass is inferred. Independent-cell jam isolation can limit the number mechanically stranded, but cannot supply a reliability probability.

[Criteria](../validation/N6_installed_trade.md) · [All cases](../analysis/results/installed_trade.json) · [Accounting ledger](INSTALLED_ACCOUNTING.csv)
