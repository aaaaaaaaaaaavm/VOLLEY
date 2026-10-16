"""Exact two-body release states for the A15 GMAT input generator.

Lengths are metres, speeds are metres per second, and angles are degrees at the
public function boundary. GMAT receives kilometres and true anomaly in degrees.
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(dot(a, a))


def scale(k, a):
    return tuple(k * x for x in a)


def add(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(3))


def wrap_deg(radians):
    return math.degrees(radians) % 360.0


def true_to_mean(nu, ecc):
    eccentric_anomaly = math.atan2(math.sqrt(1 - ecc * ecc) * math.sin(nu),
                                   ecc + math.cos(nu))
    return (eccentric_anomaly - ecc * math.sin(eccentric_anomaly)) % (2 * math.pi)


def mean_to_true(mean, ecc):
    mean %= 2 * math.pi
    eccentric_anomaly = mean
    for _ in range(20):
        change = (eccentric_anomaly - ecc * math.sin(eccentric_anomaly) - mean) / (
            1 - ecc * math.cos(eccentric_anomaly))
        eccentric_anomaly -= change
        if abs(change) < 1e-14:
            break
    return (math.atan2(math.sqrt(1 - ecc * ecc) * math.sin(eccentric_anomaly),
                       math.cos(eccentric_anomaly) - ecc)) % (2 * math.pi)


def state_to_elements(position, velocity, mu):
    radius = norm(position)
    speed2 = dot(velocity, velocity)
    h = cross(position, velocity)
    hmag = norm(h)
    node = cross((0.0, 0.0, 1.0), h)
    nmag = norm(node)
    eccvec = add(scale(1 / mu, cross(velocity, h)), scale(-1 / radius, position))
    ecc = norm(eccvec)
    sma = 1 / (2 / radius - speed2 / mu)
    if not (sma > 0 and 0 < ecc < 1 and nmag > 0):
        raise ValueError("A15 requires a nonsingular bound inclined release orbit")

    inc = math.acos(max(-1.0, min(1.0, h[2] / hmag)))
    raan = math.atan2(node[1], node[0])
    argp = math.atan2(dot(cross(node, eccvec), h) / (nmag * ecc * hmag),
                      dot(node, eccvec) / (nmag * ecc))
    nu = math.atan2(dot(cross(eccvec, position), h) / (ecc * radius * hmag),
                    dot(eccvec, position) / (ecc * radius))
    return dict(sma_m=sma, ecc=ecc, inc_deg=math.degrees(inc),
                raan_deg=wrap_deg(raan), argp_deg=wrap_deg(argp),
                true_anomaly_deg=wrap_deg(nu), mean_anomaly=true_to_mean(nu, ecc))


def release_elements(mu, earth_radius_m, altitude_m, inclination_deg,
                     relative_speed_m_s, host_mass_kg, payload_mass_kg,
                     in_plane_deg, out_plane_deg, release_time_s):
    radius = earth_radius_m + altitude_m
    inc = math.radians(inclination_deg)
    host_mean_motion = math.sqrt(mu / radius**3)
    phase = host_mean_motion * release_time_s
    radial = (math.cos(phase), math.sin(phase) * math.cos(inc),
              math.sin(phase) * math.sin(inc))
    along = (-math.sin(phase), math.cos(phase) * math.cos(inc),
             math.cos(phase) * math.sin(inc))
    normal = cross(radial, along)
    position = scale(radius, radial)
    circular_speed = math.sqrt(mu / radius)
    payload_dv = host_mass_kg / (host_mass_kg + payload_mass_kg) * relative_speed_m_s
    ip = math.radians(in_plane_deg)
    op = math.radians(out_plane_deg)
    dv_t = payload_dv * math.cos(op) * math.cos(ip)
    dv_r = payload_dv * math.cos(op) * math.sin(ip)
    dv_n = payload_dv * math.sin(op)
    velocity = add(scale(circular_speed + dv_t, along), scale(dv_r, radial),
                   scale(dv_n, normal))
    elements = state_to_elements(position, velocity, mu)
    sat_mean_motion = math.sqrt(mu / elements['sma_m']**3)
    epoch_mean = elements['mean_anomaly'] - sat_mean_motion * release_time_s
    epoch_true = mean_to_true(epoch_mean, elements['ecc'])
    elements.update(sma_km=elements['sma_m'] / 1000.0,
                    epoch_true_anomaly_deg=wrap_deg(epoch_true),
                    payload_delta_v_m_s=payload_dv,
                    host_recoil_m_s=payload_mass_kg / (host_mass_kg + payload_mass_kg)
                    * relative_speed_m_s,
                    dv_t=dv_t, dv_r=dv_r, dv_n=dv_n,
                    release_time_s=release_time_s)
    return elements
