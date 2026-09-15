"""P113-S2: bounded sequential energy-target screen, not mission feasibility."""
import argparse
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

import numpy as np
from host_reference import G0, MU, RE
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
INPUTS = dict(altitude_km=450, dry_mass_kg=300, fuel_kg=10, reserve_kg=2,
              isp_s=220, payload_kg=4, manifests=[1, 4, 12], spacing_s=[600, 3600],
              burn_limits=[0, 2, 12], missions=['COMMON_ENERGY', 'ENERGY_LADDER'],
              screens={'fixed_1': [1, 1], 'spring_screen': [.5, 2],
                       'bolley_screen': [.5, 11.8], 'gen5_screen': [.5, 16.029],
                       'gen6_screen': [.5, 29.009]})
BURN_EPS = 1e-8


def positive(*values):
    if not all(math.isfinite(v) and v > 0 for v in values):
        raise ValueError('finite positive inputs required')


def state_check(state):
    state = np.asarray(state, dtype=float)
    if state.shape != (4,) or not np.all(np.isfinite(state)):
        raise ValueError('finite planar position/velocity required')
    positive(np.linalg.norm(state[:2]))
    return state


def elements(state):
    y = state_check(state)
    r = np.linalg.norm(y[:2])
    energy = np.dot(y[2:], y[2:]) / 2 - MU / r
    h = y[0] * y[3] - y[1] * y[2]
    if energy >= 0 or h <= 0:
        raise ValueError('bound prograde orbit required')
    a = -MU / (2 * energy)
    e = math.sqrt(max(0., 1 + 2 * energy * h * h / MU**2))
    return dict(a_m=float(a), energy=float(energy), angular_momentum=float(h),
                perigee_m=float(a * (1 - e)))


def coast(state, seconds, rtol=1e-11):
    y = state_check(state)
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError('finite nonnegative coast time required')
    if elements(y)['perigee_m'] < RE + 120000:
        raise ValueError('HOST_PERIGEE_GUARD')
    if seconds == 0:
        return y.copy()

    def rhs(_, z):
        return np.r_[z[2:], -MU * z[:2] / np.linalg.norm(z[:2])**3]

    result = solve_ivp(rhs, [0, seconds], y, method='DOP853', rtol=rtol,
                       atol=[1e-5, 1e-5, 1e-8, 1e-8])
    if not result.success:
        raise ValueError('PROPAGATION_FAILED')
    return state_check(result.y[:, -1])


def release(state, mass, payload, available_fuel, isp, target_a, interval):
    """Return an event without mutating the input; reserve is excluded from fuel."""
    y = state_check(state)
    lo, hi = interval
    positive(mass, payload, isp, target_a, lo, hi)
    if (hi < lo or mass <= payload or not math.isfinite(available_fuel)
            or available_fuel < 0 or available_fuel >= mass - payload):
        raise ValueError('invalid mass, fuel or interval')
    radial = y[:2] / np.linalg.norm(y[:2])
    tangent = np.array([-radial[1], radial[0]])
    vr, vt = np.dot(y[2:], radial), np.dot(y[2:], tangent)
    speed2 = MU * (2 / np.linalg.norm(y[:2]) - 1 / target_a) - vr**2
    if speed2 <= 0 or vt <= 0:
        raise ValueError('TARGET_ENERGY_UNAVAILABLE')
    target_vt = math.sqrt(speed2)
    ideal_u = (target_vt - vt) / (1 - payload / mass)
    candidates = [float(np.clip(ideal_u, lo, hi)), float(np.clip(ideal_u, -hi, -lo))]
    u = min(candidates, key=lambda v: (abs(v - ideal_u), -v))
    ve = isp * G0

    def residual(h):
        after_burn = mass * math.exp(-abs(h) / ve)
        return vt + h + (1 - payload / after_burn) * u - target_vt

    limit = ve * math.log(mass / (mass - available_fuel))
    if abs(residual(0)) <= 1e-11:
        h = 0.
    elif residual(-limit) > 0 or residual(limit) < 0:
        raise ValueError('PROPELLANT_RESERVE')
    else:
        h = brentq(residual, -limit, limit, xtol=1e-12)
    after_burn = mass * math.exp(-abs(h) / ve)
    retained = after_burn - payload
    pre_release_v = y[2:] + h * tangent
    payload_v = pre_release_v + retained / after_burn * u * tangent
    host_v = pre_release_v - payload / after_burn * u * tangent
    host, satellite = np.r_[y[:2], host_v], np.r_[y[:2], payload_v]
    momentum = payload * payload_v + retained * host_v - after_burn * pre_release_v
    return dict(host_state=host.tolist(), payload_state=satellite.tolist(),
                mass_before_kg=mass, mass_after_burn_kg=after_burn,
                retained_mass_kg=retained, propellant_used_kg=mass-after_burn,
                host_correction_m_s=float(h), relative_speed_m_s=u,
                target_a_m=target_a, achieved_a_m=elements(satellite)['a_m'],
                momentum_residual_kg_m_s=float(np.linalg.norm(momentum)),
                relative_speed_residual_m_s=float(np.linalg.norm(payload_v-host_v-u*tangent)))


