# The operator's documents name develop and main

## Description

After F0057-S0002 and S0003 the factory and Kumpel work on `develop`, and `main` is the protected line of accepted features. The operator's documents still name `main` as the branch the factory works on, about 130 times. This story corrects them, so that an operator knows which branch holds what, how to create `develop` for a new project, how to protect `main`, and how a feature reaches `main`. It changes no code and no test.

## Interface

- The documents: `docs/operator-guide/*.md`, `docs/operator-playbook.md`, the root `README.md` and `operator/README.md`. Every mention of the factory's working branch says `develop`; a mention of the line of accepted features says `main`. `docs/runs/` and the entries of `docs/decisions.md` stay as they are.
- `docs/operator-guide/install.md`: a new project needs `develop`, created from `main`; the preflight names a missing `origin/develop`.
- A section, in the operator guide page the documenter judges right, on protecting `main`: a ruleset that requires a pull request with zero approvals and blocks force pushes and deletion, and why zero (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval). The promotion: after a feature's acceptance, Kumpel archives the feature and promotes `develop` to `main` with a merge commit, behind the switch `promote`; `main` is never fixed directly.
- The stop `main_branch_failing` keeps its name and means the working branch (F0057 decision 6); `docs/operator-guide/stops.md` says so.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in the files above) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. No test changes; the story takes the docs route.

## Acceptance criteria

1. No document of the Interface names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `install.md` tells a new project to create `develop` from `main`.
3. The operator guide tells how to protect `main` and why with zero approvals, and how a feature reaches `main`.
4. `stops.md` says that `main_branch_failing` means the working branch.
5. `make documents` ends with `documents ok (<seconds> s)`.
6. `make check` stays green.
7. docs: the files of the Interface; the reader knows which branch holds what, how to set up and protect them, and how a feature is promoted.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal
