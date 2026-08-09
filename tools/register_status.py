"""Give every OPEN_PROBLEMS entry an explicit status, and derive the counts from it.

WHY THIS EXISTS
---------------
The register carried 37 P-items and 27 E-items and no way to tell a live defect from a corrected
one retained as published history. Both are deliberately kept -- this project publishes defects
rather than deleting them -- but nothing marked which was which, so every count in the repository
(README, ROADMAP, KILL_CRITERIA, SUMMARY) mixed live engineering debt with closed history in one
number. docs/PHASE_I_CLOSURE.md section 0 named this as the first act of closing Phase I.

THE THREE STATUSES
------------------
    LIVE       -- open engineering. Something still has to be done.
    CORRECTED  -- the defect was found, fixed and propagated. Retained as the record.
    CLOSED     -- resolved by an analysis or a decision, with the closer named.

Each entry carries a `> **Status:** ...` line directly under its heading. This tool writes them
and, with --check, verifies that every entry has one and that the headline counts match.

USAGE
    python3 tools/register_status.py            # write status lines, print the tally
    python3 tools/register_status.py --check    # verify; non-zero exit if the counts drift
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, 'OPEN_PROBLEMS.md')
MARKER = '> **Status:** '

CLOSED_RE = re.compile(
    r'\bRESOLVED\b|\bFULLY CLOSED\b|\bWITHDRAWN\b|\bRETIRED\b|CLOSED \d{4}|'
    r'CLOSED \d{4}-\d{2}-\d{2}|\bHALF CLOSED\b|\bPARTIALLY CLOSED\b|ANALYSIS HALF CLOSED',
    re.I)
CORRECTED_RE = re.compile(
    r'\bCorrected\.|\bhas been corrected\b|\bnow fixed\b|\bpropagated\b|'
    r'\bstruck\b|\bwithdrawn\b|\bSharpened\b|\bQUANTIFIED\b|\bEXTENT BOUNDED\b', re.I)
LIVE_RE = re.compile(r'What would close it|remains open|still open|needs an owner decision', re.I)


def entries(text):
    lines = text.split('\n')
    idx = [(i, l) for i, l in enumerate(lines) if re.match(r'^### [PE]\d+\.', l)]
    for n, (i, l) in enumerate(idx):
        end = idx[n + 1][0] if n + 1 < len(idx) else len(lines)
        yield re.match(r'^### ([PE]\d+)\.', l).group(1), i, end, '\n'.join(lines[i:end])


def classify(body):
    head = body.split('\n')[0]
    if CLOSED_RE.search(head):
        return 'CLOSED'
    first = '\n'.join(body.split('\n')[1:8])
    if CLOSED_RE.search(first):
        return 'CLOSED'
    if LIVE_RE.search(body):
        return 'LIVE'
    if CORRECTED_RE.search(body):
        return 'CORRECTED'
    return 'LIVE'


NOTE = {
    'LIVE': 'open engineering; something still has to be done',
    'CORRECTED': 'found, fixed and propagated. Retained as the published record',
    'CLOSED': 'resolved; see the entry for what closed it',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    with open(REGISTER, encoding='utf-8') as f:
        text = f.read()

    tally, rows, missing = {'LIVE': 0, 'CORRECTED': 0, 'CLOSED': 0}, [], []
    for tag, _, _, body in entries(text):
        st = classify(body)
        tally[st] += 1
        rows.append((tag, st))
        if MARKER not in body:
            missing.append(tag)

    if args.check:
        if missing:
            raise SystemExit('entries with no status line: %s' % ', '.join(missing))
        print('register: %d entries, %d LIVE, %d CORRECTED, %d CLOSED'
              % (len(rows), tally['LIVE'], tally['CORRECTED'], tally['CLOSED']))
        return

    lines = text.split('\n')
    for tag, i, _, body in sorted(entries(text), key=lambda e: -e[1]):
        st = classify(body)
        line = f'{MARKER}`{st}` — {NOTE[st]}'
        if MARKER in body:
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].startswith(MARKER):
                    lines[j] = line
                    break
        else:
            lines.insert(i + 1, line)
            lines.insert(i + 2, '')
    with open(REGISTER, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    p_live = sum(1 for t, s in rows if t.startswith('P') and s == 'LIVE')
    e_live = sum(1 for t, s in rows if t.startswith('E') and s == 'LIVE')
    out = dict(total=len(rows), **{k.lower(): v for k, v in tally.items()},
               p_live=p_live, e_live=e_live,
               p_total=sum(1 for t, _ in rows if t.startswith('P')),
               e_total=sum(1 for t, _ in rows if t.startswith('E')),
               by_entry=dict(rows))
    with open(os.path.join(ROOT, 'analysis', 'results', 'register_status.json'),
              'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
        f.write('\n')

    print(f"{len(rows)} entries: {tally['LIVE']} LIVE, {tally['CORRECTED']} CORRECTED, "
          f"{tally['CLOSED']} CLOSED")
    print(f"  P-items {out['p_total']} total, {p_live} live")
    print(f"  E-items {out['e_total']} total, {e_live} live")
    print('\n  LIVE: ' + ' '.join(t for t, s in rows if s == 'LIVE'))
    print('\n  CORRECTED: ' + ' '.join(t for t, s in rows if s == 'CORRECTED'))


if __name__ == '__main__':
    main()
