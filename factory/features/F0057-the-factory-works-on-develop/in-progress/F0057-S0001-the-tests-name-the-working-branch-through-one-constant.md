---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 643
comments_read: [6713530910]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-07T21:54:26.901648Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-07T21:54:26.908741Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-07T21:54:47.235359Z'
  stage: intake
  run: 6d854be502294030bccbae73b2a1be15
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-07T21:56:36.452126Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-07T21:56:38.853725Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-07T21:56:54.843162Z'
  stage: intake
  run: e615b12c2bf443eb9e6613fd14b8eb20
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-07T21:56:59.412728Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-07T22:01:12.915326Z'
  stage: tests
  run: e99d0a810e6b41ecbd065847e662f4b2
---

# The tests name the working branch through one constant

## Description

The factory's working branch is named by the constant `MAIN_BRANCH` in `factory.shared.domain.paths`, but 159 test modules and about 20 lines under `src/factory/` write the name `main` literally (`origin/main`, `refs/heads/main`, a fake repository's first branch). F0057 will rename the working branch to `develop` (S0002). This story prepares that without changing any behaviour: the constant becomes `WORK_BRANCH`, still with the value `main`, every use under `src/factory/` and every test that names the branch uses it, and a guard keeps a literal branch name from coming back. After it, S0002 changes one value.

## Interface

- `factory.shared.domain.paths`: `MAIN_BRANCH` is renamed `WORK_BRANCH`. Its value stays `"main"`. Every module under `src/factory/` that imports `MAIN_BRANCH` imports `WORK_BRANCH`, and names derived from it (`_MAIN_REF`, `_ORIGIN_MAIN`, `PIPELINE_REF`, `FORM_REF`) are built from it as today. A docstring or comment that writes `origin/main` for the working branch says "the working branch" or `origin/<working branch>` instead.
- Tests: every test that names the factory's working branch by a literal (`"main"` as a branch, `origin/main`, `refs/heads/main`, `heads/main`, `git init -b main`, `--initial-branch=main`) builds it from `WORK_BRANCH` and `REMOTE` instead. A literal `main` that is no branch (a function `main`, `__main__`, a word in a message) stays.
- The human's leave (2026-11-07): the tester changes earlier tests only so far as replacing a literal branch name with the constant requires. Every changed test keeps its name and what it checks; a helper that builds a fake repository may take the constant as its default. The entry names the number of changed modules and any test whose change is more than that replacement.
- `tests/guards/test_work_branch_search.py` (new): no file under `src/factory/` and `tests/` holds `origin/main`, `heads/main`, `-b main` or `--initial-branch=main`, apart from this guard itself.
- No behaviour changes: the factory still works on `main`.

## Acceptance criteria

1. `from factory.shared.domain.paths import WORK_BRANCH` gives `"main"`, and `MAIN_BRANCH` no longer exists (one test).
2. The guard of the Interface passes on the repository, passes on a clean file inside its scope that holds none of the four strings, and fails on a file the test writes that holds `origin/main`, `heads/main`, `-b main` or `--initial-branch=main`, one row for each string (rows of one test). This test is also the only test of the Interface's docstring and comment clause.
3. Every earlier test passes unchanged in what it checks; the entry names the modules changed under the leave.
4. `make check` stays green.
5. docs: `docs/project-guide/shared.md`, where `paths` is described: the reader learns that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `docs/decisions.md`: none in this story.

## Smoke test

```bash
uv run python -c "from factory.shared.domain.paths import WORK_BRANCH; print(WORK_BRANCH)"
```
Expect: `main`

## Journal

1. 2026-11-07 human: created.
2. factory: started intake as vm.
3. intake: Questions (format check passed; the story is not accepted yet):

   1. Criterion 2 names only one failing side of the guard. The Interface forbids four strings: `origin/main`, `heads/main`, `-b main` and `--initial-branch=main`. Criterion 2 says the guard "fails on a file that holds `origin/main`", so the other three strings have no failing-side row, and a guard that checked only `origin/main` would pass every test. Should criterion 2 read: "the guard fails on a file the test writes that holds `origin/main`, `heads/main`, `-b main`, or `--initial-branch=main`, one row for each string"? I would choose that.

   2. The Interface says the guard allows `-b main` only "apart from this guard itself", and that it covers `src/factory/` and `tests/`. Should criterion 2 also have a row showing that a file inside the guard's scope that holds none of the four strings passes, and that the guard's own file is the single exemption? I would choose a passing row for a clean file and no further row for the exemption.

   3. The Interface says a docstring or comment that writes `origin/main` for the working branch changes to "the working branch" or `origin/<working branch>`. The guard covers the string `origin/main` in `src/factory/`, so the guard would catch a leftover. Please confirm that criterion 2 is meant to be the only test of this clause. I would choose to confirm.

   Checked, no finding:
   - Interface: it names `factory.shared.domain.paths`, `WORK_BRANCH` and the derived names.
   - Criterion 1: it is one test, and both sides are covered (the new name exists with the value `main`, the old name is gone).
   - Smoke test: the command is runnable and its `Expect:` line is checkable.
   - Docs criterion: it names what the reader must know (`WORK_BRANCH` names the working branch, and no code or test writes it literally). It dictates no sentences.
   - Architecture: the change sits in the `shared` domain layer and in tests, with nothing new for the layers.
   - Scope: it matches F0057 S0001 and decision 9. The human's leave for changing earlier tests is in the Interface.
4. 2026-11-07 human: 1. Yes, as you wrote it: the guard fails on a file the test writes that holds `origin/main`, `heads/main`, `-b main` or `--initial-branch=main`, one row for each string.
   2. Yes: one passing row for a clean file inside the guard's scope, and no row for the exemption.
   3. Confirmed: criterion 2 is the only test of the docstring and comment clause.
5. factory: started intake as vm.
6. intake: accepted
   - Interface: names `factory.shared.domain.paths`, `MAIN_BRANCH` to `WORK_BRANCH` (value `main`), the derived names, the new guard file and the human's leave for earlier tests. Concrete.
   - Criteria: criterion 1 is one test covering both sides (new name has value `main`, old name gone). Criterion 2 is carried in from the human's answer (journal entry 4): one failing row per string (`origin/main`, `heads/main`, `-b main`, `--initial-branch=main`), one passing row for a clean file, and this test as the only test of the docstring and comment clause. Criterion 3 names the modules changed under the leave. Each criterion is testable. Both sides of the guard rule are present.
   - Smoke test: the command is runnable, with no pytest, so there is no `-q` issue. Its `Expect: main` is checkable.
   - Docs criterion: names what the reader must know (`WORK_BRANCH` names the working branch, and no code or test writes it literally) and dictates no sentences. The `docs/shared.md` target is a path the documenter may write.
   - Architecture: the change sits in the `shared` domain layer, the tests and one guard under `tests/guards/`. No layer rule is touched.
   - Scope: matches F0057 S0001 and decision 9, with the value unchanged and no behaviour change. The leave to change earlier tests is stated in the Interface (human, 2026-11-07).
   Route: `tests`, because the Interface changes code under `src/factory/` and tests.
   Story edit: criterion 2 reworded exactly as the human answered in journal entry 4.
7. factory: started tests as vm.
8. tester: Wrote the tests for the criteria and replaced the branch name written out in the earlier tests with the constant, as the human allowed on 2026-11-07.

   Criteria → tests:
   - criterion 1: tests/shared/domain/test_work_branch.py::test_the_working_branch_is_one_constant_named_work_branch
   - criterion 2: tests/guards/test_work_branch_search.py::test_no_file_in_the_source_or_the_tests_writes_the_working_branch_by_name (the repository) and tests/guards/test_work_branch_search.py::test_the_search_finds_each_literal_branch_name_in_a_file_in_scope (a clean row, then one failing row each for `origin/main`, `heads/main`, `-b main` and `--initial-branch=main`, in a tree under tmp_path). The guard leaves out its own file and `__pycache__` folders.
   - criterion 3: the earlier tests themselves, changed under the leave (below).
   - criteria 4 and 5: no test (`make check`, docs).

   Files created: tests/shared/domain/test_work_branch.py, tests/guards/test_work_branch_search.py.

   Earlier tests changed under the leave: 163 modules under tests/ (`git diff --stat` on this branch lists them). The change in each:
   - A string that names the branch now uses the constant: `"main"` becomes `WORK_BRANCH`; `"origin/main"` becomes `f"{REMOTE}/{WORK_BRANCH}"`; `refs/heads/main`, `--initial-branch=main` and `-b main` are built from `WORK_BRANCH`.
   - Imports from `factory.shared.domain.paths` were added.
   - `MAIN_BRANCH` is renamed `WORK_BRANCH` in tests/hosting/domain/test_hosting.py, tests/shared/domain/test_paths.py and tests/pipeline/application/test_acceptance_no_state_refusals.py.
   - In docstrings and comments, `origin/main` reads `origin/<working branch>` or "the working branch". A few of those lines were reworded slightly to stay within 100 characters.
   - `"main"` stays where it is not a branch: pytest ids, a parametrize argument name in tests/entry/test_entry_arguments.py (that file is unchanged), a commit message, and file contents such as `"main\n"`.

   Changes that go beyond replacing the name:
   - tests/hosting/adapters/test_git_cli_check_ignore.py: its own constant `WORK_BRANCH = "work"` (a work item branch) is renamed `ITEM_BRANCH`, so that it no longer shadows the paths constant.
   - tests/shared/adapters/test_tmp_path_reopening.py: the child test text `INNER_TESTS` now writes `refs/heads/<branch>`, and `.replace("<branch>", WORK_BRANCH)` is applied to it, because the text is a plain string that a child pytest writes.
   - tests/agent_files/test_claude_files.py: two `TEMPLATE_RULES_LINES` strings with `origin/main` are now f-strings built from `REMOTE` and `WORK_BRANCH`. They are split at a different place to stay within the line limit, so the joined text is unchanged. The word `main` in "every tracked file on `main` itself" stays, because the guard does not forbid it.
   - tests/entry/test_watcher_main_ref.py: `UNRESOLVED` is split over two f-string lines.

   Run: `uv run pytest -q tests/shared/domain/test_work_branch.py tests/guards/test_work_branch_search.py` fails during collection: tests/conftest.py → tests/support/acceptance_walk.py → `ImportError: cannot import name 'WORK_BRANCH' from 'factory.shared.domain.paths'`. Almost every test module now imports the constant, so the whole suite stays red until the coder renames it. This is the right reason.

   I also ran the guard's search function by hand, outside pytest. On the repository it finds 12 files that still hold a literal, all under src/factory/ and none under tests/. Some of these do not import `MAIN_BRANCH` today: project_agents.py, entry/run.py, entry/watch.py, entry/wiring.py and opening.py. The coder must change them too. On written trees it finds each of the four strings and nothing in a clean file.

   `make lint` is green. I did not run the type check, as the stage says.

   Modules the test runner could not import: `factory.shared.domain.paths.WORK_BRANCH` (the name does not exist yet).

   `lint`: lint: green (0.2 s)
