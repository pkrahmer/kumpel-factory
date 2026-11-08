---
stage: review
blocked: null
round: 1
attempts: 1
crashes: 0
pull_request: 645
comments_read: [6714658360, 6714963482]
handed_over: null
claim: null
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
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T00:06:04.977579Z'
  stage: tests
  run: cd391953352249b9a6cad5a13606e579
- number: 9
  speaker: factory
  kind: stall
  at: '2026-11-08T00:06:05.180092Z'
  stage: tests
  run: cd391953352249b9a6cad5a13606e579
  reason: check_red
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T00:06:19.777436Z'
  stage: tests
- number: 11
  speaker: tester
  kind: result
  at: '2026-11-08T00:13:10.897505Z'
  stage: tests
  run: a471926f7dd547cc82b70826bbbd238a
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T00:13:15.927683Z'
  stage: doing
- number: 13
  speaker: coder
  kind: question
  at: '2026-11-08T00:18:13.889148Z'
  stage: doing
  run: b60dc63e3a9d41de919d7aa6db4cb4da
  blocked: question
- number: 14
  speaker: human
  kind: comment
  at: '2026-11-08T00:20:02.668217Z'
  stage: doing
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-08T00:20:05.057425Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-08T00:22:36.450878Z'
  stage: doing
  run: 0c406c74e000496fa33a66ee45130216
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-08T00:22:41.574100Z'
  stage: tests
- number: 18
  speaker: tester
  kind: result
  at: '2026-11-08T00:23:22.528085Z'
  stage: tests
  run: 7f7b295fc93e4010b80215138928c654
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-08T00:23:28.190642Z'
  stage: doing
- number: 20
  speaker: coder
  kind: result
  at: '2026-11-08T00:27:47.260633Z'
  stage: doing
  run: 06ed220b70894369b2afe6fd33e532a6
- number: 21
  speaker: factory
  kind: started
  at: '2026-11-08T00:27:52.148719Z'
  stage: review
- number: 22
  speaker: reviewer
  kind: result
  at: '2026-11-08T00:30:15.630909Z'
  stage: review
  run: 44ea7d2e3f1f479d8aa9f7d82e9d8a47
- number: 23
  speaker: factory
  kind: started
  at: '2026-11-08T00:30:21.323816Z'
  stage: doing
- number: 24
  speaker: coder
  kind: result
  at: '2026-11-08T00:33:04.457447Z'
  stage: doing
  run: d2bf7b4e132e4bdab9a844375f4eaff1
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-08T00:33:09.639750Z'
  stage: tests
- number: 26
  speaker: tester
  kind: result
  at: '2026-11-08T00:33:50.347731Z'
  stage: tests
  run: cb8d69dcdc3b4a3783c80c4a64b4f046
- number: 27
  speaker: factory
  kind: started
  at: '2026-11-08T00:33:55.304383Z'
  stage: doing
- number: 28
  speaker: coder
  kind: result
  at: '2026-11-08T00:38:16.549044Z'
  stage: doing
  run: a32e17dd7f12440bb15e3d54115eb65d
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
  - `settings.sh`: a fourth switch `promote`, off in a new settings file (`settings.sh set promote on|off`); `get` reads a known switch that the file lacks as `off`, so a settings file from before this story works without a new `init`.
