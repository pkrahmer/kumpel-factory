# Kumpel works on develop and promotes accepted features to main

## Description

After F0057-S0002 the factory works on `develop`, and `main` is protected. Kumpel's scripts and texts still name `main`: it starts stories there, logs there, fixes there and waits for the archive commit on the remote's default branch. This story moves Kumpel to `develop` and adds the one act that reaches `main`: the promotion of `develop` after a feature's acceptance, as a pull request with a merge commit, behind a new switch `promote` that is off by default (F0057 decisions 3 to 5). It also gives Kumpel a script to archive a finished feature (decision 8), and makes every commit Kumpel makes name Kumpel as its author (decision 7).

## Interface

- `operator/skill/kumpel/scripts/`:
  - `start-story.sh`, `next-story.sh`, `approval.sh`, `status.sh`: `develop` wherever they name the working branch today (`git checkout -q main`, `origin/main...`).
  - `merge.sh` and `status.sh`: the archive commit is looked up on `develop` (`/commits?sha=develop&per_page=20`), not on the remote's default branch.
  - `reset-to-tag.sh`: moves `develop` to the tag by force; `main` is left alone and the script says so.
  - `archive-feature.sh <feature id>` (new): refuses a feature whose `backlog/` or `in-progress/` holds a story file, or whose last acceptance is not in `done/`; otherwise moves `factory/features/<feature>/` to `factory/archive/` on `develop` with the commit `<feature id>: archived`, pulls and pushes.
  - `promote.sh <feature id>` (new): refuses unless the feature is in `factory/archive/` on `develop`; opens a pull request from `develop` to `main` titled `<feature id>: promoted to main`, whose body lists the feature's stories with their titles; with the switch `promote` on, merges it with `merge_method: merge` and the message `Promoted by Kumpel after <feature id>'s acceptance.`; with it off, prints the pull request's number for the human. Never squash, never rebase.
  - `settings.sh`: a fourth switch `promote`, off in a new settings file (`settings.sh set promote on|off`).
- `operator/lib/` (or the skill's scripts): one shell function that commits with `Kumpel <kumpel@noreply.invalid>` as author and committer, used by `start-story.sh` and `archive-feature.sh`. `references/standing-orders.md` tells Kumpel to commit its log and its fixes through it.
- `operator/skill/kumpel/references/`: every "on `main`" for Kumpel's own writes says `develop`. `approving.md` gains the step after a feature's acceptance: archive the feature, then promote it (or open the promotion for the human). `standing-orders.md`, *Safety*: never push to `main`; never fix `main` directly, a fix goes to `develop` and reaches `main` with the next promotion.
- `operator/claude/commands/kumpel.md` and the opencode command: the switch `promote` among the switches.
- Tests under `tests/operator_scripts/`: the scripts with fake remotes. The human's leave (2026-11-07): the tester changes earlier tests of these scripts only so far as the branch's name, the lookup on `develop` and the new switch require; every changed test keeps its name and what it checks, and the entry names each.

## Acceptance criteria

1. `start-story.sh` commits the move on `develop` with Kumpel as author and committer, and pushes `develop` (one test on a fake remote).
2. `archive-feature.sh` moves a finished feature to `factory/archive/` on `develop` with Kumpel as author, and refuses a feature with a story still in `backlog/` or `in-progress/` (rows of one test).
3. `promote.sh` refuses a feature not archived on `develop`; opens a pull request from `develop` to `main` with the title of the Interface; merges it with a merge commit and Kumpel's message when `promote` is on, and only prints its number when off (rows of one test with a recorded hosting API).
4. `merge.sh` finds the archive commit on `develop`, not on the default branch (one test).
5. A new settings file has `promote` off (one test).
6. `make check` stays green.
7. docs: `operator/README.md`: the switch `promote`, the two new scripts in its file table, and that Kumpel never pushes to `main`. `docs/decisions.md`: none.

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT; export KUMPEL_SETTINGS="$d/s.json"; sh operator/skill/kumpel/scripts/settings.sh init owner/name "$d" >/dev/null; sh operator/skill/kumpel/scripts/settings.sh get promote
```
Expect: `off`

## Journal
