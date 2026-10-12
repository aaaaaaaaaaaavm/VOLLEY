# Gen5 and widened R1 assembly intersection audit

The evaluated Gen5 geometry is retained as a failed configuration. This audit reads the native FreeCAD 1.0 documents and computes the exact common volume of every pair of named leaf solids. The procedure and machine-readable pair list are in [`audit_gen5_full_interference.py`](audit_gen5_full_interference.py) and [`GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json`](GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json). Assembly container shapes are excluded to avoid duplicate counting.

| Configuration | Leaf solids | Nonzero pairs | Result |
|:--|--:|--:|:--|
| Evaluated Gen5 | 20 | 17 | Fails the cassette/track width criterion and has additional intersections. |
| Widened R1 candidate | 21 | 5 | Removes cassette/track overlap only; no complete assembly clearance. |

The original **526 mm** clear width is less than the **537 mm** required by a 205 mm track and two 166 mm cassettes. Each cassette intersects the track by **32,915 mm³**. The sled also intersects the track by **82,983 mm³** and the stator by **6,300 mm³** in the reference placement. The track solid was not cut to create a roller corridor; the sled backstop shares the stator proxy volume. These two conflicts remain in R1. The ring/interface proxy intersects track, stator and enclosure proxies. Several stored-payload boxes intersect cassette solids. Those latter intersections require part-definition and intended-contact review before they can be classified as physical collisions.

The proposed correction is a separate, controlled geometry revision with an actual roller channel, stator/backstop separation, provider adapter load path, cassette rails and retention surfaces. That revision must pass whole-assembly static checks, continuous motion sweeps, clearance and tolerance stacks, then mass/CG/inertia reconciliation. No such Gen5 correction is claimed here. The Gen6 one-cell integration study addresses a different configuration and does not revise this result.
