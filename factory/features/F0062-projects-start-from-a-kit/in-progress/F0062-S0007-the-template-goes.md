---
stage: smoke-test
blocked: null
round: 1
attempts: 1
crashes: 0
pull_request: 696
comments_read: [6937913187]
handed_over: null
claim:
  instance: self
  stage: smoke-test
  started_at: '2026-11-17T04:33:33.041175Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T04:03:34.947807Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T04:03:34.955195Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T04:04:06.473839Z'
  stage: intake
  run: 4b5bde2675474b14967e2e52d26008ba
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T04:04:52.806545Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T04:04:55.384731Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T04:05:16.513702Z'
  stage: intake
  run: d6665a7d80a0424cab69fb0b136eb0f7
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T04:05:22.094981Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T04:11:03.308751Z'
  stage: tests
  run: 6c620ef8363c403bb70b7aad571efa4b
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T04:11:08.291187Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T04:15:42.814590Z'
  stage: doing
  run: 601939443edd49a5997799dc3b0a60c4
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T04:15:47.885465Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-17T04:17:08.808514Z'
  stage: review
  run: a9cea6aee6c34d8289836e2bac88ac51
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T04:17:14.039941Z'
  stage: docs
- number: 14
  speaker: documenter
  kind: result
  at: '2026-11-17T04:24:45.094727Z'
  stage: docs
  run: c89db49db1a7472faf8a802c84063086
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-17T04:24:50.128762Z'
  stage: smoke-test
- number: 16
  speaker: smoke-tester
  kind: result
  at: '2026-11-17T04:25:24.809532Z'
  stage: smoke-test
  run: d3eec7729fc44452ba50b36c497fbff6
- number: 17
  speaker: factory
  kind: stall
  at: '2026-11-17T04:25:25.006554Z'
  stage: smoke-test
  run: d3eec7729fc44452ba50b36c497fbff6
  reason: check_red
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-17T04:25:31.929540Z'
  stage: smoke-test
- number: 19
  speaker: smoke-tester
  kind: result
  at: '2026-11-17T04:25:49.798085Z'
  stage: smoke-test
  run: 9096fdd96f364d3ea401f4e94d4e8fe7
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-17T04:25:55.108186Z'
  stage: doing
- number: 21
  speaker: coder
  kind: result
  at: '2026-11-17T04:30:19.759296Z'
  stage: doing
  run: 1c44b054eab644bcaf1574afd7910b99
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-17T04:30:25.081334Z'
  stage: review
- number: 23
  speaker: reviewer
  kind: result
  at: '2026-11-17T04:31:15.460769Z'
  stage: review
  run: 07b5a8eb413b4748b535cd4d5bd369a1
- number: 24
  speaker: factory
  kind: started
  at: '2026-11-17T04:31:20.620266Z'
  stage: docs
- number: 25
  speaker: documenter
  kind: result
  at: '2026-11-17T04:33:27.436465Z'
  stage: docs
  run: cbf4b397e4b243e693295e55f384d140
- number: 26
  speaker: factory
  kind: started
  at: '2026-11-17T04:33:33.041175Z'
  stage: smoke-test
---

# The template goes

## Description

With the kit and the stack packs in place, `operator/template/` is a second, older copy of the same things: its pipeline definition is the kit's full line, its `Makefile` is the Python pack's with the kit's part still inside, and its `CLAUDE.md` is the kit's skeleton with the Python pack's sections. Two copies drift. After this story the template is gone: its three files are removed, and every test and every shipped text that read them reads the kit or the Python pack instead. Nothing a project gets changes, since the kit and the packs already hold it, and no module under `src/factory/` reads the template. The documents that still name the template are the documenter's part of this story; `demo/todo-service/README.md` is the human's.

## Interface

