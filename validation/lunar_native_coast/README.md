# Lunar native coast capture

GMAT R2026a, one TAI epoch, two prescribed MJ2000Eq planes.

- [Report](REPORT.md): model, units, outcomes, sensitivity and limits.
- [Results](RESULTS.json): 18 actual native attempts and common checkpoint comparisons.
- [Native source identities](SOURCE_IDENTITY.json), [case decks](decks/), and [runtime output](runs/).
- [Altitude figure](figures/lunar_sampled_altitude.pdf) and [refinement figure](figures/lunar_refinement.pdf).

Twelve attempts requested 180 days: seven end at the 1737.4 km sphere and five reach 180 days. Six bounded high-degree/alternative-field cases reach their requested 30 days. A completed coast does not qualify terrain clearance, lifetime, mission precision or customer acceptance.

Native histories are stored losslessly as .csv.gz. `python -B check_capture.py` verifies both compressed package identities and the decompressed native history hashes. The initial duration/guard diagnostic is separate and excluded from all final result tables.
