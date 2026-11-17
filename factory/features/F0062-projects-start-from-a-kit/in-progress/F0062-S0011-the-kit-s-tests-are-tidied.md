---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 701
comments_read: [6939751878]
handed_over: null
claim:
  instance: self
  stage: doing
  started_at: '2026-11-17T05:45:14.509124Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T05:38:58.529519Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T05:38:58.537618Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T05:39:31.445319Z'
  stage: intake
  run: 8a146b5ced6845ab869b0b28693c073c
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T05:40:17.949775Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T05:40:20.468239Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T05:40:48.823082Z'
  stage: intake
  run: 57ce641c905b4684adafa9f39a182bc3
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T05:40:54.169919Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T05:45:08.976552Z'
  stage: tests
  run: 0992ac31acbd411e8e0de2bfc15e8450
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T05:45:14.509124Z'
  stage: doing
---

# The feature's tests are tidied: one missing row, one weak check, one copy, and names that still say template

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

## Description

The reviewers of the feature's stories left notes on its tests that were not findings, and the leaves of S0007 and S0008 kept names that no longer say what a test checks. In the conformance check's tests, no row has a definition that already names `sync` among its project commands. `_assert_named` in the `make_file` tests checks only that `-f` appears somewhere, not that the sync and the command each get it. `tests/agent_files/test_installed_builder.py` asserts the same heading twice, once as a whole line of the body and once as text of the Stage section. `tests/operator_scripts/test_packs.py` holds a second copy of the Dockerfile instruction reader that `tests/support/dockerfile_support.py` keeps private. Three modules under `tests/agent_files/` are still named for the removed template although they test the kit and the Python pack, and a guard's name says "ten topics" where it checks eleven. After this story each of these is fixed. No module under `src/factory/` changes, and no test checks less than it did. This is a tests-only story; the coder has nothing to build and only runs the checks.

## Interface

- No module under `src/factory/` changes.
- `tests/pipeline/application/test_project_check_run.py`: a parametrized test with two rows for a definition whose `project_commands` name `sync`: with a `sync` target the point `makefile` has no fault, and without one it has exactly the fault `no target sync`, once.
- `tests/machine/adapters/test_make_commands_make_file.py`: `_assert_named` checks that the named makefile is passed to the sync and to the command, each on its own.
- `tests/agent_files/test_installed_builder.py`: of the two assertions on the same heading (near lines 65 and 66), the second (`in points`) goes, and the first keeps its whole-line check but is aimed at the Stage section: `"\n### The project's review points\n" in f"\n{points}\n"`.
- `tests/support/dockerfile_support.py`: its reader of instructions gets a public name. `tests/operator_scripts/test_packs.py` uses it in place of its own `_instructions`.
- Renames, each keeping every test function's name but the one below and what it checks: `tests/agent_files/test_template_makefile.py` → `test_python_pack_makefile.py`, `test_template_makefile_header.py` → `test_python_pack_makefile_header.py`, `test_template_sync.py` → `test_python_pack_sync.py`, and `tests/support/template_make_support.py` → `tests/support/kit_make_support.py` with its importers; `tests/guards/test_template_removed.py` keeps its name, since its subject is the template's removal; in `tests/guards/test_operator_guide_files.py`, `test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics` → `..._and_its_topics`.
- These change tests other stories wrote, beyond the standing leave. The human's leave (journal entry 4): "the tester may make exactly the changes this story's Interface names to the earlier tests it names, each test keeping what it checks".

## Acceptance criteria

1. The two `sync` rows of the Interface pass: with a `sync` target the `makefile` point is `ok`, and without one its faults are exactly `["no target sync"]`.
2. `_assert_named` fails for a run where only the sync gets `-f <path>`, and for one where only the command gets it; it passes when both get it.
3. `tests/operator_scripts/test_packs.py` defines no function of its own that reads Dockerfile instructions; it imports the public reader from `tests/support/dockerfile_support.py`.
4. `git ls-files tests | grep template` prints only `tests/guards/test_template_removed.py`, no test function's name under `tests/guards/` says `ten_topics`, and the renamed modules hold the same test function names as before.
5. The reviewer test in `tests/agent_files/test_installed_builder.py` asserts the heading `### The project's review points` once, as a whole line of the Stage section.
6. `make check` stays green.
7. docs: the project guide names and links the kit's make support module under its new name, `tests/support/kit_make_support.py`.

## Smoke test

