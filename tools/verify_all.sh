#!/usr/bin/env bash
# One command that verifies the programme, offline.
#
# Every gate this repository has, in dependency order, plus the one check none of them makes:
# that running them does not change a tracked file. A clean checkout followed by this script
# must leave the working tree clean. If it does not, something in the repository is generated
# from something else and has drifted -- which is the defect class P84, P100, P101, P102 and
# P107 all belong to.
#
#     ./tools/verify_all.sh            gates only, fast
#     ./tools/verify_all.sh --full     also regenerate results, figures and CAD, then diff
set -uo pipefail
cd "$(dirname "$0")/.."
FAIL=0
run() {
    printf '%-34s' "$1"; shift
    if out=$("$@" 2>&1); then printf 'PASS  %s\n' "$(echo "$out" | tail -1)"
    else FAIL=1; printf 'FAIL\n'; echo "$out" | sed 's/^/      /'; fi
}

echo "== gates =="
run "links"              python3 tools/check_links.py
run "register"           python3 tools/register_status.py --check
run "baseline"           python3 tools/make_baseline.py --check
run "public surfaces"    python3 tools/check_public.py
run "cross-references"   python3 tools/check_crossrefs.py
run "companion payloads" python3 tools/check_companions.py
run "band integrity"      python3 tools/check_bands.py
run "results freshness"   python3 tools/check_results_fresh.py
run "computational closure" python3 tools/check_computational_closure.py
run "artifacts"          python3 tools/check_artifacts.py
run "host-reference blocks" python3 analysis/host_reference.py --check-doc
run "host-reference self-test" python3 analysis/host_reference.py --self-test

if [ "${1:-}" = "--full" ]; then
    echo
    echo "== regenerate, then require no diff =="
    run "Gen5 CAD"       python3 cad/build_gen5.py --check
    run "Gen6 CAD"       python3 cad/build_gen6.py --check
    run "payload family" python3 analysis/payload_family.py
    run "cell manifest"  python3 analysis/cell_manifest.py
    run "register file"  python3 tools/register_status.py
    # host_reference.py is not re-run here. The results-freshness gate above already
    # regenerates its JSON and compares it numerically with a declared tolerance.
    # Re-running it and then requiring a clean tree would demand byte identity of
    # floating-point output, which is not a property two machines can share.
fi

echo
if ! git diff --quiet || [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    FAIL=1
    echo "TREE DIRTY after verification -- something is generated and has drifted:"
    git status --porcelain --untracked-files=no | sed 's/^/      /'
else
    echo "working tree clean after verification"
fi

[ $FAIL -eq 0 ] && echo "VERIFY: all checks passed" || echo "VERIFY: FAILURES ABOVE"
exit $FAIL
