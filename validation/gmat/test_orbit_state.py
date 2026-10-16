"""Independent state reconstruction for the A15 input generator."""

import math
import unittest

from orbit_state import release_elements


MU = 3.986004418e14
RE = 6378.137e3
ALT = 450e3
INC = math.radians(51.6)
M = 300.0
m = 4.0
u = 16.029


def vec_add(*vectors):
    return tuple(sum(v[k] for v in vectors) for k in range(3))


def vec_scale(factor, vector):
    return tuple(factor * x for x in vector)


def length(vector):
    return math.sqrt(sum(x * x for x in vector))


def independent_mean_from_true(true_anomaly, ecc):
    sine = math.sqrt(1 - ecc * ecc) * math.sin(true_anomaly) / (1 + ecc * math.cos(true_anomaly))
    cosine = (ecc + math.cos(true_anomaly)) / (1 + ecc * math.cos(true_anomaly))
    eccentric = math.atan2(sine, cosine) % (2 * math.pi)
    return (eccentric - ecc * math.sin(eccentric)) % (2 * math.pi)


def independent_true_from_mean(mean_anomaly, ecc):
    target = mean_anomaly % (2 * math.pi)
    low, high = 0.0, 2 * math.pi
    for _ in range(60):
        mid = (low + high) / 2
        if mid - ecc * math.sin(mid) < target:
            low = mid
        else:
            high = mid
    eccentric = (low + high) / 2
    return math.atan2(math.sqrt(1 - ecc * ecc) * math.sin(eccentric),
                      math.cos(eccentric) - ecc) % (2 * math.pi)


def reconstructed_state(elements, time_s):
    ecc = elements['ecc']
    a = elements['sma_m']
    mean_at_epoch = independent_mean_from_true(math.radians(elements['epoch_true_anomaly_deg']), ecc)
    nu = independent_true_from_mean(mean_at_epoch + math.sqrt(MU / a**3) * time_s, ecc)
    inc = math.radians(elements['inc_deg'])
    raan = math.radians(elements['raan_deg'])
    argp = math.radians(elements['argp_deg'])
    co, so = math.cos(raan), math.sin(raan)
    cw, sw = math.cos(argp), math.sin(argp)
    ci, si = math.cos(inc), math.sin(inc)
    p_axis = (co * cw - so * sw * ci, so * cw + co * sw * ci, sw * si)
    q_axis = (-co * sw - so * cw * ci, -so * sw + co * cw * ci, cw * si)
    p = a * (1 - ecc * ecc)
    radius = p / (1 + ecc * math.cos(nu))
    position = vec_add(vec_scale(radius * math.cos(nu), p_axis),
                       vec_scale(radius * math.sin(nu), q_axis))
    speed_scale = math.sqrt(MU / p)
    velocity = vec_add(vec_scale(-speed_scale * math.sin(nu), p_axis),
                       vec_scale(speed_scale * (ecc + math.cos(nu)), q_axis))
    return position, velocity


def expected_release_state(time_s, ip_deg, op_deg):
    radius = RE + ALT
    phase = math.sqrt(MU / radius**3) * time_s
    radial = (math.cos(phase), math.sin(phase) * math.cos(INC),
              math.sin(phase) * math.sin(INC))
    along = (-math.sin(phase), math.cos(phase) * math.cos(INC),
             math.cos(phase) * math.sin(INC))
    normal = (0.0, -math.sin(INC), math.cos(INC))
    payload_dv = M / (M + m) * u
    ip, op = math.radians(ip_deg), math.radians(op_deg)
    position = vec_scale(radius, radial)
    velocity = vec_add(
        vec_scale(math.sqrt(MU / radius) + payload_dv * math.cos(op) * math.cos(ip), along),
        vec_scale(payload_dv * math.cos(op) * math.sin(ip), radial),
        vec_scale(payload_dv * math.sin(op), normal),
    )
    return position, velocity


class OrbitStateTests(unittest.TestCase):
    def test_all_twelve_release_states_round_trip(self):
        directions = [(0, 0), (0, 0), (180, 0), (180, 0),
                      (0, 30), (180, -30), (0, 60), (180, -60),
                      (0, 90), (0, -90), (90, 0), (270, 0)]
        for index, (ip, op) in enumerate(directions):
            time_s = index * 1200.0
            with self.subTest(shot=index + 1):
                elements = release_elements(MU, RE, ALT, math.degrees(INC), u,
                                            M, m, ip, op, time_s)
                actual_r, actual_v = reconstructed_state(elements, time_s)
                expected_r, expected_v = expected_release_state(time_s, ip, op)
                self.assertLess(length(tuple(a - b for a, b in zip(actual_r, expected_r))), 1e-4)
                self.assertLess(length(tuple(a - b for a, b in zip(actual_v, expected_v))), 1e-7)
                self.assertAlmostEqual(elements['payload_delta_v_m_s']
                                       + elements['host_recoil_m_s'], u, places=12)

    def test_raan_at_ascending_node(self):
        elements = release_elements(MU, RE, ALT, math.degrees(INC), u,
                                    M, m, 0, 90, 0)
        self.assertLess(min(elements['raan_deg'], 360 - elements['raan_deg']), 1e-8)

    def test_mean_motion_has_si_units(self):
        mean_motion = math.sqrt(MU / (RE + ALT)**3)
        self.assertGreater(mean_motion, 0.001)
        self.assertLess(mean_motion, 0.002)


if __name__ == '__main__':
    unittest.main()
