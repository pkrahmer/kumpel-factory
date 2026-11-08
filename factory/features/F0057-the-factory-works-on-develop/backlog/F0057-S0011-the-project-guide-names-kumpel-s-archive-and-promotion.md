# The project guide names Kumpel's archive and promotion

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

F0057 gave Kumpel three new scripts:
- `archive-feature.sh` moves an accepted feature to `factory/archive/`.
- `promote.sh` opens or reuses the promotion of `develop` to `main`.
- `kumpel-commit.sh` makes every Kumpel commit name Kumpel (F0057 decision 7).

It also added three test modules and one test helper. The operator's documents describe the scripts. The project guide for agents who change them does not: `docs/project-guide/operator.md`, *The skill's scripts*, lists only `comment.sh` and `reset-to-tag.sh`, and its *Test modules by script* table and its list of helpers name none of the new files. F0057's second acceptance found the gap. This story writes it into the project guide. It changes no code and no test, and it takes the docs route.

## Interface

- The document: `docs/project-guide/operator.md`. Nothing else changes.
- The files it names, which exist on `develop`:
  - `operator/skill/kumpel/scripts/archive-feature.sh`
  - `operator/skill/kumpel/scripts/promote.sh`
  - `operator/skill/kumpel/scripts/kumpel-commit.sh`
  - `tests/operator_scripts/test_operator_develop.py`
  - `tests/operator_scripts/test_operator_archive_outcome.py`
  - `tests/operator_scripts/test_operator_promote_reuse.py`
  - `tests/support/archive_feature_support.py`

## Acceptance criteria

1. *The skill's scripts* in `docs/project-guide/operator.md` names `scripts/archive-feature.sh <feature id>` and `scripts/promote.sh <feature id>`, each with what it refuses and what it commits or sends. It also names `kumpel-commit.sh` as the one way a Kumpel script commits, under Kumpel's name.
2. *Test modules by script* names `test_operator_develop.py`, `test_operator_archive_outcome.py` and `test_operator_promote_reuse.py` for these scripts. *Tests of the scripts* names `tests/support/archive_feature_support.py` and what it holds.
3. `make documents` ends with `documents ok (<seconds> s)`.
4. `make check` stays green.
5. docs: `docs/project-guide/operator.md`. An agent who changes the archive or the promotion knows the scripts, their refusals, the commit helper, and where their tests and test helpers are. `docs/decisions.md`: none, since the decisions are already recorded.

## Smoke test

```bash
for name in archive-feature.sh promote.sh kumpel-commit.sh test_operator_develop.py test_operator_archive_outcome.py test_operator_promote_reuse.py archive_feature_support.py; do grep -q "$name" docs/project-guide/operator.md || echo "missing $name"; done; echo done
```
Expect: `done`, with no `missing` line before it.

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal
