"""P113-S4: bounded two-payload timing, order and first-speed enumeration."""
import argparse
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import root

import terminal_timing as single

ROOT = Path(__file__).resolve().parents[1]
campaign = single.campaign
INPUTS = dict(single.INPUTS, release_times_s=[600, 1200, 1800, 2400, 3000],
              coarse_times_s=[1200, 2400], manifest_targets=['phase_5km', 'phase_25km'],
              first_speed_policy='endpoints_midpoint_and_local', maximum_impulses=4)


def validate(order, times, interval, reserve):
    if sorted(order) != sorted(INPUTS['manifest_targets']):
        raise ValueError('two distinct reference targets required')
    if (len(times) != 2 or not all(math.isfinite(t) for t in times)
            or not 0 < times[0] < times[1] < INPUTS['terminal_time_s']):
        raise ValueError('ordered release times inside terminal window required')
    if len(interval) != 2:
        raise ValueError('two interval endpoints required')
    campaign.positive(*interval)
    if interval[0] > interval[1]:
        raise ValueError('ordered interval required')
    if not math.isfinite(reserve) or not 0 <= reserve <= INPUTS['fuel_kg']:
        raise ValueError('invalid reserve')


def shoot(start_state, target_position, duration):
    """Reuse S3's shooting formulation from an arbitrary retained host state."""
    start = campaign.state_check(start_state)
    desired = np.asarray(target_position, dtype=float)
    if desired.shape != (2,) or not np.all(np.isfinite(desired)):
        raise ValueError('finite planar target position required')
    campaign.positive(duration)
    arcs, searches = [], []
    for seed in INPUTS['seed_corrections_m_s']:
        record = dict(seed_m_s=seed, accepted=False)
        try:
            def residual(velocity):
                return campaign.coast(np.r_[start[:2], velocity], duration)[:2]-desired
            result = root(residual, start[2:]+seed, method='hybr', tol=1e-11)
            correction = np.asarray(result.x)-start[2:]
            error = float(np.linalg.norm(residual(result.x)))
            record.update(solver_success=bool(result.success), position_error_m=error)
            if not result.success or error > .001:
                record['reason'] = 'SEARCH_FAILED'
            elif np.linalg.norm(correction) > INPUTS['initial_burn_ceiling_m_s']:
                record['reason'] = 'TRANSFER_BURN_CEILING'
            else:
                record['accepted'] = True
                state = np.r_[start[:2], start[2:]+correction]
                if not any(np.linalg.norm(correction-np.array(a['correction_m_s'])) < 1e-5 for a in arcs):
                    arcs.append(dict(correction_m_s=correction.tolist(), initial_state=state.tolist(),
                                     arrival_state=campaign.coast(state, duration).tolist(),
                                     position_error_m=error))
        except (ValueError, FloatingPointError) as exc:
            record['reason'] = 'SEARCH_FAILED: '+str(exc)
        searches.append(record)
    return dict(start_state=start.tolist(), duration_s=duration, arcs=arcs, searches=searches)


def burn(mass, fuel, correction, reserve):
    dv = float(np.linalg.norm(correction))
    after = mass*math.exp(-dv/(INPUTS['isp_s']*single.G0))
    used = mass-after
    if fuel-used < reserve:
        raise ValueError('PROPELLANT_RESERVE_TRANSFER')
    return dict(magnitude_m_s=dv, mass_before_kg=mass, mass_after_kg=after,
                fuel_used_kg=used, fuel_remaining_kg=fuel-used)


def deliver(name, time, arc, mass, fuel, interval, reserve):
    transfer = burn(mass, fuel, arc['correction_m_s'], reserve)
    event = single.separate(arc['arrival_state'], single.target_state(name, time)[2:],
                            transfer['mass_after_kg'], transfer['fuel_remaining_kg']-reserve, interval)
    terminal = campaign.coast(event['payload_state'], INPUTS['terminal_time_s']-time)
    errors = single.terminal_errors(terminal, single.target_state(name, INPUTS['terminal_time_s']))
    return dict(target=name, time_s=time, transfer_burn=transfer, separation=event,
                terminal_state=terminal.tolist(), terminal_errors=errors,
                fuel_remaining_kg=transfer['fuel_remaining_kg']-event['second_fuel_kg'])


