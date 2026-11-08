# The operator's documents on the archive, the promotion and the default branch

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

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
