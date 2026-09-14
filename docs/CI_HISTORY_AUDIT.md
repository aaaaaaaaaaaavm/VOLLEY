# Pull-request history audit

2026-09-14: GitHub Actions run 34902346212 failed the authorship step because its
checkout was GitHub's temporary PR merge commit 0efdfed64. The only rejected identity
was that synthetic commit's GitHub committer. The actual head and base histories have
separate authorship obligations and must both be checked.

The workflow now checks the complete history of the event's head SHA and base SHA,
then restores the event's test commit before running integration gates. Push events
check their actual commit once. The existing identity allowlist and refusal of shallow
history are unchanged. A real branch commit carrying an unexpected identity still fails.
This is not permission to merge a GitHub-committed change into the authored history.

The merged tree remains the subject of the numerical and integration tests. The
workflow does not replace merge testing with head-only testing to obtain a green result.
