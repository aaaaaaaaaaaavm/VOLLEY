# The wiki source

**`Home.md` here is the maintained copy. The live wiki is a different repository.**

GitHub serves the wiki from `VOLLEY.wiki.git`, which is not this repository and which nothing
here writes to automatically. Editing `Home.md` and committing it changes **nothing** that a
reader sees until it is published.

```bash
tools/publish_wiki.sh --dry-run   # show what would change on the live page
tools/publish_wiki.sh             # publish it
```

## Why this file exists

Nothing said any of the above, and the page drifted for it. On **2026-08-14** the source had
been corrected four times while the live wiki had not been touched since **2026-07-30**: it
still named the project *emocd*, still quoted a **20.37 m/s** headline from before the CAD sled
reconciliation, still reported a **×1.62** lifetime multiplier from before the depth-resolved
thrust constant, and still made a phase-spacing claim withdrawn the same week as **P56**.

Every propagation tool in this repository walks tracked files, so the source was corrected each
time. **The live page is published across a repository boundary that no check here can see** —
the same class of defect as **P58**, where two authored manuscripts in two repositories forked,
and **P61**, where a run sheet drifted from its own script.

**The wiki is the least trustworthy surface this project publishes**, because it is the only one
that can be stale without anything failing. Treat what it says as advisory and the repository as
authoritative — which the page itself says at the top.
