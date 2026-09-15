"""P113-S3: single-payload terminal-state timing benchmark; no architecture verdict."""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path

import campaign_allocation as campaign
import numpy as np
from host_reference import G0, MU, RE
from scipy.optimize import brentq, root

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {'terminal_time_s': 3600, 'release_times_s': list(range(150, 3001, 150)),
              'seed_corrections_m_s': [[0, 0], [20, 0], [-20, 0]],
              'initial_altitude_km': 450, 'initial_burn_ceiling_m_s': 100,
              'dry_mass_kg': 300, 'fuel_kg': 10, 'reserve_kg': 2, 'payload_kg': 4, 'isp_s': 220,
              'position_band_m': 10, 'velocity_band_m_s': .01,
              'targets': {'phase_5km': [450, 5], 'phase_25km': [450, 25],
                       'higher_circle': [460, 0]}, 'screens': campaign.INPUTS['screens']}


def initial():
    r = RE + INPUTS['initial_altitude_km'] * 1000
    return np.array([r, 0., 0., math.sqrt(MU/r)])


def target_state(name, time):
    if name not in INPUTS['targets'] or not math.isfinite(time) or time < 0:
        raise ValueError('invalid target or time')
    alt, arc = INPUTS['targets'][name]
    r0, r = initial()[0], RE+alt*1000
    n = math.sqrt(MU/r**3)
    terminal_angle = math.sqrt(MU/r0**3)*INPUTS['terminal_time_s']+arc*1000/r0
    angle = terminal_angle+n*(time-INPUTS['terminal_time_s'])
    return np.array([r*math.cos(angle), r*math.sin(angle),
                     -n*r*math.sin(angle), n*r*math.cos(angle)])


def shoot(target_position, time):
    desired = np.asarray(target_position, dtype=float)
    if desired.shape != (2,) or not np.all(np.isfinite(desired)):
        raise ValueError('finite planar target position required')
    campaign.positive(time)
    start = initial()
    arcs, searches = [], []
    for seed in INPUTS['seed_corrections_m_s']:
        record = {'seed_m_s': seed, 'accepted': False}
        try:
            def residual(velocity):
                return campaign.coast(np.r_[start[:2], velocity], time)[:2]-desired
            # Solve in orbital velocity coordinates: relative-step termination in a
            # near-zero correction variable spuriously rejected the circular control.
            result = root(residual, start[2:]+seed, method='hybr', tol=1e-11)
            kick = np.asarray(result.x)-start[2:]
            error = float(np.linalg.norm(residual(result.x)))
            record.update(solver_success=bool(result.success), position_error_m=error)
            if not result.success or error > .001:
                record['reason'] = 'SEARCH_FAILED'
            elif np.linalg.norm(kick) > INPUTS['initial_burn_ceiling_m_s']:
                record['reason'] = 'INITIAL_BURN_CEILING'
            else:
                state = np.r_[start[:2], start[2:]+kick]
                arrival = campaign.coast(state, time)
                record['accepted'] = True
                if not any(np.linalg.norm(kick-np.array(a['initial_correction_m_s'])) < 1e-5 for a in arcs):
                    arcs.append({'initial_correction_m_s': kick.tolist(),
                                     'initial_state': state.tolist(), 'arrival_state': arrival.tolist(),
                                     'position_error_m': error})
        except (ValueError, FloatingPointError) as exc:
            record['reason'] = 'SEARCH_FAILED: '+str(exc)
        searches.append(record)
    return {'arcs': arcs, 'searches': searches}


