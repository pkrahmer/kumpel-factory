---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 652
comments_read: [6716487122]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T03:02:05.047236Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T03:02:05.054757Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T03:02:24.857623Z'
  stage: intake
  run: 5e09296d4f364fe099c31b48d59ce459
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T03:04:14.459066Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T03:04:16.853910Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T03:04:36.563626Z'
  stage: intake
  run: 9e1344fa69f44ac0b5af308488b02266
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T03:04:41.566523Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T03:06:26.825751Z'
  stage: tests
  run: 16bff0447f2a4984905ba9e5bc25b456
---

# The code names the working branch by its role


## Description

After F0057 the factory works on `develop`, and the texts the operator sees follow `WORK_BRANCH`. Several names in the code still say `main` for the working branch: a public function, private helpers, a field of a domain model, local variables, a comment and a test constant. Two modules also write the remote's name out in `f"origin/{WORK_BRANCH}"` instead of building it from `REMOTE`. The human sent these to a later story (F0057-S0002, journal entry 39), and F0057's acceptance collected them. This story renames them with no change in behaviour, so that a reader of the code sees the branch's role, not its old name.

What stays as it is:
- the stop `main_branch_failing` and `_MAIN_FAILING` (F0057 decision 6);
- the stamp fields `main_failed`/`main_probed`, which are stored in `preflight-stamp.json`;
- every entry-point function `main`.

## Interface

- `factory.entry.wiring` (entry): `stage_file_on_main(git: Git) -> str | None` becomes `stage_file_on_work_branch(git: Git) -> str | None`. Its callers in `factory.entry.run` follow.
- `factory.work.application.acceptance_reading` (application): `_main_report_paths` and `_main_reports` become `_work_report_paths` and `_work_reports`.
- `factory.watching.application.watcher` (application): `_main_commit` becomes `_work_commit`.
- `factory.pipeline.domain.evaluation` (domain): `EvaluationInput.main_commit` becomes `work_commit`. Every reader and writer of the field follows. It is not in the records contract.
- `factory.machine.application.preflight` and `factory.pipeline.domain.evaluation`: the local variables named `main` that hold the working branch's commit become `work`.
- `factory.entry.check_story`: the comment "On main a started story ..." says the working branch.
- `factory.pipeline.application.handlers.hand_over` and `factory.pipeline.application.stage`: `f"origin/{WORK_BRANCH}"` is built from `REMOTE`, as the other modules do.
- Tests: `tests/guards/test_work_branch_search.py` gains a second search (a new test in the same module). No identifier under `src/factory/` contains `main` as a word part (`main_`, `_main`), apart from `main_branch_failing`, `_MAIN_FAILING`, `main_failed` and `main_probed`.
- The human's leave (2026-11-08): the tester changes the earlier tests that name `stage_file_on_main` or `main_commit` (`tests/machine/application/test_container_environment.py`, `tests/pipeline/application/test_container_sync_origin.py`, `tests/pipeline/domain/test_evaluation_due.py`, `tests/pipeline/domain/test_evaluation_reject.py`, `tests/shared/application/test_acceptance_reviewer_role.py`, `tests/support/evaluation_support.py`) so far as the rename requires. The tester also renames the constant `NO_MAIN` in `tests/pipeline/application/test_repository_waiter.py` to `NO_WORK_BRANCH`, and the docstrings in `tests/conftest.py` (`remote`) and `tests/pipeline/application/handlers/test_merged.py` (module) say the working branch. Every test keeps its name and what it checks. The test function names that say `main` for the working branch are not renamed (the human, journal entry 4).

## Acceptance criteria

1. The new guard passes on the repository. It fails on a file it writes under its scope for each of these, one row each: an identifier `stage_file_on_main`, `x.main_commit` and `_main_reports`. It passes on a file holding `main_branch_failing`, `main_failed`, `main_probed` or `def main(` (rows of one test).
2. `from factory.entry.wiring import stage_file_on_work_branch` succeeds and `stage_file_on_main` no longer exists. `EvaluationInput` has the field `work_commit` and refuses `main_commit` as an unknown key (rows of one test).
3. Every earlier test passes, changed only under the leave.
4. The new guard, a third row of its test, fails on a file it writes under its scope that holds `f"origin/{WORK_BRANCH}"` and passes on a file that builds the name from `REMOTE`; it passes on the repository.
5. `make check` stays green.
6. docs: `docs/project-guide/machine.md` and `docs/project-guide/watching.md` name the new names where they named the old ones; `docs/decisions.md`: none.

## Smoke test

```bash
grep -rnwE "stage_file_on_main|_main_report_paths|_main_reports|_main_commit|main_commit" src/factory --include=*.py | wc -l
```
Expect: `0`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Format check passed. Questions:

   1. The Interface says `hand_over` and `stage` build `f"origin/{WORK_BRANCH}"` from `REMOTE`, but no criterion tests it. Two coders could read this differently and both pass. Options: (a) add a criterion, for example a guard row that fails on a file under `src/factory/` containing `f"origin/{WORK_BRANCH}"` and passes on the `REMOTE`-built form; (b) drop the clause from the Interface. I would choose (a), as a third row of the new guard.

   2. The Interface says the local variables named `main` in `preflight` and `evaluation` become `work`. The guard in criterion 1 searches only for `main` as a word part (`main_`, `_main`), so it cannot catch a bare variable `main`. No criterion tests this clause. Options: (a) extend the guard with a bare-`main`-identifier row that fails on `main = ...` and passes on `def main(`; (b) accept it as untested and say so in the Interface. I would choose (a).

   3. The `check_story` comment change ("On main a started story ...") has no criterion. I would accept it as an untested comment change, but please confirm. Alternatively, say the guard also covers comments.

   4. The Interface leaves one point open: "Whether the test function names that say `main` for the working branch are renamed as well is the human's to decide when refining." The tester needs this decided. Options: (a) rename none (the leave covers only the listed constants and docstrings); (b) rename them all. I would choose (a).

   5. Criterion 1's failing rows name `stage_file_on_main`, `x.main_commit` and `_main_reports`. The Interface rule covers every `main_` or `_main` word part, including `_main_commit` and `_main_report_paths`. Should one more failing row cover a leading-underscore private helper, or is `_main_reports` the representative? I would choose to keep the three rows as they are.
