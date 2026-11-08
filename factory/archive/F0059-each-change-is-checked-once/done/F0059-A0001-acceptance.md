---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 674
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T16:42:57.236497Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T16:45:40.572532Z'
  stage: acceptance
- number: 3
  speaker: factory
  kind: started
  at: '2026-11-08T16:45:42.307851Z'
  stage: acceptance
- number: 4
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T16:53:19.701663Z'
  stage: acceptance
  run: 82c6964628204530a5fa2ce0ea369403
- number: 5
  speaker: factory
  kind: done
  at: '2026-11-08T16:54:08.515013Z'
  stage: done
stories: [F0059-S0001, F0059-S0002]
outcome: accepted
---

# Acceptance of Each change is checked once

## Recommendation

accepted with stories. Both stories and the human's changes (`77c97b622`) do what `feature.md` promised. The factory's full `make check` runs once, after the smoke tester. The docs stages run `make guides` beside `secrets` and `documents`. A documents-only change keeps `check`'s key, so a passed check is reused. The coder's agent file starts from the tester's files, and the smoke tester routes a `check_red` stall. The feature smoke test, `make check` and `make guides` are green. One finding is worth a story: the operator guide and the project guide still describe the pipeline from before the human's commit (S0003). It does not count as a broken promise. Each stale passage quotes or explains a file it links, and that file is correct. An operator who believes the old text expects one check run too many and configures no fault.

## 1 Scope

Each scope line has its story:
- The coder's first step: S0001, `agents/agents/coder.md`.
- The marker `documents`, registered in `tests/conftest.py`: S0001, 13 modules marked.
- The smoke tester's route after a red check: S0002, `agents/agents/smoke-tester.md:58-61`.

No story went outside the scope, and nothing out of scope was built: the coder's own `make check` stays, there is no new factory rule, and nothing runs in parallel.

The human's changes are on `develop` in `77c97b622`:
- `Makefile`: `test` runs `-m "not documents"`. `guides` runs `-m documents` without coverage and ends with `guides: green`.
- `factory/pipeline.yml`: `guides: {time_limit: 2}`. `doing` has no `checks`. `docs` checks `[guides, secrets, documents]`, `smoke-test` checks `[check]`, and `docs-only` checks `[check, guides, secrets, documents]`. `check`'s `not_read` holds every documenter write path.
- `CLAUDE.md`: the coder's command and `make check guides`.
- `demo/todo-service/project` and `operator/template`: the same stage checks, without `guides`.

The same commit also does two things `feature.md` does not list (see 6):
- It drops the `2>/dev/null || git rev-parse HEAD` fallback of `base_ref` in all three Makefiles.
- It adds a line to `docs/runs/2026-11-05-f0052/log.md`.

Of the Goal's done-conditions, one is still open: the human's measurement run (demo-todo F0001 on a fresh repository, compared with the baseline of 2026-11-08). It is the human's, after this acceptance, and no story was owed for it.

## 2 Feature smoke test

The walk-through is one Python script, run against the real entry points on this branch with `uv run python <tmp>/smoke.py "$PWD"`. Its steps:
1. It loads `factory/pipeline.yml` through `RuamelPipelineDefinitionReader`.
2. It checks that the documenter's write paths are all in `check`'s `not_read`.
3. In a fresh clone it computes `check`'s key with `GitCli.work_tree_id(not_read)`, the key `KnownResults` reuses a check by, before and after a documents-only change to `README.md`, `docs/operator-guide/pipeline.md`, `tests/README.md` and `src/factory/README.md`, and again after a change to a test file.
4. It collects both marker selections with pytest.
5. It reads the two agent files.

