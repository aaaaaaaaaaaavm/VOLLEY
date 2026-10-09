# Phasing correction — 9 October 2026

The historical A21-R record claimed that two CubeSats released 468 seconds apart from an unchanged host, with zero relative impulse, would acquire a persistent 30° in-track phase offset. **That claim is withdrawn.** It confused the host's absolute orbital angle traversed during the wait with the relative angle between a payload and the same co-orbital host. At the second release epoch, the first payload and host are still in the same state in the stated two-body model, so both payloads start from the same state. A clock alone cannot separate them.

An actual **relative state change** can create phasing: spring impulse, a host maneuver, differential drag, or a commanded VOLLEY release. The value of each must be compared at the same epoch, with the same payload and mission assumptions. The original “255× faster” and “76.9° per shot for free” conclusions have no valid physical basis and must not be used in a presentation or trade.

![Same-epoch two-body phasing comparison](../figures/phasing_reference.svg)

*The first payload receives the indicated tangential impulse; the second receives zero after a 468 s wait. The red zero-impulse line stays at zero. This is a planar two-body surrogate, not a flight result.*

[Corrective run sheet](../validation/P113_S16_phasing_correction.md) · [Executable model](../analysis/phasing_reference.py) · [Full result JSON](../analysis/results/phasing_reference.json) · [Original A21-R, retained with withdrawal notice](../validation/A21R_release_timing.md)

This correction does **not** establish a winning Gen5 mission. The improved relative impulse still has to justify the installed mass, host resources, release reliability and payload compatibility. The finite-burn twelve-payload screen currently delivers at most 5/12 in its sampled cases. Published spring and drag systems remain valid comparators under matched assumptions.
