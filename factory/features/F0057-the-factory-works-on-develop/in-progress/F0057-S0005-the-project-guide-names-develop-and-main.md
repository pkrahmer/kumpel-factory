---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 647
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-only
  started_at: '2026-11-08T01:28:29.396342Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T01:28:06.900773Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T01:28:06.908023Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T01:28:24.740341Z'
  stage: intake
  run: 58d18eff216448f4a4d1421409871cb2
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T01:28:29.396342Z'
  stage: docs-only
---

# The project guide names develop and main

## Description

After F0057-S0002 the factory's code reads and writes `origin/develop` through the constant `WORK_BRANCH`, but the project guide still says `origin/main` about 100 times, in the descriptions of the pipeline, the work items, the watching, the machine, the hosting and the agents. This story corrects the project guide, so that a developer reads the branch the code uses. It changes no code and no test.

## Interface

- The documents: `docs/project-guide/*.md`. Every mention of the factory's working branch says `develop`, or names `WORK_BRANCH` where the page describes the code; a mention of the line of accepted features says `main`.
- `docs/project-guide/work.md`, the `paths` table: `WORK_BRANCH` in `factory.shared.domain.paths` names the working branch, and the guard `tests/guards/test_work_branch_search.py` keeps the name out of every other file.
- The stop reason `main_branch_failing` keeps its name and means the working branch (F0057 decision 6), where a page names it.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in `docs/project-guide/`) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. The tables of the project guide that the document check reads keep their rows. No test changes; the story takes the docs route.

## Acceptance criteria

1. No page of `docs/project-guide/` names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `work.md`'s `paths` table names `WORK_BRANCH` and the guard that keeps the name in one place.
3. `make documents` ends with `documents ok (<seconds> s)`.
4. `make check` stays green.
5. docs: the files of the Interface; a developer reads the branch the code uses.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names concrete documents (`docs/project-guide/*.md`), `WORK_BRANCH` in `factory.shared.domain.paths`, and the guard `tests/guards/test_work_branch_search.py`, which exists. The `paths` table in `work.md` (line 394) still shows `main` as the value, so there is something to change. The story changes only documents, so the Interface needs no signatures.
   - Criteria: 1 is checked by the grep script and its quoted output. 2 is checked by reading the `paths` table. 3 and 4 are the make targets. No Interface rule has a failing side that needs a test, because the story only edits documents.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable and does not call pytest, so the `-q` question does not arise. Its `Expect:` line, `documents ok (<seconds> s)`, can be checked against the output.
   - Docs criterion: it names the files and what the reader must know (a developer reads the branch the code uses). It dictates no sentences.
   - Architecture: nothing under `src/` changes. The paths are in `docs/`, which the documenter may write.
   - Scope: this is S0005 of F0057, which lists the project guide in its scope. It keeps `main_branch_failing` as decision 6 says. No code or test change, so the route is docs-only.
4. factory: started docs-only as vm.
