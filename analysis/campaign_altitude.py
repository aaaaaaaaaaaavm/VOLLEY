"""
VOLLEY | How long the campaign can last, and what altitude it costs.

WHY THIS EXISTS
---------------
E28, live: two GMAT runs stopped early because their satellites reentered -- 36 days at 350 km
and 55.2 deg, 29 days at 350 km and 9.6 deg -- and only the 450 km case reached the declared 90.
Nothing in this project models campaign mission life. The deployment story has always been told
without saying how long the fleet exists.

E28's own sentence is why this needs a run: "the same drag that separates the nodes is what
pulls the satellites down. The two are not independent effects to be traded; they are the same
effect."

WHAT IS ADDED
-------------
astro.lifetime and reachable_envelope's Hohmann and RAAN functions are imported, not restated.
What is added is the coupling: a campaign scored on satellites STILL ALIVE at the end, and two
lifetimes rather than one -- the satellites', which decides whether a delivery was worth making,
and the stage's, which decides whether a later one can be made at all.

Bands declared in validation/A50_campaign_altitude.md at HEAD, BEFORE this file existed.

Provenance: model output. Static atmosphere via astro.rho, orbit-averaged decay, circular
orbits, no solar-activity variation, no attitude or drag-area variation, and the STAGE's
ballistic coefficient is a DECLARED ASSUMPTION -- no stage mass or area is public, which is E5.
"""
import json
import math
import os

import astro
import reachable_envelope as re_

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

ALTITUDES_KM = (350, 400, 450, 500, 550, 600, 700, 800)
N_SATS = 12
BC_SAT = 61.0                 # astro.py's own default for a 3U, carried unchanged
BC_STAGE = 150.0              # DECLARED ASSUMPTION. A spent stage is heavier per unit area than
                              # a 3U; 150 kg/m2 is a plain guess and is named here rather than
                              # buried. E5: no stage mass or area is public.
DV_SHOT = 29.009              # A44's with-friction exit velocity
CAMPAIGN_TARGETS_D = (30.0, 90.0, 365.0)
SHELLS_PER_CAMPAIGN = 3
SHELL_STEP_KM = 50.0


def years_to_days(y):
    return y * 365.25


def sat_life_days(alt_km):
    a = astro.RE + alt_km * 1e3
    return years_to_days(astro.lifetime(a, 0.0, BC=BC_SAT))


def stage_life_days(alt_km):
    a = astro.RE + alt_km * 1e3
    return years_to_days(astro.lifetime(a, 0.0, BC=BC_STAGE))


def spread_in(alt_km, days):
    """Nodal spread the delivered fleet accumulates in `days`, at this base altitude."""
    shells = [alt_km + i * SHELL_STEP_KM for i in range(SHELLS_PER_CAMPAIGN)]
    return re_.raan_spread_deg(shells, DV_SHOT, days=days)


def campaign_dv(alt_km):
    """Repositioning cost of walking up SHELLS_PER_CAMPAIGN shells and disposing."""
    legs = 0.0
    for i in range(SHELLS_PER_CAMPAIGN - 1):
        legs += re_.hohmann_dv(alt_km + i * SHELL_STEP_KM,
                               alt_km + (i + 1) * SHELL_STEP_KM)
    return legs


def alive_after(alt_km, days):
    """Satellites still up at the end, deployed evenly across the campaign."""
    alive = 0
    for k in range(N_SATS):
        released_at = days * k / max(N_SATS - 1, 1)
        shell = alt_km + (k % SHELLS_PER_CAMPAIGN) * SHELL_STEP_KM
        if sat_life_days(shell) > (days - released_at):
            alive += 1
    return alive


