---
stage: smoke-test
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 656
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: smoke-test
  started_at: '2026-11-08T07:51:32.237920Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T07:40:24.884561Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T07:40:24.891854Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T07:40:44.776627Z'
  stage: intake
  run: ff116cb5025d4343881bf03d5efd0df5
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T07:40:49.422192Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T07:41:26.490229Z'
  stage: tests
  run: 67a05ae60de84b59b4d1460138224dd0
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T07:41:31.366834Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-08T07:46:08.759406Z'
  stage: doing
  run: 750cb135090d41f78649c761c1bf9a68
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T07:46:13.669329Z'
  stage: review
- number: 9
  speaker: reviewer
  kind: result
  at: '2026-11-08T07:47:03.475157Z'
  stage: review
  run: 1c8fab28ef7d4a20a714a76ae437d393
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T07:47:08.590717Z'
  stage: docs
- number: 11
  speaker: documenter
  kind: result
  at: '2026-11-08T07:51:27.158134Z'
  stage: docs
  run: a5aef1fb37744ba58d21c3b98d980ed9
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T07:51:32.237920Z'
  stage: smoke-test
---

# The working branch's remote ref is one constant


## Description

Sixteen places under `src/factory/` build `origin/develop` from `REMOTE` and `WORK_BRANCH`:
- **Nine private constants with the same text:** `_WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` in `tick`, `scheduler`, `preflight`, `work_items`, `acceptance`, `acceptance_reading`, `wiring`, `watcher` and `opening`.
- **Two public constants with the same value:** `FORM_REF` in `factory.pipeline.application.task` and `PIPELINE_REF` in `factory.pipeline.application.pipeline_loading`.
- **Five inline spellings:** in `handlers/hand_over.py`, in `stops.py` (twice), in `stage.py` and in `watching/application/costs.py`.

F0057-S0009's coder noticed the copies, and F0057's second acceptance collected them. This story puts the ref in one constant, `WORK_REF`, in `factory.shared.domain.paths`, beside `REMOTE` and `WORK_BRANCH`. Every one of the sixteen places then uses it. The behaviour does not change.

What stays as it is:
- `PIPELINE_REF` and `FORM_REF` keep their names, since tests and the project guide use them. Each is set to `WORK_REF`.
- `REMOTE`, `WORK_BRANCH` and `f"{REMOTE}/{snapshot.branch}"` for a work item's branch.

## Interface

```python
# factory.shared.domain.paths (domain)
WORK_REF = f"{REMOTE}/{WORK_BRANCH}"
```

- `WORK_REF` is `"origin/develop"`.
- The private `_WORK_REF` constants of the nine modules are gone. Each module imports `WORK_REF` from `factory.shared.domain.paths` instead.
- `factory.pipeline.application.task.FORM_REF` and `factory.pipeline.application.pipeline_loading.PIPELINE_REF` are `WORK_REF`.
- The five inline spellings use `WORK_REF`.
- The text `{REMOTE}/{WORK_BRANCH}` appears in exactly one `.py` file under `src/factory/`: `src/factory/shared/domain/paths.py`.
- Tests:
  - A new module `tests/shared/domain/test_paths_work_ref.py`.
  - A new guard `tests/guards/test_work_ref_search.py`, which reads `src/factory/` as `tests/guards/test_work_branch_search.py` does.
  - No earlier test changes.

## Acceptance criteria

1. `from factory.shared.domain.paths import WORK_REF` gives `"origin/develop"`, and `PIPELINE_REF` and `FORM_REF` are equal to it (rows of one test).
2. The new guard passes on the repository. It fails on a file it writes under its scope (outside `shared/domain/paths.py`) that holds `f"{REMOTE}/{WORK_BRANCH}"`, and on one that holds `_WORK_REF = f"{REMOTE}/{WORK_BRANCH}"`. It passes on a file that imports and uses `WORK_REF`, and on one that holds `f"{REMOTE}/{snapshot.branch}"` (rows of one test).
3. Every earlier test passes unchanged.
4. `make check` stays green.
5. docs: `docs/project-guide/work.md` (the `paths` table) names `WORK_REF` and says the code builds the working branch's remote ref only through it. The other project-guide files that name `_WORK_REF`, if any, follow. `docs/decisions.md`: none, a refactoring without a lasting choice.

## Smoke test

```bash
grep -rn '{REMOTE}/{WORK_BRANCH}' src/factory --include=*.py | wc -l
```
Expect: `1`

