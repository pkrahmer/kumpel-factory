---
stage: docs-review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 655
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-review
  started_at: '2026-11-08T07:37:15.637866Z'
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
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-08T07:32:51.262092Z'
  stage: docs-review
  run: 498b3315ec2f4498bfff2899214e9d37
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T07:32:56.839125Z'
  stage: docs-only
- number: 9
  speaker: documenter
  kind: result
  at: '2026-11-08T07:37:10.645710Z'
  stage: docs-only
  run: 0927e52ada5c462a8cf0a34e672c8ba7
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T07:37:15.637866Z'
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
7. reviewer: Reviewed `git diff develop...HEAD -- README.md docs operator/README.md`, which changes only `docs/project-guide/operator.md`. I checked it against `archive-feature.sh`, `promote.sh`, `kumpel-commit.sh`, `start-story.sh`, `tests/support/archive_feature_support.py`, the docstrings of the three test modules and the decision entry *The factory works on `develop`; `main` holds the accepted features* in `docs/decisions.md`.

   Facts: every claim matches the code on the branch. That covers the refusals and their exit codes, the messages `archive-feature.sh: <id> is not finished: <why>`, `promoted #<n>` and `promotion opened|open: #<n>, for the human to merge`, the title `<id>: promoted to main`, the merge method, Kumpel's identity, and that `archive-feature.sh` and `start-story.sh` are the only scripts that call `kumpel_commit` (no skill script runs `git commit` itself). The four new support-module names exist. Criteria 1 and 2 are met: every file the Interface names is in the document. The documenter reports `documents ok`.

   Writing, judged against `docs/project-guide/style.md`:

   1. `docs/project-guide/operator.md:140`, the last sentence of the `kumpel-commit.sh` bullet: "(F0057 decision 7 in [decisions.md](../decisions.md))" names a feature ID, which breaks style rule 1 (no feature or story IDs). No other line of operator.md has one. Fix: point to the entry by its heading, for example "see *The factory works on `develop`; `main` holds the accepted features* in [decisions.md](../decisions.md)".
   2. `docs/project-guide/operator.md:138`, the second sentence of the `archive-feature.sh` bullet ("It refuses, with exit 1 and ... because the factory books a refused acceptance in `done/` too."): about 70 words in one sentence, against rule 2 (split at about 25 words). Fix: give the exit code and message in one sentence, list the four refusals as their own short sentences or a sub-list, and give the reason for the `outcome: accepted` check in a sentence of its own.
   3. `docs/project-guide/operator.md:139`, the sentence "With the switch `promote` (read through `settings.sh`) on, it merges ... (`open` for a reused one) and merges nothing.": about 45 words and two parentheses, against rule 2 (about 25 words, at most one parenthesis per sentence). Fix: split it into one sentence for the switch on (merge commit, never squash or rebase, prints `promoted #<n>`) and one for the switch off (prints the message, merges nothing). Say where the switch is read in one of them, without a second parenthesis.
   4. `docs/project-guide/operator.md:158`, the `archive_feature_support.py` bullet: three parentheses in one sentence ("(`ACCEPTANCE`, `DONE_FRONT_MATTER`)", "(the files of one feature by path)", "(the remote's file list on a branch)"), against rule 2's limit of one per sentence. Fix: write it as the other helper bullets do, naming each name with what it is and no parentheses, for example "`finished_feature`, the files of one finished feature by path, and `tree`, the files a branch of the remote holds". Split the sentence if needed.
8. factory: started docs-only as vm.
9. documenter: Round 1: fixed the reviewer's four findings in one file, `docs/project-guide/operator.md`, and changed nothing else.
   1. The `kumpel-commit.sh` bullet no longer names a feature id. It points to the decision entry by its heading, *The factory works on `develop`; `main` holds the accepted features*.
   2. The `archive-feature.sh` bullet is split into three bullets. The first covers what it does and commits. The second covers the refusal: the exit code and message, the four reasons, and why `outcome: accepted` is checked, in short sentences. The third covers the other exit codes.
   3. The `promote.sh` bullet is split into three bullets. The first covers the refusal and the pull request it opens or reuses. The second covers the switch on and off, with one sentence for each. The third covers the usage exit. The `settings.sh` note and the `open` message for a reused promotion no longer use parentheses.
   4. The `archive_feature_support.py` bullet has no parentheses. It names `ACCEPTANCE` and `DONE_FRONT_MATTER`, then `finished_feature` and `tree`, each with what it holds.
   `make documents` ended with `documents ok (59.1 s)`. I did not run `make check`, because only a document changed. Nothing stale noticed. No "Why" or "Rejected" lines written.

   `check`: check: green
   `secrets`: secrets: green (0.3 s)
   `documents`: documents ok (58.1 s)
10. factory: started docs-review as vm.
