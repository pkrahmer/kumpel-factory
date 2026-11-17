# The guides catch up with the one layout and name every shared test helper

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

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