- `operator/lib/` (or the skill's scripts): one shell function that commits with `Kumpel <kumpel@noreply.invalid>` as author and committer, used by `start-story.sh` and `archive-feature.sh`. `references/standing-orders.md` tells Kumpel to commit its log and its fixes through it.
- `operator/skill/kumpel/references/`: every "on `main`" for Kumpel's own writes says `develop`. `approving.md` gains the step after a feature's acceptance: archive the feature, then promote it (or open the promotion for the human). `standing-orders.md`, *Safety*: never push to `main`; never fix `main` directly, a fix goes to `develop` and reaches `main` with the next promotion.
- `operator/claude/commands/kumpel.md` and the opencode command: the switch `promote` among the switches.
- Tests under `tests/operator_scripts/`: the scripts with fake remotes. The human's leave (2026-11-07): the tester changes earlier tests of these scripts only so far as the branch's name, the lookup on `develop` and the new switch require; every changed test keeps its name and what it checks, and the entry names each.

## Acceptance criteria

1. `start-story.sh` commits the move on `develop` with Kumpel as author and committer, and pushes `develop` (one test on a fake remote).
2. `archive-feature.sh` moves a finished feature to `factory/archive/` on `develop` with the commit subject `<feature id>: archived` and Kumpel as author, and the remote's `develop` holds it; it refuses a feature with a story still in `backlog/` or `in-progress/`, and a feature whose acceptance is missing or whose last acceptance is not in `done/` (no acceptance report counts as not finished) (rows of one test).
3. `promote.sh` refuses a feature not archived on `develop`; opens a pull request from `develop` to `main` with the title of the Interface and a body that lists the feature's stories with their titles; merges it with `merge_method: merge` and Kumpel's message when `promote` is on, and only prints its number when off (rows of one test with a recorded hosting API).
4. `merge.sh` finds the archive commit on `develop`, not on the default branch (one test).
5. A new settings file has `promote` off; `set promote on` then `get promote` prints `on`; another value is refused the way the other switches refuse one; a settings file without the `promote` key reads it as `off`.
6. `next-story.sh`, `approval.sh` and `status.sh` work on `develop`, and `status.sh` finds the archive commit there (rows of one test).
7. `reset-to-tag.sh` moves `develop` to the tag, leaves `main` unchanged, and its output says so (one test).
8. The commands `operator/claude/commands/kumpel.md` and `operator/opencode/command/kumpel.md` list `promote` among the switches, and `references/standing-orders.md` says never push to `main` and that a fix goes to `develop` (rows of one test).
9. `make check` stays green.
10. docs: `operator/README.md`: the switch `promote`, the two new scripts in its file table, and that Kumpel never pushes to `main`. `docs/decisions.md`: none.

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
8. tester: Tests written from the numbered criteria and from the criteria the human added in journal 4 (the intake did not write those into the Description; I left it unchanged too).

   Criterion → test:
   - criterion 1 (start-story commits on `develop` as Kumpel, pushes `develop`, `main` untouched): tests/operator_scripts/test_operator_develop.py::test_start_story_commits_on_develop_as_kumpel
   - criterion 2, with journal 4 items 1 and 2 (finished feature moved to `factory/archive/` on `develop` with subject `F0001: archived` and Kumpel as author and committer, the remote's `develop` holds it, `main` untouched, other features stay; refusal rows: story in backlog/, story in in-progress/, no acceptance, acceptance in in-progress/, last acceptance A0002 in in-progress/): test_operator_develop.py::test_archive_feature_moves_only_a_finished_feature_to_the_archive_on_develop
   - criterion 3, with journal 4 item 3 (refusal when the feature is not archived on `develop`; POST /pulls with head `develop`, base `main`, title `F0001: promoted to main`, a body that lists the story ids and titles; switch on: PUT merge with `merge_method: merge` and `commit_message` `Promoted by Kumpel after F0001's acceptance.`; switch off: no merge, the number is printed): test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on
   - criterion 4 (merge.sh finds the archive commit on `develop`, not on the default branch; rows for both sides): tests/operator_scripts/test_operator_merge_reset.py::test_the_merge_looks_for_the_archive_commit_on_develop
   - criterion 5, with journal 4 item 6 (new file has `promote` off; `set promote on|off` works; another value is refused with exit 2 and `settings.sh: yes is neither on nor off`): test_operator_develop.py::test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others
   - journal 4 item 4 (next-story, approval and status read `develop`, and status finds the archive commit there; one row per script on a remote where `develop` is ahead of `main`): test_operator_develop.py::test_next_story_approval_and_status_read_develop_not_main
   - journal 4 item 5 (reset moves `develop` by force, sends no request for `main`, and prints a line that names `main`): test_operator_merge_reset.py::test_the_reset_moves_develop_and_says_that_main_is_left_alone
   - journal 4 item 8 (both kumpel commands name `promote`; standing-orders.md says "never push to main" and "a fix goes to develop", checked with backticks removed and case ignored): test_operator_develop.py::test_the_texts_name_the_promote_switch_and_keep_kumpel_off_main

   Files created: tests/operator_scripts/test_operator_develop.py.

   Earlier test files changed:
   - Under the human's leave of 2026-11-07, limited to the branch name, the lookup on `develop` and the new switch. Every test keeps its name and what it checks.
     - tests/support/operator_skill_support.py: `SCRIPTS_BRANCH` is now `develop`, and `commits()` answers `/commits?sha=develop&per_page=20`. `make_bare_remote` also gives the remote a `main` at the same commit as its `HEAD`, so a clone starts on `main` and each script must switch to `develop` itself.
     - tests/operator_scripts/test_operator_merge_reset.py: the commits route, "would move/moved develop to", `ALLOWED_CHANGE` allows `develop` instead of `main`, and the only-moves test ignores the line about `main`.
     - tests/operator_scripts/test_operator_skill_scripts.py: `DEFAULT_SWITCHES` gains `promote: False`, the `show` line gains `promote off`, and the commits failure route uses `sha=develop`.
   - Under the standing leave to move a shared test helper: `KUMPEL` moved from tests/operator_scripts/test_operator_skill_signature.py to tests/support/operator_skill_support.py, and that test file now imports it.

   Test run: no module failed to import, because these are shell scripts and every test imports. The one run of the four files failed as intended: every new test failed, along with the earlier tests that now expect `develop`, the new route or the `promote` switch. `archive-feature.sh` and `promote.sh` do not exist yet.

   Open:
   - `make lint` was interrupted when the session ended and I have no result for it. I did run `ruff format` on the new file. The factory's lint check after this stage will show whether it is green.
   - `promote.sh` is tested against a git checkout: it must find the archived feature and the story titles in the checkout's `develop`, as `next-story.sh` does, not through the API's contents. If the coder wants to read them through the API, that is a question for the human.
   - The reset test checks only that some printed line names `main`. The wording of that line is the coder's choice.
9. factory: Stage tests stalled (attempt 1 of 2): a check is red after the stage: `lint`
   Bytecode compiled 4164 files in 81ms
   sync: green (0.1 s)
   Bytecode compiled 4164 files in 53ms
   tests/operator_scripts/test_operator_merge_reset.py:252:101: E501 Line too long (102 > 100)
   tests/operator_scripts/test_operator_skill_signature.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   tests/support/operator_skill_support.py:189:101: E501 Line too long (119 > 100)
   Found 3 errors.
   [*] 1 fixable with `--fix`.
   make: *** [Makefile:32: lint] Error 1
10. factory: started tests as vm.
11. tester: Attempt 2 of the tests stage. The tests from journal entry 8 were already committed. This round I only fixed the lint findings behind the stall (journal 9). I left the Description unchanged.

    Lint fixes (each test keeps its name and what it checks):
    - tests/operator_scripts/test_operator_merge_reset.py: the over-long assertion on the commits route now builds the `routes` list first. `ruff format` then rewrapped one assertion in the reset test.
    - tests/support/operator_skill_support.py: `commits()` now builds its route in a local variable, to keep the line under 100 characters.
    - tests/operator_scripts/test_operator_skill_signature.py: the import block is sorted (`ruff check --fix`, I001). This is the import of `KUMPEL` moved under the standing leave.
    `make lint`: green.

    Criterion → test (unchanged from journal 8):
    - criterion 1: tests/operator_scripts/test_operator_develop.py::test_start_story_commits_on_develop_as_kumpel
    - criterion 2 (with journal 4 items 1 and 2): tests/operator_scripts/test_operator_develop.py::test_archive_feature_moves_only_a_finished_feature_to_the_archive_on_develop
    - criterion 3 (with journal 4 item 3): tests/operator_scripts/test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on
    - criterion 4: tests/operator_scripts/test_operator_merge_reset.py::test_the_merge_looks_for_the_archive_commit_on_develop
    - criterion 5 (with journal 4 item 6): tests/operator_scripts/test_operator_develop.py::test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others
    - journal 4 item 4 (next-story, approval, status on develop): tests/operator_scripts/test_operator_develop.py::test_next_story_approval_and_status_read_develop_not_main
    - journal 4 item 5 (reset-to-tag): tests/operator_scripts/test_operator_merge_reset.py::test_the_reset_moves_develop_and_says_that_main_is_left_alone
    - journal 4 item 8 (command and standing-orders texts): tests/operator_scripts/test_operator_develop.py::test_the_texts_name_the_promote_switch_and_keep_kumpel_off_main

    Files created: tests/operator_scripts/test_operator_develop.py (attempt 1).

    Earlier test files changed:
    - Under the human's leave of 2026-11-07: tests/support/operator_skill_support.py, tests/operator_scripts/test_operator_merge_reset.py and tests/operator_scripts/test_operator_skill_scripts.py.
    - Under the standing leave to move a shared helper: tests/operator_scripts/test_operator_skill_signature.py (`KUMPEL` moved to the support module).
    Journal 8 gives the details.

    Modules the test runner could not import: none, because the tests drive shell scripts. One run of the four files: the new tests fail, and so do the earlier tests that now expect `develop`, the new commits route or the `promote` switch (for example test_operator_skill_signature.py::test_the_start_commit_is_kumpels_and_the_clone_keeps_its_identity). `archive-feature.sh`, `promote.sh` and `kumpel-commit.sh` do not exist yet.

    Open (as in journal 8): `promote.sh` is tested against a git checkout of `develop`, not through the API's contents. The wording of the reset's line about `main` is the coder's choice.

    `lint`: lint: green (0.1 s)
12. factory: started doing as vm.
13. coder: Question: `make check` is red because of two failures that are outside my write paths. Everything else is done and green.

    What I built (left in the working tree):
    - `operator/skill/kumpel/scripts/kumpel-commit.sh` (new): `kumpel_commit <message>` commits what is staged, with `Kumpel <kumpel@noreply.invalid>` as author and committer. `start-story.sh` and `archive-feature.sh` source it.
    - `archive-feature.sh` (new): works on `develop`. It refuses a feature with an `<id>-S*.md` in `backlog/` or `in-progress/`, a feature with no acceptance, and a feature whose last acceptance (the highest `<id>-A*.md` across its folders) is not in `done/`. Otherwise it runs `git mv` into `factory/archive/`, commits `<id>: archived` as Kumpel, pulls, and pushes `origin develop`.
    - `promote.sh` (new): refuses unless `factory/archive/<id>-*/` exists on `develop`. It POSTs `/pulls` with head `develop`, base `main` and title `<id>: promoted to main`; the body lists every `<id>-S*` story with the `# ` title of its file. With `promote` on, it PUTs the merge with `merge_method: merge` and `Promoted by Kumpel after <id>'s acceptance.`. With it off, it prints `promotion opened: #<n>, for the human to merge`.
    - `start-story.sh`, `next-story.sh`, `approval.sh`: `develop` instead of `main`. `merge.sh` and `status.sh` look up `/commits?sha=develop&per_page=20`. `reset-to-tag.sh` moves `refs/heads/develop` and prints that it left `main` alone (as a plan line without `--yes`, after the move with it). `settings.sh` has a fourth switch, `promote`, off by default.
    - Texts: `promote` added to the switches in `operator/claude/commands/kumpel.md` and `operator/opencode/command/kumpel.md`, and as a row in the switches table of `SKILL.md`. In `references/standing-orders.md`, *Safety* now says never push to `main` and that a fix goes to `develop` and reaches `main` with the next promotion; *The log* now says to commit the log and every fix on `develop` through `kumpel_commit`. In `references/approving.md`, `answering.md` and `shaping.md`, every "on `main`" for Kumpel's own writes is now `develop`, and `approving.md` gains *After a feature's acceptance* (archive, then promote).

    Main choice: `promote.sh` reads the archived feature and the story titles from the checkout's `develop`, as `next-story.sh` does and as the tests expect. The alternative I rejected was reading them through the contents API, which would need more routes and is not what the tests record. Refactor pass: I read my diff and found nothing to change.

    The two red tests in `make check`:
    1. `tests/guards/test_work_branch_search.py::test_no_file_in_the_source_or_the_tests_writes_the_working_branch_by_name` fails with `E   Left contains one more item: 'tests/operator_scripts/test_operator_merge_reset.py: heads/main'`. The tester's new test `test_the_reset_moves_develop_and_says_that_main_is_left_alone` contains the literal `"/heads/main"` (`assert [request for request in machine.requests() if "/heads/main" in request.route] == []`), and the guard forbids that literal anywhere in `tests`. The code can't fix this; the test has to change. I propose (my choice) that the tester writes `f"/heads/{DEFAULT_BRANCH}"`, which checks the same thing. Route: `tests`.
    2. `tests/operator_scripts/test_operator_site_check.py::test_the_operator_readme_names_every_script_and_library` fails with `E   AssertionError: assert ['kumpel-comm... 'promote.sh'] == []`. The three new scripts are not named in `operator/README.md`. Only the documenter may write that file, and the docs stage comes after doing, so this story can't leave doing green. Options: (a) the human adds the three rows (`archive-feature.sh`, `promote.sh`, `kumpel-commit.sh`) to the file table of `operator/README.md` on this branch, and the documenter finishes the docs criterion later (my choice); (b) the human gives the coder leave and a write path for `operator/README.md` for this story; (c) merge `kumpel_commit` into an existing script, dropping `kumpel-commit.sh`. Option (c) only removes one of the three names and goes against your answer in journal 4, item 7.

    I noticed but did not touch: a settings file written before this change has no `promote` key. `settings.sh get promote` then exits with `unknown key: promote`, so `promote.sh` stops before it opens anything. The operator has to run `settings.sh init` again, or a later story could have `get` default a missing switch to off. The Description is unchanged: the intake left the criteria from journal 4 in the journal only, and my write paths do not include the work item.
14. 2026-11-08 human: 1. Yes: the tester writes `f"/heads/{DEFAULT_BRANCH}"`; route tests for that.
    2. (b): the coder may write operator/README.md for this story (factory/pipeline.yml on develop). Add the three rows to its file table; the documenter finishes the rest of the docs criterion.
    3. The missing `promote` key: yes, in this story `settings.sh get` treats a missing switch as `off`, so an old settings file works without a new init. The tester adds a row for it.
15. factory: started doing as vm.
16. coder: Round 0, after the human's answer (journal 14). I changed code for items 2 and 3. Two test changes are open for the tester.

    What I built (left in the working tree; the earlier work from journal 13 is already committed):
    - `operator/README.md` (the human's leave for this story, item 2): three rows in the file table, for `archive-feature.sh`, `promote.sh` and `kumpel-commit.sh`. The documenter finishes the rest of the docs criterion.
    - `operator/skill/kumpel/scripts/settings.sh` (item 3): `get` treats a known switch (`merge`, `answer`, `start_next`, `promote`) that the file lacks as `off`, so a settings file from before this change works without a new `init`. An unknown key still exits with `unknown key: <key>`. I checked this by hand on an old-shape file: `get promote` prints `off`.

    Changes for the tester:
    1. In `tests/operator_scripts/test_operator_merge_reset.py::test_the_reset_moves_develop_and_says_that_main_is_left_alone`, write `f"/heads/{DEFAULT_BRANCH}"` instead of the literal `"/heads/main"` (journal 14, item 1).
    2. In `tests/operator_scripts/test_operator_develop.py::test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others` (or a test of its own), add a row: a settings file without a `promote` key gives `off` from `settings.sh get promote` (journal 14, item 3).

    `make check`: lint, types, layers, sast, secrets and licenses are green. `test` is red on one test only: `tests/guards/test_work_branch_search.py::test_no_file_in_the_source_or_the_tests_writes_the_working_branch_by_name` (`E   Left contains one more item: 'tests/operator_scripts/test_operator_merge_reset.py: heads/main'`). Change 1 fixes it. The README test now passes.

    Main choice: `get` recognises the missing switch by a fixed list of the four known switches. The alternative I rejected was adding the missing key to the file whenever the script reads it, which would make a read write the file.

    Refactor: the list of the four switches now appears twice in `settings.sh`, in the defaults that `init` writes and in `get`. Both are in separate Python heredocs, and sharing the list would need an extra variable passed into both, so I kept it as it is.

    Noticed, not touched: `settings.sh set promote on` on an old file still fails with `unknown switch: promote`, because the human's answer covers only `get`. The operator can run `init` again, or a later story can make `set` add a known switch. The journal did not change the meaning of the task beyond these items. The Description stays as it is: the work item is outside my write paths.
17. factory: started tests as vm.
18. tester: Approved test change. This entry covers the two changes the coder's journal entry 16 names, as the human answered them in journal 14, items 1 and 3.

    1. tests/operator_scripts/test_operator_merge_reset.py::test_the_reset_moves_develop_and_says_that_main_is_left_alone: the check that no request touches `main` now matches `f"/heads/{DEFAULT_BRANCH}"` instead of the literal `"/heads/main"`. `DEFAULT_BRANCH` is imported from tests/support/operator_skill_support.py. The test still checks the same thing, and the guard `tests/guards/test_work_branch_search.py` no longer finds the literal. `ruff format` rewrapped the assertion.
    2. The new test tests/operator_scripts/test_operator_develop.py::test_a_settings_file_without_the_promote_switch_reads_it_as_off writes a settings file that has only `merge`, `answer` and `start_next`, and checks that `settings.sh get promote` exits 0 and prints `off`. I made it a test of its own, not a row of test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others, because its setup is a hand-written old file rather than `settings.sh init`.

    Criterion mapping (journal 14 item 3 → test_a_settings_file_without_the_promote_switch_reads_it_as_off). The rest is unchanged from journal 11.

    Files created: none. Files changed: the two test files above, both from this story.

    Modules the test run could not import: none.

    Test run: `uv run pytest -q` on the two files: all 66 tests pass, since the coder's code is already in place. `make lint`: green.

    `lint`: lint: green (0.2 s)
19. factory: started doing as vm.
20. coder: Round 0, after the tester's approved test change (journal 18). I changed no code this run.

    The working tree was clean on arrival: my code from journals 13 and 16 and the tester's two changes from journal 18 are all committed. `make check` now passes with every check green (`test: green (107.8 s)`, `check: green`, coverage 99.22 %). The guard `tests/guards/test_work_branch_search.py` and the operator README test, the two red tests behind the earlier question, both pass.

    What the story built (paths, all committed):
    - `operator/skill/kumpel/scripts/`: the new `kumpel-commit.sh`, `archive-feature.sh` and `promote.sh`. `start-story.sh`, `next-story.sh`, `approval.sh`, `status.sh`, `merge.sh` and `reset-to-tag.sh` moved to `develop`. `settings.sh` has the switch `promote`, and `get` reads a known switch that the file lacks as `off`.
    - Texts: `operator/claude/commands/kumpel.md`, `operator/opencode/command/kumpel.md`, `operator/skill/kumpel/SKILL.md` and `references/standing-orders.md`, `approving.md`, `answering.md`, `shaping.md`.
    - `operator/README.md`: only the three file-table rows, which the human allowed in journal 14. The documenter finishes the rest of the docs criterion.

    Main choice: `promote.sh` reads the archived feature and the story titles from the checkout's `develop`. I rejected reading them through the contents API (journal 13).

    Refactor: no new diff this run, so there was nothing to change. Journal 16 already notes the four-switch list that appears twice in `settings.sh`, and I left it.

    Noticed, not touched:
    - On a settings file from before this change, `settings.sh set promote on` still fails with `unknown switch: promote`. The human's answer covered only `get`.
    - The Description does not yet carry the criteria the human added in journals 4 and 14. The work item is outside my write paths.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
21. factory: started review as vm.
22. reviewer: Review, round 0. I read the work item, then `git diff develop...HEAD -- . ':!factory'`: the scripts under `operator/skill/kumpel/scripts/`, the reference texts, both commands, `operator/README.md`, the new `tests/operator_scripts/test_operator_develop.py` and the four earlier test files. I checked each criterion, including the ones the human added in journals 4 and 14, against its test.

    Group 1 (criteria): every criterion has a test that checks what it names, and the coder's `make check` was green (journal 20). Group 2 (architecture): the change sits in shell scripts under `operator/`, so the `src/` layer rules don't apply. Group 3 (security): request bodies are built with `json.dumps`, not by joining strings, and the diff has no secrets and no markers. Documents: I checked the three new `operator/README.md` rows, `approving.md`, `standing-orders.md` and `SKILL.md` against the scripts, and every claim matches.

    Findings:
    1. `operator/skill/kumpel/scripts/settings.sh:89-92` (`set`): on a settings file from before this story, `settings.sh set promote on` (and so `/kumpel promote on`) exits with `unknown switch: promote`. That is every existing operator's file, which goes against the reason the human gave in journal 14 item 3 ("so an old settings file works without a new init"). The list of known switches is also now written twice, as the defaults dict at line 48 and the tuple at line 76. Fix: keep one table of the known switches and their defaults, and use it in `init`, `get` and `set`, where `set` accepts a known switch the file lacks and writes it. Then route `tests` for one row: an old-shape file, `set promote on`, then `get promote` prints `on`.
    2. `tests/operator_scripts/test_operator_develop.py:51` `head()` copies `remote_commit` from `tests/support/git_support.py:178`. Lines 329-331 repeat the body of `write_switches` (lines 139-143). Fix: use `remote_commit`, and give `write_switches` the switches dict so the old-file test calls it.

    Description corrected (only the reviewer can write the work item, and the coder and tester said so in journals 13, 16, 18 and 20):
    - Interface `settings.sh`: "off in a new settings file" -> also says `get` reads a known switch the file lacks as `off` (journal 14 item 3).
    - Criterion 2: rows for a story in backlog/in-progress -> also the subject `<feature id>: archived`, that the remote's `develop` holds it, and the refusal of a missing or unfinished last acceptance (journal 4 items 1-2). Test: `test_archive_feature_moves_only_a_finished_feature_to_the_archive_on_develop`.
    - Criterion 3: title and merge commit -> also the body listing stories with titles, and `merge_method: merge` (journal 4 item 3). Test: `test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on`.
    - Criterion 5: only `promote` off in a new file -> also `set on`, another value refused, and a missing key reads `off` (journal 4 item 6, journal 14 item 3). Tests: `test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others`, `test_a_settings_file_without_the_promote_switch_reads_it_as_off`.
    - New criterion 6, `next-story.sh`, `approval.sh` and `status.sh` on `develop` (journal 4 item 4). Test: `test_next_story_approval_and_status_read_develop_not_main`.
    - New criterion 7, `reset-to-tag.sh` (journal 4 item 5). Test: `test_the_reset_moves_develop_and_says_that_main_is_left_alone`.
    - New criterion 8, the command and standing-orders texts (journal 4 item 8). Test: `test_the_texts_name_the_promote_switch_and_keep_kumpel_off_main`.
    - The closing criteria are renumbered to 9 (`make check`) and 10 (docs). Each added criterion already has its test, so none of them needs a new one.

    Rejected: counting the old-file test as a separate function where a row was required. A file without the key is a different rule from `set`, and its setup differs. I also did not ask the human about finding 1: the Interface names `set promote on|off`, and journal 14 states the goal that an old file keeps working.

    Earlier tests:
    - `tests/operator_scripts/test_operator_merge_reset.py`: the human's leave of 2026-11-07, named in the Interface (branch name, lookup on `develop`). It also adds two new tests.
    - `tests/operator_scripts/test_operator_skill_scripts.py`: the human's leave of 2026-11-07 (the new switch, lookup on `develop`).
    - `tests/operator_scripts/test_operator_skill_signature.py`: the standing leave to move a shared test helper (`KUMPEL` moved to `tests/support/operator_skill_support.py`).
    - `tests/support/operator_skill_support.py`: the human's leave of 2026-11-07 (`SCRIPTS_BRANCH`, the commits route, a remote whose `HEAD` is `main`). The `KUMPEL` move is under the standing leave.
23. factory: started doing as vm.
24. coder: Round 1. This run handles the reviewer's findings in journal 22.

    Finding 1 (code, done): `operator/skill/kumpel/scripts/settings.sh` now has a single table of the known switches and their defaults, the shell variable `switches` (a JSON object). It is passed as an argument into the Python heredocs of `init`, `get` and `set`:
    - `init` writes the table as the new file's switches.
    - `get` reads a known switch that the file lacks as `off`, as before.
    - `set` accepts a known switch that the file lacks and writes it into the file. An unknown switch is still refused with `unknown switch: <name> (known: merge, answer, start_next, promote)`. The list now comes from the table, not from the file.

    I checked this by hand on a file with only `merge`, `answer` and `start_next`:
    - `get promote` printed `off`.
    - `set promote on` printed `promote on`, and then `get promote` printed `on`.
    - `set colour on` exited 1 with the unknown-switch message.

    `make check`: green (`test: green (108.0 s)`, coverage 99.22 %).

    Main choice: the table is one JSON string in shell, handed to each heredoc as an argument. I rejected making `get` and `set` write the missing defaults into the file on every read, because a read should not write. I also rejected keeping a Python tuple next to the defaults dict, which is the duplication the finding names.

    Refactor: the diff is the table and its three uses. I found nothing more to change.

    Test changes for the tester:
    1. Finding 1's row, in `tests/operator_scripts/test_operator_develop.py`: take a settings file without a `promote` key, run `settings.sh set promote on`, then check that `settings.sh get promote` prints `on`.
    2. Finding 2:
       - In `tests/operator_scripts/test_operator_develop.py`, `head()` (line 51) should use `remote_commit` from `tests/support/git_support.py` instead of copying it.
       - `write_switches` (lines 139-143) should take the switches dict, so that the old-file test (lines 329-331) calls it instead of repeating its body.

    Noticed, not touched: the Description already carries the criteria from journals 4 and 14 (the reviewer added them in journal 22). Nothing in this round changes the meaning of the task.
25. factory: started tests as vm.
26. tester: Tester, round 1. I made the test changes the coder named in journal 24 (the reviewer's findings 1 and 2 in journal 22). Every change is in `tests/operator_scripts/test_operator_develop.py`, a file this story wrote. No other test file changed.

    What changed:
    - Finding 1 (row): `test_a_settings_file_without_the_promote_switch_reads_it_as_off` is now parametrized with two rows:
      - `read`: a settings file without the `promote` key, then `get promote` prints `off`. This is what the test checked before.
      - `set-on` (new): on the same file, `set promote on`, then `get promote` prints `on`.
      The test keeps its name.
    - Finding 2:
      - I removed the local `head()`. Its callers now use `remote_commit` from `tests/support/git_support.py`.
      - `write_switches(operator, switches)` now takes the dict of switches.
      - A new constant, `OLD_SWITCHES`, holds the three switches from before this story. The promote test calls `write_switches(operator, {**OLD_SWITCHES, "promote": promote})`. The old-file test calls `write_switches(operator, OLD_SWITCHES)` instead of repeating its body.

    Criteria mapping is unchanged from journal 22. The changed tests:
    - criterion 5: `tests/operator_scripts/test_operator_develop.py::test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others` and `::test_a_settings_file_without_the_promote_switch_reads_it_as_off`.

    Files created: none. Files changed: `tests/operator_scripts/test_operator_develop.py`.

    Modules the test run could not import: none.

    Test run: `uv run pytest -q tests/operator_scripts/test_operator_develop.py`: all 23 tests pass, since the coder's change to `settings.sh` is already in place. `make lint`: green.

    `lint`: lint: green (0.1 s)
27. factory: started doing as vm.
28. coder: Round 1, after the tester's change (journal 26). I changed no code in this run.

    The working tree was clean when I started. The commits already hold my fix for the reviewer's finding 1 (journal 24: `operator/skill/kumpel/scripts/settings.sh` has one table of the known switches and their defaults, used by `init`, `get` and `set`; `set` now accepts a known switch the file lacks and writes it). They also hold the tester's changes for findings 1 and 2 in `tests/operator_scripts/test_operator_develop.py`: the new `set-on` row, `remote_commit` used in place of the copied `head()`, and `write_switches` taking the dict of switches.

    `make check` is green: `test: green (108.3 s)`, coverage 99.22 %, `check: green`.

    Main choice (unchanged from journal 24): the switch table is one JSON string in the shell, passed into each Python heredoc as an argument. I rejected having reads fill in missing defaults by writing to the file, because a read should not write.

    Refactor: this run added no diff, so there was nothing to change.

    Noticed, not touched: nothing new. Both of the reviewer's findings are addressed, and the Description already carries the criteria from journals 4 and 14.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