def campaign(n, spacing, mission, interval, burn_limit, config=None):
    c = INPUTS if config is None else config
    if not isinstance(n, int) or n < 1 or not isinstance(burn_limit, int) or burn_limit < 0:
        raise ValueError('invalid manifest or burn count')
    positive(spacing, c['dry_mass_kg'], c['fuel_kg'], c['isp_s'], c['payload_kg'], c['altitude_km'])
    if not math.isfinite(c['reserve_kg']) or not 0 <= c['reserve_kg'] <= c['fuel_kg']:
        raise ValueError('invalid reserve')
    if mission not in INPUTS['missions']:
        raise ValueError('unknown mission')
    targets = ([RE + 460000.] * n if mission == 'COMMON_ENERGY' or n == 1
               else np.linspace(RE + 440000., RE + 480000., n).tolist())
    r = RE + c['altitude_km'] * 1000
    state = np.array([r, 0., 0., math.sqrt(MU/r)])
    mass = c['dry_mass_kg'] + c['fuel_kg'] + n*c['payload_kg']
    fuel, burns, events, stop = c['fuel_kg'], 0, [], None
    for i, target in enumerate(targets):
        try:
            if i:
                state = coast(state, spacing)
            event = release(state, mass, c['payload_kg'], max(0., fuel-c['reserve_kg']),
                            c['isp_s'], target, interval)
            next_burns = burns + int(abs(event['host_correction_m_s']) > BURN_EPS)
            if next_burns > burn_limit:
                stop = 'BURN_COUNT_LIMIT'
                break
        except ValueError as exc:
            stop = str(exc)
            break
        event.update(index=i+1, time_s=i*spacing)
        events.append(event)
        state = np.array(event['host_state'])
        mass = event['retained_mass_kg']
        fuel -= event['propellant_used_kg']
        burns = next_burns
    return dict(manifest=n, spacing_s=spacing, mission=mission, burn_limit=burn_limit,
                delivered=len(events), completed=len(events)==n, stopping_reason=stop,
                total_host_delta_v_m_s=sum(abs(e['host_correction_m_s']) for e in events),
                propellant_used_kg=c['fuel_kg']-fuel, fuel_remaining_kg=fuel,
                final_retained_mass_kg=mass, burn_count=burns,
                scheduled_duration_s=(n-1)*spacing, events=events)


def build():
    rows = []
    for mission, n, spacing, (name, interval), count in itertools.product(
            INPUTS['missions'], INPUTS['manifests'], INPUTS['spacing_s'],
            INPUTS['screens'].items(), INPUTS['burn_limits']):
        row = campaign(n, spacing, mission, interval, count)
        row['screen'] = name
        rows.append(row)
    paths = ['analysis/campaign_allocation.py', 'analysis/host_reference.py',
             'validation/P113_S2_campaign_allocation.md']
    return dict(study='P113-S2', status='ENERGY_TARGET_SCREEN_NOT_MISSION_FEASIBILITY',
                open_items=['P113', 'E5'], inputs=INPUTS,
                source_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                input_sha256=hashlib.sha256(json.dumps(INPUTS, sort_keys=True).encode()).hexdigest(),
                cases=rows)