def speed_choices(arrival, name, time, mass, interval):
    lo, hi = interval
    d = float(np.linalg.norm(single.target_state(name, time)[2:]-np.asarray(arrival)[2:]))
    local = float(np.clip(d/(1-INPUTS['payload_kg']/mass), lo, hi))
    choices = sorted(set([float(lo), float(hi), float((lo+hi)/2), local]))
    return [(u, u == local) for u in choices]


def case(order, times, interval, reserve=None, first_solution=None):
    reserve = INPUTS['reserve_kg'] if reserve is None else reserve
    validate(order, times, interval, reserve)
    mass = INPUTS['dry_mass_kg']+INPUTS['fuel_kg']+2*INPUTS['payload_kg']
    solution = first_solution if first_solution is not None else shoot(
        single.initial(), single.target_state(order[0], times[0])[:2], times[0])
    candidates, second_transfers = [], []
    for first_index, arc in enumerate(solution['arcs']):
        try:
            initial_burn = burn(mass, INPUTS['fuel_kg'], arc['correction_m_s'], reserve)
        except ValueError as exc:
            candidates.append(dict(accepted=False, reason=str(exc), events=[], first_arc_index=first_index))
            continue
        for speed, is_local in speed_choices(arc['arrival_state'], order[0], times[0],
                                              initial_burn['mass_after_kg'], interval):
            base = dict(first_arc_index=first_index, first_speed_m_s=speed,
                        local_first_speed=is_local, accepted=False, events=[])
            try:
                first = deliver(order[0], times[0], arc, mass, INPUTS['fuel_kg'], [speed, speed], reserve)
            except ValueError as exc:
                candidates.append(dict(base, reason=str(exc)))
                continue
            base['events'] = [first]
            if not first['terminal_errors']['accepted']:
                candidates.append(dict(base, reason='FIRST_TERMINAL_STATE_MISS'))
                continue
            retained = first['separation']
            second = shoot(retained['host_state'], single.target_state(order[1], times[1])[:2], times[1]-times[0])
            transfer_index = len(second_transfers)
            second_transfers.append(dict(first_arc_index=first_index, first_speed_m_s=speed, **second))
            base['second_transfer_index'] = transfer_index
            if not second['arcs']:
                candidates.append(dict(base, reason='SECOND_SEARCH_FAILED'))
            for second_index, second_arc in enumerate(second['arcs']):
                candidate = dict(base, second_arc_index=second_index)
                try:
                    last = deliver(order[1], times[1], second_arc, retained['retained_mass_kg'],
                                   first['fuel_remaining_kg'], interval, reserve)
                    candidate['events'] = [first, last]
                    ok = last['terminal_errors']['accepted']
                    candidate.update(accepted=ok, reason=None if ok else 'SECOND_TERMINAL_STATE_MISS',
                                     total_fuel_kg=INPUTS['fuel_kg']-last['fuel_remaining_kg'],
                                     total_host_delta_v_m_s=sum(e['transfer_burn']['magnitude_m_s']+
                                         e['separation']['second_burn_magnitude_m_s'] for e in candidate['events']))
                except ValueError as exc:
                    candidate['reason'] = str(exc)
                candidates.append(candidate)
    good = [i for i, c in enumerate(candidates) if c['accepted']]
    best = min(good, key=lambda i:(candidates[i]['total_fuel_kg'], i)) if good else None
    return dict(order=list(order), release_times_s=list(times), accepted=bool(good),
                reason=None if good else ('FIRST_SEARCH_FAILED' if not solution['arcs'] else 'CANDIDATES_REJECTED'),
                first_transfer=solution, second_transfers=second_transfers,
                candidates=candidates, best_candidate_index=best)


def selections(rows):
    selected = []
    orders = ['either']+['then'.join(o) for o in itertools.permutations(INPUTS['manifest_targets'])]
    for screen, grid, policy, order in itertools.product(INPUTS['screens'], ['coarse', 'fine'],
                                                         ['enumerated', 'local_only'], orders):
        choices = []
        for row_index, row in enumerate(rows):
            if row['screen'] != screen or (order != 'either' and 'then'.join(row['order']) != order):
                continue
            if grid == 'coarse' and not all(t in INPUTS['coarse_times_s'] for t in row['release_times_s']):
                continue
            for candidate_index, c in enumerate(row['candidates']):
                if c['accepted'] and (policy != 'local_only' or c['local_first_speed']):
                    choices.append((c['total_fuel_kg'], *row['release_times_s'], tuple(row['order']),
                                    row_index, candidate_index))
        winner = min(choices) if choices else None
        selected.append(dict(screen=screen, grid=grid, policy=policy, order=order,
                             status='BEST_TESTED' if winner else 'NO_ACCEPTED_SEARCH_RESULT',
                             fuel_kg=winner[0] if winner else None,
                             case_index=winner[-2] if winner else None,
                             candidate_index=winner[-1] if winner else None))
    return selected


