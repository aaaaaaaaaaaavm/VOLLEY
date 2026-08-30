# Publishing the profile README

GitHub shows the README of a repository named exactly after the account at the top of the
profile page. It is the first thing a visitor sees after clicking through from a repository.

## One-time setup

1. Create a new public repository named exactly `aaaaaaaaaaaavm`.
   GitHub confirms when you have found the special repository name. If it does not, the
   name is wrong.
2. Copy `README.md` from this directory into it and push.

```bash
gh repo create aaaaaaaaaaaavm --public --description "Profile"
git clone https://github.com/aaaaaaaaaaaavm/aaaaaaaaaaaavm.git
cp <this-dir>/README.md aaaaaaaaaaaavm/
cd aaaaaaaaaaaavm && git add README.md
git commit -m "Profile" && git push
```

## Then pin the repositories

Profile, then Customize your pins, and select `VOLLEY`, `VOLLEY-paper`, `VOLLEY-thesis`, `VOLLEY-lab`.
Pinning is separate from the README and has to be done in the web UI. Without it the four
repositories sit below everything else on the account.

## Why this file lives here

It is kept in the flagship rather than in the profile repo so it stays with the rest of the
programme's tooling, next to `bootstrap_repos.sh` and `publish_releases.sh`. This directory is
the source; the profile repo is a copy. Edit here, then re-copy, the same
generated-not-maintained rule the companion repositories follow, for the same reason.

## Constraints it is written under

- No hardware claim. The repository's front page states that nothing has been built, fired or
  measured, and the profile has to agree with it. This changes the day `B-1` produces a number.
- No skill-percentage bars, trophy widgets or streak counters.
- The paper is described as a manuscript, because it is written and unsubmitted.

---

## This template forked from its own output once, and that is worth guarding

Found 2026-08-10. The published `aaaaaaaaaaaavm/README.md` was *more current* than this
directory's copy: the published one had been edited in place with the corrected operating point
while this source still carried 16.5 m/s, 10.7 g, 2.58 kJ and "Thirty-one numbered defects".

The source was staler than the artifact generated from it, which is the opposite of how this
repository is supposed to work and the same class as P42 (the Pages site) one layer out.

Both copies are now byte-identical. When updating the profile, edit *here* and copy across,
or if you edit the published one directly, copy it back. `diff` them before assuming either is
current:

```bash
diff tools/profile-readme/README.md ../aaaaaaaaaaaavm/README.md
```

## It forked a second time, on 2026-08-30, and in the other direction

The first fork was the source being edited without re-copying. This one was the reverse: five
commits landed on the profile repository — the GatewayCX section, the portfolio map, and a table
of six focused repositories — and none of them came back here. The copy became the newer
document, which is exactly what the rule above exists to prevent, and `check_public.py` had been
naming the fork since it appeared.

Resolved by bringing the profile repository's version back into this file, because it was the one
with the newer content. That is the right answer for this instance and the wrong habit in
general: **the fix is not to decide which side is newer, it is not to edit the copy.**

Before publishing, every image URL on the page was fetched. All nineteen return real content.
A stale local clone of a sibling repository will make them look missing when they are not, and
the disk is not the evidence — the URL is.