def separate(arrival, target_velocity, mass, available_fuel, interval):
    state = campaign.state_check(arrival)
    target = np.asarray(target_velocity, dtype=float)
    if target.shape != (2,) or not np.all(np.isfinite(target)):
        raise ValueError('finite target velocity required')
    lo, hi = interval
    campaign.positive(mass, lo, hi)
    m, ve = INPUTS['payload_kg'], INPUTS['isp_s']*G0
    if (hi < lo or not math.isfinite(available_fuel) or available_fuel < 0
            or mass-available_fuel <= m):
        raise ValueError('invalid mass, fuel or interval')
    delta = target-state[2:]
    d = float(np.linalg.norm(delta))
    axis = delta/d if d > 1e-12 else np.array([-state[1], state[0]])/np.linalg.norm(state[:2])
    u = float(np.clip(d/(1-m/mass), lo, hi))

    def residual(h):
        post = mass*math.exp(-abs(h)/ve)
        return h+(1-m/post)*u-d

    limit = ve*math.log(mass/(mass-available_fuel))
    if abs(residual(0)) <= 1e-11:
        h = 0.
    elif residual(-limit) > 0 or residual(limit) < 0:
        raise ValueError('PROPELLANT_RESERVE')
    else:
        h = brentq(residual, -limit, limit, xtol=1e-12)
    post = mass*math.exp(-abs(h)/ve)
    before_release = state[2:]+h*axis
    vp = before_release+(1-m/post)*u*axis
    vh = before_release-m/post*u*axis
    return {'second_correction_m_s': (h*axis).tolist(), 'relative_velocity_m_s': (u*axis).tolist(),
                'second_burn_magnitude_m_s': abs(h), 'mass_before_second_kg': mass,
                'mass_after_second_kg': post, 'retained_mass_kg': post-m,
                'second_fuel_kg': mass-post,
                'payload_state': np.r_[state[:2], vp].tolist(), 'host_state': np.r_[state[:2], vh].tolist(),
                'momentum_residual_kg_m_s': float(np.linalg.norm(m*vp+(post-m)*vh-post*before_release)),
                'relative_velocity_residual_m_s': float(np.linalg.norm(vp-vh-u*axis))}


def terminal_errors(state, target):
    y, t = campaign.state_check(state), campaign.state_check(target)
    pos, vel = float(np.linalg.norm(y[:2]-t[:2])), float(np.linalg.norm(y[2:]-t[2:]))
    return {'position_error_m': pos, 'velocity_error_m_s': vel,
                'accepted': pos <= INPUTS['position_band_m'] and vel <= INPUTS['velocity_band_m_s']}


def evaluate(name, time, arc, interval):
    W = INPUTS['dry_mass_kg']+INPUTS['fuel_kg']+INPUTS['payload_kg']
    first_dv = float(np.linalg.norm(arc['initial_correction_m_s']))
    after_first = W*math.exp(-first_dv/(INPUTS['isp_s']*G0))
    remaining = after_first-INPUTS['dry_mass_kg']-INPUTS['payload_kg']
    if remaining < INPUTS['reserve_kg']:
        return {'accepted': False, 'reason': 'PROPELLANT_RESERVE_FIRST_BURN'}
    try:
        event = separate(arc['arrival_state'], target_state(name, time)[2:], after_first,
                         remaining-INPUTS['reserve_kg'], interval)
        terminal = campaign.coast(event['payload_state'], INPUTS['terminal_time_s']-time)
        errors = terminal_errors(terminal, target_state(name, INPUTS['terminal_time_s']))
        total_fuel = W-event['mass_after_second_kg']
        return dict(**errors, reason=None if errors['accepted'] else 'TERMINAL_STATE_MISS',
                    first_burn_magnitude_m_s=first_dv, total_fuel_kg=total_fuel,
                    total_host_delta_v_m_s=first_dv+event['second_burn_magnitude_m_s'],
                    terminal_state=terminal.tolist(), event=event)
    except ValueError as exc:
        return {'accepted': False, 'reason': str(exc)}


def selections(rows):
    result = []
    for target in INPUTS['targets']:
        for screen in INPUTS['screens']:
            for grid in ['coarse_300s', 'fine_150s']:
                choices = [r for r in rows if r['target']==target and r['screen']==screen
                           and r['accepted'] and (grid=='fine_150s' or r['release_time_s'] % 300==0)]
                winner = min(choices, key=lambda r: (r['best']['total_fuel_kg'], r['release_time_s'])) if choices else None
                result.append({'target': target, 'screen': screen, 'grid': grid,
                                   'status': 'BEST_TESTED' if winner else 'NO_ACCEPTED_SEARCH_RESULT',
                                   'release_time_s': winner['release_time_s'] if winner else None,
                                   'fuel_kg': winner['best']['total_fuel_kg'] if winner else None,
                                   'delta_v_m_s': winner['best']['total_host_delta_v_m_s'] if winner else None})
    return result