```bash
uv run python -c "from factory.shared.domain.paths import WORK_REF; print(WORK_REF)"
```
Expect: `origin/develop`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names the concrete module `factory.shared.domain.paths` and the one constant `WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` (value `origin/develop`). paths.py already holds `REMOTE` and `WORK_BRANCH`. I counted the 16 current spellings in `src/factory`: 9 `_WORK_REF`, `FORM_REF`, `PIPELINE_REF` and 5 inline (hand_over, stops twice, stage, costs). That matches the Description.
   - Criteria: (1) the value, `PIPELINE_REF` and `FORM_REF` are rows of one test. (2) The guard has fail rows (the inline form, and `_WORK_REF = ...`) and pass rows (a file that uses `WORK_REF`, and `f"{REMOTE}/{snapshot.branch}"`). It reads `src/factory` like the existing `tests/guards/test_work_branch_search.py`, which exists. (3) is the unchanged earlier tests. The failing side of the single-spelling rule is covered by the guard's fail rows.
   - Smoke test: both commands are runnable and neither uses pytest. Today the grep prints 16, and it will print 1 once paths.py holds the one line. Each `Expect:` line is a single checkable value.
   - Docs criterion: it names `docs/project-guide/work.md` (the `paths` table) and what the reader must know, namely that `WORK_REF` is the only way the code builds the working branch's remote ref. It dictates no sentences, and it says no decision entry is needed.
   - Architecture: the constant sits in the `shared` domain layer, which every area may import. That fits the layer rules. The change is a refactoring and behaviour stays the same.
   - Scope: it is a behaviour-free cleanup that F0057's acceptance collected, within the feature's one-constant goal. Nothing in the feature's Out of scope is touched. No earlier test changes. Route: `tests`.
4. factory: started tests as vm.
5. tester: I wrote the tests for the criteria that need tests. They fail now, as they should, because the code is not changed yet.

   - criterion 1: tests/shared/domain/test_paths_work_ref.py::test_the_working_branch_s_remote_ref_is_origin_develop. It has three rows: `work-ref`, `pipeline-ref` and `form-ref`. Each row expects `"origin/develop"`.
   - criterion 2, the repository: tests/guards/test_work_ref_search.py::test_no_source_file_but_the_paths_module_builds_the_working_branch_s_remote_ref
   - criterion 2, the rows: tests/guards/test_work_ref_search.py::test_the_search_finds_each_file_that_builds_the_working_branch_s_remote_ref
     - Rows that must be found: `inline` (`f"{REMOTE}/{WORK_BRANCH}"`) and `private-constant` (`_WORK_REF = ...`, in a nested area module).
     - Rows that must pass: `imports-work-ref`, `work-item-branch` (`f"{REMOTE}/{snapshot.branch}"`) and `the-paths-module`.
     - `the-paths-module` checks the guard's one allowed file, `shared/domain/paths.py`. That file is the boundary of the scope the Interface states.
   - criteria 3, 4 and 5: no new test. Criterion 3 is the existing suite run unchanged, 4 is `make check`, and 5 is the docs stage's work.

   The guard reads every `.py` file under `src/factory/` except `__pycache__` folders, in the same way as `tests/guards/test_work_branch_search.py`. It reports each file that holds the text `{REMOTE}/{WORK_BRANCH}`, other than `src/factory/shared/domain/paths.py`.

   I ran the two new files once:
   - `work-ref` fails because `WORK_REF` is not in `factory.shared.domain.paths` yet.
   - The repository guard fails because the sixteen spellings are still in the source.
   - The other rows already pass: `PIPELINE_REF` and `FORM_REF` already equal `"origin/develop"`, and the guard's rows test the search on files it writes.
   - Every module imported; nothing failed to import.

   `make lint` is green. I skipped the type check as the stage says: it will report the missing `paths.WORK_REF` until the coder adds it.

   Files created: tests/shared/domain/test_paths_work_ref.py and tests/guards/test_work_ref_search.py. No earlier test changed.

   `lint`: lint: green (0.2 s)
6. factory: started doing as vm.
7. coder: I added `WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` to `src/factory/shared/domain/paths.py`, beside `REMOTE` and `WORK_BRANCH`. All sixteen spellings now use it:
   - The nine private `_WORK_REF` constants are removed, and each module imports `WORK_REF` instead. The modules are `pipeline/application/{tick,scheduler}.py`, `machine/application/preflight.py`, `work/application/{work_items,acceptance,acceptance_reading}.py`, `entry/wiring.py`, `watching/application/watcher.py` and `hosting/application/opening.py`.
   - `FORM_REF` in `pipeline/application/task.py` and `PIPELINE_REF` in `pipeline/application/pipeline_loading.py` are now `= WORK_REF`.
   - The five inline spellings now use `WORK_REF`: `pipeline/application/handlers/hand_over.py`, `pipeline/application/stops.py` (both places), `pipeline/application/stage.py` and `watching/application/costs.py`.
   - I removed imports of `REMOTE` and `WORK_BRANCH` wherever they were no longer used. Modules that still need them for `f"{REMOTE}/{snapshot.branch}"` or `checkout(WORK_BRANCH, ...)` keep them.

   `grep -rn '{REMOTE}/{WORK_BRANCH}' src/factory --include=*.py` now finds only the one line in `paths.py`. `make check` is green: coverage is 99.22 %, the run ends with `check: green`, and the two new test modules pass without any test changed.

   Main choice: `PIPELINE_REF` and `FORM_REF` stay as public names set to `WORK_REF`, as the Description asks. The alternative was to drop them and import `WORK_REF` wherever they are used. I rejected it because tests and the project guide name them.

   Refactor pass: I read the whole diff. It is a mechanical substitution, so I found nothing to change. The only extra step was undoing a multi-line import that the tooling had produced in `costs.py`, which keeps that diff to one line.

   The journal did not change the meaning of the task.

   Noticed, not touched:
   - The project guide may still name `_WORK_REF`. That is the docs stage's work under criterion 5.

   `check`: check: green
   `duplicates`: duplicates: 6 new, 39 known, 4 gone
