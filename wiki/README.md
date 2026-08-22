# The wiki source — retired

**`Home.md` here is a deprecation stub, and the live wiki serves the same stub.** Publish with
`tools/publish_wiki.sh`. Nothing else belongs here.

## Why

GitHub serves the wiki from `VOLLEY.wiki.git`, a repository this one cannot see, so **no gate here
can tell whether the live page is stale** — and it was, repeatedly, in the ways
[`Home.md`](Home.md) now records. Every other public surface in this project is checked against the
results files by `tools/check_public.py`; the wiki was the one that could not be.

**It was retired rather than synchronised** ([`docs/STATE_OF_THE_PROJECT.md`](../docs/STATE_OF_THE_PROJECT.md)
decision **D9**), because maintaining a hand-written duplicate of the whole programme narrative with
no gate is how the problem started.

**Do not restore content here.** If a reader needs something, it belongs in the repository, where a
check can reach it.

## Publishing the stub

`tools/publish_wiki.sh` needs ordinary push credentials for `VOLLEY.wiki.git`. **GitHub does not
expose wiki repositories through its API**, so a sandboxed or proxied environment cannot reach it —
attempting it is refused because a `.wiki` repository is not addressable the way every other
surface here is, and there is no
fallback. **The stub was written and committed here on 2026-08-22; it must be published from a
machine with normal credentials:**

```bash
tools/publish_wiki.sh --dry-run   # confirm the diff
tools/publish_wiki.sh             # publish
```

**Until that runs, the live wiki still serves the superseded page.** Nothing in this repository
links to it, and no printed handout points at it, so the exposure is limited to a reader who finds
the GitHub wiki tab unprompted — but it is real, and it is the one public surface this project
cannot gate.