- Removed: `operator/template/CLAUDE.md`, `operator/template/Makefile`, `operator/template/factory/pipeline.yml`, and with them the folder.
- Where a shipped file under `agents/`, `operator/` or `src/` names `operator/template`, the coder names the kit or the pack that now holds the thing; a sentence that is only about the template goes.
- What replaces each file for a reader: the pipeline definition is `operator/kit/factory/pipeline.full.yml`; the makefile is `operator/packs/python/Makefile` together with `operator/kit/factory/kit.mk` (the shell settings, `$(start)`, `$(green)` and the start facts are in `kit.mk`, the targets in the pack's makefile); `CLAUDE.md` is `operator/kit/CLAUDE.md`, with the Python sections in `operator/packs/python/CLAUDE.sections.md`.
- Tests: `tests/guards/test_template_removed.py`, new. `feature.md` gives this leave (decision 25): "S0007 may change every earlier test and test helper that reads a file under `operator/template/`, or that pins that folder's name, so that it reads the kit or the Python pack instead: each test keeps its name and checks the same thing at the new place. Where the thing a test checks is now split between `kit.mk` and the pack's makefile, the test reads both, or an assembled makefile from `tests/support/kit_support.py`. A test whose only subject was that the template exists or lists its files is changed to check the same of the kit and the Python pack. The tester names every changed file in its entry."
- The coder's green run (journal entry 4): the coder may end its run with the new guard `tests/guards/test_template_removed.py` red and the folder-readme row red, both only on `operator/README.md` naming `operator/template`, which the docs stage fixes.

## Acceptance criteria

1. `operator/template` does not exist, and no tracked file under `src/`, `agents/`, `operator/` or `tests/` holds the text `operator/template`, except the new guard itself and the guard of the removed root folders, which may name it as a folder that must not exist.
2. Every earlier test that read the template passes at its new place, and none of them was deleted: the names of the test functions in the changed files are the names they had, compared in the tester's entry.
3. The checks of the Python makefile that earlier tests made on the template (its header, its `sync`, its `secrets` recipe beside the demo's, its `mutants`, its pins) hold for `operator/packs/python/Makefile` with `kit.mk`.
4. The checks of the template's pipeline definition (valid with the shipped roles, its tool paths, the working branch in its texts) hold for both pipeline definitions of the kit, the thin line included where the check does not depend on the seven roles.
5. `make check` stays green.
6. docs: `README.md`, the operator guide, the project guide and `docs/decisions.md` name the kit and the packs wherever they named the template as the start of a project, and no document tells a reader to copy `operator/template/`; `operator/README.md` has no entry for the template; `docs/decisions.md` records that the template was removed on this date because the kit and the Python pack hold everything it held. An older entry of the decision log that tells history keeps its words.

## Smoke test

```bash
test ! -e operator/template && echo gone
git grep -l 'operator/template' -- src agents operator tests | grep -v -e 'tests/guards/test_template_removed.py' -e 'tests/guards/test_root_operator_folders_removed.py' | wc -l
```
Expect: `gone`, then `0`.

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
p="$d/p"; git init -q "$p"; mkdir -p "$p/src" "$p/tests" "$p/docs"
cp -r operator/kit/factory "$p/factory"; cp operator/kit/CLAUDE.md "$p/"
mv "$p/factory/pipeline.full.yml" "$p/factory/pipeline.yml"; rm "$p/factory/pipeline.thin.yml"
cp operator/packs/python/Makefile "$p/Makefile"
touch "$p/src/a" "$p/tests/a" "$p/docs/a" "$p/README.md"
git -C "$p" add -A; git -C "$p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$p" | tail -1
```
Expect: `project: ready`.

```bash
uv run pytest tests/guards/test_template_removed.py tests/agent_files/
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: 1. Criterion 1 and the coder's green run conflict over `operator/README.md`. Criterion 1 says no tracked file under `operator/` may hold the text `operator/template`. The new guard `tests/guards/test_template_removed.py` will check that, and it runs in `make test`. But `operator/README.md` names the folder twice (line 19, and the table row at line 124), and that file is the documenter's (criterion 6, "`operator/README.md` has no entry for the template"). So when the coder removes the folder, its run cannot end with `make check guides` green: the new guard fails on `operator/README.md`, and so, most likely, does the folder-readme row in `make guides`, because the README lists a folder that is gone. The README is fixed only in the docs stage. This is the same situation decision 27 covers for S0005 and S0006 with `kit/` and `packs/`. I see three options:
      (a) Extend decision 27's leave to S0007. The coder may end with the new guard red and the folder-readme row red, both only on `operator/README.md`'s naming of `operator/template`, and the docs stage fixes both.
      (b) The guard of criterion 1 leaves out `operator/README.md`, and criterion 6 alone covers that file.
      (c) The coder may delete the two lines in `operator/README.md` (a write outside its usual paths), and the documenter only checks them.
      I would choose (a), because it matches decision 27 and keeps criterion 1 strict. If you agree, please add the leave to the story (or to `feature.md`) in those words.

   For the record, the rest checked out:
   - The format check passed.
   - The Interface names the files to remove, what replaces each one, the new guard and leave 25.
   - The criteria are testable, and criterion 2 asks the tester to compare the test names.
   - The smoke tests can be run: `check_project` exists, and `addopts` already sets `-q`, which the pytest smoke test leaves out, so its summary line will print.
   - The docs criterion says what the reader must know.
   - The story is within the feature's scope.
   - `operator/kit/README.md:5` names the template too. It is a shipped file under `operator/`, so the coder rewords it by the Interface's second line.
4. 2026-11-17 human: (a). Leave given: the coder may end its run with the new guard `tests/guards/test_template_removed.py` red and the folder-readme row red, both only on `operator/README.md` naming `operator/template`, which the docs stage fixes.
5. factory: started intake as self.
6. intake: accepted
   - Answer carried in: I added the human's leave from journal entry 4 to the Interface, as a line after the Tests line. With it, the coder may end its run with `tests/guards/test_template_removed.py` and the folder-readme row red, but only on `operator/README.md` naming `operator/template`. The docs stage fixes both. This matches decision 27 for S0005 and S0006.
   - Interface: names the three files to remove and what replaces each one: `pipeline.full.yml`, the Python pack's `Makefile` with `kit.mk`, and the kit's `CLAUDE.md` with `CLAUDE.sections.md`. It also names how shipped texts under `agents/`, `operator/` and `src/` are reworded, and the new guard. `operator/kit/README.md:5` is one of those shipped texts, so the coder rewords it.
   - Criteria: each one is testable. Criterion 1 is a git-grep guard with two named exceptions. Criterion 2 asks the tester's entry to compare the test function names. Criteria 3 and 4 name the checks that move to the pack's makefile with `kit.mk` and to both kit pipeline definitions. The story adds no new rule with a failing side, because it moves existing checks to a new place.
   - Smoke test: all three blocks can be run. `check_project` exists. The pytest block passes no `-q`, because `addopts` already sets it, so the summary line prints. Each `Expect:` (`gone` then `0`, `project: ready`, a summary line with only passed) can be checked against the output.
   - Docs criterion: it names what the reader must know: the kit and the packs replace the template, no document tells the reader to copy it, `operator/README.md` has no template entry, and the decision log has a removal entry while older history keeps its words. It dictates no sentences.
   - Architecture: no module under `src/factory/` reads the template. Changes to tests made by other stories are covered by `feature.md` decision 25. `demo/todo-service/README.md` stays the human's.
   - Scope: within F0062 (projects start from a kit). This story is the cleanup after S0005 and S0006 and is not in the feature's out-of-scope list.
   - Route: `tests`. The story removes files under `operator/` and changes tests and shipped texts, which are outside the documenter's paths.
7. factory: started tests as self.
8. tester: Tests written. Every earlier test that read `operator/template/` now reads the kit or the Python pack, under leave 25 in `feature.md`. The new guard is red for the right reason.

   Criterion → test:
   - criterion 1: `tests/guards/test_template_removed.py::test_the_template_folder_does_not_exist` and `::test_no_shipped_file_or_test_names_the_template_folder`. The second runs `git ls-files` over `src agents operator tests`, skips files that are gone from disk, and leaves out this guard and `test_root_operator_folders_removed.py`. Both carry the marker `documents`, so they run in `make guides` (the coder's `make check guides`) and not in `make test`, because they read `operator/README.md`, which the documenter fixes. Both are red now: the folder exists, and `operator/README.md` and `operator/kit/README.md` name it.
   - criterion 2: test function names in each changed test file, compared against `HEAD` with a sorted grep of `^def test_`. They are identical in all 13 files: `test_claude_agent_texts_mutants.py`, `test_claude_files.py`, `test_demo_makefile_secrets.py`, `test_template_makefile.py`, `test_template_makefile_header.py`, `test_template_sync.py` (all `tests/agent_files/`), `tests/guards/test_license_headers.py`, `test_pins.py`, `test_root_operator_folders_removed.py`, `test_working_branch_in_agent_texts.py`, `tests/operator_scripts/test_kit_files.py`, `tests/pipeline/adapters/test_pipeline_yaml_tool_paths.py` and `tests/shared/domain/test_folder_readmes_list.py`. No test was deleted.
   - criterion 3 (the Python makefile with `kit.mk`):
     - header: `tests/agent_files/test_template_makefile_header.py::test_template_makefile_header_calls_mutants_a_sweep_by_hand`, and `test_template_makefile.py::test_header_names_the_development_dependency`
     - `sync`: `test_template_sync.py::test_template_says_the_contract_is_four_targets` and `::test_sync_runs_uv_sync_frozen_once_and_says_green`
     - `secrets` beside the demo's: `test_demo_makefile_secrets.py::test_the_todo_demos_secrets_target_is_the_templates`
     - `mutants`: `test_claude_agent_texts_mutants.py::test_template_makefile_leaves_mutants_to_a_sweep_by_hand`
     - pins: `tests/guards/test_pins.py::test_the_template_has_no_placeholder_files_and_no_tasks_directory`, over the kit and the Python pack
     - the rest of `test_template_makefile.py`, run on a project made of the pack's `Makefile` plus `factory/kit.mk`
   - criterion 4 (the kit's pipeline definitions):
     - valid with the shipped roles: `test_claude_files.py::test_template_pipeline_definition_is_valid_with_the_shipped_roles`. Full line only, because it depends on the seven roles.
     - tool paths: `test_pipeline_yaml_tool_paths.py::test_the_shipped_definitions_hold_no_tool_paths_and_load`, with rows for both `pipeline.full.yml` and `pipeline.thin.yml`.
     - working branch: `test_working_branch_in_agent_texts.py::*`, whose folders are now `agents/agents`, `operator/kit` (both lines) and `operator/packs/python`.
     - `sync` named and listed by no stage: `test_template_sync.py::test_template_pipeline_definition_names_sync_and_no_stage_lists_it`. Full line only, because it pins the full line's project commands.
   - criteria 5 and 6: none (`make check`; docs).

   Helpers changed:
   - `tests/support/template_make_support.py`: `MAKEFILE` is now the Python pack's makefile. New `KIT_MK` and `header_text()` (the opening comment lines joined into one). `template_project` also copies `kit.mk` to `factory/kit.mk`.
   - `tests/support/shipped_agents.py`: `TEMPLATE_PIPELINE` is now `operator/kit/factory/pipeline.full.yml`. This moves `template_definition()` users to the full line: `test_decide_docs_slip.py`, `test_claude_agent_texts*.py` and `test_take_refuses_write_and_edit.py`, none of which needed an edit.

   Docstrings changed: `tests/README.md` and `tests/agent_files/__init__.py`.

   Choices I made to keep each check the same at the new place (please say if one is wrong):
   - Header rows: they check the phrases inside the joined header, not lines 1, 4 and 5, because the pack wraps those lines differently.
   - `rules-file` row: the kit's `CLAUDE.md` names no project commands, so the row now checks two things. `kit.mk` says "defines `sync`, `lint`, `test` and `check`". Neither the kit's `CLAUDE.md` nor the pack's sections say "names `check`, `lint` and `test`".
   - `test_template_rules_file_is_the_python_project_text`: the expected lines are now the kit's `CLAUDE.md` with the Python sections put in by `pack_claude_md("python")`, taken from today's files.
   - Folder listing: `test_template_holds_only_…` now pins what the kit and the Python pack each list.
   - Secrets file list: the expected lists in `test_secrets_scans_the_changed_files_or_every_tracked_file` now include `factory/kit.mk`, because the project made from the pack tracks it.
   - License headers: the guard leaves out `operator/kit/` where it used to leave out `operator/template/`. The packs stay in scope, because their script carries the header.
   - Folder READMEs: the list test checks `operator/packs/python/README.md`.
   - `test_kit_files.py::test_the_template_stays_with_its_three_files` and `test_root_operator_folders_removed.py::test_the_moved_file_lies_under_operator` now check the kit and pack files that replace the template's three.

   Runs:
   - `make test`: green, 102.1 s. The new guard is outside it because of the `documents` marker.
   - `uv run pytest tests/guards/test_template_removed.py`: 2 failed, for the right reasons.
   - `make lint`: green.
   - Every module imported.

   Files created: `tests/guards/test_template_removed.py`.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: Removed the template and reworded the one shipped text that named it, which `operator/` is mine to change.

    What I built:
    - Removed `operator/template/CLAUDE.md`, `operator/template/Makefile` and `operator/template/factory/pipeline.yml`, and with them the folder. They are staged as deletions.
    - `operator/kit/README.md:5`: removed the clause that said `operator/template/` still stays beside the packs. The sentence now ends at the link to `operator/packs/`. The clause was only about the template, so by the Interface's second line it goes.
    - Nothing under `src/` or `agents/` named the template. A case-insensitive grep for "template" over `agents src operator` found only the README lines above and an unrelated "ESP32 template" in `operator/packs/c-host/TRAPS.md`.

    Runs:
    - The tester's files (`tests/agent_files`, `tests/guards`, `test_kit_files.py`, `test_pipeline_yaml_tool_paths.py`, `test_folder_readmes_list.py`): all pass except one test, `tests/guards/test_template_removed.py::test_no_shipped_file_or_test_names_the_template_folder`. It fails only on `operator/README.md`.
    - `make check guides`:
      - `make check` is fully green: lint, types, layers, sast, secrets, licenses, and test (102.0 s), ending with `check: green`.
      - `make guides` fails on that one test alone. Its failure line: `E AssertionError: assert ['operator/README.md'] == []`, at `tests/guards/test_template_removed.py:37`.
      - This is within the leave in journal entry 4: `operator/README.md` (lines 3, 19 and 124) is the documenter's to fix. The folder-readme row did not fail.
    - Smoke test: the first block's condition holds (the folder is gone, and the grep finds only `operator/README.md`, which the docs stage fixes). My attempt to run the `check_project` smoke block in a temporary directory was denied by the shell's permissions, so it is not run here; the smoke tester runs it.

    Main choice:
    - I kept `operator/README.md` untouched and left its three mentions to the docs stage, as the leave says. That includes line 3's "and for now the template", which the guard does not catch but criterion 6 covers.
    - Rejected: editing `operator/README.md` myself (option (c) at intake, which the human did not choose).

    Refactor: the diff is three deletions and one shortened sentence; nothing to change.

    The journal changed nothing in the task's meaning beyond the leave, which intake already carried into the Interface. The Description stays as it is.

    Noticed, not touched:
    - `docs/` and `README.md` may still name the template. That is criterion 6, for the documenter.
    - `demo/todo-service/README.md` is the human's.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
12. reviewer: no findings

    What I checked against the code on the branch:
    - Criterion 1:
      - `operator/template` is gone.
      - `git grep 'operator/template' -- src agents operator tests` finds only `operator/README.md:19` and `:124`. Leave 4 allows both, and the docs stage fixes them (criterion 6).
      - The new guard `tests/guards/test_template_removed.py` searches the tracked files under the four folders and leaves out only itself and `test_root_operator_folders_removed.py`. It carries the marker `documents`, so it runs in `make guides`.
      - I ran it: it fails only with `assert ['operator/README.md'] == []` (`tests/guards/test_template_removed.py:37`), which is within the leave.
    - Criterion 2: I compared the sorted `^def test_` lines of every changed test file against `develop`. They are identical in all of them, and no test was deleted.
    - Criterion 3, checked on the pack's `Makefile` with `kit.mk`:
      - header: `test_template_makefile_header.py`, `test_template_makefile.py`
      - `sync`: `test_template_sync.py`
      - `secrets` beside the demo's: `test_demo_makefile_secrets.py`
      - `mutants`: `test_claude_agent_texts_mutants.py`
      - pins: `test_pins.py`, over the kit and the Python pack
      - `template_project` copies `kit.mk` to `factory/kit.mk`, which the pack's makefile includes.
    - Criterion 4:
      - valid with the shipped roles: checked on `pipeline.full.yml` only, because the check depends on the seven roles. The thin line's roles are already checked against the shipped agents by `tests/operator_scripts/test_kit_files.py` (the `agents` point of `project_faults`, rows `thin` and `full`).
      - tool paths: `test_pipeline_yaml_tool_paths.py` has rows for both lines.
      - working branch: `test_working_branch_in_agent_texts.py` reads `operator/kit`, which holds both lines, and `operator/packs/python`.
    - Criterion 5 and the run:
      - The coder's entry says `make check` was green and `make guides` red only on the guard row the leave allows.
      - I ran every changed test file plus the guard (`-m ''`): everything passed except that one expected row.
    - Architecture and security: nothing under `src/` changed, the diff adds no silencing marker, and the one shipped text (`operator/kit/README.md:5`) loses only its sentence about the template, as the Interface's second line asks.
    - Quality and other changes:
      - The license-header guard now leaves out `operator/kit/` where it left out the template. The kit holds no script, and the packs stay in scope, so no file changes status.
      - The folder-readme list test checks `operator/packs/python/README.md`, which, like the template, carries no README.
    - Work item: the Description matches what was built. The docs criterion still says what the documenter must change: `README.md`, the operator guide, the project guide, `docs/decisions.md` and the two lines of `operator/README.md`.

    Earlier tests (all `M`, all under the human's leave in `feature.md` decision 25, which the story's Interface quotes):
    - tests/README.md: decision 25 (a docstring-like line naming the folder)
    - tests/agent_files/__init__.py: decision 25
    - tests/agent_files/test_claude_agent_texts_mutants.py: decision 25
    - tests/agent_files/test_claude_files.py: decision 25
    - tests/agent_files/test_demo_makefile_secrets.py: decision 25
    - tests/agent_files/test_template_makefile.py: decision 25
    - tests/agent_files/test_template_makefile_header.py: decision 25
    - tests/agent_files/test_template_sync.py: decision 25
    - tests/guards/test_license_headers.py: decision 25
    - tests/guards/test_pins.py: decision 25
    - tests/guards/test_root_operator_folders_removed.py: decision 25
    - tests/guards/test_working_branch_in_agent_texts.py: decision 25
    - tests/operator_scripts/test_kit_files.py: decision 25
    - tests/pipeline/adapters/test_pipeline_yaml_tool_paths.py: decision 25
    - tests/shared/domain/test_folder_readmes_list.py: decision 25
    - tests/support/shipped_agents.py: decision 25 (a test helper)
    - tests/support/template_make_support.py: decision 25 (a test helper)
13. factory: started docs as self.
14. documenter: Docs written. Every document that named the template as the start of a project now names the kit and the packs. `operator/README.md` no longer lists the template, and the decision log has the removal entry.

    Files changed:
    - `operator/README.md`: removed "and for now the template" from line 3, and removed the template's bullet and its table row. This fixes the one hit that the coder's run left on `tests/guards/test_template_removed.py`.
    - `docs/operator-guide/agent-runtime.md`: the full line is now `operator/kit/factory/pipeline.full.yml`, and the thin line names `pipeline.thin.yml`. "A new project starts from…" now names the kit and a stack pack: what each brings, the Python pack's `SOURCE` and `LAYERS` placeholders, and links to the kit's and the packs' READMEs. The old text said the forms were yours to add; the kit now ships them, so that is gone.
    - `docs/operator-guide/install.md`: the three mentions of "the template" (`uv run`, `make secrets`, `mutants`) now name the Python pack's makefile. The `CLAUDE.md` part of the mutants sentence is gone, because the pack's sections do not mention mutants.
    - `docs/operator-guide/pipeline.md`, three changes:
      - *Start facts* now reads `kit.mk`: `WORKING_BRANCH`, `FACTS_LEFT_OUT`, and the pack's `':!uv.lock'`. Its example is `kit.mk`'s real `facts-diff`. The table's stage column is now the full line's, and the thin line's facts are named.
      - The smoke-test, review and `sync` sentences now say "the kit's full line"; the thin line's `sync` limit is 10.
      - The `factory-check-project` example is rebuilt from the kit's full line and the Python pack. I ran it in a temporary folder and got the same seven lines as printed, ending `project: not ready (2 faults)`.
    - `docs/project-guide/agents.md`: the title, intro and section heading now say "the start of a project", and the line about data the image carries no longer names the template. The decisions in `test_claude_agent_texts.py` are now derived from `pipeline.full.yml`. *The template* became *The start of a project*. It covers `pipeline.full.yml` (all its old detail kept), `pipeline.thin.yml`, the kit's `CLAUDE.md` with the pack's `CLAUDE.sections.md`, `kit.mk`, and the Python pack's `Makefile` (secrets, demo equality, duplicates, mutants, placeholders, all checked against the file). The forms now ship with the kit. A line names the two test helpers.
    - `docs/project-guide/README.md`: changed the `agents.md` index line and section name, the licence-guard scope (`operator/kit/` in place of `operator/template/`), the `tests/agent_files/` line and the `template_make_support.py` line (now `KIT_MK` and `header_text`).
    - `docs/project-guide/machine.md`: the `sync` text now names the packs' makefiles and both kit pipeline definitions.
    - `docs/project-guide/operator.md`: removed the template's line from the layout listing, and its bullet.
    - `docs/project-guide/shared.md`: replaced the sentence about the template carrying no README with one about `operator/kit/factory/README.md`, which is not on `FOLDER_READMES`.
    - `docs/decisions.md`:
      - New entry, *The template is removed* (2026-11-17, F0062-S0007): what replaces each file, the new guard, and the licence-header guard's scope moving to `operator/kit/`.
      - Its Why is the story's: the kit and the Python pack hold everything, and two copies drift.
      - It has no Rejected line, because the story names no rejected option.
      - The older entries that tell history keep their words (lines 11, 465, 1576, 1660 and 1745).

    Runs:
    - `make documents`: documents ok (47.5 s).
    - `make check guides`: check: green, guides: green (9.3 s). The new guard now passes, because nothing under `src agents operator tests` names `operator/template`.

    Cross-read and found current: `README.md` (it does not name the template), `operator/kit/README.md` (the coder's change), `docs/operator-guide/machine.md` (its "template" is the systemd unit, which is unrelated), `docs/project-guide/hosting.md` (`remote_template` is unrelated).

    Stale but not mine to touch:
    - `docs/brochure/README.md:459` still says "A new project starts from the **template**". The brochure states it describes Kumpel "as of November 2026 (version 1.1)", a record of that time, so I left it. The human may want it updated.
    - `demo/todo-service/README.md` is the human's, as the Description says.

    `guides`: guides: green (9.4 s)
    `secrets`: secrets: green (2.9 s)
    `documents`: documents ok (47.3 s)
15. factory: started smoke-test as self.
16. smoke-tester: Smoke test run from the repository root, each block exactly as written. All three blocks met their `Expect:` lines, and no criterion is contradicted. No findings.

    Block 1 (the folder is gone and nothing under the shipped folders or tests names it):
    ```
    gone
    0
    ```
    Met: `gone`, then `0`.

    Block 2 (`check_project` on a project made from the kit's full line, the kit's `CLAUDE.md` and the Python pack's `Makefile`):
    ```
    Bytecode compiled 4164 files in 83ms
    project: ready
    ```
    Met: the last line is `project: ready`. The first line is uv's own output on stderr. `tail -1` does not filter stderr, so that line shows too.

    Block 3 (`uv run pytest tests/guards/test_template_removed.py tests/agent_files/`, last lines):
    ```
    ........................................................................ [ 82%]
    ........................................................................ [ 99%]
    ...                                                                      [100%]
    435 passed in 3.82s
    ```
    Met: the summary line has only `passed`.

    Checked against the criteria:
    - Criterion 1: confirmed by block 1. The guard's two exceptions are the only hits left.
    - Criterion 6: `git grep 'operator/template' -- README.md docs operator` finds no hit in `README.md`, `operator/`, the operator guide or the project guide.
      - In `docs/decisions.md`, the template is named only in older history entries (lines 1576, 1660 and 1745), which keep their words, and in the new entry *The template is removed* (line 1747).
      - The other hits are under `docs/runs/`, which is the human's.
    - Criteria 2 to 5: the smoke test contradicts none of them. The factory's `make check` follows this stage.

    Open, as the documenter noted: `docs/brochure/README.md:459` still says a new project starts from the template. It is a dated record of v1.1. The human may want it updated.
17. factory: Stage smoke-test stalled (attempt 1 of 2): a check is red after the stage: `check`
    Bytecode compiled 4164 files in 52ms
    Success: no issues found in 1103 source files
    types: green (4.8 s)
    Bytecode compiled 4164 files in 51ms

    ╔══╗─────────▶╔╗ ╔╗      ╔╗◀───┐
    ╚╣╠╝◀─────┐  ╔╝╚╗║║────▶╔╝╚╗   │
     ║║   ╔══╦══╦╩╗╔╝║║  ╔╦═╩╗╔╝╔═╦══╗
     ║║╔══╣╔╗║╔╗║╔╣║ ║║ ╔╬╣╔╗║║ ║│║╔═╝
    ╔╣╠╣║║║╚╝║╚╝║║║╚╗║╚═╝║║║║║╚╗║═╣║
    ╚══╩╩╩╣╔═╩══╩╝╚═╝╚═══╩╩╝╚╩═╩╩═╩╝
      └──▶║║                    ▲ 
          ╚╝────────────────────┘

    make: *** [Makefile:44: layers] Error 139
18. factory: started smoke-test as self.
19. smoke-tester: Routed the factory's red `make check` from the stall in journal entry 17. As the stage says, I did not run the smoke test again: my last run (entry 16) met all three `Expect:` lines.

    Findings:
    1. The `layers` check failed during the factory's `make check` after the smoke-test stage. The output ended `make: *** [Makefile:44: layers] Error 139`, which comes from the `layers` target at `Makefile:44` (import-linter run against the contracts in `pyproject.toml`). Exit 139 means the process was killed by a segmentation fault. It is not a broken contract: import-linter printed no contract output before it stopped. `types` was green just before it. Under the stage's rules a layer failure goes to `doing`, since it is not a file the documenter writes.

    What I observed when I ran `make layers` once by hand on this branch: `Contracts: 4 kept, 0 broken.` and `layers: green (0.3 s)`, exit 0. The crash did not happen again, so it looks like a one-time segfault of the import-linter process rather than something the story's diff caused. The diff touches no file under `src/` and no import contract. For the coder: run `make check` again. If `layers` is green, nothing in the code needs to change. If exit 139 comes back, the crash is in the tool or the machine (import-linter or the Python build that uv runs) and it is a `question` for the human, not a code fix.

    Not run: the smoke test (per the stage's rule after a `check_red` stall) and the whole `make check` (the factory runs it after this stage).
20. factory: started doing as self.
21. coder: Rework round 1: the smoke tester's one finding (entry 19) was that `layers` crashed with exit 139 (a segfault) in the factory's `make check` after the smoke-test stage. I changed no code, because there is nothing in the code to fix.

    What I did:
    - I ran `make check` twice on this branch in the foreground. Both runs were green, ending `check: green`. The second run printed `Contracts: 4 kept, 0 broken.` and `layers: green (0.2 s)`, and every other target was green too: lint, types, sast, secrets, licenses, and test (108.5 s, coverage 99.14 %).
    - `make guides`: green (9.2 s). It includes `tests/guards/test_template_removed.py`, which now passes because the documenter fixed `operator/README.md`.
    - `git status --short` was empty: the working tree holds no change from me.

    Why no change: the crash did not happen again in three runs (the smoke tester's run by hand and my two). This story's diff touches nothing under `src/`, no import contract and no configuration that import-linter reads. That points to a one-time crash of the import-linter process, which the story did not cause. Rejected: asking the human now. As entry 19 says, a question is only due if exit 139 comes back.

    Open: if `layers` segfaults again in the factory's check, the cause is in the tool or the machine (import-linter or the Python build that uv runs), and that is the human's question. `docs/brochure/README.md:459` still names the template, as the documenter noted; I did not touch it. The journal changed nothing in the task's meaning, so the Description stays as it is.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
22. factory: started review as self.
23. reviewer: no findings

    What I checked in round 1, against the code on the branch. The coder's rework (entry 21) changed no file. So the new part of this review is the documenter's diff, checked under the Documents item, and I went through groups 1 to 6 again:
    - Criterion 1:
      - `operator/template` is gone.
      - `tests/guards/test_template_removed.py` checks that the folder does not exist. It also checks the tracked files under `src agents operator tests` for the folder's name, leaving out only the two named guards. It builds the name from parts, so it does not find itself.
      - The documenter removed the three mentions in `operator/README.md` (lines 3, 19 and the table row), so the leave of entry 4 is no longer needed. The documenter's `make check guides` was green, and the smoke tester's block 1 printed `0`.
    - Criteria 2 to 4: unchanged since entry 12, where I checked them.
      - The test names are identical in every changed file.
      - The pack's `Makefile` with `kit.mk` is checked for its header, `sync`, `secrets`, `mutants` and pins.
      - Both kit lines are checked for tool paths, and both are covered by the working-branch test.
    - Criterion 5: the coder's two `make check` runs in entry 21 were green, and `make guides` was green. The `layers` exit 139 in entry 17 did not come back. The diff touches nothing under `src/` and no import contract.
    - Criterion 6 (Documents), each claim checked against the files:
      - `docs/operator-guide/pipeline.md`:
        - The `kit.mk` snippet (`facts_base`, `facts_paths`, the `facts-diff` recipe) matches `operator/kit/factory/kit.mk` word for word.
        - `WORKING_BRANCH ?= develop` and `FACTS_LEFT_OUT` are in `kit.mk`, and `FACTS_LEFT_OUT = ':!uv.lock'` is at `operator/packs/python/Makefile:15`.
        - The `context` lists of the stage table and the YAML block match `pipeline.full.yml:12-31`. The thin line's `facts-files` for `doing` and `facts-diff` for `review` match `pipeline.thin.yml`.
        - The `sync` limits match: 5 in the full line, 10 in the thin line.
        - The smoke-test and review lines match `pipeline.full.yml:31,33`.
        - The `check_project` example uses the kit's and the pack's real paths. Its output was copied from the documenter's real run (entry 14).
      - `docs/operator-guide/agent-runtime.md`:
        - The kit holds both lines, the two forms, `kit.mk` and `CLAUDE.md`.
        - `SOURCE` and `LAYERS` are the pack's placeholders (`Makefile:21-22`).
        - `operator/packs/README.md` exists.
      - `docs/operator-guide/install.md`: the pack's header line 5 says `mutants` is for a sweep by hand, and `uv run` and `make secrets` are in the pack.
      - `docs/project-guide/agents.md`:
        - `kit.mk` sets bash with `.ONESHELL`, `.DEFAULT_GOAL := check`, `$(start)`, `$(green)` and the three facts targets.
        - The pack includes `factory/kit.mk`.
        - The `secrets` recipe leaves out `uv.lock|.secrets.baseline|.*\.costs\.jsonl` (`Makefile:70`).
        - There is no `documents` target.
        - The section list of `CLAUDE.sections.md` matches the file.
        - The forms are in `operator/kit/factory/`.
      - `docs/project-guide/shared.md`: `operator/kit/factory/README.md` exists and is not on `FOLDER_READMES` (`src/factory/shared/domain/folder_readmes.py`), and the count of 22 is unchanged.
      - `docs/project-guide/README.md`: the licence-guard scope matches `KIT = "operator/kit/"` in `tests/guards/test_license_headers.py:18`, and the helper names match `tests/support/template_make_support.py`.
      - `docs/project-guide/machine.md`: the `sync` targets and limits match.
      - `docs/decisions.md`: the new entry *The template is removed* records the replacements, the guard, the licence scope and the reason. The older entries keep their words: the diff only appends.
    - Architecture and security: no change under `src/`, no silencing marker, no new baseline entry.
    - Quality: the guard's two tests check two different rules, so two test functions are right.
    - Work item: the Description matches what was built, and the docs criterion is met.
    - Open, not mine: `docs/brochure/README.md:459` still says a new project starts from the template. It is a dated record of v1.1, and it is the human's call (entries 14 and 16).

    Earlier tests (all `M`, all under the human's leave in `feature.md` decision 25, which the story's Interface quotes):
    - tests/README.md: decision 25
    - tests/agent_files/__init__.py: decision 25
    - tests/agent_files/test_claude_agent_texts_mutants.py: decision 25
    - tests/agent_files/test_claude_files.py: decision 25
    - tests/agent_files/test_demo_makefile_secrets.py: decision 25
    - tests/agent_files/test_template_makefile.py: decision 25
    - tests/agent_files/test_template_makefile_header.py: decision 25
    - tests/agent_files/test_template_sync.py: decision 25
    - tests/guards/test_license_headers.py: decision 25
    - tests/guards/test_pins.py: decision 25
    - tests/guards/test_root_operator_folders_removed.py: decision 25
    - tests/guards/test_working_branch_in_agent_texts.py: decision 25
    - tests/operator_scripts/test_kit_files.py: decision 25
    - tests/pipeline/adapters/test_pipeline_yaml_tool_paths.py: decision 25
    - tests/shared/domain/test_folder_readmes_list.py: decision 25
    - tests/support/shipped_agents.py: decision 25 (a test helper)
    - tests/support/template_make_support.py: decision 25 (a test helper)
24. factory: started docs as self.
25. documenter: Round 1 docs. There was nothing to rework, so I changed no file.

    The coder's rework (entry 21) changed no file, and the reviewer (entry 23) had no findings. The documents I wrote in entry 14 are therefore still current against the branch.

    What I checked:
    - `git status --short` is empty: no change is waiting in the working tree.
    - `git grep 'operator/template'` over `README.md`, `docs/operator-guide`, `docs/project-guide`, `operator`, `src`, `agents` and `tests` finds no hit in any document. The only other files that may name the folder are the two named guards, as criterion 1 allows.
    - `make documents` printed `documents ok (47.1 s)`. The two "not run (vm)" lines it prints are the examples that need the VM, in `docs/operator-guide/records.md:53` and `docs/project-guide/pipeline.md:143`. Neither is from this story.
    - I did not run `make check`, because I changed no file.

    Cross-read and found current: the files changed in entry 14 (`operator/README.md`, `docs/operator-guide/agent-runtime.md`, `install.md` and `pipeline.md`, `docs/project-guide/README.md`, `agents.md`, `machine.md`, `operator.md` and `shared.md`, and `docs/decisions.md`), plus `README.md`. The reviewer checked each of these against the code in entry 23.

    Stale, not mine to touch: `docs/brochure/README.md:459` still says a new project starts from the template. It is a dated record of v1.1, so whether to update it is the human's call. `demo/todo-service/README.md` belongs to the human.

    `guides`: guides: green (9.4 s)
    `secrets`: secrets: green (2.9 s)
    `documents`: documents ok (47.2 s)
26. factory: started smoke-test as self.