```bash
git ls-files tests | grep template
```
Expect: one line, `tests/guards/test_template_removed.py`.

```bash
uv run pytest tests/pipeline/application/test_project_check_run.py tests/operator_scripts/test_packs.py 2>&1 | tail -1
```
Expect: one line ending with `passed` and a time, with no `failed`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: 1. The leave. The Interface gives the leave for changing other stories' tests only as "proposed wording", and the journal has no entry from the human that gives it. CLAUDE.md lists a change to a test you did not write, beyond the standing leave, under "Not without asking". Do you give the leave as worded ("the tester may make exactly the changes this story's Interface names to the earlier tests it names, each test keeping what it checks")? If so, should it go into the Interface as your word, in place of "proposed wording"? I would carry it in exactly as worded.
   2. The docs criterion is wrong. Criterion 6 says none of the four documents names the renamed modules. `docs/project-guide/agents.md:404` and `docs/project-guide/README.md:192` both link to `tests/support/template_make_support.py`. Once it is renamed to `kit_make_support.py`, those links break, and the docs stage's `make documents` gate checks links. Options: (a) rewrite criterion 6 as "docs: the project guide names and links the kit's make support module under its new name, `tests/support/kit_make_support.py`", which makes the story take the documenter's stage; (b) keep the old module name, which drops one rename. I would choose (a).
   3. The `test_installed_builder.py` change has no criterion, and it may check less. Line 65 asserts `"\n### The project's review points\n" in f"\n{body}\n"`, meaning the heading is a line of its own somewhere in the body. Line 66 asserts only that the text appears in the Stage section. The two are not the same check. Removing line 65 loses the "line of its own" part, which goes against "no test checks less than it did". Options: (a) remove line 66 and keep line 65's whole-line check, but aimed at `points` (`"\n### The project's review points\n" in f"\n{points}\n"`), and add a criterion: "the reviewer test asserts the heading once, as a whole line of the Stage section"; (b) drop this item from the story. I would choose (a).
   4. A minor gap: no criterion covers keeping each renamed module's test functions under the same names (Interface: "each keeping every test function's name"). Should criterion 4 add "and the renamed modules hold the same test function names as before"? I would add it.

   Checks I made, which raised no question: the smoke test is runnable (`addopts` already sets `-q`, and the command passes none, so the summary line prints). Every file the Interface names exists as described: `_instructions` sits in both `test_packs.py:94` and `dockerfile_support.py:61`; `_assert_named` checks only `"-f" in script or "-f" in arguments`; the guard is named `..._ten_topics`. The architecture is fine (tests only, and the shared reader is in `tests/support/`). The scope is within F0062, as the tidy-up the feature's acceptance proposed.
