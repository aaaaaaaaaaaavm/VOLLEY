"""Classify what is left, and refuse to call it hardware when it is arithmetic.

WHY THIS EXISTS
---------------
The programme goal is COMPUTATIONAL CLOSURE: the state in which no remaining question's honest
next step is "more computation". That is a claim about every live entry in the register at once,
and a claim like that decays the moment it is written unless something checks it.

The failure mode this guards is specific and tempting: relabelling an unsolved calculation as
"needs hardware" so the closure count reaches zero. A gate cannot read intent, so it reads the
words -- an entry classified HARDWARE whose next step says "model", "simulate", "compute" or
"select from public data" is caught and named.

THE CLASSIFICATION
------------------
Every LIVE entry in OPEN_PROBLEMS.md carries, under its Status line:

    > **Scope:** `GEN6` · **Next step:** `HARDWARE` - measure the seal friction

Scope is GEN6, GEN5 or PROGRAMME. Closure is counted over GEN6 only, because Gen5 is a frozen
baseline and reclassifying its history to shrink the number would be the same dishonesty in a
different place. Classes:

    COMPUTATION   model, simulate, optimise, FEA, CFD, Monte Carlo, CAD, a standards comparison,
                  a public-data literature check, or selecting a component from published data
    HARDWARE      measure, manufacture, qualify, test
    HOST_DATA     non-public launch-provider or host-stage interface data
    FLIGHT_OPS    flight or operational data that does not exist until something flies
    DECISION      a human programme decision that no analysis settles

    python3 tools/check_computational_closure.py
    python3 tools/check_computational_closure.py --closed   # also require GEN6 COMPUTATION == 0
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import register_status as rs                                        # noqa: E402

CLASSES = ("COMPUTATION", "HARDWARE", "HOST_DATA", "FLIGHT_OPS", "DECISION")
SCOPES = ("GEN6", "GEN5", "PROGRAMME")
MARK = re.compile(r'^> \*\*Scope:\*\* `(\w+)` · \*\*Next step:\*\* `(\w+)` — (.+)$', re.M)

# Words that describe computation. A non-COMPUTATION entry whose next step uses one is either
# misclassified or badly worded, and either way it must not be counted as closed.
COMPUTE_WORDS = re.compile(
    r'\b(model|models|modelled|simulat\w*|comput\w*|calculat\w*|optimis\w*|optimiz\w*|'
    r'FEA|CFD|Monte Carlo|sweep|swept|CAD|analys\w*|analyz\w*|re-?run|design the|'
    r'select .*public|from public data|literature)\b', re.I)

DOC = os.path.join(ROOT, "docs", "COMPUTATIONAL_CLOSURE.md")


def scan():
    txt = open(os.path.join(ROOT, "OPEN_PROBLEMS.md"), encoding="utf-8").read()
    rows, problems = [], []
    for tag, i, end, body in rs.entries(txt):
        if rs.classify(body) != "LIVE":
            if MARK.search(body):
                problems.append(f"{tag}: carries a next-step class but is not LIVE. "
                                f"A closed entry has no next step")
            continue
        m = MARK.search(body)
        if not m:
            problems.append(f"{tag}: LIVE with no `**Scope:**`/`**Next step:**` line. "
                            f"Every live entry must say what would actually move it")
            continue
        scope, cls, nxt = m.group(1), m.group(2), m.group(3).strip()
        if scope not in SCOPES:
            problems.append(f"{tag}: scope `{scope}` is not one of {SCOPES}")
        if cls not in CLASSES:
            problems.append(f"{tag}: class `{cls}` is not one of {CLASSES}")
        if cls in ("HARDWARE", "HOST_DATA", "FLIGHT_OPS"):
            hit = COMPUTE_WORDS.search(nxt)
            if hit:
                problems.append(f"{tag}: classified {cls} but its next step says "
                                f"\"{hit.group(0)}\" — {nxt!r}. A calculation relabelled as "
                                f"hardware is how a closure count gets faked")
        rows.append((tag, scope, cls, nxt))
    return rows, problems


def main():
    rows, problems = scan()
    counts = {s: {c: 0 for c in CLASSES} for s in SCOPES}
    for _, scope, cls, _ in rows:
        if scope in counts and cls in CLASSES:
            counts[scope][cls] += 1

    # The closure document must agree with the register, or one of them is decoration.
    if os.path.exists(DOC):
        doc = open(DOC, encoding="utf-8").read()
        m = re.search(r'Remaining COMPUTATION items:\s*\*{0,2}(\d+)\*{0,2}', doc)
        if not m:
            problems.append("docs/COMPUTATIONAL_CLOSURE.md does not state "
                            "'Remaining COMPUTATION items: N'")
        elif int(m.group(1)) != counts["GEN6"]["COMPUTATION"]:
            problems.append(f"docs/COMPUTATIONAL_CLOSURE.md says "
                            f"'Remaining COMPUTATION items: {m.group(1)}' and the register has "
                            f"{counts['GEN6']['COMPUTATION']}")

    if "--closed" in sys.argv and counts["GEN6"]["COMPUTATION"]:
        problems.append(f"closure was asserted with {counts['GEN6']['COMPUTATION']} GEN6 entries "
                        f"still classified COMPUTATION")

    if problems:
        print(f"closure: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"closure: {len(rows)} live entries classified")
    for s in SCOPES:
        line = "  ".join(f"{c} {counts[s][c]}" for c in CLASSES if counts[s][c])
        print(f"  {s:10s} {line}")
    print(f"\n  GEN6 remaining COMPUTATION: {counts['GEN6']['COMPUTATION']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
