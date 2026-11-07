---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 645
comments_read: [6714658360]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-07T23:49:25.889667Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-07T23:46:54.145527Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-07T23:46:54.152624Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-07T23:47:14.904952Z'
  stage: intake
  run: 8417f04a47624544afc10e6655fe8c62
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-07T23:49:04.769765Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-07T23:49:07.129161Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-07T23:49:21.012473Z'
  stage: intake
  run: d6714e2db4cf48e08789a38090a89ad6
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-07T23:49:25.889667Z'
  stage: tests
---

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

1. 2026-11-07 human: created.
2. factory: started intake as vm.
3. intake: Questions (format check passed; the Interface has behaviours and rules without a criterion):
   1. `archive-feature.sh` also refuses a feature "whose last acceptance is not in `done/`". Criterion 2 tests only the story files in `backlog/` and `in-progress/`. Add a row for the missing or unfinished acceptance (I would add it to criterion 2), and say what a feature with no acceptance report counts as.
   2. `archive-feature.sh` commits with the message `<feature id>: archived`, then pulls and pushes. No criterion checks the message or the push. Criterion 2 should say the commit subject and that `develop` on the remote holds it.
   3. `promote.sh` has three behaviours with no criterion: the pull request body lists the feature's stories with their titles, the merge uses `merge_method: merge` (criterion 3 says "merge commit", which I read as this), and the "off" side prints the number. Please say whether the body is a row of criterion 3. I would add it.
   4. `next-story.sh`, `approval.sh` and `status.sh` move to `develop` (`origin/develop...`), and `status.sh` looks up the archive commit on `develop`. Criterion 1 covers only `start-story.sh`, and criterion 4 covers only `merge.sh`. Each of these scripts needs a criterion, or the Interface line should drop them.
   5. `reset-to-tag.sh` moves `develop` to the tag by force and leaves `main` alone, and says so. No criterion tests either part. I would add one (`develop` moved, `main` unchanged, the output says so).
   6. `settings.sh set promote on|off` is the switch itself. Criterion 5 tests only the default `off`. Add a criterion that `set promote on` makes `get promote` print `on`, and that another value is refused (what does `set` do with it today?).
   7. The shell function that commits as `Kumpel <kumpel@noreply.invalid>` is used by `start-story.sh` and `archive-feature.sh`. Criteria 1 and 2 test the author and the committer. Please name the module or file (`operator/lib/...` or the skill's scripts) so that the coder has one place to put it.
   8. The Interface changes `references/standing-orders.md`, `approving.md` and the commands `kumpel.md` and the opencode command. The docs criterion names only `operator/README.md`. Please say whether those files are covered by a criterion (for example the commands list `promote` among the switches), since `operator/skill/` is not a path the documenter may write.
   Route: I would choose `tests`, because the story changes scripts.
4. 2026-11-07 human: Yes to each, as you propose. Route: tests.
   1. A row in criterion 2: a feature whose acceptance is missing or not in `done/` is refused; no acceptance report counts as not finished.
   2. Yes: criterion 2 checks the subject `<feature id>: archived` and that the remote's `develop` holds it.
   3. Yes: rows of criterion 3 for the body (stories with titles), `merge_method: merge`, and the printed number when off.
   4. A new criterion: `next-story.sh`, `approval.sh` and `status.sh` work on `develop`, and `status.sh` finds the archive commit there (rows of one test).
   5. Yes: `develop` moved to the tag, `main` unchanged, the output says so.
   6. Yes: `set promote on` then `get promote` prints `on`; another value is refused the way the other switches refuse one today.
   7. `operator/skill/kumpel/scripts/kumpel-commit.sh`, sourced by the scripts that commit (the skill stays self-contained).
   8. The coder writes these files (`operator/skill/*`, `operator/claude/*`, `operator/opencode/*` are its paths). A criterion: the commands list `promote` among the switches, and `standing-orders.md` says never push to `main` and that a fix goes to `develop`.
5. factory: started intake as vm.
6. intake: accepted
   - Interface: names concrete paths and scripts (the Kumpel scripts, `kumpel-commit.sh` as the one commit function, `archive-feature.sh <id>`, `promote.sh <id>`, `settings.sh set promote on|off`). The human's answer fixed the file for the shared function (journal 4, item 7).
   - Criteria: the human's answer in journal 4 (items 1 to 8) gives the criteria I asked for, but they are not yet written into the story. I did not edit the story. The coder and tester are to read journal 4 together with the numbered criteria: criterion 2 gains the missing-or-unfinished-acceptance row and the subject/remote check; criterion 3 gains the body, `merge_method: merge` and printed-number rows; there are new criteria for `next-story.sh`, `approval.sh` and `status.sh`, for `reset-to-tag.sh`, for `settings.sh set promote on|off` (another value refused as today), and for the command and `standing-orders.md` texts. Each is one test with rows, and each rule has its failing side. Risk: someone reading only the numbered list will miss them.
   - Smoke test: runnable (`settings.sh init`, then `get promote`), no pytest in it, and `Expect: off` can be checked against the output.
   - Docs criterion: names what the reader must know (the switch, the two new scripts in the file table, that Kumpel never pushes to `main`) and dictates no sentences.
   - Architecture: the change sits in `operator/skill/kumpel/scripts/`, `operator/skill/*`, `operator/claude/*` and `operator/opencode/*`, which are the coder's paths, with tests under `tests/operator_scripts/`. This matches the layout in CLAUDE.md.
   - Scope: within F0057's scope (S0003 line) and not in its out-of-scope list. Earlier tests change only as far as the human's 2026-11-07 leave allows. Route: tests.
7. factory: started tests as vm.
