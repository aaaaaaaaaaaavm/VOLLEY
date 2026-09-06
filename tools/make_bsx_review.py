"""Build my BSX review from the live register; do not turn a freeze into completion."""
import argparse
from pathlib import Path
import check_computational_closure as closure
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"docs/BSX_REVIEW.md"
def render():
    rows, problems=closure.scan()
    if problems: raise ValueError("; ".join(problems))
    text=["# BSX review and Gen6 handoff", "", "Reviewed 2026-09-06. I use this as the entry point for engineering conversations. The tables below are generated from the live register, not hand-maintained closure counts.", "", "## What I can defend", "", "VOLLEY Gen5 is a frozen computational baseline with declared failures. Nothing has been built, fired, measured, qualified or flown. The [baseline](BASELINE.md) supplies the operating numbers and [Gen5 closure](GEN5_CLOSURE.md) names their evidence. A passing software gate establishes internal consistency, not flight readiness.", "", "The mission remains post-primary upper-stage deployment: provider-authorised stage manoeuvres do the coarse placement; the dispenser sets each satellite's release condition. Host propulsion reserve, restart capability, attitude control and disposal authority require provider data.", "", "## Gen6 preparation", "", "Gen6 already exists as a stage-integrated cold-gas design study. It is not a blank next generation and does not inherit Gen5 validation. Before a new architecture freeze:", "", "1. Resolve P92's secondary/tube architecture decision using A72-A74, then freeze revised requirements before implementing its successor. Do not advertise the suspended trim stage as available.", "2. Resolve the guided-contact model and tolerance questions P103/P108 against the corrected continuous tube. Keep P109's withdrawn jam result withdrawn; do not cite the original tip-off magnitude as established.", "3. Complete the reliability, backup-ejection, fill-window, pressure-vessel, sensing, materials and inhibit work named below. Retain failed bands and distinguish a calculation from component selection and measurement.", "4. Close the independent CAD check against the chosen geometry, then regenerate dependent evidence and both companions as one coherent batch.", "5. Freeze only with the remaining exceptions named, and use the closure gate to test any assertion that computation is finished.", "", "## Questions for BSX", "", "- Launch provider: available post-primary propulsion and restart windows, interface loads/envelope, stage mass properties, attitude authority, power, command access, and disposal/passivation constraints.", "- Mechanisms or test team: review the guide/contact geometry, seal-friction measurement at temperature, tip-off measurement and retention/release load paths.", "- Payload team: actual magnetic sensitivity, allowed release rate/acceleration, contamination limits and mechanical interfaces. Unmodified is a design objective; compatibility is not demonstrated.", "", "## Remaining work by scope", "", "| Scope | Computation | Hardware | Host data | Flight/operations | Decision |", "|---|---:|---:|---:|---:|---:|"]
    for scope in closure.SCOPES:
        counts=[sum(s==scope and c==cls for _,s,c,_ in rows) for cls in closure.CLASSES]
        text.append("| "+scope+" | "+" | ".join(map(str,counts))+" |")
    for scope in closure.SCOPES:
        text += ["", "## "+scope+" live items", "", "| Entry | Next step class | Action that would move it |", "|---|---|---|"]
        for tag,s,cls,action in rows:
            if s==scope: text.append(f"| [{tag}](../OPEN_PROBLEMS.md) | {cls} | {action.replace('|','/')} |")
    text += ["", "## Reproduce", "", "Run `python tools/make_bsx_review.py --check` and `bash tools/verify_all.sh` from a clean committed checkout. The scripts report skipped or unavailable checks. See [CONTRIBUTING.md](CONTRIBUTING.md) for dependencies and companion publication order.", ""]
    return "\n".join(text)
def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args();text=render()
    if a.check:
        if not OUTPUT.exists() or OUTPUT.read_text()!=text: raise SystemExit("stale BSX review; regenerate from the register")
        print("BSX review agrees with the live register")
    else: OUTPUT.write_text(text)
if __name__=="__main__": main()
