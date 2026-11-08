---
stage: doing
blocked: null
round: 0
attempts: 1
crashes: 0
pull_request: 649
comments_read: [6715900227]
handed_over: null
claim:
  instance: vm
  stage: doing
  started_at: '2026-11-08T02:01:23.633164Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T01:56:37.057055Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T01:56:37.063998Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T01:56:58.825388Z'
  stage: intake
  run: 987fdcefbced421da9c4118f89b64d9e
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T01:58:48.021805Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T01:58:50.365369Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T01:59:13.879411Z'
  stage: intake
  run: 4a5a383a98e54aeabede6cd574789432
- number: 7
  speaker: factory
  kind: stall
  at: '2026-11-08T01:59:13.976515Z'
  stage: intake
  run: 4a5a383a98e54aeabede6cd574789432
  reason: form_invalid
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T01:59:20.565439Z'
  stage: intake
- number: 9
  speaker: intake
  kind: result
  at: '2026-11-08T01:59:35.730078Z'
  stage: intake
  run: ed6e98bb0524411080a6ae143119229c
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T01:59:40.719704Z'
  stage: tests
- number: 11
  speaker: tester
  kind: result
  at: '2026-11-08T02:01:18.489759Z'
  stage: tests
  run: 0d1497c0fff544059754de59bcd675f2
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T02:01:23.633164Z'
  stage: doing
---

# archive-feature.sh refuses a feature whose acceptance was refused

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

`operator/skill/kumpel/scripts/archive-feature.sh` counts a feature as finished when no story file is left in its `backlog/` or `in-progress/` and its last acceptance report is in `done/`. The factory also books a closed acceptance in `done/`, with `outcome: refused` in its front matter, so the script archives a refused feature, and `promote.sh` then promotes it to `main` (F0057-A0001, smoke test probe). This story makes the script read the outcome: a feature is finished only when its last acceptance in `done/` says `outcome: accepted`. What else counts as finished stays the same, and `promote.sh` is unchanged; it reads the archive.

## Interface

- `operator/skill/kumpel/scripts/archive-feature.sh <feature id>`: after its existing checks, it reads the front matter of the last acceptance report, the block between its first two `---` lines. The script refuses unless that block holds the line `outcome: accepted`, with `archive-feature.sh: <id> is not finished: its last acceptance <path> is not accepted` on stderr and exit status 1. Nothing is moved, committed or pushed, and the checkout stays on `develop` with no change.
- The existing refusals and their texts stay: a story in `backlog/` or `in-progress/`, no acceptance, and a last acceptance outside `done/`.
- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 names the new refusal among the ones Kumpel reports to the human.
- Tests: a new module `tests/operator_scripts/test_operator_archive_outcome.py`, on a fake remote through the `operator` fixture.
- The human's leave, given in journal entry 4: `tests/operator_scripts/test_operator_develop.py`, whose `finished_feature` writes an acceptance report without front matter. The tester gives that text the front matter of a booked acceptance (`stage: done`, `outcome: accepted`), so far as the new rule requires. Every changed test keeps its name and what it checks.

## Acceptance criteria

1. `archive-feature.sh F0001` on a feature whose stories are all in `done/`, run against acceptance reports in `done/`, gives these results (rows of one test):
   - Last report has `outcome: accepted`: exits 0 and moves the feature to `factory/archive/` on the remote's `develop`.
   - Last report has `outcome: refused`: exits 1 with `archive-feature.sh: F0001 is not finished: its last acceptance <path> is not accepted`, and the remote's `develop` is unchanged.
   - Last report has front matter but no `outcome` line: refused the same way.
   - Last report has no front matter: refused the same way.
   - Last report has an opening `---` but no closing one: refused the same way.
   - Last report has `outcome: accepted` only in its body, after the front matter's closing `---`: refused the same way.
   - `F0001-A0001` refused and `F0001-A0002` accepted, both in `done/`: exits 0, since the last one counts.
   Every refused row also checks that the local checkout is still on `develop` with a clean working tree.
