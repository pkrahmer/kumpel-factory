---
stage: docs-only
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 699
comments_read: []
handed_over: null
claim: null
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
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T05:10:46.282495Z'
  stage: intake
  run: 52b57a2d34e7473ba66f471cd715be90
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T05:10:51.191726Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-17T05:15:09.194683Z'
  stage: docs-only
  run: 8af73bcc14a14ad99642663b7a91bc4f
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-17T05:15:14.415382Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-17T05:16:03.676242Z'
  stage: docs-review
  run: fcbc454622334846a4d2d4643d35c7a8
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
3. intake: accepted
   - Interface: only documents change: `docs/operator-guide/pipeline.md` (the "Until the command is installed" sentence at line 219 goes), `docs/operator-guide/start-a-project.md` and `pipeline.md` (one sentence beside the `python -m factory.entry.check_project` examples, at pipeline.md:234 and start-a-project.md:49 and :74), and a new entry in `docs/decisions.md` that widens *The conformance check is a command of its own, not a preflight item* (line 1716). No module, test or `operator/` file changes; the console script exists in `pyproject.toml:19`. Every path is one the documenter may write, so the route is docs-only.
   - Criteria: each can be checked on its own: 1 by grep; 2 per page and section that has a module example; 3 by reading the new entry for each listed point (clone, `<stage image>-check`, settings without a dataset, live points only after a clean static part with nothing printed after a failure, make part of the sync only, widens S0001). The live-part points match decisions 12, 13 and 17 of `feature.md`. 4 is `make documents` (both pages are in `docs/checked-documents.txt`); 5 is `make check`. These are document criteria with no rule that has a refused side.
   - Smoke test: both greps run from the checkout root. Expecting `0` is exact. Expecting "at least 2" can be checked against the count.
   - Docs criterion: it names what the reader must know (the command's name, why the examples run the module, why the live part uses a clone, its own image and the static part first). It dictates no sentences.
   - Architecture: no code. The decision log is the place for lasting reasons and the operator guide for the operator, as CLAUDE.md *Docs* says.
   - Scope: within F0062. It brings the documents of S0001 and S0003 up to date, and none of it is under the feature's Out of scope.
4. factory: started docs-only as self.
5. documenter: Wrote the whole change; only documents changed.

   Files changed:
   - `docs/operator-guide/pipeline.md`, *Checking a repository before the factory runs it*: removed the sentence "Until the command is installed as a console script…". The paragraph that introduces the example now says that `python -m factory.entry.check_project` is the same command as the installed `factory-check-project`, with the same arguments. It also says why the example uses the module: the document check runs the page's examples in the factory's own checkout, where the module can be reached whether or not the console script is on the path.
   - `docs/operator-guide/start-a-project.md`, *The walk in one example*: added the same sentence to the paragraph before the two module examples. It points back to steps 7 and 8, which name `factory-check-project`.
   - `docs/decisions.md`: added a new entry, *The live part of the conformance check works on a clone with an image of its own* (2026-11-17, F0062-S0003), right after the S0001 entry. It records:
     - the three live points;
     - the temporary clone of `HEAD`, never the dataset;
     - the image `<stage image>-check`, never the project image;
     - that it needs an instance's settings and no dataset;
     - that live points run only after a clean static part, and none is printed after a failed one;
     - that the live sync runs only the make part of the sync script;
     - that the agent home serves only the point `agents`;
     - that it widens *The conformance check is a command of its own, not a preflight item*, whose text is unchanged.
     The "Why" (it can run beside a working instance and for another repository) and the "Rejected" line (running on the instance's dataset or project image) come from decision 12. I put the clone and the image on separate lines so that the smoke test's `grep -c` counts 2.

   Checks: `grep -c 'Until the command is installed' docs/operator-guide/pipeline.md` prints 0. The smoke grep on `docs/decisions.md` prints 2. `make documents` ends `documents ok (46.6 s)`; both pages' check_project examples ran and print what the pages show. I did not run `make check`, because only documents changed (the factory runs the stage's checks).

   Open for the reviewer: criterion 6 asks the decision log to say why the live part runs only after the static part. Decision 13 and the story state the rule but give no reason. Following the documenter's lesson, I wrote no reason of my own; the entry has only the "When it runs" rule. If a reason is wanted, the human should word it.

   Cross-read and found current: the rest of the *Checking a repository* section and its *Reference* in `docs/operator-guide/pipeline.md` (the live part, the faults, the usage and the exit status agree with decisions 12, 13 and 17); steps 7 and 8 and *The live check on the machine* in `start-a-project.md`; and the S0001, S0002, S0004, S0005, S0007 and S0008 entries in `docs/decisions.md`. I saw no unrelated stale text.

   `check`: check: green (not run again: passed on tree 115bc87f3451 at 2026-11-17T04:56:37Z)
   `guides`: guides: green (9.3 s)
   `secrets`: secrets: green (1.4 s)
   `documents`: documents ok (47.0 s)
6. factory: started docs-review as self.
7. reviewer: Reviewed `git diff develop...HEAD -- README.md docs operator/README.md`. I checked the documents against `src/factory/entry/check_project.py`, `src/factory/machine/application/project_run.py`, `src/factory/pipeline/application/project_check.py`, `pyproject.toml:19` and decisions 12, 13 and 17 of the feature's `feature.md`. I judged the writing by `docs/project-guide/style.md`.

   What the code confirms:
   - The six static points (pipeline, makefile, stage file, agents, write paths, forms) and the three live ones.
   - The temporary clone of `HEAD`: `ProjectRun.run`, `tempfile.mkdtemp`, `_clone`.
   - The image tag `<stage image>-check`: `CHECK_TAG_SUFFIX`, `check_image_tag`.
   - `--run` needs the settings and no dataset: `main` reads `read_environment_settings` and calls `build_project_run`.
   - The live points run only after a clean static part, and nothing is printed after a failed one: `is_ready(points)` in `main`, the early returns in `_run_in`.
   - The live sync runs only the make part, from the public constants `SYNC_MAKE` and `NAMED_SYNC_MAKE`.
   - The agent home serves only the point `agents`, through `build_agent_definitions`.
   - The S0001 entry keeps its text.

   Criteria 1 and 2 are met, and so are points 1 to 5 of criterion 3. Criterion 6 is met for the operator guide.

   Findings:
   1. `docs/decisions.md`, new entry *The live part of the conformance check works on a clone with an image of its own*: criterion 6 asks the log to say why the live part runs only after the static part, and the entry gives the rule ("When it runs") but no reason. The code has one. `src/factory/entry/check_project.py` `_live_points` reads the pipeline definition on the comment "The static part has just read the definition at the same commit, so it is there and valid". `ProjectRun._sync` and `_check` take the named makefile (`definition.make_file`) and the time limits (`command_time_limit`) from that definition. Fix: add a "Why after the static part" line saying that the live points run with the pipeline definition's makefile and time limits, which only a clean static part has read and validated. If the documenter does not want to word a reason from the code, end with `question` to the human instead.
   2. `docs/operator-guide/pipeline.md:223`, the added sentence "The example runs `python -m factory.entry.check_project`, which is the same command … on the path." is about 50 words, against style rule 2 (split a sentence of more than about 25 words). Fix: split it in two, one sentence that names `factory-check-project` as the same command with the same arguments, and one that says why the example runs the module.
   3. `docs/operator-guide/start-a-project.md:38`, the added sentence "Its two checks run `python -m factory.entry.check_project`, which is the same command … on the path." is about 55 words, against the same style rule 2. Fix: split it the same way as finding 2.