def report(data):
    lines = ['# Sequential delivery: orbital energy and host resources', '',
             'Generated by `analysis/campaign_allocation.py`. Do not hand-edit.', '',
             '**P113 and E5 remain open. No mechanism or provider is selected.**', '',
             'This screen propagates the host between scheduled releases, solves burn mass loss',
             'and recoil together, and retains partial deliveries. Targets specify semi-major',
             'axis only, not complete destination states or circular orbits. The same placeholder',
             'installed dry mass is used for all screens. This is not a hardware mass comparison.', '',
             '[Frozen criteria](../validation/P113_S2_campaign_allocation.md) ·',
             '[Full event histories](../analysis/results/campaign_allocation.json) ·',
             '[Programme decisions](PROGRAMME_EXECUTION.md)', '',
             '![Campaign resource screen](../figures/campaign_allocation.svg)', '',
             '## Twelve payloads, 600 s spacing, at most twelve host corrections', '',
             'Assumed 300 kg dry host, 10 kg fuel, 2 kg protected reserve, 220 s Isp, 4 kg payloads.',
             'Every interval is hypothetical, including the 0.5 m/s lower limit. Even the fixed',
             '1 m/s comparator may choose prograde or retrograde release without a slew penalty.', '',
             '| Mission | Screen | Delivered | Host delta-v, m/s | Fuel used, kg | Corrections | Stop |',
             '|---|---|---:|---:|---:|---:|---|']
    for row in data['cases']:
        if row['manifest']==12 and row['spacing_s']==600 and row['burn_limit']==12:
            lines.append(f"| {row['mission']} | {row['screen']} | {row['delivered']}/12 | "
                         f"{row['total_host_delta_v_m_s']:.4f} | {row['propellant_used_kg']:.5f} | "
                         f"{row['burn_count']} | {row['stopping_reason'] or 'none'} |")
    lines += ['', 'Fuel and delta-v for incomplete cases cover only their delivered prefix.',
              'They cannot be ranked against complete deliveries as if the mission were equal.', '',
              '## What this calculation can decide', '',
              'It exposes the coupling between release authority, repeated host corrections,',
              'remaining manifest mass and assumed burn-count limits. Greedy minimum-current-burn',
              'selection is not global campaign optimisation. A larger interval can change the',
              'subsequent trajectory, so no monotonic campaign advantage is assumed.', '',
              'The sweep contains 180 cases: two energy missions, three manifests, two schedules,',
              'five speed screens and three correction-count limits. All failures remain in JSON.', '',
              '## What remains before an architecture decision', '',
              'Full target states and time windows, release-time optimisation, finite burns and',
              'minimum impulse, real restart/coast limits, attitude restoration, mechanism energy',
              'and consumables, payload dispersion, clearance/recontact, J2/drag and lifetime,',
              'complete installed mass/volume and common-mode failure exposure are omitted.',
              'The 120 km perigee guard only prevents propagating an unsuitable reference host;',
              'it is not a disposal, payload-orbit or collision-safety acceptance test.', '',
              'Both providers still need to supply interfaces. No common-stage mass credit or',
              'flight reliability follows from this resource screen. BOLLEY cage acceptance and',
              'Gen6 contact/trim problems remain independent of these hypothetical speed intervals.', '',
              '## Reproduce', '', '```bash', 'python3 analysis/campaign_allocation.py',
              'python3 analysis/campaign_allocation.py --check',
              'python3 -m pytest tests/test_campaign_allocation.py', '```', '']
    return '\n'.join(lines)