4. 2026-11-17 human: 1: yes, the leave is given as worded, and it goes into the Interface as the human's word. 2: (a). 3: (a). 4: add it.
5. factory: started intake as self.
6. intake: accepted. I added the human's answers from journal entry 4 to the story. 1: the leave now stands in the Interface as the human's word, not "proposed wording". 2 (a): criterion 7 (docs) now asks that the project guide name and link the kit's make support module under its new name, `tests/support/kit_make_support.py`. 3 (a): the Interface line for `test_installed_builder.py` now drops the second assertion (`in points`) and keeps the whole-line check, aimed at `points`. The Description says the two assertions differ, and the new criterion 5 covers it. 4: criterion 4 now also requires the renamed modules to keep the same test function names. The criteria are renumbered, and `make check` and docs stay last.
   - Interface: names concrete test modules, the support module, the helper `_assert_named`, the two `sync` rows, the exact assertion to keep, each rename and the guard rename. It says no module under `src/factory/` changes. The human gave the leave for changing other stories' tests (entry 4).
   - Criteria: each one can be tested by one test function or one check. Both sides of each rule are covered: the `sync` rule (with the target: ok; without: exactly `["no target sync"]`) and `_assert_named` (it fails when only the sync gets `-f`, fails when only the command gets it, and passes when both get it). Criterion 3 covers the shared Dockerfile reader, criterion 4 the renames with their function names kept, and criterion 5 the single heading assertion.
   - Smoke test: both commands can run. The pytest command passes no `-q` (`addopts` already sets it), so pytest prints its summary line. Each `Expect:` can be checked: exactly one line naming the file, and a summary line ending in `passed` with no `failed`.
   - Docs criterion: it names what the reader must know (the module's new name and link) and dictates no sentences. The links at `docs/project-guide/agents.md:404` and `docs/project-guide/README.md:192` will need it.
   - Architecture: only tests change. The shared reader stays in `tests/support/`, as CLAUDE.md asks, and no test module imports another.
   - Scope: this is the tidy-up of F0062's tests that the feature's acceptance proposed. It stays within the feature and adds nothing new. The route is `tests`, because the Interface changes test files and the documenter may not write those.
7. factory: started tests as self.
8. tester: Tests written. This is a tests-only story, so nothing is red on purpose: `make test` is green (coverage 99.14 %) and `make lint` and `make types` are green too. The coder has nothing to build. It only runs the checks.

   Criteria → tests:
   - criterion 1: `tests/pipeline/application/test_project_check_run.py::test_a_definition_naming_sync_among_its_commands_asks_for_its_target_once`. It has two rows. Both use a definition, `NAMING_SYNC` (`PIPELINE_YAML` plus `sync: {time_limit: 5}` under `project_commands`). With `READY_MAKEFILE` the `makefile` point has `[]`. With `WITHOUT_SYNC` it has `["no target sync"]`. Each row also checks that the definition point has no fault.
   - criterion 2: `tests/machine/adapters/test_make_commands_make_file.py::test_the_named_makefile_must_reach_the_sync_and_the_command_each`. It has three rows (both / only-sync / only-command). Only the both row passes `_assert_named`; the other two raise `AssertionError`. `_assert_named` now splits the script on `&&`. It finds the sync segment and the command segment, by the word itself or by the `"$n"` argument that holds it. It then checks that each segment holds `-f "$k"` next to each other, where argument k is the named makefile. The old checks stay: the shell, the path not in the script, the path and `check` among the arguments, and sync present only `with_sync`.
   - criterion 3: `tests/operator_scripts/test_packs.py::test_each_stage_file_keeps_the_layer_rule_and_checks_every_download` now uses `dockerfile_instructions` from `tests/support/dockerfile_support.py`. Its own `_instructions` is gone. It checks `f"{keyword} {arguments}"`, so a download on a bare line is still searched.
   - criterion 4: `git ls-files tests | grep template` prints only `tests/guards/test_template_removed.py`. Renames: `tests/agent_files/test_template_makefile.py` → `test_python_pack_makefile.py`, `test_template_makefile_header.py` → `test_python_pack_makefile_header.py`, `test_template_sync.py` → `test_python_pack_sync.py`, and `tests/support/template_make_support.py` → `tests/support/kit_make_support.py`. Every function name is unchanged, including `test_template_*` function names, as the Interface asks. In `tests/guards/test_operator_guide_files.py`, `..._ten_topics` became `..._and_its_topics`.
   - criterion 5: `tests/agent_files/test_installed_builder.py::test_the_installed_reviewer_checks_the_projects_review_points`. It now asserts the heading once, as a whole line of the Stage section: `"\n### The project's review points\n" in f"\n{points}\n"`.

   Earlier tests changed under the human's leave (entry 4):
   - the Interface's targets: `test_project_check_run.py`, `test_make_commands_make_file.py`, `test_installed_builder.py`, `test_packs.py`, `dockerfile_support.py`, the three renamed modules and `test_operator_guide_files.py`;
   - the renamed support module's importers: `tests/operator_scripts/test_packs.py`, `tests/operator_scripts/test_kit_makefile.py`, `tests/support/kit_support.py` and the three renamed modules.

   The renames forced two changes outside the files the Interface names. Each still checks the same thing:
   - `tests/guards/test_tests_layout.py`: `FORMER_ROOT_HELPERS` now lists `kit_make_support`. `FORMER_ROOT_TEST_MODULES` lists the three new module names. The placement pattern `test_template_*.py` became `test_python_pack_*.py`, since a pattern that matches nothing fails `assert fitting`.
   - `tests/vm/test_stage_image.py`: imports and calls the reader under its public name.

   The public name is `dockerfile_instructions`, not `instructions`, because `test_stage_image.py` already has local variables named `instructions`.

   Rejected: keeping `_instructions` as an alias beside the public name, which would be a second name for one helper.

   For the documenter:
   - criterion 7: `docs/project-guide/agents.md:404` and `docs/project-guide/README.md:192` still link `tests/support/template_make_support.py`.
   - `docs/project-guide/README.md:164` still calls the Dockerfile reader `_instructions`; its new name is `dockerfile_instructions`.

   Files created: none (four renamed). No module failed to import.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