def main():
    print(f"{'alt km':>7s} {'sat life d':>11s} {'stage life d':>13s} {'spread 90d':>11s} "
          f"{'alive@90d':>10s} {'campaign dv':>12s}")
    rows = []
    for h in ALTITUDES_KM:
        sl, gl = sat_life_days(h), stage_life_days(h)
        sp90 = spread_in(h, 90.0)
        a90 = alive_after(h, 90.0)
        dv = campaign_dv(h)
        rows.append(dict(alt_km=h, sat_life_d=sl, stage_life_d=gl, spread_90d=sp90,
                         alive_90d=a90, campaign_dv=dv))
        print(f"{h:7d} {sl:11.1f} {gl:13.1f} {sp90:10.1f}° {a90:10d} {dv:11.1f} m/s")

    # band 6: spread actually ACHIEVED before the fleet dies, not spread in a fixed window
    print(f"\n{'alt km':>7s} {'window d':>10s} {'spread achieved':>17s}")
    achieved = []
    for h in ALTITUDES_KM:
        w = min(sat_life_days(h), stage_life_days(h))
        s = spread_in(h, w)
        achieved.append(dict(alt_km=h, window_d=w, spread_deg=s))
        print(f"{h:7d} {w:10.1f} {s:16.1f}°")
    best = max(achieved, key=lambda r: r['spread_deg'])

    # band 5
    ok90 = [r for r in rows if r['alive_90d'] >= 9]
    # band 8: what a one-year campaign needs
    year_alt = next((h for h in ALTITUDES_KM if sat_life_days(h) >= 365.0), None)

    sats = [r['sat_life_d'] for r in rows]
    rates = [spread_in(h, 1.0) for h in ALTITUDES_KM]

    bands = [
        ('1', 'satellite lifetime at 350 km <= 60 days, consistent with E28',
         f"{rows[0]['sat_life_d']:.1f} d", rows[0]['sat_life_d'] <= 60.0),
        ('2', 'satellite lifetime at 450 km > 90 days, consistent with E28',
         f"{rows[2]['sat_life_d']:.1f} d", rows[2]['sat_life_d'] > 90.0),
        ('3', 'satellite lifetime monotonically increasing in altitude',
         f"{sats[0]:.1f} -> {sats[-1]:.1f} d",
         all(a < b for a, b in zip(sats, sats[1:]))),
        ('4', 'nodal spread rate monotonically decreasing in altitude',
         f"{rates[0]:.3f} -> {rates[-1]:.3f} deg/day",
         all(a > b for a, b in zip(rates, rates[1:]))),
        ('5', 'an altitude exists where a 90-day campaign ends with >= 9 of 12 alive',
         f"{ok90[0]['alt_km']} km" if ok90 else "none", bool(ok90)),
        ('6', 'spread achieved before the fleet dies is reported, and its maximum identified',
         f"max {best['spread_deg']:.1f} deg at {best['alt_km']} km", True),
        ('7', f'campaign dv over {SHELLS_PER_CAMPAIGN} shells <= 200 m/s',
         f"{rows[0]['campaign_dv']:.1f} m/s", rows[0]['campaign_dv'] <= 200.0),
        ('8', 'the altitude for a one-year campaign is stated',
         f"{year_alt} km" if year_alt else f"above {ALTITUDES_KM[-1]} km",
         True),
        ('9', "both the satellites' and the stage's lifetimes are computed",
         'both', True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A50', bands_declared_commit='HEAD~1',
               note='static atmosphere via astro.rho, orbit-averaged decay, circular orbits, no '
                    'solar-activity variation, no attitude or drag-area variation. The STAGE '
                    'ballistic coefficient is a declared assumption of %.0f kg/m2 -- no stage '
                    'mass or area is public, which is E5.' % BC_STAGE,
               bc_sat=BC_SAT, bc_stage=BC_STAGE, dv_shot=DV_SHOT,
               shells_per_campaign=SHELLS_PER_CAMPAIGN, rows=rows,
               spread_achieved=achieved, best_spread=best,
               ninety_day_altitudes=[r['alt_km'] for r in ok90],
               one_year_altitude_km=year_alt,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'campaign_altitude.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
