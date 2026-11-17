---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: self
  stage: intake
  started_at: '2026-11-17T05:10:26.392628Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T05:10:26.386168Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T05:10:26.392628Z'
  stage: intake
---

# The conformance check's documents catch up with the console script and the live part

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

## Description

Two texts about `factory-check-project` fell behind what the feature built. First, `docs/operator-guide/pipeline.md` still says "Until the command is installed as a console script, run it … as `uv run python -m factory.entry.check_project`". The console script has been in `pyproject.toml` since the human's change after S0001. Meanwhile the walk in `docs/operator-guide/start-a-project.md` and the prose of both pages say `factory-check-project`, and every runnable example on both pages runs `python -m factory.entry.check_project`, with no sentence saying why. Second, the decision log records the check as one that "starts no container and runs no project command" (*The conformance check is a command of its own, not a preflight item*). No entry records the lasting choices of the live part `--run`: it works on a temporary clone, builds its image as `<stage image>-check` and never touches the instance's dataset or project image, needs an instance's settings and not a dataset, runs the live points only after a clean static part and prints no point after a failed one, and runs only the make part of the stage's sync script. After this story the operator guide says once, and consistently, that the command is `factory-check-project` and why its examples run the module. The decision log also records the live part. This is a story of documents only; no code, test or file under `operator/` changes.

## Interface

- No module under `src/factory/`, no test and no file under `operator/` changes.
- `docs/operator-guide/pipeline.md`, *Checking a repository before the factory runs it*: the sentence beginning "Until the command is installed as a console script" goes.
- `docs/operator-guide/start-a-project.md` and `docs/operator-guide/pipeline.md`: wherever an example runs `python -m factory.entry.check_project`, one sentence says that this is the same command as `factory-check-project`, and why the example uses the module (the examples run in the factory's own checkout under the document check). The examples stay runnable by `make documents`.
- `docs/decisions.md`: a new entry for the live part, with its date and its story (F0062-S0003), its decision, its reasons and what was rejected, as decisions 12, 13 and 17 of the feature's `feature.md` give them. The S0001 entry keeps its text, and the new entry says that it widens it.

## Acceptance criteria

1. `grep -c 'Until the command is installed' docs/operator-guide/pipeline.md` prints `0`.
2. Every page under `docs/operator-guide/` that has an example running `python -m factory.entry.check_project` has, in the same section, a sentence that names `factory-check-project` as the installed command, and says why the example runs the module.
3. `docs/decisions.md` has an entry whose heading names the live part of the conformance check. It records the temporary clone, the image `<stage image>-check`, that it needs an instance's settings and no dataset, that the live points run only after a clean static part and that no point after a failed one is printed, and that the live sync runs only the make part of the sync script. It also names the S0001 entry as the one it widens.
4. `make documents` ends with `documents ok`, and every example the two pages run still prints what the page shows.
5. `make check` stays green.
6. docs: in `docs/operator-guide/pipeline.md` and `docs/operator-guide/start-a-project.md`, the reader learns that the check's command is `factory-check-project` and why the examples run the module; in `docs/decisions.md`, why the live part works on a clone with an image of its own and runs only after the static part.

## Smoke test

```bash
grep -c 'Until the command is installed' docs/operator-guide/pipeline.md
```
Expect: `0`

```bash
grep -c -e '<stage image>-check' -e 'temporary clone' docs/decisions.md
```
Expect: a number of at least 2.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
