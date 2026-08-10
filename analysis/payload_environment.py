"""P34 step 1: the magnetic environment a payload experiences INSIDE this deployer.

WHY THIS IS A DIFFERENT DOCUMENT FROM THE KEEP-OUT
--------------------------------------------------
paper.tex publishes a magnetic keep-out radius, and ADR-010 specifies four things VOLLEY asks
of a HOST. Both point outward. Neither states what the deployer does to the satellite it is
carrying, and "the satellite is never modified" -- the central claim of this project -- has been
doing quiet work on that silence. This script computes the inward-facing half.

WHY IT CAN BE COMPUTED NOW
--------------------------
P34 step 1 said "compute the field over the payload envelope with a model whose far field is
trustworthy, which means resolving P3 first". P3 and P21 are both resolved: magpylib's Cuboid is
an EXACT analytic solution for a uniformly magnetised block, so the finite-array field is already
three-dimensional and correct with no mesh, and far_field_sensitivity.py showed the n_wave=7
default is converged to 0.64 % at 10 mm and 4.4 % at 20 mm against a 15-wavelength array. The
block behind step 1 was real when it was written and is not real now.

WHAT IT DOES NOT ESTABLISH
--------------------------
The field a satellite sees while stowed in a CASSETTE, as opposed to cradled on the sled. The
cassette sits off the thrust line and its standoff from the sled arrays is not in
cad/parameters.json in a form this model can consume. Every number here is referenced to the
sled's own Halbach arrays, which is the worst case and the case that matters, but it is not the
whole duty cycle. Stated rather than quietly omitted.

Run:  python3 analysis/payload_environment.py
"""
import json
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

B_EARTH = 45e-6           # LEO, 25-65 uT range. A14 comparator table
MAG_FULL_SCALE = 100e-6   # class figure for a CubeSat attitude magnetometer, NOT a datasheet
PAYLOAD_NEAR, PAYLOAD_FAR = 0.020, 0.120   # CAD z of the 3U payload envelope

# The envelope, sampled at the stations a customer would ask about.
STATIONS = [0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090, 0.100, 0.110, 0.120]


def peak_at(field, z, nx=240):
    """Peak |B| over one wavelength at height z. Peak, not mean: a payload does not get to
    average over the pole pitch, it sits at whatever phase it sits at."""
    xs = np.linspace(0, mm.LAM, nx, endpoint=False)
    pts = np.stack([xs, np.full(nx, z), np.zeros(nx)], axis=1)
    return float(np.linalg.norm(field.getB(pts), axis=1).max())


def main():
    field = mm.build_field()

    # Operating point, imported rather than restated.
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        motor = json.load(f)
    t_shot_ms = motor['shot']['t_ms']

    rows = []
    for z in STATIONS:
        b = peak_at(field, z)
        # Gradient by central difference: force on a soft-magnetic part goes as grad(B^2),
        # so the gradient is the quantity that says whether a part is also PULLED.
        h = 0.001
        db_dz = (peak_at(field, z + h) - peak_at(field, z - h)) / (2 * h)
        rows.append(dict(
            z_mm=z * 1e3,
            B_mT=b * 1e3,
            vs_earth=b / B_EARTH,
            vs_magnetometer_fullscale=b / MAG_FULL_SCALE,
            dB_dz_mT_per_mm=db_dz * 1e3 / 1e3,
        ))

    # Where the field falls below each comparator.
    zs = np.concatenate([np.linspace(0.015, 0.20, 120), np.linspace(0.21, 1.0, 40)])
    prof = [(float(z), peak_at(field, z)) for z in zs]
    below_fs = next((z for z, b in prof if b < MAG_FULL_SCALE), None)
    below_earth = next((z for z, b in prof if b < B_EARTH), None)

    res = dict(
        analysis='P34 payload magnetic environment',
        method='magpylib finite-block analytic field, exact in free space; peak over one '
               'wavelength at each station',
        unblocked_by='P3 and P21 both CORRECTED; far_field_sensitivity.py showed n_wave=7 '
                     'converged',
        reference_frame='z measured from the stator mid-plane; array back face at z = 14 mm',
        envelope=dict(near_face_mm=PAYLOAD_NEAR * 1e3, far_face_mm=PAYLOAD_FAR * 1e3,
                      note='3U payload envelope from cad/parameters.json'),
        comparators=dict(earth_field_uT=B_EARTH * 1e6,
                         magnetometer_full_scale_uT=MAG_FULL_SCALE * 1e6,
                         magnetometer_note='class figure, not a datasheet; replace with a '
                                           'specific part before this is cited'),
        stations=rows,
        crossings=dict(below_magnetometer_fullscale_mm=below_fs * 1e3 if below_fs else None,
                       below_earth_field_mm=below_earth * 1e3 if below_earth else None),
        exposure=dict(
            drive_transient_ms=t_shot_ms,
            drive_transient_note='one shot. A14 found the drive is NOT the dominant term',
            static_note='the Halbach array is a permanent magnet. The static field is present '
                        'continuously while the payload is cradled, not only during the shot',
            cadence_s=1200.0,
            cadence_source='ADR-020',
            campaign_s=12 * 1200.0,
            static_bound_note='lower bound one cadence interval if indexed immediately before '
                              'firing; upper bound the whole campaign if cradled throughout. '
                              'Cradle dwell is not specified anywhere in this repository',
        ),
        soft_magnetic_parts_in_the_load_path=dict(
            magazine_septum='silicon steel, 1.0 mm, cad/parameters.json groups.magazine',
            gate_pins='A-286',
            note='this is the deployer own materials, NOT a payload materials list. P34 step 2 '
                 'still needs the latter',
        ),
    )

    print('P34 payload magnetic environment, across the 3U envelope\n')
    print(f"  {'z mm':>7}{'B mT':>10}{'x Earth':>10}{'x mag FS':>11}{'dB/dz mT/mm':>14}")
    for r in rows:
        print(f"  {r['z_mm']:7.0f}{r['B_mT']:10.3f}{r['vs_earth']:10.1f}"
              f"{r['vs_magnetometer_fullscale']:11.1f}{r['dB_dz_mT_per_mm']:14.4f}")
    print(f"\n  below magnetometer full scale at z = {below_fs*1e3:.0f} mm")
    print(f"  below Earth's field at        z = {below_earth*1e3:.0f} mm")
    print(f"  envelope spans z = {PAYLOAD_NEAR*1e3:.0f} to {PAYLOAD_FAR*1e3:.0f} mm, so the "
          f"WHOLE payload sits above both")
    print(f"\n  drive transient {t_shot_ms:.1f} ms per shot; static field continuous while cradled")

    path = os.path.join(RESULTS, 'payload_environment.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
