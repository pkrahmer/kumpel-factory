---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 656
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: doing
  started_at: '2026-11-08T07:41:31.366834Z'
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
