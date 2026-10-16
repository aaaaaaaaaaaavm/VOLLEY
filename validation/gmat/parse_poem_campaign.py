"""Parse twelve native GMAT R1 reports without importing project analysis code.

The nearest separation is a sampled value. It is not continuous-time clearance.
"""

import argparse
import datetime as dt
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
REPORTS = [HERE / 'output' / 'r1' / f'sat{i:02d}.txt' for i in range(1, 13)]
OUT = REPO / 'validation' / 'results' / 'A15_R1_gmat_r2026a_review.json'
RE_KM = 6378.137
MU_KM = 398600.4418
INITIAL_ALT_KM = 450.0
REFERENCE_INC_DEG = 51.6
PAYLOAD_KG = 4.0
HOST_KG = 300.0
RELATIVE_SPEED_M_S = 16.029
SPACING_S = 1200.0


def circular_span_deg(angles):
    ordered = sorted(x % 360 for x in angles)
    gaps = [b - a for a, b in zip(ordered, ordered[1:])]
    gaps.append(ordered[0] + 360 - ordered[-1])
    return 360 - max(gaps)


def angular_distance_deg(angle):
    return abs((angle + 180) % 360 - 180)


def parse_line(line):
    parts = line.split()
    if len(parts) != 12:
        raise ValueError(f'Expected date plus eight numeric fields: {line[:100]!r}')
    time = dt.datetime.strptime(' '.join(parts[:4]), '%d %b %Y %H:%M:%S.%f')
    return time, [float(x) for x in parts[4:]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports-dir', type=Path, default=HERE / 'output' / 'r1')
    args = parser.parse_args()
    reports = [args.reports_dir / f'sat{i:02d}.txt' for i in range(1, 13)]
    handles = [path.open(encoding='utf-8') for path in reports]
    try:
        headers = [handle.readline().split() for handle in handles]
        if any(len(header) != 9 for header in headers):
            raise ValueError('Unexpected GMAT report header')
        first = last = None
        count = 0
        closest = (math.inf, None, None)
        largest_step_s = 0.0
        start_time = previous_time = None
        for lines in itertools.zip_longest(*handles):
            if any(line is None for line in lines):
                raise ValueError('GMAT report row counts differ')
            parsed = [parse_line(line) for line in lines]
            times = [item[0] for item in parsed]
            if any(time != times[0] for time in times):
                raise ValueError(f'GMAT report timestamps differ at row {count + 1}')
            time = times[0]
            states = [item[1] for item in parsed]
            if start_time is None:
                start_time = time
                first = states
            else:
                largest_step_s = max(largest_step_s, (time - previous_time).total_seconds())
            previous_time = time
            last = states
            count += 1
            elapsed_s = (time - start_time).total_seconds()
            for i in range(12):
                for j in range(i + 1, 12):
                    if elapsed_s < j * SPACING_S:
                        continue
                    pos_i, pos_j = states[i][5:8], states[j][5:8]
                    distance_km = math.sqrt(sum((a - b)**2 for a, b in zip(pos_i, pos_j)))
                    if distance_km < closest[0]:
                        closest = (distance_km, [i + 1, j + 1], time.isoformat())
        if count == 0:
            raise ValueError('No GMAT data rows')
        elapsed_days = (previous_time - start_time).total_seconds() / 86400.0
        if abs(elapsed_days - 90.0) > 1e-5:
            raise ValueError(f'Campaign ended at {elapsed_days} days, not 90')

        inc_change = max(abs(s[2] - REFERENCE_INC_DEG) for s in first)
        raan_change = max(angular_distance_deg(s[3]) for s in first)
        apogees = [s[0] * (1 + s[1]) - RE_KM for s in first]
        perigees = [s[0] * (1 - s[1]) - RE_KM for s in first]
        extent = max(apogees) - min(perigees)
        final_raan_span = circular_span_deg([s[3] for s in last])
        initial_raan_span = circular_span_deg([s[3] for s in first])
        radius = RE_KM + INITIAL_ALT_KM
        vc_km_s = math.sqrt(MU_KM / radius)
        payload_dv_km_s = HOST_KG / (HOST_KG + PAYLOAD_KG) * RELATIVE_SPEED_M_S / 1000
        reference_sma = 1 / (2 / radius - (vc_km_s + payload_dv_km_s)**2 / MU_KM)
        sma_error_pct = abs(first[0][0] - reference_sma) / reference_sma * 100

        bands = [
            {'band': 1, 'value': inc_change, 'limit': '<=0.13 deg', 'pass': inc_change <= 0.13},
            {'band': 2, 'value': extent, 'limit': '>=100 km', 'pass': extent >= 100},
            {'band': 3, 'value': raan_change, 'limit': '<=0.75 deg', 'pass': raan_change <= 0.75},
            {'band': 4, 'value': final_raan_span, 'limit': '>=5 deg', 'pass': final_raan_span >= 5},
            {'band': 5, 'value': sma_error_pct, 'limit': '<=0.5 pct', 'pass': sma_error_pct <= 0.5,
             'caveat': 'GMAT initializes with generated SMA; this is an input consistency check'},
            {'band': 6, 'value': closest[0], 'limit': '>0.1 km', 'sampled_pass': closest[0] > 0.1,
             'caveat': 'Adaptive output samples do not prove continuous-time clearance'},
        ]
        result = {
            'analysis': 'A15 R1 current-baseline review',
            'solver': 'GMAT R2026a',
            'status': 'NATIVE EXECUTED; provisional until independent review',
            'relative_speed_m_s': RELATIVE_SPEED_M_S,
            'payload_delta_v_m_s': payload_dv_km_s * 1000,
            'sample_count_per_satellite': count,
            'start_utc': start_time.isoformat(),
            'end_utc': previous_time.isoformat(),
            'elapsed_days': elapsed_days,
            'largest_report_step_s': largest_step_s,
            'initial_circular_raan_span_deg': initial_raan_span,
            'minimum_sampled_separation_km': closest[0],
            'minimum_sampled_pair': closest[1],
            'minimum_sampled_time': closest[2],
            'bands': bands,
            'band7': {'allocated_slot_h': 4.0, 'first_to_last_shot_h': 11 * SPACING_S / 3600},
            'band8': 'VOID; no named host manoeuvre authority',
            'limitations': ['Fixed 300 kg host per shot; no recoil propagation or mass depletion',
                            'Preloaded post-release orbits, not a real sequential release simulation',
                            'Analytic backward propagation neglects J2 and drag during up to 3.67 h',
                            'R2/R3 reference orbit provenance remains unverified'],
        }
        OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, indent=2))
    finally:
        for handle in handles:
            handle.close()


if __name__ == '__main__':
    main()