def build():
    rows, first_cache = [], {}
    for order in itertools.permutations(INPUTS['manifest_targets']):
        for times in itertools.combinations(INPUTS['release_times_s'], 2):
            key = (order[0], times[0])
            if key not in first_cache:
                first_cache[key] = shoot(single.initial(), single.target_state(order[0], times[0])[:2], times[0])
            for screen, interval in INPUTS['screens'].items():
                rows.append(dict(screen=screen, **case(order, times, interval, first_solution=first_cache[key])))
    paths = ['analysis/manifest_timing.py', 'analysis/terminal_timing.py',
             'analysis/campaign_allocation.py', 'analysis/host_reference.py',
             'validation/P113_S4_manifest_timing.md']
    return dict(study='P113-S4', status='TWO_PAYLOAD_BOUNDED_SEARCH', open_items=['P113', 'E5'],
                inputs=INPUTS, source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                cases=rows, selections=selections(rows))


def report(data):
    lines = ['# Two-payload terminal-state campaign', '',
             'Generated by `analysis/manifest_timing.py`. Do not hand-edit.', '',
             '**P113/E5 remain open. These are best tested campaigns, not global optima or hardware rankings.**', '',
             'Two 4 kg payloads share one 300 kg dry host with 10 kg fuel and a 2 kg reserve.',
             'Both must reach prescribed 450 km circular-orbit states, 5 km and 25 km ahead',
             'of the reference host at 3600 s. Acceptance tests position AND velocity.', '',
             '[Frozen criteria](../validation/P113_S4_manifest_timing.md) ·',
             '[Every case and search](../analysis/results/manifest_timing.json) ·',
             '[Programme](PROGRAMME_EXECUTION.md)', '',
             '![Shared-host campaign comparison](../figures/manifest_timing.svg)', '',
             '## Best tested campaign on the fine grid', '',
             '| Assumed screen | Fuel, kg | First target | Release times, s | First speed, m/s | Local-only fuel, kg |',
             '|---|---:|---|---|---:|---:|']
    for screen in INPUTS['screens']:
        group = [s for s in data['selections'] if s['screen']==screen and s['grid']=='fine' and s['order']=='either']
        chosen = next(s for s in group if s['policy']=='enumerated')
        local = next(s for s in group if s['policy']=='local_only')
        if chosen['case_index'] is None:
            lines.append(f'| {screen} | No accepted search | | | | |')
            continue
        row = data['cases'][chosen['case_index']]
        c = row['candidates'][chosen['candidate_index']]
        local_text = 'none' if local['fuel_kg'] is None else f"{local['fuel_kg']:.6f}"
        lines.append(f"| {screen} | {chosen['fuel_kg']:.6f} | {row['order'][0]} | {row['release_times_s']} | "
                     f"{c['first_speed_m_s']:.6f} | {local_text} |")
    accepted = sum(r['accepted'] for r in data['cases'])
    lines += ['', f'{accepted} of {len(data["cases"])} schedule/order/screen cases have an accepted campaign.',
              'Failed searches and interrupted deliveries remain in the JSON; missing roots are not proofs of infeasibility.', '',
              '## Controls and interpretation', '',
              'Each comparator receives both target orders and the same increasing release-time pairs',
              'from 600, 1200, 1800, 2400 and 3000 s. Coarse selection uses 1200 and 2400 s.',
              'For each first arc the speed search contains endpoints, midpoint and the locally',
              'fuel-minimizing speed. The local-only column restricts that same search to the last choice.',
              'The second transfer begins with the actual retained host state and mass after the first release.', '',
              'Up to four ideal impulses are allowed: initial transfer, first pre-release correction,',
              'post-first-release transfer and final pre-release correction. The two impulses around',
              'the first release are charged separately and act on different retained masses.',
              'No clearing time, plume exclusion or attitude recovery is represented.', '',
              'An accepted full campaign is stronger evidence than two independently initialized',
              'deliveries, but these controls are still an idealized screen. Installation mass is the',
              'same placeholder for all candidates. No mechanism energy or qualification claim follows.',
              'The release intervals, including the 0.5 m/s minimum, remain hypothetical.', '',
              'A selected time at 600 or 3000 s, or an adjacent pair, may be constrained by the grid.',
              'Equal coarse/fine values do not establish convergence. Discrete first-speed grids differ',
              'between intervals; an apparent reversal is not proof that less available authority is better.',
              'All fixed-order, coarse/fine and local/enumerated selections are retained in the JSON.', '',
              '## Next decisions', '',
              'Do not add more payloads merely to multiply cases. First quantify the effect of required',
              'clearing/settling intervals, release/navigation errors and installed burden. Compare',
              'independent bays, banks and the shared path with explicit failure consequences.',
              'Those constraints can change the ranking and still govern mechanism selection.', '',
              '## Reproduce', '', '```bash', 'python3 analysis/manifest_timing.py',
              'python3 analysis/manifest_timing.py --check', 'python3 -m pytest tests/test_manifest_timing.py', '```', '']
    return '\n'.join(lines)