def build():
    rows, transfers = [], []
    for name in INPUTS['targets']:
        for time in INPUTS['release_times_s']:
            solution = shoot(target_state(name, time)[:2], time)
            transfers.append(dict(target=name, release_time_s=time, **solution))
            for screen, interval in INPUTS['screens'].items():
                evaluated = [dict(arc_index=i, **evaluate(name, time, a, interval))
                             for i, a in enumerate(solution['arcs'])]
                good = [e for e in evaluated if e['accepted']]
                best = min(good, key=lambda e: e['total_fuel_kg']) if good else None
                rows.append({'target': name, 'release_time_s': time, 'screen': screen,
                                 'accepted': bool(good), 'best': best, 'candidates': evaluated,
                                 'reason': None if good else ('SEARCH_FAILED' if not evaluated else 'CANDIDATES_REJECTED')})
    paths = ['analysis/terminal_timing.py', 'analysis/campaign_allocation.py',
             'analysis/host_reference.py', 'validation/P113_S3_terminal_timing.md']
    return {'study': 'P113-S3', 'status': 'SINGLE_PAYLOAD_BOUNDED_SEARCH', 'open_items': ['P113', 'E5'],
                'inputs': INPUTS, 'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                'transfers': transfers, 'cases': rows, 'selections': selections(rows)}


def report(data):
    lines = ['# Terminal-state delivery and release timing', '',
             'Generated by `analysis/terminal_timing.py`. Do not hand-edit.', '',
             '**P113/E5 remain open. Best tested timing is not a global optimum or selected mechanism.**', '',
             'One 4 kg payload must reach a prescribed circular-orbit position AND velocity at 3600 s.',
             'All five hypothetical speed screens receive the same host controls, target states and',
             'release-time grid. The host can burn at time zero and immediately before release.',
             'Transfer arcs come from a bounded seed search; failed searches do not prove infeasibility.', '',
             '[Criteria](../validation/P113_S3_terminal_timing.md) ·',
             '[All searches and events](../analysis/results/terminal_timing.json) ·',
             '[Programme decisions](PROGRAMME_EXECUTION.md)', '',
             '![Timing and host propellant](../figures/terminal_timing.svg)', '',
             '## Best accepted point on each timing grid', '',
             '300 kg assumed dry host including equal placeholder installation, 10 kg fuel,',
             '2 kg reserve, 220 s Isp. No mechanism energy, slew or settling penalty is charged.',
             'Every speed range is hypothetical, including the 0.5 m/s lower limit.', '',
             '| Target | Screen | Coarse fuel, kg | Fine fuel, kg | Fine release, s | Status |',
             '|---|---|---:|---:|---:|---|']
    for name in INPUTS['targets']:
        for screen in INPUTS['screens']:
            pair = [s for s in data['selections'] if s['target']==name and s['screen']==screen]
            coarse, fine = pair
            fmt = lambda x: '—' if x is None else f'{x:.5f}'
            lines.append(f"| {name} | {screen} | {fmt(coarse['fuel_kg'])} | {fmt(fine['fuel_kg'])} | "
                         f"{fine['release_time_s'] if fine['release_time_s'] is not None else '—'} | {fine['status']} |")
    lines += ['', 'The two phase targets are 5 km and 25 km ahead along the 450 km reference circle.',
              'The higher-circle target is 460 km at the unperturbed host terminal angle.',
              'Out-of-plane position/velocity are identically zero. This is not plane-change capability.', '',
              '## Interpretation limits', '',
              'Unlike the preceding energy-only screen, accepted payloads meet both Cartesian',
              'position and velocity bands at the same epoch. This does not establish an operational',
              'rendezvous, clearance, collision avoidance, or compatibility with an actual launcher.',
              'The timing search and initial host burn are available to every comparator.', '',
              'The fine grid contains the entire coarse grid. An equal best value establishes no',
              'continuous-time convergence. A best point at 3000 s is on the search boundary,',
              'not a bracketed optimum. Missing branches, narrow feasible windows, finite burns',
              'and different manoeuvre schedules may change the answer. No reliability, installed',
              'mass advantage, multi-payload optimum or flight readiness follows from fuel alone.', '',
              '## Next decision', '',
              'Use these terminal-state requirements to define a bounded multi-payload scheduling',
              'problem, then add navigation/release uncertainty, attitude recovery, installed mass',
              'and independent-bank versus common-path failure exposure. Keep conventional controls.', '',
              '## Reproduce', '', '```bash', 'python3 analysis/terminal_timing.py',
              'python3 analysis/terminal_timing.py --check',
              'python3 -m pytest tests/test_terminal_timing.py', '```', '']
    return '\n'.join(lines)


def figure(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with plt.rc_context({'svg.hashsalt': 'P113-S3', 'font.family': 'DejaVu Sans'}):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.7), sharey=True)
        colors = ['#566174', '#a76b1a', '#007d88', '#7854a4', '#be4b58']
        for ax, name in zip(axes, INPUTS['targets']):
            for screen, color in zip(INPUTS['screens'], colors):
                rows = [r for r in data['cases'] if r['target']==name and r['screen']==screen]
                ax.plot([r['release_time_s'] for r in rows],
                        [r['best']['total_fuel_kg'] if r['accepted'] else float('nan') for r in rows],
                        label=screen.replace('_', ' '), color=color, linewidth=1.5,
                        marker='o', markersize=3, markevery=4)
            ax.set_title(name.replace('_', ' '), fontsize=11)
            ax.set_xlabel('Release time (s)')
            ax.set_xticks([150, 1500, 3000])
            ax.set_ylim(bottom=0)
            ax.grid(alpha=.2)
            ax.spines[['top', 'right']].set_visible(False)
        axes[0].set_ylabel('Total host propellant (kg)')
        fig.suptitle('Same terminal state, same timing search | P113-S3', fontsize=14, y=.98)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5,.09), ncol=5, fontsize=9)
        fig.text(.5, .05, 'Successful candidates only; gaps are rejected or unfound arcs. Coincident curves share a result.', ha='center', fontsize=9)
        fig.text(.5, .012, 'Assumed speed intervals and ideal host control. No installation, attitude or mechanism-energy comparison.', ha='center', fontsize=9, color='#555555')
        fig.tight_layout(rect=[0, .18, 1, .94])
        stream = io.StringIO()
        fig.savefig(stream, format='svg', metadata={'Date': None})
        plt.close(fig)
        return '\n'.join(line.rstrip() for line in stream.getvalue().splitlines())+'\n'


