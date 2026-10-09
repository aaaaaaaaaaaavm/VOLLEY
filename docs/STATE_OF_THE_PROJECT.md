# Where VOLLEY stands

Updated 2026-10-09. [Current configuration status](NEXT_GENERATION_STATUS.md) · [Open review gates](GEN5_FREEZE_READINESS.md) · [Engineering repository](https://github.com/aaaaaaaaaaaavm/VOLLEY)

## Academic review configuration

Gen5 is the controlled computational configuration for the thesis and IEEE-formatted paper. It models a host-mounted, reusable electromagnetic launch path for ordinary 3U CubeSats with sequential side-cassette feed, a permanent-magnet sled, pulse store and eddy-current arrest. The academic review can present the complete *evaluation*, including negative findings. The final design and academic freeze remain open; no hardware has been built or measured, and no provider or payload interface has been approved.

The reference arrangement fails an **11 mm transverse fit** and **32,915 mm³ exact-solid overlap per cassette**. Modeled dry mass is **10.55 kg per carried 3U**, failing the study's economic screen and an approximate 6 kg canister comparison. A finite-geometry force screen gives **12.448 m/s at ideal phase** and challenges the historical **16.029 m/s** periodic-model point. Independent 2-D FEM and 3-D numerical checks corroborate selected ideal force quantities, not a rated winding or flight performance. [CAD audit](../validation/P116_gen5_assembly_packaging.md) · [mass audit](../validation/P117_rated_energy_mass_audit.md) · [force audit](../validation/P118_gen5_finite_force_map.md).

A matched reference mission compares the same host, payload and target against a spring class and Gen5 model speeds. No sampled twelve-shot case closes. The earlier two-payload campaign remains a bounded exploratory study. Neither establishes product-market fit, a qualified mission service or an acceptable installed burden. [Mission record](MATCHED_MISSION_REFERENCE.md) · [market and spacecraft fit](../MARKET_AND_CUSTOMER_FIT.md).

## Development boundary

R1 is an unselected widened feeder geometry candidate; it does not replace the evaluated Gen5 results. Gen6 is future research toward a 1 km/s-class objective, with no selected architecture or achieved speed. The independent spring-cell bank and long gas guide are historical, unselected studies. [Configuration details](NEXT_GENERATION_STATUS.md) · [lab vault](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab).

The next release decision needs one named payload and host/provider interface, a functioning feeder/release/brake design, moving clearances and tolerances, complete installed budgets, power and force closure, matched mission value, and independent technical review. Instrumented multi-shot hardware tests remain future work. [Issue #42](https://github.com/aaaaaaaaaaaavm/VOLLEY/issues/42) groups those gates.

## How to review the evidence

Start with the [flagship front page](../README.md), [computational review PDF](../reports/GEN5_COMPUTATIONAL_REVIEW.pdf), [STEP/CAD review](../cad/GEN5_CAD_REVIEW.pdf), [provenance policy](PROVENANCE.md) and [open-problem register](../OPEN_PROBLEMS.md). The [Blender operations storyboard](../cad/renders/sequence/README.md) is a STEP-derived depiction of intent, not a moving-mechanism validation. Dated programme and generation records retain their original assumptions for audit; this page controls the current review interpretation.
