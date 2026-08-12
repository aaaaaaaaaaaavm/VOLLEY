"""
VOLLEY | Is a segmented stator actually redundant, or is that just a word?

WHY THIS EXISTS
---------------
docs/FMEA.md classifies the stator winding as one of nine elements whose single failure
forfeits the remaining manifest, and says so deliberately:

    "The stator winding is segmented (paper.tex Sec.VII, and P29 closed the modelling half),
     so losing one segment should degrade thrust rather than stop the machine. NEVER ANALYSED
     as a redundancy. If it holds, the winding stops being a manifest-forfeiting element and
     the requirement above loosens."

This analyses it. A segmented long-stator machine energises only the section under the mover,
so a dead segment is a length of track over which the sled coasts rather than accelerates --
IF the sled is already moving when it gets there.

THE ASYMMETRY THAT MATTERS
--------------------------
A dead segment is not equivalent to any other dead segment. The sled starts at rest. If the
FIRST segment is dead there is no force on a stationary sled and the shot never starts; if a
LATER segment is dead the sled coasts through it and exits slow. The redundancy claim is
therefore true for some segments and false for one, which is not what "redundant" usually
means and is why this needed computing rather than asserting.

Provenance: model output, not independently re-derived. Imports motor_model for the operating
point rather than restating it.
"""
import json
import math
import os

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

M_PAY = 4.0
M_TOT = mm.M_SLED + M_PAY
L_ZONE = mm.ACCEL_ZONE                     # 1.30 m of acceleration
V_NOM = 16.388


def shot_with_dead_segment(n_seg, dead_index, F=None):
    """Exit velocity with segment `dead_index` (0-based) unpowered.

    Energy method: the sled gains F*dx over live segments and coasts over dead ones. Valid
    because the machine is thrust-limited rather than acceleration-limited over the stroke,
    which is the same assumption PII-11 uses to extend the track at constant force.
    """
    if F is None:
        Kt, _ = mm.thrust_constant()
        F = 0.9 * Kt * mm.K_RATED
    L_seg = L_ZONE / n_seg
    if dead_index == 0:
        # No force on a stationary sled. The shot never starts.
        return dict(v_exit=0.0, started=False, work_J=0.0)
    live_len = L_ZONE - L_seg
    W = F * live_len
    v = math.sqrt(2 * W / M_TOT)
    return dict(v_exit=v, started=True, work_J=W)


def sweep():
    out = []
    for n_seg in (2, 4, 6, 8, 12):
        rows = []
        for d in range(n_seg):
            r = shot_with_dead_segment(n_seg, d)
            rows.append(dict(dead=d, v_exit=r['v_exit'], started=r['started'],
                             frac_of_nominal=r['v_exit'] / V_NOM))
        worst = min(r['v_exit'] for r in rows if r['started']) if any(
            r['started'] for r in rows) else 0.0
        out.append(dict(n_segments=n_seg, seg_len_mm=1000 * L_ZONE / n_seg, rows=rows,
                        degraded_v=worst, degraded_frac=worst / V_NOM,
                        n_fatal=sum(1 for r in rows if not r['started'])))
    return out


def lifetime_of(v):
    """What a degraded shot is still worth, since that is the metric E30 uses."""
    import astro
    if v <= 0:
        return 0.0
    a, e = astro.boosted_elements(450e3, v)
    return astro.lifetime(abs(a), abs(e))


if __name__ == '__main__':
    import astro
    base = astro.lifetime(astro.RE + 450e3, 0.0)
    nom = lifetime_of(V_NOM)
    spring = lifetime_of(2.5)
    print(f"nominal {V_NOM} m/s -> {nom:.3f} yr (+{100*(nom/base-1):.1f} %)\n")
    print(f"{'segments':>9s} {'seg len':>9s} {'v if a LATER segment dies':>26s} {'yr':>7s} "
          f"{'vs spring':>10s} {'fatal segs':>11s}")
    res = sweep()
    for s in res:
        lt = lifetime_of(s['degraded_v'])
        print(f"{s['n_segments']:9d} {s['seg_len_mm']:7.0f}mm "
              f"{s['degraded_v']:10.2f} m/s ({100*s['degraded_frac']:4.1f} %) {lt:7.3f} "
              f"{lt/spring:9.2f}x {s['n_fatal']:11d}")
    print("\nThe 'fatal segs' column is the first segment: no force on a stationary sled,")
    print("so the shot never starts. Every other segment degrades the shot rather than losing it.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(v_nominal=V_NOM, m_total=M_TOT, accel_zone_m=L_ZONE,
                   nominal_life_yr=nom, spring_life_yr=spring, unboosted_yr=base,
                   sweep=res), open(os.path.join(RESULTS, 'segment_redundancy.json'), 'w'),
              indent=2)
    print("\n-> results/segment_redundancy.json")
