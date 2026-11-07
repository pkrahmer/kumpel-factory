---
stage: smoke-test
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 643
comments_read: [6713530910, 6713705040, 6713791298]
handed_over: null
claim:
  instance: vm
  stage: smoke-test
  started_at: '2026-11-07T22:27:19.751456Z'
  lease_duration: 60
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
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-07T22:01:18.200585Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-07T22:06:15.142507Z'
  stage: doing
  run: 2803d32adae74e23a8df939b50d3a2ea
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-07T22:06:20.282543Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-07T22:08:46.226771Z'
  stage: review
  run: bf4b923c43204665b828a5657a96e13c
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-07T22:08:51.194414Z'
  stage: doing
- number: 14
  speaker: coder
  kind: result
  at: '2026-11-07T22:09:20.796744Z'
  stage: doing
  run: d01515587b7d4c94b6c1bfd4e0b77941
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-07T22:09:26.561624Z'
  stage: tests
- number: 16
  speaker: tester
  kind: result
  at: '2026-11-07T22:09:47.701402Z'
  stage: tests
  run: 6540cd4040ff4fbe83327a2345400331
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-07T22:09:52.679855Z'
  stage: doing
- number: 18
  speaker: coder
  kind: question
  at: '2026-11-07T22:12:12.483831Z'
  stage: doing
  run: 4946c6d986a943848914638d44902e62
  blocked: question
- number: 19
  speaker: human
  kind: comment
  at: '2026-11-07T22:14:01.385317Z'
  stage: doing
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-07T22:14:03.828516Z'
  stage: doing
- number: 21
  speaker: coder
  kind: result
  at: '2026-11-07T22:18:32.309072Z'
  stage: doing
  run: 778771c663a240ed983c79bb7aed3112
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-07T22:18:37.733429Z'
  stage: review
- number: 23
  speaker: reviewer
  kind: question
  at: '2026-11-07T22:19:59.292074Z'
  stage: review
  run: c945bbe1e0934ad78c44854139498bd2
  blocked: question
- number: 24
  speaker: human
  kind: comment
  at: '2026-11-07T22:21:48.255497Z'
  stage: review
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-07T22:21:50.831777Z'
  stage: review
- number: 26
  speaker: reviewer
  kind: result
  at: '2026-11-07T22:22:37.811631Z'
  stage: review
  run: a7c7950216f848d39af3b7bed63c2602
- number: 27
  speaker: factory
  kind: started
  at: '2026-11-07T22:22:42.967750Z'
  stage: docs
- number: 28
  speaker: documenter
  kind: result
  at: '2026-11-07T22:27:14.307591Z'
  stage: docs
  run: 7dc00d3388654a30a498f823c89728a5
- number: 29
  speaker: factory
  kind: started
  at: '2026-11-07T22:27:19.751456Z'
  stage: smoke-test
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
5. docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story.

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
9. factory: started doing as vm.
10. coder: I renamed the constant for the working branch and removed every branch name written out under `src/factory/`. I changed no tests. `make check` is green: `check: green`, test coverage 99.22 %.

    What I built (24 files under `src/factory/`, 71 lines added and 70 removed):
    - `src/factory/shared/domain/paths.py`: `MAIN_BRANCH` is now `WORK_BRANCH`, still `"main"`.
    - Every module that imported `MAIN_BRANCH` now imports `WORK_BRANCH` and uses it the same way. That is task, the closed, hand_over and merged handlers, recovery, tick, stops, scheduler, pipeline_loading and stage under pipeline/application; preflight; work_items, acceptance and acceptance_reading; wiring; costs and watcher; pygithub_hosting. The derived names (`_MAIN_REF`, `_ORIGIN_MAIN`, `PIPELINE_REF`, `FORM_REF`) are still built from the constant, as the Interface says.
    - `src/factory/hosting/application/opening.py`: `_MAIN` was written as `"origin/main"`. It is now `f"{REMOTE}/{WORK_BRANCH}"`, and its error message is built from `_MAIN`.
    - `src/factory/machine/application/preflight.py`: the message `_NO_MAIN_TO_PREPARE` is now built from `_MAIN_REF`. Its text is unchanged, which the test in tests/hosting/application/test_agent_run_probe_environment.py expects.
    - Docstrings and comments that named the branch now say `origin/<working branch>` or "the working branch". These are in recovery, scheduler, stage_environment, work_items, acceptance, run, watch, wiring, watcher, opening and project_agents. Four lines were reworded or rewrapped to stay within 100 characters (run.py, wiring.py, opening.py, scheduler.py).

    Main choice: I built the two messages (opening, preflight) from the ref constants, so S0002 changes them with the one value. I rejected rewording them to "the working branch": that would change text a test checks, and the story allows no change in behaviour.

    Refactor pass: I read the diff, which is a mechanical rename plus the lines above. Nothing needed changing.

    Noticed but not touched:
    - `hand_over.py` and `stage.py` build `f"origin/{WORK_BRANCH}"` with the remote written out instead of `REMOTE`. That was there before, and the guard does not catch it.
    - Several local names still say "main" (`_MAIN_REF`, `_ORIGIN_MAIN`, `_MAIN`, `_NO_MAIN_TO_PREPARE`). The Interface keeps them, so S0002 or a later story may want to rename them.
    - The meaning of the task is unchanged by the journal, so I did not rewrite the Description. The human's answers (entry 4) are already carried into criterion 2.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
11. factory: started review as vm.
12. reviewer: Findings:

    1. `tests/entry/test_watcher_main_ref.py:1`: the reworded module docstring reads "A watch on a clone without an the working branch ends with ...". The replacement of `origin/main` left the article "an" behind, so the sentence is broken. Fix: "A watch on a clone without the working branch ends with the git error the operator reads." This is a test file, so the change is the tester's, under the human's leave of 2026-11-07.
    2. Work item, criterion 5 (docs): the criterion sends the documenter to `docs/project-guide/shared.md`, "where `paths` is described". That file does not describe `paths.py` at all: it names neither `REMOTE` nor `MAIN_BRANCH`. Meanwhile the guide still names `MAIN_BRANCH`, which this story removes, in `docs/project-guide/hosting.md:23`, `docs/project-guide/work.md:394` (the table row `REMOTE`, `MAIN_BRANCH`), `docs/project-guide/machine.md:400` and `docs/project-guide/pipeline.md:624`, `:640`, `:641` and `:773`. A documenter who follows the criterion would leave all of these stale. Fix: rewrite criterion 5 so that it names these files, says `MAIN_BRANCH` is now `WORK_BRANCH` in each, and puts the sentence "`WORK_BRANCH` names the working branch; no code or test writes the name literally" where the constant is already described (`hosting.md:23` or `work.md:394`), not in `shared.md`.

    What I checked and found sound:
    - Criterion 1: `tests/shared/domain/test_work_branch.py` checks that `WORK_BRANCH == "main"` and that `paths` has no `MAIN_BRANCH`. Both sides are in one test.
    - Criterion 2: `tests/guards/test_work_branch_search.py` has a test that the repository passes, and one parametrized test with a clean row and one failing row for each of the four strings. The search skips its own file, as the Interface allows.
    - Criterion 3: the coder's `make check` was green (journal entry 10). No `def test_` line is removed or renamed in the diff. In the test changes that are not a plain replacement, the code checks the same things: formatter reflows, `ITEM_BRANCH`, `INNER_TESTS` and `UNRESOLVED`. The tester named each of these in entry 8.
    - `src/`: every `MAIN_BRANCH` is now `WORK_BRANCH`. The derived refs (`_MAIN_REF`, `_ORIGIN_MAIN`, `PIPELINE_REF`, `FORM_REF`, `_MAIN` in `opening.py`) are built from the constant. Every docstring and comment that wrote `origin/main` now names the working branch. No other branch literal is left.
    - Architecture: no new imports between layers; the constant stays in `shared.domain`.
    - Security: no suppression markers and no strings built for a shell.
    - Duplicates: `make duplicates` reports 6 new findings. All 6 are in code this diff does not change (`claude_runtime`/`opencode_runtime`, `folder_readmes.py`, `cost_records.py`), or they are a known pair listed in the other order (`hand_over`/`acceptance`). None comes from this story.
    - Left out of scope on purpose, not findings: the prose messages that still say "main" (`src/factory/pipeline/application/scheduler.py:135`, `stops.py:123`, `stage.py:162`). The Interface covers only `origin/main` in docstrings and comments, and changing a message would change behaviour.

    Earlier tests (all 163 are status M; no tests were renamed or deleted):
    - `tests/agent_files/test_claude_files.py`: the human's leave (Interface, 2026-11-07). Beyond the replacement: two `TEMPLATE_RULES_LINES` strings are now f-strings and split at a different place; the joined text is unchanged (named in entry 8).
    - `tests/entry/test_watcher_main_ref.py`: the human's leave. `UNRESOLVED` is split over two f-string lines (named in entry 8); the docstring slip is finding 1.
    - `tests/hosting/adapters/test_git_cli_check_ignore.py`: the human's leave. Beyond the replacement: its local `WORK_BRANCH = "work"` is renamed `ITEM_BRANCH` so it does not shadow the constant (named in entry 8).
    - `tests/shared/adapters/test_tmp_path_reopening.py`: the human's leave. Beyond the replacement: `INNER_TESTS` writes `<branch>`, which is filled in with `.replace` (named in entry 8).
    - Each of the following: the human's leave (Interface, 2026-11-07); a literal branch name is replaced by `WORK_BRANCH`/`REMOTE`, or `MAIN_BRANCH` by `WORK_BRANCH`:
    - `tests/agent_files/test_template_makefile.py`
    - `tests/agents/adapters/test_claude_runtime_environment.py`
    - `tests/agents/application/test_agent_run_probe.py`
    - `tests/agents/application/test_agent_run_probe_project_agent.py`
    - `tests/agents/application/test_project_agents.py`
    - `tests/entry/test_board_reader_acceptance.py`
    - `tests/entry/test_git_hooks.py`
    - `tests/entry/test_run.py`
    - `tests/entry/test_run_fetch_before_tick.py`
    - `tests/entry/test_run_image_sizes.py`
    - `tests/entry/test_run_one_fetch.py`
    - `tests/entry/test_run_project_image_rebuild.py`
    - `tests/entry/test_run_waiter.py`
    - `tests/entry/test_tick_agent_definition.py`
    - `tests/entry/test_tick_project_agent.py`
    - `tests/entry/test_tick_shipped_agent_file.py`
    - `tests/entry/test_watch.py`
    - `tests/entry/test_watch_acceptance.py`
    - `tests/entry/test_watch_main.py`
    - `tests/entry/test_wiring_acceptance.py`
    - `tests/entry/test_wiring_container_extra.py`
    - `tests/entry/test_wiring_environment.py`
    - `tests/entry/test_wiring_extras.py`
    - `tests/entry/test_wiring_handlers.py`
    - `tests/entry/test_wiring_human_handlers.py`
    - `tests/entry/test_wiring_image_path.py`
    - `tests/entry/test_wiring_preflight.py`
    - `tests/entry/test_wiring_project_agents.py`
    - `tests/entry/test_wiring_project_image.py`
    - `tests/entry/test_wiring_run.py`
    - `tests/entry/test_wiring_stage_image_sizes.py`
    - `tests/guards/test_git_support.py`
    - `tests/guards/test_human_clone.py`
    - `tests/guards/test_proof_support.py`
    - `tests/guards/test_suite_fixtures.py`
    - `tests/hosting/adapters/test_git_cli_arguments.py`
    - `tests/hosting/adapters/test_git_cli_branches.py`
    - `tests/hosting/adapters/test_git_cli_history.py`
    - `tests/hosting/adapters/test_git_cli_reading.py`
    - `tests/hosting/adapters/test_git_cli_restoring.py`
    - `tests/hosting/adapters/test_git_cli_seal.py`
    - `tests/hosting/adapters/test_git_cli_work_tree.py`
    - `tests/hosting/adapters/test_git_cli_writing.py`
    - `tests/hosting/adapters/test_pygithub_hosting.py`
    - `tests/hosting/application/test_acceptance_ticks_repeated.py`
    - `tests/hosting/application/test_agent_run_probe_environment.py`
    - `tests/hosting/application/test_checkout_preparer.py`
    - `tests/hosting/application/test_costs.py`
    - `tests/hosting/application/test_hosting_failure_releases_claim.py`
    - `tests/hosting/application/test_opening.py`
    - `tests/hosting/application/test_preflight_stale_main_stop.py`
    - `tests/hosting/application/test_watcher.py`
    - `tests/hosting/domain/test_git.py`
    - `tests/hosting/domain/test_hosting.py`
    - `tests/machine/application/test_container_environment.py`
    - `tests/machine/application/test_preflight_login_line.py`
    - `tests/machine/application/test_preflight_run.py`
    - `tests/operator_scripts/test_operator_merge_reset.py`
    - `tests/operator_scripts/test_operator_skill_scripts.py`
    - `tests/operator_scripts/test_operator_skill_signature.py`
    - `tests/pipeline/application/handlers/test_closed.py`
    - `tests/pipeline/application/handlers/test_hand_over.py`
    - `tests/pipeline/application/handlers/test_handler_subjects.py`
    - `tests/pipeline/application/handlers/test_lookups.py`
    - `tests/pipeline/application/handlers/test_merged.py`
    - `tests/pipeline/application/handlers/test_reject.py`
    - `tests/pipeline/application/handlers/test_run.py`
    - `tests/pipeline/application/handlers/test_run_gate.py`
    - `tests/pipeline/application/test_acceptance_due_handler.py`
    - `tests/pipeline/application/test_acceptance_hand_over.py`
    - `tests/pipeline/application/test_acceptance_merged.py`
    - `tests/pipeline/application/test_acceptance_no_state_refusals.py`
    - `tests/pipeline/application/test_after_agent.py`
    - `tests/pipeline/application/test_claims.py`
    - `tests/pipeline/application/test_claims_refusals.py`
    - `tests/pipeline/application/test_container_environment_take.py`
    - `tests/pipeline/application/test_container_sync_origin.py`
    - `tests/pipeline/application/test_docs_route.py`
    - `tests/pipeline/application/test_human_line_posts.py`
    - `tests/pipeline/application/test_known_results.py`
    - `tests/pipeline/application/test_no_state_refusals.py`
    - `tests/pipeline/application/test_opening_journal_edges.py`
    - `tests/pipeline/application/test_pipeline_loading.py`
    - `tests/pipeline/application/test_pipeline_loading_agents.py`
    - `tests/pipeline/application/test_pipeline_loading_project_agents.py`
    - `tests/pipeline/application/test_pipeline_loading_rules.py`
    - `tests/pipeline/application/test_pipeline_loading_stage_moves.py`
    - `tests/pipeline/application/test_pipeline_loading_strict_values.py`
    - `tests/pipeline/application/test_pipeline_loading_yaml_fault.py`
    - `tests/pipeline/application/test_preflight_stops_commit.py`
    - `tests/pipeline/application/test_probe_nested_repository.py`
    - `tests/pipeline/application/test_recovery_cap.py`
    - `tests/pipeline/application/test_recovery_crash.py`
    - `tests/pipeline/application/test_repository_waiter.py`
    - `tests/pipeline/application/test_scheduler.py`
    - `tests/pipeline/application/test_stage_changes.py`
    - `tests/pipeline/application/test_stage_environment_of.py`
    - `tests/pipeline/application/test_stage_finish.py`
    - `tests/pipeline/application/test_stage_known_results.py`
    - `tests/pipeline/application/test_stage_launch.py`
    - `tests/pipeline/application/test_stage_nested_repository.py`
    - `tests/pipeline/application/test_stage_run.py`
    - `tests/pipeline/application/test_stage_run_acceptance.py`
    - `tests/pipeline/application/test_stale_branches.py`
    - `tests/pipeline/application/test_stall_edges.py`
    - `tests/pipeline/application/test_stall_labels.py`
    - `tests/pipeline/application/test_stall_reasons_recorded.py`
    - `tests/pipeline/application/test_stop_posting.py`
    - `tests/pipeline/application/test_stop_publisher.py`
    - `tests/pipeline/application/test_take.py`
    - `tests/pipeline/application/test_take_edges.py`
    - `tests/pipeline/application/test_task.py`
    - `tests/pipeline/application/test_task_acceptance.py`
    - `tests/pipeline/application/test_tick.py`
    - `tests/pipeline/application/test_tick_disk.py`
    - `tests/pipeline/application/test_tick_preflight.py`
    - `tests/pipeline/application/test_tick_restore_ignored.py`
    - `tests/pipeline/application/test_tick_stale_branch.py`
    - `tests/pipeline/application/test_tick_stop_records.py`
    - `tests/pipeline/application/test_watcher_acceptance.py`
    - `tests/shared/application/test_acceptance_reviewer_role.py`
    - `tests/shared/domain/test_approval_description.py`
    - `tests/shared/domain/test_document_references.py`
    - `tests/shared/domain/test_fault_paths_7_to_13.py`
    - `tests/shared/domain/test_identifiers.py`
    - `tests/shared/domain/test_paths.py`
    - `tests/support/acceptance_walk.py`
    - `tests/support/container_extra_support.py`
    - `tests/support/container_support.py`
    - `tests/support/cost_image_support.py`
    - `tests/support/crash_support.py`
    - `tests/support/git_support.py`
    - `tests/support/human_clone.py`
    - `tests/support/operator_skill_support.py`
    - `tests/support/preflight_support.py`
    - `tests/support/proof_support.py`
    - `tests/support/stage_run_support.py`
    - `tests/support/stall_support.py`
    - `tests/support/undo_support.py`
    - `tests/support/watch_support.py`
    - `tests/support/work_item_support.py`
    - `tests/support/write_path_support.py`
    - `tests/watching/application/test_acceptance_ticks_merged.py`
    - `tests/watching/application/test_bill_service.py`
    - `tests/watching/application/test_board_in_progress.py`
    - `tests/work/application/test_acceptance_closed.py`
    - `tests/work/application/test_acceptance_facts_human.py`
    - `tests/work/application/test_acceptance_merged_before_approval.py`
    - `tests/work/application/test_acceptance_merged_on_two_routes.py`
    - `tests/work/application/test_acceptance_reading.py`
    - `tests/work/application/test_acceptance_refusals.py`
    - `tests/work/application/test_acceptance_repeated.py`
    - `tests/work/application/test_acceptance_service.py`
    - `tests/work/application/test_acceptance_snapshots.py`
    - `tests/work/application/test_board_reader.py`
    - `tests/work/application/test_watcher_move_rule.py`
    - `tests/work/application/test_work_items.py`
    - `tests/work/application/test_work_items_duplicate.py`
    - `tests/work/domain/test_stop_table.py`
