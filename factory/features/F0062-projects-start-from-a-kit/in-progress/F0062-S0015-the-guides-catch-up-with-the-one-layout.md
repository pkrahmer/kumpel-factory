---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 708
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T07:46:56.151183Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T07:46:56.158292Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T07:47:17.345058Z'
  stage: intake
  run: 58a833bd0df64c388bf4065d62ab95fd
---

# The guides catch up with the one layout and name every shared test helper


## Description

S0013 gave every project one layout, with the factory's makefile at `factory/Makefile`, but two sentences outside the pages its docs criterion named still describe the layouts before it. The project guide's `docs/project-guide/operator.md` says the packs' README tells how kit and pack are assembled "at the root or, for an existing repository, with `make_file: factory/Makefile`", and the operator guide's `docs/operator-guide/install.md`, *The project's make targets*, says the project defines its targets "in the Makefile at the root of its checkout", though the kit's definitions name `factory/Makefile`. Separately, the project guide's index `docs/project-guide/README.md` says that it names every module of `tests/support/`, and eight are missing from it, four of them this feature's (`kit_support.py`, `make_file_support.py`, `project_check_support.py`, `project_run_support.py`) and four older (`archive_feature_support.py`, `bill_cache_support.py`, `first_message_support.py`, `shared_rules_support.py`); S0013's documenter noticed the first. After this story the three pages agree with the one layout and the index keeps its promise. No code, no test and no file under `operator/` changes.

## Interface

- No module under `src/factory/`, no test and no file under `operator/` changes.
- `docs/project-guide/operator.md`, the bullet on `operator/packs/`: the assembly is described as the one way (every pack file but `CLAUDE.sections.md` and `TRAPS.md` into the project's `factory/`), without "at the root or, for an existing repository".
- `docs/operator-guide/install.md`, *The project's make targets*: the targets are defined in the makefile the pipeline definition names with `make_file` (`factory/Makefile` in a project assembled from the kit), else in the `Makefile` at the root of the checkout, with a link to *Name the makefile* in `pipeline.md`.
- `docs/project-guide/README.md`, the list of the modules of `tests/support/` that no earlier list holds: one bullet for each of the eight modules named in the Description, each with what it holds, in the style of the bullets around it.

## Acceptance criteria

1. `grep -c 'at the root or, for an existing repository' docs/project-guide/operator.md` prints `0`.
2. `grep -c 'Makefile at the root of its checkout' docs/operator-guide/install.md` prints `0`, and *The project's make targets* names `make_file` and `factory/Makefile`.
3. For every file `tests/support/<name>.py` but `__init__.py`, `docs/project-guide/README.md` holds the text `tests/support/<name>.py`.
4. `make documents` ends with `documents ok`, and `make guides` is green.
5. `make check` stays green.
6. docs: in `docs/project-guide/operator.md` and `docs/operator-guide/install.md`, the reader learns that a project assembled from the kit has its make targets in `factory/Makefile`, which the pipeline definition names, and that there is one way to assemble kit and pack; in `docs/project-guide/README.md`, what each of the eight shared test helpers holds.

## Smoke test

```bash
grep -c 'at the root or, for an existing repository' docs/project-guide/operator.md; grep -c 'Makefile at the root of its checkout' docs/operator-guide/install.md
```
Expect: `0`, then `0`.

```bash
for f in tests/support/*.py; do b=$(basename "$f"); [ "$b" = __init__.py ] || grep -q "tests/support/$b" docs/project-guide/README.md || echo "missing: $b"; done; echo done
```
Expect: the single line `done`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: it names three documents and the exact place in each: the `operator/packs/` bullet of `docs/project-guide/operator.md` (line 25 now holds "at the root or, for an existing repository"), *The project's make targets* in `docs/operator-guide/install.md` (line 230 now holds "Makefile at the root of its checkout"), and the list of `tests/support/` modules in `docs/project-guide/README.md`. It also states what stays unchanged: no `src/`, no test, nothing under `operator/`. *Name the makefile* exists in `docs/operator-guide/pipeline.md` (line 93), so the link has a target. I checked that the eight modules the Description names are the ones the index misses today, and they are.
   - Criteria: each one can be checked mechanically without further decisions. 1 and 2 are greps that must print `0`, and 2 also names `make_file` and `factory/Makefile`. 3 checks every support module against the index. 4 is `make documents` and `make guides`, and 5 is `make check`. Every Interface line has a criterion: removing the old wording (1 and 2), the new targets wording (2), the eight bullets (3). The "what it holds" part of each bullet is a matter of content, and the docs criterion covers it. The Interface states no rule with a failing side.
   - Smoke test: both blocks run from the checkout root as written. Each `Expect:` can be checked against the output (`0` then `0`; the single line `done`). Run today, the second block prints exactly the eight `missing` lines, so it tells the state before the story from the state after it.
   - Docs criterion: it says what the reader must know (a kit project's make targets live in `factory/Makefile`, which the pipeline definition names; there is one way to assemble kit and pack; what each of the eight helpers holds) and dictates no sentences.
   - Architecture: the story changes documents only. The documenter keeps the project guide and the operator guide (CLAUDE.md, *Docs*), and no code or layer is touched.
   - Scope: within F0062's "The guide for a fresh start and for a brownfield repository". It brings the pages into line with S0013's one layout and does not touch the feature's "Out of scope". Every path it changes is under `docs/`, which the documenter may write, so the route is `docs-only`.
