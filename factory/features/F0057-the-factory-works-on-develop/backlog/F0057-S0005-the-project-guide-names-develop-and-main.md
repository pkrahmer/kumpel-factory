# The project guide names develop and main

## Description

After F0057-S0002 the factory's code reads and writes `origin/develop` through the constant `WORK_BRANCH`, but the project guide still says `origin/main` about 100 times, in the descriptions of the pipeline, the work items, the watching, the machine, the hosting and the agents. This story corrects the project guide, so that a developer reads the branch the code uses. It changes no code and no test.

## Interface

- The documents: `docs/project-guide/*.md`. Every mention of the factory's working branch says `develop`, or names `WORK_BRANCH` where the page describes the code; a mention of the line of accepted features says `main`.
- `docs/project-guide/shared.md`: `WORK_BRANCH` in `factory.shared.domain.paths` names the working branch, and the guard `tests/guards/test_work_branch_search.py` keeps the name out of every other file.
- The stop reason `main_branch_failing` keeps its name and means the working branch (F0057 decision 6), where a page names it.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in `docs/project-guide/`) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. The tables of the project guide that the document check reads keep their rows. No test changes; the story takes the docs route.

## Acceptance criteria

1. No page of `docs/project-guide/` names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `shared.md` names `WORK_BRANCH` and the guard that keeps the name in one place.
3. `make documents` ends with `documents ok (<seconds> s)`.
4. `make check` stays green.
5. docs: the files of the Interface; a developer reads the branch the code uses.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal
