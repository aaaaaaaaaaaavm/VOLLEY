"""Check every link in the repository resolves, and that the cross-link block has not forked.

Three failure modes have actually happened here, which is why each is checked:

  1. A file moved and the links to it did not. The front-door restructure moved ten files
     into docs/ and left three absolute links in wiki/Home.md pointing at the old root.
  2. A relative link was written against the wrong directory. docs/ pages linking to
     ../OPEN_PROBLEMS.md and docs pages linking to sibling docs are easy to get backwards.
  3. The shared repository table drifted between copies. It appears in the flagship's
     PROGRAMME.md, in the generated companions, and in tools/lab-seed/README.md, and a
     hand-edit to any one of them silently forks it.

Run:   python3 tools/check_links.py
Exits non-zero on the first category with any failure, so it works in CI.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "aaaaaaaaaaaavm"

# Directories whose links are deliberately not maintained: superseded scripts kept for the
# record, and archived paper builds. Both are frozen by intent.
SKIP_DIRS = {".git", "legacy", "paper/archive", "node_modules", "__pycache__"}

# Only rendered files are checked. Scripts and LaTeX are excluded on purpose: the link-shaped
# strings inside make_baseline.py, export_companion.py and seed_issues.sh are templates for
# files written elsewhere. Checking those texts here reports the generator's own directory,
# which is never where the link will live. The generated output is checked instead, which is
# the thing a reader actually clicks.
#
# ONE EXCEPTION, and it is the reason this comment changed. seed_issues.sh writes $B/<path>,
# where $B is the flagship base URL, so those are absolute flagship paths and they DO resolve
# against this checkout. Blanket-excluding the file treated them as if they were relative
# template links, which they are not, and a dead one survived there for weeks: the VAULT-01
# rename moved docs/PHASE_II.md to docs/VAULT.md across twenty-one files and missed this one,
# where no gate could see it. `$B/` paths are checked below.
EXTS = (".md", ".html")

REL = re.compile(r"\]\(([^)\s#]+\.(?:md|py|sh|json|tex|png|gif|stl|step|dxf|cir|csv))(?:#[^)]*)?\)")

# Only FLAGSHIP links are resolved against this checkout. Links to the sibling repositories
# (VOLLEY-lab, VOLLEY-paper, VOLLEY-thesis) point at files that do not exist here and must not
# be reported broken -- the trailing slash after the repo name is what stops "VOLLEY" matching
# "VOLLEY-lab". Found when tools/lab-seed/README.md gained links to two files that live in the
# lab repository by design.
FLAGSHIP = "VOLLEY"
ABS = re.compile(
    r"https://(?:github\.com/%s/%s/(?:blob|tree)/main|"
    r"raw\.githubusercontent\.com/%s/%s/main)/([^)\s\"'>]+)" % (OWNER, FLAGSHIP, OWNER, FLAGSHIP))


def tracked_files():
    for base, dirs, files in os.walk(ROOT):
        rel_base = os.path.relpath(base, ROOT)
        if any(rel_base == d or rel_base.startswith(d + os.sep) for d in SKIP_DIRS):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(EXTS):
                yield os.path.join(base, f)


# tools/lab-seed/ is a template for VOLLEY-lab, not a directory of this repository's own
# pages. Its RELATIVE links -- to PII-8_free_flyer.md and its siblings -- resolve in the
# repository it seeds and cannot resolve here. It is exempted from link resolution only; it
# stays inside the cross-link block check, which is the check it actually needs.
SEED_DIRS = {os.path.join("tools", "lab-seed")}


def check_links():
    """Relative links resolve against the linking file; absolute ones against the repo root."""
    bad = []
    for path in tracked_files():
        rel = os.path.relpath(path, ROOT)
        if any(rel == d or rel.startswith(d + os.sep) for d in SEED_DIRS):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for m in REL.finditer(text):
            target = m.group(1)
            if target.startswith(("http", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                bad.append((rel, target, "relative"))
        for m in ABS.finditer(text):
            target = m.group(1).split("#")[0]
            if not os.path.exists(os.path.join(ROOT, target)):
                bad.append((rel, target, "absolute"))
    return bad


DOLLAR_B = re.compile(r"\$B/([A-Za-z0-9_./-]+)")
SEED_SCRIPT = os.path.join("tools", "seed_issues.sh")


def check_seed_paths():
    """Resolve the $B/<path> targets seed_issues.sh writes into GitHub issues.

    $B is the flagship base URL, so every one of these is an absolute path into this
    repository and is resolvable here. They are checked separately from the markdown
    sweep because the file is a shell script, not a rendered page, and because a broken
    one is published into an issue body where nobody reruns a link checker.
    """
    path = os.path.join(ROOT, SEED_SCRIPT)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return sorted({t for t in DOLLAR_B.findall(text)
                   if not os.path.exists(os.path.join(ROOT, t))})


def check_header_block():
    """The repository table must be byte-identical everywhere it appears.

    export_companion.py builds it from HEADER_ROWS and writes it between the
    PROGRAMME-HEADER markers. Any copy that disagrees has been hand-edited.
    """
    marker = re.compile(
        r"<!-- PROGRAMME-HEADER-START -->\n(.*?)<!-- PROGRAMME-HEADER-END -->",
        re.S)
    found = {}
    for path in tracked_files():
        if not path.endswith(".md"):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            m = marker.search(fh.read())
        if m:
            # Two things vary per repository by design and are normalised away: the trailing
            # "You are here" column, and the bold markers, which are what mark the row for the
            # repository the reader is currently in. Everything else must match exactly.
            body = "\n".join(ln.rsplit("|", 2)[0].replace("**", "")
                             for ln in m.group(1).strip().splitlines())
            found[os.path.relpath(path, ROOT)] = body
    if len(set(found.values())) > 1:
        return found
    return None


def main():
    failed = False

    bad = check_links()
    if bad:
        failed = True
        print(f"{len(bad)} broken link(s):")
        for rel, target, kind in sorted(set(bad)):
            print(f"  {rel}  ->  {target}  ({kind})")
    else:
        print("links: all resolve")

    seed_bad = check_seed_paths()
    if seed_bad:
        failed = True
        print(f"{len(seed_bad)} dead path(s) in {SEED_SCRIPT}, which is published into issues:")
        for t in seed_bad:
            print(f"  $B/{t}")
    else:
        print(f"seed paths: all $B targets in {SEED_SCRIPT} resolve")

    forked = check_header_block()
    if forked:
        failed = True
        print("\nthe cross-link block has forked between copies:")
        for rel in sorted(forked):
            print(f"  {rel}")
        print("  Fix PROGRAMME.md and re-run tools/export_companion.py; do not hand-edit.")
    else:
        print("cross-link block: consistent")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
