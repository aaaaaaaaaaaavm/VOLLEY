# What a clean environment needs, and what degrades quietly without it

Adityavardhan Mishra · 2026-09-14, extended 2026-09-15

[`PROTOTYPE_READINESS.md`](PROTOTYPE_READINESS.md) package 0 asks for environment limitations to
be recorded separately from failures and omissions, and package 12 asks for the release evidence
to be rerun from a clean environment. This is that record. The first three rows were measured on
2026-09-14 in a container that had been reset, and the fourth on 2026-09-15. None is inferred from
the scripts.

**The point of this file is the third column.** A missing dependency that stops a gate is a
nuisance. A missing dependency that lets a gate print a clean line is a defect in the evidence,
and the second and third rows below are that. The fourth is a third kind: it leaves every gate
correct and blocks work no gate looks at.

## Measured degradation modes

| Missing | Affected gate | What it does |
|---|---|---|
| `numpy` and the rest of `requirements.txt` | A2-R levers, A13 band consistency, results freshness, artifacts | **Loud failure.** Tracebacks, `ModuleNotFoundError`. Harmless, because nobody reads a traceback as a pass |
| `cadquery==2.8.0` | artifacts | **False positive.** Four STEP files reported `STALE ... rebuild it, or the published artifact contradicts its own source`. They are current: the gate rebuilds and compares when a pair looks stale by commit time, and without cadquery it cannot, so it falls back to the time comparison it explicitly documents as unreliable. With cadquery installed, all four report `older ... but rebuilds byte-identically` and the gate passes. `check_artifacts.py` already records that *a false positive in a check is a defect in the check* |
| Full git history | authorship | **False clean**, and this is the dangerous one. A shallow clone made `check_authorship.py` print `52 commits, every author and committer is the repository's own`. The repository has 412. The sentence is a claim about every commit and it was made over an eighth of them. Fixed on 2026-09-14: the gate now refuses a shallow clone rather than passing on one |
| Network egress to anything but GitHub and package registries | none | **No gate is affected, and that is why it went unrecorded until it blocked a register entry.** Measured 2026-09-15: `ieeexplore.ieee.org`, `www.mdpi.com`, `arxiv.org`, `doi.org` and `api.crossref.org` all refuse with `EGRESS_BLOCKED` or a 403 from the proxy tunnel, while `pypi.org` returns 200 and git pushes succeed. Every gate in `verify_all.sh` runs offline by design, so the suite is entirely blind to this. What it stops is the reading and citation-checking work: [P57](../OPEN_PROBLEMS.md#p57) and [E16](../OPEN_PROBLEMS.md#e16) both need a publisher and cannot reach one, including the two references that are open access and need no subscription |

## The commands that were actually required

`tools/env-setup.sh` covers the solvers, LaTeX and the two requirement files. Three things it did
not cover, each of which stopped or corrupted a gate on this container:

```
git fetch --unshallow                     # or the authorship gate cannot make its claim
pip install --ignore-installed packaging  # Debian owns packaging 24.0; pip refuses to uninstall it
pip install cadquery==2.8.0               # optional in requirements.txt, but the artifacts gate needs it
```

The `packaging` conflict aborts the **entire** requirements install with
`Cannot uninstall packaging 24.0, RECORD file not found`, so every downstream dependency is
missing even though only one package conflicted.

## Identity, which resets on every container restart

The working container sets a machine account as its **global** `user.name` and `user.email`. A
repository clone with no local override inherits it silently. This is not hypothetical: it is how
a sibling repository acquired a commit under the wrong identity, repaired on 2026-08-31.

Neither the global correction nor the per-repository overrides survive a container restart — on
2026-09-14 the restart had re-cloned every repository, so all eight local overrides were gone at
once. **The only durable control is the one committed to the repository**,
[`tools/check_authorship.py`](../tools/check_authorship.py), which checks what actually landed
rather than what the environment intends. Before the first commit in any fresh environment:

```
git config user.email    # must be the repository's author, not the container default
```

## What this file does not claim

It does not claim the environment is the only reason a gate can be wrong, and it is not a
substitute for the gates. It records four specific measured behaviours. Three of them have a
command that removes them; the fourth does not, because a network policy is set outside the
container and no line in this repository can change it.

The first three were found by running the gates. The fourth was found by trying to do engineering
work, and no gate would ever have reported it, because every gate here is offline on purpose. That
is the more useful half of the habit: a suite that passes tells you the things it checks are
sound, and says nothing at all about the work it was never pointed at.