def figure(data):
    """Only complete, like-for-like energy-screen cases; no hardware ranking."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with plt.rc_context({'svg.hashsalt': 'P113-S2', 'font.family': 'DejaVu Sans'}):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
        colors = ['#566174', '#a76b1a', '#007d88', '#7854a4', '#be4b58']
        for ax, mission in zip(axes, INPUTS['missions']):
            for (name, _), color in zip(INPUTS['screens'].items(), colors):
                rows = [r for r in data['cases'] if r['mission']==mission
                        and r['spacing_s']==600 and r['burn_limit']==12 and r['screen']==name]
                ax.plot([r['manifest'] for r in rows],
                        [r['propellant_used_kg'] if r['completed'] else float('nan') for r in rows],
                        marker='o', label=name.replace('_', ' '), color=color, linewidth=1.7)
            ax.set_title(mission.replace('_', ' ').title(), fontsize=11)
            ax.set_xlabel('Payload count (4 kg each)')
            ax.set_xticks([1, 4, 12])
            ax.set_ylim(bottom=-.08)
            ax.grid(alpha=.18)
            ax.spines[['top', 'right']].set_visible(False)
        axes[0].text(.06, .13, 'Three larger screens coincide at zero.',
                     transform=axes[0].transAxes, fontsize=8, color='#555555')
        axes[0].set_ylabel('Host correction propellant (kg)')
        axes[1].legend(fontsize=8, loc='upper left')
        fig.suptitle('Sequential orbital-energy delivery | P113-S2', fontsize=14, x=.5, y=.97)
        fig.text(.5, .045, '600 s spacing; maximum 12 corrections; complete cases only. Assumed speed intervals.',
                 ha='center', fontsize=9)
        fig.text(.5, .008, 'Equal placeholder installation mass. Mechanism energy, attitude, clearance and full mission constraints excluded.',
                 ha='center', fontsize=8, color='#555555')
        fig.tight_layout(rect=[0, .08, 1, .93])
        stream = io.StringIO()
        fig.savefig(stream, format='svg', metadata={'Date': None})
        plt.close(fig)
        return '\n'.join(line.rstrip() for line in stream.getvalue().splitlines()) + '\n'


def outputs(data):
    return {'analysis/results/campaign_allocation.json': json.dumps(data, indent=2, sort_keys=True)+'\n',
            'docs/CAMPAIGN_ALLOCATION.md': report(data),
            'figures/campaign_allocation.svg': figure(data)}


def numerical_match(actual, expected, path=()):
    """Exact discrete evidence; field-specific SI tolerances below verification limits.

    Cartesian component reproducibility must not collapse near an axis crossing.
    See docs/MISSION_FRESHNESS_20260915.md for the observed runner disagreement.
    """
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            numerical_match(actual[k], value, path+(k,)) for k, value in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            numerical_match(a, b, path+(i,)) for i, (a, b) in enumerate(zip(actual, expected)))
    if isinstance(expected, float):
        atol = 1e-9
        if path and path[-1] == 'position_error_m':
            atol = 1e-5
        if path and path[-1] in ('velocity_error_m_s', 'first_burn_magnitude_m_s',
                                'second_burn_magnitude_m_s', 'total_host_delta_v_m_s',
                                'delta_v_m_s', 'host_correction_m_s'):
            atol = 1e-7
        if len(path) >= 2:
            field, index = path[-2:]
            if field in ('host_state', 'payload_state', 'initial_state', 'arrival_state', 'terminal_state'):
                atol = 1e-5 if index < 2 else 1e-7
            elif field in ('initial_correction_m_s', 'second_correction_m_s', 'relative_velocity_m_s'):
                atol = 1e-7
        return math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=atol)
    return actual == expected


def check_outputs(root, rendered):
    result_path = 'analysis/results/campaign_allocation.json'
    try:
        actual = json.loads((root/result_path).read_text())
        expected = json.loads(rendered[result_path])
    except (OSError, ValueError):
        return [p for p, content in rendered.items()
                if not (root/p).is_file() or (root/p).read_text() != content]
    # Inputs and source hashes remain exact. Only computed case numbers use tolerance.
    if not isinstance(actual, dict):
        return [result_path]
    metadata = {k: v for k, v in actual.items() if k != 'cases'}
    reference = {k: v for k, v in expected.items() if k != 'cases'}
    if (json.dumps(metadata, sort_keys=True) != json.dumps(reference, sort_keys=True)
            or not numerical_match(actual.get('cases'), expected['cases'])):
        return [result_path]
    # Presentations must exactly reproduce the accepted stored numerical payload.
    accepted = outputs(actual)
    return [p for p, content in accepted.items() if p != result_path and
            (not (root/p).is_file() or (root/p).read_text() != content)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = outputs(build())
    if args.check:
        stale = check_outputs(ROOT, rendered)
        print('campaign allocation: '+(', '.join(stale)+' STALE' if stale else 'current; P113/E5 open'))
        return int(bool(stale))
    for path, content in rendered.items():
        (ROOT/path).write_text(content)
    print('campaign allocation: wrote 180 cases; P113/E5 open')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
