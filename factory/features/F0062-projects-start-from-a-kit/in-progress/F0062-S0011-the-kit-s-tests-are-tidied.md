---
stage: intake
blocked: question
round: 0
attempts: 0
crashes: 0
pull_request: 701
comments_read: []
handed_over: null
claim: null
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
---

# The feature's tests are tidied: one missing row, one weak check, one copy, and names that still say template

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

## Description

The reviewers of the feature's stories left notes on its tests that were not findings, and the leaves of S0007 and S0008 kept names that no longer say what a test checks. In the conformance check's tests, no row has a definition that already names `sync` among its project commands. `_assert_named` in the `make_file` tests checks only that `-f` appears somewhere, not that the sync and the command each get it. `tests/agent_files/test_installed_builder.py` asserts the same heading twice. `tests/operator_scripts/test_packs.py` holds a second copy of the Dockerfile instruction reader that `tests/support/dockerfile_support.py` keeps private. Three modules under `tests/agent_files/` are still named for the removed template although they test the kit and the Python pack, and a guard's name says "ten topics" where it checks eleven. After this story each of these is fixed. No module under `src/factory/` changes, and no test checks less than it did. This is a tests-only story; the coder has nothing to build and only runs the checks.

## Interface

- No module under `src/factory/` changes.
- `tests/pipeline/application/test_project_check_run.py`: a parametrized test with two rows for a definition whose `project_commands` name `sync`: with a `sync` target the point `makefile` has no fault, and without one it has exactly the fault `no target sync`, once.
- `tests/machine/adapters/test_make_commands_make_file.py`: `_assert_named` checks that the named makefile is passed to the sync and to the command, each on its own.
- `tests/agent_files/test_installed_builder.py`: the redundant first of the two assertions on the same heading (near line 65) goes.
- `tests/support/dockerfile_support.py`: its reader of instructions gets a public name. `tests/operator_scripts/test_packs.py` uses it in place of its own `_instructions`.
- Renames, each keeping every test function's name but the one below and what it checks: `tests/agent_files/test_template_makefile.py` → `test_python_pack_makefile.py`, `test_template_makefile_header.py` → `test_python_pack_makefile_header.py`, `test_template_sync.py` → `test_python_pack_sync.py`, and `tests/support/template_make_support.py` → `tests/support/kit_make_support.py` with its importers; `tests/guards/test_template_removed.py` keeps its name, since its subject is the template's removal; in `tests/guards/test_operator_guide_files.py`, `test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics` → `..._and_its_topics`.
- These change tests other stories wrote, beyond the standing leave. The human gives the leave when refining (proposed wording): "the tester may make exactly the changes this story's Interface names to the earlier tests it names, each test keeping what it checks".

## Acceptance criteria

1. The two `sync` rows of the Interface pass: with a `sync` target the `makefile` point is `ok`, and without one its faults are exactly `["no target sync"]`.
2. `_assert_named` fails for a run where only the sync gets `-f <path>`, and for one where only the command gets it; it passes when both get it.
3. `tests/operator_scripts/test_packs.py` defines no function of its own that reads Dockerfile instructions; it imports the public reader from `tests/support/dockerfile_support.py`.
4. `git ls-files tests | grep template` prints only `tests/guards/test_template_removed.py`, and no test function's name under `tests/guards/` says `ten_topics`.
5. `make check` stays green.
6. docs: none; only tests change, and none of the four documents names the renamed modules.

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
