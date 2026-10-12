# VOLLEY publication gate

This rule applies to every public push, release, website, wiki, issue/comment, report, slide deck and shared artifact. The working draft may be incomplete; a public item must pass the checks below **before** it appears online. A green CI run after a push is detection, not prepublication approval.

## Gate order

1. **Select the exact publication set.** Record repository, commit, changed paths, artifact hashes, destination and the prior published commit in the private AVM Work Index. Do not publish from an unidentified working tree.
2. **Run the automatic gate locally.** `python3 tools/prepublish_gate.py --base <prior-published-commit>` checks changed files for internal draft names, probable secrets, accidental tool footers, broken local links, corrupt PDF/STEP/image signatures and oversized artifacts. A release candidate also runs `--all`; full-tree failures need a fix or a documented exclusion before a new release.
3. **Run the repo's existing engineering and build gates.** Recompute changed analyses, check numerical identities and uncertainty, rebuild affected CAD/figures/PDFs, verify manifest hashes, run current CI commands, and compare source/result copies in companion repositories. Do not turn a failed technical criterion into a passing publication criterion.
4. **Review claims against evidence.** Each headline number, graph, CAD view and capability statement must name the exact result/CAD revision. State model assumptions and uncertainty. Label a Blender image as a render, an unbuilt mechanism as a design, Gen6 speed as a target, and external tests as prior art. Never call simulated output measured or qualified.
5. **Review people and private material.** Check names, IDs, emails, institutional forms, notes to a guide, discussion text, PDF metadata, archives and image metadata for intended audience and consent. An academic authorship line must reflect actual authorship; do not assert sole authorship without evidence. Check every *new* issue/comment/wiki/release body before posting, since the file gate cannot see it.
6. **Review the reader route.** Open the rendered README, site, wiki, report, paper and slides affected by the change. Verify links, figures, labels, alt text, page count, citations, download targets, social preview and repository About text. A source-file check cannot establish that GitHub rendered it correctly.
7. **Propagate design changes.** For every change to geometry, mass, motor, power, mission or literature, follow source → simulation/result → STEP → figure → report/paper → slides → README/site/wiki → private work item. Update or explicitly retire dependent artifacts before publishing.
8. **Record the decision privately.** Mark each applicable gate pass/fail/not applicable in AVM Work Index with evidence links, reviewer/date, exact commit/hash and unresolved exceptions. Failed or unknown means hold. An exception needs a named owner, explanation and accurate public limitation; it cannot waive a secret exposure or a false claim.

## Enforcement and scope

Install the local pre-push hook with `git config core.hooksPath .githooks`. The same automatic script runs in CI to detect bypasses. GitHub rules should require the checks before merge or deployment; with the current one-branch workflow and unavailable repository-settings access, direct GitHub web edits and `git push --no-verify` remain possible bypasses. The owner must enable suitable rules or a protected staging workflow for a technical guarantee. Manual posts and settings changes still require the private decision record before publication.

The gate is intentionally incremental for routine pushes because older historical links and releases have known defects. A final release uses `--all` and the full eight-step review. It does not label unresolved engineering or college decisions complete.
