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

Each entry carries a `> **Status:** ...` line directly under its heading. This tool writes them,
and derives analysis/results/register_status.json from them.

--check verifies two things: that every entry has a status line, and that the committed JSON is
what a fresh run would write. The second half did not exist until 2026-08-16 -- --check returned
before reaching the JSON at all -- so the committed result went one entry stale and nothing
reported it. See P65.

USAGE
    python3 tools/register_status.py            # write status lines and the JSON, print the tally
    python3 tools/register_status.py --check    # verify; non-zero exit if either drifts
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, 'OPEN_PROBLEMS.md')
RESULT = os.path.join(ROOT, 'analysis', 'results', 'register_status.json')
MARKER = '> **Status:** '

# The leading (?<!-) on each word matters. `\bRESOLVED\b` matches inside "depth-resolved",
# so an entry whose first lines cite ADR-030 by filename was classified CLOSED on the strength
# of a hyphenated adjective in a link target. Two entries were silently restatused that way on
# 2026-08-14 before it was noticed. A word used as half of a compound is not a status keyword.
CLOSED_RE = re.compile(
    r'(?<!-)\bRESOLVED\b|\bFULLY CLOSED\b|(?<!-)\bWITHDRAWN\b|(?<!-)\bRETIRED\b|'
    r'CLOSED \d{4}|CLOSED \d{4}-\d{2}-\d{2}|\bHALF CLOSED\b|\bPARTIALLY CLOSED\b|'
    r'ANALYSIS HALF CLOSED',
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
    # Drop the tool's own Status line before reading anything. It sits inside the window the
    # keyword scan looks at, and the note it carries ("resolved; see the entry for what closed
    # it") contains a status keyword -- so a single misclassification used to write a line that
    # then re-justified itself on every later run. A classifier must not read its own output.
    body = '\n'.join(l for l in body.split('\n') if not l.startswith(MARKER))
    head = body.split('\n')[0]
    # Read the status from the STATUS SUFFIX, not from anywhere in the heading. An entry is
    # titled "<what is wrong>: <STATUS>, <date>", so a status keyword used as an ordinary word
    # in the title is not a status. P69 -- "Mass parity ... is withdrawn: HIGH, NEW" -- was
    # classified CLOSED because the claim was withdrawn, not the defect. Same failure as the
    # RESOLVED/depth-resolved match: keying on a word wherever it appears rather than where
    # status actually lives. P70.
    if CLOSED_RE.search(head.rsplit(':', 1)[-1]):
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


def payload(rows, tally):
    """The generated result, built in one place so --check can compare against it."""
    return dict(total=len(rows), **{k.lower(): v for k, v in tally.items()},
                p_live=sum(1 for t, s in rows if t.startswith('P') and s == 'LIVE'),
                e_live=sum(1 for t, s in rows if t.startswith('E') and s == 'LIVE'),
                p_total=sum(1 for t, _ in rows if t.startswith('P')),
                e_total=sum(1 for t, _ in rows if t.startswith('E')),
                by_entry=dict(rows))


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
        fresh = payload(rows, tally)
        try:
            with open(RESULT, encoding='utf-8') as f:
                committed = json.load(f)
        except FileNotFoundError:
            raise SystemExit('%s does not exist; run without --check' % RESULT)
        if committed != fresh:
            drift = sorted(k for k in set(committed) | set(fresh)
                           if committed.get(k) != fresh.get(k))
            raise SystemExit(
                'register_status.json is stale in %s; run without --check'
                % ', '.join(drift))
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

    out = payload(rows, tally)
    p_live, e_live = out['p_live'], out['e_live']
    with open(RESULT, 'w', encoding='utf-8') as f:
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
