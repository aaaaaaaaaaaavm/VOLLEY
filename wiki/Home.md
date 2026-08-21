# VOLLEY — this wiki is retired

**Nothing is maintained here. Go to the repository:**
**[github.com/aaaaaaaaaaaavm/VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)**

---

## Why it was retired, 2026-08-22

This page was a **second, uncontrolled source of truth**, and it lost.

The repository publishes every number from a committed JSON result and re-checks it against the
script that produced it on every commit. **A wiki page cannot be checked that way**: GitHub serves
it from `VOLLEY.wiki.git`, a different repository that no gate in the project can see. So it was
the only surface that could go stale without anything failing — and it did, repeatedly. At one
point the live page still named the project by its old name, still quoted a headline velocity from
before the CAD sled reconciliation, still gave a lifetime multiplier from before the depth-resolved
thrust constant, and still made a phase-spacing claim the project had withdrawn.

Keeping it synchronised would have meant maintaining a duplicate of the whole programme narrative
by hand, forever, with no gate. **Retiring it was the cheaper and more honest option**, and
[`docs/STATE_OF_THE_PROJECT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/STATE_OF_THE_PROJECT.md)
had already listed the choice as decision **D9**.

## Where the content went

| If you wanted… | Read |
|---|---|
| The one-page version | [`SUMMARY.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/SUMMARY.md) |
| What the thing is and why it exists | [`docs/CONCEPT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/CONCEPT.md) |
| The frozen Gen5 evidence case | [`docs/GEN5_CLOSURE.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/GEN5_CLOSURE.md) |
| Current programme disposition | [`docs/STATE_OF_THE_PROJECT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/STATE_OF_THE_PROJECT.md) |
| Every headline number, gate-checked | [`docs/BASELINE.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/BASELINE.md) |
| What is broken | [`OPEN_PROBLEMS.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/OPEN_PROBLEMS.md) |
| The renders and the CAD | [`cad/`](https://github.com/aaaaaaaaaaaavm/VOLLEY/tree/main/cad) |

> **Nothing in this project has been built, fired, measured, qualified or flown.** That was true on
> every version of this page and it is still true.
