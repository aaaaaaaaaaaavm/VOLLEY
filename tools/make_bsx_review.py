"""Build my BSX review from the live register without erasing configuration history."""
import argparse
import re
from pathlib import Path
import check_computational_closure as closure
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"docs/BSX_REVIEW.md"
def render():
    rows, problems=closure.scan()
    if problems: raise ValueError("; ".join(problems))
    text=["# BSX review and Gen6 handoff", "", "Reviewed 2026-09-16. I use this as an engineering-conversation entry point. The live-item tables are generated from the register; configuration-specific history is retained rather than rewritten as current hardware.", "", "## What I can defend", "", "VOLLEY Gen5 is a frozen computational baseline with declared failures. Nothing has been built, fired, measured, qualified or flown. The [baseline](BASELINE.md) supplies the operating numbers and [Gen5 closure](GEN5_CLOSURE.md) names their evidence. A passing software gate establishes internal consistency, not flight readiness.", "", "The programme remains provider-hosted control of spacecraft departure conditions: provider-authorised host manoeuvres can supply coarse orbital placement and the deployment system supplies the relative release condition. Host propulsion reserve, restart capability, attitude control, navigation uncertainty, interface limits and disposal authority require provider data.", "", "## Current Gen6 preparation", "", "The clean-sheet reference carried forward for the next calculations is **independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. It is not selected flight hardware. P92/P113 remain open.", "", "1. Turn S1-S4 into architecture-driving uncertainty and clearing/settling requirements before assigning release-cell tolerances.", "2. Quantify installed burden and failure topology for independent cells, small banks and the shared magazine/path using one system boundary.", "3. Try to falsify the reference before detailed CAD: accumulator force-displacement, preload sensitivity, latch shock, pusher friction/guidance, tip-off, catcher load and cycle life.", "4. Carry the surviving reference into a dated P92 configuration decision, then engineer one real cell and scale 2/4/12-cell arrangements.", "5. Keep the approximately 8 m gas guide, A72-A74 trim/tube conflict, P103/P108 contact work and pressure-system studies as historical gas-Gen6 evidence. Do not transfer their geometry or failure magnitudes to the compact reference without a new validation path.", "", "The generated live-item table below still reproduces each register entry's recorded next-step wording. P92's legacy row therefore describes the historical gas trim/tube decision that produced A72-A74; the current programme-level P92 path is the clean-sheet reference and its explicit falsifiers in [GEN6_REFERENCE_ARCHITECTURE.md](GEN6_REFERENCE_ARCHITECTURE.md). The register status remains LIVE until its native closure condition is legitimately dispositioned.", "", "## Questions for BSX / host review", "", "- Launch provider: retained post-primary body, usable envelope/mounts/keep-outs, remaining propulsion and restart windows, stage mass properties, attitude authority, navigation uncertainty, power/energy, thermal limits, command access, and disposal/passivation constraints.", "- Mechanisms or test team: review independent retention, accumulator/latch/pusher/catcher load paths, release repeatability, shock/tip-off measurement and the smallest useful coupon before a flight-like cell is drawn.", "- Payload team: actual retention, acceleration, shock, tip-off, contamination and magnetic limits. Unmodified is a design objective; compatibility is not demonstrated.", "", "## Remaining work by scope", "", "| Scope | Computation | Hardware | Host data | Flight/operations | Decision |", "|---|---:|---:|---:|---:|---:|"]
    for scope in closure.SCOPES:
        counts=[sum(s==scope and c==cls for _,s,c,_ in rows) for cls in closure.CLASSES]
        text.append("| "+scope+" | "+" | ".join(map(str,counts))+" |")
    for scope in closure.SCOPES:
        text += ["", "## "+scope+" live items", "", "| Entry | Next step class | Action that would move it |", "|---|---|---|"]
        for tag,s,cls,action in rows:
            if s==scope:
                action = re.sub(r"\[([^]]+)\]\(#[^)]+\)", r"\1", action)
                text.append(f"| [{tag}](../OPEN_PROBLEMS.md) | {cls} | {action.replace('|','/')} |")
    text += ["", "## Reproduce", "", "Run `python tools/make_bsx_review.py --check` and `bash tools/verify_all.sh` from a clean committed checkout. The scripts report skipped or unavailable checks. See [CONTRIBUTING.md](CONTRIBUTING.md) for dependencies and companion publication order. [BSX_PORTFOLIO_AUDIT.md](BSX_PORTFOLIO_AUDIT.md) records the repositories and checks covered by this review.", ""]
    return "\n".join(text)
def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args();text=render()
    if a.check:
        if not OUTPUT.exists() or OUTPUT.read_text()!=text: raise SystemExit("stale BSX review; regenerate from the register")
        print("BSX review agrees with the live register")
    else: OUTPUT.write_text(text)
if __name__=="__main__": main()