def outputs(data):
    return {'analysis/results/terminal_timing.json': json.dumps(data, sort_keys=True, indent=2)+'\n',
            'docs/TERMINAL_TIMING.md': report(data),
            'figures/terminal_timing.svg': figure(data)}


def check_outputs(directory, rendered):
    path = 'analysis/results/terminal_timing.json'
    try:
        actual, expected = json.loads((directory/path).read_text()), json.loads(rendered[path])
    except (OSError, ValueError):
        return [p for p, text in rendered.items() if not (directory/p).is_file() or (directory/p).read_text()!=text]
    if not isinstance(actual, dict):
        return [path]
    meta = ['study', 'status', 'open_items', 'inputs', 'source_sha256']
    if (set(actual)!=set(expected) or any(json.dumps(actual[k], sort_keys=True)!=json.dumps(expected[k], sort_keys=True) for k in meta)
            or any(not campaign.numerical_match(actual[k], expected[k]) for k in ['transfers', 'cases', 'selections'])):
        return [path]
    accepted = outputs(actual)
    return [p for p, content in accepted.items() if p != path and
            (not (directory/p).is_file() or (directory/p).read_text()!=content)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = outputs(build())
    if args.check:
        stale = check_outputs(ROOT, rendered)
        print('terminal timing: '+('STALE '+', '.join(stale) if stale else 'current; P113/E5 open'))
        return int(bool(stale))
    for path, text in rendered.items():
        (ROOT/path).write_text(text)
    print('terminal timing: wrote 300 rows; P113/E5 open')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