2. The earlier refusals keep their texts and exit statuses, each a row of a test in the new module (the existing test only checks a non-zero status, not the texts): a story in `backlog/`, a story in `in-progress/`, no acceptance, a last acceptance outside `done/`; each exits 1 with its existing text on stderr (the texts as the script has them), and the remote's `develop` is unchanged. The earlier tests of `test_operator_develop.py` pass, changed only under the leave given in journal entry 4.
3. `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 contains the refusal text `is not finished: its last acceptance` (a test in the new module reads the file; the coder writes it).
4. `make check` stays green.
5. docs: `operator/README.md` and `docs/operator-guide/install.md` (*The promotion*) say that only a feature whose last acceptance was accepted is archived and promoted; `docs/decisions.md`: none.

## Smoke test

```bash
uv run pytest tests/operator_scripts/test_operator_archive_outcome.py 2>&1 | tail -1
```
Expect: a line ending in `passed in <seconds>s` with no `failed`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions before this story can start (the format check passed):

   1. The human's leave for `tests/operator_scripts/test_operator_develop.py` is not given yet. The Interface says "to be given when refining", and a story that changes another story's test needs the human's word. Please give it in your answer: may the tester change `finished_feature` so that its acceptance report has the front matter of a booked acceptance (`stage: done`, `outcome: accepted`), with every changed test keeping its name and what it checks? I would choose yes.

   2. The Interface says `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1, names the new refusal. No criterion tests or checks this. The path is not one the documenter may write, so the Interface changes a file outside the docs route and no criterion covers it. Please do one of these. (a) Add a criterion, for example a test that `approving.md` step 1 contains the refusal text. (b) Name `approving.md` in the docs criterion. I would choose (a), plus a note on which stage writes the file.

   3. The Interface says that on a refusal "nothing is moved, committed or pushed, and the checkout stays on `develop` with no change". Criterion 1 only tests that the remote's `develop` is unchanged. Please add to the refusal rows that the local checkout is still on `develop` with a clean tree, or drop the clause from the Interface. I would choose adding it.

   4. The Interface reads the front matter as "the block between its first two `---` lines". Criterion 1 does not say what happens when the file has an opening `---` but no closing one, or when `outcome: accepted` appears only in the body, after the front matter. Please add a row for each, refused the same way, or say they do not matter. I would choose adding both rows.

   5. Criterion 2 says the earlier refusals keep their texts and exit statuses, and it points at `test_operator_develop.py`. Please confirm that this file's existing tests for the three earlier refusals (a story in `backlog/` or `in-progress/`, no acceptance, a last acceptance outside `done/`) already pin each text and exit status. If one is missing, add a row to the new module.

   Also noted: S0006 is not in `feature.md`'s Stories or Scope lists. The story's own comment says the feature acceptance proposed it, so I treat it as in scope.