def figure(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with plt.rc_context({'svg.hashsalt':'P113-S4', 'font.family':'DejaVu Sans'}):
        fig, ax = plt.subplots(figsize=(9, 4.8))
        labels = list(INPUTS['screens'])
        for offset, policy, color in [(-.18, 'local_only', '#657386'), (.18, 'enumerated', '#007d88')]:
            values = [next(s['fuel_kg'] for s in data['selections'] if s['screen']==screen
                           and s['grid']=='fine' and s['order']=='either' and s['policy']==policy) for screen in labels]
            ax.bar(np.arange(len(labels))+offset, [v if v is not None else float('nan') for v in values],
                   width=.34, color=color, label=policy.replace('_', ' '))
        ax.set_xticks(np.arange(len(labels)), [s.replace('_', '\n') for s in labels])
        ax.set_ylabel('Host propellant for both deliveries (kg)')
        ax.set_title('Shared host, two complete target states | P113-S4')
        ax.legend(frameon=False)
        ax.grid(axis='y', alpha=.2)
        ax.spines[['top', 'right']].set_visible(False)
        fig.text(.5, .035, 'Best tested grid points. Assumed intervals; no installation, settling or mechanism-energy cost.',
                 ha='center', fontsize=9)
        fig.tight_layout(rect=[0, .07, 1, 1])
        stream = io.StringIO()
        fig.savefig(stream, format='svg', metadata={'Date':None})
        plt.close(fig)
        return '\n'.join(line.rstrip() for line in stream.getvalue().splitlines())+'\n'


def outputs(data):
    return {'analysis/results/manifest_timing.json':json.dumps(data, sort_keys=True, indent=2)+'\n',
            'docs/MANIFEST_TIMING.md':report(data), 'figures/manifest_timing.svg':figure(data)}


def check_outputs(directory, rendered):
    path = 'analysis/results/manifest_timing.json'
    try:
        actual, expected = json.loads((directory/path).read_text()), json.loads(rendered[path])
    except (OSError, ValueError):
        return [path]
    meta = ['study', 'status', 'open_items', 'inputs', 'source_sha256']
    if (not isinstance(actual, dict) or set(actual)!=set(expected)
            or any(json.dumps(actual[k], sort_keys=True)!=json.dumps(expected[k], sort_keys=True) for k in meta)
            or any(not campaign.numerical_match(actual[k], expected[k]) for k in ['cases', 'selections'])):
        return [path]
    return [p for p, content in outputs(actual).items() if p!=path and
            (not (directory/p).is_file() or (directory/p).read_text()!=content)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = outputs(build())
    if args.check:
        stale = check_outputs(ROOT, rendered)
        print('manifest timing: '+('STALE '+', '.join(stale) if stale else 'current; P113/E5 open'))
        return int(bool(stale))
    for path, content in rendered.items():
        (ROOT/path).write_text(content)
    print('manifest timing: wrote 100 cases; P113/E5 open')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