4. 2026-11-08 human: 1. (a), a third row of the new guard.
   2. (b): accepted as untested; a guard on a bare `main` would be fragile next to `main()` and `__main__`. The reviewer checks it by reading.
   3. Confirmed, an untested comment change.
   4. (a), rename none.
   5. Keep the three rows.
5. factory: started intake as vm.
6. intake: accepted. I carried in the human's answers (journal entry 4) and wrote exactly two edits into the story. (1) Answer 1(a): new criterion 4, a third row of the guard for `f"origin/{WORK_BRANCH}"`, failing and passing sides. The closing criteria are now 5 (`make check`) and 6 (`docs:`). (2) Answer 4(a): the Interface's open sentence now says the test function names are not renamed.
   - Interface: concrete modules, old and new names, and the field `work_commit`. Answers 2 and 3 are accepted as untested (bare `main` variables and the `check_story` comment, read by the reviewer). Answer 5 keeps the three failing rows.
   - Criteria: each is testable by one test function, with rows for the passing and the failing side. Every Interface clause that is not an accepted exception has a criterion: the guard rows, the import and the unknown key, the unchanged earlier tests, and the `REMOTE` form (new criterion 4).
   - Smoke test: the grep command is runnable, and `Expect: 0` is checkable.
   - Docs criterion: it names the two project-guide files and what they must say, and dictates no sentences.
   - Architecture: renames only, no layer changes. `main_failed` and `main_probed` stay because they are stored in a stamp. `REMOTE` is used the way the other modules use it.
   - Scope: within F0057 (the working branch's name in code). It leaves out the stop `main_branch_failing`, as decision 6 says. The earlier tests it changes are named and covered by the human's leave of 2026-11-08.
7. factory: started tests as vm.
8. tester: Wrote the tests for every criterion and changed the earlier tests the human's leave (2026-11-08) names, only as far as the rename needs.

   Criterion → test:
   - criterion 1: tests/guards/test_work_branch_search.py::test_no_identifier_in_the_source_names_the_working_branch_main (passes on the repository) and tests/guards/test_work_branch_search.py::test_the_search_finds_each_name_that_says_main_for_the_working_branch (rows: public-function, field, private-helper fail; kept-stop, kept-stamp-failed, kept-stamp-probed, entry-point pass)
   - criterion 2: tests/entry/test_wiring_work_branch_names.py::test_the_working_branch_is_named_by_its_role (rows: new-reader, old-reader-gone, work-commit, main-commit-refused)
   - criterion 3: the earlier suite, with the leave edits below
   - criterion 4: the same two guard tests (rows remote-spelled-out fails, remote-from-constant passes; the repository test covers "passes on the repository")
   - criteria 5, 6: not tests (make check; docs).

   How the new guard reads the source: it scans the `.py` files under `src/factory` with `tokenize`, so it looks only at NAME tokens. Strings and comments are not scanned. A name is flagged when `main` (any case) is one of its underscore-separated parts. Dunders (`__main__`) and the four kept names are skipped. Separately, the guard flags the text `origin/{WORK_BRANCH}`. Since it reads only identifiers, the string `"test_reject_..._leaves_main_clean"` in `src/factory/pipeline/domain/fault_paths.py` is not flagged. That string names a test function, and the human chose not to rename those.

   Note for the coder: under the Interface's rule ("no identifier under src/factory/ contains main as a word part"), the guard also flags names that the Interface's list does not mention:
   - `on_main` in `src/factory/pipeline/application/pipeline_loading.py` and `src/factory/work/domain/acceptance.py`
   - `_follow_main` in `src/factory/entry/run.py`

   These must be renamed too for the guard to pass on the repository.

   Files created: tests/entry/test_wiring_work_branch_names.py.
   Files changed, under the human's leave:
   - tests/guards/test_work_branch_search.py (the new search and its two tests)
   - tests/support/evaluation_support.py, tests/pipeline/domain/test_evaluation_due.py, tests/pipeline/domain/test_evaluation_reject.py: `main_commit=` became `work_commit=`
   - tests/pipeline/application/test_repository_waiter.py: `NO_MAIN` became `NO_WORK_BRANCH`; ruff format re-wrapped one line
   - tests/conftest.py: the `remote` docstring
   - tests/pipeline/application/handlers/test_merged.py: the module docstring, split onto two lines to fit the length limit

   Left unchanged: the `main_commit` fixtures in tests/machine/application/test_container_environment.py and tests/pipeline/application/test_container_sync_origin.py, and a local variable in tests/shared/application/test_acceptance_reviewer_role.py. They do not touch the renamed API, and the guard reads only `src/factory`, so the rename does not require changing them. No earlier test was renamed.

   Test run: the test files I wrote or changed (except conftest.py, which every run loads) ran red for the right reason. In test_evaluation_reject.py, `EvaluationInput` refuses the new `work_commit` key, which does not exist yet. The new guard and import tests fail because the old names are still there. No module failed to import: `stage_file_on_work_branch` is imported inside its test row, so the module still collects. make lint: green.

   `lint`: lint: green (0.1 s)
