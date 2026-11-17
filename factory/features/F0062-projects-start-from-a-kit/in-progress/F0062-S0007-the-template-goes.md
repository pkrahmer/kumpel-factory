---
stage: review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 696
comments_read: [6937913187]
handed_over: null
claim: null
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
