# The guides name the folder READMEs as they are now

<!-- proposed by feature acceptance of 2026-11-07; refine before starting -->

## Description

Since the feature's first acceptance, the human has written `factory/README.md`, `factory/features/README.md` and `docs/runs/README.md`, and F0055-S0008 made the guard fail when a listed README has no file. Four sentences of the documents still describe the time before that. The root `README.md`, `## The folders`, gives `factory/` no link to its README, although F0055-S0005's criterion said the section links each folder's README that exists. `docs/README.md` gives `runs/` no link to `runs/README.md`. `docs/project-guide/style.md`, *Folder READMEs*, says the guard checks each listed README "that exists", which was the skip that S0008 removed. `docs/project-guide/shared.md`, *The folder READMEs*, says `FOLDER_READMES` lists "every folder README of the repository, 22 in all". The human's three READMEs, `planning/README.md`, `demo/README.md` and `operator/README.md` are folder READMEs outside that list. The human kept their own three off the list on purpose (`factory/features/` holds feature folders that come and go, and that its README names by kind, not by name). This story corrects these four places. It changes no code, no test, no README of the human's and nothing on `FOLDER_READMES`. Whether the human's READMEs join the list is the human's decision, and this story leaves it open.

## Interface

- No module changes, and no test changes. The story takes the docs route.
- `README.md`, `## The folders`: the `factory/` line ends with a link to `factory/README.md`, as the other lines link theirs.
- `docs/README.md`: the `runs/` subfolder line links `runs/README.md`. It stays one sentence of at most 25 words, so the guard over `docs/README.md` stays green.
- `docs/project-guide/style.md`, *Folder READMEs*: the guard checks every README on the list, and a listed README with no file is a finding.
- `docs/project-guide/shared.md`, *The folder READMEs*: `FOLDER_READMES` holds the 22 READMEs that the guard and the document check read. The folder READMEs outside it are named (the human's `factory/`, `factory/features/`, `docs/runs/` and `planning/`, plus `demo/README.md` and `operator/README.md`, each in its own form), together with the reason the human's stay off the list.

## Acceptance criteria

1. `README.md`, `## The folders`: the `factory/` line links `factory/README.md`. `grep -c '](factory/README.md)' README.md` gives `1`.
2. `docs/README.md`: the `runs/` line links `runs/README.md`. `grep -c '](runs/README.md)' docs/README.md` gives `1`. The guard `tests/guards/test_folder_readmes.py` passes for `docs/README.md`.
3. `docs/project-guide/style.md`, *Folder READMEs*, no longer says the guard checks only the READMEs that exist. `grep -c 'each one that exists' docs/project-guide/style.md` gives `0`.
4. `docs/project-guide/shared.md`, *The folder READMEs*, no longer calls the 22 paths every folder README of the repository. `grep -c 'every folder README of the repository' docs/project-guide/shared.md` gives `0`. The section names the folder READMEs outside the list.
5. `make documents` ends with `documents ok (<seconds> s)`.
6. `make check` stays green.
7. docs: `README.md` and `docs/README.md`: a newcomer finds the READMEs of `factory/` and `docs/runs/` from the folder lists. `docs/project-guide/style.md` and `docs/project-guide/shared.md`: an agent learns that a listed README with no file fails the guard, and which folder READMEs are outside `FOLDER_READMES` and why. `docs/decisions.md`: none, because no new decision is made.

## Smoke test

```bash
grep -c '](factory/README.md)' README.md; grep -c '](runs/README.md)' docs/README.md
```
Expect: `1` and `1`, on two lines.

```bash
grep -c 'each one that exists' docs/project-guide/style.md; grep -c 'every folder README of the repository' docs/project-guide/shared.md
```
Expect: `0` and `0`, on two lines.

```bash
uv run pytest tests/guards/test_folder_readmes.py 2>&1 | tail -1 | grep -c failed
```
Expect: `0`

## Journal