4. 2026-11-08 human: 1. Yes, the leave as you wrote it.
   2. (a): a test that approving.md step 1 names the refusal; the coder writes approving.md (operator/skill/* is its path).
   3. Yes, add it.
   4. Yes, both rows, refused the same way.
   5. Yes: confirm, and add a row to the new module for any that is missing.
5. factory: started intake as vm.
6. intake: accepted, with the human's answers (journal entry 4) carried into the story.
   - Interface: names `archive-feature.sh`, its refusal text and exit status, and `approving.md` step 1. The leave for `test_operator_develop.py` is now stated as given (entry 4, answer 1).
   - Criteria: criterion 1 gains two rows (opening `---` with no closing one; `outcome: accepted` only in the body) and a clean-`develop`-checkout check on every refused row (answers 3 and 4). Criterion 2 now has its own rows in the new module for the four earlier refusals. I checked the existing test: it asserts only a non-zero exit status, not the texts, so they were not pinned (answer 5). New criterion 3 tests that `approving.md` step 1 holds the refusal text (answer 2, option a). `make check` and `docs:` stay last, and the docs criterion names what the reader must know. Every rule has a failing side.
   - Smoke test: runnable. The command has no `-q`, and its Expect line is checkable.
   - Docs criterion: names the files and what they must say, with no sentences dictated.
   - Architecture: the change is in an operator script and its tests. It belongs in `operator/skill/kumpel`, and `promote.sh` is unchanged.
   - Scope: S0006 is not in `feature.md`'s Stories list, but it comes from the feature's acceptance, so I treat it as in scope.
   - Route: `tests`. The Interface changes the script and `approving.md`, which are outside the documenter's paths.
7. factory: Stage intake stalled (attempt 1 of 2): the work item's form broke during the stage: criterion numbered 4 where 5 is expected
8. factory: started intake as vm.
9. intake: accepted. The format finding (criterion numbered 4 where 5 is expected) came from the criterion I added in the earlier intake run (journal entry 6, carrying in answer 2): I did not renumber the closing `docs:` criterion. I renumbered it from 4 to 5 and changed nothing else.
   - Interface: names `operator/skill/kumpel/scripts/archive-feature.sh`, its refusal text and exit status 1, the unchanged earlier refusals, `approving.md` step 1, the new test module, and the human's leave (entry 4) for `test_operator_develop.py`.
   - Criteria: each is testable by one parametrized test. Every refusal has its failing side. The refused rows cover a missing `outcome` line, no front matter, no closing `---`, and `outcome: accepted` only in the body. They also cover the accepted row and the last-report-wins row. Each refused row checks a clean `develop` checkout. Criterion 2 pins the four earlier refusal texts. Criterion 3 tests the text in `approving.md`.
   - Smoke test: runnable. The command passes no `-q`, and the project's pytest configuration was not checked for `addopts`. The Expect line is checkable.
   - Docs criterion: names the two files and what the reader must know, and dictates no sentences.
   - Architecture: the change is in an operator script, its reference file and its tests, and `promote.sh` is unchanged.
   - Scope: S0006 is not in `feature.md`'s Stories list, but the feature's acceptance proposed it, so I treat it as in scope.
   - Route: `tests`, because the script and `approving.md` are outside the documenter's write paths.
10. factory: started tests as vm.
11. tester: I wrote one test per criterion. They fail now on purpose: they are the coder's spec.

    Mapping:
    - criterion 1: tests/operator_scripts/test_operator_archive_outcome.py::test_archive_feature_archives_only_a_feature_whose_last_acceptance_was_accepted. It has 7 rows: accepted, refused, no-outcome-line, no-front-matter, no-closing-line, accepted-only-in-body, refused-then-accepted. Each refused row checks:
      - exit status 1
      - the refusal line, with the report's path, on stderr
      - the remote's `develop` is unchanged
      - the checkout is on `develop` and `git status --porcelain` is empty
    - criterion 2: tests/operator_scripts/test_operator_archive_outcome.py::test_archive_feature_keeps_its_earlier_refusals_and_their_texts. It has 4 rows: story-in-backlog, story-in-progress, no-acceptance, last-acceptance-outside-done. Each checks exit status 1, the script's current text on stderr, and that the remote's `develop` is unchanged. The earlier test in tests/operator_scripts/test_operator_develop.py still covers this criterion's second half.
    - criterion 3: tests/operator_scripts/test_operator_archive_outcome.py::test_approving_names_the_refusal_of_a_feature_whose_acceptance_was_not_accepted. It checks that the `1.` line under `## After a feature's acceptance` in `operator/skill/kumpel/references/approving.md` contains `is not finished: its last acceptance`.
    - criteria 4 and 5: no test (`make check` and the docs).

    Files:
    - Created: tests/operator_scripts/test_operator_archive_outcome.py
    - Created: tests/support/archive_feature_support.py
    - Changed: tests/operator_scripts/test_operator_develop.py

    Why test_operator_develop.py changed:
    - **Standing leave to move a shared test helper (CLAUDE.md, Tests):** the new module needed the feature constants, `finished_feature` and `tree`, so I moved them from test_operator_develop.py into tests/support/archive_feature_support.py. test_operator_develop.py now imports them from there. Every test keeps its name and what it checks.
    - **The human's leave (journal entry 4):** the acceptance report that `finished_feature` writes (`ACCEPTANCE`) now has the front matter `stage: done` and `outcome: accepted` before the same body. The new `ACCEPTANCE_BODY` holds that body without front matter, for the refused rows.

    Test run (`uv run pytest -q` on the two files):
    - 6 tests fail, all for the right reason. The five refused rows of criterion 1 get exit 0, because the script archives anyway. The criterion 3 test fails because step 1 of approving.md does not have the text yet.
    - Everything else passes, test_operator_develop.py included. That is correct: those rows describe behaviour that already holds.
    - No module failed to import. The script under test is a shell script, so the failures are wrong results, not import errors.

    `make lint` is green. Nothing in the criteria needed interpreting.

    `lint`: lint: green (0.2 s)
12. factory: started doing as vm.
