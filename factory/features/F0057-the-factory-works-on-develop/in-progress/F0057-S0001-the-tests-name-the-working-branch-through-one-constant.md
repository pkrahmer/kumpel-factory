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
  started_at: '2026-11-07T21:54:26.908741Z'
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
2. The guard of the Interface passes on the repository and fails on a file that holds `origin/main` (rows of one test, the failing row on a file the test writes).
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