```text
1. the pipeline definition loads; checks per stage:
   doing: checks=[] reports=['duplicates'] -> 42 of 60 min
   docs: checks=['guides', 'secrets', 'documents'] reports=[] -> 47 of 60 min
   smoke-test: checks=['check'] reports=[] -> 48 of 60 min
   docs-only: checks=['check', 'guides', 'secrets', 'documents'] reports=[] -> 55 of 60 min
2. documenter write paths not in check's not_read: []
3. documents-only change: check's key unchanged: True | whole tree changed: True
4. test-file change: check's key changed: True
5. documents: 176/11183 tests collected (11007 deselected) in 4.75s
   not documents: 11007/11183 tests collected (176 deselected) in 4.61s
6. coder starts with the named test files: True
   smoke tester routes check_red: ["When the work item's latest journal record is a stall with the reason `check_red`, the factory's `ma"]
```

The make targets, run in the foreground on this branch:

```text
$ make check 2>&1 | tail -3
test: green (110.3 s)
check: green
$ make guides 2>&1 | tail -1
guides: green (9.7 s)
$ make documents 2>&1 | tail -1
documents ok (60.0 s)
```

What the run shows:
- The leases fit, as `feature.md` computed.
- A documents-only change leaves `check`'s key as it was, so the passed check is reused, while a test change runs it again.
- 176 + 11007 = 11183: the two selections together make up the whole suite.

Green.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- S0001 coder (entries 13, 20, 24): `CLAUDE.md` named the single-test-file command only in the tester's words. Fixed by the human in `77c97b622`.
- S0001 documenter (entry 28): `docs/operator-guide/pipeline.md:131` says that `README.md` and `docs/` stay in `check`'s key and that a documents-only change can turn `make check` red. The human's commit made it false, and it is still there. The same goes for:
  - `docs/project-guide/README.md:231` ("Until then `make test` still runs every test").
  - `docs/operator-guide/pipeline.md:69`, the template's `doing` with `checks: [check]`.
  - `docs/operator-guide/pipeline.md:76`, the template's `base_ref` with the fallback the human removed.
  - `docs/operator-guide/pipeline.md:97`, the template's `smoke-test` without `checks`.
  - `docs/operator-guide/pipeline.md:104`, step 3 of the docs route, which does not name `guides`.

  Proposed as S0003.
- S0001 reviewer note (entry 26): `tests/agent_files/test_claude_agent_texts_first_tests.py:30` asserts `"only" in text`, which any "only" in the section meets. It is a looser check, not a wrong one, and the phrase checks beside it pin the claim. Not worth a run of its own; left to the human.
- S0002 smoke tester (entry 13): the coder's entry says `grep -c check_red` printed 2. It prints 1, because `grep -c` counts lines. Harmless.
- S0002 reviewer: the new module's private `_sentences` follows a different rule from the two other copies, so it is not a duplicate. Nothing to do.
- Both stories' coder entries record `duplicates: 7 new, 39 known, 4 gone`. `make duplicates` gives the same today, and neither story changed `src/`. The seven predate F0059 and include:
  - the `handed_over` copy in `hand_over`/`acceptance`;
  - the `_system_prompt_file` lines of the two runtimes;
  - vulture's `readme_problems`, at 60 % confidence; the tests use it;
  - three `cost_records` fields.

  They are the baseline's drift from earlier features, for the human to accept or give to a feature that touches those modules. Not proposed here.

## 5 The documentation as a whole

`README.md`, `docs/operator-guide/` and `docs/project-guide/` were read for the checks after the coder, the docs stage and the smoke-test stage. `make documents` is green, but the guides contradict the human's commit:
- `docs/operator-guide/pipeline.md`:
  - The quote of `operator/template/factory/pipeline.yml` (line 69) shows `doing` with `checks: [check]`.
  - The quote of `operator/template/Makefile` (line 76) shows the old `base_ref`.
  - *More than one route* (line 97) quotes the template's `smoke-test` without `checks: [check]`.
  - *The docs route*, step 3 (line 104), says `make check` is reused "only when no document that a test reads has changed", and `make check` now reads no document.
  - The paragraph on kumpel-factory's `not_read` and its YAML block (lines 131-135) still give the old list and say a documents-only change can turn `make check` red.
- `docs/project-guide/README.md:231` speaks of `guides` as future ("Once the human's `guides` project command…", "Until then `make test` still runs every test").

Nobody owned these: the human's commit came after both docs stages, and the documenter of S0001 flagged the first one as waiting for that commit. `docs/project-guide/agents.md:366` (S0002) and `CLAUDE.md` are current, and the project guide's *Stalls* matches the smoke tester's rule. Nothing explains the same thing twice in different ways, and no runnable example fails. One documents-only story repairs all of this (S0003).

## 6 Decisions taken for the human

To accept or revisit:
1. `feature.md` decisions 1 to 4: S0001 lands before the `Makefile` change; the marked guards run in the docs stages and in the coder's `make check guides`; the marker is the project's; no check after the coder, and a red check after the smoke tester is a `check_red` stall that the smoke tester routes.
2. S0001 entry 4: the smoke test and criteria 1 and 2 drop `-q`. Criterion 3 is met by the tester's search, with no test function. The partition is guarded by `tests/guards/test_documents_marker.py`. The completeness of the marked list is not: a new test that reads a document without the marker is caught only by a reviewer.
3. S0001 entry 9: the whole module `tests/operator_scripts/test_operator_site_check.py` is marked. All its operator-script tests now run only in `make guides`, not in `make test`.
4. S0001 entries 8 and 9: the tester's search added `test_license_headers.py`, `test_work_branch_search.py`, `test_root_operator_folders_removed.py` and `test_agent_folder_names.py`, and the human confirmed them. Entry 15 added `test_mount_program_search.py`. Some of these guard code as well as documents: licence headers on every tracked file, the branch-name and mount-program searches over `src/`. They now run only in the docs stages and in the coder's own `make check guides`, not in the factory's `make check` after the smoke tester. Every route to the approval passes a docs stage after the last coder run, so they still gate. This is a consequence to know, not a gap.
5. S0001 entry 9: `test_guide_index_problems.py` and `test_document_tests_write_their_documents.py` stay unmarked.
6. S0001 entry 18: `test_todays_install_guide_gives_no_settings_finding` moved, under the same name, into the new marked module `tests/guards/test_install_guide_settings.py`.
7. The human's commit `77c97b622`, beyond `feature.md`'s list: the `base_ref` fallback is gone in the root, demo and template Makefiles, so a checkout without `origin/develop` now gets an empty base. Plus one line in `docs/runs/2026-11-05-f0052/log.md`.

Earlier tests changed, from the reviewers' entries:
- S0001 (entry 26):
  - `tests/conftest.py`: the Interface's leave (marker registration).
  - The eleven `tests/guards/` modules: the Interface's leave (marker line and `pytest` import).
  - `tests/operator_scripts/test_operator_site_check.py`: the human's answer, entry 9.
  - `tests/shared/domain/test_document_settings.py`: the human's answer, entry 18 (the one test moved out, and its unused imports removed).
- S0002 (entry 9): none; every test change is an addition.

Every change named its leave. No finding.

## 7 The slow checks

The project offers nothing beyond `make check` but `make mutants` (check 3); no image scan and no SBOM.

From `.reports/junit.xml` of this branch's `make check`: 11007 tests, 967 s of test time, 110.3 s wall. The slowest test is new with this feature: `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other` at 20.1 s, which runs three pytest collections. The next ones are the 10 s `ROOMY_LIMIT` tests (`test_podman_timeout_status`, `test_claude_runtime_resume`, `test_document_examples`). The marker test is unmarked, so every `make check` pays for it, on one worker. Worth watching in the measurement run; no story for now. `make guides` takes 9.7 s against its `time_limit` of 2 minutes, and `make documents` 60.0 s.

Disk: at the start record, `/srv/factory/vm` had 11.2 GB free with 1.6 GB used; now 10.6 GB free with 1.5 GB used. `/srv/factory/vm/state` and `/tmp` show the same 0.6 GB drop in free space, and their used space is unchanged: state at 0.0 GB, `/tmp` at 2.1 GB. The three share one pool, and 0.6 GB of it went to something outside these mounts, while the instance's own use shrank. This feature changed only text, so it does not explain the 0.6 GB. Something else on the pool took it, perhaps another instance's dataset or snapshots, and the human may want to look.

## 8 Cost

The stories cost 19 runs, 27.4 min, 143 turns and $7.77. S0001 stands out: 13 runs and $6.02, against S0002's 6 runs and $1.75.
- S0001's first tester run cost $1.39 (272 s, 29 turns), the search over `tests/` for readers of the documents. It still missed two modules, which the reviewer found (entry 15).
- That finding cost a question, three coder runs that changed nothing (entries 17, 20 and 24, $0.68 together), a second tester run and a second review.
- The documenter's 389 s went partly into the folder-README form of `tests/README.md`, which the guard refused twice (entry 28).

S0002 ran the plain route once, with no rework.

Human interventions: 3 questions answered, all of cause `question` and all in S0001. They came at intake (the `-q` of the smoke test, entry 3), at tests (a module outside the leave, entry 8) and at doing (how to mark a single test outside `tests/guards/`, entry 17). They waited 0.1 h together. S0001 needed the human most because its leave covered only `tests/guards/`, and documents were read from two modules outside it.

## Proposed stories

- `F0059-S0003-the-guides-describe-one-full-check-per-story.md`: repairs the operator guide's quotes of the template and of kumpel-factory's definition, its docs-route step, and the project guide's paragraph on the marker. All were made false by the human's commit after the stories, which no docs stage saw. Documents only, so the docs route.

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 036d6fb5079ed6b7c731d9927f1d8fd45a414cdb.
3. factory: started acceptance as vm.
4. acceptance-reviewer: accepted with stories; 1 story proposed

   1. Scope: each scope line has its story, and the human's changes are on `develop` (`77c97b622`). That commit also drops the Makefiles' `base_ref` fallback, which `feature.md` does not list. The measurement run against the 2026-11-08 baseline is still open and is the human's.
   2. Feature smoke test: green.
      - The pipeline definition loads, and the leases fit (42, 47, 48 and 55 of 60 min).
      - Every documenter write path is in `check`'s `not_read`.
      - A documents-only change keeps `check`'s key, so the passed check is reused; a test-file change runs it again.
      - The marker selections give 176 + 11007 = 11183 tests, the whole suite.
      - `make check` and `make guides` (9.7 s) are green, and `make documents` ends with `documents ok`.
   3. Mutation testing: by sweep, not run here.
   4. Noticed:
      - The coder's note on `CLAUDE.md` is fixed by the human.
      - The documenter's stale `docs/operator-guide/pipeline.md:131` is still there, with five more stale places → S0003.
      - The reviewer's note on the loose `"only"` assert is left to the human.
      - The 7 duplicates findings are older than F0059 and are listed for the human.
   5. Documentation: the operator guide's quotes of the template (`doing` checks, `base_ref`, `smoke-test`), its docs-route step 3, its kumpel `not_read` paragraph and `docs/project-guide/README.md:231` contradict the human's commit. They are explanations of linked files that are correct, so this is not a misleading behaviour gap → S0003.
   6. Decisions: the four from `feature.md`, the human's answers in S0001 (entries 4, 9 and 18) and the human's extra `base_ref` change are gathered. The guards that read both code and documents (licence headers, mount and branch searches) now run only in `make guides`. Every earlier test changed under a named leave.
   7. Slow checks: nothing beyond `make check`. The slowest test is the new unmarked `test_documents_marker.py` (20.1 s, three collections). Free space on the pool fell by 0.6 GB while the instance's own use shrank, which this text-only feature does not explain.
   8. Cost: 19 runs, $7.77. S0001 cost $6.02 of it: the tester's search missed two modules, which led to a review finding, a question and three coder runs that changed nothing. The stories had 3 human questions, all in S0001, with 0.1 h waited.
5. factory: done (pull request merged); cost: 1 runs, 7.5 min, 35 turns, 92350 tokens in (1966742 more from cache), 24404 out, $1.62
