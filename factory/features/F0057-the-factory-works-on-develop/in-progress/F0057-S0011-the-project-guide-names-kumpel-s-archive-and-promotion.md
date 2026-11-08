---
stage: docs-review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 655
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-review
  started_at: '2026-11-08T07:31:57.866012Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T07:26:50.906694Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T07:26:50.913857Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T07:27:09.848613Z'
  stage: intake
  run: 6a67ad7f02e942f89a1d8eb02fb5f57c
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T07:27:14.558846Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T07:31:51.991752Z'
  stage: docs-only
  run: 1e2b8def3903413d852d050cd43972ec
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T07:31:57.866012Z'
  stage: docs-review
---

# The project guide names Kumpel's archive and promotion


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

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names one document, `docs/project-guide/operator.md`, and seven files. I checked that all seven exist, and that the document has the sections the story cites (*The skill's scripts*, *Tests of the scripts*, *Test modules by script*).
   - Criteria: criteria 1 and 2 are checkable by reading the document: each named script and test file appears, and each script has its refusals and its commit or send. The failing side (what each script refuses) is in criterion 1. Criteria 3 and 4 are the standard checks. No criterion tests behaviour beyond the document, as the story intends.
   - Smoke test: the first command is a runnable grep loop and its `Expect:` is checkable (`done` with no `missing` line). The second runs `factory.entry.check_documents`, which prints `documents ok (<seconds> s)` as its last line. The story runs no pytest, so there is no `-q` problem.
   - Docs criterion: it names what the reader must know (the scripts, their refusals, the commit helper, where the tests and helpers are) and dictates no sentences.
   - Architecture: the Interface changes only a document that the documenter may write, so the story takes the docs route. No code or test changes.
   - Scope: F0057 adds this documentation as a follow-up to its second acceptance. It is not in the feature's "Out of scope" list.
4. factory: started docs-only as vm.
5. documenter: Changed one file, `docs/project-guide/operator.md`, from the code on the branch (`archive-feature.sh`, `promote.sh`, `kumpel-commit.sh`, `start-story.sh`, `tests/support/archive_feature_support.py` and the three test modules' docstrings):
   - *The layout*: the skill's script list now names `archive-feature.sh`, `promote.sh` and the sourced helper `kumpel-commit.sh`.
   - *The skill's scripts*: the usage block lists `archive-feature.sh <feature id>` and `promote.sh <feature id>`. `archive-feature.sh` gets its refusals (story left in `backlog/` or `in-progress/`, no acceptance, last acceptance not in `done/`, last acceptance without `outcome: accepted`, unknown feature, usage exit 2) and what it commits (`<id>: archived`) and pushes. `promote.sh` gets its refusal (feature not archived on `develop`), the pull request it opens or reuses, the `promote` switch, and the merge commit, never a squash or rebase. `kumpel-commit.sh` is named as the one way `archive-feature.sh` and `start-story.sh` commit, under Kumpel's name (decision 7 of F0057).
   - *Tests of the scripts*: `tests/support/archive_feature_support.py` is added to the helper list, with what it holds.
   - *Test modules by script*: a new row maps the three scripts to `test_operator_develop.py`, `test_operator_archive_outcome.py` and `test_operator_promote_reuse.py`.

   Checks run:
   - The story's grep loop printed no `missing` line.
   - `make documents` ended with `documents ok (58.1 s)`.
   - I did not run `make check`: only a document changed.

   Cross-read and found current: the rest of `operator.md` (the site, hosting, job and sanitiser sections), and `docs/decisions.md` for the F0057 entry. `docs/decisions.md` is unchanged, as the criterion says: decisions 1 to 7 are already recorded there.

   No stale text noticed. I wrote no "Why" or "Rejected" lines.

   `check`: check: green
   `secrets`: secrets: green (0.3 s)
   `documents`: documents ok (58.8 s)
6. factory: started docs-review as vm.