13. factory: started doing as vm.
14. coder: Round 1: I worked on the reviewer's two findings from entry 12 and changed no code under `src/factory/`.

    Test change for the tester (finding 1): in `tests/entry/test_watcher_main_ref.py`, the first line, the module docstring, should read "A watch on a clone without the working branch ends with the git error the operator reads." The stray "an" goes. The human's leave of 2026-11-07 covers this change. Under R9 I do not edit tests, so the tester makes it.

    Finding 2 (criterion 5): I rewrote criterion 5 in this work item as the reviewer proposed, because the old text sent the documenter to `docs/project-guide/shared.md`, and that file does not describe `paths`. Before rewriting it I checked the guide. It still names `MAIN_BRANCH` in these places:
    - `docs/project-guide/hosting.md:23`
    - `docs/project-guide/work.md:394` (the table of constants in `paths`)
    - `docs/project-guide/machine.md:400`
    - `docs/project-guide/pipeline.md:624`, `:640`, `:641` and `:773`

    The new criterion 5 names those files. It asks for `MAIN_BRANCH` to become `WORK_BRANCH` in each. It puts the sentence about `WORK_BRANCH` naming the working branch, with no code or test writing it literally, where the constant is already described: `work.md`'s table or `hosting.md`. The meaning of the task is otherwise unchanged. If my write paths do not include the work item, this edit is dropped and the criterion needs the human.

    Main choice: I sent finding 1 to the tester with the `tests` decision. I rejected asking the human, because the leave already covers this kind of change.

    Not run: `make check`. Since the green run in entry 10, nothing that `make check` reads has changed; the only change is the work item.

    Noticed but not touched (same as entry 10):
    - `hand_over.py` and `stage.py` build `f"origin/{WORK_BRANCH}"` with the remote's name written out instead of `REMOTE`.
    - Some local names still say "main": `_MAIN_REF`, `_ORIGIN_MAIN`, `_MAIN` and `_NO_MAIN_TO_PREPARE`.

    The factory left out changes outside the write paths: factory/features/F0057-the-factory-works-on-develop/in-progress/F0057-S0001-the-tests-name-the-working-branch-through-one-constant.md.
