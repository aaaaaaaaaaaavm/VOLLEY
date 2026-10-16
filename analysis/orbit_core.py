"""Small orbital constants and the circular prograde impulse check.

This module has no motor, field, plotting or third-party dependencies, so GMAT
input generation can use the same reference calculation as the main analysis.
"""

import math


MU = 3.986004418e14  # m^3/s^2
RE = 6378.137e3      # m


def boosted_elements(alt_m, dv_m_s):
    radius = RE + alt_m
    circular_speed = math.sqrt(MU / radius)
    semimajor_axis = 1 / (2 / radius - (circular_speed + dv_m_s) ** 2 / MU)
    return semimajor_axis, 1 - radius / semimajor_axis