8. factory: started review as vm.
9. reviewer: no findings

   What I checked (round 0, scope `git diff develop...HEAD -- . ':!factory'` plus the work item):
   - Criterion 1: `tests/shared/domain/test_paths_work_ref.py::test_the_working_branch_s_remote_ref_is_origin_develop` has the rows `work-ref`, `pipeline-ref` and `form-ref` in one parametrized test, and each expects `"origin/develop"`. `src/factory/shared/domain/paths.py:14` adds `WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` beside `REMOTE` and `WORK_BRANCH`. `PIPELINE_REF` in `pipeline_loading.py` and `FORM_REF` in `task.py` are now `= WORK_REF`.
   - Criterion 2: `tests/guards/test_work_ref_search.py` runs the guard on the repository. One parametrized test covers both sides of the rule:
     - The fail rows are `inline` and `private-constant`.
     - The pass rows are `imports-work-ref` and `work-item-branch`, plus `the-paths-module` for the one allowed file, which tests the "exactly one file" limit from the other side.
     - The scan reads `src/factory/**/*.py` as `test_work_branch_search.py` does, as the Interface asks.
     - I compared it with `tests/support/search_support.modules_matching`. That helper leaves files out by bare name, not by path, and is built for `tests/`, so the new scan is not a copy of it.
   - Criterion 3: the diff adds only test files (status `A`), so no earlier test was touched. The coder's journal entry 7 reports `check: green`.
   - Source: I read every hunk of the 16 modules. Each of the nine `_WORK_REF` constants and each of the five inline spellings became `WORK_REF`, with no other change in behaviour. A work item's branch keeps `f"{REMOTE}/{snapshot.branch}"`. Each module still imports `REMOTE` or `WORK_BRANCH` only where it still uses it (`hand_over`, `stops` and `costs` for `REMOTE`; `preflight`, `scheduler`, `tick`, `stage` and `stops` for `WORK_BRANCH`). `grep` finds `{REMOTE}/{WORK_BRANCH}` only in `paths.py`, and no `_WORK_REF` is left under `src/factory`.
   - Architecture: the constant sits in the `shared` domain layer, which may be imported from any layer above it. There is no new dependency and no new interface.
   - Security: no new markers, secrets, shell or string-built commands.
   - Quality: names, imports and docstrings are fine, and there is no dead code. `make duplicates` reports 6 new findings, but this change only removes duplication.
   - Work item hygiene: the journal gives the main choice (keep `PIPELINE_REF` and `FORM_REF` as aliases) and the alternative it rejected. The Description matches what was built. Docs criterion 5 still holds: `docs/project-guide/work.md:394-396` (the `paths` table) does not name `WORK_REF` yet, and the documenter adds it next. No project-guide file names `_WORK_REF`.
   - Documents: the diff changes none.

   Earlier tests: none. The diff changes, renames or deletes no test file that `develop` already holds.
10. factory: started docs as vm.
11. documenter: Files changed:
    - `docs/project-guide/work.md`: the `paths` table has a new row for `WORK_REF` (`origin/develop`, built from `REMOTE` and `WORK_BRANCH`). A new bullet says the code builds the working branch's remote ref only through `WORK_REF`. It also says the text `f"{REMOTE}/{WORK_BRANCH}"` stands in `paths.py` alone, and that `tests/guards/test_work_ref_search.py` enforces this. It says `PIPELINE_REF` and `FORM_REF` are set to `WORK_REF`, and that a work item's branch still uses `f"{REMOTE}/{snapshot.branch}"`.

    I read the code on the branch first: `paths.py:14`, `task.py` and `pipeline_loading.py`. I then ran `make documents`, which ended with `documents ok (58.9 s)`. I did not run `make check`, because I changed only a document.

    Documents cross-read and found current:
    - A grep of `README.md` and `docs/` finds no `_WORK_REF`.
    - The `origin/develop` literals in `watching.md`, `pipeline.md` and `hosting.md` are prose about behaviour that did not change.
    - `docs/decisions.md` needs no entry, as the criterion says. I wrote no "Why" or "Rejected" line.

    Stale text I noticed and did not touch: none. Findings for the coder: none.

    `check`: check: green
    `secrets`: secrets: green (0.8 s)
    `documents`: documents ok (58.6 s)
12. factory: started smoke-test as vm.