15. factory: started tests as vm.
16. tester: Approved test change (finding 1 from entry 12, passed on in the coder's entry 14, covered by the human's leave of 2026-11-07). I fixed the module docstring on the first line of `tests/entry/test_watcher_main_ref.py`. It now reads "A watch on a clone without the working branch ends with the git error the operator reads." The stray "an" is gone.

    Nothing else changed: no test function, assertion or other file. No criterion's mapping changes, and I created no files. The test runner imported every module.

    Checks run after the change:
    - `uv run pytest -q tests/entry/test_watcher_main_ref.py` passed (2 tests).
    - `make lint` is green.

    `lint`: lint: green (0.2 s)
17. factory: started doing as vm.
18. coder: Round 1, after the tester's fix. Finding 1 from entry 12 is done: the tester fixed the docstring in `tests/entry/test_watcher_main_ref.py` (entry 16). `make check` is green on this branch (`check: green`, coverage 99.22 %). I did not change any code under `src/factory/` in this round. The code is as described in entry 10.

    Finding 2 from entry 12 is still open, and I cannot close it. The finding asks for criterion 5 (docs) to be rewritten. My rewrite in entry 14 was dropped, because the work item is outside the coder's write paths (R14). Criterion 5 still sends the documenter to `docs/project-guide/shared.md`, "where `paths` is described". That file does not describe `paths`. The guide still names the removed `MAIN_BRANCH` in these places:
    - `docs/project-guide/hosting.md:23`
    - `docs/project-guide/work.md:394` (the `paths` constants table)
    - `docs/project-guide/machine.md:400`
    - `docs/project-guide/pipeline.md:624`, `:640`, `:641` and `:773`

    Question: how should criterion 5 read?
    - (a) I would choose this one. Replace it with: "docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story." Please commit it on the branch, or tell me which stage may write it.
    - (b) Keep criterion 5 as it is, and let the documenter also fix the stale `MAIN_BRANCH` names it finds. The risk is that the documenter follows the text literally and adds a `paths` section to `shared.md` while the stale names stay.
    - (c) Leave the stale names for S0002, which changes the same lines again.

    Once the criterion is settled, there is nothing left for the coder. The next decision would be `review`.

    Noticed but not touched (as in entry 10):
    - `hand_over.py` and `stage.py` build `f"origin/{WORK_BRANCH}"` with the remote's name written out, not from `REMOTE`.
    - The local names `_MAIN_REF`, `_ORIGIN_MAIN`, `_MAIN` and `_NO_MAIN_TO_PREPARE` still say "main".

    `check`: check: green
