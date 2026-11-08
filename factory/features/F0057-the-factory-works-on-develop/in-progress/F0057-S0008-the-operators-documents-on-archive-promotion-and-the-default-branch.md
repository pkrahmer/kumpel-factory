---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 651
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T02:43:14.644807Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T02:43:14.652576Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T02:43:33.009475Z'
  stage: intake
  run: 1a36392f8680469c85735dc04423d368
---

# The operator's documents on the archive, the promotion and the default branch


## Description

F0057's acceptance read the operator's documents as a whole and found four gaps that no story owned:
- `docs/operator-playbook.md` still moves a finished feature to `factory/archive/` "by hand (`git mv`)", although `archive-feature.sh` does it as Kumpel (F0057 decision 8). The playbook's acceptance step also says nothing of the promotion that follows.
- `docs/operator-guide/work-items.md` asks the operator to turn off *Automatically delete head branches* for the story's sake only. With the setting on, the merge of a promotion would delete `develop` itself.
- `docs/operator-guide/install.md` does not say which branch is the repository's default. F0057 keeps `main` (*The human's changes*, step 5).
- `install.md` step 1 says the preflight names a missing `origin/develop`. On a remote with only `main` the operator sees the `repository_unavailable` stop "the repository has no develop branch yet".

This story corrects the documents. It changes no code and no test, and it takes the docs route.

## Interface

- The documents: `docs/operator-playbook.md`, `docs/operator-guide/work-items.md` and `docs/operator-guide/install.md`. Nothing else changes.
- The default branch is the human's choice. The story writes what F0057 decided (`main` stays the default; the factory and Kumpel check out `develop` themselves) unless the human says otherwise when refining.

## Acceptance criteria

1. `docs/operator-playbook.md` names `operator/skill/kumpel/scripts/archive-feature.sh` for archiving a finished feature, where it said `git mv` by hand. After the acceptance step it names the promotion (`promote.sh`, the switch `promote`).
2. `docs/operator-guide/work-items.md`, where it asks to clear *Automatically delete head branches*, also says that with the setting on the merge of a promotion deletes `develop`.
3. `docs/operator-guide/install.md` says which branch is the repository's default and that a fresh clone starts there.
4. `docs/operator-guide/install.md` step 1 names what an instance shows on a remote without `develop`: the `repository_unavailable` stop with the detail `the repository has no develop branch yet`, linked to its row in `health.md`.
5. `make documents` ends with `documents ok (<seconds> s)`.
6. `make check` stays green.
7. docs: the files of the Interface. The reader knows how a finished feature is archived and promoted, why the auto-delete setting stays off, which branch is the default, and what a new project without `develop` shows. `docs/decisions.md`: none.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names three concrete documents (`docs/operator-playbook.md`, `docs/operator-guide/work-items.md`, `docs/operator-guide/install.md`), all writable by the documenter; it changes no code. The default branch is stated as `main`, which matches F0057's decisions.
   - Criteria: criteria 1 to 4 are each testable by reading one document (`archive-feature.sh` replaces `git mv` at playbook line 203; the promotion with `promote.sh` and the switch `promote`; the auto-delete warning near work-items.md line 224; the default branch; the stop detail). Both sides of each rule are covered because they are text statements. I checked that the files and anchors exist: `archive-feature.sh` and `promote.sh` are in `operator/skill/kumpel/scripts/`, and health.md line 187 holds the row for `the repository has no develop branch yet`.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable (the module exists). It passes no pytest flags. The Expect line `documents ok (<seconds> s)` can be checked against the output.
   - Docs criterion: it names what the reader must know (archive and promotion, why auto-delete stays off, the default branch, what a project without `develop` shows). It dictates no sentences.
   - Architecture: documents only, so there is no layer or area impact.
   - Scope: it fits F0057's goal of the operator's documents naming `develop` and `main`. It touches no "Out of scope" item. It is a follow-up gap found at acceptance, and it is not a new feature.
