---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T07:40:24.891854Z'
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