19. 2026-11-07 human: (a). Criterion 5 reads from now on: "docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story." The human does not commit on the work item's branch; this answer is the criterion's text for every later stage, and the documenter writes the docs. My earlier text sent the reader to shared.md by mistake; it does not describe `paths`. The two notes (the remote's name written out, the local names that say main) stay for S0002.
20. factory: started doing as vm.
21. coder: Round 1, after the human's answer in entry 19. I changed no code and no tests in this run.

    What the journal changed: the human chose option (a). Criterion 5 now reads: "docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story." I did not rewrite `## Description`, because the work item is outside the coder's write paths. Entry 19 holds the criterion's text for every later stage, and the documenter writes the docs. The stale `MAIN_BRANCH` names in the guide are listed in entry 18: `hosting.md:23`, `work.md:394`, `machine.md:400`, `pipeline.md:624/640/641/773`.

    Both findings from entry 12 are now settled:
    - Finding 1: the tester fixed the docstring (entry 16).
    - Finding 2: settled by the human's answer above.

    The code is as entry 10 describes it. Nothing to refactor.

    Noticed but not touched; the human left both for S0002 (entry 19):
    - `hand_over.py` and `stage.py` write the remote's name out in `f"origin/{WORK_BRANCH}"` instead of building it from `REMOTE`.
    - The local names `_MAIN_REF`, `_ORIGIN_MAIN`, `_MAIN` and `_NO_MAIN_TO_PREPARE` still say "main".

    `make check`: `check: green`, coverage 99.22 %.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
22. factory: started review as vm.
23. reviewer: Round 1 review. The code and tests have no findings. One problem is still open, and no stage can fix it: finding 2 from entry 12, against criterion 5 (the docs criterion). So I am asking instead of sending the work item back to `doing`.

    Question: criterion 5 still sends the documenter to `docs/project-guide/shared.md`, "where `paths` is described". That file does not describe `paths`. The constants of `paths` are described in `docs/project-guide/work.md:7` and in its table at `work.md:394` (`REMOTE`, `MAIN_BRANCH`). The guide also still names the removed `MAIN_BRANCH` in four more files: `docs/project-guide/hosting.md:23`, `docs/project-guide/machine.md:400`, and `docs/project-guide/pipeline.md:624`, `:640`, `:641` and `:773`. The coder rewrote the criterion in entry 14, but the factory dropped the edit because the work item is outside the coder's write paths. My own leave covers only the Description and new criteria, not the rewording of a criterion. How should criterion 5 read?
    - (a) This is my choice. "docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally; `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story." Answer "(a)", and the next review run writes it into criterion 5 and passes with `docs`. You can also commit it on the branch yourself.
    - (b) Keep criterion 5 as it is. The risk: a documenter who follows it literally adds a `paths` section to `shared.md`, and four guide files keep naming a constant that no longer exists.
    - (c) Leave the stale names for S0002, which changes the same lines anyway. The guide would be wrong in the meantime.

    Checked in this round, no findings:
    - Criterion 1: `tests/shared/domain/test_work_branch.py` checks in one test that `WORK_BRANCH == "main"` and that `MAIN_BRANCH` no longer exists.
    - Criterion 2: `tests/guards/test_work_branch_search.py` has two tests.
      - One checks that the repository passes.
      - The other is one parametrized test with a clean row and one failing row each for `origin/main`, `heads/main`, `-b main` and `--initial-branch=main`.
      - The search skips only its own file and `__pycache__`.
      - `grep` finds `MAIN_BRANCH` nowhere under `src/` or `tests/` except the criterion 1 test.
    - Criterion 3: no `def test_` line is removed or renamed in the diff. The coder's `make check` after the merge of `origin/main` was green (entry 18).
    - The tester fixed round 0's finding 1 (the stray "an" in the `tests/entry/test_watcher_main_ref.py` docstring) in entry 16.
    - `src/`, read in full:
      - every `MAIN_BRANCH` is now `WORK_BRANCH`;
      - `_MAIN_REF`, `_ORIGIN_MAIN`, `PIPELINE_REF`, `FORM_REF` and `_MAIN` in `opening.py` are built from the constant;
      - the messages in `opening.py` and `preflight.py` are built from those refs, with their text unchanged;
      - docstrings and comments now say `origin/<working branch>` or "the working branch".
    - Architecture: no new imports between layers.
    - Security: no markers, no shell strings.
    - Out of scope, not findings:
      - `hand_over.py` and `stage.py` still write the remote as `"origin/"`, which was already so on `main`;
      - local names still say "main" (`_MAIN_REF`, `_ORIGIN_MAIN`, `_MAIN`, `_NO_MAIN_TO_PREPARE`), which the Interface keeps.

    Earlier tests: all 163 have status M; none was renamed or deleted. Each was changed under the human's leave in the Interface (2026-11-07).
    - Changes that go beyond the replacement, all named in entry 8:
      - `tests/agent_files/test_claude_files.py`: two `TEMPLATE_RULES_LINES` f-strings are split at a new place; the joined text is unchanged.
      - `tests/entry/test_watcher_main_ref.py`: `UNRESOLVED` is split over two f-string lines, and the docstring is fixed (entry 16).
      - `tests/hosting/adapters/test_git_cli_check_ignore.py`: its local `WORK_BRANCH` is renamed `ITEM_BRANCH`.
      - `tests/shared/adapters/test_tmp_path_reopening.py`: `INNER_TESTS` holds a `<branch>` placeholder that `.replace` fills in.
    - In every other file, a literal branch name became `WORK_BRANCH`/`REMOTE`, or `MAIN_BRANCH` became `WORK_BRANCH`. By folder:
      - `tests/agent_files/`: test_template_makefile.py
      - `tests/agents/`: adapters/test_claude_runtime_environment.py, application/test_agent_run_probe.py, application/test_agent_run_probe_project_agent.py, application/test_project_agents.py
      - `tests/entry/`: test_board_reader_acceptance.py, test_git_hooks.py, test_run.py, test_run_fetch_before_tick.py, test_run_image_sizes.py, test_run_one_fetch.py, test_run_project_image_rebuild.py, test_run_waiter.py, test_tick_agent_definition.py, test_tick_project_agent.py, test_tick_shipped_agent_file.py, test_watch.py, test_watch_acceptance.py, test_watch_main.py, test_wiring_acceptance.py, test_wiring_container_extra.py, test_wiring_environment.py, test_wiring_extras.py, test_wiring_handlers.py, test_wiring_human_handlers.py, test_wiring_image_path.py, test_wiring_preflight.py, test_wiring_project_agents.py, test_wiring_project_image.py, test_wiring_run.py, test_wiring_stage_image_sizes.py
      - `tests/guards/`: test_git_support.py, test_human_clone.py, test_proof_support.py, test_suite_fixtures.py
      - `tests/hosting/adapters/`: test_git_cli_arguments.py, test_git_cli_branches.py, test_git_cli_history.py, test_git_cli_reading.py, test_git_cli_restoring.py, test_git_cli_seal.py, test_git_cli_work_tree.py, test_git_cli_writing.py, test_pygithub_hosting.py
      - `tests/hosting/application/`: test_acceptance_ticks_repeated.py, test_agent_run_probe_environment.py, test_checkout_preparer.py, test_costs.py, test_hosting_failure_releases_claim.py, test_opening.py, test_preflight_stale_main_stop.py, test_watcher.py
      - `tests/hosting/domain/`: test_git.py, test_hosting.py
      - `tests/machine/application/`: test_container_environment.py, test_preflight_login_line.py, test_preflight_run.py
      - `tests/operator_scripts/`: test_operator_merge_reset.py, test_operator_skill_scripts.py, test_operator_skill_signature.py
      - `tests/pipeline/application/handlers/`: test_closed.py, test_hand_over.py, test_handler_subjects.py, test_lookups.py, test_merged.py, test_reject.py, test_run.py, test_run_gate.py
      - `tests/pipeline/application/`: test_acceptance_due_handler.py, test_acceptance_hand_over.py, test_acceptance_merged.py, test_acceptance_no_state_refusals.py, test_after_agent.py, test_claims.py, test_claims_refusals.py, test_container_environment_take.py, test_container_sync_origin.py, test_docs_route.py, test_human_line_posts.py, test_known_results.py, test_no_state_refusals.py, test_opening_journal_edges.py, test_pipeline_loading.py, test_pipeline_loading_agents.py, test_pipeline_loading_project_agents.py, test_pipeline_loading_rules.py, test_pipeline_loading_stage_moves.py, test_pipeline_loading_strict_values.py, test_pipeline_loading_yaml_fault.py, test_preflight_stops_commit.py, test_probe_nested_repository.py, test_recovery_cap.py, test_recovery_crash.py, test_repository_waiter.py, test_scheduler.py, test_stage_changes.py, test_stage_environment_of.py, test_stage_finish.py, test_stage_known_results.py, test_stage_launch.py, test_stage_nested_repository.py, test_stage_run.py, test_stage_run_acceptance.py, test_stale_branches.py, test_stall_edges.py, test_stall_labels.py, test_stall_reasons_recorded.py, test_stop_posting.py, test_stop_publisher.py, test_take.py, test_take_edges.py, test_task.py, test_task_acceptance.py, test_tick.py, test_tick_disk.py, test_tick_preflight.py, test_tick_restore_ignored.py, test_tick_stale_branch.py, test_tick_stop_records.py, test_watcher_acceptance.py
      - `tests/shared/`: application/test_acceptance_reviewer_role.py, domain/test_approval_description.py, domain/test_document_references.py, domain/test_fault_paths_7_to_13.py, domain/test_identifiers.py, domain/test_paths.py
      - `tests/support/`: acceptance_walk.py, container_extra_support.py, container_support.py, cost_image_support.py, crash_support.py, git_support.py, human_clone.py, operator_skill_support.py, preflight_support.py, proof_support.py, stage_run_support.py, stall_support.py, undo_support.py, watch_support.py, work_item_support.py, write_path_support.py
      - `tests/watching/application/`: test_acceptance_ticks_merged.py, test_bill_service.py, test_board_in_progress.py
      - `tests/work/application/`: test_acceptance_closed.py, test_acceptance_facts_human.py, test_acceptance_merged_before_approval.py, test_acceptance_merged_on_two_routes.py, test_acceptance_reading.py, test_acceptance_refusals.py, test_acceptance_repeated.py, test_acceptance_service.py, test_acceptance_snapshots.py, test_board_reader.py, test_watcher_move_rule.py, test_work_items.py, test_work_items_duplicate.py
      - `tests/work/domain/`: test_stop_table.py
24. 2026-11-07 human: (a). Write it into criterion 5 as you proposed, the same text I gave the coder above.
25. factory: started review as vm.
26. reviewer: Round 1 review, after the human's answer in entry 24. No findings.

    Criterion 5 written as the human asked in entry 24 (the text the human gave in entry 19). It said: "docs: `docs/project-guide/shared.md`, where `paths` is described: the reader learns that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `docs/decisions.md`: none in this story." It now says: "docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_BRANCH` in place of `MAIN_BRANCH`, and the reader learns there that `WORK_BRANCH` names the factory's working branch and that no code or test writes the name literally. `hosting.md`, `machine.md` and `pipeline.md` name `WORK_BRANCH` wherever they named `MAIN_BRANCH`. `docs/decisions.md`: none in this story." I changed nothing else in the work item. This closes finding 2 from entry 12. Finding 1 was closed by the tester in entry 16.

    Checked in this run:
    - Since the review in entry 23, the only change outside `factory/` is `docs/runs/2026-11-05-f0052/log.md`. It came in with the merge of `origin/main` (aaf537e26). It is the human's file and not under review.
    - `MAIN_BRANCH` is now named under `src/` and `tests/` only in the criterion 1 test (`tests/shared/domain/test_work_branch.py:9`).
    - No `.py` file under `src/` or `tests/` holds `origin/main`, `heads/main`, `-b main` or `--initial-branch=main`, apart from the guard itself.
    - The rest of the review in entry 23 still holds: criteria 1 to 3, `src/`, architecture and security, with no findings. The coder's `make check` was green (entry 21).
    - The Description still matches what was built. I did not run `make check`, as the stage says.

    For the documenter, the stale `MAIN_BRANCH` names in the guide: `docs/project-guide/hosting.md:23`, `work.md:394`, `machine.md:400`, `pipeline.md:624`, `:640`, `:641` and `:773`.

    Earlier tests: all 163 have status M; none was renamed or deleted. Each was changed under the human's leave in the Interface (2026-11-07). Entry 23 lists them one by one. Four changes go beyond the plain replacement, all named in entry 8 and all within the leave:
    - `tests/agent_files/test_claude_files.py`
    - `tests/entry/test_watcher_main_ref.py`, including the docstring fix of entry 16
    - `tests/hosting/adapters/test_git_cli_check_ignore.py`
    - `tests/shared/adapters/test_tmp_path_reopening.py`
27. factory: started docs as vm.
28. documenter: Docs stage, round 1, for the docs criterion (criterion 5). I read the story, the diff outside `factory/`, `docs/` and `README.md`, and the guide. `make documents` ended with `documents ok (58.2 s)`. I did not run `make check`, because I changed only documents.

    Files changed:
    - `docs/project-guide/work.md`: the `paths` table row now reads `REMOTE`, `WORK_BRANCH`. I added one bullet saying that `WORK_BRANCH` names the factory's working branch. The bullet also says no code under `src/factory/` and no test writes the name literally, and that `tests/guards/test_work_branch_search.py` fails on `origin/main`, `heads/main`, `-b main` and `--initial-branch=main`.
    - `docs/project-guide/hosting.md` (line 23), `machine.md` (line 400) and `pipeline.md` (lines 624, 640, 641, 773): `MAIN_BRANCH` renamed to `WORK_BRANCH`, the same seven places the reviewer listed. No `MAIN_BRANCH` is left in `README.md` or `docs/`, outside `docs/runs/`, which is the human's.

    Cross-read and found current:
    - `docs/project-guide/watching.md`, `docs/project-guide/shared.md`, the rest of `machine.md` and `docs/operator-guide/` write `origin/main` as the branch's value. That is still true, because the value is still `main`, so I left it. S0002 will have to revisit those passages when it changes the value.
    - `README.md`.

    I read `src/factory/shared/domain/paths.py`: `WORK_BRANCH = "main"`.

    `docs/decisions.md` has no change, as the criterion says.

    Findings for the coder: none. Nothing stale and unrelated to this story stood out.

    `check`: check: green
    `secrets`: secrets: green (4.6 s)
    `documents`: documents ok (59.4 s)
29. factory: started smoke-test as vm.
